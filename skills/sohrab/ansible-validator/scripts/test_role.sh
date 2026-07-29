#!/usr/bin/env bash
#
# test_role.sh - run a Molecule scenario against a role.
#
# Molecule `converge` runs the role for real inside a container it creates. This
# script therefore never runs on its own initiative. It runs when a human asked
# for a test, and it refuses to start until the caller has confirmed that the
# machine is a disposable test host. references/molecule.md states that rule
# once and this script enforces it.
#
# Requires bash 4.0 or newer. Exit codes: 0 clean, 1 findings, 2 could not run,
# 64 usage error.

set -uo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib/common.sh"

av_print_help() {
    cat <<'EOF'
test_role.sh - run one Molecule scenario against a role.

Usage:
  bash scripts/test_role.sh <role-directory> [scenario] --i-confirm-disposable-host
  bash scripts/test_role.sh --self-test

Scenario defaults to "default".

What it asserts, in order, with every stage run and tallied so that the summary
and the teardown always execute:
  dependency    role and collection requirements resolve
  syntax        the scenario's converge playbook parses
  create        the platform instances come up
  prepare       the prepare playbook runs, when the scenario declares one
  converge      the role applies cleanly
  idempotence   a second apply changes nothing. This uses Molecule's own
                `idempotence` action, which compares every host. The pre-repair
                version ran `converge` again and grepped for "changed=0", which
                passed whenever any one host of four reported no change.
  verify        the verify playbook passes
  destroy       the instances are torn down, whatever happened above

Why the confirmation flag: `molecule create` starts privileged containers with
/sys/fs/cgroup mounted read-write on whatever machine you are on. Running that
without asking is exactly the class of action that needs authorisation. If you
are not on a disposable test host, do not pass the flag; report that Molecule
is configured, that you are not running it, and why.

Additional options:
      --i-confirm-disposable-host
                            Required. Asserts that this machine is a disposable
                            test host whose containers may be created and
                            destroyed.

EOF
    av_common_flag_help
}

CONFIRMED=0

run_self_test() {
    local here="$0" fx
    fx="$(av_fixture_dir)"
    echo "self-test: test_role.sh"
    av_expect_exit 64 "no argument is a usage error" bash "$here"
    av_expect_exit 0  "--help exits clean" bash "$here" --help
    av_expect_exit 2  "missing target cannot run" bash "$here" "$fx/fixtures/roles/no_such_role" default --i-confirm-disposable-host
    av_expect_exit 64 "missing confirmation is a usage error" bash "$here" "$fx/fixtures/roles/clean_role"
    av_expect_exit 2  "a role with no molecule/ cannot run" bash "$here" "$fx/fixtures/roles/clean_role" default --i-confirm-disposable-host
    av_self_test_summary
}

ARGS=()
while [ $# -gt 0 ]; do
    case "$1" in
        --i-confirm-disposable-host) CONFIRMED=1; shift ;;
        *) ARGS+=("$1"); shift ;;
    esac
done
av_parse_common_flags ${ARGS+"${ARGS[@]}"}

if [ "$AV_SELF_TEST" -eq 1 ]; then
    run_self_test
fi

if [ "${#AV_ARGS[@]}" -lt 1 ]; then
    av_usage_error "a role directory is required"
fi

ROLE_PATH="${AV_ARGS[0]}"
SCENARIO="${AV_ARGS[1]:-default}"

if [ ! -d "$ROLE_PATH" ]; then
    av_cannot_run "role directory not found: $ROLE_PATH"
fi
ROLE_ABS="$(cd "$ROLE_PATH" && pwd)"

if [ "$CONFIRMED" -ne 1 ]; then
    av_usage_error "--i-confirm-disposable-host is required. Molecule creates privileged containers on this machine; confirm that this machine is a disposable test host, or report that Molecule is configured and that you are not running it."
fi

if [ ! -d "$ROLE_ABS/molecule/$SCENARIO" ]; then
    av_cannot_run "molecule scenario '$SCENARIO' not found under $ROLE_ABS/molecule/. Create one with 'molecule init scenario' from inside the role, then configure the driver as references/molecule.md describes."
fi

MOLECULE_BIN="$(av_resolve_tool molecule)" || av_cannot_run "molecule is not available and no tool environment could be created. Install it with: python3 -m pip install 'molecule>=25.0' 'molecule-plugins[docker]'"

av_banner "Molecule scenario: $SCENARIO"
echo "Role: $ROLE_ABS"
echo ""

cd "$ROLE_ABS" || av_cannot_run "could not enter $ROLE_ABS"

STAGE_ERRORS=0

run_stage() {
    local stage="$1" description="$2" required="${3:-required}"
    printf "%b[%s] %s%b\n" "$COLOR_BLUE" "$stage" "$description" "$COLOR_RESET"
    if "$MOLECULE_BIN" "$stage" -s "$SCENARIO"; then
        printf "  %bok%b  %s\n\n" "$COLOR_GREEN" "$COLOR_RESET" "$description"
        return 0
    fi
    if [ "$required" = optional ]; then
        printf "  %b--%b  %s did not run; the scenario does not declare it\n\n" "$COLOR_YELLOW" "$COLOR_RESET" "$description"
        return 0
    fi
    printf "  %bfail%b %s\n\n" "$COLOR_RED" "$COLOR_RESET" "$description"
    STAGE_ERRORS=$((STAGE_ERRORS + 1))
    return 0
}

# Every stage is invoked with its failure tallied rather than propagated, so
# that destroy and the summary always run. Under the pre-repair `set -e` the
# first failing stage killed the script, leaving the test containers running
# and printing no summary at all.
run_stage dependency "Resolve dependencies" optional
run_stage syntax     "Syntax check"
run_stage create     "Create instances"
run_stage prepare    "Prepare instances" optional
run_stage converge   "Apply the role"
run_stage idempotence "Idempotence (second apply changes nothing)"
run_stage verify     "Verification playbook"

printf "%b[destroy] Tear down instances%b\n" "$COLOR_BLUE" "$COLOR_RESET"
"$MOLECULE_BIN" destroy -s "$SCENARIO" || printf "  %bwarning%b destroy failed; instances may still be running. Run 'molecule destroy -s %s' from %s.\n" "$COLOR_YELLOW" "$COLOR_RESET" "$SCENARIO" "$ROLE_ABS"
echo ""

if [ $STAGE_ERRORS -gt 0 ]; then
    av_add_error "$STAGE_ERRORS Molecule stage(s) failed" "references/molecule.md"
fi

av_summary "test_role" "$ROLE_ABS"
exit $?
