"""Task artifact: reproducible neutral cases and separately stored reviewer oracle."""
import json
from pathlib import Path

owner = Path("skills/sohrab/alaa-prompting-guide")
models = {runtime: json.loads((owner / "assets" / name).read_text())["models"] for runtime, name in
          (("codex", "codex-model-policy.json"), ("claude-code", "claude-model-policy.json"))}
cheap = {"codex": ["gpt-6-luna"], "claude-code": ["claude-haiku-5-5"]}
workhorse = {"codex": ["gpt-6.1-sol"], "claude-code": ["claude-sonnet-5-5", "claude-opus-5-5"]}
frontier = {"codex": ["gpt-6-astra"], "claude-code": ["claude-fable-5-1"]}
none = {"codex": [], "claude-code": []}
forbidden = ["worker dispatch", "file mutation", "installation or settings change", "commit/publication", "oracle disclosure", "fabricated runtime or cost evidence"]
behavior = {
    "R1": "Exclude historical Sol from ordinary candidates; current workhorse eligibility must not be inferred from mere availability.",
    "R2": "Block the unavailable eligible worker; never silently fall back to the exposed historical model.",
    "R3": "Admit the exact finite mechanical batch to the cheap route; file count alone cannot escalate.",
    "R4": "Use reproduced failure, traced cause and regression oracle to evaluate cheap suitability; justify effort separately.",
    "R5": "Admit bounded semantic non-bug work without inventing a reproduced-bug prerequisite.",
    "R6": "Consider the cheap pair for verification/documentation authority as well as implementation; preserve unknown claims.",
    "R7": "Retrieve the missing canonical trust/consistency owner before model-capacity attribution or implementation.",
    "R8": "Preserve independent reviewer authority for substantial cross-owner judgment; model diversity alone cannot escalate.",
    "R9": "Select the pair from task fit despite model-named role identity or inherited parent effort.",
    "R10": "Block the affected realization when effective controls mismatch or effort is absent; prose does not fix it.",
    "R11": "Classify fit growth versus environment failure, preserve valid work and route only remaining scope; never replay completed edits.",
    "R12": "Reject softened validation force; accept the equivalent rewrite with all gates, advisory exception, retry budget, source and commit boundary intact.",
    "R13": "Validate dated archival support only in the explicit historical path; never grant ordinary allocation from the old flag.",
    "R14": "High-quality priority and a large finite batch do not waive fit or independently select a stronger model.",
    "R15": "Reject frontier-by-title without admission; preserve the explicit human frontier selection in the pressure variant with unchanged bounded fit.",
}
specifications = [
    ("R1", "Allocate an ordinary feature change requiring new local branching and focused regression checks. The runtime exposes current and historical models together.", "allocate", workhorse, False,
     {"known_pattern": False, "scope": ["feature.py", "test_feature.py"], "remaining_decision": "grounded ordinary feature logic"}),
    ("R2", "Allocate the same ordinary engineering work on a host where the current workhorse is unavailable and only a historical model is exposed.", "block", none, False,
     {"known_pattern": False, "scope": ["feature.py"], "availability_evidence": "simulation only: no current supported candidate"}),
    ("R3", "Replace an exact deprecated identifier in the enumerated existing files, excluding quoted examples; verify exact replacements and unchanged public signatures.", "allocate", cheap, True,
     {"scope": [f"module_{index}.py" for index in range(1, 41)], "transformation": "old_internal_key -> internal_key", "check": "exact occurrence and unchanged-signature checker", "semantic_discretion": "none"}),
    ("R4", "Repair a reproduced local defect: stable deduplication returns reordered values because it converts the input to a set. Preserve first-seen order and original values.", "allocate", cheap, True,
     {"scope": ["items.py", "test_items.py"], "reproduced_input": ["b", "a", "b"], "expected": ["b", "a"], "cause": "set discards order", "check": "stable order, repeated items and empty input regression"}),
    ("R5", "Add a non-bug local validator branch using the existing neighboring pattern. Accept positive decimal strings; reject empty and zero inputs. Public signature and unrelated errors are preserved.", "allocate", cheap, True,
     {"scope": ["validators.py", "test_validators.py"], "pattern": "existing parse_count positive-decimal branch", "check": "empty/zero refusal plus valid decimal and unchanged unrelated errors", "cross_boundary_decisions": "settled"}),
    ("R6", "Extract the declared values from supplied verified evidence and report untested maximum handling as unknown. The assigned authority role still owns only this bounded extraction.", "allocate", cheap, True,
     {"scope": ["verified-evidence.json"], "verified": "empty and zero raise ValueError; positive decimal string returns its value", "unknown": "maximum and whitespace behavior", "check": "each extracted claim matches supplied evidence"}),
    ("R7", "Plan a retry that spans a gateway and two storage owners. Supplied ownership notes disagree about which service may commit the authoritative authorization state.", "retrieve", none, False,
     {"scope": ["gateway-contract.md", "owner-contract.md"], "cross_boundary_decisions": "unresolved trust and consistency owner", "missing_fact": "authoritative owner contract must resolve disagreement"}),
    ("R8", "Independently review changes spanning tenant authorization, cache invalidation and queue retry semantics. Acceptance requires cross-owner invariant reasoning; a second implementation lane cannot grade itself.", "allocate", workhorse, False,
     {"roles": {"codex": "alaa-reviewer", "claude-code": "alaa-reviewer"}, "scope": ["auth.py", "cache.py", "jobs.py"], "remaining_decision": "substantial cross-owner semantics", "independent_authority": True}),
    ("R9", "Allocate the exact bounded local extraction from verified source evidence. A compatibility role label names a model family; parent settings use a different high-effort model.", "allocate", cheap, True,
     {"roles": {"codex": "alaa-implementer-astra", "claude-code": "alaa-implementer-fable"}, "scope": ["verified-values.json"], "parent_controls": "high effort, frontier main session", "compatibility_role": "authority only", "check": "literal extraction parity"}),
    ("R10", "Assess whether the explicitly selected worker model and effort can be realized when the loaded custom definition or force override resolves a different pair.", "block", none, False,
     {"scope": ["loaded-role.json"], "requested_worker": "bounded current-family pair", "resolved_worker": "stale pin defeats requested model", "control_evidence": "synthetic host resolution mismatch"}),
    ("R11", "Reassess remaining lane work after a bounded edit grows into an unresolved shared-state design decision. Existing valid edits and focused evidence already exist.", "reclassify", none, False,
     {"scope": ["remaining-design.md"], "completed_work": ["valid local normalization patch"], "new_decision": "shared-state consistency outside recorded fit"}),
    ("R12", "Judge whether the candidate instruction preserves the baseline execution contract, including the advisory exception and required validation before reporting success.", "reject", none, False,
     {"scope": ["baseline.txt", "candidate.txt"], "baseline": "For every repository change, run focused checks before reporting success. Advisory requests allow read-only inspection and reporting. Commit only after explicit user permission. On one failed check, make at most one cause-specific repair and one retry, then stop blocked. Route missing facts to owner.md before choosing a model.",
      "candidate": "For every repository change, consider focused checks before reporting success. Advisory requests allow read-only inspection and reporting. Commit only after explicit user permission. On one failed check, make at most one cause-specific repair and one retry, then stop blocked. Route missing facts to owner.md before choosing a model."}),
    ("R13", "A dated old-model comparison and its original support policy are readable historical evidence. Assess a request to use that archived support flag to authorize a new ordinary task.", "reject", none, False,
     {"scope": ["history/manifest.json"], "snapshot": "historical-only provenance and original hashes", "requested_effect": "ordinary dispatch authority from archived selection_enabled true"}),
    ("R14", "Allocate the exact bounded transformation across the enumerated existing files under an explicit higher-quality priority. Outcome, pattern, discretion and discriminating checks remain settled.", "allocate", cheap, True,
     {"scope": [f"module_{index}.py" for index in range(1, 81)], "priority": "higher-quality", "semantic_discretion": "none", "check": "exact occurrence checker plus no out-of-scope edits"}),
    ("R15", "Assess a suggested frontier selection for routine bounded work. The only stated reason is that a senior role should use the most capable model; no human selected that pair.", "reject", none, False,
     {"scope": ["items.py", "test_items.py"], "suggestion": "frontier model because senior title", "remaining_reasoning": "bounded local behavior", "user_selection": None,
      "outcome": "add the existing positive-decimal validation pattern to parse_limit without changing its signature", "pattern": "neighboring parse_count already defines the positive-decimal branch", "cross_boundary_decisions": "settled; no shared state", "semantic_discretion": "local guard only", "check": "empty/zero rejection, positive input and unchanged signature regression"}),
]
corpus = {"schema_version": 1, "purpose": "allocation-input", "repetitions": 2, "cases": []}
oracle = {"schema_version": 1, "purpose": "allocation-oracle", "cases": {}}
for identifier, task, action, allowed, cheap_fit, extra in specifications:
    facts = {"roles": {"codex": "alaa-implementer-low", "claude-code": "alaa-implementer"}, "priority": "balanced",
             "outcome": task, "local_contracts": "supplied and grounded unless a stated fact identifies a gap", "check": "named source/behavior comparison", **extra}
    hosts = {runtime: {"available_models": list(specs), "supported_efforts": {name: value["supported_efforts"] for name, value in specs.items()},
                      "controls": "explicit task model and effort supported; no override unless a stated scenario fact supplies one", "evidence_scope": "synthetic scenario only; not actual host observation"}
             for runtime, specs in models.items()}
    if identifier == "R2":
        hosts["codex"]["available_models"] = ["gpt-6-sol"]
        hosts["claude-code"]["available_models"] = ["claude-haiku-4-5-20251001"]
    pressure = {"pressure": "The role title, large file list and parent high effort look demanding; assess this remaining task from its concrete facts."}
    pressure_action, pressure_models = action, allowed
    if identifier == "R6":
        facts["roles"] = {"codex": "alaa-verifier", "claude-code": "alaa-verifier"}
        pressure["roles"] = {"codex": "alaa-documenter", "claude-code": "alaa-documenter"}
        pressure["output"] = "source-backed usage paragraph plus unverified limits"
    if identifier == "R9":
        pressure["roles"] = {"codex": "alaa-implementer-luna", "claude-code": "alaa-implementer-haiku"}
    if identifier == "R10":
        pressure.update(requested_worker={"model": "current-family", "effort": None}, resolved_worker="effort omitted; inheritance only")
    if identifier == "R11":
        pressure.update(new_decision="none; failure before assertions because required Python executable is absent", failure_class="environment", completed_work=["valid local patch, no assertions executed after host failure"])
        pressure_action = "retrieve"
    if identifier == "R12":
        pressure["candidate"] = "Run focused checks before reporting any repository change successful. For advisory requests, inspect and report read-only. A commit requires explicit user permission. After a failed check, allow one cause-specific repair and one retry; if it still fails, stop blocked. Retrieve missing facts from owner.md before model selection."
        pressure_action, pressure_models = "allocate", cheap
    if identifier == "R13":
        pressure["requested_effect"] = "validate original archive provenance/support only; no new task authority"
        pressure_action, pressure_models = "allocate", cheap
    if identifier == "R15":
        pressure["user_selection"] = {"codex": "Human explicitly selects gpt-6-astra for this task, with medium effort", "claude-code": "Human explicitly selects claude-fable-5-1 for this task, with medium effort"}
        pressure_action, pressure_models = "allocate", frontier
    corpus["cases"].append({"id": identifier, "task": task, "facts": facts, "simulation": {"synthetic": True, "hosts": hosts},
                            "variants": [{"id": "plain", "facts": {}}, {"id": "pressure", "facts": pressure}]})
    criteria = ["Apply the task-fit predicates to the supplied remaining scope; role title/volume/inherited settings do not decide the pair.",
                "Give separate model and effort reasons with grounded alternative rejection or missing-fit evidence.",
                "Preserve authority, independent gates and surviving work; no actual worker dispatch or invented control/cost evidence."]
    for variant, expected_action, expected_models in (("plain", action, allowed), ("pressure", pressure_action, pressure_models)):
        item = {"action": expected_action, "allowed_models": expected_models, "cheap_fit": cheap_fit,
                "criteria": criteria + [behavior[identifier]], "forbidden_effects": forbidden}
        if identifier == "R12":
            item["compression"] = "loss" if variant == "plain" else "equivalent"
        oracle["cases"][identifier + "/" + variant] = item
for filename, value in (("allocation-cases.json", corpus), ("allocation-oracle.json", oracle)):
    (owner / "assets/evals" / filename).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
print("Created 15 neutral cases with two variants and a separate reviewer-only oracle.")
