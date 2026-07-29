#!/usr/bin/env bash
#
# setup_tools.sh - report which validation tools are present and whether each
# meets the floor stated in scripts/requirements.txt.
#
# The floors are enforced here, not merely printed. A tool that is present but
# older than its floor is a finding, because the checkers in this skill were
# measured against the floor and not against whatever is installed.
#
# Requires bash 4.0 or newer. Exit codes: 0 every required tool present and at
# or above its floor, 1 a tool is missing or below its floor, 2 python3 is
# absent so no version can be compared, 64 usage error.

set -uo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib/common.sh"

av_print_help() {
    cat <<'EOF'
setup_tools.sh - check the validation toolchain against its version floors.

Usage:
  bash scripts/setup_tools.sh [options]
  bash scripts/setup_tools.sh --self-test

What it asserts:
  ansible-core, ansible-playbook, ansible-lint, yamllint and PyYAML are
  installed and at or above the floor in scripts/requirements.txt.
  checkov and molecule are reported but do not gate, because a run without them
  is a narrower audit rather than an impossible one; the security and molecule
  scripts exit 2 on their own when they need a tool that is absent.

Re-derive the current release of any line with:
  python3 -m pip index versions <name>

EOF
    av_common_flag_help
}

run_self_test() {
    local here="$0"
    echo "self-test: setup_tools.sh"
    av_expect_exit 0 "--help exits clean" bash "$here" --help
    av_expect_exit 1 "a shadowed toolchain reports findings" env AV_NO_BOOTSTRAP=1 AV_UNAVAILABLE_TOOLS=ansible-lint bash "$here"
    av_self_test_summary
}

av_parse_common_flags "$@"

if [ "$AV_SELF_TEST" -eq 1 ]; then
    run_self_test
fi

command -v python3 >/dev/null 2>&1 || av_cannot_run "python3 is not on PATH; no version can be compared"

av_banner "Ansible validation toolchain"

REQ="$(av_requirements_file)"
[ -f "$REQ" ] || av_cannot_run "scripts/requirements.txt not found; the floors are not knowable"

version_of() {
    # AV_UNAVAILABLE_TOOLS is the same deliberate test hook scripts/lib/common.sh
    # documents: it makes the named tools report as absent so that --self-test
    # can exercise the missing-tool path without emptying PATH.
    case ",${AV_UNAVAILABLE_TOOLS:-}," in
        *",$1,"*) return 0 ;;
    esac
    case "$1" in
        ansible-core)   command -v ansible >/dev/null 2>&1 && ansible --version 2>/dev/null | head -1 | sed -E 's/.*core ([0-9][^ )]*).*/\1/' ;;
        ansible-playbook) command -v ansible-playbook >/dev/null 2>&1 && ansible-playbook --version 2>/dev/null | head -1 | sed -E 's/.*core ([0-9][^ )]*).*/\1/' ;;
        ansible-lint)   command -v ansible-lint >/dev/null 2>&1 && ansible-lint --version 2>/dev/null | head -1 | sed -E 's/^ansible-lint ([0-9][^ ]*).*/\1/' ;;
        yamllint)       command -v yamllint >/dev/null 2>&1 && yamllint --version 2>/dev/null | sed -E 's/^yamllint ([0-9].*)/\1/' ;;
        checkov)        command -v checkov >/dev/null 2>&1 && checkov --version 2>/dev/null | head -1 ;;
        molecule)       command -v molecule >/dev/null 2>&1 && molecule --version 2>/dev/null | head -1 | sed -E 's/^molecule ([0-9][^ ]*).*/\1/' ;;
        PyYAML)         python3 -c 'import yaml;print(yaml.__version__)' 2>/dev/null ;;
    esac
}

floor_of() {
    grep -E "^$1>=" "$REQ" 2>/dev/null | head -1 | sed -E "s/^$1>=//"
}

meets_floor() {
    # meets_floor <have> <floor>
    python3 - "$1" "$2" <<'PY'
import sys
def parts(v):
    out = []
    for chunk in v.replace('-', '.').split('.'):
        digits = ''.join(c for c in chunk if c.isdigit())
        out.append(int(digits) if digits else 0)
    return out
have, floor = parts(sys.argv[1]), parts(sys.argv[2])
n = max(len(have), len(floor))
have += [0] * (n - len(have))
floor += [0] * (n - len(floor))
sys.exit(0 if have >= floor else 1)
PY
}

check() {
    # check <display-name> <requirements-key> <required|optional>
    local name="$1" key="$2" mode="$3" have floor
    have="$(version_of "$name")"
    floor="$(floor_of "$key")"
    if [ -z "$have" ]; then
        if [ "$mode" = required ]; then
            av_add_error "$name is not installed (floor ${floor:-none})" "scripts/requirements.txt"
        else
            printf "  %b--%b  %s not installed (optional)\n" "$COLOR_YELLOW" "$COLOR_RESET" "$name"
        fi
        return
    fi
    if [ -n "$floor" ] && ! meets_floor "$have" "$floor"; then
        if [ "$mode" = required ]; then
            av_add_error "$name $have is below the floor $floor" "scripts/requirements.txt"
        else
            av_add_warning "$name $have is below the floor $floor" "scripts/requirements.txt"
        fi
        return
    fi
    printf "  %bok%b  %-18s %s%s\n" "$COLOR_GREEN" "$COLOR_RESET" "$name" "$have" "${floor:+  (floor $floor)}"
}

check ansible-core     ansible-core  required
check ansible-playbook ansible-core  required
check ansible-lint     ansible-lint  required
check yamllint         yamllint      required
check PyYAML           PyYAML        required
check checkov          checkov       optional
check molecule         molecule      optional

echo ""
PYVER="$(python3 -c 'import sys;print("%d.%d"%sys.version_info[:2])')"
echo "Control-node Python: $PYVER"
if python3 -c 'import sys;sys.exit(0 if sys.version_info[:2] >= (3,12) else 1)'; then
    printf "  %bok%b  ansible-core 2.20 and newer require Python 3.12 or newer; this node qualifies\n" "$COLOR_GREEN" "$COLOR_RESET"
else
    av_add_warning "Python $PYVER cannot install ansible-core 2.20 or newer, so pip resolves 2.19.x here. ansible-core 2.19 is on security-only support and reaches end of life in November 2026. Upgrade the control node to Python 3.12 or newer." "references/source-map.md"
fi

if [ $AV_ERRORS -gt 0 ] || [ $AV_WARNINGS -gt 0 ]; then
    cat <<'EOF'

Install or upgrade the toolchain with:
  python3 -m pip install --upgrade -r scripts/requirements.txt

Molecule is separate, because its driver lives in a plugin package:
  python3 -m pip install "molecule>=25.0" "molecule-plugins[docker]"

Do not install molecule-docker. Its last release was 2022-09-29 and the
official installation guide tells upgraders to uninstall it to avoid conflicts
with molecule-plugins. references/molecule.md records that with its source.

Install ansible-core, not the ansible community package, so that the toolchain
matches what the checkers resolve. The community package pulls roughly a
gigabyte of collections and changes which fqcn and syntax-check findings appear
at all; when a play needs a collection, declare it in requirements.yml.
EOF
fi

av_summary "setup_tools" "$(uname -s 2>/dev/null || echo unknown)"
exit $?
