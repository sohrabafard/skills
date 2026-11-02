# Fixture: a fleet-shaped Makefile that fronts commands owned elsewhere.
# Every target here is a local invocation of a command whose definition lives in
# service-ci-kit or service-runtime-kit. Running this file through
# validate_makefile.sh must report no error and no warning.

SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

# Where the shared kits are unpacked in a service repository.
CI_KIT := .service-ci-kit/ci/scripts
RUNTIME := scripts/runtime
COMPOSE_MODE ?= prod

.PHONY: help runtime/render runtime/validate runtime/up ci/build ci/release ci/migrate ci/deploy

## Show every target and the command it invokes (default target)
help:
	@sed -n 's/^## //p' $(MAKEFILE_LIST)

## Regenerate the runtime files from service-runtime-kit
runtime/render:
	bash $(RUNTIME)/render-runtime.sh --repo-root .

## Run the runtime contract validator exactly as the runner runs it
runtime/validate:
	bash $(RUNTIME)/validate-runtime.sh --repo-root .

## Bring the local Compose runtime up in COMPOSE_MODE
runtime/up: runtime/render
	bash scripts/docker/up-local.sh $(COMPOSE_MODE)

## Build and push the service image through the kit gate
ci/build:
	bash $(CI_KIT)/build_image.sh

## Run the semantic-release gate
ci/release:
	bash $(CI_KIT)/release.sh

## Run the database migration gate
ci/migrate:
	bash $(CI_KIT)/migrate_db.sh

## Run the deploy gate
ci/deploy:
	bash $(CI_KIT)/deploy.sh
