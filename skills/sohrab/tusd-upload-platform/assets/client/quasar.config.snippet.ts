// Adapt this snippet inside quasar.config.ts.
//
// Two rules it implements:
//  - upload boot files stay client-only so SSR never touches a browser global;
//  - the service worker never intercepts an upload request.
//
// The upload base path comes from configuration and has no fallback on
// purpose. A route literal here silently stops matching the day the
// deployment path changes, and the service worker then swallows PATCH
// requests, which looks like an upload bug and is not one.

const uploadBasePath = process.env.UPLOAD_BASE_PATH
if (!uploadBasePath) {
  throw new Error('UPLOAD_BASE_PATH must be set: the service-worker denylist is built from it.')
}

boot: [
  { path: 'uploads', server: false },
  { path: 'sentry', server: false },
],

pwa: {
  workboxMode: 'generateSW',
  extendGenerateSWOptions(cfg) {
    cfg.navigateFallbackDenylist = [
      new RegExp(`^${uploadBasePath.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`),
    ]

    // Any runtimeCaching rule added later must exclude the upload origin and
    // this path. If that needs finer control, switch to injectManifest and own
    // the exclusion in a custom service worker.
  },
}
