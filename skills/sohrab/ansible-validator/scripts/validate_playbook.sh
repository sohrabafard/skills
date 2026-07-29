#!/usr/bin/env bash
#
# validate_playbook.sh - YAML, Ansible syntax and ansible-lint on one playbook.
#
# Requires bash 4.0 or newer. See scripts/lib/common.sh for the exit-code
# contract, the configuration override order and the cached tool environment.

set -uo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib/common.sh"

av_print_help() {
    cat <<'EOF'
validate_playbook.sh - validate one Ansible playbook file.

Usage:
  bash scripts/validate_playbook.sh <playbook.yml> [options]
  bash scripts/validate_playbook.sh --self-test

Stages, in order. Each stage names what it asserts:
  1 yamllint                     the file is well-formed YAML under the
                                 resolved yamllint config
  2 ansible-playbook --syntax-check
                                 Ansible can parse the play, its includes and
                                 its module references
  3 ansible-lint                 the file satisfies the resolved ansible-lint
                                 profile

EOF
    av_common_flag_help
}

run_self_test() {
    local here="$0" fx
    fx="$(av_fixture_dir)"
    echo "self-test: validate_playbook.sh"
    av_expect_exit 64 "no argument is a usage error" bash "$here"
    av_expect_exit 0  "--help exits clean" bash "$here" --help
    av_expect_exit 2  "missing target cannot run" bash "$here" "$fx/playbooks/does-not-exist.yml"
    av_expect_exit 2  "missing tool cannot run" env AV_NO_BOOTSTRAP=1 AV_UNAVAILABLE_TOOLS=yamllint,ansible-lint,ansible-playbook bash "$here" "$fx/playbooks/good-playbook.yml"
    av_expect_exit 0  "good playbook is clean" bash "$here" "$fx/playbooks/good-playbook.yml"
    av_expect_exit 1  "bad playbook reports findings" bash "$here" "$fx/playbooks/bad-playbook.yml"
    av_self_test_summary
}

av_parse_common_flags "$@"

if [ "$AV_SELF_TEST" -eq 1 ]; then
    run_self_test
fi

if [ "${#AV_ARGS[@]}" -lt 1 ]; then
    av_usage_error "a playbook path is required"
fi

PLAYBOOK="${AV_ARGS[0]}"

if [ ! -f "$PLAYBOOK" ]; then
    av_cannot_run "playbook not found: $PLAYBOOK"
fi

av_assert_no_crlf "$PLAYBOOK"

PLAYBOOK_ABS="$(cd "$(dirname "$PLAYBOOK")" && pwd)/$(basename "$PLAYBOOK")"
PLAYBOOK_DIR="$(dirname "$PLAYBOOK_ABS")"

if [ "$AV_FORMAT" = "text" ]; then
    av_banner "Ansible Playbook Validation"
    echo "Target: $PLAYBOOK_ABS"
    echo ""
fi

YAMLLINT_CONFIG="$(av_resolve_yamllint_config "$PLAYBOOK_DIR")"
ANSIBLE_LINT_CONFIG="$(av_resolve_ansible_lint_config "$PLAYBOOK_DIR")"

YAMLLINT_BIN="$(av_resolve_tool yamllint)" || av_cannot_run "yamllint is not available and no tool environment could be created. Install it with: python3 -m pip install -r scripts/requirements.txt"
ANSIBLE_PLAYBOOK_BIN="$(av_resolve_tool ansible-playbook)" || av_cannot_run "ansible-playbook is not available and no tool environment could be created. Install it with: python3 -m pip install -r scripts/requirements.txt"
ANSIBLE_LINT_BIN="$(av_resolve_tool ansible-lint)" || av_cannot_run "ansible-lint is not available and no tool environment could be created. Install it with: python3 -m pip install -r scripts/requirements.txt"

# --- Stage 1: YAML ---------------------------------------------------------
[ "$AV_FORMAT" = "text" ] && printf "%b[1/3] YAML (yamllint -c %s)%b\n" "$COLOR_BLUE" "$YAMLLINT_CONFIG" "$COLOR_RESET"
YAMLLINT_OUT="$("$YAMLLINT_BIN" -c "$YAMLLINT_CONFIG" -f parsable "$PLAYBOOK_ABS" 2>&1)"
YAMLLINT_STATUS=$?
if [ $YAMLLINT_STATUS -eq 0 ]; then
    [ "$AV_FORMAT" = "text" ] && printf "  %bok%b  YAML is well formed\n" "$COLOR_GREEN" "$COLOR_RESET"
elif [ $YAMLLINT_STATUS -eq 1 ]; then
    [ "$AV_FORMAT" = "text" ] && echo "$YAMLLINT_OUT"
    av_add_error "yamllint reported findings in $(basename "$PLAYBOOK_ABS")" "references/failure-classes.md"
else
    av_cannot_run "yamllint exited $YAMLLINT_STATUS (configuration error, not a finding): $YAMLLINT_OUT"
fi

# --- Stage 2: Ansible syntax ----------------------------------------------
[ "$AV_FORMAT" = "text" ] && printf "\n%b[2/3] Ansible syntax (ansible-playbook --syntax-check)%b\n" "$COLOR_BLUE" "$COLOR_RESET"
if SYNTAX_OUT="$("$ANSIBLE_PLAYBOOK_BIN" --syntax-check "$PLAYBOOK_ABS" 2>&1)"; then
    [ "$AV_FORMAT" = "text" ] && printf "  %bok%b  Ansible parses the play\n" "$COLOR_GREEN" "$COLOR_RESET"
else
    [ "$AV_FORMAT" = "text" ] && echo "$SYNTAX_OUT"
    av_add_error "ansible-playbook --syntax-check failed" "references/failure-classes.md"
fi

# --- Stage 3: ansible-lint -------------------------------------------------
[ "$AV_FORMAT" = "text" ] && printf "\n%b[3/3] ansible-lint (-c %s)%b\n" "$COLOR_BLUE" "$ANSIBLE_LINT_CONFIG" "$COLOR_RESET"
LINT_OUT="$("$ANSIBLE_LINT_BIN" -c "$ANSIBLE_LINT_CONFIG" "$PLAYBOOK_ABS" 2>&1)"
LINT_STATUS=$?
case $LINT_STATUS in
    0)
        [ "$AV_FORMAT" = "text" ] && printf "  %bok%b  ansible-lint is clean\n" "$COLOR_GREEN" "$COLOR_RESET"
        ;;
    1|2)
        [ "$AV_FORMAT" = "text" ] && echo "$LINT_OUT"
        av_add_error "ansible-lint reported violations" "references/best_practices.md"
        ;;
    *)
        av_cannot_run "ansible-lint exited $LINT_STATUS, which means it could not run (an invalid configuration file exits 3). Output: $LINT_OUT"
        ;;
esac

av_summary "validate_playbook" "$PLAYBOOK_ABS"
exit $?
