// Adapt this helper to the project's Sentry initialization.
// The important rule is to remove raw upload URLs, auth headers, cookies, and raw Upload-Metadata.
import { redactUploadUrl } from './uploadTelemetry'

export function beforeSendUploadSafe(event: any) {
  for (const request of [event?.request, event?.contexts?.request]) {
    if (!request) continue

    if (typeof request.url === 'string') {
      request.url = redactUploadUrl(request.url)
    }

    const headers = request.headers
    if (!headers) continue

    for (const key of Object.keys(headers)) {
      const normalized = key.toLowerCase()
      if (normalized === 'authorization' || normalized === 'cookie' || normalized === 'upload-metadata') {
        headers[key] = '[Filtered]'
      }
    }
  }

  return event
}
