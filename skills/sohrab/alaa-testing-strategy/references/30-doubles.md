# Test Doubles

## Vocabulary, fixed

These five words mean exactly this in this fleet, because an unfixed vocabulary makes every review of a double ambiguous.

| Name | What it is | What it can prove |
|---|---|---|
| **Real** | The actual implementation, running | Everything the implementation decides |
| **Fake** | A working implementation of the same observable contract, simplified — an in-memory repository, an in-memory broker, a fake sink | That the caller's logic is correct against a contract someone believes the real one has |
| **Stub** | Canned answers to the calls the test makes, with no behaviour | That the caller handles those specific answers |
| **Mock** | A stub that also asserts how it was called | That a particular call was or was not made |
| **Spy** | A real or fake collaborator that records calls for the test to assert afterwards | The same as a mock, without coupling the arrangement to the assertion |

## When to use which

The real dependency needs no justification, because it is the only option that cannot encode a wrong belief. The two reasons to substitute in `SKILL.md` non-negotiable 3 cover these cases:

1. **A state the real dependency cannot be put into on demand**: a timeout, a connection refusal, a slow but successful response, a dropped message, a third party's rate-limit response, a clock at a boundary, a specific random value. This reason produces most negative tests. `/alaa-reliability-sla` owns which of these modes to inject at a dependency boundary.
2. **The suite's time budget**: the real dependency runs, but not at the rate this layer's suite must run.

No other reason qualifies. An inconvenient setup, a longer test or another team's ownership each trades a permanent loss of fidelity for a one-time saving.

Then pick the kind:

- **Fake** when the caller needs behaviour across several calls: store then read, publish then consume, acquire then release. A stub cannot express behaviour, and a stub made to do so grows into a bad fake.
- **Stub** when the caller needs one canned answer and the test asserts what the caller did with it.
- **Mock or spy** only when the call itself is the outcome: zero outbound requests on a refusal path, exactly one effect under retry, an emitted audit or security event. Prefer a spy, because a mock's arrangement and assertion are one object and a reader cannot tell setup from test.
- **Never a mock for an outcome observable in state.** A call-sequence assertion fails on every behaviour-preserving refactor. The team then learns to update tests without reading them, and the suite records the implementation instead of the contract.

## The drift rule

**A double that can drift is a liability that carries a maintenance obligation until something binds it.** A double can drift when the real dependency can change its behaviour without the double failing to compile and without any test failing. A drifted double keeps the suite green while production is broken, and the green result stops anyone looking.

Three bindings, strongest first:

1. **Generation from the artifact the real implementation is generated from** — a shared schema, an interface definition, a generated client. An artifact change regenerates both, so drift becomes a compile failure.
2. **A parity suite** — one set of cases run against the double and the real implementation, with identical results required. It is proof level 3 in `40-proof-strength.md` and the only binding for a hand-written double.
3. **A compile-time contract** — the double implements the real dependency's interface, so a signature change breaks the build. It catches shape drift only, never behavioural drift. Never treat it as sufficient.

Nothing else binds a double. A comment saying that it mirrors the real one binds nothing.

## Parity suites

One suite, two subjects, identical assertions.

- **Cases**: every case the callers rely on, plus every error and edge case the real dependency can produce on the calls the callers make, not only the cases the double implements.
- **Cadence**: against the double on every commit, and against the real implementation at a cadence the repository names, such as every mainline merge or nightly. Declare both cadences where the suite lives, because an undeclared cadence means the second half never runs.
- **On divergence**: the run fails and the change is blocked. Correct the double to match the real implementation, never the reverse, because the real implementation is the contract.
- **When the real implementation cannot run in this environment**, the double is unbindable. Record a gap at the severity of what the double stands in for. Never present the double's green suite as evidence about the real dependency.

## Never double what you do not own, unbound

A hand-written double of a third-party API encodes a belief about a vendor, who need not match it. Do one of these:

- Bind it with a parity suite against the vendor's sandbox, or against a recorded-interaction fixture refreshed on a stated cadence, with the refresh failing loudly when the recording no longer matches.
- Place the assertion at the contract layer against the vendor's published schema, so a schema change breaks it.
- Accept the limit explicitly: the test proves the caller handles this response shape, and the claim that the vendor sends it is recorded as an untested gap.

## Shared fixtures and factories

- Mutable data shared across tests breaks hermeticity. Build the data a test asserts on per test, through a factory that produces a fresh, independent instance. `90-test-economy.md` shares expensive infrastructure and immutable fixture data.
- A factory sets only the fields the assertion discriminates on, and randomises or defaults the rest. A factory that sets every field hides which field mattered.
- Clean up by construction, with the isolation order in `90-test-economy.md` *Setup once*. Never use a teardown that deletes named rows, because a failing test skips its teardown and poisons every later test.
