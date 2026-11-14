---
name: alaa-algorithms-data-structures
description: "Complexity budgets and structure choice for service code: stating the bound an operation must hold as input grows, finding it from the system rather than assuming, choosing a structure from the access pattern, and catching the N+1 family. Use when writing or reviewing a loop, query, fan-out, batch, export, or in-memory collection that grows with tenants, rows, history, or events; when a path was fine in staging and slow in production; when choosing between a list, map, or set; and before a growing path ships with no stated bound. Do not use for a path whose every input already has a small maximum enforced in code. Route Go internals to /golang-data-structures, /golang-performance, and /golang-benchmark; query shape to /alaa-data-layer; timeout and cardinality values to /alaa-reliability-sla and /alaa-observability-soc; subsystem design to /alaa-system-design."
---

# Alaa Algorithms And Data Structures

Before the code is written, decide three things: what an operation may cost as its input grows, which structure serves the way the input is actually accessed, and which chosen values a deployment may change. The deliverable is a written budget and a named rejected alternative, not a faster implementation. This skill owns that decision. It owns no implementation, syntax, algorithm catalogue, or platform value. It discharges obligation 7 of the quality bar in `/alaa-project-constitution`. Write cross-skill references as `/name`.

## When this applies

Apply the trigger test to one code path at a time. One route can require a budget while every other route in the same file requires none. A path needs a complexity budget when **any** of these three conditions holds. Each is observable in the code:

1. **Unbounded dimension** — an input dimension feeding the path has no maximum enforced in code that a reader can name.
2. **Per-element remote or blocking work** — the work done once per element is a query, a network call, a cache round trip, a lock acquisition, or a file read, and the element count is not a constant written in the code.
3. **Growing dimension** — the dimension's maximum grows with something the business grows: tenants, rows per tenant, retained history, catalogue size, fan-out per event, or elapsed time.

**When none of the three holds, the path is finished when it is clear.** State no budget. Run no benchmark. Do not replace a list with a map. Do not stream what already fits. Each of those costs a reader on every future change and defends against a load the enforced maximum already prevents.

## The complexity budget

**A complexity budget is one sentence with four parts: the named operation, the input dimension that grows, the bound the operation must hold as that dimension grows, and the input size at which the bound was measured or reasoned. Fewer than four parts is not a budget.**

```text
<operation> is <bound> in <dimension>, <measured|reasoned> at <dimension> = <size>.
```

- **A budget with no named growing dimension is not a budget.** "It is fast" states something about today's data. Today's data is the one input size the operation is guaranteed to be acceptable on. Naming the dimension makes the claim falsifiable next year.
- **A budget with no stated input size cannot be re-checked**, because the size is what a later reader re-measures against.
- **Write the budget before the implementation.** A budget produced afterwards records what was built instead of deciding it. The code that produced it always satisfies it.
- **Budget a cost introduced as a security or correctness requirement like any other cost, against the rate of the path it sits on.** State per-request cost multiplied by peak request rate before you accept the choice. A cost that is correct once per login is a denial of service once per authenticated request. Example: a memory-hard key derivation on a token verification path reads as a security measure and behaves as a self-inflicted outage. `/alaa-security-review` owns which primitive belongs on which path. Stating its cost against peak rate belongs here.

## Finding the real bound on N

This is the step agents skip, and skipping it makes every decision after it arbitrary.

**The bound on an input dimension is found in the system, never assumed. Read it from a boundary that enforces it: a page size cap, a batch cap, a recursion or depth limit, a quota, a schema cardinality, a fan-out list length. Or read it from the largest value the dimension has actually reached in production multiplied by the growth horizon the design states. The value used is the largest the system permits, never the typical or median one. A dimension whose bound cannot be found either way is unbounded. An unbounded dimension on a path with a deadline is a design defect to report, never a number to guess.**

Two rules follow:

- **A bound you cannot compute is not a bound.** When a worst case is a product of other dimensions, compute the product and record it. Examples: recipients per notification times channels per recipient, rows times replicas. "It is probably small" is an unbounded answer. Treat it as unbounded. `/alaa-observability-soc` applies this rule to metric cardinality. This skill owns the general form.
- **A boundary is how an unbounded input becomes bounded.** The fix is to add the enforcing boundary in the same change: a maximum page size, batch, depth, or array length in the request schema. Then cite it as the bound's source. A report of an unbounded input that does not name the boundary that would bound it leaves the next engineer the same question.

Every bound carries its source, labelled `boundary`, `measurement`, or `assumption`. An assumption is legitimate and checkable later. A bound with no source is re-guessed at the next incident.

## Choosing a structure

**The structure follows the access pattern, not the shape of the data.** A list looked up by identifier a thousand times per request is a map that happened to arrive as a list.

Answer these five questions before you name a structure. A structure chosen without them is the first one that came to mind.

1. **What is looked up, by what key, how many times?** When a collection has more than one lookup by one key, index it by that key once, before the loop.
2. **Must the result stay ordered, and by what?** Establish ordering once, at the boundary that produces the data, never inside an iteration.
3. **Is membership the only question, and must values be unique?** When both answers are yes, use a set. A list used for membership makes every check proportional to the list.
4. **Traversed whole, indexed by position, or reached by key?** When a collection is traversed whole and never keyed, the simplest sequence wins. An index on it is unused weight.
5. **How is it mutated, by how many writers, and does it outlive one request?** A structure that outlives one request is a cache. It inherits every obligation `/alaa-data-layer` puts on a cache.

**When the authoritative copy lives in a database and the lookup key is a column, the answer is an index on that column and a query, not an in-memory map.** An in-memory map of a table is a cache with no invalidation. Its memory grows with the table, not the request. It is stale the moment another replica writes.

**Every value used as a map key, set member, deduplication key, or comparison key has a stated normalisation applied before that use** (field order, encoding, case, absent-versus-empty, numeric form). Without one, two values a human calls equal hash differently. The duplicate is silent: no error, one extra row, one extra notification, one missed idempotency hit.

Record the rejected alternative and the condition that would revive it. A choice with no rejected alternative is not yet a choice.

## The call in a loop

The N+1 query is one instance of a family. The same defect appears in database access, HTTP fan-out, cache lookups, permission checks, and file reads. It is the most common real complexity defect in this estate.

**Detection rule: a call that leaves the process (a query, an HTTP request, a cache round trip, an authorization check, a file read) inside a loop whose iteration count is not a constant written in the code. The rule is about the call's effect, not its syntax. A lazy relation accessor, a property getter, a decorator, and a middleware all issue the call with no call site that looks like one.**

Try these resolutions in this order:

1. **One call for the whole set** — a join, an `IN` list, a batch endpoint, a pipelined cache read, a bulk authorization check.
2. **Prefetch and index.** Fetch every needed key in one call before the loop. Build a map keyed by the loop's lookup key. Read the map inside the loop.
3. **Restructure so the loop is unnecessary.** Push the aggregation, filter, or ordering to the component that already holds the data.
4. **Bound the loop.** Use this when the per-element call genuinely cannot be batched. Give its dimension an enforced maximum. State the resulting call count in the budget. This is the only form in which a process-leaving call may remain inside a loop.

**A batch is unfinished until its own maximum and its partial-failure behaviour are stated.** Batching changes the failure mode. Five hundred separate calls fail independently. One batch of five hundred fails once and wholly, holds one connection for its whole duration, and produces one timeout instead of five hundred retries. Retry legality, backoff, and idempotency for that batch belong to `/alaa-reliability-sla`.

## Memory as a budget

**State peak memory as proportional to a named dimension. Stream a result set, file, export, or import in chunks when its element count is one of the path's growing dimensions. Never materialise it whole. Materialising makes peak memory proportional to total data while the response stays proportional to one page.** The chunk size is a stated value with a default and a validated range, never a literal inside the loop. The materialising failure arrives at the container's memory limit, not at any timeout. Its symptom is a restart, not a slow response.

## Tuning points

Both halves are defects alone. A value hardcoded where deployments differ cannot change without a release. A value made configurable where nothing differs moves an undecided question into a file nobody reads.

**Configurable when, and only when, one is true:**

- it must differ between environments or deployments of the same code;
- it must differ with a scale factor the deployment sets, such as replica count or tenant size;
- it must be changeable during an incident without a deploy, and someone can name the observable that would prompt the change.

**A named constant in code when:**

- it is derivable from another configured value, in which case derive it;
- it is a correctness constraint rather than a performance one, such as a batch cap that also bounds a transaction;
- nobody can state what a different value would do. The decision has not been made, and configuration hides that.

**Every configurable value ships three things or it is not configurable, it is unset:**

- a default safe at the worst case rather than optimal at the typical one;
- a validated range checked at startup, where an out-of-range or missing value fails the boot with a message naming the setting;
- one sentence stating what changes when it moves and in which direction.

## Proving it

**A complexity claim is verified by measuring at two input sizes and comparing the observed ratio against the shape the bound predicts. One measurement establishes a constant and can never establish a shape, so a bound reported from a single run is reported as reasoned, not measured.**

Ten times the input moves a linear bound roughly ten times, a quadratic bound roughly a hundred times, and a logarithmic bound barely at all. A ratio that disagrees with the claimed shape means one of three things: the claim is wrong, fixed cost dominated the run, or a second dimension moved. Resolve which before you report either number. The larger size is at or above the bound found in step 3, because a measurement below the enforced maximum proves nothing about the path at its maximum. `/alaa-testing-strategy` owns whether a benchmark counts as evidence and at which proof level. `/golang-benchmark` owns Go benchmark and profiling mechanics.

## The procedure, and when to read each reference

Walk the steps in order. Each step names the one reference that owns its detail and the condition for opening it. Read only the references whose condition this task meets. Loading the whole tree means the task was not scoped. Every budget decision, structure choice, and review of either returns the report block in `references/10-complexity-budget.md`, in the order given there. Mark any field the task did not reach `not reached`. Do not omit it.

1. **Apply the trigger test.** If none of the three conditions holds, write the clearest code and stop here. — `references/80-when-not-to.md`, when the test did not fire and an optimisation is still proposed.
2. **Name the operation and every input dimension feeding it.** Then state the budget once step 3 supplies the bounds. — `references/10-complexity-budget.md`, when writing or reviewing a budget, and before returning any report.
3. **Find the real bound on each dimension, with its source.** Report any unbounded dimension with the boundary that would bound it. — `references/20-finding-n.md`, before stating any budget, and whenever a bound is about to be assumed.
4. **Choose the structure from the access pattern.** Record the rejected alternative. — `references/30-choosing-a-structure.md`, when a collection is introduced or a lookup is added over an existing one.
5. **Scan every loop over a growing dimension for a call that leaves the process.** Resolve each. — `references/40-call-in-a-loop.md`, when a loop body reaches a database, service, cache, authorization check, or file.
6. **State peak memory and decide materialise versus stream.** — `references/50-memory-and-streaming.md`, when a result set, export, import, or file is read whole.
7. **Decide which values are configurable.** Give each a default and boundary validation. — `references/60-tuning-points.md`, when a numeric constant is about to be written into code or configuration.
8. **Measure at two input sizes.** Compare against the claimed shape. — `references/70-proving-it.md`, before reporting any complexity or performance claim.

## Stop conditions

Stop successfully when all of these hold:

- every dimension has a bound with a source;
- every budget carries all four parts;
- every structure names its rejected alternative;
- every loop over a growing dimension is free of unresolved process-leaving calls;
- every reported bound was measured at two sizes or labelled reasoned.

Stop and report blocked when any of these holds:

- a dimension has no enforced maximum and adding the boundary is outside this change's scope. In that case, name the boundary that would fix it;
- a worst case is a product that cannot be computed;
- the second input size cannot be produced here and the claim depends on shape rather than constant;
- the right structure needs a schema, index, or query change owned by `/alaa-data-layer`.

## When NOT to use

- Every input dimension the path touches already has a small maximum enforced in code — a fixed enum, a
  schema-bounded column set, a list whose length a validator caps. There is no growth to bound.
- The work is a one-off script over a known fixed input that will not be run again against a larger one.
- The change alters no loop, no query, no fan-out, no batch, no export, and no retained collection.
- The question is which index serves a query, what a timeout or pool value should be, or how a subsystem
  is shaped. The routing table below names each owner.

## What this skill does not own

This skill decides inside whatever the skills below define. It states none of their values. The four `golang-*` packs are vendored upstream. Route to them for mechanics. Never restate or edit them.

| Owner | What it owns |
|---|---|
| `/golang-data-structures` | Go slice, map, container internals; capacity growth; preallocation; copy semantics |
| `/golang-performance` | Go optimisation patterns once a bottleneck is identified |
| `/golang-benchmark` | Go benchmark, `pprof`, `benchstat` mechanics |
| `/golang-concurrency` | Goroutine, channel, synchronisation mechanics |
| `/alaa-php-clean-code`, `/alaa-golang-clean-code-principles`, `/alaa-vue-typescript-clean-code` | Language idiom, design patterns, and each framework's own N+1 fix |
| `/alaa-data-layer` | Query shape, index design, keyset pagination, driver and pool mechanics, cache semantics |
| `/alaa-observability-soc` | Telemetry's quantitative budgets: cardinality ceilings, histogram boundaries, sampling rates |
| `/alaa-services-contract` | Every Ala platform value: deadlines, timeouts, pool maxima, in-flight limits |
| `/alaa-reliability-sla` | Retry, breaker, shedding, degradation, and idempotency doctrine |
| `/alaa-system-design` | Subsystem design: boundaries, dependency table, assumed peak, growth horizon |
| `/alaa-testing-strategy` | Whether a benchmark is evidence, and at which proof level a claim may be reported |
| `/alaa-security-review` | Which cryptographic primitive belongs on which path |
| `/alaa-controlled-ops` | That package's canonical digest specification |
| `/alaa-project-constitution` | The quality bar whose obligation 7 this skill discharges |
| `/alaa-prompting-guide` | Model and effort capability evidence; the runtime orchestrator owns task allocation. Never name a model here |

## Anti-patterns

- "it is fast", or any bound with no dimension, offered as a budget;
- a bound taken from the median tenant or the demo dataset instead of the largest the system permits;
- replacing a list with a map, or a loop with a clever traversal, on a path whose every dimension has a small maximum enforced in code;
- a batch introduced to fix an N+1 with no cap of its own, turning many bounded calls into one unbounded query;
- a knob added because the correct value was never decided, with no default, no validated range, and no statement of what moving it changes;
- restating a timeout, pool size, page cap, or cardinality ceiling a contract skill owns, creating a second copy that drifts.
