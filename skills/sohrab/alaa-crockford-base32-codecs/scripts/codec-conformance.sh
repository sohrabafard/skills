#!/usr/bin/env bash
#
# Cross-runtime conformance harness for the lowercase Crockford Base32 wire format
# owned by the skill `alaa-crockford-base32-codecs`.
#
# The harness drives all four shipped implementations over one shared corpus and
# fails when any two available runtimes disagree on a single case. Run it after every
# change to any implementation and paste its output into the change record.
set -euo pipefail

readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
readonly SKILL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

readonly EXIT_OK=0
readonly EXIT_USAGE=2
readonly EXIT_DISAGREEMENT=3
readonly EXIT_ENVIRONMENT=4
readonly EXIT_SELF_TEST=5

usage() {
    cat <<'EOF'
Usage: codec-conformance.sh [--help] [--self-test] [--verbose]

Runs the PHP, JavaScript, shell, and HAProxy Lua implementations of the Crockford
Base32 wire format over one shared corpus and compares their answers case by case.

Options:
    -h, --help      Show this help
    --self-test     Check the harness comparator itself, then exit
    --verbose       Print every case and every runtime answer, not only failures

Runtime selection:
    php             php
    javascript      node
    shell           scripts/crockford-base32-cli.sh with python3
    lua             lua5.4, lua5.3, lua5.2, lua5.1, lua, or luajit

    A runtime whose interpreter is absent is reported as skipped and excluded from
    the comparison. The harness never reports agreement for a runtime it did not run.

Exit codes:
    0  Every available runtime agreed on every case.
       Caller obligation: none.
    2  Usage error: an unknown option was supplied.
       Caller obligation: fix the invocation and retry; do not retry unchanged.
    3  At least two runtimes disagreed, or a runtime failed to execute.
       Caller obligation: treat the wire format as broken and do not ship or copy
       any implementation until every reported case agrees again.
    4  Fewer than two runtimes are available, so no comparison was possible.
       Caller obligation: install the missing interpreters and rerun; do not record
       this as a pass.
    5  The harness comparator failed its own self-test.
       Caller obligation: fix the harness before trusting any result it reports.
EOF
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
# --------------------------------------------------------------------------------

DISAGREEMENTS=0
CASES=0

# Compare one case across runtimes.
# Arguments: label, then one "runtime=answer" pair per available runtime.
compare_case() {
    local label="${1}"
    shift

    CASES=$((CASES + 1))

    local reference="" reference_name="" pair name answer mismatch=0

    for pair in "$@"; do
        name="${pair%%=*}"
        answer="${pair#*=}"

        if [[ -z "${reference_name}" ]]; then
            reference="${answer}"
            reference_name="${name}"
            continue
        fi

        if [[ "${answer}" != "${reference}" ]]; then
            mismatch=1
        fi
    done

    if [[ ${mismatch} -eq 0 ]]; then
        if [[ ${VERBOSE} -eq 1 ]]; then
            printf 'agree     %-52s %s\n' "${label}" "${reference}"
        fi
        return 0
    fi

    DISAGREEMENTS=$((DISAGREEMENTS + 1))
    printf 'DISAGREE  %s\n' "${label}"

    for pair in "$@"; do
        printf '            %-12s %s\n' "${pair%%=*}" "${pair#*=}"
    done

    return 0
}

self_test() {
    local failures=0

    DISAGREEMENTS=0
    CASES=0
    compare_case "self-test agreement" "php=OK|5" "javascript=OK|5" "lua=OK|5" >/dev/null
    if [[ ${DISAGREEMENTS} -ne 0 ]]; then
        echo "FAIL  comparator reported a disagreement for identical answers" >&2
        failures=$((failures + 1))
    else
        echo "pass  comparator accepts identical answers"
    fi

    DISAGREEMENTS=0
    compare_case "self-test disagreement" "php=OK|5" "javascript=OK|50" "lua=OK|5" >/dev/null
    if [[ ${DISAGREEMENTS} -ne 1 ]]; then
        echo "FAIL  comparator missed a differing answer" >&2
        failures=$((failures + 1))
    else
        echo "pass  comparator detects a differing answer"
    fi

    DISAGREEMENTS=0
    compare_case "self-test error text" "php=ERR|bad" "javascript=ERR|worse" >/dev/null
    if [[ ${DISAGREEMENTS} -ne 1 ]]; then
        echo "FAIL  comparator missed differing error text" >&2
        failures=$((failures + 1))
    else
        echo "pass  comparator detects differing error text"
    fi

    DISAGREEMENTS=0
    compare_case "self-test ok versus err" "php=OK|5" "javascript=ERR|nope" >/dev/null
    if [[ ${DISAGREEMENTS} -ne 1 ]]; then
        echo "FAIL  comparator missed success against failure" >&2
        failures=$((failures + 1))
    else
        echo "pass  comparator detects success against failure"
    fi

    DISAGREEMENTS=0
    CASES=0

    if [[ ${failures} -ne 0 ]]; then
        printf '\n%d comparator self-test case(s) failed.\n' "${failures}" >&2
        exit "${EXIT_SELF_TEST}"
    fi

    printf '\nComparator self-test passed.\n'
}

# --------------------------------------------------------------------------------
# Runtime discovery
# --------------------------------------------------------------------------------

PHP_BIN=""
NODE_BIN=""
LUA_BIN=""
PYTHON_BIN_FOUND=""
SKIPPED=()

discover_runtimes() {
    local candidate

    if command -v php >/dev/null 2>&1; then
        PHP_BIN="php"
    else
        SKIPPED+=("php: no 'php' on PATH")
    fi

    if command -v node >/dev/null 2>&1; then
        NODE_BIN="node"
    else
        SKIPPED+=("javascript: no 'node' on PATH")
    fi

    for candidate in lua5.4 lua5.3 lua5.2 lua5.1 lua luajit; do
        if command -v "${candidate}" >/dev/null 2>&1; then
            LUA_BIN="${candidate}"
            break
        fi
    done

    if [[ -z "${LUA_BIN}" ]]; then
        SKIPPED+=("lua: no lua5.4, lua5.3, lua5.2, lua5.1, lua, or luajit on PATH")
    fi

    for candidate in python3 python; do
        if command -v "${candidate}" >/dev/null 2>&1 \
            && "${candidate}" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' >/dev/null 2>&1; then
            PYTHON_BIN_FOUND="${candidate}"
            break
        fi
    done

    if [[ -z "${PYTHON_BIN_FOUND}" ]]; then
        SKIPPED+=("shell: no Python 3.9+ interpreter for crockford-base32-cli.sh")
    fi
}

# --------------------------------------------------------------------------------
# Drivers
#
# Every driver answers on one line: "OK|<value>" or "ERR|<message>". Byte payloads
# cross the driver boundary as hexadecimal because a process argument cannot carry
# raw binary; the PHP, JavaScript, and Lua library functions themselves take bytes.
# --------------------------------------------------------------------------------

write_drivers() {
    WORKDIR="$(mktemp -d)"

    cat > "${WORKDIR}/driver.php" <<PHPDRIVER
<?php
require '${SKILL_ROOT}/assets/crockford-base32/CrockfordBase32Codec.php';
PHPDRIVER

    cat >> "${WORKDIR}/driver.php" <<'PHPDRIVER'

use App\Support\Encoding\CrockfordBase32Codec as Codec;

function parseHex(string $value): string
{
    if (preg_match('/\A(?:[0-9a-fA-F]{2})*\z/', $value) !== 1) {
        throw new InvalidArgumentException('Byte payload must be canonical hexadecimal text.');
    }

    return $value === '' ? '' : (string) hex2bin($value);
}

$command = $argv[1] ?? '';
$value = $argv[2] ?? '';

try {
    switch ($command) {
        case 'encode-bytes': $result = Codec::encodeBytes(parseHex($value)); break;
        case 'decode-bytes': $result = bin2hex(Codec::decodeBytes($value)); break;
        case 'encode-int': $result = Codec::encodeInt($value); break;
        case 'decode-int': $result = Codec::decodeInt($value); break;
        case 'encode-string': $result = Codec::encodeString($value); break;
        case 'decode-string': $result = Codec::decodeString($value); break;
        case 'encode-uuidv7': $result = Codec::encodeUuidV7($value); break;
        case 'decode-uuidv7': $result = Codec::decodeUuidV7($value); break;
        default: throw new InvalidArgumentException(sprintf('Unsupported command [%s].', $command));
    }

    echo "OK|" . $result . "\n";
} catch (Throwable $error) {
    echo "ERR|" . $error->getMessage() . "\n";
}
PHPDRIVER

    cat > "${WORKDIR}/driver.mjs" <<NODEDRIVER
import { CrockfordBase32Codec as Codec } from '${SKILL_ROOT}/assets/crockford-base32/crockford-base32-codec.mjs';
NODEDRIVER

    cat >> "${WORKDIR}/driver.mjs" <<'NODEDRIVER'

const parseHex = (value) => {
  if (!/^(?:[0-9a-fA-F]{2})*$/.test(value)) {
    throw new TypeError('Byte payload must be canonical hexadecimal text.');
  }

  const bytes = new Uint8Array(value.length / 2);

  for (let index = 0; index < bytes.length; index += 1) {
    bytes[index] = Number.parseInt(value.slice(index * 2, index * 2 + 2), 16);
  }

  return bytes;
};

const toHex = (bytes) => Array.from(bytes, (byte) => byte.toString(16).padStart(2, '0')).join('');

const command = process.argv[2] ?? '';
const value = process.argv[3] ?? '';

try {
  let result;

  switch (command) {
    case 'encode-bytes': result = Codec.encodeBytes(parseHex(value)); break;
    case 'decode-bytes': result = toHex(Codec.decodeBytes(value)); break;
    case 'encode-int': result = Codec.encodeInt(value); break;
    case 'decode-int': result = Codec.decodeInt(value); break;
    case 'encode-string': result = Codec.encodeString(value); break;
    case 'decode-string': result = Codec.decodeString(value); break;
    case 'encode-uuidv7': result = Codec.encodeUuidV7(value); break;
    case 'decode-uuidv7': result = Codec.decodeUuidV7(value); break;
    default: throw new TypeError(`Unsupported command [${command}].`);
  }

  process.stdout.write(`OK|${result}\n`);
} catch (error) {
  process.stdout.write(`ERR|${error.message}\n`);
}
NODEDRIVER

    cat > "${WORKDIR}/driver.lua" <<LUADRIVER
local Codec = dofile('${SKILL_ROOT}/assets/haproxy/crockford-base32-codec.lua')
LUADRIVER

    cat >> "${WORKDIR}/driver.lua" <<'LUADRIVER'

local function parse_hex(value)
    if not value:match("^[0-9a-fA-F]*$") or (#value % 2) ~= 0 then
        error("Byte payload must be canonical hexadecimal text.", 0)
    end

    local parts = {}

    for index = 1, #value, 2 do
        parts[#parts + 1] = string.char(tonumber(value:sub(index, index + 1), 16))
    end

    return table.concat(parts)
end

local function to_hex(value)
    local parts = {}

    for index = 1, #value do
        parts[index] = string.format("%02x", value:byte(index))
    end

    return table.concat(parts)
end

local command = arg[1] or ""
local value = arg[2] or ""

local dispatch = {
    ["encode-bytes"] = function(input) return Codec.encode_bytes(parse_hex(input)) end,
    ["decode-bytes"] = function(input) return to_hex(Codec.decode_bytes(input)) end,
    ["encode-int"] = function(input) return Codec.encode_int(input) end,
    ["decode-int"] = function(input) return Codec.decode_int(input) end,
    ["encode-string"] = function(input) return Codec.encode_string(input) end,
    ["decode-string"] = function(input) return Codec.decode_string(input) end,
    ["encode-uuidv7"] = function(input) return Codec.encode_uuid_v7(input) end,
    ["decode-uuidv7"] = function(input) return Codec.decode_uuid_v7(input) end,
}

local handler = dispatch[command]

if handler == nil then
    io.write("ERR|Unsupported command [" .. command .. "].\n")
    os.exit(0)
end

local ok, result = pcall(handler, value)

if ok then
    io.write("OK|" .. result .. "\n")
else
    io.write("ERR|" .. tostring(result) .. "\n")
end
LUADRIVER
}

run_php() { "${PHP_BIN}" "${WORKDIR}/driver.php" "${1}" "${2}"; }
run_node() { "${NODE_BIN}" "${WORKDIR}/driver.mjs" "${1}" "${2}"; }
run_lua() { "${LUA_BIN}" "${WORKDIR}/driver.lua" "${1}" "${2}"; }

# The shell runtime is exercised through the shipped CLI so the harness proves the
# artifact callers actually run, not a private copy of its logic.
run_shell() {
    local command="${1}" value="${2}" output status=0

    output="$(PYTHON_BIN="${PYTHON_BIN_FOUND}" bash "${SKILL_ROOT}/scripts/crockford-base32-cli.sh" "${command}" "${value}" 2>&1)" || status=$?

    if [[ ${status} -eq 0 ]]; then
        printf 'OK|%s\n' "${output}"
    else
        printf 'ERR|%s\n' "${output}"
    fi
}

# --------------------------------------------------------------------------------
# Corpus
# --------------------------------------------------------------------------------

run_case() {
    local command="${1}" value="${2}" label="${3}"
    local answers=()

    if [[ -n "${PHP_BIN}" ]]; then answers+=("php=$(run_php "${command}" "${value}")"); fi
    if [[ -n "${NODE_BIN}" ]]; then answers+=("javascript=$(run_node "${command}" "${value}")"); fi
    if [[ -n "${PYTHON_BIN_FOUND}" ]]; then answers+=("shell=$(run_shell "${command}" "${value}")"); fi
    if [[ -n "${LUA_BIN}" ]]; then answers+=("lua=$(run_lua "${command}" "${value}")"); fi

    compare_case "${label}" "${answers[@]}"
}

run_corpus() {
    local value

    # Integer magnitudes, including every boundary the four runtimes represent
    # differently in their native numeric types.
    for value in 0 1 31 32 1023 4294967295 9007199254740991 9007199254740993 \
        9223372036854775807 9223372036854775808 18446744073709551615 \
        18446744073709551616 1606938044258990275541962092341162602522202993782792835301375; do
        run_case encode-int "${value}" "encode-int ${value}"
        run_case encode-int "-${value}" "encode-int -${value}"
    done

    # Integer input grammar. Every case below was accepted by at least one runtime
    # and rejected by another before the shared grammar was enforced.
    run_case encode-int "-0" "encode-int -0"
    run_case encode-int "007" "encode-int 007 (leading zeros)"
    run_case encode-int "" "encode-int empty"
    run_case encode-int $'12\n' 'encode-int "12\\n" (D3)'
    run_case encode-int $'\n42\t' 'encode-int "\\n42\\t" (D4)'
    run_case encode-int "+5" "encode-int +5 (D4)"
    run_case encode-int " 12 " "encode-int ' 12 ' (D4)"
    run_case encode-int "1_0" "encode-int 1_0 (D4)"
    run_case encode-int "١٢" "encode-int Arabic-Indic digits (D4)"
    run_case encode-int "0x10" "encode-int 0x10 (D4)"
    run_case encode-int "0b101" "encode-int 0b101 (D4)"
    run_case encode-int "0o17" "encode-int 0o17 (D4)"
    run_case encode-int "  " "encode-int spaces (D4)"
    run_case encode-int "12.0" "encode-int 12.0"
    run_case encode-int "abc" "encode-int abc"

    # Integer payload decoding, including case folding, aliases, and minimality.
    run_case decode-int "3ttx" "decode-int 3ttx (contract example)"
    run_case decode-int "3TTX" "decode-int uppercase"
    run_case decode-int "3TtX" "decode-int mixed case"
    run_case decode-int "3t-tx" "decode-int inner hyphen"
    run_case decode-int "-3ttx" "decode-int negative"
    run_case decode-int "-0" "decode-int -0"
    run_case decode-int "" "decode-int empty"
    run_case decode-int "-" "decode-int lone sign"
    run_case decode-int "00" "decode-int 00 (non-minimal)"
    run_case decode-int "01" "decode-int 01 (non-minimal)"
    run_case decode-int "o1" "decode-int o1 (non-minimal via alias)"
    run_case decode-int "i" "decode-int alias i"
    run_case decode-int "I" "decode-int alias I"
    run_case decode-int "l" "decode-int alias l"
    run_case decode-int "L" "decode-int alias L"
    run_case decode-int "1o" "decode-int alias o"
    run_case decode-int "1O" "decode-int alias O"
    run_case decode-int "u" "decode-int u is not an alias"
    run_case decode-int "U" "decode-int U is not an alias"
    run_case decode-int "zuz" "decode-int out-of-alphabet u"
    run_case decode-int "a!b" "decode-int out-of-alphabet punctuation"
    run_case decode-int "zzzzzzzzzzzzz" "decode-int wide magnitude"

    # Byte payloads, including the trailing padding-bit rule.
    run_case encode-bytes "" "encode-bytes empty"
    run_case encode-bytes "00" "encode-bytes 00"
    run_case encode-bytes "ff" "encode-bytes ff"
    run_case encode-bytes "0102030405" "encode-bytes 5 bytes"
    run_case encode-bytes "000102030405060708090a0b0c0d0e0f" "encode-bytes 16 bytes"
    run_case encode-bytes "zz" "encode-bytes invalid hex"
    run_case encode-bytes "abc" "encode-bytes odd-length hex"
    run_case decode-bytes "" "decode-bytes empty"
    run_case decode-bytes "z0" "decode-bytes z0 (zero padding bits)"
    run_case decode-bytes "zz" "decode-bytes zz (non-zero padding bits)"
    run_case decode-bytes "00" "decode-bytes 00"
    run_case decode-bytes "ZW" "decode-bytes uppercase"
    run_case decode-bytes "-z0-" "decode-bytes leading and trailing hyphen"
    run_case decode-bytes "z---0" "decode-bytes hyphen run"
    run_case decode-bytes "iIlL1111" "decode-bytes aliases i I l L"
    run_case decode-bytes "oOoO0000" "decode-bytes aliases o O"
    run_case decode-bytes "u0" "decode-bytes u is rejected"
    run_case decode-bytes "U0" "decode-bytes U is rejected"
    run_case decode-bytes "*~" "decode-bytes check symbols are rejected"
    run_case decode-bytes "a b" "decode-bytes embedded space"

    # UTF-8 string payloads.
    run_case encode-string "" "encode-string empty"
    run_case encode-string "hello" "encode-string ascii"
    run_case encode-string "naïve" "encode-string two-byte"
    run_case encode-string "日本語" "encode-string three-byte"
    run_case encode-string "🙂" "encode-string four-byte emoji"
    run_case encode-string "a🙂ü日" "encode-string mixed widths"
    run_case decode-string "" "decode-string empty"
    run_case decode-string "d1jprv3f" "decode-string ascii"
    run_case decode-string "zw" "decode-string invalid UTF-8 (D5)"
    run_case decode-string "zzzzzzzz" "decode-string invalid UTF-8 continuation"
    run_case decode-string "y0" "decode-string lone continuation byte"

    # UUIDv7 payloads.
    run_case encode-uuidv7 "018f7c8e-1f2a-7c3d-8e4f-5a6b7c8d9e0f" "encode-uuidv7 canonical"
    run_case encode-uuidv7 "018F7C8E-1F2A-7C3D-8E4F-5A6B7C8D9E0F" "encode-uuidv7 uppercase"
    run_case encode-uuidv7 "018f7c8e-1f2a-4c3d-8e4f-5a6b7c8d9e0f" "encode-uuidv7 version 4 rejected"
    run_case encode-uuidv7 "018f7c8e-1f2a-7c3d-0e4f-5a6b7c8d9e0f" "encode-uuidv7 bad variant rejected"
    run_case encode-uuidv7 "018f7c8e1f2a7c3d8e4f5a6b7c8d9e0f" "encode-uuidv7 unhyphenated rejected"
    run_case encode-uuidv7 "" "encode-uuidv7 empty rejected"
    run_case decode-uuidv7 "067qs3gz59y3v3jfb9nqs3cy1w" "decode-uuidv7 canonical"
    run_case decode-uuidv7 "067QS3GZ59Y3V3JFB9NQS3CY1W" "decode-uuidv7 uppercase"
    run_case decode-uuidv7 "067qs3gz-59y3v3jf-b9nqs3cy1w" "decode-uuidv7 hyphenated"
    run_case decode-uuidv7 "067qs3gz5963v3jfb9nqs3cy1w" "decode-uuidv7 version 4 rejected"
    run_case decode-uuidv7 "067qs3gz59y3t3jfb9nqs3cy1w" "decode-uuidv7 bad variant rejected"
    run_case decode-uuidv7 "067qs3gz59y3v3jfb9nqs3cy1x" "decode-uuidv7 non-zero padding bits rejected"
    run_case decode-uuidv7 "not-valid" "decode-uuidv7 short payload rejected"
    run_case decode-uuidv7 "" "decode-uuidv7 empty rejected"
    run_case decode-uuidv7 "067qs3gz59y3v3jfb9nqs3cy1w00" "decode-uuidv7 long payload rejected"
}

# --------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------

main() {
    local argument

    for argument in "$@"; do
        case "${argument}" in
            -h|--help) usage; exit "${EXIT_OK}" ;;
            --self-test) self_test; exit "${EXIT_OK}" ;;
            --verbose) VERBOSE=1 ;;
            *) printf 'Unknown option [%s].\n\n' "${argument}" >&2; usage >&2; exit "${EXIT_USAGE}" ;;
        esac
    done

    discover_runtimes

    local available=0
    [[ -n "${PHP_BIN}" ]] && available=$((available + 1))
    [[ -n "${NODE_BIN}" ]] && available=$((available + 1))
    [[ -n "${PYTHON_BIN_FOUND}" ]] && available=$((available + 1))
    [[ -n "${LUA_BIN}" ]] && available=$((available + 1))

    printf 'Crockford Base32 cross-runtime conformance\n'
    printf 'skill root: %s\n' "${SKILL_ROOT}"
    printf 'runtimes compared: %d of 4\n' "${available}"
    [[ -n "${PHP_BIN}" ]] && printf '  php         %s\n' "$(php -r 'echo PHP_VERSION;' 2>/dev/null || echo unknown)"
    [[ -n "${NODE_BIN}" ]] && printf '  javascript  %s %s\n' "${NODE_BIN}" "$("${NODE_BIN}" --version 2>/dev/null || echo unknown)"
    [[ -n "${PYTHON_BIN_FOUND}" ]] && printf '  shell       crockford-base32-cli.sh via %s\n' "$("${PYTHON_BIN_FOUND}" -V 2>&1)"
    [[ -n "${LUA_BIN}" ]] && printf '  lua         %s\n' "$("${LUA_BIN}" -v 2>&1 | head -1)"

    local skip
    for skip in "${SKIPPED[@]:-}"; do
        [[ -n "${skip}" ]] && printf 'SKIPPED %s\n' "${skip}"
    done

    if [[ ${available} -lt 2 ]]; then
        printf '\nFewer than two runtimes are available, so nothing was compared.\n' >&2
        exit "${EXIT_ENVIRONMENT}"
    fi

    write_drivers
    printf '\n'
    run_corpus

    printf '\ncases: %d   disagreements: %d\n' "${CASES}" "${DISAGREEMENTS}"

    if [[ ${DISAGREEMENTS} -ne 0 ]]; then
        printf 'Result: FAIL. The four implementations no longer share one wire format.\n' >&2
        exit "${EXIT_DISAGREEMENT}"
    fi

    printf 'Result: PASS. Every available runtime agreed on every case.\n'
}

main "$@"
