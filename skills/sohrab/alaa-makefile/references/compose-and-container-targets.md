# Targets that front Compose and image builds

**`/alaa-docker-production` (`$alaa-docker-production`) owns the Dockerfile, the image expression and
the Compose file, including the fail-closed interpolation invariant.** This file owns only the target
name, its prerequisites and its failure propagation. Nothing here authorises writing a Dockerfile, a
`compose.yaml` or a registry policy; if a task needs one of those, route it.

Read `ci-entrypoint.md` first: everything it says about verdict propagation applies here unchanged, and
is not repeated.

## On this fleet, a container target fronts a script, not `docker` directly

`service-runtime-kit` already owns the local container lifecycle. Its `up-local.sh` renders the runtime
files, ensures the shared network, boots shared infra, builds the runtime image, provisions the database
and starts the app, worker and scheduler services. A Makefile that runs `docker compose up` itself
skips all of that and produces a local runtime that differs from every other developer's.

```makefile
RUNTIME ?= scripts/runtime
COMPOSE_MODE ?= prod

## Bring the local runtime up in COMPOSE_MODE (dev or prod)
runtime/up: runtime/render
	bash scripts/docker/up-local.sh $(COMPOSE_MODE)

## Regenerate the runtime files from service-runtime-kit
runtime/render:
	bash $(RUNTIME)/render-runtime.sh --repo-root .
```

Write a bare `docker compose` target only in a repository that has no runtime kit. `up-local.sh` exits
`0` on success, `1` on a runtime, dependency or contract failure and `2` on invalid arguments, so the
`COMPOSE_MODE` value must be `dev` or `prod`; a Makefile that passes anything else turns a usable error
into a usage dump.

## Where a target does invoke `docker compose` directly

Name the target after the lifecycle step, not after the tool, and keep one command per recipe line so a
failure names the step that failed.

```makefile
COMPOSE ?= docker compose
COMPOSE_FILE ?= compose.yaml
ENV_FILE ?= .env

## Start the stack in the background
compose/up:
	$(COMPOSE) -f $(COMPOSE_FILE) --env-file $(ENV_FILE) up -d

## Stop the stack and remove its containers, keeping named volumes
compose/down:
	$(COMPOSE) -f $(COMPOSE_FILE) down --remove-orphans

## Stop the stack and delete its named volumes. Destroys local data.
compose/purge:
	$(COMPOSE) -f $(COMPOSE_FILE) down --remove-orphans --volumes
```

Four rules, each of which a reviewer can check by reading the recipe:

1. **`--env-file` is the only interpolation source a target may add.** Compose interpolates from the
   shell environment and `--env-file`, never from a service-level `env_file:` key. A target that exports
   a variable to make interpolation succeed is hiding a missing `--env-file` entry, and it will succeed
   locally and fail on the runner.
2. **`down --volumes` is never the recipe of a target named `down` or `clean`.** Give data destruction
   its own target with a name that says so and a `##` line that says so. A developer types `make clean`
   without reading it.
3. **A container target is `.PHONY`.** It creates no file whose timestamp means anything.
4. **No `-` prefix and no `|| true`,** including on `down`. If the stack may legitimately not be running,
   `docker compose down` already exits 0 in that case; if some other command does not, test the
   condition rather than discarding the status.

## Image builds

On this fleet, `ci/build` fronts `build_image.sh` and the Makefile does not run `docker build` at all.
`scripts/validate_makefile.sh` reports an inline `docker build` or `docker push` as a fleet-boundary
finding and names `ci/scripts/build_image.sh`.

In a repository with no kit, the target still decides nothing about the image:

```makefile
IMAGE ?= $(error IMAGE is not set)

## Build the service image
image/build:
	docker build --pull -t $(IMAGE) .

## Push the service image
image/push: image/build
	docker push $(IMAGE)
```

- `IMAGE` fails closed with `$(error …)` rather than defaulting. A default tag pushed to a real registry
  is the failure mode this prevents.
- A tag, a digest, a build argument, a target stage, a cache mount and a registry are all decided by
  `/alaa-docker-production` (`$alaa-docker-production`). The Makefile passes what that skill specifies.
- Never pass a secret as `--build-arg`; it is recorded in the image's layer history. `security-guide.md`
  owns the alternative.

## Parallel safety

An image build and a package installer both write to a shared cache, so two of them under `make -j`
corrupt it. `optimization-guide.md` owns `.NOTPARALLEL`, `.WAIT` and the version floors for each; the
short form is that on GNU Make 4.4 or newer `.NOTPARALLEL: image/build image/push` serialises just those
targets, and on older releases a shared prerequisite is the portable equivalent. The validator reports
the absence of either when it sees such a command.

## Cleanup

`docker image rm` on an image that is not present exits non-zero, which is exactly the case people
reach for `-` or `|| true` to suppress. Test the condition instead:

```makefile
## Remove the locally built image if it exists
image/rm:
	if docker image inspect $(IMAGE) >/dev/null 2>&1; then docker image rm $(IMAGE); fi
```

That recipe needs `SHELL := bash` and `.SHELLFLAGS := -eu -o pipefail -c` to behave, both of which the
mandated preamble supplies; `makefile-structure.md` owns the preamble.

## What this file does not decide

- Dockerfile content, base images, stages, users, healthchecks, image tags and the Compose file itself:
  `/alaa-docker-production` (`$alaa-docker-production`).
- Which generator variable expresses a runtime value in a rendered Compose file:
  `/service-runtime-kit-governance` (`$service-runtime-kit-governance`).
- How the build job is expressed on a runner: `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`).
- Kubernetes and Helm equivalents of these targets: `/alaa-k8s-helm` (`$alaa-k8s-helm`), and for Arvan
  CaaS `/caas-arvan-kuber` (`$caas-arvan-kuber`).
