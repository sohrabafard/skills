#!/usr/bin/env python3
"""Validate a Mediana/IPPanel Edge payload, or normalise an Iranian mobile number.

This helper never calls Mediana/IPPanel. It checks payload shape and it renders
recipient strings. It cannot check an account-approved sender, a pattern code, a
phonebook id, or a geographic id, because none of those exist outside the panel.

Exit codes, and what each obliges the caller to do:

  0  The requested check passed. Continue.
  1  The payload is invalid, --normalize rejected its input, or --self-test found
     a disagreement. Fix the payload or the normaliser and rerun; do not send.
  2  The invocation is wrong. Fix the arguments.
  3  The payload file is unreadable or is not JSON. Fix the path or the contents.
  4  scripts/phone-conformance-corpus.json is missing, unreadable, or its
     corpus_sha256 does not match its cases. Reconcile with the alaa-bale-provider
     copy of the same file; never edit one copy alone.
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
EXIT_INVALID = 1
EXIT_USAGE = 2
EXIT_INPUT = 3
EXIT_CORPUS = 4

CORPUS_FILENAME = "phone-conformance-corpus.json"

# --------------------------------------------------------------------------
# Phone normalisation - the single canonical implementation for both channels.
# --------------------------------------------------------------------------

CHANNEL_PREFIX = {"mediana": "+98", "bale": "98"}

# Digit folding is by Unicode general category Nd, one code point to one ASCII digit.
# Never enumerate digit families: an enumerated list is a defect class, not a fix, and this
# fold covered two families only until 2026-07-28. Category No is deliberately excluded --
# superscripts are No, not Nd, so a superscript string is still rejected.
# The fold and its canonical implementations are owned by /alaa-input-normalization
# ($alaa-input-normalization); this is a local mirror kept runnable, not a second contract.
def _fold_digit(char: str) -> str:
    if unicodedata.category(char) == "Nd":
        return str(unicodedata.digit(char))
    return char

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


MSISDN_RE = re.compile(r"^(?:\+98|0098|98|0|)(9\d{9})$")


class NormalizationError(ValueError):
    """Raised when a raw value cannot be rendered as an Iranian mobile number."""

    def __init__(self, reason: str, detail: str) -> None:
        super().__init__(f"{reason}: {detail}")
        self.reason = reason
        self.detail = detail


def fold_and_strip(raw: str) -> str:
    """Fold Persian and Arabic-Indic digits to ASCII and drop every display separator.

    Only those two digit families are folded. Any other Unicode digit family, and
    every superscript digit, survives cleanup and is rejected by the shape check,
    because a normaliser that accepts every Unicode digit accepts input no Iranian
    subscriber types and no vendor renders.
    """
    out = []
    for char in raw:
        folded = _fold_digit(char)
        if is_display_separator(folded):
            continue
        out.append(folded)
    return "".join(out)


def normalize_msisdn(raw: Any, channel: str = "mediana") -> str:
    """Render one Iranian mobile number in one channel's wire form.

    The channel is a required part of the contract, not a formatting detail:
    Mediana's wire form is +989xxxxxxxxx and Bale's is 989xxxxxxxxx. A normaliser
    that does not take the channel renders one channel's number for the other, and
    an OTP rendered for the wrong channel is rejected by the vendor at best and
    delivered to the wrong subscriber at worst.
    """
    if channel not in CHANNEL_PREFIX:
        raise NormalizationError("unknown_channel", f"expected one of {sorted(CHANNEL_PREFIX)}")
    if not isinstance(raw, str):
        raise NormalizationError("not_a_string", f"got {type(raw).__name__}")

    cleaned = fold_and_strip(raw)
    if not cleaned:
        raise NormalizationError("empty_after_cleanup", "nothing remained once display characters were removed")

    unexpected = sorted({ch for ch in cleaned if not (ch.isdigit() and ch in "0123456789") and ch != "+"})
    if unexpected:
        names = ", ".join(f"U+{ord(ch):04X}" for ch in unexpected)
        raise NormalizationError("unexpected_characters", f"non-digit characters remain: {names}")

    match = MSISDN_RE.fullmatch(cleaned)
    if match is None:
        raise NormalizationError("not_iranian_mobile", "expected an Iranian mobile number, 9xxxxxxxxx after the country code")

    return CHANNEL_PREFIX[channel] + match.group(1)


# --------------------------------------------------------------------------
# Payload validation
# --------------------------------------------------------------------------

SENDER_RE = re.compile(r"^\+98[A-Za-z0-9]+$")
SEND_TIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")

JSON_SEND_TYPES = {
    "webservice",
    "normal",
    "peer_to_peer",
    "pattern",
    "votp",
    "postal_code",
    "country",
    "geolocation",
    "job",
    "keyword_phonebook",
    "phonebook",
}
MULTIPART_SEND_TYPES = {"file", "keyword", "peer_to_peer_file"}
ALL_SEND_TYPES = JSON_SEND_TYPES | MULTIPART_SEND_TYPES

# Modes that resolve their audience from vendor data or an uploaded file. Every
# one of them needs the approval gate in references/15-targeting-and-bulk-sends.md
# before a live send, so the warning is emitted from exactly one place.
BULK_TARGETING_TYPES = {
    "postal_code",
    "country",
    "geolocation",
    "job",
    "keyword_phonebook",
    "phonebook",
    "file",
    "keyword",
    "peer_to_peer_file",
}

ALLOWED_TOP_LEVEL = {
    "webservice": {"sending_type", "from_number", "message", "params", "send_time"},
    "normal": {"sending_type", "from_number", "message", "params", "send_time"},
    "pattern": {"sending_type", "from_number", "code", "recipients", "params", "phonebook"},
    "votp": {"sending_type", "message", "params", "from_number"},
    "peer_to_peer": {"sending_type", "from_number", "params", "send_time"},
    "file": {"sending_type", "from_number", "message", "files", "files[]", "other_recipients", "other_recipients[]", "send_time"},
    "keyword": {"sending_type", "from_number", "message", "files", "files[]", "send_time"},
    "peer_to_peer_file": {"sending_type", "from_number", "files", "files[]", "send_time"},
    "keyword_phonebook": {"sending_type", "from_number", "message", "params", "send_time"},
    "phonebook": {"sending_type", "from_number", "message", "params", "send_time"},
    "postal_code": {"sending_type", "from_number", "message", "params", "other_recipients", "send_time"},
    "country": {"sending_type", "from_number", "message", "params", "other_recipients", "send_time"},
    "geolocation": {"sending_type", "from_number", "message", "params", "other_recipients", "send_time"},
    "job": {"sending_type", "from_number", "message", "params", "send_time"},
}

# The sibling skill ships reject_mediana_shape(); the guard exists in both
# directions so a payload built for the wrong provider is caught by whichever
# validator the agent happens to run.
BALE_FIELDS = (
    "bot_id",
    "phone_number",
    "message_data",
    "otp_message",
    "template_message",
    "request_id",
    "api-access-key",
    "chat_id",
    "parse_mode",
    "callback_data",
    "disable_notification",
)

WINDOW_KEYS = {"start", "size"}

BULK_PARAM_RULES = {
    "postal_code": {
        "allowed": {"bank", "postal_code", "gender", "age_from", "age_to", "mci", "irancell", "other"},
        "required": ("postal_code",),
        "windows": ("mci", "irancell", "other"),
        "operator_array": False,
    },
    "country": {
        "allowed": {"bank", "pre", "province_id", "county_id", "city_id", "gender", "age_from", "age_to", "mci", "irancell", "other"},
        "required_any": ("province_id", "county_id", "city_id"),
        "windows": ("mci", "irancell", "other"),
        "operator_array": False,
    },
    "geolocation": {
        "allowed": {"province_id", "county_id", "city_id", "pre", "gender", "from_age", "to_age", "operator"},
        "required": ("operator",),
        "windows": (),
        "operator_array": True,
    },
    "job": {
        "allowed": {"main_category_id", "sub_category_id", "operator"},
        "required": ("main_category_id", "sub_category_id", "operator"),
        "windows": (),
        "operator_array": True,
    },
}

CROSS_MODE_HINTS = {
    ("country", "from_age"): "country uses age_from and age_to; from_age and to_age belong to geolocation",
    ("country", "to_age"): "country uses age_from and age_to; from_age and to_age belong to geolocation",
    ("country", "operator"): "country uses the mci, irancell and other window objects; the operator array belongs to geolocation and job",
    ("geolocation", "age_from"): "geolocation uses from_age and to_age",
    ("geolocation", "age_to"): "geolocation uses from_age and to_age",
    ("geolocation", "mci"): "geolocation uses the operator array, not per-operator window objects",
    ("geolocation", "irancell"): "geolocation uses the operator array, not per-operator window objects",
    ("geolocation", "other"): "geolocation uses the operator array, not per-operator window objects",
}


class Reporter:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, path: str, message: str) -> None:
        self.errors.append(f"{path}: {message}")

    def warn(self, path: str, message: str) -> None:
        self.warnings.append(f"{path}: {message}")


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def reject_bale_shape(payload: dict[str, Any], reporter: Reporter) -> None:
    found = [field for field in BALE_FIELDS if field in payload]
    if found:
        reporter.error(
            "$",
            "carries Bale Safir fields (" + ", ".join(found) + "); Mediana uses sending_type, from_number, message, params or recipients, with an Authorization header",
        )


def reject_unknown_top_level(payload: dict[str, Any], reporter: Reporter, sending_type: str) -> None:
    allowed = ALLOWED_TOP_LEVEL.get(sending_type)
    if allowed is None:
        return
    for key in sorted(set(payload) - allowed):
        if key in BALE_FIELDS:
            continue
        reporter.error(f"$.{key}", f"is not a field of a {sending_type} send; allowed fields are " + ", ".join(sorted(allowed)))


def validate_sender(payload: dict[str, Any], reporter: Reporter, *, required: bool = True) -> None:
    sender = payload.get("from_number")
    if not is_non_empty_string(sender):
        if required:
            reporter.error("$.from_number", "must be a non-empty configured sender string")
        return
    if not SENDER_RE.fullmatch(sender):
        reporter.warn(
            "$.from_number",
            "does not look like a +98 sender line or label; keep it only if this exact sender is approved on the account",
        )


def validate_send_time(payload: dict[str, Any], reporter: Reporter) -> None:
    if "send_time" not in payload:
        return
    send_time = payload["send_time"]
    if not is_non_empty_string(send_time) or not SEND_TIME_RE.fullmatch(send_time):
        reporter.error("$.send_time", "must be UTC in YYYY-MM-DD HH:MM:SS format")


def validate_recipients(value: Any, reporter: Reporter, path: str, *, exactly_one: bool = False) -> None:
    if not isinstance(value, list) or not value:
        reporter.error(path, "must be a non-empty array of recipient strings")
        return
    if exactly_one and len(value) != 1:
        reporter.error(path, "must contain exactly one recipient for this endpoint")
    for index, recipient in enumerate(value):
        item_path = f"{path}[{index}]"
        if not isinstance(recipient, str):
            reporter.error(item_path, "must be a string")
            continue
        try:
            canonical = normalize_msisdn(recipient, "mediana")
        except NormalizationError as exc:
            reporter.error(item_path, f"is not a usable Iranian mobile number ({exc.reason}); run --normalize on the source value")
            continue
        if canonical != recipient:
            reporter.error(item_path, "must already be normalised; --normalize renders this value differently")


def validate_params_object(value: Any, reporter: Reporter, path: str) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        reporter.error(path, "must be an object")
        return None
    return value


def validate_params_array(value: Any, reporter: Reporter, path: str) -> list[Any] | None:
    if not isinstance(value, list) or not value:
        reporter.error(path, "must be a non-empty array")
        return None
    return value


def validate_files_field(payload: dict[str, Any], reporter: Reporter) -> None:
    value = payload.get("files[]", payload.get("files"))
    if value is None:
        reporter.error("$.files[]", "multipart variants require files[]")
        return
    values = value if isinstance(value, list) else [value]
    if not values:
        reporter.error("$.files[]", "must include at least one file reference")
    for index, item in enumerate(values):
        if not is_non_empty_string(item):
            reporter.error(f"$.files[][{index}]", "must be a non-empty file path or reference string")


def validate_webservice_or_normal(payload: dict[str, Any], reporter: Reporter, sending_type: str) -> None:
    if sending_type == "normal":
        reporter.warn("$.sending_type", "normal is legacy; send webservice unless a committed fixture in this repository already sends normal")
    validate_sender(payload, reporter)
    if not is_non_empty_string(payload.get("message")):
        reporter.error("$.message", "must be a non-empty SMS text string")
    params = validate_params_object(payload.get("params"), reporter, "$.params")
    if params is not None:
        validate_recipients(params.get("recipients"), reporter, "$.params.recipients")
    if "recipients" in payload:
        reporter.error("$.recipients", "webservice recipients belong under $.params.recipients; the top-level key belongs to pattern")


def validate_peer_to_peer(payload: dict[str, Any], reporter: Reporter) -> None:
    validate_sender(payload, reporter)
    params = validate_params_array(payload.get("params"), reporter, "$.params")
    if params is None:
        return
    for index, item in enumerate(params):
        path = f"$.params[{index}]"
        if not isinstance(item, dict):
            reporter.error(path, "must be an object")
            continue
        if not is_non_empty_string(item.get("message")):
            reporter.error(f"{path}.message", "must be a non-empty message string")
        validate_recipients(item.get("recipients"), reporter, f"{path}.recipients")


def validate_pattern(payload: dict[str, Any], reporter: Reporter) -> None:
    validate_sender(payload, reporter)
    if not is_non_empty_string(payload.get("code")):
        reporter.error("$.code", "must be a non-empty provider pattern code string")
    validate_recipients(payload.get("recipients"), reporter, "$.recipients", exactly_one=True)
    params = validate_params_object(payload.get("params"), reporter, "$.params")
    if params is not None:
        if "recipients" in params:
            reporter.error("$.params.recipients", "pattern recipients belong at top level; $.params holds pattern variables only")
        variables = [(key, value) for key, value in params.items() if key != "recipients"]
        if not variables:
            reporter.error("$.params", "must contain at least one pattern variable")
        for key, value in variables:
            if not is_non_empty_string(key):
                reporter.error("$.params", "every pattern variable key must be a non-empty string")
            if not isinstance(value, str):
                reporter.error(
                    f"$.params.{key}",
                    "must be a string; Mediana substitutes params values as text, so a number drops a leading zero",
                )
    if "phonebook" in payload:
        phonebook = payload["phonebook"]
        if not isinstance(phonebook, dict):
            reporter.error("$.phonebook", "must be an object when provided")
        elif "id" not in phonebook:
            reporter.error("$.phonebook.id", "is required when phonebook is provided")


def validate_votp(payload: dict[str, Any], reporter: Reporter) -> None:
    if "from_number" in payload:
        reporter.warn("$.from_number", "the documented votp body and the vendor sample both omit from_number; send it only when a committed fixture shows it")
    code = payload.get("message")
    if not is_non_empty_string(code):
        reporter.error("$.message", "must be a non-empty OTP code string")
    elif not re.fullmatch(r"[0-9]{4,8}", code):
        reporter.error("$.message", "must be 4 to 8 ASCII digits; str.isdigit() also accepts Persian, Arabic-Indic and superscript digits, which no dialler speaks")
    params = validate_params_object(payload.get("params"), reporter, "$.params")
    if params is not None:
        validate_recipients(params.get("recipients"), reporter, "$.params.recipients", exactly_one=True)
    if "recipients" in payload:
        reporter.error("$.recipients", "votp recipients belong under $.params.recipients")


def validate_multipart_metadata(payload: dict[str, Any], reporter: Reporter, sending_type: str) -> None:
    reporter.warn("$", f"{sending_type} is multipart/form-data on the wire; this checks the JSON-equivalent metadata only")
    validate_sender(payload, reporter)
    validate_files_field(payload, reporter)
    if sending_type in {"file", "keyword"} and not is_non_empty_string(payload.get("message")):
        reporter.error("$.message", "must be a non-empty message string")
    others = payload.get("other_recipients[]", payload.get("other_recipients"))
    if others is not None:
        validate_recipients(others, reporter, "$.other_recipients")


def validate_keyword_phonebook(payload: dict[str, Any], reporter: Reporter) -> None:
    validate_sender(payload, reporter)
    if not is_non_empty_string(payload.get("message")):
        reporter.error("$.message", "must be a non-empty message string")
    params = validate_params_array(payload.get("params"), reporter, "$.params")
    if params is None:
        return
    for index, item in enumerate(params):
        if not isinstance(item, dict):
            reporter.error(f"$.params[{index}]", "must be an object")
        elif "phonebook_id" not in item:
            reporter.error(f"$.params[{index}].phonebook_id", "is required")


def validate_phonebook(payload: dict[str, Any], reporter: Reporter) -> None:
    validate_sender(payload, reporter)
    if not is_non_empty_string(payload.get("message")):
        reporter.error("$.message", "must be a non-empty message string")
    params = validate_params_array(payload.get("params"), reporter, "$.params")
    if params is None:
        return
    for index, item in enumerate(params):
        path = f"$.params[{index}]"
        if not isinstance(item, dict):
            reporter.error(path, "must be an object")
            continue
        item_type = item.get("type")
        if item_type not in {"all", "detail"}:
            reporter.error(f"{path}.type", "must be all or detail")
            continue
        if item_type == "all":
            if "phonebook_ids" not in item:
                reporter.error(f"{path}.phonebook_ids", "is required when type is all")
            if "phonebook_id" in item:
                reporter.error(f"{path}.phonebook_id", "belongs to type detail; with type all it widens the selection silently")
        else:
            if "phonebook_id" not in item:
                reporter.error(f"{path}.phonebook_id", "is required when type is detail")
            if "number_ids" not in item:
                reporter.error(f"{path}.number_ids", "is required when type is detail")
            if "phonebook_ids" in item:
                reporter.error(f"{path}.phonebook_ids", "belongs to type all; with type detail it widens the selection silently")


def validate_window(value: Any, reporter: Reporter, path: str) -> None:
    if not isinstance(value, dict):
        reporter.error(path, "must be an object with start and size")
        return
    for key in sorted(set(value) - WINDOW_KEYS):
        reporter.error(f"{path}.{key}", "is not part of an operator window; only start and size are")
    for key in ("start", "size"):
        if key not in value:
            reporter.error(f"{path}.{key}", "is required; set size to 0 to exclude this operator rather than omitting the object")
        elif not isinstance(value[key], int) or isinstance(value[key], bool) or value[key] < 0:
            reporter.error(f"{path}.{key}", "must be a non-negative integer")


def validate_operator_array(value: Any, reporter: Reporter, path: str) -> None:
    if not isinstance(value, list) or not value:
        reporter.error(path, "must be a non-empty array of {start, size, id} objects")
        return
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not isinstance(item, dict):
            reporter.error(item_path, "must be an object")
            continue
        for key in sorted(set(item) - {"start", "size", "id"}):
            reporter.error(f"{item_path}.{key}", "is not part of an operator range; only start, size and id are")
        for key in ("start", "size", "id"):
            if key not in item:
                reporter.error(f"{item_path}.{key}", "is required")
            elif not isinstance(item[key], int) or isinstance(item[key], bool) or item[key] < 0:
                reporter.error(f"{item_path}.{key}", "must be a non-negative integer")


def validate_bulk_targeting(payload: dict[str, Any], reporter: Reporter, sending_type: str) -> None:
    validate_sender(payload, reporter)
    if not is_non_empty_string(payload.get("message")):
        reporter.error("$.message", "must be a non-empty message string")
    others = payload.get("other_recipients")
    if others is not None:
        validate_recipients(others, reporter, "$.other_recipients")
    params = validate_params_array(payload.get("params"), reporter, "$.params")
    if params is None:
        return

    rules = BULK_PARAM_RULES[sending_type]
    for index, item in enumerate(params):
        path = f"$.params[{index}]"
        if not isinstance(item, dict):
            reporter.error(path, "must be an object")
            continue
        for key in sorted(set(item) - rules["allowed"]):
            hint = CROSS_MODE_HINTS.get((sending_type, key))
            detail = hint if hint else "allowed keys are " + ", ".join(sorted(rules["allowed"]))
            reporter.error(f"{path}.{key}", f"is not a {sending_type} selector; {detail}")
        for key in rules.get("required", ()):
            if key not in item:
                reporter.error(f"{path}.{key}", "is required")
        required_any = rules.get("required_any")
        if required_any and not any(key in item for key in required_any):
            reporter.error(path, "must carry at least one of " + ", ".join(required_any))
        for key in rules.get("windows", ()):
            if key in item:
                validate_window(item[key], reporter, f"{path}.{key}")
        if rules["operator_array"] and "operator" in item:
            validate_operator_array(item["operator"], reporter, f"{path}.operator")


def validate_cancel(payload: dict[str, Any], reporter: Reporter) -> None:
    for key in sorted(set(payload) - {"message_outbox_id"}):
        reporter.error(f"$.{key}", "is not part of a cancel payload; send one message_outbox_id per request")
    value = payload.get("message_outbox_id")
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        reporter.error("$.message_outbox_id", "must be a positive integer")


def validate_price(payload: dict[str, Any], reporter: Reporter) -> None:
    for key in sorted(set(payload) - {"number", "message"}):
        reporter.error(f"$.{key}", "is not part of a calculate-price payload; it takes number and message")
    if not is_non_empty_string(payload.get("number")):
        reporter.error("$.number", "must be a non-empty sender number string")
    if not is_non_empty_string(payload.get("message")):
        reporter.error("$.message", "must be a non-empty message string")


def validate_payload(payload: Any, reporter: Reporter) -> None:
    if not isinstance(payload, dict):
        reporter.error("$", "payload must be a JSON object")
        return

    reject_bale_shape(payload, reporter)

    if "sending_type" not in payload:
        if "message_outbox_id" in payload:
            validate_cancel(payload, reporter)
            return
        if "number" in payload and "message" in payload:
            validate_price(payload, reporter)
            return
        reporter.error("$.sending_type", "is required for send payloads; cancel and calculate-price have their own shapes")
        return

    sending_type = payload.get("sending_type")
    if sending_type not in ALL_SEND_TYPES:
        reporter.error("$.sending_type", "must be one of: " + ", ".join(sorted(ALL_SEND_TYPES)))
        return

    reject_unknown_top_level(payload, reporter, sending_type)
    validate_send_time(payload, reporter)

    if sending_type in BULK_TARGETING_TYPES:
        reporter.warn(
            "$.sending_type",
            f"{sending_type} resolves its audience from vendor or file data; a live send needs the approval gate in references/15-targeting-and-bulk-sends.md",
        )

    if sending_type in {"webservice", "normal"}:
        validate_webservice_or_normal(payload, reporter, sending_type)
    elif sending_type == "peer_to_peer":
        validate_peer_to_peer(payload, reporter)
    elif sending_type == "pattern":
        validate_pattern(payload, reporter)
    elif sending_type == "votp":
        validate_votp(payload, reporter)
    elif sending_type in MULTIPART_SEND_TYPES:
        validate_multipart_metadata(payload, reporter, sending_type)
    elif sending_type == "keyword_phonebook":
        validate_keyword_phonebook(payload, reporter)
    elif sending_type == "phonebook":
        validate_phonebook(payload, reporter)
    elif sending_type in BULK_PARAM_RULES:
        validate_bulk_targeting(payload, reporter, sending_type)


# --------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------

PAYLOAD_CASES: list[tuple[str, dict[str, Any], bool]] = [
    ("webservice, minimal", {"sending_type": "webservice", "from_number": "+983000505", "message": "Your order shipped", "params": {"recipients": ["+989123830000"]}}, True),
    ("webservice, unnormalised recipient", {"sending_type": "webservice", "from_number": "+983000505", "message": "x", "params": {"recipients": ["09123830000"]}}, False),
    ("webservice, top-level recipients", {"sending_type": "webservice", "from_number": "+983000505", "message": "x", "recipients": ["+989123830000"], "params": {"recipients": ["+989123830000"]}}, False),
    ("pattern, minimal", {"sending_type": "pattern", "from_number": "+983000505", "code": "abc123", "recipients": ["+989123830000"], "params": {"code": "458921"}}, True),
    ("pattern, numeric variable", {"sending_type": "pattern", "from_number": "+983000505", "code": "abc123", "recipients": ["+989123830000"], "params": {"code": 458921}}, False),
    ("pattern, two recipients", {"sending_type": "pattern", "from_number": "+983000505", "code": "abc123", "recipients": ["+989123830000", "+989123830001"], "params": {"code": "458921"}}, False),
    ("pattern, recipients inside params", {"sending_type": "pattern", "from_number": "+983000505", "code": "abc123", "recipients": ["+989123830000"], "params": {"recipients": ["+989123830000"], "code": "1"}}, False),
    ("votp, minimal", {"sending_type": "votp", "message": "45852", "params": {"recipients": ["+989123830000"]}}, True),
    ("votp, Persian-Indic code", {"sending_type": "votp", "message": "\u06f4\u06f5\u06f8\u06f5\u06f2", "params": {"recipients": ["+989123830000"]}}, False),
    ("votp, superscript code", {"sending_type": "votp", "message": "\u00b2\u00b3\u2074\u2075", "params": {"recipients": ["+989123830000"]}}, False),
    ("bale payload", {"bot_id": 1, "phone_number": "989123830000", "message_data": {"message": {"text": "hi"}}}, False),
    ("unknown top-level key", {"sending_type": "webservice", "from_number": "+983000505", "message": "x", "params": {"recipients": ["+989123830000"]}, "chat_id": 4}, False),
    ("postal_code, unvalidated params", {"sending_type": "postal_code", "from_number": "+98BANK", "message": "x", "params": [{"garbage": "totally-unvalidated"}]}, False),
    ("postal_code, valid", {"sending_type": "postal_code", "from_number": "+98BANK", "message": "x", "params": [{"bank": "all", "postal_code": 131, "gender": 0, "age_from": 1330, "age_to": 1402, "mci": {"start": 0, "size": 1}, "irancell": {"start": 0, "size": 0}, "other": {"start": 0, "size": 0}}]}, True),
    ("geolocation with country field names", {"sending_type": "geolocation", "from_number": "+98BANK", "message": "x", "params": [{"province_id": 1, "age_from": 1354, "age_to": 1364, "operator": [{"start": 0, "size": 10, "id": 1}]}]}, False),
    ("job, valid", {"sending_type": "job", "from_number": "+98PRO", "message": "x", "params": [{"main_category_id": 1, "sub_category_id": 1, "operator": [{"start": 0, "size": 3373, "id": 2}]}]}, True),
    ("phonebook, mixed selectors", {"sending_type": "phonebook", "from_number": "+983000505", "message": "x", "params": [{"type": "all", "phonebook_ids": ["1"], "phonebook_id": "2"}]}, False),
    ("file, bad files entry", {"sending_type": "file", "from_number": "+983000505", "message": "x", "files[]": [123]}, False),
    ("cancel, valid", {"message_outbox_id": 1148303263}, True),
    ("cancel, extra key", {"message_outbox_id": 1148303263, "sending_type_hint": "x"}, False),
    ("price, valid", {"number": "+983000505", "message": "x"}, True),
]


def load_corpus(script_dir: Path) -> list[dict[str, Any]]:
    path = script_dir / CORPUS_FILENAME
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit_(EXIT_CORPUS, f"corpus is missing or unreadable at {path}: {exc}")
    cases = document.get("cases")
    stored = document.get("corpus_sha256")
    if not isinstance(cases, list) or not isinstance(stored, str):
        raise SystemExit_(EXIT_CORPUS, f"corpus at {path} has no cases array or no corpus_sha256")
    # The corpus canonicalization field is the contract: the digest covers the parsed
    # cases re-serialised with ensure_ascii=False, so it describes the data and not the
    # \uXXXX escaping the file happens to be stored in. Keep this identical to
    # run_self_test() in alaa-bale-provider/scripts/validate_bale_payload.py.
    canonical = json.dumps(cases, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    if digest != stored:
        raise SystemExit_(
            EXIT_CORPUS,
            f"corpus checksum mismatch at {path}: cases hash to {digest}, file records {stored}",
        )
    return cases


class SystemExit_(Exception):
    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def run_self_test(script_dir: Path) -> int:
    failures: list[str] = []
    cases = load_corpus(script_dir)

    for index, case in enumerate(cases):
        raw = case["input"]
        for channel in ("mediana", "bale"):
            expected = case[f"{channel}_expected"]
            try:
                actual: Any = normalize_msisdn(raw, channel)
            except NormalizationError as exc:
                actual = None
                reason = exc.reason
            else:
                reason = ""
            if actual != expected:
                failures.append(
                    f"corpus[{index}] {channel}: expected {expected!r}, got {actual!r}"
                    + (f" ({reason})" if reason else "")
                )

    for name, payload, should_pass in PAYLOAD_CASES:
        reporter = Reporter()
        validate_payload(payload, reporter)
        passed = not reporter.errors
        if passed != should_pass:
            verdict = "accepted" if passed else "rejected"
            failures.append(f"payload case {name!r}: {verdict}, expected the opposite. errors={reporter.errors}")

    print(f"[SELF-TEST] {len(cases)} corpus cases x 2 channels, {len(PAYLOAD_CASES)} payload cases")
    if failures:
        for failure in failures:
            print(f"[FAIL] {failure}")
        print(f"[SELF-TEST] {len(failures)} disagreement(s)")
        return EXIT_INVALID
    print("[SELF-TEST] all cases agree")
    return EXIT_OK


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate a Mediana/IPPanel Edge payload, or normalise an Iranian mobile number.",
        epilog=(
            "exit codes: 0 passed | 1 payload invalid, number rejected, or self-test disagreed | "
            "2 wrong invocation | 3 payload file unreadable or not JSON | 4 conformance corpus missing or checksum mismatch"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("payload", nargs="?", type=Path, help="path to a JSON payload file")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    parser.add_argument("--normalize", metavar="RAW", help="render one raw number in a channel's wire form")
    parser.add_argument(
        "--channel",
        choices=sorted(CHANNEL_PREFIX),
        default="mediana",
        help="target channel for --normalize (default: mediana)",
    )
    parser.add_argument("--self-test", action="store_true", help="drive the shared conformance corpus and the payload cases")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    script_dir = Path(__file__).resolve().parent

    modes = [bool(args.self_test), args.normalize is not None, args.payload is not None]
    if sum(modes) != 1:
        parser.print_usage(sys.stderr)
        print("[ERROR] give exactly one of: a payload path, --normalize RAW, or --self-test", file=sys.stderr)
        return EXIT_USAGE

    if args.self_test:
        try:
            return run_self_test(script_dir)
        except SystemExit_ as exc:
            print(f"[ERROR] {exc.message}", file=sys.stderr)
            return exc.code

    if args.normalize is not None:
        try:
            print(normalize_msisdn(args.normalize, args.channel))
        except NormalizationError as exc:
            print(f"[ERROR] cannot render this value for {args.channel}: {exc}", file=sys.stderr)
            return EXIT_INVALID
        return EXIT_OK

    try:
        payload = json.loads(args.payload.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"[ERROR] cannot read {args.payload}: {exc}", file=sys.stderr)
        return EXIT_INPUT
    except json.JSONDecodeError as exc:
        print(f"[ERROR] {args.payload} is not valid JSON: {exc}", file=sys.stderr)
        return EXIT_INPUT

    reporter = Reporter()
    validate_payload(payload, reporter)

    for warning in reporter.warnings:
        print(f"[WARN] {warning}")
    for error in reporter.errors:
        print(f"[ERROR] {error}")

    if reporter.errors or (args.strict and reporter.warnings):
        return EXIT_INVALID

    print("[OK] Mediana/IPPanel payload shape is valid; account truth is unchecked")
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
