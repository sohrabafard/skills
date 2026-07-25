# Proving A Complexity Claim

Load before reporting any complexity or performance claim.

`SKILL.md` owns the rule: measure at two input sizes, compare the observed ratio against the shape the bound
predicts, and report a single-run claim as reasoned rather than measured. This file says how to run the comparison so
the ratio means something, and how to read a disagreement.

Mechanics are not here. `/golang-benchmark` (`$golang-benchmark`) owns Go benchmarks, `pprof`, and `benchstat`;
`/alaa-testing-strategy` (`$alaa-testing-strategy`) owns whether a benchmark is evidence, at which proof level, and
how a result is reported. This file owns only the two-size comparison.

## The comparison

1. **Pick the dimension** the budget names. One dimension moves; everything else is held fixed. Two dimensions
   moving together produce a ratio nobody can attribute.
2. **Pick two sizes**, the larger at or above the enforced maximum from `20-finding-n.md`, and the smaller a clean
   multiple below it — ten times apart is easiest to read. A measurement below the enforced maximum proves nothing
   about the path at its maximum, which is the only size the budget is about.
3. **Hold the environment fixed** across both runs: same machine, same concurrency, same warm or cold state, same
   dataset shape. A ratio taken across two environments measures the environments.
4. **Discard the first run** or run long enough that startup, connection establishment, cache warming, and
   compilation are not in the sample.
5. **Compare the ratio to the shape.** Ten times the input predicts roughly ten times for a linear bound, a hundred
   for a quadratic one, and barely any change for a logarithmic one.

## Reading a disagreement

A ratio that does not match the claimed shape has exactly three explanations, and the report names which one:

- **The claim is wrong.** The most common case, and the reason the measurement exists. A ratio well above the
  claimed shape usually means a call inside a loop — go to `40-call-in-a-loop.md`.
- **Fixed cost dominated.** At the smaller size the constant overhead swamped the variable part, so the ratio
  understates growth. Diagnose by adding a third, larger size: if the ratio between the two larger sizes matches the
  shape, the claim holds and the small size was the problem.
- **A second dimension moved.** The larger dataset was not just larger — deeper, wider, more distinct keys, more
  tenants. Fix the fixture and re-run rather than explaining the number.

A ratio *below* the claimed shape is not a success to report. It usually means the larger input did not exercise the
path — a filter, a cache, a short-circuit, or an early return kept the work small — and the measurement therefore
says nothing.

## What the measurement must exercise

- **The real data shape**, not a uniform synthetic one. A structure whose cost depends on key distribution behaves
  differently on sequential fixture keys than on production keys.
- **The real engine** for anything the engine decides: a query plan changes with table size, so a plan measured on a
  thousand rows is not the plan that runs on a million. `/alaa-data-layer` (`$alaa-data-layer`) owns plan reading.
- **The concurrency the path actually runs at**, when the budget is about a shared resource — a pool, a lock, a
  single-threaded consumer. A serial measurement of a contended resource measures the uncontended case.

## Reporting

State: the dimension, both sizes, both observed results, the ratio, the claimed shape, and whether they agree. Then
state the environment, because a number with no environment cannot be reproduced or compared with a later run.

A claim that could not be measured is reported as reasoned, with the reasoning and the blocker that prevented
measurement. That is a legitimate outcome and is materially different from a measured claim; reporting it as
measured invents evidence.

## Anti-patterns

- one measurement, reported as proof of a bound;
- two measurements at sizes both below the enforced maximum;
- comparing a run on a laptop with a run in the cluster;
- a benchmark whose fixture is small enough to stay in cache at both sizes;
- a ratio that disagrees with the claim, reported with the claim unchanged;
- reporting a percentage improvement with no input size, which is a constant-factor claim wearing a complexity
  claim's clothes;
- profiling to find what to optimise before any measurement has established that the path is outside its budget.
