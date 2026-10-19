from pathlib import Path

addition = '''
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
    suffix = ".toml" if ROOT.name == "alaa-codex-orchestrator" else ".md"
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
            broken[index] += "\\n" + obsolete
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

'''

for name in ('alaa-codex-orchestrator', 'alaa-cc-orchestrator'):
    path = Path('skills/sohrab') / name / 'scripts/check_agent_contracts.py'
    text = path.read_text(encoding='utf-8')
    anchor = '\ndef cadence_sources() -> tuple[str, str, str, str, str, str]:'
    assert anchor in text
    text = text.replace(anchor, '\n' + addition + '\ndef cadence_sources() -> tuple[str, ...]:', 1)
    text = text.replace('implementer: str, planner: str, verifier: str) -> list[str]:',
                        'implementer: str, planner: str, verifier: str,\n                     design: str, contract: str, critic: str) -> list[str]:', 1)
    anchor = '    errors = [f"missing scheduling contract: {clause}"\n              for clause in CADENCE_REQUIREMENTS if not contract_present(clause, gates)]'
    assert anchor in text
    text = text.replace(anchor, anchor + '\n    errors.extend(specialist_cadence_failures(design, contract, critic))', 1)
    anchor = '        "references/delegation-prompts/40-verification.md"))'
    assert anchor in text
    text = text.replace(anchor, '        "references/delegation-prompts/40-verification.md")) + specialist_cadence_sources()', 1)
    text = text.replace('    cases.extend(cadence_self_tests())', '    cases.extend(cadence_self_tests())\n    cases.extend(specialist_cadence_self_tests())', 1)
    path.write_text(text, encoding='utf-8', newline='\n')
print('Mirrored focused specialist-cadence assertions and regression cases added; no CLI change')
