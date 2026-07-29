#!/usr/bin/env bash
#
# check_assets.sh - prove that the shipped lint configurations still enable the
# rules they claim to enable.
#
# This exists because a configuration can silently disable a rule. Before the
# 2026-07-29 repair, assets/.ansible-lint set `task_name_prefix: "{path}:"`;
# `{path}` is not a valid substitution key, ansible-lint swallowed the resulting
# KeyError, and NameRule died. Measured: 19 failures and zero name[missing] with
# that line, 21 failures and two name[missing] without it. The config disabled
# the two rules its own enable_list explicitly asked for, and nothing reported
# that. This script reports it.
#
# Requires bash 4.0 or newer. Exit codes: 0 the configs assert what they claim,
# 1 a claimed rule did not fire, 2 a tool is missing or a config is invalid,
# 64 usage error.

set -uo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib/common.sh"

av_print_help() {
    cat <<'EOF'
check_assets.sh - assert that assets/.ansible-lint and assets/.yamllint report
what they claim to report.

Usage:
  bash scripts/check_assets.sh [options]
  bash scripts/check_assets.sh --self-test

What it asserts, against test/fixtures/lint/:
  1. ansible-lint accepts assets/.ansible-lint (exit 0 or 1 or 2, never 3).
  2. Every rule named in the config's enable_list fires on the fixture built to
     violate it. Today that is name[missing] and name[casing].
  3. yamllint accepts assets/.yamllint.
  4. The two configs agree about truthy values: a file containing `become: yes`
     is reported by both, not by one and passed by the other.
  5. The two configs agree about the leading `---`: a conventional Ansible file
     that starts with `---` is clean under both.

--self-test runs the same assertions and is therefore an alias for a plain run
plus the argument-handling checks.

EOF
    av_common_flag_help
}

run_self_test() {
    local here="$0"
    echo "self-test: check_assets.sh"
    av_expect_exit 0 "--help exits clean" bash "$here" --help
    av_expect_exit 64 "an unknown flag is a usage error" bash "$here" --no-such-flag
    av_expect_exit 2 "missing tool cannot run" env AV_NO_BOOTSTRAP=1 AV_UNAVAILABLE_TOOLS=ansible-lint,yamllint bash "$here"
    av_expect_exit 0 "the shipped configs assert what they claim" bash "$here"
    av_self_test_summary
}

av_parse_common_flags "$@"

if [ "$AV_SELF_TEST" -eq 1 ]; then
    run_self_test
fi

FX="$(av_fixture_dir)/fixtures/lint"
ALINT_CFG="$AV_SKILL_DIR/assets/.ansible-lint"
YLINT_CFG="$AV_SKILL_DIR/assets/.yamllint"

[ -f "$ALINT_CFG" ] || av_cannot_run "assets/.ansible-lint not found at $ALINT_CFG"
[ -f "$YLINT_CFG" ] || av_cannot_run "assets/.yamllint not found at $YLINT_CFG"
[ -d "$FX" ] || av_cannot_run "lint fixtures not found at $FX"

ANSIBLE_LINT_BIN="$(av_resolve_tool ansible-lint)" || av_cannot_run "ansible-lint is not available and no tool environment could be created"
YAMLLINT_BIN="$(av_resolve_tool yamllint)" || av_cannot_run "yamllint is not available and no tool environment could be created"

av_banner "Shipped lint configuration assertions"

# 1. The ansible-lint config must be accepted. Exit 3 means the file itself is
#    rejected, which makes every project that copies it unlintable.
LINT_OUT="$("$ANSIBLE_LINT_BIN" -c "$ALINT_CFG" "$FX/unnamed-task.yml" 2>&1)"
LINT_STATUS=$?
if [ $LINT_STATUS -ge 3 ]; then
    av_cannot_run "ansible-lint rejects assets/.ansible-lint (exit $LINT_STATUS). Output: $LINT_OUT"
fi
printf "  %bok%b  ansible-lint accepts assets/.ansible-lint\n" "$COLOR_GREEN" "$COLOR_RESET"

# A swallowed rule exception is printed as a WARNING and then ignored. Treat it
# as a finding: a rule that raised is a rule that is not running.
if printf '%s' "$LINT_OUT" | grep -qi 'Ignored exception from'; then
    av_add_error "ansible-lint swallowed an exception from a rule, so that rule is not running: $(printf '%s' "$LINT_OUT" | grep -i 'Ignored exception from' | head -1)" "assets/.ansible-lint"
fi

# 2. Every rule in enable_list must fire on the fixture built to violate it.
assert_rule_fires() {
    # assert_rule_fires <rule-id> <fixture>
    local rule="$1" fixture="$2" out
    out="$("$ANSIBLE_LINT_BIN" -c "$ALINT_CFG" "$FX/$fixture" 2>&1)"
    if printf '%s' "$out" | grep -q "$rule"; then
        printf "  %bok%b  %s fires on %s\n" "$COLOR_GREEN" "$COLOR_RESET" "$rule" "$fixture"
    else
        av_add_error "$rule is in enable_list but did not fire on $fixture; the config disables a rule it asks for" "assets/.ansible-lint"
    fi
}

assert_rule_fires "name\[missing\]" unnamed-task.yml
assert_rule_fires "name\[casing\]" lowercase-task-name.yml
assert_rule_fires "fqcn\[action-core\]" unnamed-task.yml

# 3. yamllint must accept its config.
if ! YOUT="$("$YAMLLINT_BIN" -c "$YLINT_CFG" -f parsable "$FX/truthy-yes.yml" 2>&1)"; then
    YSTATUS=$?
    if [ "$YSTATUS" -gt 1 ]; then
        av_cannot_run "yamllint rejects assets/.yamllint (exit $YSTATUS). Output: $YOUT"
    fi
fi
printf "  %bok%b  yamllint accepts assets/.yamllint\n" "$COLOR_GREEN" "$COLOR_RESET"

# 4. The two configs must agree about truthy.
Y_TRUTHY=0
printf '%s' "$YOUT" | grep -q 'truthy' && Y_TRUTHY=1
A_TRUTHY=0
"$ANSIBLE_LINT_BIN" -c "$ALINT_CFG" "$FX/truthy-yes.yml" 2>&1 | grep -q 'yaml\[truthy\]' && A_TRUTHY=1
if [ "$Y_TRUTHY" -eq "$A_TRUTHY" ]; then
    printf "  %bok%b  yamllint and ansible-lint agree about 'become: yes'\n" "$COLOR_GREEN" "$COLOR_RESET"
else
    av_add_error "yamllint and ansible-lint disagree about 'become: yes' (yamllint reports=$Y_TRUTHY, ansible-lint reports=$A_TRUTHY). One of them is teaching the opposite of the other." "assets/.yamllint"
fi

# 5. The two configs must agree about the leading document start.
if "$YAMLLINT_BIN" -c "$YLINT_CFG" -f parsable "$FX/document-start.yml" 2>&1 | grep -q 'document-start'; then
    av_add_error "assets/.yamllint reports the leading '---' that every conventional Ansible file carries. Set document-start: present: true." "assets/.yamllint"
else
    printf "  %bok%b  a leading '---' is clean under assets/.yamllint\n" "$COLOR_GREEN" "$COLOR_RESET"
fi

av_summary "check_assets" "$AV_SKILL_DIR/assets"
exit $?
