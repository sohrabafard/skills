"""Canonical Codex model policy reader; no runtime discovery or implicit fallback."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from task_model_controls import validate_task_selection

ARTIFACTS = {f"alaa-{role}": f"skills/sohrab/alaa-codex-orchestrator/agents/alaa-{role}.toml" for role in "spec-analyst explorer researcher test-strategist implementer implementer-astra verifier failure-analyst reviewer reviewer-deep adversarial-reviewer documenter architecture-critic security-reviewer migration-guardian api-contract-reviewer dependency-auditor accessibility-reviewer browser-qa performance-profiler observability-reviewer release-guardian instruction-reviewer implementer-high planner planner-high implementer-luna implementer-low implementer-luna-high implementer-luna-low implementer-xhigh implementer-astra-medium implementer-astra-xhigh".split()}
ARTIFACTS["alaa-rule-writer"] = "skills/sohrab/alaa-prompting-guide/assets/rule-writer/codex/alaa-rule-writer.toml"

DEFAULT_POLICY = Path(__file__).resolve().parents[1] / "assets/codex-model-policy.json"


class PolicyLoadError(ValueError):
    """Policy input could not be read or decoded; a failed gate, not findings."""


def _iso_date(value: object) -> bool:
    try:
        return isinstance(value, str) and date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def validate_policy(policy: dict) -> list[str]:
    """Return schema and policy findings without mutating the supplied mapping."""
    errors = []
    if not isinstance(policy, dict):
        return ["policy must be an object"]
    if type(policy.get("schema_version")) is not int or policy.get("schema_version") != 2 or policy.get("surface") != "codex":
        errors.append("schema_version must be 2 and surface must be codex")
    if set(policy) - {"schema_version", "policy_version", "surface", "verified_on", "sources", "capability_evidence", "models", "profiles", "notes"}:
        errors.append("unknown policy keys; role defaults/legacy selections forbidden")
    for key in ("policy_version", "verified_on", "capability_evidence"):
        if not isinstance(policy.get(key), str) or not policy[key].strip():
            errors.append(f"missing {key}")
    if not _iso_date(policy.get("verified_on")):
        errors.append("verified_on requires an ISO calendar date")
    sources = policy.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("sources must contain official dated evidence")
    else:
        for source in sources:
            if not isinstance(source, dict) or not all(isinstance(source.get(k), str) and source[k].strip() for k in ("url", "verified_on", "scope")):
                errors.append("source requires url, verified_on and scope")
            elif not _iso_date(source["verified_on"]):
                errors.append("source verified_on requires an ISO calendar date")
    models, profiles = policy.get("models"), policy.get("profiles")
    if not isinstance(models, dict) or not models:
        return errors + ["models must be a nonempty object"]
    if not isinstance(profiles, dict) or not profiles:
        return errors + ["profiles must be a nonempty object"]
    for model, spec in models.items():
        if model not in {"gpt-6-astra", "gpt-6-sol", "gpt-6.1-sol", "gpt-6-luna"}:
            errors.append(f"{model}: unsupported exact model ID")
        if not isinstance(spec, dict):
            errors.append(f"{model}: model specification must be an object")
            continue
        levels = spec.get("supported_efforts")
        if not isinstance(levels, list) or not levels or any(not isinstance(x, str) or x not in ("low", "medium", "high", "xhigh", "max", "ultra") for x in levels) or len(set(levels)) != len(levels):
            errors.append(f"{model}: supported_efforts must be distinct nonempty strings")
        elif spec.get("recommended_start") not in levels:
            errors.append(f"{model}: recommended_start is unsupported")
    if set(profiles) != set(ARTIFACTS) | {"main", "main-deep"}:
        errors.append("coverage: every managed role and main/main-deep required")
    for model, spec in models.items():
        if isinstance(spec, dict) and type(spec.get("selection_enabled")) is not bool:
            errors.append(f"{model}: selection_enabled must be boolean")
    for role, profile in profiles.items():
        main = role in {"main", "main-deep"}
        expected = {"kind": "policy-only" if main else "agent",
                    "selection_mode": "externally-configured" if main else "task-selected",
                    "artifacts": [] if main else [ARTIFACTS.get(role)]}
        if profile != expected:
            errors.append(f"{role}: dynamic role identity/artifacts drift; model/effort defaults forbidden")
    return errors


def load_policy(path: str | Path | None = None) -> dict:
    """Read and validate the canonical policy, raising ValueError on any failure."""
    try:
        policy = json.loads(Path(path or DEFAULT_POLICY).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise PolicyLoadError(f"cannot load model policy: {exc}") from exc
    errors = validate_policy(policy)
    if errors:
        raise ValueError("; ".join(errors))
    return policy


def validate_agent_pin(agent: dict, policy: dict) -> list[str]:
    """Compatibility API name: managed definitions must omit BOTH executable pins."""
    errors = validate_policy(policy)
    if errors:
        return errors
    if not isinstance(agent, dict):
        return ["agent must be an object"]
    role = agent.get("name")
    if not isinstance(role, str) or role not in ARTIFACTS:
        return [f"unregistered agent profile: {role!r}"]
    for key in ("model", "model_reasoning_effort", "effort"):
        if key in agent:
            errors.append(f"{role}: executable {key} defeats task-selected controls")
    return errors
