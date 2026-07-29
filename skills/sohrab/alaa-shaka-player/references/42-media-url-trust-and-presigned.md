# Media URL trust: presigned URLs, tokens and share links

A presigned media URL is a **bounded, named, expiring read grant**. It is not a transport detail and
not a component prop. This file states the player-side binding of that fact; the grant itself, its TTL
and its `STORAGE_*` contract are owned by `/alaa-minio-object-storage`
(`$alaa-minio-object-storage`), `references/60-presigned-urls-and-delivery.md` and
`/alaa-arvan-object-storage` (`$alaa-arvan-object-storage`). The trust property — that a
client-supplied opaque value carries no trust — is owned by `/alaa-trust-gateway-auth`
(`$alaa-trust-gateway-auth`). Threat classes are `/alaa-security-review` (`$alaa-security-review`).

## The sharpest rule, and it is this skill's own

**The grant's remaining TTL must exceed the longest expected single segment request, and renewal
happens inside the networking request filter, not in component state.**

Both halves matter:

- **TTL versus request length, not versus session length.** A manifest is fetched once; segments are
  fetched continuously for the whole session. A grant that covers "the lecture" is the wrong unit —
  what must fit inside the remaining TTL is one segment request *including its retries*, which is
  bounded by `retryParameters.timeout × maxAttempts` plus the backoff sum. Compute that number from
  the values in `35-unstable-networks-and-resilience.md` and require the TTL to exceed it with margin.
- **Renewal in the filter, not in state.** Request filters run **on every retry attempt** since v5.0
  and `request.attempt` tells you which attempt you are on. That is the only place in the player where
  a credential can be refreshed *between* the failure and the next attempt. A component that holds a
  token in a `ref` and re-renders cannot reach the in-flight retry loop at all.

## What carries a credential in a player

| Surface | Risk |
|---|---|
| A presigned **manifest** URL | Passed to `load()`. Anyone who reads it can fetch the manifest until it expires. |
| Presigned **segment** URLs inside the manifest | Frequently a different TTL from the manifest's. Expiry mid-session is the common production incident. |
| The **licence** request | Carries the bearer token that proves entitlement. |
| `request.headers['Authorization']` | Visible to any code that registers a later filter. |
| `error.data` on a network error | **Contains the failing URI and its query string.** Never `JSON.stringify` a Shaka error into the DOM, a log line, a Sentry breadcrumb, or a bug report. |
| `getStats()` / `downloadfailed` payloads | `e.request.uris` is the presigned URL. Record the request **type** and status, never the URI. |
| A **share link** `/watch/<id>?t=123.4` | Safe only while `<id>` resolves through an authorization check. If `<id>` ever resolves to a presigned asset, the share link is a transferred read grant. |
| A **stored offline asset** | `50-offline-and-in-app-download.md`: the stored manifest can retain the URLs it was fetched from. A presigned URL persisted into IndexedDB outlives the session that authorised it. |
| A **component prop** | `extraHeaders` or `manifestUri` as a `defineProps` field puts the credential into the Vue devtools component tree and into any component-tree dump. |

## The rules

1. A token or a signature reaches the player **only** through a request filter that calls a getter. No
   token is a component prop, a `defineProps` field, a Pinia state field, or a captured closure value.
2. Every media URL is fetched over `https`. Set `networking.forceHTTPS` rather than relying on the
   manifest.
3. **Never log or render a Shaka error object.** Log `code`, `category`, `severity` and, for
   `BAD_HTTP_STATUS`, `data[1]` (the status) and `data[4]` (the `RequestType`). Nothing else.
4. Compute the required minimum TTL from the retry budget, assert it in a test, and fail the build if
   the configured TTL is below it. "Long enough" is not a checkable condition; a number compared
   against a number is.
5. If a stored offline asset must survive longer than any grant, the offline networking filter signs
   at **download** time and playback of stored content never re-fetches from the origin. If it does
   re-fetch, treat the stored manifest as credential-bearing data and read
   `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`),
   `references/60-data-classification.md`.
6. A share link carries an **asset identifier and a timestamp**, never a signature. Resolution to a
   playable URL happens server-side, after an authorization check.

## Working snippet — signing in the filter, with a TTL assertion

```ts
import type { ShakaNamespace, ShakaPlayer } from "./shakaTypes";

/** A read grant with a known expiry. The TTL contract lives with the object-storage skill;
 *  this type is only how the player consumes it. */
export interface MediaGrant {
  readonly token: string;
  readonly expiresAtMs: number;
}

/** The longest a single segment request can legitimately take, including retries.
 *  Derived from the retry budget - not guessed. */
export function worstCaseRequestMs(retry: {
  maxAttempts: number; timeout: number; baseDelay: number; backoffFactor: number;
}): number {
  let backoffSum = 0;
  for (let attempt = 1; attempt < retry.maxAttempts; attempt += 1) {
    // fuzzFactor 0.5 can extend a delay by 50%.
    backoffSum += retry.baseDelay * Math.pow(retry.backoffFactor, attempt - 1) * 1.5;
  }
  return retry.maxAttempts * retry.timeout + backoffSum;
}

/** Fails loudly at configure time rather than silently at minute 40 of a lecture. */
export function assertGrantOutlivesRequests(
  grant: MediaGrant,
  retry: Parameters<typeof worstCaseRequestMs>[0],
  marginMs = 30_000
): void {
  const remaining = grant.expiresAtMs - Date.now();
  const required = worstCaseRequestMs(retry) + marginMs;
  if (remaining < required) {
    throw new Error(
      `Media grant expires in ${remaining}ms but one segment request can take ${required}ms. ` +
      `Request a longer grant before calling load().`
    );
  }
}

/** The only place a credential enters the player. Reads a GETTER so that a refresh
 *  during a retry loop is visible to the very next attempt. */
export function installMediaAuth(
  shaka: ShakaNamespace,
  player: ShakaPlayer,
  getGrant: () => Promise<MediaGrant>
): void {
  const net = player.getNetworkingEngine();
  const T = shaka.net.NetworkingEngine.RequestType;

  net.registerRequestFilter(async (type, request) => {
    if (type !== T.SEGMENT && type !== T.MANIFEST && type !== T.LICENSE) return;
    const grant = await getGrant();          // may refresh; runs on EVERY attempt
    request.headers["Authorization"] = `Bearer ${grant.token}`;
  });

  // Telemetry that cannot leak the grant: type and status only, never the URI.
  player.addEventListener("downloadfailed", (e: any) => {
    reportDownloadFailure({ requestType: e.requestType, httpStatus: e.httpResponseCode });
  });
}
```

## Reviewer checklist

- [ ] `grep -rn "defineProps" src | grep -i -E "header|token|auth|signed"` returns nothing.
- [ ] `grep -rn "JSON.stringify" src` returns no hit whose argument is an error or an event detail.
- [ ] Every `registerRequestFilter` call in the repository reads a getter, not a captured string.
- [ ] The offline `Storage` engine has its own filter (`40-networking-engine-and-filters.md`).
- [ ] The TTL assertion above, or its equivalent, runs before the first `load()`.
- [ ] Share-link generation emits an identifier and a timestamp, and no signature.

**Best practice.** Give the player a `getGrant()` function and nothing else. The player then cannot
hold a stale credential, because it never holds one at all.
**Common mistake.** Passing `headers?: Record<string, string>` as a Vue prop into the wrapper. It puts
a bearer token in the devtools component tree, and — because the filter captures it at registration —
it also guarantees the token can never be refreshed on a retry, which is the exact failure the v5
per-attempt filter behaviour exists to solve.
