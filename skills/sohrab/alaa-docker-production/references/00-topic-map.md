# Topic map

One row per file. Every destination is a filename in this directory or a script in `scripts/`.
Open the file whose trigger matches; if none matches, the subject may not be this skill's and
`90-companion-boundary.md` names the owner.

## By task

| I am about to… | Open |
|---|---|
| write or review a Dockerfile, or a `.dockerignore` | `10-dockerfile-authorship.md` |
| pass a credential into a build, add a cache mount, or produce release evidence | `15-build-secrets-and-attestations.md` |
| write or review any Compose file | `20-compose-authorship.md` |
| write `${VAR:...}` anywhere, or change a generator that emits it | `25-fail-closed-interpolation.md` |
| write a Swarm stack file, or change how a deployment rolls out | `30-swarm-delivery.md` |
| get a password, key or token into a running container, or rotate one | `35-secret-delivery.md` |
| add or change a healthcheck, a start-up window, or a shutdown grace period | `40-healthcheck-and-lifecycle.md` |
| choose an image reference, a tag, a digest, or a mirror | `45-registry-and-mirrors.md` |
| attach a service to a network, name it, or publish a port | `50-network-dns-and-exposure.md` |
| size a container, tune OPcache or workers, or set `nofile` | `60-resource-limits-and-load.md` |
| decide where a container's logs go, or bound them | `70-container-observability.md` |
| check whether a subject belongs to this skill, or open a merge request | `90-companion-boundary.md` |
| change a version-sensitive statement | `00-source-map.md` |

## By symptom

| The failure looks like… | Start with | Then |
|---|---|---|
| build is slow, or a dependency install runs on every source edit | `10-dockerfile-authorship.md` §3 | `15-build-secrets-and-attestations.md` §2 |
| a build variable is empty inside a `RUN` | `10-dockerfile-authorship.md` §6 | — |
| the image is far larger than expected | `10-dockerfile-authorship.md` §4, §11 | — |
| a credential appears in `docker history` or in a layer | `15-build-secrets-and-attestations.md` §1 | `35-secret-delivery.md` §8 |
| a value is set in `.env` and empty in the container | `20-compose-authorship.md` §4 | `25-fail-closed-interpolation.md` §2 |
| `up` hangs waiting for a dependency to be healthy | `20-compose-authorship.md` §5 | `40-healthcheck-and-lifecycle.md` §3 |
| a one-shot job is running as a long-lived service | `20-compose-authorship.md` §3 | — |
| a checker passes a file that is obviously wrong | `25-fail-closed-interpolation.md` §4 | — |
| the service was briefly down during a deploy that reported success | `30-swarm-delivery.md` §2, §3 | `40-healthcheck-and-lifecycle.md` §1 |
| a rollout stopped half-way and nothing alerted | `30-swarm-delivery.md` §2 | — |
| tasks stuck `Pending` or `Preparing` | `30-swarm-delivery.md` §9 | `45-registry-and-mirrors.md` §6 |
| jobs are lost on every deploy | `40-healthcheck-and-lifecycle.md` §4 | `30-swarm-delivery.md` §8 |
| a container is `running` and serving nothing | `40-healthcheck-and-lifecycle.md` §2, §3 | — |
| a probe flaps under load | `40-healthcheck-and-lifecycle.md` §2 | `60-resource-limits-and-load.md` §1 |
| a config change "did not take" after a Swarm deploy | `30-swarm-delivery.md` §7 | — |
| the application image pulls and its dependencies do not | `45-registry-and-mirrors.md` §1 | — |
| the same tag gives different content on different nodes | `45-registry-and-mirrors.md` §3, §4 | — |
| a name does not resolve, or resolves and refuses the connection | `50-network-dns-and-exposure.md` §5 | — |
| a database or broker is reachable from outside the host | `50-network-dns-and-exposure.md` §3 | — |
| routing broke after a deploy | `50-network-dns-and-exposure.md` §2 | — |
| a container restarts with nothing in its own logs | `60-resource-limits-and-load.md` §1 | `70-container-observability.md` §3 |
| latency rises with no CPU saturation on the host | `60-resource-limits-and-load.md` §1, §2 | — |
| 32 worker processes appear in a 2-CPU container | `60-resource-limits-and-load.md` §2 | — |
| `accept: too many open files` | `60-resource-limits-and-load.md` §4 | — |
| the node ran out of disk and unrelated containers failed | `70-container-observability.md` §2 | — |
| the application runs and logs nothing at all | `70-container-observability.md` §1 | — |

## Checkers

| Script | Asserts | Run it |
|---|---|---|
| `scripts/check-compose-interpolation.mjs` | Every substitution fails closed; no safety-control variable carries a disabling default. | `node scripts/check-compose-interpolation.mjs docker-compose.yml docker-compose.swarm.yml` |
| `scripts/check-dockerfile-contract.mjs` | Syntax directive, stages, non-root final stage, no build tooling in the final image, layer order, OCI revision label, healthcheck, `.dockerignore` coverage. | `node scripts/check-dockerfile-contract.mjs Dockerfile` |
| `scripts/check-stack-rollout.mjs` | Every long-lived Swarm service has update, rollback, replica, reservation, restart-delay, healthcheck and secret-mode control. | `node scripts/check-stack-rollout.mjs docker-compose.swarm.yml` |
| `scripts/check-image-pinning.mjs` | No floating or bare-major reference, including inside a `${VAR:-default}`; no end-of-life upstream line; digests on a release; mirror coverage. | `node scripts/check-image-pinning.mjs --mirror-var PUBLIC_DOCKER_REGISTRY docker-compose.yml` |

All four take `--help` and `--self-test`, and exit **0** clean, **1** findings, **2** could not run.
Exit 2 is not a pass. `node scripts/check-image-pinning.mjs --versions` prints every pinned upstream
value in this skill with the command or URL that re-derives it.
