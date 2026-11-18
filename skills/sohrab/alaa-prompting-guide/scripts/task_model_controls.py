"""Static explicit-control validation; no role allocation or runtime discovery."""

# Superseded Codex models: effort history only, never ordinary task selection.
HISTORICAL_MODELS = frozenset({"gpt-6-sol", "gpt-6.1-sol", "gpt-6-astra"})


def validate_task_selection(role, selection, policy, resolved=None):
    """Check a registered task role and BOTH requested controls; optional realized pair."""
    profiles = policy.get("profiles", {}) if isinstance(policy, dict) else {}
    profile = profiles.get(role) if isinstance(profiles, dict) and isinstance(role, str) else None
    if not isinstance(profile, dict) or profile.get("selection_mode") != "task-selected":
        return [f"{role!r}: registered task-selected authority role required"]
    if not isinstance(selection, dict) or set(selection) != {"model", "effort"} or any(
        not isinstance(selection.get(key), str) or not selection[key].strip()
        for key in ("model", "effort")
    ):
        return [f"{role}: explicit model AND effort required; inheritance is not selection"]
    models = policy.get("models", {})
    if policy.get("surface") == "codex" and selection["model"] in HISTORICAL_MODELS:
        return [f"{role}: historical model cannot authorize ordinary task selection"]
    model = models.get(selection["model"]) if isinstance(models, dict) else None
    if not isinstance(model, dict) or model.get("selection_enabled") is not True:
        return [f"{role}: unsupported or inactive model"]
    if selection["effort"] not in model.get("supported_efforts", []):
        return [f"{role}: unsupported model/effort pair"]
    if resolved is not None:
        if not isinstance(resolved, dict) or set(resolved) != {"model", "effort"} or resolved != selection:
            return [f"{role}: effective controls missing, unknown or different; affected lane blocked"]
    return []
