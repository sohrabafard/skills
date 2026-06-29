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
  if (!storage?.estimate) {
    return { supported: false, persisted: 'unknown' };
  }

  const estimate = await storage.estimate();
  const usageBytes = estimate.usage ?? 0;
  const quotaBytes = estimate.quota ?? 0;
  const availableBytes = Math.max(0, quotaBytes - usageBytes);
  const usageRatio = quotaBytes > 0 ? usageBytes / quotaBytes : undefined;

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
    availableBytes,
    usageRatio,
    persisted,
  };
}

export async function requestPersistentStorageAfterUserIntent(): Promise<'granted' | 'denied' | 'unsupported'> {
  const storage = typeof navigator !== 'undefined' ? navigator.storage : undefined;
  if (!storage?.persist) return 'unsupported';

  try {
    const granted = await storage.persist();
    return granted ? 'granted' : 'denied';
  } catch {
    return 'denied';
  }
}

export function shouldStopOptionalWrites(summary: StorageEstimateSummary): boolean {
  if (!summary.supported || summary.usageRatio === undefined) return false;
  return summary.usageRatio > 0.85 || (summary.availableBytes ?? Infinity) < 50 * 1024 * 1024;
}

export function bucketBytes(bytes?: number): string {
  if (bytes === undefined) return 'unknown';
  const mb = bytes / 1024 / 1024;
  if (mb < 10) return '<10MB';
  if (mb < 100) return '10-100MB';
  if (mb < 1024) return '100MB-1GB';
  if (mb < 10 * 1024) return '1-10GB';
  return '>10GB';
}
