/**
 * Estimate, persistence request, and budget thresholds.
 * references/30-quota-model-and-budgets.md
 *
 * Every threshold is configuration. No literal appears at a call site.
 */

/** Read from the feature's assets/storage-budget-policy-template.md instance. */
export interface StorageBudgetPolicy {
  /** Stop optional prefetch and cache writes above this ratio of quota. */
  readonly softStopUsageRatio: number;
  /** Stop every write except user-generated unsynced work above this ratio. */
  readonly hardStopUsageRatio: number;
  /** Absolute floor of free bytes below which optional writes stop. */
  readonly minFreeBytes: number;
  /** softStop cap in bytes, whichever binds first. */
  readonly softStopMaxBytes: number;
}

export const DEFAULT_BUDGET_POLICY: StorageBudgetPolicy = {
  softStopUsageRatio: 0.85,
  hardStopUsageRatio: 0.95,
  minFreeBytes: 50 * 1024 * 1024,
  softStopMaxBytes: 200 * 1024 * 1024,
};

/** Rejects a policy that would silently disable the guard it exists to provide. */
export function validateBudgetPolicy(policy: StorageBudgetPolicy): StorageBudgetPolicy {
  const inUnitRange = (n: number): boolean => Number.isFinite(n) && n > 0 && n < 1;
  if (!inUnitRange(policy.softStopUsageRatio)) {
    throw new RangeError('softStopUsageRatio must be between 0 and 1, exclusive');
  }
  if (!inUnitRange(policy.hardStopUsageRatio)) {
    throw new RangeError('hardStopUsageRatio must be between 0 and 1, exclusive');
  }
  if (policy.hardStopUsageRatio <= policy.softStopUsageRatio) {
    throw new RangeError('hardStopUsageRatio must exceed softStopUsageRatio');
  }
  if (!Number.isFinite(policy.minFreeBytes) || policy.minFreeBytes < 0) {
    throw new RangeError('minFreeBytes must be a non-negative finite number');
  }
  if (!Number.isFinite(policy.softStopMaxBytes) || policy.softStopMaxBytes <= 0) {
    throw new RangeError('softStopMaxBytes must be positive');
  }
  return policy;
}

export interface StorageEstimateSummary {
  supported: boolean;
  usageBytes?: number;
  quotaBytes?: number;
  availableBytes?: number;
  usageRatio?: number;
  persisted: boolean | 'unknown';
}

export async function getStorageEstimateSummary(): Promise<StorageEstimateSummary> {
  const storage = typeof navigator !== 'undefined' ? navigator.storage : undefined;
  if (!storage?.estimate) return { supported: false, persisted: 'unknown' };

  // Both numbers are approximations: compression, deduplication and deliberate
  // obfuscation. Never gate a write on them alone. MDN, read 2026-07-28.
  const estimate = await storage.estimate();
  const usageBytes = estimate.usage ?? 0;
  const quotaBytes = estimate.quota ?? 0;

  let persisted: boolean | 'unknown' = 'unknown';
  if (storage.persisted) {
    try {
      persisted = await storage.persisted();
    } catch {
      persisted = 'unknown';
    }
  }

  return {
    supported: true,
    usageBytes,
    quotaBytes,
    availableBytes: Math.max(0, quotaBytes - usageBytes),
    usageRatio: quotaBytes > 0 ? usageBytes / quotaBytes : undefined,
    persisted,
  };
}

export type PersistenceOutcome = 'granted' | 'refused' | 'unsupported' | 'failed';

/**
 * Call at the moment the user confirms an action implying they want the data kept.
 * A call on first paint is refused by the engines that judge by engagement.
 *
 * `failed` is distinct from `refused`: a thrown call is not a decision, and
 * conflating them hides a broken environment as a user refusal.
 */
export async function requestPersistentStorageAfterUserIntent(): Promise<PersistenceOutcome> {
  const storage = typeof navigator !== 'undefined' ? navigator.storage : undefined;
  if (!storage?.persist) return 'unsupported';

  try {
    return (await storage.persist()) ? 'granted' : 'refused';
  } catch {
    return 'failed';
  }
}

export function shouldStopOptionalWrites(
  summary: StorageEstimateSummary,
  policy: StorageBudgetPolicy = DEFAULT_BUDGET_POLICY,
): boolean {
  // No estimate means tier 1: the budget file's fixed caps govern, not measurement.
  if (!summary.supported || summary.usageRatio === undefined) return false;
  return (
    summary.usageRatio > policy.softStopUsageRatio ||
    (summary.availableBytes ?? Number.POSITIVE_INFINITY) < policy.minFreeBytes
  );
}

export function shouldStopAllButUnsyncedWrites(
  summary: StorageEstimateSummary,
  policy: StorageBudgetPolicy = DEFAULT_BUDGET_POLICY,
): boolean {
  if (!summary.supported || summary.usageRatio === undefined) return false;
  return summary.usageRatio > policy.hardStopUsageRatio;
}

/** Telemetry carries bands, never the exact pair: the exact pair fingerprints. */
export function bucketBytes(bytes?: number): string {
  if (bytes === undefined) return 'unknown';
  const mb = bytes / 1024 / 1024;
  if (mb < 10) return '<10MB';
  if (mb < 100) return '10-100MB';
  if (mb < 1024) return '100MB-1GB';
  if (mb < 10 * 1024) return '1-10GB';
  return '>10GB';
}
