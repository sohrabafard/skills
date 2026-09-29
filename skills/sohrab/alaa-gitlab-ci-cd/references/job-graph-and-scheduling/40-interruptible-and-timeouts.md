# Cancellation and timeouts

Open this guide when the task involves job cancellation safety or timeouts. The topic map routes to this file.

For current feature claims and release qualifications, use the [source map](../00-source-map.md) and [version notes](../feature-version-notes.md).

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
`/alaa-reliability-sla` owns the value; this file owns
where it is written.
