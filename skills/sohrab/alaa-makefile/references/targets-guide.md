# Targets, prerequisites and the standard target set

**Owner of:** `.PHONY` and its rationale, the GNU standard target set, prerequisite kinds including the
order-only form, double-colon rules, and the help target. No other file in this skill states these
rules.

## Anatomy

```makefile
target: normal-prerequisites | order-only-prerequisites
	recipe line, indented with one TAB
```

A target is a file make can create, or a name for an action. A prerequisite is something that must be up
to date first. A recipe is the shell commands that make the target, and every recipe line begins with a
literal tab — spaces produce `*** missing separator. Stop.`

## `.PHONY`

Declare every target that creates no file:

```makefile
.PHONY: all build test check install clean help
.PHONY: ci/build ci/release ci/deploy runtime/up
```

Two things happen without it. First, the day a file called `test` appears in the repository, `make test`
prints `make: 'test' is up to date.` and runs nothing — and on this fleet that is a CI gate that stopped
running while reporting success. Second, make consults its implicit-rule search for the target on every
invocation, which is wasted work.

Group the declarations near the targets they describe rather than in one block at the top of a long
file; both forms are legal and the grouped form survives editing better. `mbake` will insert missing
`.PHONY` declarations for you (`mbake-tool.md`).

A phony target must not be a prerequisite of a file target. The phony target is always out of date, so
the file target rebuilds on every run:

```makefile
# wrong: app.o rebuilds every time
.PHONY: generate
app.o: app.c generate

# right: depend on the file the generator produces
app.o: app.c config.h
config.h: config.h.in
	./gen-config.sh
```

## Prerequisite kinds

| Form | Meaning |
|---|---|
| `t: a b` | rebuild `t` when `a` or `b` is newer than `t` |
| `t: \| d` | `d` must exist before `t` is built, but its timestamp is ignored |
| `t:: a` | double-colon: each rule for `t` has an independent recipe, all of which run |
| `t: a .WAIT b` | GNU Make 4.4+: finish `a` before starting `b`. Owned by `optimization-guide.md` |

### Order-only prerequisites, for directories

A directory's modification time changes whenever any file is written into it. A normal prerequisite on a
directory therefore makes the target rebuild on every run. Use the order-only form:

```makefile
$(BUILDDIR)/app: $(SOURCES) | $(BUILDDIR)
	$(CC) $^ -o $@

$(BUILDDIR):
	mkdir -p $@
```

This is unconditional for directories: there is no case in which a directory belongs on the left of the
pipe. `scripts/validate_makefile.sh` reports a recipe that runs `mkdir -p` in a file that uses no
order-only prerequisite anywhere.

Order-only is also correct for a lock file, a state file and a marker file — anything whose existence
matters and whose timestamp does not.

### Double-colon rules

Rare and mostly avoidable. They allow several independent recipes for the same target, all of which run.
The one honest use is a modular file set where each fragment contributes a step to a shared name:

```makefile
# mk/app.mk
install:: ; install -m 755 $(APP) $(DESTDIR)$(BINDIR)/
# mk/docs.mk
install:: ; install -m 644 $(MAN) $(DESTDIR)$(MANDIR)/
```

Mixing `::` and `:` rules for one target is an error. When the steps have an ordering, use prerequisites
instead; the ordering of double-colon recipes is file order, which is not a contract anyone should rely
on.

## The standard target set

The GNU Coding Standards fix the meaning of these names, and a developer, a packager and a CI job all
assume them. Redefining one is worse than inventing a new name.

| Target | Contract |
|---|---|
| `all` | Build everything the repository produces. First target in the file, so it is the default goal. Does not install, does not clean, does not test. |
| `install` | Depends on `all`. Installs under `$(PREFIX)`, prefixing every path with `$(DESTDIR)`. Creates its own directories. Idempotent. |
| `uninstall` | Removes exactly what `install` placed. |
| `clean` | Removes build output. Leaves configuration, so a rebuild needs no reconfiguration. |
| `distclean` | Depends on `clean`. Also removes generated configuration, leaving only the sources. |
| `test` | Runs the test suite. Fails when a test fails. |
| `check` | GNU alias for `test`. Usually `check: test`. |
| `dist` | Produces a distribution archive. |
| `help` | Prints the documented targets. |

What the `test` and `check` targets must actually assert, and which test layer each belongs to, is
decided by `/alaa-testing-strategy` (`$alaa-testing-strategy`). This skill decides only that the target
exists, is phony, and fails when the command fails.

`scripts/add_standard_targets.sh` appends any of these that a file is missing, and `--dry-run` exits 1
when something is missing, so it can gate a pipeline. Every recipe it appends is a placeholder that
fails loudly until it is replaced with the real command.

## Naming beyond the standard set

Namespace with `/`:

```makefile
.PHONY: ci/build ci/release ci/deploy
.PHONY: runtime/render runtime/validate runtime/up
.PHONY: db/migrate db/seed
```

The namespace names the owner of the commands, which makes the boundary visible in `make help` and
groups the output. Name the target after the step, not the tool: `ci/build` survives a move from
`docker build` to `buildx`; `docker-build` does not. `ci-entrypoint.md` holds the fleet's target table.

Target names are a contract. A runner job, a developer's habit and another skill's route may all name
one, so renaming a target needs the same review as renaming a runner job.

## The help target

Document each target with a `## ` comment directly above it and let one target print them all:

```makefile
## Build and push the service image through the kit gate
ci/build:
	bash $(CI_KIT)/build_image.sh

## Show every documented target
help:
	@sed -n 's/^## //p' $(MAKEFILE_LIST)
```

`$(MAKEFILE_LIST)` contains every file make has read, so included fragments are documented too. Keep the
`##` line to one sentence that says what command the target fronts, and add a second `##` line when the
target is destructive or not idempotent.

`help` is the default goal in a Makefile that only fronts gates, because there is nothing safe for a bare
`make` to do in that file. In a Makefile that builds something, `all` is the default goal and `help` is a
named target.

## Target-specific variables

```makefile
ci/deploy: COMPOSE_MODE := prod
```

The value applies to the target and to everything it depends on. `variables-guide.md` owns the operator
and the inheritance rule.

## What this file does not decide

- The preamble, section order and includes: `makefile-structure.md`.
- Assignment operators and override precedence: `variables-guide.md`.
- Pattern rules, static pattern rules and automatic variables: `patterns-guide.md`.
- `.NOTPARALLEL`, `.WAIT`, `.INTERMEDIATE`, `.SECONDARY`, `.PRECIOUS`, `.NOTINTERMEDIATE`:
  `optimization-guide.md`.
- What a gate-fronting target may and may not do: `ci-entrypoint.md`.
- Compilation targets for C, C++ and Java: `native-toolchain.md`.
