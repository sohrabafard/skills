import { defineBoot } from '#q-app/wrappers'

// Register this boot file as client-only in quasar.config when SSR is enabled.
// Keep browser-only upload code out of the server runtime.
export default defineBoot(() => {
  if (typeof window === 'undefined') {
    return
  }

  // This is intentionally lightweight. Prefer importing the upload composable
  // where it is needed instead of creating a global singleton by default.
})
