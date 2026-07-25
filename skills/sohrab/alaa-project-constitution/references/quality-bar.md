# The Service Quality Bar

Read this reference on every CREATE and UPDATE. It is the named owner of the ten obligations
that apply to every service in this estate regardless of what kind of service it is. Other
skills point here instead of restating it; when another skill's rule and this file disagree,
this file loses only where that skill owns the topic by name.

The bar answers one question about the project under authoring: **is this fit for a service
that must not fail?** The services in scope are production, security-sensitive,
high-concurrency, and carry an availability target above 99.99%. An availability target is a
statement about failure, not about success, so most of what follows is about failure.

## How this file is used

1. For every evidenced surface and every owned journey, walk the ten obligations below and
   answer the investigation questions for that surface.
2. Every obligation that applies produces at least one candidate. An obligation that does not
   apply is excluded with a stated reason and the evidence path proving the surface is out of
   owned scope. Silence is not exclusion.
3. Kind-specific obligations come from `project-archetypes.md`, which does not restate these ten.
   Where an archetype names a concrete rule for one of them, writing the archetype's specific
   rule satisfies both.
4. Resolve each candidate through the disposition list in `intent-and-risk-discovery.md`. This
   file establishes that an obligation applies; that file establishes how it enters the
   constitution or why it does not.

## The ten obligations

| # | Obligation | Questions to answer for each surface |
|---|---|---|
| 1 | **Correctness and testability** | What proves this behaves correctly — and would that proof fail against a plausible broken implementation, or does it only exercise the happy path? Which behaviour is test-driven, which is covered after the fact, and which is deliberately untested? What races, duplicate work, ordering, idempotency, isolation, consistency, or cache-coordination failures could violate the owned outcome? |
| 2 | **Failure behaviour** | What is the timeout for every outbound call, and is the total deadline smaller than the caller's? How many retries, with what backoff and jitter, and which operations are unsafe to retry without an idempotency key? What does the system do when a dependency is gone rather than slow? Which journeys degrade, which shed load, and which fail closed? What is the recovery objective, and who observes that it was met? |
| 3 | **Security** | Where are the trust boundaries, and what proves identity at each? What authorises each action — per action and per record, not per page? Which input is untrusted, and where is it validated and bounded? Where do secrets live, how do they rotate, and what proves they are absent from logs and artifacts? Where is tenant or user isolation enforced, and what test proves a cross-tenant read fails? |
| 4 | **Observability** | For each new failure mode, what signal makes it diagnosable in production without a code change? Which logs, metrics, traces, and their field contracts are owned here, and which canonical source owns them? What correlation identifier crosses every hop? Which condition raises an alert, and what does the responder do next? "Add logging" is not an answer. |
| 5 | **Concurrency and load** | What happens at ten times current traffic in one minute? What bounds connection pools, in-flight work per caller, and queue depth? Where is lock contention or an N+1 access pattern possible, and what detects it? What are the cache semantics — key, maximum age, invalidation trigger, and stampede protection? Where is backpressure applied, and what is shed first? |
| 6 | **Clean code, SOLID, and design patterns** | Which pattern is applied here, and what does it earn? Which boundary does each module own, and what may cross it? Where would a pattern be decoration rather than structure, and is it absent there? Uniformity across services outranks local cleverness: does this look like the rest of the estate? |
| 7 | **Algorithm and data-structure choice** | What is the stated complexity budget for each hot path, in the input size that actually varies? Which structure was chosen deliberately over which alternative, and why? Where does an operation grow with total data rather than with the requested page? |
| 8 | **Configurability** | Which behaviour varies by environment or scale, and is it configurable with a safe default and validation at the boundary rather than hardcoded? Which value is deliberately not configurable, and why? What happens at startup when a required setting is missing or malformed — fail fast, or run in an undefined state? |
| 9 | **Speed of development and debuggability** | What is the one command that runs the tests, the one that runs the service locally, and the one that reproduces a production failure? How long does the feedback loop take? Guidance that makes correct work slow gets bypassed, so a rule that adds a step must remove one or state what it buys. |
| 10 | **Documentation** | What shipped, how it is operated, and how it fails — where is each of those three written, and which source owns it? What does an on-call responder read at 03:00? Which document must change when this behaviour changes, and what enforces that? |

## Two standing preferences that cut across all ten

**Wrap official capabilities; do not reimplement them.** When a framework, database, broker,
platform, or standard already provides a mechanism, the project uses it and wraps it. A
wrapper around an official mechanism survives an upgrade; a reimplementation accumulates
divergence until it becomes the reason an upgrade is impossible. A constitution that permits
a local reimplementation of an official capability states which capability, why, and what
retires the local version.

**Uniformity outranks local optimality.** Every service in this estate is developed in one
recognisable style. Inconsistency across services costs more in review, on-call, and
migration than any single clever local choice saves. Where a project deviates from an estate
convention, the constitution records the deviation and its reason, so the next agent inherits
a decision rather than an accident.

## Coverage gate

Before writing, verify that each of the ten obligations has, for every owned journey and
high-risk surface, either a candidate with a disposition or a recorded exclusion with its
evidence path. Report the count of exclusions in the final response. An obligation that was
never considered is a gap in the authoring run, not an absence in the project.
