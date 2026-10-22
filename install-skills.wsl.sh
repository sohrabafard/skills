#!/usr/bin/env bash
# Install personal skill symlinks from the Linux clone; never replace existing entries.
# Source roots are read as data from install-skills.md, not evaluated as PowerShell.
set -euo pipefail

usage() {
  cat <<'HELP'
Usage: bash install-skills.wsl.sh [--dry-run | -h | --help]
Link skills from the source roots in install-skills.md into both personal agent homes.

Options:
  --dry-run   Show planned links and conflicts without changing destinations.
  -h, --help  Show this help.
Environment:
  HOME        Personal homes: $HOME/.codex/skills and $HOME/.claude/skills.
Dependencies: Linux Bash 4+, readlink, dirname, mkdir, ln; no downloads or sudo.
Exit codes: 0 completed (including reported skips), 1 setup/I/O error, 2 usage error.
Examples:
  bash install-skills.wsl.sh --dry-run
  bash install-skills.wsl.sh
HELP
}

dry_run=false
case "${1:-}" in
  -h | --help)
    usage
    exit 0
    ;;
  --dry-run) dry_run=true ;;
  '') ;;
  *)
    usage >&2
    exit 2
    ;;
esac
if (($# > 1)); then
  usage >&2
  exit 2
fi

fail() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}
[[ $(uname -s) == Linux ]] || fail 'Run this installer inside WSL/Linux.'
: "${HOME:?HOME must be set}"
repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
case "$repo_root" in /mnt/*) fail 'Run the copy in the Linux project clone, not /mnt.' ;; esac
source_document="$repo_root/install-skills.md"
[[ -f $source_document ]] || fail "Missing canonical source list: $source_document"

# Parse only the documented literal Join-Path entries. Unknown syntax fails before linking.
roots=()
in_roots=false
complete=false
# shellcheck disable=SC2016 # Match the literal PowerShell variable, not a Bash variable.
root_pattern='^[[:space:]]*\(Join-Path \$repoRoot "([^"]+)"\)[[:space:]]*$'
while IFS= read -r line || [[ -n $line ]]; do
  if ! "$in_roots"; then
    if [[ $line =~ ^[[:space:]]*\$srcRoots[[:space:]]*=[[:space:]]*@\([[:space:]]*$ ]]; then
      in_roots=true
    fi
    continue
  fi
  if [[ $line =~ ^[[:space:]]*\)[[:space:]]*$ ]]; then
    complete=true
    break
  fi
  if [[ $line =~ ^[[:space:]]*(#.*)?$ ]]; then continue; fi
  [[ $line =~ $root_pattern ]] || fail "Unsupported source-root expression: $line"
  relative=${BASH_REMATCH[1]//\\//}
  case "/$relative/" in */../* | */./*) fail 'Source roots must stay inside the clone.' ;; esac
  [[ -n $relative && $relative != /* && $relative != *:* ]] || fail 'Expected a relative source root.'
  roots+=("$repo_root/$relative")
done <"$source_document"
if ! "$complete" || ((${#roots[@]} == 0)); then
  fail 'No complete source-root list found.'
fi

shopt -s nullglob
shopt -u dotglob
declare -A planned=()
linked=0
skipped=0
conflicts=0
for source_root in "${roots[@]}"; do
  if [[ ! -d $source_root ]]; then
    printf 'WARN source root missing, skipped: %s\n' "$source_root" >&2
    continue
  fi
  for source in "$source_root"/*; do
    [[ -d $source && -f $source/SKILL.md ]] || continue
    name=${source##*/}
    expected=$(readlink -f -- "$source")
    for runtime in codex claude; do
      destination="$HOME/.$runtime/skills/$name"
      status=EXIST
      reason=''
      if [[ -n ${planned[$destination]:-} ]]; then
        actual=${planned[$destination]}
        if [[ $actual != "$expected" ]]; then reason="different target: $actual"; fi
      elif [[ -L $destination ]]; then
        actual=$(readlink -f -- "$destination" 2>/dev/null || true)
        if [[ $actual != "$expected" ]]; then
          reason="different or unresolved target: $(readlink -- "$destination")"
        fi
      elif [[ -e $destination ]]; then
        reason='existing entry is not a symlink'
      else
        status=LINK
        if "$dry_run"; then
          status=WOULD-LINK
          planned[$destination]=$expected
        else
          mkdir -p -- "$(dirname -- "$destination")"
          ln -s -- "$source" "$destination"
        fi
        linked=$((linked + 1))
      fi
      printf '%s [%s] %s\n  Source:      %s\n  Destination: %s\n' \
        "$status" "$runtime" "$name" "$source" "$destination"
      if [[ $status == EXIST ]]; then skipped=$((skipped + 1)); fi
      if [[ -n $reason ]]; then
        conflicts=$((conflicts + 1))
        printf '  WARN skipped: %s\n' "$reason" >&2
      fi
    done
  done
done
printf 'Summary: links=%s existing/skipped=%s conflicts=%s dry-run=%s\n' \
  "$linked" "$skipped" "$conflicts" "$dry_run"
