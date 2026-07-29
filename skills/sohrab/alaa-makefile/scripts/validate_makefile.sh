#!/usr/bin/env bash
#
# alaa-makefile — Makefile validator
#
# Interpreter requirement: GNU bash 4.2 or newer. On Windows run it under Git Bash
# or WSL; `cmd.exe` and PowerShell cannot execute it. The repository ships
# `.gitattributes` with `*.sh text eol=lf` so a Windows checkout with
# core.autocrlf=true does not leave a carriage return on the shebang line.
#
# Exit codes (the only contract callers may rely on):
#   0  clean      — every stage ran and reported no error and no warning
#   1  findings   — every stage ran and at least one error or warning was reported
#   2  could not run — a dependency, argument or input problem stopped the run
#
# Informational notes never change the exit code.
#
# Usage: bash validate_makefile.sh [OPTIONS] <Makefile>
#        bash validate_makefile.sh --help
#        bash validate_makefile.sh --self-test

set -euo pipefail

# Keep Python-based validators stable under Windows Git Bash and legacy consoles.
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8

SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIXTURE_DIR="${SCRIPT_DIR}/fixtures"

# ------------------------------------------------------------------
# Pinned values. Each one states the command that re-derives it, so a
# later reader checks rather than trusts. Verified 2026-07-29.
# ------------------------------------------------------------------
GNU_MAKE_CURRENT="4.4.1"   # re-derive: curl -s https://ftp.gnu.org/gnu/make/ | grep -o 'make-[0-9][0-9.]*\.tar\.gz' | sort -V | tail -1
GNU_MAKE_44_FLOOR="4.4"    # .WAIT, .NOTPARALLEL with prerequisites, .NOTINTERMEDIATE, $(let ...), $(intcmp ...)
MBAKE_CURRENT="1.4.6"      # re-derive: curl -s https://pypi.org/pypi/mbake/json | python3 -c 'import json,sys;print(json.load(sys.stdin)["info"]["version"])'

EXIT_CLEAN=0
EXIT_FINDINGS=1
EXIT_CANNOT_RUN=2

if [ -n "${NO_COLOR:-}" ] || [ ! -t 1 ]; then
    RED=''; YELLOW=''; GREEN=''; BLUE=''; NC=''
else
    RED='\033[0;31m'; YELLOW='\033[1;33m'; GREEN='\033[0;32m'; BLUE='\033[0;34m'; NC='\033[0m'
fi

ERRORS=0
WARNINGS=0
INFO=0

USE_VENV=1
RUN_MBAKE=1
FLEET_CHECKS=1
MBAKE_BIN="${MBAKE_BIN:-}"
VENV_DIR="${TMPDIR:-/tmp}/alaa-makefile-venv-$$"
WORK_DIR="${TMPDIR:-/tmp}/alaa-makefile-work-$$"
CLEANUP_DONE=0

cleanup() {
    if [ "$CLEANUP_DONE" -eq 0 ]; then
        CLEANUP_DONE=1
        if [ -d "$VENV_DIR" ] && [[ "$VENV_DIR" == */alaa-makefile-venv-* ]]; then
            rm -rf "$VENV_DIR"
        fi
        if [ -d "$WORK_DIR" ] && [[ "$WORK_DIR" == */alaa-makefile-work-* ]]; then
            rm -rf "$WORK_DIR"
        fi
    fi
}
trap cleanup EXIT INT TERM

# Every could-not-run path goes through here so exit 2 is never confused with a verdict.
cannot_run() {
    printf '%b[CANNOT RUN]%b %s\n' "$RED" "$NC" "$1" >&2
    exit "$EXIT_CANNOT_RUN"
}

count_error()   { ERRORS=$((ERRORS + 1)); }
count_warning() { WARNINGS=$((WARNINGS + 1)); }
count_info()    { INFO=$((INFO + 1)); }

say_error()   { printf '%b✗%b %s\n' "$RED" "$NC" "$1"; count_error; }
say_warning() { printf '%b⚠%b %s\n' "$YELLOW" "$NC" "$1"; count_warning; }
say_info()    { printf '%bℹ%b %s\n' "$BLUE" "$NC" "$1"; count_info; }
say_ok()      { printf '%b✓%b %s\n' "$GREEN" "$NC" "$1"; }
detail()      { printf '   %s\n' "$1"; }

print_header() {
    echo ""
    echo "========================================"
    echo "$1"
    echo "========================================"
}

print_subheader() { printf '\n%b[%s]%b\n' "$BLUE" "$1" "$NC"; }

usage() {
    cat <<EOF
Usage: ${SCRIPT_NAME} [OPTIONS] <Makefile>

Validate a Makefile for syntax, recipe failure behaviour, credential leakage,
parallel safety and fleet-boundary violations.

Options:
  -h, --help          Show this help and exit 0.
      --self-test     Run every check against the fixtures in scripts/fixtures/
                      and assert the expected exit code for each. Exits 0 when
                      all assertions hold, 1 when any assertion fails, 2 when the
                      fixtures are missing.
      --no-venv       Do not create a virtual environment and do not run pip.
                      Use \$MBAKE_BIN if it is set and executable, otherwise the
                      mbake on PATH, otherwise skip the mbake stages.
      --skip-mbake    Do not run mbake at all. Implies --no-venv.
      --no-fleet-checks
                      Disable the checks that compare a recipe against the
                      commands owned by service-ci-kit and service-runtime-kit.
                      Use this on a repository that is not on this fleet.

Environment:
  MBAKE_BIN           Absolute path to an mbake executable. Honoured with
                      --no-venv; skips the 20-40s pip install on a prepared image.
  NO_COLOR            Any non-empty value disables colour (https://no-color.org/).
  TMPDIR              Where the venv and the scratch index are created. Nothing
                      is ever written inside the repository being validated.

Exit codes:
  0  clean          every stage ran; no error and no warning
  1  findings       every stage ran; at least one error or warning
  2  could not run  missing dependency, unreadable input, or bad arguments

Version anchors checked on 2026-07-29 (re-derivation commands are in the header
of this script and in references/SOURCES.md):
  GNU Make current stable  ${GNU_MAKE_CURRENT}
  mbake current release    ${MBAKE_CURRENT}

Examples:
  bash ${SCRIPT_NAME} Makefile
  bash ${SCRIPT_NAME} --no-venv build.mk
  MBAKE_BIN=/usr/local/bin/mbake bash ${SCRIPT_NAME} --no-venv Makefile
  bash ${SCRIPT_NAME} --self-test
EOF
}

# ------------------------------------------------------------------
# Dependencies
# ------------------------------------------------------------------
PYTHON_CMD=()
HAVE_MAKE=0

check_dependencies() {
    if command -v make >/dev/null 2>&1; then
        HAVE_MAKE=1
    else
        say_info "GNU make is not installed; the syntax stage and the version-floor stage are skipped."
    fi

    if [ "$RUN_MBAKE" -eq 0 ]; then
        return 0
    fi

    if [ "$USE_VENV" -eq 1 ]; then
        if command -v python3 >/dev/null 2>&1; then
            PYTHON_CMD=(python3)
        elif command -v python >/dev/null 2>&1; then
            PYTHON_CMD=(python)
        elif command -v py >/dev/null 2>&1; then
            PYTHON_CMD=(py -3)
        else
            cannot_run "python3, python or 'py -3' is required to install mbake. Re-run with --no-venv or --skip-mbake."
        fi
    fi
}

resolve_existing_mbake() {
    if [ -n "$MBAKE_BIN" ]; then
        if [ -x "$MBAKE_BIN" ]; then
            return 0
        fi
        cannot_run "MBAKE_BIN is set to '$MBAKE_BIN' but that path is not executable."
    fi
    if command -v mbake >/dev/null 2>&1; then
        MBAKE_BIN="$(command -v mbake)"
        return 0
    fi
    return 1
}

setup_mbake() {
    if [ "$RUN_MBAKE" -eq 0 ]; then
        return 0
    fi

    if [ "$USE_VENV" -eq 0 ]; then
        if resolve_existing_mbake; then
            say_ok "Using existing mbake: $MBAKE_BIN"
        else
            RUN_MBAKE=0
            say_info "mbake is not available and --no-venv forbids installing it; the two mbake stages are skipped."
            detail "Install it with 'pip install mbake' or set MBAKE_BIN to an existing executable."
        fi
        return 0
    fi

    print_subheader "ENVIRONMENT SETUP"
    echo "Creating temporary venv at: $VENV_DIR"
    "${PYTHON_CMD[@]}" -m venv "$VENV_DIR" >/dev/null 2>&1 || cannot_run "Failed to create the virtual environment at $VENV_DIR."

    local venv_python=""
    for candidate in "$VENV_DIR/bin/python" "$VENV_DIR/Scripts/python.exe" "$VENV_DIR/Scripts/python"; do
        if [ -x "$candidate" ]; then venv_python="$candidate"; break; fi
    done
    [ -n "$venv_python" ] || cannot_run "Failed to locate Python inside the virtual environment."

    echo "Installing mbake..."
    "$venv_python" -m pip install --quiet mbake >/dev/null 2>&1 || cannot_run "Failed to install mbake. Re-run with --no-venv on an offline machine."

    for candidate in "$VENV_DIR/bin/mbake" "$VENV_DIR/Scripts/mbake.exe" "$VENV_DIR/Scripts/mbake"; do
        if [ -x "$candidate" ]; then MBAKE_BIN="$candidate"; break; fi
    done
    [ -n "$MBAKE_BIN" ] || cannot_run "Failed to locate mbake inside the virtual environment."
    say_ok "Environment ready"
}

# ------------------------------------------------------------------
# Input validation
# ------------------------------------------------------------------
validate_file() {
    local file=$1
    [ -e "$file" ] || cannot_run "File not found: $file"
    [ -f "$file" ] || cannot_run "Not a regular file: $file"
    [ -r "$file" ] || cannot_run "File not readable: $file"
    [ -s "$file" ] || cannot_run "File is empty, so there is nothing to validate: $file"
}

# ------------------------------------------------------------------
# Recipe index
#
# Historic defect: six checks were written as grep -E "^\t..." inside double
# quotes, where \t is the letter t and not a tab, so every check that inspected
# a recipe line was dead. They are repaired here by building the recipe index
# once with awk, which knows what a recipe line actually is, and then matching
# against the index. The index also carries the owning target, which the
# per-target checks need and grep could never supply.
#
# Index record: RECIPE<TAB>lineno<TAB>target<TAB>text-with-leading-tab-removed
#               SPACEREC<TAB>lineno<TAB>target<TAB>text
#               RULE<TAB>lineno<TAB>target<TAB>prerequisites
# ------------------------------------------------------------------
INDEX_FILE=""

build_index() {
    local file=$1
    mkdir -p "$WORK_DIR" || cannot_run "Cannot create the scratch directory $WORK_DIR."
    INDEX_FILE="$WORK_DIR/index.tsv"

    awk '
    function is_conditional(s) {
        return (s ~ /^[ ]*(ifeq|ifneq|ifdef|ifndef|else|endif|include|-include|sinclude|define|endef|export|unexport|vpath|override)([ (]|$)/)
    }
    BEGIN { rule=""; cont=0 }
    {
        line=$0
        sub(/\r$/, "", line)

        if (cont) {
            cont = (line ~ /\\$/) ? 1 : 0
            next
        }

        if (line ~ /^\t/) {
            if (rule != "") {
                text=line
                sub(/^\t/, "", text)
                printf "RECIPE\t%d\t%s\t%s\n", NR, rule, text
            }
            if (line ~ /\\$/) cont=1
            next
        }

        if (line ~ /^[ \t]*$/) next          # a blank line does not end recipe context
        if (line ~ /^#/) next                # nor does a comment line

        if (line ~ /^[ ]+[^ ]/) {            # space-indented, not tab-indented
            if (rule != "" && !is_conditional(line)) {
                text=line
                sub(/^[ ]+/, "", text)
                printf "SPACEREC\t%d\t%s\t%s\n", NR, rule, text
            }
            if (line ~ /\\$/) cont=1
            next
        }

        # A non-tab, non-blank, non-comment line ends the current recipe context.
        rule=""
        if (!is_conditional(line) && line ~ /:/ && line !~ /^[^:]*[:?+!]=/) {
            name=line
            sub(/:.*$/, "", name)
            gsub(/[ \t]+$/, "", name)
            prereq=line
            sub(/^[^:]*:+/, "", prereq)
            sub(/^[ \t]+/, "", prereq)
            if (name != "") {
                printf "RULE\t%d\t%s\t%s\n", NR, name, prereq
                rule=name
            }
        }
        if (line ~ /\\$/) cont=1
    }
    ' "$file" > "$INDEX_FILE" || cannot_run "Failed to build the recipe index for $file."
}

# Recipe text for every target, one per line.
recipe_lines() { awk -F'\t' '$1=="RECIPE"{print $4}' "$INDEX_FILE"; }
# "lineno: text" for reporting.
recipe_report() { awk -F'\t' '$1=="RECIPE"{printf "%s: %s\n", $2, $4}' "$INDEX_FILE"; }
space_report()  { awk -F'\t' '$1=="SPACEREC"{printf "%s: %s\n", $2, $4}' "$INDEX_FILE"; }

# ------------------------------------------------------------------
# Line endings — the second Windows defect class named in the brief.
# A recipe line ending in CR passes the CR to the shell as part of the last
# argument, so `bash script.sh\r` fails with a message that shows no CR.
# ------------------------------------------------------------------
line_ending_check() {
    local file=$1
    print_subheader "LINE ENDINGS"
    if LC_ALL=C grep -q $'\r' "$file"; then
        say_error "The file contains carriage returns (CRLF or CR line endings)."
        detail "GNU make passes the trailing CR to the shell, so a recipe fails with a message whose bytes look correct."
        detail "Fix: run 'sed -i \$'s/\\r\$//' $file' and add '*.mk text eol=lf' plus 'Makefile text eol=lf' to .gitattributes."
    else
        say_ok "LF line endings throughout"
    fi
}

# ------------------------------------------------------------------
# Syntax
#
# Historic defect: any non-zero exit from `make -n` was reported as
# "Syntax errors detected", so a correct Makefile validated in a checkout whose
# sources are not materialised got a hard error. A missing prerequisite is not a
# syntax error, and it is now reported as such.
# ------------------------------------------------------------------
syntax_check() {
    local file=$1
    print_subheader "SYNTAX CHECK (GNU make)"

    if [ "$HAVE_MAKE" -eq 0 ]; then
        say_info "Skipped — GNU make is not installed."
        return 0
    fi

    local abs_file dir name out rc
    abs_file="$(cd "$(dirname "$file")" && pwd)/$(basename "$file")"
    dir="$(dirname "$abs_file")"
    name="$(basename "$abs_file")"

    set +e
    out="$( (cd "$dir" && make -f "$name" --dry-run) 2>&1 )"
    rc=$?
    set -e

    if [ "$rc" -eq 0 ]; then
        say_ok "No syntax errors found"
        return 0
    fi

    if printf '%s' "$out" | grep -qE "missing separator|unterminated|unexpected|commands commence before first target|extraneous|references itself|Circular"; then
        say_error "Syntax errors detected:"
        printf '%s\n' "$out" | head -20
        return 0
    fi

    if printf '%s' "$out" | grep -qE "No rule to make target|No such file or directory"; then
        say_info "make --dry-run stopped on a prerequisite that does not exist in this checkout. That is not a syntax error."
        printf '%s\n' "$out" | head -5
        return 0
    fi

    say_warning "make --dry-run exited $rc for a reason this checker does not classify:"
    printf '%s\n' "$out" | head -20
}

# ------------------------------------------------------------------
# mbake
# ------------------------------------------------------------------
mbake_validation() {
    local file=$1
    [ "$RUN_MBAKE" -eq 1 ] || return 0
    print_subheader "MBAKE VALIDATION"
    local out rc
    set +e
    out="$("$MBAKE_BIN" validate "$file" 2>&1)"
    rc=$?
    set -e
    if [ "$rc" -eq 0 ]; then
        say_ok "mbake validation passed"
    else
        say_error "mbake validation failed (exit $rc):"
        printf '%s\n' "$out" | head -20
    fi
}

mbake_format_check() {
    local file=$1
    [ "$RUN_MBAKE" -eq 1 ] || return 0
    print_subheader "MBAKE FORMAT CHECK"

    local out rc oneline cleaned
    set +e
    out="$("$MBAKE_BIN" format --check "$file" 2>&1)"
    rc=$?
    set -e
    oneline="$(printf '%s' "$out" | tr '\n' ' ' | tr -s ' ')"

    # Known mbake limitation: it does not recognise these GNU Make special targets.
    # Documented in references/mbake-tool.md; do not treat as a finding.
    cleaned="$(printf '%s' "$oneline" | sed -E "s/[^ ]*:[0-9]+: Error: Unknown special target '\.[A-Z_]+'//g")"

    if [ "$rc" -eq 0 ]; then
        say_ok "Formatting is consistent"
        return 0
    fi
    if printf '%s' "$oneline" | grep -q "Would reformat:"; then
        # Known mbake 1.4.6 defect: `mbake format` deletes the final newline, so
        # every POSIX-conformant Makefile fails `mbake format --check` with a
        # "Would reformat" whose only change is that newline. Reproduce with:
        #   printf '.PHONY: all\nall:\n\t@echo hi\n' > /tmp/m.mk
        #   mbake format --check /tmp/m.mk   # exit 1
        #   mbake format /tmp/m.mk && mbake format --check /tmp/m.mk   # exit 0
        # Documented in references/mbake-tool.md. Establish whether the newline is
        # the only difference before turning it into a finding.
        local copy="$WORK_DIR/mbake-roundtrip.mk"
        cp "$file" "$copy" 2>/dev/null || true
        "$MBAKE_BIN" format "$copy" >/dev/null 2>&1 || true
        if [ -f "$copy" ] && [ "$(sed -e '$a\' "$file" | cksum)" = "$(sed -e '$a\' "$copy" | cksum)" ]; then
            say_info "mbake would rewrite this file only by deleting its final newline, which is an mbake 1.4.6 defect, not a Makefile defect."
            detail "See references/mbake-tool.md. Do not 'fix' it; a text file ends with a newline."
            return 0
        fi
        say_warning "mbake would reformat this file."
        printf '%s\n' "$out" | grep -v "Unknown special target" | grep -v '^$' | head -10 || true
        detail "Preview with 'mbake format --diff $file' and apply with 'mbake format $file'."
        return 0
    fi
    if printf '%s' "$cleaned" | grep -qE "Error:|Fatal error"; then
        say_warning "mbake reported an error that is not a known false positive:"
        printf '%s\n' "$out" | grep -v "Unknown special target" | grep -v '^$' | head -10 || true
        return 0
    fi
    say_ok "Formatting is consistent"
    detail "mbake reported only unknown special targets, which is a known mbake limitation."
}

# ------------------------------------------------------------------
# Structural checks — the file as a whole
# ------------------------------------------------------------------
structural_checks() {
    local file=$1
    print_subheader "STRUCTURE AND PREAMBLE"
    local found=0

    if ! grep -q "^\.DELETE_ON_ERROR:" "$file"; then
        say_warning "Missing .DELETE_ON_ERROR"
        detail "Without it a failed recipe leaves a partial target file, which the next run treats as up to date."
        detail "Fix: add '.DELETE_ON_ERROR:' to the preamble. Owner: references/makefile-structure.md."
        found=1
    fi

    if ! grep -qE "^SHELL[[:space:]]*:?=[[:space:]]*(bash|/bin/bash|/usr/bin/bash|/usr/bin/env bash)" "$file"; then
        say_info "No explicit 'SHELL := bash'"
        detail "Recipes then run under /bin/sh, which on Debian and Alpine is not bash."
        found=1
    fi

    if ! grep -q -- "MAKEFLAGS.*--warn-undefined-variables" "$file"; then
        say_info "Missing 'MAKEFLAGS += --warn-undefined-variables'"
        found=1
    fi
    if ! grep -q -- "MAKEFLAGS.*--no-builtin-rules" "$file"; then
        say_info "Missing 'MAKEFLAGS += --no-builtin-rules'"
        found=1
    fi

    if ! grep -q "^\.PHONY:" "$file"; then
        say_warning "No .PHONY declaration"
        detail "A target that creates no file and is not declared phony stops running as soon as a file of that name exists."
        detail "Owner: references/targets-guide.md."
        found=1
    fi

    if grep -q "^\.EXPORT_ALL_VARIABLES:" "$file"; then
        say_warning ".EXPORT_ALL_VARIABLES exports every Make variable to every subprocess, including any that holds a credential."
        detail "Fix: delete it and 'export' the specific variables the recipes need."
        found=1
    fi

    # Historic check :382. The pattern was written in double quotes, so bash removed
    # the backslash before $ and grep -E then read $ as an end-of-line anchor and
    # never matched. Single-quoted here.
    local shell_lines
    shell_lines="$(grep -nE '^[[:space:]]*[A-Za-z_][A-Za-z0-9_]*[[:space:]]*=[[:space:]]*\$\(shell' "$file" | head -5)" || true
    if [ -n "$shell_lines" ]; then
        say_warning "Recursive assignment '=' holding \$(shell ...): the shell command re-runs on every reference."
        printf '%s\n' "$shell_lines"
        detail "Fix: use ':=' so the command runs once. Owner: references/variables-guide.md."
        found=1
    fi

    # Documented default target (retained from the previous revision, informational).
    if ! grep -qE "^##?.*(([Dd]efault|[Mm]ain|[Ff]irst).*target|target.*(default|main)|\(default\))" "$file"; then
        if ! grep -B1 "^all:" "$file" 2>/dev/null | grep -qE "^##"; then
            say_info "The default target carries no '##' documentation line, so 'make help' cannot describe it."
            found=1
        fi
    fi

    # Built-in rule search (retained from the previous revision, informational).
    if grep -qE "^%\." "$file" || grep -qE "^\.[a-z]+\.[a-z]+:" "$file"; then
        if ! grep -q "^\.SUFFIXES:" "$file"; then
            say_info "Pattern or suffix rules are present and '.SUFFIXES:' is absent, so make searches its built-in suffix rules for every target."
            found=1
        fi
    fi

    # Intermediate file handling (retained from the previous revision, informational).
    if grep -E "\.o|\.tmp|\.temp" "$file" | grep -q ":"; then
        if ! grep -qE "^\.(INTERMEDIATE|SECONDARY|NOTINTERMEDIATE):" "$file"; then
            say_info "Intermediate files (.o, .tmp, .temp) appear as targets and none of .INTERMEDIATE, .SECONDARY or .NOTINTERMEDIATE is declared."
            detail "GNU Make ${GNU_MAKE_44_FLOOR}+ adds .NOTINTERMEDIATE to keep a file that make would otherwise delete after use."
            found=1
        fi
    fi

    local cred_lines
    cred_lines="$(grep -niE '(password|secret|api[_-]?key|apikey|token|private[_-]?key|aws_access_key|aws_secret_access_key|github_token|auth_token|credentials|azure_client_secret|database_url|db_password|ssh_key|ssl_key|encryption_key)[[:space:]]*[:?]?=' "$file" | grep -vE '^[0-9]+:[[:space:]]*#' | grep -vE '\?=[[:space:]]*\$\(error' | head -5)" || true
    if [ -n "$cred_lines" ]; then
        say_error "Credential-shaped assignment in the Makefile:"
        printf '%s\n' "$cred_lines"
        detail "Fix: read the value from the environment and fail closed when it is absent:"
        detail "  API_TOKEN ?= \$(error API_TOKEN is not set)"
        detail "Owner: references/security-guide.md."
        found=1
    fi

    if [ "$found" -eq 0 ]; then
        say_ok "Preamble and structure are complete"
    fi
}

# ------------------------------------------------------------------
# Recipe checks — every one of these was dead before this revision
# ------------------------------------------------------------------
recipe_checks() {
    local file=$1
    print_subheader "RECIPE BEHAVIOUR"
    local found=0

    # --- spaces where a tab belongs (historic check :306) ------------------
    # The old pattern matched any 2/4/8-space indent anywhere in the file, so a
    # legal variable line continuation was reported as an error and the file was
    # failed. It also missed 1, 3, 5, 6 and 7 space indents. The index only marks
    # a space-indented line when a recipe is genuinely open at that point.
    local space_lines
    space_lines="$(space_report | head -5)"
    if [ -n "$space_lines" ]; then
        say_error "Recipe lines indented with spaces instead of a tab:"
        printf '%s\n' "$space_lines"
        detail "Fix: replace the leading spaces with one tab character, or run 'mbake format' on the file."
        found=1
    fi

    # --- .ONESHELL without -e (historic checks :454, :456) ------------------
    # This is the fleet's most dangerous silent-success mode. With .ONESHELL the
    # whole recipe is one shell invocation and only the LAST command's status is
    # the recipe's status, so an earlier failure is discarded and make exits 0.
    if grep -q "^\.ONESHELL:" "$file"; then
        local flags_line=""
        flags_line="$(grep -E "^\.SHELLFLAGS[[:space:]]*:?=" "$file" | head -1)" || true
        if [ -z "$flags_line" ]; then
            say_error ".ONESHELL is set and .SHELLFLAGS is absent."
            detail "Every recipe becomes one shell invocation whose status is the status of its LAST command, so an earlier failure exits 0."
            detail "Fix: add '.SHELLFLAGS := -eu -o pipefail -c'."
            found=1
        elif ! printf '%s' "$flags_line" | grep -qE '(^|[[:space:]])-[a-zA-Z]*e'; then
            say_error ".ONESHELL is set and .SHELLFLAGS does not contain -e: $flags_line"
            detail "Without -e a command that fails part way through a recipe is ignored and the target reports success."
            detail "Fix: '.SHELLFLAGS := -eu -o pipefail -c'."
            found=1
        else
            if ! printf '%s' "$flags_line" | grep -qE '(^|[[:space:]])-[a-zA-Z]*u'; then
                say_info ".SHELLFLAGS has -e but not -u, so an unset variable expands to the empty string instead of failing."
                found=1
            fi
            if ! printf '%s' "$flags_line" | grep -q "pipefail"; then
                say_info ".SHELLFLAGS has -e but not -o pipefail, so a failure anywhere but the last stage of a pipe is discarded."
                found=1
            fi
        fi
    fi

    # --- leading '-' and '|| true' (new) ------------------------------------
    # The '-' prefix tells make to ignore the command's exit status. On a target
    # that fronts a gate this converts a red gate into a green one. The previous
    # revision of this script recommended the '-' prefix as error control; that
    # recommendation is removed because it produces the defect it claims to fix.
    local dash_lines gate_dash
    dash_lines="$(awk -F'\t' '$1=="RECIPE" && $4 ~ /^-[^-]/ {printf "%s: %s\n", $2, $4}' "$INDEX_FILE")"
    gate_dash="$(printf '%s' "$dash_lines" | grep -E 'ci/scripts/|scripts/[a-z-]+\.sh|docker compose|docker-compose|\$\(MAKE\)' || true)"
    if [ -n "$gate_dash" ]; then
        say_error "A recipe line that invokes a gate command is prefixed with '-', so its exit status is discarded:"
        printf '%s\n' "$gate_dash" | head -5
        detail "Fix: delete the '-'. A target that fronts a gate must exit with the gate's status unmodified."
        detail "Owner: references/ci-entrypoint.md."
        found=1
    elif [ -n "$dash_lines" ]; then
        say_warning "Recipe lines prefixed with '-' discard their exit status:"
        printf '%s\n' "$dash_lines" | head -5
        detail "Fix: delete the '-' and make the command tolerate the condition itself, for example 'rm -rf build' with -f, or 'docker rmi x 2>/dev/null || exit 0' when absence is genuinely acceptable."
        found=1
    fi

    local ortrue
    ortrue="$(awk -F'\t' '$1=="RECIPE"{printf "%s: %s\n", $2, $4}' "$INDEX_FILE" | grep -E '(ci/scripts/[a-z_]+\.sh|scripts/[a-z-]+\.sh|docker compose|\$\(MAKE\)).*\|\|[[:space:]]*true' || true)"
    if [ -n "$ortrue" ]; then
        say_error "A gate command is followed by '|| true', which converts every failure into success:"
        printf '%s\n' "$ortrue" | head -5
        detail "Fix: delete '|| true'. Owner: references/ci-entrypoint.md."
        found=1
    fi

    # --- semicolon chaining (historic check :351, re-scoped) ----------------
    # The old check fired whenever any target name began with the letter t and
    # never otherwise, and its message recommended the '-' prefix. Restated as
    # the condition that is actually a defect: commands chained with ';' on one
    # recipe line, where the status of everything but the last is discarded.
    local semi
    semi="$(awk -F'\t' '$1=="RECIPE"{printf "%s: %s\n", $2, $4}' "$INDEX_FILE" | grep -E '[^;];[[:space:]]*[a-zA-Z@$_./]' | grep -vE '(&&|set -e|for |while |case |done|esac|then|fi;|;;)' || true)"
    if [ -n "$semi" ]; then
        say_warning "Commands chained with ';' on one recipe line discard the status of every command but the last:"
        printf '%s\n' "$semi" | head -5
        detail "Fix: chain with '&&', or open the line with 'set -e;'."
        found=1
    fi

    # --- bash-only constructs without SHELL := bash (new) -------------------
    # SKILL.md frames the /bin/sh versus bash decision; this is the check that
    # enforces the consequence of getting it wrong.
    if ! grep -qE "^SHELL[[:space:]]*:?=[[:space:]]*(bash|/bin/bash|/usr/bin/bash|/usr/bin/env bash)" "$file"; then
        local bashisms
        bashisms="$(awk -F'\t' '$1=="RECIPE"{printf "%s: %s\n", $2, $4}' "$INDEX_FILE" | grep -E '(^|[^a-zA-Z])(source[[:space:]]|declare[[:space:]]+-|local[[:space:]]|mapfile|readarray)|\[\[|<<<|\$\{[A-Za-z_]+\[|\bpushd\b|\bpopd\b|-o[[:space:]]+pipefail' || true)"
        if [ -n "$bashisms" ]; then
            say_error "Recipes use bash-only constructs while SHELL is not set to bash, so they run under /bin/sh and fail:"
            printf '%s\n' "$bashisms" | head -5
            detail "Fix: either add 'SHELL := bash' to the preamble, or rewrite the construct in POSIX shell ('.' instead of 'source', no '[[', no arrays)."
            detail "Owner for the shell logic itself: /alaa-bash-shell (\$alaa-bash-shell)."
            found=1
        fi
    fi

    # --- bare make instead of $(MAKE) (historic check :405) -----------------
    local make_lines
    make_lines="$(awk -F'\t' '$1=="RECIPE"{printf "%s: %s\n", $2, $4}' "$INDEX_FILE" \
        | grep -E '(^|[^a-zA-Z0-9_/$(-])make[[:space:]]' \
        | grep -vE '(echo|printf|\$\(MAKE\)|"[^"]*make[^"]*"|'"'"'[^'"'"']*make[^'"'"']*'"'"')' || true)"
    if [ -n "$make_lines" ]; then
        say_warning "Bare 'make' in a recipe instead of \$(MAKE):"
        printf '%s\n' "$make_lines" | head -5
        detail "Fix: use '\$(MAKE)'. Bare make loses -j, -n and the jobserver, so a dry run executes for real and a parallel build serialises."
        found=1
    fi

    # --- mkdir -p without an order-only prerequisite (historic check :500) ---
    if recipe_lines | grep -qE 'mkdir[[:space:]]+(-p|-[a-z]*p)'; then
        if ! grep -qE '\|[[:space:]]*\$?\(?[A-Za-z_]' "$file"; then
            say_info "Recipes create directories with 'mkdir -p' and no rule uses an order-only prerequisite."
            detail "A directory's timestamp changes whenever a file is written into it, so a normal prerequisite on a directory rebuilds the target on every run."
            detail "Fix: '\$(BUILD_DIR)/app: \$(SOURCES) | \$(BUILD_DIR)'. Owner: references/targets-guide.md."
            found=1
        fi
    fi

    # --- parallel-unsafe commands without .NOTPARALLEL (historic check :514) -
    if recipe_lines | grep -qE '(docker build|docker buildx build|npm (ci|install)|pip install|yarn install|bundle install|composer install)'; then
        if ! grep -q "^\.NOTPARALLEL" "$file"; then
            say_info "Recipes run a command that writes to a shared cache (a package installer or an image build) and .NOTPARALLEL is absent."
            detail "Under 'make -j' two such recipes corrupt the shared cache."
            detail "Fix: '.NOTPARALLEL: <those targets>' on GNU Make ${GNU_MAKE_44_FLOOR}+, or give the targets a common prerequisite on older releases. Owner: references/optimization-guide.md."
            found=1
        fi
    fi

    # --- dangerous commands driven by an undefined variable ------------------
    local unsafe=""
    while IFS= read -r line; do
        local var_name
        var_name="$(printf '%s' "$line" | grep -oE '\$\([A-Z_][A-Z0-9_]*\)' | head -1 | tr -d '$()')" || true
        if [ -n "$var_name" ] && ! grep -qE "^${var_name}[[:space:]]*[:?+]?=" "$file"; then
            unsafe="${unsafe}${line}"$'\n'
        fi
    done < <(recipe_lines | grep -E '(rm -rf|sudo |curl |wget )' || true)
    if [ -n "$unsafe" ]; then
        say_warning "A destructive or network command is driven by a variable that this file never defines:"
        printf '%s' "$unsafe" | head -5
        detail "Fix: give the variable a default with ':=' or fail closed with '?= \$(error NAME is not set)'."
        found=1
    fi

    if [ "$found" -eq 0 ]; then
        say_ok "Recipe failure behaviour is sound"
    fi
}

# ------------------------------------------------------------------
# Fleet boundary check — the executable form of this skill's boundary sentence.
# A Make target is a local invocation of a command whose definition is owned
# elsewhere. A recipe that re-implements a kit-owned command inline guarantees
# that the local verdict and the runner's verdict can drift.
# ------------------------------------------------------------------
fleet_checks() {
    print_subheader "FLEET BOUNDARY"
    [ "$FLEET_CHECKS" -eq 1 ] || { say_info "Skipped — --no-fleet-checks was passed."; return 0; }

    local found=0
    check_reimplementation() {
        local label=$1 pattern=$2 owner=$3 script=$4
        local hits
        hits="$(awk -F'\t' '$1=="RECIPE"{printf "%s: %s\n", $2, $4}' "$INDEX_FILE" | grep -E "$pattern" || true)"
        [ -n "$hits" ] || return 0
        if recipe_lines | grep -q "$script"; then
            return 0
        fi
        say_warning "A recipe runs $label inline; that command is owned by $owner ($script)."
        printf '%s\n' "$hits" | head -3
        detail "Fix: invoke the owning script so the local verdict is the runner's verdict, for example 'bash .service-ci-kit/ci/scripts/$(basename "$script")'."
        detail "Owner of how the gate is expressed on a runner: /alaa-gitlab-ci-cd (\$alaa-gitlab-ci-cd). Owner of this rule: references/ci-entrypoint.md."
        found=1
    }

    check_reimplementation "an image build or push" 'docker (buildx )?build|docker push' "service-ci-kit" "ci/scripts/build_image.sh"
    check_reimplementation "a Helm release"          'helm (upgrade|install)'              "service-ci-kit" "ci/scripts/deploy.sh"
    check_reimplementation "a semantic release"      'semantic-release|npx semantic'       "service-ci-kit" "ci/scripts/release.sh"
    check_reimplementation "a database export"       'pg_dump'                             "service-ci-kit" "ci/scripts/export_db.sh"
    check_reimplementation "a database migration"    'artisan migrate'                     "service-ci-kit" "ci/scripts/migrate_db.sh"

    if [ "$found" -eq 0 ]; then
        say_ok "No recipe re-implements a kit-owned command"
    fi
}

# ------------------------------------------------------------------
# Version floor — the freshness check lives in the checker, not only in prose.
# ------------------------------------------------------------------
version_checks() {
    local file=$1
    print_subheader "GNU MAKE VERSION FLOOR"
    echo "Current stable GNU Make on 2026-07-29: ${GNU_MAKE_CURRENT}"
    echo "Re-derive with: curl -s https://ftp.gnu.org/gnu/make/ | grep -o 'make-[0-9][0-9.]*\\.tar\\.gz' | sort -V | tail -1"

    local uses_44=""
    grep -q "^\.WAIT\|[[:space:]]\.WAIT\b" "$file" && uses_44="${uses_44} .WAIT"
    grep -qE "^\.NOTPARALLEL:[[:space:]]*[^[:space:]]" "$file" && uses_44="${uses_44} .NOTPARALLEL-with-prerequisites"
    grep -q "^\.NOTINTERMEDIATE" "$file" && uses_44="${uses_44} .NOTINTERMEDIATE"
    grep -q '\$(let ' "$file" && uses_44="${uses_44} \$(let)"
    grep -q '\$(intcmp ' "$file" && uses_44="${uses_44} \$(intcmp)"

    if [ -z "$uses_44" ]; then
        say_ok "No GNU Make ${GNU_MAKE_44_FLOOR}+ only construct is used, so any GNU Make 4.0+ runs this file."
        return 0
    fi

    echo "Constructs that require GNU Make ${GNU_MAKE_44_FLOOR}+:${uses_44}"
    if [ "$HAVE_MAKE" -eq 0 ]; then
        say_info "GNU make is not installed here, so the local version cannot be compared against the floor."
        return 0
    fi
    local local_ver
    local_ver="$(make --version 2>/dev/null | head -1 | grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -1)"
    if [ -z "$local_ver" ]; then
        say_info "Could not parse the local GNU Make version from 'make --version'."
        return 0
    fi
    if [ "$(printf '%s\n%s\n' "$GNU_MAKE_44_FLOOR" "$local_ver" | sort -V | head -1)" = "$GNU_MAKE_44_FLOOR" ]; then
        say_ok "Local GNU Make ${local_ver} satisfies the ${GNU_MAKE_44_FLOOR} floor"
    else
        say_error "This file needs GNU Make ${GNU_MAKE_44_FLOOR}+ and the local GNU Make is ${local_ver}."
        detail "Fix: either raise the toolchain to ${GNU_MAKE_CURRENT} or replace the construct with a plain prerequisite."
        detail "Owner: references/optimization-guide.md."
    fi
}

# ------------------------------------------------------------------
# Optional third-party linters
# ------------------------------------------------------------------
checkmake_validation() {
    local file=$1
    print_subheader "CHECKMAKE (optional)"
    if ! command -v checkmake >/dev/null 2>&1; then
        say_info "checkmake is not installed; skipping."
        detail "Install: go install github.com/checkmake/checkmake/cmd/checkmake@latest  (current release v0.3.2, verified 2026-07-29)"
        return 0
    fi
    local out
    out="$(checkmake "$file" 2>&1)" || true
    if [ -n "$out" ]; then
        printf '%s\n' "$out"
        local n
        n="$(printf '%s' "$out" | grep -c "WARN" || true)"
        if [ "${n:-0}" -gt 0 ]; then WARNINGS=$((WARNINGS + n)); fi
    else
        say_ok "checkmake reported nothing"
    fi
}

unmake_validation() {
    local file=$1
    print_subheader "UNMAKE, POSIX PORTABILITY (optional)"
    if ! command -v unmake >/dev/null 2>&1; then
        say_info "unmake is not installed; skipping."
        detail "See https://github.com/mcandre/unmake (current release 0.0.27, verified 2026-07-29)."
        return 0
    fi
    # unmake accepts both a file path and a directory; verified against upstream
    # main on 2026-07-29. Single-file invocation is the form this checker needs.
    local out
    out="$(unmake "$file" 2>&1)" || true
    if [ -n "$out" ]; then
        printf '%s\n' "$out"
        local n
        n="$(printf '%s' "$out" | grep -ciE "warning" || true)"
        if [ "${n:-0}" -gt 0 ]; then WARNINGS=$((WARNINGS + n)); fi
    else
        say_ok "unmake reported nothing (POSIX compatible)"
    fi
}

# ------------------------------------------------------------------
print_summary() {
    local file=$1
    print_header "VALIDATION SUMMARY"
    echo "File:     $file"
    printf 'Errors:   %s\n' "$ERRORS"
    printf 'Warnings: %s\n' "$WARNINGS"
    printf 'Notes:    %s\n' "$INFO"
    echo ""
    if [ "$ERRORS" -gt 0 ] || [ "$WARNINGS" -gt 0 ]; then
        printf '%bFINDINGS — exit 1%b\n' "$YELLOW" "$NC"
        return "$EXIT_FINDINGS"
    fi
    printf '%bCLEAN — exit 0%b\n' "$GREEN" "$NC"
    return "$EXIT_CLEAN"
}

run_validation() {
    local makefile=$1
    print_header "MAKEFILE VALIDATOR"
    echo "File: $makefile"

    check_dependencies
    validate_file "$makefile"
    build_index "$makefile"
    setup_mbake

    line_ending_check "$makefile"
    syntax_check "$makefile"
    mbake_validation "$makefile"
    mbake_format_check "$makefile"
    structural_checks "$makefile"
    recipe_checks "$makefile"
    fleet_checks
    version_checks "$makefile"
    checkmake_validation "$makefile"
    unmake_validation "$makefile"

    set +e
    print_summary "$makefile"
    local rc=$?
    set -e
    return "$rc"
}

# ------------------------------------------------------------------
# Self-test
# ------------------------------------------------------------------
self_test() {
    local failures=0 checks=0

    for f in clean-fleet.mk oneshell-swallow.mk defective.mk continuation.mk; do
        if [ ! -f "$FIXTURE_DIR/$f" ]; then
            printf '[CANNOT RUN] fixture missing: %s\n' "$FIXTURE_DIR/$f" >&2
            exit "$EXIT_CANNOT_RUN"
        fi
    done

    assert_exit() {
        local expected=$1 label=$2; shift 2
        local out rc
        set +e
        out="$(NO_COLOR=1 bash "${BASH_SOURCE[0]}" --skip-mbake --no-fleet-checks "$@" 2>&1)"
        rc=$?
        set -e
        checks=$((checks + 1))
        if [ "$rc" -eq "$expected" ]; then
            printf 'PASS  exit %s  %s\n' "$rc" "$label"
        else
            printf 'FAIL  expected exit %s, got %s  %s\n' "$expected" "$rc" "$label"
            printf '%s\n' "$out" | tail -25
            failures=$((failures + 1))
        fi
    }

    assert_contains() {
        local needle=$1 label=$2; shift 2
        local out
        set +e
        out="$(NO_COLOR=1 bash "${BASH_SOURCE[0]}" --skip-mbake --no-fleet-checks "$@" 2>&1)"
        set -e
        checks=$((checks + 1))
        if printf '%s' "$out" | grep -q "$needle"; then
            printf 'PASS  reported  %s\n' "$label"
        else
            printf 'FAIL  did not report  %s\n' "$label"
            failures=$((failures + 1))
        fi
    }

    assert_absent() {
        local needle=$1 label=$2; shift 2
        local out
        set +e
        out="$(NO_COLOR=1 bash "${BASH_SOURCE[0]}" --skip-mbake --no-fleet-checks "$@" 2>&1)"
        set -e
        checks=$((checks + 1))
        if printf '%s' "$out" | grep -q "$needle"; then
            printf 'FAIL  falsely reported  %s\n' "$label"
            failures=$((failures + 1))
        else
            printf 'PASS  did not report  %s\n' "$label"
        fi
    }

    echo "alaa-makefile validator self-test"
    echo "Fixtures: $FIXTURE_DIR"
    echo ""

    assert_exit 0 "clean fleet Makefile is clean"                 "$FIXTURE_DIR/clean-fleet.mk"
    assert_exit 1 "'.ONESHELL' without -e is a finding"           "$FIXTURE_DIR/oneshell-swallow.mk"
    assert_contains ".ONESHELL is set and .SHELLFLAGS is absent" \
        "the .ONESHELL silent-success mode"                        "$FIXTURE_DIR/oneshell-swallow.mk"
    assert_exit 1 "defective Makefile is a finding"                "$FIXTURE_DIR/defective.mk"
    assert_contains "prefixed with '-'"  "the leading-dash defect" "$FIXTURE_DIR/defective.mk"
    assert_contains "bash-only constructs" "the bashism defect"    "$FIXTURE_DIR/defective.mk"
    assert_contains "Bare 'make'"        "the bare-make defect"    "$FIXTURE_DIR/defective.mk"
    assert_contains "Recursive assignment" "the recursive \$(shell) defect" "$FIXTURE_DIR/defective.mk"
    assert_exit 0 "legal line continuation is not a tab error"     "$FIXTURE_DIR/continuation.mk"
    assert_absent "indented with spaces" "the historic tab false positive" "$FIXTURE_DIR/continuation.mk"
    assert_exit 2 "a path that does not exist cannot run"          "$FIXTURE_DIR/does-not-exist.mk"

    checks=$((checks + 1))
    set +e
    NO_COLOR=1 bash "${BASH_SOURCE[0]}" --help >/dev/null 2>&1
    local help_rc=$?
    set -e
    if [ "$help_rc" -eq 0 ]; then
        printf 'PASS  exit 0  --help\n'
    else
        printf 'FAIL  expected exit 0, got %s  --help\n' "$help_rc"
        failures=$((failures + 1))
    fi

    # The fleet boundary check is disabled for the assertions above so the other
    # fixtures stay independent of it; assert it here on its own.
    checks=$((checks + 1))
    set +e
    local fleet_out
    fleet_out="$(NO_COLOR=1 bash "${BASH_SOURCE[0]}" --skip-mbake "$FIXTURE_DIR/defective.mk" 2>&1)"
    set -e
    if printf '%s' "$fleet_out" | grep -q "owned by service-ci-kit"; then
        printf 'PASS  reported  a recipe re-implementing a kit-owned command\n'
    else
        printf 'FAIL  did not report  a recipe re-implementing a kit-owned command\n'
        failures=$((failures + 1))
    fi

    echo ""
    echo "checks: $checks   failures: $failures"
    if [ "$failures" -eq 0 ]; then
        echo "SELF-TEST PASSED"
        return "$EXIT_CLEAN"
    fi
    echo "SELF-TEST FAILED"
    return "$EXIT_FINDINGS"
}

# ------------------------------------------------------------------
main() {
    local target=""
    while [ $# -gt 0 ]; do
        case "$1" in
            -h|--help) usage; exit "$EXIT_CLEAN" ;;
            --self-test) self_test; exit $? ;;
            --no-venv) USE_VENV=0; shift ;;
            --skip-mbake) RUN_MBAKE=0; USE_VENV=0; shift ;;
            --no-fleet-checks) FLEET_CHECKS=0; shift ;;
            --) shift; break ;;
            -*) usage >&2; cannot_run "Unknown option: $1" ;;
            *) if [ -n "$target" ]; then cannot_run "Only one Makefile may be given; got '$target' and '$1'."; fi
               target="$1"; shift ;;
        esac
    done
    [ $# -eq 0 ] || { [ -n "$target" ] && cannot_run "Only one Makefile may be given."; target="$1"; }

    if [ -z "$target" ]; then
        usage >&2
        cannot_run "No Makefile given."
    fi

    set +e
    run_validation "$target"
    local rc=$?
    set -e
    exit "$rc"
}

main "$@"
