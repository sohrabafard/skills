# Makefile structure

**Owner of:** the hardening preamble, `.DELETE_ON_ERROR`, `.SUFFIXES`, `.POSIX`, file section order,
`include` and modular `.mk` files, and the recursive-versus-non-recursive decision. No other file in
this skill states these rules.

## The hardening preamble

Every Makefile in this fleet opens with these six lines, in this order, before any variable:

```makefile
SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules
```

A file that omits a line carries a comment directly above the gap naming the environment that forbids
it. "Simplicity" is not such an environment.

| Line | What it prevents | Floor |
|---|---|---|
| `SHELL := bash` | recipes silently running under `dash` (Debian) or `ash` (Alpine), where `source`, `[[`, arrays and `declare` fail | all |
| `.ONESHELL:` | each recipe line running in its own shell, so `cd` and shell variables do not survive to the next line | 3.82 |
| `.SHELLFLAGS := -eu -o pipefail -c` | the recipe reporting its **last** command's status while an earlier command failed; an unset variable expanding to empty; a failure in any pipe stage but the last being discarded | 3.82 |
| `.DELETE_ON_ERROR:` | a failed recipe leaving a partial target file that the next run treats as up to date | all |
| `--warn-undefined-variables` | a typo in a variable name expanding to the empty string and silently changing a command | 4.0 |
| `--no-builtin-rules` | make inventing a rule for a target you did not write, and searching roughly ninety built-in suffix rules per target | 4.0 |

`.ONESHELL:` and `.SHELLFLAGS` belong together and never apart. `.ONESHELL` without `-e` is this
skill's single worst silent-success mode; `ci-entrypoint.md` demonstrates it with a runnable fixture.

On `.DELETE_ON_ERROR`, the GNU manual is explicit that the behaviour it enables is what you want and
that you must ask for it: *"This is almost always what you want make to do, but it is not historical
practice; so for compatibility, you must explicitly request it."*

Add `.SUFFIXES:` with no prerequisites when the file defines any pattern or suffix rule. It clears the
built-in suffix list so make stops searching it. Add `.POSIX:` only when the file is genuinely written
to the POSIX `make` subset, which on this fleet means it must run under BSD make or an Alpine default
shell; `.POSIX:` with GNU-only syntax below it is a false claim.

## Section order

```makefile
# 1. First-line comment: what this file fronts, and any dialect decision
# 2. The hardening preamble
# 3. .SUFFIXES: and .POSIX: when they apply
# 4. User-overridable variables         (?=)          — variables-guide.md
# 5. Project-owned variables            (:=)          — variables-guide.md
# 6. include / -include                 (this file)
# 7. .PHONY declarations                              — targets-guide.md
# 8. The default target, documented with ##           — targets-guide.md
# 9. Everything else, grouped by lifecycle stage
# 10. The help target                                 — targets-guide.md
```

The default goal is the first non-special target in the file, so the ordering above is load-bearing:
moving a rule above `all` silently changes what `make` with no argument does. Special targets whose
names begin with a dot are never candidates for the default goal, so the preamble does not interfere.

## Includes and modular `.mk` files

```makefile
include config.mk          # fails if config.mk is missing
-include local.mk          # silently skipped if local.mk is missing
```

The `-` prefix on `include` is not the `-` prefix on a recipe line. On `include` it means "this file is
optional"; on a recipe line it means "discard this command's exit status", which is a blocking defect
(`ci-entrypoint.md`). Use `-include` for a developer's untracked local overrides and for generated
dependency files, and plain `include` for anything the build genuinely requires, so a missing shared
fragment fails at parse time rather than producing a subtly different build.

Split a Makefile when a section has its own lifecycle: `ci.mk` for gate targets, `runtime.mk` for
container targets, `dev.mk` for local conveniences. Keep the preamble in the top-level file only;
repeating it in an included fragment makes the effective `.SHELLFLAGS` depend on include order.

```makefile
include mk/ci.mk
include mk/runtime.mk
-include mk/local.mk
```

`$(MAKEFILE_LIST)` holds every file make has read, in order, so a help target built on it documents the
included fragments too without further work.

## Recursive versus non-recursive make

Non-recursive is the default. A single make process sees one dependency graph, so it rebuilds exactly
what changed and parallelises correctly.

```makefile
# Non-recursive: one process, one graph
SRC := $(wildcard src/*.c) $(wildcard lib/*.c)
OBJ := $(SRC:%.c=build/%.o)
```

Recursive make gives each sub-directory its own process and its own graph. The processes cannot see each
other's prerequisites, so a change in `lib/` does not rebuild what depends on it in `src/`, and a
parallel build can start a dependent before its dependency finishes. Peter Miller's *Recursive Make
Considered Harmful* is the canonical statement of why.

Two cases where recursion is nonetheless correct: a genuinely separate build system in a sub-directory
that you do not own, and a target that fronts another repository's Makefile. In both, use `$(MAKE)`:

```makefile
## Build the vendored component with its own build system
vendor/build:
	$(MAKE) -C third_party/thing
```

`$(MAKE)` propagates `-j` through the jobserver, propagates `-n` so a dry run stays dry, and propagates
`MAKEFLAGS`. Bare `make` propagates none of them: under `make -n` it *executes*, and under `make -j` the
sub-build serialises. The validator reports bare `make` in a recipe.

Never write `for dir in $(SUBDIRS); do $(MAKE) -C $$dir; done`. The loop is one recipe line, so a failure
in the first directory is invisible unless the shell is running under `-e`, and the directories cannot
run in parallel. Use a phony target per directory instead, which restores both:

```makefile
SUBDIRS := lib1 lib2 lib3
.PHONY: $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@

lib2: lib1        # express the real ordering as prerequisites
```

## Recipe line mechanics

With `.ONESHELL:` set, every line of a recipe runs in one shell, so `cd` persists and a shell variable
set on one line is visible on the next. Without it, each line is a separate shell and neither survives —
which is the reason the preamble sets it. Because `.SHELLFLAGS` supplies `-e`, a failure on any line ends
the recipe.

`@` suppresses the echo of a command. Use it on `echo`, `printf` and `sed`, and on nothing that can
fail: silencing a command removes it from the log, and the command is what a reader needs when it fails.

A backslash continues a logical line. There must be no character after the backslash, not even a space.
Inside a recipe, `$$` is a literal dollar for the shell and `$` alone is a make expansion; this is the
single most common source of an empty shell variable in a loop.

## What this file does not decide

- Which assignment operator a variable takes: `variables-guide.md`.
- `.PHONY`, standard targets and order-only prerequisites: `targets-guide.md`.
- Pattern rules and automatic variables: `patterns-guide.md`.
- `.NOTPARALLEL`, `.WAIT` and intermediate-file handling: `optimization-guide.md`.
- Gate fronting and verdict propagation: `ci-entrypoint.md`.
- C, C++ and Java compilation structure: `native-toolchain.md`.
