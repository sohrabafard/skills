# Script Contract

## Contents

1. Shebang and shell hints
2. Help contract
3. File header contract
4. Function contract
5. Variable and naming rules
6. Logging, errors, and exit codes
7. IDE-friendly hints
8. When to add common CLI flags

## 1. Shebang and shell hints

Use the shebang to declare the real interpreter.

- Bash CLI or library files:
  - `#!/usr/bin/env bash`
  - add `# shellcheck shell=bash` near the top when the shebang is not enough for tooling
- Portable POSIX shell scripts:
  - `#!/bin/sh`
  - add `# shellcheck shell=sh` when the file may be sourced, templated, or wrapped

Do not use `#!/bin/sh` for Bash code.

## 2. Help contract

Every user-facing CLI script must implement `-h` and `--help`.

The help output should include:

- usage line
- short description
- options
- arguments, if any
- environment variables, if any
- dependencies, if any
- exit codes
- at least one realistic example

Help should not require network access, user input, or external state that is unnecessary for showing usage.

Prefer help that fits this shape:

```text
Usage: sync-cache.sh [OPTIONS] SOURCE DESTINATION

Description:
  Synchronize cache metadata and report drift.

Options:
  -h, --help        Show this help and exit
  -v, --verbose     Increase log verbosity
      --debug       Enable shell tracing
      --dry-run     Print actions without changing files

Environment:
  TMPDIR            Override temp directory
  NO_COLOR          Disable ANSI colors

Dependencies:
  bash, jq

Exit codes:
  0 success
  1 runtime error
  2 usage error

Examples:
  sync-cache.sh ./input ./output
  sync-cache.sh --dry-run ./input ./output
```

## 3. File header contract

Keep the header concise and useful. A good default is:

```bash
#!/usr/bin/env bash
# shellcheck shell=bash
#
# sync-cache.sh
#
# Description:
#   Synchronize cache metadata from SOURCE to DESTINATION.
#
# Dependencies:
#   bash, jq
#
# Environment:
#   TMPDIR      Optional temp directory
#   NO_COLOR    Disable ANSI color output
#
# Exit codes:
#   0 success
#   1 runtime failure
#   2 usage error
```

Avoid decorative banners that make the file harder to scan.

## 4. Function contract

Non-trivial functions should have a short docblock immediately above them.

Use this style:

```bash
#######################################
# Read a JSON file and extract active ids.
# Arguments:
#   $1 - Path to JSON file.
# Outputs:
#   Writes one id per line to stdout.
# Returns:
#   0 on success, non-zero on failure.
#######################################
read_active_ids() {
  local json_file=$1
  jq -r '.items[] | select(.active) | .id' -- "${json_file}"
}
```

For POSIX `sh`, keep the same docblock style even though `local` is unavailable.

## 5. Variable and naming rules

Prefer predictable naming:

- functions: `lower_snake_case`
- Bash library functions: optional namespace such as `project::sync_cache`
- constants and exported environment variables: `UPPER_SNAKE_CASE`
- internal variables: descriptive lowercase names

For Bash, use declaration attributes to show intent when they genuinely help:

- `local -i` for integers
- `local -a` for indexed arrays
- `local -A` for associative arrays
- `readonly` for constants
- `export` only when a child process truly needs the variable

For POSIX `sh`, there are no standard type declarations. Document intent in names and docblocks.

## 6. Logging, errors, and exit codes

Use `printf` for messages.

Recommended exit code convention:

- `0` success
- `1` runtime or dependency failure
- `2` usage or argument error

User-facing error messages should:

- go to stderr
- name the failing argument, file, command, or assumption
- avoid vague messages like `failed` with no context

For scripts with side effects, expose `--dry-run` when it genuinely helps reviewers and operators.

## 7. IDE-friendly hints

Shell has no native cross-editor type system. Be honest about that. The most practical hints are:

- correct shebang
- `# shellcheck shell=<dialect>` directives
- `# shellcheck source=...` directives for sourced files when needed
- Bash declaration attributes like `local -a`, `local -A`, `local -i`
- consistent docblocks with argument, output, and return sections

When suppressing ShellCheck, keep the suppression narrow and explain why:

```bash
# shellcheck disable=SC2155 # Single-use local keeps the pipeline close to the data source.
local result=$(jq -r '.value' -- "${json_file}")
```

## 8. When to add common CLI flags

Add only the flags that fit the script:

- `-h`, `--help`: always for user-facing CLIs
- `--debug`: when extra trace output helps support or incident work
- `-v`, `--verbose`: when a normal run can be meaningfully quieter
- `--dry-run`: when the script mutates files, services, or remote systems
- `--version`: for public or shared tools with a maintained release notion

Do not add option clutter mechanically.
