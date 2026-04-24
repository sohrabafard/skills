#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import urllib.request
from pathlib import Path
from typing import Any, Iterable

DEFAULT_SCHEMA_URL = "https://schema.getpostman.com/collection/json/v2.1.0/draft-04/collection.json"
CANONICAL_COLLECTION_SCHEMA_URL = "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
COLLECTION_SCHEMA_HINT = "v2.1.0"
VARIABLE_RE = re.compile(r"{{\s*([^{}\s][^{}]*?)\s*}}")
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
)
DEPRECATED_SCRIPT_PATTERNS = (
    "postman.setEnvironmentVariable",
    "postman.clearEnvironmentVariable",
    "postman.setGlobalVariable",
    "postman.clearGlobalVariable",
    "postman.getEnvironmentVariable",
    "postman.getGlobalVariable",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


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
    return any(hint in normalized for hint in PLACEHOLDER_HINTS if hint)


def looks_sensitive_key(name: str) -> bool:
    lowered = name.lower()
    return any(hint in lowered for hint in SECRET_HINTS)


def validate_events(events: list[Any], scope: str, errors: list[str], warnings: list[str]) -> None:
    for index, event in enumerate(events):
        event_scope = f"{scope}.event[{index}]"
        if not isinstance(event, dict):
            errors.append(f"{event_scope}: event must be an object")
            continue
        listen = event.get("listen")
        if listen not in {"prerequest", "test"}:
            warnings.append(f"{event_scope}: unexpected event listener `{listen}`")
        script = event.get("script")
        if script is None:
            continue
        if not isinstance(script, dict):
            errors.append(f"{event_scope}: script must be an object")
            continue
        exec_value = script.get("exec")
        if exec_value is not None and not isinstance(exec_value, (list, str)):
            errors.append(f"{event_scope}: script.exec must be a string or array of lines")
            continue

        script_text = ""
        if isinstance(exec_value, list):
            if not all(isinstance(line, str) for line in exec_value):
                errors.append(f"{event_scope}: script.exec array must contain only strings")
                continue
            script_text = "\n".join(exec_value)
        elif isinstance(exec_value, str):
            script_text = exec_value

        for pattern in DEPRECATED_SCRIPT_PATTERNS:
            if pattern in script_text:
                warnings.append(f"{event_scope}: deprecated Postman script API `{pattern}` reduces portability")


def walk_items(items: Any, scope: str, errors: list[str], warnings: list[str]) -> None:
    if not isinstance(items, list):
        errors.append(f"{scope}: `item` must be an array")
        return

    for index, item in enumerate(items):
        item_scope = f"{scope}.item[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{item_scope}: item must be an object")
            continue

        name = item.get("name")
        if not isinstance(name, str) or not name.strip():
            warnings.append(f"{item_scope}: item is missing a clear name")

        request = item.get("request")
        child_items = item.get("item")
        if request is None and child_items is None:
            errors.append(f"{item_scope}: item must contain either `request` or nested `item`")

        if child_items is not None:
            walk_items(child_items, item_scope, errors, warnings)

        if request is not None and not isinstance(request, (dict, str)):
            errors.append(f"{item_scope}: request must be an object or URL string")

        responses = item.get("response", [])
        if responses is not None and not isinstance(responses, list):
            errors.append(f"{item_scope}: response must be an array when present")
        elif isinstance(responses, list):
            for response_index, response in enumerate(responses):
                response_scope = f"{item_scope}.response[{response_index}]"
                if not isinstance(response, dict):
                    errors.append(f"{response_scope}: response must be an object")
                    continue
                if "originalRequest" not in response:
                    warnings.append(f"{response_scope}: saved response is missing `originalRequest`")
                if "code" not in response:
                    warnings.append(f"{response_scope}: saved response is missing `code`")

        events = item.get("event", [])
        if events is not None and not isinstance(events, list):
            errors.append(f"{item_scope}: event must be an array when present")
        elif isinstance(events, list):
            validate_events(events, item_scope, errors, warnings)


def validate_collection(
    collection: dict[str, Any],
    environment_keys: set[str],
    allow_external: set[str],
    errors: list[str],
    warnings: list[str],
) -> None:
    info = collection.get("info")
    if not isinstance(info, dict):
        errors.append("collection: missing `info` object")
    else:
        if not isinstance(info.get("name"), str) or not info["name"].strip():
            errors.append("collection.info: missing `name`")
        schema_value = info.get("schema")
        if not isinstance(schema_value, str) or COLLECTION_SCHEMA_HINT not in schema_value:
            errors.append("collection.info: expected a Postman Collection Format v2.1 schema URL")
        elif schema_value != CANONICAL_COLLECTION_SCHEMA_URL:
            errors.append(
                "collection.info: use the Postman v2.1 export marker "
                f"`{CANONICAL_COLLECTION_SCHEMA_URL}` so Insomnia can detect the Postman importer"
            )

    items = collection.get("item")
    if not isinstance(items, list) or not items:
        errors.append("collection: missing non-empty `item` array")
    else:
        walk_items(items, "collection", errors, warnings)

    top_level_events = collection.get("event", [])
    if top_level_events is not None and isinstance(top_level_events, list):
        validate_events(top_level_events, "collection", errors, warnings)

    collection_variable_keys = collect_collection_variable_keys(collection)
    referenced = variable_refs(collection)
    missing = sorted(referenced - collection_variable_keys - environment_keys - allow_external)
    for name in missing:
        warnings.append(f"collection: variable `{{{{{name}}}}}` is referenced but not defined in collection/env inputs")

    for block in iter_variable_blocks(collection):
        for variable in block:
            if not isinstance(variable, dict):
                continue
            key = variable.get("key") or variable.get("name")
            value = variable.get("value")
            if isinstance(key, str) and looks_sensitive_key(key) and not is_placeholder(value):
                warnings.append(
                    f"collection.variable: `{key}` looks secret-like and does not look like a placeholder"
                )


def validate_environment(path: Path, env: Any, errors: list[str], warnings: list[str]) -> None:
    scope = f"environment `{path.name}`"
    if not isinstance(env, dict):
        errors.append(f"{scope}: top-level value must be an object")
        return
    name = env.get("name")
    if not isinstance(name, str) or not name.strip():
        warnings.append(f"{scope}: missing or unclear `name`")
    values = env.get("values")
    if not isinstance(values, list):
        warnings.append(f"{scope}: expected a `values` array in exported Postman environment JSON")
        return
    for index, variable in enumerate(values):
        item_scope = f"{scope}.values[{index}]"
        if not isinstance(variable, dict):
            errors.append(f"{item_scope}: value entry must be an object")
            continue
        key = variable.get("key") or variable.get("name")
        if not isinstance(key, str) or not key.strip():
            errors.append(f"{item_scope}: missing `key`")
            continue
        value = variable.get("value")
        if looks_sensitive_key(key) and not is_placeholder(value):
            warnings.append(f"{item_scope}: `{key}` looks secret-like and does not look like a placeholder")


def try_schema_validation(collection: dict[str, Any], schema_url: str, warnings: list[str], errors: list[str]) -> None:
    try:
        import jsonschema
    except ImportError:
        warnings.append("schema: skipped official schema validation because `jsonschema` is not installed")
        return

    try:
        with urllib.request.urlopen(schema_url, timeout=20) as response:
            schema = json.load(response)
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"schema: skipped official schema validation because schema fetch failed: {exc}")
        return

    try:
        jsonschema.validate(instance=collection, schema=schema)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"schema: official Postman schema validation failed: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Postman collection and environment artifacts with light portability checks."
    )
    parser.add_argument("collection", type=Path, help="Path to a Postman collection JSON file")
    parser.add_argument("--env", action="append", default=[], type=Path, help="Path to a Postman environment JSON file")
    parser.add_argument(
        "--allow-external-var",
        action="append",
        default=[],
        help="Variable name that is intentionally external to the provided collection and environment files",
    )
    parser.add_argument("--skip-schema", action="store_true", help="Skip official schema validation")
    parser.add_argument("--schema-url", default=DEFAULT_SCHEMA_URL, help="Official Postman schema URL")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    try:
        collection = load_json(args.collection)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: failed to read collection `{args.collection}`: {exc}")
        return 1

    if not isinstance(collection, dict):
        print("ERROR: collection JSON must be an object")
        return 1

    environment_keys: set[str] = set()
    for env_path in args.env:
        try:
            env = load_json(env_path)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"environment `{env_path.name}`: failed to read JSON: {exc}")
            continue
        validate_environment(env_path, env, errors, warnings)
        if isinstance(env, dict):
            environment_keys.update(extract_environment_keys(env))

    validate_collection(collection, environment_keys, set(args.allow_external_var), errors, warnings)

    if not args.skip_schema:
        try_schema_validation(collection, args.schema_url, warnings, errors)

    if errors:
        print("Errors:")
        for error in errors:
            print(f"- {error}")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")

    if not errors and not warnings:
        print("Validation passed with no issues.")
    elif not errors:
        print("Validation passed with warnings.")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
