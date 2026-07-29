# Makefile variables

**Owner of:** `=`, `:=`, `::=`, `?=`, `+=`, `!=`, override precedence, `export`/`unexport`/`override`,
the environment boundary, and `$(shell …)` caching. No other file in this skill states these rules.

## The five assignment operators

| Operator | Expansion | Use it for |
|---|---|---|
| `:=` | immediate, once, at the point of assignment | every project-owned value, and everything computed |
| `=` | deferred, re-expanded on every reference | only a value that must see a variable defined later |
| `?=` | deferred, and only if the variable is not already set | every value a user, the environment or the runner may override |
| `+=` | follows the flavour of the original assignment | extending a list |
| `!=` | runs a shell command once and assigns the output | a shell result, where `:=` with `$(shell …)` also works |

### `:=` is the default

```makefile
SOURCES := $(wildcard src/*.c)
OBJECTS := $(SOURCES:src/%.c=build/%.o)
VERSION := $(shell git describe --tags --always --dirty 2>/dev/null || echo dev)
```

With `=`, each of those re-runs its right-hand side at every reference. `VERSION = $(shell git …)` forks
git once per use; `BUILD_TIME = $(shell date +%s)` gives a *different* value in two targets of the same
run. `scripts/validate_makefile.sh` reports `NAME = $(shell …)` as a finding for exactly this reason.

`::=` is the POSIX spelling of `:=` and behaves identically in GNU Make. Write `:=` unless the file
declares `.POSIX:`.

### `?=` marks the override boundary

```makefile
PREFIX ?= /usr/local
COMPOSE_MODE ?= prod
CI_KIT ?= .service-ci-kit/ci/scripts
```

`?=` assigns only when the variable is unset **or set to the empty string from the environment**. It is
the correct operator for anything a developer, an environment file or a runner job may need to change:

```console
make ci/deploy CI_KIT=/opt/kit/ci/scripts
CI_KIT=/opt/kit/ci/scripts make ci/deploy
```

A value the file owns takes `:=`, so an accidental environment variable of the same name cannot change
the build. Choosing `?=` for a project-owned value is how an unrelated exported variable silently
rewrites a command.

### Fail closed rather than defaulting

A variable whose absence must stop the run does not get a default:

```makefile
IMAGE ?= $(error IMAGE is not set)
API_TOKEN ?= $(error API_TOKEN is not set; export it or use the secret store)
```

`$(error …)` inside `?=` is deferred, so it fires when the variable is *referenced*, not when the file is
parsed — a target that does not use `IMAGE` still runs. That is the intended behaviour. Use it for any
value whose wrong default is worse than a stopped build: a registry, an image tag, a credential, a
destination host, a size cap. `security-guide.md` owns the credential case;
`/alaa-security-review` (`$alaa-security-review`) decides what must fail closed.

### `+=` inherits the original flavour

```makefile
CFLAGS ?= -Wall -Wextra -O2   # deferred
CFLAGS += -Iinclude           # still deferred

DIRS := build
DIRS += build/obj             # still immediate
```

Appending to a variable that was never assigned creates a deferred one. Assign first, then append.

## Override precedence

From strongest to weakest, the value that wins is:

1. `make VAR=value` on the command line.
2. An `override VAR = value` directive in the Makefile.
3. A plain assignment in the Makefile.
4. `VAR ?= value` in the Makefile, when the variable is otherwise unset.
5. The environment, when `-e` is passed or when the Makefile used `?=`.
6. Make's built-in default, for the variables that have one.

`override` exists so a Makefile can add to a flag the user also set:

```makefile
override CFLAGS += -DPROJECT_VERSION=\"$(VERSION)\"
```

Without `override`, a command-line `CFLAGS=...` discards the addition silently. Use `override` only for
a value the file must contribute; using it to defeat a deliberate user override is a defect.

## The environment boundary

```makefile
export DATABASE_URL          # visible to every recipe's shell
unexport HISTFILE            # explicitly withheld
```

`export` with no argument exports everything, and `.EXPORT_ALL_VARIABLES:` does the same. Both send every
Make variable — including any that holds a credential — to every subprocess, and both are reported by
the validator. Export the specific names the recipes need.

Inside a recipe, `$(VAR)` is a Make variable expanded before the shell sees the line, and `$$VAR` is a
shell variable the shell expands itself. A loop that writes `$file` sees an empty Make variable:

```makefile
# wrong: $file is a Make variable, and it is empty
check:
	for f in *.sh; do shellcheck $f; done

# right
check:
	for f in *.sh; do shellcheck "$$f"; done
```

Quote every expansion that reaches a shell command. `$(FILES)` with a space in a path becomes two
arguments; `"$(FILES)"` becomes one. Where a value comes from outside the repository, quoting is not
sufficient on its own — `security-guide.md` owns validation of untrusted values.

## Guarding at the boundary

```makefile
ifndef CI_KIT
$(error CI_KIT is not set)
endif

ifeq ($(strip $(COMPOSE_MODE)),)
$(error COMPOSE_MODE must be dev or prod)
endif
```

Conditional directives are evaluated at parse time and are not indented with a tab — a tab makes them
part of the preceding recipe. GNU Make 4.4 adds `$(intcmp a,b,lt,eq,gt)` for numeric comparison and
`$(let name,value,body)` for a scoped local; both raise the file's floor to 4.4, which
`scripts/validate_makefile.sh` reports against the locally installed make.

## Standard variable names

Use the GNU names where a GNU meaning exists, because packagers and CI images already set them:
`PREFIX`, `DESTDIR`, `BINDIR`, `LIBDIR`, `SYSCONFDIR`, `INSTALL`, `RM`. `DESTDIR` is prepended by the
packager and is never given a value in the Makefile:

```makefile
PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin

install: all
	install -d $(DESTDIR)$(BINDIR)
	install -m 755 $(TARGET) $(DESTDIR)$(BINDIR)/
```

The compiler variables — `CC`, `CXX`, `AR`, `RANLIB`, `CFLAGS`, `CXXFLAGS`, `CPPFLAGS`, `LDFLAGS`,
`LDLIBS`, `YACC`, `LEX` — and the full documentation-directory set are in `native-toolchain.md`, because
nothing on this fleet compiles native code.

Shared names that cross a service boundary — log field names, the `alaa_*` metric catalog, `OTEL_*`
values and defaults, host-port assignments — are decided by `/alaa-services-contract`
(`$alaa-services-contract`), not here. Which generator variable expresses a runtime value is decided by
`/service-runtime-kit-governance` (`$service-runtime-kit-governance`).

## Naming

Upper case for anything overridable, lower case for a purely internal value. Full words: `SOURCES`, not
`S`. Do not reuse a name make already owns — assigning `MAKEFLAGS` replaces make's own flags rather than
adding to them, which is why the preamble uses `+=`, and assigning `MAKE` breaks every sub-make.

## Target-specific and pattern-specific values

```makefile
ci/deploy: COMPOSE_MODE := prod
ci/deploy: ; bash $(CI_KIT)/deploy.sh

test/%: VERBOSE := 1
```

A target-specific value applies to that target **and to everything it depends on**, which is the usual
surprise. When a prerequisite is shared with another target, the value leaks into it; give the shared
work its own target rather than relying on the inherited value.

## Quiet mode

```makefile
VERBOSE ?= 0
ifeq ($(VERBOSE),1)
Q :=
else
Q := @
endif

build:
	$(Q)$(COMPOSE) build
```

`make build VERBOSE=1` shows the commands. Do not apply `$(Q)` to a command that fronts a gate;
`ci-entrypoint.md` owns that prohibition.

## What this file does not decide

- The preamble and `MAKEFLAGS` lines themselves: `makefile-structure.md`.
- `.PHONY` and the standard targets that use these variables: `targets-guide.md`.
- Automatic variables `$@ $< $^ $*`: `patterns-guide.md`.
- Caching a `$(shell …)` for speed rather than correctness: `optimization-guide.md`.
- Credential handling and untrusted-value validation: `security-guide.md`.
