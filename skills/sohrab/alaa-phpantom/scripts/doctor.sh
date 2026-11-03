#!/usr/bin/env bash
# Fast, read-only local environment sanity check; no auto installation.
set -u
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
PROJECT="${1:-$PWD}"
printf 'PHPantom skill source: %s\n' "$ROOT"
printf 'Project: %s\n' "$PROJECT"
if [[ -f "$ROOT/.claude-plugin/plugin.json" && -f "$ROOT/.lsp.json" && -f "$ROOT/hooks/hooks.json" && -f "$ROOT/SKILL.md" ]]; then
  echo 'Manifest, LSP, hook and skill: present'
else
  echo 'ERROR: required plugin files missing' >&2
  exit 1
fi
if [[ -f "$PROJECT/composer.json" ]]; then echo 'Composer root: yes'; else echo 'Composer root: no (check project path)'; fi
if command -v php >/dev/null 2>&1; then
  php -v | head -n 1
else
  echo 'php -l hook: unavailable (no PHP CLI on PATH; hook skips silently)'
fi
if /home/sohrab/.local/bin/phpantom_lsp --version; then
  echo 'PHPantom binary: available'
else
  echo 'PHPantom binary: unavailable (configure PHPANTOM_SERVER_PATH)' >&2
  exit 1
fi
