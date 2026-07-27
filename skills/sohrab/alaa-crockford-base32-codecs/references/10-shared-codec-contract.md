# Shared Codec Contract

This file is the wire format. The four bundled implementations are interchangeable
answers to it, and `scripts/codec-conformance.sh` is the check that they still are.
Every rule below is a rule the harness enforces, except the runtime notes marked
"not harness-checked", which state facts about one runtime that no cross-runtime
comparison can observe.

Change any rule here and all four implementations in the same effort, then run the
harness. A rule that no implementation satisfies is a defect in this file.

## Bundled assets

| Runtime | Path | Input for byte codecs |
| --- | --- | --- |
| PHP | `assets/crockford-base32/CrockfordBase32Codec.php` | raw bytes |
| JavaScript | `assets/crockford-base32/crockford-base32-codec.mjs` | `Uint8Array`, `ArrayBuffer`, or byte array |
| HAProxy Lua | `assets/haproxy/crockford-base32-codec.lua` | raw byte string |
| Shell CLI | `scripts/crockford-base32-cli.sh` | hexadecimal text |

The CLI takes hexadecimal because a process argument cannot carry raw binary. The
PHP, JavaScript, and Lua library functions take raw bytes. Call `hex2bin()`,
`Uint8Array.from()`, or an equivalent before `encodeBytes()` when the caller holds a
hex string, because passing the hex string itself encodes the ASCII of the hex.

## Alphabet and normalization

The lowercase Crockford alphabet is `0123456789abcdefghjkmnpqrstvwxyz`.

Encode emits lowercase only, with no padding character.

Decode normalizes before validation, in this order:

1. Uppercase letters become lowercase.
2. Every hyphen is removed, at any position. Leading hyphens, trailing hyphens, and
   hyphen runs are all removed, not only hyphens between payload characters. The one
   exception is a single leading `-` on an integer payload, which is read as the sign
   before normalization begins.
3. `i`, `I`, `l`, and `L` become `1`.
4. `o` and `O` become `0`.

`u` and `U` are rejected, not aliased. Crockford excludes `u` from the alphabet to
avoid accidental obscenities, and this codec keeps it excluded rather than folding it
to `v`.

There is no check symbol. Crockford's optional `*`, `~`, `$`, `=`, and `U` check
characters are not computed, not accepted, and not stripped. A payload carrying a
trailing check symbol is rejected as an invalid character, so a consumer that appends
one will have every value refused.

Whitespace is not stripped. A space, tab, or newline anywhere in a payload is an
invalid character.

## Decode validation

Decode rejects a payload whose trailing padding bits are not zero. Base32 characters
carry five bits each, so a payload that is not a whole number of bytes has leftover
bits, and those bits must be zero for the payload to be the canonical encoding of its
bytes. `z0` decodes to the single byte `0xf8`; `zz` is rejected, because its two
leftover bits are set.

Integer decode rejects a non-minimal magnitude. A magnitude longer than one character
must not start with `0` after normalization, so `00`, `01`, and `o1` are all rejected
while `0` alone is accepted.

## Value codecs

### Raw bytes

- `encodeBytes(bytes) -> base32`
- `decodeBytes(base32) -> bytes`
- Empty input encodes to the empty string, and the empty string decodes to empty
  bytes.

### Signed integers

- `encodeInt(value) -> base32`
- `decodeInt(base32) -> decimal text`

The integer width is unbounded. These are not 64-bit codecs: PHP and Lua use decimal
long division, JavaScript uses `BigInt`, and the CLI uses Python `int`, so a value
larger than 2^64 encodes and decodes exactly. Decode returns decimal text rather than
a native number so no runtime silently rounds a value above its own exact integer
range.

Sign strategy:

- positive integers encode as minimal unsigned Crockford Base32 digits
- negative integers encode as `-` plus the minimal unsigned magnitude
- zero encodes as `0`, and `-0` encodes as `0`

The encode input grammar is `-?[0-9]+` matched against the whole value, with nothing
before or after it. Leading zeros are accepted and normalized, so `007` encodes as
`7`. Every one of the following is rejected in all four runtimes:

| Rejected input | Why it is called out |
| --- | --- |
| `12` followed by a newline | PCRE `$` accepted it and the newline became an extra decimal digit zero |
| `+5` | Python `int()` accepts a leading plus |
| `" 12 "` | Python `int()` accepts surrounding whitespace |
| `1_0` | Python `int()` accepts PEP 515 digit separators |
| `١٢` | Python `int()` accepts non-ASCII decimal digits |
| `0x10`, `0b101`, `0o17` | `BigInt()` accepts base prefixes |
| `""`, `"  "` | `BigInt()` reads these as zero |
| `true`, `false`, `[]`, `["7"]` | `BigInt()` coerces non-string types |

Pass magnitudes above 2^53 as strings. A JavaScript `number` or a Lua `number` has
already lost precision before the codec sees it, and no implementation can recover it.

Decode consumes at most one leading `-` as the sign, then removes every remaining
hyphen, so `-3ttx` is negative and `3t-tx` is positive.

Required examples:

- `encode-int 9` -> `9`
- `encode-int 25` -> `s`
- `encode-int 125789` -> `3ttx`
- `decode-int 3ttx` -> `125789`

### UTF-8 strings

- `encodeString(text) -> base32`
- `decodeString(base32) -> text`

Both directions validate UTF-8 per RFC 3629. Overlong forms, surrogate code points,
and code points above U+10FFFF are rejected. `decodeString` on a payload that decodes
to bytes which are not valid UTF-8 raises rather than returning the raw bytes, so
`decode-string zw` is an error in all four runtimes and not the byte `0xff`.

The PHP and Lua implementations carry an explicit RFC 3629 validator because they
operate on byte strings and have no string type that guarantees validity. The
JavaScript implementation rejects unpaired surrogates on encode, because
`TextEncoder` would otherwise substitute U+FFFD and produce bytes the other three
runtimes refuse to produce.

### UUIDv7

- `generateUuidV7() -> canonical UUIDv7`
- `encodeUuidV7(uuid) -> base32`
- `decodeUuidV7(base32) -> canonical UUIDv7`

Byte order is preserved, so a full 16-byte UUID payload encodes to 26 lowercase
Crockford Base32 characters.

Encode requires canonical 8-4-4-4-12 hexadecimal form. An unhyphenated 32-character
string is rejected.

Decode validates, in this order: exactly 16 decoded bytes, version nibble `7`, then
RFC 4122 variant bits. A canonical UUIDv7 payload always has zero trailing padding
bits, so a 26-character payload with padding bits set is rejected before the length
check.

## Exact error messages

All four implementations raise these strings verbatim. The harness compares message
text, so changing a string in one implementation without the other three is a
disagreement.

| Condition | Message |
| --- | --- |
| Byte or string payload has an out-of-alphabet character | `Invalid Crockford Base32 character [X].` |
| Integer payload has an out-of-alphabet character | `Invalid Crockford Base32 integer character [X].` |
| Trailing padding bits are not zero | `Invalid Crockford Base32 payload padding bits.` |
| Integer payload is empty or is a lone sign | `Integer payload cannot be empty.` |
| Integer payload magnitude is non-minimal | `Integer payload must use a minimal Crockford Base32 representation.` |
| Integer input violates the `-?[0-9]+` grammar | `Integer input must be a canonical base-10 integer.` |
| Text to encode is not valid UTF-8 | `Text input is not valid UTF-8.` |
| Decoded bytes are not valid UTF-8 | `Decoded payload is not valid UTF-8.` |
| UUID text is not canonical 8-4-4-4-12 hex | `UUID must be in canonical 8-4-4-4-12 hexadecimal form.` |
| UUID payload is not 16 bytes | `UUID payload must contain exactly 16 bytes.` |
| UUID payload version nibble is not 7 | `UUID payload must be version 7.` |
| UUID payload variant bits are not RFC 4122 | `UUID payload must use the RFC 4122 variant bits.` |

## Conformance harness

Run `scripts/codec-conformance.sh` after changing any implementation. It drives all
four over one corpus and exits non-zero on any disagreement, printing the input and
each runtime's answer. `--verbose` prints every case; `--self-test` checks the
comparator itself.

What it covers: integer boundaries at 0, 1, 31, 32, 1023, 2^32-1, 2^53-1, 2^53+1,
2^63-1, 2^63, 2^64-1, 2^64, and 2^200-1, each in both signs; `-0`; the full grammar
table above; case folding, hyphen handling, and every alias character; `u` and `U`
rejection; check-symbol rejection; the empty string; zero and non-zero trailing
padding bits; non-minimal integer payloads; canonical, version-4, bad-variant,
short, long, and padding-bit-set UUID payloads; and UTF-8 strings from ASCII through
four-byte emoji plus three invalid-UTF-8 decode payloads.

What it deliberately does not cover, and why:

- `generate-uuidv7` output, because it is random and time-dependent and two runtimes
  cannot produce the same value. Generation is covered by the per-runtime properties
  in the next section instead.
- Payloads that decode to text containing a newline, because the driver protocol is
  one line per answer.
- Any runtime whose interpreter is absent. The harness names it as skipped and
  excludes it, and it exits 4 rather than 0 when fewer than two runtimes are
  available, so a skip is never reported as agreement.

For what this level of proof is worth and what it does not replace, read
`/alaa-testing-strategy` (`$alaa-testing-strategy`).

## Runtime notes

### Randomness and clock sources

Not harness-checked. Each row states what one runtime actually uses, because a
weakness that is documented for only one runtime stays invisible in the others.

| Runtime | Random source | Clock source | Ordering guarantee |
| --- | --- | --- | --- |
| PHP | `random_bytes` (CSPRNG) | `microtime(true)` | millisecond |
| JavaScript | `crypto.getRandomValues` (CSPRNG) | `Date.now()` | millisecond |
| Shell CLI | Python `uuid.uuid4()` (`os.urandom`) | `time.time()` | millisecond |
| HAProxy Lua | `math.random`, seeded once per Lua state from `/dev/urandom` | `core.now()` when reachable, otherwise `os.time()` | millisecond under `core.now()`, one second otherwise, and strictly increasing within a process either way |

The Lua generator is a non-cryptographic PRNG on every path. The other three draw
their random bits from a CSPRNG, so only the Lua row is weaker than its runtime's
best available source.

### PHP

- The class uses `declare(strict_types=1);`.
- The namespace is the one line a copying repository is expected to change.

### JavaScript

- The class ships as an ESM module.
- `generateUuidV7()` requires `globalThis.crypto.getRandomValues` and raises when it
  is absent rather than falling back to `Math.random`.

### Shell

- The CLI requires Python 3.9 or newer and asserts the version before feeding the
  program to the interpreter, because a bare `python` on PATH may be Python 2 and
  would otherwise fail with a `SyntaxError` that reads like a code defect.
- Exit codes and the caller's obligation for each are documented in `--help`.

### HAProxy Lua

- **HAProxy supports only Lua 5.3 and above.** HAProxy's own `INSTALL`, section 4.7,
  states "Only versions 5.3 and above are supported", so LuaJIT — which implements
  5.1 — is not a supported HAProxy target and a 5.1 fallback buys nothing inside
  HAProxy. Confirm the linked version on the running binary with `haproxy -vv`
  before deploying this module. `/alaa-haproxy-lua` (`$alaa-haproxy-lua`) owns that
  rule and the rest of the HAProxy Lua execution model.
- The module itself requires nothing above Lua 5.1, so it also runs under a
  standalone 5.1 or 5.2 interpreter for testing and CLI use. Every bit operation is
  written as arithmetic on values below 2^48; the module previously used the 5.3
  `>>` and `&` operators and failed to parse on a 5.1 interpreter with
  `unexpected symbol near '>'`. Running the conformance harness under a different
  interpreter than the one `haproxy -vv` reports tests a different language, so
  match it before treating a harness result as evidence about production.
- The module seeds `math.random` once per Lua state from `/dev/urandom`, falling back
  to a process-state mix when `/dev/urandom` is unreadable. Under
  `lua-load-per-thread` each thread is a separate state and draws its own seed.
- `generateUuidV7` carries an RFC 9562 section 6.2 twelve-bit counter in `rand_a`, so
  identifiers from one process are strictly increasing even when the clock resolution
  is one second. When the counter overflows within a millisecond the timestamp
  advances by one millisecond, as that section allows.
- `core.now()` is documented for body, init, task, and action context. The UUIDv7
  fetch runs in sample-fetch context, so the module calls it defensively and falls
  back to `os.time()` at one-second resolution when the call is unavailable.
- Converters propagate errors instead of returning `nil`. A `nil` sample leaves the
  HAProxy variable unset, which renders as an empty header value, so a malformed or
  forged identifier would have been stored as an empty string rather than rejected.
- `M.set_clock` and `M.set_random_source` exist so a host or a test can inject a
  deterministic source. Leave both unset in production unless the host supplies a
  clock with better than one-second resolution.

Module loading, `lua-load` against `lua-load-per-thread`, edge failure handling, and
non-blocking rules are owned by `/alaa-haproxy-lua` (`$alaa-haproxy-lua`). HAProxy
configuration and its validation are owned by `/alaa-haproxy` (`$alaa-haproxy`). This
file states only what the codec itself does.

## Minimal HAProxy example

This example shows the codec's own registration surface. Read
`/alaa-haproxy-lua` (`$alaa-haproxy-lua`) before wiring it into a real frontend,
because the choice of load directive and the handling of a failed sample are decided
there, not here.

```haproxy
global
  lua-load /etc/haproxy/lua/crockford-base32-codec.lua

frontend edge_http
  bind :80
  http-request set-var(txn.request_uuid) lua.crockford_b32_uuidv7
  http-request set-header x-request-id %[var(txn.request_uuid)]
```

A request identifier generated here can reach a downstream store as a correlation
key, so a duplicate value breaks correlation joins and an empty value breaks them
silently. Trusted-header policy for such a header is owned by
`/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`).

The helper auto-registers converters for the bytes, string, integer, and UUIDv7
codecs, plus one fetch named `crockford_b32_uuidv7`.
