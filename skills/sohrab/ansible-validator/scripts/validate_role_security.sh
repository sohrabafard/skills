#!/usr/bin/env bash
#
# validate_role_security.sh - Checkov security scan of one role directory.
#
# Requires bash 4.0 or newer. Exit codes: 0 clean, 1 findings, 2 could not run,
# 64 usage error. "Checkov could not produce a report" is exit 2 and never a
# pass, because a security check that did not run is not a passing check.

set -uo pipefail

AV_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib"
source "$AV_LIB/common.sh"
source "$AV_LIB/checkov_scan.sh"

av_print_help() {
    cat <<'EOF'
validate_role_security.sh - Checkov security scan of one role directory.

Usage:
  bash scripts/validate_role_security.sh <role-directory> [options]

What it asserts:
  Checkov reports zero failed checks under --framework ansible,secrets over the
  named role directory.

Why both frameworks: see validate_playbook_security.sh --help, and
references/security_checklist.md, which states the division of labour between
Checkov's two frameworks and scripts/scan_secrets.sh once.

Additional options:
      --frameworks LIST     Override the framework list (default ansible,secrets).

EOF
    av_common_flag_help
}


ARGS=()
while [ $# -gt 0 ]; do
    case "$1" in
        --frameworks)
            [ $# -ge 2 ] || { echo "Usage error: --frameworks needs a value" >&2; exit 64; }
            AV_CHECKOV_FRAMEWORKS="$2"; shift 2 ;;
        *) ARGS+=("$1"); shift ;;
    esac
done
av_parse_common_flags ${ARGS+"${ARGS[@]}"}


if [ "${#AV_ARGS[@]}" -lt 1 ]; then
    av_usage_error "a role directory is required"
fi

TARGET="${AV_ARGS[0]}"
if [ ! -d "$TARGET" ]; then
    av_cannot_run "role directory not found: $TARGET"
fi
TARGET_ABS="$(cd "$TARGET" && pwd)"

if [ "$AV_FORMAT" = "text" ]; then
    av_banner "Ansible Role Security Scan"
    echo "Target: $TARGET_ABS"
    echo ""
fi

av_checkov_stage "$TARGET_ABS" directory
av_security_epilogue
av_summary "validate_role_security" "$TARGET_ABS"
exit $?
