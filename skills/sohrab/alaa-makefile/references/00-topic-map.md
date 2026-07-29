# Alaa Makefile topic map

The only router in this skill. Open the one file whose condition matches, then stop. Each rule below is
owned by exactly one file; if two files seem to cover a rule, the owner named here is correct and the
other file is out of date.

## Front a command that something else already runs

- A target must run a CI gate the way the runner runs it, and its verdict must match:
  `ci-entrypoint.md` — **owner** of gate fronting, exit-status propagation, the `make -n` diff, and what
  a target prints when it fails.
- A target fronts `docker compose`, an image build or a container lifecycle:
  `compose-and-container-targets.md` — **owner** of container-target naming, prerequisites and cleanup.

## Write or redesign a Makefile

- File layout, section order, the hardening preamble, `include` and modular `.mk`:
  `makefile-structure.md` — **owner** of the preamble, `.DELETE_ON_ERROR`, `.SUFFIXES`, includes and the
  recursive-versus-non-recursive decision.
- Variable assignment, override precedence, the environment boundary:
  `variables-guide.md` — **owner** of `=`, `:=`, `?=`, `+=`, `!=`, `export`, `override` and `$(shell)`
  caching.
- Standard targets, `.PHONY`, prerequisites, order-only prerequisites, the help target:
  `targets-guide.md` — **owner** of `.PHONY` rationale, the GNU standard-target set and order-only form.
- Pattern rules, static pattern rules, automatic variables:
  `patterns-guide.md` — **owner** of `$@ $< $^ $* $(@D)` and of pattern-rule selection.

## Review, harden or speed up an existing Makefile

- A symptom in hand and the fix unknown:
  `common-mistakes.md` — organised as symptom, consequence, smallest fix, escalation.
- Secrets, injection, path traversal, temporary files, downloads:
  `security-guide.md` — read this first in any review lane.
- Parallel safety, incremental builds, build caches:
  `optimization-guide.md` — **owner** of `-j`, `.NOTPARALLEL`, `.WAIT`, `--shuffle`, `.INTERMEDIATE`,
  `.SECONDARY`, `.PRECIOUS` and `.NOTINTERMEDIATE`.

## Run the tooling

- What mbake asserts, how it is invoked, its exit codes and its known false positives:
  `mbake-tool.md` — **owner** of everything mbake. This file is about mbake, the Python Makefile
  formatter this skill installs; it has nothing to do with Docker Buildx Bake.
- The bundled scripts: `../scripts/validate_makefile.sh`, `../scripts/generate_makefile_template.sh`,
  `../scripts/add_standard_targets.sh`. Each carries `--help` and `--self-test`; read `--help` rather
  than a reference file.

## Compile native code with Make

- C, C++ or Java compilation, header dependency generation, ccache, VPATH, pkg-config, precompiled
  headers, LTO: `native-toolchain.md`. Nothing on this fleet currently compiles native code; open this
  file only when a repository genuinely does.

## Check a version claim

- `SOURCES.md` — the provenance ledger. Every pinned version there carries the command that re-derives
  it. Read it whenever a task says latest, current, supported or end-of-life.

## Working rule

Open one file. If it points at another file for a rule, follow the pointer rather than reasoning from
the first file's summary, because only the owner is kept current.
