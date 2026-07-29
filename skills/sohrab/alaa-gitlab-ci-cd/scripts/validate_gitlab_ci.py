#!/usr/bin/env python3
"""Static GitLab CI/CD validator.

Scope, stated so a caller knows what a clean result means:

- It reads one file at a time and resolves YAML anchors and merge keys.
- It resolves `default:` inheritance into every job before checking.
- It cannot see anything behind `include:`. When `include:` is present, every
  cross-file name check is downgraded to a note and one `unresolved-include`
  note is emitted.
- It cannot see the body of a script the pipeline invokes by path
  (`bash ci/scripts/deploy.sh`). Only inline script text is inspected.
- It reports facts. It does not decide whether a check must block a pipeline.
  That decision belongs to the skill that owns the stack, and the messages of
  `advisory-not-gate` and `no-code-gate` say so.

Exit codes:
  0  clean
  1  findings (any error; also any warning when --fail-on-warnings is set)
  2  could not run (missing dependency, missing file, unreadable or unparsable
     input, bad arguments)

Runs on Windows: pure Python 3.9+, no shell-out, no POSIX path assumptions, all
reads are explicitly UTF-8, and CRLF input is normalised by splitlines().
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterator

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_CANNOT_RUN = 2

try:
    import yaml
except ImportError:  # pragma: no cover - exercised by the documented remediation
    import sys

    sys.stderr.write(
        "validate_gitlab_ci.py needs PyYAML and could not import it.\n"
        "Install it with: python -m pip install PyYAML\n"
    )
    raise SystemExit(EXIT_CANNOT_RUN)


# Top-level keys that are configuration rather than jobs.
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

# Keys a job inherits from `default:` when the job does not set them itself.
DEFAULT_INHERITED_KEYS = (
    "after_script",
    "artifacts",
    "before_script",
    "cache",
    "hooks",
    "id_tokens",
    "image",
    "interruptible",
    "retry",
    "services",
    "tags",
    "timeout",
)

# Top-level keys GitLab deprecated in favour of `default:`.
DEPRECATED_GLOBAL_KEYS = ("image", "services", "cache", "before_script", "after_script")

VALID_WHEN = {"on_success", "on_failure", "always", "manual", "delayed", "never"}

# Failure classes `retry:when` accepts. Quoted in the retry-bare-count message.
RETRY_INFRA_CLASSES = ("runner_system_failure", "stuck_or_timeout_failure")

SECRET_NAME_RE = re.compile(
    r"(?:TOKEN|PASSWORD|PASS|SECRET|PRIVATE[_-]?KEY|ACCESS[_-]?KEY)", re.IGNORECASE
)
INLINE_SECRET_VALUE_RE = re.compile(r"^[A-Za-z0-9+/=_-]{16,}$")
VAR_IN_PATH_RE = re.compile(r"\$[{A-Za-z_]")
RULES_IF_BRACE_VAR_RE = re.compile(r"\$\{[A-Za-z_][A-Za-z0-9_]*\}")

# GitLab expansion understands $VAR and ${VAR}. It does not implement the
# shell-style ${VAR:-default} / ${VAR:?msg} / ${VAR-default} forms; it reads the
# whole brace body as one variable name, which does not exist, and yields empty.
SHELL_STYLE_DEFAULT_RE = re.compile(r"\$\{[A-Za-z_][A-Za-z0-9_]*[:!+?=-]")

# A tag that carries no version component is floating: it names a moving target
# exactly as `latest` does.
FLOATING_TAGS = {
    "latest",
    "rootless",
    "stable",
    "edge",
    "main",
    "master",
    "dev",
    "nightly",
    "current",
    "release",
    "cli",
    "dind",
}

DIND_RE = re.compile(r"(^|/)docker(?::[0-9][^\s]*)?-dind$")
CREDENTIAL_IN_URL_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9+.-]*://[^\s/@:]+:[^\s/@]+@")
GIT_REMOTE_SET_URL_RE = re.compile(r"\bgit\s+remote\s+set-url\b")

# Script fragments that turn a failing command into a passing job.
ADVISORY_SUFFIX_RE = re.compile(r"(\|\|\s*(true|:|exit\s+0)|;\s*true\s*$)")

# Jobs whose names or stages mean "this mutates something outside the pipeline".
MUTATING_NAME_RE = re.compile(
    r"(migrat|deploy|releas|publish|promot|rollout|rollback|seed|bootstrap|provision|"
    r"terraform|apply|upgrade)",
    re.IGNORECASE,
)

# Commands that assert something about the code. Used only to report the absence
# of any code gate; the decision about which gates must exist is not made here.
CODE_GATE_RE = re.compile(
    r"\b("
    r"pytest|tox|nose2|python -m unittest|ruff|flake8|mypy|bandit|pylint|"
    r"black --check|isort --check|"
    r"phpunit|pest|artisan\s+test|phpstan|psalm|pint|php-cs-fixer|phpcs|rector|"
    r"composer\s+audit|"
    r"jest|vitest|mocha|cypress\s+run|playwright\s+test|eslint|stylelint|"
    r"tsc|vue-tsc|"
    r"(npm|yarn|pnpm|bun)\s+(run\s+)?(test|lint|typecheck|type-check|check|audit|e2e)|"
    r"go\s+test|golangci-lint|govulncheck|staticcheck|"
    r"cargo\s+(test|clippy|audit)|"
    r"rspec|rubocop|brakeman|"
    r"(mvn|gradle)\s+(test|verify|check)|dotnet\s+test|"
    r"shellcheck|hadolint|yamllint|kubeconform|kubeval|helm\s+lint|conftest|"
    r"trivy|grype|gitleaks|semgrep|checkov|tflint|"
    r"make\s+(test|lint|check|ci|verify)"
    r")\b",
    re.IGNORECASE,
)



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


class GitLabLoader(yaml.SafeLoader):
    """SafeLoader that tolerates GitLab's custom YAML tags.

    `!reference [.job, key]` is valid GitLab syntax and extremely common. A plain
    SafeLoader raises ConstructorError on it, which is a YAMLError subclass, so a
    naive handler mislabels a correct file as a syntax error and abandons it.
    """


class Unresolved:
    """Placeholder for a tag this checker deliberately does not resolve."""

    def __init__(self, tag: str, value: Any) -> None:
        self.tag = tag
        self.value = value

    def __repr__(self) -> str:  # pragma: no cover - diagnostic only
        return f"<{self.tag} {self.value!r}>"


def _construct_unknown(loader: yaml.Loader, tag_suffix: str, node: yaml.Node) -> Unresolved:
    if isinstance(node, yaml.SequenceNode):
        value: Any = loader.construct_sequence(node, deep=True)
    elif isinstance(node, yaml.MappingNode):
        value = loader.construct_mapping(node, deep=True)
    else:
        value = loader.construct_scalar(node)
    return Unresolved("!" + tag_suffix, value)


GitLabLoader.add_multi_constructor("!", _construct_unknown)


def issue(
    path: Path,
    severity: str,
    line: int,
    rule: str,
    message: str,
    suggestion: str | None = None,
) -> Issue:
    return Issue(str(path), severity, line, rule, message, suggestion)


def build_line_map(text: str) -> dict[str, int]:
    """Map a top-level or nested key name to the first line that declares it."""
    result: dict[str, int] = {}
    for lineno, line in enumerate(text.splitlines(), start=1):
        m = re.match(r"^(\s*)(\"[^\"]+\"|'[^']+'|[^\s:#][^:#]*?)\s*:", line)
        if not m:
            continue
        key = m.group(2).strip().strip("\"'")
        result.setdefault(key, lineno)
        result.setdefault(f"{len(m.group(1))}:{key}", lineno)
    return result


def jobs_using_merge_keys(text: str) -> set[str]:
    """Names of top-level blocks whose body contains a `<<:` merge key.

    The parser flattens a merge key into the mapping, so after loading there is
    no way to tell an inherited value from a declared one. This pre-pass reads
    the source text and restores that distinction.
    """
    result: set[str] = set()
    current: str | None = None
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        if indent == 0:
            m = re.match(r"^(\"[^\"]+\"|'[^']+'|[^\s:#][^:#]*?)\s*:", line)
            current = m.group(1).strip().strip("\"'") if m else None
            continue
        if current and re.match(r"^\s+<<\s*:", line):
            result.add(current)
    return result


def get_line(line_map: dict[str, int], key: str, indent: int | None = None) -> int:
    if indent is not None:
        specific = line_map.get(f"{indent}:{key}")
        if specific:
            return specific
    return line_map.get(key, 0)


def load_yaml(path: Path) -> tuple[dict[str, Any], dict[str, int], set[str]]:
    """Return the merged config mapping and a key-to-line map.

    Raises CannotRun for anything that stops the checker producing a verdict.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise CannotRun(f"File not found: {path}")
    except OSError as exc:
        raise CannotRun(f"Could not read {path}: {exc}")
    except UnicodeDecodeError as exc:
        raise CannotRun(f"{path} is not valid UTF-8: {exc}")

    line_map = build_line_map(text)

    try:
        docs = list(yaml.load_all(text, Loader=GitLabLoader))
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        where = f" at line {mark.line + 1}" if mark is not None else ""
        raise CannotRun(f"YAML syntax error in {path}{where}: {exc}")

    docs = [d for d in docs if d is not None]
    if not docs:
        raise CannotRun(f"{path} contains no YAML document")

    if len(docs) == 1:
        config = docs[0]
    elif len(docs) == 2 and isinstance(docs[0], dict) and isinstance(docs[1], dict):
        # GitLab component layout: a `spec:` header document, then the config.
        config = dict(docs[1])
        for key, value in docs[0].items():
            config.setdefault(key, value)
    else:
        raise CannotRun(
            f"{path} has {len(docs)} YAML documents; GitLab accepts one config "
            "document, or a two-document component file"
        )

    if not isinstance(config, dict):
        raise CannotRun(f"{path}: GitLab CI/CD config root must be a mapping")

    return config, line_map, jobs_using_merge_keys(text)


def iter_jobs(config: dict[str, Any]) -> Iterator[tuple[str, dict[str, Any]]]:
    for name, value in config.items():
        if name in GLOBAL_KEYWORDS:
            continue
        if isinstance(value, dict):
            yield str(name), value


def resolve_extends(
    name: str,
    config: dict[str, Any],
    seen: frozenset[str] = frozenset(),
) -> dict[str, Any]:
    """Apply GitLab's `extends:` merge within this file.

    YAML anchors and merge keys are resolved by the parser; `extends:` is a
    GitLab feature the parser knows nothing about, so a rule that reads a job
    without resolving it sees neither the inherited retry nor the inherited
    resource group.
    """
    raw = config.get(name)
    if not isinstance(raw, dict) or name in seen:
        return dict(raw) if isinstance(raw, dict) else {}
    parents = raw.get("extends")
    if not parents:
        return dict(raw)
    parent_list = parents if isinstance(parents, list) else [parents]
    merged: dict[str, Any] = {}
    for parent in parent_list:
        if not isinstance(parent, str) or parent not in config:
            continue
        for key, value in resolve_extends(parent, config, seen | {name}).items():
            merged[key] = value
    for key, value in raw.items():
        merged[key] = value
    return merged


def effective_job(job: dict[str, Any], defaults: dict[str, Any]) -> dict[str, Any]:
    """Resolve `default:` inheritance for the keys GitLab propagates."""
    merged = dict(job)
    for key in DEFAULT_INHERITED_KEYS:
        if key not in merged and key in defaults:
            merged[key] = defaults[key]
    return merged


def normalize_script(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            out.extend(normalize_script(item))
        return out
    if isinstance(value, Unresolved):
        return []
    return [str(value)]


def script_lines(job: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for key in ("before_script", "script", "after_script"):
        for block in normalize_script(job.get(key)):
            lines.extend(block.splitlines() or [block])
    return lines


def image_reference(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return str(value.get("name", ""))
    return ""


def split_image(reference: str) -> tuple[str, str | None, str | None]:
    """Split an image reference into (repository, tag, digest).

    A registry host may carry an explicit port, so the colon that separates a
    port is not a tag separator. `registry.example.com:5000/team/php` has no tag.
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


def tag_is_floating(tag: str) -> bool:
    if tag.lower() in FLOATING_TAGS:
        return True
    # A tag with no digit anywhere names no version.
    return not any(ch.isdigit() for ch in tag)


def check_image_reference(
    out: list[Issue],
    path: Path,
    line: int,
    owner: str,
    where: str,
    reference: str,
) -> None:
    if not reference:
        return
    if "$[[" in reference or reference.startswith("$") or "${" in reference:
        return  # Value comes from an input or a variable; pin at that source.
    _repo, tag, digest = split_image(reference)
    if digest:
        return
    if tag is None:
        out.append(
            issue(
                path,
                "warning",
                line,
                "image-unpinned",
                f"{owner} uses {where} with no tag or digest: {reference}",
                "Write a version tag, or '@sha256:<digest>' where the exact bytes matter",
            )
        )
        return
    if tag_is_floating(tag):
        out.append(
            issue(
                path,
                "warning",
                line,
                "image-latest",
                f"{owner} uses {where} with the floating tag '{tag}': {reference}",
                "A tag with no version component moves under you; write a version "
                "tag or '@sha256:<digest>'",
            )
        )


def scan_variables_map(
    out: list[Issue],
    path: Path,
    line: int,
    owner: str,
    variables: Any,
) -> None:
    if not isinstance(variables, dict):
        return
    for key, value in variables.items():
        text = value if isinstance(value, str) else ""
        if SECRET_NAME_RE.search(str(key)) and text and not text.startswith("$"):
            if INLINE_SECRET_VALUE_RE.match(text):
                out.append(
                    issue(
                        path,
                        "warning",
                        line,
                        "secret-inline",
                        f"{owner} sets '{key}' to a literal that looks like a secret",
                        "Move the value to a protected, masked, or file variable in "
                        "GitLab settings and reference it as $NAME",
                    )
                )
        if text and SHELL_STYLE_DEFAULT_RE.search(text):
            out.append(
                issue(
                    path,
                    "error",
                    line,
                    "variables-shell-default",
                    f"{owner} sets '{key}' to {text!r}, which uses shell-style "
                    "expansion GitLab does not implement",
                    "GitLab expands $VAR and ${VAR} only. It reads the whole brace "
                    "body as one variable name, finds nothing, and assigns an empty "
                    "string — overwriting any predefined variable of that name. "
                    "Assign the plain value, or compute the default inside the script.",
                )
            )


def scan_script_body(
    out: list[Issue],
    path: Path,
    line: int,
    owner: str,
    job: dict[str, Any],
) -> None:
    for key in ("before_script", "script", "after_script"):
        for block in normalize_script(job.get(key)):
            for command in block.splitlines() or [block]:
                stripped = command.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                if re.search(r"(^|[;&|]\s*)set\s+-[a-zA-Z]*x", stripped):
                    out.append(
                        issue(
                            path,
                            "warning",
                            line,
                            "set-x",
                            f"{owner} turns on shell tracing in {key}",
                            "Shell tracing prints expanded arguments, so a masked "
                            "variable reaches the log in transformed form. Trace "
                            "only blocks that touch no secret.",
                        )
                    )
                if "docker login" in stripped and "--password-stdin" not in stripped:
                    out.append(
                        issue(
                            path,
                            "warning",
                            line,
                            "docker-login-stdin",
                            f"{owner} runs 'docker login' without '--password-stdin'",
                            "Pipe the password through standard input so it never "
                            "appears in the process table or the job log",
                        )
                    )
                if GIT_REMOTE_SET_URL_RE.search(stripped) or CREDENTIAL_IN_URL_RE.search(
                    stripped
                ):
                    out.append(
                        issue(
                            path,
                            "warning",
                            line,
                            "script-credential-in-url",
                            f"{owner} writes a credential into a URL or a Git remote",
                            "'git remote set-url' persists the credential in "
                            ".git/config, which survives the job on a shell runner. "
                            "Use 'git -c http.extraHeader=...' per invocation, or a "
                            "credential helper pointed at a file the job deletes.",
                        )
                    )
                if re.fullmatch(r"exit\s+0", stripped):
                    out.append(
                        issue(
                            path,
                            "note",
                            line,
                            "script-skips-with-exit-0",
                            f"{owner} can end early with 'exit 0' and report success "
                            "without doing its work",
                            "A job that skips inside its script shows as passed. Move "
                            "the condition into 'rules:' so the job is not created, "
                            "and the pipeline shows what actually ran.",
                        )
                    )
                if ADVISORY_SUFFIX_RE.search(stripped):
                    out.append(
                        issue(
                            path,
                            "warning",
                            line,
                            "advisory-not-gate",
                            f"{owner} ends a command so that its failure cannot fail "
                            f"the job: {stripped[:80]}",
                            "This is a fact, not a verdict: whether this check must "
                            "block belongs to the skill that owns the stack "
                            "(alaa-frontend-devops for a frontend repository, "
                            "alaa-cicd-laravel-postgres for a PHP or Laravel service).",
                        )
                    )


def check_cache(
    out: list[Issue],
    path: Path,
    line: int,
    owner: str,
    job: dict[str, Any],
) -> None:
    cache = job.get("cache")
    items = cache if isinstance(cache, list) else [cache] if cache else []
    for item in items:
        if not isinstance(item, dict):
            continue
        key = item.get("key")
        if key is None:
            out.append(
                issue(
                    path,
                    "note",
                    line,
                    "cache-key-missing",
                    f"{owner} declares cache with no key",
                    "Without a key every job on the runner shares one cache entry. "
                    "Name the key after what the cache contents depend on.",
                )
            )
        if isinstance(key, dict):
            files = key.get("files")
            if isinstance(files, list) and len(files) > 2:
                out.append(
                    issue(
                        path,
                        "error",
                        line,
                        "cache-key-files-limit",
                        f"{owner} lists {len(files)} paths under cache:key:files",
                        "GitLab accepts a maximum of two files under cache:key:files",
                    )
                )
        elif item.get("paths"):
            out.append(
                issue(
                    path,
                    "note",
                    line,
                    "cache-key-not-lockfile-derived",
                    f"{owner} keys its cache on something other than a lockfile",
                    "A key derived from cache:key:files over the lockfile changes "
                    "exactly when the cached contents should change. A branch- or "
                    "project-derived key does not.",
                )
            )
        fallbacks = item.get("fallback_keys")
        if isinstance(fallbacks, list) and len(fallbacks) > 5:
            out.append(
                issue(
                    path,
                    "error",
                    line,
                    "fallback-keys-limit",
                    f"{owner} lists {len(fallbacks)} fallback_keys",
                    "GitLab accepts up to five fallback keys per cache entry",
                )
            )
        if item.get("paths") and "policy" not in item:
            out.append(
                issue(
                    path,
                    "note",
                    line,
                    "cache-policy-unset",
                    f"{owner} declares cache with no policy",
                    "The default is pull-push, so a job that only reads the cache "
                    "still re-uploads it. Set 'policy: pull' on read-only jobs and "
                    "'policy: push' on the one job that builds it.",
                )
            )


def check_retry(
    out: list[Issue], path: Path, line: int, owner: str, job: dict[str, Any]
) -> None:
    if "retry" not in job:
        return
    retry = job["retry"]
    classes = ", ".join(RETRY_INFRA_CLASSES)
    if isinstance(retry, int):
        out.append(
            issue(
                path,
                "warning",
                line,
                "retry-bare-count",
                f"{owner} sets a bare 'retry: {retry}'",
                "A bare count retries every failure class, so an assertion failure "
                f"is retried and reads as a flake. Narrow it: retry: {{max: {retry}, "
                f"when: [{classes}]}}.",
            )
        )
    elif isinstance(retry, dict) and "when" not in retry:
        out.append(
            issue(
                path,
                "warning",
                line,
                "retry-bare-count",
                f"{owner} sets 'retry:max' with no 'when:' list",
                f"Without 'when:' every failure class is retried. List the "
                f"infrastructure classes only: [{classes}].",
            )
        )


def validate_config(path: Path) -> list[Issue]:
    config, line_map, merged_jobs = load_yaml(path)
    out: list[Issue] = []

    has_include = "include" in config
    cross_file_severity = "note" if has_include else "error"
    if has_include:
        out.append(
            issue(
                path,
                "note",
                get_line(line_map, "include") or 1,
                "unresolved-include",
                "This file uses 'include:', so names defined in the included files "
                "are invisible here",
                "Cross-file checks for extends, needs, dependencies and stage are "
                "reported as notes in this file. Run 'glab ci lint --dry-run' for a "
                "merged-configuration verdict.",
            )
        )

    default_block = (
        dict(config["default"]) if isinstance(config.get("default"), dict) else {}
    )
    # A deprecated top-level image/services/cache/before_script/after_script still
    # applies to every job, so it is checked through the same inheritance path.
    defaults = dict(default_block)
    for key in DEPRECATED_GLOBAL_KEYS:
        if key in config and key not in defaults:
            defaults[key] = config[key]

    for key in DEPRECATED_GLOBAL_KEYS:
        if key in config:
            out.append(
                issue(
                    path,
                    "warning",
                    get_line(line_map, key, 0),
                    "deprecated-global-keyword",
                    f"Top-level '{key}:' is deprecated",
                    f"Move it under 'default:' so it reads as inheritance rather "
                    f"than a global.",
                )
            )

    stages = config.get("stages")
    declared_stages: list[str] = []
    if stages is not None:
        if not isinstance(stages, list):
            out.append(
                issue(
                    path,
                    "error",
                    get_line(line_map, "stages"),
                    "stages-type",
                    "'stages' must be a list",
                )
            )
        else:
            seen: set[str] = set()
            for stage in stages:
                if not isinstance(stage, str):
                    out.append(
                        issue(
                            path,
                            "error",
                            get_line(line_map, "stages"),
                            "stage-type",
                            f"Stage names must be strings, got {type(stage).__name__}",
                        )
                    )
                    continue
                declared_stages.append(stage)
                if stage in seen:
                    out.append(
                        issue(
                            path,
                            "warning",
                            get_line(line_map, "stages"),
                            "stage-duplicate",
                            f"Duplicate stage '{stage}'",
                        )
                    )
                seen.add(stage)

    scan_variables_map(
        out, path, get_line(line_map, "variables", 0), "Top-level variables", config.get("variables")
    )

    for source, owner, anchor in (
        (default_block, "default:", "default"),
        (
            {k: config[k] for k in DEPRECATED_GLOBAL_KEYS if k in config},
            "The top-level block",
            DEPRECATED_GLOBAL_KEYS[0],
        ),
    ):
        if not source:
            continue
        source_line = get_line(line_map, anchor, 0) or 1
        check_image_reference(
            out, path, source_line, owner, "an image", image_reference(source.get("image"))
        )
        services = source.get("services")
        for svc in services if isinstance(services, list) else []:
            check_image_reference(
                out, path, source_line, owner, "a service image", image_reference(svc)
            )
        for svc in services if isinstance(services, list) else []:
            if DIND_RE.search(image_reference(svc)):
                out.append(
                    issue(
                        path,
                        "warning",
                        source_line,
                        "dind-service",
                        f"{owner} declares the Docker-in-Docker service "
                        f"'{image_reference(svc)}' for every job",
                        "DinD needs a privileged runner. Confirm the runner fleet is "
                        "dedicated and the nodes are isolated.",
                    )
                )
                break
        check_cache(out, path, source_line, owner, source)
        check_retry(out, path, source_line, owner, source)
        scan_script_body(out, path, source_line, owner, source)

    has_workflow = isinstance(config.get("workflow"), dict)
    any_rules = False
    any_mr_rule = False
    any_needs = False
    resource_groups: set[str] = set()
    jobs_with_resource_group = 0
    concrete_jobs = 0
    needed_by: dict[str, set[str]] = {}
    needs_of: dict[str, set[str]] = {}
    job_stage: dict[str, str] = {}
    any_image_declared = bool(defaults.get("image"))
    gate_commands_seen: list[str] = []

    job_names = {name for name, _ in iter_jobs(config)}

    for job_name, declared_job in iter_jobs(config):
        raw_job = resolve_extends(job_name, config)
        job = effective_job(raw_job, defaults)
        job_line = get_line(line_map, job_name)
        owner = f"Job '{job_name}'"
        hidden = job_name.startswith(".")
        if not hidden:
            concrete_jobs += 1

        if job_name in RESERVED_NAMES and not hidden:
            out.append(
                issue(
                    path,
                    "error",
                    job_line,
                    "job-name-reserved",
                    f"{owner} collides with a reserved top-level keyword",
                )
            )

        if not hidden and not any(
            key in job for key in ("script", "run", "trigger", "release")
        ):
            out.append(
                issue(
                    path,
                    "warning",
                    job_line,
                    "job-action-missing",
                    f"{owner} declares no 'script', 'run', 'trigger' or 'release'",
                    "A hidden job (name starting with a dot) may omit these; a "
                    "concrete job normally cannot",
                )
            )

        if "only" in raw_job or "except" in raw_job:
            out.append(
                issue(
                    path,
                    "warning",
                    job_line,
                    "only-except",
                    f"{owner} uses deprecated 'only' or 'except'",
                    "GitLab's replacement is 'rules'; 'only:refs' becomes 'rules:if' "
                    "and 'only:changes' becomes 'rules:changes'",
                )
            )

        stage_name = job.get("stage")
        if isinstance(stage_name, str):
            job_stage[job_name] = stage_name
            if declared_stages and stage_name not in declared_stages:
                out.append(
                    issue(
                        path,
                        cross_file_severity,
                        job_line,
                        "stage-missing",
                        f"{owner} references stage '{stage_name}', which this file "
                        "does not declare",
                    )
                )

        if "when" in job and job["when"] not in VALID_WHEN:
            out.append(
                issue(
                    path,
                    "error",
                    job_line,
                    "when-invalid",
                    f"{owner} uses invalid 'when' value '{job['when']}'",
                )
            )

        if "extends" in declared_job:
            parents = (
                declared_job["extends"]
                if isinstance(declared_job["extends"], list)
                else [declared_job["extends"]]
            )
            for parent in parents:
                if isinstance(parent, str) and parent not in job_names:
                    out.append(
                        issue(
                            path,
                            cross_file_severity,
                            job_line,
                            "extends-missing",
                            f"{owner} extends '{parent}', which this file does not "
                            "define",
                        )
                    )

        if "needs" in job:
            any_needs = True
            needs = job["needs"]
            items = needs if isinstance(needs, list) else [needs]
            targets: set[str] = set()
            for need in items:
                if isinstance(need, str):
                    target: str | None = need
                elif isinstance(need, dict):
                    raw_target = need.get("job")
                    target = raw_target if isinstance(raw_target, str) else None
                else:
                    target = None
                if target is None:
                    continue
                targets.add(target)
                if target not in job_names:
                    out.append(
                        issue(
                            path,
                            cross_file_severity,
                            job_line,
                            "needs-missing",
                            f"{owner} needs '{target}', which this file does not define",
                        )
                    )
                else:
                    needed_by.setdefault(target, set()).add(job_name)
            needs_of[job_name] = targets

        if "dependencies" in job:
            deps = (
                job["dependencies"]
                if isinstance(job["dependencies"], list)
                else [job["dependencies"]]
            )
            for dep in deps:
                if isinstance(dep, str) and dep not in job_names:
                    out.append(
                        issue(
                            path,
                            cross_file_severity,
                            job_line,
                            "dependencies-missing",
                            f"{owner} depends on '{dep}', which this file does not "
                            "define",
                        )
                    )

        rules = job.get("rules")
        if isinstance(rules, list):
            any_rules = True
            for rule in rules:
                if not isinstance(rule, dict):
                    continue
                if_cond = rule.get("if")
                if isinstance(if_cond, str):
                    if RULES_IF_BRACE_VAR_RE.search(if_cond):
                        out.append(
                            issue(
                                path,
                                "warning",
                                job_line,
                                "rules-if-brace-var",
                                f"{owner} writes '${{VAR}}' inside rules:if",
                                "Write '$VAR' inside a rules:if expression",
                            )
                        )
                    if "merge_request_event" in if_cond:
                        any_mr_rule = True
                if rule.get("allow_failure") is True:
                    out.append(
                        issue(
                            path,
                            "warning",
                            job_line,
                            "advisory-not-gate",
                            f"{owner} sets allow_failure: true in a rule, so its "
                            "failure cannot fail the pipeline",
                            "This is a fact, not a verdict: whether this check must "
                            "block belongs to the skill that owns the stack.",
                        )
                    )
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
                    if any(VAR_IN_PATH_RE.search(c) for c in candidates):
                        out.append(
                            issue(
                                path,
                                "warning",
                                job_line,
                                "rules-path-var",
                                f"{owner} uses variable syntax inside rules:{key}",
                                "GitLab does not expand variables in path filters; "
                                "write the literal paths",
                            )
                        )

        if job.get("allow_failure") is True:
            out.append(
                issue(
                    path,
                    "warning",
                    job_line,
                    "advisory-not-gate",
                    f"{owner} sets allow_failure: true, so its failure cannot fail "
                    "the pipeline",
                    "This is a fact, not a verdict: whether this check must block "
                    "belongs to the skill that owns the stack "
                    "(alaa-frontend-devops for a frontend repository, "
                    "alaa-cicd-laravel-postgres for a PHP or Laravel service).",
                )
            )

        image_name = image_reference(raw_job.get("image"))
        if image_name:
            any_image_declared = True
        check_image_reference(out, path, job_line, owner, "an image", image_name)

        services = raw_job.get("services")
        service_names: list[str] = []
        if isinstance(services, list):
            for item in services:
                service_names.append(image_reference(item))
        elif isinstance(services, str):
            service_names.append(services)
        for svc in service_names:
            check_image_reference(out, path, job_line, owner, "a service image", svc)
            if DIND_RE.search(svc):
                out.append(
                    issue(
                        path,
                        "warning",
                        job_line,
                        "dind-service",
                        f"{owner} uses the Docker-in-Docker service '{svc}'",
                        "DinD needs a privileged runner. Confirm the runner fleet is "
                        "dedicated and the nodes are isolated.",
                    )
                )
                break

        check_cache(out, path, job_line, owner, raw_job)
        check_retry(out, path, job_line, owner, raw_job)

        artifacts = raw_job.get("artifacts")
        if isinstance(artifacts, dict) and artifacts and "expire_in" not in artifacts:
            out.append(
                issue(
                    path,
                    "note",
                    job_line,
                    "artifacts-expire-missing",
                    f"{owner} publishes artifacts with no 'expire_in'",
                    "Unset means the instance-wide default applies, which the "
                    "pipeline author cannot see. Set it deliberately.",
                )
            )

        resource_group = job.get("resource_group")
        if resource_group is not None:
            jobs_with_resource_group += 1
            resource_groups.add(str(resource_group))

        if "run" in raw_job:
            out.append(
                issue(
                    path,
                    "warning",
                    job_line,
                    "run-experimental",
                    f"{owner} uses the 'run' keyword",
                    "'run' invokes GitLab Functions, which GitLab documents as an "
                    "experimental feature subject to breaking changes. Use 'script' "
                    "unless the task requires Functions.",
                )
            )

        merged_vars = {}
        if isinstance(config.get("variables"), dict):
            merged_vars.update(config["variables"])
        if isinstance(raw_job.get("variables"), dict):
            merged_vars.update(raw_job["variables"])
        if str(merged_vars.get("CI_DEBUG_TRACE", "")).lower() == "true":
            out.append(
                issue(
                    path,
                    "warning",
                    job_line,
                    "debug-trace",
                    f"{owner} enables CI_DEBUG_TRACE",
                    "Debug trace prints every variable the job can see, masked ones "
                    "included in transformed form",
                )
            )

        scan_variables_map(out, path, job_line, owner, raw_job.get("variables"))
        scan_script_body(out, path, job_line, owner, raw_job)

        interruptible = job.get("interruptible")
        mutating_name = bool(
            MUTATING_NAME_RE.search(job_name)
            or (isinstance(stage_name, str) and MUTATING_NAME_RE.search(stage_name))
        )
        if interruptible is True and not hidden:
            if mutating_name:
                out.append(
                    issue(
                        path,
                        "warning",
                        job_line,
                        "interruptible-on-mutating-job",
                        f"{owner} resolves to interruptible: true and its name or "
                        "stage says it mutates a shared target",
                        "A superseding pipeline cancels this job mid-write. Set "
                        "'interruptible: false' on every job that mutates a database, "
                        "a registry, a Git remote or a cluster.",
                    )
                )
            elif resource_group is not None and (
                "interruptible" not in declared_job or job_name in merged_jobs
            ):
                out.append(
                    issue(
                        path,
                        "note",
                        job_line,
                        "interruptible-on-mutating-job",
                        f"{owner} resolves to interruptible: true while holding a "
                        "resource_group",
                        "A resource group usually means a shared target. Confirm this "
                        "job is safe to cancel halfway; if it is not, set "
                        "'interruptible: false'.",
                    )
                )

        if not hidden and "timeout" not in job and (
            resource_group is not None or "environment" in job
        ):
            out.append(
                issue(
                    path,
                    "note",
                    job_line,
                    "job-timeout-missing",
                    f"{owner} holds a resource group or an environment and sets no "
                    "'timeout:'",
                    "Without a job timeout the project-wide default applies, and a "
                    "hung job holds the resource group for that whole budget",
                )
            )

        for command in script_lines(job):
            match = CODE_GATE_RE.search(command)
            if match:
                gate_commands_seen.append(match.group(0))

    # Pipeline-level findings.
    if any_rules and any_mr_rule and not has_workflow:
        out.append(
            issue(
                path,
                "warning",
                get_line(line_map, "workflow") or 1,
                "workflow-missing",
                "Jobs use merge-request-aware rules with no top-level workflow:rules",
                "Without it one push can create both a branch pipeline and a merge "
                "request pipeline",
            )
        )

    if any_needs and concrete_jobs >= 2 and len(resource_groups) == 1 and (
        jobs_with_resource_group >= concrete_jobs
    ):
        only = next(iter(resource_groups))
        out.append(
            issue(
                path,
                "warning",
                get_line(line_map, "stages") or 1,
                "resource-group-saturation",
                f"Every job shares one resource_group ({only!r}) while 'needs:' is in "
                "use, so the DAG cannot run anything in parallel",
                "A resource group admits one job at a time. Name it after the target "
                "it protects and apply it only to the jobs that touch that target.",
            )
        )

    if any_needs and declared_stages:
        stage_index = {name: i for i, name in enumerate(declared_stages)}

        def closure(job_name: str, seen: set[str] | None = None) -> set[str]:
            seen = seen if seen is not None else set()
            for target in needs_of.get(job_name, set()):
                if target not in seen:
                    seen.add(target)
                    closure(target, seen)
            return seen

        for name in sorted(job_names):
            if name.startswith(".") or needed_by.get(name):
                continue
            own_stage = stage_index.get(job_stage.get(name, ""), -1)
            if own_stage < 0:
                continue
            for other in sorted(job_names):
                if other == name or other.startswith("."):
                    continue
                if not needs_of.get(other):
                    continue
                if stage_index.get(job_stage.get(other, ""), -1) <= own_stage:
                    continue
                if name in closure(other):
                    continue
                out.append(
                    issue(
                        path,
                        "note",
                        get_line(line_map, name),
                        "dag-orphan",
                        f"No job needs '{name}', and '{other}' in a later stage can "
                        "start without it",
                        "Under DAG semantics a stage boundary is not a precondition. "
                        f"If '{other}' must not run before '{name}', add the "
                        "'needs:' edge.",
                    )
                )
                break

    if concrete_jobs >= 3 and not any_image_declared and not has_include:
        out.append(
            issue(
                path,
                "note",
                1,
                "runner-supplied-image",
                "No job and no 'default:' declares 'image:', so the image comes from "
                "runner configuration",
                "The pin still has to exist. Pin 'image =' under "
                "[runners.kubernetes] (or the shell runner's provisioned toolchain) "
                "and check it with validate_runner_config.py.",
            )
        )

    # A file with one or two jobs is a fragment, not a pipeline; the absence of
    # a code gate is only meaningful for a file that is the whole pipeline.
    if concrete_jobs >= 3 and not gate_commands_seen and not has_include:
        out.append(
            issue(
                path,
                "warning",
                1,
                "no-code-gate",
                f"This file defines {concrete_jobs} jobs and none of them runs a "
                "recognised test, lint, static-analysis or dependency-audit command",
                "A pipeline that asserts nothing about the code is green whether the "
                "code is correct or not. Which checks must exist is decided by the "
                "skill that owns the stack (alaa-frontend-devops for a frontend "
                "repository, alaa-cicd-laravel-postgres for a PHP or Laravel "
                "service); this checker only reports that none is present here.",
            )
        )

    return out


TEXT_REPEAT_LIMIT = 3


def render(issues: list[Issue], as_json: bool) -> None:
    severity_order = {"error": 0, "warning": 1, "note": 2}
    issues.sort(key=lambda i: (i.path, severity_order.get(i.severity, 99), i.line, i.rule))
    if as_json:
        # JSON is the machine surface and is never collapsed.
        print(json.dumps([asdict(i) for i in issues], indent=2))
        return
    if not issues:
        print("No issues found.")
        return
    # One rule inherited by every job produces one finding per job. Text output
    # shows the first few and counts the rest so a real second finding stays
    # visible; --json still carries every occurrence.
    shown: dict[tuple[str, str], int] = {}
    suppressed: dict[tuple[str, str], int] = {}
    for item in issues:
        key = (item.path, item.rule)
        count = shown.get(key, 0)
        if count >= TEXT_REPEAT_LIMIT:
            suppressed[key] = suppressed.get(key, 0) + 1
            continue
        shown[key] = count + 1
        line_part = f":{item.line}" if item.line else ""
        print(f"{item.severity.upper():7} {item.path}{line_part} [{item.rule}] {item.message}")
        if item.suggestion:
            print(f"         suggestion: {item.suggestion}")
    for (path, rule), extra in sorted(suppressed.items()):
        print(f"         ... [{rule}] fires on {extra} more job(s) in {path}; use --json for all")


def fixtures_dir() -> Path:
    return Path(__file__).resolve().parent / "fixtures"


SELF_TEST_EXPECTATIONS: dict[str, dict[str, Any]] = {
    "good-pipeline.gitlab-ci.yml": {"absent": {"*"}},
    "reference-tag.gitlab-ci.yml": {"absent": {"*"}},
    # The fleet's standard wrapper must never produce an error: every unresolved
    # cross-file name is a note, and the file must not fail a pipeline.
    "thin-wrapper.gitlab-ci.yml": {
        "present": {"unresolved-include", "extends-missing", "needs-missing"},
        "absent": {"no-code-gate", "runner-supplied-image"},
        "max_severity": "note",
    },
    "default-block.gitlab-ci.yml": {
        "present": {"image-unpinned", "cache-key-missing", "set-x", "secret-inline"},
    },
    "registry-port.gitlab-ci.yml": {"present": {"image-unpinned"}},
    "scheduling-hazards.gitlab-ci.yml": {
        "present": {
            "retry-bare-count",
            "interruptible-on-mutating-job",
            "resource-group-saturation",
            "dag-orphan",
            "job-timeout-missing",
            "no-code-gate",
        },
    },
    "cache-and-pinning.gitlab-ci.yml": {
        "present": {
            "cache-key-files-limit",
            "fallback-keys-limit",
            "cache-policy-unset",
            "image-latest",
            "deprecated-global-keyword",
        },
    },
    "advisory-and-secrets.gitlab-ci.yml": {
        "present": {
            "advisory-not-gate",
            "variables-shell-default",
            "script-credential-in-url",
            "docker-login-stdin",
        },
    },
}

SEVERITY_RANK = {"note": 0, "warning": 1, "error": 2}


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
            issues = validate_config(fixture)
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
        cap = expectation.get("max_severity")
        if cap:
            limit = SEVERITY_RANK[cap]
            for item in issues:
                if SEVERITY_RANK.get(item.severity, 9) > limit:
                    failures.append(
                        f"{name}: '{item.rule}' is {item.severity}, expected at most {cap}"
                    )

    missing = base / "does-not-exist.yml"
    try:
        validate_config(missing)
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
        prog="validate_gitlab_ci.py",
        description=(
            "Validate one or more GitLab CI/CD YAML files. Reports facts about how a "
            "pipeline is expressed; it does not decide which checks must block."
        ),
        epilog=(
            "Exit codes: 0 clean, 1 findings, 2 could not run. "
            "--fail-on-warnings folds warnings into exit 1; which warnings must block "
            "is the calling skill's decision, not this script's."
        ),
    )
    parser.add_argument("paths", nargs="*", help="GitLab CI/CD YAML files to validate")
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

    all_issues: list[Issue] = []
    blocked = False
    for raw in args.paths:
        try:
            all_issues.extend(validate_config(Path(raw)))
        except CannotRun as exc:
            print(f"CANNOT RUN: {exc}")
            blocked = True

    if blocked:
        return EXIT_CANNOT_RUN

    render(all_issues, args.json_output)

    if any(i.severity == "error" for i in all_issues):
        return EXIT_FINDINGS
    if args.fail_on_warnings and any(i.severity == "warning" for i in all_issues):
        return EXIT_FINDINGS
    return EXIT_CLEAN


if __name__ == "__main__":
    raise SystemExit(main())
