# SSR Auth and Session Patterns

Use this file when auth, session, protected-route, token-storage, refresh, or SSR request propagation is in scope.

## Prime rule

Do not assume one auth pattern.

Before editing auth code, inspect:

- login and logout endpoints
- refresh endpoint contract
- fetch wrappers and server boot files
- where access tokens and refresh capability live today
- whether the browser calls APIs directly, through a BFF, or through a trusted gateway

If the repo context is still ambiguous after inspection, ask a short clarifying question before changing the auth model.

## Decision order

1. Prefer a BFF or proxying backend-for-frontend when the app already has a server tier that can hold session state safely.
2. If the frontend must hold an access token but can rely on a backend for refresh and session state, prefer a token-mediating backend.
3. Use a server-only cookie-to-Authorization bridge only when the app truly performs backend API calls from the SSR layer and the repo already follows that pattern.
4. Use a gateway-backed bearer flow only when the platform already verifies bearer tokens at the edge and injects trusted downstream headers.
5. Use a browser-only OAuth public-client flow only when the repo actually uses direct OAuth in the browser and the identity provider supports Authorization Code + PKCE correctly.

## Supported patterns

### Pattern A: BFF or proxying backend-for-frontend

Best fit when:

- the frontend already has a trusted server tier
- the server can call upstream APIs on behalf of the browser
- the goal is to minimize token exposure in browser code

Frontend posture:

- browser uses `credentials: 'include'`
- BFF keeps session or tokens server-side
- browser never needs raw upstream tokens

### Pattern B: Token-mediating backend

Best fit when:

- the browser needs a short-lived access token for direct API calls
- refresh capability should stay server-side
- the app can exchange a cookie-backed session for a fresh access token

Frontend posture:

- refresh token stays outside browser JavaScript
- access token can stay in memory and be re-requested when needed
- avoid persistent browser storage when the backend can mint or return a new short-lived access token

### Pattern C: Server-only SSR cookie-to-header bridge

Best fit when:

- the SSR layer reads an HttpOnly cookie
- SSR requests to an upstream API must add `Authorization: Bearer <token>`
- the browser should never receive that token in page HTML or initial state

Safe boundary:

- do the mapping only in server code
- never serialize the token into the client bundle, route payload, or boot state

### Pattern D: Gateway-backed bearer flow

Best fit when:

- the browser sends an access token to a gateway
- the gateway verifies it and injects trusted downstream headers
- the repo already depends on a platform-wide trust model

Frontend posture:

- inspect the existing login, verify, and refresh flow first
- a common gateway-backed shape is: login or verify returns an access token to browser code, while refresh capability stays in an HttpOnly cookie
- in that shape, prefer keeping the access token in memory; treat `localStorage` as legacy storage, not the default recommendation
- inspect whether refresh needs only the cookie or also requires the current access token, device metadata, or request identifiers
- do not invent trusted internal headers from the browser
- pair with `$alaa-trust-gateway-auth` when gateway rules or downstream trust are relevant

### Pattern E: Browser-only OAuth public client

Best fit when:

- there is no BFF or token-mediating backend
- the identity provider supports Authorization Code + PKCE for browser apps
- the app really must call resource servers directly from browser code

Requirements:

- use Authorization Code + PKCE
- protect the redirect flow against CSRF
- keep redirect URIs exact
- treat refresh tokens as high-risk and rotate or sender-constrain them when the provider supports that

## Storage guidance

Preferred order:

1. Server-side session or BFF
2. Refresh outside browser JavaScript plus in-memory access token
3. Web Worker isolated storage when the app truly needs direct browser token handling
4. Persistent browser storage only as a legacy fallback with explicit risk acknowledgement

Practical rule:

- Prefer keeping the access token in memory, not `localStorage`.
- Treat `localStorage` or `sessionStorage` token storage as a legacy compromise, not the default recommendation.
- If the repo currently uses persistent storage, preserve behavior unless the user asks for a migration, but call out the security trade-off and the safer in-memory alternative.

## Silent refresh rules

- Use one refresh coordinator per browser tab or app shell.
- Serialize concurrent refresh attempts so five failing requests do not trigger five refresh calls.
- Retry original requests only after refresh succeeds.
- If refresh fails with an auth-expired result, clear in-memory auth state and route to the repo's logout or re-auth flow.
- Do not keep retrying forever.

Pattern: in-memory access token with serialized refresh

```js
let accessToken = null
let refreshPromise = null

export function setAccessToken(token) {
  accessToken = token || null
}

export async function getAccessToken(refresh) {
  if (accessToken) return accessToken

  if (!refreshPromise) {
    refreshPromise = refresh()
      .then((token) => {
        accessToken = token || null
        return accessToken
      })
      .finally(() => {
        refreshPromise = null
      })
  }

  return refreshPromise
}
```

## SSR-safe code patterns

Pattern: server-only cookie-to-header bridge

```js
export async function serverApiFetch({ request, fetch, url, init = {} }) {
  const token = request.cookies?.access_token
  const headers = new Headers(init.headers || {})

  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  return fetch(url, { ...init, headers })
}
```

Pattern: browser session fetch through a BFF

```js
export function bffFetch(url, init = {}) {
  return fetch(url, {
    ...init,
    credentials: 'include',
    headers: {
      Accept: 'application/json',
      ...(init.headers || {}),
    },
  })
}
```

## Anti-patterns

- Assuming every SSR app uses cookie-to-header mapping
- Reading or writing auth state in `localStorage` from code that also runs during SSR
- Serializing tokens into SSR HTML, boot payloads, or `window.__INITIAL_STATE__`
- Keeping long-lived access tokens in persistent browser storage by default
- Starting multiple refresh calls in parallel when one would do
- Trusting `X-User-Id`, `X-Project-Id`, or similar internal headers from the browser
- Rewriting the auth model during an unrelated bug fix

## Practical review checklist

- Which exact component owns the browser auth state today?
- Which endpoint issues the initial access token?
- Which endpoint refreshes it, and what storage does that refresh depend on?
- Are SSR requests using request-scoped auth helpers, or leaking state through globals?
- Does logout clear in-memory state, cookies, and cached protected data?
- Do protected-route redirects behave the same on first SSR load and client navigation?

## Pairing guidance

- Ala gateway, trusted headers, refresh-cookie plus bearer-token flow, or tenant-context trust:
  - Pair with `$alaa-trust-gateway-auth`
- Exact Quasar SSR boot-file or `preFetch` wiring:
  - Pair with `$alaa-quasar-app-vite-v3`
- Frontend-facing auth error envelopes, cache headers, or pagination around protected data:
  - Also load `45-api-and-data-shaping.md`

## Useful standards and references

- OAuth browser-based applications draft:
  - [https://datatracker.ietf.org/doc/draft-ietf-oauth-browser-based-apps/](https://datatracker.ietf.org/doc/draft-ietf-oauth-browser-based-apps/)
- OWASP HTML5 storage guidance:
  - [https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html)
