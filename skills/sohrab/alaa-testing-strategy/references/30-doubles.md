# Test Doubles

## Vocabulary, fixed

Use these five words with exactly these meanings.

| Name | What it is | What it can prove |
|---|---|---|
| **Real** | The actual implementation, running | Everything the implementation decides |
| **Fake** | A simplified working implementation of the same observable contract: an in-memory repository, an in-memory broker, a fake sink | That the caller's logic is correct against the contract someone believes the real one has |
| **Stub** | Canned answers to the calls the test makes, with no behaviour | That the caller handles those answers |
| **Mock** | A stub that also asserts how it was called | That a call was or was not made |
| **Spy** | A real or fake collaborator that records calls for the test to assert afterwards | The same as a mock, with the arrangement separate from the assertion |

## When to use which

`SKILL.md` non-negotiable 3 allows two reasons to substitute:

1. **A state the real dependency cannot enter on demand**: a timeout, a connection refusal, a slow but successful response, a dropped message, a third party's rate-limit response, a clock at a boundary, a specific random value. `/alaa-reliability-sla` owns which of these modes to inject at a dependency boundary.
2. **The suite's time budget**: the real dependency runs, but not at the rate this layer's suite must run.

An inconvenient setup, a longer test and another team's ownership are not reasons.

Then choose the kind:

- **Fake** when the caller needs behaviour across several calls: store then read, publish then consume, acquire then release.
- **Stub** when the caller needs one canned answer, and the test asserts what the caller did with it.
- **Mock or spy** only when the call itself is the outcome: zero outbound requests on a refusal path, exactly one effect under retry, an emitted audit or security event. Prefer a spy, because a mock merges setup and assertion in one object.
- **Never a mock for an outcome observable in state.** A call-sequence assertion fails on every behaviour-preserving refactor.

## The drift rule

**A double can drift when the real dependency can change its behaviour while the double still compiles and every test still passes.** A drifted double keeps the suite green while production is broken. Three bindings exist, strongest first:

1. **Generation from the artifact that also generates the real implementation**: a shared schema, an interface definition, a generated client. Drift becomes a compile failure.
2. **A parity suite.** It is proof level 3 in `40-proof-strength.md`, and the only binding for a hand-written double.
3. **A compile-time contract**: the double implements the real dependency's interface. It catches shape drift only, never behavioural drift, so it is never sufficient alone.

Nothing else binds a double. A comment that says the double mirrors the real one binds nothing.

## Parity suites

One suite, two subjects, identical assertions.

- **Cases**: every case the callers rely on, plus every error and edge case that the real dependency can produce on the calls the callers make. The cases the double implements are not the limit.
- **Cadence**: against the double on every commit, and against the real implementation at a cadence the repository names, such as every mainline merge or nightly. Declare both cadences where the suite lives.
- **On divergence**: the run fails and blocks the change. Correct the double, never the real implementation, which is the contract.
- **When the real implementation cannot run in this environment**, the double is unbindable. Record a gap at the severity of what the double stands in for. Never present the double's green suite as evidence about the real dependency.

## Never double what you do not own, unbound

A hand-written double of a third-party API encodes a belief about a vendor. Do one of these:

- Bind it with a parity suite against the vendor's sandbox, or against a recorded-interaction fixture that is refreshed on a stated cadence and fails loudly when the recording no longer matches.
- Place the assertion at the contract layer against the vendor's published schema, so that a schema change breaks it.
- Accept the limit explicitly: the test proves that the caller handles this response shape, and the claim that the vendor sends it is recorded as an untested gap.

## Shared fixtures and factories

- Build the data that a test asserts on per test, through a factory that returns a fresh, independent instance. `90-test-economy.md` *Setup once* shares expensive infrastructure and immutable fixture data.
- A factory sets only the fields the assertion discriminates on, and defaults or randomises the others.
- Clean up by construction, in the isolation order of `90-test-economy.md` *Setup once*. Never use a teardown that deletes named rows: a failing test skips its teardown and poisons every later test.
