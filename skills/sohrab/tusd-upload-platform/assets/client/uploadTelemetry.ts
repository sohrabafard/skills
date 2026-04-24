export interface SafeUploadTelemetryInput {
  appUploadId?: string
  status?: string
  sizeBytes?: number
  retryCount?: number
  httpStatus?: number | null
  safeErrorCode?: string
  targetType?: string
}

export function sizeBucket(sizeBytes?: number): string {
  if (sizeBytes === undefined) return 'unknown'
  if (sizeBytes < 10 * 1024 * 1024) return '<10MiB'
  if (sizeBytes < 100 * 1024 * 1024) return '<100MiB'
  if (sizeBytes < 1024 * 1024 * 1024) return '<1GiB'
  return '>=1GiB'
}

export function toSafeUploadTelemetry(input: SafeUploadTelemetryInput): Record<string, string | number | null | undefined> {
  return {
    app_upload_id: input.appUploadId,
    upload_status: input.status,
    size_bucket: sizeBucket(input.sizeBytes),
    retry_count: input.retryCount,
    http_status: input.httpStatus,
    error_code: input.safeErrorCode,
    target_type: input.targetType,
  }
}

export function redactUploadUrl(value: string): string {
  return value.replace(/\/files\/[^/?#]+/g, '/files/[upload-id]')
}

export function scrubUploadHeaders(headers: Record<string, unknown>): Record<string, unknown> {
  const blocked = new Set(['authorization', 'cookie', 'upload-metadata'])
  return Object.fromEntries(
    Object.entries(headers).map(([key, value]) => [
      key,
      blocked.has(key.toLowerCase()) ? '[Filtered]' : value,
    ]),
  )
}
