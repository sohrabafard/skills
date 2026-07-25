# Test Doubles

Read when substituting anything for a real dependency, when a double already exists in the repository, or when a suite passes while an integration breaks. `SKILL.md` holds the binding rules: the real dependency is used whenever it runs deterministically inside the budget, a substitution records which of two reasons applies, and every double that can drift is bound by a parity suite.

## Vocabulary, fixed

These five words are used inconsistently across teams, and an unfixed vocabulary makes every review of a double ambiguous. In this fleet they mean exactly this.

| Name | What it is | What it can prove |
|---|---|---|
| **Real** | The actual implementation, running | Everything the implementation decides |
| **Fake** | A working implementation of the same observable contract, simplified — an in-memory repository, an in-memory broker, a fake sink | That the caller's logic is correct against a contract someone believes the real one has |
| **Stub** | Canned answers to the calls the test makes, with no behaviour | That the caller handles those specific answers |
| **Mock** | A stub that also asserts how it was called | That a particular call was or was not made |
| **Spy** | A real or fake collaborator that records calls for the test to assert afterwards | The same as a mock, without coupling the arrangement to the assertion |

## When to use which

**Use the real dependency** whenever it can run in the test environment deterministically and inside the suite's time budget. This is the default and it needs no justification, because it is the only option that cannot encode a wrong belief.

**Substitute** for exactly one of two reasons, recorded beside the double:

1. **A state the real dependency cannot be put into on demand.** A timeout, a connection refusal, a slow-but-succeeding response, a broker that drops a message, a third party's rate-limit response, a clock at a boundary, a specific random value. This is the reason that produces most negative tests, and `/alaa-reliability-sla` (`$alaa-reliability-sla`) owns which of these modes to inject at a dependency boundary.
2. **The suite's time budget.** The real dependency runs, but not at the rate this layer's suite must run at.

Any other reason — the real one is inconvenient to set up, the test would be longer, the dependency is owned by another team — is not a reason, because each of them trades a permanent loss of fidelity for a one-time saving.

**Then pick the kind:**

- **Fake** when the caller needs the dependency to behave across several calls: store then read, publish then consume, acquire then release. A stub cannot express behaviour, so a test needing behaviour from a stub grows a stub that is a bad fake.
- **Stub** when the caller needs one canned answer and the test asserts on what the caller did with it.
- **Mock or spy** only when the call itself is the outcome under test: zero outbound requests on a refusal path, exactly one effect under retry, an audit or security event emitted. Prefer a spy, because a mock's arrangement and assertion are the same object and a reader cannot tell which lines are setup and which are the test.
- **Never a mock for an outcome that is observable in state.** Asserting the sequence of internal calls fails on every behaviour-preserving refactor, which teaches the team to update tests without reading them — after which the suite records the implementation rather than the contract.

## The drift rule

**A double that cannot drift from the real thing is safe. A double that can drift is a liability, and it carries a maintenance obligation until something binds it.**

The test for drift is observable: **can the real dependency change its behaviour without the double failing to compile and without any test failing?** If yes, the double can drift. When it drifts, the suite stays green while production is broken — which is worse than having no test, because the green result is what stops anyone looking.

Three things make a double non-drifting, in descending order of strength:

1. **Generation from the same artifact the real implementation is generated from** — a shared schema, an interface definition, a generated client. A change to the artifact regenerates both, so drift becomes a compile failure.
2. **A parity suite** — one set of cases run against the double and against the real implementation, with identical results required. This is proof level 3 in `40-proof-strength.md`, and it is the only binding available when the double is hand-written.
3. **A compile-time contract** — the double implements the same interface as the real dependency, so a signature change breaks the build. This catches shape drift only; it does not catch behavioural drift, and treating it as sufficient is the common mistake.

Nothing else binds a double. A comment saying it mirrors the real one binds nothing.

## Parity suites

One suite, two subjects, identical assertions.

- **Cases**: every case the callers rely on, plus every error and edge case the real dependency can produce — not the cases the double happens to implement.
- **Cadence**: against the double on every commit, and against the real implementation at a stated cadence the repository names (every merge to the mainline, or nightly). Both cadences are declared where the suite lives; an undeclared cadence means the second half never runs.
- **On divergence**: the run fails and the change is blocked. The double is corrected to match the real implementation, never the reverse — the real implementation is the contract.
- **When the real implementation cannot be run in this environment at all**, the double is unbindable. Record it as a gap at the severity of what the double stands in for, and say so in the report; do not present the double's green suite as evidence about the real dependency.

## Never double what you do not own, unbound

A hand-written double of a third-party API encodes a belief about a vendor's behaviour, and the vendor is under no obligation to match it. Bind it or do not rely on it:

- Bind it with a parity suite run against the vendor's sandbox or a recorded-interaction fixture refreshed on a stated cadence, with the refresh failing loudly when the recording no longer matches.
- Or place the assertion at the contract layer against the vendor's published schema, so a schema change is what breaks.
- Or accept the limit explicitly: the test proves the caller handles *this* response shape, and the claim that the vendor sends that shape is untested and recorded as a gap.

## Shared fixtures and factories

- A fixture shared across tests is shared state, and shared state breaks hermeticity. Build state per test through a factory that produces a fresh, independent instance.
- A factory sets only the fields the test's assertion discriminates on, and randomises or defaults the rest. A factory that sets every field makes each test look meaningful and hides which field mattered.
- Clean-up is by construction — a transaction rolled back, a fresh schema, a unique namespace per test — never a teardown routine that deletes named rows, because a failing test skips its teardown and poisons every test after it.
