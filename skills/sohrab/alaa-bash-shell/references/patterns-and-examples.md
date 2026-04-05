# Patterns and Examples

## Contents

1. Manual long-option parser
2. Safe temp directory
3. Shared library pattern
4. Structured data pattern
5. Batch processing pattern

## 1. Manual long-option parser

This is a good default for scripts that need both short and long options without depending on external `getopt`:

```bash
parse_args() {
  POSITIONAL=()

  while (($#)); do
    case "$1" in
      -h|--help)
        usage
        exit 0
        ;;
      -v|--verbose)
        VERBOSE=1
        shift
        ;;
      --debug)
        DEBUG=1
        shift
        ;;
      --dry-run)
        DRY_RUN=1
        shift
        ;;
      --)
        shift
        while (($#)); do
          POSITIONAL+=("$1")
          shift
        done
        ;;
      -*)
        die "unknown option: $1"
        ;;
      *)
        POSITIONAL+=("$1")
        shift
        ;;
    esac
  done
}
```

For POSIX `sh`, use the same `case` structure but accumulate positional arguments carefully because arrays are unavailable.

## 2. Safe temp directory

```bash
make_temp_dir() {
  temp_dir=$(mktemp -d "${TMPDIR:-/tmp}/sync-cache.XXXXXX") || return 1
}

cleanup() {
  rc=$?
  if [[ -n "${temp_dir:-}" && -d "${temp_dir}" ]]; then
    rm -rf -- "${temp_dir}"
  fi
  return "${rc}"
}

trap cleanup EXIT
```

When portability is extremely strict, verify the local `mktemp` syntax on the target platform.

## 3. Shared library pattern

Entry point:

```bash
#!/usr/bin/env bash
# shellcheck shell=bash

readonly SCRIPT_DIR=$(cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=../lib/project-common.sh
source "${SCRIPT_DIR}/../lib/project-common.sh"

main() {
  project::require_cmd jq
  project::log info "ready"
}

main "$@"
```

Library:

```bash
# shellcheck shell=bash

project::log() {
  local level=$1
  shift
  printf '[%s] %s\n' "${level}" "$*" >&2
}

project::require_cmd() {
  local tool=$1
  command -v "${tool}" >/dev/null 2>&1 || {
    printf 'missing required command: %s\n' "${tool}" >&2
    return 1
  }
}
```

## 4. Structured data pattern

Use `jq` and `yq` instead of regex:

```bash
jq -r '.items[] | select(.enabled) | .name' -- "${json_file}"
yq -r '.services[] | select(.enabled == true) | .name' -- "${yaml_file}"
```

## 5. Batch processing pattern

Portable and readable pattern for many files:

```bash
find "${root_dir}" -type f -name '*.log' -exec awk -f summarize.awk {} +
```

Developer-ergonomic pattern when `fd` is an accepted dependency:

```bash
fd -e log . "${root_dir}" -x awk -f summarize.awk
```

Prefer the portable pattern when the script must work on unfamiliar systems.
