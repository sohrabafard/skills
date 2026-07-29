#!/usr/bin/env bash
# Shared Checkov stage for validate_playbook_security.sh and
# validate_role_security.sh. Both scripts were byte-identical for 57 lines
# before the 2026-07-29 repair; the shared part lives here now.
#
# shellcheck shell=bash

if [ -n "${AV_CHECKOV_SOURCED:-}" ]; then
    return 0
fi
AV_CHECKOV_SOURCED=1

# The framework list is the whole point of this file.
#
# --framework ansible alone is not a secrets scanner. It carries twelve
# policies and every one of them is about TLS, HTTPS or GPG. Measured
# 2026-07-29 against checkov 3.3.8 and test/fixtures/secrets/planted-secrets.yml
# (six planted credentials), with `-o json --skip-download`:
#
#   --framework ansible          passed=0 failed=0   nothing at all
#   --framework secrets          passed=0 failed=5   CKV_SECRET_2 (AWS access
#                                                    key), CKV_SECRET_4 (basic
#                                                    auth credentials),
#                                                    CKV_SECRET_6 x2 (high
#                                                    entropy), CKV_SECRET_13
#                                                    (private key)
#   --framework ansible,secrets  passed=0 failed=5
#
# So this skill mandates `--framework ansible,secrets` on every invocation, and
# running the ansible framework alone is a security scan that cannot see a
# leaked AWS key. Neither framework replaces scripts/scan_secrets.sh, which
# catches the Ansible-specific shapes that are about vault indirection rather
# than entropy: on the same fixture Checkov missed the plaintext
# `db_password: "hunter2-plaintext"` that scan_secrets.sh reports.
AV_CHECKOV_FRAMEWORKS="${AV_CHECKOV_FRAMEWORKS:-ansible,secrets}"

av_checkov_stage() {
    # av_checkov_stage <target-abs> <file|directory>
    local target="$1" kind="$2" bin out summary
    local -a args

    bin="$(av_resolve_tool checkov)" || av_cannot_run "checkov is not available and no tool environment could be created. Install it with: python3 -m pip install -r scripts/requirements.txt"

    if [ "$kind" = file ]; then
        # Scan the named file. The pre-repair version silently widened the scan
        # to the whole containing directory, so "validate this playbook"
        # reported findings from every sibling file with no indication of which
        # file they came from.
        args=(-f "$target")
    else
        args=(-d "$target")
    fi
    # --skip-download stops Checkov reaching api0.prismacloud.io for guideline
    # text. In a locked-down runner that call fails with a proxy traceback that
    # buries the report; the policies themselves are local and unaffected.
    # -o json is what makes "could not run" distinguishable from "clean": the
    # JSON summary always carries passed, failed and parsing_errors, while the
    # CLI renderer prints nothing at all for a clean file, which is exactly the
    # output an unparsable file also produces.
    args+=(--framework "$AV_CHECKOV_FRAMEWORKS" -o json --skip-download --quiet)

    [ "$AV_FORMAT" = "text" ] && printf "%bCheckov (--framework %s)%b\n" "$COLOR_BLUE" "$AV_CHECKOV_FRAMEWORKS" "$COLOR_RESET"

    out="$("$bin" "${args[@]}" 2>/dev/null)"

    summary="$(printf '%s' "$out" | python3 -c '
import json, sys
raw = sys.stdin.read().strip()
if not raw:
    print("NOREPORT")
    sys.exit(0)
try:
    data = json.loads(raw)
except Exception:
    print("NOREPORT")
    sys.exit(0)
if isinstance(data, dict):
    data = [data]
passed = failed = parse_errors = 0
ids = []
for report in data:
    s = report.get("summary") or {}
    passed += s.get("passed", 0)
    failed += s.get("failed", 0)
    parse_errors += s.get("parsing_errors", 0)
    for check in (report.get("results") or {}).get("failed_checks") or []:
        cid = check.get("check_id")
        path = check.get("file_path", "")
        line = (check.get("file_line_range") or [0])[0]
        ids.append(f"{cid} {path}:{line}")
print(f"{passed} {failed} {parse_errors}")
for entry in ids:
    print(entry)
' 2>/dev/null)"

    if [ -z "$summary" ] || [ "${summary%%$'\n'*}" = "NOREPORT" ]; then
        # No parsable report means Checkov evaluated nothing: an unparsable
        # target, a crash, or a framework that never loaded. That is exit 2,
        # not a security failure and not a pass.
        av_cannot_run "Checkov produced no parsable JSON report, so it evaluated nothing. This is not a clean result."
    fi

    local counts passed failed parse_errors
    counts="${summary%%$'\n'*}"
    read -r passed failed parse_errors <<<"$counts"

    if [ "${parse_errors:-0}" -gt 0 ]; then
        av_cannot_run "Checkov reported $parse_errors parsing error(s). A file it could not parse was not evaluated, so this is not a clean result."
    fi

    if [ "$AV_FORMAT" = "text" ]; then
        echo "  passed: $passed   failed: $failed   parsing errors: $parse_errors"
    fi

    if [ "${failed:-0}" -gt 0 ]; then
        if [ "$AV_FORMAT" = "text" ]; then
            printf '%s\n' "$summary" | tail -n +2 | while IFS= read -r entry; do
                [ -n "$entry" ] && echo "    $entry"
            done
        fi
        av_add_error "Checkov reported $failed failed check(s)" "references/security_checklist.md"
    elif [ "$AV_FORMAT" = "text" ]; then
        printf "  %bok%b  no Checkov policy failed\n" "$COLOR_GREEN" "$COLOR_RESET"
    fi
}

av_security_epilogue() {
    [ "$AV_FORMAT" = "text" ] || return 0
    cat <<'EOF'

This stage is one half of the security audit. The other half is
  bash scripts/scan_secrets.sh <target>
  python3 scripts/check_task_safety.py <target>
All three run on every audit. A scan that could not run is a blocked audit, not
a clean one, and exits 2.

Whether a finding blocks the change is not this skill's decision:
/alaa-security-review ($alaa-security-review) owns fail-closed doctrine.
EOF
}
