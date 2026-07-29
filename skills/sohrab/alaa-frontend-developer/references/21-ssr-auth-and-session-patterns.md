# SSR Auth and Session Patterns

Read this before touching auth, session, protected-route, token-storage, refresh or SSR request
propagation. This file owns the frontend posture only. Gateway verification, trusted headers and
downstream trust are `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`)
`references/10-verification-and-ingress.md` and `references/20-claims-headers-and-sentinels.md`.

## Prime rule

Do not assume one auth pattern. Before editing, inspect the login and logout endpoints, the refresh
contract, the fetch wrappers and server boot files, where the access token and the refresh capability
live today, and whether the browser calls APIs directly, through a BFF, or through a gateway. If the model
is still ambiguous after inspection, ask before changing it.

## Decision order

1. A BFF or proxying backend-for-frontend when a trusted server tier already exists.
2. A token-mediating backend when the browser needs a short-lived access token but refresh can stay
   server-side.
3. A server-only cookie-to-`Authorization` bridge when the SSR layer itself calls the API and the repo
   already does this.
4. A gateway-backed bearer flow when the platform already verifies bearer tokens at the edge.
5. A browser-only OAuth public client with Authorization Code + PKCE only when the repo genuinely has no
   server tier and the provider supports PKCE correctly.

## The five postures

**A — BFF / proxying backend.** Browser uses `credentials: 'include'`; the BFF holds session or tokens;
the browser never sees an upstream token.

**B — Token-mediating backend.** Refresh capability stays outside browser JavaScript; the access token
lives in memory and is re-requested when needed.

**C — Server-only cookie-to-header bridge.** The mapping happens in server code only. The token is never
serialized into page HTML, a route payload, boot state, or `window.__INITIAL_STATE__`.

**D — Gateway-backed bearer.** Login or verify returns an access token to browser code while refresh
capability stays in an HttpOnly cookie. Inspect whether refresh needs only the cookie or also the current
access token, device metadata, or a request id. Never invent a trusted internal header in the browser.

**E — Browser-only OAuth public client.** Authorization Code + PKCE, CSRF protection on the redirect,
exact redirect URIs, refresh tokens rotated or sender-constrained where the provider supports it.

## Token storage — constraints, not preferences

- Gate 4 in `SKILL.md` governs where the access token lives. This file owns what to do about the ones
  already written: where a persistent write exists today, open a tracked migration item naming the file,
  the endpoint that mints the token, and the owning maintainer, before this change merges. Preserving the
  existing behaviour without opening that item is how the write survives another year.
- Refresh capability stays outside browser JavaScript wherever the backend can mint a new access token.
- Any other browser-side persistence question — what may be stored, quota, eviction, purge, multi-tab
  writes — belongs to `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`)
  `references/61-authority-boundary.md` and `references/62-poisoning-and-purge.md`. A token is not an
  exception to that skill; it is simply not stored at all.

## Silent refresh

One refresh coordinator per tab or app shell. Concurrent refresh attempts are serialized, so five failing
requests trigger one refresh call. Original requests are retried only after refresh succeeds. On an
auth-expired result, in-memory auth state is cleared and the repo's re-auth flow runs.

How many attempts, at what interval, and under which deadline are not decided here: `/alaa-reliability-sla`
(`$alaa-reliability-sla`) `references/20-retries.md` and `references/10-deadlines-and-timeouts.md` own the
retry and timeout policy; `46-resilience-and-degradation.md` carries the client-side expression.

```ts
let accessToken: string | null = null
let refreshPromise: Promise<string | null> | null = null

export function setAccessToken(token: string | null): void {
  accessToken = token ?? null
}

export async function getAccessToken(refresh: () => Promise<string | null>): Promise<string | null> {
  if (accessToken) return accessToken
  refreshPromise ??= refresh()
    .then((token) => (accessToken = token ?? null))
    .finally(() => { refreshPromise = null })
  return refreshPromise
}
```

## SSR-safe bridge

```ts
export async function serverApiFetch(
  { request, fetch, url, init = {} }: ServerFetchArgs,
): Promise<Response> {
  const token = request.cookies?.access_token
  const headers = new Headers(init.headers ?? {})
  if (token) headers.set('Authorization', `Bearer ${token}`)
  return fetch(url, { ...init, headers })
}
```

## Anti-patterns

Assuming every SSR app bridges cookies to headers; reading or writing auth state in `localStorage` from
code that also runs during SSR; serializing a token into SSR HTML or boot payload; parallel refresh calls;
trusting `X-User-Id`, `X-Project-Id` or a similar internal header sent by the browser; rewriting the auth
model during an unrelated fix.

## Review checklist

Which component owns browser auth state; which endpoint mints the token and which refreshes it and on
what storage; whether SSR requests use request-scoped helpers rather than globals; whether logout clears
in-memory state, cookies and cached protected data; whether a protected-route redirect behaves the same on
first SSR load and on client navigation.

## Standards

- OAuth 2.0 for Browser-Based Applications — `draft-ietf-oauth-browser-based-apps-26`, submitted to the
  IESG and in the RFC Editor queue as a Best Current Practice; still an Internet-Draft, not yet an RFC.
  [datatracker.ietf.org](https://datatracker.ietf.org/doc/draft-ietf-oauth-browser-based-apps/) — read:
  2026-07-28. Its recommendation order still matches the decision order above.
- OWASP HTML5 Security Cheat Sheet, storage section:
  [cheatsheetseries.owasp.org](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html)
  — read: unverified as of 2026-07-28.
