#!/usr/bin/env bash
#
# validate_role.sh - structure, YAML, Ansible syntax, ansible-lint and Molecule
# presence for one role directory.
#
# Requires bash 4.0 or newer. See scripts/lib/common.sh for the exit-code
# contract, the configuration override order and the cached tool environment.

set -uo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib/common.sh"

av_print_help() {
    cat <<'EOF'
validate_role.sh - validate one Ansible role directory.

Usage:
  bash scripts/validate_role.sh <role-directory> [options]
  bash scripts/validate_role.sh --self-test

Stages, in order. Each stage names what it asserts:
  1 structure      tasks/ exists; defaults/, handlers/, meta/, templates/ and
                   vars/ are reported when absent; each present directory has
                   a main.yml
  2 YAML           every .yml and .yaml file under the role is well formed
                   under the resolved yamllint config. A file that yamllint
                   rejects is counted as an error. This stage read grep's exit
                   status before the 2026-07-29 repair, which made it
                   incapable of reporting a failure; test/fixtures/roles/
                   broken_yaml_role is the regression fixture that proves the
                   repair and keeps it proved.
  3 Ansible syntax the role loads inside a generated one-play test playbook
  4 ansible-lint   the role satisfies the resolved ansible-lint profile
  5 Molecule       a molecule/ directory is reported when present, with its
                   scenarios. This stage runs nothing; scripts/test_role.sh
                   runs scenarios, and only when asked.

EOF
    av_common_flag_help
}

run_self_test() {
    local here="$0" fx
    fx="$(av_fixture_dir)"
    echo "self-test: validate_role.sh"
    av_expect_exit 64 "no argument is a usage error" bash "$here"
    av_expect_exit 0  "--help exits clean" bash "$here" --help
    av_expect_exit 2  "missing target cannot run" bash "$here" "$fx/fixtures/roles/no_such_role"
    av_expect_exit 2  "missing tool cannot run" env AV_NO_BOOTSTRAP=1 AV_UNAVAILABLE_TOOLS=yamllint,ansible-lint,ansible-playbook bash "$here" "$fx/fixtures/roles/clean_role"
    av_expect_exit 0  "clean role passes" bash "$here" "$fx/fixtures/roles/clean_role"
    # The regression case: every file starts with '---' and one of them is
    # syntactically broken. Before the repair this printed 'YAML syntax check
    # passed'. It must now be exit 1.
    av_expect_exit 1  "broken YAML behind a leading --- is reported" bash "$here" "$fx/fixtures/roles/broken_yaml_role"
    av_self_test_summary
}

av_parse_common_flags "$@"

if [ "$AV_SELF_TEST" -eq 1 ]; then
    run_self_test
fi

if [ "${#AV_ARGS[@]}" -lt 1 ]; then
    av_usage_error "a role directory is required"
fi

ROLE_PATH="${AV_ARGS[0]}"

if [ ! -d "$ROLE_PATH" ]; then
    av_cannot_run "role directory not found: $ROLE_PATH"
fi

ROLE_ABS="$(cd "$ROLE_PATH" && pwd)"
ROLE_NAME="$(basename "$ROLE_ABS")"

if [ "$AV_FORMAT" = "text" ]; then
    av_banner "Ansible Role Validation"
    echo "Target: $ROLE_ABS"
    echo ""
fi

YAMLLINT_CONFIG="$(av_resolve_yamllint_config "$ROLE_ABS")"
ANSIBLE_LINT_CONFIG="$(av_resolve_ansible_lint_config "$ROLE_ABS")"

YAMLLINT_BIN="$(av_resolve_tool yamllint)" || av_cannot_run "yamllint is not available and no tool environment could be created. Install it with: python3 -m pip install -r scripts/requirements.txt"
ANSIBLE_PLAYBOOK_BIN="$(av_resolve_tool ansible-playbook)" || av_cannot_run "ansible-playbook is not available and no tool environment could be created. Install it with: python3 -m pip install -r scripts/requirements.txt"
ANSIBLE_LINT_BIN="$(av_resolve_tool ansible-lint)" || av_cannot_run "ansible-lint is not available and no tool environment could be created. Install it with: python3 -m pip install -r scripts/requirements.txt"

# --- Stage 1: structure ----------------------------------------------------
[ "$AV_FORMAT" = "text" ] && printf "%b[1/5] Role structure%b\n" "$COLOR_BLUE" "$COLOR_RESET"

if [ ! -d "$ROLE_ABS/tasks" ]; then
    av_add_error "tasks/ is missing; a role without tasks/ cannot be applied" "references/best_practices.md"
elif [ "$AV_FORMAT" = "text" ]; then
    printf "  %bok%b  tasks/\n" "$COLOR_GREEN" "$COLOR_RESET"
fi

for dir in defaults handlers meta templates vars; do
    if [ ! -d "$ROLE_ABS/$dir" ]; then
        av_add_warning "$dir/ is absent" "references/best_practices.md"
    elif [ "$AV_FORMAT" = "text" ]; then
        printf "  %bok%b  %s/\n" "$COLOR_GREEN" "$COLOR_RESET" "$dir"
    fi
done

for dir in tasks defaults handlers vars meta; do
    if [ -d "$ROLE_ABS/$dir" ] && [ ! -f "$ROLE_ABS/$dir/main.yml" ] && [ ! -f "$ROLE_ABS/$dir/main.yaml" ]; then
        av_add_warning "$dir/ exists but has no main.yml; Ansible will not load it automatically" "references/best_practices.md"
    fi
done

# --- Stage 2: YAML ---------------------------------------------------------
[ "$AV_FORMAT" = "text" ] && printf "\n%b[2/5] YAML (yamllint -c %s)%b\n" "$COLOR_BLUE" "$YAMLLINT_CONFIG" "$COLOR_RESET"

YAML_ERRORS=0
YAML_CHECKED=0
# find -print0 plus read -d '' so a path containing a space, which is normal on
# Windows, is one filename and not two.
while IFS= read -r -d '' file; do
    YAML_CHECKED=$((YAML_CHECKED + 1))
    av_assert_no_crlf "$file"
    # The exit status read here is yamllint's, taken directly. Piping this
    # through grep, as the pre-repair version did, replaced yamllint's status
    # with grep's, and grep exits 0 whenever it printed anything.
    if ! FILE_OUT="$("$YAMLLINT_BIN" -c "$YAMLLINT_CONFIG" -f parsable "$file" 2>&1)"; then
        YAML_ERRORS=$((YAML_ERRORS + 1))
        [ "$AV_FORMAT" = "text" ] && echo "$FILE_OUT"
    fi
done < <(find "$ROLE_ABS" -type f \( -name '*.yml' -o -name '*.yaml' \) \
    ! -path '*/.git/*' ! -path '*/molecule/*' -print0 2>/dev/null)

if [ $YAML_CHECKED -eq 0 ]; then
    av_add_warning "no YAML files found under the role" "references/failure-classes.md"
elif [ $YAML_ERRORS -gt 0 ]; then
    av_add_error "yamllint reported findings in $YAML_ERRORS of $YAML_CHECKED file(s)" "references/failure-classes.md"
elif [ "$AV_FORMAT" = "text" ]; then
    printf "  %bok%b  %d file(s) are well formed\n" "$COLOR_GREEN" "$COLOR_RESET" "$YAML_CHECKED"
fi

# --- Stage 3: Ansible syntax ----------------------------------------------
[ "$AV_FORMAT" = "text" ] && printf "\n%b[3/5] Ansible syntax%b\n" "$COLOR_BLUE" "$COLOR_RESET"

# The scratch playbook and the roles directory are created under the system
# temporary directory, never inside the repository, because the caller's mount
# may be read-only and may forbid unlink.
SCRATCH="$(mktemp -d 2>/dev/null)" || av_cannot_run "could not create a temporary directory for the syntax check"
cleanup_scratch() { rm -rf "$SCRATCH" 2>/dev/null || true; }
trap cleanup_scratch EXIT INT TERM

mkdir -p "$SCRATCH/roles"
# Copy rather than symlink: ln -s needs Developer Mode or elevation on Windows.
cp -R "$ROLE_ABS" "$SCRATCH/roles/$ROLE_NAME"
cat > "$SCRATCH/syntax_check.yml" <<EOF
---
- name: Syntax check for role $ROLE_NAME
  hosts: localhost
  gather_facts: false
  roles:
    - role: $ROLE_NAME
EOF

if SYNTAX_OUT="$(ANSIBLE_ROLES_PATH="$SCRATCH/roles" "$ANSIBLE_PLAYBOOK_BIN" --syntax-check "$SCRATCH/syntax_check.yml" 2>&1)"; then
    [ "$AV_FORMAT" = "text" ] && printf "  %bok%b  the role loads\n" "$COLOR_GREEN" "$COLOR_RESET"
else
    [ "$AV_FORMAT" = "text" ] && echo "$SYNTAX_OUT"
    av_add_error "ansible-playbook --syntax-check failed on the role" "references/failure-classes.md"
fi

# --- Stage 4: ansible-lint -------------------------------------------------
[ "$AV_FORMAT" = "text" ] && printf "\n%b[4/5] ansible-lint (-c %s)%b\n" "$COLOR_BLUE" "$ANSIBLE_LINT_CONFIG" "$COLOR_RESET"
LINT_OUT="$("$ANSIBLE_LINT_BIN" -c "$ANSIBLE_LINT_CONFIG" "$ROLE_ABS" 2>&1)"
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

# --- Stage 5: Molecule presence -------------------------------------------
[ "$AV_FORMAT" = "text" ] && printf "\n%b[5/5] Molecule configuration%b\n" "$COLOR_BLUE" "$COLOR_RESET"
if [ -d "$ROLE_ABS/molecule" ]; then
    if [ "$AV_FORMAT" = "text" ]; then
        printf "  %bok%b  molecule/ present. Scenarios:\n" "$COLOR_GREEN" "$COLOR_RESET"
        for scenario in "$ROLE_ABS"/molecule/*/; do
            [ -d "$scenario" ] && echo "        - $(basename "$scenario")"
        done
        echo "        Run one with: bash scripts/test_role.sh $ROLE_ABS <scenario>"
        echo "        This script does not run scenarios. See references/molecule.md"
        echo "        for the condition under which running one is correct."
    fi
elif [ "$AV_FORMAT" = "text" ]; then
    printf "  %b--%b  no molecule/ directory; scenario testing is not configured\n" "$COLOR_YELLOW" "$COLOR_RESET"
fi

av_summary "validate_role" "$ROLE_ABS"
exit $?
