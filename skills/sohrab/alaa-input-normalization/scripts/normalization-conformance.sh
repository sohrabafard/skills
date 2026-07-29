#!/usr/bin/env bash
#
# Cross-language conformance harness for the Alaa input-boundary normalization contract,
# owned by the skill `alaa-input-normalization`.
#
# It drives every canonical implementation under `assets/input-normalization/` over the one
# corpus at `scripts/normalization-corpus.json`, in both modes, and fails when any
# implementation disagrees with the corpus on any case. Run it after every change to any
# canonical implementation and paste its output into the change record, because a change
# proved in one runtime is not proved in the others, and because the ruling this contract
# serves has two enforcement points that must agree byte for byte.
#
# A runtime whose interpreter or toolchain is absent is reported as skipped and excluded.
# The harness never reports a pass for a runtime it did not run, and a run in which fewer
# than two runtimes executed is not a pass at all.
#
# What a green run proves: every runtime that executed produced, for every case in the
# corpus, the exact bytes the corpus requires. It proves nothing about an input the corpus
# does not carry. Add the case first, then fix the implementations.
set -euo pipefail

readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
readonly SKILL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly ASSET_DIR="${SKILL_ROOT}/assets/input-normalization"
readonly CORPUS="${SKILL_ROOT}/scripts/normalization-corpus.json"

# The corpus expectations were produced under Unicode 14.0.0. A runtime whose Unicode
# data is older folds fewer families than the corpus requires, silently, and only for a
# user who types a digit family it has never heard of.
readonly MIN_UNICODE_MAJOR=14

readonly EXIT_OK=0
readonly EXIT_USAGE=2
readonly EXIT_DISAGREEMENT=3
readonly EXIT_ENVIRONMENT=4
readonly EXIT_SELF_TEST=5
readonly EXIT_FIXTURES=6

usage() {
    cat <<'USAGEEOF'
Usage: normalization-conformance.sh [--help] [--self-test] [--verbose]

Runs the Python, TypeScript, PHP, and Go canonical normalization implementations over one
shared corpus, in both `text` and `typed` mode, and compares each answer against the bytes
the corpus requires.

Options:
    -h, --help      Show this help
    --self-test     Check the harness comparator and the corpus checksum, then exit
    --verbose       Print every case and every answer, not only failures

Runtime selection:
    python      python3 3.9 or newer
    typescript  node with TypeScript type stripping (22.6 or newer), or node with tsx
    php         php 8.2 or newer, with class Normalizer reachable (ext-intl, or
                symfony/polyfill-intl-normalizer autoloaded through COMPOSER_AUTOLOAD)
    go          go, plus golang.org/x/text/unicode/norm from a module cache, a network,
                or a local checkout named by ALAA_XTEXT_DIR

Environment:
    COMPOSER_AUTOLOAD   Path to a vendor/autoload.php that provides Normalizer, for a PHP
                        without ext-intl. Unset means ext-intl or nothing.
    ALAA_XTEXT_DIR      Path to a local golang.org/x/text checkout, used through a module
                        replace directive so the Go runtime can be proved with no network.

A runtime whose toolchain is absent is reported as "skipped: <reason>" and excluded.
A skipped runtime is unproved, not passing.

Exit codes:
    0  Every runtime that ran matched the corpus on every case, and at least two ran.
       Caller obligation: none.
    2  Usage error: an unknown option was supplied.
       Caller obligation: fix the invocation and retry; do not retry unchanged.
    3  At least one runtime disagreed with the corpus, a driver failed to execute, or a
       runtime reported Unicode data older than the pinned minimum.
       Caller obligation: treat the contract as broken and ship no implementation, no
       middleware, and no browser change until every reported case matches again. Fix the
       implementation, never the corpus: the corpus is the evidence.
    4  Fewer than two runtimes ran, so no cross-runtime agreement was compared.
       Caller obligation: install a toolchain and rerun; do not record this as a pass.
       This contract's whole claim is that two enforcement points agree, so one runtime
       answering correctly is not evidence for it.
    5  The harness comparator failed its own self-test.
       Caller obligation: fix the harness before trusting any result it reports.
    6  The corpus is missing, its checksum does not match its cases, or a canonical
       implementation file is absent.
       Caller obligation: find which copy drifted and reconcile it before reading any
       result, because every runtime can agree on a corpus that is wrong.
USAGEEOF
}

VERBOSE=0
WORKDIR=""

cleanup() {
    if [[ -n "${WORKDIR}" && -d "${WORKDIR}" ]]; then
        rm -rf "${WORKDIR}"
    fi
}
trap cleanup EXIT

# The scratch directory is created under TMPDIR, never inside the skill or the repository
# that copied it, so an interrupted run leaves no untracked file behind.
make_workdir() {
    mktemp -d "${TMPDIR:-/tmp}/alaa-normalization-conformance.XXXXXX"
}

# --------------------------------------------------------------------------------
# Comparator
#
# Every driver writes one line per case per mode: "<index>:<mode>\t<expected>\t<actual>",
# where both values are the lowercase hex of the UTF-8 bytes of the string. Hex is the
# wire form because the values under test contain tabs, newlines, bidi controls and
# zero-width characters, and because two runtimes must not be able to disagree about how
# to escape them. The driver reads the expectation from the same corpus it is being tested
# against, so a runtime that reports a case at all reports what that case required.
#
# A line whose first field begins with '#' is runtime metadata, not a case.
# --------------------------------------------------------------------------------

LAST_SEEN=0
LAST_MISMATCHES=0

render_hex() {
    local hex="${1}"

    if [[ -n "${PYTHON_BIN}" ]]; then
        "${PYTHON_BIN}" -c 'import sys; print(bytes.fromhex(sys.argv[1]).decode("utf-8", "replace").encode("unicode_escape").decode("ascii"))' "${hex}" 2>/dev/null && return 0
    fi

    printf '%s\n' "${hex}"
}

# Sets LAST_SEEN and LAST_MISMATCHES rather than printing them, so diagnostic lines and
# the result never share one stream and a mismatch report can never be read as a count.
compare_output() {
    local runtime="${1}" path="${2}" expected_cases="${3}"
    local seen=0 mismatches=0 case_id expected actual

    while IFS=$'\t' read -r case_id expected actual; do
        # A driver on Windows writes CRLF. read strips only the LF, so a carriage return
        # would ride along on the last field and every answer would mismatch while its
        # rendered bytes looked identical. Strip it from every field, on every platform.
        case_id="${case_id%$'\r'}"
        expected="${expected%$'\r'}"
        actual="${actual%$'\r'}"
        [[ -z "${case_id}" ]] && continue
        [[ "${case_id}" == \#* ]] && continue
        seen=$((seen + 1))

        if [[ "${expected}" == "${actual}" ]]; then
            if [[ ${VERBOSE} -eq 1 ]]; then
                printf '  match     %-12s %-14s %s\n' "${runtime}" "${case_id}" "${actual}"
            fi
            continue
        fi

        mismatches=$((mismatches + 1))
        printf '  MISMATCH  %-12s %s\n' "${runtime}" "${case_id}"
        printf '              corpus requires %s\n' "${expected}"
        printf '                          as text  %s\n' "$(render_hex "${expected}")"
        printf '              %-12s answered %s\n' "${runtime}" "${actual}"
        printf '                          as text  %s\n' "$(render_hex "${actual}")"
    done < "${path}"

    if [[ ${seen} -ne ${expected_cases} ]]; then
        printf '  MISSING   %-12s reported %d of %d answers\n' "${runtime}" "${seen}" "${expected_cases}"
        mismatches=$((mismatches + 1))
    fi

    LAST_SEEN="${seen}"
    LAST_MISMATCHES="${mismatches}"
}

self_test() {
    local failures=0 scratch
    scratch="$(make_workdir)"

    printf '0:text\t616263\t616263\n0:typed\tdb b1\tdb b1\n' | tr -d ' ' > "${scratch}/agree.tsv"
    compare_output selftest "${scratch}/agree.tsv" 2 >/dev/null
    if [[ "${LAST_SEEN}" -eq 2 && "${LAST_MISMATCHES}" -eq 0 ]]; then
        echo 'pass  comparator accepts answers that match the corpus'
    else
        echo 'FAIL  comparator rejected answers that match the corpus' >&2
        failures=$((failures + 1))
    fi

    printf '0:text\t31\t32\n' > "${scratch}/differ.tsv"
    compare_output selftest "${scratch}/differ.tsv" 1 >/dev/null
    if [[ "${LAST_MISMATCHES}" -eq 1 ]]; then
        echo 'pass  comparator detects an answer that differs from the corpus'
    else
        echo 'FAIL  comparator missed an answer that differs from the corpus' >&2
        failures=$((failures + 1))
    fi

    # The two strings below render identically and differ only in composition: U+0622 as
    # one code point, and U+0627 U+0653 as two. An implementation that skips NFC, or that
    # applies it before the fold instead of after, produces exactly this difference, and it
    # is the failure the contract calls a false digit bug.
    printf '0:text\td8a2\td8a7d693\n' > "${scratch}/nfc.tsv"
    compare_output selftest "${scratch}/nfc.tsv" 1 >/dev/null
    if [[ "${LAST_MISMATCHES}" -eq 1 ]]; then
        echo 'pass  comparator detects an answer that differs only in Unicode composition'
    else
        echo 'FAIL  comparator accepted an answer that was not in the required form' >&2
        failures=$((failures + 1))
    fi

    printf '0:text\t31\t31\n' > "${scratch}/short.tsv"
    compare_output selftest "${scratch}/short.tsv" 2 >/dev/null
    if [[ "${LAST_MISMATCHES}" -eq 1 ]]; then
        echo 'pass  comparator detects a driver that skipped an answer'
    else
        echo 'FAIL  comparator accepted a driver that skipped an answer' >&2
        failures=$((failures + 1))
    fi

    printf '#unicode\t14.0.0\t-\n0:text\t31\t31\n' > "${scratch}/meta.tsv"
    compare_output selftest "${scratch}/meta.tsv" 1 >/dev/null
    if [[ "${LAST_SEEN}" -eq 1 && "${LAST_MISMATCHES}" -eq 0 ]]; then
        echo 'pass  comparator counts a metadata line as metadata and not as an answer'
    else
        echo 'FAIL  comparator counted a metadata line as an answer' >&2
        failures=$((failures + 1))
    fi

    if unicode_major_too_old "13.0.0"; then
        echo 'pass  version guard rejects Unicode data older than the pinned minimum'
    else
        echo 'FAIL  version guard accepted Unicode data older than the pinned minimum' >&2
        failures=$((failures + 1))
    fi

    if unicode_major_too_old "15.1.0" || unicode_major_too_old "unknown"; then
        echo 'FAIL  version guard rejected a version it must accept' >&2
        failures=$((failures + 1))
    else
        echo 'pass  version guard accepts a current version and does not judge an unknown one'
    fi

    rm -rf "${scratch}"

    if [[ ${failures} -ne 0 ]]; then
        printf '\n%d comparator self-test case(s) failed.\n' "${failures}" >&2
        exit "${EXIT_SELF_TEST}"
    fi

    printf '\nComparator self-test passed.\n'
}

# --------------------------------------------------------------------------------
# Unicode version guard
# --------------------------------------------------------------------------------

# Returns success when the reported version is a number lower than the pinned minimum.
# A version string that is not dotted-numeric is not judged: it is reported as unknown and
# the case comparison decides, because the alternative is failing every PHP on this fleet,
# none of which installs ext-intl and none of which can therefore name its Unicode data.
unicode_major_too_old() {
    local version="${1}" major

    major="${version%%.*}"

    [[ "${major}" =~ ^[0-9]+$ ]] || return 1
    [[ "${major}" -lt "${MIN_UNICODE_MAJOR}" ]]
}

read_metadata() {
    local path="${1}" key="${2}"

    awk -F'\t' -v key="${key}" '$1 == key { print $2; exit }' "${path}"
}

# --------------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------------

CORPUS_CASES=0
CORPUS_ANSWERS=0
PYTHON_BIN=""

check_fixtures() {
    local declared computed missing=0 file

    for file in normalize_reference.py input-normalization.ts InputNormalization.php input_normalization.go; do
        if [[ ! -f "${ASSET_DIR}/${file}" ]]; then
            printf 'implementation: MISSING at %s\n' "${ASSET_DIR}/${file}" >&2
            missing=$((missing + 1))
        fi
    done

    if [[ ! -f "${CORPUS}" ]]; then
        printf 'corpus: MISSING at %s\n' "${CORPUS}" >&2
        missing=$((missing + 1))
    fi

    if [[ ${missing} -ne 0 ]]; then
        exit "${EXIT_FIXTURES}"
    fi

    if command -v python3 >/dev/null 2>&1; then
        PYTHON_BIN="python3"
    fi

    if [[ -n "${PYTHON_BIN}" ]]; then
        read -r declared computed CORPUS_CASES <<< "$("${PYTHON_BIN}" -c '
import hashlib, json, sys
doc = json.load(open(sys.argv[1], encoding="utf-8"))
cases = doc["cases"]
canonical = json.dumps(cases, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
print(doc["corpus_sha256"], hashlib.sha256(canonical).hexdigest(), len(cases))
' "${CORPUS}")"
    elif command -v node >/dev/null 2>&1; then
        read -r declared computed CORPUS_CASES <<< "$(node -e '
const fs = require("fs");
const crypto = require("crypto");
const doc = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
const sortKeys = (value) => {
  if (Array.isArray(value)) { return value.map(sortKeys); }
  if (value && typeof value === "object") {
    return Object.keys(value).sort().reduce((acc, key) => { acc[key] = sortKeys(value[key]); return acc; }, {});
  }
  return value;
};
const canonical = JSON.stringify(sortKeys(doc.cases));
const digest = crypto.createHash("sha256").update(Buffer.from(canonical, "utf8")).digest("hex");
console.log(doc.corpus_sha256, digest, doc.cases.length);
' "${CORPUS}")"
    else
        printf 'corpus: checksum SKIPPED, no python3 or node available to canonicalise the case array\n'
        CORPUS_CASES="$(grep -c '"text_expected"' "${CORPUS}")"
        CORPUS_ANSWERS=$((CORPUS_CASES * 2))
        printf 'corpus: %d cases read by line count, which is weaker evidence than the checksum\n' "${CORPUS_CASES}"
        return 0
    fi

    if [[ "${declared}" != "${computed}" ]]; then
        printf 'corpus: CHECKSUM MISMATCH\n' >&2
        printf '  declared %s\n' "${declared}" >&2
        printf '  computed %s\n' "${computed}" >&2
        exit "${EXIT_FIXTURES}"
    fi

    CORPUS_ANSWERS=$((CORPUS_CASES * 2))
    printf 'corpus: %d cases x 2 modes = %d answers, checksum verified %s\n' \
        "${CORPUS_CASES}" "${CORPUS_ANSWERS}" "${computed}"
}

# --------------------------------------------------------------------------------
# Runtime discovery
# --------------------------------------------------------------------------------

TS_MODE=""
NODE_BIN=""
PHP_BIN=""
GO_BIN=""
PYTHON_SKIP=""
TS_SKIP=""
PHP_SKIP=""
GO_SKIP=""

discover_runtimes() {
    if [[ -z "${PYTHON_BIN}" ]]; then
        PYTHON_SKIP="python3 not installed"
    fi

    if command -v node >/dev/null 2>&1; then
        NODE_BIN="node"
        local probe
        probe="$(make_workdir)"
        printf 'const value: number = 1;\nconsole.log(value);\n' > "${probe}/probe.ts"
        if node "${probe}/probe.ts" >/dev/null 2>&1; then
            TS_MODE="strip"
        elif node --experimental-strip-types "${probe}/probe.ts" >/dev/null 2>&1; then
            TS_MODE="strip-flag"
        elif command -v tsx >/dev/null 2>&1; then
            TS_MODE="tsx"
        else
            TS_SKIP="node present but cannot run TypeScript; install node 22.6 or newer, or tsx"
        fi
        rm -rf "${probe}"
    else
        TS_SKIP="node not installed"
    fi

    if command -v php >/dev/null 2>&1; then
        if ! php -r 'exit(PHP_VERSION_ID >= 80200 ? 0 : 1);' >/dev/null 2>&1; then
            PHP_SKIP="php older than 8.2"
        elif php -r '
$autoload = getenv("COMPOSER_AUTOLOAD");
if (is_string($autoload) && $autoload !== "" && is_file($autoload)) { require $autoload; }
exit(class_exists("Normalizer") ? 0 : 1);' >/dev/null 2>&1; then
            PHP_BIN="php"
        else
            PHP_SKIP="php present but class Normalizer is unreachable; install ext-intl, or point COMPOSER_AUTOLOAD at a vendor/autoload.php providing symfony/polyfill-intl-normalizer"
        fi
    else
        PHP_SKIP="php not installed"
    fi

    if command -v go >/dev/null 2>&1; then
        GO_BIN="go"
    else
        GO_SKIP="go not installed"
    fi
}

# --------------------------------------------------------------------------------
# Drivers
#
# Each driver takes the corpus path, runs every case in both modes against the canonical
# implementation for its language, and writes "<index>:<mode>\t<expected>\t<actual>".
# --------------------------------------------------------------------------------

write_drivers() {
    WORKDIR="$(make_workdir)"
    mkdir -p "${WORKDIR}/py" "${WORKDIR}/ts" "${WORKDIR}/php" "${WORKDIR}/go"

    cat > "${WORKDIR}/py/driver.py" <<'PYDRV'
import json
import sys
import unicodedata

sys.path.insert(0, sys.argv[2])

import normalize_reference as reference

corpus = json.load(open(sys.argv[1], encoding="utf-8"))
out = ["#unicode\t" + unicodedata.unidata_version + "\t-"]

for index, case in enumerate(corpus["cases"]):
    for mode, key in (("text", "text_expected"), ("typed", "typed_expected")):
        expected = case[key].encode("utf-8").hex()
        actual = reference.MODES[mode](case["input"]).encode("utf-8").hex()
        out.append(f"{index}:{mode}\t{expected}\t{actual}")

sys.stdout.write("\n".join(out) + "\n")
PYDRV

    cp "${ASSET_DIR}/input-normalization.ts" "${WORKDIR}/ts/"

    cat > "${WORKDIR}/ts/driver.ts" <<'TSDRV'
import { readFileSync } from "node:fs";
import { normalize } from "./input-normalization.ts";

type Case = {
  input: string;
  text_expected: string;
  typed_expected: string;
};

const corpus = JSON.parse(readFileSync(process.argv[2], "utf8")) as { cases: Case[] };
const hex = (value: string): string => Buffer.from(value, "utf8").toString("hex");
const lines: string[] = [`#unicode\t${process.versions.unicode ?? "unknown"}\t-`];

corpus.cases.forEach((testCase, index) => {
  lines.push(`${index}:text\t${hex(testCase.text_expected)}\t${hex(normalize(testCase.input, "text"))}`);
  lines.push(`${index}:typed\t${hex(testCase.typed_expected)}\t${hex(normalize(testCase.input, "typed"))}`);
});

process.stdout.write(`${lines.join("\n")}\n`);
TSDRV

    cp "${ASSET_DIR}/InputNormalization.php" "${WORKDIR}/php/"

    cat > "${WORKDIR}/php/driver.php" <<'PHPDRV'
<?php

declare(strict_types=1);

$autoload = getenv('COMPOSER_AUTOLOAD');

if (is_string($autoload) && $autoload !== '' && is_file($autoload)) {
    require $autoload;
}

require __DIR__.'/InputNormalization.php';

use Alaa\Support\Input\InputNormalization;

$corpus = json_decode((string) file_get_contents($argv[1]), true, 512, JSON_THROW_ON_ERROR);

// The fold reads PCRE's Unicode tables and the composition step reads ICU's or the
// polyfill's, so PHP can carry two Unicode data versions at once. Report the one the
// category test uses when it is knowable, and say which it is.
$version = 'unknown';
$source = 'pcre '.PCRE_VERSION;

if (class_exists('IntlChar')) {
    $version = implode('.', array_slice(IntlChar::getUnicodeVersion(), 0, 3));
    $source = 'ext-intl icu, category test still reads pcre '.PCRE_VERSION;
}

echo "#unicode\t".$version."\t-\n";
echo "#datasource\t".$source."\t-\n";

foreach ($corpus['cases'] as $index => $case) {
    echo $index.":text\t".bin2hex($case['text_expected'])."\t".bin2hex(InputNormalization::text($case['input']))."\n";
    echo $index.":typed\t".bin2hex($case['typed_expected'])."\t".bin2hex(InputNormalization::typed($case['input']))."\n";
}
PHPDRV

    sed 's/^package inputnorm$/package main/' "${ASSET_DIR}/input_normalization.go" > "${WORKDIR}/go/input_normalization.go"

    cat > "${WORKDIR}/go/driver.go" <<'GODRV'
package main

import (
	"encoding/hex"
	"encoding/json"
	"fmt"
	"os"
	"strings"
	"unicode"
)

type conformanceCase struct {
	Input         string `json:"input"`
	TextExpected  string `json:"text_expected"`
	TypedExpected string `json:"typed_expected"`
}

type conformanceCorpus struct {
	Cases []conformanceCase `json:"cases"`
}

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintln(os.Stderr, "usage: driver <corpus.json>")
		os.Exit(2)
	}

	payload, err := os.ReadFile(os.Args[1])
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(2)
	}

	var corpus conformanceCorpus
	if err := json.Unmarshal(payload, &corpus); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(2)
	}

	var out strings.Builder

	fmt.Fprintf(&out, "#unicode\t%s\t-\n", unicode.Version)

	for index, testCase := range corpus.Cases {
		fmt.Fprintf(&out, "%d:text\t%s\t%s\n", index,
			hex.EncodeToString([]byte(testCase.TextExpected)),
			hex.EncodeToString([]byte(NormalizeText(testCase.Input))))
		fmt.Fprintf(&out, "%d:typed\t%s\t%s\n", index,
			hex.EncodeToString([]byte(testCase.TypedExpected)),
			hex.EncodeToString([]byte(NormalizeTyped(testCase.Input))))
	}

	os.Stdout.WriteString(out.String())
}
GODRV

    {
        printf 'module normalizationconformance\n\ngo 1.21\n\nrequire golang.org/x/text v0.14.0\n'
        if [[ -n "${ALAA_XTEXT_DIR:-}" && -d "${ALAA_XTEXT_DIR}" ]]; then
            printf '\nreplace golang.org/x/text => %s\n' "${ALAA_XTEXT_DIR}"
        fi
    } > "${WORKDIR}/go/go.mod"
}

# --------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------

RAN=0
FAILED=0

report_runtime() {
    local runtime="${1}" path="${2}" version

    version="$(read_metadata "${path}" '#unicode')"
    [[ -z "${version}" ]] && version="unknown"

    local note
    note="$(read_metadata "${path}" '#datasource')"

    compare_output "${runtime}" "${path}" "${CORPUS_ANSWERS}"

    RAN=$((RAN + 1))

    if unicode_major_too_old "${version}"; then
        FAILED=$((FAILED + 1))
        printf '%-12s fail    unicode data %s is older than the pinned minimum %d.0.0\n' \
            "${runtime}" "${version}" "${MIN_UNICODE_MAJOR}"
        return 0
    fi

    if [[ "${LAST_MISMATCHES}" -eq 0 ]]; then
        printf '%-12s pass    %d of %d answers matched the corpus   unicode %s\n' \
            "${runtime}" "${LAST_SEEN}" "${CORPUS_ANSWERS}" "${version}"
    else
        FAILED=$((FAILED + 1))
        printf '%-12s fail    %d answer(s) disagreed with the corpus   unicode %s\n' \
            "${runtime}" "${LAST_MISMATCHES}" "${version}"
    fi

    if [[ -n "${note}" ]]; then
        printf '%-12s note    unicode data source: %s\n' "${runtime}" "${note}"
    fi
}

report_driver_failure() {
    local runtime="${1}" path="${2}"

    RAN=$((RAN + 1))
    FAILED=$((FAILED + 1))
    printf '%-12s fail    driver did not execute\n' "${runtime}"
    sed 's/^/              /' "${path}" | head -20
}

report_skip() {
    printf '%-12s skipped: %s\n' "${1}" "${2}"
}

# Go needs golang.org/x/text/unicode/norm, which the standard library does not provide. A
# build that fails because that module cannot be fetched, or because the installed Go is
# older than the module wants, is an environment that could not run the runtime, which is
# a skip; any other build failure is a broken implementation, which is a failure. The two
# are told apart by the text of the build error, so the distinction is checkable rather
# than assumed, and the skip line prints that text.
go_cannot_run() {
    local path="${1}"

    grep -qE 'golang\.org/x/text|proxy\.golang\.org|module lookup disabled|dial tcp|no required module provides|missing go\.sum entry|Forbidden|connection refused|certificate|requires go >=|toolchain' "${path}"
}

main() {
    local argument

    for argument in "$@"; do
        case "${argument}" in
            -h|--help) usage; exit "${EXIT_OK}" ;;
            --self-test)
                if command -v python3 >/dev/null 2>&1; then PYTHON_BIN="python3"; fi
                self_test
                check_fixtures
                exit "${EXIT_OK}"
                ;;
            --verbose) VERBOSE=1 ;;
            *) printf 'Unknown option [%s].\n\n' "${argument}" >&2; usage >&2; exit "${EXIT_USAGE}" ;;
        esac
    done

    printf 'Alaa input-normalization cross-language conformance\n'
    printf 'skill root: %s\n' "${SKILL_ROOT}"
    check_fixtures

    discover_runtimes
    write_drivers
    printf '\n'

    if [[ -n "${PYTHON_BIN}" ]]; then
        # PYTHONDONTWRITEBYTECODE keeps the driver's import of the reference implementation
        # from leaving a __pycache__ directory inside the skill, because a harness that
        # writes into the tree it is checking is a harness that changes its own subject.
        if PYTHONDONTWRITEBYTECODE=1 "${PYTHON_BIN}" "${WORKDIR}/py/driver.py" "${CORPUS}" "${ASSET_DIR}" \
            > "${WORKDIR}/py.out" 2> "${WORKDIR}/py.err"; then
            report_runtime python "${WORKDIR}/py.out"
        else
            report_driver_failure python "${WORKDIR}/py.err"
        fi
    else
        report_skip python "${PYTHON_SKIP}"
    fi

    if [[ -n "${TS_MODE}" ]]; then
        local -a ts_command
        case "${TS_MODE}" in
            strip) ts_command=("${NODE_BIN}" "${WORKDIR}/ts/driver.ts") ;;
            strip-flag) ts_command=("${NODE_BIN}" --experimental-strip-types "${WORKDIR}/ts/driver.ts") ;;
            tsx) ts_command=(tsx "${WORKDIR}/ts/driver.ts") ;;
        esac

        if "${ts_command[@]}" "${CORPUS}" > "${WORKDIR}/ts.out" 2> "${WORKDIR}/ts.err"; then
            report_runtime typescript "${WORKDIR}/ts.out"
        else
            report_driver_failure typescript "${WORKDIR}/ts.err"
        fi
    else
        report_skip typescript "${TS_SKIP}"
    fi

    if [[ -n "${PHP_BIN}" ]]; then
        if "${PHP_BIN}" "${WORKDIR}/php/driver.php" "${CORPUS}" \
            > "${WORKDIR}/php.out" 2> "${WORKDIR}/php.err"; then
            report_runtime php "${WORKDIR}/php.out"
        else
            report_driver_failure php "${WORKDIR}/php.err"
        fi
    else
        report_skip php "${PHP_SKIP}"
    fi

    if [[ -n "${GO_BIN}" ]]; then
        if (cd "${WORKDIR}/go" && GOCACHE="${WORKDIR}/gocache" GOFLAGS=-mod=mod \
            "${GO_BIN}" build -o "${WORKDIR}/go/driver" . ) > "${WORKDIR}/go.build" 2>&1; then
            if "${WORKDIR}/go/driver" "${CORPUS}" > "${WORKDIR}/go.out" 2> "${WORKDIR}/go.err"; then
                report_runtime go "${WORKDIR}/go.out"
            else
                report_driver_failure go "${WORKDIR}/go.err"
            fi
        elif go_cannot_run "${WORKDIR}/go.build"; then
            report_skip go "golang.org/x/text/unicode/norm could not be built here; populate the module cache, allow the module proxy, or set ALAA_XTEXT_DIR to a local checkout the installed Go can build"
            sed 's/^/              /' "${WORKDIR}/go.build" | head -5
        else
            report_driver_failure go "${WORKDIR}/go.build"
        fi
    else
        report_skip go "${GO_SKIP}"
    fi

    printf '\nruntimes run: %d   runtimes failing: %d\n' "${RAN}" "${FAILED}"

    if [[ ${FAILED} -ne 0 ]]; then
        printf 'Result: FAIL. The implementations no longer share one normalization contract.\n' >&2
        printf 'Fix the implementation that disagreed. Regenerating the corpus to match it destroys the evidence.\n' >&2
        exit "${EXIT_DISAGREEMENT}"
    fi

    if [[ ${RAN} -lt 2 ]]; then
        printf 'Result: NOTHING PROVED. %d runtime(s) ran, so no two enforcement points were compared.\n' "${RAN}" >&2
        exit "${EXIT_ENVIRONMENT}"
    fi

    printf 'Result: PASS for every runtime run, over every case this corpus carries.\n'
    printf 'A skipped runtime is unproved, not passing, and an input the corpus does not carry is untested.\n'
}

main "$@"
