# Skill composition and model-routing review

Date: 2026-11-03. Source: `1bff3b51458db30e6fbd81c70016109ea2ad5bd5..7ac6bb7f709a4601b7fc2505ca139f8e634b5eea`.

## Outcome

The source change composes prompts through reachable canonical skill owners and adds a bounded Codex Terra candidate. Existing task-selected controls, neutral role authority, review cadence, and external-effect limits remain in force. No skill installation, runtime activation, live Terra dispatch, benchmark, comparative trial, or rollout occurred.

## Proposal dispositions

| Proposal | Disposition | Shipped result and rationale |
|---|---|---|
| 1. Compose instructions from skills | ADAPT | The prompting guide now requires resolving registered name, surface syntax, recipient-readable source, companion load conditions, and decisions. Missing required sources use an already authorized equivalent preserving the obligation or block. See [composition rules](../../skills/sohrab/alaa-prompting-guide/references/06-invocation-and-composition.md). |
| 2. Evaluate instruction changes | ADAPT | The authoring guide adds proportional source scenarios and distinguishes static checks, source walkthroughs, and observed runs. It does not treat walkthroughs as execution. See [authoring evidence](../../skills/sohrab/alaa-prompting-guide/references/60-skill-authoring.md). |
| 3. Compare instruction variants | ADOPT | An optional protocol specifies matched conditions, representative and held-out cases, first-pass versus repaired outcomes, and evidence. It creates no mandatory run or dispatch gate; no comparison was run. |
| 4. Add general Python/Rust skill coverage | DEFER | The review found no recurring demonstrated gap for a new language skill. Python CLI/tooling is already used; no tracked Rust/Cargo need was established, and Vector/VRL remains a separate domain. |
| 5. Add skill-composition presets | ALREADY COVERED; DEFER presets | Exact task/phase skill bindings and model-neutral role templates already exist in the workflow and orchestrator contracts. This change clarifies composition at the canonical prompting owner without duplicating those mechanisms. |
| 6. Consider GPT-6.1 Terra | ADAPT | Terra is selectable only for supplied-material writing, defined-outcome computer use, and scoped fixes when all bounded-suitability predicates and an exact verified host pair hold. The runtime orchestrator still chooses; broader work does not qualify. See [routing policy](../../skills/sohrab/alaa-codex-orchestrator/references/routing-matrix.md) and [Terra controls](../../skills/sohrab/alaa-prompting-guide/references/12-gpt-6.md). |

## Source and review evidence

The composition changes landed in `1417b436`; Terra policy and host evidence in `fc705fe5`; the authorized-equivalent checklist clarification in `7ac6bb7f`. The review inspected nine source changes and expected source walkthrough cases. Both independent reviews returned **APPROVED-WITH-NITS**; both nits were fixed. The review details are in [review.md](./review.md).

Focused static evidence passed: diff whitespace check, model-policy/neutral-role checker, Python AST parse, and the follow-up whitespace check for `7ac6bb7f`. Earlier invocation failures remain recorded as historical attempts; after explicit user authorization, the final model-policy check passed. See [focused results](verification/focused.json) and [review-fix results](verification/review-fix.json). Static results and source walkthroughs do not prove agent behavior.

## Limits and unchanged documents

All ten final native gates passed on the frozen source candidate `312f28c1379f0baa412b4c7d49870373d5b737cb`; the evidence records matching initial/final tree snapshots and command logs in [final gate results](verification/final-gates.json). These gates are static proof for the nine source files. This report-only evidence update is outside that source verdict and has its own documentation checks.

The four lifecycle states are independent: **IMPLEMENTED: proven**; **MERGE_CANDIDATE: proven**; **RELEASE_CANDIDATE: not requested**; **PUBLISHED: not requested**. The canonical workflow plan is `beads:alaa-mehm`.

Final curation admitted no candidates. Reusable knowledge already belongs in canonical skills; runtime recovery uses its existing owner. No memory was written or published. Hindsight recall was unavailable. No pipeline reopening was required.

No live activation, Terra run, fixture test, benchmark, comparative trial, or rollout was observed. Runtime compliance, comparative quality, and installation remain unverified.

No Python/Rust general-purpose skill or new composition preset was added: evidence did not establish a recurring gap, and existing exact bindings and neutral templates already cover the mechanism. Shared Claude behavior and role authority were preserved; Terra eligibility is Codex-specific.
