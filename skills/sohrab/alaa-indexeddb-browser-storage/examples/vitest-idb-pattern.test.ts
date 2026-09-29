/**
 * Level 2 (unit) in /alaa-testing-strategy's ladder.
 * references/80-testing-and-proof-levels.md
 *
 * fake-indexeddb is imported here so the file RUNS as shipped. It does not
 * reproduce WebKit: not transaction-inactivity timing, not quota, not private
 * mode, not eviction. A green run bounds the logic and nothing else.
 */
import 'fake-indexeddb/auto';
import { beforeEach, describe, expect, it } from 'vitest';
import { openIndexedDb, withTransaction, requestToPromise, classifyStorageFailure } from './idb-core';
import { openAlaaClientStorage, DEFAULT_SCHEMA_CONFIG } from './migration-pattern';
import {
  claimNextOutboxBatch,
  classifyResponse,
  enqueueOutboxItem,
  type BrowserOutboxItem,
} from './outbox-pattern';
import { reapOrphanedOutboxRows } from './outbox-reaper';
import { AlaaClientStorage, parseLearningState } from './alaa-client-storage';

const config = (name: string) => ({ ...DEFAULT_SCHEMA_CONFIG, dbName: name });
let dbName: string;

beforeEach(() => {
  dbName = `test-db-${Math.random().toString(36).slice(2)}`;
});

describe('open and write', () => {
  it('opens, writes and reads a record', async () => {
    const db = await openIndexedDb({
      name: dbName,
      version: 1,
      upgrade(database) {
        database.createObjectStore('items', { keyPath: 'id' });
      },
    });

    await withTransaction(db, 'items', 'readwrite', (tx) => {
      tx.objectStore('items').put({ id: 'a', value: 1 });
    });

    const tx = db.transaction('items', 'readonly');
    const item = (await requestToPromise(tx.objectStore('items').get('a'))) as { value: number };
    expect(item.value).toBe(1);
    db.close();
  });

  it('aborts rather than silently mis-sequencing when the callback returns a Promise', async () => {
    const db = await openIndexedDb({
      name: dbName,
      version: 1,
      upgrade: (database) => void database.createObjectStore('items', { keyPath: 'id' }),
    });

    await expect(
      withTransaction(db, 'items', 'readwrite', async (tx) => {
        tx.objectStore('items').put({ id: 'a' });
      }),
    ).rejects.toThrow(/must not return a Promise/);
    db.close();
  });
});

describe('migrations', () => {
  it('runs every branch on a fresh install and records the schema version', async () => {
    const db = await openAlaaClientStorage({ config: config(dbName) });
    for (const store of ['meta', 'migration_journal', 'learning_state', 'wa_outbox', 'drafts']) {
      expect(db.objectStoreNames.contains(store)).toBe(true);
    }
    const tx = db.transaction('meta', 'readonly');
    const meta = (await requestToPromise(tx.objectStore('meta').get('schemaVersion'))) as {
      value: number;
    };
    expect(meta.value).toBe(DEFAULT_SCHEMA_CONFIG.dbVersion);
    db.close();
  });

  it('upgrades from version 1 without losing the version-1 store', async () => {
    const v1 = await openIndexedDb({
      name: dbName,
      version: 1,
      upgrade(database) {
        database.createObjectStore('meta', { keyPath: 'key' });
        database.createObjectStore('migration_journal', { keyPath: 'id' });
        database.createObjectStore('capabilities', { keyPath: 'key' });
        database
          .createObjectStore('storage_items', { keyPath: 'id' })
          .createIndex('byDataClassLastAccessedAt', ['dataClass', 'lastAccessedAt']);
      },
    });
    await withTransaction(v1, 'meta', 'readwrite', (tx) => {
      tx.objectStore('meta').put({ key: 'survivor', value: true, updatedAt: 'x' });
    });
    v1.close();

    const v4 = await openAlaaClientStorage({ config: config(dbName) });
    const tx = v4.transaction('meta', 'readonly');
    expect(await requestToPromise(tx.objectStore('meta').get('survivor'))).toBeTruthy();
    expect(v4.objectStoreNames.contains('drafts')).toBe(true);
    v4.close();
  });

  it('fires blocked when a second connection holds the old version', async () => {
    // A raw connection deliberately omits the production helper's mandatory close handler.
    const heldRequest = indexedDB.open(dbName, 1);
    heldRequest.onupgradeneeded = () => heldRequest.result.createObjectStore('meta', { keyPath: 'key' });
    const held = await requestToPromise(heldRequest);
    let sawVersionChange = false;
    held.onversionchange = () => { sawVersionChange = true; };

    let blocked = false;
    const upgrade = openIndexedDb({
      name: dbName,
      version: 2,
      upgrade: () => {},
      onBlocked: () => {
        blocked = true;
        held.close(); // the reload UX would do this in the application
      },
    });

    const next = await upgrade;
    expect(sawVersionChange).toBe(true);
    expect(blocked).toBe(true);
    next.close();
  });
});

describe('record validation on read', () => {
  it('rejects an older-schema record and a malformed record', () => {
    expect(parseLearningState({ schema: 0, id: 'a', accountKey: 'k', contentId: 'c', updatedAt: 't' }))
      .toBeNull();
    expect(parseLearningState({ schema: 1, id: 42 })).toBeNull();
    expect(parseLearningState(null)).toBeNull();
    expect(
      parseLearningState({
        schema: 1,
        id: 'a',
        accountKey: 'k',
        contentId: 'c',
        updatedAt: 't',
        createdAt: 't',
        syncStatus: 'local',
      }),
    ).not.toBeNull();
  });
});

describe('quota classification', () => {
  it('separates the retryable classes from the defects', () => {
    expect(classifyStorageFailure(new DOMException('x', 'QuotaExceededError'))).toBe('quota-exceeded');
    expect(classifyStorageFailure(new DOMException('x', 'ConstraintError'))).toBe('constraint');
    expect(classifyStorageFailure(new DOMException('x', 'TransactionInactiveError'))).toBe(
      'transaction-inactive',
    );
    expect(classifyStorageFailure(new Error('plain'))).toBe('unknown');
  });

  it('tells the user when a quota failure survives cleanup and one retry', async () => {
    const failures: { userMustBeTold: boolean }[] = [];
    let attempts = 0;
    let cleanups = 0;
    const db = { transaction() {
      attempts += 1;
      throw new DOMException('quota fixture', 'QuotaExceededError');
    } } as unknown as IDBDatabase;
    const storage = new AlaaClientStorage(
      (f) => failures.push(f), async () => { cleanups += 1; }, async () => db,
    );
    await expect(
      storage.set('a', {
        id: 'a',
        schema: 1,
        accountKey: 'k',
        contentId: 'c',
        syncStatus: 'local',
        createdAt: 't',
        updatedAt: 't',
      }),
    ).rejects.toBeDefined();
    expect(attempts).toBe(2);
    expect(cleanups).toBe(1);
    expect(failures).toEqual([{ kind: 'quota-exceeded', userMustBeTold: true }]);
  });
});

describe('outbox', () => {
  const item = (id: string, over: Partial<BrowserOutboxItem> = {}): BrowserOutboxItem => ({
    id,
    accountKey: 'acct',
    endpointKey: 'wa.track',
    body: {},
    idempotencyKey: `idem-${id}`,
    status: 'queued',
    priority: 'normal',
    attempts: 0,
    nextAttemptAt: '2020-01-01T00:00:00.000Z',
    createdAt: '2020-01-01T00:00:00.000Z',
    updatedAt: '2020-01-01T00:00:00.000Z',
    ...over,
  });

  it('classifies 401 and 403 differently', () => {
    expect(classifyResponse(401).kind).toBe('pause');
    expect(classifyResponse(403).kind).toBe('abandon');
    expect(classifyResponse(409).kind).toBe('conflict');
    expect(classifyResponse(503).kind).toBe('retry');
    expect(classifyResponse(204).kind).toBe('sent');
  });

  it('moves claimed and reaped rows outside their exact-status cursor ranges', () => {
    expect(indexedDB.cmp('sending', 'queued')).toBe(1);
    expect(indexedDB.cmp('queued', 'sending')).toBe(-1);
    const claims = IDBKeyRange.bound(['queued', ''], ['queued', '2021-01-01']);
    const reaps = IDBKeyRange.bound(['sending'], ['sending', []]);
    expect(claims.includes(['sending', '2020-01-01'])).toBe(false);
    expect(reaps.includes(['queued', '2020-01-01'])).toBe(false);
  });

  it('claims each due row exactly once', async () => {
    const db = await openAlaaClientStorage({ config: config(dbName) });
    for (const id of ['a', 'b', 'c']) await enqueueOutboxItem(db, item(id));

    const batch = await claimNextOutboxBatch(db, '2021-01-01T00:00:00.000Z');
    expect(batch.map((i) => i.id).sort()).toEqual(['a', 'b', 'c']);
    expect(new Set(batch.map((i) => i.id)).size).toBe(3);

    const second = await claimNextOutboxBatch(db, '2021-01-01T00:00:00.000Z');
    expect(second).toHaveLength(0); // all now 'sending', outside the claim range
    db.close();
  });

  it('reaps a row orphaned in sending and leaves a fresh one alone', async () => {
    const db = await openAlaaClientStorage({ config: config(dbName) });
    const now = new Date('2021-01-01T00:10:00.000Z');
    await enqueueOutboxItem(db, item('stale'));
    await enqueueOutboxItem(db, item('fresh'));
    await claimNextOutboxBatch(db, '2021-01-01T00:00:00.000Z'); // both -> sending @ 00:00

    // staleAfterMs 120_000; 'fresh' is rewritten with a recent sendingSince.
    const tx = db.transaction('wa_outbox', 'readwrite');
    const store = tx.objectStore('wa_outbox');
    const got = await requestToPromise(store.get('fresh'));
    store.put({ ...(got as BrowserOutboxItem), sendingSince: now.toISOString() });
    await new Promise<void>((r) => {
      tx.oncomplete = () => r();
    });

    const result = await reapOrphanedOutboxRows({ db, now: () => now });
    expect(result.reaped).toBe(1);
    expect(result.inFlight).toBe(1);
    db.close();
  });
});

describe('logout purge', () => {
  it('removes every record for the previous account and leaves the current one', async () => {
    const db = await openAlaaClientStorage({ config: config(dbName) });
    const storage = new AlaaClientStorage(undefined, undefined, async () => db);
    const write = (id: string, accountKey: string) => storage.set(id, {
      id, schema: 1, accountKey, contentId: 'c', syncStatus: 'local',
      createdAt: 't', updatedAt: '2021-01-01T00:00:00.000Z',
    });
    await withTransaction(db, 'storage_items', 'readwrite', (tx) => {
      tx.objectStore('storage_items').put({ id: 'orphan', accountKey: 'gone', updatedAt: 't' });
    });

    await write('old-1', 'gone');
    await write('old-2', 'gone');
    await write('keep', 'current');
    const removed = await storage.deleteByAccount('gone');
    expect(removed).toBe(2);
    const remaining = await requestToPromise(db.transaction('learning_state').objectStore('learning_state').getAll());
    expect(remaining.map((row) => row.id)).toEqual(['keep']);
    const metadata = await requestToPromise(db.transaction('storage_items').objectStore('storage_items').getAll());
    expect(metadata.map((row) => row.id)).toEqual(['learning_state:keep']);
    expect(await storage.deleteByAccount('gone')).toBe(0);
    db.close();
  });
});
