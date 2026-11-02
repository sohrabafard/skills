#!/usr/bin/env bash
# Compatibility entrypoint; testing-strategy owns help, arguments and execution.
set -euo pipefail
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
runner="$script_dir/../../alaa-testing-strategy/scripts/run-low-priority.sh"
if [[ ! -f "$runner" ]]; then
  printf 'Missing canonical testing-strategy runner: %s. Provide a compatible alaa-testing-strategy package; no automatic installation.\n' "$runner" >&2
  exit 2
fi
exec bash "$runner" "$@"
