import { computed, readonly, ref, shallowRef } from 'vue'
import * as tus from 'tus-js-client'

export type TusUploadStatus =
  | 'idle'
  | 'creating-session'
  | 'ready'
  | 'uploading'
  | 'paused'
  | 'retrying'
  | 'completed-upload'
  | 'failed'
  | 'cancelled'

export interface TusUploadSession {
  endpoint?: string
  uploadUrl?: string
  appUploadId: string
  expiresAt?: string
  allowTerminate?: boolean
  headers?: Record<string, string>
  metadata?: Record<string, string | number | boolean | null | undefined>
  retryDelays?: number[] | null
  chunkSize?: number
  uploadDataDuringCreation?: boolean
  storeFingerprintForResuming?: boolean
  removeFingerprintOnSuccess?: boolean
  resumeAcrossSessions?: boolean
  withCredentials?: boolean
  targetType?: string
  maxSizeBytes?: number
}

export interface StartTusUploadInput {
  file: File
  session: TusUploadSession
  getFreshHeaders?: () => Promise<Record<string, string>> | Record<string, string>
  onUploadUrlAvailable?: (url: string) => void
  onCompleted?: (result: TusUploadResult) => Promise<void> | void
  onError?: (error: Error, context: TusUploadErrorContext) => void
}

export interface TusUploadResult {
  appUploadId: string
  uploadUrl: string | null
  bytesUploaded: number
  bytesTotal: number
}

export interface TusUploadErrorContext {
  appUploadId: string
  statusCode: number | null
  uploadUrlKnown: boolean
  bytesUploaded: number
  bytesTotal: number
  targetType?: string
}

interface TusErrorLike extends Error {
  originalResponse?: {
    getStatus?: () => number
    getHeader?: (name: string) => string | null | undefined
  }
}

const DEFAULT_RETRY_DELAYS = [0, 1000, 3000, 5000, 10000]
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

function normalizeMetadata(metadata: TusUploadSession['metadata'] = {}): Record<string, string> {
  return Object.fromEntries(
    Object.entries(metadata)
      .filter(([, value]) => value !== undefined && value !== null)
      .map(([key, value]) => [key, String(value)]),
  )
}

function getStatusCode(error: unknown): number | null {
  if (!error || typeof error !== 'object') return null
  const candidate = error as TusErrorLike
  return candidate.originalResponse?.getStatus?.() ?? null
}

function assertSafeSession(session: TusUploadSession, file: File): void {
  if (!session.endpoint && !session.uploadUrl) {
    throw new Error('UPLOAD_SESSION_MISSING_TUS_TARGET')
  }

  if (session.maxSizeBytes !== undefined && file.size > session.maxSizeBytes) {
    throw new Error('UPLOAD_SIZE_EXCEEDED')
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

  const isActive = computed(() => status.value === 'uploading' || status.value === 'retrying')
  const canPause = computed(() => status.value === 'uploading' || status.value === 'retrying')
  const canResume = computed(() => status.value === 'paused')
  const canCancel = computed(() => Boolean(upload.value) && status.value !== 'completed-upload' && status.value !== 'cancelled')

  async function start(input: StartTusUploadInput): Promise<void> {
    if (!isBrowser()) {
      throw new Error('Tus uploads must only start in the browser runtime.')
    }

    if (!tus.isSupported) {
      throw new Error('This browser does not support tus uploads.')
    }

    assertSafeSession(input.session, input.file)

    status.value = 'creating-session'
    terminalError.value = null
    appUploadId.value = input.session.appUploadId
    uploadExpiresAt.value = input.session.expiresAt ?? null
    allowTerminate.value = input.session.allowTerminate ?? false

    const shouldStoreForResume =
      input.session.storeFingerprintForResuming ??
      Boolean(input.session.resumeAcrossSessions && tus.canStoreURLs)

    const clientUpload = new tus.Upload(input.file, {
      endpoint: input.session.endpoint,
      uploadUrl: input.session.uploadUrl,
      metadata: normalizeMetadata(input.session.metadata),
      retryDelays: input.session.retryDelays ?? DEFAULT_RETRY_DELAYS,
      removeFingerprintOnSuccess: input.session.removeFingerprintOnSuccess ?? true,
      storeFingerprintForResuming: shouldStoreForResume,
      uploadDataDuringCreation: input.session.uploadDataDuringCreation ?? false,
      withCredentials: input.session.withCredentials ?? false,
      chunkSize: input.session.chunkSize,
      async onBeforeRequest(req) {
        const freshHeaders = await Promise.resolve(input.getFreshHeaders?.() ?? {})
        const headers = {
          ...(input.session.headers ?? {}),
          ...freshHeaders,
          'X-Request-Id': buildRequestId(),
        }

        for (const [key, value] of Object.entries(headers)) {
          req.setHeader(key, value)
        }
      },
      onAfterResponse(_req, res) {
        uploadUrl.value = clientUpload.url ?? input.session.uploadUrl ?? null
        uploadExpiresAt.value = res.getHeader('Upload-Expires') ?? uploadExpiresAt.value
      },
      onUploadUrlAvailable() {
        uploadUrl.value = clientUpload.url ?? input.session.uploadUrl ?? null
        if (uploadUrl.value) input.onUploadUrlAvailable?.(uploadUrl.value)
      },
      onProgress(uploaded, total) {
        status.value = 'uploading'
        bytesUploaded.value = uploaded
        bytesTotal.value = total
        progressPercent.value = total > 0 ? Math.round((uploaded / total) * 100) : 0
      },
      onShouldRetry(error, _retryAttempt, options) {
        const statusCode = getStatusCode(error)

        if (typeof navigator !== 'undefined' && navigator.onLine === false) {
          status.value = 'paused'
          return false
        }

        if (statusCode !== null && NON_RETRYABLE_STATUSES.has(statusCode)) {
          return false
        }

        status.value = 'retrying'

        if (statusCode !== null && statusCode >= 400 && statusCode < 500) {
          return statusCode === 409 || statusCode === 423
        }

        return Boolean(options.retryDelays)
      },
      async onSuccess() {
        status.value = 'completed-upload'
        progressPercent.value = 100
        bytesUploaded.value = input.file.size
        bytesTotal.value = input.file.size
        uploadUrl.value = clientUpload.url ?? input.session.uploadUrl ?? null
        await input.onCompleted?.({
          appUploadId: input.session.appUploadId,
          uploadUrl: uploadUrl.value,
          bytesUploaded: bytesUploaded.value,
          bytesTotal: bytesTotal.value,
        })
      },
      onError(error) {
        const normalized = error instanceof Error ? error : new Error(String(error))
        status.value = 'failed'
        terminalError.value = normalized
        input.onError?.(normalized, {
          appUploadId: input.session.appUploadId,
          statusCode: getStatusCode(error),
          uploadUrlKnown: Boolean(uploadUrl.value),
          bytesUploaded: bytesUploaded.value,
          bytesTotal: bytesTotal.value,
          targetType: input.session.targetType,
        })
      },
    })

    upload.value = clientUpload
    status.value = 'ready'

    if (shouldStoreForResume) {
      const previousUploads = await clientUpload.findPreviousUploads()
      if (previousUploads.length > 0) {
        clientUpload.resumeFromPreviousUpload(previousUploads[0])
      }
    }

    status.value = 'uploading'
    clientUpload.start()
  }

  async function pause(): Promise<void> {
    if (!upload.value) return
    await upload.value.abort()
    status.value = 'paused'
  }

  async function resume(): Promise<void> {
    if (!upload.value) return
    status.value = 'uploading'
    upload.value.start()
  }

  async function cancel(options?: { terminate?: boolean }): Promise<void> {
    if (!upload.value) return
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
    upload: readonly(upload),
    status: readonly(status),
    progressPercent: readonly(progressPercent),
    bytesUploaded: readonly(bytesUploaded),
    bytesTotal: readonly(bytesTotal),
    uploadUrl: readonly(uploadUrl),
    uploadExpiresAt: readonly(uploadExpiresAt),
    appUploadId: readonly(appUploadId),
    terminalError: readonly(terminalError),
    allowTerminate: readonly(allowTerminate),
    isActive,
    canPause,
    canResume,
    canCancel,
    start,
    pause,
    resume,
    cancel,
    reset,
  }
}
