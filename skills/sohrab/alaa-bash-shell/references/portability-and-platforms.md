# Portability and Platforms

## Contents

1. Bash vs POSIX `sh`
2. Bash-only features and portable alternatives
3. Alpine vs Debian
4. GNU vs BSD and macOS differences
5. Practical portability rules

## 1. Bash vs POSIX `sh`

Use this table to choose the shell deliberately.

| Need | Prefer |
| --- | --- |
| Arrays, associative arrays, `[[ ]]`, `mapfile`, process substitution, `coproc`, `pipefail` | Bash |
| `/bin/sh` portability, BusyBox, `dash`, init hooks, packaging scripts | POSIX `sh` |
| Minimal container with Alpine defaults | POSIX `sh` unless Bash is a declared dependency |
| Controlled Linux developer environment with richer tooling | Bash |

Do not describe a script as portable just because it happens to work once under Bash.

## 2. Bash-only features and portable alternatives

| Bash feature | Portable `sh` alternative |
| --- | --- |
| `[[ ... ]]` | `[ ... ]` plus `case` where needed |
| arrays | positional parameters, newline-delimited streams, temp files, or a fuller language |
| associative arrays | `awk`, temporary files, or `case` for small maps |
| `mapfile` / `readarray` | `while IFS= read -r line; do ...; done` |
| process substitution `< <(...)` | temp files, FIFOs, or pipeline restructuring |
| `${var^^}` / `${var,,}` | `tr` |
| `${var//x/y}` | `sed`, `awk`, or simpler parameter expansion where possible |
| `pipefail` | split the pipeline and check statuses explicitly |
| `local` | not standard in POSIX `sh`; keep functions small and names explicit |

## 3. Alpine vs Debian

### Alpine

Assume these constraints unless the user says otherwise:

- the default shell is BusyBox `ash`
- many common utilities come from BusyBox
- BusyBox tools usually expose fewer flags than their GNU counterparts

Design implications:

- do not assume Bash is installed
- do not assume GNU `sed`, `grep`, `find`, `xargs`, `date`, or `stat`
- prefer POSIX shell and POSIX utility flags when Alpine compatibility matters
- test `/bin/sh` scripts with `busybox ash` when available

### Debian

Assume these constraints unless the user says otherwise:

- `/bin/sh` is commonly `dash`
- the system usually provides GNU userland tools

Design implications:

- `/bin/sh` scripts must avoid Bash syntax
- GNU flags may work on Debian and still break on Alpine or macOS
- `checkbashisms` is especially useful for `/bin/sh` review

## 4. GNU vs BSD and macOS differences

Common pain points:

| Command | GNU behavior often assumed | Safer cross-platform approach |
| --- | --- | --- |
| `sed -i` | GNU accepts `-i` with no backup suffix | write to a temp file and `mv`, or wrap GNU vs BSD syntax |
| `date` | GNU `date -d` | avoid shell date parsing, or wrap per platform, or use another language |
| `readlink -f` | available on GNU systems | prefer `realpath` when available, otherwise provide a fallback |
| `stat` | GNU `stat -c` | wrap GNU vs BSD forms |
| `grep -P` | often absent outside GNU builds | prefer `grep -E`, `awk`, or `perl` |
| `xargs -r` | GNU-only | do not depend on it for portability |
| `find -print0` / `xargs -0` | common but not POSIX | use when the dependency is acceptable; otherwise prefer `find -exec ... +` or a carefully designed loop |

macOS note:

- the default interactive shell is `zsh`, not Bash
- do not confuse the user's interactive shell with the interpreter declared by a script shebang
- do not assume a modern Bash is already installed

## 5. Practical portability rules

- For Bash scripts, use `#!/usr/bin/env bash`.
- For POSIX shell scripts, use `#!/bin/sh`.
- Prefer `getopts` or a manual `case` parser over external `getopt`.
- Prefer `printf` over `echo -e`.
- Prefer `command -v tool >/dev/null 2>&1` to check dependencies.
- Prefer `find ... -exec cmd {} +` over newline-unsafe `for file in $(find ...)`.
- Prefer `awk` or `jq` to complex nested shell loops.
- Document every non-portable external dependency in help text and file headers.
