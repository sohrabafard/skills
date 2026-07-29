#!/usr/bin/env python3
"""Report Ansible task actions written as short names instead of FQCN.

One YAML parse per file, then a walk over task keys only. The pre-repair
implementation ran one `grep -r` traversal per name over a 94-name table, which
was two orders of magnitude more work and structure-blind: it reported the
`group:` parameter of `ansible.builtin.template` and the `gather_facts:` play
keyword as modules.

Runs on Windows: pure Python, pathlib, no shell, no Path(__file__).parents[N],
and no temporary directory anywhere.

Exit codes: 0 clean, 1 findings, 2 could not run, 64 usage error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_CANNOT_RUN = 2
EXIT_USAGE = 64

try:
    import yaml
except ImportError:  # pragma: no cover - environment problem, not a finding
    print(
        "BLOCKED: PyYAML is not installed. Install it with "
        "'python3 -m pip install -r scripts/requirements.txt'. "
        "This is exit 2: the check could not run. It is not a pass.",
        file=sys.stderr,
    )
    sys.exit(EXIT_CANNOT_RUN)

from ansible_walk import iter_tasks, line_of  # noqa: E402

# Short name -> the FQCN it resolves to today, verified 2026-07-29 against
# ansible-core's config/ansible_builtin_runtime.yml routing table. Re-derive
# with scripts/check_module_currency.py --routing.
SHORT_TO_FQCN = {
    # ansible.builtin, still in core
    "add_host": "ansible.builtin.add_host",
    "apt": "ansible.builtin.apt",
    "apt_key": "ansible.builtin.apt_key",
    "apt_repository": "ansible.builtin.apt_repository",
    "assemble": "ansible.builtin.assemble",
    "assert": "ansible.builtin.assert",
    "async_status": "ansible.builtin.async_status",
    "blockinfile": "ansible.builtin.blockinfile",
    "command": "ansible.builtin.command",
    "copy": "ansible.builtin.copy",
    "cron": "ansible.builtin.cron",
    "debconf": "ansible.builtin.debconf",
    "debug": "ansible.builtin.debug",
    "dnf": "ansible.builtin.dnf",
    "dpkg_selections": "ansible.builtin.dpkg_selections",
    "expect": "ansible.builtin.expect",
    "fail": "ansible.builtin.fail",
    "fetch": "ansible.builtin.fetch",
    "file": "ansible.builtin.file",
    "find": "ansible.builtin.find",
    "gather_facts": "ansible.builtin.gather_facts",
    "get_url": "ansible.builtin.get_url",
    "getent": "ansible.builtin.getent",
    "git": "ansible.builtin.git",
    "group": "ansible.builtin.group",
    "group_by": "ansible.builtin.group_by",
    "hostname": "ansible.builtin.hostname",
    "import_playbook": "ansible.builtin.import_playbook",
    "import_role": "ansible.builtin.import_role",
    "import_tasks": "ansible.builtin.import_tasks",
    "include_role": "ansible.builtin.include_role",
    "include_tasks": "ansible.builtin.include_tasks",
    "include_vars": "ansible.builtin.include_vars",
    "iptables": "ansible.builtin.iptables",
    "known_hosts": "ansible.builtin.known_hosts",
    "lineinfile": "ansible.builtin.lineinfile",
    "meta": "ansible.builtin.meta",
    "package": "ansible.builtin.package",
    "package_facts": "ansible.builtin.package_facts",
    "pause": "ansible.builtin.pause",
    "ping": "ansible.builtin.ping",
    "pip": "ansible.builtin.pip",
    "raw": "ansible.builtin.raw",
    "reboot": "ansible.builtin.reboot",
    "replace": "ansible.builtin.replace",
    "rpm_key": "ansible.builtin.rpm_key",
    "script": "ansible.builtin.script",
    "service": "ansible.builtin.service",
    "service_facts": "ansible.builtin.service_facts",
    "set_fact": "ansible.builtin.set_fact",
    "set_stats": "ansible.builtin.set_stats",
    "setup": "ansible.builtin.setup",
    "shell": "ansible.builtin.shell",
    "slurp": "ansible.builtin.slurp",
    "stat": "ansible.builtin.stat",
    "subversion": "ansible.builtin.subversion",
    "systemd": "ansible.builtin.systemd_service",
    "systemd_service": "ansible.builtin.systemd_service",
    "sysvinit": "community.general.sysvinit",
    "tempfile": "ansible.builtin.tempfile",
    "template": "ansible.builtin.template",
    "unarchive": "ansible.builtin.unarchive",
    "uri": "ansible.builtin.uri",
    "user": "ansible.builtin.user",
    "validate_argument_spec": "ansible.builtin.validate_argument_spec",
    "wait_for": "ansible.builtin.wait_for",
    "wait_for_connection": "ansible.builtin.wait_for_connection",
    "yum_repository": "ansible.builtin.yum_repository",
    # Left core: the short name still resolves through a redirect, so the task
    # runs where the collection happens to be installed and fails where it is
    # not. The FQCN plus a requirements.yml entry is the only stable form.
    "archive": "community.general.archive",
    "authorized_key": "ansible.posix.authorized_key",
    "acl": "ansible.posix.acl",
    "at": "ansible.posix.at",
    "firewalld": "ansible.posix.firewalld",
    "mount": "ansible.posix.mount",
    "seboolean": "ansible.posix.seboolean",
    "selinux": "ansible.posix.selinux",
    "synchronize": "ansible.posix.synchronize",
    "sysctl": "ansible.posix.sysctl",
    "yum": "ansible.builtin.dnf",
    # Common community.general short names
    "alternatives": "community.general.alternatives",
    "apk": "community.general.apk",
    "composer": "community.general.composer",
    "docker_container": "community.docker.docker_container",
    "docker_image": "community.docker.docker_image",
    "docker_network": "community.docker.docker_network",
    "docker_volume": "community.docker.docker_volume",
    "filesystem": "community.general.filesystem",
    "gem": "community.general.gem",
    "homebrew": "community.general.homebrew",
    "htpasswd": "community.general.htpasswd",
    "locale_gen": "community.general.locale_gen",
    "lvg": "community.general.lvg",
    "lvol": "community.general.lvol",
    "npm": "community.general.npm",
    "parted": "community.general.parted",
    "pam_limits": "community.general.pam_limits",
    "timezone": "community.general.timezone",
    "ufw": "community.general.ufw",
    "zypper": "community.general.zypper",
}

# Short names whose FQCN is in a collection, so a requirements.yml entry is
# needed as well as the rename.
NEEDS_COLLECTION = {
    name: fqcn
    for name, fqcn in SHORT_TO_FQCN.items()
    if not fqcn.startswith("ansible.builtin.")
}


class Finding:
    __slots__ = ("path", "line", "short", "fqcn")

    def __init__(self, path: str, line: int, short: str, fqcn: str) -> None:
        self.path = path
        self.line = line
        self.short = short
        self.fqcn = fqcn

    def as_dict(self) -> dict:
        return {
            "file": self.path,
            "line": self.line,
            "short_name": self.short,
            "fqcn": self.fqcn,
            "needs_collection": self.short in NEEDS_COLLECTION,
        }


def scan_file(path: Path, findings: list, errors: list) -> None:
    try:
        with path.open("r", encoding="utf-8") as handle:
            node = yaml.compose(handle)
    except (yaml.YAMLError, UnicodeDecodeError, OSError) as exc:
        errors.append(f"{path}: {exc}")
        return
    if node is None:
        return
    for _task, key_node, _value in iter_tasks(node):
        key = key_node.value
        if key in SHORT_TO_FQCN:
            findings.append(Finding(str(path), line_of(key_node), key, SHORT_TO_FQCN[key]))


def collect(target: Path) -> list:
    if target.is_file():
        return [target]
    out = []
    skip = {".git", "venv", ".venv", "node_modules", "__pycache__", ".molecule", ".tox"}
    for pattern in ("*.yml", "*.yaml"):
        for candidate in sorted(target.rglob(pattern)):
            if skip.intersection(candidate.parts):
                continue
            out.append(candidate)
    return out


def self_test() -> int:
    here = Path(__file__).resolve().parent
    fixtures = here.parent / "test" / "fixtures" / "fqcn"
    checks = [
        ("fqcn-correct.yml", 0, "a fully FQCN playbook reports nothing"),
        ("short-names.yml", 1, "short names are reported"),
    ]
    passed = failed = 0
    print("self-test: check_fqcn.py")
    for name, expected, label in checks:
        path = fixtures / name
        if not path.exists():
            print(f"  FAIL {label}: fixture missing at {path}")
            failed += 1
            continue
        findings, errors = [], []
        scan_file(path, findings, errors)
        actual = 1 if findings else 0
        if errors:
            actual = 2
        if actual == expected:
            print(f"  ok   {label} ({len(findings)} finding(s))")
            passed += 1
        else:
            print(f"  FAIL {label}: expected {expected}, got {actual} ({findings and findings[0].short})")
            failed += 1

    # The two historical false positives must stay absent: the `group:`
    # parameter of a template task and the `gather_facts:` play keyword.
    findings, errors = [], []
    scan_file(fixtures / "fqcn-correct.yml", findings, errors)
    shorts = {f.short for f in findings}
    for noise in ("group", "gather_facts"):
        if noise in shorts:
            print(f"  FAIL '{noise}' is reported as a module; it is a parameter or play keyword")
            failed += 1
        else:
            print(f"  ok   '{noise}' is not misreported as a module")
            passed += 1

    print()
    if failed:
        print(f"self-test: {passed} passed, {failed} FAILED")
        return EXIT_FINDINGS
    print(f"self-test: {passed} assertion(s) passed")
    return EXIT_OK


def main(argv: list) -> int:
    parser = argparse.ArgumentParser(
        prog="check_fqcn.py",
        description=(
            "Report Ansible task actions written as short names instead of "
            "fully qualified collection names."
        ),
        epilog=(
            "Exit codes: 0 clean, 1 findings, 2 could not run, 64 usage error. "
            "FQCN is an error, not advice: assets/.ansible-lint enables "
            "fqcn[action-core] as an error and this script agrees with it."
        ),
    )
    parser.add_argument("target", nargs="?", help="playbook, role directory or project directory")
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
            f"BLOCKED: no .yml or .yaml files under {target}. "
            "This is exit 2: the check could not run. It is not a pass.",
            file=sys.stderr,
        )
        return EXIT_CANNOT_RUN

    findings: list = []
    errors: list = []
    for path in files:
        scan_file(path, findings, errors)

    if errors:
        for err in errors:
            print(f"BLOCKED: could not parse {err}", file=sys.stderr)
        print(
            "This is exit 2: the check could not run over every file. It is not a pass.",
            file=sys.stderr,
        )
        return EXIT_CANNOT_RUN

    if args.format == "json":
        print(json.dumps({"findings": [f.as_dict() for f in findings]}, indent=2))
    else:
        if not findings:
            print("PASS - every task action is fully qualified")
        else:
            print("Short module names found. Each must be replaced with its FQCN:")
            print()
            for f in findings:
                marker = "  (declare the collection in requirements.yml)" if f.short in NEEDS_COLLECTION else ""
                print(f"  {f.path}:{f.line}: {f.short} -> {f.fqcn}{marker}")
            print()
            collections = sorted(
                {SHORT_TO_FQCN[f.short].rsplit(".", 1)[0] for f in findings if f.short in NEEDS_COLLECTION}
            )
            if collections:
                print("Collections these FQCNs require, to add to requirements.yml:")
                for coll in collections:
                    print(f"  - name: {coll}")
                print()
            print("The name-to-FQCN mapping and what each removed module became is")
            print("references/module_alternatives.md.")

    return EXIT_FINDINGS if findings else EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
