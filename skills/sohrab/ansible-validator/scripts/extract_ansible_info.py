#!/usr/bin/env python3
"""Extract module, collection and version information from playbooks and roles.

Emits JSON on stdout. This is the most reliable assertion in the skill: every
YAML file in scope must parse, and a file that does not parse exits 2 with the
file and the parser message.

Two defects were repaired on 2026-07-29 and both are covered by --self-test:

* Classification. `builtin_modules` and `custom_modules` were computed by
  testing fully qualified names against a set of short names, so a correct,
  fully-FQCN playbook reported four "custom" modules and triggered an expensive
  documentation lookup, while a playbook using only unqualified builtins
  reported no modules at all. Classification now reads the collection prefix.

* Block recursion. `block`, `rescue` and `always` were in the skip list at the
  top of the key loop, and the `continue` fired before the recursion below it,
  so no module inside a `block:` was ever seen.

Runs on Windows: pure Python, pathlib, no shell, no Path(__file__).parents[N],
and no temporary directory anywhere.

Exit codes: 0 clean, 1 findings (none are defined today; reserved), 2 could not
run, 64 usage error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_CANNOT_RUN = 2
EXIT_USAGE = 64

try:
    import yaml
except ImportError:  # pragma: no cover
    print(
        json.dumps(
            {
                "error": "PyYAML is not installed",
                "remediation": "python3 -m pip install -r scripts/requirements.txt",
                "exit": EXIT_CANNOT_RUN,
            }
        ),
        file=sys.stderr,
    )
    sys.exit(EXIT_CANNOT_RUN)

# Task-level keys that are never the action.
TASK_KEYWORDS = frozenset(
    """
    action any_errors_fatal args async become become_exe become_flags
    become_method become_user changed_when check_mode collections connection
    debugger delay delegate_facts delegate_to diff environment failed_when
    ignore_errors ignore_unreachable listen loop loop_control module_defaults
    name no_log notify poll port register remote_user retries run_once tags
    throttle timeout until vars when with_dict with_fileglob with_first_found
    with_flattened with_indexed_items with_inventory_hostnames with_items
    with_lines with_list with_nested with_random_choice with_sequence
    with_subelements with_together
    """.split()
)

NESTED_TASK_KEYS = ("block", "rescue", "always")

# Short names that are provided by ansible.builtin today. Used only to decide
# whether an unqualified action needs a collection declaration, never to
# classify a fully qualified name.
BUILTIN_SHORT_NAMES = frozenset(
    """
    add_host apt apt_key apt_repository assemble assert async_status blockinfile
    command copy cron debconf debug dnf dpkg_selections expect fail fetch file
    find gather_facts get_url getent git group group_by hostname import_playbook
    import_role import_tasks include_role include_tasks include_vars iptables
    known_hosts lineinfile meta package package_facts pause ping pip raw reboot
    replace rpm_key script service service_facts set_fact set_stats setup shell
    slurp stat subversion systemd systemd_service tempfile template unarchive
    uri user validate_argument_spec wait_for wait_for_connection yum_repository
    """.split()
)


class AnsibleInfoExtractor:
    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.modules: Set[str] = set()
        self.unqualified_actions: Set[str] = set()
        self.collections: Set[str] = set()
        self.collection_versions: Dict[str, str] = {}
        self.errors: List[str] = []

    # -- traversal ---------------------------------------------------------
    def extract(self) -> Dict[str, Any]:
        if self.path.is_file():
            self._process_file(self.path)
        elif self.path.is_dir():
            self._process_directory(self.path)
        else:
            self.errors.append(f"Path not found: {self.path}")
        return self._build_result()

    def _process_directory(self, directory: Path) -> None:
        for candidate in (
            directory / "requirements.yml",
            directory / "collections" / "requirements.yml",
            directory / "meta" / "requirements.yml",
        ):
            if candidate.exists():
                self._process_requirements(candidate)

        skip = {".git", "venv", ".venv", "node_modules", "__pycache__", ".tox"}
        seen = set()
        for pattern in ("*.yml", "*.yaml"):
            for yaml_file in sorted(directory.rglob(pattern)):
                if skip.intersection(yaml_file.parts):
                    continue
                if yaml_file in seen:
                    continue
                seen.add(yaml_file)
                self._process_file(yaml_file)

    def _process_file(self, file_path: Path) -> None:
        try:
            with file_path.open("r", encoding="utf-8") as handle:
                content = yaml.safe_load(handle)
        except yaml.YAMLError as exc:
            self.errors.append(f"YAML error in {file_path}: {exc}")
            return
        except (OSError, UnicodeDecodeError) as exc:
            self.errors.append(f"Error reading {file_path}: {exc}")
            return

        if not content:
            return
        if isinstance(content, list):
            # A playbook is a list of plays; a task file is a list of tasks.
            if any(isinstance(item, dict) and "hosts" in item for item in content):
                for play in content:
                    if isinstance(play, dict):
                        self._extract_from_play(play)
            else:
                self._extract_from_task_list(content)
        elif isinstance(content, dict):
            if "tasks" in content or "hosts" in content:
                self._extract_from_play(content)

    def _process_requirements(self, req_file: Path) -> None:
        try:
            with req_file.open("r", encoding="utf-8") as handle:
                content = yaml.safe_load(handle)
        except (yaml.YAMLError, OSError, UnicodeDecodeError) as exc:
            self.errors.append(f"Error reading requirements {req_file}: {exc}")
            return
        if not isinstance(content, dict):
            return
        for collection in content.get("collections") or []:
            if isinstance(collection, dict):
                name = collection.get("name", "")
                version = collection.get("version", "unpinned")
                if name:
                    self.collections.add(name)
                    self.collection_versions[name] = version
            elif isinstance(collection, str):
                self.collections.add(collection)
                self.collection_versions.setdefault(collection, "unpinned")

    def _extract_from_play(self, play: Dict) -> None:
        for key in ("pre_tasks", "tasks", "post_tasks", "handlers"):
            if key in play:
                self._extract_from_task_list(play[key])
        if "roles" in play:
            self._extract_from_roles(play["roles"])
        for collection in play.get("collections") or []:
            if isinstance(collection, str):
                self.collections.add(collection)

    def _extract_from_task_list(self, tasks: Any) -> None:
        if not isinstance(tasks, list):
            return
        for task in tasks:
            if not isinstance(task, dict):
                continue
            # Recurse into block, rescue and always first. Reaching them before
            # the keyword filter is the repair: the old code listed them in the
            # skip set and `continue`d past the recursion.
            for nested in NESTED_TASK_KEYS:
                if isinstance(task.get(nested), list):
                    self._extract_from_task_list(task[nested])
            for key in task:
                if key in TASK_KEYWORDS or key in NESTED_TASK_KEYS:
                    continue
                if key.startswith("_"):
                    continue
                if "." in key:
                    parts = key.split(".")
                    if len(parts) >= 3:
                        self.collections.add(f"{parts[0]}.{parts[1]}")
                    self.modules.add(key)
                else:
                    self.unqualified_actions.add(key)

    def _extract_from_roles(self, roles: Any) -> None:
        if not isinstance(roles, list):
            return
        for role in roles:
            name = ""
            if isinstance(role, dict):
                name = role.get("role") or role.get("name") or ""
            elif isinstance(role, str):
                name = role
            if name.count(".") >= 2:
                parts = name.split(".")
                self.collections.add(f"{parts[0]}.{parts[1]}")

    # -- output ------------------------------------------------------------
    def _build_result(self) -> Dict[str, Any]:
        builtin = sorted(m for m in self.modules if m.startswith("ansible.builtin."))
        collection_modules = sorted(
            m for m in self.modules if not m.startswith("ansible.builtin.")
        )
        unqualified = sorted(self.unqualified_actions)
        return {
            "modules": sorted(self.modules) + unqualified,
            "builtin_modules": builtin,
            "collection_modules": collection_modules,
            "unqualified_actions": unqualified,
            "unqualified_actions_needing_collection": sorted(
                a for a in unqualified if a not in BUILTIN_SHORT_NAMES
            ),
            "collections": sorted(self.collections),
            "collection_versions": self.collection_versions,
            "unpinned_collections": sorted(
                name for name, ver in self.collection_versions.items() if ver == "unpinned"
            ),
            "errors": self.errors,
        }


def self_test() -> int:
    here = Path(__file__).resolve().parent
    fixtures = here.parent / "test"
    passed = failed = 0
    print("self-test: extract_ansible_info.py")

    def assert_true(condition: bool, label: str) -> None:
        nonlocal passed, failed
        if condition:
            print(f"  ok   {label}")
            passed += 1
        else:
            print(f"  FAIL {label}")
            failed += 1

    good = fixtures / "playbooks" / "good-playbook.yml"
    result = AnsibleInfoExtractor(str(good)).extract()
    assert_true(not result["errors"], "the good playbook parses")
    assert_true(
        bool(result["builtin_modules"]) and not result["collection_modules"],
        "fully qualified builtins classify as builtin, not as collection modules",
    )
    assert_true(
        not result["unqualified_actions"],
        "the good playbook has no unqualified action",
    )

    blocks = fixtures / "fixtures" / "extract" / "block-nesting.yml"
    result = AnsibleInfoExtractor(str(blocks)).extract()
    assert_true(
        "ansible.builtin.debug" in result["builtin_modules"]
        and "ansible.builtin.fail" in result["builtin_modules"]
        and "ansible.builtin.file" in result["builtin_modules"],
        "modules inside block, rescue and always are all seen",
    )

    bad = fixtures / "playbooks" / "bad-playbook.yml"
    result = AnsibleInfoExtractor(str(bad)).extract()
    assert_true(
        bool(result["unqualified_actions"]),
        "a playbook of unqualified builtins reports its actions rather than nothing",
    )

    broken = fixtures / "fixtures" / "yaml" / "broken-with-doc-start.yml"
    result = AnsibleInfoExtractor(str(broken)).extract()
    assert_true(bool(result["errors"]), "an unparsable file is an error, not a silent pass")

    print()
    if failed:
        print(f"self-test: {passed} passed, {failed} FAILED")
        return EXIT_FINDINGS
    print(f"self-test: {passed} assertion(s) passed")
    return EXIT_OK


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="extract_ansible_info.py",
        description="Extract module, collection and version information as JSON.",
        epilog="Exit codes: 0 clean, 2 could not run, 64 usage error.",
    )
    parser.add_argument("target", nargs="?", help="playbook, role directory or project directory")
    parser.add_argument("--self-test", action="store_true", help="run against the shipped fixtures")
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return EXIT_USAGE

    if args.self_test:
        return self_test()

    if not args.target:
        print("Usage error: a target path is required. Run with --help.", file=sys.stderr)
        return EXIT_USAGE

    result = AnsibleInfoExtractor(args.target).extract()
    print(json.dumps(result, indent=2))
    if result["errors"]:
        print(
            "BLOCKED: one or more files did not parse. This is exit 2: the "
            "extraction could not run over every file. It is not a pass.",
            file=sys.stderr,
        )
        return EXIT_CANNOT_RUN
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
