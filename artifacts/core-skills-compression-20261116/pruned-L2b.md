# Pruned rules — lane L2b, `alaa-testing-strategy`

Second pass under `lane-brief-2.md`. Paths are relative to `skills/sohrab/alaa-testing-strategy/`.
The checker is `scripts/check_execution_contracts.py`. `REQ` is `REQUIREMENTS`, `NORM` is
`NORMATIVE_DUPLICATES`.

## Decisions (not prunes)

| File | Decision | Checker effect |
|---|---|---|
| `references/50-flake.md` | The sentence "Treat and report an unclassifiable case as a product defect" contradicted the `SKILL.md` stop condition. It is replaced: a case still unclassified after every step and the production question is a blocker, gets no default class, and is reported blocked under `SKILL.md` *Stop conditions*. The production tiebreaker and the "nothing the test controls" row stay. | `CONTRADICTIONS` gains the full old clause, so a file that restores it fails the gate |
| `scripts/check_execution_contracts.py` | `NORM.doctrine` held a forbidden string that no owned file carried: "a check outside the list runs only when the repair changes shared behaviour or proves a new reachable surface". It is realigned to the sentence that now states that rule, in `references/100-test-execution.md`: "Extend coverage only for shared behavior, a newly reachable surface or a required uncovered claim". | Removed from `NORM.doctrine`; the new clause added to `REQ.execution` and `NORM.execution` |
| `SKILL.md`, `references/100-test-execution.md`, `references/80-evidence-and-reporting.md` | Four statements of the concealment ban are merged into one owner sentence under `SKILL.md` *A failing tier is classified before it is repaired*: "Never make a check pass by deleting or weakening an assertion, suppressing a finding, lowering a threshold, widening a tolerance, adding an assertion retry, skipping a case or altering a fixture". It carries the union of the four. `100` and `80` point to it. | `REQ.doctrine` and `NORM.doctrine` entry reworded to the new sentence; `REQ.execution` entry replaced by the pointer clause "which also bans every change that conceals a failure"; `NORM.execution` entry deleted as merged |
| `SKILL.md`, `references/70-failure-mode-first.md` | The ten design steps moved from the body to `70` *Design order*. The body keeps the heading and one triggered pointer. Step 1 of the old list already sent every designer to `70`. | none |
| `SKILL.md`, `references/80-evidence-and-reporting.md` | The output contract keeps all 17 field names, their order, and the tokens of `Decision`, `Not written`, `Tier` and `Flake` in the body. The content of the other fields moved to `80` *The report fields*, behind a pointer that triggers before the report is written. | none |
| `SKILL.md`, `references/90-test-economy.md` | Detail of non-negotiables 10, 13 and 14 (create shared infrastructure once, the topic definition, which steps consume a build) is stated once in `90` *Setup once*, *Topic and layer selectors* and *Build once per tree state*. Each non-negotiable keeps its rule and a pointer. | none |

## Pruned rules

| File | Rule, in one line | Code | Checker clause deleted |
|---|---|---|---|
| `SKILL.md` | After a failed maintainer check: "Preserve evidence." The repair budget and the blocked report stay. | P1 | none; "Either nonzero blocks the affected claim" stays bound |
| `SKILL.md` | "This skill owns what each class licenses you to conclude." The rule that no class permits a pass report stays. | P5 | none |
| `SKILL.md` | "Source checks prove no live-agent compliance." The script docstring states it. | P6 | none |
| `SKILL.md` | "Before you read any reference, read the topic map." Narrowed to a reference that no body pointer names. | P2 | none |
| `SKILL.md` | "Runtime orchestration is optional. Role allocation, observer independence and scheduling stay with the caller's runtime orchestrator" in *Executing checks*. | P5 | none |
| `SKILL.md` | The pointer that sent every design, review and execution to `10` *Anti-patterns*. | P2 | none |
| `references/00-topic-map.md` | "`/alaa-prompting-guide` owns model and effort capability evidence. This skill names no model." | P5 | none |
| `references/00-topic-map.md` | "`/alaa-workflow` owns durable execution state, write ownership and resume." | P5 | none |
| `references/00-topic-map.md` | Reliability row: "the rule that an untested degraded path is a broken path" (another skill's rule, restated). | P5 | none |
| `references/00-topic-map.md` | "Loading the whole tree means the task was not scoped." | P1 | none |
| `references/40-proof-strength.md` | "This file owns only what the resulting proof is called and what it rules out." | P5 | none |
| `references/70-failure-mode-first.md` | Dependency modes are "ordered there by how often they are missed". | P5 | none |
| `references/80-evidence-and-reporting.md` | "No other output contract exists in this skill." | P5 | none |
| `references/80-evidence-and-reporting.md` | "This file owns claim evidence and proof reporting." | P5 | none |
| `references/80-evidence-and-reporting.md` | A citation across a subagent boundary: "the observing lane's evidence carries its owner". The rule to name the observing agent stays. | P3 | none |
| `references/90-test-economy.md` | "`SKILL.md` *Scope tiers* owns which selectors each tier runs." | P5 | none |
| `references/100-test-execution.md` | "This file owns execution procedure, with or without an orchestrator." | P5 | none |
| `references/110-execution-resources.md` | "This policy applies to direct work and either runtime." | P5 | none |
| `references/110-execution-resources.md` | "PHPUnit is commonly single-process unless a parallel runner is configured." | P4 | none |
| `references/120-result-classification.md` | "This vocabulary applies with or without an orchestrator." | P5 | none |
| `references/120-result-classification.md` | Diagnostic step: "Inspect the owning code, test or configuration path." | P2 | `REQ.classification` and `NORM.classification`: the same string |
| `references/120-result-classification.md` | Diagnostic step: "Route the smallest grounded next action." | P2 | `REQ.classification` and `NORM.classification`: the same string |

## Checker clauses deleted with a merged or duplicate sentence

The brief needs no row for a duplicate sentence. Acceptance criterion 4 needs a row for each
deleted clause, so these are listed.

| File | Sentence | Why it went | Clause deleted |
|---|---|---|---|
| `references/110-execution-resources.md` | "Priority alone is not a CPU limit." | Duplicate of "Lower priority does not limit parallelism. Configure both", which stays bound and forbidden | `REQ.resources` and `NORM.resources`: the same string. The contradiction "Priority alone caps CPU usage" stays |
| `references/100-test-execution.md` | "When no machine-readable reporter exists, retain the raw exit status and output." | Merged into the reporter item of the check list; the rule stays | `REQ.execution`: the old string. The merged clause binds both halves |
| `references/100-test-execution.md` | "Never weaken assertions, suppress findings, lower thresholds, widen tolerances, add assertion retries or alter fixtures to conceal failure." | Merged into the `SKILL.md` owner sentence (see Decisions) | `NORM.execution`: the old string. `REQ.execution` now binds the pointer |

## Checker clauses reworded (the lead re-checks these forbidden strings at integration)

Each new string was searched in both orchestrator packs and in `alaa-workflow` at `37ce87a4`:
no hit.

| Tuple | Old clause, start | New clause |
|---|---|---|
| `REQ.body` | "references/00-topic-map.md" | "references/100-test-execution.md": the *Executing checks* sentence now names the execution reference directly, and the literal follows it |
| `REQ.execution`, `NORM.execution` | "Runtime orchestrators own role authority, observer independence, allocation, and the scheduling…" | "This procedure grants no role authority, observer independence, allocation or scheduling" |
| `REQ.execution`, `NORM.execution` | "required gates, exact commands and scoped inputs, cwd, timeout, … and eligible citations" (one clause) | "the required gates, with each exact command, its scoped inputs, cwd, timeout, environment and resource limits" and "the expected cases, declared case dependencies, aggregate-to-child coverage and eligible citations" (two clauses) |
| `REQ.execution`, `NORM.execution` | "Record each command's machine-readable reporter when available and retain its output" | "each command's machine-readable reporter, with its output retained; without one, the raw exit status and output" |
| `REQ.execution`, `NORM.execution` | "Record the tested content snapshot, relevant untracked inputs and tool versions" | "the tested content snapshot, relevant untracked inputs and tool versions" |
| `REQ.doctrine` | "cite the result with its original command and timestamp" | "Cite a recorded result, with its original command and timestamp" |
| `REQ.doctrine`, `NORM.doctrine` | "A tier is never made to pass by deleting an assertion, …" | "Never make a check pass by deleting or weakening an assertion, …" (see Decisions) |

Counts by `measure.py`, before to after: `REQUIREMENTS` 213 to 211; `NORMATIVE_DUPLICATES` 105
to 102; `CONTRADICTIONS` 19 to 20. As tuple lengths they are 205 to 203 and 101 to 98.
`EXPECTED_NORMATIVE_INVENTORY_SHA256` was recomputed by the script's
own `normative_inventory_failures`. The tuples `router`, `flake`, `economy`, `workspace`
and `continuity` are unchanged.

## Removed without a row (duplicates of a rule that stays in this skill, and reasons)

Listed so that the owner can find them; the brief requires no row.

- `references/10-what-makes-a-test.md` *Anti-patterns*: 20 negative restatements, each with a
  pointer to its owner file. 17 restate an always-loaded body rule. The other three stay in
  `30-doubles.md` (no mock for an outcome observable in state), `50-flake.md` (quarantine
  owner and deadline) and `90-test-economy.md` *Setup once* (no engine, container, migration
  or application boot per test).
- `references/90-test-economy.md` *Review checks*: five restatements of rules in the same file.
  Its one unique rule stays in *Candidates that are not owed a test*: a kit or package under
  development keeps the tests of the behaviour it owns.
- `references/50-flake.md` *Why the classification comes first* and
  `references/70-failure-mode-first.md` *Ordering, and what it prevents*: rationale for
  non-negotiables 6 and 8.
- `references/70-failure-mode-first.md` *Deriving the test from the mode*: steps 3, 5 and 6
  restated `20-layers.md` and the core rule. The design-gap stop and the on-demand cause stay.
- `references/00-topic-map.md`: the ownership rows for the orchestrators, the per-language
  skills and `/alaa-controlled-ops`. `SKILL.md`, `100-test-execution.md` and
  `40-proof-strength.md` state each at the decision site.
- `references/40-proof-strength.md`: the four-item list for an unreachable level; `80` *When a
  test cannot be run at all* owns the steps.
- `references/20-layers.md`: the "double's fidelity" row (in `30-doubles.md`) and the closing
  pointer to `100` and `110`.
- `references/110-execution-resources.md`: the targeted Go example (the runner example shows
  the same flags), the restated validity and exhaustive-tier rules, and the shared-container
  rule that `90-test-economy.md` owns.
- `SKILL.md`: the pointer to `80` *Reruns* under the validity rules and the "under `80`"
  pointer for an unreachable tier. The topic-map row for reporting a result routes both.
- `agents/openai.yaml` `default_prompt`: eleven sentences that restated `SKILL.md`.
- Reason clauses that only restated their rule, in non-negotiables 1, 2, 4, 5, 9, 11, 13, 14
  and 15 and across the references.
