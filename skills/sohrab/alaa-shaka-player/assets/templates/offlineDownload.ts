/**
 * In-app download for Shaka v5.2.3.
 *
 * SEAM: this file owns what the player stores, how it is fetched and licensed. The storage
 * substrate - quota, eviction, persistence, and what happens when a stored asset is evicted
 * mid-session - is owned by /alaa-indexeddb-browser-storage ($alaa-indexeddb-browser-storage),
 * references/30-storage-quota-persistence-and-eviction.md.
 *
 * The fact that joins them: Shaka's only use of navigator.storage anywhere in lib/ is two
 * estimate() calls. IT NEVER CALLS navigator.storage.persist(). A download therefore lives in
 * best-effort storage and the browser may evict it at any time without telling the player.
 * `requestDurableStorage()` below is this application's half of that; surviving an eviction
 * is the other skill's half.
 */

import type {
  ShakaAbortableOperation, ShakaNamespace, ShakaPlayer, ShakaStorage, ShakaStoredContent
} from "./shakaTypes";

export type DownloadRefusal =
  | "unsupported"          // shaka.offline.Storage.support().basic === false
  | "live-not-storable"    // CANNOT_STORE_LIVE_OFFLINE (9005)
  | "quota"                // STORAGE_LIMIT_REACHED (9014)
  | "storage-unavailable"  // INDEXED_DB_INIT_TIMED_OUT (9017)
  | "storage-corrupt"      // INDEXED_DB_ERROR (9001)
  | "no-init-data"         // NO_INIT_DATA_FOR_OFFLINE (9007)
  | "failed";

export interface DownloadOptions {
  /** Largest video height to store, px. Storing every rendition is the identity default's bug. */
  readonly maxHeight: number;
  /** Text-track languages to store. */
  readonly textLanguages: readonly string[];
  /** Refuse a download that would push usage past this fraction of quota. 0..0.95.
   *  Shaka's own default is 0.95; being stricter leaves room for the rest of the app. */
  readonly quotaFraction: number;
  readonly onProgress?: (originalManifestUri: string, fraction: number) => void;
  /** Called on every download request attempt. */
  readonly getToken?: () => Promise<string>;
}

export const DEFAULT_DOWNLOAD_OPTIONS: DownloadOptions = Object.freeze({
  maxHeight: 720,
  textLanguages: ["fa", "en"],
  quotaFraction: 0.8
});

export interface DownloadHandle {
  readonly promise: Promise<ShakaStoredContent>;
  abort(): Promise<void>;
}

/**
 * Asks the browser for persistent (non-evictable) storage. Shaka never does this.
 * Record the result: `false` means every download here is evictable.
 */
export async function requestDurableStorage(): Promise<boolean> {
  if (!navigator.storage?.persist) return false;
  try { return await navigator.storage.persist(); } catch { return false; }
}

/** Sets the IndexedDB open timeout. MUST run before any other offline operation. */
export function setStorageOpenTimeout(shaka: unknown, seconds: number | false): void {
  const ns = shaka as { offline?: { indexeddb?: { StorageMechanismOpenTimeout?: number | false } } };
  if (ns.offline?.indexeddb) ns.offline.indexeddb.StorageMechanismOpenTimeout = seconds;
}

export async function createDownloadManager(
  shaka: ShakaNamespace,
  player: ShakaPlayer,
  input: Partial<DownloadOptions> = {}
): Promise<{
  isSupported: boolean;
  canStorePersistentLicence: boolean;
  start(uri: string, appMetadata?: Record<string, unknown>): DownloadHandle;
  list(): Promise<ShakaStoredContent[]>;
  listInterrupted(): Promise<ShakaStoredContent[]>;
  remove(offlineUri: string): Promise<void>;
  dispose(): Promise<void>;
}> {
  const options: DownloadOptions = { ...DEFAULT_DOWNLOAD_OPTIONS, ...input };
  if (!(options.quotaFraction > 0 && options.quotaFraction <= 0.95)) {
    throw new RangeError(`quotaFraction must be in (0, 0.95]; received ${options.quotaFraction}`);
  }

  const support = await shaka.offline.Storage.support();
  const canStorePersistentLicence = support.encrypted["com.widevine.alpha"] === true;

  const storage: ShakaStorage = new shaka.offline.Storage(player);
  // Orphaned persistent DRM sessions accumulate across removals. Upstream: call on startup.
  await storage.removeEmeSessions();

  storage.configure({
    offline: {
      numberOfParallelDownloads: 5,
      // false means the asset needs a network connection at playback time to fetch a licence.
      usePersistentLicense: canStorePersistentLicence,

      // The DEFAULT is identity, which stores every rendition of every language.
      trackSelectionCallback: async (tracks: readonly Record<string, unknown>[]) => {
        const variants = tracks.filter(t =>
          t.type === "variant" && typeof t.height === "number" &&
          (t.height as number) <= options.maxHeight);
        const best = [...variants].sort(
          (a, b) => (b.bandwidth as number) - (a.bandwidth as number))[0];
        const text = tracks.filter(t =>
          t.type === "text" && options.textLanguages.includes(t.language as string));
        return best ? [best, ...text] : tracks;
      },

      // sizeEstimate is bitrate-derived (bandwidth * duration / 8), NOT a measured byte count.
      // Returning false makes store() reject with STORAGE_LIMIT_REACHED (9014).
      downloadSizeCallback: async (sizeEstimate: number) => {
        if (!navigator.storage?.estimate) return true;
        const { usage = 0, quota = 0 } = await navigator.storage.estimate();
        return usage + sizeEstimate < quota * options.quotaFraction;
      },

      progressCallback: (content: ShakaStoredContent, fraction: number) => {
        options.onProgress?.(content.originalManifestUri, fraction);
      }
    }
  });

  // Storage has its OWN networking engine: filters on the Player's engine do not apply here.
  const getToken = options.getToken;
  if (getToken) {
    storage.getNetworkingEngine().registerRequestFilter(async (_type, request) => {
      request.headers["Authorization"] = `Bearer ${await getToken()}`;
    });
  }

  function start(uri: string, appMetadata: Record<string, unknown> = {}): DownloadHandle {
    // Live cannot be stored (9005). Refusing here gives a better message than the rejection.
    if (player.isLive()) {
      return {
        promise: Promise.reject(refusal("live-not-storable", 9005)),
        abort: async () => {}
      };
    }
    // Shaka does NOT deduplicate: storing the same URI twice downloads it twice.
    const operation: ShakaAbortableOperation<ShakaStoredContent> =
      storage.store(uri, appMetadata);

    return {
      // `.promise`, not the operation itself.
      promise: operation.promise.catch((raw: unknown) => { throw toRefusal(raw); }),
      abort: () => operation.abort()
    };
  }

  async function listInterrupted(): Promise<ShakaStoredContent[]> {
    // There is NO resume API. `isIncomplete` is the only record that a store was interrupted,
    // and `offlineUri` is null for these, which makes targeted removal awkward.
    return (await storage.list()).filter(c => c.isIncomplete);
  }

  return {
    isSupported: support.basic,
    canStorePersistentLicence,
    start,
    list: () => storage.list(),
    listInterrupted,
    remove: (offlineUri: string) => storage.remove(offlineUri),
    dispose: () => storage.destroy()
  };
}

class DownloadError extends Error {
  constructor(readonly refusal: DownloadRefusal, readonly shakaCode: number | null) {
    super(`download refused: ${refusal}`);
    this.name = "DownloadError";
  }
}

function refusal(kind: DownloadRefusal, code: number | null): DownloadError {
  return new DownloadError(kind, code);
}

function toRefusal(raw: unknown): DownloadError {
  const code = (raw as { code?: unknown }).code;
  if (typeof code !== "number") return refusal("failed", null);
  switch (code) {
    case 9000: return refusal("unsupported", code);
    case 9001: return refusal("storage-corrupt", code);
    case 9005: return refusal("live-not-storable", code);
    case 9007: return refusal("no-init-data", code);
    case 9014: return refusal("quota", code);
    case 9017: return refusal("storage-unavailable", code);
    default:   return refusal("failed", code);
  }
}
