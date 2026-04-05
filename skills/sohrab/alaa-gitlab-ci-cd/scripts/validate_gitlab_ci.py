#!/usr/bin/env python3
"""Static GitLab CI/CD validator.

Purpose:
- Fast local feedback before CI Lint.
- Conservative checks for syntax, structure, variable pitfalls, and common security issues.
- Supports one or more YAML files.

This script intentionally does not try to fully reimplement GitLab's parser.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable

import yaml

GLOBAL_KEYWORDS = {
    "default",
    "include",
    "stages",
    "types",
    "variables",
    "workflow",
    "spec",
    "image",
    "services",
    "before_script",
    "after_script",
    "cache",
    "pages",
}

RESERVED_NAMES = {
    "image",
    "services",
    "stages",
    "types",
    "before_script",
    "after_script",
    "variables",
    "cache",
    "include",
    "pages",
    "default",
    "workflow",
    "spec",
}

VALID_WHEN = {"on_success", "on_failure", "always", "manual", "delayed", "never"}
SECRET_NAME_RE = re.compile(r"(?:TOKEN|PASSWORD|PASS|SECRET|PRIVATE[_-]?KEY|ACCESS[_-]?KEY)", re.IGNORECASE)
INLINE_SECRET_VALUE_RE = re.compile(r"^[A-Za-z0-9+/=_-]{16,}$")
VAR_IN_PATH_RE = re.compile(r"\$[{A-Za-z_]")
RULES_IF_BRACE_VAR_RE = re.compile(r"\$\{[A-Za-z_][A-Za-z0-9_]*\}")
LATEST_TAG_RE = re.compile(r"(^|:)latest$")
UNPINNED_IMAGE_RE = re.compile(r"^[^:@]+$")
DIND_RE = re.compile(r"(^|/)docker(?::[0-9][^\s]*)?-dind$")


@dataclass
class Issue:
    path: str
    severity: str
    line: int
    rule: str
    message: str
    suggestion: str | None = None


def build_line_map(text: str) -> dict[str, int]:
    result: dict[str, int] = {}
    for lineno, line in enumerate(text.splitlines(), start=1):
        m = re.match(r"^(\s*)([A-Za-z0-9_.-]+):", line)
        if m:
            key = m.group(2)
            result.setdefault(key, lineno)
            result.setdefault(f"{len(m.group(1))}:{key}", lineno)
    return result


def issue(path: Path, severity: str, line: int, rule: str, message: str, suggestion: str | None = None) -> Issue:
    return Issue(str(path), severity, line, rule, message, suggestion)


def load_yaml(path: Path) -> tuple[dict[str, Any] | None, list[Issue], dict[str, int], str]:
    issues: list[Issue] = []
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None, [issue(path, "error", 0, "file-not-found", f"File not found: {path}")], {}, ""
    except Exception as exc:
        return None, [issue(path, "error", 0, "file-read-error", f"Could not read file: {exc}")], {}, ""

    line_map = build_line_map(text)

    try:
        docs = list(yaml.safe_load_all(text))
    except yaml.YAMLError as exc:
        line = getattr(getattr(exc, "problem_mark", None), "line", 0) + 1
        return None, [issue(path, "error", line, "yaml-syntax", f"YAML syntax error: {exc}")], line_map, text

    if not docs:
        return None, [issue(path, "error", 1, "yaml-empty", "Empty YAML file")], line_map, text

    if len(docs) == 1:
        config = docs[0]
    elif len(docs) == 2 and isinstance(docs[0], dict) and isinstance(docs[1], dict):
        # Common GitLab component layout: header doc with spec, then main config doc.
        config = dict(docs[1])
        for key, value in docs[0].items():
            if key not in config:
                config[key] = value
    else:
        return None, [issue(path, "error", 1, "yaml-documents", "Use a single GitLab config document, or a two-document component file with a header doc and the main config")], line_map, text

    if not isinstance(config, dict):
        return None, [issue(path, "error", 1, "yaml-root", "GitLab CI/CD config root must be a mapping")], line_map, text

    return config, issues, line_map, text


def get_line(line_map: dict[str, int], key: str, indent: int | None = None) -> int:
    if indent is not None:
        specific = line_map.get(f"{indent}:{key}")
        if specific:
            return specific
    return line_map.get(key, 0)


def iter_jobs(config: dict[str, Any]) -> Iterable[tuple[str, dict[str, Any]]]:
    for name, value in config.items():
        if name in GLOBAL_KEYWORDS:
            continue
        if isinstance(value, dict):
            yield name, value


def normalize_script(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def scan_hardcoded_secrets(path: Path, config: dict[str, Any], line_map: dict[str, int]) -> list[Issue]:
    issues: list[Issue] = []
    for scope_key in ("variables",):
        vars_obj = config.get(scope_key)
        if isinstance(vars_obj, dict):
            for key, value in vars_obj.items():
                if SECRET_NAME_RE.search(str(key)):
                    if isinstance(value, str) and value and not value.startswith("$") and INLINE_SECRET_VALUE_RE.match(value):
                        issues.append(issue(path, "warning", get_line(line_map, str(key)), "secret-inline", f"Variable '{key}' looks like a hardcoded secret", "Move the value to a protected or file variable in GitLab settings"))
    for job_name, job in iter_jobs(config):
        vars_obj = job.get("variables")
        if isinstance(vars_obj, dict):
            for key, value in vars_obj.items():
                if SECRET_NAME_RE.search(str(key)):
                    if isinstance(value, str) and value and not value.startswith("$") and INLINE_SECRET_VALUE_RE.match(value):
                        issues.append(issue(path, "warning", get_line(line_map, job_name), "secret-inline", f"Job '{job_name}' contains a variable that looks like a hardcoded secret: {key}", "Move the value to project, group, or environment-scoped variables"))
    return issues


def validate_config(path: Path) -> list[Issue]:
    config, issues, line_map, _text = load_yaml(path)
    if config is None:
        return issues

    out = list(issues)

    stages = config.get("stages")
    declared_stages: list[str] = []
    if stages is not None:
        if not isinstance(stages, list):
            out.append(issue(path, "error", get_line(line_map, "stages"), "stages-type", "'stages' must be a list"))
        else:
            seen: set[str] = set()
            for stage in stages:
                if not isinstance(stage, str):
                    out.append(issue(path, "error", get_line(line_map, "stages"), "stage-type", f"Stage names must be strings, got {type(stage).__name__}"))
                    continue
                declared_stages.append(stage)
                if stage in seen:
                    out.append(issue(path, "warning", get_line(line_map, "stages"), "stage-duplicate", f"Duplicate stage '{stage}'"))
                seen.add(stage)

    has_workflow = isinstance(config.get("workflow"), dict)
    any_rules = False
    any_mr_rule = False

    job_names = {name for name, _ in iter_jobs(config)}

    for job_name, job in iter_jobs(config):
        job_line = get_line(line_map, job_name)
        if job_name in RESERVED_NAMES and not job_name.startswith("."):
            out.append(issue(path, "error", job_line, "job-name-reserved", f"Job name '{job_name}' conflicts with a reserved top-level keyword"))

        if not isinstance(job, dict):
            out.append(issue(path, "error", job_line, "job-type", f"Job '{job_name}' must be a mapping"))
            continue

        if not job_name.startswith(".") and not any(key in job for key in ("script", "run", "trigger", "release")):
            out.append(issue(path, "warning", job_line, "job-action-missing", f"Job '{job_name}' has no 'script', 'run', 'trigger', or 'release'", "Hidden template jobs are fine without actions, but concrete jobs usually need one"))

        if "only" in job or "except" in job:
            out.append(issue(path, "warning", job_line, "only-except", f"Job '{job_name}' uses 'only' or 'except'", "Prefer 'workflow:rules' and job 'rules' for new work"))

        if "stage" in job and declared_stages and job["stage"] not in declared_stages:
            out.append(issue(path, "error", job_line, "stage-missing", f"Job '{job_name}' references undefined stage '{job['stage']}'"))

        if "when" in job and job["when"] not in VALID_WHEN:
            out.append(issue(path, "error", job_line, "when-invalid", f"Job '{job_name}' uses invalid 'when' value '{job['when']}'"))

        if "extends" in job:
            parents = job["extends"] if isinstance(job["extends"], list) else [job["extends"]]
            for parent in parents:
                if isinstance(parent, str) and parent not in job_names:
                    out.append(issue(path, "error", job_line, "extends-missing", f"Job '{job_name}' extends unknown job or template '{parent}'"))

        if "needs" in job:
            needs = job["needs"]
            items = needs if isinstance(needs, list) else [needs]
            for need in items:
                if isinstance(need, str):
                    target = need
                elif isinstance(need, dict):
                    target = need.get("job")
                else:
                    target = None
                if isinstance(target, str) and target not in job_names:
                    out.append(issue(path, "error", job_line, "needs-missing", f"Job '{job_name}' needs unknown job '{target}'"))

        if "dependencies" in job:
            deps = job["dependencies"] if isinstance(job["dependencies"], list) else [job["dependencies"]]
            for dep in deps:
                if isinstance(dep, str) and dep not in job_names:
                    out.append(issue(path, "error", job_line, "dependencies-missing", f"Job '{job_name}' depends on unknown job '{dep}'"))

        rules = job.get("rules")
        if isinstance(rules, list):
            any_rules = True
            for rule in rules:
                if not isinstance(rule, dict):
                    continue
                if_cond = rule.get("if")
                if isinstance(if_cond, str):
                    if RULES_IF_BRACE_VAR_RE.search(if_cond):
                        out.append(issue(path, "warning", job_line, "rules-if-brace-var", f"Job '{job_name}' uses '${{VAR}}' style in rules:if", "Use '$VAR' inside rules:if expressions"))
                    if "merge_request_event" in if_cond:
                        any_mr_rule = True
                for key in ("changes", "exists", "compare_to"):
                    value = rule.get(key)
                    candidates: list[str] = []
                    if isinstance(value, str):
                        candidates = [value]
                    elif isinstance(value, list):
                        candidates = [str(v) for v in value]
                    elif isinstance(value, dict):
                        for maybe_list in value.values():
                            if isinstance(maybe_list, list):
                                candidates.extend(str(v) for v in maybe_list)
                    if any(VAR_IN_PATH_RE.search(candidate) for candidate in candidates):
                        out.append(issue(path, "warning", job_line, "rules-path-var", f"Job '{job_name}' uses variable-like syntax inside rules:{key}", "Prefer literal paths in path-based rules"))

        image = job.get("image")
        if isinstance(image, str):
            image_name = image
        elif isinstance(image, dict):
            image_name = str(image.get("name", ""))
        else:
            image_name = ""
        if image_name and "$[[" not in image_name and not image_name.startswith("$"):
            if LATEST_TAG_RE.search(image_name):
                out.append(issue(path, "warning", job_line, "image-latest", f"Job '{job_name}' uses a 'latest' image tag: {image_name}", "Pin the image to an explicit version or digest"))
            elif UNPINNED_IMAGE_RE.match(image_name):
                out.append(issue(path, "warning", job_line, "image-unpinned", f"Job '{job_name}' uses an image without an explicit tag or digest: {image_name}", "Pin the image to an explicit version or digest"))

        cache = job.get("cache")
        cache_items = cache if isinstance(cache, list) else [cache] if cache else []
        for cache_item in cache_items:
            if isinstance(cache_item, dict) and "key" not in cache_item:
                out.append(issue(path, "note", job_line, "cache-key-missing", f"Job '{job_name}' has cache without an explicit key", "Use an explicit cache key when cache sharing behavior matters"))

        artifacts = job.get("artifacts")
        if isinstance(artifacts, dict) and artifacts and "expire_in" not in artifacts:
            out.append(issue(path, "note", job_line, "artifacts-expire-missing", f"Job '{job_name}' has artifacts without 'expire_in'", "Set artifact retention intentionally to avoid storage sprawl"))

        if "run" in job:
            out.append(issue(path, "warning", job_line, "run-experimental", f"Job '{job_name}' uses the 'run' keyword", "Confirm current GitLab support before using 'run' in production pipelines"))

        if str(config.get("variables", {}).get("CI_DEBUG_TRACE", "")).lower() == "true" or str(job.get("variables", {}).get("CI_DEBUG_TRACE", "")).lower() == "true":
            out.append(issue(path, "warning", job_line, "debug-trace", f"Job '{job_name}' enables CI_DEBUG_TRACE", "Avoid debug trace around secret-handling steps because logs become much noisier and riskier"))

        services = job.get("services") or config.get("services")
        if services:
            service_names: list[str] = []
            if isinstance(services, list):
                for item in services:
                    if isinstance(item, str):
                        service_names.append(item)
                    elif isinstance(item, dict):
                        service_names.append(str(item.get("name", "")))
            elif isinstance(services, str):
                service_names.append(services)
            for svc in service_names:
                if DIND_RE.search(svc):
                    out.append(issue(path, "warning", job_line, "dind-service", f"Job '{job_name}' uses Docker-in-Docker service '{svc}'", "Use a dedicated privileged runner and prefer BuildKit rootless when daemon behavior is not required"))
                    break

        for script_key in ("before_script", "script", "after_script"):
            for command in normalize_script(job.get(script_key)):
                if "set -x" in command or command.strip().startswith("set -x"):
                    out.append(issue(path, "warning", job_line, "set-x", f"Job '{job_name}' uses shell tracing in {script_key}", "Do not trace secret-handling commands"))
                if "docker login" in command and "--password-stdin" not in command:
                    out.append(issue(path, "warning", job_line, "docker-login-stdin", f"Job '{job_name}' runs 'docker login' without '--password-stdin'", "Pipe the password through standard input instead of putting it on the command line"))

    if any_rules and any_mr_rule and not has_workflow:
        out.append(issue(path, "warning", get_line(line_map, "workflow") or 1, "workflow-missing", "Jobs use merge-request-aware rules but no top-level workflow:rules", "Add workflow:rules to make pipeline creation explicit and reduce duplicate-pipeline surprises"))

    out.extend(scan_hardcoded_secrets(path, config, line_map))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate one or more GitLab CI/CD YAML files")
    parser.add_argument("paths", nargs="+", help="YAML files to validate")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit JSON instead of text")
    parser.add_argument("--fail-on-warnings", action="store_true", help="Return non-zero if warnings are found")
    args = parser.parse_args()

    all_issues: list[Issue] = []
    for raw in args.paths:
        all_issues.extend(validate_config(Path(raw)))

    severity_order = {"error": 0, "warning": 1, "note": 2}
    all_issues.sort(key=lambda i: (i.path, severity_order.get(i.severity, 99), i.line, i.rule))

    if args.json_output:
        print(json.dumps([asdict(i) for i in all_issues], indent=2))
    else:
        if not all_issues:
            print("No issues found.")
        else:
            for item in all_issues:
                line_part = f":{item.line}" if item.line else ""
                print(f"{item.severity.upper():7} {item.path}{line_part} [{item.rule}] {item.message}")
                if item.suggestion:
                    print(f"         suggestion: {item.suggestion}")

    has_error = any(i.severity == "error" for i in all_issues)
    has_warning = any(i.severity == "warning" for i in all_issues)
    if has_error:
        return 1
    if args.fail_on_warnings and has_warning:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
