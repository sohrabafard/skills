# Job graph and scheduling

The job graph is this domain's data structure. Everything below is about which
job may start when, and what that costs in wall-clock time and in correctness.

## Table of contents

- Stages versus `needs:`
- What an edge means, and what a missing edge means
- Critical path and the cost of a stage boundary
- `needs:` size and artifact fetching
- `parallel:` and `parallel:matrix`
- `resource_group`
- `interruptible`
- Job `timeout:`
- `retry:` and its failure classes
- Skipping inside a script versus not creating the job

## Stages versus `needs:`

When deciding between stage barriers and explicit job dependencies, use [DAG edges and critical path](./job-graph-and-scheduling/10-dag-edges-and-critical-path.md).

## What an edge means, and what a missing edge means

When reviewing job prerequisites in a DAG, use [DAG edges and critical path](./job-graph-and-scheduling/10-dag-edges-and-critical-path.md).

## Critical path and the cost of a stage boundary

When estimating how a graph change affects pipeline duration, use [DAG edges and critical path](./job-graph-and-scheduling/10-dag-edges-and-critical-path.md).

## `needs:` size and artifact fetching

When checking edge limits or artifact downloads, use [Needs and artifacts](./job-graph-and-scheduling/20-needs-and-artifacts.md).

## `parallel:` and `parallel:matrix`

When configuring parallel jobs or matrices, use [Parallelism and resource groups](./job-graph-and-scheduling/30-parallelism-and-resource-groups.md).

## `resource_group`

When serializing jobs that mutate a shared target, use [Parallelism and resource groups](./job-graph-and-scheduling/30-parallelism-and-resource-groups.md).

## `interruptible`

When deciding whether GitLab may cancel a job, use [Cancellation and timeouts](./job-graph-and-scheduling/40-interruptible-and-timeouts.md).

## Job `timeout:`

When bounding job duration or a resource lock, use [Cancellation and timeouts](./job-graph-and-scheduling/40-interruptible-and-timeouts.md).

## `retry:` and its failure classes

When selecting retryable failure classes, use [Retry failure classes](./job-graph-and-scheduling/50-retry-failure-classes.md).

## Skipping inside a script versus not creating the job

When deciding whether a job should exist, use [Job creation conditions](./job-graph-and-scheduling/60-job-creation-conditions.md).
