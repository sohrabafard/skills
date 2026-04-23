# Source Map

Use this file when annotation guidance depends on current Vue, Quasar, Vite, SSR, or browser behavior.

## Source Priority

Prefer sources in this order:

1. The code being annotated and nearby repo-local conventions.
2. Official docs for the surface being documented:
   - Vue docs: https://vuejs.org/
   - Vue release policy: https://vuejs.org/about/releases
   - Quasar docs: https://quasar.dev/
   - Vite docs: https://vite.dev/
   - MDN Web Docs for browser APIs: https://developer.mozilla.org/
3. Official package release notes or migration guides when a comment depends on current behavior.
4. Community posts, StackOverflow answers, and issue comments only as troubleshooting context.

## Freshness Triggers

Re-check official docs before writing or updating comments that mention:

- "currently", "latest", "deprecated", "removed", "safe", "unsupported", or "browser behavior"
- Vue lifecycle, hydration, reactivity, watcher, Suspense, or SSR behavior
- Quasar SSR, PWA, boot-file, or platform-mode semantics
- Vite transform, import, env, asset URL, or dev-server behavior
- Web APIs with security or compatibility sensitivity, such as storage, cookies, service workers, BroadcastChannel, WebOTP, WebRTC, or media APIs

## Community Troubleshooting Boundary

Do not cite community material inside JSDoc or inline comments.

Use community material only to form a hypothesis, then verify the actual behavior against the repo, official docs, or a focused local reproduction before writing the comment.

## Small Anti-Pattern

Anti-pattern:

```js
// Workaround for Vue bug from StackOverflow.
```

Better:

```js
// Keep this client-only because SSR cannot read browser storage.
```

The second comment explains the durable constraint without pinning the code to an unverified external anecdote.
