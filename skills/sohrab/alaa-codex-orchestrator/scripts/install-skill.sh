#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source_dir="$(cd -- "$script_dir/.." && pwd)"
target_dir="${1:-$HOME/.codex/skills/alaa-codex-orchestrator}"
mkdir -p "$(dirname "$target_dir")"

if [[ "$source_dir" == "$(cd -- "$target_dir" 2>/dev/null && pwd || true)" ]]; then
  "$source_dir/scripts/install-agents.sh"
  exit 0
fi

staging="$target_dir.tmp.$$.$RANDOM"
backup=""
timestamp="$(date +%Y%m%d-%H%M%S)"
trap 'rm -rf "$staging" 2>/dev/null || true' EXIT
cp -R "$source_dir" "$staging"
python3 "$staging/scripts/validate_pack.py"

if [[ -e "$target_dir" ]]; then
  backup_root="$(dirname "$target_dir")/.alaa-codex-orchestrator-backups"
  mkdir -p "$backup_root"
  backup="$backup_root/$timestamp"
  mv "$target_dir" "$backup"
fi

if ! mv "$staging" "$target_dir"; then
  if [[ -n "$backup" && ! -e "$target_dir" ]]; then mv "$backup" "$target_dir"; fi
  exit 1
fi
"$target_dir/scripts/install-agents.sh"
printf '{"Status":"OK","SkillDirectory":"%s","PreviousSkillBackup":"%s"}\n' "$target_dir" "$backup"
