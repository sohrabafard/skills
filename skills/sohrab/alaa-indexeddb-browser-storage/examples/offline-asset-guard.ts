/**
 * Detecting a partial or evicted offline media asset.
 * references/72-offline-media-store.md
 *
 * Shaka Player v5.2.3 never calls navigator.storage.persist() and offers no resume
 * or repair API for an interrupted store(). Detecting the partial state is this
 * layer's job; restarting the download is the caller's.
 *
 * What the player stores, how it fetches and licenses it, and the shaka.offline
 * surface are /alaa-shaka-player ($alaa-shaka-player). This file touches none of it:
 * it takes a `listStoredUris` callback that the player skill's code supplies.
 */
import { txDone, accountRange } from './idb-core';
import {
  getStorageEstimateSummary,
  requestPersistentStorageAfterUserIntent,
  type PersistenceOutcome,
} from './quota-manager';

export interface OfflineAssetRecord {
  id: string;
  accountKey: string;
  schema: number;
  contentId: string;
  /** Written before the download begins, cleared only after it resolves. */
  downloadState: 'requested' | 'storing' | 'complete';
  /** The handle the player skill defines for a completed asset. */
  offlineUri?: string;
  expectedBytes?: number;
  /** Result of the persistence request made when the user confirmed. */
  persistence: PersistenceOutcome;
  startedAt: string;
  completedAt?: string;
  lastVerifiedAt?: string;
  updatedAt: string;
}

export const OFFLINE_ASSET_SCHEMA = 1;

export interface OfflineStoreConfig {
  readonly storeName: string;
  readonly accountIndexName: string;
  /** Total offline bytes permitted on this device. From the budget file. */
  readonly maxTotalBytes: number;
  /** Refuse to start unless free space exceeds the asset size by this factor. */
  readonly freeSpaceSafetyFactor: number;
}

export const DEFAULT_OFFLINE_STORE_CONFIG: OfflineStoreConfig = {
  storeName: 'offline_assets',
  accountIndexName: 'byAccountUpdatedAt',
  maxTotalBytes: 4 * 1024 * 1024 * 1024,
  freeSpaceSafetyFactor: 1.25,
};

export type StartDecision =
  | { ok: true; persistence: PersistenceOutcome }
  | { ok: false; reason: 'insufficient-space' | 'over-device-cap' | 'no-estimate' };

/**
 * Called at the moment the user confirms the download. That confirmation is the
 * strongest engagement signal the engines that judge by history will see, so the
 * persistence request belongs here and not on first paint.
 */
export async function decideDownloadStart(options: {
  expectedBytes: number;
  currentOfflineBytes: number;
  config?: OfflineStoreConfig;
}): Promise<StartDecision> {
  const config = options.config ?? DEFAULT_OFFLINE_STORE_CONFIG;

  if (options.currentOfflineBytes + options.expectedBytes > config.maxTotalBytes) {
    return { ok: false, reason: 'over-device-cap' };
  }

  const estimate = await getStorageEstimateSummary();
  if (!estimate.supported || estimate.availableBytes === undefined) {
    // Tier below 2: no measurement, so no offline affordance. references/20.
    return { ok: false, reason: 'no-estimate' };
  }

  // The estimate is approximate, so a margin below the asset size is insufficient,
  // not a close call.
  if (estimate.availableBytes < options.expectedBytes * config.freeSpaceSafetyFactor) {
    return { ok: false, reason: 'insufficient-space' };
  }

  return { ok: true, persistence: await requestPersistentStorageAfterUserIntent() };
}

/** Commit 'storing' in its own transaction BEFORE the download begins. */
export async function markDownloadStarting(
  db: IDBDatabase,
  record: Omit<OfflineAssetRecord, 'schema' | 'downloadState' | 'updatedAt'>,
  config: OfflineStoreConfig = DEFAULT_OFFLINE_STORE_CONFIG,
): Promise<void> {
  const nowIso = new Date().toISOString();
  const tx = db.transaction(config.storeName, 'readwrite');
  tx.objectStore(config.storeName).put({
    ...record,
    schema: OFFLINE_ASSET_SCHEMA,
    downloadState: 'storing',
    updatedAt: nowIso,
  } satisfies OfflineAssetRecord);
  await txDone(tx);
}

export type AssetVerdict =
  /** The record says storing: interrupted. There is no resume API; restart it. */
  | { state: 'partial'; record: OfflineAssetRecord }
  /** The record says complete but the player no longer holds it: evicted. */
  | { state: 'evicted'; record: OfflineAssetRecord }
  | { state: 'playable'; record: OfflineAssetRecord };

/**
 * Reconcile local records against what the player actually holds.
 *
 * Call on boot and again before offering or starting offline playback. Never wait
 * for a playback error: the user tapping a missing download gets an error instead
 * of an explanation.
 *
 * Complexity: O(log n + k) over the account index, plus one call to listStoredUris.
 * It never scans the whole store.
 */
export async function reconcileOfflineAssets(options: {
  db: IDBDatabase;
  accountKey: string;
  /** Supplied by the player layer. This file does not know how it is implemented. */
  listStoredUris: () => Promise<readonly string[]>;
  config?: OfflineStoreConfig;
}): Promise<AssetVerdict[]> {
  const config = options.config ?? DEFAULT_OFFLINE_STORE_CONFIG;
  const stored = new Set(await options.listStoredUris());
  const verdicts: AssetVerdict[] = [];

  const tx = options.db.transaction(config.storeName, 'readonly');
  const index = tx.objectStore(config.storeName).index(config.accountIndexName);

  await new Promise<void>((resolve, reject) => {
    const request = index.openCursor(accountRange(options.accountKey));
    request.onerror = () => reject(request.error ?? new Error('Offline asset cursor failed'));
    request.onsuccess = () => {
      const cursor = request.result;
      if (!cursor) {
        resolve();
        return;
      }
      const record = cursor.value as OfflineAssetRecord;
      if (record.downloadState !== 'complete') {
        verdicts.push({ state: 'partial', record });
      } else if (!record.offlineUri || !stored.has(record.offlineUri)) {
        verdicts.push({ state: 'evicted', record });
      } else {
        verdicts.push({ state: 'playable', record });
      }
      cursor.continue();
    };
  });

  await txDone(tx);
  return verdicts;
}

/**
 * Delete the local record so the UI does not offer the asset again this session.
 * The caller then tells the user the browser removed it and falls through to
 * online playback in the same interaction. Never re-download silently.
 */
export async function forgetEvictedAsset(
  db: IDBDatabase,
  id: string,
  config: OfflineStoreConfig = DEFAULT_OFFLINE_STORE_CONFIG,
): Promise<void> {
  const tx = db.transaction(config.storeName, 'readwrite');
  tx.objectStore(config.storeName).delete(id);
  await txDone(tx);
}
