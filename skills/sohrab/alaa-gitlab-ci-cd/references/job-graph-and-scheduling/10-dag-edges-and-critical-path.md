# DAG edges and critical path

Open this guide when the task involves job ordering, dependencies and critical-path analysis. The topic map routes to this file.

For current feature claims and release qualifications, use the [source map](../00-source-map.md) and [version notes](../feature-version-notes.md).

## Stages versus `needs:`

`stages` orders jobs in bands: no job in band *n+1* starts until every job in band
*n* has finished. `needs:` replaces that with a directed acyclic graph: a job
starts when the jobs it names have finished, regardless of stage.

Use `needs:` when a downstream job's real precondition is one or two upstream
jobs rather than a whole band, and when the wall-clock saving is larger than the
review cost of the extra edges. Keep stages as the readable spine even when every
job carries `needs:`; the stage names are what a reader sees in the UI.

`needs:` buys parallelism only among jobs that do not contend for the same
`resource_group`. See [resource-group serialization](./30-parallelism-and-resource-groups.md).

## What an edge means, and what a missing edge means

An edge is a precondition, not decoration. Two failure directions, and the second
is the one that reaches production:

- **Too many edges.** An over-specified DAG is harder to refactor: renaming a job
  breaks every edge that names it, and the graph stops matching the mental model.
  Cost is maintenance.
- **Too few edges.** A job that no other job needs is not "last"; it is
  *unordered*. Under DAG semantics a job in a later stage starts as soon as *its
  own* needs complete, so it can run while an unreferenced job is still running,
  or after that job has already failed. The pipeline goes red and the deploy has
  already happened. Cost is correctness.

The rule: for every job B whose correctness depends on job A having finished
successfully, B declares `needs: [A]`. A stage boundary is not a substitute,
because the moment any job uses `needs:` the pipeline is a DAG.

`validate_gitlab_ci.py` reports the second direction as `dag-orphan`.

## Critical path and the cost of a stage boundary

The pipeline's duration is the longest path through the graph, not the sum of the
jobs. Two consequences worth stating in any answer that restructures a pipeline:

- A stage boundary costs the difference between the slowest job in the band and
  each other job in it. Splitting a slow job out of a band and giving its
  dependants explicit `needs:` removes that difference.
- Adding a job to the middle of the critical path adds its whole duration.
  Adding a job off the critical path adds nothing until it becomes the longest
  path.

Compute the critical path before proposing a reordering, and state the before and
after in the answer. Where the target duration itself is in question — how long a
pipeline is allowed to take before it stops being a feedback loop — that is a
service-level decision and belongs to `/alaa-reliability-sla`.
