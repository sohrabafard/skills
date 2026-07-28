/**
 * Safe upload telemetry.
 *
 * Nothing here emits a URL, an object key, a filename, raw Upload-Metadata,
 * an Authorization header, a cookie or a credential. The base path is always
 * an argument, never a constant, so redaction keeps working when the
 * deployment's upload path changes.
 */
import type { UploadState } from './uploadStates'

export interface SafeUploadTelemetryInput {
  appUploadId?: string
  status?: UploadState
  sizeBytes?: number
  retryCount?: number
  httpStatus?: number | null
  safeErrorCode?: string
  targetType?: string
}

/** Coarse buckets keep metric cardinality bounded; an exact size does not. */
export function sizeBucket(sizeBytes?: number): string {
  if (sizeBytes === undefined) return 'unknown'
  if (sizeBytes < 10 * 1024 * 1024) return '<10MiB'
  if (sizeBytes < 100 * 1024 * 1024) return '<100MiB'
  if (sizeBytes < 1024 * 1024 * 1024) return '<1GiB'
  return '>=1GiB'
}

export function toSafeUploadTelemetry(
  input: SafeUploadTelemetryInput,
): Record<string, string | number | null | undefined> {
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

function escapeForRegExp(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

/**
 * Replace the upload identifier in a URL with a placeholder.
 *
 * `basePath` is the deployment's tus base path, for example the value the app
 * already uses to build upload URLs. Passing it in is what keeps this helper
 * correct across deployments and keeps a route literal out of this file.
 */
export function redactUploadUrl(value: string, basePath: string): string {
  const normalized = `/${basePath.replace(/^\/+|\/+$/g, '')}/`
  const pattern = new RegExp(`${escapeForRegExp(normalized)}[^/?#]+`, 'g')
  return value.replace(pattern, `${normalized}[upload-id]`)
}

const BLOCKED_HEADERS = new Set([
  'authorization',
  'cookie',
  'set-cookie',
  'upload-metadata',
  'x-user-id',
  'x-project-id',
  'x-access',
  'x-access-token-id',
])

export function scrubUploadHeaders(headers: Record<string, unknown>): Record<string, unknown> {
  return Object.fromEntries(
    Object.entries(headers).map(([key, value]) => [
      key,
      BLOCKED_HEADERS.has(key.toLowerCase()) ? '[Filtered]' : value,
    ]),
  )
}
