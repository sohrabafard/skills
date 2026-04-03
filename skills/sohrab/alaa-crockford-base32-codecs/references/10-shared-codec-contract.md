# Shared Codec Contract

Use this reference when a task needs one shared lowercase Crockford Base32 codec contract across PHP, JavaScript, shell tooling, or HAProxy Lua.

## Bundled assets

- PHP class:
  - `assets/crockford-base32/CrockfordBase32Codec.php`
- JavaScript class:
  - `assets/crockford-base32/crockford-base32-codec.mjs`
- Bash CLI helper:
  - `scripts/crockford-base32-cli.sh`
- HAProxy Lua helper:
  - `assets/haproxy/crockford-base32-codec.lua`

## Shared encoding rules

- All encode operations emit lowercase Crockford Base32 only.
- The lowercase Crockford alphabet is:
  - `0123456789abcdefghjkmnpqrstvwxyz`
- Decode normalizes the common Crockford aliases before validation:
  - uppercase letters become lowercase
  - `o` maps to `0`
  - `i` and `l` map to `1`
  - hyphens are ignored inside Base32 payloads
- Raw Base32 helpers operate on bytes with no padding.
- The helpers are pure codecs. They do not add type prefixes or token wrapper metadata.

## Value codecs

### Raw bytes codec

- `encode-bytes HEX -> base32`
- `decode-bytes base32 -> HEX`
- empty bytes encode to the empty string

### Integer codec

- `encode-int VALUE -> base32`
- `decode-int base32 -> VALUE`
- signed integer strategy:
  - positive integers encode as minimal unsigned Crockford Base32 digits
  - negative integers encode as `-` plus the minimal unsigned magnitude
  - zero always encodes as `0`
- integer payloads should stay canonical:
  - no leading zero digits on multi-digit magnitudes
  - no fixed-width binary packing

Required examples:

- `encode-int 9` -> `9`
- `encode-int 25` -> `s`
- `encode-int 125789` -> `3ttx`
- `decode-int 3ttx` -> `125789`

### UTF-8 string codec

- `encode-string TEXT -> base32`
- `decode-string base32 -> TEXT`
- string encode and decode operate on UTF-8 bytes directly with no metadata

### UUIDv7 codec

- `generate-uuidv7 -> canonical UUIDv7`
- `encode-uuidv7 UUID -> base32`
- `decode-uuidv7 base32 -> canonical UUIDv7`
- UUID values preserve their original byte order
- UUID decode must validate:
  - exactly 16 decoded bytes
  - UUID version `7`
  - RFC 4122 variant bits
- full UUID payload encoding yields 26 lowercase Crockford Base32 characters

## CLI surface

The CLI exposes only:

- `encode-bytes`
- `decode-bytes`
- `encode-int`
- `decode-int`
- `encode-string`
- `decode-string`
- `generate-uuidv7`
- `encode-uuidv7`
- `decode-uuidv7`

## Runtime notes

### PHP

- The PHP class uses `declare(strict_types=1);`.
- `decodeInt()` returns canonical base-10 text so the helper stays lossless.
- Adapt the namespace to the target Laravel or PHP repository before copying.

### JavaScript

- The JavaScript class ships as an ESM module.
- `decodeInt()` returns canonical base-10 text so callers never lose precision.
- UUID generation relies on `globalThis.crypto.getRandomValues`, which is available in modern browsers and current Node runtimes.

### Shell

- The bash helper is a strict-mode CLI wrapper.
- It uses Python 3 internally for deterministic byte, integer, and UUID work.

### HAProxy Lua

- Load the Lua helper with `lua-load` or `lua-load-per-thread`.
- Keep runtime use non-blocking.
- Validate the final HAProxy configuration with `haproxy -c -f <cfg>` after wiring in the helper.
- The Lua UUIDv7 generator is suitable for request IDs and correlation values, not for secret material.
- The helper auto-registers:
  - converters for bytes, strings, integers, and UUIDv7 codecs
  - one fetch for `uuidv7`

## Minimal HAProxy example

```haproxy
global
  lua-load /etc/haproxy/lua/crockford-base32-codec.lua

frontend edge_http
  bind :80
  http-request set-var(txn.request_uuid) lua.crockford_b32_uuidv7
  http-request set-header x-request-id %[var(txn.request_uuid)]
```

## When to prefer this helper set

- request IDs or correlation values need a lowercase human-safe Base32 form
- one repo needs the same bytes, integer, string, and UUIDv7 codecs in backend PHP, frontend JavaScript, CLI scripts, and HAProxy edge logic
- a task needs copy-ready helpers instead of re-deriving Crockford Base32 and UUIDv7 details inside each repository
