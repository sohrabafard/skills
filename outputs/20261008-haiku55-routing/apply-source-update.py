"""One scoped source update; no installation or live model execution."""
from pathlib import Path
import json
import re

ROOT = Path.cwd()
PACK = ROOT / "skills/sohrab"
ARCHIVE = ROOT / "outputs/20261008-haiku55-routing"
PG = PACK / "alaa-prompting-guide"
CC = PACK / "alaa-cc-orchestrator"
CX = PACK / "alaa-codex-orchestrator"
before = {}


def write(path, text):
    before.setdefault(path, path.read_bytes() if path.exists() else None)
    path.write_text(text, encoding="utf-8", newline="\n")


def replace(path, old, new):
    text = path.read_text(encoding="utf-8")
    assert old in text, (path, old)
    write(path, text.replace(old, new))


# Pass one records the decisions; pass two below ships shorter equivalent instructions.
drafts = {
    "gate economics": "Before dispatching validation, the lead must create one list of all required checks. It must record what each aggregate actually executes and which child checks remain uncovered. If the aggregate executes exactly the same child gate with the same scoped inputs, environment and flags under the required independent authority, run the aggregate instead of repeating that child. Do not count a wrapper and child as two independent passes. Preserve mandatory gates, changed-input reruns, independent observers and checker self-tests when checker logic changes. Reuse follows existing Evidence quality and testing doctrine. Do not repeat checks for a phase transition or new agent alone.",
    "Haiku explorer": "The explorer must receive one bounded repository question with named starting paths or symbols and explicit required evidence. It must read and follow applicable guidance, trace the real ownership and execution paths, and report evidence for each requested relationship. It must finish only when every requested edge or ownership fact has evidence, or mark the missing evidence and report the smallest next inspection. When answering needs architecture judgment, a wider investigation or external research, it must return that need to the lead and must not broaden itself.",
    "Haiku verifier": "The verifier receives an exact finite command list that the lead has already consolidated. It executes only those commands in the supplied directory with the supplied resources and captures an observed result for every command. It must not diagnose failures, repair commands, choose substitutes, reorder the plan or invent a missing result. Report an ambiguous or blocked command to the lead for the owning analyst. Finish only when every command has an observed classification or an explicit reason why it could not run. No unrun check is a pass.",
    "Haiku documenter": "The documenter works only on the named documents and sections after review, using reconciled verified behavior and implementation evidence. It must inspect that evidence, update affected documentation, check changed links and examples through established commands, and report every required size grade. It must not infer missing behavior or decide new API, architecture or operational policy. Return unclear evidence or a wider documentation contract to the lead before dependent edits; complete only when each named document is updated and grounded or explicitly unchanged for a reason.",
}
write(ARCHIVE / "instruction-drafts.md", "# Instruction drafts\n\n" + "\n\n".join(f"## {name}\n\n{text}" for name, text in drafts.items()) + "\n")

policy_path = PG / "assets/claude-model-policy.json"
policy = json.loads(policy_path.read_text(encoding="utf-8"))
policy["policy_version"] = "2.0.0"
policy["verified_on"] = "2026-10-08"
for source in policy["sources"]:
    if source["id"] in {"effort", "model-config", "subagents"}:
        source["verified_on"] = "2026-10-08"
    if source["id"] == "effort":
        source["scope"] = "Generation-specific supported effort values; Haiku 5.5 supports effort, historical Haiku 4.5 does not"
for sid, url, scope in (
    ("haiku-launch", "https://www.anthropic.com/claude-haiku-5-5", "Announced workloads; vendor claims are not local calibration"),
    ("haiku-migration", "https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide", "Exact ID, effort, adaptive thinking and disabled/manual API boundaries"),
    ("haiku-prompt", "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5", "Explicit retrieval, checking, completion and bounded dispatch guidance"),
):
    policy["sources"].append({"id": sid, "url": url, "verified_on": "2026-10-08", "scope": scope})
policy["models"]["claude-haiku-5-5"] = {
    "supported_efforts": ["low", "medium", "high", "xhigh", "max"],
    "default_effort": "medium", "thinking_mode": "adaptive",
    "source_ids": ["haiku-migration", "effort", "model-config"],
    "minimum_claude_code": "2.1.293",
    "notes": "API disabled thinking is allowed at low/medium/high; xhigh/max require adaptive. Manual budgets are unsupported. Claude Code prevents disabling thinking for this model. API capability does not authorize a harness control."
}
haiku_roles = {"alaa-explorer", "alaa-verifier", "alaa-documenter", "alaa-browser-qa"}
fable_roles = {"alaa-implementer-opus", "alaa-architecture-critic", "alaa-adversarial-reviewer", "alaa-instruction-reviewer", "alaa-failure-analyst"}
medium_roles = {"main", "alaa-spec-analyst", "alaa-researcher"}
reasons = {
    "alaa-explorer": ("Bounded repository retrieval with named starts, explicit relationship evidence and completion checks; unrun workload hypothesis.", "Return wider architecture, external research or unresolved ownership judgment to the lead."),
    "alaa-verifier": ("Finite, consolidated exact-command execution with observed outcomes and no diagnosis or repair; unrun workload hypothesis.", "Return ambiguity, command repair and failure diagnosis to the lead and owning analyst."),
    "alaa-documenter": ("Named documentation updates from verified behavior, with link/example checks and completion criteria; unrun workload hypothesis.", "Return missing behavior evidence, policy decisions or broader documentation scope to the lead."),
    "alaa-browser-qa": ("Declared URL/environment/scenario execution and browser evidence collection; unrun workload hypothesis.", "Return ambiguous scenarios, design judgment and wider flow scope to the lead."),
    "alaa-implementer-opus": ("Concrete unresolved design choices affecting correctness or failure behavior; unrun workload hypothesis.", "Use only when the routing matrix records the qualifying open decision; settled work returns to the default role."),
    "alaa-architecture-critic": ("Cross-cutting architecture and interacting invariants require difficult judgment; unrun workload hypothesis.", "Diagnose missing source/context before considering greater effort."),
    "alaa-adversarial-reviewer": ("Attack load-bearing assumptions for the named blast-radius/conflict trigger; unrun workload hypothesis.", "Return conflicts to the lead; never begin a fix loop."),
    "alaa-instruction-reviewer": ("Instruction ownership, authority, loading scope and compression fidelity require difficult judgment; unrun workload hypothesis.", "Return missing source/intent to the lead; never invent policy."),
    "alaa-failure-analyst": ("Interacting ambiguous, cross-lane or environmental failure evidence requires difficult diagnosis; unrun workload hypothesis.", "Exclude missing tools/context/spec facts before changing effort."),
    "alaa-researcher": ("General official-source and repository research with source reconciliation; unrun workload hypothesis.", "Escalate unresolved cross-system judgment after evidence and context are complete."),
    "alaa-implementer": ("Ordinary implementation of a ratified contract with focused checks; unrun workload hypothesis.", "Route unresolved qualifying design choices to difficult implementation."),
}
for name, profile in list(policy["profiles"].items()):
    model = "claude-haiku-5-5" if name in haiku_roles else "claude-fable-5-1" if name in fable_roles else "claude-opus-5-5"
    profile["model"] = model
    profile["effort"] = "medium" if name in haiku_roles | medium_roles else "high"
    profile["availability"]["minimum_claude_code"] = policy["models"][model]["minimum_claude_code"]
    profile["source_ids"] = ["effort", "model-config", "subagents"] + (["haiku-launch", "haiku-migration", "haiku-prompt"] if name in haiku_roles else ["models", "fable-prompt"] if name in fable_roles else ["models", "opus-prompt"])
    if name in reasons:
        profile["rationale"], profile["escalation_criterion"] = reasons[name]
    profile["calibration_status"] = "unrun"
    if name == "alaa-implementer-opus":
        profile["artifacts"] = ["skills/sohrab/alaa-cc-orchestrator/agents/alaa-implementer-fable.md"]
        del policy["profiles"][name]
        policy["profiles"]["alaa-implementer-fable"] = profile
policy["notes"] = "Active starting hypotheses use Haiku 5.5, Opus 5.5 and Fable 5.1. Historical models remain comparison snapshots only. No live calibration, account check, installation or runtime activation is implied; unavailable targets never silently fall back."
write(policy_path, json.dumps(policy, indent=2) + "\n")

# The parent performs the original-file retirement before this script runs.
for path in CC.rglob("*"):
    if path.is_file() and path.suffix in {".md", ".py"} and path.name != "CHANGELOG.md":
        text = path.read_text(encoding="utf-8")
        if "alaa-implementer-opus" in text:
            write(path, text.replace("alaa-implementer-opus", "alaa-implementer-fable"))
for path in (PG / "scripts/claude_model_policy.py",):
    replace(path, "implementer-opus", "implementer-fable")
    replace(path, r"claude-(?:opus|sonnet|fable)-\d+(?:-\d+)?|claude-haiku-\d+-\d+-\d{8}", r"claude-(?:opus|sonnet|fable)-\d+(?:-\d+)?|claude-haiku-(?:5-5|4-5-\d{8})")
    replace(path, 'if model.startswith("claude-haiku-") and levels != []:', 'if model.startswith("claude-haiku-4-5-") and levels != []:')
    replace(path, 'Haiku has no effort parameter', 'Haiku 4.5 has no effort parameter')
for name, profile in policy["profiles"].items():
    if name == "main":
        continue
    path = ROOT / profile["artifacts"][0]
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^model: .*$", f'model: {profile["model"]}', text, flags=re.M)
    text = re.sub(r"^effort: .*$", f'effort: {profile["effort"]}', text, flags=re.M)
    if name == "alaa-implementer-fable":
        text = text.replace(" Compatibility identifier retained.", "")
    if text != path.read_text(encoding="utf-8"):
        write(path, text)

replace(CC / "agents/alaa-explorer.md", "Answer one bounded repository question with direct evidence.", "Answer one bounded repository question with direct evidence. Require named starting paths/symbols and requested relationships; return missing scope to the lead before investigation.")
replace(CC / "agents/alaa-explorer.md", "Authority:\n", "Complete only when every requested ownership fact or edge has evidence or an explicit unresolved boundary and next inspection. Return wider architecture judgment or investigation to the lead; never expand the lane.\n\nAuthority:\n")
replace(CC / "agents/alaa-verifier.md", "2. Run commands exactly as dispatched, from the specified cwd.", "2. Run the lead's finite, consolidated command list exactly as dispatched, from the specified cwd. Apply its aggregate coverage and eligible evidence citations; never add or repeat checks on your own.")
replace(CC / "agents/alaa-verifier.md", "- Never fix a failure or change command semantics to obtain a pass.", "- Never diagnose or fix a failure, substitute, reorder or repair commands, or change semantics to obtain a pass. Return ambiguous or blocked evidence to the lead and owning analyst.")
replace(CC / "agents/alaa-verifier.md", "Report metadata after", "Complete when every supplied command has an observed classification or an explicit unrun/block reason. Missing evidence never passes.\n\nReport metadata after")
replace(CC / "agents/alaa-documenter.md", "Rules:\n", "Use the named documents/sections and reconciled evidence only. Return missing behavior evidence, policy decisions or wider scope to the lead before dependent edits. Complete when each named document is grounded and updated or explicitly unchanged; report required link/example checks and size grades.\n\nRules:\n")
replace(CC / "agents/alaa-explorer.md", "Fast read-only repository mapper for orchestrated goals.", "Bounded read-only repository mapper with named starting paths/symbols and required relationship evidence.")
replace(CC / "agents/alaa-documenter.md", "Documentation-only lane after implementation/review gates.", "Bounded documentation lane for named documents/sections and verified behavior after implementation/review gates.")
browser_path = CC / "agents/alaa-browser-qa.md"
browser_text = browser_path.read_text(encoding="utf-8")
browser_head, browser_body = browser_text.split("\n---\n", 1)
write(browser_path, browser_head + "\n---\n" + "\nUse only the declared URL, environment and scenarios. Collect browser evidence for each scenario and finish with an observed outcome or explicit block for every item. Return ambiguity, scenario/design judgment or wider flow scope to the lead before dependent work; never choose broader scenarios.\n" + browser_body)

economics = """Before validation dispatch, record one check list in the existing plan: required gates, exact scoped inputs and commands, aggregate-to-child coverage, observer, and eligible evidence citations. Inspect aggregate execution; a wrapper's name proves no coverage. Run an aggregate instead of its identical covered children only when inputs, environment, flags and required independent authority match. Run uncovered gates separately; report partial coverage. Count underlying checks once, not wrapper and child as separate passes. Phase transitions and new agents alone earn no rerun. Evidence quality below owns reuse; /alaa-testing-strategy owns stricter proof and fresh exhaustive gates. Preserve mandatory checks and changed-input reruns; run checker self-tests only when checker logic changes.\n\n"""
for root in (CC, CX):
    replace(root / "references/verification-and-gates.md", "1. **Resolve cheap read-only gates", economics + "1. **Resolve cheap read-only gates")
    replace(root / "SKILL.md", "Run `python scripts/check_agent_contracts.py` after instruction-contract changes", "Schedule the commands below through `references/verification-and-gates.md` Gate economics; proven aggregate coverage may discharge an identical child invocation, never a different scope or observer.\n\nRun `python scripts/check_agent_contracts.py` after instruction-contract changes")
    replace(root / "SKILL.md", "checks run versus checks cited", "underlying checks run versus checks cited (count covered children once)")
replace(CX / "agents/alaa-verifier.toml", "2. Run commands exactly as dispatched, from the specified cwd.", "2. Run the lead's consolidated command list exactly as dispatched, from the specified cwd. Apply its coverage and eligible evidence citations; never add or repeat checks on your own.")

replace(PG / "SKILL.md", "Sonnet 5.5, or Haiku 4.5", "or Haiku 5.5")
replace(PG / "SKILL.md", "from this skill directory run\n`python scripts/check_claude_model_policy.py`", "from this skill directory run\n`python scripts/check_claude_model_policy.py`") if False else None
replace(PG / "SKILL.md", "Source consistency proves neither installed activation nor calibration.", "A verified aggregate may discharge an identical covered command; the active orchestrator's Gate economics owns consolidation, and uncovered managed roots still require this check. Source consistency proves neither installed activation nor calibration.")
replace(PG / "references/00-topic-map.md", "| Assess Haiku for a bounded comparison | `references/35-haiku-4-5.md` | It lacks effort support and uses a different thinking control |", "| Tune current Haiku prompts or select bounded retrieval, verification or documentation | `references/36-haiku-5-5.md` | Explicit completion, retrieval and check instructions preserve bounded work |\n| Compare historical Haiku 4.5 explicitly | `references/35-haiku-4-5.md` | Its missing effort support does not transfer to Haiku 5.5 |")
replace(PG / "references/00-topic-map.md", "Tune current Sonnet prompting or migrate Sonnet API controls", "Compare retained Sonnet prompting or migrate Sonnet API controls explicitly")
replace(PG / "references/90-model-selection.md", "Compare Fable or Haiku only in an explicitly authorized, representative evaluation; neither is an automatic local fallback.", "Use the registered Haiku, Opus or Fable role profile; none is an automatic fallback. Historical Sonnet and Haiku 4.5 snapshots authorize no active profile.")
replace(PG / "references/50-effort-and-thinking.md", "thinking controls. Current Opus, Fable and Sonnet reject disabled/manual thinking; their\nmodel references own supported modes and exceptions. Haiku uses extended thinking and has\nno effort parameter. These API controls are not interchangeable Claude Code settings.", "thinking controls. Current model references own modes and exceptions. Haiku 5.5 supports effort and adaptive thinking; its API disabled-thinking exception does not transfer to Claude Code. Historical Haiku 4.5 uses extended thinking without effort. These API controls are not interchangeable Claude Code settings.")
replace(PG / "references/50-effort-and-thinking.md", "them. For Haiku, use its own supported thinking controls.", "them. Read `references/36-haiku-5-5.md` for current Haiku controls.")
replace(PG / "references/50-effort-and-thinking.md", "Do not carry manual thinking budgets into adaptive-only models. Haiku is the extended-thinking\nexception.", "Do not carry manual thinking budgets into current adaptive models. Historical Haiku 4.5 is the extended-thinking exception.")
replace(PG / "references/50-effort-and-thinking.md", "`references/35-haiku-4-5.md`, `references/12-gpt-6.md`", "`references/36-haiku-5-5.md`, `references/12-gpt-6.md`")
replace(PG / "references/35-haiku-4-5.md", "Haiku is a comparison candidate", "Historical Haiku 4.5 is a comparison candidate")
replace(PG / "references/35-haiku-4-5.md", "Haiku uses extended thinking", "Haiku 4.5 uses extended thinking")
replace(PG / "references/93-claude-evaluation.md", "The architecture case compares Fable explicitly at shared effort; it creates no default role\nor fallback. Haiku needs a separately designed comparison because its missing effort control\nprevents a model-only comparison at a shared effort.", "The architecture case compares the registered Fable profile with Opus at shared effort; the corpus does not prove that routing choice or authorize fallback. Current Haiku 5.5 has effort-enabled candidate pairs. Historical Haiku 4.5 needs a separate control-regime comparison.")
replace(PG / "references/42-fable-5-1.md", "Explicit comparisons may test Fable for unresolved demanding reasoning or long-horizon work\nafter diagnosing the current profile's context and tools.", "The policy assigns Fable to difficult judgment roles as unrun starting hypotheses. Explicit comparisons may test those hypotheses after diagnosing context and tools; no source claim proves local superiority.")
replace(PG / "references/00-source-map.md", "Opus 5.5, Sonnet 5.5, and Fable 5.1", "Opus 5.5, Fable 5.1, Haiku 5.5, and retained Sonnet 5.5")
write(PG / "references/00-source-map.md", (PG / "references/00-source-map.md").read_text(encoding="utf-8") + "\nHaiku 5.5 launch, migration, prompting, effort and Claude Code selection/subagent sources were refreshed 8 October 2026. Read `references/36-haiku-5-5.md` for URLs, workload limits and API-versus-harness controls. Local calibration and installed activation remain unrun.\n")
replace(PG / "references/41-claude-code-runtime-features.md", "The policy records minimum versions for its assigned profiles; Fable 5.1 additionally requires\n2.1.257.", "The policy records sourced minimum versions for assigned profiles. Haiku 5.5 requires Claude Code 2.1.293; unlike its API disabled-thinking exception, Code prevents switching thinking off for it (verified 8 October 2026 against model-config).")
replace(PG / "references/06-invocation-and-composition.md", "- **Claude Sonnet 5.5", "- **Claude Haiku 5.5 — bound delegated work explicitly.** Give one concrete task, named retrieval sources, required checks and completion/failure conditions. General fan-out polarity remains unmeasured; never infer lead suitability from subagent performance. Read `references/36-haiku-5-5.md` before tuning.\n- **Claude Sonnet 5.5")

haiku_reference = """# Claude Haiku 5.5

Use for bounded retrieval, exact-procedure execution and documentation from verified behavior. `assets/claude-model-policy.json` owns assigned role pins, effort, availability and calibration. The launch's fast agentic-work claims support candidate workload selection; they do not prove local quality, latency or equivalence to a GPT model.

## Prompting and work boundaries

Give one outcome, named inputs or retrieval starts, required evidence/checks, allowed tools and side effects, and explicit completion and failure conditions. Require retrieval before factual conclusions and observed checks before success. Keep narrow lanes complete: report every requested item as evidenced or unresolved, and stop at the acceptance criteria. Return missing scope/evidence, wider architecture judgment or ambiguous failures to the lead rather than inventing facts or expanding the task.

The orchestrator owns role triggers and independent gates. Use its registered bounded explorer, verifier, browser-evidence and documenter profiles; general research, policy design and difficult review need their own registered profiles. Do not make Haiku the lead or a universal fallback from a vendor benchmark. Unknown serving identity remains unknown; missing target access blocks dispatch.

## API and Claude Code controls

Verified 8 October 2026: exact ID `claude-haiku-5-5`; supported efforts `low`, `medium`, `high`, `xhigh`, `max`; default `medium`. Adaptive thinking is supported and manual token budgets are unsupported. The API permits disabled thinking through `high`; `xhigh` and `max` require adaptive. Claude Code prevents disabling thinking for this model and requires version 2.1.293 or later. API controls do not establish a Claude Code setting.

Treat the assigned medium effort as an unrun workload hypothesis. Compare one factor at a time on representative tasks before claiming quality or savings. Inspect account/provider mapping, override precedence, caps and effective tools before activation through `references/41-claude-code-runtime-features.md`. Historical Haiku 4.5 has no effort parameter; its controls never govern this generation.

## Sources and unrun limits

- [Launch and stated workloads](https://www.anthropic.com/claude-haiku-5-5)
- [Migration and API controls](https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide)
- [Prompting Haiku 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5)
- [Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Code model configuration](https://code.claude.com/docs/en/model-config)
- [Code subagents](https://code.claude.com/docs/en/sub-agents)

No live model calls, installation, account entitlement checks or local calibration ran. Static policy agreement proves source consistency only.
"""
write(ARCHIVE / "haiku-reference-draft.md", haiku_reference.replace("Give one outcome", "For each bounded task, the dispatch must explicitly give one outcome").replace("API controls do not establish", "The fact that an API control is documented does not establish"))
write(PG / "references/36-haiku-5-5.md", haiku_reference)

corpus_path = PG / "assets/evals/claude-agent-comparisons.json"
corpus = json.loads(corpus_path.read_text(encoding="utf-8"))
corpus["policy_version"] = policy["policy_version"]
for case in corpus["scenarios"]:
    profile = policy["profiles"][case["profile"]]
    case["candidate"] = {key: profile[key] for key in ("model", "effort")}
    case["comparator"] = {"model": "claude-opus-5-5", "effort": "high"} if case["id"] == "architecture" else {"model": profile["model"], "effort": "low" if profile["effort"] == "medium" else "medium"}
write(corpus_path, json.dumps(corpus, indent=2) + "\n")

replace(CC / "references/model-effort-policy.md", "Role identifiers remain stable for callers, including the historical `alaa-implementer-fable` name.", "The difficult implementation role is `alaa-implementer-fable`; the retired `alaa-implementer-opus` is not an alias. Source updates do not change installed definitions. Before an explicitly authorized update, inspect managed stale wrappers and retire the old one with separate target-path authority; never dispatch both or treat a wildcard copy as retirement.")
replace(CC / "references/agent-catalog.md", "Run `python scripts/check_agent_grants.py` after any change", "Schedule `python scripts/check_agent_grants.py` (or its identical aggregate-covered invocation under Gate economics) after any change")
replace(CC / "VERSION", "4.2.1", "5.0.0")
replace(CC / "CHANGELOG.md", "# Changelog\n", "# Changelog\n\n## 5.0.0 - 2026-10-08\n\n- Project the prompting guide's Haiku 5.5, Opus 5.5 and Fable 5.1 routing; keep calibration unrun and preserve grants. Haiku work has bounded evidence and completion contracts.\n- Rename difficult implementation to `alaa-implementer-fable`; no source alias remains. Authorized installed updates must inspect and retire stale `alaa-implementer-opus` wrappers separately; wildcard copying does not retire them.\n- Consolidate actual aggregate/child coverage and eligible independent evidence in one check list; preserve mandatory gates and changed-input reruns.\n")
replace(ROOT / "install-skills.md", "# Claude world — once, applies to every project", "# Claude world — once, applies to every project") if False else None
replace(ROOT / "install-skills.md", "The Codex `agents/*.toml` files are transport-neutral templates.", "Claude source version 5.0.0 renames the difficult implementation role to `alaa-implementer-fable`. The wildcard copy above leaves a previously installed `alaa-implementer-opus.md` in place. Before a future authorized update, inspect and retire that managed old wrapper under explicit target-path authority; never dispatch both names or assume the copy retires it. Read `skills/sohrab/alaa-cc-orchestrator/references/model-effort-policy.md`. This source update does not install or retire agents on your machine.\n\nThe Codex `agents/*.toml` files are transport-neutral templates.")

# Concrete generation compatibility warrants a small extension of the existing self-test.
replace(PG / "scripts/check_claude_model_policy.py", "    for filename in (\"duplicate.json\", \"malformed.json\"):", "    current_haiku = copy.deepcopy(policy)\n    current_haiku[\"profiles\"][role].update(model=\"claude-haiku-5-5\", effort=\"medium\")\n    current_haiku[\"profiles\"][role][\"availability\"][\"minimum_claude_code\"] = \"2.1.293\"\n    assert not validate_policy(current_haiku)\n    assert not validate_agent_pin({\"name\":role, \"model\":\"claude-haiku-5-5\", \"effort\":\"medium\"}, current_haiku, role + \".md\")\n    current_haiku[\"profiles\"][role][\"effort\"] = None\n    assert validate_policy(current_haiku), \"Haiku 5.5 requires a supported effort\"\n    for filename in (\"duplicate.json\", \"malformed.json\"):")

compression = """# Compression evidence

Pass one: instruction-drafts.md and haiku-reference-draft.md record the complete decisions. Pass two: shipped blocks remove narration/repeated qualifiers; no trigger, exception, authority, source date, failure condition or check changes between draft and compressed text. Existing pin changes and role rename are explicit policy changes, not claimed compression.

| Block | Draft | Shipped location | Behavior preserved |
|---|---|---|---|
| Consolidation | instruction-drafts.md: gate economics | Both orchestrator verification-and-gates.md | One list, inspected aggregate coverage, proper observer, no duplicate child, uncovered checks, changed inputs, mandatory gates and self-test trigger |
| Explorer | instruction-drafts.md: Haiku explorer | CC alaa-explorer.md | Named starts, actual retrieval, per-item evidence, unresolved boundary and return of wider judgment |
| Verifier | instruction-drafts.md: Haiku verifier | CC alaa-verifier.md | Finite exact list, observed results, no repair/diagnosis, explicit unrun/block and completion |
| Documenter | instruction-drafts.md: Haiku documenter | CC alaa-documenter.md | Named docs, verified evidence, no policy invention, links/examples/grades and completion |
| Haiku reference | haiku-reference-draft.md | Prompting guide 36-haiku-5-5.md | Same scope, controls, source dates, gates, runtime limits and unrun status |

Remaining edits are precise substitutions/projections of the ratified policy: active pins, generation-specific capability references, renamed role callers and checker identifiers. The existing sentences provide the draft; substitutions preserve their surrounding contract while changing only the stated ratified behavior. Consolidation command pointers route to the owner instead of copying its doctrine. New source-level capability: bounded Haiku 5.5 routing with effort; new scheduling capability: explicit aggregate-child accounting. No speed or quality measurement is claimed.
"""
write(ARCHIVE / "compression-evidence.md", compression)
write(ARCHIVE / "source-evidence.md", "# Source evidence - 8 October 2026\n\nThe lead verified these official sources before ratifying the lane; this writer reused that research rather than duplicating retrieval.\n\n" + "\n".join(f"- {s['id']}: {s['url']} (verified {s['verified_on']}); {s['scope']}." for s in policy["sources"] if s["id"] in {"haiku-launch", "haiku-migration", "haiku-prompt", "effort", "model-config", "subagents"}) + "\n\nExact Haiku ID claude-haiku-5-5; efforts low/medium/high/xhigh/max, default medium; Code >=2.1.293. API thinking may be disabled through high; Code prevents switching it off. Manual budgets unsupported. Active routing is local starting policy, not a vendor comparative ranking. Profiles remain unrun. No live models, account/access checks, installation, model-quality benchmark or latency measurement ran. Prior Opus/Fable snapshots retain their own source dates.\n")
write(ARCHIVE / "changed-source-files.json", json.dumps([p.relative_to(ROOT).as_posix() for p in before if p.is_relative_to(PACK) or p.name == "install-skills.md"], indent=2) + "\n")
print(f"Updated {len(before)} source/evidence paths; acceptance remains independent.")
