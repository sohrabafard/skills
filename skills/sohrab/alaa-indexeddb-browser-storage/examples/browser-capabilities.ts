/**
 * The single declaration of the capability contract. references/20 points here;
 * assets/capability-tier-contract.json is the contract the harness enforces over both.
 * scripts/capability_contract_conformance.py fails on any disagreement.
 */
import { probeIndexedDbWrite } from './idb-core';

export type CapabilityValue = boolean | 'unknown';

export interface BrowserStorageCapabilities {
  indexedDb: 'unavailable' | 'core' | 'modern';
  testedWrite: boolean;
  estimate: boolean;
  persist: boolean;
  persisted: CapabilityValue;
  getAll: boolean;
  getAllKeys: boolean;
  getAllRecords: boolean;
  transactionDurability: CapabilityValue;
  databases: boolean;
  broadcastChannel: boolean;
  locks: boolean;
  serviceWorker: boolean;
  backgroundSync: boolean;
  opfs: boolean;
  workerIdb: CapabilityValue;
  storageBuckets: boolean;
  privateModeLikely: CapabilityValue;
}

export async function detectBrowserStorageCapabilities(): Promise<BrowserStorageCapabilities> {
  const testedWrite = await probeIndexedDbWrite();
  const nav = typeof navigator !== 'undefined' ? navigator : undefined;
  const storage = nav?.storage;
  const estimate = typeof storage?.estimate === 'function';
  const persist = typeof storage?.persist === 'function';

  let persisted: CapabilityValue = 'unknown';
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
    transactionDurability:
      typeof IDBTransaction === 'undefined' ? 'unknown' : 'durability' in IDBTransaction.prototype,
    databases: typeof indexedDB !== 'undefined' && typeof indexedDB.databases === 'function',
    broadcastChannel: typeof BroadcastChannel !== 'undefined',
    locks: !!nav && 'locks' in nav,
    serviceWorker: !!nav && 'serviceWorker' in nav,
    // Background Sync is Chromium-only: absent in every Firefox and every Safari/iOS
    // (caniuse, read 2026-07-28). Never the only flush trigger.
    backgroundSync:
      typeof ServiceWorkerRegistration !== 'undefined' && 'sync' in ServiceWorkerRegistration.prototype,
    opfs: !!storage && typeof storage.getDirectory === 'function',
    workerIdb: typeof Worker === 'undefined' ? 'unknown' : true,
    // Chromium 122+ only. references/25-storage-buckets-api.md; never a requirement.
    storageBuckets: !!nav && 'storageBuckets' in nav,
    privateModeLikely: await inferPrivateModeWeakSignal(estimate),
  };
}

async function inferPrivateModeWeakSignal(canEstimate: boolean): Promise<CapabilityValue> {
  // No standard private-mode detector exists. This is a weak UX hint only.
  // Never fingerprint users or block functionality on it alone.
  if (!canEstimate) return 'unknown';
  try {
    const { quota } = await navigator.storage.estimate();
    if (!quota) return 'unknown';
    return quota < 100 * 1024 * 1024;
  } catch {
    return 'unknown';
  }
}

/**
 * Tier definitions are in references/20 and assets/capability-tier-contract.json.
 * Tier 3 is reachable; the conformance harness asserts that it is.
 */
export function chooseCapabilityTier(c: BrowserStorageCapabilities): 0 | 1 | 2 | 3 {
  if (c.indexedDb === 'unavailable' || !c.testedWrite) return 0;
  if (!c.estimate) return 1;

  const hasLargeValueStore = c.opfs || typeof caches !== 'undefined';
  const hasCoordination = c.broadcastChannel && c.locks;
  const hasWorker = c.workerIdb === true;
  if (hasWorker && hasLargeValueStore && hasCoordination) return 3;

  return 2;
}
