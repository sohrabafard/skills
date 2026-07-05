#!/usr/bin/env python3
"""Validate a Mediana/IPPanel send JSON payload or JSON-equivalent multipart metadata.

This is a local skill helper for examples, fixtures, and payload builders. It does
not call Mediana/IPPanel and it does not validate account-specific sender numbers,
pattern codes, phonebook IDs, geographic IDs, or file contents.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

RECIPIENT_RE = re.compile(r"^\+989\d{9}$")
SENDER_RE = re.compile(r"^\+98[A-Za-z0-9]+$")
SEND_TIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")

JSON_SEND_TYPES = {
    "webservice",
    "normal",  # legacy/account-specific; warn when used
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
    bale_fields = [field for field in ("bot_id", "phone_number", "message_data") if field in payload]
    if bale_fields:
        reporter.error(
            "$",
            "looks like a Bale Safir payload; Mediana uses Authorization and sending_type/from_number/message/params or recipients",
        )


def validate_sender(payload: dict[str, Any], reporter: Reporter, *, required: bool = True) -> None:
    sender = payload.get("from_number")
    if not is_non_empty_string(sender):
        if required:
            reporter.error("$.from_number", "must be a non-empty configured sender/originator string")
        return
    if not SENDER_RE.fullmatch(sender):
        reporter.warn(
            "$.from_number",
            "does not match common +98 sender examples; keep only if this exact sender is account-approved",
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
        reporter.error(path, "must contain exactly one recipient for this Mediana/IPPanel endpoint")
    for index, recipient in enumerate(value):
        recipient_path = f"{path}[{index}]"
        if not is_non_empty_string(recipient):
            reporter.error(recipient_path, "must be a non-empty string")
        elif not RECIPIENT_RE.fullmatch(recipient):
            reporter.error(recipient_path, "must match +989xxxxxxxxx, e.g. +989123830000")


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
            reporter.error(f"$.files[][${index}]", "must be a non-empty file path/reference string")


def validate_webservice_or_normal(payload: dict[str, Any], reporter: Reporter, sending_type: str) -> None:
    if sending_type == "normal":
        reporter.warn("$.sending_type", "normal is legacy/account-specific; prefer webservice unless repo truth requires normal")
    validate_sender(payload, reporter)
    if not is_non_empty_string(payload.get("message")):
        reporter.error("$.message", "must be a non-empty SMS text string")
    params = validate_params_object(payload.get("params"), reporter, "$.params")
    if params is not None:
        validate_recipients(params.get("recipients"), reporter, "$.params.recipients")
    if "recipients" in payload:
        reporter.error("$.recipients", "webservice/normal recipients must be nested under $.params.recipients")


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
            reporter.error("$.params.recipients", "pattern recipients must be top-level $.recipients; $.params is for pattern variables")
        variable_items = [(key, value) for key, value in params.items() if key != "recipients"]
        if not variable_items:
            reporter.error("$.params", "must contain at least one pattern variable")
        for key, value in variable_items:
            if not is_non_empty_string(key):
                reporter.error("$.params", "all pattern variable keys must be non-empty strings")
            if not isinstance(value, (str, int, float, bool)) or value is None:
                reporter.error(f"$.params.{key}", "pattern variable values must be scalar strings/numbers/bools")
    if "phonebook" in payload:
        phonebook = payload["phonebook"]
        if not isinstance(phonebook, dict):
            reporter.error("$.phonebook", "must be an object when provided")
        elif "id" not in phonebook:
            reporter.error("$.phonebook.id", "is required when phonebook is provided")


def validate_votp(payload: dict[str, Any], reporter: Reporter) -> None:
    if "from_number" in payload:
        reporter.warn("$.from_number", "official VOTP body and vendor SDK omit from_number; confirm account behavior before sending it")
    code = payload.get("message")
    if not is_non_empty_string(code):
        reporter.error("$.message", "must be a non-empty OTP code string")
    elif not code.isdigit():
        reporter.warn("$.message", "VOTP code should normally contain only ASCII digits")
    params = validate_params_object(payload.get("params"), reporter, "$.params")
    if params is not None:
        validate_recipients(params.get("recipients"), reporter, "$.params.recipients", exactly_one=True)
    if "recipients" in payload:
        reporter.error("$.recipients", "VOTP recipients must be nested under $.params.recipients")


def validate_multipart_metadata(payload: dict[str, Any], reporter: Reporter, sending_type: str) -> None:
    reporter.warn("$", f"{sending_type} is multipart/form-data in live requests; this validates only JSON-equivalent metadata")
    validate_sender(payload, reporter)
    validate_files_field(payload, reporter)
    if sending_type in {"file", "keyword"} and not is_non_empty_string(payload.get("message")):
        reporter.error("$.message", "must be a non-empty message string")
    if "other_recipients" in payload:
        validate_recipients(payload.get("other_recipients"), reporter, "$.other_recipients")


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
        elif item_type == "all" and "phonebook_ids" not in item:
            reporter.error(f"{path}.phonebook_ids", "is required when type is all")
        elif item_type == "detail":
            if "phonebook_id" not in item:
                reporter.error(f"{path}.phonebook_id", "is required when type is detail")
            if "number_ids" not in item:
                reporter.error(f"{path}.number_ids", "is required when type is detail")


def validate_bulk_targeting(payload: dict[str, Any], reporter: Reporter, sending_type: str) -> None:
    reporter.warn("$.sending_type", f"{sending_type} can produce bulk/targeted outreach; require explicit product/compliance approval")
    validate_sender(payload, reporter)
    if not is_non_empty_string(payload.get("message")):
        reporter.error("$.message", "must be a non-empty message string")
    params = validate_params_array(payload.get("params"), reporter, "$.params")
    if params is None:
        return
    if "other_recipients" in payload:
        validate_recipients(payload.get("other_recipients"), reporter, "$.other_recipients")


def validate_cancel(payload: dict[str, Any], reporter: Reporter) -> None:
    value = payload.get("message_outbox_id")
    if not isinstance(value, int) or value <= 0:
        reporter.error("$.message_outbox_id", "must be a positive integer")


def validate_price(payload: dict[str, Any], reporter: Reporter) -> None:
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
        reporter.error("$.sending_type", "is required for send payloads; cancel and price payloads have their own shapes")
        return

    sending_type = payload.get("sending_type")
    if sending_type not in ALL_SEND_TYPES:
        reporter.error(
            "$.sending_type",
            "must be one of: " + ", ".join(sorted(ALL_SEND_TYPES)),
        )
        return

    validate_send_time(payload, reporter)

    if sending_type in BULK_TARGETING_TYPES:
        reporter.warn("$.sending_type", f"{sending_type} may be high-volume/bulk; do not live-send without approval")

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
    elif sending_type in {"postal_code", "country", "geolocation", "job"}:
        validate_bulk_targeting(payload, reporter, sending_type)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Mediana/IPPanel send JSON payload or JSON-equivalent metadata.")
    parser.add_argument("payload", type=Path, help="Path to JSON payload file")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    args = parser.parse_args()

    try:
        payload = json.loads(args.payload.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"[ERROR] File not found: {args.payload}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"[ERROR] Invalid JSON: {exc}", file=sys.stderr)
        return 2

    reporter = Reporter()
    validate_payload(payload, reporter)

    for warning in reporter.warnings:
        print(f"[WARN] {warning}")
    for error in reporter.errors:
        print(f"[ERROR] {error}")

    if reporter.errors or (args.strict and reporter.warnings):
        return 1

    print("[OK] Mediana/IPPanel payload metadata is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
