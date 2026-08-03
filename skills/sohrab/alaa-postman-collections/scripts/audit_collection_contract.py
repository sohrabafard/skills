#!/usr/bin/env python3
"""Audit Postman v2.1 request documentation, examples, and executable scripts.

Exit codes, documented in references/60-validation-and-output-contract.md:

  0  no findings
  1  at least one finding; every finding this script reports is blocking
  2  could not run: an input file could not be read or is not a JSON object

A "could not run" must never be reported as a failing artifact, because a harness that
cannot tell them apart treats a missing file as a fixable finding and a broken gate as a
broken collection.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


POSTMAN_SCHEMA = "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
DEPRECATED_SCRIPT_RE = re.compile(
    r"\bpostman\.(?:setEnvironmentVariable|getEnvironmentVariable|clearEnvironmentVariable|setNextRequest)\b"
)
VARIABLE_SET_RE = re.compile(
    r"\bpm\.(?:environment|collectionVariables)\.set\(\s*['\"]([^'\"]+)['\"]"
)
VARIABLE_ARRAY_SET_RE = re.compile(
    r"\b(?:setLocal|setVariables|saveVariables)\(\s*\[(?P<body>[^\]]*)\]"
)
QUOTED_NAME_RE = re.compile(r"['\"]([^'\"]+)['\"]")


@dataclass
class Finding:
    severity: str
    request: str
    message: str


@dataclass
class AuditResult:
    label: str
    path: Path
    requests: int = 0
    saved_responses: int = 0
    executable_script_requests: int = 0
    findings: list[Finding] = field(default_factory=list)

    def add(self, severity: str, request: str, message: str) -> None:
        self.findings.append(Finding(severity, request, message))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "collection",
        nargs="+",
        help="Collection path, optionally prefixed with LABEL=.",
    )
    parser.add_argument(
        "--min-description-chars",
        type=int,
        default=120,
        help="Minimum non-whitespace request-description length (default: 120).",
    )
    parser.add_argument(
        "--require-saved-responses",
        action="store_true",
        help="Fail when a request has no attached saved response example.",
    )
    parser.add_argument(
        "--environment",
        type=Path,
        help="Optional Postman environment used to validate variables written by scripts.",
    )
    parser.add_argument(
        "--require-success-guarded-captures",
        action="store_true",
        help="Fail when a response-variable capture script has no explicit HTTP success guard.",
    )
    parser.add_argument(
        "--forbid-description-hint",
        action="append",
        default=[],
        help="Fail when any collection, folder, request, or saved-example description contains this text.",
    )
    parser.add_argument("--json", action="store_true", help="Write a machine-readable report.")
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Suppress individual findings while retaining the failing exit status.",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read Postman JSON `{path}`: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"Postman artifact `{path}` must contain a JSON object")
    return value


def description_text(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict) and isinstance(value.get("content"), str):
        return value["content"].strip()
    return ""


def script_lines(events: Any, listener: str | None = None) -> Iterable[str]:
    if not isinstance(events, list):
        return
    for event in events:
        if not isinstance(event, dict):
            continue
        if listener is not None and event.get("listen") != listener:
            continue
        script = event.get("script")
        lines = script.get("exec") if isinstance(script, dict) else None
        if isinstance(lines, str):
            yield from lines.splitlines()
            continue
        if not isinstance(lines, list):
            continue
        for line in lines:
            if isinstance(line, str):
                yield line


def validate_event_structure(events: Any, scope: str, result: AuditResult) -> None:
    if events in (None, []):
        return
    if not isinstance(events, list):
        result.add("error", scope, "event must be an array")
        return
    listeners: set[str] = set()
    for index, event in enumerate(events):
        event_scope = f"{scope}.event[{index}]"
        if not isinstance(event, dict):
            result.add("error", event_scope, "event must be an object")
            continue
        listener = event.get("listen")
        if listener not in {"prerequest", "test"}:
            result.add("error", event_scope, f"unsupported event listener `{listener}`")
        elif listener in listeners:
            result.add("error", event_scope, f"duplicate `{listener}` listener in the same scope")
        else:
            listeners.add(listener)
        script = event.get("script")
        if not isinstance(script, dict):
            result.add("error", event_scope, "script must be an object")
            continue
        exec_value = script.get("exec")
        if not isinstance(exec_value, list) or not all(isinstance(line, str) for line in exec_value):
            result.add("error", event_scope, "script.exec must be an array of strings")


def request_label(item: dict[str, Any]) -> str:
    request = item.get("request")
    method = str(request.get("method", "GET")).upper() if isinstance(request, dict) else "GET"
    name = str(item.get("name", "unnamed request"))
    return f"{method} {name}"


def raw_url(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict) and isinstance(value.get("raw"), str):
        return value["raw"]
    return ""


def endpoint_url(value: Any) -> str:
    """Return the scheme/host/path identity while allowing saved query variants."""
    return raw_url(value).split("#", 1)[0].split("?", 1)[0]


def walk_request_items(items: Any) -> Iterable[dict[str, Any]]:
    if not isinstance(items, list):
        return
    for item in items:
        if not isinstance(item, dict):
            continue
        if "request" in item:
            yield item
        yield from walk_request_items(item.get("item"))


def walk_non_request_script_scopes(node: Any, scope: str) -> Iterable[tuple[str, Any]]:
    if not isinstance(node, dict):
        return
    if "request" not in node:
        yield scope, node.get("event")
    items = node.get("item")
    if not isinstance(items, list):
        return
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or f"item[{index}]")
        yield from walk_non_request_script_scopes(item, f"{scope}/{name}")


def walk_descriptions(node: Any, scope: str) -> Iterable[tuple[str, str]]:
    if isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk_descriptions(value, f"{scope}[{index}]")
        return
    if not isinstance(node, dict):
        return

    text = description_text(node.get("description"))
    if text:
        yield scope, text
    for key, value in node.items():
        if key != "description":
            yield from walk_descriptions(value, f"{scope}.{key}")


def variable_keys(entries: Any) -> set[str]:
    if not isinstance(entries, list):
        return set()
    return {
        str(entry.get("key") or entry.get("name"))
        for entry in entries
        if isinstance(entry, dict) and (entry.get("key") or entry.get("name"))
    }


def written_variable_names(script_text: str) -> set[str]:
    names = set(VARIABLE_SET_RE.findall(script_text))
    for match in VARIABLE_ARRAY_SET_RE.finditer(script_text):
        names.update(QUOTED_NAME_RE.findall(match.group("body")))
    return names


def is_correlation_variable(name: str) -> bool:
    return name in {"last_request_id", "last_traceparent"} or name.endswith(
        ("_last_request_id", "_last_traceparent")
    )


def audit_collection(
    label: str,
    path: Path,
    minimum_description_chars: int,
    require_saved_responses: bool,
    environment_keys: set[str],
    require_success_guarded_captures: bool,
    forbidden_description_hints: list[str],
) -> AuditResult:
    collection = load_json(path)
    result = AuditResult(label=label, path=path)
    declared_variables = variable_keys(collection.get("variable")) | environment_keys

    info = collection.get("info")
    if not isinstance(info, dict) or info.get("schema") != POSTMAN_SCHEMA:
        result.add("error", "collection", f"info.schema must equal `{POSTMAN_SCHEMA}`")

    normalized_forbidden_hints = [hint.lower() for hint in forbidden_description_hints if hint.strip()]
    for scope, description in walk_descriptions(collection, "collection"):
        lowered = description.lower()
        for hint in normalized_forbidden_hints:
            if hint in lowered:
                result.add("error", scope, f"description contains forbidden hint `{hint}`")

    for item in walk_request_items(collection.get("item")):
        result.requests += 1
        label_text = request_label(item)
        request = item.get("request")
        if not isinstance(request, dict):
            result.add("error", label_text, "request must be an object")
            continue

        description = description_text(request.get("description") or item.get("description"))
        if len(description) < minimum_description_chars:
            result.add(
                "error",
                label_text,
                f"description has {len(description)} characters; minimum is {minimum_description_chars}",
            )

        misplaced_events = request.get("event")
        if isinstance(misplaced_events, list) and misplaced_events:
            result.add(
                "error",
                label_text,
                "scripts are under request.event; Postman v2.1 executes item-level event scripts",
            )

        validate_event_structure(item.get("event"), label_text, result)
        executable_lines = list(script_lines(item.get("event")))
        if executable_lines:
            result.executable_script_requests += 1
        script_text = "\n".join(executable_lines)
        test_script_text = "\n".join(script_lines(item.get("event"), "test"))
        written_variables = written_variable_names(test_script_text)
        guarded_variables = {name for name in written_variables if not is_correlation_variable(name)}
        if require_success_guarded_captures and guarded_variables:
            success_guard_markers = (
                "pm.response.code",
                "pm.response.to.be.success",
                "pm.response.to.have.status",
                "pm.expect(pm.response.code",
            )
            if not any(marker in test_script_text for marker in success_guard_markers):
                result.add(
                    "error",
                    label_text,
                    "response-variable capture has no explicit HTTP success guard",
                )
        for line in executable_lines:
            if DEPRECATED_SCRIPT_RE.search(line):
                result.add("error", label_text, "script uses a deprecated Postman interface")
        for variable_name in sorted(written_variable_names(script_text)):
            if variable_name not in declared_variables:
                result.add(
                    "error",
                    label_text,
                    f"script writes undeclared variable `{variable_name}`",
                )

        responses = item.get("response")
        saved_responses = responses if isinstance(responses, list) else []
        request_method = str(request.get("method", "GET")).upper()
        request_endpoint = endpoint_url(request.get("url"))
        result.saved_responses += len(saved_responses)
        if require_saved_responses and not saved_responses:
            result.add("error", label_text, "request has no attached saved response example")
        for index, response in enumerate(saved_responses, start=1):
            if not isinstance(response, dict):
                result.add("error", label_text, f"saved response {index} must be an object")
                continue
            if not isinstance(response.get("code"), int):
                result.add("error", label_text, f"saved response {index} has no numeric HTTP code")
            original_request = response.get("originalRequest")
            if not isinstance(original_request, dict):
                result.add("error", label_text, f"saved response {index} has no originalRequest")
            else:
                original_method = str(original_request.get("method", "GET")).upper()
                if original_method != request_method:
                    result.add(
                        "error",
                        label_text,
                        f"saved response {index} method `{original_method}` does not match `{request_method}`",
                    )
                original_endpoint = endpoint_url(original_request.get("url"))
                if request_endpoint and original_endpoint != request_endpoint:
                    result.add(
                        "error",
                        label_text,
                        f"saved response {index} originalRequest endpoint does not match the request endpoint",
                    )
            if "body" not in response:
                result.add("error", label_text, f"saved response {index} has no body field")

    for scope, events in walk_non_request_script_scopes(collection, "collection"):
        validate_event_structure(events, scope, result)
        all_script_text = "\n".join(script_lines(events))
        test_script_text = "\n".join(script_lines(events, "test"))
        if DEPRECATED_SCRIPT_RE.search(all_script_text):
            result.add("error", scope, "script uses a deprecated Postman interface")
        for variable_name in sorted(written_variable_names(all_script_text)):
            if variable_name not in declared_variables:
                result.add("error", scope, f"script writes undeclared variable `{variable_name}`")
        guarded_variables = {
            name for name in written_variable_names(test_script_text) if not is_correlation_variable(name)
        }
        if require_success_guarded_captures and guarded_variables:
            success_guard_markers = (
                "pm.response.code",
                "pm.response.to.be.success",
                "pm.response.to.have.status",
                "pm.expect(pm.response.code",
            )
            if not any(marker in test_script_text for marker in success_guard_markers):
                result.add("error", scope, "response-variable capture has no explicit HTTP success guard")

    if result.requests == 0:
        result.add("error", "collection", "collection contains no request items")
    return result


def split_collection_arg(raw: str) -> tuple[str, Path]:
    if "=" in raw:
        label, path = raw.split("=", 1)
        return label, Path(path)
    path = Path(raw)
    return path.stem, path


def main() -> int:
    args = parse_args()
    results: list[AuditResult] = []
    try:
        environment_keys: set[str] = set()
        if args.environment:
            environment = load_json(args.environment)
            environment_keys = variable_keys(environment.get("values"))
        for raw in args.collection:
            label, path = split_collection_arg(raw)
            results.append(
                audit_collection(
                    label,
                    path,
                    args.min_description_chars,
                    args.require_saved_responses,
                    environment_keys,
                    args.require_success_guarded_captures,
                    args.forbid_description_hint,
                )
            )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(
            json.dumps(
                [
                    {
                        "label": result.label,
                        "path": str(result.path),
                        "requests": result.requests,
                        "saved_responses": result.saved_responses,
                        "executable_script_requests": result.executable_script_requests,
                        "findings": [finding.__dict__ for finding in result.findings],
                    }
                    for result in results
                ],
                indent=2,
            )
        )
    else:
        for result in results:
            errors = sum(1 for finding in result.findings if finding.severity == "error")
            print(
                f"{result.label}: requests={result.requests} "
                f"saved_responses={result.saved_responses} "
                f"scripted_requests={result.executable_script_requests} errors={errors}"
            )
            if not args.summary_only:
                for finding in result.findings:
                    print(f"  {finding.severity.upper()}: {finding.request}: {finding.message}")

    return 1 if any(result.findings for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
