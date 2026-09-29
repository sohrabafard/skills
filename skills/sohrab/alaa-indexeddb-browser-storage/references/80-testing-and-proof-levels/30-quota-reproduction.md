## Debug surfaces per engine

**Chrome and Edge** — DevTools → Application → IndexedDB; Application → Storage for usage and "Clear site
data"; `navigator.storage.estimate()` from the console. **Firefox** — DevTools → Storage Inspector; the
persistent-storage prompt appears here and nowhere else, so Firefox is the lane that exercises the prompt
path. **Safari and WebKit** — Web Inspector → Storage; whether recent Safari moved some surfaces to
Develop → Inspect Apps and Devices is `unverified as of 2026-07-28`, so look there before concluding data
is absent.

