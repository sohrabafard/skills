# Time, Randomness, and Identity

Three defects in this area produced duplicate identifiers and inverted event ordering in code that passed review. Each has a one-line rule and a measured reason.

## `os.clock()` is not a clock

`os.clock()` returns **processor time used by the process**, in seconds. It is not wall-clock time, it does not advance while the process waits on I/O, and it measures CPU consumption rather than elapsed request time.

Measured on 26 July 2026: forty freshly started `lua5.4` processes each evaluated `os.clock()` immediately after startup. Every value landed between **0.001535 s and 0.001797 s** — a 262-microsecond band.

Two consequences follow directly.

**As an entropy source it supplies almost nothing.** The seeding expression `os.time() + math.floor(os.clock() * 1000000)` spans that 262-value band inside a one-second bucket. Across the same forty processes it produced **36 distinct seeds out of 40**, and the UUIDs derived from them were **38 unique out of 40 — two exact duplicates.**

**As a sub-second clock it is worse than nothing, because it inverts ordering.** The expression `(os.time() * 1000) + math.floor((os.clock() * 1000) % 1000)` takes the second from the wall clock and the milliseconds from CPU consumption, so a CPU-heavy caller reports a later time than a CPU-light caller that ran after it. Measured within a single wall-clock second: process A ran first and burned 0.35 s of CPU; process B ran 450 ms later and burned 0.0018 s. A derived `1785102625350`, B derived `1785102625001`. **B, which happened second, sorts first, by 349 ms.**

**Alaa policy:** do not use `os.clock()` for request timestamps, deadlines or entropy. CPU profiling is a different measurement; keep it in a dedicated benchmark harness.

## The wall clock is `core.now()`

`core.now()` returns a table with `sec` and `usec`, taken from HAProxy's own clock, which the reference says "assures than the hour will be monotonic and that the system call `gettimeofday` will not be called too". Milliseconds:

```lua
local now = core.now()
local milliseconds = now.sec * 1000 + now.usec // 1000
```

Two properties to design around:

- **The value is refreshed per Lua execution or resume, not per call.** The reference states that "two consecutive call to the function `now` will probably returns the same result". `core.now()` is therefore a timestamp, never a stopwatch; it cannot measure how long your own handler took.
- **The documented contexts are body, init, task, and action.** Sample fetches and converters are not in that list. Verified on HAProxy 2.8.16 on 26 July 2026, a `core.now()` call inside a registered sample fetch did return a correct value, so the observed behaviour is wider than the documented contract. Depending on the undocumented part is a choice to make explicitly, and the safer design does not need it: take the timestamp in an action, store it with `TXN.set_var`, and pass the fetched value into the converter. A converter has no TXN object.

`os.time()` remains legitimate for whole seconds where a second is genuinely the unit. **Multiplying `os.time()` changes units, not precision.** This is legitimate when a consumer accepts second-granularity timestamps expressed in milliseconds; do not present it as sub-second measurement or mix it with CPU time. `os.date` is formatting/calendar behavior, not a scheduler clock. Both require `os` in the library allowlist.

## Entropy

Lua's `math.random` is a pseudo-random generator seeded once per Lua state. Under `lua-load-per-thread` the file body runs once per thread, sequentially, inside the same second, so a clock-derived seed gives every thread a neighbouring value from the same tiny band; under `lua-load` the seed is drawn once per process and every reload redraws from the same band.

**Rule: when a value must not collide, its entropy comes from the operating system, never from a clock.** Read it in the body or init context, where blocking file access is permitted:

```lua
-- Body context: HAProxy permits blocking reads here, before traffic is served.
local handle = assert(io.open("/dev/urandom", "rb"))
local raw = handle:read(8)
handle:close()
assert(raw and #raw == 8, "entropy unavailable")
local seed = 0
for index = 1, 8 do seed = (seed << 8) | string.byte(raw, index) end
math.randomseed(seed)
```

Verified on 26 July 2026 on HAProxy 2.8.16 with `nbthread 4` and `lua-load-per-thread`: this produced four widely separated seeds across the four threads, while the clock-derived expression in the same file produced four values inside a 63000-unit band.

Note the boundary: this seeds a *pseudo*-random generator for values that merely need to be unlikely to repeat. `math.random` is not a cryptographic source, so it must not produce a token, a nonce, a session identifier, or anything an attacker benefits from predicting. For those, use a reviewed cryptographic mechanism and route its ownership to
`/alaa-security-review`; never perform a blocking entropy-file read on the request
path. Loading entropy at startup does not make the PRNG cryptographic. Check reads
for failure and exact length before seeding any non-security PRNG.

## Identity: the two classes

Separate them before writing any generator, because they have different acceptance criteria.

- **Unlikely to repeat.** A correlation identifier for tracing. A rare duplicate merges two traces in a dashboard. A pseudo-random source seeded from the operating system is sufficient.
- **Collision corrupts data.** A primary key, an idempotency key, a deduplication key, an audit-record identifier. One collision silently overwrites or merges two real records, and the damage is discovered later, downstream, without a link back to the edge. This class needs full entropy per value and a test that measures the collision rate across process restarts, not a smoke test.

A generator can produce plausible individual values while repeating across process starts. `references/50-testing.md` gives the test shape that catches it.

## Do not write the generator

HAProxy generates UUIDs natively. From the configuration manual for 3.0 through 3.4:

```
uuid([<version>]) : string
  Returns a UUID following the RFC 9562 standard. If the version is not
  specified, a UUID version 4 (fully random) is returned.

  Versions 4 and 7 are supported.
```

**Use native `uuid(7)` when UUIDv7 is the required format and the target build supports it.** Preserve the fleet format, trust rules and existing v4/v7 choice; availability is not authorization to change identity contracts. Native generation avoids maintaining a Lua clock and seeding implementation.

Version floor, measured rather than assumed: `uuid([<version>])` with "Versions 4 and 7 are supported" appears in the configuration manual for v3.0.0, v3.1.0, v3.2.0, v3.3.0, and v3.4.0, read on 26 July 2026. On HAProxy 2.8.16, `%[uuid(7)]` fails at configuration parse with `invalid args in fetch method 'uuid' : Unsupported UUID version: '7'`. Confirm the running branch with `haproxy -vv` before relying on it; branch and upgrade policy is owned by `/alaa-haproxy`.

When a Crockford Base32 or UUIDv7 *representation* has to match backend, frontend, or CLI code, the encoding contract is owned by `/alaa-crockford-base32-codecs`. Generating the value and encoding it are separate decisions: take the value from `uuid(7)` and apply the shared codec to it.
