# Dockerfile authorship

Open this file when writing or reviewing a Dockerfile or a `.dockerignore`.

This skill is the only governor of the Dockerfile for every service in the fleet.
`service-runtime-kit` emits a `build:` stanza that *references* a Dockerfile — `dockerfile:
Dockerfile`, `target: runtime`, with build args `IMAGE_PROXY_PREFIX`, `OCTANE_BASE_IMAGE`,
`COMPOSER_VERSION`, `WWWUSER`, `WWWGROUP` — and deliberately generates no Dockerfile
(`service-runtime-kit/README.md:182`). Nothing else in the programme reviews these files.

The checker for this file is `scripts/check-dockerfile-contract.mjs`. Every rule id below is the
rule id it reports. Run it before opening a merge request that touches a Dockerfile:

```
node scripts/check-dockerfile-contract.mjs path/to/Dockerfile
```

---

## 1. The syntax directive is line 1, not an option

Rule id: `syntax-directive`.

```dockerfile
# syntax=docker/dockerfile:1
```

This must be the first line of the file, before any other comment or blank line. It selects the
BuildKit Dockerfile frontend and pins it to the stable major, so BuildKit fetches the newest stable
syntax of that major before every build
(https://docs.docker.com/reference/dockerfile/, checked 2026-07-29).

It is not optional because without it the available syntax is whatever frontend the daemon happens
to carry. `RUN --mount=type=secret`, `RUN --mount=type=cache`, `COPY --chmod`, heredocs and build
checks are then present on the engineer's machine and absent on a runner, or the reverse, and the
build fails with a parse error that names a line rather than a missing feature. Pin the major, not
a full version: `docker/dockerfile:1.7` freezes the frontend and stops you receiving fixes.

## 2. `.dockerignore` is the build-context contract

Rule ids: `dockerignore-missing`, `dockerignore-incomplete`.

Every Dockerfile has a `.dockerignore` beside it. The file the builder receives is the build
context, and everything in the context is uploaded to the builder, is visible to every `COPY`, and
— for anything a `COPY . .` picks up — ends up in a layer.

The required entries for a service in this fleet:

```gitignore
# Version control and CI metadata: large, and never needed at runtime.
.git
.gitignore
.gitlab-ci.yml

# Secrets. .env is the single file that holds every credential this service uses.
.env
.env.*
!.env.example
docker/.local-secrets
storage/oauth-*.key

# Anything the build stage produces for itself.
vendor
node_modules
.pnpm-store

# Local runtime state that would otherwise be baked into the image.
storage/logs
storage/framework/cache
storage/framework/sessions
storage/framework/views
*.sqlite

# Test and tooling output.
coverage
.phpunit.result.cache
.php-cs-fixer.cache
```

`.env` and `docker/.local-secrets` are not on that list to save bytes. `service-runtime-kit`
writes the local secret bundle into `./docker/.local-secrets/` and mounts it
(`render-runtime.sh:1178`); a `COPY . .` with no `.dockerignore` copies the application key and the
Passport private key into a layer, and a layer is readable by anyone who can pull the image, for as
long as the image exists, whether or not a later `RUN rm` deletes the file.

`!.env.example` is the exception form: an exclamation-mark line re-includes a path a previous
pattern excluded, and `.env.example` carries no values.

## 3. Layer order is decided by rate of change

Rule id: `context-copy-before-install`.

A layer's cache entry is invalidated when its inputs change, and every layer after it rebuilds.
Therefore instructions are ordered from least likely to change to most likely to change, and the
dependency manifest and lockfile are copied on their own, before the install, and before the
application source. The four inbound rules from `/alaa-frontend-devops`
(`$alaa-frontend-devops`) — layer ordering by manifest and lockfile, layer-invalidation avoidance,
multi-stage separation, image minimisation — are all instances of this one economic fact, and
"do not copy the full repo before dependency install" is the specific violation that costs the most.

Correct:

```dockerfile
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-scripts --no-interaction --prefer-dist
COPY . .
```

Wrong, and the single most common defect in this fleet's Dockerfiles:

```dockerfile
COPY . .
RUN composer install --no-dev --no-scripts --no-interaction --prefer-dist
```

The observable difference: with the correct order, editing one PHP file rebuilds one layer. With
the wrong order, editing one PHP file re-resolves every dependency, re-downloads every package, and
adds the full install time to every build on every branch. On a Laravel service with a warm
Composer cache that is roughly 5 seconds against roughly 90; on a cold runner it is 5 seconds
against several minutes, multiplied by every pipeline run.

Three corollaries.

- **`--no-scripts` on the dependency install.** Composer and npm post-install scripts read the
  application source, which is not present yet at that point in the correct order. Run them after
  the source arrives: `composer dump-autoload --classmap-authoritative --no-dev`.
- **Copy the lockfile, and fail if it is absent.** `composer install` without `composer.lock`
  resolves fresh versions and produces a different image from the same commit. `npm ci` fails
  outright without `package-lock.json`, which is the behaviour to want; `composer install` does
  not, so `.dockerignore` must not exclude `composer.lock` and the build must not use
  `composer update`.
- **A cache mount is not a substitute for order.** `RUN --mount=type=cache` keeps the package
  archive between builds, which makes a re-install faster; it does not stop the layer being
  invalidated, so the install still runs. Both are needed. Cache mount syntax and its `uid`/`gid`
  arguments are in this skill's `references/15-build-secrets-and-attestations.md`.

## 4. Stages: build tooling never reaches the final image

Rule ids: `single-stage`, `final-stage-build-tooling`.

At least two `FROM` instructions. The build stage holds the compiler, the package manager, the
development dependencies and the source tree; the final stage receives only the artifacts, by
`COPY --from`.

The testable predicate — the form `/alaa-frontend-devops` (`$alaa-frontend-devops`) already states
as an obligation at its `references/20-ci-gates-and-predicates.md:44`, whose *how* is this section:
**the final image contains no package manager binary, no compiler, and no development
dependency.** Verify it against a built image rather than by reading the Dockerfile:

```
docker run --rm --entrypoint sh IMAGE -c 'command -v apt-get apk yum gcc cc make composer npm; exit 0'
docker run --rm --entrypoint sh IMAGE -c 'test ! -d /root/.composer && test ! -d /usr/local/lib/node_modules'
```

Both must print nothing and exit 0.

A single-stage build is permitted only where the runtime image is itself the artifact of another
build — a first-party base image such as `octane-base`, or a sidecar built from a published binary.
Mark it in the file so the checker and the reviewer agree:

```dockerfile
# single-stage-exempt: this file builds the shared octane-base image; there is no artifact to copy in
```

Where a runtime package genuinely must be installed in the final stage — an ICU data package, a
CA bundle — install and remove the build tooling in the same `RUN`, so no layer ever contains it:

```dockerfile
RUN set -eux; \
    apk add --no-cache --virtual .build-deps build-base autoconf; \
    pecl install redis-6.4.0; \
    docker-php-ext-enable redis; \
    apk del .build-deps
```

## 5. Base images are pinned, and the pin is current

Rule ids: `base-image-floating`, and `image-eol-line` in
`scripts/check-image-pinning.mjs`.

Every `FROM` names a tag that is neither `latest` nor a bare major. `FROM php:8.4` is a bare major
in the sense that matters: the tag moves to a new patch release on every upstream build, so the
same commit produces different images on different days and a reproduction of last week's incident
is not available. `FROM php:8.4.13-fpm-trixie` does not move. A release build additionally pins by
digest; see this skill's `references/45-registry-and-mirrors.md` for when a digest is required and
how the release manifest records it.

Current lines as of 2026-07-29, with the command that re-derives each: run
`node scripts/check-image-pinning.mjs --versions`. Summary, so a Dockerfile author has a default to
reach for rather than picking one per repository:

| Line | Current as of 2026-07-29 | Use for |
|---|---|---|
| Alpine | 3.24 stable; 3.21 and newer supported | A runtime image with no glibc dependency |
| Debian slim | 13 "trixie"; 12 "bookworm" is oldstable | Anything linking glibc, ICU, or a proprietary driver |
| PHP | 8.4 and 8.5 in active support; 8.3 security-only to 2027-12-31 | The `octane-base` build |
| Node.js | 24 "Krypton" Active LTS to 2026-10-20, then maintenance to 2028-04-30 | An SSR or build-tool image |

Choose Alpine only when the runtime has no glibc dependency. PHP with `swoole`, `pdo_pgsql` and
`intl` builds on musl but the ICU data handling differs, and Node's prebuilt native modules are
built against glibc: an Alpine Node image compiles them from source at install time, which turns a
30-second install into a multi-minute one. The rule: if the image installs a native module or links
ICU, use the Debian slim line.

`docker init`'s PHP template is Apache-based and is not a starting point for an Octane or Swoole
service; its output would need every instruction in this file replaced.

## 6. `ARG` scope, and what `ARG` leaks

An `ARG` declared before the first `FROM` is available to every `FROM` line and to no `RUN`
instruction. To use it inside a stage, re-declare it inside that stage. This is the single most
common cause of an empty build variable:

```dockerfile
ARG OCTANE_BASE_IMAGE=registry.takhtenegar.ir/docker/octane-base:v1.3.1
FROM ${OCTANE_BASE_IMAGE} AS runtime
ARG OCTANE_BASE_IMAGE          # re-declared: now visible to RUN and LABEL in this stage
```

**A build argument is recoverable from image history.** `docker history` and the image config
record every `ARG` value the build used. A registry token, a Composer auth credential or a private
package password passed as `ARG` is therefore published with the image, and no later `RUN unset`
removes it. Build-time credentials use `RUN --mount=type=secret`; the forms are in this skill's
`references/15-build-secrets-and-attestations.md`.

## 7. Labels: the image says which commit it is

Rule id: `missing-oci-revision-label`.

```dockerfile
ARG VCS_REF=unknown
ARG BUILD_DATE=unknown
LABEL org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.source="https://gitlab.example/alaa/comment-service" \
      org.opencontainers.image.title="comment-service" \
      org.opencontainers.image.description="Comment service, Octane/Swoole runtime" \
      org.opencontainers.image.licenses="UNLICENSED" \
      org.opencontainers.image.base.name="registry.takhtenegar.ir/docker/octane-base:v1.3.1"
```

`org.opencontainers.image.revision` is the one that is mandatory, because it is the only way to
answer "which commit is running in production right now" from a running container:

```
docker inspect --format '{{index .Config.Labels "org.opencontainers.image.revision"}}' CONTAINER
```

The key set is the OCI predefined annotation list
(https://github.com/opencontainers/image-spec/blob/main/annotations.md, checked 2026-07-29).
`BUILD_DATE` must be passed as an RFC 3339 timestamp; leaving it defaulted is preferable to writing
a wrong value, because a timestamp that changes on every rebuild also changes the image digest and
destroys the cache for every consumer of the image. Whether the pipeline passes these arguments is
`/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`)'s call; the `LABEL` instruction is this skill's.

## 8. `USER`, and what runs as root

Rule id: `final-stage-root`.

The last `USER` in the final stage names a non-root user or a numeric UID. Use the numeric form,
`USER 1000:1000`, when the image is consumed by an orchestrator that may not resolve the name, and
match the `WWWUSER`/`WWWGROUP` build args the kit passes (`render-runtime.sh:1305-1306`), whose
default is 1000.

Ownership is set at copy time, not by a `RUN chown`:

```dockerfile
COPY --from=vendor --chown=1000:1000 /app /var/www/html
COPY --chown=1000:1000 --chmod=0555 docker/octane/ /usr/local/bin/octane/
```

A `RUN chown -R` after the fact writes a complete second copy of every file into a new layer,
which on a Laravel application with `vendor/` roughly doubles the image size for no benefit.

Directories the application writes to are created and chowned in the same `RUN` that creates them,
and the set is explicit, because the root filesystem is read-only at runtime (see this skill's
`references/20-compose-authorship.md` for the `read_only` and `tmpfs` keys that make it so):

```dockerfile
RUN set -eux; \
    mkdir -p storage/framework/{cache,sessions,views} storage/logs bootstrap/cache; \
    chown -R 1000:1000 storage bootstrap/cache
```

`USER` set before a `COPY` does not change what `COPY` writes — `COPY` runs as root unless
`--chown` says otherwise — so put `USER` last, after every `COPY` and `RUN` that needs privilege,
and never set it back to root afterwards.

## 9. PID 1, `ENTRYPOINT`, `CMD` and `STOPSIGNAL`

The process the container starts is PID 1, and PID 1 has no default signal handlers: a SIGTERM
delivered to a PID 1 that has not installed a handler is discarded, the container ignores
`docker stop`, and the runtime SIGKILLs it after the grace period. That is how an Octane worker
loses the request it was serving and how a queue worker loses the job it was running.

Rules:

- Use exec form everywhere: `ENTRYPOINT ["/usr/local/bin/octane/entrypoint.sh"]`, not
  `ENTRYPOINT /usr/local/bin/octane/entrypoint.sh`. Shell form wraps the command in
  `/bin/sh -c`, which becomes PID 1 and does not forward signals to its child.
- An entrypoint script ends with `exec "$@"` or `exec <command>`, so the real process replaces the
  shell and becomes PID 1 itself.
- `STOPSIGNAL SIGTERM` is the default and is written explicitly when the process needs a different
  signal — `STOPSIGNAL SIGQUIT` for an nginx front, which treats SIGQUIT as graceful shutdown and
  SIGTERM as fast shutdown.
- `ENTRYPOINT` holds what always runs; `CMD` holds the default arguments a Compose `command:` key
  overrides. This matters directly here: `service-runtime-kit` sets `command:` on every worker
  (`render-runtime.sh:1248,1250-1253`), which replaces `CMD` and leaves `ENTRYPOINT` in place, so
  any check the entrypoint performs after `exec "$@"` never runs for a worker. Put every
  precondition check *before* `exec`.
- Where the process genuinely cannot reap children — a wrapper that spawns background helpers —
  set `init: true` in Compose rather than adding a supervisor to the image. Reasoning and the key
  are in this skill's `references/40-healthcheck-and-lifecycle.md`.

## 10. `HEALTHCHECK` in the image

Rule id: `missing-healthcheck`.

```dockerfile
HEALTHCHECK --interval=10s --timeout=2s --start-period=45s --start-interval=2s --retries=3 \
  CMD ["/usr/local/bin/octane/healthcheck.sh"]
```

An image that must not carry a probe says so, so that "no healthcheck" is never ambiguous between
"considered and rejected" and "forgotten":

```dockerfile
# healthcheck-exempt: one-shot migration image; it exits, so there is no steady state to probe
```

The five options, what each does, the values per role, and `HEALTHCHECK NONE` are in this skill's
`references/40-healthcheck-and-lifecycle.md`. The Compose `healthcheck:` key overrides whatever the
image declares, so the two must be written together.

## 11. Image size and build time have budgets

An image-size rule with no number is not a rule. The budgets for this fleet, stated as CI-checkable
numbers:

| Image class | Compressed size budget | Cold build budget | Warm build budget |
|---|---|---|---|
| PHP Octane/Swoole service | 400 MB | 6 min | 90 s |
| Node SSR runtime | 250 MB | 4 min | 60 s |
| Static asset image (nginx + built assets) | 60 MB | 3 min | 30 s |
| One-shot job image (reuses the service image) | same as its service | 0 (no separate build) | 0 |

Measure, do not estimate:

```
docker image inspect --format '{{.Size}}' IMAGE                  # uncompressed, bytes
docker manifest inspect IMAGE | awk '/"size"/ {s+=$2} END {print s}'   # compressed, bytes
docker buildx build --progress=plain . 2>&1 | tail -1            # wall clock of the last step
```

Exceeding a budget is not automatically a defect; shipping past it without naming the cause is.
The merge request states which layer grew and why. `docker history --no-trunc IMAGE` orders layers
by size and names the instruction that created each one, which identifies the cause in one command.

Whether a size budget gates a pipeline is `/alaa-frontend-devops` (`$alaa-frontend-devops`)'s
decision for frontend images and `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`)'s to express; the
numbers above are this skill's, and they are what a gate would assert.

---

## Worked artifact A — Octane/Swoole PHP service

This is the shape every Laravel service in the fleet builds. It matches the `build:` stanza
`service-runtime-kit` emits (`render-runtime.sh:1295-1306`): `target: runtime`, and the build args
`IMAGE_PROXY_PREFIX`, `OCTANE_BASE_IMAGE`, `COMPOSER_VERSION`, `WWWUSER`, `WWWGROUP`.

```dockerfile
# syntax=docker/dockerfile:1

# The mirror prefix and the base image are build args because the kit passes them; their names are
# service-runtime-kit-governance's, their use here is this skill's. A default is given so a manual
# `docker build` with no --build-arg produces the same image the kit's up-local.sh produces.
ARG IMAGE_PROXY_PREFIX=mirror.cdn.ir/
ARG OCTANE_BASE_IMAGE=registry.takhtenegar.ir/docker/octane-base:v1.3.1
ARG COMPOSER_VERSION=2.9.5
ARG WWWUSER=1000
ARG WWWGROUP=1000

# ---------------------------------------------------------------------------
# Stage 1: the Composer binary, taken from the official image rather than
# downloaded, so the build makes no network call to install its own tooling.
# ---------------------------------------------------------------------------
FROM ${IMAGE_PROXY_PREFIX}composer:${COMPOSER_VERSION} AS composer-bin

# ---------------------------------------------------------------------------
# Stage 2: PHP dependencies. Nothing from this stage survives except /app.
# ---------------------------------------------------------------------------
FROM ${OCTANE_BASE_IMAGE} AS vendor
WORKDIR /app
COPY --from=composer-bin /usr/bin/composer /usr/bin/composer

# Manifest and lockfile only. This layer is invalidated by a dependency change
# and by nothing else, which is the whole point of copying them separately.
COPY composer.json composer.lock ./

# The cache mount keeps Composer's package archive between builds. uid/gid match
# the user the RUN executes as; without them the mount is root-owned and Composer
# writes to /tmp instead, silently losing the cache.
RUN --mount=type=cache,target=/tmp/composer-cache,uid=1000,gid=1000 \
    COMPOSER_HOME=/tmp/composer-cache \
    composer install \
      --no-dev --no-scripts --no-interaction --no-progress \
      --prefer-dist --optimize-autoloader

# Application source arrives after the install. Editing a controller now rebuilds
# this layer and the two after it, and does not re-resolve a single package.
COPY . .

RUN COMPOSER_HOME=/tmp/composer-cache \
    composer dump-autoload --classmap-authoritative --no-dev --no-interaction

# ---------------------------------------------------------------------------
# Stage 3: frontend assets, when the service serves any. Kept separate so a PHP
# change does not rebuild assets and an asset change does not re-run Composer.
# ---------------------------------------------------------------------------
FROM ${IMAGE_PROXY_PREFIX}node:24.9.0-trixie-slim AS assets
WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci --no-audit --no-fund
COPY resources ./resources
COPY vite.config.js ./
RUN npm run build

# ---------------------------------------------------------------------------
# Stage 4: runtime. This is `target: runtime`, the stanza the kit references.
# It receives artifacts and nothing else: no Composer, no npm, no source-only
# files, no build cache.
# ---------------------------------------------------------------------------
FROM ${OCTANE_BASE_IMAGE} AS runtime

ARG WWWUSER
ARG WWWGROUP
ARG VCS_REF=unknown
ARG BUILD_DATE=unknown

LABEL org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.title="comment-service" \
      org.opencontainers.image.description="Comment service, Octane/Swoole runtime" \
      org.opencontainers.image.base.name="registry.takhtenegar.ir/docker/octane-base:v1.3.1"

WORKDIR /var/www/html

# OPcache and JIT for a long-lived worker. Values and the argument for each are in
# alaa-docker-production references/60-resource-limits-and-load.md.
COPY --chmod=0444 docker/octane/opcache.ini /usr/local/etc/php/conf.d/10-opcache.ini
COPY --chmod=0444 docker/octane/php.ini      /usr/local/etc/php/conf.d/20-runtime.ini

# Runtime helper scripts, mode 0555: executable by everyone, writable by nobody,
# including the runtime user. The container cannot rewrite its own entrypoint.
COPY --chown=${WWWUSER}:${WWWGROUP} --chmod=0555 docker/octane/ /usr/local/bin/octane/

COPY --from=vendor --chown=${WWWUSER}:${WWWGROUP} /app /var/www/html
COPY --from=assets --chown=${WWWUSER}:${WWWGROUP} /app/public/build /var/www/html/public/build

# Writable paths are created explicitly, because the root filesystem is mounted
# read-only at runtime and everything else must fail loudly rather than silently.
RUN set -eux; \
    mkdir -p storage/framework/cache storage/framework/sessions storage/framework/views \
             storage/logs bootstrap/cache; \
    chown -R ${WWWUSER}:${WWWGROUP} storage bootstrap/cache

ENV OCTANE_SERVER=swoole \
    OCTANE_PORT=8000 \
    APP_DIR=/var/www/html

EXPOSE 8000
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=10s --timeout=2s --start-period=45s --start-interval=2s --retries=3 \
  CMD ["/usr/local/bin/octane/healthcheck.sh"]

USER ${WWWUSER}:${WWWGROUP}

ENTRYPOINT ["/usr/local/bin/octane/entrypoint.sh"]
CMD ["/usr/local/bin/octane/start-octane.sh"]
```

Two things this file deliberately does not do. It does not run `php artisan config:cache` at build
time, because the cached configuration would freeze the environment variables present during the
build rather than the ones present at runtime; that belongs in the entrypoint, after the `_FILE`
secrets are loaded (this skill's `references/35-secret-delivery.md`). And it does not install
extensions: `octane-base` carries `swoole`, `pdo_pgsql`, `redis` and `intl`, which is what makes
this Dockerfile short. Extension selection and Octane tuning are `/alaa-octane-performance`
(`$alaa-octane-performance`)'s subject; installing them into an image is this skill's.

## Worked artifact B — Node SSR frontend runtime

The frontend delivery gates that this image must satisfy are `/alaa-frontend-devops`
(`$alaa-frontend-devops`)'s register; how the image satisfies them is below.

```dockerfile
# syntax=docker/dockerfile:1

ARG IMAGE_PROXY_PREFIX=mirror.cdn.ir/
ARG NODE_IMAGE=node:24.9.0-trixie-slim

# ---------------------------------------------------------------------------
# Stage 1: dependencies. `npm ci` is used, not `npm install`: ci fails when
# package-lock.json disagrees with package.json, which is the behaviour that
# makes a build reproducible from a commit.
# ---------------------------------------------------------------------------
FROM ${IMAGE_PROXY_PREFIX}${NODE_IMAGE} AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci --no-audit --no-fund

# ---------------------------------------------------------------------------
# Stage 2: build. Needs the dev dependencies from stage 1 and the source.
# ---------------------------------------------------------------------------
FROM ${IMAGE_PROXY_PREFIX}${NODE_IMAGE} AS build
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# Build-time public configuration only. Anything secret at runtime is read from
# the environment by the server process, never compiled into a client bundle:
# a value in a client bundle is published to every visitor.
ARG PUBLIC_API_BASE_URL
ENV NUXT_PUBLIC_API_BASE=${PUBLIC_API_BASE_URL}
RUN npm run build

# ---------------------------------------------------------------------------
# Stage 3: production dependencies only. A second, separate install with
# --omit=dev, because pruning an existing tree leaves optional dev artifacts.
# ---------------------------------------------------------------------------
FROM ${IMAGE_PROXY_PREFIX}${NODE_IMAGE} AS prod-deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci --omit=dev --no-audit --no-fund

# ---------------------------------------------------------------------------
# Stage 4: runtime. No npm registry access, no dev dependencies, no source.
# ---------------------------------------------------------------------------
FROM ${IMAGE_PROXY_PREFIX}${NODE_IMAGE} AS runtime

ARG VCS_REF=unknown
LABEL org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.title="storefront-ssr" \
      org.opencontainers.image.base.name="node:24.9.0-trixie-slim"

WORKDIR /app
ENV NODE_ENV=production \
    PORT=3000 \
    # Node's default heap is sized from host memory, which in a container is the
    # host's, not the cgroup's. Set it against the Compose memory limit or the
    # process is OOM-killed by the kernel before V8 decides to collect.
    NODE_OPTIONS=--max-old-space-size=768

COPY --from=prod-deps --chown=1000:1000 /app/node_modules ./node_modules
COPY --from=build     --chown=1000:1000 /app/.output       ./.output
COPY --chown=1000:1000 package.json ./

EXPOSE 3000
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=10s --timeout=2s --start-period=15s --start-interval=1s --retries=3 \
  CMD ["node", "-e", "fetch('http://127.0.0.1:3000/healthz').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"]

# The image ships the `node` user at UID 1000; the numeric form is used so an
# orchestrator that does not resolve names still runs unprivileged.
USER 1000:1000

# Exec form, no shell, so SIGTERM reaches Node and its `close` handler runs.
CMD ["node", ".output/server/index.mjs"]
```

The `NODE_OPTIONS` line is the Node counterpart of the `nproc` trap described in this skill's
`references/60-resource-limits-and-load.md`: a container runtime constrains memory through cgroups,
and a process that sizes itself from `/proc/meminfo` sees the host. Set the heap to roughly 75% of
the Compose `deploy.resources.limits.memory` value and change both together.

---

## Reviewing an existing Dockerfile

Read in this order; each question has a one-command answer and the first "no" is the finding.

1. `head -1 Dockerfile` — is the syntax directive there?
2. `ls -a $(dirname Dockerfile)/.dockerignore` — does it exist, and does it list `.env` and the
   local-secrets directory?
3. `grep -n '^FROM' Dockerfile` — two or more, each with a non-floating tag?
4. `grep -n 'COPY \. ' Dockerfile` — does any whole-context copy appear before the install `RUN` in
   the same stage?
5. `grep -n '^USER' Dockerfile` — is the last one in the final stage non-root?
6. `docker history --no-trunc IMAGE | head -20` — does any layer in the final stage name a package
   manager?
7. `node scripts/check-dockerfile-contract.mjs Dockerfile` — this answers 1 to 5 mechanically and
   reports the `.dockerignore` gaps as well.

Anti-pattern diagnostics that the positive rules above cannot state, because they are about
spotting a shape rather than writing one:

| Symptom in an existing file | What it means | Where the fix is |
|---|---|---|
| `RUN rm -rf /some/secret` after a `COPY` | The secret is still in the earlier layer and is pullable. The image must be rebuilt, and the credential rotated. | §2, §6 |
| Final image is several hundred MB larger than the base | Either the build stage is the final stage, or a `RUN chown -R` duplicated the tree. `docker history` names the layer. | §4, §8 |
| Build is fast locally and slow in CI | The local build reuses a layer cache the runner does not have. The ordering in §3 is what makes a cold build fast, not the cache. | §3 |
| `docker stop` takes exactly the grace period, every time | PID 1 is a shell, or the entrypoint used shell form, so SIGTERM went nowhere. | §9 |
| A build variable is empty inside a `RUN` | `ARG` was declared before the first `FROM` and not re-declared in the stage. | §6 |
| Two builds of the same commit produce different digests | A floating base tag, a missing lockfile, or a `BUILD_DATE` label. | §3, §5, §7 |
