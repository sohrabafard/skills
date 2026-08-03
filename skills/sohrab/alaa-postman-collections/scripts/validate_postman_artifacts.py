#!/usr/bin/env python3
"""Validate Postman Collection v2.1 and environment artifacts as an implementation contract.

Exit codes are distinct and documented in
references/60-validation-and-output-contract.md:

  0  no errors; warnings may be present and are printed
  1  at least one rule violation in the collection or an environment
  2  input failure: a file could not be read, is not a JSON object, a flag is invalid, or
     --require-schema was passed and official schema validation could not run
  3  official Postman v2.1 schema validation ran and failed
  4  a committed artifact carries a value that looks like a real credential

When several apply, the highest-priority code wins in this order: 2, 4, 3, 1, 0.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import Any, Iterable

DEFAULT_SCHEMA_URL = "https://schema.getpostman.com/collection/json/v2.1.0/draft-04/collection.json"
CANONICAL_COLLECTION_SCHEMA_URL = "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
COLLECTION_SCHEMA_HINT = "v2.1.0"

EXIT_OK = 0
EXIT_RULES = 1
EXIT_INPUT = 2
EXIT_SCHEMA = 3
EXIT_SECRET = 4

VARIABLE_RE = re.compile(r"{{\s*([^{}\s][^{}]*?)\s*}}")
HEADING_RE = re.compile(r"^[ \t]{0,3}#{1,6}[ \t]+(.+?)[ \t]*#*[ \t]*$", re.MULTILINE)

SECRET_HINTS = (
    "secret",
    "token",
    "password",
    "passwd",
    "api_key",
    "apikey",
    "private_key",
    "client_secret",
    "bearer",
    "credential",
)
PLACEHOLDER_HINTS = (
    "",
    "<replace-me>",
    "<redacted>",
    "<token>",
    "changeme",
    "replace-me",
    "example",
    "placeholder",
    "dummy",
    "your-",
)
DEPRECATED_SCRIPT_PATTERNS = (
    "postman.setEnvironmentVariable",
    "postman.clearEnvironmentVariable",
    "postman.setGlobalVariable",
    "postman.clearGlobalVariable",
    "postman.getEnvironmentVariable",
    "postman.getGlobalVariable",
    "postman.setNextRequest",
)
# Script APIs with no Insomnia counterpart. See
# references/50-insomnia-compatibility-and-free-plan-rules.md for each source.
UNPORTABLE_SCRIPT_APIS = ("pm.vault", "pm.require(", "pm.state", "pm.datasets", "pm.visualizer")
# Members Insomnia registers on `insomnia.response.to`. Read from Insomnia's own source at
# packages/insomnia-scripting-environment/src/objects/response.ts, tag `core@12.6.0`. Any
# other member is unresolved after the `pm.`-to-`insomnia.` rewrite.
# references/50-insomnia-compatibility-and-free-plan-rules.md carries the citation.
INSOMNIA_RESPONSE_TO_MEMBERS = frozenset(
    {"withBody", "error", "ok", "json", "status", "header", "body", "jsonBody", "jsonSchema"}
)
RESPONSE_TO_MEMBER_RE = re.compile(
    r"pm\.response\.to\.(?:not\.)?(?:have\.|be\.)?([A-Za-z_$][\w$]*)"
)
# Auth types Insomnia's Postman importer maps. Any other type imports as no auth.
INSOMNIA_MAPPED_AUTH_TYPES = frozenset(
    {"basic", "bearer", "apikey", "digest", "oauth1", "oauth2", "awsv4", "noauth"}
)

VARIABLE_SET_RE = re.compile(
    r"\bpm\.(?:environment|collectionVariables|globals)\.set\(\s*['\"]([^'\"]+)['\"]"
)
VARIABLE_ARRAY_SET_RE = re.compile(
    r"\b(?:setLocal|setVariables|saveVariables)\(\s*\[(?P<body>[^\]]*)\]"
)
QUOTED_NAME_RE = re.compile(r"['\"]([^'\"]+)['\"]")

# --- Structural capture-guard analysis -------------------------------------------------
# references/42-scripts-and-state-capture.md requires that a capture not run on an error
# response. A substring search for `pm.response.code` cannot prove that: 43-response-tests
# mandates `pm.expect(pm.response.code).to.eql(200)` on every request, so the substring is
# present in every conforming collection and the check can never fail. The test below is
# structural instead — the guard must dominate the write.

# A condition that can actually stop the write: the response code compared with an
# operator, or tested for membership in an explicit set of accepted codes.
RESPONSE_CODE_TEST_RE = re.compile(
    r"pm\.response\.code\s*(?:===|!==|==|!=|>=|<=|>|<)"
    r"|(?:===|!==|==|!=|>=|<=|>|<)\s*pm\.response\.code"
    r"|\.(?:includes|indexOf|has)\(\s*pm\.response\.code\s*\)"
)
# A bare chai assertion on the response code. At top level an uncaught throw aborts the
# rest of the script, so it does stop a later write. Inside a `pm.test` callback the
# runner catches the throw and the script continues, which is why paren depth is checked.
BARE_CODE_ASSERTION_RE = re.compile(
    r"pm\.expect\(\s*pm\.response\.code|pm\.response\.to\.(?:have\.status|be\.success)"
)
CONDITION_HEADER_RE = re.compile(r"\b(?:if|while|for)\s*\(")
FUNCTION_HEADER_RE = re.compile(r"=>\s*$|\bfunction\b\s*[\w$]*\s*\(")
REGEX_LITERAL_PRECEDERS = frozenset("(,=:[!&|?{};+-*%~^<>")

# --- Pinned vendor identifiers ---------------------------------------------------------
# A committed environment value that pins a vendor model or engine identifier is an
# implementation constant the generator should own, not operator input. The rule is keyed
# on the variable name and the value's shape, never on a list of vendor or model names:
# which model to use is owned by alaa-prompting-guide, not by this skill.
VENDOR_PINNED_KEY_HINTS = ("model", "llm", "engine", "deployment", "embedding", "completion")
VENDOR_PINNED_VALUE_RE = re.compile(r"^[A-Za-z][A-Za-z0-9._-]*$")

CORRELATION_VARIABLE_SUFFIXES = ("_last_request_id", "_last_traceparent")
CORRELATION_VARIABLE_NAMES = frozenset({"last_request_id", "last_traceparent"})
TOKEN_BODY_KEYS = ('"access_token"', '"refresh_token"', '"id_token"', '"accessToken"', '"refreshToken"')

# A value matching one of these is a real credential shape, not a placeholder.
REAL_SECRET_PATTERNS = (
    ("JSON Web Token", re.compile(r"eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}")),
    ("OpenAI-style key", re.compile(r"\bsk-[A-Za-z0-9]{16,}")),
    ("GitHub token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}|\bgithub_pat_[A-Za-z0-9_]{20,}")),
    ("AWS access key id", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{30,}")),
    ("PEM private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
)
HIGH_ENTROPY_RE = re.compile(r"^[A-Za-z0-9+/=_-]{24,}$")


class InputError(Exception):
    """A file could not be read or is not the expected JSON shape."""


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.secrets: list[str] = []
        self.schema_errors: list[str] = []
        self.schema_skipped: str | None = None
        self.counts: dict[str, int] = {
            "requests": 0,
            "saved_responses": 0,
            "requests_with_success_example": 0,
            "requests_with_error_example": 0,
            "requests_with_tests": 0,
            "requests_with_captures": 0,
            "requests_with_scripts": 0,
        }

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def secret(self, message: str) -> None:
        self.secrets.append(message)

    def bump(self, key: str) -> None:
        self.counts[key] = self.counts.get(key, 0) + 1


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InputError(f"cannot read JSON `{path}`: {exc}") from exc


def iter_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
        return
    if isinstance(value, list):
        for item in value:
            yield from iter_strings(item)
        return
    if isinstance(value, dict):
        for item in value.values():
            yield from iter_strings(item)


def variable_refs(value: Any) -> set[str]:
    refs: set[str] = set()
    for text in iter_strings(value):
        for raw_name in VARIABLE_RE.findall(text):
            name = raw_name.strip()
            if name.startswith("$"):
                continue
            refs.add(name)
    return refs


def iter_variable_blocks(node: Any) -> Iterable[list[dict[str, Any]]]:
    if not isinstance(node, dict):
        return
    variables = node.get("variable")
    if isinstance(variables, list):
        yield variables
    items = node.get("item")
    if isinstance(items, list):
        for item in items:
            yield from iter_variable_blocks(item)


def collect_collection_variable_keys(collection: dict[str, Any]) -> set[str]:
    keys: set[str] = set()
    for block in iter_variable_blocks(collection):
        for variable in block:
            if isinstance(variable, dict):
                key = variable.get("key") or variable.get("id") or variable.get("name")
                if isinstance(key, str) and key:
                    keys.add(key)
    return keys


def extract_environment_keys(env: dict[str, Any]) -> set[str]:
    keys: set[str] = set()
    values = env.get("values")
    if not isinstance(values, list):
        return keys
    for variable in values:
        if isinstance(variable, dict):
            key = variable.get("key") or variable.get("name")
            if isinstance(key, str) and key:
                keys.add(key)
    return keys


def is_placeholder(value: Any) -> bool:
    if value is None:
        return True
    if not isinstance(value, str):
        return False
    normalized = value.strip().lower()
    if normalized in PLACEHOLDER_HINTS:
        return True
    if "{{" in normalized:
        return True
    return any(hint in normalized for hint in PLACEHOLDER_HINTS if hint)


def pinned_vendor_identifier(key: str, value: Any) -> str | None:
    """Return the pinned identifier when a committed value names a vendor model or engine.

    Keyed on the variable name and the value's shape, never on a list of vendor or model
    names: this skill carries no such list. A `{{reference}}` or a placeholder is correct and
    produces nothing.
    """
    lowered = key.lower()
    if not any(hint in lowered for hint in VENDOR_PINNED_KEY_HINTS):
        return None
    if not isinstance(value, str):
        return None
    candidate = value.strip()
    if not candidate or is_placeholder(candidate):
        return None
    if not VENDOR_PINNED_VALUE_RE.match(candidate):
        return None
    if not any(char.isdigit() for char in candidate) and "-" not in candidate:
        return None
    return candidate


def report_pinned_vendor_identifier(scope: str, key: str, value: Any, report: Report) -> None:
    pinned = pinned_vendor_identifier(key, value)
    if pinned:
        report.error(
            f"{scope}: committed value `{pinned}` pins a vendor model or engine identifier. It is an "
            "implementation constant the generator should own: declare it as a generator input, "
            "reference it as a variable here, and route which identifier to use to "
            "`/alaa-prompting-guide` (`$alaa-prompting-guide`)."
        )


def looks_sensitive_key(name: str) -> bool:
    lowered = name.lower()
    normalized = re.sub(r"[^a-z0-9]", "", lowered)
    if normalized.endswith("tokenid"):
        return False
    return any(hint in lowered for hint in SECRET_HINTS)


def real_secret_reason(value: Any, key_is_sensitive: bool = False) -> str | None:
    """Return why this value looks like a real credential, or None."""
    if not isinstance(value, str):
        return None
    candidate = value.strip()
    if not candidate or "{{" in candidate:
        return None
    for label, pattern in REAL_SECRET_PATTERNS:
        if pattern.search(candidate):
            return label
    if key_is_sensitive and not is_placeholder(candidate):
        stripped = candidate.removeprefix("Bearer ").strip()
        if (
            HIGH_ENTROPY_RE.match(stripped)
            and any(character.isdigit() for character in stripped)
            and any(character.isalpha() for character in stripped)
        ):
            return "high-entropy value under a secret-like key"
    return None


def description_text(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict) and isinstance(value.get("content"), str):
        return value["content"].strip()
    return ""


def heading_names(text: str) -> set[str]:
    return {match.strip().lower() for match in HEADING_RE.findall(text)}


def raw_url(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict) and isinstance(value.get("raw"), str):
        return value["raw"]
    return ""


def endpoint_url(value: Any) -> str:
    """Return the scheme/host/path identity while allowing saved query variants."""
    return raw_url(value).split("#", 1)[0].split("?", 1)[0]


def script_text_of(events: Any, listener: str | None = None) -> str:
    lines: list[str] = []
    if not isinstance(events, list):
        return ""
    for event in events:
        if not isinstance(event, dict):
            continue
        if listener is not None and event.get("listen") != listener:
            continue
        script = event.get("script")
        if not isinstance(script, dict):
            continue
        exec_value = script.get("exec")
        if isinstance(exec_value, str):
            lines.append(exec_value)
        elif isinstance(exec_value, list):
            lines.extend(line for line in exec_value if isinstance(line, str))
    return "\n".join(lines)


def written_variable_names(script_text: str) -> set[str]:
    names = set(VARIABLE_SET_RE.findall(script_text))
    for match in VARIABLE_ARRAY_SET_RE.finditer(script_text):
        names.update(QUOTED_NAME_RE.findall(match.group("body")))
    return names


def is_correlation_variable(name: str) -> bool:
    return name in CORRELATION_VARIABLE_NAMES or name.endswith(CORRELATION_VARIABLE_SUFFIXES)


def mask_script(text: str) -> str:
    """Blank comment, string and regex-literal contents, preserving length and newlines.

    Scanning runs on the mask so a brace inside a string cannot move the block depth and a
    `pm.response.code` inside a comment cannot count as a guard. Offsets stay aligned with
    the original text.
    """
    out = list(text)
    length = len(text)
    index = 0
    previous = ""

    def blank(start: int, end: int) -> None:
        for position in range(start, min(end, length)):
            if out[position] != "\n":
                out[position] = " "

    while index < length:
        char = text[index]
        nxt = text[index + 1] if index + 1 < length else ""
        if char == "/" and nxt == "/":
            end = text.find("\n", index)
            end = length if end == -1 else end
            blank(index, end)
            index = end
            continue
        if char == "/" and nxt == "*":
            end = text.find("*/", index + 2)
            end = length if end == -1 else end + 2
            blank(index, end)
            index = end
            continue
        if char in "'\"`" or (char == "/" and previous in REGEX_LITERAL_PRECEDERS):
            closer = char if char != "/" else "/"
            end = index + 1
            in_class = False
            while end < length:
                if text[end] == "\\":
                    end += 2
                    continue
                if char == "/" and text[end] in "[]":
                    in_class = text[end] == "["
                elif text[end] == closer and not in_class:
                    end += 1
                    break
                elif char == "/" and text[end] == "\n":
                    break
                end += 1
            blank(index, end)
            previous = "x"
            index = end
            continue
        if not char.isspace():
            previous = char
        index += 1
    return "".join(out)


class ScanFailure(Exception):
    """A script could not be scanned into balanced brace blocks."""


def scan_blocks(masked: str) -> list[tuple[int, int, str, int]]:
    """Return `(open_offset, close_offset, header_text, depth)` for every brace block.

    The header is the masked text between the previous statement boundary and the opening
    brace, which is what carries `if (pm.response.code === 200)`.
    """
    blocks: list[tuple[int, int, str, int]] = []
    stack: list[tuple[int, str, int]] = []
    for index, char in enumerate(masked):
        if char == "{":
            boundary = max(masked.rfind(separator, 0, index) for separator in (";", "{", "}"))
            stack.append((index, masked[boundary + 1 : index], len(stack)))
        elif char == "}":
            if not stack:
                raise ScanFailure("a closing brace has no matching opening brace")
            open_offset, header, depth = stack.pop()
            blocks.append((open_offset, index, header, depth))
    if stack:
        raise ScanFailure("an opening brace has no matching closing brace")
    return blocks


def unguarded_capture_names(script_text: str) -> tuple[list[str], str | None]:
    """Classify every literal-named capture write in one script.

    Returns the names written on a path an error response also reaches, and a reason when the
    analysis could not decide. A capture is guarded when one of these dominates the write: an
    enclosing `if`, `while` or `for` whose own condition tests `pm.response.code`; a top-level
    early exit on `pm.response.code` that returns or throws first; or a top-level bare chai
    assertion on `pm.response.code` whose uncaught throw aborts the script. Correlation-only
    variables are exempt: they are captured on error responses on purpose.
    """
    writes = [
        (match.start(), match.group(1))
        for match in VARIABLE_SET_RE.finditer(script_text)
        if not is_correlation_variable(match.group(1))
    ]
    if not writes:
        return [], None

    masked = mask_script(script_text)
    try:
        blocks = scan_blocks(masked)
    except ScanFailure as exc:
        return [], str(exc)

    conditional_blocks = [
        (open_offset, close_offset, header, depth)
        for open_offset, close_offset, header, depth in blocks
        if CONDITION_HEADER_RE.search(header) and RESPONSE_CODE_TEST_RE.search(header)
    ]
    guard_spans = [(open_offset, close_offset) for open_offset, close_offset, _, _ in conditional_blocks]
    early_exit_ends = [
        close_offset
        for open_offset, close_offset, _, depth in conditional_blocks
        if depth == 0 and re.search(r"\b(?:return|throw)\b", masked[open_offset:close_offset])
    ]
    earliest_exit = min(early_exit_ends) if early_exit_ends else None

    assertion_offsets = [
        match.start()
        for match in BARE_CODE_ASSERTION_RE.finditer(masked)
        if masked.count("(", 0, match.start()) == masked.count(")", 0, match.start())
        and not any(open_o < match.start() < close_o for open_o, close_o, _, _ in blocks)
    ]
    earliest_assertion = min(assertion_offsets) if assertion_offsets else None

    function_spans = [
        (open_offset, close_offset)
        for open_offset, close_offset, header, _ in blocks
        if FUNCTION_HEADER_RE.search(header.rstrip())
    ]

    unguarded: list[str] = []
    inside_function = False
    for offset, name in writes:
        if any(open_o < offset < close_o for open_o, close_o in guard_spans):
            continue
        if earliest_exit is not None and offset > earliest_exit:
            continue
        if earliest_assertion is not None and offset > earliest_assertion:
            continue
        if any(open_o < offset < close_o for open_o, close_o in function_spans):
            inside_function = True
            continue
        unguarded.append(name)
    if inside_function and not unguarded:
        return [], "the capture runs inside a nested function whose call sites this check does not follow"
    return sorted(set(unguarded)), None


def check_script_text(script_text: str, scope: str, report: Report) -> None:
    for pattern in DEPRECATED_SCRIPT_PATTERNS:
        if pattern in script_text:
            report.error(
                f"{scope}: deprecated Postman interface `{pattern}`; Insomnia does not support it. "
                "Use the modern `pm.environment.*` equivalent."
            )
    if "pm.globals." in script_text:
        report.error(
            f"{scope}: `pm.globals.*` is not part of either committed artifact and Insomnia does not "
            "support it. Write to `pm.environment.*` instead."
        )
    for api in UNPORTABLE_SCRIPT_APIS:
        if api in script_text:
            report.warn(f"{scope}: `{api}` has no Insomnia counterpart; keep it out of required behavior")
    unsupported_members = sorted(
        {
            member
            for member in RESPONSE_TO_MEMBER_RE.findall(script_text)
            if member not in INSOMNIA_RESPONSE_TO_MEMBERS
        }
    )
    for member in unsupported_members:
        report.warn(
            f"{scope}: `pm.response.to...{member}` has no counterpart on Insomnia's response object "
            "after the `pm.`-to-`insomnia.` rewrite; Insomnia registers only "
            f"{', '.join(sorted(INSOMNIA_RESPONSE_TO_MEMBERS))}. Use `pm.expect(pm.response.code)` "
            "or one of those members instead."
        )
    for label, pattern in REAL_SECRET_PATTERNS:
        if pattern.search(script_text):
            report.secret(f"{scope}: script contains a literal that looks like a {label}")
            break


def validate_events(
    events: list[Any],
    scope: str,
    report: Report,
    require_success_guarded_captures: bool,
    declared_variables: set[str],
) -> None:
    seen_listeners: set[str] = set()
    for index, event in enumerate(events):
        event_scope = f"{scope}.event[{index}]"
        if not isinstance(event, dict):
            report.error(f"{event_scope}: event must be an object")
            continue
        listen = event.get("listen")
        if listen not in {"prerequest", "test"}:
            report.warn(f"{event_scope}: unexpected event listener `{listen}`")
        elif listen in seen_listeners:
            report.error(
                f"{event_scope}: a second `{listen}` event in one scope is dropped by Insomnia's "
                "importer; merge it into the first one"
            )
        else:
            seen_listeners.add(listen)

        script = event.get("script")
        if script is None:
            continue
        if not isinstance(script, dict):
            report.error(f"{event_scope}: script must be an object")
            continue
        exec_value = script.get("exec")
        if exec_value is None:
            continue
        if isinstance(exec_value, list):
            if not all(isinstance(line, str) for line in exec_value):
                report.error(f"{event_scope}: script.exec array must contain only strings")
                continue
            script_text = "\n".join(exec_value)
        elif isinstance(exec_value, str):
            report.warn(f"{event_scope}: script.exec is a single string; an array of lines reviews better")
            script_text = exec_value
        else:
            report.error(f"{event_scope}: script.exec must be a string or array of lines")
            continue

        check_script_text(script_text, event_scope, report)

        written = written_variable_names(script_text)
        guarded = {name for name in written if not is_correlation_variable(name)}
        if listen == "test" and require_success_guarded_captures and guarded:
            unguarded, undecided = unguarded_capture_names(script_text)
            if unguarded:
                names = ", ".join(f"`{name}`" for name in unguarded)
                report.error(
                    f"{event_scope}: capture writes {names} on a path an error response also reaches, so "
                    "an intentional error overwrites a working value. Move the write inside an explicit "
                    "`if (pm.response.code === 200)` block, or return early on any other code."
                )
            elif undecided:
                report.error(
                    f"{event_scope}: the capture's success guard could not be established structurally "
                    f"because {undecided}. Move the write into an explicit "
                    "`if (pm.response.code === 200)` block in this script so the guard is provable."
                )
        for variable_name in sorted(written - declared_variables):
            report.error(
                f"{event_scope}: script writes undeclared variable `{variable_name}`; declare it in the "
                "collection or the environment"
            )


def check_request_auth(request: dict[str, Any], scope: str, report: Report) -> None:
    auth = request.get("auth")
    if not isinstance(auth, dict):
        return
    auth_type = auth.get("type")
    if isinstance(auth_type, str) and auth_type not in INSOMNIA_MAPPED_AUTH_TYPES:
        report.warn(
            f"{scope}: auth type `{auth_type}` is not mapped by Insomnia's importer and arrives as no "
            "auth; use basic, bearer, apikey, digest, oauth1, oauth2, or awsv4"
        )
    entries = auth.get(auth_type) if isinstance(auth_type, str) else None
    if isinstance(entries, list):
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            key = str(entry.get("key", ""))
            reason = real_secret_reason(entry.get("value"), looks_sensitive_key(key) or key in {"value", "token"})
            if reason:
                report.secret(f"{scope}: auth.{auth_type}.{key} carries a {reason}")


def check_request_headers(request: dict[str, Any], scope: str, report: Report) -> None:
    headers = request.get("header")
    if not isinstance(headers, list):
        return
    for header in headers:
        if not isinstance(header, dict):
            continue
        key = str(header.get("key", ""))
        value = header.get("value")
        if key.lower() != "authorization":
            reason = real_secret_reason(value, looks_sensitive_key(key))
            if reason:
                report.secret(f"{scope}: header `{key}` carries a {reason}")
            continue
        text = value if isinstance(value, str) else ""
        if "{{" not in text:
            report.secret(
                f"{scope}: header `Authorization` has a literal value; reference a declared variable such "
                "as `Bearer {{access_token}}` and populate it from a capture script"
            )
        else:
            reason = real_secret_reason(text, True)
            if reason:
                report.secret(f"{scope}: header `Authorization` carries a {reason}")


def walk_items(
    items: Any,
    scope: str,
    report: Report,
    options: argparse.Namespace,
    declared_variables: set[str],
) -> None:
    if not isinstance(items, list):
        report.error(f"{scope}: `item` must be an array")
        return

    for index, item in enumerate(items):
        item_scope = f"{scope}.item[{index}]"
        if not isinstance(item, dict):
            report.error(f"{item_scope}: item must be an object")
            continue

        name = item.get("name")
        if isinstance(name, str) and name.strip():
            item_scope = f"{scope}.item[{index}] `{name.strip()}`"
        else:
            report.warn(f"{item_scope}: item is missing a clear name")

        request = item.get("request")
        child_items = item.get("item")
        if request is None and child_items is None:
            report.error(f"{item_scope}: item must contain either `request` or nested `item`")

        if child_items is not None:
            walk_items(child_items, item_scope, report, options, declared_variables)

        if request is not None and not isinstance(request, (dict, str)):
            report.error(f"{item_scope}: request must be an object or URL string")

        events = item.get("event", [])
        if events is not None and not isinstance(events, list):
            report.error(f"{item_scope}: event must be an array when present")
            events = []
        elif isinstance(events, list):
            validate_events(
                events,
                item_scope,
                report,
                options.require_success_guarded_captures,
                declared_variables,
            )

        if not isinstance(request, dict):
            continue

        report.bump("requests")

        misplaced_events = request.get("event")
        if isinstance(misplaced_events, list) and misplaced_events:
            report.error(
                f"{item_scope}.request.event: Postman v2.1 never executes scripts here; move them to the "
                "request item's own `event` array"
            )

        description = description_text(request.get("description") or item.get("description"))
        if options.min_description_chars > 0 and len(description) < options.min_description_chars:
            report.error(
                f"{item_scope}: request description has {len(description)} characters; minimum is "
                f"{options.min_description_chars}"
            )
        if options.require_doc_section:
            present = heading_names(description)
            for section in options.require_doc_section:
                if section.strip().lower() not in present:
                    report.error(f"{item_scope}: description has no `{section}` section heading")

        check_request_auth(request, item_scope, report)
        check_request_headers(request, item_scope, report)

        body = request.get("body")
        if body is not None:
            for label, pattern in REAL_SECRET_PATTERNS:
                if pattern.search(json.dumps(body)):
                    report.secret(f"{item_scope}: request body contains a literal that looks like a {label}")
                    break

        script_text = script_text_of(events)
        test_script_text = script_text_of(events, "test")
        if script_text.strip():
            report.bump("requests_with_scripts")
        if "pm.test(" in script_text:
            report.bump("requests_with_tests")
        elif options.require_tests:
            report.error(f"{item_scope}: no `pm.test` assertion in any executable script")
        captured = written_variable_names(test_script_text)
        if captured:
            report.bump("requests_with_captures")
        if options.require_correlation_assertion and "X-Request-Id" not in test_script_text:
            report.error(
                f"{item_scope}: tests never reference `X-Request-Id`, so the mandatory correlation header "
                "is unasserted"
            )

        responses = item.get("response", [])
        if responses is not None and not isinstance(responses, list):
            report.error(f"{item_scope}: response must be an array when present")
            responses = []
        responses = responses or []
        report.counts["saved_responses"] += len(responses)

        if options.require_saved_responses and not responses:
            report.error(f"{item_scope}: request has no saved response example")

        success_codes: list[int] = []
        error_codes: list[int] = []
        seen_pairs: set[tuple[Any, str]] = set()
        token_in_success_example = False
        request_method = str(request.get("method", "GET")).upper()
        request_endpoint = endpoint_url(request.get("url"))

        for response_index, response in enumerate(responses):
            response_scope = f"{item_scope}.response[{response_index}]"
            if not isinstance(response, dict):
                report.error(f"{response_scope}: response must be an object")
                continue
            response_name = str(response.get("name") or "")
            if response_name:
                response_scope = f"{item_scope}.response `{response_name}`"
            code = response.get("code")
            if not isinstance(code, int):
                report.error(f"{response_scope}: saved response has no numeric `code`")
            else:
                if 200 <= code < 300:
                    success_codes.append(code)
                elif code >= 400:
                    error_codes.append(code)
                pair = (code, response_name.strip().lower())
                if pair in seen_pairs:
                    report.error(
                        f"{response_scope}: a second example with status {code} and the same name is not "
                        "addressable by `x-mock-response-name`; give it a distinct name"
                    )
                seen_pairs.add(pair)
            if not response_name:
                report.warn(f"{response_scope}: saved example has no name; name it `<status> <condition>`")

            if "body" not in response:
                report.error(f"{response_scope}: saved response has no `body` field")
            body_text = response.get("body")
            if isinstance(body_text, str):
                for label, pattern in REAL_SECRET_PATTERNS:
                    if pattern.search(body_text):
                        report.secret(f"{response_scope}: example body contains a literal that looks like a {label}")
                        break
                if isinstance(code, int) and 200 <= code < 300:
                    if any(token_key in body_text for token_key in TOKEN_BODY_KEYS):
                        token_in_success_example = True

            original_request = response.get("originalRequest")
            if original_request is None:
                report.error(f"{response_scope}: saved response has no `originalRequest`")
            elif isinstance(original_request, dict):
                original_method = str(original_request.get("method", "GET")).upper()
                if original_method != request_method:
                    report.error(
                        f"{response_scope}: originalRequest method `{original_method}` does not match "
                        f"`{request_method}`"
                    )
                original_endpoint = endpoint_url(original_request.get("url"))
                if request_endpoint and original_endpoint != request_endpoint:
                    report.error(f"{response_scope}: originalRequest endpoint does not match the request endpoint")

        if success_codes:
            report.bump("requests_with_success_example")
        elif options.require_success_example:
            report.error(
                f"{item_scope}: no saved example with a 2xx status; a mock server would serve an error "
                "example as its default response"
            )
        if error_codes:
            report.bump("requests_with_error_example")
        if options.require_error_examples > 0 and len(error_codes) < options.require_error_examples:
            report.error(
                f"{item_scope}: {len(error_codes)} error example(s); minimum is "
                f"{options.require_error_examples}"
            )

        if options.require_token_capture and token_in_success_example:
            if not any("token" in captured_name.lower() for captured_name in captured):
                report.error(
                    f"{item_scope}: success example returns a token but no script writes a token variable, "
                    "so the next request needs a manual copy"
                )


def validate_collection(
    collection: dict[str, Any],
    environment_keys: set[str],
    report: Report,
    options: argparse.Namespace,
) -> None:
    collection_variable_keys = collect_collection_variable_keys(collection)
    allow_external = set(options.allow_external_var)
    declared_variables = collection_variable_keys | environment_keys | allow_external

    info = collection.get("info")
    if not isinstance(info, dict):
        report.error("collection: missing `info` object")
    else:
        if not isinstance(info.get("name"), str) or not info["name"].strip():
            report.error("collection.info: missing `name`")
        if not description_text(info.get("description")):
            report.warn("collection.info: no collection description; the environment contract has nowhere to live")
        schema_value = info.get("schema")
        if not isinstance(schema_value, str) or COLLECTION_SCHEMA_HINT not in schema_value:
            report.error("collection.info: expected a Postman Collection Format v2.1 schema URL")
        elif schema_value != CANONICAL_COLLECTION_SCHEMA_URL:
            report.error(
                "collection.info: use the Postman v2.1 export marker "
                f"`{CANONICAL_COLLECTION_SCHEMA_URL}`; Insomnia compares this string exactly and reports "
                "`No importers found for file` for any other value"
            )

    items = collection.get("item")
    if not isinstance(items, list) or not items:
        report.error("collection: missing non-empty `item` array")
    else:
        walk_items(items, "collection", report, options, declared_variables)
        # A collection whose top-level `item` array holds only folders satisfies the check
        # above and contains nothing for any per-request rule to fire on, so every
        # `--require-*` flag passes vacuously. references/70-aggregate-collections-and-
        # consumer-repos.md names two merge-program invariants that produce exactly this
        # artifact, so it is a real failure and not a hypothetical one.
        if report.counts["requests"] == 0:
            report.error(
                "collection: contains folders but no request items, so every `--require-*` flag "
                "passed with nothing to check; fix the collection or the merge program that emitted it"
            )

    top_level_events = collection.get("event", [])
    if isinstance(top_level_events, list):
        validate_events(
            top_level_events,
            "collection",
            report,
            options.require_success_guarded_captures,
            declared_variables,
        )

    referenced = variable_refs(collection)
    for name in sorted(referenced - declared_variables):
        report.error(
            f"collection: variable `{{{{{name}}}}}` is referenced but declared in neither the collection nor "
            "any environment input; declare it or pass --allow-external-var"
        )

    for block in iter_variable_blocks(collection):
        for variable in block:
            if not isinstance(variable, dict):
                continue
            key = variable.get("key") or variable.get("name")
            if not isinstance(key, str):
                continue
            value = variable.get("value")
            sensitive = looks_sensitive_key(key)
            reason = real_secret_reason(value, sensitive)
            if reason:
                report.secret(f"collection.variable `{key}`: carries a {reason}")
            elif sensitive and not is_placeholder(value):
                report.warn(
                    f"collection.variable `{key}`: looks secret-like and its value is not a placeholder"
                )
            if options.forbid_pinned_vendor_identifier:
                report_pinned_vendor_identifier(f"collection.variable `{key}`", key, value, report)
            if "-" in key:
                report.warn(
                    f"collection.variable `{key}`: Insomnia rewrites a hyphenated name into bracket "
                    "notation; use snake_case"
                )


def validate_environment(path: Path, env: Any, report: Report, options: argparse.Namespace) -> None:
    scope = f"environment `{path.name}`"
    if not isinstance(env, dict):
        report.error(f"{scope}: top-level value must be an object")
        return
    if not isinstance(env.get("name"), str) or not env["name"].strip():
        report.warn(f"{scope}: missing or unclear `name`")
    variable_scope = env.get("_postman_variable_scope")
    if variable_scope != "environment":
        report.error(
            f"{scope}: `_postman_variable_scope` must be `\"environment\"`; Insomnia's environment importer "
            f"rejects any other value, and this file has {variable_scope!r}"
        )
    values = env.get("values")
    if not isinstance(values, list):
        report.error(f"{scope}: expected a `values` array in exported Postman environment JSON")
        return
    seen: set[str] = set()
    for index, variable in enumerate(values):
        item_scope = f"{scope}.values[{index}]"
        if not isinstance(variable, dict):
            report.error(f"{item_scope}: value entry must be an object")
            continue
        key = variable.get("key") or variable.get("name")
        if not isinstance(key, str) or not key.strip():
            report.error(f"{item_scope}: missing `key`")
            continue
        item_scope = f"{scope} `{key}`"
        if key in seen:
            report.error(f"{item_scope}: declared more than once; the later value silently wins")
        seen.add(key)
        if "-" in key:
            report.warn(
                f"{item_scope}: Insomnia rewrites a hyphenated name into bracket notation; use snake_case"
            )
        if variable.get("enabled") is False:
            report.warn(
                f"{item_scope}: `enabled` is false, so Insomnia's importer drops it; delete it or give it a "
                "placeholder value"
            )
        value = variable.get("value")
        sensitive = looks_sensitive_key(key)
        reason = real_secret_reason(value, sensitive)
        if reason:
            report.secret(f"{item_scope}: carries a {reason}")
        elif sensitive and not is_placeholder(value):
            report.warn(f"{item_scope}: looks secret-like and its value is not a placeholder")
        if sensitive:
            if variable.get("type") != "secret":
                message = (
                    f"{item_scope}: secret-like variable is not typed `\"type\": \"secret\"`, so Postman "
                    "shows its value in plain text"
                )
                if options.require_secret_typing:
                    report.error(message)
                else:
                    report.warn(message)
        if options.forbid_pinned_vendor_identifier:
            report_pinned_vendor_identifier(item_scope, key, value, report)


def try_schema_validation(collection: dict[str, Any], schema_url: str, report: Report) -> None:
    """Validate against the official schema, recording why the check was skipped if it was.

    A skip is not a pass. `--require-schema` turns any skip into exit 2, so an air-gapped
    CI runner cannot report success while the strongest structural check never ran.
    """
    try:
        import jsonschema
    except ImportError:
        report.schema_skipped = "`jsonschema` is not installed"
        report.warn("schema: skipped official schema validation because `jsonschema` is not installed")
        return
    try:
        with urllib.request.urlopen(schema_url, timeout=20) as response:
            schema = json.load(response)
    except Exception as exc:  # noqa: BLE001
        report.schema_skipped = f"the schema fetch failed: {exc}"
        report.warn(f"schema: skipped official schema validation because schema fetch failed: {exc}")
        return
    try:
        jsonschema.validate(instance=collection, schema=schema)
    except Exception as exc:  # noqa: BLE001
        report.schema_errors.append(f"schema: official Postman v2.1 schema validation failed: {exc}")


def print_section(title: str, findings: list[str], limit: int) -> None:
    if not findings:
        return
    print(f"{title} ({len(findings)}):")
    for finding in findings[:limit]:
        print(f"- {finding}")
    if len(findings) > limit:
        print(f"- ... and {len(findings) - limit} more; raise --max-findings to see them")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate Postman collection and environment artifacts as an implementation contract."
    )
    parser.add_argument("collection", type=Path, help="Path to a Postman collection JSON file")
    parser.add_argument("--env", action="append", default=[], type=Path, help="Path to a Postman environment JSON file")
    parser.add_argument(
        "--allow-external-var",
        action="append",
        default=[],
        help="Variable name intentionally supplied outside the provided collection and environment files",
    )
    parser.add_argument("--skip-schema", action="store_true", help="Skip official schema validation")
    parser.add_argument(
        "--require-schema",
        action="store_true",
        help="Exit 2 when official schema validation could not run; recommended in CI",
    )
    parser.add_argument("--schema-url", default=DEFAULT_SCHEMA_URL, help="Official Postman schema URL")
    parser.add_argument(
        "--forbid-pinned-vendor-identifier",
        action="store_true",
        help="Fail when a committed collection or environment value pins a vendor model or engine identifier",
    )
    parser.add_argument(
        "--min-description-chars",
        type=int,
        default=0,
        help="Require every request description to contain at least this many characters",
    )
    parser.add_argument(
        "--require-saved-responses",
        action="store_true",
        help="Require every request item to include at least one saved response example",
    )
    parser.add_argument(
        "--require-success-example",
        action="store_true",
        help="Require every request item to include a saved example with a 2xx status",
    )
    parser.add_argument(
        "--require-error-examples",
        type=int,
        default=0,
        help="Require every request item to include at least this many saved examples with a 4xx/5xx status",
    )
    parser.add_argument(
        "--require-tests",
        action="store_true",
        help="Require every request item to carry at least one `pm.test` assertion",
    )
    parser.add_argument(
        "--require-correlation-assertion",
        action="store_true",
        help="Require every request item's tests to reference the `X-Request-Id` response header",
    )
    parser.add_argument(
        "--require-token-capture",
        action="store_true",
        help="Require a request whose success example returns a token to write a token variable in a script",
    )
    parser.add_argument(
        "--require-success-guarded-captures",
        action="store_true",
        help="Require response-variable capture scripts to include an explicit HTTP success guard",
    )
    parser.add_argument(
        "--require-doc-section",
        action="append",
        default=[],
        metavar="HEADING",
        help="Require every request description to contain this Markdown heading; repeatable",
    )
    parser.add_argument(
        "--require-secret-typing",
        action="store_true",
        help="Fail when a secret-like environment variable is not typed `\"type\": \"secret\"`",
    )
    parser.add_argument(
        "--max-findings",
        type=int,
        default=200,
        help="Print at most this many findings per section (default: 200)",
    )
    parser.add_argument("--json", action="store_true", help="Write a machine-readable report instead of text")
    return parser


def main() -> int:
    parser = build_parser()
    options = parser.parse_args()

    if options.min_description_chars < 0 or options.require_error_examples < 0 or options.max_findings < 1:
        print("ERROR: --min-description-chars and --require-error-examples must be >= 0, --max-findings >= 1", file=sys.stderr)
        return EXIT_INPUT

    report = Report()

    try:
        collection = load_json(options.collection)
        if not isinstance(collection, dict):
            raise InputError(f"collection `{options.collection}` must contain a JSON object")
        environment_keys: set[str] = set()
        environments: list[tuple[Path, Any]] = []
        for env_path in options.env:
            env = load_json(env_path)
            environments.append((env_path, env))
            if isinstance(env, dict):
                environment_keys.update(extract_environment_keys(env))
    except InputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_INPUT

    for env_path, env in environments:
        validate_environment(env_path, env, report, options)

    validate_collection(collection, environment_keys, report, options)

    if options.skip_schema:
        report.schema_skipped = "`--skip-schema` was passed"
    else:
        try_schema_validation(collection, options.schema_url, report)

    if options.json:
        print(
            json.dumps(
                {
                    "collection": str(options.collection),
                    "environments": [str(path) for path, _ in environments],
                    "counts": report.counts,
                    "secrets": report.secrets,
                    "schema_skipped": report.schema_skipped,
                    "schema_errors": report.schema_errors,
                    "errors": report.errors,
                    "warnings": report.warnings,
                },
                indent=2,
            )
        )
    else:
        print_section("Secret findings", report.secrets, options.max_findings)
        print_section("Schema errors", report.schema_errors, options.max_findings)
        print_section("Errors", report.errors, options.max_findings)
        print_section("Warnings", report.warnings, options.max_findings)
        counts = report.counts
        print(
            "Counts: requests={requests} saved_responses={saved_responses} "
            "with_success_example={requests_with_success_example} "
            "with_error_example={requests_with_error_example} "
            "with_tests={requests_with_tests} with_captures={requests_with_captures}".format(**counts)
        )
        if not (report.secrets or report.schema_errors or report.errors or report.warnings):
            print("Validation passed with no issues.")
        elif not (report.secrets or report.schema_errors or report.errors):
            print("Validation passed with warnings.")

    if options.require_schema and report.schema_skipped:
        print(
            f"ERROR: --require-schema was passed but official schema validation could not run because "
            f"{report.schema_skipped}; the collection was not checked against the official schema",
            file=sys.stderr,
        )
        return EXIT_INPUT
    if report.secrets:
        return EXIT_SECRET
    if report.schema_errors:
        return EXIT_SCHEMA
    if report.errors:
        return EXIT_RULES
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
