#!/usr/bin/env bash
# phase-check.sh — read the alaa-go-chi execution scope phase from repository truth.
#
# Owned by the alaa-go-chi-development skill, references/05-phase-and-source-truth.md.
# Read-only, offline. In normal operation it writes nothing and opens no network
# connection. --self-test creates one temporary directory under $TMPDIR, uses it,
# and removes it; it touches nothing else.

set -u

VERSION="1.0.0"

# Tokens that look like a phase name but are not one. Extend only with a comment
# saying why the token is not a phase.
IGNORE_RE='NOT_ASSESSED_KIT_FIRST|NEEDS_CONFIRMATION|NOT_ASSESSED|DO_NOT_EDIT'

usage() {
  cat <<'HELPTEXT'
phase-check.sh — read the alaa-go-chi execution scope phase from repository truth.

USAGE
  phase-check.sh <kit-repo-root>
  phase-check.sh --self-test
  phase-check.sh --help

WHAT IT READS (three authority locations, all inside <kit-repo-root>)
  L1  docs/CONSUMERS.md                              the execution-scope banner
  L2  AGENTS.md, CONSTITUTION.md, GOVERNANCE.md      the binding phase statements
  L3  docs/change-requests/YYYY-MM-DD-<slug>-scope.md   the newest scope decision
      record, selected by filename date (lexicographic sort on the date prefix)

EXTRACTION RULES (deliberately explicit, so a reading can be reproduced by hand)
  Scope-record citation: any match of
      change-requests/YYYY-MM-DD-<kebab-slug>-scope.md
  Phase name: an ALL-CAPS underscore token inside backticks, on a line that also
  contains "phase", "scope", or "activat" (case-insensitive), excluding the
  documented non-phase tokens: NOT_ASSESSED_KIT_FIRST, NEEDS_CONFIRMATION,
  NOT_ASSESSED, DO_NOT_EDIT.
  L3 contributes its own filename as its citation; a scope record does not need
  to cite itself.

EXIT CODES AND WHAT EACH ONE OBLIGES YOU TO DO
  0  Agreement. One scope record, one phase name. Use the printed phase name as
     the key into the capability matrix in references/05-phase-and-source-truth.md.
     If the printed name is not a row in that matrix, treat it as unrecognised and
     stop, exactly as exit 3 requires.
  2  Usage error, or <kit-repo-root> is not an alaa-go-chi checkout. Fix the
     invocation. Do not proceed on an assumed phase.
  3  Divergence. The three locations do not agree on one scope record, or they
     name more than one phase. Stop. Hold no consumer capability. Report both
     readings verbatim, file the disagreement as drift, and ask the project owner
     which record governs. Do not pick a side.
  4  A single scope record is agreed, but no location names a phase. Stop and
     treat the phase as unrecognised: hold no consumer capability, report the
     record path, and ask the owner to name the phase in the record.
  5  No scope record matching the required path shape was found. Stop. The phase
     is undetermined; hold no consumer capability.
  1  Internal failure (a location could not be read). Report the failure; do not
     infer a phase from a partial read.

EXAMPLES
  phase-check.sh /repos/alaa-go-chi
  phase-check.sh --self-test
HELPTEXT
}

# ---------------------------------------------------------------- extraction --

cite_refs() { # $1 = file
  [ -r "$1" ] || return 0
  grep -oE 'change-requests/[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9][a-z0-9-]*-scope\.md' "$1" 2>/dev/null \
    | sed 's#.*/##'
}

phase_tokens() { # $1 = file
  [ -r "$1" ] || return 0
  grep -iE 'phase|scope|activat' "$1" 2>/dev/null \
    | grep -oE '`[A-Z][A-Z0-9]*(_[A-Z0-9]+)+`' \
    | tr -d '`' \
    | grep -vxE "$IGNORE_RE"
}

newest_scope_record() { # $1 = repo root; prints basename or nothing
  local d="$1/docs/change-requests"
  [ -d "$d" ] || return 0
  ls -1 "$d" 2>/dev/null \
    | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9][a-z0-9-]*-scope\.md$' \
    | sort \
    | tail -n 1
}

# ------------------------------------------------------------------- reading --

run_check() { # $1 = repo root
  local root="$1"

  if [ ! -d "$root" ]; then
    printf 'phase-check: not a directory: %s\n' "$root" >&2
    return 2
  fi
  if [ ! -d "$root/docs" ] || { [ ! -f "$root/AGENTS.md" ] && [ ! -f "$root/CONSTITUTION.md" ]; }; then
    printf 'phase-check: %s does not look like an alaa-go-chi checkout (need docs/ and AGENTS.md or CONSTITUTION.md)\n' "$root" >&2
    return 2
  fi

  local l1_file="$root/docs/CONSUMERS.md"
  local l2_files="$root/AGENTS.md $root/CONSTITUTION.md $root/GOVERNANCE.md"

  local l1_refs l2_refs l3_record
  l1_refs="$(cite_refs "$l1_file" | sort -u)"
  l2_refs="$(for f in $l2_files; do cite_refs "$f"; done | sort -u)"
  l3_record="$(newest_scope_record "$root")"

  local l1_phase l2_phase l3_phase
  l1_phase="$(phase_tokens "$l1_file" | sort -u)"
  l2_phase="$(for f in $l2_files; do phase_tokens "$f"; done | sort -u)"
  l3_phase=""
  [ -n "$l3_record" ] && l3_phase="$(phase_tokens "$root/docs/change-requests/$l3_record" | sort -u)"

  printf 'phase-check %s — repo: %s\n' "$VERSION" "$root"
  printf '  L1 docs/CONSUMERS.md          cites: %s | names: %s\n' "${l1_refs:-<none>}" "${l1_phase:-<none>}"
  printf '  L2 AGENTS/CONSTITUTION/GOV    cites: %s | names: %s\n' "${l2_refs:-<none>}" "${l2_phase:-<none>}"
  printf '  L3 newest scope record        file:  %s | names: %s\n' "${l3_record:-<none>}" "${l3_phase:-<none>}"

  if [ -z "$l3_record" ]; then
    printf 'RESULT: no-scope-record — no docs/change-requests/YYYY-MM-DD-<slug>-scope.md exists.\n'
    return 5
  fi

  local all_refs
  all_refs="$(printf '%s\n%s\n%s\n' "$l1_refs" "$l2_refs" "$l3_record" | grep -v '^$' | sort -u)"
  local ref_count
  ref_count="$(printf '%s\n' "$all_refs" | grep -c . )"

  if [ -z "$l1_refs" ] || [ -z "$l2_refs" ]; then
    printf 'RESULT: divergence — a required location cites no scope record.\n'
    return 3
  fi
  if [ "$ref_count" -ne 1 ]; then
    printf 'RESULT: divergence — locations cite different scope records: %s\n' "$(printf '%s' "$all_refs" | tr '\n' ' ')"
    return 3
  fi

  local all_phases phase_count
  all_phases="$(printf '%s\n%s\n%s\n' "$l1_phase" "$l2_phase" "$l3_phase" | grep -v '^$' | sort -u)"
  phase_count="$(printf '%s\n' "$all_phases" | grep -c . )"

  if [ "$phase_count" -eq 0 ]; then
    printf 'RESULT: phase-unnamed — record %s is agreed but no location names a phase.\n' "$l3_record"
    return 4
  fi
  if [ "$phase_count" -ne 1 ]; then
    printf 'RESULT: divergence — locations name different phases: %s\n' "$(printf '%s' "$all_phases" | tr '\n' ' ')"
    return 3
  fi

  printf 'RESULT: agreement\n'
  printf 'PHASE=%s\n' "$all_phases"
  printf 'RECORD=docs/change-requests/%s\n' "$l3_record"
  return 0
}

# ----------------------------------------------------------------- self-test --

fixture() { # $1=dir $2=cited-record $3=phase-token-or-empty $4=record-file-or-empty
  mkdir -p "$1/docs/change-requests"
  {
    printf '# alaa-go-chi Consumers\n\n## Current Execution Scope\n\n'
    printf 'The project-owner decision in `change-requests/%s` sets the current scope.\n' "$2"
    printf 'Record every consumer as `NOT_ASSESSED_KIT_FIRST` until explicit owner reactivation.\n'
  } > "$1/docs/CONSUMERS.md"
  {
    printf '# Agents\n\n## Current scope\n\n'
    if [ -n "$3" ]; then
      printf 'The project owner activated `%s` in `docs/change-requests/%s`.\n' "$3" "$2"
    else
      printf 'The project owner set the scope in `docs/change-requests/%s`.\n' "$2"
    fi
  } > "$1/AGENTS.md"
  cp "$1/AGENTS.md" "$1/CONSTITUTION.md"
  cp "$1/AGENTS.md" "$1/GOVERNANCE.md"
  [ -n "$4" ] && printf '# Scope decision\n\nOwner-ratified execution scope.\n' > "$1/docs/change-requests/$4"
  return 0
}

expect() { # $1=label $2=expected-code $3=dir
  local got
  run_check "$3" >/dev/null 2>&1
  got=$?
  if [ "$got" -eq "$2" ]; then
    printf 'ok    %-28s exit %s\n' "$1" "$got"
    return 0
  fi
  printf 'FAIL  %-28s expected %s, got %s\n' "$1" "$2" "$got"
  return 1
}

self_test() {
  local tmp fails=0
  tmp="$(mktemp -d "${TMPDIR:-/tmp}/phase-check-selftest.XXXXXX")" || return 1
  trap 'rm -rf "$tmp"' EXIT

  fixture "$tmp/agree" 2026-01-01-alpha-scope.md TEST_PHASE_ALPHA 2026-01-01-alpha-scope.md
  expect "agreement"              0 "$tmp/agree"      || fails=$((fails+1))

  fixture "$tmp/stale" 2026-01-01-alpha-scope.md TEST_PHASE_ALPHA 2026-01-01-alpha-scope.md
  printf '# Newer scope\n' > "$tmp/stale/docs/change-requests/2026-06-01-beta-scope.md"
  expect "stale citation vs newer" 3 "$tmp/stale"     || fails=$((fails+1))

  fixture "$tmp/twophase" 2026-01-01-alpha-scope.md TEST_PHASE_ALPHA 2026-01-01-alpha-scope.md
  printf 'The `TEST_PHASE_BETA` phase is active.\n' >> "$tmp/twophase/GOVERNANCE.md"
  expect "two phase names"        3 "$tmp/twophase"   || fails=$((fails+1))

  fixture "$tmp/unnamed" 2026-01-01-alpha-scope.md "" 2026-01-01-alpha-scope.md
  expect "record but no phase"    4 "$tmp/unnamed"    || fails=$((fails+1))

  fixture "$tmp/norecord" 2026-01-01-alpha-scope.md TEST_PHASE_ALPHA ""
  expect "no scope record"        5 "$tmp/norecord"   || fails=$((fails+1))

  fixture "$tmp/nobanner" 2026-01-01-alpha-scope.md TEST_PHASE_ALPHA 2026-01-01-alpha-scope.md
  printf '# alaa-go-chi Consumers\n\nNo scope banner here.\n' > "$tmp/nobanner/docs/CONSUMERS.md"
  expect "banner removed"         3 "$tmp/nobanner"   || fails=$((fails+1))

  mkdir -p "$tmp/notakit"
  expect "not a kit checkout"     2 "$tmp/notakit"    || fails=$((fails+1))

  rm -rf "$tmp"
  trap - EXIT
  if [ "$fails" -eq 0 ]; then
    printf 'self-test: 7 passed\n'
    return 0
  fi
  printf 'self-test: %s failed\n' "$fails"
  return 1
}

# ------------------------------------------------------------------- dispatch --

case "${1:-}" in
  --help|-h|"") usage; [ -n "${1:-}" ] && exit 0; exit 2 ;;
  --self-test)  self_test; exit $? ;;
  -*)           printf 'phase-check: unknown option %s\n\n' "$1" >&2; usage >&2; exit 2 ;;
  *)            run_check "$1"; exit $? ;;
esac
