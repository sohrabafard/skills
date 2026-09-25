#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source_dir="$(cd -- "$script_dir/.." && pwd)"
target_dir="${1:-$HOME/.codex/skills/alaa-codex-orchestrator}"
policy_root="${2:-$(dirname "$source_dir")/alaa-prompting-guide}"
agent_target_dir="${3:-$HOME/.codex/agents}"
python3 -B "$source_dir/scripts/validate_pack.py" --policy-root "$policy_root"
mkdir -p "$(dirname "$target_dir")"

if [[ "$source_dir" == "$(cd -- "$target_dir" 2>/dev/null && pwd || true)" ]]; then
  "$source_dir/scripts/install-agents.sh" "$source_dir/agents" "$agent_target_dir" "$policy_root"
  exit 0
fi

staging="$target_dir.tmp.$$.$RANDOM"
# The previous directory is moved aside only so a failed swap can be undone; it is removed on
# success, so no copy of a prior version is retained.
replaced=""
trap 'rm -rf "$staging" 2>/dev/null || true' EXIT
cp -R "$source_dir" "$staging"
python3 -B "$staging/scripts/validate_pack.py" --policy-root "$policy_root"

if [[ -e "$target_dir" ]]; then
  replaced="$target_dir.replaced.$$.$RANDOM"
  mv "$target_dir" "$replaced"
fi

if ! mv "$staging" "$target_dir"; then
  if [[ -n "$replaced" && ! -e "$target_dir" ]]; then mv "$replaced" "$target_dir"; fi
  exit 1
fi
if [[ -n "$replaced" ]]; then rm -rf -- "$replaced"; fi
"$target_dir/scripts/install-agents.sh" "$target_dir/agents" "$agent_target_dir" "$policy_root"
printf '{"Status":"OK","SkillDirectory":"%s"}\n' "$target_dir"
