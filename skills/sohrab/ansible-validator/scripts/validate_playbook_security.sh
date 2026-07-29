#!/usr/bin/env bash
#
# validate_playbook_security.sh - Checkov security scan of one playbook file.
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
validate_playbook_security.sh - Checkov security scan of one playbook.

Usage:
  bash scripts/validate_playbook_security.sh <playbook.yml> [options]
  bash scripts/validate_playbook_security.sh --self-test

What it asserts:
  Checkov reports zero failed checks under --framework ansible,secrets for the
  named file, and only for the named file.

Why both frameworks: --framework ansible carries twelve TLS, HTTPS and GPG
policies and models no credential shape. Against the six secrets planted in
test/fixtures/secrets/planted-secrets.yml it reported zero on 2026-07-29;
--framework secrets reported all six. Running the ansible framework alone is a
security scan that cannot see a leaked AWS key.

Additional options:
      --frameworks LIST     Override the framework list (default ansible,secrets).

EOF
    av_common_flag_help
}

run_self_test() {
    local here="$0" fx
    fx="$(av_fixture_dir)"
    echo "self-test: validate_playbook_security.sh"
    av_expect_exit 64 "no argument is a usage error" bash "$here"
    av_expect_exit 0  "--help exits clean" bash "$here" --help
    av_expect_exit 2  "missing target cannot run" bash "$here" "$fx/playbooks/does-not-exist.yml"
    av_expect_exit 2  "missing tool cannot run" env AV_NO_BOOTSTRAP=1 AV_UNAVAILABLE_TOOLS=checkov bash "$here" "$fx/playbooks/good-playbook.yml"
    av_expect_exit 1  "planted secrets are reported" bash "$here" "$fx/fixtures/secrets/planted-secrets.yml"
    av_expect_exit 0  "good playbook is clean" bash "$here" "$fx/playbooks/good-playbook.yml"
    av_self_test_summary
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

if [ "$AV_SELF_TEST" -eq 1 ]; then
    run_self_test
fi

if [ "${#AV_ARGS[@]}" -lt 1 ]; then
    av_usage_error "a playbook path is required"
fi

TARGET="${AV_ARGS[0]}"
if [ ! -f "$TARGET" ]; then
    av_cannot_run "playbook not found: $TARGET"
fi
av_assert_no_crlf "$TARGET"
TARGET_ABS="$(cd "$(dirname "$TARGET")" && pwd)/$(basename "$TARGET")"

if [ "$AV_FORMAT" = "text" ]; then
    av_banner "Ansible Playbook Security Scan"
    echo "Target: $TARGET_ABS"
    echo ""
fi

av_checkov_stage "$TARGET_ABS" file
av_security_epilogue
av_summary "validate_playbook_security" "$TARGET_ABS"
exit $?
