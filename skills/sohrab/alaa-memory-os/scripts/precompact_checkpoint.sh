#!/usr/bin/env bash
# shellcheck shell=bash
# precompact_checkpoint.sh - nonwriting Claude Code PreCompact hook.
#
# Reads no payload, transcript, environment, git or vault content, and writes
# nothing. Always exits 0. Current Claude Code discards PreCompact
# systemMessage and continue, so this output guarantees no context injection.
# See references/checkers-and-hooks.md for the hook protocol.

case "${1:-}" in
-h | --help)
  cat <<'USAGE'
Usage: precompact_checkpoint.sh

Print a compatibility JSON pointer to /alaa-workflow for a PreCompact hook.
Reads and writes nothing. Exit codes: 0 always.
Example: bash precompact_checkpoint.sh
USAGE
  exit 0
  ;;
esac

printf '%s\n' '{"systemMessage":"Before active-task compaction, use /alaa-workflow for its checkpoint and handoff.","continue":true}'
exit 0
