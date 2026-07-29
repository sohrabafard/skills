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

`stages` orders jobs in bands: no job in band *n+1* starts until every job in band
*n* has finished. `needs:` replaces that with a directed acyclic graph: a job
starts when the jobs it names have finished, regardless of stage.

Use `needs:` when a downstream job's real precondition is one or two upstream
jobs rather than a whole band, and when the wall-clock saving is larger than the
review cost of the extra edges. Keep stages as the readable spine even when every
job carries `needs:`; the stage names are what a reader sees in the UI.

`needs:` buys parallelism only among jobs that do not contend for the same
`resource_group`. See below.

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
service-level decision and belongs to `/alaa-reliability-sla`
(`$alaa-reliability-sla`).

## `needs:` size and artifact fetching

`needs:` accepts a maximum number of jobs per job. It is a **plan limit**
(`ci_needs_size_limit`), not a constant of the YAML language: it differs between
GitLab.com plans and is adjustable on self-managed instances through the Plan
Limits API or the Rails console. Do not write a number into a design; state that
the limit exists, is instance-dependent, and must be checked against the target
instance if a job approaches a few dozen edges.

`needs:` also controls artifact download. Be explicit:

```yaml
deploy:
  needs:
    - job: build          # ordering and artifacts
      artifacts: true
    - job: security_scan  # ordering only
      artifacts: false
```

`dependencies:` controls artifact download and nothing else. If a job declares
`needs:`, express artifact fetching through `needs:artifacts:` and do not add a
second `dependencies:` list saying something different.

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
target reached from two projects gets the same group name in both.
`validate_gitlab_ci.py` reports the saturated case as `resource-group-saturation`.

`process_mode` decides which waiting job runs next when the group frees up:
`unordered` (default, no guarantee), `oldest_first`, or `newest_first`. For a
deploy group, `newest_first` deploys the latest commit and discards intermediate
ones; `oldest_first` deploys every commit in order. Choose deliberately and say
which, because the default guarantees neither.

## `interruptible`

`interruptible: true` lets GitLab cancel the job when a newer pipeline supersedes
it on the same ref. It is correct for anything whose only output is a verdict:
lint, tests, type checks, a build whose artifact the superseding pipeline will
rebuild anyway.

It is wrong for any job that mutates something outside the pipeline. A cancelled
`migrate` is a half-applied migration; a cancelled release is a tag pushed with
no release object; a cancelled deploy is a partially rolled-out workload.

Set `interruptible: false` explicitly on every mutating job. This matters most
when `interruptible: true` sits in `default:` or a hidden template, because then
every job inherits it and only the jobs that override are safe.
`validate_gitlab_ci.py` resolves that inheritance and reports
`interruptible-on-mutating-job`.

## Job `timeout:`

Set `timeout:` on every job. Without it, the project-wide timeout applies, and
that value is invisible from the pipeline file — a reader cannot tell whether a
job is allowed ten minutes or three hours.

Two cases where it is not optional:

- A job holding a `resource_group`. Its timeout is how long a hung job blocks
  every other job that needs the same target.
- A job with an `environment:`. Its timeout bounds how long a deployment can be
  in flight before the pipeline gives up on it.

Where a job's own tooling has an internal deadline (a `helm --timeout`, a
`kubectl wait`), derive the internal deadline from `CI_JOB_TIMEOUT` minus a
buffer, so the tool reports its own failure before the runner kills the job and
loses the diagnosis. What that deadline *should be* is a reliability decision:
`/alaa-reliability-sla` (`$alaa-reliability-sla`) owns the value; this file owns
where it is written.

## `retry:` and its failure classes

A bare integer retries **every** failure class, including an assertion failure.
That converts a real defect into an intermittent one, and the second run's green
result hides the first run's red one.

```yaml
default:
  retry:
    max: 1
    when:
      - runner_system_failure
      - stuck_or_timeout_failure
```

This retries infrastructure and not logic. Add `api_failure` or
`scheduler_failure` where the instance genuinely produces them; do not add
`script_failure`, which is the class that means "the code is wrong".

Opt a mutating job out of retries entirely unless the operation is idempotent.
Retrying a `semantic-release` that already pushed a tag, or a migration whose
Kubernetes Job deliberately sets `backoffLimit: 0`, does damage that the first
failure did not. `validate_gitlab_ci.py` reports `retry-bare-count`.

## Skipping inside a script versus not creating the job

A job whose script begins "if this is not a release, `exit 0`" reports success and
did nothing. A reader sees twelve green jobs and cannot tell which of them ran.
The pipeline is green whether or not anything was verified.

Put the condition in `rules:` so the job is not created:

```yaml
deploy:
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH && $CI_COMMIT_REF_PROTECTED == "true"
    - when: never
```

Then a pipeline with no deploy job shows that no deploy was attempted, and a
pipeline with a green deploy job shows that one succeeded. Use a script-level
skip only where the condition is unknowable until the job runs — a value produced
by an earlier job through a dotenv report, for example — and say so in a comment
on the line. `validate_gitlab_ci.py` reports `script-skips-with-exit-0`.
