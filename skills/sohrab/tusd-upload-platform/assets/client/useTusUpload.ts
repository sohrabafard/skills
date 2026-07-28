import { computed, readonly, ref, shallowRef } from 'vue'
import * as tus from 'tus-js-client'
import { isActiveUploadState, type UploadState } from './uploadStates'

/**
 * Reference implementation of one resumable upload in the browser.
 *
 * It imports only `vue`, `tus-js-client` and the canonical state list. It
 * contains no URL, no tenant, no credential and no application import, so it
 * can be dropped into any project and wired to that project's control plane.
 *
 * Everything the server decides arrives in `UploadPlanComponent`. The client
 * decides nothing about size, chunking, retry budget, metadata or resume
 * policy.
 */

/** One component of an upload plan, as returned by the control plane. */
export interface UploadPlanComponent {
  /** Where to create the tus resource. The response's Location header is the real resource URL. */
  tusCreationUrl?: string
  /** An already-created tus resource URL, when the plan pre-created one. */
  tusResourceUrl?: string
  /** The application's own identifier for this upload. Used to match a stored resume candidate. */
  appUploadId: string
  /** The size the server expects. Upload-Length must equal it exactly. */
  declaredSize: number
  /** Allowlisted metadata from the plan. The client adds nothing to it. */
  metadata?: Record<string, string | number | boolean | null | undefined>
  /** Chunk size chosen by the server from the smallest body cap on the path. */
  chunkSize?: number
  /** Retry budget in milliseconds, from the server. Jitter is applied here. */
  retryDelaysMs?: number[] | null
  expiresAt?: string
  allowTerminate?: boolean
  resumeAcrossSessions?: boolean
  storeFingerprintForResuming?: boolean
  removeFingerprintOnSuccess?: boolean
  withCredentials?: boolean
  headers?: Record<string, string>
  targetType?: string
}

export interface StartTusUploadInput {
  file: File
  plan: UploadPlanComponent
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

/**
 * Fallback retry budget in milliseconds, used only when the plan supplies
 * none. It is a budget, not a schedule: `jitteredRetryDelays` randomises each
 * value so that every client recovering from one shared outage does not retry
 * in lockstep and reproduce the load that caused it.
 */
const FALLBACK_RETRY_BUDGET_MS = [0, 1_000, 3_000, 5_000, 10_000]

const NON_RETRYABLE_STATUSES = new Set([401, 403, 404, 410])

/** Full jitter: each delay becomes a uniform random value in [0, delay]. */
function jitteredRetryDelays(budgetMs: number[]): number[] {
  return budgetMs.map((delay) => (delay <= 0 ? 0 : Math.floor(Math.random() * delay)))
}

function isBrowser(): boolean {
  return typeof window !== 'undefined'
}

function buildRequestId(): string {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID()
  }

  return `${Date.now()}-${Math.random().toString(16).slice(2)}`
}

function normalizeMetadata(metadata: UploadPlanComponent['metadata'] = {}): Record<string, string> {
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

function isOffline(): boolean {
  return typeof navigator !== 'undefined' && navigator.onLine === false
}

function assertPlanMatchesFile(plan: UploadPlanComponent, file: File): void {
  if (!plan.tusCreationUrl && !plan.tusResourceUrl) {
    throw new Error('UPLOAD_PLAN_MISSING_TUS_TARGET')
  }

  // Upload-Length must equal the declared size exactly. Failing here costs
  // nothing; failing at creation costs a round trip and a confusing status.
  if (file.size !== plan.declaredSize) {
    throw new Error('UPLOAD_SIZE_MISMATCH')
  }
}

/**
 * Decide whether a stored resume candidate belongs to this upload.
 *
 * Resuming `previousUploads[0]` unconditionally is the defect this guards
 * against: after a project or account switch, a fingerprint stored for a
 * different upload matches on file identity alone and resumes the wrong
 * upload. The application identifier must be carried in the metadata for
 * this to work, which is why it is always added below.
 */
function matchesThisUpload(
  candidate: tus.PreviousUpload,
  appUploadId: string,
): boolean {
  return candidate.metadata?.app_upload_id === appUploadId
}

export function useTusUpload() {
  const upload = shallowRef<tus.Upload | null>(null)
  const status = ref<UploadState>('idle')
  const progressPercent = ref(0)
  const bytesUploaded = ref(0)
  const bytesTotal = ref(0)
  const uploadUrl = ref<string | null>(null)
  const uploadExpiresAt = ref<string | null>(null)
  const appUploadId = ref<string | null>(null)
  const terminalError = shallowRef<Error | null>(null)
  const allowTerminate = ref(false)

  /**
   * Set when the retry decision stops because the device is offline. The tus
   * client emits its error path immediately afterwards; without this flag the
   * error handler overwrites the paused state with a terminal one, so going
   * offline reports permanent failure for an upload that is fully resumable.
   */
  const pausedByOffline = ref(false)

  const isActive = computed(() => isActiveUploadState(status.value))
  const canPause = computed(() => isActiveUploadState(status.value))
  const canResume = computed(() => status.value === 'paused')
  const canCancel = computed(
    () => Boolean(upload.value) && status.value !== 'completed-upload' && status.value !== 'cancelled',
  )

  async function start(input: StartTusUploadInput): Promise<void> {
    if (!isBrowser()) {
      throw new Error('Tus uploads must only start in the browser runtime.')
    }

    if (!tus.isSupported) {
      throw new Error('This browser does not support tus uploads.')
    }

    assertPlanMatchesFile(input.plan, input.file)

    status.value = 'creating-plan'
    terminalError.value = null
    pausedByOffline.value = false
    appUploadId.value = input.plan.appUploadId
    uploadExpiresAt.value = input.plan.expiresAt ?? null
    allowTerminate.value = input.plan.allowTerminate ?? false

    const shouldStoreForResume =
      input.plan.storeFingerprintForResuming ??
      Boolean(input.plan.resumeAcrossSessions && tus.canStoreURLs)

    const metadata = {
      ...normalizeMetadata(input.plan.metadata),
      // Carried so a stored resume candidate can be matched to this upload.
      app_upload_id: input.plan.appUploadId,
    }

    const clientUpload = new tus.Upload(input.file, {
      endpoint: input.plan.tusCreationUrl,
      uploadUrl: input.plan.tusResourceUrl,
      metadata,
      retryDelays: jitteredRetryDelays(input.plan.retryDelaysMs ?? FALLBACK_RETRY_BUDGET_MS),
      removeFingerprintOnSuccess: input.plan.removeFingerprintOnSuccess ?? true,
      storeFingerprintForResuming: shouldStoreForResume,
      uploadDataDuringCreation: false,
      withCredentials: input.plan.withCredentials ?? false,
      chunkSize: input.plan.chunkSize,
      async onBeforeRequest(req) {
        const freshHeaders = await Promise.resolve(input.getFreshHeaders?.() ?? {})
        const headers = {
          ...(input.plan.headers ?? {}),
          ...freshHeaders,
          'X-Request-Id': buildRequestId(),
        }

        for (const [key, value] of Object.entries(headers)) {
          req.setHeader(key, value)
        }
      },
      onAfterResponse(_req, res) {
        // The resource URL is the Location header of the creation response,
        // which tus-js-client exposes as `clientUpload.url`. A URL that came
        // from the plan is an application URL, not a tus resource.
        uploadUrl.value = clientUpload.url ?? input.plan.tusResourceUrl ?? null
        uploadExpiresAt.value = res.getHeader('Upload-Expires') ?? uploadExpiresAt.value
      },
      onUploadUrlAvailable() {
        uploadUrl.value = clientUpload.url ?? input.plan.tusResourceUrl ?? null
        if (uploadUrl.value) input.onUploadUrlAvailable?.(uploadUrl.value)
      },
      onProgress(uploaded, total) {
        if (status.value !== 'paused') status.value = 'uploading'
        pausedByOffline.value = false
        bytesUploaded.value = uploaded
        bytesTotal.value = total
        progressPercent.value = total > 0 ? Math.round((uploaded / total) * 100) : 0
      },
      onShouldRetry(error, _retryAttempt, options) {
        const statusCode = getStatusCode(error)

        if (isOffline()) {
          status.value = 'paused'
          pausedByOffline.value = true
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
        uploadUrl.value = clientUpload.url ?? input.plan.tusResourceUrl ?? null
        await input.onCompleted?.({
          appUploadId: input.plan.appUploadId,
          uploadUrl: uploadUrl.value,
          bytesUploaded: bytesUploaded.value,
          bytesTotal: bytesTotal.value,
        })
      },
      onError(error) {
        const normalized = error instanceof Error ? error : new Error(String(error))
        const statusCode = getStatusCode(error)

        if (pausedByOffline.value) {
          // Offline is a pause, not a failure. The server still holds the
          // offset, so resume() after reconnecting continues the upload.
          status.value = 'paused'
        } else if (statusCode === 410) {
          status.value = 'expired'
          terminalError.value = normalized
        } else {
          status.value = 'failed'
          terminalError.value = normalized
        }

        input.onError?.(normalized, {
          appUploadId: input.plan.appUploadId,
          statusCode,
          uploadUrlKnown: Boolean(uploadUrl.value),
          bytesUploaded: bytesUploaded.value,
          bytesTotal: bytesTotal.value,
          targetType: input.plan.targetType,
        })
      },
    })

    upload.value = clientUpload
    status.value = 'ready'

    if (shouldStoreForResume) {
      const previousUploads = await clientUpload.findPreviousUploads()
      const candidate = previousUploads.find((entry) =>
        matchesThisUpload(entry, input.plan.appUploadId),
      )
      if (candidate) {
        clientUpload.resumeFromPreviousUpload(candidate)
      }
    }

    status.value = 'uploading'
    clientUpload.start()
  }

  async function pause(): Promise<void> {
    if (!upload.value) return
    await upload.value.abort()
    pausedByOffline.value = false
    status.value = 'paused'
  }

  async function resume(): Promise<void> {
    if (!upload.value) return
    pausedByOffline.value = false
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
    pausedByOffline.value = false
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
