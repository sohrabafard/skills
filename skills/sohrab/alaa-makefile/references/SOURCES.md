# Sources and version ledger

Read this file whenever a task says latest, current, supported, deprecated or end-of-life, and whenever
a pinned version appears in something you are about to write.

## Freshness procedure

A version written into a file goes stale silently, so every pinned value below carries the one command
that re-derives it. Run the command; do not trust the number. `scripts/validate_makefile.sh` prints the
GNU Make anchor and its re-derivation command on every run, so a routine validation also re-exposes the
claim.

## Version ledger, verified 2026-07-29

| Claim | Value on 2026-07-29 | Re-derive with |
|---|---|---|
| GNU Make current stable | **4.4.1**, released 2023-02-26 | `curl -s https://ftp.gnu.org/gnu/make/ \| grep -o 'make-[0-9][0-9.]*\.tar\.gz' \| sort -V \| tail -1` |
| GNU Make 4.4 feature floor | `.WAIT`, `.NOTPARALLEL` with prerequisites, `.NOTINTERMEDIATE`, `--shuffle`, `$(let …)`, `$(intcmp …)`, named-pipe jobserver | `make --version` locally; feature list at the [4.4 announcement](https://lists.gnu.org/archive/html/info-gnu/2022-10/msg00008.html) |
| mbake current release | **1.4.6**, released 2026-03-31 | `curl -s https://pypi.org/pypi/mbake/json \| python3 -c 'import json,sys;print(json.load(sys.stdin)["info"]["version"])'` |
| mbake canonical repository | `https://github.com/EbodShojaei/bake` | the `Repository` entry in the same PyPI JSON |
| checkmake current release | **v0.3.2**, released 2026-01-10; no longer experimental since v0.3.0 | `https://github.com/checkmake/checkmake/releases` |
| checkmake install path | `go install github.com/checkmake/checkmake/cmd/checkmake@latest` | the repository README |
| unmake current release | **0.0.27**, crate updated 2026-03-25 | `curl -s https://crates.io/api/v1/crates/unmake \| python3 -c 'import json,sys;print(json.load(sys.stdin)["crate"]["max_stable_version"])'` |

Two corrections applied in this revision, both to this file. The mbake URL previously given here was
`https://github.com/StackExchange/mbake`, which returns 404; the canonical repository is
`EbodShojaei/bake`. The checkmake URL previously given here was `https://github.com/mrtazz/checkmake`,
which now redirects; the canonical repository is `checkmake/checkmake`.

## Invocation forms, confirmed against upstream on 2026-07-29

- `mbake validate <file>` and `mbake format --check <file>` are both current subcommands. mbake's full
  subcommand set is `init`, `config`, `validate`, `format`, `setup-command`, `completions`, `update`.
  Its documented exit codes are `0` success, `1` needs formatting or validation failed, `2` error.
- `checkmake <Makefile>` accepts one or more file paths. Single-file invocation is the documented form.
- `unmake <path>` accepts a file path as well as a directory; the upstream README shows `unmake .`
  because it walks directories recursively, and the source treats a file argument directly. Exit `0`
  when nothing is found, `1` when a quirk or lint warning is found.

## Known upstream defect, reproduced here 2026-07-29

`mbake format` deletes the file's final newline, so any POSIX-conformant Makefile fails
`mbake format --check` with a `Would reformat` whose only change is that newline. Reproduce:

```bash
printf '.PHONY: all\nall:\n\t@echo hi\n' > /tmp/m.mk
mbake format --check /tmp/m.mk   # exit 1
mbake format /tmp/m.mk
mbake format --check /tmp/m.mk   # exit 0, and the trailing newline is gone
```

`scripts/validate_makefile.sh` round-trips the file and downgrades this to a note rather than a finding.
Full description in `mbake-tool.md`.

## Primary sources, in the order to consult them

- GNU Make manual: https://www.gnu.org/software/make/manual/
- GNU Make NEWS: https://git.savannah.gnu.org/cgit/make.git/tree/NEWS
- GNU Make releases: https://ftp.gnu.org/gnu/make/
- GNU Make 4.4 announcement: https://lists.gnu.org/archive/html/info-gnu/2022-10/msg00008.html
- GNU Make 4.4.1 announcement: https://lists.gnu.org/archive/html/info-gnu/2023-02/msg00011.html
- POSIX `make`: https://pubs.opengroup.org/onlinepubs/9799919799/utilities/make.html
- GNU Coding Standards, Makefile conventions: https://www.gnu.org/prep/standards/html_node/Makefile-Conventions.html
- GNU Bash manual: https://www.gnu.org/software/bash/manual/

## Validation and formatting tools

- mbake: https://github.com/EbodShojaei/bake and https://pypi.org/project/mbake/
- checkmake: https://github.com/checkmake/checkmake
- unmake: https://github.com/mcandre/unmake
- ShellCheck: https://www.shellcheck.net/
- shfmt: https://github.com/mvdan/sh/tree/master/cmd/shfmt

## Conflict resolution

1. The repository's own Makefile behaviour and the user's explicit constraints.
2. The GNU Make manual, or the POSIX `make` specification when the file declares POSIX intent.
3. The tool's own documentation for a validator's behaviour.
4. This skill's references and scripts.

## Community sources

Use community posts, Stack Overflow answers and issue comments only for concrete troubleshooting, after
the manual, the validator output and a local reproduction have been checked. They are never normative
for portability, security or style.

Applying that rule, this revision removed six statistics that the previous revision presented as
findings ("35% of developers…", "40% faster…", "60% reduction…", "40%+ in some cases", "up to 60%", and
a four-row block sourced to moldstud.com). They came from a content farm, not a study, and the skill's
own policy forbade using them as authority. The advice they were attached to is independently sound and
is retained without them. The unsourced benchmark table in `optimization-guide.md` ("45s to 3s", "3-4x",
"10x") was removed for the same reason: no methodology, no hardware, no source.
