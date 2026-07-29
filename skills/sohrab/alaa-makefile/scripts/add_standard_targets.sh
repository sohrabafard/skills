#!/usr/bin/env bash
#
# alaa-makefile — add standard targets to an existing Makefile
#
# Interpreter requirement: GNU bash 4.2 or newer. On Windows run it under Git Bash
# or WSL. The repository ships `.gitattributes` with `*.sh text eol=lf`, so a
# Windows checkout with core.autocrlf=true does not leave a carriage return on the
# shebang line; this script also refuses to edit a Makefile that has CRLF endings,
# because appending LF text to a CRLF file produces a file make parses two ways.
#
# Exit codes:
#   0  done          targets were added, or every requested target already existed
#   1  findings      --dry-run and at least one target is missing
#   2  could not run bad arguments, missing file, unknown target name, CRLF input
#
# History: every invocation of the previous revision failed. `set -euo pipefail`
# combined with `((targets_added++))` starting from zero made the arithmetic
# command return exit status 1 on the first increment, and `main` was called
# without `|| true`, so the script aborted at the first target in every mode
# including --dry-run. Every counter here uses `n=$((n+1))`, which returns 0.

set -euo pipefail

SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

EXIT_DONE=0
EXIT_FINDINGS=1
EXIT_CANNOT_RUN=2

if [ -n "${NO_COLOR:-}" ] || [ ! -t 1 ]; then
    RED=''; GREEN=''; YELLOW=''; BLUE=''; NC=''
else
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
fi

KNOWN_TARGETS=(all install uninstall clean distclean test check help dist)

print_error()   { printf '%bERROR:%b %s\n' "$RED" "$NC" "$*" >&2; }
print_success() { printf '%bSUCCESS:%b %s\n' "$GREEN" "$NC" "$*"; }
print_info()    { printf '%bINFO:%b %s\n' "$YELLOW" "$NC" "$*"; }
print_added()   { printf '%b+%b Added target: %b%s%b\n' "$GREEN" "$NC" "$BLUE" "$1" "$NC"; }
print_skipped() { printf '%b-%b Skipped (already present): %b%s%b\n' "$YELLOW" "$NC" "$BLUE" "$1" "$NC"; }

cannot_run() { print_error "$1"; exit "$EXIT_CANNOT_RUN"; }

usage() {
    cat <<EOF
Usage: ${SCRIPT_NAME} [OPTIONS] [MAKEFILE] [TARGETS...]

Append the standard GNU targets that a Makefile is missing. An existing target is
never overwritten and never reordered.

Arguments:
  MAKEFILE    Path to the Makefile (default: Makefile)
  TARGETS     Target names to add (default: every target listed below)

Available targets:
  all         Build everything the repository produces
  install     Install built files under PREFIX, honouring DESTDIR
  uninstall   Remove what install placed
  clean       Remove build output
  distclean   Remove build output and generated configuration
  test        Run the test suite
  check       GNU alias for test
  help        Print every '##' documentation line in the Makefile
  dist        Create a distribution tarball

Options:
  -h, --help      Show this help and exit 0
  -l, --list      List available targets and exit 0
  -n, --dry-run   Report what would be added and change nothing. Exits 1 when at
                  least one target is missing, so it can gate a pipeline.
      --self-test Run against a scratch Makefile in TMPDIR and assert the result
      --with-vars Also append definitions for PREFIX, INSTALL, RM, BUILDDIR and
                  VERSION when the file does not define them. Off by default,
                  because a Makefile that fronts CI gates needs none of them.

Exit codes:
  0  done, or nothing to do
  1  --dry-run found at least one missing target
  2  could not run: bad arguments, missing file, unknown target name, CRLF input

Examples:
  ${SCRIPT_NAME}                        # add every missing target to ./Makefile
  ${SCRIPT_NAME} build.mk               # add every missing target to build.mk
  ${SCRIPT_NAME} Makefile clean test    # add only clean and test
  ${SCRIPT_NAME} -n Makefile install    # report whether install is missing
EOF
}

list_targets() {
    cat <<EOF
Standard targets this script can append:

  all         Build everything the repository produces
  install     Install built files under PREFIX, honouring DESTDIR
  uninstall   Remove what install placed
  clean       Remove build output
  distclean   Remove build output and generated configuration
  test        Run the test suite
  check       GNU alias for test
  help        Print every '##' documentation line in the Makefile
  dist        Create a distribution tarball
EOF
}

is_known_target() {
    local candidate=$1 t
    for t in "${KNOWN_TARGETS[@]}"; do
        [ "$t" = "$candidate" ] && return 0
    done
    return 1
}

target_exists() {
    grep -qE "^${1}[[:space:]]*:" "$2" 2>/dev/null
}

# Targets are appended, not inserted. Make expands a recipe's variable references
# when the recipe runs, not when the file is parsed, so a definition that appears
# after a recipe is still in effect for that recipe. Appending therefore never
# needs the whole-file rewrite the previous revision performed through a fragile
# header split, which corrupted any Makefile whose header was not pure comments.
generate_target() {
    case "$1" in
        all)
            cat <<'EOF'

## Build everything this repository produces
.PHONY: all
all: build
EOF
            ;;
        install)
            cat <<'EOF'

## Install built files under PREFIX
.PHONY: install
install: all
	$(INSTALL) -d $(DESTDIR)$(PREFIX)/bin
	$(INSTALL) -m 755 $(BUILDDIR)/$(PROJECT) $(DESTDIR)$(PREFIX)/bin/
EOF
            ;;
        uninstall)
            cat <<'EOF'

## Remove what install placed
.PHONY: uninstall
uninstall:
	$(RM) $(DESTDIR)$(PREFIX)/bin/$(PROJECT)
EOF
            ;;
        clean)
            cat <<'EOF'

## Remove build output
.PHONY: clean
clean:
	$(RM) -r $(BUILDDIR)
EOF
            ;;
        distclean)
            cat <<'EOF'

## Remove build output and generated configuration
.PHONY: distclean
distclean: clean
	$(RM) config.h config.log config.status
	$(RM) -r autom4te.cache/
EOF
            ;;
        test)
            cat <<'EOF'

## Run the test suite. Replace the body with the command the runner runs.
.PHONY: test
test:
	@echo "No test command is wired yet. Replace this recipe with the command the CI runner executes, byte for byte."
	@exit 1
EOF
            ;;
        check)
            cat <<'EOF'

## GNU alias for test
.PHONY: check
check: test
EOF
            ;;
        help)
            cat <<'EOF'

## Print every documented target
.PHONY: help
help:
	@sed -n 's/^## //p' $(MAKEFILE_LIST)
EOF
            ;;
        dist)
            cat <<'EOF'

## Create a distribution tarball
.PHONY: dist
dist:
	tar -czf $(PROJECT)-$(VERSION).tar.gz \
		--transform 's,^,$(PROJECT)-$(VERSION)/,' \
		--exclude='.git*' \
		--exclude='$(BUILDDIR)' \
		.
EOF
            ;;
        *)
            return 1
            ;;
    esac
}

# Only the variables the appended targets actually reference, and only when the
# file does not already define them. The previous revision injected
# PROJECT := myproject, TARGET, BUILDDIR and VERSION into every file
# unconditionally, which is wrong for a Makefile that fronts Compose.
append_missing_variables() {
    local makefile=$1 added_text=$2
    local block=""

    add_var() {
        local name=$1 line=$2
        printf '%s' "$added_text" | grep -q "\$($name)" || return 0
        grep -qE "^${name}[[:space:]]*[:?+]?=" "$makefile" && return 0
        block="${block}${line}"$'\n'
    }

    add_var PROJECT  'PROJECT ?= $(notdir $(CURDIR))'
    add_var PREFIX   'PREFIX ?= /usr/local'
    add_var INSTALL  'INSTALL ?= install'
    add_var RM       'RM ?= rm -f'
    add_var BUILDDIR 'BUILDDIR ?= build'
    add_var VERSION  'VERSION ?= 0.0.0'

    [ -n "$block" ] || return 0
    {
        echo ""
        echo "# Variables referenced by the targets ${SCRIPT_NAME} appended."
        printf '%s' "$block"
    } >> "$makefile"
    print_info "Appended the variable definitions the new targets reference"
}

self_test() {
    local work failures=0 checks=0 rc
    work="$(mktemp -d "${TMPDIR:-/tmp}/alaa-makefile-ast-XXXXXX")" || {
        print_error "Cannot create a scratch directory in ${TMPDIR:-/tmp}"
        exit "$EXIT_CANNOT_RUN"
    }
    # Expand the path now: `work` is local to this function and the EXIT trap runs
    # after the function has returned, where the name is no longer bound.
    # shellcheck disable=SC2064  # expansion at trap-set time is what is wanted here
    trap "rm -rf '${work}'" EXIT

    printf '# scratch Makefile\n.PHONY: build\nbuild:\n\t@echo build\n' > "$work/Makefile"

    record() {
        checks=$((checks + 1))
        if [ "$1" = "pass" ]; then printf 'PASS  %s\n' "$2"
        else printf 'FAIL  %s\n' "$2"; failures=$((failures + 1)); fi
    }

    echo "alaa-makefile add_standard_targets self-test"
    echo "Scratch directory: $work"
    echo ""

    set +e
    NO_COLOR=1 bash "${BASH_SOURCE[0]}" --dry-run "$work/Makefile" clean test >/dev/null 2>&1
    rc=$?
    set -e
    [ "$rc" -eq 1 ] && record pass "--dry-run with missing targets exits 1" || record fail "--dry-run exits 1 (got $rc)"
    grep -q '^clean:' "$work/Makefile" && record fail "--dry-run left the file unchanged" || record pass "--dry-run left the file unchanged"

    set +e
    NO_COLOR=1 bash "${BASH_SOURCE[0]}" "$work/Makefile" clean test help >/dev/null 2>&1
    rc=$?
    set -e
    [ "$rc" -eq 0 ] && record pass "adding three targets exits 0" || record fail "adding three targets exits 0 (got $rc)"

    for t in clean test help; do
        grep -qE "^${t}[[:space:]]*:" "$work/Makefile" \
            && record pass "target '$t' is now present" \
            || record fail "target '$t' is now present"
    done

    if command -v make >/dev/null 2>&1; then
        set +e
        (cd "$work" && make -f Makefile --dry-run build >/dev/null 2>&1)
        rc=$?
        set -e
        [ "$rc" -eq 0 ] && record pass "the edited Makefile still parses" || record fail "the edited Makefile still parses (make exit $rc)"
    else
        record pass "the edited Makefile still parses (skipped: GNU make absent)"
    fi

    set +e
    NO_COLOR=1 bash "${BASH_SOURCE[0]}" "$work/Makefile" clean >/dev/null 2>&1
    rc=$?
    set -e
    [ "$rc" -eq 0 ] && record pass "re-running on an existing target exits 0" || record fail "re-running on an existing target exits 0 (got $rc)"
    [ "$(grep -cE '^clean[[:space:]]*:' "$work/Makefile")" -eq 1 ] \
        && record pass "an existing target is not duplicated" \
        || record fail "an existing target is not duplicated"

    set +e
    NO_COLOR=1 bash "${BASH_SOURCE[0]}" "$work/does-not-exist.mk" clean >/dev/null 2>&1
    rc=$?
    set -e
    [ "$rc" -eq 2 ] && record pass "a missing Makefile exits 2" || record fail "a missing Makefile exits 2 (got $rc)"

    set +e
    NO_COLOR=1 bash "${BASH_SOURCE[0]}" "$work/Makefile" frobnicate >/dev/null 2>&1
    rc=$?
    set -e
    [ "$rc" -eq 2 ] && record pass "an unknown target name exits 2" || record fail "an unknown target name exits 2 (got $rc)"

    printf '# crlf\r\n.PHONY: build\r\nbuild:\r\n\t@echo x\r\n' > "$work/crlf.mk"
    set +e
    NO_COLOR=1 bash "${BASH_SOURCE[0]}" "$work/crlf.mk" clean >/dev/null 2>&1
    rc=$?
    set -e
    [ "$rc" -eq 2 ] && record pass "a CRLF Makefile exits 2" || record fail "a CRLF Makefile exits 2 (got $rc)"

    set +e
    NO_COLOR=1 bash "${BASH_SOURCE[0]}" --help >/dev/null 2>&1
    rc=$?
    set -e
    [ "$rc" -eq 0 ] && record pass "--help exits 0" || record fail "--help exits 0 (got $rc)"

    echo ""
    echo "checks: $checks   failures: $failures"
    if [ "$failures" -eq 0 ]; then echo "SELF-TEST PASSED"; return "$EXIT_DONE"; fi
    echo "SELF-TEST FAILED"
    return "$EXIT_FINDINGS"
}

main() {
    local dry_run=0 with_vars=0

    while [ $# -gt 0 ]; do
        case "$1" in
            -h|--help) usage; exit "$EXIT_DONE" ;;
            -l|--list) list_targets; exit "$EXIT_DONE" ;;
            -n|--dry-run) dry_run=1; shift ;;
            --with-vars) with_vars=1; shift ;;
            --self-test) self_test; exit $? ;;
            --) shift; break ;;
            -*) usage >&2; cannot_run "Unknown option: $1" ;;
            *) break ;;
        esac
    done

    local makefile="${1:-Makefile}"
    [ $# -gt 0 ] && shift || true

    local targets=()
    if [ $# -eq 0 ]; then
        targets=("${KNOWN_TARGETS[@]}")
    else
        targets=("$@")
    fi

    [ -e "$makefile" ] || cannot_run "Makefile not found: $makefile"
    [ -f "$makefile" ] || cannot_run "Not a regular file: $makefile"
    [ -r "$makefile" ] || cannot_run "Makefile not readable: $makefile"

    local t
    for t in "${targets[@]}"; do
        is_known_target "$t" || cannot_run "Unknown target '$t'. Run '${SCRIPT_NAME} --list' for the accepted names."
    done

    if LC_ALL=C grep -q $'\r' "$makefile"; then
        cannot_run "$makefile has CRLF line endings. Convert it first with: sed -i \$'s/\\r\$//' $makefile"
    fi

    if [ "$dry_run" -eq 0 ]; then
        [ -w "$makefile" ] || cannot_run "Makefile is not writable: $makefile"
    fi

    print_info "Processing: $makefile"
    echo ""

    local added=0 skipped=0 content=""
    for t in "${targets[@]}"; do
        if target_exists "$t" "$makefile"; then
            print_skipped "$t"
            skipped=$((skipped + 1))
            continue
        fi
        added=$((added + 1))
        if [ "$dry_run" -eq 1 ]; then
            printf '%b+%b Would add: %b%s%b\n' "$GREEN" "$NC" "$BLUE" "$t" "$NC"
        else
            content="${content}$(generate_target "$t")"$'\n'
        fi
    done

    echo ""

    if [ "$dry_run" -eq 1 ]; then
        echo "Summary: would add $added target(s), skip $skipped existing target(s). Nothing was written."
        if [ "$added" -gt 0 ]; then
            return "$EXIT_FINDINGS"
        fi
        return "$EXIT_DONE"
    fi

    if [ "$added" -eq 0 ]; then
        print_info "Every requested target already exists; the file was not modified."
        echo "Summary: added 0, skipped $skipped."
        return "$EXIT_DONE"
    fi

    printf '%s' "$content" >> "$makefile"
    if [ "$with_vars" -eq 1 ]; then
        append_missing_variables "$makefile" "$content"
    fi

    for t in "${targets[@]}"; do
        target_exists "$t" "$makefile" && print_added "$t"
    done

    print_success "Added $added target(s) to $makefile"
    echo "Summary: added $added, skipped $skipped."
    echo ""
    print_info "Each appended recipe is a placeholder. Replace it with the command the CI runner runs, byte for byte, then validate:"
    print_info "  bash ${SCRIPT_DIR}/validate_makefile.sh $makefile"
    return "$EXIT_DONE"
}

set +e
main "$@"
rc=$?
set -e
exit "$rc"
