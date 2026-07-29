# mbake

**This file is about mbake, the Python Makefile formatter and linter that this skill installs and runs.
It has nothing to do with Docker Buildx Bake.** The previous filename, `bake-tool.md`, invited that
confusion; the content never contained a single `buildx` token. Buildx Bake belongs to
`/alaa-docker-production` (`$alaa-docker-production`).

**Owner of:** what mbake asserts, how it is invoked, its exit codes, its configuration and its known
false positives.

## Version, verified 2026-07-29

| Fact | Value | Re-derive |
|---|---|---|
| Current release | 1.4.6, published 2026-03-31 | `curl -s https://pypi.org/pypi/mbake/json \| python3 -c 'import json,sys;print(json.load(sys.stdin)["info"]["version"])'` |
| Repository | `https://github.com/EbodShojaei/bake` | the `Repository` project URL in the same JSON |
| Python floor | 3.9 | `requires_python` in the same JSON |

The distribution is named `mbake` on PyPI and the repository is named `bake`; both are correct and they
are the same project.

## What it decides

mbake decides **Makefile formatting**, and it validates syntax by running GNU make in dry-run mode. It
does not decide whether a target is correct, whether a recipe propagates a verdict, or whether a command
belongs in a Makefile at all. Those are this skill's own checks in `scripts/validate_makefile.sh`.

What `mbake format` changes:

- converts space-indented recipe lines to tabs
- normalises spacing around `=` and after `:`
- removes trailing whitespace
- normalises backslash line continuations
- detects targets that create no file and inserts or groups `.PHONY` declarations

## Invocation

```bash
pip install mbake

mbake format --check Makefile     # report; change nothing. The CI form.
mbake format --diff Makefile      # show what would change
mbake format Makefile             # apply
mbake format --backup Makefile    # apply, leaving Makefile.bak
mbake validate Makefile           # syntax check via GNU make --dry-run
mbake --version
```

Subcommands in 1.4.6: `init`, `config`, `validate`, `format`, `setup-command`, `completions`, `update`.

Documented exit codes: `0` success, `1` needs formatting or validation failed, `2` error. Note that this
is **not** the exit-code contract of this skill's own scripts, where `1` is findings and `2` is could not
run; when wrapping mbake in a gate, translate rather than pass through.

## How this skill runs it

`scripts/validate_makefile.sh` creates a virtual environment under `TMPDIR`, installs mbake into it, runs
`mbake validate` and `mbake format --check`, and deletes the environment on exit. That costs roughly
20-40 seconds and needs network access, so two escapes exist:

```bash
bash scripts/validate_makefile.sh --no-venv Makefile              # use mbake from PATH
MBAKE_BIN=/usr/local/bin/mbake bash scripts/validate_makefile.sh --no-venv Makefile
bash scripts/validate_makefile.sh --skip-mbake Makefile           # native checks only
```

On a prepared CI image, install mbake in the image and always pass `--no-venv`.

## Known false positives

### 1. `mbake format` deletes the file's final newline

Reproduced against 1.4.6 on 2026-07-29:

```console
$ printf '.PHONY: all\nall:\n\t@echo hi\n' > /tmp/m.mk
$ mbake format --check /tmp/m.mk ; echo "exit=$?"
Would reformat: /tmp/m.mk
exit=1
$ mbake format /tmp/m.mk >/dev/null
$ od -c /tmp/m.mk | tail -2
0000020  \n  \t   @   e   c   h   o       h   i
$ mbake format --check /tmp/m.mk ; echo "exit=$?"
exit=0
```

Every POSIX-conformant Makefile — that is, every text file that ends with a newline — therefore fails
`mbake format --check`, which makes bare `mbake format --check` unusable as a CI gate. Do not "fix" it by
stripping the newline from your Makefiles.

`scripts/validate_makefile.sh` handles this: when `format --check` reports `Would reformat`, it copies the
file to `TMPDIR`, formats the copy, and compares the two with a normalised trailing newline. If the
newline is the only difference, it reports a note and the exit code stays 0. Anything else is a warning.

### 2. Unknown special targets

mbake reports `Error: Unknown special target '.DELETE_ON_ERROR'` and the same for `.SUFFIXES`,
`.ONESHELL` and `.POSIX`. All four are valid GNU Make special targets and all four are required or
permitted by this skill's preamble. `validate_makefile.sh` filters these messages out before deciding.

### 3. `format --check` and `format` disagree

Some `format --check` messages describe changes that `format` does not make. When the two disagree,
`mbake format --diff` is the authority: it prints the actual change set.

## Configuration

`mbake init` writes `~/.bake.toml`; a `.bake.toml` in the working directory overrides it, and built-in
defaults are the fallback.

| Option | Default | Effect |
|---|---|---|
| `space_around_assignment` | `true` | `VAR = value` rather than `VAR=value` |
| `space_after_colon` | `true` | `target: prereq` rather than `target:prereq` |
| `normalize_line_continuations` | `true` | clean up backslash continuations |
| `remove_trailing_whitespace` | `true` | strip end-of-line spaces |
| `fix_missing_recipe_tabs` | `true` | convert space-indented recipe lines to tabs |
| `auto_insert_phony_declarations` | `true` | add `.PHONY` for targets that create no file |
| `group_phony_declarations` | `true` | combine several `.PHONY` lines into one |
| `phony_at_top` | `false` | place `.PHONY` at the top of the file |

Commit `.bake.toml` so every developer and the runner format identically. Leave
`fix_missing_recipe_tabs` on: it is the one option that fixes a defect rather than a style.

Suppress formatting for a region that must keep its shape:

```makefile
# bake-format off
LEGACY   =    value
# bake-format on
```

## The other two linters

Both are optional in `validate_makefile.sh`; it reports their absence as a note and continues.

**checkmake** — v0.3.2, released 2026-01-10, and no longer marked experimental since v0.3.0. It checks
rules mbake does not: a missing `all` or `test` target, a target that should be phony, a maximum body
length. Install and run:

```bash
go install github.com/checkmake/checkmake/cmd/checkmake@latest
checkmake Makefile
checkmake list-rules
checkmake --config checkmake.ini Makefile
```

**unmake** — 0.0.27, crate updated 2026-03-25. A POSIX portability linter. It accepts a directory, which
it walks recursively, and a single file path:

```bash
unmake .
unmake Makefile
```

Exit `0` when nothing is found, `1` when a quirk or lint warning is found. Its findings are only
actionable when the file has declared portability as a requirement; on a GNU-only Makefile they are
noise. `common-mistakes.md` entry E3 covers that decision.

## What this file does not decide

- Whether a Makefile's formatting findings are blocking: `common-mistakes.md` and the body's blocking-
  defect list.
- Docker Buildx Bake, HCL bake files, and image build configuration: `/alaa-docker-production`
  (`$alaa-docker-production`).
- How a formatting gate is expressed on a runner: `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`).
- Editor configuration. Put `indent_style = tab` for `[Makefile]` in the repository's `.editorconfig`
  and let each developer's editor read it, rather than documenting per-editor settings here.
