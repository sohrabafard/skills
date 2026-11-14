# Topic map

The one router for this skill. Open the narrowest file whose trigger matches the
task in front of you. Do not read every file.

| Open | When the task involves |
|---|---|
| `pipeline-authoring/10-pipeline-creation-and-paths.md` | writing `workflow:rules` or job `rules:`, including the terminal arm that makes pipeline creation explicit, or selecting jobs by changed paths |
| `pipeline-authoring/20-authoring-defaults.md` | writing or changing a job or a pipeline: its stages, `workflow:rules`, `needs:`, shared `default:` setup, a job split, or a job script |
| `pipeline-authoring/30-reuse-composition.md` | deciding whether to reuse job text through a hidden job, `extends`, `!reference`, an include or a component, or composing child pipelines |
| `pipeline-authoring/30-environments-and-rollback.md` | recording a deployment environment or rolling back a deployment |
| `pipeline-authoring/40-child-pipelines-and-checklist.md` | child pipelines or multi-file layout |
| `job-graph-and-scheduling/10-dag-edges-and-critical-path.md` | stage versus DAG ordering, job dependencies or critical-path cost |
| `job-graph-and-scheduling/20-needs-and-artifacts.md` | writing `needs:`, checking its size limits, or controlling artifact fetching |
| `job-graph-and-scheduling/30-parallelism-and-resource-groups.md` | `parallel:`, `parallel:matrix`, or a `resource_group` that serializes jobs on a shared resource |
| `job-graph-and-scheduling/40-interruptible-and-timeouts.md` | `interruptible` and cancellation safety, or a job `timeout:` |
| `job-graph-and-scheduling/50-retry-failure-classes.md` | writing `retry:`: whether a job may retry, and on which failures |
| `job-graph-and-scheduling/60-job-creation-conditions.md` | writing a job that runs only under a condition, or a script that skips itself with `exit 0`: deciding whether the job is created or omitted |
| `cache-artifacts-and-pinning.md` | a cache key, `policy:`, `fallback_keys`, where a cache lives, artifact scoping and `expire_in`, and how an image reference is pinned in each of the five places one can appear |
| `variables-and-inputs/10-mechanism-and-expansion.md` | choosing between an input, a variable, a file variable and a dotenv report, or checking how GitLab expands a variable |
| `variables-and-inputs/20-variable-precedence.md` | resolving variable precedence |
| `variables-and-inputs/30-protected-and-file-variables.md` | masking, a protected variable, or a file-variable path |
| `variables-and-inputs/40-tokens-and-secure-files.md` | `id_tokens:`, the `secrets:` block, or secure files |
| `variables-and-inputs/50-inputs-and-components.md` | typed `spec:inputs` for a component |
| `variables-and-inputs/60-rules-and-value-availability.md` | variable availability during rule evaluation |
| `variables-and-inputs/70-downstream-forwarding.md` | forwarding variables to a downstream pipeline |
| `variables-and-inputs/80-variable-debugging-and-inventory.md` | diagnosing or documenting variable values |
| `runner-shell-and-kubernetes.md` | runner architecture: executor choice, container-hosted manager bootstrap, persistent configuration, authentication-token source and TLS trust, `config.toml`, Helm `values.yaml` versus embedded TOML, RBAC and namespaces, restricted clusters, `concurrent`, distributed cache, `image_pull_secrets` and `helper_image` |
| `container-build-strategies.md` | designing any image-build job, before you write it: choosing a build path (rootless BuildKit, Docker-in-Docker, a shell runner against a host daemon with its four preconditions, Podman or Buildah) and registry cache wiring |
| `security-and-hardening.md` | the threat model for each runner type, the credential order, runner isolation, credential handling, merge-request and fork exposure, pull policy, privileged mode, and credentials that outlive a job |
| `validation-and-debugging/10-static-validation-and-checkers.md` | choosing the cheapest check that answers the question, or what each bundled checker asserts and cannot see |
| `validation-and-debugging/40-gate-eligibility.md` | deciding which findings are errors, warnings, notes, or gate-eligible |
| `validation-and-debugging/20-live-validation.md` | merged-configuration CI Lint or project-context validation |
| `validation-and-debugging/30-failure-class-triage.md` | a CI failure whose class (configuration, runner or runtime) is not yet known |
| `validation-and-debugging/30-configuration-and-rule-failures.md` | a YAML or schema failure, or a pipeline that is missing or duplicated: the symptoms, diagnosis, smallest retry and escalation point of classes 1 and 2 |
| `validation-and-debugging/40-runner-and-runtime-failures.md` | runner placement, executor startup or job runtime failures: the symptoms, diagnosis, smallest retry and escalation point of classes 3 to 5 |
| `validation-and-debugging/50-symptoms-and-cross-file.md` | matching a literal failure symptom, or debugging across several included files |
| `feature-version-notes/10-compute-supported-baseline.md` | the target GitLab or Runner version is unknown or must be stated: the release cadence that computes the current supported line, the URL that confirms it, and how to write an answer without a checked version |
| `feature-version-notes/20-feature-status-limits-and-deprecations.md` | deciding whether a named feature is generally available, experimental or deprecated, checking a GitLab or Runner hard limit, or replacing a deprecated keyword, API surface or tool |
| `90-companion-boundary.md` | any question about whether this skill decides the matter, and which skill does if not: the full companion table |
| `00-source-map.md` | a version-sensitive claim you must verify before writing it: which official page is authoritative for it, and the order in which conflicting sources are resolved |
