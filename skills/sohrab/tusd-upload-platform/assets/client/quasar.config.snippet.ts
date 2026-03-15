// Adapt this snippet inside quasar.config.ts.
// The upload boot file stays client-only for SSR, and PWA rules must keep
// upload paths out of service-worker fallbacks and any custom runtime caching.

boot: [
  { path: 'uploads', server: false },
  { path: 'sentry', server: false },
],

pwa: {
  workboxMode: 'generateSW',
  extendGenerateSWOptions(cfg) {
    cfg.navigateFallbackDenylist = [
      /^\/files\//,
    ]

    // If you add runtimeCaching rules later, keep the upload origin and path
    // out of those rules. If you need finer control, switch to injectManifest
    // and own the exclusion in your custom service worker.
  },
}
