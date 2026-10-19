# Workflow plan-kind acceptance

Source: the current user goal, captured in the linked design and execution plan. This map links requirements to final evidence; Beads retains task state.

| Requirement | Final evidence |
|---|---|
| Design is local, hierarchy-free, with owned dated decisions/questions, handoff/checkpoint and approval | Kind-specific templates and documentation; regression cases; temporary design sample validation |
| Execution requires linked approved design, Beads hierarchy and skill mappings | Admission and hierarchy regressions; temporary execution sample; owner references |
| Long-run and parallel execution contract | Scoped lane ownership, real dependency/readiness semantics, shared handoff/checkpoint owners |
| Explicit initializer kind and kind-specific templates | CLI positive/negative tests, collision/no-write and dry-run tests |
| Design never needs execution phases/snapshots/reviews | Complete design sample and regression assertions |
| Installed skill sources resolve and remain verified | Tilde/native Windows positive tests; missing/unreadable/name-mismatch negatives |
| Single owner per normative rule | Final instruction review; lifecycle/tracking/continuity owner matrix |
| Existing contracts preserved | Existing unmarked-family regression coverage and root native gates |

Final commands: `python -B skills/sohrab/alaa-workflow/tests/test_workflow_files.py`; initializer/validator self-tests only if exposed by their CLI; sample init/validate commands in a temporary directory; `python -B scripts/validate_sohrab_skill_pack.py`; `python -B scripts/check_skill_index.py`; `python -B scripts/check_fleet_references.py`; `python -B scripts/check_lifecycle_contract.py`; `git diff --check`.

Test missing/duplicate/unsupported header kinds, malformed approval dates/attribution, missing/wrong/unapproved design links, design execution-field leakage, deterministic paths, unchanged legacy verdicts and no partial output on rejected initialization. Body examples must not select a plan kind. A static gate proves recorded metadata, not authentic user approval, live issue readiness, installed activation or agent compliance.

Run bounded native checks at normal priority, one test process at a time. No command is declared CPU-heavy; no parallel test workers. Only final gates may run the complete suite. Preserve logs and report exact exits. No commit, push, installation, remote synchronization or legacy assignee migration.
