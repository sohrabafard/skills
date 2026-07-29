#!/usr/bin/env bash
# Shared library for every ansible-validator script.
#
# Source it with:
#   source "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
#
# Interpreter requirement: bash 4.0 or newer. macOS ships bash 3.2 as
# /bin/bash; install a current bash (`brew install bash`) and invoke the
# scripts as `bash scripts/<name>.sh`, which resolves the newer bash from
# PATH. On Windows run them under Git Bash or WSL.
#
# Exit-code contract, identical in all ten scripts:
#   0   clean      - the check ran and found nothing
#   1   findings   - the check ran and found something the caller must fix
#   2   could not run - a required tool is missing, an input does not parse,
#                    or a target path does not exist
#   64  usage      - a missing or unrecognised argument
# A CI gate treats 2 as a hard stop, never as a pass.

# shellcheck shell=bash

if [ -n "${AV_COMMON_SOURCED:-}" ]; then
    return 0
fi
AV_COMMON_SOURCED=1

AV_EXIT_OK=0
AV_EXIT_FINDINGS=1
AV_EXIT_CANNOT_RUN=2
AV_EXIT_USAGE=64

# ---------------------------------------------------------------------------
# Colours. Disabled when stdout is not a terminal or NO_COLOR is set, so that
# captured output is plain text a grep or a log aggregator can read.
# ---------------------------------------------------------------------------
if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
    COLOR_GREEN='\033[0;32m'
    COLOR_YELLOW='\033[1;33m'
    COLOR_RED='\033[0;31m'
    COLOR_BLUE='\033[0;34m'
    COLOR_CYAN='\033[0;36m'
    COLOR_RESET='\033[0m'
else
    COLOR_GREEN=''
    COLOR_YELLOW=''
    COLOR_RED=''
    COLOR_BLUE=''
    COLOR_CYAN=''
    COLOR_RESET=''
fi

av_skill_dir() {
    # Resolves from the sourcing script's own location. Never from the caller's
    # working directory and never from a fixed number of parent hops.
    local lib_dir
    lib_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    cd "$lib_dir/../.." && pwd
}

AV_SKILL_DIR="${AV_SKILL_DIR:-$(av_skill_dir)}"
AV_SCRIPT_DIR="$AV_SKILL_DIR/scripts"

av_banner() {
    printf "%b========================================%b\n" "$COLOR_BLUE" "$COLOR_RESET"
    printf "%b%s%b\n" "$COLOR_BLUE" "$1" "$COLOR_RESET"
    printf "%b========================================%b\n" "$COLOR_BLUE" "$COLOR_RESET"
    echo ""
}

av_usage_error() {
    printf "%bUsage error: %s%b\n" "$COLOR_RED" "$1" "$COLOR_RESET" >&2
    echo "Run with --help for the full argument list." >&2
    exit $AV_EXIT_USAGE
}

av_cannot_run() {
    printf "%b[BLOCKED] %s%b\n" "$COLOR_RED" "$1" "$COLOR_RESET" >&2
    echo "This is exit 2: the check could not run. It is not a pass." >&2
    exit $AV_EXIT_CANNOT_RUN
}

# ---------------------------------------------------------------------------
# CRLF guard. A shell driver that reads a CRLF file leaves a carriage return on
# the last field of every parsed line, so every comparison fails while the
# rendered bytes look identical. Detect it and stop rather than report nonsense.
# ---------------------------------------------------------------------------
av_assert_no_crlf() {
    local file="$1"
    [ -f "$file" ] || return 0
    if LC_ALL=C grep -q $'\r' "$file" 2>/dev/null; then
        av_cannot_run "$file contains CRLF line endings. Convert it to LF (git config core.autocrlf input, or dos2unix) before validating; every field comparison in this toolchain reads the trailing carriage return as data."
    fi
}

# ---------------------------------------------------------------------------
# Virtual-environment bootstrap.
#
# The venv lives under the user cache directory, keyed by the hash of
# scripts/requirements.txt, so repeated invocations reuse it instead of paying
# a pip install per file reviewed. It is never created inside the repository,
# because the owner's mount is read-only in places and forbids unlink.
#
# Set AV_NO_BOOTSTRAP=1 to forbid the bootstrap entirely: a missing tool then
# exits 2 instead of reaching for the network. That is the correct setting in a
# locked-down CI runner.
# ---------------------------------------------------------------------------
AV_VENV=""

av_venv_bin() {
    # Windows venvs place executables in Scripts/, POSIX venvs in bin/.
    local venv="$1"
    if [ -d "$venv/Scripts" ]; then
        echo "$venv/Scripts"
    else
        echo "$venv/bin"
    fi
}

av_requirements_file() {
    echo "$AV_SCRIPT_DIR/requirements.txt"
}

av_cache_root() {
    local root="${AV_CACHE_DIR:-${XDG_CACHE_HOME:-$HOME/.cache}/ansible-validator}"
    echo "$root"
}

av_bootstrap() {
    # av_bootstrap <pip-spec...>
    # Creates or reuses the cached venv and sets AV_VENV. Returns non-zero when
    # the bootstrap is forbidden or impossible; the caller decides whether that
    # is exit 2.
    if [ -n "${AV_NO_BOOTSTRAP:-}" ]; then
        return 1
    fi
    command -v python3 >/dev/null 2>&1 || return 1

    local req key root venv bindir
    req="$(av_requirements_file)"
    if [ -f "$req" ]; then
        key="$(av_hash_file "$req")"
    else
        key="norequirements"
    fi
    root="$(av_cache_root)"
    venv="$root/venv-$key"
    bindir="$(av_venv_bin "$venv")"

    if [ -x "$bindir/python" ] || [ -x "$bindir/python.exe" ]; then
        AV_VENV="$venv"
        return 0
    fi

    mkdir -p "$root" || return 1
    echo "Creating a cached tool environment at $venv (first run only)..." >&2
    python3 -m venv "$venv" >&2 || return 1
    bindir="$(av_venv_bin "$venv")"
    "$bindir/python" -m pip install --quiet --upgrade pip >&2 || return 1
    if [ -f "$req" ]; then
        "$bindir/python" -m pip install --quiet -r "$req" >&2 || return 1
    else
        "$bindir/python" -m pip install --quiet "$@" >&2 || return 1
    fi
    AV_VENV="$venv"
    return 0
}

av_hash_file() {
    local f="$1"
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$f" | cut -c1-16
    elif command -v shasum >/dev/null 2>&1; then
        shasum -a 256 "$f" | cut -c1-16
    else
        python3 -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest()[:16])" "$f"
    fi
}

av_resolve_tool() {
    # av_resolve_tool <name> -> prints an invocable path, or nothing.
    # Prefers the system tool; falls back to the cached venv; bootstraps only
    # when AV_NO_BOOTSTRAP is unset.
    local name="$1" bindir
    # AV_UNAVAILABLE_TOOLS is a deliberate test hook, not a workaround. Each
    # script's --self-test uses it to exercise the "tool is missing" path and
    # assert exit 2, because emptying PATH would also remove the interpreter and
    # produce 127, and a self-test that cannot reach the code path it is testing
    # proves nothing. Set it to a comma-separated list of tool names.
    case ",${AV_UNAVAILABLE_TOOLS:-}," in
        *",$name,"*) return 1 ;;
    esac
    if command -v "$name" >/dev/null 2>&1; then
        command -v "$name"
        return 0
    fi
    if [ -n "$AV_VENV" ]; then
        bindir="$(av_venv_bin "$AV_VENV")"
        if [ -x "$bindir/$name" ]; then
            echo "$bindir/$name"
            return 0
        fi
    fi
    if av_bootstrap; then
        bindir="$(av_venv_bin "$AV_VENV")"
        if [ -x "$bindir/$name" ]; then
            echo "$bindir/$name"
            return 0
        fi
    fi
    return 1
}

# ---------------------------------------------------------------------------
# Configuration resolution. A caller must be able to override the skill's own
# lint configs, because a project with its own .ansible-lint is entitled to it.
# Precedence: explicit flag, then environment variable, then the project's file
# found by walking up from the target, then the skill's shipped asset.
# ---------------------------------------------------------------------------
AV_YAMLLINT_CONFIG=""
AV_ANSIBLE_LINT_CONFIG=""

av_find_project_config() {
    # av_find_project_config <start-dir> <filename>
    local dir="$1" name="$2"
    dir="$(cd "$dir" 2>/dev/null && pwd)" || return 1
    while [ -n "$dir" ] && [ "$dir" != "/" ]; do
        if [ -f "$dir/$name" ]; then
            echo "$dir/$name"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}

av_resolve_yamllint_config() {
    # av_resolve_yamllint_config <start-dir>
    local start="$1" found
    if [ -n "$AV_YAMLLINT_CONFIG" ]; then
        [ -f "$AV_YAMLLINT_CONFIG" ] || av_cannot_run "yamllint config not found: $AV_YAMLLINT_CONFIG"
        echo "$AV_YAMLLINT_CONFIG"
        return 0
    fi
    if [ -n "${ANSIBLE_VALIDATOR_YAMLLINT_CONFIG:-}" ]; then
        [ -f "$ANSIBLE_VALIDATOR_YAMLLINT_CONFIG" ] || av_cannot_run "yamllint config not found: $ANSIBLE_VALIDATOR_YAMLLINT_CONFIG"
        echo "$ANSIBLE_VALIDATOR_YAMLLINT_CONFIG"
        return 0
    fi
    if found="$(av_find_project_config "$start" .yamllint)"; then
        echo "$found"
        return 0
    fi
    echo "$AV_SKILL_DIR/assets/.yamllint"
}

av_resolve_ansible_lint_config() {
    local start="$1" found
    if [ -n "$AV_ANSIBLE_LINT_CONFIG" ]; then
        [ -f "$AV_ANSIBLE_LINT_CONFIG" ] || av_cannot_run "ansible-lint config not found: $AV_ANSIBLE_LINT_CONFIG"
        echo "$AV_ANSIBLE_LINT_CONFIG"
        return 0
    fi
    if [ -n "${ANSIBLE_VALIDATOR_ANSIBLE_LINT_CONFIG:-}" ]; then
        [ -f "$ANSIBLE_VALIDATOR_ANSIBLE_LINT_CONFIG" ] || av_cannot_run "ansible-lint config not found: $ANSIBLE_VALIDATOR_ANSIBLE_LINT_CONFIG"
        echo "$ANSIBLE_VALIDATOR_ANSIBLE_LINT_CONFIG"
        return 0
    fi
    if found="$(av_find_project_config "$start" .ansible-lint)"; then
        echo "$found"
        return 0
    fi
    echo "$AV_SKILL_DIR/assets/.ansible-lint"
}

# ---------------------------------------------------------------------------
# Shared option parsing. Consumes the flags every script accepts and leaves the
# positional arguments in AV_ARGS.
# ---------------------------------------------------------------------------
AV_ARGS=()
AV_SELF_TEST=0
AV_FORMAT="text"

av_parse_common_flags() {
    AV_ARGS=()
    while [ $# -gt 0 ]; do
        case "$1" in
            -h|--help)
                av_print_help
                exit $AV_EXIT_OK
                ;;
            --self-test)
                AV_SELF_TEST=1
                shift
                ;;
            --yamllint-config)
                [ $# -ge 2 ] || av_usage_error "--yamllint-config needs a path"
                AV_YAMLLINT_CONFIG="$2"
                shift 2
                ;;
            --ansible-lint-config)
                [ $# -ge 2 ] || av_usage_error "--ansible-lint-config needs a path"
                AV_ANSIBLE_LINT_CONFIG="$2"
                shift 2
                ;;
            --format)
                [ $# -ge 2 ] || av_usage_error "--format needs a value (text or json)"
                case "$2" in
                    text|json) AV_FORMAT="$2" ;;
                    *) av_usage_error "--format accepts text or json, got '$2'" ;;
                esac
                shift 2
                ;;
            --)
                shift
                while [ $# -gt 0 ]; do AV_ARGS+=("$1"); shift; done
                ;;
            -*)
                av_usage_error "unrecognised option '$1'"
                ;;
            *)
                AV_ARGS+=("$1")
                shift
                ;;
        esac
    done
}

av_common_flag_help() {
    cat <<'EOF'
Common options:
  -h, --help                    Print this help and exit 0.
      --self-test               Run this script against the fixtures under
                                test/ and assert the documented exit codes.
      --yamllint-config PATH    Use PATH instead of the resolved yamllint config.
      --ansible-lint-config PATH
                                Use PATH instead of the resolved ansible-lint config.
      --format text|json        Output shape. json emits one object with the
                                counts and the findings list.

Configuration resolution order: the flag, then
ANSIBLE_VALIDATOR_YAMLLINT_CONFIG / ANSIBLE_VALIDATOR_ANSIBLE_LINT_CONFIG,
then the nearest .yamllint / .ansible-lint found by walking up from the target,
then the skill's own assets/ copy.

Environment:
  AV_NO_BOOTSTRAP=1   Never create a tool environment. A missing tool exits 2.
  AV_CACHE_DIR=PATH   Where the cached tool environment lives. Defaults to
                      $XDG_CACHE_HOME/ansible-validator (never inside the repo).
  NO_COLOR=1          Plain output.

Exit codes: 0 clean, 1 findings, 2 could not run, 64 usage error.
EOF
}

# ---------------------------------------------------------------------------
# Findings accumulator and the shared summary block.
# ---------------------------------------------------------------------------
AV_ERRORS=0
AV_WARNINGS=0
AV_FINDINGS=()

av_add_error() {
    AV_ERRORS=$((AV_ERRORS + 1))
    AV_FINDINGS+=("ERROR|$1|${2:-}")
    printf "%b[ERROR]%b %s\n" "$COLOR_RED" "$COLOR_RESET" "$1"
}

av_add_warning() {
    AV_WARNINGS=$((AV_WARNINGS + 1))
    AV_FINDINGS+=("WARNING|$1|${2:-}")
    printf "%b[WARNING]%b %s\n" "$COLOR_YELLOW" "$COLOR_RESET" "$1"
}

av_json_escape() {
    python3 -c 'import json,sys;print(json.dumps(sys.stdin.read())[1:-1])' <<<"$1"
}

av_emit_json() {
    # av_emit_json <tool> <target>
    local tool="$1" target="$2" first=1 f level msg ref
    printf '{"tool":"%s","target":"%s","errors":%d,"warnings":%d,"findings":[' \
        "$tool" "$(av_json_escape "$target")" "$AV_ERRORS" "$AV_WARNINGS"
    for f in ${AV_FINDINGS+"${AV_FINDINGS[@]}"}; do
        level="${f%%|*}"
        msg="${f#*|}"
        ref="${msg#*|}"
        msg="${msg%%|*}"
        [ $first -eq 1 ] || printf ','
        first=0
        printf '{"level":"%s","message":"%s","reference":"%s"}' \
            "$level" "$(av_json_escape "$msg")" "$(av_json_escape "$ref")"
    done
    printf ']}\n'
}

av_summary() {
    # av_summary <title> <target>
    local title="$1" target="${2:-}"
    if [ "$AV_FORMAT" = "json" ]; then
        av_emit_json "$title" "$target"
    else
        echo ""
        av_banner "$title"
        if [ $AV_ERRORS -eq 0 ] && [ $AV_WARNINGS -eq 0 ]; then
            printf "%bPASS - no findings%b\n" "$COLOR_GREEN" "$COLOR_RESET"
        elif [ $AV_ERRORS -eq 0 ]; then
            printf "%bPASS with %d warning(s)%b\n" "$COLOR_YELLOW" "$AV_WARNINGS" "$COLOR_RESET"
        else
            printf "%bFAIL - %d error(s), %d warning(s)%b\n" "$COLOR_RED" "$AV_ERRORS" "$AV_WARNINGS" "$COLOR_RESET"
            echo ""
            echo "Remediation is cited per finding above. The failure-class index is"
            echo "references/failure-classes.md; the ruleset each finding is measured"
            echo "against is references/best_practices.md."
        fi
    fi
    if [ $AV_ERRORS -gt 0 ]; then
        return $AV_EXIT_FINDINGS
    fi
    return $AV_EXIT_OK
}

# ---------------------------------------------------------------------------
# Self-test helper. Runs a command and asserts its exit code.
# ---------------------------------------------------------------------------
AV_ST_PASS=0
AV_ST_FAIL=0
AV_ST_BLOCKED=0

av_expect_exit() {
    # av_expect_exit <expected> <label> <command...>
    local expected="$1" label="$2"
    shift 2
    local actual=0
    "$@" >/dev/null 2>&1 || actual=$?
    if [ "$actual" = "$expected" ]; then
        printf "  %bok%b   %s (exit %s)\n" "$COLOR_GREEN" "$COLOR_RESET" "$label" "$actual"
        AV_ST_PASS=$((AV_ST_PASS + 1))
    elif [ "$actual" = "$AV_EXIT_CANNOT_RUN" ] && [ "$expected" != "$AV_EXIT_CANNOT_RUN" ]; then
        # The assertion did not fail; it could not be evaluated, because the
        # script under test reported a missing tool. Recording that as a failure
        # is the defect this whole exit-code contract exists to prevent, so it is
        # counted separately and it makes the self-test exit 2, not 1.
        printf "  %bBLOCKED%b %s (expected exit %s, tool unavailable)\n" "$COLOR_YELLOW" "$COLOR_RESET" "$label" "$expected"
        AV_ST_BLOCKED=$((AV_ST_BLOCKED + 1))
    else
        printf "  %bFAIL%b %s (expected exit %s, got %s)\n" "$COLOR_RED" "$COLOR_RESET" "$label" "$expected" "$actual"
        AV_ST_FAIL=$((AV_ST_FAIL + 1))
    fi
}

av_self_test_summary() {
    echo ""
    if [ $AV_ST_FAIL -eq 0 ] && [ $AV_ST_BLOCKED -eq 0 ]; then
        printf "%bself-test: %d assertion(s) passed%b\n" "$COLOR_GREEN" "$AV_ST_PASS" "$COLOR_RESET"
        exit $AV_EXIT_OK
    fi
    if [ $AV_ST_FAIL -eq 0 ]; then
        printf "%bself-test: %d passed, %d BLOCKED by a missing tool%b\n" "$COLOR_YELLOW" "$AV_ST_PASS" "$AV_ST_BLOCKED" "$COLOR_RESET"
        printf "Install scripts/requirements.txt and run again. Nothing failed; nothing was proved either.\n"
        exit $AV_EXIT_CANNOT_RUN
    fi
    printf "%bself-test: %d passed, %d FAILED, %d blocked%b\n" "$COLOR_RED" "$AV_ST_PASS" "$AV_ST_FAIL" "$AV_ST_BLOCKED" "$COLOR_RESET"
    exit $AV_EXIT_FINDINGS
}

av_fixture_dir() {
    echo "$AV_SKILL_DIR/test"
}
