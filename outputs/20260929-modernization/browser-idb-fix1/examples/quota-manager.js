export const DEFAULT_BUDGET_POLICY = {
    softStopUsageRatio: 0.85,
    hardStopUsageRatio: 0.95,
    minFreeBytes: 50 * 1024 * 1024,
    softStopMaxBytes: 200 * 1024 * 1024
};
export function validateBudgetPolicy(policy) {
    const inUnitRange = (n)=>Number.isFinite(n) && n > 0 && n < 1;
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
export async function getStorageEstimateSummary() {
    const storage = typeof navigator !== 'undefined' ? navigator.storage : undefined;
    if (!storage?.estimate) return {
        supported: false,
        persisted: 'unknown'
    };
    const estimate = await storage.estimate();
    const usageBytes = estimate.usage ?? 0;
    const quotaBytes = estimate.quota ?? 0;
    let persisted = 'unknown';
    if (storage.persisted) {
        try {
            persisted = await storage.persisted();
        } catch  {
            persisted = 'unknown';
        }
    }
    return {
        supported: true,
        usageBytes,
        quotaBytes,
        availableBytes: Math.max(0, quotaBytes - usageBytes),
        usageRatio: quotaBytes > 0 ? usageBytes / quotaBytes : undefined,
        persisted
    };
}
export async function requestPersistentStorageAfterUserIntent() {
    const storage = typeof navigator !== 'undefined' ? navigator.storage : undefined;
    if (!storage?.persist) return 'unsupported';
    try {
        return await storage.persist() ? 'granted' : 'refused';
    } catch  {
        return 'failed';
    }
}
export function shouldStopOptionalWrites(summary, policy = DEFAULT_BUDGET_POLICY) {
    if (!summary.supported || summary.usageRatio === undefined) return false;
    return summary.usageRatio > policy.softStopUsageRatio || (summary.availableBytes ?? Number.POSITIVE_INFINITY) < policy.minFreeBytes;
}
export function shouldStopAllButUnsyncedWrites(summary, policy = DEFAULT_BUDGET_POLICY) {
    if (!summary.supported || summary.usageRatio === undefined) return false;
    return summary.usageRatio > policy.hardStopUsageRatio;
}
export function bucketBytes(bytes) {
    if (bytes === undefined) return 'unknown';
    const mb = bytes / 1024 / 1024;
    if (mb < 10) return '<10MB';
    if (mb < 100) return '10-100MB';
    if (mb < 1024) return '100MB-1GB';
    if (mb < 10 * 1024) return '1-10GB';
    return '>10GB';
}
