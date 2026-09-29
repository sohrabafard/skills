# Topic map

The one router for this skill. Open the narrowest file whose trigger matches the
task in front of you. Do not read every file.

| Open | When the task involves |
|---|---|
| `pipeline-authoring/10-pipeline-creation-and-paths.md` | pipeline creation rules or path selection |
| `pipeline-authoring/20-authoring-defaults.md` | job authoring defaults |
| `pipeline-authoring/30-reuse-composition.md` | hidden jobs, includes, components or child pipelines |
| `pipeline-authoring/30-environments-and-rollback.md` | deployment environment recording or deployment rollback |
| `pipeline-authoring/40-child-pipelines-and-checklist.md` | child pipelines or multi-file layout |
| `job-graph-and-scheduling/10-dag-edges-and-critical-path.md` | stage versus DAG ordering, job dependencies or critical-path cost |
| `job-graph-and-scheduling/20-needs-and-artifacts.md` | `needs:` size limits or artifact fetching |
| `job-graph-and-scheduling/30-parallelism-and-resource-groups.md` | parallel jobs, matrices or shared-resource serialization |
| `job-graph-and-scheduling/40-interruptible-and-timeouts.md` | cancellation safety or job timeout bounds |
| `job-graph-and-scheduling/50-retry-failure-classes.md` | choosing whether and which failures a job may retry |
| `job-graph-and-scheduling/60-job-creation-conditions.md` | deciding whether a job should be created or omitted |
| `cache-artifacts-and-pinning.md` | a cache key, `policy:`, `fallback_keys`, where a cache lives, artifact scoping and `expire_in`, and how an image reference is pinned in each of the five places one can appear |
| `variables-and-inputs/10-mechanism-and-expansion.md` | choosing a variable/input mechanism or understanding expansion |
| `variables-and-inputs/20-variable-precedence.md` | resolving variable precedence |
| `variables-and-inputs/30-protected-and-file-variables.md` | masking, protected variables or file-variable paths |
| `variables-and-inputs/40-tokens-and-secure-files.md` | job identity tokens, secret fetches or secure files |
| `variables-and-inputs/50-inputs-and-components.md` | typed component inputs |
| `variables-and-inputs/60-rules-and-value-availability.md` | variable availability during rule evaluation |
| `variables-and-inputs/70-downstream-forwarding.md` | forwarded variables in downstream pipelines |
| `variables-and-inputs/80-variable-debugging-and-inventory.md` | diagnosing or documenting variable values |
| `runner-shell-and-kubernetes.md` | runner architecture: executor choice, `config.toml`, Helm `values.yaml` versus embedded TOML, RBAC and namespaces, restricted clusters, `concurrent`, distributed cache, `image_pull_secrets` and `helper_image` |
| `container-build-strategies.md` | choosing a build path: rootless BuildKit, Docker-in-Docker, a shell runner against a host daemon, Podman or Buildah, and registry cache wiring |
| `security-and-hardening.md` | runner isolation, credential handling, merge-request and fork exposure, pull policy, privileged mode, and credentials that outlive a job |
| `validation-and-debugging/10-static-validation-and-checkers.md` | the validation ladder or bundled checker limits |
| `validation-and-debugging/40-gate-eligibility.md` | deciding which findings are errors, warnings, notes, or gate-eligible |
| `validation-and-debugging/20-live-validation.md` | merged-configuration CI Lint or project-context validation |
| `validation-and-debugging/30-failure-class-triage.md` | choosing the failure-class route |
| `validation-and-debugging/30-configuration-and-rule-failures.md` | YAML/schema problems or missing/duplicated pipelines |
| `validation-and-debugging/40-runner-and-runtime-failures.md` | runner placement, executor startup or job runtime failures |
| `validation-and-debugging/50-symptoms-and-cross-file.md` | literal symptoms or multi-file include/debugging work |
| `feature-version-notes.md` | whether a feature is generally available, experimental, deprecated or limited, and how to compute the current supported GitLab baseline instead of reading a stale one |
| `90-companion-boundary.md` | any question about whether this skill decides the matter, and which skill does if not |
| `00-source-map.md` | a claim that must be current: which official page is authoritative for it, and the order in which conflicting sources are resolved |
