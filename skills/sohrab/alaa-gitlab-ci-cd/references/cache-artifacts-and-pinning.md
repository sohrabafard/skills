# Cache, artifacts and pinning

Three subjects that share one property: each is a value written in a pipeline
file whose effect is invisible from the file itself unless it is written
deliberately.

## Table of contents

- Cache keys
- `policy:`, `untracked` and `when`
- `fallback_keys`
- Where a cache actually lives
- Artifacts: scope, retention and reports
- Pinning an image reference in each of the five places
- Fanning one pin out from one variable

## Cache keys

The key answers one question: *when should the cached contents be considered
stale?* Derive it from whatever decides that.

**Lockfile-derived, which is the default correct answer for a dependency cache:**

```yaml
cache:
  key:
    files:
      - composer.lock
    prefix: vendor
  paths:
    - vendor/
```

GitLab hashes the named files and appends the hash to `prefix`. The key changes
exactly when the dependency set changes and at no other time. **`key:files`
accepts a maximum of two file paths.** More than two is a configuration error,
not a slow path; `validate_gitlab_ci.py` reports `cache-key-files-limit`.

**A literal or variable-built key** is correct only when the cached contents
depend on something no file records:

```yaml
cache:
  key: "$CI_JOB_NAME-$CI_COMMIT_REF_SLUG"
```

Two hazards to check before writing one:

- A key that omits the branch shares one cache across every branch. On a
  persistent shell runner that is a cross-branch write path: a job on any branch
  can put content into the cache that a job on the default branch then restores.
- A key that omits the job name shares one cache between jobs with different
  contents, and the last writer wins.

`cache:` with no `key:` at all uses the literal string `default`, so every job on
the runner shares one entry. `validate_gitlab_ci.py` reports `cache-key-missing`
and `cache-key-not-lockfile-derived`.

## `policy:`, `untracked` and `when`

`policy:` takes `pull`, `push` or `pull-push`, and the default is `pull-push` —
so a job that only reads the cache still re-uploads it at the end, paying upload
time and risking a write from a job that had no business writing.

The shape that follows from that: one job builds the cache with `policy: push`,
every other job reads it with `policy: pull`.

```yaml
warm_cache:
  cache: {key: {files: [composer.lock]}, paths: [vendor/], policy: push}

unit_tests:
  cache: {key: {files: [composer.lock]}, paths: [vendor/], policy: pull}
```

`untracked: true` adds every file Git does not track to the cache. Use it only
when the tool's output location is not knowable in advance; otherwise it caches
build output nobody wanted and grows without bound.

`cache:when` takes `on_success` (default), `on_failure` or `always`. Use
`on_failure` or `always` only for a cache whose value survives a failed job, such
as a package download directory.

## `fallback_keys`

When the exact key misses, GitLab tries each fallback in order and uses the first
hit. **Up to five fallback keys per cache entry.**

```yaml
cache:
  key:
    files: [composer.lock]
  fallback_keys:
    - vendor-$CI_DEFAULT_BRANCH
    - vendor-default
  paths: [vendor/]
```

The value of a fallback is a partially warm cache after a lockfile change. The
cost is that a fallback restores contents keyed on a *different* dependency set,
so the job must still run the install step and let it reconcile. Never use a
fallback as a substitute for the install step. `validate_gitlab_ci.py` reports
`fallback-keys-limit`.

## Where a cache actually lives

This is where most cache designs fail silently.

- **Shell executor:** the cache is a directory on that host, under the runner
  user's home unless `cache_dir` says otherwise. It survives between jobs. It is
  shared by every project that runs on that host. It does not exist on any other
  host.
- **Docker executor:** a Docker volume on that host. Same locality.
- **Kubernetes executor:** each job is a new pod. **A cache written to the pod's
  filesystem does not exist for the next job.** Without distributed cache storage
  configured on the runner, every `cache:` key in every pipeline on that runner is
  a no-op that costs upload time and returns nothing.

Distributed cache means a `[runners.cache]` block with a `Type` and its
credentials, so the runner uploads and downloads cache archives from object
storage. That is runner-side configuration, covered in
`runner-shell-and-kubernetes.md`; `validate_runner_config.py` reports
`kube-cache-not-distributed`. The object store itself — bucket naming, lifecycle,
credentials — belongs to `/alaa-minio-object-storage`
(`$alaa-minio-object-storage`) or `/alaa-arvan-object-storage`
(`$alaa-arvan-object-storage`).

If distributed cache is not available, say in the answer that caching is
deliberately off and why, rather than shipping `cache:` blocks that do nothing.

## Artifacts: scope, retention and reports

A cache is an optimisation the pipeline may lose without changing its result. An
artifact is an output a later job or a human depends on. Do not use one for the
other.

```yaml
build:
  artifacts:
    expire_in: 1 week
    when: on_success
    paths:
      - dist/
    reports:
      dotenv: build.env
```

- **`expire_in` is not optional.** When it is unset, GitLab applies the
  instance-wide default, which the pipeline author cannot see and an
  administrator can change. Write it. `validate_gitlab_ci.py` reports
  `artifacts-expire-missing`.
- **`when:`** takes `on_success` (default), `on_failure` or `always`. A test
  report or a log bundle is worth more on failure than on success, so those take
  `always`.
- **`reports:dotenv`** publishes variables into every job that `needs:` this one.
  It is the correct handoff for a value computed in one job — a version string, a
  built image tag — and it is not a place for a secret, because it is stored as a
  job artifact.
- **Scope the paths.** An artifact is uploaded, stored and downloaded by every
  dependent job. A database dump, a full `vendor/` tree or a log of a production
  export in an artifact is a copy of that data with the artifact's retention and
  the project's access rules, not the data store's. Where a job produces data of
  that kind, write it to the store that owns it and publish only a reference.
  Whether the data class may be copied at all is
  `/alaa-security-review` (`$alaa-security-review`)'s decision.

## Pinning an image reference in each of the five places

The prohibition on floating tags is `/alaa-frontend-devops`
(`$alaa-frontend-devops`)'s. This section is the mechanism: an image reference can
appear in five places, and a pin that covers only one of them is not a pin.

**1. `image:` on a job.**

```yaml
build:
  image: registry.example.com:5000/ci/php:8.5.8-alpine3.24
```

**2. `default: image:`, with `name:` and `entrypoint:` when the image has an
entrypoint that would swallow the job script.**

```yaml
default:
  image:
    name: moby/buildkit:v0.31.2-rootless
    entrypoint: [""]
```

A top-level `image:` does the same thing and is deprecated; use `default:`.

**3. A `services:` entry.** A service image is an input to the job's result
exactly as the build image is. Pin its major and minor to the version the
service runs in production, and pin both from the same source.

```yaml
default:
  services:
    - name: registry.example.com:5000/mirror/postgres:17.7-alpine3.24
      alias: postgres
```

**4. `image =` inside `[runners.kubernetes]`**, in `config.toml` or in the Helm
chart's `runners.config`. This is the image used when a pipeline declares no
`image:` at all — the case where every pin in the pipeline file inspects a key
that does not exist. If a fleet's pipelines carry no `image:`, this is where the
whole toolchain pin lives.

**5. `helper_image`**, also under `[runners.kubernetes]`. The helper container
clones the repository and uploads artifacts. Left unset it is pulled from
GitLab's registry at job time, which fails in a restricted-egress cluster; set it
to a mirrored, version-tagged reference.

Both 4 and 5 are checked by `validate_runner_config.py`
(`kube-image-unpinned`, `kube-helper-image-unpinned`, `kube-helper-image-unset`).

### Tag or digest

A **version tag** (`8.5.8-cli-alpine3.24`) is the normal form. It is readable, it
sorts, and a reader can tell what moved.

A **digest** (`php@sha256:...`) is required when the exact bytes must not change
between two runs of the same pipeline: a release build whose output is signed or
attested, a base image outside your control, or any image referenced from a
protected-ref job. Use both together where readability also matters:
`php:8.5.8-cli-alpine3.24@sha256:...`.

A tag with no version component — `latest`, `rootless`, `stable`, `edge`, `main`
— is floating whatever it is called. `validate_gitlab_ci.py` reports
`image-latest` for all of them, not only for the literal string `latest`.

### A private registry with an explicit port

`registry.example.com:5000/team/php` has **no tag**: the colon belongs to the
port. The pinned form puts the tag after the repository path:

```
registry.example.com:5000/team/php:1.8.3
registry.example.com:5000/team/php@sha256:...
```

This is the fleet's normal case and it is the form a naive regular expression
mistakes for a pinned image. Both bundled checkers split the reference on the
last colon that is not inside a path segment, so the port form is classified
correctly.

## Fanning one pin out from one variable

A version that appears in three places moves in one place and rots in the other
two. Declare it once and reference it:

```yaml
variables:
  PHP_IMAGE_TAG: "8.5.8-cli-alpine3.24"
  POSTGRES_IMAGE_TAG: "17.7-alpine3.24"

default:
  image: registry.example.com:5000/ci/php:$PHP_IMAGE_TAG
  services:
    - name: registry.example.com:5000/mirror/postgres:$POSTGRES_IMAGE_TAG
      alias: postgres
```

Where the same value must also be true of a runtime deployment — the PostgreSQL
major and minor a service tests against matching the one it runs against — the
variable is a shared name and its canonical home is
`/alaa-services-contract` (`$alaa-services-contract`). This file states only that
the value is written once and referenced, not what the value is.
