#!/usr/bin/env bash
#
# Wire format owner: skill `alaa-crockford-base32-codecs`,
# `references/10-shared-codec-contract.md`. Change this file only together with the
# PHP, JavaScript, and HAProxy Lua implementations, then run
# `scripts/codec-conformance.sh` from that skill.
set -euo pipefail
IFS=$'\n\t'

readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"

readonly EXIT_OK=0
readonly EXIT_USAGE=2
readonly EXIT_INVALID_INPUT=3
readonly EXIT_ENVIRONMENT=4
readonly EXIT_SELF_TEST=5

readonly MINIMUM_PYTHON="3.9"

usage() {
    cat <<'EOF'
Usage: crockford-base32-cli.sh COMMAND [VALUE]

Commands:
    encode-bytes HEX           Encode raw bytes given as hexadecimal to Base32
    decode-bytes BASE32        Decode Base32 back to hexadecimal
    encode-int VALUE           Encode one signed integer to minimal Crockford Base32
    decode-int BASE32          Decode Crockford Base32 back to base-10 text
    encode-string VALUE        Encode one UTF-8 string to Base32
    decode-string BASE32       Decode Base32 back to a UTF-8 string
    generate-uuidv7            Generate one canonical UUIDv7 string
    encode-uuidv7 UUID         Encode one canonical UUIDv7 string to Base32
    decode-uuidv7 BASE32       Decode Base32 back to a canonical UUIDv7 string
    -h, --help                 Show this help
    --self-test                Run the contract examples and the regression cases

Integer grammar:
    - the only accepted form is -?[0-9]+ with nothing before or after it
    - leading zeros are accepted and normalized; -0 encodes as 0
    - whitespace, a leading +, base prefixes, digit separators, and non-ASCII
      digits are rejected

Notes:
    - encode-bytes takes hexadecimal because a shell argument cannot carry raw
      binary; the PHP, JavaScript, and Lua library functions take raw bytes.
    - Encode output always uses lowercase Crockford Base32.
    - This CLI requires Python 3.9 or newer and asserts the version before running.

Exit codes:
    0  Success. The result is on stdout.
    2  Usage error: unknown command, or a required argument was not supplied.
       Caller obligation: fix the invocation and retry; do not retry unchanged.
    3  Invalid input: the value violates the codec contract.
       Caller obligation: treat the input as rejected and do not substitute a
       fallback or empty value downstream.
    4  Environment error: no Python 3.9+ interpreter was found.
       Caller obligation: install or point PYTHON_BIN at a suitable interpreter;
       do not treat this as an input rejection.
    5  Self-test failure: this CLI disagrees with the codec contract.
       Caller obligation: stop using this copy of the CLI and report the failure
       against the skill that owns the contract.
EOF
}

find_python() {
    local candidate

    if [[ -n "${PYTHON_BIN:-}" ]]; then
        if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
            echo "Configured PYTHON_BIN is not executable: ${PYTHON_BIN}" >&2
            exit "${EXIT_ENVIRONMENT}"
        fi

        if ! is_supported_python "${PYTHON_BIN}"; then
            echo "Configured PYTHON_BIN is older than Python ${MINIMUM_PYTHON}: ${PYTHON_BIN}" >&2
            exit "${EXIT_ENVIRONMENT}"
        fi

        printf '%s\n' "${PYTHON_BIN}"
        return
    fi

    for candidate in python3 python; do
        if command -v "${candidate}" >/dev/null 2>&1 && is_supported_python "${candidate}"; then
            printf '%s\n' "${candidate}"
            return
        fi
    done

    echo "Python ${MINIMUM_PYTHON} or newer is required for ${SCRIPT_NAME}." >&2
    exit "${EXIT_ENVIRONMENT}"
}

# A bare `python` on PATH may be Python 2, which cannot parse the embedded program.
# The probe runs before the program is fed to the interpreter so the failure is a
# clear environment error rather than a SyntaxError.
is_supported_python() {
    "${1}" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' >/dev/null 2>&1
}

self_test() {
    local python_bin failures=0
    python_bin="$(find_python)"

    run_case() {
        local expectation="${1}" description="${2}"
        shift 2

        local observed status=0
        observed="$(run_program "${python_bin}" "$@" 2>&1)" || status=$?

        local actual
        if [[ ${status} -eq 0 ]]; then
            actual="ok:${observed}"
        else
            actual="exit${status}"
        fi

        if [[ "${actual}" == "${expectation}" ]]; then
            printf 'pass  %-34s %s\n' "${description}" "${actual}"
            return 0
        fi

        printf 'FAIL  %-34s expected [%s] observed [%s]\n' "${description}" "${expectation}" "${actual}"
        failures=$((failures + 1))
        return 0
    }

    echo "Contract examples (10-shared-codec-contract.md):"
    run_case "ok:9" "encode-int 9" encode-int 9
    run_case "ok:s" "encode-int 25" encode-int 25
    run_case "ok:3ttx" "encode-int 125789" encode-int 125789
    run_case "ok:125789" "decode-int 3ttx" decode-int 3ttx

    echo "Regression cases:"
    run_case "exit${EXIT_INVALID_INPUT}" "D3 trailing newline rejected" encode-int '12
'
    run_case "exit${EXIT_INVALID_INPUT}" "D4 leading plus rejected" encode-int '+5'
    run_case "exit${EXIT_INVALID_INPUT}" "D4 surrounding space rejected" encode-int ' 12 '
    run_case "exit${EXIT_INVALID_INPUT}" "D4 digit separator rejected" encode-int '1_0'
    run_case "exit${EXIT_INVALID_INPUT}" "D4 non-ASCII digit rejected" encode-int '١٢'
    run_case "exit${EXIT_INVALID_INPUT}" "D4 empty integer rejected" encode-int ''
    run_case "exit${EXIT_INVALID_INPUT}" "D4 hex prefix rejected" encode-int '0x10'
    run_case "exit${EXIT_INVALID_INPUT}" "D5 invalid UTF-8 rejected" decode-string zw
    run_case "ok:0" "-0 encodes as 0" encode-int -0
    run_case "exit${EXIT_INVALID_INPUT}" "u is not an alias" decode-int u
    run_case "exit${EXIT_INVALID_INPUT}" "non-zero padding bits rejected" decode-bytes zz
    run_case "ok:f8" "zero padding bits accepted" decode-bytes z0
    run_case "exit${EXIT_INVALID_INPUT}" "non-minimal integer rejected" decode-int 01
    run_case "exit${EXIT_USAGE}" "missing argument is a usage error" encode-int
    run_case "exit${EXIT_USAGE}" "unknown command is a usage error" not-a-command

    if [[ ${failures} -ne 0 ]]; then
        printf '\n%d self-test case(s) failed.\n' "${failures}" >&2
        exit "${EXIT_SELF_TEST}"
    fi

    printf '\nAll self-test cases passed.\n'
}

run_program() {
    local python_bin="${1}"
    shift

    "${python_bin}" - "$@" <<'PY'
import re
import sys
import time
import uuid

ALPHABET = "0123456789abcdefghjkmnpqrstvwxyz"
LOOKUP = {character: index for index, character in enumerate(ALPHABET)}
UUID_PATTERN = re.compile(
    r"\A[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\Z"
)
# `\Z` is the true end of the subject. `$` would accept a trailing newline.
INTEGER_PATTERN = re.compile(r"\A-?[0-9]+\Z")
HEX_PATTERN = re.compile(r"\A(?:[0-9a-fA-F]{2})*\Z")

EXIT_USAGE = 2
EXIT_INVALID_INPUT = 3


class UsageError(Exception):
    """Raised when the invocation itself is wrong, not the value."""


def encode_bytes(payload: bytes) -> str:
    if payload == b"":
        return ""

    buffer = 0
    bit_count = 0
    encoded: list = []

    for byte in payload:
        buffer = (buffer << 8) | byte
        bit_count += 8

        while bit_count >= 5:
            bit_count -= 5
            encoded.append(ALPHABET[(buffer >> bit_count) & 31])
            buffer &= (1 << bit_count) - 1

    if bit_count > 0:
        encoded.append(ALPHABET[(buffer << (5 - bit_count)) & 31])

    return "".join(encoded)


def normalize_encoded(value: str) -> str:
    normalized = value.lower().replace("-", "")
    return normalized.replace("i", "1").replace("l", "1").replace("o", "0")


def decode_bytes(encoded: str) -> bytes:
    normalized = normalize_encoded(encoded)

    if normalized == "":
        return b""

    buffer = 0
    bit_count = 0
    decoded = bytearray()

    for character in normalized:
        try:
            value = LOOKUP[character]
        except KeyError as exc:
            raise ValueError(f"Invalid Crockford Base32 character [{character}].") from exc

        buffer = (buffer << 5) | value
        bit_count += 5

        while bit_count >= 8:
            bit_count -= 8
            decoded.append((buffer >> bit_count) & 0xFF)
            buffer &= (1 << bit_count) - 1

    if bit_count > 0 and buffer != 0:
        raise ValueError("Invalid Crockford Base32 payload padding bits.")

    return bytes(decoded)


def parse_integer(text: str) -> int:
    # Bare `int()` accepts surrounding whitespace, a leading +, PEP 515 underscores,
    # and non-ASCII digits, none of which the other three runtimes accept.
    if INTEGER_PATTERN.match(text) is None:
        raise ValueError("Integer input must be a canonical base-10 integer.")

    return int(text)


def encode_int(value: int) -> str:
    if value == 0:
        return "0"

    negative = value < 0
    magnitude = -value if negative else value
    digits: list = []

    while magnitude > 0:
        magnitude, remainder = divmod(magnitude, 32)
        digits.append(ALPHABET[remainder])

    encoded = "".join(reversed(digits))
    return f"-{encoded}" if negative else encoded


def split_signed_encoded_integer(encoded: str):
    if encoded == "":
        raise ValueError("Integer payload cannot be empty.")

    negative = encoded.startswith("-")
    magnitude = normalize_encoded(encoded[1:] if negative else encoded)

    if magnitude == "":
        raise ValueError("Integer payload cannot be empty.")

    if len(magnitude) > 1 and magnitude[0] == "0":
        raise ValueError("Integer payload must use a minimal Crockford Base32 representation.")

    return negative, magnitude


def decode_int(encoded: str) -> str:
    negative, magnitude = split_signed_encoded_integer(encoded)
    value = 0

    for character in magnitude:
        try:
            digit = LOOKUP[character]
        except KeyError as exc:
            raise ValueError(f"Invalid Crockford Base32 integer character [{character}].") from exc

        value = (value * 32) + digit

    if negative and value != 0:
        return f"-{value}"

    return str(value)


def encode_string(value: str) -> str:
    try:
        payload = value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("Text input is not valid UTF-8.") from exc

    return encode_bytes(payload)


def decode_string(encoded: str) -> str:
    payload = decode_bytes(encoded)

    try:
        return payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Decoded payload is not valid UTF-8.") from exc


def parse_hex(value: str) -> bytes:
    # `bytes.fromhex` also accepts spaces between byte pairs, which the PHP,
    # JavaScript, and Lua drivers do not.
    if HEX_PATTERN.match(value) is None:
        raise ValueError("Byte payload must be canonical hexadecimal text.")

    return bytes.fromhex(value)


def generate_uuid_v7() -> str:
    random_bytes = bytearray(uuid.uuid4().bytes)
    milliseconds = int(time.time() * 1000)

    for index in range(5, -1, -1):
        random_bytes[index] = milliseconds & 0xFF
        milliseconds >>= 8

    random_bytes[6] = (random_bytes[6] & 0x0F) | 0x70
    random_bytes[8] = (random_bytes[8] & 0x3F) | 0x80

    return str(uuid.UUID(bytes=bytes(random_bytes)))


def uuid_to_bytes(value: str) -> bytes:
    normalized = value.lower()

    if UUID_PATTERN.match(normalized) is None:
        raise ValueError("UUID must be in canonical 8-4-4-4-12 hexadecimal form.")

    return bytes.fromhex(normalized.replace("-", ""))


def assert_uuid_v7_bytes(payload: bytes) -> None:
    if len(payload) != 16:
        raise ValueError("UUID payload must contain exactly 16 bytes.")

    if payload[6] >> 4 != 7:
        raise ValueError("UUID payload must be version 7.")

    if payload[8] & 0xC0 != 0x80:
        raise ValueError("UUID payload must use the RFC 4122 variant bits.")


def encode_uuid_v7(value: str) -> str:
    payload = uuid_to_bytes(value)
    assert_uuid_v7_bytes(payload)
    return encode_bytes(payload)


def decode_uuid_v7(encoded: str) -> str:
    payload = decode_bytes(encoded)
    assert_uuid_v7_bytes(payload)
    return str(uuid.UUID(bytes=payload))


def require_arg(arguments: list, position: int, label: str) -> str:
    try:
        return arguments[position]
    except IndexError as exc:
        raise UsageError(f"Missing required argument: {label}") from exc


def main(argv: list) -> int:
    command = require_arg(argv, 1, "command")

    if command == "encode-bytes":
        print(encode_bytes(parse_hex(require_arg(argv, 2, "hex"))))
        return 0
    if command == "decode-bytes":
        print(decode_bytes(require_arg(argv, 2, "base32")).hex())
        return 0
    if command == "encode-int":
        print(encode_int(parse_integer(require_arg(argv, 2, "value"))))
        return 0
    if command == "decode-int":
        print(decode_int(require_arg(argv, 2, "base32")))
        return 0
    if command == "encode-string":
        print(encode_string(require_arg(argv, 2, "value")))
        return 0
    if command == "decode-string":
        print(decode_string(require_arg(argv, 2, "base32")))
        return 0
    if command == "generate-uuidv7":
        print(generate_uuid_v7())
        return 0
    if command == "encode-uuidv7":
        print(encode_uuid_v7(require_arg(argv, 2, "uuid")))
        return 0
    if command == "decode-uuidv7":
        print(decode_uuid_v7(require_arg(argv, 2, "base32")))
        return 0

    raise UsageError(f"Unsupported command [{command}].")


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv))
    except UsageError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(EXIT_USAGE)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(EXIT_INVALID_INPUT)
PY
}

main() {
    if [[ $# -eq 0 ]]; then
        usage >&2
        exit "${EXIT_USAGE}"
    fi

    case "${1}" in
        -h|--help)
            usage
            exit "${EXIT_OK}"
            ;;
        --self-test)
            self_test
            exit "${EXIT_OK}"
            ;;
    esac

    local python_bin
    python_bin="$(find_python)"

    run_program "${python_bin}" "$@"
}

main "$@"
