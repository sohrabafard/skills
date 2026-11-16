# Lane LB ledger — orchestrator pair, version 7.1.0

Scope: `skills/sohrab/alaa-cc-orchestrator` (cc) and `skills/sohrab/alaa-codex-orchestrator` (codex).
A row applies to both packs unless its first column names one. "W2.1" means Workstream 2 item 1 of
`plan.md`. Paths are relative to each pack.

## Rules changed, added or removed

| File | Old rule | New rule | Plan item | Checker clause |
|---|---|---|---|---|
| `references/routing-matrix.md` step 3 heading | "Select the cheapest suitable pair" | "Select the pair that fits": a pair is neither stronger nor weaker than the lane needs | W2.1 | none bound the heading |
| `references/routing-matrix.md` step 3 | "Evaluate the cheapest eligible supported available model AND effort pair for EVERY role, the rule-writer included" | Record two facts for each lane, then "read the model AND effort pair for EVERY role from the fit table, the rule-writer included" | W2.1 | `BOUNDED_REQUIREMENTS`: literal reworded |
| `references/routing-matrix.md` step 3 | new | The two facts: judgment left to the lane selects the model; search and length selects the effort | W2.1 | none |
| `references/routing-matrix.md` step 3 | new | Fit table: five judgment rows and one exceptional-model row, four effort columns, and the supporting row of `90-model-selection.md` for each row | W2.1 | none |
| `references/routing-matrix.md` step 3 | "Select the least costly suitable available pair. Depart from it only on an explicit user choice or recorded task evidence" | removed; the fit table selects, and a departure in either direction records its predicate or evidence | W2.1, W2.2 | not bound |
| `references/routing-matrix.md` step 3 | new | Effort within a model: start at *Ordinary*, one column right for a long, strict or unverifiable lane, one column left for a short, fully specified lane or one of many similar short lanes; a cheap check over an enumerated scope keeps *Ordinary*; the top levels need a recorded measured gain | W2.3 | none |
| `references/routing-matrix.md` step 3 | new | Effort support: where each effort cell comes from, and which cells are local policy | W2.1 | none |
| `references/routing-matrix.md` step 3 | new | *Reclassify* cell: two facts contradict each other; correct the judgment fact | W2.2 | none |
| `references/routing-matrix.md` step 4 (old) | "Admit an exceptional model only on evidence", a separate step with three evidence arms | The same three arms and both guard sentences, as the last table row and one bullet under the table | W2.4 | not bound |
| `references/routing-matrix.md` step 2 | The title, sensitivity, duration, whole-goal and second-lens sentence, and "Independence comes from context and authority, not model diversity" | Both sentences unchanged, moved into the *Too strong* defect | W2.2 | `task_allocation_failures` raw literals kept |
| `references/routing-matrix.md` step 3 | new | *Too strong* defect: a model from a later row, or `high` effort or above, on a settled lane with a discriminating check, with its cost | W2.2 | none |
| `references/routing-matrix.md` step 3 | new | *Too weak* defect: a model of the first two rows on coupled decisions; `low` or default effort on a long unverifiable lane; a cheap pair while a fit predicate fails; cost, volume and file count never select a weaker pair | W2.2 | none |
| `references/routing-matrix.md` step 3 | "Justify model and effort separately, each from the remaining reasoning need, the priority, current official guidance and applicable prior evidence" | "Justify model and effort separately: the model from the judgment fact, the effort from the search and length fact" | W2.1 | `BOUNDED_REQUIREMENTS` literal kept |
| `references/routing-matrix.md` step 3 | "When you reject a cheaper pair, record the actual failed fit predicate or stronger task-specific evidence" | "When you depart from the table cell in either direction, record the actual failed fit predicate or stronger task-specific evidence" | W2.2 | `BOUNDED_REQUIREMENTS` literal kept |
| `references/routing-matrix.md` step 4 (new) | new | Feedback at a reassessment point of Batch allocation or Reassignment, for remaining work only: raise effort for a search shortfall, raise the model for a judgment shortfall, lower one step after a trivial finish; completed work stays | W2.5 | none |
| `references/routing-matrix.md` step 5 | Record role, scope and workload class, departing priority, pair, admission and evidence | One line for each lane: role, pair, and the fit-table row and column; plus the reason for a departure and the evidence for an exceptional model | W2.6 | none |
| `references/routing-matrix.md` *Implementation routing* | "These routes classify workload fit only. Apply All-role task allocation separately" | A route selects the role identity only, from the two fit facts; the fit table selects the pair; each route names its fit row | W2 alignment | cc positional clause of the bounded branch kept |
| `references/routing-matrix.md` *Stack-bound roles* | "Record the lane's workload class in the allocation record: ..." | "For a stack-bound lane the two fit facts select the task pair and no role identity"; the generic fallback role is the one the routes name for the two fit facts | W2.6 | none |
| `references/model-effort-policy.md` (codex) | no statement of inheritance | Supply both controls on every spawn: an unset subagent model or effort inherits the parent agent's value (Codex subagents page, read 2026-11-17) | W2, dispatch fact | `DEFAULT_REQUIREMENTS` untouched |
| `references/model-effort-policy.md` (cc) *Native Advisor consultation* | Consider Advisor after pair selection; "Consultation stays optional" | Two consultation points when the session has an advisor: before plan ratification and before the final report; other points as before; no pair, authority or gate changes; the run never depends on it | W3.4 | none |
| `references/delegation-prompts.md` (cc) | new | A dispatch states no advisor text; pointer to `41` *Prompts for a session that may have an advisor* for another surface | W3.4 | none |
| `references/delegation-prompts.md` `<task_controls>` field | "actual task scope/complexity" | "the two fit facts and the fit-table row and column" | W2.6 | `dispatch_failures` literals kept |
| `references/delegation-prompts.md` `<task_controls>` rule | "Correct a missing or different parameter before you send." | Adds the reason: a lane inherits the lead's own value for an omitted control, the most common cause of a pair that is too strong | W2, dispatch fact | none |
| `references/delegation-prompts.md` `<beads_identity>` rule | Resolve through the workflow owner; read-only gates use `none` | Adds: a write lane gets its own actor and `claim`, claims, reads back, appends the checkpoint before it returns or stops, never closes; the lead closes after it reconciles the diff and keeps one `Lane:` line for each live leaf | W1.3 | `dispatch_failures` literals kept |
| `references/delegation-prompts/30-implementation.md` | no `<beads_identity>` guidance | Fill `<beads_identity>` with the lane's own actor and `claim`, under the envelope rule | W1.3 | none |
| `references/delegation-prompts/30-implementation.md`, `90-completion/20-review-followup.md` | `<role_selection>` names "selection reason"; workhorse routes record "the workload class" | "fit-table row and column"; "the two fit facts" | W2.6 | none |
| `references/verification-and-gates.md` cadence | Plan fields read as if a phase always exists | A native plan may have no phase milestone: `Final phase` names the root, and the root is the one phase for the phase rules of the file | W1.1 | `CADENCE_REQUIREMENTS` kept |
| `SKILL.md` *Dispatch discipline* | "Every dispatch carries `/alaa-low-noise`" | Name `/alaa-low-noise` only for a discovery-heavy or log-heavy lane, because every definition carries the output rule | W4.2 | none |
| `SKILL.md` step 5 | "record each role and its selection reason in the plan" | "record each role with its pair and the fit-table row and column that selected it" | W2.6 | none |
| `SKILL.md` (cc) advisor pointer | "consultation during execution" | "consultation, including the lead's two consultation points" | W3.4 | none |
| `assets/implementation-contract.md` and every implementer definition | Return sentence at the end: findings, no transcript, bulky output to the artifact directory, about 40 lines | `Output rule:` paragraph after `Effective authority:` (I5 and the return default); the bulky-output sentence stays at the end | W4.1 | none |
| `assets/implementation-contract.md`, `alaa-documenter` | new | `Task tracking:` block: by ownership action, the claim command with read-back, the checkpoint append command with block I1, never close, no `bd` write under `none` | W1.3, W4.1 | none |
| `assets/planner-contract.md` and both planner definitions | "Return a bounded report with evidence paths, never a transcript or a raw log. Default length ..." | Replaced by the shared `Output rule:` paragraph | W4.1 | none |
| codex `assets/reviewer-contract.md`, both reviewer definitions | no output or return-length rule | `Output rule:` paragraph | W4.1 | none |
| 20 cc and 19 codex hand-written definitions | no output or return-length rule | `Output rule:` paragraph after `Effective authority:` | W4.1 | none |
| `VERSION`, `CHANGELOG.md`, codex `README-fa.md` | 7.0.0 | 7.1.0, one entry; the codex entry records that the advisor points have no equivalent | version | none |

## Lead correction applied after the first commit

| File | First commit | Corrected | Source |
|---|---|---|---|
| `references/delegation-prompts.md`, `assets/implementation-contract.md`, `alaa-documenter`, every implementer definition | `bd --sandbox --actor <actor> update <id> ...` | Flags after the subcommand: `bd --sandbox update <id> --claim --actor <actor>` and `bd --sandbox update <id> --if-assignee <actor> --append-notes "<block>" --actor <actor>` | lead correction, to match `alaa-workflow references/task-tracking.md` `## Agent identity and ownership` |
| `references/delegation-prompts.md` `<beads_identity>` rule | `Lane:` lines "in the root notes" | `Lane:` lines in the root's checkpoint block; only the lines of the last block are live | lead correction, checkpoint I1 |
| both packs | no statement of the resume commands I3 | no change: neither pack states I3 | lead correction, point 2 |

## Checker clauses

| Tuple | Reworded | Deleted |
|---|---|---|
| `BOUNDED_REQUIREMENTS` (both `scripts/check_agent_contracts.py`) | 1: "Evaluate the cheapest eligible supported available model AND effort pair for EVERY role" becomes "read the model AND effort pair for EVERY role from the fit table" | 0 |
| `task_allocation_failures`, `economy_failures`, `DEFAULT_REQUIREMENTS`, `DEFAULT_MODEL_CLAUSES`, `agent_failures`, `dispatch_failures`, cc positional clause | 0 | 0 |
| `validate_pack.py` | 0: it imports `task_allocation_failures` and holds no literal of its own | 0 |

## Fit-table walk, cc

| Sample lane | Judgment row | Search column | Pair read | Expected |
|---|---|---|---|---|
| (a) Exact rename over many enumerated files, with a cheap check | None | Ordinary: a cheap check over an enumerated scope keeps the lane there | Haiku 5.5, `medium` | match |
| (b) Bounded comparison of sources against four files | Grounded everyday: bounded decisions and no discriminating check | Ordinary | Sonnet 5.5, `medium` | match |
| (c) Everyday feature with known patterns and explicit acceptance | Grounded everyday | Ordinary | Sonnet 5.5, `medium` | match |
| (d) Refactor across services with unresolved contracts | Coupled or cross-boundary | Ordinary; third column when long | Opus 5.5, `medium`; `high` when long | match |
| (e) Judgment-dense instruction rewrite that no check can catch | Judgment-dense | Third column: hard to verify | Opus 5.5, `high`. No official row names the exceptional model for this task, so Fable 5.2, `high` needs workhorse inadequacy or a user selection | match |
| (f) Migration that runs unattended for hours | Judgment-dense or hours of autonomous work; the official row for sessions that run for hours names the exceptional model | Third column: long | Fable 5.2, `high` | match |
| (g) Second-lens review of a broad change | Coupled or cross-boundary; the second lens raises nothing (*Too strong*) | Ordinary, or third column | Opus 5.5, `medium` or `high` | match |

## Fit-table walk, codex

| Sample lane | Judgment row | Search column | Pair read | Cell |
|---|---|---|---|---|
| (a) | None | Ordinary | `gpt-6-luna`, `medium` | official: *Small existing-file edits*, balanced |
| (b) | Grounded everyday | Ordinary | `gpt-6.1-sol`, `medium` | official: *Research decisions/fact verification*, balanced |
| (c) | Grounded everyday | Ordinary | `gpt-6.1-sol`, `medium` | official: *Application features*, balanced |
| (d) | Coupled or cross-boundary | Ordinary; third column when long | `gpt-6.1-sol`, `medium`; `high` when long | local policy; nearest row *Update/debug existing software* |
| (e) | Judgment-dense | Third column | `gpt-6.1-sol`, `high`; `gpt-6-astra` only on the evidence | local policy; analogy *Adapt existing content* |
| (f) | Judgment-dense or hours of autonomous work | Third column | `gpt-6.1-sol`, `high` | official: *App/service migration*, balanced |
| (g) | Coupled or cross-boundary | Ordinary, or third column | `gpt-6.1-sol`, `medium` or `high` | local policy; subagents page prose on `high` for reviewer agents |

## Pair comparison after normalization

`SKILL.md`, `references/verification-and-gates.md`, `references/delegation-prompts.md` and the allocation
procedure differ between the packs only in these places: the pack and runtime names; the fit-table model
names, support cells and the two effort bullets; the codex eligibility sentences of step 2, its Terra
section and its bug branch; the role names of each roster; and the cc advisor text, which the codex
changelog records as having no equivalent. Each difference that existed before this lane is unchanged.
