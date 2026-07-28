#!/usr/bin/env bash
#
# Cross-language conformance harness for the Alaa permission bitmap, owned by the skill
# `alaa-permission-generator`.
#
# It drives every canonical implementation under `assets/permission-bitmap/` over the one
# corpus at `scripts/permission-bitmap-corpus.json` and fails when any implementation
# disagrees with the corpus on any case. Run it after every change to any canonical
# implementation and paste its output into the change record, because a change proved in one
# runtime is not proved in the others.
#
# A runtime whose interpreter or toolchain is absent is reported as skipped and excluded.
# The harness never reports a pass for a runtime it did not run.
set -euo pipefail

readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
readonly SKILL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly ASSET_DIR="${SKILL_ROOT}/assets/permission-bitmap"
readonly CORPUS="${SKILL_ROOT}/scripts/permission-bitmap-corpus.json"

readonly EXIT_OK=0
readonly EXIT_USAGE=2
readonly EXIT_DISAGREEMENT=3
readonly EXIT_ENVIRONMENT=4
readonly EXIT_SELF_TEST=5
readonly EXIT_CORPUS=6

usage() {
    cat <<'USAGEEOF'
Usage: bitmap-conformance.sh [--help] [--self-test] [--verbose]

Runs the Go, PHP, and TypeScript canonical permission-bitmap decoders over one shared
corpus and compares each answer against the answer the corpus requires.

Options:
    -h, --help      Show this help
    --self-test     Check the harness comparator and the corpus checksum, then exit
    --verbose       Print every case and every answer, not only failures

Runtime selection:
    go              go, built as a throwaway module from assets/permission-bitmap
    php             php 8.2 or newer
    typescript      node with TypeScript type stripping, or node with tsx

    A runtime whose toolchain is absent is reported as "skipped: <runtime> not installed"
    and excluded. The harness never reports a pass for a runtime it did not run.

Exit codes:
    0  Every available runtime matched the corpus on every case.
       Caller obligation: none.
    2  Usage error: an unknown option was supplied.
       Caller obligation: fix the invocation and retry; do not retry unchanged.
    3  At least one runtime disagreed with the corpus, or a driver failed to execute.
       Caller obligation: treat the bitmap contract as broken and ship no implementation
       and no consumer change until every reported case matches again.
    4  No runtime was available, so nothing was proved.
       Caller obligation: install a toolchain and rerun; do not record this as a pass.
    5  The harness comparator failed its own self-test.
       Caller obligation: fix the harness before trusting any result it reports.
    6  The corpus checksum does not match the case array it covers.
       Caller obligation: find which copy of the corpus drifted and reconcile it before
       reading any result, because two runtimes can agree on a corpus that is wrong.
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

# --------------------------------------------------------------------------------
# Comparator
#
# Every driver writes one line per case: "<case_id>\t<expected>\t<actual>". The driver
# reads the expectation from the same corpus it is being tested against, so a runtime that
# reports a case at all reports what that case required.
# --------------------------------------------------------------------------------

LAST_SEEN=0
LAST_MISMATCHES=0

# Sets LAST_SEEN and LAST_MISMATCHES rather than printing them, so diagnostic lines and the
# result never share one stream and a mismatch report can never be read as a count.
compare_output() {
    local runtime="${1}" path="${2}" expected_cases="${3}"
    local seen=0 mismatches=0 case_id expected actual

    while IFS=$'\t' read -r case_id expected actual; do
        [[ -z "${case_id}" ]] && continue
        seen=$((seen + 1))

        if [[ "${expected}" == "${actual}" ]]; then
            if [[ ${VERBOSE} -eq 1 ]]; then
                printf '  match     %-12s %-38s %s\n' "${runtime}" "${case_id}" "${actual}"
            fi
            continue
        fi

        mismatches=$((mismatches + 1))
        printf '  MISMATCH  %-12s %s\n' "${runtime}" "${case_id}"
        printf '              corpus requires %s\n' "${expected}"
        printf '              %s answered     %s\n' "${runtime}" "${actual}"
    done < "${path}"

    if [[ ${seen} -ne ${expected_cases} ]]; then
        printf '  MISSING   %-12s reported %d of %d cases\n' "${runtime}" "${seen}" "${expected_cases}"
        mismatches=$((mismatches + 1))
    fi

    LAST_SEEN="${seen}"
    LAST_MISMATCHES="${mismatches}"
}

self_test() {
    local failures=0 scratch
    scratch="$(mktemp -d)"

    printf 'a\tOK|1\tOK|1\nb\tERR|x\tERR|x\n' > "${scratch}/agree.tsv"
    compare_output selftest "${scratch}/agree.tsv" 2 >/dev/null
    if [[ "${LAST_SEEN}" -eq 2 && "${LAST_MISMATCHES}" -eq 0 ]]; then
        echo 'pass  comparator accepts answers that match the corpus'
    else
        echo 'FAIL  comparator rejected answers that match the corpus' >&2
        failures=$((failures + 1))
    fi

    printf 'a\tOK|1\tOK|2\n' > "${scratch}/differ.tsv"
    compare_output selftest "${scratch}/differ.tsv" 1 >/dev/null
    if [[ "${LAST_MISMATCHES}" -eq 1 ]]; then
        echo 'pass  comparator detects an answer that differs from the corpus'
    else
        echo 'FAIL  comparator missed an answer that differs from the corpus' >&2
        failures=$((failures + 1))
    fi

    printf 'a\tERR|empty_bitmap\tERR|invalid_bitmap\n' > "${scratch}/code.tsv"
    compare_output selftest "${scratch}/code.tsv" 1 >/dev/null
    if [[ "${LAST_MISMATCHES}" -eq 1 ]]; then
        echo 'pass  comparator detects a wrong error code'
    else
        echo 'FAIL  comparator accepted a wrong error code' >&2
        failures=$((failures + 1))
    fi

    printf 'a\tOK|1\tOK|1\n' > "${scratch}/short.tsv"
    compare_output selftest "${scratch}/short.tsv" 2 >/dev/null
    if [[ "${LAST_MISMATCHES}" -eq 1 ]]; then
        echo 'pass  comparator detects a driver that skipped a case'
    else
        echo 'FAIL  comparator accepted a driver that skipped a case' >&2
        failures=$((failures + 1))
    fi

    rm -rf "${scratch}"

    if [[ ${failures} -ne 0 ]]; then
        printf '\n%d comparator self-test case(s) failed.\n' "${failures}" >&2
        exit "${EXIT_SELF_TEST}"
    fi

    printf '\nComparator self-test passed.\n'
}

# --------------------------------------------------------------------------------
# Corpus checksum
#
# The checksum covers the case array only, canonicalised as JSON with sorted keys and no
# separator spaces. It is what makes a drifted copy of the corpus visible instead of silent.
# --------------------------------------------------------------------------------

CORPUS_CASES=0

check_corpus() {
    local declared computed

    if [[ ! -f "${CORPUS}" ]]; then
        printf 'corpus: MISSING at %s\n' "${CORPUS}" >&2
        exit "${EXIT_CORPUS}"
    fi

    if command -v python3 >/dev/null 2>&1; then
        read -r declared computed CORPUS_CASES <<< "$(python3 -c '
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
        CORPUS_CASES="$(grep -c '"case_id"' "${CORPUS}")"
        printf 'corpus: %d cases read by line count, which is weaker evidence than the checksum\n' "${CORPUS_CASES}"
        return 0
    fi

    if [[ "${declared}" != "${computed}" ]]; then
        printf 'corpus: CHECKSUM MISMATCH\n' >&2
        printf '  declared %s\n' "${declared}" >&2
        printf '  computed %s\n' "${computed}" >&2
        exit "${EXIT_CORPUS}"
    fi

    printf 'corpus: %d cases, checksum verified %s\n' "${CORPUS_CASES}" "${computed}"
}

# --------------------------------------------------------------------------------
# Runtime discovery
# --------------------------------------------------------------------------------

GO_BIN=""
PHP_BIN=""
TS_MODE=""
NODE_BIN=""
GO_SKIP=""
PHP_SKIP=""
TS_SKIP=""

discover_runtimes() {
    if command -v go >/dev/null 2>&1; then
        GO_BIN="go"
    else
        GO_SKIP="go not installed"
    fi

    if command -v php >/dev/null 2>&1 \
        && php -r 'exit(PHP_VERSION_ID >= 80200 ? 0 : 1);' >/dev/null 2>&1; then
        PHP_BIN="php"
    elif command -v php >/dev/null 2>&1; then
        PHP_SKIP="php older than 8.2"
    else
        PHP_SKIP="php not installed"
    fi

    if command -v node >/dev/null 2>&1; then
        NODE_BIN="node"
        local probe
        probe="$(mktemp -d)"
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
}

# --------------------------------------------------------------------------------
# Drivers
#
# Each driver takes the corpus path, runs every case against the canonical implementation
# for its language, and writes "<case_id>\t<expected>\t<actual>" per case.
# --------------------------------------------------------------------------------

write_drivers() {
    WORKDIR="$(mktemp -d)"

    mkdir -p "${WORKDIR}/go" "${WORKDIR}/php" "${WORKDIR}/ts"

    sed 's/^package authz$/package main/' "${ASSET_DIR}/permission_bitmap.go" > "${WORKDIR}/go/permission_bitmap.go"
    printf 'module bitmapconformance\n\ngo 1.21\n' > "${WORKDIR}/go/go.mod"

    cat > "${WORKDIR}/go/driver.go" <<'GODRV'
package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

type conformanceCase struct {
	CaseID          string            `json:"case_id"`
	Op              string            `json:"op"`
	Access          string            `json:"access"`
	MaxPermissionID int               `json:"max_permission_id"`
	MaxEncodedLen   *int              `json:"max_encoded_length"`
	NamesByID       map[string]string `json:"names_by_id"`
	Permission      string            `json:"permission"`
	Expect          string            `json:"expect"`
}

type conformanceCorpus struct {
	Cases []conformanceCase `json:"cases"`
}

func errorCode(err error) string {
	switch {
	case errors.Is(err, ErrEmptyAccessBitmap):
		return "empty_bitmap"
	case errors.Is(err, ErrInvalidAccessBitmap):
		return "invalid_bitmap"
	case errors.Is(err, ErrAccessBitmapTooLong):
		return "bitmap_too_long"
	case errors.Is(err, ErrNoKnownPermissions):
		return "no_known_permissions"
	case errors.Is(err, ErrInvalidDecodeBound):
		return "invalid_decode_bound"
	default:
		return "unmapped_error:" + err.Error()
	}
}

func namesByID(raw map[string]string) map[int]string {
	names := make(map[int]string, len(raw))
	for key, value := range raw {
		id, err := strconv.Atoi(key)
		if err != nil {
			continue
		}
		names[id] = value
	}

	return names
}

func answer(testCase conformanceCase) string {
	names := namesByID(testCase.NamesByID)

	switch testCase.Op {
	case "decode_ids":
		var (
			ids []int
			err error
		)
		if testCase.MaxEncodedLen == nil {
			ids, err = DecodePermissionBitmap(testCase.Access, testCase.MaxPermissionID)
		} else {
			ids, err = DecodePermissionBitmapWithLimits(testCase.Access, testCase.MaxPermissionID, *testCase.MaxEncodedLen)
		}
		if err != nil {
			return "ERR|" + errorCode(err)
		}
		text := make([]string, 0, len(ids))
		for _, id := range ids {
			text = append(text, strconv.Itoa(id))
		}

		return "OK|" + strings.Join(text, ",")
	case "decode_set":
		var (
			set Set
			err error
		)
		if testCase.MaxEncodedLen == nil {
			set, err = DecodePermissionSet(testCase.Access, names, testCase.MaxPermissionID)
		} else {
			set, err = DecodePermissionSetWithLimits(testCase.Access, names, testCase.MaxPermissionID, *testCase.MaxEncodedLen)
		}
		if err != nil {
			return "ERR|" + errorCode(err)
		}
		granted := set.Names()
		sort.Strings(granted)

		return "OK|" + strings.Join(granted, ",")
	case "has":
		if HasPermission(testCase.Access, testCase.Permission, PermissionMap(names)) {
			return "OK|true"
		}

		return "OK|false"
	default:
		return "ERR|unsupported_op:" + testCase.Op
	}
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

	for _, testCase := range corpus.Cases {
		fmt.Printf("%s\t%s\t%s\n", testCase.CaseID, testCase.Expect, answer(testCase))
	}
}
GODRV

    cp "${ASSET_DIR}/PermissionBitmap.php" "${ASSET_DIR}/PermissionBitmapException.php" "${WORKDIR}/php/"

    cat > "${WORKDIR}/php/driver.php" <<'PHPDRV'
<?php

declare(strict_types=1);

require __DIR__.'/PermissionBitmap.php';
require __DIR__.'/PermissionBitmapException.php';

use Alaa\Support\Authorization\PermissionBitmap;
use Alaa\Support\Authorization\PermissionBitmapException;

$corpus = json_decode((string) file_get_contents($argv[1]), true, 512, JSON_THROW_ON_ERROR);

/**
 * @param  array<string, string>  $raw
 * @return array<int, string>
 */
function namesById(array $raw): array
{
    $names = [];

    foreach ($raw as $key => $value) {
        $names[(int) $key] = $value;
    }

    return $names;
}

/**
 * @param  array<string, mixed>  $case
 */
function answer(array $case): string
{
    $names = namesById($case['names_by_id'] ?? []);
    $limit = $case['max_encoded_length'];

    try {
        switch ($case['op']) {
            case 'decode_ids':
                $ids = $limit === null
                    ? PermissionBitmap::decodeIds($case['access'], $case['max_permission_id'])
                    : PermissionBitmap::decodeIds($case['access'], $case['max_permission_id'], $limit);

                return 'OK|'.implode(',', $ids);
            case 'decode_set':
                $set = $limit === null
                    ? PermissionBitmap::decodeSet($case['access'], $names, $case['max_permission_id'])
                    : PermissionBitmap::decodeSet($case['access'], $names, $case['max_permission_id'], $limit);
                $granted = array_keys($set);
                sort($granted, SORT_STRING);

                return 'OK|'.implode(',', $granted);
            case 'has':
                $granted = PermissionBitmap::hasPermission(
                    $case['access'],
                    $case['permission'],
                    $names,
                    $case['max_permission_id'],
                );

                return 'OK|'.($granted ? 'true' : 'false');
            default:
                return 'ERR|unsupported_op:'.$case['op'];
        }
    } catch (PermissionBitmapException $exception) {
        return 'ERR|'.$exception->errorCode;
    }
}

foreach ($corpus['cases'] as $case) {
    echo $case['case_id']."\t".$case['expect']."\t".answer($case)."\n";
}
PHPDRV

    cp "${ASSET_DIR}/permission-bitmap.ts" "${WORKDIR}/ts/"

    cat > "${WORKDIR}/ts/driver.ts" <<'TSDRV'
import { readFileSync } from "node:fs";
import {
  PermissionBitmapError,
  decodePermissionIds,
  decodePermissionSet,
  hasPermission,
} from "./permission-bitmap.ts";

type ConformanceCase = {
  case_id: string;
  op: string;
  access: string;
  max_permission_id: number;
  max_encoded_length: number | null;
  names_by_id?: Record<string, string>;
  permission?: string;
  expect: string;
};

const namesById = (raw: Record<string, string> | undefined): Record<number, string> => {
  const names: Record<number, string> = {};

  for (const key of Object.keys(raw ?? {})) {
    names[Number(key)] = (raw ?? {})[key];
  }

  return names;
};

const answer = (testCase: ConformanceCase): string => {
  const names = namesById(testCase.names_by_id);
  const limit = testCase.max_encoded_length;

  try {
    if (testCase.op === "decode_ids") {
      const ids =
        limit === null
          ? decodePermissionIds(testCase.access, testCase.max_permission_id)
          : decodePermissionIds(testCase.access, testCase.max_permission_id, limit);

      return `OK|${ids.join(",")}`;
    }

    if (testCase.op === "decode_set") {
      const set =
        limit === null
          ? decodePermissionSet(testCase.access, names, testCase.max_permission_id)
          : decodePermissionSet(testCase.access, names, testCase.max_permission_id, limit);

      return `OK|${[...set].sort().join(",")}`;
    }

    if (testCase.op === "has") {
      const granted = hasPermission(
        testCase.access,
        testCase.permission ?? "",
        names,
        testCase.max_permission_id,
      );

      return `OK|${granted ? "true" : "false"}`;
    }

    return `ERR|unsupported_op:${testCase.op}`;
  } catch (error) {
    if (error instanceof PermissionBitmapError) {
      return `ERR|${error.errorCode}`;
    }

    throw error;
  }
};

const corpus = JSON.parse(readFileSync(process.argv[2], "utf8")) as {
  cases: ConformanceCase[];
};

const lines = corpus.cases.map(
  (testCase) => `${testCase.case_id}\t${testCase.expect}\t${answer(testCase)}`,
);

process.stdout.write(`${lines.join("\n")}\n`);
TSDRV
}

# --------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------

RAN=0
FAILED=0

report_runtime() {
    local runtime="${1}" path="${2}"

    compare_output "${runtime}" "${path}" "${CORPUS_CASES}"

    RAN=$((RAN + 1))

    if [[ "${LAST_MISMATCHES}" -eq 0 ]]; then
        printf '%-12s pass    %d of %d cases matched the corpus\n' "${runtime}" "${LAST_SEEN}" "${CORPUS_CASES}"
    else
        FAILED=$((FAILED + 1))
        printf '%-12s fail    %d case(s) disagreed with the corpus\n' "${runtime}" "${LAST_MISMATCHES}"
    fi
}

report_driver_failure() {
    local runtime="${1}" path="${2}"

    RAN=$((RAN + 1))
    FAILED=$((FAILED + 1))
    printf '%-12s fail    driver did not execute\n' "${runtime}"
    sed 's/^/              /' "${path}" | head -20
}

main() {
    local argument

    for argument in "$@"; do
        case "${argument}" in
            -h|--help) usage; exit "${EXIT_OK}" ;;
            --self-test) self_test; check_corpus; exit "${EXIT_OK}" ;;
            --verbose) VERBOSE=1 ;;
            *) printf 'Unknown option [%s].\n\n' "${argument}" >&2; usage >&2; exit "${EXIT_USAGE}" ;;
        esac
    done

    printf 'Alaa permission-bitmap cross-language conformance\n'
    printf 'skill root: %s\n' "${SKILL_ROOT}"
    check_corpus

    discover_runtimes
    write_drivers
    printf '\n'

    if [[ -n "${GO_BIN}" ]]; then
        if (cd "${WORKDIR}/go" && GOCACHE="${WORKDIR}/gocache" GOFLAGS=-mod=mod \
            "${GO_BIN}" run . "${CORPUS}" > "${WORKDIR}/go.out" 2> "${WORKDIR}/go.err"); then
            report_runtime go "${WORKDIR}/go.out"
        else
            report_driver_failure go "${WORKDIR}/go.err"
        fi
    else
        printf '%-12s skipped: %s\n' go "${GO_SKIP}"
    fi

    if [[ -n "${PHP_BIN}" ]]; then
        if "${PHP_BIN}" "${WORKDIR}/php/driver.php" "${CORPUS}" > "${WORKDIR}/php.out" 2> "${WORKDIR}/php.err"; then
            report_runtime php "${WORKDIR}/php.out"
        else
            report_driver_failure php "${WORKDIR}/php.err"
        fi
    else
        printf '%-12s skipped: %s\n' php "${PHP_SKIP}"
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
        printf '%-12s skipped: %s\n' typescript "${TS_SKIP}"
    fi

    printf '\nruntimes run: %d   runtimes failing: %d\n' "${RAN}" "${FAILED}"

    if [[ ${RAN} -eq 0 ]]; then
        printf 'Result: NOTHING PROVED. No runtime was available, so this run is not a pass.\n' >&2
        exit "${EXIT_ENVIRONMENT}"
    fi

    if [[ ${FAILED} -ne 0 ]]; then
        printf 'Result: FAIL. The canonical implementations no longer share one bitmap contract.\n' >&2
        exit "${EXIT_DISAGREEMENT}"
    fi

    printf 'Result: PASS for every runtime run. A skipped runtime is unproved, not passing.\n'
}

main "$@"
