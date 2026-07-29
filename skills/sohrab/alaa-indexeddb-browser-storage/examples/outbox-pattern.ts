/**
 * The browser-side outbox. references/71-browser-outbox.md
 *
 * The state set is deliberately NOT the server-side one. /alaa-async-messaging
 * ($alaa-async-messaging) owns pending|claimed|published, where a claim releases
 * itself by transaction rollback. Here a claim releases only via the reaper in
 * ./outbox-reaper.ts, because the claiming context can simply cease to exist.
 *
 * Retry doctrine — backoff, jitter, caps, timeouts — is /alaa-reliability-sla
 * ($alaa-reliability-sla). This file takes a policy; it embeds no literal.
 */
import { txDone } from './idb-core';

export type BrowserOutboxStatus = 'queued' | 'sending' | 'sent' | 'conflict' | 'abandoned';

export interface BrowserOutboxItem<TBody = unknown> {
  id: string;
  accountKey: string;
  endpointKey: string;
  body: TBody;
  /** Generated at enqueue. The shared contract with the server that makes retry safe. */
  idempotencyKey: string;
  status: BrowserOutboxStatus;
  priority: 'critical' | 'normal' | 'low';
  attempts: number;
  nextAttemptAt: string;
  /** Set on claim, read by the reaper. Absent unless status is 'sending'. */
  sendingSince?: string;
  createdAt: string;
  updatedAt: string;
  lastError?: string;
  expiresAt?: string;
}

/** Every value here is registered in /alaa-services-contract ($alaa-services-contract). */
export interface OutboxPolicy {
  readonly storeName: string;
  readonly indexName: string;
  readonly batchSize: number;
  readonly sendTimeoutMs: number;
  readonly maxAttempts: number;
  /** Delay for attempt n, supplied by /alaa-reliability-sla doctrine. */
  readonly nextDelayMs: (attempts: number) => number;
}

export const DEFAULT_OUTBOX_POLICY: OutboxPolicy = {
  storeName: 'wa_outbox',
  indexName: 'byStatusNextAttemptAt',
  batchSize: 25,
  sendTimeoutMs: 15_000,
  maxAttempts: 10,
  nextDelayMs: (attempts) => Math.min(3_600_000, 2 ** attempts * 1000),
};

export function validateOutboxPolicy(policy: OutboxPolicy): OutboxPolicy {
  if (!Number.isInteger(policy.batchSize) || policy.batchSize < 1) {
    throw new RangeError('batchSize must be a positive integer');
  }
  if (!Number.isInteger(policy.maxAttempts) || policy.maxAttempts < 1) {
    throw new RangeError('maxAttempts must be a positive integer');
  }
  if (!Number.isFinite(policy.sendTimeoutMs) || policy.sendTimeoutMs <= 0) {
    throw new RangeError('sendTimeoutMs must be positive');
  }
  return policy;
}

export async function enqueueOutboxItem<TBody>(
  db: IDBDatabase,
  item: BrowserOutboxItem<TBody>,
  policy: OutboxPolicy = DEFAULT_OUTBOX_POLICY,
): Promise<void> {
  if (item.status !== 'queued') throw new Error('An enqueued item must be queued');
  const tx = db.transaction(policy.storeName, 'readwrite');
  tx.objectStore(policy.storeName).put(item);
  await txDone(tx);
}

/**
 * Claim a batch in one short transaction.
 *
 * SORT INVARIANT: this cursor walks ['queued', ...] and writes 'sending' into the
 * indexed `status` field while iterating. 'sending' < 'queued' lexicographically, so
 * an updated record moves BEHIND the cursor and is not visited twice. Renaming either
 * token without re-checking that ordering yields an infinite claim loop.
 * The test in ./vitest-idb-pattern.test.ts asserts it.
 */
export async function claimNextOutboxBatch(
  db: IDBDatabase,
  nowIso: string,
  policy: OutboxPolicy = DEFAULT_OUTBOX_POLICY,
): Promise<BrowserOutboxItem[]> {
  const tx = db.transaction(policy.storeName, 'readwrite');
  const index = tx.objectStore(policy.storeName).index(policy.indexName);
  const range = IDBKeyRange.bound(['queued', ''], ['queued', nowIso]);
  const items: BrowserOutboxItem[] = [];

  await new Promise<void>((resolve, reject) => {
    const request = index.openCursor(range);
    request.onerror = () => reject(request.error ?? new Error('Outbox cursor failed'));
    request.onsuccess = () => {
      const cursor = request.result;
      if (!cursor || items.length >= policy.batchSize) {
        resolve();
        return;
      }
      const item = cursor.value as BrowserOutboxItem;
      const claimed: BrowserOutboxItem = {
        ...item,
        status: 'sending',
        sendingSince: nowIso,
        updatedAt: nowIso,
      };
      cursor.update(claimed);
      items.push(claimed);
      cursor.continue();
    };
  });

  await txDone(tx);
  return items;
}

async function writeOutcome(
  db: IDBDatabase,
  policy: OutboxPolicy,
  id: string,
  mutate: (item: BrowserOutboxItem) => BrowserOutboxItem,
): Promise<void> {
  const tx = db.transaction(policy.storeName, 'readwrite');
  const store = tx.objectStore(policy.storeName);
  const request = store.get(id);
  request.onsuccess = () => {
    const item = request.result as BrowserOutboxItem | undefined;
    if (item) store.put(mutate(item));
  };
  await txDone(tx);
}

export type SendOutcome =
  | { kind: 'sent' }
  | { kind: 'retry'; error: string }
  | { kind: 'conflict'; error: string }
  | { kind: 'abandon'; error: string }
  /** 401: the session expired. Pause the flush; do NOT burn an attempt. */
  | { kind: 'pause'; error: string };

export function classifyResponse(status: number): SendOutcome {
  if (status >= 200 && status < 300) return { kind: 'sent' };
  if (status === 401) return { kind: 'pause', error: 'http_401' };
  if (status === 403) return { kind: 'abandon', error: 'http_403' };
  if (status === 409) return { kind: 'conflict', error: 'http_409' };
  if (status === 429 || status >= 500) return { kind: 'retry', error: `http_${status}` };
  return { kind: 'abandon', error: `http_${status}` };
}

export interface FlushResult {
  sent: number;
  retried: number;
  conflicted: number;
  abandoned: number;
  paused: boolean;
}

export async function flushOutbox(options: {
  db: IDBDatabase;
  now?: () => Date;
  send: (item: BrowserOutboxItem, signal: AbortSignal) => Promise<Response>;
  policy?: OutboxPolicy;
  signal?: AbortSignal;
}): Promise<FlushResult> {
  const policy = validateOutboxPolicy(options.policy ?? DEFAULT_OUTBOX_POLICY);
  const now = options.now ?? (() => new Date());
  const batch = await claimNextOutboxBatch(options.db, now().toISOString(), policy);
  const result: FlushResult = { sent: 0, retried: 0, conflicted: 0, abandoned: 0, paused: false };

  for (const item of batch) {
    if (options.signal?.aborted || result.paused) {
      // Return unsent claims to the queue rather than leaving them for the reaper.
      await requeue(options.db, policy, item.id, now);
      continue;
    }

    // A send with no timeout never settles and never reports.
    const timeout = new AbortController();
    const timer = setTimeout(() => timeout.abort(), policy.sendTimeoutMs);
    let outcome: SendOutcome;
    try {
      const response = await options.send(item, timeout.signal);
      outcome = classifyResponse(response.status);
    } catch (error) {
      outcome = { kind: 'retry', error: error instanceof Error ? error.name : 'network_error' };
    } finally {
      clearTimeout(timer);
    }

    await applyOutcome(options.db, policy, item, outcome, now, result);
  }

  return result;
}

async function applyOutcome(
  db: IDBDatabase,
  policy: OutboxPolicy,
  item: BrowserOutboxItem,
  outcome: SendOutcome,
  now: () => Date,
  result: FlushResult,
): Promise<void> {
  const nowIso = now().toISOString();

  switch (outcome.kind) {
    case 'sent':
      await writeOutcome(db, policy, item.id, (current) => ({
        ...current,
        status: 'sent',
        sendingSince: undefined,
        updatedAt: nowIso,
      }));
      result.sent += 1;
      return;

    case 'pause':
      // Attempts unchanged: an expired session must not burn a valid mutation's budget.
      await requeue(db, policy, item.id, now, outcome.error, /* incrementAttempts */ false);
      result.paused = true;
      return;

    case 'conflict':
      await writeOutcome(db, policy, item.id, (current) => ({
        ...current,
        status: 'conflict',
        sendingSince: undefined,
        lastError: outcome.error,
        updatedAt: nowIso,
      }));
      result.conflicted += 1;
      return;

    case 'abandon':
      await writeOutcome(db, policy, item.id, (current) => ({
        ...current,
        status: 'abandoned',
        sendingSince: undefined,
        lastError: outcome.error,
        updatedAt: nowIso,
      }));
      result.abandoned += 1;
      return;

    case 'retry': {
      const attempts = item.attempts + 1;
      const exhausted = attempts >= policy.maxAttempts;
      await writeOutcome(db, policy, item.id, (current) => ({
        ...current,
        attempts,
        status: exhausted ? 'abandoned' : 'queued',
        sendingSince: undefined,
        nextAttemptAt: new Date(now().getTime() + policy.nextDelayMs(attempts)).toISOString(),
        lastError: outcome.error,
        updatedAt: nowIso,
      }));
      if (exhausted) result.abandoned += 1;
      else result.retried += 1;
      return;
    }
  }
}

async function requeue(
  db: IDBDatabase,
  policy: OutboxPolicy,
  id: string,
  now: () => Date,
  lastError?: string,
  incrementAttempts = false,
): Promise<void> {
  const nowIso = now().toISOString();
  await writeOutcome(db, policy, id, (current) => ({
    ...current,
    status: 'queued',
    sendingSince: undefined,
    attempts: incrementAttempts ? current.attempts + 1 : current.attempts,
    lastError: lastError ?? current.lastError,
    updatedAt: nowIso,
  }));
}
