#!/usr/bin/env bash
set -euo pipefail

priority="BelowNormal"
cpu_count=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --priority) priority="$2"; shift 2 ;;
    --cpu-count) cpu_count="$2"; shift 2 ;;
    --) shift; break ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

if [[ $# -eq 0 ]]; then
  echo "Usage: run-low-priority.sh [--priority BelowNormal|Idle|Normal] [--cpu-count N] -- command [args...]" >&2
  exit 2
fi

case "$priority" in
  Normal) nice_value=0 ;;
  BelowNormal) nice_value=10 ;;
  Idle) nice_value=19 ;;
  *) echo "Invalid priority: $priority" >&2; exit 2 ;;
esac

cmd=("$@")
if [[ "$cpu_count" -gt 0 ]] && command -v taskset >/dev/null 2>&1; then
  last_cpu=$((cpu_count - 1))
  exec nice -n "$nice_value" taskset -c "0-$last_cpu" "${cmd[@]}"
fi
exec nice -n "$nice_value" "${cmd[@]}"
