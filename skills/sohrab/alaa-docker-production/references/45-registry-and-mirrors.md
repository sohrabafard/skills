# Registry strategy, mirrors and pinning

Open this file on any pull failure, mirror question, or decision about how an image is referenced.

The checker is `scripts/check-image-pinning.mjs`. `node scripts/check-image-pinning.mjs --versions`
prints every pinned upstream value in this skill with the command or URL that re-derives it.

---

## 1. Two mirror mechanisms, and they are not interchangeable

This is the distinction the fleet's older guidance left ambiguous, and getting it wrong produces a
mirror that silently does nothing for most images.

### Mechanism A — daemon `registry-mirrors`

```json
// /etc/docker/daemon.json
{ "registry-mirrors": ["https://mirror.cdn.ir"] }
```

The daemon consults the mirror before Docker Hub for any image reference that resolves to Docker
Hub. Image references are unchanged: `postgres:18.3` stays `postgres:18.3`.

**It mirrors Docker Hub only.** The documentation is explicit: "It's currently not possible to
mirror another private registry. Only the central Hub can be mirrored"
(https://docs.docker.com/docker-hub/image-library/mirror/, checked 2026-07-29). A pull from
`ghcr.io`, `quay.io`, `registry.k8s.io` or a first-party registry bypasses `registry-mirrors`
entirely and goes direct. That is the failure this section exists to prevent: an operator configures
`registry-mirrors`, sees Docker Hub pulls served from the mirror, and concludes the mirror covers
everything.

It is also host configuration, not repository configuration: it requires root on every node and a
daemon restart, and nothing in the repository records that it is in place.

### Mechanism B — image-reference prefix rewriting

```yaml
image: ${PUBLIC_DOCKER_REGISTRY:-mirror.cdn.ir/}postgres:18.3
```

The reference itself names the mirror host, so the pull goes to the mirror regardless of which
upstream the image originally came from. This works for any upstream, is recorded in the repository,
needs no daemon change, and is overridable per environment by setting one variable.

**This is the mechanism the fleet uses.** `service-runtime-kit` carries
`PUBLIC_DOCKER_REGISTRY` with the tracked default `mirror.cdn.ir/`
(`contracts/service.runtime.env.example:24`) and passes it into the build as `IMAGE_PROXY_PREFIX`
(`render-runtime.sh:301,1302`). The trailing slash is part of the value, and
`normalize_public_registry_prefix` (`render-runtime.sh:709-718`) appends one when it is missing, so
both `mirror.cdn.ir` and `mirror.cdn.ir/` work in the supported path.

The two mechanisms compose: use B in every reference, and A as a safety net for any tool that
constructs its own Docker Hub reference.

### Current gap in the fleet

Prefix rewriting is applied to the application base image and to nothing else. Every shared-infra
image is a literal in the generator with no prefix and no override variable: `postgres:18.3`
(`render-runtime.sh:1417,1485`), `rabbitmq:4.2.4-management` (`:1438,1535`), `redis:8.6.1-alpine`
(`:1518`), `adminer:5.4.2` (`:1506`), `edoburu/pgbouncer:v1.24.1-p1` (`:1556,1747`). Checked:

```
$ node scripts/check-image-pinning.mjs docker-compose.yml \
    --mirror-var PUBLIC_DOCKER_REGISTRY --private-host registry.takhtenegar.ir
docker-compose.yml:326: image-not-mirrored: image postgres:18.3 is a literal public reference;
  prefix it with ${PUBLIC_DOCKER_REGISTRY:-...} so the mirror governs it
...
```

The consequence is not theoretical: when Docker Hub is unreachable or rate-limits the egress IP, the
application image pulls through the mirror and every dependency it needs does not, so the stack
comes up with the app and no database.

## 2. Public mirror versus private registry: keep the variables separate

| Variable | Holds | Rotated when | Example |
|---|---|---|---|
| `PUBLIC_DOCKER_REGISTRY` | prefix for upstream public images | the mirror host changes | `mirror.cdn.ir/` |
| `IMAGE_PROXY_PREFIX` | the same value, passed into a build | with the above | `mirror.cdn.ir/` |
| `PRIVATE_DOCKER_REGISTRY` | host for first-party images and OCI artifacts | the private registry moves | `registry.takhtenegar.ir` |
| registry credentials | authentication for the private registry | on a credential rotation | delivered as a secret, never a file in the repository |

They are separate because they change for different reasons and are owned by different people.
Collapsing them into one variable means rotating a mirror host also rotates the private-registry
path, and a build that should have failed loudly instead pulls a first-party image from a public
mirror that does not have it.

Registry credentials are never baked into an image and never committed. In CI they arrive as masked
variables and are consumed by `docker login`; at runtime, Swarm needs `--with-registry-auth` on the
`stack deploy` command so the manager forwards them to the nodes that must pull. Which variable
holds them and how the runner receives them is `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`)'s
decision; that they exist and are separate is this skill's.

## 3. Tags, digests, and what "pinned" means

A tag is a mutable pointer. A digest is the content address of a manifest and cannot be repointed.
Three levels, each correct in a different place:

| Level | Form | Use in |
|---|---|---|
| Floating | `postgres:latest`, `postgres` | Nowhere. `image-floating-latest`. |
| Bare major | `postgres:18` | Nowhere. It moves on every upstream minor release, so the same file deploys different software on different days. `image-bare-major`. |
| Tag pin | `postgres:18.3` | Development Compose, and production Compose for shared infrastructure. |
| Digest pin | `postgres:18.3@sha256:...` | Every Swarm stack file and every release manifest. |

The rule with no escape clause: **every `FROM` in a Dockerfile and every `image:` in a
production-shaped Compose or stack file names a tag that is neither `latest` nor a bare major, and a
release additionally pins by digest.** "Production-shaped" means any file that is deployed to a
shared host: `docker-compose.yml` and `docker-compose.swarm.yml` are; `docker-compose.dev.yml` is
not.

`${VAR:-default}` does not exempt the default. `${COMMENT_DOCKER_IMAGE:-comment-service:latest}`
(`render-runtime.sh:289`, rendered at `docker-compose.yml:19,132,234` and into the Swarm stack)
deploys `comment-service:latest` on any manager where the variable is unset — which is the normal
state of a manager node, since the variable comes from the deploying environment. The default is
what the file *means*; write it as `${COMMENT_DOCKER_IMAGE:?set the built image reference}` and the
file cannot deploy an accident.

Resolving a tag to a digest:

```
docker buildx imagetools inspect mirror.cdn.ir/postgres:18.3 --format '{{.Manifest.Digest}}'
docker image inspect postgres:18.3 --format '{{index .RepoDigests 0}}'
```

Note that a digest is per-registry-content, so an image mirrored to `mirror.cdn.ir` has the same
digest as upstream only if the mirror is a pull-through cache rather than a re-push. Verify once per
mirror; if they differ, record the mirror's digest, because that is what will be pulled.

## 4. Pull behaviour

| Setting | Where | Effect |
|---|---|---|
| `pull_policy: always` | Compose service | Pull on every `up`. Correct for a floating dev tag, wasteful for a pinned one. |
| `pull_policy: missing` | Compose service | Default. Pull only when the image is not present locally. |
| `pull_policy: never` | Compose service | Fail rather than pull. Use in an air-gapped or offline test. |
| `docker compose pull` | command | Explicit pull step before `up`, which separates a network failure from a start failure in the logs. |
| `docker stack deploy --resolve-image always` | command | Default. The manager resolves the tag to a digest and pins the task spec to it, so all tasks run the same content even if the tag moves mid-rollout. |
| `--resolve-image never` | command | Passes the tag through unresolved. Only for a registry the manager cannot reach. |

`--resolve-image always` is the reason a Swarm rollout is consistent even with a tag reference, and
it is also the reason a `stack deploy` with an unchanged tag but a moved image *does* redeploy: the
resolved digest changed even though the file did not.

## 5. Upstream lines, and how to re-derive them

Verified 2026-07-29. Run `node scripts/check-image-pinning.mjs --versions` for the full table with
re-derivation commands; the checker also reports `image-eol-line` for an image built on a line that
has left support.

| Line | Current | Re-derive with |
|---|---|---|
| Docker Engine | 29.6.2 (16 July 2026) | `docker version --format '{{.Server.Version}}'`; https://docs.docker.com/engine/release-notes/29/ |
| Docker Compose | v5.3.1 (7 July 2026) | `docker compose version`; https://github.com/docker/compose/releases |
| Alpine | 3.24 stable; 3.21+ supported | https://www.alpinelinux.org/releases/ |
| Debian slim | 13 "trixie", point release 13.6 | https://www.debian.org/releases/ |
| PHP | 8.5 newest; 8.4 and 8.5 active | https://www.php.net/supported-versions.php |
| Node.js | 24 "Krypton" Active LTS | https://github.com/nodejs/Release |
| PostgreSQL image | pinned in the generator at 18.3 | `docker buildx imagetools inspect mirror.cdn.ir/postgres:18 --format '{{json .Manifest}}'` |

An image pinned to a line that has left support is a defect even when nothing is currently broken:
security patches stop arriving, so every future scanner finding on it is permanently unfixable and
the only remedy is a base-image migration under time pressure.

## 6. Diagnosing a pull failure

```
docker pull IMAGE                                  # reproduce outside Compose first
docker buildx imagetools inspect IMAGE             # does the manifest exist at all
docker info --format '{{json .RegistryConfig.Mirrors}}'   # is a daemon mirror configured
docker service ps --no-trunc SERVICE               # Swarm: the task error column names the failure
journalctl -u docker --since '10 min ago'          # the daemon's own view of the pull
```

| Symptom | Cause | Section |
|---|---|---|
| Application image pulls, dependencies do not | Only the app reference carries the mirror prefix | §1 |
| Mirror configured, non-Hub pulls still go direct | `registry-mirrors` mirrors Docker Hub only | §1, mechanism A |
| Works on the manager, tasks `Pending` on workers | `--with-registry-auth` missing from `stack deploy` | §2 |
| Same tag, different content between two nodes | Tag moved and `--resolve-image never` was used, or the nodes pulled at different times | §4 |
| `manifest unknown` for a digest that exists upstream | The mirror re-pushes rather than caching, so digests differ | §3 |
| Rate-limit errors under load | Pulls reaching Docker Hub directly rather than the mirror | §1 |
| Deploy pulls a new image although the file did not change | `--resolve-image always` resolved a moved tag — which is the argument for digest pinning | §3, §4 |
