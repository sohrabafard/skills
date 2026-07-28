#!/usr/bin/env python3
"""Deterministic checks on the Ala gateway trust boundary.

Four checks, each answering a question that prose cannot answer reliably:

  sanitize   Does every header the gateway injects also carry an unconditional
             request-side delete in the same file and section, so no
             client-supplied copy can survive to the backend?
  bitmap     Does a permission-bitmap decoder agree with the oracle on the
             least-significant-bit-first, unpadded-base64url contract?
  reads      Does this service read only trusted headers that are on the frozen
             list, and no others?
  bypass     Is an authentication or step-up bypass switch truthy in a
             non-local environment file without a recorded decision beside it?

Standard library only. No network access. No file is modified.

The bitmap contract itself is owned by `alaa-permission-generator`, which emits
the decoders for PHP, Go and TypeScript and ships the canonical conformance
corpus and the harness that drives every emitted decoder over it. The oracle in
this file is deliberately small and exists to prove that one reader of trusted
context agrees with the contract. It does not define the contract, and a
disagreement between this oracle and the generator's corpus is resolved in the
generator's favour.
"""

from __future__ import annotations

import argparse
import base64
import os
import re
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_FINDING = 1
EXIT_USAGE = 2
EXIT_NOT_RUN = 3

# ---------------------------------------------------------------------------
# Bitmap oracle
# ---------------------------------------------------------------------------

_B64URL_ALPHABET = re.compile(r"^[A-Za-z0-9_-]+$")


class BitmapError(ValueError):
    """The value is not a usable permission bitmap."""


def decode_bitmap(value: str, max_permission_id: int) -> list[int]:
    """Decode an ``X-Access`` bitmap into the permission ids it sets.

    Ids are 1-based, ``bit_index`` equals ``id - 1``, bits are packed
    least-significant-bit first within each byte, and the bytes are encoded as
    unpadded base64url. An id above ``max_permission_id`` is ignored rather than
    treated as an error, because the bitmap is issued against the whole platform
    catalog while a service knows only its own subset.

    Raises BitmapError for empty input, padded input, an impossible length, or a
    character outside the base64url alphabet.
    """
    if max_permission_id < 1:
        raise ValueError("max_permission_id must be at least 1")
    if value == "":
        raise BitmapError("empty value")
    if "=" in value:
        raise BitmapError("padded value; the contract is unpadded base64url")
    if not _B64URL_ALPHABET.match(value):
        raise BitmapError("character outside the base64url alphabet")
    if len(value) % 4 == 1:
        raise BitmapError("impossible base64url length")
    raw = base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))
    ids: list[int] = []
    for byte_index, byte in enumerate(raw):
        if byte == 0:
            continue
        for bit_index in range(8):
            if byte & (1 << bit_index):
                permission_id = byte_index * 8 + bit_index + 1
                if permission_id <= max_permission_id:
                    ids.append(permission_id)
    return ids


def encode_bitmap(ids: list[int], max_permission_id: int) -> str:
    """Encode permission ids under the same contract. Used by the self-test."""
    byte_count = (max_permission_id + 7) // 8
    raw = bytearray(byte_count)
    for permission_id in ids:
        if 1 <= permission_id <= max_permission_id:
            index = permission_id - 1
            raw[index // 8] |= 1 << (index % 8)
    return base64.urlsafe_b64encode(bytes(raw)).decode().rstrip("=")


# Vectors verified against the live catalog and the gateway contract on
# 2026-07-27. Ids 92-95 are the tusd upload-intake permissions.
BITMAP_VECTORS: list[tuple[str, int, list[int]]] = [
    ("AAAAAAAAAAAAAAAI", 95, [92]),
    ("AAAAAAAAAAAAAAAQ", 95, [93]),
    ("AAAAAAAAAAAAAAAg", 95, [94]),
    ("AAAAAAAAAAAAAABA", 95, [95]),
    ("AAAAAAAAAAAAAAB4", 95, [92, 93, 94, 95]),
    # A bitmap wider than the service's own maximum decodes; it does not fail.
    ("AAAAAAAAAAAAAAB4", 40, []),
    # Bit-order proof at the first byte boundary.
    ("AQA", 16, [1]),
    ("gAA", 16, [8]),
    ("AAE", 16, [9]),
]

BITMAP_REJECTIONS: list[tuple[str, str]] = [
    ("", "empty input"),
    ("AAAA=", "padded input"),
    ("AAAAA", "impossible base64url length"),
    ("AA*A", "character outside the base64url alphabet"),
]

BITMAP_ENCODINGS: list[tuple[list[int], int, str]] = [
    ([1], 16, "AQA"),
    ([8], 16, "gAA"),
    ([9], 16, "AAE"),
    ([92, 93, 94, 95], 95, "AAAAAAAAAAAAAAB4"),
]


def check_bitmap(values: list[str], max_permission_id: int) -> tuple[list[str], list[str]]:
    """Decode caller-supplied bitmaps and report the result."""
    findings: list[str] = []
    notes: list[str] = []
    for value in values:
        try:
            ids = decode_bitmap(value, max_permission_id)
        except BitmapError as exc:
            findings.append(
                f"bitmap: {value!r} is not a usable bitmap ({exc}); the trusted-context "
                f"normalizer rejects it with AUTH_ACCESS_BITMAP_INVALID"
            )
            continue
        if not ids:
            findings.append(
                f"bitmap: {value!r} resolves to zero permission ids at or below "
                f"{max_permission_id}; a protected request carrying it is rejected with "
                f"AUTH_ACCESS_BITMAP_INVALID rather than allowed with an empty permission set"
            )
            continue
        notes.append(f"bitmap: {value!r} -> ids {ids}")
    return findings, notes


# ---------------------------------------------------------------------------
# Sanitize / inject symmetry
# ---------------------------------------------------------------------------

_SET_HEADER = re.compile(r"\b(?:set-header|add-header)\s+([A-Za-z0-9_\-]+|\{\{[^}]*\}\})")
_DEL_HEADER = re.compile(r"\bdel-header\s+([A-Za-z0-9_\-]+|\{\{[^}]*\}\})")
_YAML_ITEM = re.compile(r"^(\s*)-\s*([A-Za-z][A-Za-z0-9_\-]*)\s*$")
_YAML_KEY = re.compile(r"^(\s*)([A-Za-z_][A-Za-z0-9_\-]*)\s*:\s*(.*?)\s*$")
_TEMPLATE_PATH = re.compile(r"\.Values((?:\.[A-Za-z0-9_]+)+)")
_TEMPLATE_VAR = re.compile(r"\{\{-?\s*(\$[A-Za-z0-9_]+|\.)\s*(?:\|[^}]*)?-?\}\}")
_RANGE = re.compile(r"range\s+(?:(\$[A-Za-z0-9_]+)\s*,\s*)?(\$[A-Za-z0-9_]+)?\s*:?=?\s*\$?\.Values((?:\.[A-Za-z0-9_]+)+)")
_END = re.compile(r"\{\{-?\s*end\s*-?\}\}")
# An HAProxy section start. The colon guard keeps YAML keys such as
# `defaults:` in a values file from opening a section.
_SECTION = re.compile(r"^\s*(frontend|backend|listen|defaults)\b(?!\s*:)\s*(\S*)")
# The ACL tail of an http-request rule: everything from ` if ` or ` unless `.
_CONDITION = re.compile(r"\s(if|unless)\s+(\S.*)$")


def load_values(text: str) -> dict[str, object]:
    """Flatten a values file into dotted-path -> scalar or list of scalars.

    This is deliberately not a YAML parser. It exists so a templated header name
    such as `{{ .Values.totpProof.trustedHeaders.purpose }}` or a name produced
    by `range ... := .Values.jwt.claimsToHeaders` can be resolved to the literal
    header that renders there, which is all the sanitize check needs.
    """
    values: dict[str, object] = {}
    stack: list[tuple[int, str]] = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        item = _YAML_ITEM.match(raw)
        if item and stack:
            path = ".".join(k for _, k in stack)
            bucket = values.setdefault(path, [])
            if isinstance(bucket, list):
                bucket.append(item.group(2))
            continue
        match = _YAML_KEY.match(raw)
        if not match:
            continue
        indent, key, scalar = len(match.group(1)), match.group(2), match.group(3)
        while stack and stack[-1][0] >= indent:
            stack.pop()
        path = ".".join([k for _, k in stack] + [key])
        if scalar and scalar[0] not in "|>{[#":
            values[path] = scalar.strip().strip('"').strip("'")
        else:
            stack.append((indent, key))
    return values


def _children(values: dict[str, object], path: str) -> list[str]:
    """Every scalar leaf directly or indirectly under a values path."""
    found: list[str] = []
    direct = values.get(path)
    if isinstance(direct, list):
        found.extend(direct)
    elif isinstance(direct, str):
        found.append(direct)
    prefix = path + "."
    for key, value in values.items():
        if key.startswith(prefix) and isinstance(value, str):
            found.append(value)
    return [f for f in found if f]


def resolve_header_token(
    token: str,
    values: dict[str, object] | None = None,
    bindings: dict[str, list[str]] | None = None,
) -> list[str]:
    """Resolve one header token to the literal header keys it can render as.

    Returns lowercase keys. A token that cannot be resolved returns a single key
    prefixed `unresolved:`, which the caller reports as a check that could not
    run rather than as a defect, because an unresolved name is not evidence of
    a missing delete.
    """
    token = token.strip()
    if not token.startswith("{{"):
        return [token.lower()]
    variable = _TEMPLATE_VAR.match(token)
    if variable and bindings:
        bound = bindings.get(variable.group(1))
        if bound:
            return [name.lower() for name in bound]
    path = _TEMPLATE_PATH.search(token)
    if path and values:
        resolved = _children(values, path.group(1).lstrip("."))
        if resolved:
            return [name.lower() for name in resolved]
    default = re.search(r'default\s+"([^"]+)"', token)
    if default:
        return [default.group(1).lower()]
    return ["unresolved:" + token]


def scan_sanitize(text: str, values: dict[str, object] | None = None) -> dict[str, object]:
    """Scan one config text for injected and deleted request headers.

    Returns a dict with:
      injected              key -> set of section labels where it is set
      deleted               key -> set of section labels holding an
                            UNCONDITIONAL request-side delete
      deleted_conditional   key -> list of (section, condition) for deletes
                            guarded by `if`/`unless`
      display               key -> printable form

    Only request-side mutation is in scope. A header set by `http-response` or
    `http-after-response` travels to the client and cannot be a spoofing surface
    for a backend, so it is not a finding here. For the same reason a
    response-side delete proves nothing about client input and is not recorded.

    A delete guarded by a condition is recorded separately and never counts as
    protection: when the condition does not hold, the client-supplied value
    passes through untouched, whatever the injection's own condition says.
    """
    injected: dict[str, set[str]] = {}
    deleted: dict[str, set[str]] = {}
    deleted_conditional: dict[str, list[tuple[str, str]]] = {}
    display: dict[str, str] = {}
    defaults_of: dict[str, str | None] = {}
    scopes: list[dict[str, list[str]]] = []
    section = ""
    current_defaults: str | None = None
    anonymous_defaults = 0

    def bindings() -> dict[str, list[str]]:
        merged: dict[str, list[str]] = {}
        for scope in scopes:
            merged.update(scope)
        return merged

    def keys_of(token: str) -> list[str]:
        resolved = resolve_header_token(token, values, bindings())
        for key in resolved:
            display.setdefault(key, token.strip() if key.startswith("unresolved:") else key)
        return resolved

    for raw_line in text.splitlines():
        loop = _RANGE.search(raw_line)
        if loop:
            names = _children(values or {}, loop.group(3).lstrip("."))
            scope: dict[str, list[str]] = {}
            if loop.group(2):
                scope[loop.group(2)] = names
            else:
                scope["."] = names
            scopes.append(scope)
        elif _END.search(raw_line) and scopes:
            scopes.pop()

        line = raw_line.split("#", 1)[0]
        opened = _SECTION.match(line)
        if opened:
            kind, name = opened.group(1), opened.group(2)
            if kind == "defaults":
                # Rules in a defaults section apply only to the proxies
                # associated with it - by `from <name>` or by being the
                # nearest preceding defaults - never to the whole file.
                if name:
                    section = f"defaults {name}"
                else:
                    anonymous_defaults += 1
                    section = f"defaults @{anonymous_defaults}"
                current_defaults = section
            else:
                section = f"{kind} {name}".strip()
                explicit = re.search(r"\bfrom\s+(\S+)", line[opened.end():])
                defaults_of[section] = (
                    f"defaults {explicit.group(1)}" if explicit else current_defaults
                )
        if "-response" not in line:
            for token in _SET_HEADER.findall(line):
                for key in keys_of(token):
                    injected.setdefault(key, set()).add(section)
            for match in _DEL_HEADER.finditer(line):
                condition = _CONDITION.search(line[match.end():])
                for key in keys_of(match.group(1)):
                    if condition:
                        deleted_conditional.setdefault(key, []).append(
                            (section, condition.group(0).strip())
                        )
                    else:
                        deleted.setdefault(key, set()).add(section)
        item = _YAML_ITEM.match(raw_line)
        if item and item.group(2).lower().startswith("x-"):
            for key in keys_of(item.group(2)):
                deleted.setdefault(key, set()).add(section)
    return {
        "injected": injected,
        "deleted": deleted,
        "deleted_conditional": deleted_conditional,
        "display": display,
        "defaults_of": defaults_of,
    }


# A header the gateway injects for tracing rather than for trust. Injecting one
# of these without deleting the inbound copy is a deliberate pass-through, not a
# spoofing surface, because no service takes an authorization decision from it.
_TRACE_HEADERS = {"x-request-id", "x-request-ip", "traceparent", "tracestate", "baggage",
                  "x-forwarded-proto", "x-forwarded-for", "x-forwarded-host", "x-forwarded-port",
                  "x-forwarded-prefix", "x-real-ip"}


def _evaluate_sanitize(
    scans: list[tuple[str, dict[str, object]]],
    resolved_values: int = 0,
) -> tuple[list[str], list[str], list[str]]:
    """Judge scan results. Protection is never borrowed across files or sections.

    An injected header is protected only by an unconditional request-side delete
    in the same file, in the same section or in a `defaults` section of that
    file. A conditional delete, a delete in another section, or a delete in
    another file each produce a finding that names what is missing, because none
    of them proves the client-supplied value is removed on the injecting route.
    """
    findings: list[str] = []
    notes: list[str] = []
    not_run: list[str] = []

    uncond_elsewhere: dict[str, list[str]] = {}
    injected_keys: set[str] = set()
    deleted_keys: set[str] = set()
    for label, scan in scans:
        for key in scan["deleted"]:
            uncond_elsewhere.setdefault(key, []).append(label)
        injected_keys |= set(scan["injected"])
        deleted_keys |= set(scan["deleted"]) | set(scan["deleted_conditional"])
    notes.append(
        f"sanitize: {len(injected_keys)} injected request-header names, "
        f"{len(deleted_keys)} deleted header names, "
        f"{resolved_values} template values resolved"
    )

    for label, scan in scans:
        display = scan["display"]
        for key in sorted(scan["injected"]):
            if key in _TRACE_HEADERS:
                continue
            if key.startswith("unresolved:"):
                not_run.append(
                    f"sanitize: {display.get(key, key)} could not be resolved to a literal header "
                    f"name; pass the values file that defines it, then re-run"
                )
                continue
            name = display.get(key, key)
            del_sections = scan["deleted"].get(key, set())
            defaults_of = scan.get("defaults_of", {})

            def covered(section: str) -> bool:
                if section in del_sections:
                    return True
                # A delete in a defaults section protects only the proxies
                # associated with THAT defaults section (by `from <name>` or
                # by nearest-preceding order), never every section in the file.
                associated = defaults_of.get(section)
                return associated is not None and associated in del_sections

            uncovered = sorted(s for s in scan["injected"][key] if not covered(s))
            if not uncovered:
                continue
            conditional = scan["deleted_conditional"].get(key, [])
            other_files = [f for f in uncond_elsewhere.get(key, []) if f != label]
            where = f" in {label}" if len(scans) > 1 else ""
            if conditional:
                conds = "; ".join(sorted({c for _, c in conditional}))
                findings.append(
                    f"sanitize: {name} is injected{where} but its only request-side delete is "
                    f"conditional ({conds}); when the condition does not hold, the client-supplied "
                    f"value passes through untouched, so a conditional delete is not sanitization. "
                    f"Delete it unconditionally on the injecting route"
                )
            elif del_sections:
                findings.append(
                    f"sanitize: {name} is injected in section "
                    f"{', '.join(repr(s) for s in uncovered)}{where} but deleted only in "
                    f"{', '.join(sorted(repr(s) for s in del_sections))}; a delete in another "
                    f"section does not run on the injecting route. Delete it in the same section "
                    f"or in the defaults section that section is associated with"
                )
            elif other_files:
                findings.append(
                    f"sanitize: {name} is injected{where} but its only unconditional delete is in "
                    f"{', '.join(sorted(other_files))}; nothing proves both apply to the same "
                    f"rendered configuration, so an unrelated file cannot stand in for the missing "
                    f"delete. Keep the delete beside the injection, or pass one combined config"
                )
            else:
                findings.append(
                    f"sanitize: {name} is injected{where} but never deleted from client input; "
                    f"a public client can forge it and a service reading it cannot tell the difference"
                )
    return findings, notes, not_run


def check_sanitize(paths: list[Path]) -> tuple[list[str], list[str], list[str]]:
    texts = [(path, path.read_text(encoding="utf-8", errors="replace")) for path in paths]
    values: dict[str, object] = {}
    for _, text in texts:
        values.update(load_values(text))
    scans = [(str(path), scan_sanitize(text, values)) for path, text in texts]
    return _evaluate_sanitize(scans, resolved_values=len(values))


# ---------------------------------------------------------------------------
# Undeclared trusted-header read
# ---------------------------------------------------------------------------

_HEADER_READ = re.compile(
    r"""["'`](X-[A-Za-z0-9\-]{2,})["'`]""",
    re.IGNORECASE,
)

_SOURCE_SUFFIXES = {".php", ".go", ".ts", ".js", ".py", ".rb", ".java", ".kt", ".lua", ".vue"}


def load_allowlist(path: Path) -> set[str]:
    """Read the frozen trusted-header list.

    The list itself is owned by `alaa-services-contract`; pass its file so this
    check never carries a second copy that can drift.
    """
    names: set[str] = set()
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        for token in re.findall(r"X-[A-Za-z0-9\-]{2,}", line, re.IGNORECASE):
            names.add(token.lower())
    return names


def check_reads(roots: list[Path], allowed: set[str]) -> tuple[list[str], list[str]]:
    findings: list[str] = []
    notes: list[str] = []
    seen: dict[str, str] = {}
    scanned = 0
    for root in roots:
        files = [root] if root.is_file() else [
            p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in _SOURCE_SUFFIXES
        ]
        for path in files:
            scanned += 1
            for line_no, line in enumerate(
                path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1
            ):
                for token in _HEADER_READ.findall(line):
                    key = token.lower()
                    if key in allowed or key in _TRACE_HEADERS:
                        continue
                    seen.setdefault(key, f"{path}:{line_no}")
    notes.append(f"reads: scanned {scanned} source files against {len(allowed)} allowed header names")
    for key, where in sorted(seen.items()):
        findings.append(
            f"reads: {key} is read at {where} and is not on the frozen trusted-header list, so "
            f"the gateway does not delete an inbound copy and a public client can set it. Either "
            f"prove the read treats it as untrusted client metadata, or add the name to the frozen "
            f"list through alaa-services-contract and to the gateway sanitize list, in that order"
        )
    return findings, notes


# ---------------------------------------------------------------------------
# Bypass-switch audit
# ---------------------------------------------------------------------------

_BYPASS_KEY = re.compile(
    r"^\s*(?:export\s+)?([A-Z0-9_]*(?:BYPASS|SKIP_AUTH|DISABLE_AUTH|NO_AUTH|INSECURE|ALLOW_UNVERIFIED)[A-Z0-9_]*)\s*[=:]\s*(.+?)\s*$"
)
_TRUTHY = {"1", "true", "yes", "on", "enabled"}
_DECISION = re.compile(r"decision", re.IGNORECASE)
_LOCAL_HINT = re.compile(r"(^|[^a-z])(local|dev|development|test|testing|example|sample)([^a-z]|$)", re.IGNORECASE)


def check_bypass(paths: list[Path]) -> tuple[list[str], list[str]]:
    findings: list[str] = []
    notes: list[str] = []
    inspected = 0
    for path in paths:
        files = [path] if path.is_file() else [p for p in path.rglob("*") if p.is_file()]
        for env_file in files:
            name = env_file.name.lower()
            if not (name.startswith(".env") or name.endswith(".env") or name.endswith(".envrc")):
                continue
            inspected += 1
            local = bool(_LOCAL_HINT.search(name))
            lines = env_file.read_text(encoding="utf-8", errors="replace").splitlines()
            for index, line in enumerate(lines):
                match = _BYPASS_KEY.match(line)
                if not match:
                    continue
                key, value = match.group(1), match.group(2).strip().strip('"').strip("'").lower()
                if value not in _TRUTHY:
                    continue
                context = "\n".join(lines[max(0, index - 3):index])
                if _DECISION.search(context):
                    notes.append(f"bypass: {env_file}:{index + 1} {key} is truthy with a recorded decision above it")
                    continue
                if local:
                    notes.append(f"bypass: {env_file}:{index + 1} {key} is truthy in a file named as local or test")
                    continue
                findings.append(
                    f"bypass: {env_file}:{index + 1} sets {key} truthy in a non-local environment file "
                    f"with no recorded decision naming the compensating control, the verifier and the "
                    f"date; this is a /alaa-security-review trigger"
                )
    notes.append(f"bypass: inspected {inspected} environment files")
    return findings, notes


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

_SANITIZE_FIXTURE_CLEAN = """
    http-request del-header X-User-Id
    http-request del-header X-Access
    http-request set-header X-User-Id %[var(txn.sub)]
    http-request set-header X-Access %[var(txn.prm)]
    http-request set-header X-Request-Id %[uuid()]
"""

_SANITIZE_FIXTURE_BROKEN = """
    http-request del-header X-User-Id
    http-request set-header X-User-Id %[var(txn.sub)]
    http-request set-header X-User-Roles %[var(txn.rol)]
"""

# A conditional delete must not count as protection for an injection: when the
# condition is false, the client-supplied value passes through untouched.
_SANITIZE_FIXTURE_CONDITIONAL = """
    http-request del-header X-User-Id if is_admin
    http-request set-header X-User-Id %[var(txn.sub)]
"""

# A response-side delete says nothing about client input on the request path.
_SANITIZE_FIXTURE_RESPONSE_DELETE = """
    http-response del-header X-User-Id
    http-request set-header X-User-Id %[var(txn.sub)]
"""

# A delete in one section does not run on a route handled by another.
_SANITIZE_FIXTURE_SECTION_MISMATCH = """
frontend fe_public
    http-request del-header X-User-Id
frontend fe_other
    http-request set-header X-User-Id %[var(txn.sub)]
"""

# A delete in a defaults section applies to the proxies associated with it.
_SANITIZE_FIXTURE_DEFAULTS_DELETE = """
defaults
    http-request del-header X-User-Id
frontend fe_public
    http-request set-header X-User-Id %[var(txn.sub)]
"""

# A delete in one named defaults does not protect a proxy associated with a
# DIFFERENT defaults section.
_SANITIZE_FIXTURE_DEFAULTS_MISMATCH = """
defaults sanitized
    http-request del-header X-User-Id
defaults unsanitized
frontend fe_public
    http-request set-header X-User-Id %[var(txn.sub)]
"""

# An explicit `from <name>` association wins over the preceding defaults.
_SANITIZE_FIXTURE_DEFAULTS_FROM = """
defaults sanitized
    http-request del-header X-User-Id
defaults unsanitized
frontend fe_public from sanitized
    http-request set-header X-User-Id %[var(txn.sub)]
"""

# Split across two unrelated files, the same two lines prove nothing together.
_SANITIZE_FIXTURE_FILE_A_INJECT = """
    http-request set-header X-User-Id %[var(txn.sub)]
"""

_SANITIZE_FIXTURE_FILE_B_DELETE = """
    http-request del-header X-User-Id
"""


def _sanitize_findings(*texts: str) -> list[str]:
    scans = [(f"fixture-{index}", scan_sanitize(text)) for index, text in enumerate(texts)]
    findings, _, _ = _evaluate_sanitize(scans)
    return findings


def self_test() -> int:
    failures: list[str] = []
    checks = 0

    for value, maximum, expected in BITMAP_VECTORS:
        checks += 1
        try:
            got = decode_bitmap(value, maximum)
        except BitmapError as exc:
            failures.append(f"decode({value!r}, {maximum}) raised {exc}; expected {expected}")
            continue
        if got != expected:
            failures.append(f"decode({value!r}, {maximum}) = {got}; expected {expected}")

    for value, why in BITMAP_REJECTIONS:
        checks += 1
        try:
            decode_bitmap(value, 95)
        except BitmapError:
            continue
        failures.append(f"decode({value!r}, 95) was accepted; it must be rejected ({why})")

    for ids, maximum, expected in BITMAP_ENCODINGS:
        checks += 1
        got = encode_bitmap(ids, maximum)
        if got != expected:
            failures.append(f"encode({ids}, {maximum}) = {got!r}; expected {expected!r}")

    checks += 1
    if encode_bitmap([1], 16) == "gAA":
        failures.append("encode([1], 16) produced gAA; that decoder is most-significant-bit-first and is wrong")

    checks += 1
    if _sanitize_findings(_SANITIZE_FIXTURE_CLEAN):
        failures.append(
            f"clean sanitize fixture reported a finding: {_sanitize_findings(_SANITIZE_FIXTURE_CLEAN)}"
        )

    checks += 1
    broken = _sanitize_findings(_SANITIZE_FIXTURE_BROKEN)
    if not any("x-user-roles" in finding for finding in broken):
        failures.append("broken sanitize fixture did not report the injected-but-undeleted header")

    checks += 1
    conditional = _sanitize_findings(_SANITIZE_FIXTURE_CONDITIONAL)
    if not any("x-user-id" in f and "conditional" in f for f in conditional):
        failures.append(
            "a conditional delete was accepted as protection for an unconditional injection"
        )

    checks += 1
    if not any("x-user-id" in f for f in _sanitize_findings(_SANITIZE_FIXTURE_RESPONSE_DELETE)):
        failures.append("a response-side delete was accepted as protection for a request injection")

    checks += 1
    if not any("x-user-id" in f for f in _sanitize_findings(_SANITIZE_FIXTURE_SECTION_MISMATCH)):
        failures.append("a delete in an unrelated section was accepted as protection")

    checks += 1
    if _sanitize_findings(_SANITIZE_FIXTURE_DEFAULTS_DELETE):
        failures.append("a preceding-defaults delete did not protect its associated proxy")

    checks += 1
    if not any("x-user-id" in f for f in _sanitize_findings(_SANITIZE_FIXTURE_DEFAULTS_MISMATCH)):
        failures.append("a delete in an unassociated named defaults was accepted as protection")

    checks += 1
    if _sanitize_findings(_SANITIZE_FIXTURE_DEFAULTS_FROM):
        failures.append("a delete in the defaults named by `from` did not protect its proxy")

    checks += 1
    cross_file = _sanitize_findings(_SANITIZE_FIXTURE_FILE_A_INJECT, _SANITIZE_FIXTURE_FILE_B_DELETE)
    if not any("x-user-id" in f for f in cross_file):
        failures.append("a delete in an unrelated file was accepted as protection")

    checks += 1
    combined = _sanitize_findings(_SANITIZE_FIXTURE_FILE_B_DELETE + _SANITIZE_FIXTURE_FILE_A_INJECT)
    if combined:
        failures.append(f"the same delete and injection in one file reported a finding: {combined}")

    checks += 1
    resolved = resolve_header_token(
        "{{ .Values.totpProof.trustedHeaders.purpose }}",
        load_values("totpProof:\n  trustedHeaders:\n    purpose: X-TOTP-PURPOSE\n"),
    )
    if resolved != ["x-totp-purpose"]:
        failures.append(f"templated header name resolved to {resolved!r}; expected ['x-totp-purpose']")

    checks += 1
    if not resolve_header_token("{{ .Values.absent.key }}")[0].startswith("unresolved:"):
        failures.append("an unresolvable template did not report itself as unresolved")

    checks += 1
    loop_values = load_values("jwt:\n  claimsToHeaders:\n    sub: X-User-Id\n    prm: X-Access\n")
    loop_text = (
        "{{- range $claim, $hdr := .Values.jwt.claimsToHeaders }}\n"
        "      http-request set-header {{ $hdr }} %[var(txn.claim)]\n"
        "{{- end }}\n"
    )
    loop_injected = set(scan_sanitize(loop_text, loop_values)["injected"])
    if loop_injected != {"x-user-id", "x-access"}:
        failures.append(f"range-bound header names resolved to {sorted(loop_injected)}; expected x-access and x-user-id")

    checks += 1
    if not _BYPASS_KEY.match("BYPASS_GATEWAY_PROOF=true"):
        failures.append("bypass key pattern did not match a BYPASS_-prefixed key")

    for line in failures:
        print(f"FAIL {line}")
    print(f"self-test: {checks - len(failures)}/{checks} passed")
    return EXIT_FINDING if failures else EXIT_OK


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

EPILOG = """exit codes
  0  every requested check ran and passed. Nothing is owed.
  1  a check found a defect. Fix the defect before the change ships; on a
     sanitize or bypass finding, fix the gateway or environment configuration
     first, because no service-side change closes a forgeable header.
  2  the invocation was wrong or an input file could not be read. Fix the
     command and re-run; a usage error is not a pass.
  3  a requested check could not run because its input was missing. Supply the
     input and re-run. Do not report a pass for a check that did not run.

examples
  trust_boundary_check.py --self-test
  trust_boundary_check.py --gateway-config charts/gateway/templates/configmap.yaml
  trust_boundary_check.py --bitmap AAAAAAAAAAAAAAB4 --max-permission-id 95
  trust_boundary_check.py --source-root app --allowlist trusted-headers.md
  trust_boundary_check.py --env-root deploy/
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="trust_boundary_check.py",
        description="Deterministic checks on the Ala gateway trust boundary.",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--self-test", action="store_true", help="run the built-in oracle and fixtures, then exit")
    parser.add_argument("--gateway-config", action="append", default=[], metavar="PATH",
                        help="gateway config or values file; repeatable. Runs the sanitize/inject symmetry check")
    parser.add_argument("--bitmap", action="append", default=[], metavar="VALUE",
                        help="an X-Access value to decode; repeatable")
    parser.add_argument("--max-permission-id", type=int, default=0, metavar="N",
                        help="this service's highest known permission id; required with --bitmap")
    parser.add_argument("--source-root", action="append", default=[], metavar="PATH",
                        help="service source directory to scan for trusted-header reads; repeatable")
    parser.add_argument("--allowlist", metavar="PATH",
                        help="file containing the frozen trusted-header list, owned by alaa-services-contract")
    parser.add_argument("--env-root", action="append", default=[], metavar="PATH",
                        help="directory or file to audit for truthy bypass switches; repeatable")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    requested = bool(args.gateway_config or args.bitmap or args.source_root or args.env_root)
    if not requested:
        parser.print_help()
        return EXIT_USAGE

    findings: list[str] = []
    notes: list[str] = []
    not_run: list[str] = []

    def resolve(values: list[str], label: str) -> list[Path]:
        paths = []
        for value in values:
            path = Path(os.path.expanduser(value))
            if not path.exists():
                print(f"error: {label} path does not exist: {path}", file=sys.stderr)
                raise SystemExit(EXIT_USAGE)
            paths.append(path)
        return paths

    if args.gateway_config:
        f, n, s = check_sanitize(resolve(args.gateway_config, "--gateway-config"))
        findings += f
        notes += n
        not_run += s

    if args.bitmap:
        if args.max_permission_id < 1:
            not_run.append("bitmap: --max-permission-id was not supplied, so no bitmap was decoded")
        else:
            f, n = check_bitmap(args.bitmap, args.max_permission_id)
            findings += f
            notes += n

    if args.source_root:
        if not args.allowlist:
            not_run.append(
                "reads: --allowlist was not supplied. The frozen trusted-header list is owned by "
                "alaa-services-contract; pass its file rather than letting this script carry a copy"
            )
        else:
            allowlist_path = Path(os.path.expanduser(args.allowlist))
            if not allowlist_path.exists():
                print(f"error: --allowlist path does not exist: {allowlist_path}", file=sys.stderr)
                return EXIT_USAGE
            allowed = load_allowlist(allowlist_path)
            if not allowed:
                not_run.append(f"reads: {allowlist_path} contained no header names")
            else:
                f, n = check_reads(resolve(args.source_root, "--source-root"), allowed)
                findings += f
                notes += n

    if args.env_root:
        f, n = check_bypass(resolve(args.env_root, "--env-root"))
        findings += f
        notes += n

    for note in notes:
        print(f"ok   {note}")
    for line in not_run:
        print(f"skip {line}")
    for finding in findings:
        print(f"FAIL {finding}")

    if findings:
        return EXIT_FINDING
    if not_run:
        return EXIT_NOT_RUN
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
