#!/usr/bin/env python3
"""Structural validator for the skills/sohrab/ skill pack.

WHAT THIS ASSERTS, per skill directory
    V1  SKILL.md has frontmatter carrying name and description
    V2  the description is at or under the plugin-validation hard limit of 1024 characters,
        and warns above the author target (default 900)
    V3  the body carries a heading matching ^#+\\s+.*\\b(when not to use|do not use)\\b
    V4  warns when the body above the first reference exceeds 120 lines
    V5  every bundled-resource path cited in SKILL.md exists
    V6  agents/openai.yaml exists
    V7  interface.short_description is 25 to 64 characters inclusive
    V8  interface.default_prompt mentions $<skill-name>
    V9  every bundled-resource path cited in references/00-topic-map.md exists
    V10 alaa-services-contract names no alaa_* metric, exchange or queue it never registered

    V3 and V7/V8 are the two rules a skill cannot discover by reading. A section titled
    "What this skill does not decide" does not satisfy V3; a literal "When NOT to use" heading
    does.

WHAT THIS DELIBERATELY DOES NOT ASSERT
    Cross-skill path resolution across the other 738 Markdown files in the pack. That belongs to
    check_fleet_references.py, which resolves a citation against every skill, knows the two path
    notations, and carries the four exclusions this tool does not. Widening V5 and V9 to every
    Markdown file would put two resolvers in one job with different answers -- the two-indexes,
    two-lies failure this pack is being repaired to remove. V5 and V9 stay scoped to the two
    always-loaded surfaces, SKILL.md and the topic-map router, where a broken path is worst.

YAML
    Parsed by the bundled MiniYaml subset parser, not by PyYAML. PyYAML is not guaranteed on the
    Windows machine this runs on or in CI, and importing it when present would fork behaviour:
    a file the fallback rejects would pass on a developer's laptop and fail in CI. One code path
    everywhere. MiniYaml raises on any construct outside its subset rather than guessing, and an
    unparseable file is exit 2 -- "I could not evaluate this rule" is never reported as clean.

EXIT CODES
    0  clean          no errors
    1  errors         one or more rule violations. Warnings alone do not reach 1.
    2  could not run  pack directory missing or unreadable, zero skills found, a file that is
                      not decodable UTF-8, YAML the subset parser cannot parse, or any
                      unexpected exception

WINDOWS
    Python 3 standard library only. The pack directory comes from --pack-dir or --root, or is
    discovered by searching upward from the current directory; Path(__file__).parents[N] is
    never used, so moving this script does not break it. Files are read as bytes and decoded
    explicitly, newlines are normalised before any line is parsed, and no temp directory is
    created.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

EXIT_CLEAN = 0
EXIT_ERRORS = 1
EXIT_CANNOT_RUN = 2

PACK_RELATIVE = ("skills", "sohrab")

PATH_RE = re.compile(r"`((?:references|docs|examples|scripts|assets|output|test|tests)/[^`]+)`")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
METRIC_RE = re.compile(r"^alaa_[a-z0-9]+(?:_[a-z0-9]+)*$")
BROKER_RE = re.compile(
    r"^(?:"
    r"[a-z][a-z0-9_]*\.events"
    r"|[a-z][a-z0-9_]*\.commands(?:\.dlx)?"
    r"|[a-z][a-z0-9_]*\.jobs\.[a-z0-9_]+"
    r"|notification\.command\.[a-z0-9_.]+"
    r"|notif\.[a-z0-9_.]+"
    r")(?:\.retry|\.dlq)?$"
)
REGISTRY_SKILL = "alaa-services-contract"
METRIC_REGISTRY = "references/24-metric-registry.md"
QUEUE_REGISTRY = "references/23-queue-and-exchange-registry.md"
LOCAL_RESOURCE_PREFIXES = ("references/", "examples/", "scripts/", "assets/")
TARGET_REPO_PREFIXES = ("docs/", "output/", "test/", "tests/")

SKILL_NAME_RE = re.compile(
    r"[/$]?\b((?:alaa|golang|caas|ansible|clickhouse|jitsi|service|tusd|vector|playwright|openfga|openai)[a-z0-9-]*)\b"
)

# Plugin validation rejects a description over this length. It is stricter than the
# 1536-character listing cap documented for Claude Code, so this is the binding number.
DESCRIPTION_HARD_MAX = 1024
# Author target. The plugin validator's own character count exceeds a YAML-parsed count by at
# least thirty, so 900 leaves the margin that keeps a passing description passing. This is the
# one place the number lives; --description-target overrides it without a code edit, which is
# what the open 900-versus-950 question needs.
DESCRIPTION_TARGET_MAX_DEFAULT = 900
BODY_LINE_WARN = 120
SHORT_DESCRIPTION_MIN = 25
SHORT_DESCRIPTION_MAX = 64


class CannotRun(Exception):
    """Raised for every condition that means the validator could not evaluate its rules."""


# --------------------------------------------------------------------------------------
# MiniYaml -- the narrow YAML subset these files actually use
# --------------------------------------------------------------------------------------


class MiniYamlError(Exception):
    pass


_KEY_RE = re.compile(r"^([A-Za-z0-9_.$-]+)\s*:(?:\s+(.*))?$")
_BLOCK_SCALAR_RE = re.compile(r"^([|>])([+-]?)$")
_DQ_ESCAPES = {
    "n": "\n",
    "t": "\t",
    "r": "\r",
    "0": "\0",
    '"': '"',
    "\\": "\\",
    "/": "/",
}


def _strip_plain_comment(value: str) -> str:
    """Remove a trailing comment from a plain scalar. A `#` only starts a comment when it is
    preceded by whitespace or begins the value."""
    out: List[str] = []
    for i, ch in enumerate(value):
        if ch == "#" and (i == 0 or value[i - 1].isspace()):
            break
        out.append(ch)
    return "".join(out).strip()


def _parse_double_quoted(text: str, i: int) -> Tuple[str, int]:
    out: List[str] = []
    i += 1
    while i < len(text):
        ch = text[i]
        if ch == "\\":
            if i + 1 >= len(text):
                raise MiniYamlError("double-quoted scalar ends with a backslash")
            nxt = text[i + 1]
            if nxt in _DQ_ESCAPES:
                out.append(_DQ_ESCAPES[nxt])
                i += 2
                continue
            raise MiniYamlError(f"unsupported escape \\{nxt} in a double-quoted scalar")
        if ch == '"':
            return "".join(out), i + 1
        out.append(ch)
        i += 1
    raise MiniYamlError("unterminated double-quoted scalar")


def _parse_single_quoted(text: str, i: int) -> Tuple[str, int]:
    out: List[str] = []
    i += 1
    while i < len(text):
        ch = text[i]
        if ch == "'":
            if i + 1 < len(text) and text[i + 1] == "'":
                out.append("'")
                i += 2
                continue
            return "".join(out), i + 1
        out.append(ch)
        i += 1
    raise MiniYamlError("unterminated single-quoted scalar")


def _coerce(value: str) -> Any:
    low = value.lower()
    if low in ("true", "yes", "on"):
        return True
    if low in ("false", "no", "off"):
        return False
    if low in ("null", "~", ""):
        return None
    if re.fullmatch(r"[+-]?\d+", value):
        return int(value)
    if re.fullmatch(r"[+-]?\d*\.\d+", value):
        return float(value)
    return value


def _parse_scalar(raw: str) -> Any:
    raw = raw.strip()
    if not raw:
        return None
    if raw[0] == '"':
        value, end = _parse_double_quoted(raw, 0)
        rest = raw[end:].strip()
        if rest and not rest.startswith("#"):
            raise MiniYamlError(f"trailing text after a double-quoted scalar: {rest!r}")
        return value
    if raw[0] == "'":
        value, end = _parse_single_quoted(raw, 0)
        rest = raw[end:].strip()
        if rest and not rest.startswith("#"):
            raise MiniYamlError(f"trailing text after a single-quoted scalar: {rest!r}")
        return value
    if raw[0] in "&*!":
        raise MiniYamlError(f"anchors, aliases and tags are not supported: {raw!r}")
    plain = _strip_plain_comment(raw)
    if ": " in plain or plain.endswith(":"):
        # YAML forbids ": " inside a plain scalar because it cannot be told from a nested mapping.
        # Coercing it to a string accepted a file a YAML parser rejects, so a rule was reported
        # against a value the file does not actually carry.
        raise MiniYamlError(
            f"a plain scalar may not contain ': ' or end with a colon: {plain!r}; quote it"
        )
    return _coerce(plain)


def _parse_flow(raw: str) -> Tuple[Any, int]:
    """Parse a flow mapping or sequence starting at raw[0]. Used for the single-line
    `interface: {display_name: "...", short_description: "..."}` form."""
    if raw[0] == "{":
        result: Dict[str, Any] = {}
        i = 1
        while True:
            while i < len(raw) and raw[i] in " \t,":
                i += 1
            if i >= len(raw):
                raise MiniYamlError("unterminated flow mapping")
            if raw[i] == "}":
                return result, i + 1
            key_start = i
            while i < len(raw) and raw[i] != ":":
                i += 1
            if i >= len(raw):
                raise MiniYamlError("flow mapping key without a value")
            key = raw[key_start:i].strip().strip("\"'")
            i += 1
            while i < len(raw) and raw[i] in " \t":
                i += 1
            if i >= len(raw):
                raise MiniYamlError("flow mapping key without a value")
            if raw[i] == '"':
                value, i = _parse_double_quoted(raw, i)
            elif raw[i] == "'":
                value, i = _parse_single_quoted(raw, i)
            elif raw[i] in "{[":
                raise MiniYamlError("nested flow collections are not supported")
            else:
                start = i
                depth = 0
                while i < len(raw) and (raw[i] not in ",}" or depth):
                    if raw[i] in "[{":
                        depth += 1
                    elif raw[i] in "]}":
                        depth -= 1
                    i += 1
                value = _coerce(raw[start:i].strip())
            result[key] = value
    if raw[0] == "[":
        items: List[Any] = []
        i = 1
        while True:
            while i < len(raw) and raw[i] in " \t,":
                i += 1
            if i >= len(raw):
                raise MiniYamlError("unterminated flow sequence")
            if raw[i] == "]":
                return items, i + 1
            if raw[i] == '"':
                value, i = _parse_double_quoted(raw, i)
            elif raw[i] == "'":
                value, i = _parse_single_quoted(raw, i)
            else:
                start = i
                while i < len(raw) and raw[i] not in ",]":
                    i += 1
                value = _coerce(raw[start:i].strip())
            items.append(value)
    raise MiniYamlError(f"not a flow collection: {raw[:20]!r}")


class _Lines:
    """A single-pass cursor over the significant lines of a document.

    Blank lines and whole-line comments are dropped here because no construct outside a block
    scalar treats them as content. A block scalar does, so _parse_block_scalar reads text_lines
    directly instead of these rows.
    """

    def __init__(self, text: str) -> None:
        self.rows: List[Tuple[int, str, int]] = []
        for n, raw in enumerate(text.split("\n"), 1):
            if not raw.strip() or raw.lstrip().startswith("#"):
                continue
            # Measure the whole leading whitespace run, not only the spaces. lstrip(" ") leaves
            # a leading tab in place and reports indent 0, which silently promoted a
            # tab-indented nested key to a top-level key instead of rejecting the file.
            leading = raw[: len(raw) - len(raw.lstrip())]
            if "\t" in leading:
                raise MiniYamlError(f"line {n}: tab used for indentation")
            indent = len(leading)
            self.rows.append((indent, raw.strip(), n))
        self.i = 0
        self.text_lines = text.split("\n")

    def peek(self) -> Optional[Tuple[int, str, int]]:
        return self.rows[self.i] if self.i < len(self.rows) else None

    def reopen_current(self, indent: int, content: str) -> None:
        """Re-present the current row at a different column with different text.

        A block sequence item such as `- domain: x` is, once the dash is consumed, the first line
        of a block mapping whose column is that of the text after the dash. Rewriting the row in
        place is how that dash is unwound without copying the row list. The row is visited once,
        so no later read sees the pre-rewrite form.
        """
        self.rows[self.i] = (indent, content, self.rows[self.i][2])

    def skip_through_line(self, lineno: int) -> None:
        """Advance past every row whose source line is at or before lineno."""
        while self.i < len(self.rows) and self.rows[self.i][2] <= lineno:
            self.i += 1


def _fold_block_lines(body_lines: List[str], first_lineno: int) -> str:
    """Fold a block scalar as YAML defines it: a line break between two non-empty lines becomes a
    single space, and a run of empty lines becomes that many newlines.

    A line indented further than the first line of the block is a "more indented" line, whose
    breaks YAML preserves literally rather than folding. No file in this pack uses that form, so
    it raises instead of being guessed at; a literal `|` block expresses the same intent.
    """
    out: List[str] = []
    pending = 0
    for offset, line in enumerate(body_lines):
        if not line:
            pending += 1
            continue
        if line[:1] == " ":
            raise MiniYamlError(
                f"line {first_lineno + offset}: a folded block scalar line indented further than "
                f"the first line of the block is not supported; use a literal | block"
            )
        if pending:
            out.append("\n" * pending)
            pending = 0
        elif out:
            out.append(" ")
        out.append(line)
    return "".join(out)


def _parse_block_scalar(
    lines: _Lines, style: str, chomp: str, parent_indent: int, key_lineno: int
) -> str:
    """Read a literal or folded block scalar from the physical lines following its key.

    Physical lines, not the filtered row list: inside a block scalar a blank line and a line
    beginning with `#` are content, and the row list drops both. Reading the filtered rows
    returned a string shorter than YAML defines without reporting anything, which is the one
    failure mode worse than raising.
    """
    collected: List[str] = []
    # split("\n") leaves a final empty string for a document that ends with a newline. That
    # element is the line terminator, not a blank line, and counting it as content added one
    # newline to every kept block scalar.
    limit = len(lines.text_lines)
    if limit and lines.text_lines[-1] == "":
        limit -= 1
        ends_with_newline = True
    else:
        ends_with_newline = False
    j = key_lineno  # text_lines is 0-based, so index key_lineno is the line after the key.
    while j < limit:
        line = lines.text_lines[j]
        if not line.strip():
            collected.append("")
            j += 1
            continue
        if len(line) - len(line.lstrip()) <= parent_indent:
            break
        collected.append(line)
        j += 1
    lines.skip_through_line(j)
    # The block's last line carries a line break unless the block ran to an unterminated end of
    # document. Chomping acts on that break, so with no break there is nothing to keep or clip.
    terminated = j < limit or ends_with_newline

    # Trailing blank lines are not content; how many of them survive is decided by the chomping
    # indicator alone.
    trailing_blanks = 0
    while collected and not collected[-1]:
        collected.pop()
        trailing_blanks += 1
    if not collected:
        return "\n" * trailing_blanks if chomp == "+" else ""

    first = next(i for i, line in enumerate(collected) if line)
    leading = collected[first][: len(collected[first]) - len(collected[first].lstrip())]
    if "\t" in leading:
        raise MiniYamlError(f"line {key_lineno + 1 + first}: tab used for indentation")
    base = len(leading)

    body_lines: List[str] = []
    for offset, line in enumerate(collected):
        if not line:
            body_lines.append("")
            continue
        if len(line) - len(line.lstrip()) < base:
            raise MiniYamlError(
                f"line {key_lineno + 1 + offset}: block scalar line is less indented than the "
                f"first line of the block"
            )
        body_lines.append(line[base:])

    if style == "|":
        body = "\n".join(body_lines)
    else:
        body = _fold_block_lines(body_lines, key_lineno + 1)

    if chomp == "-" or not terminated:
        return body
    if chomp == "+":
        return body + "\n" * (1 + trailing_blanks)
    # Clip, the default: exactly one trailing newline survives when there is any content.
    return body + "\n" if body else ""


def _parse_block_value(lines: _Lines, indent: int) -> Any:
    """Parse the block collection that starts at the current row, at column indent."""
    row = lines.peek()
    if row is not None and _is_sequence_item(row[1]):
        return _parse_sequence(lines, indent)
    return _parse_mapping(lines, indent)


def _is_sequence_item(content: str) -> bool:
    """True for a block sequence entry: `- value`, or a bare `-` whose value is on later lines."""
    return content == "-" or content.startswith("- ")


def _parse_mapping(lines: _Lines, indent: int) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    while True:
        row = lines.peek()
        if row is None:
            return result
        row_indent, content, lineno = row
        if row_indent < indent:
            return result
        if row_indent > indent:
            raise MiniYamlError(f"line {lineno}: unexpected indentation")
        if _is_sequence_item(content):
            raise MiniYamlError(f"line {lineno}: sequence item where a mapping key was expected")
        m = _KEY_RE.match(content)
        if not m:
            raise MiniYamlError(f"line {lineno}: not a mapping key: {content!r}")
        key, value = m.group(1), (m.group(2) or "").strip()
        lines.i += 1

        if value == "" or value.startswith("#"):
            nxt = lines.peek()
            if nxt is None or nxt[0] < indent:
                result[key] = None
                continue
            # A block sequence may sit at its parent key's own column, which is the commoner YAML
            # style; a nested mapping may not. Anything else at or below this column belongs to
            # this mapping, not to this key.
            if nxt[0] == indent:
                if _is_sequence_item(nxt[1]):
                    result[key] = _parse_sequence(lines, indent)
                else:
                    result[key] = None
                continue
            result[key] = _parse_block_value(lines, nxt[0])
            continue

        if value[0] in "|>":
            bs = _BLOCK_SCALAR_RE.match(value)
            if not bs:
                # An explicit indentation indicator such as `|2`, or a comment after the header,
                # is outside this subset. Falling through to the scalar reader would have stored
                # the two characters of the header as the value.
                raise MiniYamlError(
                    f"line {lineno}: unsupported block scalar header {value!r}"
                )
            result[key] = _parse_block_scalar(
                lines, bs.group(1), bs.group(2), indent, lineno
            )
            continue
        if value[0] in "{[":
            parsed, end = _parse_flow(value)
            rest = value[end:].strip()
            if rest and not rest.startswith("#"):
                raise MiniYamlError(f"line {lineno}: trailing text after a flow collection")
            result[key] = parsed
            continue
        result[key] = _parse_scalar(value)


def _parse_sequence(lines: _Lines, indent: int) -> List[Any]:
    items: List[Any] = []
    while True:
        row = lines.peek()
        if row is None or row[0] < indent:
            return items
        row_indent, content, lineno = row
        if row_indent > indent:
            raise MiniYamlError(f"line {lineno}: unexpected indentation in a sequence")
        if not _is_sequence_item(content):
            return items

        after_dash = content[1:]
        # The item's column is where the text after the dash begins, and that column is the indent
        # of any block collection the item opens. It is why a sibling key of `- domain: x` sits
        # under the `d` and not under the dash.
        item_indent = row_indent + 1 + (len(after_dash) - len(after_dash.lstrip(" ")))
        rest = after_dash.strip()

        if rest == "":
            lines.i += 1
            nxt = lines.peek()
            if nxt is None or nxt[0] <= row_indent:
                items.append(None)
                continue
            items.append(_parse_block_value(lines, nxt[0]))
            continue

        if _is_sequence_item(rest):
            lines.reopen_current(item_indent, rest)
            items.append(_parse_sequence(lines, item_indent))
            continue

        if rest[0] in "{[|>":
            # A flow collection or a block scalar as a sequence item needs machinery no file in
            # this pack calls for. Falling through to the scalar reader would have stored the
            # literal text `{a: 1}` or `|` as the item's value.
            raise MiniYamlError(
                f"line {lineno}: a flow collection or block scalar as a sequence item is outside "
                f"this subset; a mapping item or a plain or quoted scalar item is supported"
            )

        if _KEY_RE.match(rest):
            lines.reopen_current(item_indent, rest)
            items.append(_parse_mapping(lines, item_indent))
            continue

        lines.i += 1
        items.append(_parse_scalar(rest))


def mini_yaml_load(text: str) -> Any:
    """Parse the YAML subset these files use: block mappings, block sequences including sequences
    of mappings, plain, single- and double-quoted scalars, literal and folded block scalars with
    all three chomping indicators, single-line flow collections, and comments. Anything else
    raises MiniYamlError rather than being guessed at, and every caller turns that into exit 2."""
    body = text.replace("\r\n", "\n").replace("\r", "\n")
    if body.startswith("\ufeff"):
        body = body[1:]
    # A single leading document marker is normal in a standalone YAML file; a second one means a
    # multi-document stream, which is outside the subset and must raise rather than be guessed at.
    if body.lstrip().startswith("---"):
        body = body.lstrip()[3:].lstrip("\n")
    if re.search(r"^(---|\.\.\.)\s*$", body, re.M):
        raise MiniYamlError("multi-document YAML is not supported")
    if not body.strip():
        return {}
    lines = _Lines(body)
    first = lines.peek()
    if first is None:
        return {}
    if _is_sequence_item(first[1]):
        result: Any = _parse_sequence(lines, first[0])
    else:
        result = _parse_mapping(lines, first[0])
    if lines.peek() is not None:
        raise MiniYamlError(f"line {lines.peek()[2]}: unparsed trailing content")
    return result


# --------------------------------------------------------------------------------------
# Pack rules -- every rule the previous version enforced correctly is preserved verbatim
# --------------------------------------------------------------------------------------


def is_placeholder_or_glob(path: str) -> bool:
    return any(token in path for token in ("*", "?", "[", "]", "<", ">"))


def is_command_example(path: str) -> bool:
    return any(char.isspace() for char in path)


def should_validate_path(skill_dir: Path, path: str) -> bool:
    """Return true only for bundled skill resource paths.

    Skill docs often mention target-repository paths such as `docs/BIG_PICTURE.md` or command
    placeholders such as `scripts/validate_makefile.sh <file>`. Those are not bundled resources
    and must not fail pack validation. The `<repo>/...` notation introduced with
    check_fleet_references.py is inert here for two independent reasons: PATH_RE requires the
    code span to begin with a resource prefix, and is_placeholder_or_glob rejects angle brackets.
    """
    normalized = path.replace("\\", "/").strip()

    if is_placeholder_or_glob(normalized) or is_command_example(normalized):
        return False

    if normalized.endswith("/"):
        return False

    for prefix in LOCAL_RESOURCE_PREFIXES:
        if normalized.startswith(prefix):
            return (skill_dir / prefix.rstrip("/")).exists()

    if normalized.startswith("docs/"):
        return (skill_dir / "docs").exists()

    if normalized.startswith(TARGET_REPO_PREFIXES):
        return False

    return True


def local_reference_paths(skill_dir: Path, text: str):
    """Yield bundled-resource paths that this skill owns.

    A cross-skill pointer names the owning skill on the same line before the path --
    `alaa-services-contract` `references/22-...md`. Resolving such a path inside the citing
    skill is wrong, so the line is skipped once another skill is named on it.
    """
    own = skill_dir.name
    for line in text.split("\n"):
        paths = PATH_RE.findall(line)
        if not paths:
            continue
        named = {
            n
            for n in SKILL_NAME_RE.findall(line)
            if n != own and (skill_dir.parent / n).is_dir()
        }
        if named:
            continue
        for path in paths:
            if should_validate_path(skill_dir, path):
                yield path


def read_text(path: Path) -> str:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise CannotRun(f"cannot read {path}: {exc}") from exc
    if b"\x00" in raw:
        raise CannotRun(f"{path} contains a NUL byte and is not decodable text")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CannotRun(f"{path} is not decodable UTF-8: {exc}")
    if text.startswith("\ufeff"):
        text = text[1:]
    # Normalised before any line is parsed. A carriage return left on the last field of a line
    # makes every comparison fail while the rendered bytes look identical.
    return text.replace("\r\n", "\n").replace("\r", "\n")


def check_registries(skill_dir: Path) -> List[str]:
    """Fail when this skill names a metric, exchange, or queue it never registered.

    A registry nothing checks goes stale. This proves one half: no reference file in
    alaa-services-contract may name an `alaa_*` metric absent from
    references/24-metric-registry.md, or a broker exchange or queue absent from
    references/23-queue-and-exchange-registry.md. The other half - that a service repository
    emits only registered names - cannot be checked from here and is stated as such in
    24-metric-registry.md.
    """
    errors: List[str] = []
    refs = skill_dir / "references"
    if not refs.is_dir():
        return errors

    registries = {}
    for rel in (METRIC_REGISTRY, QUEUE_REGISTRY):
        path = skill_dir / rel
        if not path.exists():
            errors.append(f"{skill_dir.name}: registry file missing -> {rel}")
            return errors
        registries[rel] = read_text(path)

    for md in sorted(refs.glob("*.md")):
        rel_name = f"references/{md.name}"
        text = read_text(md)
        for token in BACKTICK_RE.findall(text):
            token = token.strip()
            if any(ch in token for ch in "<>*?[]/ \t"):
                continue
            if METRIC_RE.match(token):
                target = METRIC_REGISTRY
            elif BROKER_RE.match(token):
                target = QUEUE_REGISTRY
            else:
                continue
            if rel_name == target:
                continue
            if f"`{token}`" not in registries[target]:
                errors.append(
                    f"{skill_dir.name}: {rel_name} names `{token}` with no row in {target}"
                )
    return sorted(set(errors))


def load_skill(skill_dir: Path) -> Tuple[Optional[Dict[str, Any]], str]:
    """Return the parsed frontmatter mapping and the body.

    The frontmatter is parsed as YAML rather than split on the first colon of each line. The
    previous line-splitting reader mis-read a folded description as the two characters `>-`, and
    stripped only outer quotes so an escaped quote inside a description was counted twice.
    """
    raw = read_text(skill_dir / "SKILL.md")
    m = re.match(r"^---\n([\s\S]*?)\n---\n?", raw)
    if not m:
        return None, raw
    try:
        front = mini_yaml_load(m.group(1))
    except MiniYamlError as exc:
        raise CannotRun(f"{skill_dir.name}/SKILL.md: frontmatter is not parseable YAML: {exc}")
    if front is None:
        front = {}
    if not isinstance(front, dict):
        raise CannotRun(
            f"{skill_dir.name}/SKILL.md: frontmatter is a {type(front).__name__}, "
            f"not a mapping"
        )
    return front, raw[m.end() :]


def load_openai_interface(path: Path) -> Dict[str, Any]:
    text = read_text(path)
    try:
        data = mini_yaml_load(text)
    except MiniYamlError as exc:
        raise CannotRun(f"{path}: not parseable YAML: {exc}")
    if not isinstance(data, dict):
        raise CannotRun(f"{path}: top level is a {type(data).__name__}, not a mapping")
    interface = data.get("interface")
    if interface is None:
        return {}
    if not isinstance(interface, dict):
        raise CannotRun(f"{path}: interface is a {type(interface).__name__}, not a mapping")
    return interface


def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def validate_skill(
    skill_dir: Path, description_target: int
) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    name = skill_dir.name

    front, body = load_skill(skill_dir)
    if front is None:
        errors.append(f"{name}: missing or invalid frontmatter")
        return errors, warnings

    declared_name = as_text(front.get("name")).strip()
    description = as_text(front.get("description")).strip()
    if not declared_name or not description:
        errors.append(f"{name}: frontmatter must include name and description")
    else:
        # Plugin validation rejects a description over 1024 characters outright, which is a
        # harder limit than the 1536-character listing cap in the Claude Code docs. Measure the
        # collapsed single-line form, because a folded YAML scalar is counted that way.
        desc_len = len(" ".join(description.split()))
        if desc_len > DESCRIPTION_HARD_MAX:
            errors.append(
                f"{name}: description is {desc_len} chars, over the "
                f"{DESCRIPTION_HARD_MAX}-char plugin-validation limit"
            )
        elif desc_len > description_target:
            warnings.append(
                f"{name}: description is {desc_len} chars, within "
                f"{DESCRIPTION_HARD_MAX - desc_len} of the {DESCRIPTION_HARD_MAX}-char limit; "
                f"keep it at or under {description_target} so one added clause cannot break "
                f"the build"
            )
        # A rule for "no angle bracket in a description" is deliberately NOT added here. The
        # definition of done requires it and no tool reports it, but adding a new failing rule
        # while five skills are being rewritten in parallel would turn another lane's finished
        # work red for a reason that lane was never told about. It needs a measurement of how
        # many descriptions contain one first, and that measurement needs the pack on disk.

    # Accept any casing and either phrasing. The rule is that the body states a negative scope
    # somewhere; forcing one exact spelling only produced false failures.
    if not re.search(r"^#+\s+.*\b(when\s+not\s+to\s+use|do\s+not\s+use)\b", body, re.I | re.M):
        errors.append(f"{name}: missing a 'When not to use' or 'Do not use' section")

    lines = body.count("\n") + 1
    if lines > BODY_LINE_WARN:
        warnings.append(f"{name}: top-level body is {lines} lines")

    for match in local_reference_paths(skill_dir, body):
        if not (skill_dir / match).exists():
            errors.append(f"{name}: referenced path does not exist -> {match}")

    openai_path = skill_dir / "agents" / "openai.yaml"
    if not openai_path.exists():
        errors.append(f"{name}: missing agents/openai.yaml")
    else:
        interface = load_openai_interface(openai_path)
        short_description = as_text(interface.get("short_description")).strip()
        default_prompt = as_text(interface.get("default_prompt"))
        if not (SHORT_DESCRIPTION_MIN <= len(short_description) <= SHORT_DESCRIPTION_MAX):
            errors.append(
                f"{name}: short_description must be {SHORT_DESCRIPTION_MIN}-"
                f"{SHORT_DESCRIPTION_MAX} chars, is {len(short_description)}"
            )
        sigil = "$" + (declared_name or name)
        if sigil not in default_prompt:
            errors.append(f"{name}: default_prompt must mention {sigil}")

    if name == REGISTRY_SKILL:
        errors.extend(check_registries(skill_dir))

    for topic_map in (
        skill_dir / "references" / "00-topic-map.md",
        skill_dir / "docs" / "00-topic-map.md",
    ):
        if topic_map.exists():
            for rel in local_reference_paths(skill_dir, read_text(topic_map)):
                if not (skill_dir / rel).exists():
                    errors.append(f"{name}: topic map path missing -> {rel}")
    return errors, warnings


# --------------------------------------------------------------------------------------
# Discovery and entry point
# --------------------------------------------------------------------------------------


def find_pack_dir(root_arg: Optional[str], pack_arg: Optional[str]) -> Path:
    if pack_arg is not None:
        candidate = Path(pack_arg).expanduser()
        if not candidate.is_dir():
            raise CannotRun(f"--pack-dir is not a directory: {candidate}")
        return candidate
    if root_arg is not None:
        candidate = Path(root_arg).expanduser()
        if not candidate.is_dir():
            raise CannotRun(f"--root is not a directory: {candidate}")
        pack = candidate.joinpath(*PACK_RELATIVE)
        if not pack.is_dir():
            raise CannotRun(f"--root {candidate} does not contain {'/'.join(PACK_RELATIVE)}")
        return pack
    here = Path.cwd().resolve()
    for candidate in (here, *here.parents):
        pack = candidate.joinpath(*PACK_RELATIVE)
        if pack.is_dir():
            return pack
    raise CannotRun(
        f"no ancestor of {here} contains {'/'.join(PACK_RELATIVE)}; pass --root or --pack-dir"
    )


def discover_skills(pack_dir: Path) -> List[Path]:
    try:
        entries = sorted(p for p in pack_dir.iterdir() if p.is_dir())
    except OSError as exc:
        raise CannotRun(f"cannot read {pack_dir}: {exc}") from exc
    skills = [p for p in entries if (p / "SKILL.md").is_file()]
    if not skills:
        raise CannotRun(
            f"zero skills found under {pack_dir}; a successful run over an empty pack "
            f"directory must not look like a pass"
        )
    return skills


def run(pack_dir: Path, description_target: int) -> Tuple[List[str], List[str], List[str], int]:
    errors: List[str] = []
    warnings: List[str] = []
    blockers: List[str] = []
    skills = discover_skills(pack_dir)
    for skill_dir in skills:
        try:
            e, w = validate_skill(skill_dir, description_target)
        except CannotRun as exc:
            # Keep going so one broken file does not hide the state of the other sixty-six,
            # then still exit 2 because at least one rule could not be evaluated.
            blockers.append(str(exc))
            continue
        errors.extend(e)
        warnings.extend(w)
    return errors, warnings, blockers, len(skills)


# --------------------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------------------

SELF_TEST_CASES: Tuple[Tuple[str, int, Tuple[str, ...], Tuple[str, ...]], ...] = (
    # (fixture, expected exit, error substrings that must appear, warning substrings)
    ("green", EXIT_CLEAN, (), ()),
    ("green-unquoted-scalars", EXIT_CLEAN, (), ()),
    ("green-flow-mapping", EXIT_CLEAN, (), ()),
    ("green-block-scalar", EXIT_CLEAN, (), ()),
    ("green-repo-notation", EXIT_CLEAN, (), ()),
    ("green-sequence-of-mappings", EXIT_CLEAN, (), ()),
    ("red-short-description-too-short", EXIT_ERRORS, ("short_description must be 25-64",), ()),
    ("red-default-prompt-no-sigil", EXIT_ERRORS, ("default_prompt must mention",), ()),
    ("red-missing-when-not-to-use", EXIT_ERRORS, ("missing a 'When not to use'",), ()),
    ("red-missing-openai-yaml", EXIT_ERRORS, ("missing agents/openai.yaml",), ()),
    ("red-broken-reference-path", EXIT_ERRORS, ("referenced path does not exist",), ()),
    ("red-topic-map-path-missing", EXIT_ERRORS, ("topic map path missing",), ()),
    ("red-description-over-hard-max", EXIT_ERRORS, ("over the 1024-char",), ()),
    ("red-registry-unregistered-metric", EXIT_ERRORS, ("with no row in",), ()),
    ("warn-description-over-target", EXIT_CLEAN, (), ("keep it at or under 900",)),
    ("warn-body-over-120-lines", EXIT_CLEAN, (), ("top-level body is",)),
    ("red-unparseable-openai-yaml", EXIT_CANNOT_RUN, (), ()),
    ("red-unparseable-sequence-indent", EXIT_CANNOT_RUN, (), ()),
    ("red-unparseable-frontmatter", EXIT_CANNOT_RUN, (), ()),
    ("red-empty-pack", EXIT_CANNOT_RUN, (), ()),
)

MINI_YAML_CASES: Tuple[Tuple[str, str, Any], ...] = (
    (
        "unquoted plain scalar",
        "interface:\n  short_description: SigNoz docs routing and ClickHouse SQL\n",
        "SigNoz docs routing and ClickHouse SQL",
    ),
    (
        "double-quoted scalar",
        'interface:\n  short_description: "SigNoz docs routing and ClickHouse SQL"\n',
        "SigNoz docs routing and ClickHouse SQL",
    ),
    (
        "single-quoted scalar with a doubled quote",
        "interface:\n  short_description: 'it''s a routing surface for docs'\n",
        "it's a routing surface for docs",
    ),
    (
        "folded block scalar",
        "interface:\n  short_description: >-\n    SigNoz docs routing\n    and ClickHouse SQL\n",
        "SigNoz docs routing and ClickHouse SQL",
    ),
    (
        "literal block scalar",
        "interface:\n  short_description: |-\n    SigNoz docs routing\n",
        "SigNoz docs routing",
    ),
    (
        "single-line flow mapping",
        'interface: {display_name: "X", short_description: "SigNoz docs routing and CH SQL"}\n',
        "SigNoz docs routing and CH SQL",
    ),
    (
        "trailing comment on a plain scalar",
        "interface:\n  short_description: SigNoz docs routing and SQL  # keep this short\n",
        "SigNoz docs routing and SQL",
    ),
    (
        "hash inside a quoted scalar is not a comment",
        'interface:\n  short_description: "colour #3A5BA0 routing surface here"\n',
        "colour #3A5BA0 routing surface here",
    ),
)

# Whole-structure cases. MINI_YAML_CASES only reads one string out of one key, so it cannot see a
# collection shape at all. Every expected value here was confirmed identical to PyYAML's parse of
# the same text; PyYAML is the oracle for these values and is deliberately not a runtime import.
MINI_YAML_STRUCTURE_CASES: Tuple[Tuple[str, str, Any], ...] = (
    (
        "block sequence of mappings",
        "policy:\n"
        "  not_this_skill:\n"
        "    - domain: routing, Cache API; PWA update flow\n"
        "      route_to: $alaa-quasar-app-vite-v3\n"
        "    - domain: what a media player stores\n"
        "      route_to: $alaa-shaka-player\n",
        {
            "policy": {
                "not_this_skill": [
                    {
                        "domain": "routing, Cache API; PWA update flow",
                        "route_to": "$alaa-quasar-app-vite-v3",
                    },
                    {"domain": "what a media player stores", "route_to": "$alaa-shaka-player"},
                ]
            }
        },
    ),
    (
        "block sequence of scalars",
        "policy:\n  primary_domains:\n    - indexeddb\n    - browser-storage\n",
        {"policy": {"primary_domains": ["indexeddb", "browser-storage"]}},
    ),
    (
        "sequence at its parent key's own column",
        "policy:\n  primary_domains:\n  - indexeddb\n  - browser-storage\n",
        {"policy": {"primary_domains": ["indexeddb", "browser-storage"]}},
    ),
    (
        "sequence of mappings followed by a sibling key",
        "d:\n  - a: 1\n  - a: 2\nother: z\n",
        {"d": [{"a": 1}, {"a": 2}], "other": "z"},
    ),
    (
        "a mapping nested inside a sequence item's mapping",
        "d:\n  - a:\n      x: 1\n    b: 2\n",
        {"d": [{"a": {"x": 1}, "b": 2}]},
    ),
    (
        "a bare dash whose value is the block below it",
        "d:\n  -\n    a: 1\n    b: 2\n",
        {"d": [{"a": 1, "b": 2}]},
    ),
    (
        "extra spaces after the dash move the item's column",
        "d:\n  -   a: 1\n      b: 2\n",
        {"d": [{"a": 1, "b": 2}]},
    ),
    (
        "a folded scalar under clip chomping keeps exactly one newline",
        "notes:\n  scope: >\n    one\n    two\n",
        {"notes": {"scope": "one two\n"}},
    ),
    (
        "a literal scalar under clip chomping keeps exactly one newline",
        "notes:\n  scope: |\n    one\n    two\n",
        {"notes": {"scope": "one\ntwo\n"}},
    ),
    (
        "keep chomping keeps every trailing blank line and no more",
        "notes:\n  scope: |+\n    one\n\n\nother: 1\n",
        {"notes": {"scope": "one\n\n\n"}, "other": 1},
    ),
    (
        "an unterminated final line has no line break to chomp",
        "notes:\n  scope: |\n    one",
        {"notes": {"scope": "one"}},
    ),
    (
        "a blank line and a hash line inside a block scalar are content",
        "notes:\n  scope: |\n    one\n\n    # not a comment\n",
        {"notes": {"scope": "one\n\n# not a comment\n"}},
    ),
)

# Inputs that must raise. A parser that guesses at malformed YAML turns "I could not evaluate
# this file" into a rule verdict, which is the one failure the exit-code contract exists to stop.
# Every entry here is either malformed YAML that PyYAML also rejects, or a construct outside this
# subset that would otherwise have been silently coerced to the wrong value.
MINI_YAML_REJECT_CASES: Tuple[Tuple[str, str], ...] = (
    ("an anchor", "interface:\n  short_description: &anchor value\n"),
    ("an alias", "interface:\n  short_description: *anchor\n"),
    ("a tab used for indentation", "interface:\n\tshort_description: value\n"),
    ("a sequence item's sibling key one space too deep", "d:\n  - a: 1\n   b: 2\n"),
    ("a sequence item's sibling key far too deep", "d:\n  - a: 1\n      b: 2\n"),
    ("a sequence item more indented than its sequence", "d:\n  - a: 1\n    - b\n"),
    ("a multi-document stream", "a: 1\n---\nb: 2\n"),
    ("an unterminated double-quoted scalar", 'k: "abc\n'),
    ("a block scalar indentation indicator", "k: |2\n   one\n"),
    ("a flow collection as a sequence item", "d:\n  - {a: 1}\n"),
    ("a block scalar as a sequence item", "d:\n  - |\n    x\n"),
    ("a multi-line plain scalar", "k: one\n  two\n"),
    ("a plain scalar containing a colon and a space", "k: some: thing\n"),
    ("a plain scalar ending in a colon", "k: value:\n"),
    ("a nested flow collection", "i: {a: {b: 1}}\n"),
    ("a folded scalar line indented past the first", "k: >\n  one\n    deeper\n"),
)


def run_case(pack_dir: Path, description_target: int) -> Tuple[int, str]:
    import contextlib
    import io

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        code = main(["--pack-dir", str(pack_dir), "--description-target", str(description_target)])
    return code, buf.getvalue()


def self_test(fixtures_dir: Path) -> int:
    base = fixtures_dir / "validator"
    if not base.is_dir():
        print(f"BLOCKED: fixture directory not found: {base}")
        return EXIT_CANNOT_RUN
    passed = failed = blocked = 0

    for label, text, expected in MINI_YAML_CASES:
        try:
            got = mini_yaml_load(text)["interface"]["short_description"]
        except Exception as exc:  # noqa: BLE001 - a parser crash is a blocked case
            print(f"BLOCKED  mini-yaml: {label}: {type(exc).__name__}: {exc}")
            blocked += 1
            continue
        if got != expected:
            print(f"FAIL     mini-yaml: {label}: got {got!r}, expected {expected!r}")
            failed += 1
        else:
            print(f"PASS     mini-yaml: {label}")
            passed += 1

    for label, text, expected_obj in MINI_YAML_STRUCTURE_CASES:
        try:
            got_obj = mini_yaml_load(text)
        except Exception as exc:  # noqa: BLE001 - a parser crash is a blocked case
            print(f"BLOCKED  mini-yaml structure: {label}: {type(exc).__name__}: {exc}")
            blocked += 1
            continue
        if got_obj != expected_obj:
            print(f"FAIL     mini-yaml structure: {label}: got {got_obj!r}, expected {expected_obj!r}")
            failed += 1
        else:
            print(f"PASS     mini-yaml structure: {label}")
            passed += 1

    for label, text in MINI_YAML_REJECT_CASES:
        try:
            got_obj = mini_yaml_load(text)
        except MiniYamlError:
            print(f"PASS     mini-yaml rejects: {label}")
            passed += 1
        except Exception as exc:  # noqa: BLE001 - any other exception type is not a clean refusal
            print(f"BLOCKED  mini-yaml rejects: {label}: raised {type(exc).__name__}: {exc}")
            blocked += 1
        else:
            print(f"FAIL     mini-yaml rejects: {label}: accepted it as {got_obj!r}")
            failed += 1

    for name, expect_code, want_errors, want_warnings in SELF_TEST_CASES:
        pack = base / name / "skills" / "sohrab"
        if not pack.is_dir():
            print(f"BLOCKED  {name}: fixture pack missing ({pack})")
            blocked += 1
            continue
        code, out = run_case(pack, DESCRIPTION_TARGET_MAX_DEFAULT)
        if code != expect_code:
            if code == EXIT_CANNOT_RUN:
                print(f"BLOCKED  {name}: exit 2 (could not run), expected {expect_code}")
                print("         " + out.strip().replace("\n", "\n         "))
                blocked += 1
            else:
                print(f"FAIL     {name}: exit {code}, expected {expect_code}")
                print("         " + out.strip().replace("\n", "\n         "))
                failed += 1
            continue
        missing = [s for s in want_errors + want_warnings if s not in out]
        if missing:
            print(f"FAIL     {name}: output does not mention {missing}")
            print("         " + out.strip().replace("\n", "\n         "))
            failed += 1
            continue
        print(f"PASS     {name}")
        passed += 1

    print(f"\nself-test: {passed} passed, {failed} failed, {blocked} blocked")
    if blocked:
        return EXIT_CANNOT_RUN
    return EXIT_ERRORS if failed else EXIT_CLEAN


# --------------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------------

EPILOG = """\
what each rule asserts
  V1  SKILL.md frontmatter carries name and description
  V2  description at or under 1024 characters, warning above the author target
  V3  a heading matches ^#+\\s+.*\\b(when not to use|do not use)\\b. A section titled
      "What this skill does not decide" does not satisfy it.
  V4  warning when the body exceeds 120 lines
  V5  every bundled-resource path cited in SKILL.md exists
  V6  agents/openai.yaml exists
  V7  interface.short_description is 25 to 64 characters inclusive
  V8  interface.default_prompt mentions $<skill-name>
  V9  every bundled-resource path cited in references/00-topic-map.md exists
  V10 alaa-services-contract registers every alaa_* metric, exchange and queue it names

not asserted here
  Cross-skill path resolution over the rest of the pack's Markdown. That is
  check_fleet_references.py's job; it knows the $SKILL_DIR/ and <repo>/ notations and the
  exclusions this tool does not carry.

exit codes
  0 clean   1 errors (warnings alone do not reach 1)   2 could not run
"""


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="validate_sohrab_skill_pack.py",
        description="Validate the structure of every skill in the skills/sohrab/ pack.",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--root", help="repository root containing skills/sohrab.")
    p.add_argument("--pack-dir", help="the pack directory itself, overriding --root.")
    p.add_argument(
        "--description-target",
        type=int,
        default=DESCRIPTION_TARGET_MAX_DEFAULT,
        metavar="N",
        help=f"warn above this description length. Default {DESCRIPTION_TARGET_MAX_DEFAULT}.",
    )
    p.add_argument(
        "--self-test",
        action="store_true",
        help="run against the bundled fixtures. 0 pass, 1 fail, 2 a fixture could not be run.",
    )
    p.add_argument(
        "--fixtures",
        metavar="PATH",
        help="fixture directory. Default: the fixtures directory beside this script.",
    )
    return p


def clean_arg(value: Optional[str]) -> Optional[str]:
    """Strip surrounding whitespace, including a carriage return, from a path argument.

    A shell or Python driver that writes CRLF leaves a carriage return on the last field of every
    line it parses. Without this, the failure message shows a path that renders identically to the
    correct one.
    """
    return None if value is None else value.strip().strip("\r\n")


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    args.root = clean_arg(args.root)
    args.pack_dir = clean_arg(args.pack_dir)
    args.fixtures = clean_arg(args.fixtures)

    if args.self_test:
        fixtures = (
            Path(args.fixtures).expanduser()
            if args.fixtures
            # Sibling of this file. Path(__file__).parents[N] is forbidden because it encodes a
            # guess about the repository layout above the script.
            else Path(__file__).resolve().with_name("fixtures")
        )
        try:
            return self_test(fixtures)
        except CannotRun as exc:
            print(f"BLOCKED: {exc}")
            return EXIT_CANNOT_RUN

    try:
        pack_dir = find_pack_dir(args.root, args.pack_dir)
        errors, warnings, blockers, skill_count = run(pack_dir, args.description_target)
    except CannotRun as exc:
        print(f"could not run: {exc}", file=sys.stderr)
        return EXIT_CANNOT_RUN
    except Exception as exc:  # noqa: BLE001 - any unexpected failure is "could not run", not "clean"
        print(f"could not run: unexpected {type(exc).__name__}: {exc}", file=sys.stderr)
        return EXIT_CANNOT_RUN

    print(f"{pack_dir}: {skill_count} skills")
    if errors:
        print("Errors:")
        for err in errors:
            print(f"- {err}")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    if blockers:
        print("Could not evaluate:")
        for blocker in blockers:
            print(f"- {blocker}")
        return EXIT_CANNOT_RUN
    return EXIT_ERRORS if errors else EXIT_CLEAN


if __name__ == "__main__":
    raise SystemExit(main())
