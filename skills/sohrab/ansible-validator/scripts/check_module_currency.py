#!/usr/bin/env python3
"""Report a fully qualified module name that no longer resolves where it says.

The failure this catches: a module leaves ansible-core into a collection, core
keeps a compatibility redirect, and every example that names the old FQCN keeps
running on a machine where the collection happens to be installed and fails on
a machine where it is not. Nothing reports it, and a large module reference
rots invisibly. Three of the 34 `ansible.builtin.*` names taught by
ansible-generator/references/module-patterns.md were in that state on
2026-07-29 -- `yum`, `archive` and `authorized_key`, an 8.8% defect rate over an
exhaustive sample of that stratum.

It reads ansible-core's own routing table,
`ansible/config/ansible_builtin_runtime.yml`, plus the presence of the module
file, so it needs no network and no installed collection. Run it on a schedule:
it is the only defence against that rate recurring.

Scope: any file. It extracts every FQCN-shaped token and checks each one, so it
works on markdown references, playbooks and role trees alike. It is the reason
ansible-generator (/ansible-generator, $ansible-generator) routes here rather
than maintaining a second mapping of its own.

Runs on Windows: pure Python, pathlib, no shell, no Path(__file__).parents[N],
and no temporary directory anywhere.

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

IGNORE_MARKER = "check-module-currency:ignore"
# A whole file may exempt itself. references/module_alternatives.md is the
# mapping table: every stale name in it is there deliberately, as the left
# column, and marking each row would put a visible artefact in the rendered
# table.
IGNORE_FILE_MARKER = "check-module-currency:ignore-file"

FQCN = re.compile(
    r"\b(ansible\.builtin|ansible\.posix|ansible\.windows|ansible\.netcommon|"
    r"ansible\.utils|community\.[a-z_]+|amazon\.aws|azure\.azcollection|"
    r"google\.cloud|kubernetes\.core)\.([a-z0-9_]+)\b"
)


def core_paths():
    try:
        import ansible
    except ImportError:
        return None, None
    root = Path(ansible.__file__).resolve().parent
    return root / "config" / "ansible_builtin_runtime.yml", root / "modules"


def load_routing(routing_file: Path) -> dict:
    import yaml

    data = yaml.safe_load(routing_file.read_text(encoding="utf-8")) or {}
    routing = data.get("plugin_routing", {})
    merged = {}
    for section in ("modules", "action"):
        for name, entry in (routing.get(section) or {}).items():
            merged.setdefault(name, entry)
    return merged


def check_builtin(short: str, routing: dict, modules_dir: Path):
    """Return (ok, reason). ok is False when the name is not a live builtin."""
    entry = routing.get(short) or {}
    redirect = entry.get("redirect")
    if redirect and redirect != f"ansible.builtin.{short}":
        return False, f"redirects to {redirect}"
    if entry.get("tombstone"):
        return False, "tombstoned in ansible-core"
    if not (modules_dir / f"{short}.py").exists():
        return False, "no module of that name is shipped in ansible-core"
    if entry.get("deprecation"):
        return False, "deprecated in ansible-core"
    return True, ""


def scan(paths, routing, modules_dir):
    findings = []
    seen = set()
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            return None, f"could not read {path}: {exc}"
        if IGNORE_FILE_MARKER in text:
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            # An explicit exemption, for prose that names a stale FQCN in order
            # to say it must not be used. In markdown write it as an HTML
            # comment, which renders invisibly:
            #     <!-- check-module-currency:ignore -->
            if IGNORE_MARKER in line:
                continue
            for match in FQCN.finditer(line):
                collection, short = match.group(1), match.group(2)
                fqcn = f"{collection}.{short}"
                if collection != "ansible.builtin":
                    continue
                key = (str(path), fqcn)
                if key in seen:
                    continue
                seen.add(key)
                ok, reason = check_builtin(short, routing, modules_dir)
                if not ok:
                    findings.append(
                        {
                            "file": str(path),
                            "line": line_no,
                            "fqcn": fqcn,
                            "reason": reason,
                        }
                    )
    return findings, None


def collect(target: Path):
    if target.is_file():
        return [target]
    out = []
    # test/fixtures holds files that are deliberately stale, so a directory scan
    # skips them. --self-test reaches them by passing the file path directly.
    skip = {".git", "venv", ".venv", "node_modules", "__pycache__", ".tox", "fixtures"}
    for pattern in ("*.md", "*.yml", "*.yaml"):
        for candidate in sorted(target.rglob(pattern)):
            if skip.intersection(candidate.parts):
                continue
            out.append(candidate)
    return out


def self_test() -> int:
    here = Path(__file__).resolve().parent
    fixture = here.parent / "test" / "fixtures" / "modules" / "stale-fqcns.md"
    routing_file, modules_dir = core_paths()
    print("self-test: check_module_currency.py")
    if routing_file is None or not routing_file.exists():
        print("  BLOCKED ansible-core is not importable, so no routing table is readable")
        return EXIT_CANNOT_RUN
    routing = load_routing(routing_file)
    passed = failed = 0

    findings, err = scan([fixture], routing, modules_dir)
    if err:
        print(f"  FAIL {err}")
        return EXIT_CANNOT_RUN
    reported = {f["fqcn"] for f in findings}
    for name in ("ansible.builtin.yum", "ansible.builtin.archive", "ansible.builtin.authorized_key"):
        if name in reported:
            print(f"  ok   {name} is reported as no longer a live builtin")
            passed += 1
        else:
            print(f"  FAIL {name} is NOT reported")
            failed += 1
    for name in ("ansible.builtin.dnf", "ansible.builtin.template", "ansible.builtin.systemd_service"):
        if name in reported:
            print(f"  FAIL {name} is a live builtin but was reported")
            failed += 1
        else:
            print(f"  ok   {name} is accepted as a live builtin")
            passed += 1
    print()
    if failed:
        print(f"self-test: {passed} passed, {failed} FAILED")
        return EXIT_FINDINGS
    print(f"self-test: {passed} assertion(s) passed")
    return EXIT_OK


def main(argv) -> int:
    parser = argparse.ArgumentParser(
        prog="check_module_currency.py",
        description=(
            "Report an ansible.builtin.* name that ansible-core no longer "
            "provides directly, so that documentation and playbooks do not "
            "keep teaching a name that works only through a redirect."
        ),
        epilog="Exit codes: 0 clean, 1 findings, 2 could not run, 64 usage error.",
    )
    parser.add_argument("target", nargs="?", help="file or directory to scan")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--routing", action="store_true", help="print the routing entry for every builtin name found")
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

    routing_file, modules_dir = core_paths()
    if routing_file is None or not routing_file.exists():
        print(
            "BLOCKED: ansible-core is not importable, so its routing table "
            "cannot be read. Install it with "
            "'python3 -m pip install -r scripts/requirements.txt'. "
            "This is exit 2: the check could not run. It is not a pass.",
            file=sys.stderr,
        )
        return EXIT_CANNOT_RUN

    try:
        routing = load_routing(routing_file)
    except Exception as exc:  # noqa: BLE001 - any failure here is exit 2
        print(f"BLOCKED: could not parse {routing_file}: {exc}", file=sys.stderr)
        return EXIT_CANNOT_RUN

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
            f"BLOCKED: no .md, .yml or .yaml files under {target}. "
            "This is exit 2: the check could not run. It is not a pass.",
            file=sys.stderr,
        )
        return EXIT_CANNOT_RUN

    findings, err = scan(files, routing, modules_dir)
    if err:
        print(f"BLOCKED: {err}", file=sys.stderr)
        return EXIT_CANNOT_RUN

    if args.format == "json":
        print(json.dumps({"findings": findings}, indent=2))
    elif not findings:
        print(f"PASS - every ansible.builtin name in {len(files)} file(s) is a live builtin")
    else:
        print("Names that ansible-core no longer provides directly:")
        print()
        for f in findings:
            print(f"  {f['file']}:{f['line']}: {f['fqcn']} - {f['reason']}")
        print()
        print("Replace each with the name on the right of the redirect and declare")
        print("the collection in requirements.yml. references/module_alternatives.md")
        print("carries the full mapping.")

    return EXIT_FINDINGS if findings else EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
