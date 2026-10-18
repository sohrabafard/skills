#!/usr/bin/env python3
"""Structural instruction-contract regression checks, not live behavior proof.

Exit 0 clean, 1 findings, 2 unavailable input. --self-test rejects known regressions.
"""
from __future__ import annotations
from pathlib import Path
import re
import json
import sys

ROOT = Path(__file__).resolve().parent.parent

# Complete reviewed clauses, never isolated keyword scores. This is a finite
# source regression gate; arbitrary semantic equivalence still needs review.
EQUIVALENT_REQUIREMENTS = {
    "Retain required retrieval, focused implementer checks and independent acceptance gates":
        "Keep required source retrieval and focused implementer checks; independent acceptance gates remain mandatory",
    "Independent verification and review inspect the actual artifact":
        "Independent verification and review must inspect the changed artifact itself",
    "Plan-only work grants no product execution, branch, or commit authority":
        "Planning alone authorizes no product execution, branch creation or commit",
    "Explicitly supply BOTH model AND effort":
        "Supply an explicit model and an explicit reasoning effort for each dispatch",
}
BOUNDED_REQUIREMENTS = (
    "Evaluate the cheapest eligible supported available model AND effort pair for EVERY role",
    "explicit outcome", "finite named scope", "grounded local contracts/known invariants",
    "known pattern or causal path", "settled cross-boundary decisions", "bounded local discretion",
    "discriminating check", "Non-bug semantic work needs no reproduced failure",
    "Justify model and effort separately", "actual failed fit predicate or stronger task-specific evidence",
    "no quotas", "no mandatory trial ladder", "replay",
)


def contract_present(required: str, text: str) -> bool:
    normal = " ".join(text.split()).casefold()
    alternatives = (required, EQUIVALENT_REQUIREMENTS.get(required, required))
    return any(" ".join(clause.split()).casefold() in normal for clause in alternatives)


def agent_failures(text: str) -> list[str]:
    errors = []
    for required in ("CONFIGURED", "REQUESTED", "OBSERVED", "otherwise unknown",
                     "Never infer observed identity from a pin or request",
                     "Report metadata after the verdict/status or opening outcome",
                     "Effective authority:", "parent overrides", "tool/MCP grants",
                     "Task controls:", "model AND effort", "block this lane",
                     "model choice changes no authority"):
        if required not in text:
            errors.append(f"missing metadata/authority contract: {required}")
    if "Identity line: begin" in text:
        errors.append("identity-first contradicts verdict/outcome-first")
    if re.search(r"AGENT:.*\| MODEL:.*\| EFFORT:", text):
        errors.append("configured identity presented as runtime assertion")
    return errors


def orchestrator_failures(text: str) -> list[str]:
    errors = []
    for required in ("Activation grants no installation or update authority",
                     "Never silently substitute a model or a generic role",
                     "Do not implement product changes",
                     "alaa-workflow references/artifact-lifecycle.md",
                     "Plan-only work grants no product execution, branch, or commit authority",
                     "report saved plan/checkpoint paths when admitted",
                     "Commit only with explicit user authorization",
                     "local-only completion requires no merge prompt",
                     "Independent verification and review inspect the actual artifact",
                     "Do not infer a universal watchdog timeout"):
        if not contract_present(required, text):
            errors.append(f"missing authority contract: {required}")
    for forbidden in ("On activation, idempotently installs", "Auto-install authority",
                      "Commit on the run's own work branch at each completed subtask",
                      "continue with general-purpose subagents",
                      "Every profile runs all six phases",
                      "**Do not add verification instructions.**",
                      "A watchdog ends a lane on silence rather than on duration",
                      "Do not edit repository files, and do not create workflow artifacts",
                      "Do not edit files or imply implementation occurred",
                      "Advisor mode runs none of them: Phases A, B, and F"):
        if forbidden in text:
            errors.append(f"retired authority/fallback contract: {forbidden}")
    return errors


def dispatch_failures(text: str) -> list[str]:
    errors = []
    for required in ("<skills>", "exact names, sources, activation conditions, and absence actions",
                     "alaa-workflow references/companion-routing.md",
                     "<task_controls>", "explicit model AND effort",
                     "verified invocation surface and effective controls"):
        if required not in text:
            errors.append(f"missing dispatch skill bindings: {required}")
    if "<progress>report meaningful progress under the active host contract" not in text:
        errors.append("missing host-specific dispatch progress contract")
    if "Do not infer a universal watchdog timeout" not in text:
        errors.append("missing watchdog evidence boundary in dispatch")
    for retired in ("emit one line between steps", "a stream watchdog can kill it mid-run"):
        if retired in text:
            errors.append(f"retired dispatch progress claim: {retired}")
    return errors


def planning_failures(gates: str, implementation: str) -> list[str]:
    errors = []
    for required in ("resolved skill bindings under `alaa-workflow references/companion-routing.md`",
                     "executable phase/task skill bindings before implementation or write-lane dispatch"):
        if required not in gates:
            errors.append(f"missing plan/lane skill bindings: {required}")
    blocks = re.findall(r"```xml\s*\n(.*?)```", implementation, re.S)
    if not blocks:
        errors.append("missing implementation dispatch template")
    for index, block in enumerate(blocks, 1):
        if "<skills>" not in block or "resolved lane bindings" not in block:
            errors.append(f"implementation template {index}: missing resolved skill bindings")
        if "<clean_code_skill>" in block:
            errors.append(f"implementation template {index}: clean-code-only skill routing")
    return errors


IMPLEMENTER_REQUIREMENTS = (
    "Run only supplied",
    "focused commands: this lane's failure-mode tests",
    "this lane's failure-mode tests and lint/type/build scoped to touched files",
    "Judge actual command scope, never its tier label",
    "Never run affected/exhaustive checks",
    "full suite, race detector, end-to-end suite, or another lane's checks",
    "Independent gates own that breadth; duplicating it mixes authority and pays twice",
    "If dispatch conflicts, report the conflict and excluded commands",
    "run only known, separable focused commands",
    "Leave ambiguous or inseparable mixed commands unrun",
    "invent no substitutes or flags",
    "If none qualify, report validation not run and request focused commands from the parent",
    "Your results never discharge independent acceptance",
    "An explicitly assigned task owner may also run supplied bounded task-acceptance selectors at task end",
    "this grants no boundary affected/exhaustive authority",
    "whole-engagement cadence and exact phase/task/subtask cursor",
)
GATE_REQUIREMENTS = (
    "Before implementation or fix-cycle dispatch, classify actual command scope, never tier labels",
    "send focused commands to subtask workers and explicitly bounded task-acceptance commands to the task owner",
    "reserve affected/exhaustive commands for boundary gates",
    "Retain required retrieval, focused implementer checks and independent acceptance gates",
    "Role definitions own dispatch-conflict handling",
    "reconcile every excluded command and unrun check before accepting the lane",
    "reuse requires the correct observer as well as unchanged tree",
    "tool/dependency versions, environment/service state, and flags/seed/cwd",
    "Independent acceptance requires an observer independent of the implementation with authority for that gate",
    "An implementer's broad PASS cannot discharge it, even with unchanged inputs",
    "cite valid unchanged independent evidence instead of repeating it",
    "excludes exhaustive results from reuse",
    "Run any required exhaustive tier once, fresh on the final candidate after documentation",
)


def implementer_failures(text: str) -> list[str]:
    errors = [f"missing implementer verification boundary: {item}"
              for item in IMPLEMENTER_REQUIREMENTS if item not in text]
    # Contradictions must fail even when all required sentences remain present.
    for pattern in (r"Run the dispatched checks only", r"run (?:all|every) dispatched command",
                    r"run (?:the )?(?:affected|exhaustive) (?:tier|checks|suite)",
                    r"run ambiguous or inseparable", r"invent (?:replacement|substitute) commands"):
        if re.search(pattern, text, re.I):
            errors.append(f"contradictory implementer instruction: {pattern}")
    return errors


def implementation_template_failures(text: str) -> list[str]:
    errors = []
    blocks = [block for block in re.findall(r"```xml\s*\n(.*?)```", text, re.S)
              if re.search(r"<task>(?:Implement|Resolve reviewer/specialist findings)", block)]
    if not blocks:
        return ["missing implementation/fix-cycle dispatch template"]
    for index, block in enumerate(blocks, 1):
        prefix = f"implementation template {index}: "
        verification = re.search(r'<verification tier="focused">(.*?)</verification>', block, re.S)
        if not verification:
            errors.append(prefix + "missing focused verification block")
            continue
        commands = re.search(r"<commands>(.*?)</commands>", verification[1], re.S)
        excluded = re.search(r"<excluded>(.*?)</excluded>", verification[1], re.S)
        if not commands or not all(term in commands[1] for term in ("exact", "scoped")):
            errors.append(prefix + "missing exact scoped command contract")
        if not excluded or not all(term in excluded[1] for term in
                                   ("full suite", "race detector", "end-to-end suite", "other lane")):
            errors.append(prefix + "missing broad-check exclusions")
        acceptance = re.search(r"<task_acceptance>(.*?)</task_acceptance>", block, re.S)
        if not acceptance or not all(term in acceptance[1] for term in
                                     ("only for the explicitly assigned task owner", "exact bounded", "or not assigned")):
            errors.append(prefix + "missing bounded task-owner acceptance authority")
        if commands and re.search(r"affected|exhaustive|full suite|race detector|end-to-end|"
                                  r"-race\b|\./\.\.\.|--all\b", commands[1], re.I):
            errors.append(prefix + "overbroad command despite focused label")
    return errors


def economy_failures(skill: str, gates: str, routing: str | None = None) -> list[str]:
    errors = []
    for required in ("## Admission", "route a single bounded edit", "logical outcomes", "Coalesce compatible actions"):
        if required not in skill:
            errors.append(f"missing economical intake/pipeline contract: {required}")
    for required in ("observed host slots", "resource ceilings", "integration barriers", "only one CPU-heavy", "Phase transitions and new agents alone earn no rerun", "workflow-selected", "references/context-curation.md"):
        # Workspace selection is stated as current-checkout in the gates.
        if required == "workflow-selected":
            required = "current-checkout or isolation decision"
        if required not in gates:
            errors.append(f"missing economical execution contract: {required}")
    routing = routing if routing is not None else (ROOT / "references/routing-matrix.md").read_text(encoding="utf-8")
    for required in ("## Batch allocation", "tasks, dependencies and consolidation decisions are finalized", "balanced default", "priority is not an effort value", "Reopen allocation only for remaining work"):
        if required not in routing:
            errors.append(f"missing finalized-plan batch allocation contract: {required}")
    for forbidden in ("at most two workspace-writing", "Dispatch one `alaa-implementer` per routine lane", "refuse to start on a tree carrying changes this run did not make"):
        if forbidden in gates:
            errors.append(f"retired costly default: {forbidden}")
    return errors


def verification_failures(gates: str, templates: list[str], roles: dict[str, str]) -> list[str]:
    """Inspect integrated source contracts, never simulate model obedience."""
    errors = [f"missing gate authority boundary: {item}"
              for item in GATE_REQUIREMENTS if item not in gates]
    policy_name = "codex-model-policy.json"
    policy = json.loads((ROOT.parent / "alaa-prompting-guide" / "assets" / policy_name).read_text(encoding="utf-8"))
    suffix = ".toml"
    expected = {name + suffix for name in policy["profiles"] if name.startswith("alaa-implementer")}
    if set(roles) != expected:
        errors.append("expected all registered implementer variants")
    for name, text in roles.items():
        errors.extend(f"{name}: {item}" for item in implementer_failures(text))
        if name.endswith(".toml") and name != "alaa-implementer.toml":
            if "Run only supplied focused commands" not in text:
                errors.append(f"{name}: dispatched-only command source widened")
    for index, text in enumerate(templates, 1):
        errors.extend(f"template file {index}: {item}"
                      for item in implementation_template_failures(text))
    for pattern in (r"author(?:'s)? (?:broad )?PASS (?:satisfies|discharges)",
                    r"reuse implementer evidence for independent acceptance"):
        if re.search(pattern, gates, re.I):
            errors.append("author evidence substituted for independent acceptance")
    return errors


def task_allocation_failures(routing: str, controls: str) -> list[str]:
    errors = []
    for required in ("## All-role task allocation", "EVERY role", "balanced default",
                     "priority is not an effort value", "Role title, sensitivity, duration",
                     "second independent lens", "not model diversity", "model AND effort",
                     "compatibility identities", "exact verified available compatibility realization",
                     "block that affected lane", "Source changes do not reload"):
        if required not in routing:
            errors.append(f"missing all-role task allocation: {required}")
    for required in BOUNDED_REQUIREMENTS:
        if not contract_present(required, routing):
            errors.append(f"missing all-role bounded suitability: {required}")
    if "exclude gpt-6-sol ordinarily even if available" not in routing:
        errors.append("missing ordinary/historical Sol eligibility boundary")
    for required in ("Before every dispatch", "Explicitly supply BOTH model AND effort",
                     "effective configured pair matches", "or block", "affected lane",
                     "Source checks prove neither installed activation", "parent overrides"):
        if not contract_present(required, controls):
            errors.append(f"missing effective task controls: {required}")
    for forbidden in ("owns only role triggers", "Agent metadata carries executable pins",
                      "both standard and deep review inherit", "non-implementation roles remain fixed",
                      "stronger model solely because it is a second lens"):
        if forbidden in routing or forbidden in controls:
            errors.append(f"retired role-selected controls: {forbidden}")
    return errors


# Cadence assertions are source contracts, not a simulation of agent obedience.
# Workflow owns hierarchy validation; this consumer checks its scheduling seam.
CADENCE_REQUIREMENTS = (
    "Stages A-F name required orchestration outcomes and authority, not workflow phases",
    "New phased/delegated work uses the bound Beads phase-task-subtask hierarchy",
    "Existing unmarked/local families retain their original contract until explicit migration",
    "`Review boundary: phase|final`", "`Final phase`", "`Commit authority`",
    "`Review status`", "`Review evidence`",
    "Pass that whole-engagement contract, plan reference and exact phase/task/subtask cursor into every nested invocation",
    "Missing or inconsistent executing mappings block dependent dispatch",
    "Nested goals never reset the boundary or relabel intermediate output as final",
    "The implementer runs the smallest focused discriminating check",
    "The task owner runs bounded task-acceptance selectors across its subtasks",
    "Never dispatch independent subtask/task review or make a subtask/task commit",
    "intermediate phases retain `REVIEW_PENDING`",
    "tested issue closure advances readiness without claiming reviewed acceptance",
    "Under `phase`, only the declared phase end earns review",
    "Preserve stricter genuine repository gates and necessary focused feedback",
    "return the conflict to the plan owner rather than silently skipping either rule",
    "successful required review, accepted fixes and retests trigger the integration parent's Conventional Commit on the current branch",
    "Reuse a recorded standing user grant; do not invent another approval",
    "Without that grant, or after failed review/tests, preserve an identified uncommitted snapshot",
    "Worker roles never gain commit authority",
    "Stages C/D and final E gates wait for the inherited boundary",
    "The exhaustive tier belongs only to the whole engagement's final candidate after final documentation when required",
    "covered inputs, environment, flags and required observer match demonstrably",
    "Markdown and templates can be checker inputs: documentation-only change proves no equivalence",
    "never weaken tests or review to obtain a pass",
)


def cadence_failures(skill: str, gates: str, dispatch: str,
                     implementer: str, planner: str, verifier: str,
                     design: str, contract: str, critic: str) -> list[str]:
    errors = [f"missing scheduling contract: {clause}"
              for clause in CADENCE_REQUIREMENTS if not contract_present(clause, gates)]
    errors.extend(specialist_cadence_failures(design, contract, critic))
    for clause in ("It must not implement while viable implementers are available",
                   "Correct sparingly", "Calibrate length", "Keep dispatches lean",
                   "Do not restate the native role definition",
                   "for gate economics and independent acceptance",
                   "hard user constraint on browser choice", "--browser chromium"):
        if not contract_present(clause, skill):
            errors.append(f"missing mirrored body contract: {clause}")
    if "Remove repetition only without new changes" in skill:
        errors.append("gate economics duplicated outside its owner")
    for clause in ("<cadence>", "whole-engagement plan", "current phase/task/subtask",
                   "pending review/commit", "Delegated lanes"):
        if clause not in dispatch:
            errors.append(f"missing inherited dispatch cadence: {clause}")
    for label, text, clauses in (
        ("implementer", implementer, (
            "An explicitly assigned task owner may also run supplied bounded task-acceptance selectors at task end",
            "this grants no boundary affected/exhaustive authority",
            "whole-engagement cadence and exact phase/task/subtask cursor",
            "pending boundary review/commit rather than starting your own review or commit")),
        ("planner", planner, ("phase-task-subtask hierarchy", "existing-family compatibility",
                              "inherited review boundary, final phase, commit authority and exact cursor")),
        ("verifier dispatch", verifier, ("<review_boundary>", "whole-engagement final candidate identity",
                                        "no subtask/task independent acceptance")),
    ):
        for clause in clauses:
            if not contract_present(clause, text):
                errors.append(f"missing {label} cadence: {clause}")
    forbidden = (
        r"(?:independent )?review (?:every|each) (?:subtask|task)\b",
        r"commit (?:at|after) (?:every|each) (?:subtask|task)\b",
        r"(?:nested|child) (?:run|invocation) resets? (?:the )?review boundary",
        r"documentation-only changes? (?:always )?(?:preserve|prove) (?:test |input )?equivalence",
        r"commit on the work branch before expensive verification",
        r"(?:weaken|skip) (?:failed tests|assertions|review) to (?:obtain|force) a pass",
    )
    for pattern in forbidden:
        if re.search(pattern, gates, re.I):
            errors.append(f"contradictory scheduling instruction: {pattern}")
    return errors



# Topic: specialist review cadence; layer: structural source contract.
# The gate owner already schedules review; these consumers must not reintroduce
# early judgment or narrow a nested final candidate to its current phase.
def specialist_cadence_failures(design: str, contract: str, critic: str) -> list[str]:
    errors = []
    shared = (
        "references/verification-and-gates.md",
        "inherited", "declared phase|final boundary",
        "complete phase candidate for phase",
        "whole-engagement candidate including pending earlier phases for final",
        "Nested invocations never reset that scope",
        "Return missing, conflicting or premature cadence to the parent without judgment",
    )
    for label, text in (("design template", design), ("contract template", contract),
                        ("architecture critic", critic)):
        for clause in shared:
            if not contract_present(clause, text):
                errors.append(f"{label}: missing specialist cadence: {clause}")
        for obsolete in (
            "Pressure-test this proposed architecture before implementation",
            "Dispatch in Stage A before code exists",
            "Spawn before implementation",
            "before expensive implementation begins",
            "Questions that must be answered before implementation",
        ):
            if contract_present(obsolete, text):
                errors.append(f"{label}: premature specialist judgment: {obsolete}")
    for label, text, clauses in (
        ("design template", design, ("pre-implementation design record", "report the missing record")),
        ("contract template", contract, (
            "Record known triggers and decide consumer impact, compatibility and deprecation in Stage A",
            "a newly discovered trigger reopens the affected plan and gate")),
        ("architecture critic", critic, ("The design record remains due before implementation",
                                         "Unresolved questions and conditions that block acceptance")),
    ):
        for clause in clauses:
            if not contract_present(clause, text):
                errors.append(f"{label}: missing planning/acceptance contract: {clause}")
    return errors


def specialist_cadence_sources() -> tuple[str, str, str]:
    suffix = ".toml"
    return tuple((ROOT / path).read_text(encoding="utf-8") for path in (
        "references/delegation-prompts/20-design.md",
        "references/delegation-prompts/60-contract-review.md",
        "agents/alaa-architecture-critic" + suffix))


def specialist_cadence_self_tests() -> list[tuple[str, bool]]:
    """Immutable source setup; each mutation is isolated and checks its own diagnostic."""
    sources = specialist_cadence_sources()
    cases = [("specialist inherited phase/final cadence accepted",
              not specialist_cadence_failures(*sources))]
    for index, label in enumerate(("design template", "contract template", "architecture critic")):
        for clause in (
            "references/verification-and-gates.md", "declared phase|final boundary",
            "complete phase candidate for phase",
            "whole-engagement candidate including pending earlier phases for final",
            "Nested invocations never reset that scope",
            "Return missing, conflicting or premature cadence to the parent without judgment",
        ):
            broken = list(sources)
            broken[index] = broken[index].replace(clause, "omitted")
            diagnostic = f"{label}: missing specialist cadence: {clause}"
            cases.append((f"{label}: requires {clause}",
                          diagnostic in specialist_cadence_failures(*broken)))
        # Contradictions must fail even with every valid clause still present.
        for obsolete in ("Dispatch in Stage A before code exists", "Spawn before implementation",
                         "before expensive implementation begins"):
            broken = list(sources)
            broken[index] += "\n" + obsolete
            cases.append((f"{label}: rejects early judgment {obsolete}",
                          f"{label}: premature specialist judgment: {obsolete}"
                          in specialist_cadence_failures(*broken)))
    for index, label, clause in (
        (0, "design template", "pre-implementation design record"),
        (0, "design template", "report the missing record"),
        (1, "contract template", "Record known triggers and decide consumer impact, compatibility and deprecation in Stage A"),
        (1, "contract template", "a newly discovered trigger reopens the affected plan and gate"),
        (2, "architecture critic", "The design record remains due before implementation"),
        (2, "architecture critic", "Unresolved questions and conditions that block acceptance"),
    ):
        broken = list(sources)
        broken[index] = broken[index].replace(clause, "omitted")
        cases.append((f"{label}: preserves {clause}",
                      f"{label}: missing planning/acceptance contract: {clause}"
                      in specialist_cadence_failures(*broken)))
    return cases


def cadence_sources() -> tuple[str, ...]:
    return tuple((ROOT / path).read_text(encoding="utf-8") for path in (
        "SKILL.md", "references/verification-and-gates.md", "references/delegation-prompts.md",
        "assets/implementation-contract.md", "assets/planner-contract.md",
        "references/delegation-prompts/40-verification.md")) + specialist_cadence_sources()


def cadence_self_tests() -> list[tuple[str, bool]]:
    sources = cadence_sources()
    cases = [("inherited phase/final cadence accepted", not cadence_failures(*sources))]
    for clause in CADENCE_REQUIREMENTS:
        broken = list(sources)
        broken[1] = broken[1].replace(clause, "omitted")
        cases.append((f"cadence requires {clause}", bool(cadence_failures(*broken))))
    for index, clause in ((0, "Correct sparingly"), (0, "hard user constraint on browser choice"),
                          (2, "<cadence>"), (2, "Delegated lanes"),
                          (3, "this grants no boundary affected/exhaustive authority"),
                          (4, "existing-family compatibility"), (5, "<review_boundary>")):
        broken = list(sources)
        broken[index] = broken[index].replace(clause, "omitted")
        cases.append((f"cadence seam requires {index}:{clause}", bool(cadence_failures(*broken))))
    for contradiction in (
        "Review every task independently", "independent review each subtask",
        "Commit after each task", "commit at every subtask",
        "Child invocation resets the review boundary",
        "Documentation-only changes prove input equivalence",
        "Commit on the work branch before expensive verification",
        "Weaken failed tests to obtain a pass",
    ):
        broken = list(sources)
        broken[1] += "\n" + contradiction
        cases.append((f"cadence contradiction rejected: {contradiction}", bool(cadence_failures(*broken))))
    return cases


def verification_sources() -> tuple[str, list[str], dict[str, str]]:
    return (
        (ROOT / "references/verification-and-gates.md").read_text(encoding="utf-8"),
        [(ROOT / path).read_text(encoding="utf-8") for path in (
            "references/delegation-prompts/30-implementation.md",
            "references/delegation-prompts/90-completion/20-review-followup.md")],
        {path.name: path.read_text(encoding="utf-8")
         for path in sorted((ROOT / "agents").glob("alaa-implementer*"))
         if path.suffix in {".toml", ".md"}},
    )


def self_test() -> int:
    good = (ROOT / "agents" / next(iter(sorted(
        path.name for path in (ROOT / "agents").glob("alaa-instruction-reviewer.*"))))).read_text(encoding="utf-8")
    # A source definition contains the same contract whether represented as a
    # multiline body or a serialized scalar; these checks do not execute it.
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for original, equivalent in EQUIVALENT_REQUIREMENTS.items():
        source = next(text for text in (skill,
            (ROOT / "references/model-effort-policy.md").read_text(encoding="utf-8"),
            (ROOT / "references/verification-and-gates.md").read_text(encoding="utf-8")) if original in text)
        assert contract_present(original, source.replace(original, equivalent)), original
        assert not contract_present(original, equivalent.replace("mandatory", "optional").replace("must inspect", "may inspect").replace("authorizes no", "authorizes").replace("explicit reasoning effort", "inherited effort")), original
    dispatch = (ROOT / "references/delegation-prompts.md").read_text(encoding="utf-8")
    gates = (ROOT / "references/verification-and-gates.md").read_text(encoding="utf-8")
    implementation = (ROOT / "references/delegation-prompts/30-implementation.md").read_text(encoding="utf-8")
    cases = [
        ("valid identity and authority", not agent_failures(good)),
        ("host-specific dispatch progress", not dispatch_failures(dispatch)),
        ("dispatch missing progress rejected", bool(dispatch_failures(dispatch.replace("<progress>report meaningful progress under the active host contract", "<progress>silent")))),
        ("per-command narration rejected", bool(dispatch_failures(dispatch + "\nemit one line between steps"))),
        ("dispatch watchdog claim rejected", bool(dispatch_failures(dispatch + "\na stream watchdog can kill it mid-run"))),
        ("unknown observation required", bool(agent_failures(good.replace("otherwise unknown", "use the pin")))),
        ("identity assertion rejected", bool(agent_failures(good + "\nAGENT: fixture | MODEL: configured | EFFORT: high"))),
        ("verdict first", bool(agent_failures(good + "\nIdentity line: begin the report"))),
        ("effective permissions required", bool(agent_failures(good.replace("parent overrides", "declaration")))),
        ("advisory and authority accepted", not orchestrator_failures(skill)),
        ("plan-only execution boundary required", bool(orchestrator_failures(skill.replace("Plan-only work grants no product execution, branch, or commit authority", "Plan means execute")))),
        ("workflow admission owner required", bool(orchestrator_failures(skill.replace("alaa-workflow references/artifact-lifecycle.md", "Unowned admission")))),
        ("saved-plan report required", bool(orchestrator_failures(skill.replace("report saved plan/checkpoint paths when admitted", "Plans are chat-only")))),
        ("blanket advisor no-files rejected", bool(orchestrator_failures(skill + "\nDo not edit repository files, and do not create workflow artifacts"))),
        ("advisor output no-files rejected", bool(orchestrator_failures(skill + "\nDo not edit files or imply implementation occurred"))),
        ("blanket phase-write rationale rejected", bool(orchestrator_failures(skill + "\nAdvisor mode runs none of them: Phases A, B, and F"))),
        ("complete lane bindings accepted", not planning_failures(gates, implementation)),
        ("lane bindings omitted rejected", bool(planning_failures(gates.replace("resolved skill bindings under `alaa-workflow references/companion-routing.md`", "clean code only"), implementation))),
        ("phase bindings omitted rejected", bool(planning_failures(gates.replace("executable phase/task skill bindings before implementation or write-lane dispatch", "implicit skills"), implementation))),
        ("implementation bindings omitted rejected", bool(planning_failures(gates, implementation.replace("<skills>", "<omitted>", 1)))),
        ("clean-code-only implementation rejected", bool(planning_failures(gates, implementation.replace("<skills>", "<clean_code_skill>", 1)))),
        ("dispatch bindings omitted rejected", bool(dispatch_failures(dispatch.replace("<skills>", "<omitted>")))),
        ("dispatch binding owner omitted rejected", bool(dispatch_failures(dispatch.replace("alaa-workflow references/companion-routing.md", "implicit owner")))),
        ("activation install rejected", bool(orchestrator_failures(skill + "\nOn activation, idempotently installs"))),
        ("implicit commit rejected", bool(orchestrator_failures(skill + "\nCommit on the run's own work branch at each completed subtask"))),
        ("forced integration rejected", bool(orchestrator_failures(skill + "\nEvery profile runs all six phases"))),
        ("independent review preserved", bool(orchestrator_failures(skill.replace("Independent verification and review inspect the actual artifact", "Check summaries")))),
        ("silent fallback rejected", bool(orchestrator_failures(skill + "\ncontinue with general-purpose subagents"))),
        ("gate owner pointer preserved", bool(cadence_failures(skill.replace("for gate economics and independent acceptance", "for optional checks"), *cadence_sources()[1:]))),
        ("blanket no-verification rejected", bool(orchestrator_failures(skill + "\n**Do not add verification instructions.**"))),
        ("invented watchdog rejected", bool(orchestrator_failures(skill + "\nA watchdog ends a lane on silence rather than on duration"))),
    ]
    cases.extend(cadence_self_tests())
    cases.extend(specialist_cadence_self_tests())
    cases.append(("economical execution accepted", not economy_failures(skill, gates)))
    for required in ("observed host slots", "resource ceilings", "integration barriers", "only one CPU-heavy", "Phase transitions and new agents alone earn no rerun", "current-checkout or isolation decision", "references/context-curation.md"):
        cases.append((f"economics {required} required", bool(economy_failures(skill, gates.replace(required, "omitted")))))
    for forbidden in ("at most two workspace-writing", "Dispatch one `alaa-implementer` per routine lane", "refuse to start on a tree carrying changes this run did not make"):
        cases.append((f"costly default {forbidden} rejected", bool(economy_failures(skill, gates + "\n" + forbidden))))
    routing = (ROOT / "references/routing-matrix.md").read_text(encoding="utf-8")
    for required in ("## Batch allocation", "tasks, dependencies and consolidation decisions are finalized", "balanced default", "priority is not an effort value", "Reopen allocation only for remaining work"):
        cases.append((f"batch allocation {required} required", bool(economy_failures(skill, gates, routing.replace(required, "omitted")))))
    controls = (ROOT / "references/model-effort-policy.md").read_text(encoding="utf-8")
    cases.append(("all-role allocation/effective controls", not task_allocation_failures(routing, controls)))
    for requirement in BOUNDED_REQUIREMENTS:
        cases.append((f"bounded suitability requires {requirement}", bool(task_allocation_failures(routing.replace(requirement, "omitted"), controls))))
    for required in ("EVERY role", "model AND effort", "second independent lens",
                     "compatibility identities", "block that affected lane"):
        cases.append((f"task allocation requires {required}", bool(task_allocation_failures(
            routing.replace(required, "omitted"), controls))))
    for required in ("Explicitly supply BOTH model AND effort", "effective configured pair matches",
                     "parent overrides", "Source checks prove neither installed activation"):
        cases.append((f"effective controls require {required}", bool(task_allocation_failures(
            routing, controls.replace(required, "omitted")))))
    for path in sorted((ROOT / "agents").glob("alaa-*")):
        if path.suffix not in {".toml", ".md"}:
            continue
        text = path.read_text(encoding="utf-8")
        cases.append((f"{path.name}: explicit task controls", not agent_failures(text)))
        for requirement in ("Task controls:", "model AND effort", "block this lane"):
            cases.append((f"{path.name}: reject missing {requirement}",
                          bool(agent_failures(text.replace(requirement, "omitted")))))
    policy, templates, roles = verification_sources()
    cases.append(("integrated verification authority accepted",
                  not verification_failures(policy, templates, roles)))
    for name, role in roles.items():
        for requirement in IMPLEMENTER_REQUIREMENTS:
            broken = {**roles, name: role.replace(requirement, "omitted", 1)}
            cases.append((f"{name}: {requirement} required",
                          bool(verification_failures(policy, templates, broken))))
        for contradiction in ("run all dispatched commands", "run affected checks",
                              "run ambiguous or inseparable commands",
                              "invent substitute commands"):
            broken = {**roles, name: role + "\n" + contradiction}
            cases.append((f"{name}: contradiction {contradiction} rejected",
                          bool(verification_failures(policy, templates, broken))))
    cases.append(("missing implementer variant rejected", bool(verification_failures(
        policy, templates, dict(list(roles.items())[:1])))))
    for requirement in GATE_REQUIREMENTS:
        cases.append((f"gate boundary {requirement} required", bool(verification_failures(
            policy.replace(requirement, "omitted", 1), templates, roles))))
    for contradiction in ("author broad PASS discharges independent acceptance",
                          "reuse implementer evidence for independent acceptance"):
        cases.append(("authority laundering rejected: " + contradiction,
                      bool(verification_failures(policy + "\n" + contradiction, templates, roles))))
    for file_index, template in enumerate(templates):
        # Mutate each block independently, including escalation and fix-cycle paths.
        for block_index, block in enumerate(re.findall(r"```xml\s*\n(.*?)```", template, re.S)):
            if not re.search(r"<task>(?:Implement|Resolve reviewer/specialist findings)", block):
                continue
            for label, mutated in (
                ("focused boundary omitted", block.replace(' tier="focused"', '', 1)),
                ("exclusions omitted", re.sub(r"<excluded>.*?</excluded>", '', block, flags=re.S)),
                ("scope omitted", block.replace("scoped", "unbounded", 1)),
                ("task owner acceptance omitted", block.replace("<task_acceptance>", "<omitted>", 1)),
                ("task acceptance unbounded", block.replace("exact bounded", "unbounded", 1)),
                ("affected breadth appended", block.replace('</commands>', '; affected-tier checks</commands>', 1)),
                ("race mislabeled focused", block.replace('</commands>', '; go test -race ./...</commands>', 1)),
                ("full suite mislabeled focused", block.replace('</commands>', '; full suite</commands>', 1)),
            ):
                changed = list(templates)
                changed[file_index] = template.replace(block, mutated, 1)
                cases.append((f"template {file_index + 1}/{block_index + 1}: {label}",
                              bool(verification_failures(policy, changed, roles))))
    for label, passed in cases:
        if not passed:
            print(f"SELF-TEST FAILED: {label}", file=sys.stderr)
    if not all(passed for _, passed in cases):
        return 1
    print(f"CONTRACT SELF-TEST OK: {len(cases)} positive/negative structural fixtures")
    return 0


def main() -> int:
    try:
        if sys.argv[1:] == ["--self-test"]:
            return self_test()
        if sys.argv[1:]:
            print("usage: check_agent_contracts.py [--self-test]", file=sys.stderr)
            return 2
        errors = orchestrator_failures((ROOT / "SKILL.md").read_text(encoding="utf-8"))
        errors.extend(dispatch_failures((ROOT / "references/delegation-prompts.md").read_text(encoding="utf-8")))
        errors.extend(planning_failures(
            (ROOT / "references/verification-and-gates.md").read_text(encoding="utf-8"),
            (ROOT / "references/delegation-prompts/30-implementation.md").read_text(encoding="utf-8")))
        errors.extend(verification_failures(*verification_sources()))
        errors.extend(cadence_failures(*cadence_sources()))
        errors.extend(task_allocation_failures(
            (ROOT / "references/routing-matrix.md").read_text(encoding="utf-8"),
            (ROOT / "references/model-effort-policy.md").read_text(encoding="utf-8")))
        errors.extend(economy_failures((ROOT / "SKILL.md").read_text(encoding="utf-8"),
            (ROOT / "references/verification-and-gates.md").read_text(encoding="utf-8")))
        for path in sorted((ROOT / "agents").glob("alaa-*")):
            if path.suffix in {".toml", ".md"}:
                errors.extend(f"{path.name}: {item}" for item in agent_failures(path.read_text(encoding="utf-8")))
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
        print("CONTRACT CHECK OK: metadata, dispatch scope and independent verification authority")
        return 0
    except AssertionError as exc:
        print(f"contract self-test failed: {exc}", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, StopIteration) as exc:
        print(f"contract check unavailable: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
