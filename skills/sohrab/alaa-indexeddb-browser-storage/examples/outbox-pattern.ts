import { requestToPromise, txDone } from './idb-core';

export interface OutboxItem<TBody = unknown> {
  id: string;
  accountKey: string;
  endpointKey: string;
  body: TBody;
  idempotencyKey: string;
  status: 'pending' | 'inflight' | 'done' | 'failed' | 'dead';
  priority: 'critical' | 'normal' | 'low';
  attempts: number;
  nextAttemptAt: string;
  createdAt: string;
  updatedAt: string;
  lastError?: string;
}

export async function enqueueOutboxItem<TBody>(db: IDBDatabase, item: OutboxItem<TBody>): Promise<void> {
  const tx = db.transaction('wa_outbox', 'readwrite');
  tx.objectStore('wa_outbox').put(item);
  await txDone(tx);
}

export async function claimNextOutboxBatch(db: IDBDatabase, nowIso: string, limit = 25): Promise<OutboxItem[]> {
  const tx = db.transaction('wa_outbox', 'readwrite');
  const store = tx.objectStore('wa_outbox');
  const index = store.index('byStatusRetryAt');
  const range = IDBKeyRange.bound(['pending', ''], ['pending', nowIso]);
  const items: OutboxItem[] = [];

  await new Promise<void>((resolve, reject) => {
    const request = index.openCursor(range);
    request.onerror = () => reject(request.error ?? new Error('Outbox cursor failed'));
    request.onsuccess = () => {
      const cursor = request.result;
      if (!cursor || items.length >= limit) {
        resolve();
        return;
      }
      const item = cursor.value as OutboxItem;
      const claimed: OutboxItem = {
        ...item,
        status: 'inflight',
        updatedAt: new Date().toISOString(),
      };
      cursor.update(claimed);
      items.push(claimed);
      cursor.continue();
    };
  });

  await txDone(tx);
  return items;
}

export async function markOutboxSuccess(db: IDBDatabase, id: string): Promise<void> {
  const tx = db.transaction('wa_outbox', 'readwrite');
  const store = tx.objectStore('wa_outbox');
  const item = await requestToPromise(store.get(id)) as OutboxItem | undefined;
  if (item) {
    store.put({ ...item, status: 'done', updatedAt: new Date().toISOString() });
  }
  await txDone(tx);
}

export async function markOutboxRetry(db: IDBDatabase, id: string, errorName: string): Promise<void> {
  const tx = db.transaction('wa_outbox', 'readwrite');
  const store = tx.objectStore('wa_outbox');
  const item = await requestToPromise(store.get(id)) as OutboxItem | undefined;
  if (item) {
    const attempts = item.attempts + 1;
    const delayMs = Math.min(60 * 60 * 1000, Math.pow(2, attempts) * 1000 + Math.floor(Math.random() * 1000));
    const nextAttemptAt = new Date(Date.now() + delayMs).toISOString();
    store.put({
      ...item,
      attempts,
      status: attempts >= 10 ? 'dead' : 'pending',
      nextAttemptAt,
      lastError: errorName,
      updatedAt: new Date().toISOString(),
    });
  }
  await txDone(tx);
}

export async function flushOutbox(options: {
  db: IDBDatabase;
  now?: Date;
  send: (item: OutboxItem, signal?: AbortSignal) => Promise<Response>;
  signal?: AbortSignal;
}): Promise<{ sent: number; retried: number; dead: number }> {
  const batch = await claimNextOutboxBatch(options.db, (options.now ?? new Date()).toISOString());
  let sent = 0;
  let retried = 0;
  let dead = 0;

  for (const item of batch) {
    if (options.signal?.aborted) break;
    try {
      const response = await options.send(item, options.signal);
      if (response.ok) {
        await markOutboxSuccess(options.db, item.id);
        sent++;
      } else if (response.status === 401 || response.status === 403) {
        await markOutboxRetry(options.db, item.id, `http_${response.status}`);
        dead++;
      } else {
        await markOutboxRetry(options.db, item.id, `http_${response.status}`);
        retried++;
      }
    } catch (error) {
      await markOutboxRetry(options.db, item.id, error instanceof Error ? error.name : 'network_error');
      retried++;
    }
  }

  return { sent, retried, dead };
}
