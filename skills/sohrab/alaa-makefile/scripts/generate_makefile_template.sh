#!/usr/bin/env bash
#
# alaa-makefile — generate a Makefile template
#
# Interpreter requirement: GNU bash 4.2 or newer. On Windows run it under Git Bash
# or WSL. The repository ships `.gitattributes` with `*.sh text eol=lf` so a
# Windows checkout with core.autocrlf=true does not leave a carriage return on the
# shebang line, and every template this script writes uses LF endings.
#
# Exit codes:
#   0  done          a template was written, or --help/--list/--self-test succeeded
#   1  findings      --self-test found a generated template that fails validation
#   2  could not run bad arguments, unknown type, output exists without --force
#
# Every template emitted here carries the preamble the body of this skill
# mandates, and every template is asserted against scripts/validate_makefile.sh
# by --self-test, so the generator and the validator cannot drift apart.

set -euo pipefail

SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

EXIT_DONE=0
EXIT_FINDINGS=1
EXIT_CANNOT_RUN=2

FORCE=0
PROJECT_TYPE=""
PROJECT_NAME="myproject"
OUTPUT_FILE="Makefile"

TYPES=(fleet go python generic c c-lib cpp java)

if [ -n "${NO_COLOR:-}" ] || [ ! -t 1 ]; then
    RED=''; GREEN=''; YELLOW=''; NC=''
else
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
fi

print_error()   { printf '%bERROR:%b %s\n' "$RED" "$NC" "$*" >&2; }
print_success() { printf '%bSUCCESS:%b %s\n' "$GREEN" "$NC" "$*"; }
print_info()    { printf '%bINFO:%b %s\n' "$YELLOW" "$NC" "$*"; }
cannot_run()    { print_error "$1"; exit "$EXIT_CANNOT_RUN"; }

usage() {
    cat <<EOF
Usage: ${SCRIPT_NAME} [OPTIONS] PROJECT_TYPE [PROJECT_NAME] [OUTPUT_FILE]

Write a Makefile template that already carries the hardening preamble, a
documented default target and a help target.

Arguments:
  PROJECT_TYPE    Required. One of the types below.
  PROJECT_NAME    Name substituted into the template (default: myproject)
  OUTPUT_FILE     Path to write (default: Makefile)

Project types:
  fleet     A service on this fleet. Every target is a local invocation of a
            command owned by service-ci-kit or service-runtime-kit. Start here
            for any repository that deploys through the shared GitLab pipeline.
  go        Go module: build, test, lint, fmt, install
  python    Python package: build, install, test, lint, format
  generic   Language-neutral skeleton with the targets and none of the commands
  c         Single-binary C project
  c-lib     C static and shared library
  cpp       C++ project (CXX and CXXFLAGS, not CC and CFLAGS)
  java      Java project producing a JAR

Options:
  -f, --force     Overwrite OUTPUT_FILE if it exists
  -l, --list      List project types and exit 0
  -h, --help      Show this help and exit 0
      --self-test Generate every type into TMPDIR, assert each one parses and
                  each one passes scripts/validate_makefile.sh, then exit

Exit codes:
  0  a template was written, or --help/--list/--self-test succeeded
  1  --self-test found a generated template that fails validation
  2  could not run: no PROJECT_TYPE, unknown PROJECT_TYPE, or OUTPUT_FILE exists
     without --force

Examples:
  ${SCRIPT_NAME} fleet auth-service
  ${SCRIPT_NAME} go server Makefile
  ${SCRIPT_NAME} python mypackage build.mk
  ${SCRIPT_NAME} -f c myapp Makefile
  ${SCRIPT_NAME} --self-test
EOF
}

list_types() { printf '%s\n' "${TYPES[@]}"; }

is_known_type() {
    local candidate=$1 t
    for t in "${TYPES[@]}"; do [ "$t" = "$candidate" ] && return 0; done
    return 1
}

parse_args() {
    while [ $# -gt 0 ]; do
        case "$1" in
            -f|--force) FORCE=1; shift ;;
            -h|--help) usage; exit "$EXIT_DONE" ;;
            -l|--list) list_types; exit "$EXIT_DONE" ;;
            --self-test) self_test; exit $? ;;
            --) shift; break ;;
            -*) usage >&2; cannot_run "Unknown option: $1" ;;
            *)
                if [ -z "$PROJECT_TYPE" ]; then PROJECT_TYPE="$1"
                elif [ "$PROJECT_NAME" = "myproject" ]; then PROJECT_NAME="$1"
                else OUTPUT_FILE="$1"; fi
                shift ;;
        esac
    done
}

# The preamble every template shares. Stated once here, so the generator cannot
# disagree with the body of the skill.
emit_preamble() {
    cat <<'EOF'
SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
.SUFFIXES:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules
EOF
}

gen_fleet() {
    emit_preamble
    cat <<'EOF'

# ---------------------------------------------------------------------------
# PROJECT_NAME — local entrypoint for commands owned elsewhere.
#
# Every target below is a local invocation. It adds a name, a prerequisite order
# and a failure path; it does not decide what the command is.
#   service-ci-kit owns every ci/* command; how it is expressed on a runner is
#     owned by /alaa-gitlab-ci-cd ($alaa-gitlab-ci-cd).
#   service-runtime-kit owns every runtime/* command; the Compose file and the
#     image are owned by /alaa-docker-production ($alaa-docker-production).
# A target here runs the same command the runner runs, with the same arguments,
# and fails whenever that command fails. No '-' prefix, no '|| true'.
# ---------------------------------------------------------------------------

PROJECT ?= PROJECT_NAME
CI_KIT ?= .service-ci-kit/ci/scripts
RUNTIME ?= scripts/runtime
COMPOSE_MODE ?= prod

.PHONY: help ci/build ci/release ci/migrate ci/deploy ci/db-export
.PHONY: runtime/render runtime/validate runtime/up runtime/interpolation

## Show every target and what it invokes (default target)
help:
	@sed -n 's/^## //p' $(MAKEFILE_LIST)

## Build and push the service image through the kit gate
ci/build:
	bash $(CI_KIT)/build_image.sh

## Run the semantic-release gate
ci/release:
	bash $(CI_KIT)/release.sh

## Run the database migration gate
ci/migrate:
	bash $(CI_KIT)/migrate_db.sh

## Run the deploy gate
ci/deploy:
	bash $(CI_KIT)/deploy.sh

## Export the database through the kit gate
ci/db-export:
	bash $(CI_KIT)/export_db.sh

## Regenerate the runtime files from service-runtime-kit
runtime/render:
	bash $(RUNTIME)/render-runtime.sh --repo-root .

## Run the runtime contract validator the runner runs
runtime/validate:
	bash $(RUNTIME)/validate-runtime.sh --repo-root .

## Prove the Compose interpolation is fail-closed
runtime/interpolation:
	bash $(RUNTIME)/test-fail-closed-interpolation.sh

## Bring the local Compose runtime up in COMPOSE_MODE (dev or prod)
runtime/up: runtime/render
	bash scripts/docker/up-local.sh $(COMPOSE_MODE)
EOF
}

gen_go() {
    emit_preamble
    cat <<'EOF'

PROJECT ?= PROJECT_NAME
GO ?= go
PREFIX ?= /usr/local
BUILDDIR ?= build

VERSION := $(shell git describe --tags --always --dirty 2>/dev/null || echo dev)
GO_LDFLAGS := -ldflags "-X main.version=$(VERSION)"
SOURCES := $(shell find . -name '*.go' -not -path './vendor/*')
TARGET := $(BUILDDIR)/$(PROJECT)

.PHONY: all build install test lint fmt clean help

## Build the binary (default target)
all: build

## Build the binary into BUILDDIR
build: $(TARGET)

$(TARGET): $(SOURCES) | $(BUILDDIR)
	$(GO) build $(GO_LDFLAGS) -o $@ ./cmd/$(PROJECT)

$(BUILDDIR):
	mkdir -p $@

## Install the binary under PREFIX
install: build
	install -d $(DESTDIR)$(PREFIX)/bin
	install -m 755 $(TARGET) $(DESTDIR)$(PREFIX)/bin/$(PROJECT)

## Run the test suite
test:
	$(GO) test ./...

## Run the linter
lint:
	golangci-lint run

## Format the module
fmt:
	$(GO) fmt ./...

## Remove build output
clean:
	$(RM) -r $(BUILDDIR)

## Show every documented target
help:
	@sed -n 's/^## //p' $(MAKEFILE_LIST)
EOF
}

gen_python() {
    emit_preamble
    cat <<'EOF'

PROJECT ?= PROJECT_NAME
PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

.PHONY: all build install develop test lint format clean help

## Build the distribution (default target)
all: build

## Build the wheel and sdist
build:
	$(PYTHON) -m build

## Install the package
install:
	$(PIP) install .

## Install the package in editable mode with development extras
develop:
	$(PIP) install -e '.[dev]'

## Run the test suite
test:
	$(PYTHON) -m pytest tests/

## Run the linters
lint:
	$(PYTHON) -m ruff check src tests

## Format the source tree
format:
	$(PYTHON) -m ruff format src tests

## Remove build output and caches
clean:
	$(RM) -r build dist .pytest_cache .ruff_cache
	find . -type d -name '__pycache__' -prune -exec rm -r {} +

## Show every documented target
help:
	@sed -n 's/^## //p' $(MAKEFILE_LIST)
EOF
}

gen_generic() {
    emit_preamble
    cat <<'EOF'

PROJECT ?= PROJECT_NAME
BUILDDIR ?= build

.PHONY: all build test install clean help

## Build the project (default target)
all: build

## Build. Replace this recipe with the command the CI runner runs, byte for byte.
build:
	@echo "No build command is wired yet for $(PROJECT)."
	@exit 1

## Run the tests. Replace this recipe with the command the CI runner runs.
test:
	@echo "No test command is wired yet for $(PROJECT)."
	@exit 1

## Install. Replace this recipe with the command the release job runs.
install: build
	@echo "No install command is wired yet for $(PROJECT)."
	@exit 1

## Remove build output
clean:
	$(RM) -r $(BUILDDIR)

## Show every documented target
help:
	@sed -n 's/^## //p' $(MAKEFILE_LIST)
EOF
}

gen_c() {
    emit_preamble
    cat <<'EOF'

PROJECT ?= PROJECT_NAME
VERSION ?= 0.1.0

CC ?= cc
CFLAGS ?= -Wall -Wextra -O2
CPPFLAGS ?=
LDFLAGS ?=
LDLIBS ?=
PREFIX ?= /usr/local

SRCDIR := src
BUILDDIR := build
OBJDIR := $(BUILDDIR)/obj

SOURCES := $(wildcard $(SRCDIR)/*.c)
OBJECTS := $(SOURCES:$(SRCDIR)/%.c=$(OBJDIR)/%.o)
DEPENDS := $(OBJECTS:.o=.d)
TARGET := $(BUILDDIR)/$(PROJECT)

.PHONY: all install test clean help

## Build the binary (default target)
all: $(TARGET)

$(TARGET): $(OBJECTS) | $(BUILDDIR)
	$(CC) $(LDFLAGS) $^ $(LDLIBS) -o $@

$(OBJDIR)/%.o: $(SRCDIR)/%.c | $(OBJDIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -MMD -MP -c $< -o $@

$(BUILDDIR) $(OBJDIR):
	mkdir -p $@

-include $(DEPENDS)

## Install the binary under PREFIX
install: all
	install -d $(DESTDIR)$(PREFIX)/bin
	install -m 755 $(TARGET) $(DESTDIR)$(PREFIX)/bin/$(PROJECT)

## Run the test suite
test: all
	./tests/run.sh

## Remove build output
clean:
	$(RM) -r $(BUILDDIR)

## Show every documented target
help:
	@sed -n 's/^## //p' $(MAKEFILE_LIST)
EOF
}

gen_c_lib() {
    emit_preamble
    cat <<'EOF'

PROJECT ?= PROJECT_NAME
VERSION ?= 0.1.0

CC ?= cc
AR ?= ar
RANLIB ?= ranlib
CFLAGS ?= -Wall -Wextra -O2 -fPIC
CPPFLAGS ?=
PREFIX ?= /usr/local

SRCDIR := src
BUILDDIR := build
OBJDIR := $(BUILDDIR)/obj

SOURCES := $(wildcard $(SRCDIR)/*.c)
OBJECTS := $(SOURCES:$(SRCDIR)/%.c=$(OBJDIR)/%.o)
DEPENDS := $(OBJECTS:.o=.d)
HEADERS := $(wildcard $(SRCDIR)/*.h)

STATIC_LIB := $(BUILDDIR)/lib$(PROJECT).a
SHARED_LIB := $(BUILDDIR)/lib$(PROJECT).so.$(VERSION)

.PHONY: all static shared install clean help

## Build the static and the shared library (default target)
all: static shared

## Build the static library
static: $(STATIC_LIB)

## Build the shared library
shared: $(SHARED_LIB)

$(STATIC_LIB): $(OBJECTS) | $(BUILDDIR)
	$(AR) rcs $@ $^
	$(RANLIB) $@

$(SHARED_LIB): $(OBJECTS) | $(BUILDDIR)
	$(CC) -shared -Wl,-soname,lib$(PROJECT).so.1 $^ -o $@

$(OBJDIR)/%.o: $(SRCDIR)/%.c | $(OBJDIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -MMD -MP -c $< -o $@

$(BUILDDIR) $(OBJDIR):
	mkdir -p $@

-include $(DEPENDS)

## Install both libraries and the headers under PREFIX
install: all
	install -d $(DESTDIR)$(PREFIX)/lib
	install -m 644 $(STATIC_LIB) $(DESTDIR)$(PREFIX)/lib/
	install -m 755 $(SHARED_LIB) $(DESTDIR)$(PREFIX)/lib/
	install -d $(DESTDIR)$(PREFIX)/include/$(PROJECT)
	install -m 644 $(HEADERS) $(DESTDIR)$(PREFIX)/include/$(PROJECT)/

## Remove build output
clean:
	$(RM) -r $(BUILDDIR)

## Show every documented target
help:
	@sed -n 's/^## //p' $(MAKEFILE_LIST)
EOF
}

# Written out in full rather than produced by `sed 's/gcc/g++/g; s/\.c/.cpp/g'`
# over the C template, which left the variables named CC and CFLAGS.
gen_cpp() {
    emit_preamble
    cat <<'EOF'

PROJECT ?= PROJECT_NAME
VERSION ?= 0.1.0

CXX ?= c++
CXXFLAGS ?= -Wall -Wextra -std=c++20 -O2
CPPFLAGS ?=
LDFLAGS ?=
LDLIBS ?=
PREFIX ?= /usr/local

SRCDIR := src
BUILDDIR := build
OBJDIR := $(BUILDDIR)/obj

SOURCES := $(wildcard $(SRCDIR)/*.cpp)
OBJECTS := $(SOURCES:$(SRCDIR)/%.cpp=$(OBJDIR)/%.o)
DEPENDS := $(OBJECTS:.o=.d)
TARGET := $(BUILDDIR)/$(PROJECT)

.PHONY: all install test clean help

## Build the binary (default target)
all: $(TARGET)

$(TARGET): $(OBJECTS) | $(BUILDDIR)
	$(CXX) $(LDFLAGS) $^ $(LDLIBS) -o $@

$(OBJDIR)/%.o: $(SRCDIR)/%.cpp | $(OBJDIR)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -MMD -MP -c $< -o $@

$(BUILDDIR) $(OBJDIR):
	mkdir -p $@

-include $(DEPENDS)

## Install the binary under PREFIX
install: all
	install -d $(DESTDIR)$(PREFIX)/bin
	install -m 755 $(TARGET) $(DESTDIR)$(PREFIX)/bin/$(PROJECT)

## Run the test suite
test: all
	./tests/run.sh

## Remove build output
clean:
	$(RM) -r $(BUILDDIR)

## Show every documented target
help:
	@sed -n 's/^## //p' $(MAKEFILE_LIST)
EOF
}

gen_java() {
    emit_preamble
    cat <<'EOF'

PROJECT ?= PROJECT_NAME
VERSION ?= 0.1.0
MAIN_CLASS ?= Main

JAVAC ?= javac
JAVA ?= java
JAR ?= jar
JAVAC_FLAGS ?= -Xlint:all -encoding UTF-8

SRCDIR := src
BUILDDIR := build
CLASSDIR := $(BUILDDIR)/classes
DISTDIR := $(BUILDDIR)/dist
LIBDIR := lib

JAVA_SOURCES := $(shell find $(SRCDIR) -name '*.java' 2>/dev/null)
CLASSPATH := $(CLASSDIR)
TARGET := $(DISTDIR)/$(PROJECT)-$(VERSION).jar

.PHONY: all compile jar run test clean help

## Build the JAR (default target)
all: jar

## Compile the sources
compile: $(CLASSDIR)/.compiled

$(CLASSDIR)/.compiled: $(JAVA_SOURCES) | $(CLASSDIR)
	$(JAVAC) $(JAVAC_FLAGS) -d $(CLASSDIR) -cp "$(CLASSPATH)" $(JAVA_SOURCES)
	touch $@

$(CLASSDIR) $(DISTDIR):
	mkdir -p $@

## Package the compiled classes into a JAR
jar: compile | $(DISTDIR)
	printf 'Manifest-Version: 1.0\nMain-Class: %s\n' "$(MAIN_CLASS)" > $(BUILDDIR)/MANIFEST.MF
	$(JAR) cfm $(TARGET) $(BUILDDIR)/MANIFEST.MF -C $(CLASSDIR) .

## Run the application from the compiled classes
run: compile
	$(JAVA) -cp "$(CLASSPATH)" $(MAIN_CLASS)

## Run the test suite
test: compile
	./tests/run.sh

## Remove build output
clean:
	$(RM) -r $(BUILDDIR)

## Show every documented target
help:
	@sed -n 's/^## //p' $(MAKEFILE_LIST)
EOF
}

emit_template() {
    case "$1" in
        fleet)   gen_fleet ;;
        go)      gen_go ;;
        python)  gen_python ;;
        generic) gen_generic ;;
        c)       gen_c ;;
        c-lib)   gen_c_lib ;;
        cpp)     gen_cpp ;;
        java)    gen_java ;;
        *)       return 1 ;;
    esac
}

write_template() {
    local type=$1 project=$2 output=$3
    emit_template "$type" | sed "s/PROJECT_NAME/${project}/g" > "$output"
}

self_test() {
    local work failures=0 checks=0 rc
    work="$(mktemp -d "${TMPDIR:-/tmp}/alaa-makefile-gen-XXXXXX")" || {
        print_error "Cannot create a scratch directory in ${TMPDIR:-/tmp}"
        exit "$EXIT_CANNOT_RUN"
    }
    # Expand now: the EXIT trap runs after this function has returned.
    # shellcheck disable=SC2064  # expansion at trap-set time is what is wanted here
    trap "rm -rf '${work}'" EXIT

    record() {
        checks=$((checks + 1))
        if [ "$1" = pass ]; then printf 'PASS  %s\n' "$2"
        else printf 'FAIL  %s\n' "$2"; failures=$((failures + 1)); fi
    }

    echo "alaa-makefile generate_makefile_template self-test"
    echo "Scratch directory: $work"
    echo ""

    local t
    for t in "${TYPES[@]}"; do
        local out="$work/$t.mk"
        set +e
        NO_COLOR=1 bash "${BASH_SOURCE[0]}" "$t" "sample-$t" "$out" >/dev/null 2>&1
        rc=$?
        set -e
        if [ "$rc" -ne 0 ] || [ ! -s "$out" ]; then
            record fail "type '$t' generates a file (exit $rc)"
            continue
        fi
        record pass "type '$t' generates a file"

        if LC_ALL=C grep -q $'\r' "$out"; then
            record fail "type '$t' writes LF line endings"
        else
            record pass "type '$t' writes LF line endings"
        fi

        if command -v make >/dev/null 2>&1; then
            set +e
            (cd "$work" && make -f "$t.mk" --dry-run help >/dev/null 2>&1)
            rc=$?
            set -e
            [ "$rc" -eq 0 ] && record pass "type '$t' parses under make --dry-run" \
                            || record fail "type '$t' parses under make --dry-run (exit $rc)"
        else
            record pass "type '$t' parses under make --dry-run (skipped: GNU make absent)"
        fi

        set +e
        NO_COLOR=1 bash "$SCRIPT_DIR/validate_makefile.sh" --skip-mbake "$out" >"$work/$t.validate.log" 2>&1
        rc=$?
        set -e
        if [ "$rc" -eq 0 ]; then
            record pass "type '$t' passes validate_makefile.sh"
        else
            record fail "type '$t' passes validate_makefile.sh (exit $rc)"
            sed -n '/RECIPE BEHAVIOUR/,/VALIDATION SUMMARY/p' "$work/$t.validate.log" | head -25
        fi
    done

    set +e
    NO_COLOR=1 bash "${BASH_SOURCE[0]}" >/dev/null 2>&1
    rc=$?
    set -e
    [ "$rc" -eq 2 ] && record pass "no PROJECT_TYPE exits 2" || record fail "no PROJECT_TYPE exits 2 (got $rc)"

    set +e
    NO_COLOR=1 bash "${BASH_SOURCE[0]}" frobnicate x "$work/x.mk" >/dev/null 2>&1
    rc=$?
    set -e
    [ "$rc" -eq 2 ] && record pass "an unknown type exits 2" || record fail "an unknown type exits 2 (got $rc)"

    set +e
    NO_COLOR=1 bash "${BASH_SOURCE[0]}" go x "$work/go.mk" >/dev/null 2>&1
    rc=$?
    set -e
    [ "$rc" -eq 2 ] && record pass "an existing output without --force exits 2" || record fail "an existing output without --force exits 2 (got $rc)"

    set +e
    NO_COLOR=1 bash "${BASH_SOURCE[0]}" --force go x "$work/go.mk" >/dev/null 2>&1
    rc=$?
    set -e
    [ "$rc" -eq 0 ] && record pass "--force overwrites and exits 0" || record fail "--force overwrites and exits 0 (got $rc)"

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
    parse_args "$@"

    if [ -z "$PROJECT_TYPE" ]; then
        usage >&2
        cannot_run "PROJECT_TYPE is required."
    fi
    is_known_type "$PROJECT_TYPE" || cannot_run "Unknown project type '$PROJECT_TYPE'. Run '${SCRIPT_NAME} --list' for the accepted values."

    if [ -e "$OUTPUT_FILE" ] && [ "$FORCE" -eq 0 ]; then
        cannot_run "'$OUTPUT_FILE' already exists. Pass -f/--force to overwrite it."
    fi

    print_info "Generating the '$PROJECT_TYPE' template for '$PROJECT_NAME' at $OUTPUT_FILE"
    write_template "$PROJECT_TYPE" "$PROJECT_NAME" "$OUTPUT_FILE"
    print_success "Wrote $OUTPUT_FILE"
    print_info "Replace every placeholder recipe with the command the CI runner runs, then validate:"
    print_info "  bash ${SCRIPT_DIR}/validate_makefile.sh $OUTPUT_FILE"
    return "$EXIT_DONE"
}

set +e
main "$@"
rc=$?
set -e
exit "$rc"
