import { probeIndexedDbWrite } from './idb-core';

export type CapabilityValue = boolean | 'unknown';

export interface BrowserStorageCapabilities {
  indexedDb: 'unavailable' | 'core' | 'modern';
  testedWrite: boolean;
  estimate: boolean;
  persist: boolean;
  persisted: boolean | 'unknown';
  getAll: boolean;
  getAllKeys: boolean;
  getAllRecords: boolean;
  transactionDurability: boolean | 'unknown';
  databases: boolean;
  broadcastChannel: boolean;
  locks: boolean;
  serviceWorker: boolean;
  opfs: boolean;
  privateModeLikely: boolean | 'unknown';
}

export async function detectBrowserStorageCapabilities(): Promise<BrowserStorageCapabilities> {
  const testedWrite = await probeIndexedDbWrite();
  const storage = typeof navigator !== 'undefined' ? navigator.storage : undefined;
  const estimate = typeof storage?.estimate === 'function';
  const persist = typeof storage?.persist === 'function';

  let persisted: boolean | 'unknown' = 'unknown';
  if (typeof storage?.persisted === 'function') {
    try {
      persisted = await storage.persisted();
    } catch {
      persisted = 'unknown';
    }
  }

  const objectStoreProto = typeof IDBObjectStore !== 'undefined' ? IDBObjectStore.prototype : undefined;

  return {
    indexedDb: testedWrite ? (estimate || persist ? 'modern' : 'core') : 'unavailable',
    testedWrite,
    estimate,
    persist,
    persisted,
    getAll: !!objectStoreProto && 'getAll' in objectStoreProto,
    getAllKeys: !!objectStoreProto && 'getAllKeys' in objectStoreProto,
    getAllRecords: !!objectStoreProto && 'getAllRecords' in objectStoreProto,
    transactionDurability: typeof IDBTransaction !== 'undefined' && 'durability' in IDBTransaction.prototype,
    databases: typeof indexedDB !== 'undefined' && typeof indexedDB.databases === 'function',
    broadcastChannel: typeof BroadcastChannel !== 'undefined',
    locks: typeof navigator !== 'undefined' && 'locks' in navigator,
    serviceWorker: typeof navigator !== 'undefined' && 'serviceWorker' in navigator,
    opfs: !!storage && typeof storage.getDirectory === 'function',
    privateModeLikely: await inferPrivateModeWeakSignal(estimate),
  };
}

async function inferPrivateModeWeakSignal(canEstimate: boolean): Promise<boolean | 'unknown'> {
  // There is no standard reliable private-mode detector. Use only weak UX hints.
  // Never fingerprint users or block functionality based on this alone.
  if (!canEstimate) return 'unknown';
  try {
    const { quota } = await navigator.storage.estimate();
    if (!quota) return 'unknown';
    // Very small quota can be a hint, but not proof. Tune per product telemetry.
    return quota < 100 * 1024 * 1024;
  } catch {
    return 'unknown';
  }
}

export function chooseCapabilityTier(c: BrowserStorageCapabilities): 0 | 1 | 2 | 3 {
  if (c.indexedDb === 'unavailable' || !c.testedWrite) return 0;
  if (c.indexedDb === 'core') return 1;
  if (c.estimate || c.persist) return 2;
  return 1;
}
