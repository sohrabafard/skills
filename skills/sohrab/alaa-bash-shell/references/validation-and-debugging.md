# Validation and Debugging

## Contents

1. Static validation order
2. Dynamic validation order
3. Debug patterns
4. Portability matrix checks
5. Common failures
6. Review checklist

## 1. Static validation order

Run checks in this order:

1. syntax check with the real shell
2. ShellCheck
3. `shfmt`
4. `checkbashisms` for `/bin/sh` targets

Useful commands:

```bash
bash -n script.sh
sh -n script.sh
dash -n script.sh
shellcheck -s bash script.sh
shellcheck -s sh script.sh
shfmt -d script.sh
checkbashisms script.sh
```

Use `scripts/validate-shell.sh` when possible to bundle the common checks.

## 2. Dynamic validation order

For a CLI script, do at least these smoke tests:

```bash
./script.sh -h
./script.sh --help
./script.sh --dry-run ...    # when supported
```

Then add representative success and failure paths.

Good extra checks:

- `env -i PATH="$PATH" ./script.sh -h`
- run with filenames containing spaces
- run with empty input
- run with missing dependencies
- run with malformed input
- run twice if idempotence matters

## 3. Debug patterns

### Lightweight tracing

For Bash:

```bash
export PS4='+${BASH_SOURCE##*/}:${LINENO}:${FUNCNAME[0]:-main}: '
set -x
```

For POSIX `sh`:

```sh
set -x
```

### Structured error messages

Prefer:

```bash
die "input file not found: ${input_file}"
```

Over:

```bash
echo "failed"
exit 1
```

### Guard complex pipelines

If a pipeline is hard to inspect, split it:

```bash
filtered=$(rg --no-heading --line-number -- 'ERROR' -- "${log_file}")
summarized=$(printf '%s\n' "${filtered}" | awk -F: '{counts[$3]++} END {for (k in counts) print k, counts[k]}')
printf '%s\n' "${summarized}"
```

Use temporary variables when they improve observability.

### Cleanup

Use `mktemp` and cleanup traps for temporary files or directories. Ensure cleanup respects the exit status.

## 4. Portability matrix checks

For a portable `/bin/sh` script:

- syntax with `sh -n`
- syntax with `dash -n` when available
- syntax with `busybox ash -n` when available
- `checkbashisms`
- ShellCheck with `-s sh`
- ShellCheck with `-s busybox` when Alpine or BusyBox is in the matrix

ShellCheck's `-s` accepts `sh`, `bash`, `dash`, `ksh`, and `busybox` in current releases; `busybox` is absent from older ones, which reject it with `Unknown shell`. Treat that message as a missing capability rather than a finding, and use the dialect that matches the interpreter the script will actually meet rather than the one on the authoring machine.

For a Bash script intended for mixed developer machines:

- syntax with `bash -n`
- ShellCheck with `-s bash`
- `shfmt`
- help smoke tests

## 5. Common failures

### Help path fails

Cause:
- help needs undeclared environment or dependencies

Fix:
- move help rendering earlier
- avoid doing work before parsing `-h` or `--help`

### `/bin/sh` script breaks on Alpine or Debian

Cause:
- hidden Bashism or GNU-only external flag

Fix:
- review `portability-and-platforms.md`
- run `checkbashisms`
- replace Bash-only syntax
- wrap GNU/BSD differences

### Pipelines hide the real error

Cause:
- failure occurs in an early stage

Fix:
- in Bash use `set -o pipefail`
- in POSIX `sh`, split the pipeline or write intermediate output to a temp file for inspection

### Quoting bug appears only with spaces or globs

Cause:
- unquoted expansion

Fix:
- quote expansions by default
- add tests with spaces, wildcard characters, and empty values

## 6. Review checklist

Before final delivery, confirm:

- correct shebang
- `-h` and `--help`
- readable control flow
- clear errors to stderr
- correct quoting
- no accidental Bashisms in `/bin/sh`
- no unnecessary external processes in hot loops
- validation results summarized honestly
