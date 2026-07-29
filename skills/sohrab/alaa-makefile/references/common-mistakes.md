# Failure classes

Organised by what you observe, not by Make feature. Each entry gives the symptom, what it costs, the
smallest fix, and where to escalate. Every rule is owned by another file in this skill; this file
diagnoses and points.

Run `bash scripts/validate_makefile.sh <file>` first. Exit `0` is clean, `1` is findings, `2` is could
not run. Most of what follows it will name for you.

---

## A. A target reported success and did not do its work

### A1. The recipe printed a failure and make exited 0

**Symptom.** A command in the middle of a recipe prints an error, later lines still run, `make` exits 0
and CI is green.

**Cost.** A deploy that did not deploy, a migration that did not migrate, a gate that gated nothing. This
is the most expensive failure in this document because nothing reports it.

**Cause.** `.ONESHELL:` is set and `.SHELLFLAGS` does not contain `-e`. The whole recipe is one shell
invocation whose exit status is its **last** command's status.

**Smallest fix.** `.SHELLFLAGS := -eu -o pipefail -c`.

**Reproduce.** `scripts/fixtures/oneshell-swallow.mk`:
`make -f oneshell-swallow.mk deploy ; echo "exit=$?"` prints the failure and `exit=0`.

**Escalate.** `makefile-structure.md` for the preamble; `ci-entrypoint.md` for what a gate-fronting
target must do.

### A2. A recipe line begins with `-`

**Symptom.** A step fails and the target continues.

**Cost.** Identical to A1, one line at a time. The `-` prefix tells make to ignore that command's exit
status entirely.

**Smallest fix.** Delete the `-` and make the command tolerate the condition itself: `rm -f` instead of
`-rm`, `mkdir -p` instead of `-mkdir`. Where absence is genuinely acceptable, test for it:
`if docker image inspect $(IMAGE) >/dev/null 2>&1; then docker image rm $(IMAGE); fi`.

**Note.** A previous revision of this skill taught `-rm -rf $(BUILD_DIR)` as a method of error handling,
and the validator's own message recommended the `-` prefix. Both were wrong and both are removed. The
`-` prefix suppresses error reporting; it is not error control.

**Escalate.** `ci-entrypoint.md`.

### A3. `|| true` on a gate command

**Symptom.** The gate's own output shows a failure; the target passes.

**Smallest fix.** Delete `|| true`. If one specific failure is acceptable, test for that condition and
exit 0 only for it.

**Escalate.** `ci-entrypoint.md`.

### A4. Commands chained with `;` on one line

**Symptom.** `cmd-a ; cmd-b` — `cmd-a` fails, `cmd-b` runs, the line's status is `cmd-b`'s.

**Smallest fix.** `cmd-a && cmd-b`, or open the line with `set -e;`.

**Escalate.** `makefile-structure.md` for recipe line mechanics.

---

## B. Make refuses to parse the file

### B1. `*** missing separator. Stop.`

**Symptom.** Parse fails, usually at the first recipe line.

**Cause, in order of likelihood.** A recipe line indented with spaces instead of a tab; an editor
configured to expand tabs; a target line with no colon; a stray line inside a recipe that is not
tab-indented.

**Smallest fix.** Replace the leading spaces with one tab, or run `mbake format <file>`, which fixes
recipe indentation. Configure the editor: `.editorconfig` with `[Makefile]` and `indent_style = tab`;
Vim `autocmd FileType make setlocal noexpandtab`; VS Code
`"[makefile]": {"editor.insertSpaces": false}`.

**Note.** `scripts/validate_makefile.sh` distinguishes a space-indented recipe line from a legal
space-indented variable continuation. A previous revision did not, and reported
`SOURCES = main.c \` continued by four-space-indented `utils.c` as a hard error;
`scripts/fixtures/continuation.mk` is the regression test.

### B2. A command fails with a message whose bytes look correct

**Symptom.** `bash: .service-ci-kit/ci/scripts/build_image.sh: No such file or directory` for a file that
plainly exists.

**Cause.** The Makefile has CRLF line endings. Make passes the trailing carriage return to the shell as
part of the last argument.

**Smallest fix.** `sed -i $'s/\r$//' Makefile`, then add to `.gitattributes`:

```gitattributes
Makefile   text eol=lf
*.mk       text eol=lf
*.sh       text eol=lf
```

Without the `.gitattributes` entry, a Windows checkout with `core.autocrlf=true` reintroduces it on the
next clone. The validator reports any CR in the file.

### B3. `*** unterminated variable reference` or a value that vanished

**Cause.** An unmatched parenthesis in `$(…)`, or a backslash continuation with a trailing space after
it. A backslash must be the last character on the line.

---

## C. Make runs the wrong thing, or nothing

### C1. `make: 'test' is up to date.`

**Cause.** A file or directory named `test` exists and `test` is not declared in `.PHONY`.

**Cost.** On this fleet, a CI gate that silently stopped running while reporting success.

**Smallest fix.** `.PHONY: test`. Declare every target that creates no file.

**Escalate.** `targets-guide.md`.

### C2. A target rebuilds on every run

**Cause, in order of likelihood.** A directory used as a normal prerequisite instead of an order-only
one — a directory's timestamp changes when any file is written into it. A phony target used as a
prerequisite of a file target. A recipe that rewrites its output even when the content is unchanged.

**Smallest fix.** `target: sources | $(DIR)` for the first; depend on the generated file rather than on
the generator for the second; write to a temporary file and `cmp` before moving for the third.

**Escalate.** `targets-guide.md`, then `optimization-guide.md`.

### C3. A target does not rebuild when it should

**Cause.** The prerequisite list is incomplete. For compiled languages this is almost always missing
header dependencies.

**Smallest fix.** For C and C++, let the compiler emit the list; `native-toolchain.md` owns the
mechanism. For everything else, list the inputs explicitly or derive them from the generator's output
rather than from `$(wildcard …)`, which is evaluated before the generator runs.

### C4. `make -n` executes something

**Cause.** A recipe calls bare `make` instead of `$(MAKE)`. Bare `make` does not inherit `-n`, so the
sub-build runs for real during a dry run — and does not inherit `-j` either, so a parallel build
serialises.

**Smallest fix.** `$(MAKE)`.

**Escalate.** `makefile-structure.md`.

### C5. `*** Circular a <- b dependency dropped.`

**Cause.** Two targets list each other. Make drops one edge and the build order becomes arbitrary.

**Smallest fix.** Extract the shared work into a third target that both depend on.

---

## D. The value in a recipe is not the value you wrote

### D1. A shell variable in a loop is empty

**Cause.** `$file` inside a recipe is a Make variable, expanded before the shell sees the line, and it is
empty. `$$file` is what reaches the shell.

**Smallest fix.** `for f in *.sh; do shellcheck "$$f"; done`.

**Escalate.** `variables-guide.md`.

### D2. Two targets in the same run see different values

**Cause.** `VAR = $(shell …)` is re-expanded at every reference, so `date`, `git rev-parse` and `uuidgen`
all give a new answer per use.

**Smallest fix.** `VAR := $(shell …)`.

**Escalate.** `variables-guide.md`.

### D3. A command-line override had no effect

**Cause.** The Makefile assigned the variable with `:=` or `=` rather than `?=`, or a later `+=` in the
file was silently discarded by the command-line assignment.

**Smallest fix.** `?=` for anything overridable; `override VAR += …` for a contribution the file must
make regardless.

**Escalate.** `variables-guide.md`.

### D4. An undefined variable expanded to nothing and changed the command

**Symptom.** `rm -rf $(BUILD_DIR)/*` with `BUILD_DIR` unset becomes `rm -rf /*`.

**Smallest fix.** `MAKEFLAGS += --warn-undefined-variables` in the preamble turns the typo into a
warning, and `BUILD_DIR ?= $(error BUILD_DIR is not set)` turns the omission into a stopped build. The
validator reports a destructive command driven by a variable the file never defines.

**Escalate.** `variables-guide.md`, then `security-guide.md`.

---

## E. It works locally and fails on the runner, or the reverse

### E1. `source: not found`, `[[: not found`, `declare: not found`

**Cause.** `SHELL` is not set to bash, so recipes run under `/bin/sh` — `dash` on Debian, `ash` on
Alpine — where those constructs do not exist. The developer's machine has `/bin/sh` linked to bash and
does not reproduce it.

**Smallest fix.** `SHELL := bash` in the preamble, or rewrite in POSIX shell: `.` instead of `source`,
`[` instead of `[[`, no arrays, no `declare`. The validator reports bash-only constructs in a file that
has not set `SHELL`.

**Escalate.** `makefile-structure.md`; for the shell logic itself, `/alaa-bash-shell`
(`$alaa-bash-shell`).

### E2. The target passes and the pipeline fails, or the reverse

**Cause.** The target's command is not the runner's command. Either the target added a flag, or it
re-implements the gate inline, or the two have drifted since.

**Smallest fix.** `make -n <target>`, diffed against the runner's `script:` line. When they differ, the
runner is authoritative. The validator reports a recipe that re-implements a command owned by
`service-ci-kit`.

**Escalate.** `ci-entrypoint.md`; for the runner side, `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`).

### E3. A GNU-only construct fails under BSD make

**Symptom.** `.WAIT`, `$(let …)`, `$(intcmp …)`, `&:` grouped targets, `!=`, or `$(shell …)` behaving
differently.

**Smallest fix.** Decide first whether portability is a requirement, and record the decision in the
file's first-line comment. If it is, run `unmake <file>` for POSIX findings and remove the constructs; if
it is not, leave them and say so, so the next reviewer does not "fix" them away.

**Escalate.** `SOURCES.md` for the version floors.

---

## F. The build is slow

### F1. Parsing is slow before any command runs

**Cause.** `=` where `:=` belongs, so `$(wildcard …)` and `$(shell …)` re-run at every reference.

**Escalate.** `optimization-guide.md`.

### F2. `-j` does not help, or `-j` breaks the build

**Cause.** Missing prerequisites the declaration order was hiding, or two recipes writing to one shared
cache.

**Smallest fix.** `make --shuffle=random -j$(nproc)` on GNU Make 4.4+ to expose the first; a shared
prerequisite target for the second.

**Escalate.** `optimization-guide.md`.

### F3. The same file is regenerated on every build

**Cause.** Make treats a file produced only as a step in a rule chain as intermediate and deletes it.

**Smallest fix.** `.NOTINTERMEDIATE: <file>` on GNU Make 4.4+, or `.SECONDARY: <file>` on any release.

**Escalate.** `optimization-guide.md`.

---

## G. Something sensitive is in the wrong place

### G1. A credential-shaped assignment in the Makefile

**Smallest fix.** `API_TOKEN ?= $(error API_TOKEN is not set)` and read the real value from the
environment or the secret store. The validator reports this as an error.

### G2. A secret in the build log

**Cause.** A command that interpolates the secret was echoed, or the secret was passed as
`docker build --build-arg`, where it is recorded in the image's layer history.

**Escalate.** `security-guide.md` owns both; `/alaa-security-review` (`$alaa-security-review`) decides
what must fail closed.

### G3. `.EXPORT_ALL_VARIABLES:` or a bare `export`

**Cost.** Every Make variable, including any that holds a credential, reaches every subprocess.

**Smallest fix.** `export` the specific names the recipes need.

---

## Review checklist

Ordered by cost, highest first.

- [ ] `.ONESHELL:` present and `.SHELLFLAGS` contains `-e`
- [ ] No `-` prefix and no `|| true` on any recipe line that invokes a gate, an image build, a Compose
      command or `$(MAKE)`
- [ ] Every gate target's command matches the runner's command, proved by `make -n`
- [ ] No bash-only construct in a file that has not set `SHELL := bash`
- [ ] `.DELETE_ON_ERROR:` present
- [ ] Every non-file target declared in `.PHONY`
- [ ] No credential-shaped assignment; every required value fails closed with `$(error …)`
- [ ] LF line endings, and `.gitattributes` pinning them
- [ ] Tabs, not spaces, for every recipe line
- [ ] Directory prerequisites in the order-only form
- [ ] `$(MAKE)`, never bare `make`
- [ ] `:=` for everything computed
- [ ] Every target documented with a `## ` line
- [ ] `validate_makefile.sh` exits 0
