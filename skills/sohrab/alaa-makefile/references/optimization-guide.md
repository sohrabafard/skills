# Parallel safety and incremental builds

**Owner of:** `-j`, `--shuffle`, `--output-sync`, `.NOTPARALLEL`, `.WAIT`, `.INTERMEDIATE`,
`.SECONDARY`, `.PRECIOUS`, `.NOTINTERMEDIATE`, and the debugging flags. No other file in this skill
states these rules.

Version floors below are against GNU Make 4.4.1, the current stable release, verified 2026-07-29;
`SOURCES.md` carries the command that re-derives it.

## Parallel execution

```bash
make -j$(nproc)          # one job per core
make -j4                 # four jobs
make -j                  # unbounded; do not use in CI, it will exhaust memory
make -j4 --output-sync=target   # keep each target's output together
```

`--output-sync=target` is not optional in CI. Without it, several jobs interleave their output line by
line and the log becomes unreadable exactly when a build fails.

`$(MAKE)` passes `-j` to a sub-make through the jobserver, so the total job count stays bounded. Bare
`make` does not, so it serialises — one more reason `makefile-structure.md` forbids it.

## Making a Makefile parallel-safe

The defect is always the same shape: two recipes that can run at once touch the same thing.

```makefile
# unsafe: both recipes append to one file
report/a: ; echo a >> shared.log
report/b: ; echo b >> shared.log
```

Three correct fixes, in order of preference:

1. **Give each recipe its own output**, then combine in a third target that depends on both. This keeps
   the parallelism.
2. **Express the real ordering as a prerequisite.** If `b` genuinely needs `a` to have finished, `b: a`
   is the honest statement, and make will never run them together.
3. **Serialise explicitly** with `.NOTPARALLEL` or `.WAIT` when the ordering is a resource constraint
   rather than a data dependency.

### `.NOTPARALLEL`

```makefile
.NOTPARALLEL:                              # all versions: nothing in this file runs in parallel
.NOTPARALLEL: image/build image/push       # GNU Make 4.4+: serialise these targets' prerequisites
```

The bare form is a blunt instrument and costs the whole file its parallelism; reach for it only in a file
whose every target touches one shared resource. The form with prerequisites arrived in 4.4 and inserts a
`.WAIT` between each prerequisite of the named targets.

### `.WAIT`

```makefile
## Run the pipeline stages locally in the order the runner runs them
ci/all: ci/build .WAIT ci/release .WAIT ci/deploy
```

`.WAIT` in a prerequisite list means "everything to my left completes before anything to my right
starts". It expresses ordering without inventing a dependency, so `ci/release` does not acquire
`ci/build` as a prerequisite it would rebuild. It has no effect in a serial build, and it needs GNU Make
4.4 or newer.

Guard a 4.4 construct when the file must also run on an older release:

```makefile
MIN_MAKE := 4.4
ifeq ($(firstword $(sort $(MAKE_VERSION) $(MIN_MAKE))),$(MIN_MAKE))
ci/all: ci/build .WAIT ci/release
else
ci/release: ci/build
ci/all: ci/release
endif
```

`scripts/validate_makefile.sh` detects `.WAIT`, `.NOTPARALLEL` with prerequisites, `.NOTINTERMEDIATE`,
`$(let …)` and `$(intcmp …)`, and reports an error when the locally installed make is older than 4.4.

### `--shuffle` is how you test the claim

```bash
make --shuffle=random -j$(nproc)     # GNU Make 4.4+
make --shuffle=reverse -j$(nproc)
make --shuffle=12345 -j$(nproc)      # reproduce a specific ordering by seed
```

`--shuffle` randomises the order in which make considers prerequisites, which surfaces a missing
prerequisite that the file's declaration order was accidentally hiding. A serial build and a `-j` build
in declaration order can both pass while the graph is wrong; a shuffled build fails. Run it before
claiming a Makefile is parallel-safe, and record the seed of any failure so it can be replayed.

`--jobserver-style=fifo` selects the named-pipe jobserver, also new in 4.4, which is more robust than the
pipe-based one across a `sudo` or a container boundary. Leave it at the default unless a sub-process is
losing the jobserver.

## Shared caches serialise

A package installer and an image build both write to a cache outside the build directory, so two of them
at once corrupt it:

```makefile
# unsafe under -j2: both run the installer against one node_modules
web/build: ; npm ci && npm run build
api/build: ; npm ci && go build ./...
```

Give the shared work its own target and depend on it:

```makefile
node_modules: package-lock.json
	npm ci
	touch $@

web/build: node_modules ; npm run build
api/build: node_modules ; go build ./...
```

`touch $@` is required because `npm ci` does not reliably update the directory's own timestamp, so
without it the target reruns on every invocation. The validator reports an installer or image-build
command in a file with no `.NOTPARALLEL`.

## Incremental builds

Make rebuilds a target when a prerequisite is newer. Two things break that:

**A recipe that rewrites its output unconditionally** makes every downstream target rebuild even when
nothing changed:

```makefile
# rewrites config.json every run
config.json: config.json.in
	envsubst < $< > $@

# writes only on a real change
config.json: config.json.in
	envsubst < $< > $@.tmp
	if cmp -s $@.tmp $@; then rm -f $@.tmp; else mv $@.tmp $@; fi
```

**An incomplete prerequisite list** makes make skip a rebuild that was needed. That is the harder
failure, because it is silent. For compiled languages the compiler can emit its own dependency list;
`native-toolchain.md` owns that mechanism.

## Intermediate files

| Directive | Effect | Floor |
|---|---|---|
| `.INTERMEDIATE: f` | make may delete `f` after the build that produced it | all |
| `.SECONDARY: f` | `f` is intermediate but is not deleted | all |
| `.SECONDARY:` (bare) | nothing is deleted as intermediate | all |
| `.PRECIOUS: f` | `f` survives an interrupt or a failed recipe | all |
| `.NOTINTERMEDIATE: f` | `f` is never treated as intermediate, even when a chained rule produced it | 4.4 |

Make treats a file produced only as a step in a rule chain as intermediate and deletes it, then rebuilds
it next time — which looks like a caching failure and is not. `.NOTINTERMEDIATE`, added in 4.4, turns
that off for a named file, for a pattern, or globally when written bare. It is the direct answer to "why
does make keep regenerating this file?".

`.PRECIOUS` and `.DELETE_ON_ERROR` point in opposite directions and `.PRECIOUS` wins for the files it
names. Use it only where a partial file is genuinely more useful than none — a long download that
supports resumption. Everywhere else, `.DELETE_ON_ERROR` from the preamble is correct.

## Cheap wins

- `:=` rather than `=` for anything computed, so `wildcard` and `$(shell …)` run once. Owned by
  `variables-guide.md`; it belongs here too as the largest single parse-time cost in most files.
- `--no-builtin-rules` and `.SUFFIXES:`, both in the preamble, so make does not search its built-in rule
  database per target. Owned by `makefile-structure.md`.
- `$(words …)`, `$(filter …)` and `$(sort …)` instead of shelling out to `wc`, `grep` and `sort`. Each
  `$(shell …)` is a fork at parse time.
- Static pattern rules rather than open pattern rules for a known list, so make does no search. Owned by
  `patterns-guide.md`.

## Debugging a slow or wrong build

```bash
make -n                       # print the commands without running them
make -d                       # every decision make makes; very verbose
make --debug=basic            # only the remake decisions
make --debug=implicit         # only the implicit-rule search
make -p                       # dump the full database, including built-in rules
make --trace                  # print each recipe line with the target it belongs to
make -W file.c target         # pretend file.c changed, and show what would rebuild
```

**GNU Make has no `--profile` flag.** A previous revision of this file taught
`make --profile=profile.log` in two places; the flag does not exist in any release, and
`make --profile=/tmp/p.log` answers `make: unrecognized option '--profile='`. To time a build, use
`time make -j$(nproc)`; to attribute time to targets, use `make --trace` with timestamps or `--debug=basic`
and read the remake decisions.

## What this file does not decide

- The preamble, `.SUFFIXES:` and includes: `makefile-structure.md`.
- Assignment operators: `variables-guide.md`.
- `.PHONY`, order-only prerequisites and standard targets: `targets-guide.md`.
- Automatic variables and pattern-rule selection: `patterns-guide.md`.
- Whether a target may retry or wait on a slow dependency: `/alaa-reliability-sla`
  (`$alaa-reliability-sla`).
- Compiler caching, distributed compilation and link-time optimisation: `native-toolchain.md`.
