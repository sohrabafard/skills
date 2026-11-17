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

## Review repair (`review-main.md`, lead decisions D1-D16)

A row applies to both packs unless its first column names one. The last column names the finding or the lead
decision. No checker clause was reworded or deleted: each bound literal (`Reopen allocation only for remaining
work`, `Role title, sensitivity, duration`, `second independent lens`, `not model diversity`, `Justify model
and effort separately`, `actual failed fit predicate or stronger task-specific evidence`, `no quotas`,
`no mandatory trial ladder`) is still in the text verbatim.

| File | Old rule | New rule | Finding or decision | Checker clause |
|---|---|---|---|---|
| `references/routing-matrix.md` fit table, *Judgment-dense* row | "Judgment-dense work that no check can catch, or hours of autonomous work" | "Judgment-dense work that no check can catch"; duration moves a lane along the effort columns only | D1, 18, 33 | none |
| cc `references/routing-matrix.md` *Exceptional model* | new | The official row *agent sessions that run for hours* supports the first evidence arm only for a lane in the *Coupled or cross-boundary unresolved decisions* or *Judgment-dense work* row | D1 | none |
| codex `references/routing-matrix.md` support cells | *App/service migration* supported the *Judgment-dense* row | *Judgment-dense* row: local policy, by analogy with *Adapt existing content*. *Effort support*: for a long migration in the grounded or coupled row, *Long* is the balanced cell of *App/service migration* | D1 | none |
| `references/routing-matrix.md` under the fit table | new | A lane that implements nothing: an evidence or research lane with a given question, sources and return form takes the grounded row; a review lane takes the row of the hardest decision in its scope, never a later row because it is a second lens; the rule-writer takes the row of the text it rewrites | D2 | none |
| `references/routing-matrix.md` fit table, rows 2 and 3 | Row 2: "every bounded-suitability predicate below holds". Row 3: "A lane with bounded decisions and no discriminating check belongs here" | Row 2 only: the row applies only when every bounded-suitability predicate is recorded for the lane; otherwise the next row applies | D3 | none |
| `references/routing-matrix.md` fit table header and *Effort within a model* | "Hardest long-running work"; "Use the last column or `max` only with a recorded measured gain" (codex: plus `ultra`, or an official cell at the selected priority) | The header carries the condition in both packs: "with a recorded measured gain"; `max` (codex: and `ultra`) needs the same recorded measured gain. Codex exceptional row: an official Astra `xhigh` cell also needs it | D4, second round | none |
| `references/routing-matrix.md` *Effort within a model* | "Move one column right for a long, strict or unverifiable lane" | The same, with a threshold: more than one working session of the lane, more than about ten files that depend on each other with no cheap discriminating check over them, or a result that no check can catch | D4, second round | none |
| cc `references/routing-matrix.md` *Effort within a model*, *Effort support* | *Ordinary* "is the model's surface default in this runtime"; each model reference holds the default | "Start at the *Ordinary* cell"; *Ordinary* is each model's Claude Code default, stated in `36-haiku-5-5.md`, `31-sonnet-5-5.md`, `21-opus-5-5.md` and `43-fable-5-2.md` | D4 | none |
| cc `references/routing-matrix.md` fit table, Sonnet support cell | "effort from the Sonnet prompting note under that table" | "effort from that row's *Effort evidence* cell" | 22 | none |
| `references/routing-matrix.md` *Reclassify* | "Correct the judgment fact" | Recheck both facts against the lane record and correct the one that the record does not support | 21 | none |
| `references/routing-matrix.md` defect bullet and departure bullet | "Correct it before dispatch." A separate bullet: "When you depart from the table cell in either direction, record the actual failed fit predicate or stronger task-specific evidence" | One bullet: correct the pair before dispatch, unless a recorded reason selected it: an explicit user choice, the actual failed fit predicate or stronger task-specific evidence, such as a lane return under step 4. The separate departure bullet is removed, so a step-4 raise is no defect | 17, 34, D14 | `BOUNDED_REQUIREMENTS` literals kept |
| `references/routing-matrix.md` step 4, lower arm | "when the lower cell still fits them" | "when no fit predicate of theirs fails at the lower cell", so that the positional *Too weak* definition does not void the arm | 19 | none |
| `references/routing-matrix.md` *Too strong* | A later row, or `high` effort or above, on a settled lane with a discriminating check; one consequence sentence | A model from a later row than the lane's own, or an effort column right of the lane's own; consequence sentence removed | 19, 32, 43 | raw literals kept |
| `references/routing-matrix.md` *Too weak* | A model of the first two rows on coupled decisions; `low` or default effort on a long unverifiable lane; one consequence sentence | A model from an earlier row than the lane's own, or an effort column left of the lane's own; a cheap pair while a fit predicate fails; consequence sentence removed | 19, 43 | none |
| `references/routing-matrix.md` *Justify* | "Justify model and effort separately: the model from the judgment fact, the effort from the search and length fact." | "Justify model and effort separately." An explicit user priority decides only when the search and length fact admits two adjacent columns: the lower-cost or the higher-quality cell; local policy | 26, 25, 42, D14 | `BOUNDED_REQUIREMENTS` literal kept |
| codex `references/routing-matrix.md` *Effort support* | "Under an explicit user priority, read the lower-cost or the higher-quality cell of the named official row." | removed; the priority sentence of the *Justify* bullet replaces it, so that priority stays inside the fit | 25 | none |
| `references/routing-matrix.md` step 4, raise arm | "raise one step for the rest"; "raise the model to the next one in the table. A raise to the exceptional model still needs its evidence." | Raise for the lane's remaining scope and the remaining similar lanes; raise to the next stronger model, or the effort one column when the next row names the same model; the exceptional model only after a shortfall at `high` effort or above, with its evidence | 20, 24, D11 | none |
| `references/routing-matrix.md` *Batch allocation*, *Reassignment* | Reassessment points: a material scope change or a fix follow-up (and the initial assignment) | The same points, plus a lane return under step 4 of All-role task allocation, so that the raise and the lowering can both fire. Step 4 opens "When a lane returns in one of these two ways" in place of "At a reassessment point of Batch allocation or Reassignment", so that the two texts do not define each other | 20, D15 widened in the second round | `Reopen allocation only for remaining work` kept |
| `references/routing-matrix.md` step 3, step 4, *Implementation routing* | "A pair fits when it is neither stronger nor weaker than the lane needs."; "Completed work stays as it is, so this rule is feedback, not a trial ladder."; "Each route below names its fit-table row." | removed: each restated a rule that the same file still states | 42 | none |
| codex `references/routing-matrix.md` fit table and *Codex Terra eligibility* | No table cell named `gpt-6.1-terra`; "Compare eligible pairs through the same allocation procedure." | The bounded row names Terra "only under *Codex Terra eligibility*". A Terra pair replaces the Luna pair of that row at the same column as a recorded departure whose evidence is the Terra workload; where the official row names Terra at the selected priority (*Find visible controls in an app*, *Update specified records in an app*), take that cell | 23, D11 | none |
| codex `references/routing-matrix.md` `alaa-implementer-xhigh` | "Sustained coupled technical reasoning admitted by the batch source mapping and lane requirements." | "Sustained coupled technical reasoning."; the fit row and the search fact in the same bullet are the admission | 27, D11 | none |
| `references/delegation-prompts.md` `<task_controls>` | "and that is the most common cause of a pair that is too strong" | "which can make the pair too strong" | 22 | none |
| `references/delegation-prompts.md` `<beads_identity>` | The bullet restated the claim and checkpoint commands and "Before it returns or stops" | The implementation and documenter definitions hold the claim, checkpoint and knowledge-comment commands | 9, 30, D10 | none |
| cc `references/delegation-prompts.md` advisor sentence | "A dispatch states no advisor text"; apply `41` only to a prompt for another surface | Every dispatch does the four things of `41`: the envelope carries the first; add to `<constraints>`, unless present, the visible decision before acting and the saved deliverable before the lane declares the work done; no lane depends on an advisor; no advisor timing or weight text | 36, D16 | none |
| Shared `Output rule:` paragraph: 5 contract assets, 39 hand-written definitions, 31 rendered ones | Bound each command's output with a quiet flag, a filter, `tail` or a redirect; "Never print a whole file, log, tree or diff"; default length about 40 lines | Bound the output of each command you choose; run a supplied command unchanged and, where the dispatch permits an artifact file, redirect its output there and read only the failing slice; read a whole file or diff only when the task needs all of it; return rule and the 40-line default in one sentence | D7, D10, 28, 29 | none |
| `Task tracking:` block: both implementation contracts, both documenter definitions, 25 rendered implementers | Checkpoint only "before you return or stop"; no knowledge comment; "The last block is the current one"; "the lead closes it after it reconciles your diff"; fallback for a failed append only | Checkpoint "when your position changes and before you return or stop"; tagged knowledge comment with `bd --sandbox comments add <id> "<tag>: <text>" --actor <actor>` and the seven tags; a failed or not-permitted `bd` write goes in the return; "Never close the leaf."; a failed claim returns `BLOCKED` | D10, 9, 30, 37 | none |

Sentences that exist in one pack only after this repair: the cc sentence on the official row *agent sessions
that run for hours*; the cc *Effort support* citation of the four model references; the cc advisor paragraph
of `delegation-prompts.md`; the codex migration sentence of *Effort support*; the codex Terra cell and
section; the codex clause of the exceptional row "an `xhigh` cell also needs a recorded measured gain".

The fit-table walk rows (f) above record the row as it was before D1. After D1, lane (f) reads the
*Coupled or cross-boundary unresolved decisions* row, or the *Grounded everyday decisions* row, at the *Long*
column: Opus 5.5 `high` for a coupled migration in the cc pack, and `gpt-6.1-sol` `high` in the codex pack.

## Second repair round

Two verifiers found five items still wrong after the first repair. The rows above marked "second round" hold
the final text of three of them. The other two change `CHANGELOG.md` of both packs, which the round's task
names although the owned-path list does not:

| File | Old text | New text | Item |
|---|---|---|---|
| both `CHANGELOG.md`, 7.1.0 allocation entry | Step 4 adjusts the pair "at the existing reassessment points" | Step 4 adjusts it when a lane returns light, incomplete or trivially finished, which *Batch allocation* and *Reassignment* now list as a reassessment point | new, 20 |
| both `CHANGELOG.md`, 7.1.0 output-rule entry | "bound each command's output" | The agent bounds the output of each command it chooses, runs a supplied command unchanged with its output redirected only to a permitted artifact file, and reads a whole file or diff only when the task needs all of it | new |
| both `CHANGELOG.md`, 7.1.0 Beads entry | A checkpoint "before it returns or stops"; "the two commands" | A checkpoint when the position changes and before the lane returns or stops, knowledge as tagged comments; the claim, checkpoint and knowledge-comment commands | new |
| cc `CHANGELOG.md`, 7.1.0 advisor entry | A dispatch carries no advisor text; `41` only for another surface | Every dispatch does the four things of `41`; `<constraints>` gains the two lines unless present; no advisor timing or weight text | new |
| codex `CHANGELOG.md`, 7.1.0 entries | "its no-advisor-text dispatch rule"; cells Luna, Sol, Astra; "every other cell is marked as local policy" | "its advisor rule for dispatches"; Terra named under *Codex Terra eligibility*; *Ordinary* is official or local policy as the row says, and every cell that a row does not call official is local policy | new |

## Lead edits after the second verification

| File | Old rule | New rule | Reason | Checker clause |
|---|---|---|---|---|
| both `references/routing-matrix.md`, step 4 | A raise could enter the last column without its condition | "A raise into the last column still needs its recorded measured gain." | Verifier: conflicted with the table header | none |
| both `references/routing-matrix.md`, step 3 | "An explicit user priority decides only when ..." | "Within a model, an explicit user priority picks the effort only when ..." | Verifier: the unscoped sentence contradicted the exceptional-model arm and the Terra rule | none |
| both `references/routing-matrix.md`, step 4 | Lower "when no fit predicate of theirs fails at the lower cell" | Lower "when every fit predicate of the lower cell is recorded for them" | Verifier: an unrecorded predicate has not failed, which contradicted the tie rule at the table | none |
| codex `references/routing-matrix.md`, bug branch | The three Luna identities were chosen "from the exact official bug row and the selected priority" | They are chosen by the search and length fact | Verifier: identity and pair disagreed after the priority rule changed; the Claude Code twin already selects by length | none |
| both `references/delegation-prompts.md` | "The lead keeps one `Lane:` line ... only the lines of the last block are live." | Pointer to `alaa-workflow references/task-tracking.md` section `Agent identity and ownership` | Decision D8: the timing rule is stated once, at its owner | none |
