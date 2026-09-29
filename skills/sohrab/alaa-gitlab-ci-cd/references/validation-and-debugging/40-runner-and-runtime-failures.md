# Runner and runtime failures

Open this guide when runner matching, executor startup or a running job fails. For version-sensitive claims, follow the [source map](../00-source-map.md).

### 3. Runner matching failure

*Symptoms:* job stuck in pending with no runner; "This job is stuck because you
don't have any active runners".

*Diagnose:* compare job `tags:` against every runner's tag set; check whether the
runner is paused, offline, or out of `concurrent` slots; check protected-ref
against protected-runner; check the project or group scope the runner is
assigned to.

*Smallest retry:* nothing to retry — the job has not started. Fix placement.

*Escalate when:* a runner matches on paper and still does not pick the job up;
that is a runner-registration or instance problem.

### 4. Executor startup failure

*Symptoms:* pod never becomes ready; "timed out waiting for pod to start"; image
pull errors with no job log; a shell runner that starts with the wrong
environment; a DinD service that never responds.

*Diagnose, Kubernetes:* `poll_timeout`; cluster capacity for the runner's
namespace; API-server latency; admission webhooks; image pull time and registry
reachability from the cluster; `image_pull_secrets` on **all** the pod's
containers, not only the build container; RBAC on the service account;
`namespace_per_job` rights; whether the cluster's restricted security context
needs `logs_base_dir` and `scripts_base_dir`.

*Diagnose, DinD:* privileged mode on the runner; the service alias and port
matching `DOCKER_HOST`; TLS variables consistent with `DOCKER_TLS_CERTDIR`; the
shared certificate volume present in the runner config.

*Diagnose, shell:* the runner user's environment, the `builds_dir` contents left
by a previous job, and host tooling versions.

*Smallest retry:* re-run the single job once the runner configuration changed;
runner configuration is read per job, unlike pipeline configuration.

*Escalate when:* pods are created and killed by something outside the runner — a
quota, a PodSecurity policy, an admission webhook. That is a cluster question,
and for a managed platform it belongs to that platform's skill.

### 5. Runtime failure

*Symptoms:* the script runs and the toolchain fails; registry authentication
fails; a secret is empty; the filesystem is read-only; a variable is empty only
in a merge request pipeline.

*Diagnose:* image contents and entrypoint; variable scope, masking and protection;
file-variable paths; writable directories; network policy and DNS from the pod.
For an empty variable, walk the six-question order in `variables-and-inputs.md`
before changing anything.

*Smallest retry:* re-run the one job. If it passes on the second run with no
change, that is a flake and the bare-`retry:` rule in
`job-graph-and-scheduling.md` explains why it must not be hidden by a retry.

*Escalate when:* the same script passes locally and fails on the runner with
identical inputs — the difference is in the image or the runner, not the script.
