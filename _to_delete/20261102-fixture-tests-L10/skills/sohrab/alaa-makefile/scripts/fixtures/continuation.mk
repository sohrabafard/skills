# Fixture: legal line continuation.
#
# `SOURCES = main.c \` continued by a four-space-indented `utils.c` is correct
# Make syntax. The previous revision of validate_makefile.sh matched any 2, 4 or
# 8 space indent anywhere in the file and reported this as
# "Potential spaces instead of tabs in recipes detected", exit 2.
# This fixture is the regression test for that false positive.

SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

SOURCES = main.c \
    utils.c \
    config.c

.PHONY: list

## List the source files (default target)
list:
	@printf '%s\n' $(SOURCES)
