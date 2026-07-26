---
name: alaa-algorithms-data-structures
description: "Complexity budgets and structure choice for production service code: stating the bound an operation must hold as its input grows, finding that bound from the system rather than assuming it, choosing a structure from the access pattern, and catching the N+1 family. Use when writing or reviewing a loop, query, fan-out, batch, export, or in-memory collection that grows with tenants, rows, history, or events; when a path was fine in staging and slow in production; when choosing between a list, map, or set; and before a growing path ships with no stated bound. Do not use for a path whose every input dimension already has a small maximum enforced in code. Route Go internals and benchmarks to /golang-data-structures, /golang-performance, and /golang-benchmark; query shape and indexes to /alaa-data-layer; timeout, pool, and cardinality values to /alaa-reliability-sla and /alaa-observability-soc; subsystem design to /alaa-system-design."
---

# Alaa Algorithms And Data Structures

Decide, before the code is written, what an operation is allowed to cost as its input grows, which structure serves the way that input is actually accessed, and which chosen values a deployment may change. The deliverable is a written budget and a named rejected alternative, not a faster implementation. This skill owns that decision and no implementation, syntax, algorithm catalogue, or platform value; it discharges obligation 7 of the quality bar in `/alaa-project-constitution` (`$alaa-project-constitution`). Companion skills are written `/name` for Claude Code and `$name` for Codex; both forms appear at every call site.

## When this applies

Apply the trigger test to one code path at a time; one route can require a budget while every other route in the same file requires none. A path needs a complexity budget when **any** of these three holds, each observable in the code:

1. **Unbounded dimension** — an input dimension feeding the path has no maximum enforced in code that a reader can name.
2. **Per-element remote or blocking work** — the work done once per element is a query, a network call, a cache round trip, a lock acquisition, or a file read, and the element count is not a constant written in the code.
3. **Growing dimension** — the dimension's maximum grows with something the business grows: tenants, rows per tenant, retained history, catalogue size, fan-out per event, or elapsed time.

**When none of the three holds, the path is finished when it is clear.** State no budget, run no benchmark, do not replace a list with a map, and do not stream what already fits — each of those costs a reader on every future change and defends against a load the enforced maximum already prevents.

## The complexity budget

**A complexity budget is one sentence with four parts: the named operation, the input dimension that grows, the bound the operation must hold as that dimension grows, and the input size at which the bound was measured or reasoned. Fewer than four parts is not a budget.**

```text
<operation> is <bound> in <dimension>, <measured|reasoned> at <dimension> = <size>.
```

- **A budget with no named growing dimension is not a budget.** "It is fast" is a statement about today's data, and today's data is the one input size the operation is guaranteed to be acceptable on. Naming the dimension makes the claim falsifiable next year.
- **A budget with no stated input size cannot be re-checked**, because the size is what a later reader re-measures against.
- **The budget is written before the implementation**, because one produced afterwards records what was built instead of deciding it and is always satisfied by the code that produced it.
- **Cost introduced as a security or correctness requirement is budgeted like any other cost, against the rate of the path it sits on**: per-request cost multiplied by peak request rate is stated before the choice is accepted. A cost that is correct once per login is a denial of service once per authenticated request — a memory-hard key derivation on a token verification path reads as a security measure and behaves as a self-inflicted outage. `/alaa-security-review` (`$alaa-security-review`) owns which primitive belongs on which path; stating its cost against peak rate belongs here.

## Finding the real bound on N

This is the step agents skip, and skipping it makes every decision after it arbitrary.

**The bound on an input dimension is found in the system, never assumed. Read it from a boundary that enforces it — a page size cap, a batch cap, a recursion or depth limit, a quota, a schema cardinality, a fan-out list length — or from the largest value the dimension has actually reached in production multiplied by the growth horizon the design states. The value used is the largest the system permits, never the typical or median one. A dimension whose bound cannot be found either way is unbounded, and an unbounded dimension on a path with a deadline is a design defect to report, never a number to guess.**

Two rules follow:

- **A bound you cannot compute is not a bound.** When a worst case is a product of other dimensions — recipients per notification times channels per recipient, rows times replicas — compute the product and record it. "It is probably small" is an unbounded answer and is treated as unbounded. `/alaa-observability-soc` (`$alaa-observability-soc`) applies this to metric cardinality; the general form is owned here.
- **A boundary is how an unbounded input becomes bounded.** The fix is to add the enforcing boundary — maximum page size, batch, depth, or array length in the request schema — in the same change, then cite it as the bound's source. Reporting an unbounded input without naming the boundary that would bound it leaves the next engineer the same question.

Every bound carries its source, labelled `boundary`, `measurement`, or `assumption`. An assumption is legitimate and checkable later; a bound with no source is re-guessed at the next incident.

## Choosing a structure

**The structure follows the access pattern, not the shape of the data.** A list looked up by identifier a thousand times per request is a map that happened to arrive as a list.

Answer these five before naming a structure; one chosen without them is the first that came to mind.

1. **What is looked up, by what key, how many times?** More than one lookup by one key over one collection means it is indexed by that key once, before the loop.
2. **Must the result stay ordered, and by what?** Ordering is established once at the boundary producing the data, never inside an iteration.
3. **Is membership the only question, and must values be unique?** Both yes means a set; a list used for membership makes every check proportional to the list.
4. **Traversed whole, indexed by position, or reached by key?** Traversed whole and never keyed is where the simplest sequence wins and an index on it is unused weight.
5. **How is it mutated, by how many writers, and does it outlive one request?** A structure outliving one request is a cache and inherits every obligation `/alaa-data-layer` (`$alaa-data-layer`) puts on a cache.

**When the authoritative copy lives in a database and the lookup key is a column, the answer is an index on that column and a query, not an in-memory map.** An in-memory map of a table is a cache with no invalidation whose memory grows with the table rather than the request, and it is stale the moment another replica writes.

**Every value used as a map key, set member, deduplication key, or comparison key has a stated normalisation applied before that use** — field order, encoding, case, absent-versus-empty, numeric form. Without one, two values a human calls equal hash differently, and the duplicate is silent: no error, one extra row, one extra notification, one missed idempotency hit.

Record the alternative rejected and the condition that would revive it; a choice with no rejected alternative is not yet a choice.

## The call in a loop

The N+1 query is one instance of a family — the same defect appears in database access, HTTP fan-out, cache lookups, permission checks, and file reads — and it is the most common real complexity defect in this estate.

**Detection rule: a call that leaves the process — a query, an HTTP request, a cache round trip, an authorization check, a file read — inside a loop whose iteration count is not a constant written in the code. The rule is about the call's effect, not its syntax: a lazy relation accessor, a property getter, a decorator, and a middleware all issue the call with no call site that looks like one.**

Resolutions, in the order to try them:

1. **One call for the whole set** — a join, an `IN` list, a batch endpoint, a pipelined cache read, a bulk authorization check.
2. **Prefetch and index** — fetch every needed key in one call before the loop, build a map keyed by the loop's lookup key, read the map inside the loop.
3. **Restructure so the loop is unnecessary** — push the aggregation, filter, or ordering to the component that already holds the data.
4. **Bound the loop** — when the per-element call genuinely cannot be batched, its dimension gets an enforced maximum and the budget states the resulting call count. This is the only form in which a process-leaving call may remain inside a loop.

**Batching changes the failure mode, so a batch is unfinished until its own maximum and its partial-failure behaviour are stated.** Five hundred separate calls fail independently; one batch of five hundred fails once and wholly, holds one connection for its whole duration, and produces one timeout instead of five hundred retries. Retry legality, backoff, and idempotency for that batch belong to `/alaa-reliability-sla` (`$alaa-reliability-sla`).

## Memory as a budget

**Peak memory is stated as proportional to a named dimension. A result set, file, export, or import whose element count is one of the path's growing dimensions is streamed in chunks, never materialised whole, because materialising makes peak memory proportional to total data while the response stays proportional to one page.** The chunk size is a stated value with a default and a validated range, never a literal inside the loop. That failure arrives at the container's memory limit rather than at any timeout, so its symptom is a restart, not a slow response.

## Tuning points

Both halves are defects alone. A value hardcoded where deployments differ cannot change without a release; a value made configurable where nothing differs moves an undecided question into a file nobody reads.

**Configurable when, and only when, one is true:** it must differ between environments or deployments of the same code; it must differ with a scale factor the deployment sets, such as replica count or tenant size; or it must be changeable during an incident without a deploy, and someone can name the observable that would prompt the change.

**A named constant in code when:** it is derivable from another configured value, in which case derive it; it is a correctness constraint rather than a performance one, such as a batch cap that also bounds a transaction; or nobody can state what a different value would do, which means the decision has not been made and configuration hides that.

**Every configurable value ships three things or it is not configurable, it is unset:** a default safe at the worst case rather than optimal at the typical one; a validated range checked at startup, where an out-of-range or missing value fails the boot with a message naming the setting; and one sentence stating what changes when it moves and in which direction.

## Proving it

**A complexity claim is verified by measuring at two input sizes and comparing the observed ratio against the shape the bound predicts. One measurement establishes a constant and can never establish a shape, so a bound reported from a single run is reported as reasoned, not measured.**

Ten times the input moves a linear bound roughly ten times, a quadratic bound roughly a hundred, a logarithmic bound barely at all. A ratio disagreeing with the claimed shape means the claim is wrong, the run was dominated by fixed cost, or a second dimension moved — resolve which before reporting either number. The larger size is at or above the bound found in step 3, because a measurement below the enforced maximum proves nothing about the path at its maximum. `/alaa-testing-strategy` (`$alaa-testing-strategy`) owns whether a benchmark counts as evidence and at which proof level; `/golang-benchmark` (`$golang-benchmark`) owns Go benchmark and profiling mechanics.

## The procedure, and when to read each reference

Walk in order. Each step names the one reference owning its detail and the condition for opening it. Read only those whose condition this task meets; loading the whole tree means the task was not scoped. Every budget decision, structure choice, and review of either returns the report block in `references/10-complexity-budget.md`, in the order given there, with any field the task did not reach marked `not reached` rather than omitted.

1. **Apply the trigger test**; if none of the three conditions holds, write the clearest code and stop here. — `references/80-when-not-to.md`, when the test did not fire and an optimisation is still proposed.
2. **Name the operation and every input dimension feeding it**, then state the budget once step 3 supplies the bounds. — `references/10-complexity-budget.md`, when writing or reviewing a budget, and before returning any report.
3. **Find the real bound on each dimension, with its source**, and report any unbounded dimension with the boundary that would bound it. — `references/20-finding-n.md`, before stating any budget, and whenever a bound is about to be assumed.
4. **Choose the structure from the access pattern**, recording the rejected alternative. — `references/30-choosing-a-structure.md`, when a collection is introduced or a lookup is added over an existing one.
5. **Scan every loop over a growing dimension for a call that leaves the process**, and resolve each. — `references/40-call-in-a-loop.md`, when a loop body reaches a database, service, cache, authorization check, or file.
6. **State peak memory and decide materialise versus stream.** — `references/50-memory-and-streaming.md`, when a result set, export, import, or file is read whole.
7. **Decide which values are configurable**, with defaults and boundary validation. — `references/60-tuning-points.md`, when a numeric constant is about to be written into code or configuration.
8. **Measure at two input sizes** and compare against the claimed shape. — `references/70-proving-it.md`, before reporting any complexity or performance claim.

## Stop conditions

Stop successfully when every dimension has a bound with a source, every budget carries all four parts, every structure names its rejected alternative, every loop over a growing dimension is free of unresolved process-leaving calls, and every reported bound was measured at two sizes or labelled reasoned.

Stop and report blocked when: a dimension has no enforced maximum and adding the boundary is outside this change's scope, in which case name the boundary that would fix it; a worst case is a product that cannot be computed; the second input size cannot be produced here and the claim depends on shape rather than constant; or the right structure needs a schema, index, or query change owned by `/alaa-data-layer` (`$alaa-data-layer`).

## What this skill does not own

This skill decides inside whatever the skills below define, and states none of their values. The four `golang-*` packs are vendored upstream: route to them for mechanics, never restate or edit them.

| Owner | What it owns |
|---|---|
| `/golang-data-structures` (`$golang-data-structures`) | Go slice, map, container internals; capacity growth; preallocation; copy semantics |
| `/golang-performance` (`$golang-performance`) | Go optimisation patterns once a bottleneck is identified |
| `/golang-benchmark` (`$golang-benchmark`) | Go benchmark, `pprof`, `benchstat` mechanics |
| `/golang-concurrency` (`$golang-concurrency`) | Goroutine, channel, synchronisation mechanics |
| `/alaa-php-clean-code` (`$alaa-php-clean-code`), `/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`), `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`) | Language idiom, design patterns, and each framework's own N+1 fix |
| `/alaa-data-layer` (`$alaa-data-layer`) | Query shape, index design, keyset pagination, driver and pool mechanics, cache semantics |
| `/alaa-observability-soc` (`$alaa-observability-soc`) | Telemetry's quantitative budgets: cardinality ceilings, histogram boundaries, sampling rates |
| `/alaa-services-contract` (`$alaa-services-contract`) | Every Ala platform value: deadlines, timeouts, pool maxima, in-flight limits |
| `/alaa-reliability-sla` (`$alaa-reliability-sla`) | Retry, breaker, shedding, degradation, and idempotency doctrine |
| `/alaa-system-design` (`$alaa-system-design`) | Subsystem design: boundaries, dependency table, assumed peak, growth horizon |
| `/alaa-testing-strategy` (`$alaa-testing-strategy`) | Whether a benchmark is evidence, and at which proof level a claim may be reported |
| `/alaa-security-review` (`$alaa-security-review`) | Which cryptographic primitive belongs on which path |
| `/alaa-controlled-ops` (`$alaa-controlled-ops`) | That package's canonical digest specification |
| `/alaa-project-constitution` (`$alaa-project-constitution`) | The quality bar whose obligation 7 this skill discharges |
| `/alaa-prompting-guide` (`$alaa-prompting-guide`) | Model and effort selection — never name a model here |

## Anti-patterns

- "it is fast", or any bound with no dimension, offered as a budget;
- a bound taken from the median tenant or the demo dataset instead of the largest the system permits;
- replacing a list with a map, or a loop with a clever traversal, on a path whose every dimension has a small maximum enforced in code;
- a batch introduced to fix an N+1 with no cap of its own, turning many bounded calls into one unbounded query;
- a knob added because the correct value was never decided, with no default, no validated range, and no statement of what moving it changes;
- restating a timeout, pool size, page cap, or cardinality ceiling a contract skill owns, creating a second copy that drifts.
