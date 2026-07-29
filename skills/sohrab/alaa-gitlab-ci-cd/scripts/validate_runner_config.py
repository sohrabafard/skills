#!/usr/bin/env python3
"""Static validator for GitLab Runner `config.toml` and the Runner Helm `values.yaml`.

Scope, stated so a caller knows what a clean result means:

- It accepts a runner `config.toml`, or a Helm values file that carries a
  positive runner signal (`gitlabUrl`, `runnerToken`, `runnerTokenSecret`, or a
  `runners:` mapping containing `config`).
- A `.gitlab-ci.yml` is not a runner config. Handed one, this script exits 2 and
  names validate_gitlab_ci.py rather than inventing findings about it.
- It reads the file it is given. It does not contact a runner or a cluster.
- It reports facts about how a runner is configured. It does not decide which
  checks must block a pipeline.

Exit codes:
  0  clean
  1  findings (any error; also any warning when --fail-on-warnings is set)
  2  could not run (missing dependency, missing file, unreadable or unparsable
     input, wrong kind of file, bad arguments)

Runs on Windows: pure Python 3.9+, no shell-out, all reads explicitly UTF-8.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_CANNOT_RUN = 2

try:
    import tomllib as toml_reader  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover - exercised on 3.9/3.10
    try:
        import tomli as toml_reader  # type: ignore[no-redef]
    except ModuleNotFoundError:
        import sys

        sys.stderr.write(
            "validate_runner_config.py needs a TOML reader.\n"
            "Python 3.11 and newer ship tomllib. On 3.9 or 3.10, install the "
            "backport: python -m pip install tomli\n"
        )
        raise SystemExit(EXIT_CANNOT_RUN)

try:
    import yaml
except ImportError:  # pragma: no cover - exercised by the documented remediation
    import sys

    sys.stderr.write(
        "validate_runner_config.py needs PyYAML and could not import it.\n"
        "Install it with: python -m pip install PyYAML\n"
    )
    raise SystemExit(EXIT_CANNOT_RUN)


TOMLDecodeError = getattr(toml_reader, "TOMLDecodeError", ValueError)

# A tag that carries no version component names a moving target.
FLOATING_TAGS = {
    "latest", "rootless", "stable", "edge", "main", "master", "dev", "nightly",
    "current", "release", "cli", "dind", "bleeding",
}

# An allowlist entry that wildcards a whole registry or a whole namespace
# constrains nothing: `docker.io/library/*:*` admits every official image.
BROAD_ALLOWLIST_RE = re.compile(r"^\*|/\*(:|$)|^[^/]+/\*")


@dataclass
class Issue:
    path: str
    severity: str
    line: int
    rule: str
    message: str
    suggestion: str | None = None


class CannotRun(Exception):
    """Raised when the checker cannot produce a verdict about the input."""


def make_issue(
    path: Path,
    severity: str,
    rule: str,
    message: str,
    suggestion: str | None = None,
    line: int = 0,
) -> Issue:
    return Issue(str(path), severity, line, rule, message, suggestion)


def build_line_map(text: str) -> dict[str, int]:
    """Map a YAML key or a TOML key/table name to the line that declares it."""
    result: dict[str, int] = {}
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        table = re.match(r"^\[+([^\]]+)\]+", stripped)
        if table:
            result.setdefault(table.group(1).strip(), lineno)
            result.setdefault(table.group(1).strip().split(".")[-1], lineno)
            continue
        assignment = re.match(r"^([A-Za-z0-9_.\"'-]+)\s*[:=]", stripped)
        if assignment:
            result.setdefault(assignment.group(1).strip().strip("\"'"), lineno)
    return result


def split_image(reference: str) -> tuple[str, str | None, str | None]:
    """Split an image reference into (repository, tag, digest).

    A registry host may carry an explicit port, so the colon before a port is not
    a tag separator.
    """
    digest = None
    rest = reference
    if "@" in rest:
        rest, digest = rest.split("@", 1)
    tag = None
    last_colon = rest.rfind(":")
    if last_colon != -1 and "/" not in rest[last_colon:]:
        tag = rest[last_colon + 1 :]
        rest = rest[:last_colon]
    return rest, tag, digest


def check_pinned_image(
    issues: list[Issue],
    path: Path,
    line_map: dict[str, int],
    key: str,
    reference: Any,
    rule: str,
) -> None:
    if not isinstance(reference, str) or not reference:
        return
    _repo, tag, digest = split_image(reference)
    line = line_map.get(key, 0)
    if digest:
        return
    if tag is None:
        issues.append(
            make_issue(
                path,
                "warning",
                rule,
                f"'{key}' is set to {reference!r}, which carries no tag or digest",
                "Every container the runner starts is a supply-chain input. Write a "
                "version tag, or '@sha256:<digest>' where the exact bytes matter.",
                line,
            )
        )
    elif tag.lower() in FLOATING_TAGS or not any(ch.isdigit() for ch in tag):
        issues.append(
            make_issue(
                path,
                "warning",
                rule,
                f"'{key}' is set to {reference!r}, whose tag carries no version",
                "A floating tag changes under you between two jobs. Write a version "
                "tag or a digest.",
                line,
            )
        )


def validate_runner_table(
    path: Path, runner: dict[str, Any], line_map: dict[str, int]
) -> list[Issue]:
    issues: list[Issue] = []
    executor = runner.get("executor")
    if not executor:
        issues.append(
            make_issue(
                path,
                "error",
                "executor-missing",
                "A [[runners]] entry declares no 'executor'",
                "Set executor = \"shell\" or \"kubernetes\" (or the executor this "
                "runner actually uses)",
                line_map.get("runners", 0),
            )
        )
        return issues

    if executor == "shell":
        issues.append(
            make_issue(
                path,
                "warning",
                "shell-risk",
                "Shell executor runs job scripts directly on the host as the runner "
                "user",
                "Use it only where the host, the projects and every branch that can "
                "reach it are trusted",
                line_map.get("executor", 0),
            )
        )
        if not runner.get("builds_dir"):
            issues.append(
                make_issue(
                    path,
                    "note",
                    "shell-builds-dir",
                    "Shell runner sets no 'builds_dir'",
                    "The build directory persists between jobs on a shell runner. "
                    "Name it so cleanup and disk placement are auditable.",
                    line_map.get("executor", 0),
                )
            )
        if not runner.get("cache_dir"):
            issues.append(
                make_issue(
                    path,
                    "note",
                    "shell-cache-dir",
                    "Shell runner sets no 'cache_dir'",
                    "Name it so two projects on this host cannot silently share one "
                    "cache location",
                    line_map.get("executor", 0),
                )
            )

    if executor == "kubernetes":
        kube = runner.get("kubernetes") or {}
        if not isinstance(kube, dict):
            issues.append(
                make_issue(
                    path,
                    "error",
                    "kube-config-type",
                    "[runners.kubernetes] must be a table",
                    line=line_map.get("runners.kubernetes", 0),
                )
            )
            return issues

        kube_line = line_map.get("runners.kubernetes", 0)

        if kube.get("privileged") is True:
            issues.append(
                make_issue(
                    path,
                    "warning",
                    "kube-privileged",
                    "Kubernetes runner starts privileged build containers",
                    "A privileged container can reach the node. Keep this runner on a "
                    "dedicated fleet and dedicated nodes.",
                    kube_line,
                )
            )
            if not kube.get("node_selector"):
                issues.append(
                    make_issue(
                        path,
                        "warning",
                        "kube-privileged-node-selector",
                        "Privileged Kubernetes runner sets no node_selector",
                        "Without one, privileged job pods schedule onto general "
                        "nodes. Pin them to isolated nodes.",
                        kube_line,
                    )
                )

        allowed_images = kube.get("allowed_images") or []
        if not allowed_images:
            issues.append(
                make_issue(
                    path,
                    "note",
                    "kube-allowed-images",
                    "Kubernetes runner does not restrict allowed_images",
                    "Unset is equivalent to ['*/*:*']: any project using this runner "
                    "picks any image",
                    kube_line,
                )
            )
        else:
            for entry in allowed_images:
                if isinstance(entry, str) and BROAD_ALLOWLIST_RE.search(entry):
                    issues.append(
                        make_issue(
                            path,
                            "warning",
                            "kube-allowlist-too-broad",
                            f"allowed_images entry {entry!r} wildcards a whole "
                            "registry or namespace",
                            "An allowlist that admits every image in a namespace "
                            "constrains nothing. List the repositories this runner "
                            "actually needs, with a tag pattern that carries a "
                            "version.",
                            kube_line,
                        )
                    )

        if not kube.get("allowed_services"):
            issues.append(
                make_issue(
                    path,
                    "note",
                    "kube-allowed-services",
                    "Kubernetes runner does not restrict allowed_services",
                    "Unset admits any service container, including a DinD image on a "
                    "runner that is not meant to run one",
                    kube_line,
                )
            )

        pull_policies = kube.get("allowed_pull_policies") or []
        if isinstance(pull_policies, str):
            pull_policies = [pull_policies]
        if not pull_policies:
            issues.append(
                make_issue(
                    path,
                    "note",
                    "kube-pull-policies",
                    "Kubernetes runner does not restrict allowed_pull_policies",
                    "Unset lets a project choose 'if-not-present' and run whatever "
                    "layer is already cached on the node",
                    kube_line,
                )
            )
        elif any(str(item) == "if-not-present" for item in pull_policies):
            issues.append(
                make_issue(
                    path,
                    "warning",
                    "kube-if-not-present",
                    "Runner allows the 'if-not-present' pull policy",
                    "On a shared node a cached layer under a reused tag is served to "
                    "the next project. Allow it only where every image and every "
                    "user of this runner is trusted.",
                    kube_line,
                )
            )

        configured_pull = kube.get("pull_policy")
        if configured_pull is not None and pull_policies:
            configured = (
                configured_pull if isinstance(configured_pull, list) else [configured_pull]
            )
            allowed = {str(item) for item in pull_policies}
            for item in configured:
                if str(item) not in allowed:
                    issues.append(
                        make_issue(
                            path,
                            "error",
                            "kube-pull-policy-conflict",
                            f"pull_policy {str(item)!r} is not in allowed_pull_policies "
                            f"{sorted(allowed)}",
                            "The runner rejects its own default and every job fails "
                            "at pod creation. Make the default a member of the "
                            "allowlist.",
                            kube_line,
                        )
                    )

        if not kube.get("image_pull_secrets"):
            issues.append(
                make_issue(
                    path,
                    "note",
                    "kube-image-pull-secrets",
                    "Kubernetes runner sets no image_pull_secrets",
                    "Every job pod starts a build container, a helper container and "
                    "an init-permissions container, and all three pull. If any of "
                    "them comes from a private registry, name the docker-registry "
                    "secret here; the manager pod's own pull configuration does not "
                    "apply to job pods.",
                    kube_line,
                )
            )

        check_pinned_image(issues, path, line_map, "image", kube.get("image"), "kube-image-unpinned")
        check_pinned_image(
            issues, path, line_map, "helper_image", kube.get("helper_image"), "kube-helper-image-unpinned"
        )
        if not kube.get("helper_image"):
            issues.append(
                make_issue(
                    path,
                    "note",
                    "kube-helper-image-unset",
                    "Kubernetes runner does not set helper_image",
                    "The default helper image is pulled from GitLab's registry at job "
                    "time. In a restricted-egress cluster, mirror it and set "
                    "helper_image to the mirrored, version-tagged reference.",
                    kube_line,
                )
            )

        if kube.get("namespace_per_job") is True:
            issues.append(
                make_issue(
                    path,
                    "note",
                    "kube-namespace-per-job",
                    "Runner creates a namespace per job",
                    "This needs cluster-scoped create and delete rights on namespaces. "
                    "Confirm the service account has them before shipping.",
                    kube_line,
                )
            )
        if kube.get("pod_spec"):
            issues.append(
                make_issue(
                    path,
                    "note",
                    "kube-pod-spec",
                    "Runner patches the job pod through pod_spec",
                    "pod_spec is behind a feature flag and overrides the executor's "
                    "own fields. Keep each patch small and state which flag it needs.",
                    kube_line,
                )
            )

        cache = runner.get("cache") or {}
        cache_type = cache.get("Type") or cache.get("type") if isinstance(cache, dict) else None
        if not cache_type:
            issues.append(
                make_issue(
                    path,
                    "warning",
                    "kube-cache-not-distributed",
                    "Kubernetes runner declares no [runners.cache] Type",
                    "Each job runs in a new pod, so a cache written to the pod's own "
                    "filesystem is gone when the pod is. Without distributed cache "
                    "storage every 'cache:' key in every pipeline on this runner is a "
                    "no-op. Set Type and its credentials, or state in the pipeline "
                    "that caching is deliberately off.",
                    line_map.get("runners.cache", kube_line),
                )
            )

    return issues


def validate_toml_file(path: Path) -> list[Issue]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise CannotRun(f"File not found: {path}")
    except OSError as exc:
        raise CannotRun(f"Could not read {path}: {exc}")
    except UnicodeDecodeError as exc:
        raise CannotRun(f"{path} is not valid UTF-8: {exc}")
    try:
        data = toml_reader.loads(text)
    except TOMLDecodeError as exc:
        raise CannotRun(f"TOML syntax error in {path}: {exc}")

    line_map = build_line_map(text)
    issues: list[Issue] = []

    concurrent = data.get("concurrent")
    if concurrent is None:
        issues.append(
            make_issue(
                path,
                "warning",
                "concurrent-unset",
                "'concurrent' is not set, so this runner process runs one job at a time",
                "Set it from the host's own capacity: one slot per CPU core the "
                "heaviest job needs, bounded by memory and by any resource this "
                "runner's jobs share.",
                line_map.get("concurrent", 0),
            )
        )
    elif isinstance(concurrent, int) and concurrent <= 0:
        issues.append(
            make_issue(
                path,
                "error",
                "concurrent-zero",
                f"'concurrent = {concurrent}' stops this runner picking up any job",
                "Set a positive slot count derived from host capacity",
                line_map.get("concurrent", 0),
            )
        )

    runners = data.get("runners")
    if isinstance(runners, list):
        for runner in runners:
            if isinstance(runner, dict):
                issues.extend(validate_runner_table(path, runner, line_map))
    else:
        issues.append(
            make_issue(
                path,
                "error",
                "runners-missing",
                "No [[runners]] entries found",
                "A runner config.toml declares at least one [[runners]] table",
                1,
            )
        )
    return issues


HELM_SIGNALS = ("gitlabUrl", "runnerToken", "runnerTokenSecret", "runnerRegistrationToken")


def looks_like_runner_values(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    if any(key in data for key in HELM_SIGNALS):
        return True
    runners = data.get("runners")
    return isinstance(runners, dict) and "config" in runners


def validate_values_yaml(path: Path) -> list[Issue]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise CannotRun(f"File not found: {path}")
    except OSError as exc:
        raise CannotRun(f"Could not read {path}: {exc}")
    except UnicodeDecodeError as exc:
        raise CannotRun(f"{path} is not valid UTF-8: {exc}")
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise CannotRun(f"YAML syntax error in {path}: {exc}")

    if not isinstance(data, dict):
        raise CannotRun(f"{path}: a Helm values file must have a mapping at its root")

    if not looks_like_runner_values(data):
        raise CannotRun(
            f"{path} is not a GitLab Runner Helm values file: it declares none of "
            f"{', '.join(HELM_SIGNALS)} and no 'runners.config'. "
            "If this is a pipeline file, run validate_gitlab_ci.py instead."
        )

    line_map = build_line_map(text)
    issues: list[Issue] = []

    if not data.get("gitlabUrl"):
        issues.append(
            make_issue(
                path,
                "error",
                "gitlab-url-missing",
                "values.yaml declares no gitlabUrl",
                "The chart cannot register the runner without it",
                line_map.get("gitlabUrl", 1),
            )
        )
    if data.get("runnerRegistrationToken"):
        issues.append(
            make_issue(
                path,
                "warning",
                "registration-token-deprecated",
                "values.yaml uses runnerRegistrationToken",
                "GitLab's current workflow issues a runner authentication token "
                "(prefix 'glrt-') and instance administrators have been able to "
                "disable legacy registration since GitLab 17.0. Use runnerToken or "
                "runnerTokenSecret.",
                line_map.get("runnerRegistrationToken", 0),
            )
        )
    if not data.get("runnerToken") and not data.get("runnerTokenSecret"):
        issues.append(
            make_issue(
                path,
                "warning",
                "runner-token-missing",
                "values.yaml declares neither runnerToken nor runnerTokenSecret",
                "Supply the authentication token directly, or name the Kubernetes "
                "secret that holds it",
                1,
            )
        )

    rbac = data.get("rbac") or {}
    sa = data.get("serviceAccount") or {}
    if isinstance(rbac, dict) and rbac.get("create") is False:
        if not (isinstance(sa, dict) and sa.get("name")):
            issues.append(
                make_issue(
                    path,
                    "warning",
                    "service-account-missing",
                    "rbac.create is false and no serviceAccount.name is set",
                    "The chart falls back to the namespace default service account, "
                    "whose rights nobody declared. Name the account the cluster "
                    "administrator prepared.",
                    line_map.get("rbac", 0),
                )
            )

    runners_block = data.get("runners") or {}
    if not isinstance(runners_block, dict):
        issues.append(
            make_issue(
                path,
                "error",
                "runners-block-type",
                "The 'runners' block must be a mapping",
                line=line_map.get("runners", 0),
            )
        )
        return issues

    if runners_block.get("privileged") is True:
        issues.append(
            make_issue(
                path,
                "warning",
                "helm-privileged",
                "values.yaml enables privileged job pods",
                "Keep this release on a dedicated node pool and restrict it to "
                "trusted projects and protected refs",
                line_map.get("privileged", 0),
            )
        )

    config_text = runners_block.get("config")
    if not config_text:
        issues.append(
            make_issue(
                path,
                "warning",
                "runners-config-missing",
                "values.yaml has no runners.config block",
                "Without it the chart renders defaults nobody reviewed. Embed the "
                "runner TOML under runners.config.",
                line_map.get("runners", 0),
            )
        )
        return issues

    try:
        parsed = toml_reader.loads(config_text)
    except TOMLDecodeError as exc:
        issues.append(
            make_issue(
                path,
                "error",
                "embedded-toml",
                f"runners.config is not valid TOML: {exc}",
                "values.yaml is YAML, but runners.config is embedded TOML. Colons and "
                "YAML indentation do not work inside it.",
                line_map.get("config", 0),
            )
        )
        return issues

    embedded_line_map = build_line_map(config_text)
    offset = line_map.get("config", 0)
    embedded_line_map = {k: v + offset for k, v in embedded_line_map.items()}

    runners = parsed.get("runners")
    if isinstance(runners, list):
        for runner in runners:
            if isinstance(runner, dict):
                issues.extend(validate_runner_table(path, runner, embedded_line_map))
    else:
        issues.append(
            make_issue(
                path,
                "error",
                "embedded-runners-missing",
                "No [[runners]] entries inside runners.config",
                line=line_map.get("config", 0),
            )
        )

    return issues


def validate_file(path: Path) -> list[Issue]:
    """Route on content, not on file extension."""
    if not path.exists():
        raise CannotRun(f"File not found: {path}")
    suffix = path.suffix.lower()
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise CannotRun(f"Could not read {path}: {exc}")
    except UnicodeDecodeError as exc:
        raise CannotRun(f"{path} is not valid UTF-8: {exc}")

    if suffix == ".toml" or ("[[runners]]" in text and suffix not in {".yaml", ".yml"}):
        return validate_toml_file(path)
    if suffix in {".yaml", ".yml"}:
        return validate_values_yaml(path)
    if "[[runners]]" in text:
        return validate_toml_file(path)
    raise CannotRun(
        f"{path} is neither runner TOML nor a Runner Helm values file. "
        "For a pipeline file, run validate_gitlab_ci.py instead."
    )


def render(issues: list[Issue], as_json: bool) -> None:
    severity_order = {"error": 0, "warning": 1, "note": 2}
    issues.sort(key=lambda i: (i.path, severity_order.get(i.severity, 99), i.line, i.rule))
    if as_json:
        print(json.dumps([asdict(i) for i in issues], indent=2))
        return
    if not issues:
        print("No issues found.")
        return
    for item in issues:
        line_part = f":{item.line}" if item.line else ""
        print(f"{item.severity.upper():7} {item.path}{line_part} [{item.rule}] {item.message}")
        if item.suggestion:
            print(f"         suggestion: {item.suggestion}")


def fixtures_dir() -> Path:
    return Path(__file__).resolve().parent / "fixtures"


SELF_TEST_EXPECTATIONS: dict[str, dict[str, Any]] = {
    "runner-good.config.toml": {"absent": {"*"}},
    "runner-hazards.config.toml": {
        "present": {
            "concurrent-zero",
            "kube-privileged",
            "kube-privileged-node-selector",
            "kube-if-not-present",
            "kube-pull-policy-conflict",
            "kube-allowlist-too-broad",
            "kube-image-unpinned",
            "kube-helper-image-unpinned",
            "kube-cache-not-distributed",
        },
        "absent": {"kube-rofs-paths"},
    },
    "runner-values.yaml": {
        "present": {"registration-token-deprecated", "service-account-missing"},
    },
}


def self_test() -> int:
    base = fixtures_dir()
    if not base.is_dir():
        print(f"SELF-TEST CANNOT RUN: fixtures directory not found at {base}")
        return EXIT_CANNOT_RUN

    failures: list[str] = []
    checked = 0
    for name, expectation in sorted(SELF_TEST_EXPECTATIONS.items()):
        fixture = base / name
        if not fixture.is_file():
            print(f"SELF-TEST CANNOT RUN: missing fixture {fixture}")
            return EXIT_CANNOT_RUN
        try:
            issues = validate_file(fixture)
        except CannotRun as exc:
            print(f"SELF-TEST CANNOT RUN: {exc}")
            return EXIT_CANNOT_RUN
        checked += 1
        rules = {i.rule for i in issues}
        expected_absent = expectation.get("absent", set())
        if "*" in expected_absent:
            if issues:
                failures.append(f"{name}: expected no findings, got {sorted(rules)}")
        else:
            for rule in sorted(expected_absent):
                if rule in rules:
                    failures.append(f"{name}: rule '{rule}' should not fire")
        for rule in sorted(expectation.get("present", set())):
            if rule not in rules:
                failures.append(f"{name}: expected rule '{rule}', got {sorted(rules)}")
        if any(i.line == 0 for i in issues):
            failures.append(f"{name}: some findings carry no line number")

    # The misrouting defect: a pipeline file must never produce runner findings.
    pipeline = base / "good-pipeline.gitlab-ci.yml"
    if pipeline.is_file():
        try:
            validate_file(pipeline)
        except CannotRun:
            pass
        else:
            failures.append("a pipeline file was accepted as a Helm values file")
    else:
        failures.append(f"missing fixture {pipeline}")

    try:
        validate_file(base / "does-not-exist.toml")
    except CannotRun:
        pass
    else:
        failures.append("a missing file did not raise CannotRun")

    if failures:
        print(f"SELF-TEST FAILED ({len(failures)} problems across {checked} fixtures):")
        for line in failures:
            print(f"  - {line}")
        return EXIT_FINDINGS
    print(f"SELF-TEST PASSED: {checked} fixtures, {len(SELF_TEST_EXPECTATIONS)} expectation sets.")
    return EXIT_CLEAN


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="validate_runner_config.py",
        description=(
            "Validate a GitLab Runner config.toml or a Runner Helm values.yaml. "
            "Routes on file content, not on file extension."
        ),
        epilog=(
            "Exit codes: 0 clean, 1 findings, 2 could not run. Handed a pipeline "
            "file, this script exits 2 and names validate_gitlab_ci.py."
        ),
    )
    parser.add_argument("paths", nargs="*", help="Runner config.toml or Helm values.yaml")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit JSON")
    parser.add_argument(
        "--fail-on-warnings",
        action="store_true",
        help="Exit 1 when warnings are present, not only when errors are",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run the bundled fixture corpus in scripts/fixtures and report pass or fail",
    )
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    if not args.paths:
        parser.print_usage()
        print("error: give at least one file, or use --self-test")
        return EXIT_CANNOT_RUN

    issues: list[Issue] = []
    blocked = False
    for raw in args.paths:
        try:
            issues.extend(validate_file(Path(raw)))
        except CannotRun as exc:
            print(f"CANNOT RUN: {exc}")
            blocked = True

    if blocked:
        return EXIT_CANNOT_RUN

    render(issues, args.json_output)

    if any(i.severity == "error" for i in issues):
        return EXIT_FINDINGS
    if args.fail_on_warnings and any(i.severity == "warning" for i in issues):
        return EXIT_FINDINGS
    return EXIT_CLEAN


if __name__ == "__main__":
    raise SystemExit(main())
