# Caching, Routing and Rewrites

This file writes directives. **It decides no policy.** The boundary sentence is stated once, in
`SKILL.md`. What follows is how each policy value becomes a line of HAProxy config, and what goes
wrong when it is written the obvious way.

The four obligations this skill owes `/alaa-frontend-devops` (`$alaa-frontend-devops`),
`alaa-frontend-devops references/30-serving-caching-and-public-path.md`, each answered below:
the asset prefix reaches the origin unchanged; HTML is not stored under the immutable policy;
compression does not alter the bytes that Subresource Integrity covers; a hard refresh on a deep
link returns the same document as a client-side navigation.

`20-static-asset-cache-and-rewrite.cfg` is the worked artifact for all four.

## When no policy has been given

**Emit no directive and ask for the policy.** Do not choose a default.

Every plausible default is wrong for at least one response class: `max-age=3600` is wrong for a
content-hashed asset (too short, and it forfeits the whole point of hashing), wrong for an HTML
document (too long, and a deploy does not take effect for an hour), and wrong for an authenticated
API response (it is a cache-poisoning surface). There is no value that is safe in the absence of
information about how the build names its files.

The mechanical form of "refuse rather than default" is the preprocessor:

```
.if !defined(HAPROXY_HASHED_ASSET_CACHE_CONTROL)
.alert "HAPROXY_HASHED_ASSET_CACHE_CONTROL is not set. alaa-frontend-devops decides it."
.endif
```

`.alert` makes `haproxy -c -f` fail with that message, so the missing policy is caught by the
gate register rather than discovered in production. A variable with no default achieves the same
outcome less legibly: it expands to nothing and produces a parse error naming the line.

## Emitting `Cache-Control`

```
http-response set-header Cache-Control "<value from the policy>" if <condition>
```

**The trap: `path` is a request sample.** Writing the condition directly against `path` in an
`http-response` rule makes HAProxy warn

```
acl 'is_hashed_asset' will never match because it only involves keywords
that are incompatible with 'frontend http-response header rule'
```

and the header is then never set. The config is valid, the process starts, and the caching policy
silently did not apply. Capture the decision during the request phase into a transaction variable
and test the variable in the response phase:

```
acl is_hashed_asset path_reg "^${HAPROXY_ASSET_PREFIX}/.+\.[0-9a-fA-F]{8,}\.[a-z0-9]+\$"
http-request  set-var(txn.hashed_asset) bool(true) if is_hashed_asset
http-response set-header Cache-Control "${HAPROXY_HASHED_ASSET_CACHE_CONTROL}" if { var(txn.hashed_asset) -m bool }
```

Inside double quotes a bare `$` starts an environment-variable reference, so a regex anchor is
written `\$`. A regex needing no expansion uses single quotes instead.

`set-header` replaces any value the origin sent; `add-header` appends a second one and leaves the
cache to choose. For a response header that is a policy statement, `set-header` is the form,
because two `Cache-Control` headers is undefined behaviour spread across every intermediary.

Distinguishing HTML from a hashed asset is the whole job: an HTML document must not inherit the
immutable policy that applies to hashed assets, or a deploy is invisible to every client that has
the old document until its own `max-age` expires.

## HAProxy's own cache

A small-object, in-process cache. It is not a CDN and it is not a replacement for one.

```
cache static_cache
  total-max-size 256        # megabytes; the documented maximum is 4095
  max-object-size 262144    # bytes; at most half of total-max-size
  max-age 60                # seconds
  process-vary on
```

```
frontend ...
  http-request cache-use static_cache if <condition>
backend ...
  http-response cache-store static_cache
```

What it does not do, each of which is a production surprise:

- **An object larger than `max-object-size` is passed through uncached, silently.** A bundle that
  grows past the ceiling stops being cached with no error and no signal other than origin load.
- **The cache does not survive a reload or a restart.** Every config change empties it, so a
  frequent-deploy estate never reaches steady state.
- **It is per process and per node.** On N nodes the first request per node per key still reaches
  the origin, so the origin must be sized for N times the miss rate, not once.
- **A response the origin marks `Cache-Control: no-store` is not stored**, which is the correct
  behaviour and also the reason a cache that appears to do nothing is usually being told not to.
- `process-vary on` stores one entry per `Vary` key instead of refusing to store varying responses
  at all. Without it, any response carrying `Vary` is uncacheable.

`show cache` on the Runtime API reports what is actually stored. Use it before concluding the
cache is working.

## Compression

From 3.4 the filter is declared explicitly; on 3.2 and 3.3 HAProxy inserts it implicitly when
`compression algo` is present and no other filter is declared. One file serves both:

```
backend ...
.if version_atleast(3.4)
  filter comp-res
.endif
  compression algo gzip
  compression type "${HAPROXY_COMPRESS_TYPES[*]}"
  compression offload
```

- `compression algo` sets the response algorithm; `compression algo-req` and `algo-res` set them
  separately when request compression is also in use, with `filter comp-req` alongside
  `filter comp-res` from 3.4.
- `compression type` is a **space-separated list of media types**, so the environment variable
  carrying it uses the `"${NAME[*]}"` word-splitting form. Written as `"${NAME}"` the entire list
  becomes one media type and nothing is ever compressed, with no error.
- `compression minsize-res` (3.2 and later) sets a floor below which compression is not attempted.
  A response smaller than a network frame gains nothing from being compressed.
- `compression offload` removes `Accept-Encoding` before the request reaches the origin, so the
  origin never compresses a body HAProxy is about to compress again.
- HAProxy does not compress a response that is already compressed. Listing `image/png`,
  `image/jpeg`, `application/zip` or `font/woff2` in `compression type` therefore costs CPU and
  buys nothing.

**Compression here is a transfer encoding, not a content transformation.** The body after
decompression is byte-identical to the file on disk, so a Subresource Integrity `integrity`
attribute still verifies. Any mechanism that rewrites bytes inside a response body — a URL
rewriter, a minifier, a body-level `replace` — breaks SRI and must not be introduced on a path
that serves files the HTML pins by hash.

## Path rewrites

| Directive | What it changes |
|---|---|
| `http-request set-path <expr>` | replaces the path, leaving the query string |
| `http-request replace-path <match> <replace>` | regex-rewrites the path, leaving the query string |
| `http-request set-pathq` / `replace-pathq` | the same, including the query string |
| `http-request replace-uri <match> <replace>` | rewrites the whole URI including any absolute form |

**The default is no rewrite.** A rewrite that was not required is exactly how an asset prefix gets
stripped, and a stripped prefix produces 404 for every hashed asset while the HTML document loads
normally — which reads as a broken deploy rather than as a rewrite bug. Add a rewrite only when
the origin has been **observed** to serve the asset at a different path from the public one, and
put it behind a named condition so the reason survives in the file.

The reciprocal failure is duplication: a rewrite whose replacement re-adds a prefix the match did
not consume produces `/assets/assets/app.abc12345.js`, which 404s in the same way and looks like
the first failure.

## Deep-link fallback

A single-page or server-rendered application needs a request for `/orders/42` to resolve to the
application entry document, so that a hard refresh returns the same document as a client-side
navigation:

```
acl is_document path_reg '^[^?]*/[^./?]*$'
http-request set-path /index.html if is_document
```

**The guard is that the fallback must not catch asset requests.** The condition above matches only
a path whose last segment has no file extension. Without that guard a missing asset returns the
application document with status 200, and the browser parses HTML as JavaScript — an error whose
message names a syntax error in a file that is not JavaScript, which is among the most expensive
false trails in frontend debugging.

## Selecting a backend

`use_backend <name> if <condition>` with an ACL, or a map when the table is large or is edited by
someone who is not editing the config. Map mechanics, and when a map beats an ACL chain, are in
`20-core-config-and-timeouts.md`. Which paths route where is a routing policy and, when it follows
from the build's output layout, it is decided by `/alaa-frontend-devops`
(`$alaa-frontend-devops`); when it follows from a release step it is decided by
`/alaa-controlled-ops` (`$alaa-controlled-ops`). `13-canary-map-routing.cfg` is the worked file.
