#!/usr/bin/env bash
# Install personal skill symlinks from the Linux clone; never replace existing entries.
# Source roots are read as data from install-skills.md and never evaluated.
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
  NO_COLOR    Any non-empty value disables ANSI colors.
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

use_color() {
  local stream=$1
  [[ -z ${NO_COLOR:-} && ${TERM:-} != dumb ]] || return 1
  case "$stream" in
    stdout) [[ -t 1 ]] ;;
    stderr) [[ -t 2 ]] ;;
    *) return 1 ;;
  esac
}

print_status() {
  local status=$1 runtime=$2 name=$3 color='' runtime_color=''
  if use_color stdout; then
    case "$status" in
      LINK) color=$'\033[1;32m' ;;
      WOULD-LINK) color=$'\033[1;36m' ;;
      EXIST) color=$'\033[1;90m' ;;
    esac
    case "$runtime" in
      codex) runtime_color=$'\033[1;34m' ;;
      claude) runtime_color=$'\033[1;35m' ;;
    esac
    printf '%s%-10s\033[0m  %s[%s]\033[0m  %s\n' \
      "$color" "$status" "$runtime_color" "$runtime" "$name"
  else
    printf '%-10s  [%s]  %s\n' "$status" "$runtime" "$name"
  fi
}
[[ $(uname -s) == Linux ]] || fail 'Run this installer inside WSL/Linux.'
: "${HOME:?HOME must be set}"
repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
case "$repo_root" in /mnt/*) fail 'Run the copy in the Linux project clone, not /mnt.' ;; esac
source_document="$repo_root/install-skills.md"
[[ -f $source_document ]] || fail "Missing canonical source list: $source_document"

# Parse only the "## Source roots" text block. Each entry is one double-quoted relative path.
# Any other non-comment line fails before linking.
roots=()
stage=seek # seek -> heading -> block
complete=false
root_pattern='^"([^"]+)"$'
while IFS= read -r line || [[ -n $line ]]; do
  case "$stage" in
    seek) [[ $line == '## Source roots' ]] && stage=heading ;;
    heading) [[ $line == '```text' ]] && stage=block ;;
    block)
      if [[ $line == '```' ]]; then
        complete=true
        break
      fi
      if [[ $line =~ ^(#.*)?$ ]]; then continue; fi
      [[ $line =~ $root_pattern ]] || fail "Unsupported source-root line: $line"
      relative=${BASH_REMATCH[1]}
      case "/$relative/" in */../* | */./*) fail 'Source roots must stay inside the clone.' ;; esac
      [[ $relative != /* && $relative != *:* && $relative != *\\* ]] || fail 'Expected a relative source root.'
      roots+=("$repo_root/$relative")
      ;;
  esac
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
printf 'Skill links\n============\n'
for source_root in "${roots[@]}"; do
  if [[ ! -d $source_root ]]; then
    if use_color stderr; then
      printf '\033[1;33mWARN\033[0m source root missing, skipped: %s\n' "$source_root" >&2
    else
      printf 'WARN source root missing, skipped: %s\n' "$source_root" >&2
    fi
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
      print_status "$status" "$runtime" "$name"
      printf '  Source:      %s\n  Destination: %s\n' "$source" "$destination"
      if [[ $status == EXIST ]]; then skipped=$((skipped + 1)); fi
      if [[ -n $reason ]]; then
        conflicts=$((conflicts + 1))
        if use_color stderr; then
          printf '  \033[1;33mWARN\033[0m skipped: %s\n' "$reason" >&2
        else
          printf '  WARN skipped: %s\n' "$reason" >&2
        fi
      fi
    done
  done
done
printf '\nSummary\n=======\nLinks: %s  Existing/skipped: %s  Conflicts: %s  Dry run: %s\n' \
  "$linked" "$skipped" "$conflicts" "$dry_run"
