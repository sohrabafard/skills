#!/usr/bin/env python3
"""Assert that generated Ansible parses and that nothing was left unsubstituted.

Three checks, in one pass:

1. **Every YAML file parses.** Six of the eight YAML files in this skill's own
   scaffold failed `yaml.safe_load` until 2026-07-29, so an agent following the
   instruction "copy the role structure from assets/templates/role/" started
   from files that could not load. This check is the reason that cannot recur.

2. **No non-canonical boolean.** `yes`, `no`, `on` and `off` are rejected by
   ansible-lint's `yaml[truthy]` under the production profile. The skill's own
   checklist has said "use true/false" since before this checker existed, and
   the templates used `yes` in five places, which is what a rule with no checker
   looks like.

3. **No placeholder token survives into output.** `CHANGE_ME_*` and the literal
   `ROLE_NAME` are the scaffold's substitution tokens. A file that still
   contains one after substitution is a file that will fail at run time with a
   confusing message. `--scaffold` inverts this check: inside
   `assets/templates/` the tokens are expected, and their *absence* from a
   template would mean the placeholder convention was abandoned.

Runs on Windows: pure Python, `pathlib`, no shell, no
`Path(__file__).parents[N]`, and no temporary directory anywhere.

Exit codes: 0 clean, 1 findings, 2 could not run, 64 usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_CANNOT_RUN = 2
EXIT_USAGE = 64

try:
    import yaml
except ImportError:  # pragma: no cover
    print(
        "BLOCKED: PyYAML is not installed. Install it with "
        "'python3 -m pip install pyyaml'. "
        "This is exit 2: the check could not run. It is not a pass.",
        file=sys.stderr,
    )
    sys.exit(EXIT_CANNOT_RUN)

# A non-canonical boolean as a mapping value. Anchored on the value position so
# that a key ending in "no" and a string such as "yes, really" do not match.
TRUTHY = re.compile(r":\s+(yes|no|on|off)\s*(#.*)?$", re.IGNORECASE)

# The scaffold's substitution tokens.
PLACEHOLDER = re.compile(r"\bCHANGE_ME_[A-Za-z0-9_]*|\bROLE_NAME\b")

# The bracketed convention the scaffold used until 2026-07-29. `[ role_name ]`
# is not a placeholder: YAML reads it as a one-element flow sequence, so
# `[ role_name ]_port: [ default_port ]` is a mapping key that begins with a
# sequence and the file does not load.
BRACKET_PLACEHOLDER = re.compile(r"\[\s*[A-Za-z_][A-Za-z0-9_ ]*\s*\]\s*:")

YAML_SUFFIXES = (".yml", ".yaml")
SKIP_PARTS = {".git", "venv", ".venv", "node_modules", "__pycache__", ".tox", ".molecule"}


class Finding:
    __slots__ = ("path", "line", "rule", "message", "remediation")

    def __init__(self, path, line, rule, message, remediation):
        self.path = path
        self.line = line
        self.rule = rule
        self.message = message
        self.remediation = remediation

    def as_dict(self):
        return {
            "file": self.path,
            "line": self.line,
            "rule": self.rule,
            "message": self.message,
            "remediation": self.remediation,
        }


def collect(target: Path) -> list:
    if target.is_file():
        return [target]
    out = []
    for candidate in sorted(target.rglob("*")):
        if not candidate.is_file():
            continue
        if SKIP_PARTS.intersection(candidate.parts):
            continue
        if candidate.suffix in YAML_SUFFIXES or candidate.name in (".ansible-lint", ".yamllint"):
            out.append(candidate)
    return out


def check_file(path: Path, scaffold: bool, findings: list) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        findings.append(
            Finding(str(path), 0, "read", f"could not read the file: {exc}", "Check the encoding; this toolchain assumes UTF-8.")
        )
        return

    # 1. Parse.
    try:
        yaml.safe_load(text)
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        line = (mark.line + 1) if mark is not None else 0
        findings.append(
            Finding(
                str(path),
                line,
                "yaml[parse]",
                f"the file does not parse: {getattr(exc, 'problem', exc)}",
                "Diagnose with: python3 -c \"import yaml,sys;yaml.safe_load(open(sys.argv[1]))\" "
                f"{path}. The three usual causes are in ansible-validator "
                "references/failure-classes.md class A.",
            )
        )
        return

    for line_no, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue

        # 2. Booleans.
        if TRUTHY.search(line):
            findings.append(
                Finding(
                    str(path),
                    line_no,
                    "yaml[truthy]",
                    f"non-canonical boolean: {stripped[:70]}",
                    "Write true or false. ansible-lint's production profile "
                    "rejects yes, no, on and off.",
                )
            )

        # 3. The bracketed placeholder convention, which does not survive YAML.
        if BRACKET_PLACEHOLDER.search(line):
            findings.append(
                Finding(
                    str(path),
                    line_no,
                    "placeholder[bracketed]",
                    f"bracketed placeholder: {stripped[:70]}",
                    "YAML reads [ name ] as a one-element flow sequence, not as "
                    "a placeholder. Use a bare token such as ROLE_NAME_port or "
                    "CHANGE_ME_value. references/scaffold.md states the convention.",
                )
            )

        # 4. Surviving substitution tokens, outside the scaffold itself.
        if not scaffold and PLACEHOLDER.search(line):
            findings.append(
                Finding(
                    str(path),
                    line_no,
                    "placeholder[unsubstituted]",
                    f"substitution token left in generated output: {stripped[:70]}",
                    "Replace every ROLE_NAME with the role's name and every "
                    "CHANGE_ME_* token with a real value before delivering the file.",
                )
            )

    # 5. In scaffold mode, a role or playbook template with no token at all is a
    #    template whose convention was abandoned. The check is scoped to
    #    templates/role/ and templates/playbook/, which are substituted file by
    #    file. templates/inventory/ and templates/project/ are worked examples
    #    and configuration copied and then edited, so a concrete value there is
    #    correct rather than a defect.
    if scaffold and path.suffix in YAML_SUFFIXES:
        substituted = any(part in ("role", "playbook") for part in path.parts)
        if substituted and not PLACEHOLDER.search(text):
            findings.append(
                Finding(
                    str(path),
                    0,
                    "placeholder[missing]",
                    "a scaffold template carries no substitution token",
                    "Either the file is a finished artifact and does not belong "
                    "under assets/templates/, or its placeholders were replaced "
                    "with concrete values by accident.",
                )
            )


def self_test() -> int:
    here = Path(__file__).resolve().parent
    skill = here.parent
    passed = failed = 0
    print("self-test: check_templates.py")

    def assert_true(condition, label):
        nonlocal passed, failed
        if condition:
            print(f"  ok   {label}")
            passed += 1
        else:
            print(f"  FAIL {label}")
            failed += 1

    # The shipped scaffold must be clean in scaffold mode.
    templates = skill / "assets" / "templates"
    findings = []
    files = collect(templates)
    assert_true(len(files) >= 8, f"the scaffold has files to check ({len(files)} found)")
    for path in files:
        check_file(path, scaffold=True, findings=findings)
    if findings:
        for f in findings[:10]:
            print(f"       {f.path}:{f.line}: {f.rule}: {f.message}")
    assert_true(not findings, "every shipped template parses and uses the placeholder convention")

    # The negative fixtures must each be reported.
    fixtures = skill / "test" / "fixtures"
    cases = [
        ("broken-bracket-placeholder.yml", "yaml[parse]", "the historical bracketed placeholder is reported"),
        ("truthy-yes.yml", "yaml[truthy]", "a yes/no boolean is reported"),
        ("unsubstituted.yml", "placeholder[unsubstituted]", "a surviving CHANGE_ME token is reported in output mode"),
    ]
    for name, rule, label in cases:
        path = fixtures / name
        if not path.exists():
            print(f"  FAIL {label}: fixture missing at {path}")
            failed += 1
            continue
        got = []
        check_file(path, scaffold=False, findings=got)
        if any(f.rule == rule for f in got):
            print(f"  ok   {label}")
            passed += 1
        else:
            print(f"  FAIL {label}: expected {rule}, got {[f.rule for f in got]}")
            failed += 1

    # The generated role fixture must be clean in output mode.
    role = skill / "test" / "fixtures" / "scaffold_role"
    got = []
    for path in collect(role):
        check_file(path, scaffold=False, findings=got)
    if got:
        for f in got[:5]:
            print(f"       {f.path}:{f.line}: {f.rule}: {f.message}")
    assert_true(not got, "the substituted example role is clean in output mode")

    print()
    if failed:
        print(f"self-test: {passed} passed, {failed} FAILED")
        return EXIT_FINDINGS
    print(f"self-test: {passed} assertion(s) passed")
    return EXIT_OK


def main(argv) -> int:
    parser = argparse.ArgumentParser(
        prog="check_templates.py",
        description=(
            "Assert that Ansible YAML parses, uses canonical booleans, and "
            "carries no unsubstituted scaffold placeholder."
        ),
        epilog=(
            "Exit codes: 0 clean, 1 findings, 2 could not run, 64 usage error. "
            "Run it on generated output before delivering, and with --scaffold "
            "on assets/templates/ after editing a template."
        ),
    )
    parser.add_argument("target", nargs="?", help="file or directory to check")
    parser.add_argument(
        "--scaffold",
        action="store_true",
        help="the target is assets/templates/, where placeholders are expected",
    )
    parser.add_argument("--self-test", action="store_true", help="run against the shipped fixtures")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return EXIT_USAGE

    if args.self_test:
        return self_test()

    if not args.target:
        print("Usage error: a target path is required. Run with --help.", file=sys.stderr)
        return EXIT_USAGE

    target = Path(args.target)
    if not target.exists():
        print(
            f"BLOCKED: target not found: {target}. "
            "This is exit 2: the check could not run. It is not a pass.",
            file=sys.stderr,
        )
        return EXIT_CANNOT_RUN

    files = collect(target)
    if not files:
        print(
            f"BLOCKED: no YAML files under {target}. "
            "This is exit 2: the check could not run. It is not a pass.",
            file=sys.stderr,
        )
        return EXIT_CANNOT_RUN

    findings = []
    for path in files:
        check_file(path, scaffold=args.scaffold, findings=findings)

    if args.format == "json":
        print(json.dumps({"checked": len(files), "findings": [f.as_dict() for f in findings]}, indent=2))
    elif not findings:
        print(f"PASS - {len(files)} file(s) parse, use canonical booleans and carry no stray placeholder")
    else:
        for f in findings:
            print(f"{f.path}:{f.line}: {f.rule}: {f.message}")
            print(f"    {f.remediation}")
            print()
        print(f"{len(findings)} finding(s) in {len(files)} file(s).")
        print("Validate the result with ansible-validator (/ansible-validator,")
        print("$ansible-validator): bash <ansible-validator>/scripts/validate_role.sh <role>")

    return EXIT_FINDINGS if findings else EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
