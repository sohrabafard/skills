#!/usr/bin/env python3
"""Static validator for GitLab Runner config.toml and Helm values.yaml."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import yaml


@dataclass
class Issue:
    path: str
    severity: str
    line: int
    rule: str
    message: str
    suggestion: str | None = None


def make_issue(path: Path, severity: str, rule: str, message: str, suggestion: str | None = None, line: int = 0) -> Issue:
    return Issue(str(path), severity, line, rule, message, suggestion)


def build_line_map(text: str) -> dict[str, int]:
    result: dict[str, int] = {}
    for lineno, line in enumerate(text.splitlines(), start=1):
        m = re.match(r"^(\s*)([A-Za-z0-9_.-]+):", line)
        if m:
            result.setdefault(m.group(2), lineno)
    return result


def validate_runner_table(path: Path, runner: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    executor = runner.get("executor")
    if not executor:
        issues.append(make_issue(path, "error", "executor-missing", "Runner is missing 'executor'"))
        return issues

    if executor == "shell":
        issues.append(make_issue(path, "warning", "shell-risk", "Shell executor has weak isolation", "Use it only for trusted workloads on a trusted host"))
        if not runner.get("builds_dir"):
            issues.append(make_issue(path, "note", "shell-builds-dir", "Shell runner does not set 'builds_dir'", "Set explicit paths when filesystem placement and cleanup matter"))
        if not runner.get("cache_dir"):
            issues.append(make_issue(path, "note", "shell-cache-dir", "Shell runner does not set 'cache_dir'", "Set explicit paths when cache placement matters"))

    if executor == "kubernetes":
        kube = runner.get("kubernetes") or {}
        if not isinstance(kube, dict):
            issues.append(make_issue(path, "error", "kube-config-type", "[runners.kubernetes] must be a table"))
            return issues
        if kube.get("privileged") is True:
            issues.append(make_issue(path, "warning", "kube-privileged", "Kubernetes runner is privileged", "Use a dedicated privileged runner fleet and dedicated nodes"))
            if not kube.get("node_selector"):
                issues.append(make_issue(path, "warning", "kube-privileged-node-selector", "Privileged Kubernetes runner has no node selector", "Pin privileged jobs to isolated nodes"))
        if not kube.get("allowed_images"):
            issues.append(make_issue(path, "note", "kube-allowed-images", "Kubernetes runner does not restrict allowed_images", "Add an allowlist when the trust model is not fully closed"))
        if not kube.get("allowed_services"):
            issues.append(make_issue(path, "note", "kube-allowed-services", "Kubernetes runner does not restrict allowed_services", "Add an allowlist when service containers should be limited"))
        pull_policies = kube.get("allowed_pull_policies") or []
        if isinstance(pull_policies, str):
            pull_policies = [pull_policies]
        if not pull_policies:
            issues.append(make_issue(path, "note", "kube-pull-policies", "Kubernetes runner does not restrict allowed_pull_policies", "Restrict pull policies if users should not choose freely"))
        elif any(str(item) == "if-not-present" for item in pull_policies):
            issues.append(make_issue(path, "warning", "kube-if-not-present", "Runner allows 'if-not-present' pull policy", "Use it only on fully trusted runners and images"))
        if kube.get("namespace_per_job") is True:
            issues.append(make_issue(path, "note", "kube-namespace-per-job", "Runner uses namespace_per_job", "Verify RBAC can create and delete namespaces"))
        if kube.get("pod_spec"):
            issues.append(make_issue(path, "note", "kube-pod-spec", "Runner uses advanced pod_spec customization", "Keep pod_spec patches small and verify required feature flags"))
        rofs = False
        pod_sec = kube.get("pod_security_context") or {}
        if isinstance(pod_sec, dict) and pod_sec.get("read_only_root_filesystem") is True:
            rofs = True
        build_sec = kube.get("build_container_security_context") or {}
        if isinstance(build_sec, dict) and build_sec.get("read_only_root_filesystem") is True:
            rofs = True
        if rofs:
            if not kube.get("logs_base_dir") or not kube.get("scripts_base_dir"):
                issues.append(make_issue(path, "warning", "kube-rofs-paths", "Runner enables read-only root filesystem without logs_base_dir and scripts_base_dir", "Provide writable paths for logs and scripts"))

    return issues


def validate_toml_file(path: Path) -> list[Issue]:
    try:
        text = path.read_text(encoding="utf-8")
        data = tomllib.loads(text)
    except FileNotFoundError:
        return [make_issue(path, "error", "file-not-found", f"File not found: {path}")]
    except tomllib.TOMLDecodeError as exc:
        return [make_issue(path, "error", "toml-syntax", f"TOML syntax error: {exc}")]
    except Exception as exc:
        return [make_issue(path, "error", "file-read-error", f"Could not read file: {exc}")]

    issues: list[Issue] = []
    runners = data.get("runners")
    if isinstance(runners, list):
        for runner in runners:
            if isinstance(runner, dict):
                issues.extend(validate_runner_table(path, runner))
    else:
        issues.append(make_issue(path, "error", "runners-missing", "No [[runners]] entries found"))
    return issues


def validate_values_yaml(path: Path) -> list[Issue]:
    try:
        text = path.read_text(encoding="utf-8")
        data = yaml.safe_load(text)
    except FileNotFoundError:
        return [make_issue(path, "error", "file-not-found", f"File not found: {path}")]
    except yaml.YAMLError as exc:
        return [make_issue(path, "error", "yaml-syntax", f"YAML syntax error: {exc}")]
    except Exception as exc:
        return [make_issue(path, "error", "file-read-error", f"Could not read file: {exc}")]

    if not isinstance(data, dict):
        return [make_issue(path, "error", "yaml-root", "values.yaml root must be a mapping")]

    line_map = build_line_map(text)
    issues: list[Issue] = []

    if not data.get("gitlabUrl"):
        issues.append(make_issue(path, "error", "gitlab-url-missing", "values.yaml is missing gitlabUrl"))
    if data.get("runnerRegistrationToken"):
        issues.append(make_issue(path, "warning", "registration-token-deprecated", "values.yaml uses runnerRegistrationToken", "Prefer runnerToken with the current runner authentication-token workflow"))
    if not data.get("runnerToken") and not data.get("runnerTokenSecret"):
        issues.append(make_issue(path, "warning", "runner-token-missing", "values.yaml does not declare runnerToken or runnerTokenSecret", "Provide a runner authentication token directly or through a Kubernetes secret"))

    rbac = data.get("rbac") or {}
    sa = data.get("serviceAccount") or {}
    if isinstance(rbac, dict) and rbac.get("create") is False:
        if not (isinstance(sa, dict) and sa.get("name")):
            issues.append(make_issue(path, "warning", "service-account-missing", "rbac.create is false but no explicit serviceAccount.name is configured", "Use an existing service account and name it explicitly"))

    runners_block = data.get("runners") or {}
    if not isinstance(runners_block, dict):
        issues.append(make_issue(path, "error", "runners-block-type", "values.yaml runners block must be a mapping"))
        return issues

    if runners_block.get("privileged") is True:
        issues.append(make_issue(path, "warning", "helm-privileged", "values.yaml enables privileged runner pods", "Restrict this runner to trusted workloads and isolated nodes"))

    config_text = runners_block.get("config")
    if not config_text:
        issues.append(make_issue(path, "warning", "runners-config-missing", "values.yaml has no runners.config block", "Embed TOML runner configuration in runners.config"))
        return issues

    try:
        parsed = tomllib.loads(config_text)
    except tomllib.TOMLDecodeError as exc:
        issues.append(make_issue(path, "error", "embedded-toml", f"runners.config is not valid TOML: {exc}", "Remember that runners.config uses TOML syntax, not YAML"))
        return issues

    runners = parsed.get("runners")
    if isinstance(runners, list):
        for runner in runners:
            if isinstance(runner, dict):
                issues.extend(validate_runner_table(path, runner))
    else:
        issues.append(make_issue(path, "error", "embedded-runners-missing", "No [[runners]] entries found inside runners.config"))

    return issues


def detect_kind(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".toml":
        return "toml"
    if suffix in {".yaml", ".yml"}:
        return "yaml"
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return "unknown"
    if "[[runners]]" in text:
        return "toml"
    if "gitlabUrl:" in text or "runners:" in text:
        return "yaml"
    return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate GitLab Runner config.toml or Helm values.yaml")
    parser.add_argument("paths", nargs="+", help="Files to validate")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit JSON instead of text")
    parser.add_argument("--fail-on-warnings", action="store_true", help="Return non-zero if warnings are found")
    args = parser.parse_args()

    issues: list[Issue] = []
    for raw in args.paths:
        path = Path(raw)
        kind = detect_kind(path)
        if kind == "toml":
            issues.extend(validate_toml_file(path))
        elif kind == "yaml":
            issues.extend(validate_values_yaml(path))
        else:
            issues.append(make_issue(path, "error", "file-type", "Could not determine whether the file is runner TOML or Helm YAML"))

    severity_order = {"error": 0, "warning": 1, "note": 2}
    issues.sort(key=lambda i: (i.path, severity_order.get(i.severity, 99), i.rule))

    if args.json_output:
        print(json.dumps([asdict(i) for i in issues], indent=2))
    else:
        if not issues:
            print("No issues found.")
        else:
            for item in issues:
                print(f"{item.severity.upper():7} {item.path} [{item.rule}] {item.message}")
                if item.suggestion:
                    print(f"         suggestion: {item.suggestion}")

    has_error = any(i.severity == "error" for i in issues)
    has_warning = any(i.severity == "warning" for i in issues)
    if has_error:
        return 1
    if args.fail_on_warnings and has_warning:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
