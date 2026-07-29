# Companion boundary, change output, and maintaining this skill

Open this file when a task touches ground that may not be this skill's, and before opening a merge
request that changes a container artifact.

---

## 1. Owner table

Each row names an owner, states the condition under which that owner decides the matter, and stops.
Silence is not delegation, so a subject not in this table and not in this skill's other references
has no owner and the gap is a finding rather than an assumption.

| Owner | Decides | Condition that sends the task there |
|---|---|---|
| `/alaa-frontend-devops` (`$alaa-frontend-devops`) | The frontend delivery gate register: for each gate, the predicate it asserts, the command that evaluates it, and the artifact it inspects. | The task changes *whether* a build property is enforced, or adds a gate. This skill writes the instruction or key that satisfies a gate and never changes the gate. |
| `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`) | How a gate is expressed on a runner: job, stage, rules, artifacts, caches, credentials. | The task changes what runs in CI, in what order, or with what runner configuration. Everything in this skill that says "in the pipeline" means there. |
| `/alaa-haproxy` (`$alaa-haproxy`) | How a cache or routing decision is expressed as a proxy directive. | The task changes proxy configuration. This skill decides only which DNS name the proxy is pointed at. |
| `/alaa-haproxy-lua` (`$alaa-haproxy-lua`) | Lua running inside HAProxy. | The proxy change needs a script rather than a directive. |
| `/service-runtime-kit-governance` (`$service-runtime-kit-governance`) | Which generator variable expresses a runtime value: its name, its tracked default, which contract file holds it, and whether changing it forces a re-render. | The task adds or renames a knob. A request to change what the generated file *looks like* comes here instead. |
| `/alaa-services-contract` (`$alaa-services-contract`) | Every shared name and value: log fields, the metric catalog, `OTEL_*` names and defaults, the host-port table, canonical shared-infra and alias names. | The task needs to know what something is called or what its canonical value is. |
| `/alaa-reliability-sla` (`$alaa-reliability-sla`) | Why a timeout, retry, backoff, circuit breaker, backpressure or degradation mechanism exists and what shape it takes. | The task decides whether a service should degrade or refuse when a dependency is unavailable. This skill expresses the resulting number as a container key. |
| `/alaa-security-review` (`$alaa-security-review`) | Review triggers, threat classes, and fail-closed doctrine for security decisions. | The task asks whether a value is a security control, or whether adding back a capability is acceptable. |
| `/alaa-observability-soc` (`$alaa-observability-soc`) | Whether a signal is required, what gates on it, and why. | The task changes what is emitted or collected. This skill owns the `logging:` key and the container-level plumbing only. |
| `/alaa-testing-strategy` (`$alaa-testing-strategy`) | Test layering, doubles, flake control, and what an SLA service must cover. | The task decides what to test, as opposed to which container the test runs in. |
| `/alaa-system-design` (`$alaa-system-design`) | Designing a service or subsystem before implementation. | The container shape is being changed to work around a design problem. |
| `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) | Complexity budgets and structure choice. | A limit is being raised to compensate for a path that does not scale. |
| `/alaa-project-constitution` (`$alaa-project-constitution`) | The quality bar itself, at its `references/quality-bar.md`. | The task asks what "good" means for an artifact in this repository. |
| `/alaa-controlled-ops` (`$alaa-controlled-ops`) | Change control and proof strength. | The change is being made against a running production system and the question is what evidence is required first. |
| `/caas-arvan-kuber` (`$caas-arvan-kuber`) | The Arvan Kubernetes production path, its pinned platform version, and GitLab rollout mechanics there. | The target runtime is Arvan CaaS rather than Compose or Swarm. |
| `/alaa-k8s-helm` (`$alaa-k8s-helm`) | Kubernetes manifests, Helm charts and values. | The artifact is a manifest or a chart. A Compose file is not a starting point for one. |
| `/alaa-octane-performance` (`$alaa-octane-performance`) | Octane and Swoole behaviour: extension selection, long-lived-process state, reload semantics. | The task tunes the application server rather than the container around it. |
| `/alaa-data-layer` (`$alaa-data-layer`) | Query shape, indexes, schema, grants, and whether a query should hold a connection. | The task is about the database rather than the container running it. |
| `/alaa-minio-object-storage` (`$alaa-minio-object-storage`) | What a MinIO container's buckets, policies, lifecycle rules and credentials must be. | The task decides object-storage policy, as opposed to how the container is expressed. |
| `/alaa-arvan-object-storage` (`$alaa-arvan-object-storage`) | ArvanCloud Object Storage endpoints, regions, limits and compatibility. | The storage endpoint is Arvan rather than MinIO. |
| `/alaa-bash-shell` (`$alaa-bash-shell`) | Shell script structure, portability, help output and testing. | The task writes or refactors an entrypoint, wrapper or helper script. This skill states what the script must guarantee. |
| `/alaa-makefile` (`$alaa-makefile`) | Make targets, and making the local verdict identical to the runner's. | A container command is being given a local invocation. |
| `/alaa-cicd-laravel-postgres` (`$alaa-cicd-laravel-postgres`) | Laravel and PostgreSQL pipeline specifics. | Only alongside `/alaa-gitlab-ci-cd`, which owns runner expression. |
| `/alaa-prompting-guide` (`$alaa-prompting-guide`) | Model and effort selection, at its `references/50-effort-and-thinking.md`. | Any question about which model or effort level to use. Never write a model name or effort key into a container artifact. |

## 2. What a change to a container artifact ships with

This is a required section of the merge request description, in the repository whose artifact
changed. Not a report filed elsewhere; the merge request is the destination.

1. **What changed and why.** The Dockerfile, Compose or stack keys touched, one line each.
2. **Runtime effect.** Mode, ports, user, volumes, environment, healthchecks, secrets — state only
   what this change alters, and state the before and after value.
3. **Determinism.** What is pinned and at what level, what remains floating and why, and any digest
   recorded. This skill's `references/45-registry-and-mirrors.md`.
4. **Discovery and infrastructure.** Shared network and shared-infra assumptions, canonical aliases,
   mirror versus private-registry path. This skill's `references/50-network-dns-and-exposure.md`.
5. **Release evidence.** Provenance level, whether an SBOM was produced, the scan report artifact
   path and the severity counts from it. This skill's
   `references/15-build-secrets-and-attestations.md`.
6. **Rollout.** Restart strategy, the `update_config` and `rollback_config` values, replica count,
   and what an operator will see during the deploy. Not optional: a change with no rollout statement
   is a change whose downtime nobody has estimated. This skill's `references/30-swarm-delivery.md`.
7. **Rollback.** The exact command that reverts this change and the image reference it reverts to.
   `docker service rollback <service>` for a Swarm service; the previous digest from the release
   manifest otherwise.
8. **Checker output.** The four checkers in `scripts/`, run against the changed artifact, pasted.
   Exit 2 from any of them is not a pass and is not "the checker could not read my file, so it is
   fine".

## 3. Maintaining this skill

- The always-loaded `SKILL.md` holds only what is needed on every task: the ownership statement, the
  three rules, and the pointer to the router. Detail goes into a reference, never into the body.
- Every instruction appears exactly once across the whole skill. A rule you find yourself writing a
  second time becomes a pointer to the first.
- `references/00-topic-map.md` routes across files and its every destination is a filename that
  exists. Check it after adding or renaming a reference; a router entry pointing at a section name
  rather than a file is the defect that made the previous version of this skill unnavigable.
- Every skill named in prose gets both trigger forms — `/name` and `$name` — on first mention in
  that file. `agents/openai.yaml` is Codex-only and correctly uses the bare `$` alone.
- Cross-skill references name the owning skill alongside the path: `alaa-services-contract
  references/22-…`, never a bare `references/…`.
- Generic Docker, Compose and Swarm mechanics stay here. Ala-specific service-family constants —
  alias values, the host-port table, canonical infrastructure names — belong to
  `/alaa-services-contract` (`$alaa-services-contract`) and are referenced from here, not copied
  into here.
- Re-check the version claims when a version-sensitive statement is edited, and record what was
  checked and when in `references/00-source-map.md`. `node scripts/check-image-pinning.mjs
  --versions` prints every pinned value with the command that re-derives it.
- A new rule ships with the check that reports its violation, or it ships as a preference. If the
  rule cannot be checked mechanically, say so in the rule and state the manual command that
  evaluates it instead.
