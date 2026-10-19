# Test-First Discipline

Read this before changing what any Go code does. It owns the **sequence** a behaviour change follows and the Go
mechanics of writing the test. Which kinds of test a change requires, and where the boundary between unit,
integration, contract, and load testing sits, belong to `/alaa-testing-strategy`, which also decides whether a
behaviour is owed a test at all: a consumer of the alaa-go-chi kit, a shared package, or the standard library does
not re-test what that dependency's own suite proves.

## What counts as a behaviour change

Any edit that changes what an observer of the code can see: a different response, a different stored row, a different
message published, a different error, a different metric value, a different order of effects. Renaming a symbol,
moving a file, reformatting, and adding a comment are not behaviour changes.

## The sequence

**Rule:** for every behaviour change that `/alaa-testing-strategy` finds owed a test, in this order, with no step
skipped and no step merged into another:

1. Read the existing tests for the code you are about to change. Name them in your report.
2. Write or update the test that will pass only once the new behaviour exists.
3. Run that test alone. Confirm it fails, and confirm the failure message describes the missing behaviour rather than
   a compile error, a nil panic, or a missing fixture. A test that fails for the wrong reason proves nothing.
4. Write the smallest change that makes it pass.
5. Run that test alone again.
6. Refactor now if the design needs it, with the tests green.
7. Run the changed packages' tests, then the validation gate in `SKILL.md`.

**Forbidden:** writing the implementation first and the test afterwards, and reporting it as test-driven.

## When you cannot write the test

**Rule:** stop and report. Say which behaviour you could not put under test, the exact obstacle — an unexported seam,
a global, a hard-coded clock, a dependency with no interface, a missing fixture — and the smallest change that would
remove the obstacle. Then wait for the user's instruction.

**Forbidden:** proceeding with the implementation and recording a reason the test was not written. **Forbidden:**
substituting a weaker check — a compile check, a manual run, a log line, an assertion on something adjacent — for the
missing test. A behaviour with no test is an untested behaviour whatever is written next to it, and the record makes
it look handled.

## Where the test goes

**Rule:** put the test at the boundary that owns the rule, not at the outermost layer that can reach it:

| The change is to… | The test lives at… |
|---|---|
| a domain rule or invariant | the domain package, no fakes needed |
| a use case's flow, ordering, or error handling | the use case, with fakes at its ports |
| a repository's SQL or scanning | the repository, against a real Postgres |
| cache policy | the cache decorator, with a fake; plus real Redis for TTL and eviction (`61-redis-cache-layer.md`) |
| request decoding, validation, or status mapping | the router (`31-chi-api-guide.md`) |
| concurrency, ownership, or shutdown | a test run under `-race` |

**Forbidden:** proving a domain rule only through an HTTP test. It passes for the wrong reasons and fails for reasons
that have nothing to do with the rule.

## Go test mechanics

**Rule:** name the test for the behaviour, not the function — `TestCreateUser_RejectsDuplicateEmail`, not
`TestCreateUser`.

**Rule:** use a table with `t.Run` per case when a rule has more than two input classes; give each case a name that
reads as a sentence about the behaviour.

**Rule:** call `t.Helper()` in every assertion or setup helper, and `t.Cleanup` for every resource the test creates.

**Rule:** take the test's context from `t.Context()` so cancellation propagates when the test fails or times out.

**Forbidden:** `time.Sleep` to wait for something. **Rule:** wait on the channel, the `sync.WaitGroup`, or the fake's
signal that the work reached the point you care about.

**Forbidden:** a test whose result depends on wall-clock time, on `map` iteration order, on a random value without a
fixed seed, or on another test having run. **Rule:** inject the clock, sort before comparing, seed explicitly, and
make each test construct its own mutable state.

**Rule:** start an expensive resource — a testcontainer, a migrated schema, a booted router — once per package in
`TestMain` when tests can isolate it with a rolled-back transaction, unique namespace, or exact reset. Keep it per
test when none is safe, recording why; also create it per test when creation is the behaviour under test.

**Rule:** use a hand-written fake when the assertion is about the value the code under test produced. Use a mock when
the assertion is about the interaction itself — that a method was called, with which arguments, how many times. An
interface you do not own gets a fake only when the test needs that seam.

**Rule:** add a fuzz target for every parser, decoder, validator, and identifier codec that reads untrusted input, and
keep the target free of shared state so it stays deterministic under `-race`.

## Running the tests

**Rule:** run the single test first, then the changed packages. Running everything first hides which change broke
what. The repository-wide run, its `-race` variant and their triggers belong to the validation gate in `SKILL.md`.

**Rule:** make every test selectable by topic and layer. The topic is the package plus the behaviour prefix of the
test name, so `-run '^TestCreateUser_'` selects it. The layer is the repository's configured build tag for real-store
tests; the alaa-go-chi kit uses `testcontainers`. Before combining tagged and normal runs, inspect build constraints
and test configuration to prove the selection covers required normal behavior: tags can exclude files such as
`!integration`, and may select different production code. If that coverage is unproven, retain both selections.

**Rule:** a Go test binary is one package, so "once per run" for an expensive resource means once per package.

**Rule:** reuse Go build artifacts and test results independently. A fresh test execution may use `-count=1` when
externally mutable dependency state changes without changing the test inputs, a cache hit cannot establish the
required result, or final proof requires a new observation; this bypasses test-result reuse without discarding
reusable build outputs. Do not clear the test cache for routine runs.

**Forbidden:** reporting a test suite as passing when it was not executed in this session, and reporting a skipped
test as a passing one. Use the evidence vocabulary from `alaa-go-chi-development`
`references/05-phase-and-source-truth.md`.
