// Adapt this helper to the project's Sentry initialization.
// The rule it implements: no upload URL, auth header, cookie, raw
// Upload-Metadata or trusted internal header value leaves the browser.
//
// The upload base path is a parameter. A hardcoded path silently stops
// matching the day the deployment's path changes, and the redaction then
// passes real URLs through while still looking correct.
import { redactUploadUrl, scrubUploadHeaders } from './uploadTelemetry'

export function makeBeforeSendUploadSafe(uploadBasePath: string) {
  return function beforeSendUploadSafe(event: any) {
    for (const request of [event?.request, event?.contexts?.request]) {
      if (!request) continue

      if (typeof request.url === 'string') {
        request.url = redactUploadUrl(request.url, uploadBasePath)
      }

      if (request.headers) {
        request.headers = scrubUploadHeaders(request.headers)
      }
    }

    return event
  }
}
