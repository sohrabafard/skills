# Ledger, lane L5c-b — contract assets and agent definitions of the orchestrator pair

Scope: `skills/sohrab/alaa-cc-orchestrator` and `skills/sohrab/alaa-codex-orchestrator`:
`assets/*-contract.md`, `assets/profile-wrappers.json`, `agents/*`, and the agent-bound clauses of
`scripts/check_agent_contracts.py`. Every row applies to both packs unless it names one. Paths are
relative to a pack. "All agents" means every hand-written agent and every contract asset, and so
every generated wrapper. Criterion codes are those of `lane-brief-2.md`. Restore a rule by putting
its sentence back in the named file of both packs and, where a clause is named, the clause too.

## 1. Pruned rules

| # | File | Rule removed | Code | Checker clause deleted |
|---|---|---|---|---|
| 1 | all agents, `Task controls:` | The agent resolves an omitted model or effort itself through `references/model-effort-policy.md`. Replaced by "an omitted field is the lead's default, not a block". | P3 | `agent_failures`: "resolve an omitted field through" |
| 2 | all agents, `Task controls:` | Block the lane when the pair is still missing after that normalization. The case cannot occur once rule 1 is gone. | P3 | `agent_failures`: "missing after normalization" |
| 3 | all agents, `Task controls:` | "Model choice changes no authority, tools, skills, verdicts or independent gates." The first half of the sentence, "The role name selects no control", stays. | P1 | none; the literal "model choice changes no authority" is reworded to "The role name selects no control" |
| 4 | all agents, `Effective authority:` | "Before using tools, inspect the active sandbox, parent overrides and tool/MCP grants." The limit "stay inside the narrower of this role and the active sandbox, parent overrides and tool/MCP grants" stays. | P2 | none |
| 5 | all agents, `Effective authority:` | "A read-only declaration proves no runtime enforcement; report missing enforcement evidence as unknown." No output item and no lead step reads that report. | P3 | none |
| 6 | cc agents, `Runtime:` | "Runtime: Claude Code subagent." The Bash limit of a read-only role stays. | P4 | none |
| 7 | `assets/implementation-contract.md` | "Your dispatch gives the outcome, owned files/modules, exclusions, acceptance criteria, verification commands, constraints and known dependencies." | P4 | none |
| 8 | `assets/implementation-contract.md` | The three bases of an exceptional-model admission (official route with the remaining reasoning need and the rejected alternatives; inadequacy of the high-effort workhorse; explicit user selection) and "Complexity or role identity alone is insufficient". The lead applies them under `references/routing-matrix.md`; the agent keeps "comes only from the lead's recorded task allocation" and the pointer to its profile's section. | P5 | none; the cc-only literal is reworded |
| 9 | `assets/implementation-contract.md` | "Never assume that prose or a caller override changed pinned controls." | P1 | none |
| 10 | `assets/implementation-contract.md` | "No lightweight trial or replay of completed work is required." | P1 | none |
| 11 | `assets/implementation-contract.md`, Engineering baseline | "Follow AGENTS.md and repository conventions before editing." The runtime loads those files. | P4 | none |
| 12 | `assets/implementation-contract.md`, Engineering baseline | Fallback for a skill that is not installed: "preserve its intent: explicit types/contracts, cohesive units, SOLID where useful, explicit error handling, no dead code, and tests for changed behavior". Replaced by the absence-action rule of row R1 below. | P1 | none |
| 13 | `assets/implementation-contract.md`, Design method | "Read the architecture decisions, contracts, call sites, tests and documented failure semantics that constrain the lane." | P2 | none |
| 14 | `assets/implementation-contract.md`, Design method | "Compare the viable designs internally." The decision rule and the report of rejected alternatives stay. | P1 | none |
| 15 | `assets/implementation-contract.md`, Verification | "Consume the cadence through the orchestrator's `references/verification-and-gates.md`" (the pointer; the cadence and cursor arrive in the dispatch) and "Outside that file's floors, the parent may accept your focused evidence." | P5 | `IMPLEMENTER_REQUIREMENTS`: "the parent may accept your focused evidence" |
| 16 | `assets/planner-contract.md` | "The parent selects controls from the actual task; clear scope, contracts and constraints are distinct from interacting uncertainties." | P5 | none |
| 17 | `assets/planner-contract.md` | "`references/verification-and-gates.md` owns scheduling." | P5 | none |
| 18 | `agents/alaa-adversarial-reviewer` | "Apply only the trigger and review boundary in `references/routing-matrix.md`." The lead applies the trigger; the body states the boundary. | P5 | none |
| 19 | `agents/alaa-documenter` | "Read repository documentation conventions first." The rule to keep those conventions stays. | P2 | none |
| 20 | `agents/alaa-documenter` | "You receive the verified goal, reconciled change summary, touched files, review verdicts and documentation scope." | P4 | none |
| 21 | `agents/alaa-explorer` | "Read applicable AGENTS.md and repository guidance first." | P4 | none |
| 22 | `agents/alaa-explorer` | "Prefer targeted symbol and search traversal over broad file dumps." The preloaded routing skill (cc) and the code-graph line (codex) state the method. | P1 | none |
| 23 | `agents/alaa-explorer` | "Keep the report compact and evidence-dense." | P1 | none |
| 24 | `agents/alaa-spec-analyst` | "AGENTS.md" in the list of sources to read before asserting a guarantee. | P4 | none |
| 25 | `assets/profile-wrappers.json`, descriptions | "Scoped implementation;" in the implementer tail. | P5 | none |
| 26 | `assets/profile-wrappers.json`, descriptions | "Carries the … doctrine of its stack." (laravel, frontend, go) and "Loads the owning skill of each surface before the first edit." (infra). The binding states this; it is no trigger, exclusion or limit. | P5 | none |
| 27 | `agents/alaa-architecture-critic` | What `/alaa-system-design` owns ("the six conditions that require a design pass, the boundary and seam tests, contract-before-code, one writer per datum, the dependency classification and the two-candidate rule"). The call line and the pointer to its `references/70-review-and-readiness.md` stay. | P5 | none |
| 28 | `agents/alaa-performance-profiler` | What the complexity budget of `/alaa-algorithms-data-structures` contains ("the named operation, the growing input dimension, the bound, and the input size at which the bound was measured"). The three read conditions stay. | P5 | none |
| 29 | `agents/alaa-documenter` | "which owns the thresholds, the decision order and the only grade that needs human approval" beside the size-ladder pointer. | P5 | none |

## 2. Sentences removed as restatements of a skill the agent loads

The brief asks for one call line where a preloaded skill's body states the rule. Codex has no
preload; its call line loads the same body.

| # | File | Sentence removed | Stays |
|---|---|---|---|
| S1 | `assets/implementation-contract.md`, Design method | "Apply /alaa-testing-strategy for owed tests, reachable failures, discriminating assertions, layers and proof; record omitted candidates under its contract." | the `Testing:` call line |
| S2 | `assets/implementation-contract.md`, Execution rules | "Derive changed-behavior tests, selectors and reset-safe setup through /alaa-testing-strategy before writing them." | the `Testing:` call line |
| S3 | `agents/alaa-test-strategist` | The eight-step enumeration of the testing-strategy design procedure, and the codex-only "Doctrine:" line. | "Derive the matrix by the test-design procedure of /alaa-testing-strategy: failure modes first, the happy path last." |
| S4 | `agents/alaa-researcher` | "Before choosing a repository code-evidence surface, apply /alaa-code-intelligence-routing once and reuse its result." | "Never retrieve the same fact through a second surface", the cc preload and the codex code-graph line |

## 3. Relocations inside the owned files (no rule lost)

| # | From | To | Note |
|---|---|---|---|
| R1 | the four stack bindings in `assets/profile-wrappers.json`: "For a named skill that is not installed, follow its absence action in the dispatch's `<skills>`; when the dispatch names none, report the missing skill under residual risks…" | Engineering baseline of `assets/implementation-contract.md` | Now binds every implementer. The report goes under output item 3, which already lists a skill not loaded. |
| R2 | `Return protocol` (VERDICT form): the definition of NOT ASSESSED | the NOT ASSESSED output item of each gate role | The pointer "as the Return protocol defines it" is gone. |
| R3 | `Return protocol` (VERDICT form): "the first line is the VERDICT line, with nothing before it" | output item 1, "First line exactly" | Already stated there. |
| R4 | implementation contract: the 110 and 120 pointers in Verification | the `Testing:` line | One line carries the three references and their triggers. |
| R5 | implementation contract: "For design work, also report…" | last bullet of Design method | |
| R6 | `agents/alaa-verifier`: "never add, substitute, reorder, repair or repeat checks" (Execution protocol 1) | Authority boundary | One bullet. |

## 4. Alignments between the packs

Each row made both packs state one rule in the stronger form. None is a prune.

| # | File | Before | Now, in both packs |
|---|---|---|---|
| A1 | `agents/alaa-verifier` | cc: one bullet, "Never diagnose or fix a failure, substitute, reorder or repair commands…". codex: two bullets naming `alaa-failure-analyst` and the blocked-or-ambiguous report. | the codex form, two bullets |
| A2 | `agents/alaa-reviewer` (cc), `assets/reviewer-contract.md` (codex) | different wording of the no-filter rule and of the adversarial-lens bullet | one text: a later step never sees a withheld finding; doubt goes in severity and confidence; `alaa-adversarial-reviewer` is separately gated and runs after the reviewer |
| A3 | `agents/alaa-instruction-reviewer` | cc "no MCP, edits, fixes…"; codex "no MCP, mutations, fixes…" | "no MCP, mutation, fix, installation, commit, delegation or external action". The first clause stays per runtime: native inspection only (cc, no shell); bounded read-only file and Git commands (codex). |
| A4 | `agents/alaa-architecture-critic` | cc "Apply each of these preloaded skills when the change touches its surface"; codex "Load each of these when it is installed and when the change touches its surface" | "Apply each of these when it is installed and the change touches its surface" |
| A5 | `agents/alaa-test-strategist` | codex-only "Doctrine:" line | removed with S3; the method bullet calls the skill in both packs (cc: preloaded; codex: loaded first) |
| A6 | `agents/alaa-adversarial-reviewer` | cc "findings `alaa-reviewer` already raised"; codex "the selected correctness reviewer" | "the correctness reviewer" |
| A7 | descriptions of `alaa-adversarial-reviewer`, `alaa-api-contract-reviewer`, `alaa-dependency-auditor`, `alaa-documenter` | different text per pack | one text; the adversarial description carries both limits (never re-runs the correctness review, never enters a fix loop) |
| A8 | `agents/alaa-explorer`, `agents/alaa-researcher`, both contracts | "lead session" (cc), "main thread" (codex), "parent" | "the lead" |
| A9 | `assets/planner-contract.md` (cc) | own `Runtime:` variant | the common `Runtime:` line |
| A10 | implementer descriptions | "never this compatibility ID" and "never this role name" | "The task, not this ID, selects model and effort." |

Runtime mechanics kept as they are: the cc `Runtime:` line; the codex code-graph line; the codex
"Start no subagent" bullet in hand-written agents (cc withholds the `Agent` tool in frontmatter);
the codex shell sentence in five read-only agents; preloaded (cc) against loaded (codex) skills;
`$playwright` in codex `alaa-browser-qa`; the pack name in pointers.

## 5. Corrections

| # | File | Change |
|---|---|---|
| C1 | both contracts | "Keep the whole report under 40 lines" is now "Default length: about 40 lines; exceed it only for required items." |
| C2 | `agents/alaa-architecture-critic` | "verification-and-gates.md Phase A step 4" is now "Stage A step 4". The lead aligns the step number after L5c-a. |
| C3 | `assets/implementation-contract.md` | "If dispatch conflicts" named no second party. It is now "When a supplied command conflicts with these rules". |

## 6. Checker clauses

`scripts/check_agent_contracts.py`, identical edits in both packs unless noted.

| Tuple | Before | After | Deleted | Reworded |
|---|---|---|---|---|
| `agent_failures` (inline) | 16 | 14 | "resolve an omitted field through"; "missing after normalization" | "otherwise unknown" to "otherwise write unknown"; "Never infer observed identity from a pin or request" to "never from a pin or request"; "Report metadata after the verdict/status or opening outcome" to "Report metadata after the first line"; "omission alone is not blocked/degraded" to "an omitted field is the lead's default, not a block"; "model choice changes no authority" to "The role name selects no control" |
| `IMPLEMENTER_REQUIREMENTS` | cc 17, codex 16 | cc 16, codex 15 | "the parent may accept your focused evidence" | "If dispatch conflicts, report the conflict and excluded commands" to "When a supplied command conflicts with these rules, report the conflict and the excluded commands"; "…request focused commands from the parent" to "…from the lead"; cc only: "Exceptional model admission follows the parent's all-role task allocation record" to "An exceptional-model admission comes only from the lead's recorded task allocation" |

Kept verbatim because a tuple also requires them in a file of another lane, or in the sibling pack:
the seven shared `specialist_cadence_failures` clauses in `agents/alaa-architecture-critic`; the
six `RUN_ECONOMY_REQUIREMENTS` `verifier_agent` clauses in `agents/alaa-verifier`; the
`implementation_contract` clause "settled decision a later lane or repair owner must know". The
inline `cadence_failures` implementer and planner clauses are unchanged.
