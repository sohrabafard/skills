# Fixture: one target per defect this checker must catch.
# Every finding below was invisible to the previous revision.

.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

# Recursive assignment holding $(shell ...): the command re-runs on every reference.
BUILD_DIR = $(shell git rev-parse --show-toplevel)/build

.PHONY: clean sub deploy release bootstrap

## Remove build output (default target)
clean:
	-rm -rf $(BUILD_DIR)/*

## Delegate to a sub-Makefile with bare make instead of $(MAKE)
sub:
	make -C sub build

## Deploy with the exit status thrown away
deploy:
	bash .service-ci-kit/ci/scripts/deploy.sh || true

## Build and push an image inline instead of through the kit gate
release:
	docker build -t myapp:latest .
	docker push myapp:latest

## Use bash-only constructs while SHELL is not set to bash
bootstrap:
	source ./env.sh
	declare -A registry
