# Parallelism and resource groups

Open this guide when the task involves parallel jobs, matrices or shared-target serialization. The topic map routes to this file.

For current feature claims and release qualifications, use the [source map](../00-source-map.md) and [version notes](../feature-version-notes.md).

## `parallel:` and `parallel:matrix`

`parallel: N` runs one job definition as N instances that differ only in
`CI_NODE_INDEX` and `CI_NODE_TOTAL`; the job script must shard its own work from
those two variables. Use it when the work divides evenly and the runner fleet has
N free slots — N instances that queue behind each other are slower than one job,
because each pays its own setup.

`parallel:matrix:` runs one job definition once per combination of the variable
values listed, and each instance gets those variables set. Use it when the
dimensions are real (PHP version, database version, architecture) and name them
in the answer, because the instance count is the product of the dimensions and
grows faster than a reader expects.

Both multiply cache and artifact traffic by the instance count. Give matrix jobs
a cache key that includes the varying dimension, or every instance overwrites the
same cache entry.

## `resource_group`

A resource group admits one job at a time across the whole project. Use it for
any job that mutates a shared target: a production deploy, a release publish, a
schema change, a shared test environment, a registry tag another pipeline may
push.

**Name it after the target it protects, never after the pipeline.** One group
applied to every job serialises the entire pipeline: the `needs:` graph still
exists, nothing can use it, and the pipeline pays the sum of its jobs' durations
instead of its critical path. Two different targets get two different groups; one
target reached from two projects needs a shared coordinator or external lock.
Resource groups are project-scoped: identical names in different projects do not
serialize each other. See https://docs.gitlab.com/api/resource_groups/.
`validate_gitlab_ci.py` reports the saturated case as `resource-group-saturation`.

`process_mode` decides which waiting job runs next when the group frees up:
`unordered` (default), `oldest_first`, `newest_first`, or `newest_ready_first`.
The last two prioritize descending pipeline IDs and require idempotent jobs;
`newest_ready_first` considers jobs already waiting for the resource. Queue order
does not discard older deployments. Configure outdated-deployment protection
separately. Changing the mode uses the resource-group API and needs mutation
authority. Source: https://docs.gitlab.com/ci/resource_groups/.
