# Source Map

Use this file when codec work depends on current UUID, runtime crypto, or HAProxy Lua behavior.

## Source priority

1. This skill's shared codec contract and bundled PHP, JavaScript, shell, and HAProxy Lua assets.
2. Target repo tests and any existing copied helpers.
3. Official or primary references:
   - Douglas Crockford Base32 reference: https://www.crockford.com/base32.html
   - UUIDs RFC 9562: https://datatracker.ietf.org/doc/html/rfc9562
   - Web Crypto API: https://www.w3.org/TR/WebCryptoAPI/
   - Node.js Web Crypto API: https://nodejs.org/api/webcrypto.html
   - PHP `random_bytes`: https://www.php.net/manual/en/function.random-bytes.php
   - Python `uuid`: https://docs.python.org/3/library/uuid.html
   - HAProxy Lua API: https://www.haproxy.com/documentation/haproxy-lua-api/
4. Community implementations only for troubleshooting. Do not copy codec behavior from a gist or StackOverflow answer unless it is reconciled against the contract and tests.

## Freshness triggers

Re-check primary references and runtime behavior when the task mentions:

- latest/current UUIDv7, RFC 9562, Node, browser Web Crypto, PHP, Python, HAProxy, Lua, OpenSSL, FIPS, or crypto-runtime behavior
- changing encoded length, alphabet, alias normalization, integer strategy, byte order, UUID version/variant validation, or request-id generation
- applying the helper in an edge/runtime environment with restricted crypto APIs

## Domain-bounded anti-pattern

Bad: replacing the codec with a ULID helper because both are Base32-looking sortable IDs.

Good: preserve this skill's pure lowercase Crockford Base32 contract and use RFC 9562 only for UUIDv7 generation and validation.
