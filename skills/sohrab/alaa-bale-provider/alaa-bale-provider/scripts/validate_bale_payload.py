#!/usr/bin/env python3
"""Validate Bale Safir send_message JSON payloads used in examples or tests.

This helper validates local JSON fixtures before agents commit docs, tests, or
provider payload examples. It does not call Bale.

Usage:
    python scripts/validate_bale_payload.py payload.json
    python scripts/validate_bale_payload.py --strict payload.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

PHONE_RE = re.compile(r"^989\d{9}$")
PRIMARY_VARIANTS = ("message", "otp_message", "template_message")
BUTTON_ACTIONS = ("url", "web_app", "copy_text")


class Reporter:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, path: str, message: str) -> None:
        self.errors.append(f"{path}: {message}")

    def warn(self, path: str, message: str) -> None:
        self.warnings.append(f"{path}: {message}")


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and value != ""


def validate_payload(payload: Any, reporter: Reporter) -> None:
    if not isinstance(payload, dict):
        reporter.error("$", "payload must be a JSON object")
        return

    bot_id = payload.get("bot_id")
    if not isinstance(bot_id, int) or isinstance(bot_id, bool):
        reporter.error("$.bot_id", "must be an integer")

    phone_number = payload.get("phone_number")
    if not isinstance(phone_number, str):
        reporter.error("$.phone_number", "must be a string")
    elif not PHONE_RE.fullmatch(phone_number):
        reporter.error(
            "$.phone_number",
            "must match Alaa canonical Bale format: 98 plus a ten-digit Iranian mobile number, e.g. 989123830000",
        )

    request_id = payload.get("request_id")
    if request_id is None:
        reporter.warn("$.request_id", "missing; recommended for idempotent production sends")
    elif not is_non_empty_string(request_id):
        reporter.error("$.request_id", "must be a non-empty string when present")

    message_data = payload.get("message_data")
    if not isinstance(message_data, dict):
        reporter.error("$.message_data", "must be an object")
        return

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
            reporter.warn("$.message_data.is_secure", "secure OTP is not documented; confirm before using")
        validate_otp(message_data["otp_message"], reporter, "$.message_data.otp_message")
    elif variant == "template_message":
        validate_template(message_data["template_message"], reporter, "$.message_data.template_message")


def validate_message(message: Any, reporter: Reporter, path: str) -> None:
    if not isinstance(message, dict):
        reporter.error(path, "must be an object")
        return

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

    if not is_non_empty_string(button.get("text")):
        reporter.error(f"{path}.text", "must be a non-empty string")

    actions = [name for name in BUTTON_ACTIONS if name in button]
    if not actions:
        reporter.error(path, "must include at least one action: url, web_app, or copy_text")
    elif len(actions) > 1:
        reporter.warn(path, "has multiple button actions; prefer exactly one action per button")

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

    otp = otp_message.get("otp")
    if not is_non_empty_string(otp):
        reporter.error(f"{path}.otp", "must be a non-empty string")
    elif not otp.isdigit():
        reporter.error(f"{path}.otp", "must contain only numeric digits")


def validate_template(template_message: Any, reporter: Reporter, path: str) -> None:
    if not isinstance(template_message, dict):
        reporter.error(path, "must be an object")
        return

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


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Bale Safir send_message JSON payload.")
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

    print("[OK] Bale Safir payload is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
