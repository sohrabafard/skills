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
   - Lua 5.1 to 5.4 reference manuals: https://www.lua.org/manual/
4. This skill's `scripts/codec-conformance.sh`, whose output is the only evidence that
   a claim about cross-runtime agreement still holds.
5. Community implementations only for troubleshooting. Do not copy codec behavior from a gist or StackOverflow answer unless it is reconciled against the contract and tests.

## Version-sensitive points to re-verify

Check each against the primary source before restating it, because each one changed
the implementation once already:

- the context list for `core.now()` in the HAProxy Lua API, which excludes
  sample-fetch and converter context and therefore decides whether the Lua UUIDv7
  generator gets a millisecond clock
- which Lua version the target HAProxy build links, read from the `Built with Lua version`
  line of `haproxy -vv`. HAProxy supports only 5.3 and above (`INSTALL` section 4.7), so a
  build reporting 5.1 or LuaJIT is unsupported and the deployment question is the build, not
  the module. Testing under an interpreter other than the one that line reports tests a
  different language, and it is also what decides whether bitwise-operator syntax parses
  at all.
- RFC 9562 section 6.2 counter methods, which the Lua generator relies on for
  ordering when the clock resolution is one second

## Freshness triggers

Re-check primary references and runtime behavior when the task mentions:

- latest/current UUIDv7, RFC 9562, Node, browser Web Crypto, PHP, Python, HAProxy, Lua, OpenSSL, FIPS, or crypto-runtime behavior
- changing encoded length, alphabet, alias normalization, integer strategy, byte order, UUID version/variant validation, or request-id generation
- applying the helper in an edge/runtime environment with restricted crypto APIs

## Domain-bounded anti-pattern

Bad: replacing the codec with a ULID helper because both are Base32-looking sortable IDs.

Good: preserve this skill's pure lowercase Crockford Base32 contract and use RFC 9562 only for UUIDv7 generation and validation.
