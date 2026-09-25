"""Canonical Codex model policy reader; no runtime discovery or implicit fallback."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

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
    if policy.get("schema_version") != 1 or policy.get("surface") != "codex":
        errors.append("schema_version must be 1 and surface must be codex")
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
        if not isinstance(spec, dict):
            errors.append(f"{model}: model specification must be an object")
            continue
        levels = spec.get("supported_efforts")
        if not isinstance(levels, list) or not levels or any(not isinstance(x, str) or x not in ("low", "medium", "high", "xhigh", "max", "ultra") for x in levels) or len(set(levels)) != len(levels):
            errors.append(f"{model}: supported_efforts must be distinct nonempty strings")
        elif spec.get("recommended_start") not in levels:
            errors.append(f"{model}: recommended_start is unsupported")
    exceptions = policy.get("legacy_exceptions")
    if not isinstance(exceptions, list):
        errors.append("legacy_exceptions must be a list")
        exceptions = []
    valid_exceptions = {}
    for entry in exceptions:
        fields = ("profile", "model", "effort", "reason", "scope", "evidence", "review_condition", "approved_by", "approved_on")
        if not isinstance(entry, dict) or not all(isinstance(entry.get(k), str) and entry[k].strip() for k in fields):
            errors.append("legacy exception requires profile, model, effort, reason, scope, evidence, review_condition, approved_by and approved_on")
            continue
        if entry["profile"] in valid_exceptions or entry["profile"] not in profiles or not entry["model"].startswith("gpt-5.6-"):
            errors.append(f"invalid or duplicate legacy exception: {entry['profile']}")
        if not _iso_date(entry["approved_on"]):
            errors.append(f"{entry['profile']}: approved_on requires an ISO calendar date")
        valid_exceptions[entry["profile"]] = entry
    for role, profile in profiles.items():
        if not isinstance(profile, dict):
            errors.append(f"{role}: profile must be an object")
            continue
        model, effort = profile.get("model"), profile.get("effort")
        if not isinstance(model, str) or not isinstance(effort, str):
            errors.append(f"{role}: model and effort must be strings")
            continue
        spec = models.get(model, {})
        levels = spec.get("supported_efforts") if isinstance(spec, dict) else None
        if not isinstance(levels, list) or effort not in levels:
            errors.append(f"{role}: unsupported model/effort pair {model}/{effort}")
        if effort in ("max", "ultra"):
            errors.append(f"{role}: default max/ultra pins are prohibited")
        if not model.startswith("gpt-6-"):
            exception = valid_exceptions.get(role, {})
            if not model.startswith("gpt-5.6-") or exception.get("model") != model or exception.get("effort") != effort:
                errors.append(f"{role}: legacy pin has no matching approved exception")
        if not isinstance(profile.get("rationale"), str) or not profile["rationale"].strip():
            errors.append(f"{role}: rationale is required")
        if profile.get("calibration_status") not in ("unrun", "evaluated"):
            errors.append(f"{role}: calibration_status must be unrun or evaluated")
        if profile.get("calibration_status") == "evaluated" and (not isinstance(profile.get("evaluation_evidence"), str) or not profile["evaluation_evidence"].strip()):
            errors.append(f"{role}: evaluated pin requires evaluation_evidence")
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
    """Validate TOML top-level name/model/model_reasoning_effort against policy."""
    errors = validate_policy(policy)
    if errors:
        return errors
    if not isinstance(agent, dict):
        return ["agent must be an object"]
    role = agent.get("name")
    profile = policy["profiles"].get(role) if isinstance(role, str) else None
    if profile is None:
        return [f"unregistered agent profile: {role!r}"]
    for key, expected in (("model", profile["model"]), ("model_reasoning_effort", profile["effort"])):
        if agent.get(key) != expected:
            errors.append(f"{role}: {key} policy drift: expected {expected!r}, got {agent.get(key)!r}")
    return errors
