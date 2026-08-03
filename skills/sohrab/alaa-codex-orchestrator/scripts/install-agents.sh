#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source_dir="${1:-$(cd -- "$script_dir/.." && pwd)/agents}"
target_dir="${2:-$HOME/.codex/agents}"

if command -v python3 >/dev/null 2>&1; then
  python_cmd=(python3)
elif command -v python >/dev/null 2>&1; then
  python_cmd=(python)
else
  echo "Python 3 is required to validate agent grants before installation" >&2
  exit 2
fi

mkdir -p "$target_dir"
target_dir="$(cd -- "$target_dir" && pwd)"

lock_dir="$target_dir/.alaa-codex-orchestrator.install.lock"
if ! mkdir "$lock_dir" 2>/dev/null; then
  echo "Another Alaa agent installation is active: $lock_dir" >&2
  exit 2
fi
materialized_dir="$target_dir/.alaa-codex-orchestrator.materialized.$$.$RANDOM"
cleanup() {
  if [[ "$materialized_dir" == "$target_dir"/.alaa-codex-orchestrator.materialized.* ]]; then
    rm -rf -- "$materialized_dir"
  fi
  rmdir "$lock_dir" 2>/dev/null || true
}
trap cleanup EXIT

"${python_cmd[@]}" "$script_dir/check_agent_grants.py" --materialize "$source_dir" "$materialized_dir" || {
  code=$?
  echo "Agent grant materialization failed with exit code $code" >&2
  exit "$code"
}

mapfile -t files < <(find "$materialized_dir" -maxdepth 1 -type f -name '*.toml' -print | sort)
if [[ ${#files[@]} -eq 0 ]]; then
  echo "No agent TOML files found in: $source_dir" >&2
  exit 1
fi

changed=0
unchanged=0
timestamp="$(date +%Y%m%d-%H%M%S)"
backup_dir=""

for src in "${files[@]}"; do
  name="$(basename "$src")"
  dst="$target_dir/$name"
  if [[ -f "$dst" ]] && cmp -s "$src" "$dst"; then
    unchanged=$((unchanged + 1))
    continue
  fi
  if [[ -f "$dst" ]]; then
    if [[ -z "$backup_dir" ]]; then
      backup_dir="$target_dir/.alaa-codex-orchestrator-backups/$timestamp"
      mkdir -p "$backup_dir"
    fi
    cp -p "$dst" "$backup_dir/$name"
  fi
  tmp="$dst.tmp.$$.$RANDOM"
  cp "$src" "$tmp"
  chmod 600 "$tmp" 2>/dev/null || true
  mv -f "$tmp" "$dst"
  changed=$((changed + 1))
done

cp "$materialized_dir/.alaa-codex-orchestrator.mcp-inventory" \
  "$target_dir/.alaa-codex-orchestrator.mcp-inventory"

version_file="$(cd -- "$script_dir/.." && pwd)/VERSION"
if [[ -f "$version_file" ]]; then
  cp "$version_file" "$target_dir/.alaa-codex-orchestrator.version"
fi

printf '{"Status":"OK","InstalledOrUpdated":%d,"AlreadyCurrent":%d,"TargetDirectory":"%s","BackupDirectory":"%s"}\n' \
  "$changed" "$unchanged" "$target_dir" "$backup_dir"
