#!/usr/bin/env python3
"""Gate the alaa-rule-writer specialist: grants, parity, and the absence of a model pin.

The specialist ships one shared contract and two runtime wrappers. The contract is the
only place its behaviour is written; each wrapper embeds that contract verbatim and adds
runtime metadata and nothing else. Nothing in the repository would notice if a wrapper
drifted from the contract, if a grant widened, or if a model name reappeared, so this
checker is the only control over all three.

    assets/rule-writer/contract.md                  the shared contract
    assets/rule-writer/claude/alaa-rule-writer.md   frontmatter + contract
    assets/rule-writer/codex/alaa-rule-writer.toml  keys + contract in developer_instructions

Rules:

    G1  both wrappers exist and expose the keys this checker reads
    G2  the Claude wrapper declares tools, and grants no write, execution, or Skill tool
    G3  neither wrapper grants an MCP server
    G4  the Codex wrapper sets sandbox_mode = "read-only"
    G5  each wrapper's embedded contract equals contract.md
    G6  neither wrapper pins a model or an effort, or carries an identity line
    G7  every doctrine path a wrapper names resolves
    G8  the wrappers agree on name and description

G5 compares the value the runtime loads, not the bytes on disk, and for the Codex wrapper
those differ. A TOML basic multi-line string processes escapes, so one backslash inside
developer_instructions either joins two lines silently or makes the file unloadable, and a
reader diffing the file sees neither. The wrapper is therefore parsed with tomllib. Where
tomllib is absent -- Python below 3.11 -- the text is extracted directly and equality is
provable only while the block contains no backslash and no embedded delimiter; anything
else is reported as could-not-run rather than passed.

Exit codes:

    0  every rule holds
    1  at least one rule failed
    2  could not run -- a missing contract, an unreadable file, TOML this checker cannot
       parse, or no fixtures

A 2 is a failed gate, never a pass. Run with --self-test to prove the gate rejects known-bad
definitions; a rule with no red fixture is decoration.

Usage:

    python scripts/check_rule_writer_grants.py
    python scripts/check_rule_writer_grants.py --root <skill-directory>
    python scripts/check_rule_writer_grants.py --self-test
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

try:
    import tomllib
except ModuleNotFoundError:  # Python below 3.11; the fallback below narrows what it will claim.
    tomllib = None

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_CANNOT_RUN = 2

CONTRACT = "assets/rule-writer/contract.md"
CLAUDE_WRAPPER = "assets/rule-writer/claude/alaa-rule-writer.md"
CODEX_WRAPPER = "assets/rule-writer/codex/alaa-rule-writer.toml"

# A read-only wording lane needs to read and search, and nothing else. Skill is withheld
# deliberately: the contract names its doctrine as file paths, so Read reaches it, and a
# Skill grant would let the lane load anything.
ALLOWED_CLAUDE_TOOLS = frozenset(("Read", "Glob", "Grep"))

# Effort names are matched as whole words so that "high" inside prose does not fire; a bare
# key is matched separately below.
MODEL_NAME_RE = re.compile(r"\b(opus|sonnet|haiku|fable|luna|terra|sol)\b|gpt-?5", re.I)
IDENTITY_LINE_RE = re.compile(r"\bAGENT:\s*\S+\s*\|", re.I)
EFFORT_TOKEN_RE = re.compile(r"\bEFFORT:\s*\S", re.I)
DOCTRINE_RE = re.compile(r"`alaa-prompting-guide\s+(references/[A-Za-z0-9._/-]+\.md)`")


class CannotRun(Exception):
    """The checker could not reach a verdict. Never reported as a pass."""


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").replace("\r\n", "\n")
    except OSError as exc:
        raise CannotRun(f"cannot read {path}: {exc}") from exc
    except UnicodeDecodeError as exc:
        raise CannotRun(f"{path} is not decodable UTF-8: {exc}") from exc


def normalise(body: str) -> str:
    """Line endings and edge blank lines only.

    Everything between the first and last non-blank line is compared exactly, so a dropped
    clause or a softened verb fails. Trailing-newline style is not behaviour and is not
    what this rule is protecting.
    """
    return body.strip("\n").rstrip()


def parse_claude(text: str) -> Optional[Tuple[dict, str]]:
    """Frontmatter mapping and body, or None when the file is not a Claude agent file.

    Hand-rolled rather than a YAML library, matching the rest of this repository: one code
    path on every machine, and a key shape this checker fully owns.
    """
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 3)
    if end == -1:
        return None
    head, body = text[4:end], text[end + 5 :]
    fields: dict = {}
    for line in head.split("\n"):
        if not line.strip() or line.startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields, body


def parse_codex(text: str) -> Optional[Tuple[dict, str]]:
    """Top-level keys and the loaded developer_instructions, or None when a key is absent.

    Raises CannotRun rather than guessing: a wrapper the parser cannot read is a wrapper
    whose contents cannot be compared, and a checker that cannot compare must not pass.
    """
    if tomllib is not None:
        try:
            data = tomllib.loads(text)
        except tomllib.TOMLDecodeError as exc:
            raise CannotRun(f"the Codex wrapper is not valid TOML, so no runtime could load it: {exc}") from exc
        body = data.get("developer_instructions")
        if not isinstance(body, str):
            return None
        return data, body

    m = re.search(r'^developer_instructions\s*=\s*"""\n(.*?)\n"""\s*$', text, re.S | re.M)
    if not m:
        return None
    body = m.group(1)
    if "\\" in body or '"""' in body:
        raise CannotRun(
            "this Python has no tomllib and the contract block contains an escape, so what "
            "Codex would load cannot be derived from the file text; run on Python 3.11 or newer"
        )
    head = text[: m.start()]
    fields: dict = {}
    for line in head.split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        km = re.match(r'^([A-Za-z_][A-Za-z0-9_.-]*)\s*=\s*"(.*)"\s*$', line)
        if km:
            fields[km.group(1)] = km.group(2)
            continue
        km = re.match(r"^([A-Za-z_][A-Za-z0-9_.-]*)\s*=\s*(.+?)\s*$", line)
        if km:
            fields[km.group(1)] = km.group(2)
    return fields, body


def check(root: Path) -> List[str]:
    contract_path = root / CONTRACT
    if not contract_path.is_file():
        raise CannotRun(f"no contract at {contract_path}; nothing to compare wrappers against")
    contract = normalise(read_text(contract_path))
    if not contract:
        raise CannotRun(f"{contract_path} is empty; an empty contract cannot prove parity")

    findings: List[str] = []
    claude_path, codex_path = root / CLAUDE_WRAPPER, root / CODEX_WRAPPER
    claude = parse_claude(read_text(claude_path)) if claude_path.is_file() else None
    codex = parse_codex(read_text(codex_path)) if codex_path.is_file() else None

    if claude is None:
        findings.append(f"G1: {CLAUDE_WRAPPER} is missing or has no YAML frontmatter")
    if codex is None:
        findings.append(f"G1: {CODEX_WRAPPER} is missing or has no developer_instructions string")

    wrappers = [(n, p, w) for n, p, w in (("claude", CLAUDE_WRAPPER, claude), ("codex", CODEX_WRAPPER, codex)) if w]

    if claude:
        fields, _ = claude
        declared = fields.get("tools")
        if declared is None:
            findings.append("G2: the Claude wrapper omits tools, so it inherits every tool")
        else:
            granted = {t.strip() for t in declared.split(",") if t.strip()}
            extra = sorted(granted - ALLOWED_CLAUDE_TOOLS)
            if extra:
                findings.append(
                    "G2: the Claude wrapper grants "
                    + ", ".join(extra)
                    + "; a read-only wording lane holds only "
                    + ", ".join(sorted(ALLOWED_CLAUDE_TOOLS))
                )

    for name, rel, (fields, body) in wrappers:
        mcp = sorted(k for k in fields if k.split(".")[0] in ("mcpServers", "mcp_servers"))
        if mcp or re.search(r"^\s*mcp[_S]", body, re.M):
            findings.append(f"G3: the {name} wrapper grants an MCP server ({', '.join(mcp) or 'named in the body'})")

        if normalise(body) != contract:
            findings.append(f"G5: the contract embedded in {rel} differs from {CONTRACT}")

        for key in ("model", "effort", "model_reasoning_effort"):
            if key in fields:
                findings.append(f"G6: the {name} wrapper pins {key}; model and effort are chosen at dispatch")
        if IDENTITY_LINE_RE.search(body) or EFFORT_TOKEN_RE.search(body):
            findings.append(f"G6: the {name} wrapper's output contract carries an identity line")
        named_model = MODEL_NAME_RE.search(body) or MODEL_NAME_RE.search(fields.get("description", ""))
        if named_model:
            findings.append(f"G6: the {name} wrapper names the model {named_model.group(0)!r}")

        for cited in DOCTRINE_RE.findall(body):
            if not (root / cited).is_file():
                findings.append(f"G7: {rel} cites {cited}, which does not resolve")

    if codex:
        fields, _ = codex
        mode = fields.get("sandbox_mode")
        if mode != "read-only":
            findings.append(f"G4: the Codex wrapper sets sandbox_mode {mode!r}, not 'read-only'")

    if claude and codex:
        cf, _ = claude
        xf, _ = codex
        for key in ("name", "description"):
            if cf.get(key) != xf.get(key):
                findings.append(f"G8: the wrappers disagree on {key}")

    return findings


def self_test(fixtures: Path) -> int:
    """Every rule gets one red fixture that only it rejects, plus one green tree.

    A checker never observed rejecting a bad input is indistinguishable from one that
    always passes.
    """
    if not fixtures.is_dir():
        raise CannotRun(f"no fixtures at {fixtures}")
    cases = [
        ("green", None),
        ("red-g1-missing-codex-wrapper", "G1"),
        ("red-g2-claude-grants-write", "G2"),
        ("red-g3-codex-grants-mcp", "G3"),
        ("red-g4-codex-not-read-only", "G4"),
        ("red-g5-contract-drift", "G5"),
        ("red-g5-toml-escape-drift", "G5"),
        ("red-g6-model-pinned", "G6"),
        ("red-g7-dangling-doctrine-path", "G7"),
        ("red-g8-description-mismatch", "G8"),
        ("red-unparseable-toml", "CANNOT_RUN"),
    ]
    failures = 0
    for name, expected in cases:
        root = fixtures / name
        if not root.is_dir():
            raise CannotRun(f"missing fixture {root}")
        try:
            found = check(root)
        except CannotRun as exc:
            if expected == "CANNOT_RUN":
                continue
            print(f"SELF-TEST FAILED: {name} could not run: {exc}")
            failures += 1
            continue
        codes = {f.split(":", 1)[0] for f in found}
        if expected == "CANNOT_RUN":
            print(f"SELF-TEST FAILED: {name} should be unreadable, reported {sorted(codes) or 'nothing'}")
            failures += 1
            continue
        if expected is None:
            if found:
                print(f"SELF-TEST FAILED: {name} should be clean, reported {sorted(codes)}")
                failures += 1
            continue
        if expected not in codes:
            print(f"SELF-TEST FAILED: {name} should report {expected}, reported {sorted(codes) or 'nothing'}")
            failures += 1
    if failures:
        print(f"SELF-TEST FAILED: {failures} of {len(cases)} cases")
        return EXIT_FINDINGS
    reader = "tomllib" if tomllib is not None else "the no-escape fallback"
    print(f"SELF-TEST OK: {len(cases) - 1} red fixtures each rejected, green tree clean, Codex read via {reader}")
    return EXIT_CLEAN


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", help="skill directory to check; defaults to this script's parent")
    parser.add_argument("--fixtures", help="fixture directory for --self-test")
    parser.add_argument("--self-test", action="store_true", help="prove each rule rejects a known-bad input")
    args = parser.parse_args(argv)

    here = Path(__file__).resolve().parent
    try:
        if args.self_test:
            fixtures = Path(args.fixtures.strip().strip("\r\n")).expanduser() if args.fixtures else here / "fixtures" / "rule-writer"
            return self_test(fixtures)
        root = Path(args.root.strip().strip("\r\n")).expanduser() if args.root else here.parent
        findings = check(root)
    except CannotRun as exc:
        print(f"could not run: {exc}", file=sys.stderr)
        return EXIT_CANNOT_RUN
    except OSError as exc:
        print(f"could not run: {exc}", file=sys.stderr)
        return EXIT_CANNOT_RUN

    if findings:
        print("FINDINGS:")
        for f in findings:
            print(f"  {f}")
        return EXIT_FINDINGS
    print("OK: both wrappers embed the contract unchanged, hold read-only grants, and pin no model")
    return EXIT_CLEAN


if __name__ == "__main__":
    sys.exit(main())
