#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"

usage() {
    cat <<'EOF'
Usage: crockford-base32-cli.sh COMMAND [VALUE]

Commands:
    encode-bytes HEX           Encode raw bytes from hexadecimal to Base32
    decode-bytes BASE32        Decode Base32 back to hexadecimal
    encode-int VALUE           Encode one signed integer to minimal Crockford Base32
    decode-int BASE32          Decode Crockford Base32 back to base-10 text
    encode-string VALUE        Encode one UTF-8 string to Base32
    decode-string BASE32       Decode Base32 back to a UTF-8 string
    generate-uuidv7            Generate one canonical UUIDv7 string
    encode-uuidv7 UUID         Encode one canonical UUIDv7 string to Base32
    decode-uuidv7 BASE32       Decode Base32 back to a canonical UUIDv7 string
    -h, --help                 Show this help

Integer strategy:
    - positive integers encode as minimal unsigned Crockford Base32 digits
    - negative integers encode as '-' plus the minimal unsigned magnitude
    - zero always encodes as '0'

Notes:
    - Encode output always uses lowercase Crockford Base32.
    - The CLI uses Python 3 internally so the byte and UUID work stays deterministic.
EOF
}

find_python() {
    if [[ -n "${PYTHON_BIN:-}" ]]; then
        command -v "${PYTHON_BIN}" >/dev/null 2>&1 || {
            echo "Configured PYTHON_BIN is not executable: ${PYTHON_BIN}" >&2
            exit 1
        }
        printf '%s\n' "${PYTHON_BIN}"
        return
    fi

    if command -v python3 >/dev/null 2>&1; then
        printf '%s\n' "python3"
        return
    fi

    if command -v python >/dev/null 2>&1; then
        printf '%s\n' "python"
        return
    fi

    echo "Python 3 is required for ${SCRIPT_NAME}." >&2
    exit 1
}

main() {
    if [[ $# -eq 0 ]]; then
        usage
        exit 1
    fi

    case "${1}" in
        -h|--help)
            usage
            exit 0
            ;;
    esac

    local python_bin
    python_bin="$(find_python)"

    "${python_bin}" - "$@" <<'PY'
import re
import sys
import time
import uuid

ALPHABET = "0123456789abcdefghjkmnpqrstvwxyz"
LOOKUP = {character: index for index, character in enumerate(ALPHABET)}
UUID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
)


def encode_bytes(payload: bytes) -> str:
    if payload == b"":
        return ""

    buffer = 0
    bit_count = 0
    encoded: list[str] = []

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


def encode_int(value: int) -> str:
    if value == 0:
        return "0"

    negative = value < 0
    magnitude = -value if negative else value
    digits: list[str] = []

    while magnitude > 0:
        magnitude, remainder = divmod(magnitude, 32)
        digits.append(ALPHABET[remainder])

    encoded = "".join(reversed(digits))
    return f"-{encoded}" if negative else encoded


def split_signed_encoded_integer(encoded: str) -> tuple[bool, str]:
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
    return encode_bytes(value.encode("utf-8"))


def decode_string(encoded: str) -> str:
    return decode_bytes(encoded).decode("utf-8")


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


def require_arg(arguments: list[str], position: int, label: str) -> str:
    try:
        return arguments[position]
    except IndexError as exc:
        raise ValueError(f"Missing required argument: {label}") from exc


def main(argv: list[str]) -> int:
    command = require_arg(argv, 1, "command")

    if command == "encode-bytes":
        print(encode_bytes(bytes.fromhex(require_arg(argv, 2, "hex"))))
        return 0
    if command == "decode-bytes":
        print(decode_bytes(require_arg(argv, 2, "base32")).hex())
        return 0
    if command == "encode-int":
        print(encode_int(int(require_arg(argv, 2, "value"))))
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

    raise ValueError(f"Unsupported command [{command}].")


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv))
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
PY
}

main "$@"
