#!/usr/bin/env bash
#
# self_test.sh - run every checker's own --self-test and assert that the four
# exit codes are distinct across the whole toolchain.
#
# Before the 2026-07-29 repair every script returned 1 for "no argument",
# "target not found", "tool unavailable" and "findings present" alike, so a CI
# gate built on any of them treated a missing tool as a pass. This script is the
# gate on that gate.
#
# Requires bash 4.0 or newer. Exit codes: 0 every self-test passed, 1 a
# self-test failed, 2 the runner could not run, 64 usage error.

set -uo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib/common.sh"

av_print_help() {
    cat <<'EOF'
self_test.sh - run every checker's self-test.

Usage:
  bash scripts/self_test.sh [options]

It runs, in order:
  validate_playbook.sh --self-test
  validate_role.sh --self-test
  validate_playbook_security.sh --self-test
  validate_role_security.sh --self-test
  scan_secrets.sh --self-test
  check_fqcn.sh --self-test
  check_task_safety.py --self-test
  check_module_currency.py --self-test
  check_assets.sh --self-test
  test_role.sh --self-test
  setup_tools.sh --self-test
  extract_ansible_info.py --self-test

Every one of them runs against the fixtures under test/ and passes from a fresh
checkout with the toolchain in scripts/requirements.txt installed. A self-test
that exits 2 means the toolchain is missing, not that the skill is broken; fix
the toolchain and run it again.

EOF
    av_common_flag_help
}

av_parse_common_flags "$@"

av_banner "ansible-validator self-test"

FAILED=0
BLOCKED=0

run_one() {
    local label="$1"
    shift
    echo ""
    printf "%b--- %s ---%b\n" "$COLOR_BLUE" "$label" "$COLOR_RESET"
    local status=0
    "$@" || status=$?
    case $status in
        0) printf "%b%s: pass%b\n" "$COLOR_GREEN" "$label" "$COLOR_RESET" ;;
        2) printf "%b%s: BLOCKED (exit 2, toolchain missing)%b\n" "$COLOR_YELLOW" "$label" "$COLOR_RESET"
           BLOCKED=$((BLOCKED + 1)) ;;
        *) printf "%b%s: FAIL (exit %s)%b\n" "$COLOR_RED" "$label" "$status" "$COLOR_RESET"
           FAILED=$((FAILED + 1)) ;;
    esac
}

PY="$(command -v python3 || command -v python)" || av_cannot_run "python3 is not on PATH"

run_one validate_playbook          bash "$AV_SCRIPT_DIR/validate_playbook.sh" --self-test
run_one validate_role              bash "$AV_SCRIPT_DIR/validate_role.sh" --self-test
run_one validate_playbook_security bash "$AV_SCRIPT_DIR/validate_playbook_security.sh" --self-test
run_one validate_role_security     bash "$AV_SCRIPT_DIR/validate_role_security.sh" --self-test
run_one scan_secrets               bash "$AV_SCRIPT_DIR/scan_secrets.sh" --self-test
run_one check_fqcn                 bash "$AV_SCRIPT_DIR/check_fqcn.sh" --self-test
run_one check_task_safety          "$PY" "$AV_SCRIPT_DIR/check_task_safety.py" --self-test
run_one check_module_currency      "$PY" "$AV_SCRIPT_DIR/check_module_currency.py" --self-test
run_one check_assets               bash "$AV_SCRIPT_DIR/check_assets.sh" --self-test
run_one test_role                  bash "$AV_SCRIPT_DIR/test_role.sh" --self-test
run_one setup_tools                bash "$AV_SCRIPT_DIR/setup_tools.sh" --self-test
run_one extract_ansible_info       "$PY" "$AV_SCRIPT_DIR/extract_ansible_info.py" --self-test

echo ""
av_banner "self-test summary"
if [ $FAILED -eq 0 ] && [ $BLOCKED -eq 0 ]; then
    printf "%bAll self-tests passed.%b\n" "$COLOR_GREEN" "$COLOR_RESET"
    exit 0
fi
if [ $FAILED -eq 0 ]; then
    printf "%b%d self-test(s) were blocked by a missing tool. Install scripts/requirements.txt and run again.%b\n" "$COLOR_YELLOW" "$BLOCKED" "$COLOR_RESET"
    exit 2
fi
printf "%b%d self-test(s) FAILED, %d blocked.%b\n" "$COLOR_RED" "$FAILED" "$BLOCKED" "$COLOR_RESET"
exit 1
