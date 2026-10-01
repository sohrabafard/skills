# HTTP compression and filter order

## Compression

3.4 adds explicit `comp-req`/`comp-res` filters. Implicit compression remains
possible with no other filters or only cache/FastCGI filters; explicit declarations
make ordering reviewable. A branch-aware file uses:

```
backend ...
.if version_atleast(3.4)
  filter comp-res
.else
  filter compression
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

Compression needs `+ZLIB` or `+SLZ`, not necessarily both. When caching and
compression coexist, declare `filter cache <name>` before the compression filter
to store the uncompressed representation; changing their order changes stored
bytes/negotiation behavior. Test cache hits with different Accept-Encoding values
and compare decompressed body bytes. Legacy `filter compression` and
`compression direction` are deprecated in 3.4; use separate `comp-req`/`comp-res`.
`filter-sequence` from the announcement was reverted in 3.4.5 and is unavailable
on 3.4.6. The worked example states explicit cache/compression order.
