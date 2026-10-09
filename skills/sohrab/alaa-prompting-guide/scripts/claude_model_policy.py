"""Claude source policy validation. Static agreement is not runtime activation."""
from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse
from task_model_controls import validate_task_selection

SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_POLICY = SKILL_ROOT / "assets/claude-model-policy.json"
AGENT_DIR = "skills/sohrab/alaa-cc-orchestrator/agents"
WRITER_DIR = "skills/sohrab/alaa-prompting-guide/assets/rule-writer/claude"
ROLES = frozenset("spec-analyst explorer researcher implementer implementer-opus implementer-fable implementer-haiku implementer-haiku-high implementer-sonnet-high implementer-opus-high planner planner-high failure-analyst verifier test-strategist reviewer adversarial-reviewer architecture-critic security-reviewer migration-guardian api-contract-reviewer dependency-auditor accessibility-reviewer browser-qa performance-profiler observability-reviewer release-guardian documenter instruction-reviewer".split())
ARTIFACTS = {f"alaa-{role}": f"{AGENT_DIR}/alaa-{role}.md" for role in ROLES}
ARTIFACTS["alaa-rule-writer"] = f"{WRITER_DIR}/alaa-rule-writer.md"
EFFORTS = frozenset(("low", "medium", "high", "xhigh", "max"))
_NUMBER = r"(?:0|[1-9]\d*)"
_PRE = rf"(?:{_NUMBER}|[0-9]*[A-Za-z-][0-9A-Za-z-]*)"
SEMVER = re.compile(rf"{_NUMBER}\.{_NUMBER}\.{_NUMBER}(?:-{_PRE}(?:\.{_PRE})*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?\Z")


class CannotRun(ValueError):
    """Unreadable or undecodable input; exit 2, never a pass."""


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def semver_key(value):
    """Comparable SemVer precedence, with build metadata ignored."""
    if not isinstance(value, str) or not SEMVER.fullmatch(value):
        raise ValueError("invalid semantic version")
    version = value.split("+", 1)[0]
    core, separator, prerelease = version.partition("-")
    identifiers = tuple((0, int(part)) if part.isdigit() else (1, part)
                        for part in prerelease.split(".")) if separator else ()
    return tuple(int(part) for part in core.split(".")), not bool(separator), identifiers


def iso_date(value):
    try:
        return isinstance(value, str) and date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def relative_file(value, root=REPO_ROOT):
    if not nonempty(value) or "\\" in value or ":" in value:
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or str(path) != value:
        return None
    resolved = (root / value).resolve()
    return resolved if resolved.is_relative_to(root.resolve()) else None


def shape(obj, required, where, errors, optional=()):
    if not isinstance(obj, dict):
        errors.append(f"{where}: must be an object")
        return False
    missing, extra = set(required) - obj.keys(), obj.keys() - set(required) - set(optional) - {"notes"}
    if missing or extra:
        errors.append(f"{where}: missing keys {sorted(missing)}, unknown keys {sorted(extra)}")
    if "notes" in obj and not isinstance(obj["notes"], str):
        errors.append(f"{where}: notes must be a string")
    return True


def unique_strings(value, allow_empty=False):
    return isinstance(value, list) and (allow_empty or bool(value)) and all(nonempty(x) for x in value) and len(set(value)) == len(value)


def pair_valid(pair, policy):
    if not isinstance(pair, dict) or not isinstance(pair.get("model"), str):
        return False
    spec = policy["models"].get(pair["model"])
    if not isinstance(spec, dict):
        return False
    levels = spec.get("supported_efforts")
    return isinstance(levels, list) and ((not levels and pair.get("effort") is None) or (bool(levels) and pair.get("effort") in levels))


def validate_policy(policy, root=REPO_ROOT):
    errors = []
    if not shape(policy, ("schema_version", "policy_version", "surface", "verified_on", "sources", "models", "profiles"), "policy", errors):
        return errors
    if type(policy.get("schema_version")) is not int or policy["schema_version"] != 2:
        errors.append("schema_version must be integer 2")
    if not isinstance(policy.get("policy_version"), str) or not SEMVER.fullmatch(policy["policy_version"]):
        errors.append("policy_version must be semantic version")
    if policy.get("surface") != "claude-code" or not iso_date(policy.get("verified_on")):
        errors.append("surface/date invalid")
    sources = policy.get("sources")
    source_ids = set()
    if not isinstance(sources, list) or not sources:
        errors.append("sources must be a nonempty array")
        sources = []
    for source in sources:
        if not shape(source, ("id", "url", "verified_on", "scope"), "source", errors):
            continue
        sid = source.get("id")
        if not nonempty(sid) or sid in source_ids:
            errors.append("source id must be unique nonempty string")
        else:
            source_ids.add(sid)
        url = source.get("url")
        if not nonempty(url) or urlparse(url).scheme != "https" or not urlparse(url).netloc:
            errors.append("source url must be HTTPS")
        if not iso_date(source.get("verified_on")) or not nonempty(source.get("scope")):
            errors.append("source needs ISO date and scope")

    def references(obj, where):
        refs = obj.get("source_ids")
        if not unique_strings(refs) or any(ref not in source_ids for ref in refs):
            errors.append(f"{where}: source_ids must reference distinct existing sources")

    models, profiles = policy.get("models"), policy.get("profiles")
    if not isinstance(models, dict) or not models or not isinstance(profiles, dict) or not profiles:
        return errors + ["models and profiles must be nonempty objects"]
    for model, spec in models.items():
        if not re.fullmatch(r"claude-(?:opus|sonnet|fable)-\d+(?:-\d+)?|claude-haiku-(?:5-5|4-5-\d{8})", model):
            errors.append(f"{model}: exact API model ID required; aliases forbidden")
        if not shape(spec, ("supported_efforts", "default_effort", "thinking_mode", "source_ids"), model, errors, ("minimum_claude_code", "selection_enabled")):
            continue
        if "minimum_claude_code" in spec:
            try:
                semver_key(spec["minimum_claude_code"])
            except ValueError:
                errors.append(f"{model}: minimum_claude_code must be semantic version")
        levels = spec.get("supported_efforts")
        if not unique_strings(levels, allow_empty=True) or any(level not in EFFORTS for level in levels):
            errors.append(f"{model}: invalid supported_efforts")
        elif (levels and spec.get("default_effort") not in levels) or (not levels and spec.get("default_effort") is not None):
            errors.append(f"{model}: default_effort must be supported or null when unsupported")
        if model.startswith("claude-haiku-4-5-") and levels != []:
            errors.append(f"{model}: Haiku 4.5 has no effort parameter")
        if spec.get("thinking_mode") not in ("adaptive-always-on", "adaptive", "extended"):
            errors.append(f"{model}: invalid thinking_mode")
        if type(spec.get("selection_enabled")) is not bool:
            errors.append(f"{model}: selection_enabled must be boolean")
        if spec.get("selection_enabled") is True and "minimum_claude_code" not in spec:
            errors.append(f"{model}: active model requires minimum_claude_code")
        references(spec, model)
    if set(profiles) != set(ARTIFACTS) | {"main", "main-deep"}:
        errors.append(f"coverage: exactly main/main-deep and {len(ARTIFACTS)} managed agent profiles required")
    for role, profile in profiles.items():
        main = role in {"main", "main-deep"}
        expected = {"kind": "policy-only" if main else "agent",
                    "selection_mode": "externally-configured" if main else "task-selected",
                    "artifacts": [] if main else [ARTIFACTS.get(role)]}
        if profile != expected:
            errors.append(f"{role}: dynamic role identity/artifacts drift; model/effort defaults forbidden")
    return errors


def read_json(path):
    def reject_constant(value):
        raise CannotRun(f"nonfinite JSON number {value}")

    def distinct(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise CannotRun(f"duplicate JSON key {key}")
            result[key] = value
        return result
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=distinct, parse_constant=reject_constant)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CannotRun(f"cannot read JSON {path}: {exc}") from exc


def load_policy(path=DEFAULT_POLICY):
    policy = read_json(path)
    errors = validate_policy(policy)
    if errors:
        raise ValueError("; ".join(errors))
    return policy


def validate_agent_pin(agent, policy, filename):
    """Compatibility API name: task-selected roles omit both model and effort."""
    if not isinstance(agent, dict):
        return ["agent frontmatter must be a mapping"]
    role = agent.get("name")
    if not isinstance(role, str) or role not in ARTIFACTS:
        return [f"unknown executable profile {role!r}"]
    errors = []
    if filename != Path(ARTIFACTS[role]).name:
        errors.append(f"{role}: filename/profile mapping drift")
    for key in ("model", "effort", "model_reasoning_effort"):
        if key in agent:
            errors.append(f"{role}: executable {key} defeats task-selected controls")
    return errors


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
