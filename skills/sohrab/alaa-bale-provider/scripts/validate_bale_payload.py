#!/usr/bin/env python3
"""Validate Bale Safir payloads and normalise Iranian mobile numbers for the Safir wire.

This helper checks local JSON fixtures before an agent commits docs, tests, or provider
payload examples. It never calls Bale.

Modes:
    --mode request   (default) validate a send_message request body
    --mode response  validate a send_message or upload_file response body
    --normalize RAW  print the Safir wire form of one raw number, or fail with a reason
    --self-test      run the built-in payload vectors and the shared phone corpus

Exit codes:
    0  the input satisfied every rule that was checked
    1  the input was checked and rejected, or --strict was set and a warning fired
    2  usage error: wrong arguments, or arguments that cannot be combined
    3  the payload file does not exist
    4  the payload file is not valid JSON
    5  --self-test found a divergence, so this script is not trustworthy until fixed
    6  the shared phone corpus is missing, unreadable, or fails its own checksum

An exit of 5 or 6 is a defect in this skill, not in the payload under test: stop, fix the
script or the corpus, and do not treat any earlier green run as valid.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

EXIT_OK = 0
EXIT_REJECTED = 1
EXIT_USAGE = 2
EXIT_NO_FILE = 3
EXIT_BAD_JSON = 4
EXIT_SELF_TEST_FAILED = 5
EXIT_CORPUS_FAILED = 6

CORPUS_FILENAME = "phone-conformance-corpus.json"

# Bale Safir wire form: 98 followed by the ten-digit national significant number, no plus sign.
BALE_PHONE_RE = re.compile(r"^989\d{9}$")
# An OTP is ASCII digits only. str.isdigit() is not a substitute: it returns True for
# Persian-Indic, Arabic-Indic and superscript digits, none of which Safir accepts.
OTP_RE = re.compile(r"^[0-9]{4,8}$")

PRIMARY_VARIANTS = ("message", "otp_message", "template_message")
BUTTON_ACTIONS = ("url", "web_app", "copy_text")

ALLOWED_TOP_LEVEL = {"request_id", "bot_id", "phone_number", "message_data"}
ALLOWED_MESSAGE_DATA = {"message", "otp_message", "template_message", "is_secure"}
ALLOWED_MESSAGE = {"text", "file_id", "copy_text", "reply_markup"}
ALLOWED_BUTTON = {"text", "url", "web_app", "copy_text"}

# Field names the skill body forbids by name, each with the reason an agent must be told.
FORBIDDEN_FIELDS = {
    "chat_id": "Telegram field. Safir addresses the recipient with phone_number; send the canonical 989xxxxxxxxx there instead.",
    "parse_mode": "Telegram field. Safir documents no parse mode; send the text already rendered.",
    "callback_data": "Telegram field. Safir documents no callback buttons; use url, web_app, or copy_text on the button.",
    "disable_notification": "Telegram field. Safir documents no notification suppression; remove it.",
}

# Digit folding is by Unicode general category Nd, one code point to one ASCII digit.
# Never enumerate digit families: an enumerated list is a defect class, not a fix, and this
# fold covered two families only until 2026-07-28. Category No is deliberately excluded --
# superscripts are No, not Nd, so a superscript string is still rejected.
# The fold and its canonical implementations are owned by /alaa-input-normalization
# ($alaa-input-normalization); this is a local mirror kept runnable, not a second contract.
DIGIT_FOLD = {
    cp: str(unicodedata.digit(chr(cp)))
    for cp in range(0x110000)
    if unicodedata.category(chr(cp)) == "Nd"
}

# ---- The display-separator rule. The identical block ships in the sibling provider skill. ----
# A character is display formatting, and not a digit of the number, when its Unicode general
# category is one of these five. Scope: this rule governs recipient normalisation for the Bale
# channel and the Mediana channel, and it governs nothing else in this file.
#
#   Cf  format      ZWNJ, ZWJ, the bidi marks, the bidi isolates and overrides, the word joiner, the BOM
#   Zs  space       the no-break space, the figure space, the narrow no-break space, the ideographic space
#   Zl  line        U+2028
#   Zp  paragraph   U+2029
#   Pd  dash        the ASCII hyphen-minus, the en and em dashes, the fullwidth hyphen-minus
#
# Match these five classes by Unicode category, and never by a written-out list of characters,
# because a written-out list is always one character short of the next change in a display
# layer: the earlier list in this file carried the space, the tab, the newline and U+00A0 and
# still rejected U+2028, U+3000, U+000B and every narrow space, which is how the two providers
# came to disagree on four inputs after their first two disagreements had been fixed.
SEPARATOR_CATEGORIES = frozenset({"Cf", "Zs", "Zl", "Zp", "Pd"})

# Match the whitespace control characters with str.isspace(), because their category Cc also
# holds characters that are not separators. str.isspace() covers the tab, the line feed, the
# vertical tab, the form feed, the carriage return, the four information separators and U+0085,
# and it covers nothing else inside Cc.

# Keep these four characters written out, because no Unicode category names them precisely
# enough to be matched by one: Ps and Pe hold every bracket pair in Unicode, and Po holds the
# comma and the semicolon, which separate two numbers rather than group the digits of one.
# The solidus is in this set by a deliberate ruling rather than by inheritance: a person types
# 0912/383/0000 by hand, the ten digits it separates stay unambiguous once it is removed, and
# two numbers written 09123830000/09123830001 are refused by the same length check that already
# refuses them when a space separates them, so removing it costs no safety and spares a
# legitimate caller a rejection they cannot diagnose.
LITERAL_SEPARATORS = frozenset("()._/")

# Keep a comma in the string so that the shape check rejects the input, because a comma means
# the caller passed two numbers in one field and that input must be refused rather than
# silently concatenated into a recipient nobody entered.


def is_display_separator(character: str) -> bool:
    """Report whether one character is display formatting rather than a digit of the number."""
    return (
        unicodedata.category(character) in SEPARATOR_CATEGORIES
        or character.isspace()
        or character in LITERAL_SEPARATORS
    )


def strip_formatting(text: str) -> str:
    """Remove every display separator from a raw number, keeping the digits and any leading plus sign."""
    return "".join(character for character in text if not is_display_separator(character))


CHANNEL_PREFIX = {"bale": "98", "mediana": "+98"}


class PhoneRejected(ValueError):
    """Raised when a raw number cannot be rendered for the requested channel."""


class Reporter:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, path: str, message: str) -> None:
        self.errors.append(f"{path}: {message}")

    def warn(self, path: str, message: str) -> None:
        self.warnings.append(f"{path}: {message}")


def is_non_empty_string(value: Any) -> bool:
    """True only for a string with at least one non-whitespace character.

    A whitespace-only value is not a present value: accepting "   " as a request_id
    produces a payload that validates clean and carries no usable idempotency key.
    """
    return isinstance(value, str) and bool(value.strip())


# --------------------------------------------------------------------------------------
# Phone normalisation -- the single normaliser, shared with alaa-sms-provider-mediana
# --------------------------------------------------------------------------------------


def normalize_iranian_mobile(raw: Any, channel: str = "bale") -> str:
    """Return the wire form of one Iranian mobile number for the named channel.

    channel="bale" returns 989xxxxxxxxx. channel="mediana" returns +989xxxxxxxxx.
    The channel is a required parameter and never a default baked into the caller,
    because a number rendered for the wrong channel is rejected by the vendor at best
    and delivered to the wrong place at worst.

    Raises PhoneRejected, with the reason in the message, for anything else.
    """
    if channel not in CHANNEL_PREFIX:
        raise PhoneRejected(f"unknown channel {channel!r}; expected one of {sorted(CHANNEL_PREFIX)}")
    if not isinstance(raw, str):
        raise PhoneRejected("input must be a string")

    folded = strip_formatting(raw.translate(DIGIT_FOLD))
    if folded == "":
        raise PhoneRejected("input is empty after removing separators and zero-width characters")

    # Remove the international prefix only when the country code 98 follows it, because a
    # plus sign or an access code standing in front of anything else is not an Iranian
    # number in international form: +9123830000 and 009123830000 carry no country code at
    # all, and +09123830000 carries the domestic trunk zero where the country code belongs.
    # Stripping either one unconditionally turns a malformed number into a well-formed one
    # and sends the message to whoever owns the digits that survive.
    if folded.startswith("+98"):
        folded = folded[1:]
    elif folded.startswith("0098"):
        folded = folded[2:]

    if not folded.isascii() or not folded.isdigit():
        raise PhoneRejected("input contains characters that are not digits after normalisation")

    if len(folded) == 12 and folded.startswith("98"):
        national = folded[2:]
    elif len(folded) == 11 and folded.startswith("0"):
        national = folded[1:]
    elif len(folded) == 10:
        national = folded
    else:
        raise PhoneRejected(
            f"{len(folded)} digits after normalisation; expected 10 bare, 11 with a trunk zero, or 12 with country code 98"
        )

    if not re.fullmatch(r"9\d{9}", national):
        raise PhoneRejected("national significant number does not start with 9, so it is not an Iranian mobile number")

    return CHANNEL_PREFIX[channel] + national


# --------------------------------------------------------------------------------------
# Cross-provider guard
# --------------------------------------------------------------------------------------


def reject_mediana_shape(payload: dict[str, Any], reporter: Reporter) -> bool:
    """Reject a Mediana/IPPanel payload that reached the Bale validator.

    Mirrors reject_bale_shape() in alaa-sms-provider-mediana/scripts/validate_mediana_payload.py
    so the guard exists in both directions.
    """
    mediana_fields = [f for f in ("sending_type", "from_number", "recipients", "params", "pattern_code") if f in payload]
    if mediana_fields:
        reporter.error(
            "$",
            "looks like a Mediana/IPPanel payload (fields: "
            + ", ".join(sorted(mediana_fields))
            + "); Bale Safir uses bot_id, phone_number, and message_data",
        )
        return True
    return False


# --------------------------------------------------------------------------------------
# Request validation
# --------------------------------------------------------------------------------------


def reject_unknown_keys(obj: dict[str, Any], allowed: set[str], reporter: Reporter, path: str) -> None:
    for key in sorted(obj):
        if key in allowed:
            continue
        reason = FORBIDDEN_FIELDS.get(key)
        if reason:
            reporter.error(f"{path}.{key}", f"forbidden field. {reason}")
        else:
            reporter.error(
                f"{path}.{key}",
                "unknown field. Safir rejects or silently ignores undocumented fields; remove it, or add it here only "
                "after confirming it against live Safir documentation and recording the read date",
            )


def validate_payload(payload: Any, reporter: Reporter) -> None:
    if not isinstance(payload, dict):
        reporter.error("$", "payload must be a JSON object")
        return

    if reject_mediana_shape(payload, reporter):
        return

    reject_unknown_keys(payload, ALLOWED_TOP_LEVEL, reporter, "$")

    bot_id = payload.get("bot_id")
    if not isinstance(bot_id, int) or isinstance(bot_id, bool):
        reporter.error("$.bot_id", "must be an integer")

    phone_number = payload.get("phone_number")
    if not isinstance(phone_number, str):
        reporter.error("$.phone_number", "must be a string")
    elif not BALE_PHONE_RE.fullmatch(phone_number):
        hint = ""
        try:
            hint = f"; normalise it to {normalize_iranian_mobile(phone_number, 'bale')}"
        except PhoneRejected:
            hint = ""
        reporter.error(
            "$.phone_number",
            "must be the Safir wire form: 98 plus a ten-digit Iranian mobile number, no plus sign, "
            f"e.g. 989123830000{hint}",
        )

    if "request_id" not in payload:
        reporter.error(
            "$.request_id",
            "missing. Every production send carries request_id set to the delivery's durable public id, because a "
            "read timeout on send_message is only retryable when the retry carries the same key",
        )
    elif not is_non_empty_string(payload["request_id"]):
        reporter.error("$.request_id", "must be a non-empty, non-whitespace string")

    message_data = payload.get("message_data")
    if not isinstance(message_data, dict):
        reporter.error("$.message_data", "must be an object")
        return

    reject_unknown_keys(message_data, ALLOWED_MESSAGE_DATA, reporter, "$.message_data")

    present_variants = [name for name in PRIMARY_VARIANTS if name in message_data]
    if len(present_variants) != 1:
        reporter.error(
            "$.message_data",
            "must contain exactly one primary variant: message, otp_message, or template_message",
        )
        return

    is_secure = message_data.get("is_secure")
    if "is_secure" in message_data and not isinstance(is_secure, bool):
        reporter.error("$.message_data.is_secure", "must be boolean when present")

    variant = present_variants[0]
    if variant == "message":
        validate_message(message_data["message"], reporter, "$.message_data.message")
    elif variant == "otp_message":
        if is_secure is True:
            reporter.error(
                "$.message_data.is_secure",
                "secure OTP is not a documented Safir combination. Send otp_message without is_secure, or confirm "
                "secure OTP against live Safir documentation and record the read date before enabling it",
            )
        validate_otp(message_data["otp_message"], reporter, "$.message_data.otp_message")
    elif variant == "template_message":
        validate_template(message_data["template_message"], reporter, "$.message_data.template_message")


def validate_message(message: Any, reporter: Reporter, path: str) -> None:
    if not isinstance(message, dict):
        reporter.error(path, "must be an object")
        return

    reject_unknown_keys(message, ALLOWED_MESSAGE, reporter, path)

    content_fields = [field for field in ("text", "file_id", "copy_text") if field in message]
    if not content_fields:
        reporter.warn(path, "has no text, file_id, or copy_text; confirm it creates a visible message")

    for field in ("text", "file_id", "copy_text"):
        if field in message and not isinstance(message[field], str):
            reporter.error(f"{path}.{field}", "must be a string")

    if "reply_markup" in message:
        validate_reply_markup(message["reply_markup"], reporter, f"{path}.reply_markup")


def validate_reply_markup(markup: Any, reporter: Reporter, path: str) -> None:
    if not isinstance(markup, dict):
        reporter.error(path, "must be an object")
        return

    keyboard = markup.get("inline_keyboard")
    if not isinstance(keyboard, list) or not keyboard:
        reporter.error(f"{path}.inline_keyboard", "must be a non-empty array of button rows")
        return

    for row_index, row in enumerate(keyboard):
        row_path = f"{path}.inline_keyboard[{row_index}]"
        if not isinstance(row, list) or not row:
            reporter.error(row_path, "must be a non-empty array of buttons")
            continue
        for button_index, button in enumerate(row):
            validate_button(button, reporter, f"{row_path}[{button_index}]")


def validate_button(button: Any, reporter: Reporter, path: str) -> None:
    if not isinstance(button, dict):
        reporter.error(path, "must be an object")
        return

    reject_unknown_keys(button, ALLOWED_BUTTON, reporter, path)

    if not is_non_empty_string(button.get("text")):
        reporter.error(f"{path}.text", "must be a non-empty string")

    actions = [name for name in BUTTON_ACTIONS if name in button]
    if not actions:
        reporter.error(path, "must include at least one action: url, web_app, or copy_text")
    elif len(actions) > 1:
        reporter.warn(path, "has multiple button actions; send exactly one action per button")

    if "url" in button and not is_non_empty_string(button["url"]):
        reporter.error(f"{path}.url", "must be a non-empty string")

    if "copy_text" in button and not isinstance(button["copy_text"], str):
        reporter.error(f"{path}.copy_text", "must be a string")

    if "web_app" in button:
        web_app = button["web_app"]
        if not isinstance(web_app, dict):
            reporter.error(f"{path}.web_app", "must be an object")
        elif not is_non_empty_string(web_app.get("url")):
            reporter.error(f"{path}.web_app.url", "must be a non-empty string")


def validate_otp(otp_message: Any, reporter: Reporter, path: str) -> None:
    if not isinstance(otp_message, dict):
        reporter.error(path, "must be an object")
        return

    unknown = sorted(set(otp_message) - {"otp"})
    for key in unknown:
        reporter.error(f"{path}.{key}", "unknown field; OTPMessage carries only otp")

    otp = otp_message.get("otp")
    if not is_non_empty_string(otp):
        reporter.error(f"{path}.otp", "must be a non-empty string")
    elif not OTP_RE.fullmatch(otp):
        reporter.error(
            f"{path}.otp",
            "must be 4 to 8 ASCII digits. Persian-Indic, Arabic-Indic and superscript digits are not ASCII digits "
            "and Safir does not accept them; fold them to ASCII before building the payload",
        )


def validate_template(template_message: Any, reporter: Reporter, path: str) -> None:
    if not isinstance(template_message, dict):
        reporter.error(path, "must be an object")
        return

    unknown = sorted(set(template_message) - {"template_id", "text_fields"})
    for key in unknown:
        reporter.error(f"{path}.{key}", "unknown field; TemplateMessage carries only template_id and text_fields")

    if not is_non_empty_string(template_message.get("template_id")):
        reporter.error(f"{path}.template_id", "must be a non-empty string")

    text_fields = template_message.get("text_fields")
    if not isinstance(text_fields, dict) or not text_fields:
        reporter.error(f"{path}.text_fields", "must be a non-empty object")
        return

    for key, value in text_fields.items():
        if not is_non_empty_string(key):
            reporter.error(f"{path}.text_fields", "all keys must be non-empty strings")
        if not isinstance(value, str):
            reporter.error(f"{path}.text_fields.{key}", "all values must be strings")


# --------------------------------------------------------------------------------------
# Response validation
# --------------------------------------------------------------------------------------


def validate_response(payload: Any, reporter: Reporter) -> None:
    """Validate a send_message or upload_file response body."""
    if not isinstance(payload, dict):
        reporter.error("$", "response must be a JSON object")
        return

    if "file_id" in payload or ("error" in payload and "message_id" not in payload):
        validate_upload_response(payload, reporter)
        return

    message_id = payload.get("message_id")
    error_data = payload.get("error_data")

    if "message_id" not in payload and "error_data" not in payload:
        reporter.error("$", "response carries neither message_id nor error_data; it cannot be classified")
        return

    if "message_id" in payload and not is_non_empty_string(message_id):
        reporter.error("$.message_id", "must be a non-empty string when present")

    if error_data is None:
        return

    if not isinstance(error_data, list):
        reporter.error("$.error_data", "must be null or an array of ErrorInfo objects")
        return

    if error_data and is_non_empty_string(message_id):
        reporter.warn(
            "$",
            "message_id and a non-empty error_data are both present: this is a partial result. Record per-recipient "
            "outcomes from error_data and never mark the whole send successful on message_id alone",
        )

    for index, item in enumerate(error_data):
        validate_error_info(item, reporter, f"$.error_data[{index}]")


def validate_upload_response(payload: dict[str, Any], reporter: Reporter) -> None:
    if "file_id" in payload:
        if not is_non_empty_string(payload["file_id"]):
            reporter.error("$.file_id", "must be a non-empty string")
        return
    error = payload.get("error")
    if not isinstance(error, dict):
        reporter.error("$.error", "must be an object when file_id is absent")
        return
    validate_error_info(error, reporter, "$.error")


def validate_error_info(item: Any, reporter: Reporter, path: str) -> None:
    if not isinstance(item, dict):
        reporter.error(path, "must be an object")
        return
    code = item.get("code")
    if not isinstance(code, int) or isinstance(code, bool):
        reporter.error(f"{path}.code", "must be an integer Safir error code")
    if "phone_number" in item and not isinstance(item["phone_number"], str):
        reporter.error(f"{path}.phone_number", "must be a string when present")
    if "description" in item and not isinstance(item["description"], str):
        reporter.error(f"{path}.description", "must be a string when present")


# --------------------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------------------

# Each vector is (name, mode, payload, expected_error_substrings).
# An empty expectation list means the payload must validate with no errors.
SELF_TEST_VECTORS: list[tuple[str, str, Any, list[str]]] = [
    (
        "valid text message",
        "request",
        {
            "request_id": "01936c7e-1f2a-7b3c-8d4e-5f6a7b8c9d0e",
            "bot_id": 1,
            "phone_number": "989123830000",
            "message_data": {"message": {"text": "hello"}},
        },
        [],
    ),
    (
        "valid otp message",
        "request",
        {
            "request_id": "01936c7e-1f2a-7b3c-8d4e-5f6a7b8c9d0e",
            "bot_id": 1,
            "phone_number": "989123830000",
            "message_data": {"otp_message": {"otp": "123456"}},
        },
        [],
    ),
    (
        "valid template message",
        "request",
        {
            "request_id": "01936c7e-1f2a-7b3c-8d4e-5f6a7b8c9d0e",
            "bot_id": 1,
            "phone_number": "989123830000",
            "message_data": {"template_message": {"template_id": "t1", "text_fields": {"user": "a"}}},
        },
        [],
    ),
    (
        "valid inline url button",
        "request",
        {
            "request_id": "01936c7e-1f2a-7b3c-8d4e-5f6a7b8c9d0e",
            "bot_id": 1,
            "phone_number": "989123830000",
            "message_data": {
                "message": {
                    "text": "see this",
                    "reply_markup": {"inline_keyboard": [[{"text": "open", "url": "https://example.invalid"}]]},
                }
            },
        },
        [],
    ),
    # Defect 1: str.isdigit() accepted non-ASCII digits.
    (
        "defect-1 persian-indic otp is rejected",
        "request",
        {
            "request_id": "r",
            "bot_id": 1,
            "phone_number": "989123830000",
            "message_data": {"otp_message": {"otp": "۱۲۳۴۵۶"}},
        },
        ["otp: must be 4 to 8 ASCII digits"],
    ),
    (
        "defect-1 arabic-indic otp is rejected",
        "request",
        {
            "request_id": "r",
            "bot_id": 1,
            "phone_number": "989123830000",
            "message_data": {"otp_message": {"otp": "١٢٣٤٥٦"}},
        },
        ["otp: must be 4 to 8 ASCII digits"],
    ),
    (
        "defect-1 superscript otp is rejected",
        "request",
        {
            "request_id": "r",
            "bot_id": 1,
            "phone_number": "989123830000",
            "message_data": {"otp_message": {"otp": "²³⁴"}},
        },
        ["otp: must be 4 to 8 ASCII digits"],
    ),
    # Defect 2: no unknown-key rejection.
    (
        "defect-2 forbidden telegram fields are each named",
        "request",
        {
            "request_id": "r",
            "bot_id": 1,
            "phone_number": "989123830000",
            "chat_id": 99,
            "parse_mode": "MarkdownV2",
            "callback_data": "x",
            "disable_notification": True,
            "message_data": {"message": {"text": "hi"}},
        },
        [
            "$.chat_id: forbidden field",
            "$.parse_mode: forbidden field",
            "$.callback_data: forbidden field",
            "$.disable_notification: forbidden field",
        ],
    ),
    (
        "defect-2 callback_data inside message is rejected",
        "request",
        {
            "request_id": "r",
            "bot_id": 1,
            "phone_number": "989123830000",
            "message_data": {"message": {"text": "hi", "callback_data": "x"}},
        },
        ["$.message_data.message.callback_data: forbidden field"],
    ),
    (
        "defect-2 callback_data on a button is rejected",
        "request",
        {
            "request_id": "r",
            "bot_id": 1,
            "phone_number": "989123830000",
            "message_data": {
                "message": {
                    "text": "hi",
                    "reply_markup": {
                        "inline_keyboard": [[{"text": "go", "url": "https://example.invalid", "callback_data": "x"}]]
                    },
                }
            },
        },
        ["callback_data: forbidden field"],
    ),
    (
        "defect-2 unrecognised top-level key is rejected",
        "request",
        {
            "request_id": "r",
            "bot_id": 1,
            "phone_number": "989123830000",
            "invented_field": 1,
            "message_data": {"message": {"text": "hi"}},
        },
        ["$.invented_field: unknown field"],
    ),
    # Defect 3: whitespace-only strings validated clean.
    (
        "defect-3 whitespace-only request_id is rejected",
        "request",
        {
            "request_id": "   ",
            "bot_id": 1,
            "phone_number": "989123830000",
            "message_data": {"message": {"text": "hi"}},
        },
        ["$.request_id: must be a non-empty, non-whitespace string"],
    ),
    # request_id promoted from warning to error.
    (
        "missing request_id is an error",
        "request",
        {"bot_id": 1, "phone_number": "989123830000", "message_data": {"message": {"text": "hi"}}},
        ["$.request_id: missing"],
    ),
    (
        "non-canonical phone is rejected and the canonical form is offered",
        "request",
        {"request_id": "r", "bot_id": 1, "phone_number": "09123830000", "message_data": {"message": {"text": "hi"}}},
        ["normalise it to 989123830000"],
    ),
    (
        "two primary variants are rejected",
        "request",
        {
            "request_id": "r",
            "bot_id": 1,
            "phone_number": "989123830000",
            "message_data": {"message": {"text": "hi"}, "otp_message": {"otp": "123456"}},
        },
        ["must contain exactly one primary variant"],
    ),
    (
        "secure otp is rejected",
        "request",
        {
            "request_id": "r",
            "bot_id": 1,
            "phone_number": "989123830000",
            "message_data": {"is_secure": True, "otp_message": {"otp": "123456"}},
        },
        ["secure OTP is not a documented Safir combination"],
    ),
    (
        "mediana payload is rejected by the cross-provider guard",
        "request",
        {"sending_type": "pattern", "from_number": "+983000505", "recipients": ["+989123830000"]},
        ["looks like a Mediana/IPPanel payload"],
    ),
    (
        "valid send_message response",
        "response",
        {"message_id": "523e6875-7c41-491b-8460-04b33039d7fc", "error_data": None},
        [],
    ),
    (
        "valid otp response without error_data",
        "response",
        {"message_id": "BvQjaR.fIKt7kH.EXTddgYduJ2"},
        [],
    ),
    (
        "valid upload_file response",
        "response",
        {"file_id": "987141dd2672149"},
        [],
    ),
    (
        "error_data entries are checked",
        "response",
        {"message_id": None, "error_data": [{"phone_number": "989123830000", "code": "17", "description": "x"}]},
        ["$.error_data[0].code: must be an integer"],
    ),
]


def run_self_test(script_dir: Path) -> int:
    failures: list[str] = []

    corpus_path = script_dir / CORPUS_FILENAME
    try:
        corpus_doc = json.loads(corpus_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"[FAIL] shared corpus not found: {corpus_path}", file=sys.stderr)
        return EXIT_CORPUS_FAILED
    except json.JSONDecodeError as exc:
        print(f"[FAIL] shared corpus is not valid JSON: {exc}", file=sys.stderr)
        return EXIT_CORPUS_FAILED

    cases = corpus_doc.get("cases")
    if not isinstance(cases, list) or not cases:
        print("[FAIL] shared corpus has no cases array", file=sys.stderr)
        return EXIT_CORPUS_FAILED

    # The corpus canonicalization field is the contract: the digest covers the parsed
    # cases re-serialised with ensure_ascii=False, so it describes the data and not the
    # \uXXXX escaping the file happens to be stored in. Keep this identical to
    # load_corpus() in alaa-sms-provider-mediana/scripts/validate_mediana_payload.py.
    canonical = json.dumps(cases, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    if digest != corpus_doc.get("corpus_sha256"):
        print(
            "[FAIL] corpus checksum mismatch\n"
            f"        recorded:   {corpus_doc.get('corpus_sha256')}\n"
            f"        recomputed: {digest}\n"
            "        The corpus was edited without updating corpus_sha256, or it has diverged from the copy in "
            "alaa-sms-provider-mediana/scripts/. Reconcile both copies before trusting either validator.",
            file=sys.stderr,
        )
        return EXIT_CORPUS_FAILED

    for index, case in enumerate(cases):
        raw = case["input"]
        for channel, key in (("bale", "bale_expected"), ("mediana", "mediana_expected")):
            expected = case[key]
            try:
                actual: Any = normalize_iranian_mobile(raw, channel)
            except PhoneRejected as exc:
                actual = None
                reason = str(exc)
            else:
                reason = ""
            if actual != expected:
                failures.append(
                    f"corpus[{index}] channel={channel} input={raw!r}: expected {expected!r}, got {actual!r}"
                    + (f" (reason: {reason})" if actual is None else "")
                )

    for name, mode, payload, expected_substrings in SELF_TEST_VECTORS:
        reporter = Reporter()
        if mode == "request":
            validate_payload(payload, reporter)
        else:
            validate_response(payload, reporter)
        joined = "\n".join(reporter.errors)
        if not expected_substrings:
            if reporter.errors:
                failures.append(f"vector {name!r}: expected no errors, got:\n{joined}")
            continue
        for needle in expected_substrings:
            if needle not in joined:
                failures.append(f"vector {name!r}: expected an error containing {needle!r}, got:\n{joined or '(none)'}")

    if failures:
        for failure in failures:
            print(f"[FAIL] {failure}", file=sys.stderr)
        print(f"\n[FAIL] {len(failures)} self-test failure(s)", file=sys.stderr)
        return EXIT_SELF_TEST_FAILED

    print(
        f"[OK] self-test passed: {len(cases)} corpus cases x 2 channels, {len(SELF_TEST_VECTORS)} payload vectors, "
        f"corpus_sha256 {digest[:16]}..."
    )
    return EXIT_OK


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate a Bale Safir payload, or normalise one Iranian mobile number for the Safir wire.",
        epilog="Exit codes: 0 ok, 1 rejected, 2 usage, 3 no file, 4 bad JSON, 5 self-test failed, 6 corpus failed.",
    )
    parser.add_argument("payload", nargs="?", type=Path, help="path to a JSON payload file")
    parser.add_argument("--mode", choices=("request", "response"), default="request", help="what the file contains")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    parser.add_argument("--normalize", metavar="RAW", help="print the wire form of one raw number and exit")
    parser.add_argument(
        "--channel",
        choices=sorted(CHANNEL_PREFIX),
        default="bale",
        help="target channel for --normalize (default: bale)",
    )
    parser.add_argument("--self-test", action="store_true", help="run built-in vectors and the shared phone corpus")
    args = parser.parse_args(argv)

    script_dir = Path(__file__).resolve().parent

    selected = sum(1 for flag in (args.self_test, args.normalize is not None, args.payload is not None) if flag)
    if selected != 1:
        parser.print_usage(sys.stderr)
        print(
            "error: pass exactly one of a payload path, --normalize RAW, or --self-test",
            file=sys.stderr,
        )
        return EXIT_USAGE

    if args.self_test:
        return run_self_test(script_dir)

    if args.normalize is not None:
        try:
            print(normalize_iranian_mobile(args.normalize, args.channel))
        except PhoneRejected as exc:
            print(f"[ERROR] rejected for channel {args.channel}: {exc}", file=sys.stderr)
            return EXIT_REJECTED
        return EXIT_OK

    try:
        payload = json.loads(args.payload.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"[ERROR] file not found: {args.payload}", file=sys.stderr)
        return EXIT_NO_FILE
    except json.JSONDecodeError as exc:
        print(f"[ERROR] invalid JSON: {exc}", file=sys.stderr)
        return EXIT_BAD_JSON

    reporter = Reporter()
    if args.mode == "request":
        validate_payload(payload, reporter)
    else:
        validate_response(payload, reporter)

    for warning in reporter.warnings:
        print(f"[WARN] {warning}")
    for error in reporter.errors:
        print(f"[ERROR] {error}")

    if reporter.errors or (args.strict and reporter.warnings):
        return EXIT_REJECTED

    print(f"[OK] Bale Safir {args.mode} is valid")
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
