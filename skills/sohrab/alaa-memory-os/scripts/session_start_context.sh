#!/usr/bin/env bash
# shellcheck shell=bash
# session_start_context.sh - Claude Code SessionStart hook.
#
# Exempt from the checker exit contract: SessionStart is context-only and cannot
# block, so this hook always exits 0. Stdout is added to the session context.
# Keep it fast; it runs on every session. See references/checkers-and-hooks.md.
#
# It counts unresolved drift records in the REPOSITORY registry, not in the memory
# store (see references/drift-management.md). A missing or unreadable registry is
# reported as unobserved, never as zero.

usage() {
  cat <<'USAGE'
Usage: session_start_context.sh [--drift-dir DIR] [--repo-root DIR]

Emit conditional owner pointers and the unresolved drift-record count for a
SessionStart hook.

Options:
  --drift-dir DIR   drift registry, relative to the repo root (default: docs/drift);
                    an empty or absolute value is rejected and reported as unobserved
  --repo-root DIR   repository root (default: current directory)
  -h, --help        show this help and exit

Dependencies: bash, find, grep
Exit codes: 0 always.

Example:
  bash session_start_context.sh --repo-root "$PWD"
USAGE
}

drift_dir="docs/drift"
repo_root=""
while [ "$#" -gt 0 ]; do
  case "$1" in
  -h | --help)
    usage
    exit 0
    ;;
  --drift-dir)
    drift_dir="${2:-}"
    shift 2 || shift
    ;;
  --repo-root)
    repo_root="${2:-}"
    shift 2 || shift
    ;;
  *) shift ;;
  esac
done
[ -n "$repo_root" ] || repo_root="$PWD"

# Prints the number of open records, or -1 when the scan cannot establish a count.
count_open_drift() {
  local dir=$1 listing file open=0 rc
  [ -d "$dir" ] || {
    echo -1
    return
  }
  listing=$(find "$dir" -type f -name '*.md' 2>/dev/null) || {
    echo -1
    return
  }
  while IFS= read -r file; do
    [ -n "$file" ] || continue
    grep -Eq '^drift_status:[[:space:]]*(open|analyzed|decided|fixing)[[:space:]]*$' -- "$file" 2>/dev/null
    rc=$?
    if [ "$rc" -eq 0 ]; then
      open=$((open + 1))
    elif [ "$rc" -ne 1 ]; then
      echo -1
      return
    fi
  done <<<"$listing"
  echo "$open"
}

# An empty or absolute value would scan the whole repository root or an outside tree.
case "$drift_dir" in
"" | /*) open_count=-1 ;;
*) open_count=$(count_open_drift "$repo_root/$drift_dir") ;;
esac

# The condition tests the observed count, not command success: announcing possible
# drift on a zero count trains the reader to ignore the line.
drift_line="- Repository drift registry observation unavailable."
if [ "$open_count" -gt 0 ] 2>/dev/null; then
  drift_line="- $open_count unresolved repository drift record(s). When an affected contract is in scope, read /alaa-memory-os references/drift-management.md and the records."
elif [ "$open_count" -eq 0 ] 2>/dev/null; then
  drift_line="- No unresolved records observed in the repository drift registry."
fi

cat <<OUT
Alaa conditional owners:
- For recall, capability ownership, durable writes or source disagreement, load /alaa-memory-os and its selected adapter.
- For active task continuity or compaction, load /alaa-workflow.
$drift_line
OUT
exit 0
