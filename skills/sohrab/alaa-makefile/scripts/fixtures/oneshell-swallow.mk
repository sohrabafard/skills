# Fixture: the silent-success Makefile the appendix demonstrated.
#
# .ONESHELL turns the whole recipe into a single shell invocation whose status is
# the status of its LAST command. .SHELLFLAGS is absent, so the shell does not run
# under -e. `cd /nonexistent` fails, the recipe keeps going, `echo` succeeds, and
# `make deploy` prints "still ran - failure was swallowed" and exits 0.
#
# Reproduce the failure:  make -f oneshell-swallow.mk deploy ; echo "exit=$?"
# Expected:               exit=0 while the deploy did not happen.
#
# validate_makefile.sh must report this as an error. Before the repair in this
# revision the .ONESHELL check was dead code and the validator said nothing.

SHELL := bash
.ONESHELL:
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

.PHONY: deploy

## Deploy the service (default target)
deploy:
	cd /nonexistent
	echo "still ran - failure was swallowed"
