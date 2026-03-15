import { computed, ref, shallowRef } from 'vue'
import * as Sentry from '@sentry/vue'
import * as tus from 'tus-js-client'

type TusUploadStatus =
  | 'idle'
  | 'starting'
  | 'uploading'
  | 'paused'
  | 'completed'
  | 'cancelled'
  | 'error'

interface TusUploadSession {
  endpoint?: string
  uploadUrl?: string
  appUploadId: string
  correlationId: string
  expiresAt?: string
  allowTerminate?: boolean
  headers?: Record<string, string>
  metadata?: Record<string, string | number | boolean>
  retryDelays?: number[]
  chunkSize?: number
  uploadDataDuringCreation?: boolean
  storeFingerprintForResuming?: boolean
  removeFingerprintOnSuccess?: boolean
  withCredentials?: boolean
  targetType?: string
  tenantId?: string
}

interface StartTusUploadInput {
  file: File
  session: TusUploadSession
  getFreshHeaders?: () => Promise<Record<string, string>> | Record<string, string>
}

interface TusErrorLike extends Error {
  originalResponse?: {
    getStatus?: () => number
    getHeader?: (name: string) => string | null
  }
}

const DEFAULT_RETRY_DELAYS = [0, 1000, 3000, 5000, 10000, 20000]
const NON_RETRYABLE_STATUSES = new Set([401, 403, 404, 410])

function isBrowser(): boolean {
  return typeof window !== 'undefined'
}

function buildRequestId(): string {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID()
  }

  return `${Date.now()}-${Math.random().toString(16).slice(2)}`
}

function normalizeMetadata(
  metadata: TusUploadSession['metadata'] = {},
): Record<string, string> {
  return Object.fromEntries(
    Object.entries(metadata)
      .filter(([, value]) => value !== undefined && value !== null)
      .map(([key, value]) => [key, String(value)]),
  )
}

function getStatusCode(error: unknown): number | null {
  if (!error || typeof error !== 'object') {
    return null
  }

  const candidate = error as TusErrorLike
  return candidate.originalResponse?.getStatus?.() ?? null
}

function sanitizeUploadContext(input: StartTusUploadInput, statusCode: number | null) {
  return {
    appUploadId: input.session.appUploadId,
    correlationId: input.session.correlationId,
    expiresAt: input.session.expiresAt,
    targetType: input.session.targetType,
    tenantId: input.session.tenantId,
    fileSize: input.file.size,
    fileType: input.file.type,
    statusCode,
  }
}

export function useTusUpload() {
  const upload = shallowRef<tus.Upload | null>(null)
  const status = ref<TusUploadStatus>('idle')
  const progressPercent = ref(0)
  const bytesUploaded = ref(0)
  const bytesTotal = ref(0)
  const uploadUrl = ref<string | null>(null)
  const uploadExpiresAt = ref<string | null>(null)
  const appUploadId = ref<string | null>(null)
  const terminalError = shallowRef<Error | null>(null)
  const allowTerminate = ref(false)

  const isActive = computed(() => status.value === 'starting' || status.value === 'uploading')

  async function start(input: StartTusUploadInput): Promise<void> {
    if (!isBrowser()) {
      throw new Error('Tus uploads must only start in the browser runtime.')
    }

    if (!tus.isSupported) {
      throw new Error('This browser does not support tus uploads.')
    }

    status.value = 'starting'
    terminalError.value = null
    appUploadId.value = input.session.appUploadId
    uploadExpiresAt.value = input.session.expiresAt ?? null

    const storeFingerprintForResuming =
      input.session.storeFingerprintForResuming ?? tus.canStoreURLs

    allowTerminate.value = input.session.allowTerminate ?? false

    const clientUpload = new tus.Upload(input.file, {
      endpoint: input.session.endpoint,
      uploadUrl: input.session.uploadUrl,
      metadata: normalizeMetadata(input.session.metadata),
      retryDelays: input.session.retryDelays ?? DEFAULT_RETRY_DELAYS,
      removeFingerprintOnSuccess: input.session.removeFingerprintOnSuccess ?? true,
      storeFingerprintForResuming,
      uploadDataDuringCreation: input.session.uploadDataDuringCreation ?? false,
      withCredentials: input.session.withCredentials ?? false,
      chunkSize: input.session.chunkSize,
      async onBeforeRequest(req) {
        const freshHeaders = await Promise.resolve(input.getFreshHeaders?.() ?? {})
        const headers = {
          ...(input.session.headers ?? {}),
          ...freshHeaders,
        }

        for (const [key, value] of Object.entries(headers)) {
          req.setHeader(key, value)
        }

        req.setHeader('X-Correlation-Id', input.session.correlationId)
        req.setHeader('X-Request-Id', buildRequestId())
      },
      onAfterResponse(_req, res) {
        uploadUrl.value = clientUpload.url ?? input.session.uploadUrl ?? null
        uploadExpiresAt.value = res.getHeader('Upload-Expires') ?? uploadExpiresAt.value
      },
      onProgress(uploaded, total) {
        status.value = 'uploading'
        bytesUploaded.value = uploaded
        bytesTotal.value = total
        progressPercent.value = total > 0 ? Math.round((uploaded / total) * 100) : 0
      },
      onError(error) {
        status.value = 'error'
        terminalError.value = error instanceof Error ? error : new Error(String(error))

        const statusCode = getStatusCode(error)
        Sentry.withScope((scope) => {
          scope.setTag('feature', 'tus-upload')
          scope.setTag('app_upload_id', input.session.appUploadId)
          scope.setTag('correlation_id', input.session.correlationId)
          if (input.session.targetType) {
            scope.setTag('target_type', input.session.targetType)
          }
          if (statusCode !== null) {
            scope.setTag('http_status', String(statusCode))
          }
          scope.setContext('tus_upload', sanitizeUploadContext(input, statusCode))
          Sentry.captureException(error)
        })
      },
      onUploadUrlAvailable() {
        uploadUrl.value = clientUpload.url ?? input.session.uploadUrl ?? null
      },
      onSuccess() {
        status.value = 'completed'
        progressPercent.value = 100
        bytesUploaded.value = input.file.size
        bytesTotal.value = input.file.size
        uploadUrl.value = clientUpload.url ?? input.session.uploadUrl ?? null
      },
      onShouldRetry(error, _retryAttempt, options) {
        if (typeof navigator !== 'undefined' && navigator.onLine === false) {
          return false
        }

        const statusCode = getStatusCode(error)
        if (statusCode !== null && NON_RETRYABLE_STATUSES.has(statusCode)) {
          return false
        }

        if (statusCode !== null && statusCode >= 400 && statusCode < 500) {
          return statusCode === 409 || statusCode === 423
        }

        return options.retryDelays != null
      },
    })

    upload.value = clientUpload

    if (storeFingerprintForResuming) {
      const previousUploads = await clientUpload.findPreviousUploads()
      if (previousUploads.length > 0) {
        clientUpload.resumeFromPreviousUpload(previousUploads[0])
      }
    }

    clientUpload.start()
  }

  async function pause(): Promise<void> {
    if (!upload.value) {
      return
    }

    await upload.value.abort()
    status.value = 'paused'
  }

  async function resume(): Promise<void> {
    if (!upload.value) {
      return
    }

    status.value = 'uploading'
    upload.value.start()
  }

  async function cancel(options?: { terminate?: boolean }): Promise<void> {
    if (!upload.value) {
      return
    }

    const shouldTerminate = options?.terminate === true && allowTerminate.value
    await upload.value.abort(shouldTerminate)
    status.value = 'cancelled'
  }

  function reset(): void {
    upload.value = null
    status.value = 'idle'
    progressPercent.value = 0
    bytesUploaded.value = 0
    bytesTotal.value = 0
    uploadUrl.value = null
    uploadExpiresAt.value = null
    appUploadId.value = null
    terminalError.value = null
    allowTerminate.value = false
  }

  return {
    appUploadId,
    bytesTotal,
    bytesUploaded,
    cancel,
    isActive,
    pause,
    progressPercent,
    reset,
    resume,
    start,
    status,
    terminalError,
    uploadExpiresAt,
    uploadUrl,
  }
}
