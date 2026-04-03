# Shared Token Contract

Use this reference when a task needs one shared lowercase Crockford Base32 contract across PHP, JavaScript, shell tooling, or HAProxy Lua.

## Bundled assets

- PHP class:
  - `assets/crockford-base32/CrockfordBase32TokenCodec.php`
- JavaScript class:
  - `assets/crockford-base32/crockford-base32-token-codec.mjs`
- Bash CLI helper:
  - `scripts/crockford-base32-cli.sh`
- HAProxy Lua helper:
  - `assets/haproxy/crockford-base32-token-codec.lua`

## Shared encoding rules

- All encode operations emit lowercase Crockford Base32 only.
- The lowercase Crockford alphabet is:
  - `0123456789abcdefghjkmnpqrstvwxyz`
- Decode normalizes the common Crockford aliases before validation:
  - uppercase letters become lowercase
  - `o` maps to `0`
  - `i` and `l` map to `1`
  - hyphens are ignored
- Raw Base32 helpers operate on bytes with no padding.
- Typed helpers add a one-character lowercase Crockford prefix so different value families never collide.

## Typed token contract

| Prefix | Meaning | Payload contract |
| --- | --- | --- |
| `b` | raw bytes | Base32 of the raw bytes |
| `n` | signed integer | Base32 of one signed big-endian 64-bit value |
| `s` | UTF-8 string | Base32 of the UTF-8 bytes |
| `v` | UUIDv7 | Base32 of the 16 UUID bytes |

Working rules:

- Empty bytes encode to `b`.
- Empty strings encode to `s`.
- Integer tokens are fixed-width and signed 64-bit in every bundled implementation so PHP, JavaScript, shell, and HAProxy Lua stay aligned.
- UUID tokens must validate UUID version `7` and the RFC 4122 variant bits on decode.
- Use the typed tokens whenever a stored or transported value may later be decoded without a trusted out-of-band type hint.
- Use the raw byte helpers only when the caller already owns the type boundary and only needs lowercase Crockford Base32 as a transport primitive.

## Runtime notes

### PHP

- The PHP class uses `declare(strict_types=1);`.
- Adapt the namespace to the target Laravel or PHP repository before copying.

### JavaScript

- The JavaScript class ships as an ESM module.
- Integer decode returns `bigint` so 64-bit values remain lossless in JavaScript.
- UUID generation relies on `globalThis.crypto.getRandomValues`, which is available in modern browsers and current Node runtimes.

### Shell

- The bash helper is a strict-mode CLI wrapper.
- It uses Python 3 for the byte packing, Base32, and UUID work so the CLI stays deterministic and compact.

### HAProxy Lua

- Load the Lua helper with `lua-load` or `lua-load-per-thread`.
- Keep runtime use non-blocking.
- Validate the final HAProxy configuration with `haproxy -c -f <cfg>` after wiring in the helper.
- The Lua UUIDv7 generator is suitable for request IDs and correlation values, not for secret material.
- The helper auto-registers:
  - converters for encoding and decoding strings, integers, and UUIDv7 tokens
  - fetches for `uuidv7` and `uuidv7_token`

## Minimal HAProxy example

```haproxy
global
  lua-load /etc/haproxy/lua/crockford-base32-token-codec.lua

frontend edge_http
  bind :80
  http-request set-var(txn.request_uuid) lua.crockford_b32_uuidv7
  http-request set-var(txn.request_token) lua.crockford_b32_uuidv7_token
  http-request set-header x-request-id %[var(txn.request_uuid)]
```

## When to prefer this helper set

- request IDs or correlation values need a lowercase human-safe token form
- one repo needs the same typed token contract in backend PHP, frontend JavaScript, CLI scripts, and HAProxy edge logic
- a task needs copy-ready helpers instead of re-deriving Crockford Base32 and UUIDv7 details inside each repository
