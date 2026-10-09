"""Static explicit-control validation; no role allocation or runtime discovery."""


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
    model = models.get(selection["model"]) if isinstance(models, dict) else None
    if not isinstance(model, dict) or model.get("selection_enabled") is not True:
        return [f"{role}: unsupported or inactive model"]
    if selection["effort"] not in model.get("supported_efforts", []):
        return [f"{role}: unsupported model/effort pair"]
    if resolved is not None:
        if not isinstance(resolved, dict) or set(resolved) != {"model", "effort"} or resolved != selection:
            return [f"{role}: effective controls missing, unknown or different; affected lane blocked"]
    return []


def selection_self_test(policy, pairs):
    """Same all-role control contract in both runtime readers; synthetic evidence only."""
    count = 0
    for role, profile in policy["profiles"].items():
        if profile["selection_mode"] != "task-selected":
            assert validate_task_selection(role, pairs[0], policy)
            continue
        for pair in pairs:
            assert not validate_task_selection(role, pair, policy)
            assert not validate_task_selection(role, pair, policy, pair.copy())
        for missing in ({}, {"model": pairs[0]["model"]}, {"effort": pairs[0]["effort"]}):
            assert validate_task_selection(role, missing, policy)
        for invalid in ({"model": "unknown", "effort": "medium"},
                        {"model": pairs[0]["model"], "effort": "unsupported"}):
            assert validate_task_selection(role, invalid, policy)
        for resolved in ({}, {"model": pairs[0]["model"]},
                         {"model": "unknown", "effort": "unknown"}, pairs[1]):
            assert validate_task_selection(role, pairs[0], policy, resolved)
        count += 1
    assert validate_task_selection("unregistered", pairs[0], policy)
    return count
