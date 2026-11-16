# Core skill pack compression — design

## Context

The owner asked for the seven core skills to keep their function, or improve it, in far fewer
words, with duplicate rules removed and the text aligned with the current Anthropic and OpenAI
prompting guidance. Targets, all under `skills/sohrab/`:

`alaa-testing-strategy`, `alaa-cc-orchestrator`, `alaa-codex-orchestrator`, `alaa-workflow`,
`alaa-code-intelligence-routing`, `alaa-low-noise`, `alaa-prompting-guide`.

Exploration (three read-only mapping lanes, 2026-11-16) found that the volume is mostly structural:

| Lever | Evidence |
|---|---|
| Contract text rendered into wrappers | `assets/implementation-contract.md` (1,438 words) is embedded verbatim in 11 cc and 14 codex implementer files; planner and codex reviewer contracts likewise |
| Boilerplate blocks in hand-written agents | `Task controls`, `Report metadata`, `Effective authority`, `Return protocol`: 210 to 290 words repeated in each of about 39 files |
| Preloaded bodies | `alaa-testing-strategy/SKILL.md` (4,100 words) preloads into 13 cc agents; `alaa-code-intelligence-routing/SKILL.md` into 31 |
| Superseded model references | 6 files, 7,801 words, in `alaa-prompting-guide/references/`: `10-gpt-5-6`, `20-opus-5`, `30-sonnet-5`, `35-haiku-4-5`, `40-fable-5`, `42-fable-5-1` |
| Vendor-documentation restatement | about 2,500 words in `41-claude-code-runtime-features.md`, about 1,200 in `11-codex-runtime-features.md` |
| Dated refresh logs and incident narrative | about 650 words in `00-source-map.md`, about 2,000 on dated lines of `41` |
| Rules stated in several files or skills | tables in the mapping reports: testing body versus its references, workflow pointer repeats, orchestrator restatements of workflow, prompting-guide and low-noise rules |
| Checker-bound wording | about 500 literal clauses in `check_agent_contracts.py` (both packs) and `alaa-testing-strategy/scripts/check_execution_contracts.py` |

Owner decisions (2026-11-16): reword bound sentences together with their checker literals,
one-to-one; do all three change classes; install managed agents at the end.

## Rules that bind this work

- `skills/sohrab/AGENTS.md`: read a skill in full before editing it; one owner per rule; the
  orchestrator pair changes together; nothing is deleted (retire to
  `_to_delete/20261116-core-skills-compression/` and confirm sizes with `ls -la`); growth needs a
  reason; never edit `vendor/`.
- `alaa-prompting-guide references/60-skill-authoring.md`: the draft-then-compress loop, the
  never-remove list, "a compress pass relocates nothing", the done-test, ASD-STE100 style, and
  the carry-over review table. Rewrite this file last, because every other lane is judged by it.
- Owner feedback on record: no fixtures, self-tests or comparison evals for skills; implement,
  gate once, commit; at most one independent review, only for risky text, with no confirmation pass.
- Root `AGENTS.md` Beads binding: register and claim tasks under label `repo:skills` before
  implementation. `bd where` and `bd ping` passed against the expected workspace on 2026-11-16.

## Three change classes, committed separately

1. **Compress.** Fewer words in the same file and place. Done-test: the executing agent's
   behaviour is unchanged. No rule, condition, exception, threshold, scope, named alternative,
   reason clause, stop condition, authority limit, source or verification date is removed or
   weakened. History and incident narrative is the only freely removable prose; a reason clause
   is shortened, never dropped.
2. **Relocate or retire.** A rule moves to its single owner and the other site keeps a pointer
   whose trigger is the union of the situations the moved text served. A retired file moves to
   `_to_delete/`. Each move states its reason in the commit body.
3. **Deliberate behaviour change.** Only changes that match a row of the carry-over table in
   `60-skill-authoring.md`, judged against `43-fable-5-2.md` and `12-gpt-6.md` after the
   freshness check in Phase 0. Every such change is listed in the final report with before,
   after and the source row. A change outside the table is proposed in the report, not applied.
   The "absolute approval rule" row applies to lead-session text only: `Never deploy, publish,
   force push...` in a lane contract is a true invariant for a subagent and stays.

**Loading condition is behaviour.** Moving a rule out of a preloaded or always-loaded body
changes when it applies. For a rule that applies on every run, keep one compressed line in the
body and cut the copy in the reference. Move only lookup detail behind a pointer.

**Re-review and re-test rules.** Each lane lists every rule that makes an agent re-review,
re-test or re-confirm. The lead puts the list in the final report as proposals. None is removed
or capped in this work, because those rules sit in authority text and the owner decides them.

## Checker literals

- Before rewording a sentence, grep the three clause checkers for it.
- A bound sentence and its literal change in the same commit. The mapping stays one-to-one: no
  clause is deleted, merged or loosened, and no checker logic changes.
- Phase 0 records the clause count of every tuple in the three clause checkers. Phase 4 compares
  the counts. A lower count blocks completion.
- The pair's checkers each run on the sibling pack, so a pair literal changes in both packs in
  one commit.
- `NORMATIVE_DUPLICATES` in `check_execution_contracts.py` is pinned by a SHA-256 at line 349.
  Editing any of those strings needs the new hash in the same commit.
- Raw-`in` literals break on a moved line break; whitespace-normalized ones do not. Keep a raw
  literal on one line.
- Headings cited from outside a skill stay verbatim. Appendix A lists them.
- Sentences bound by a checker in another skill are in Appendix B.
- Fixed by other checkers and left as they are: file and directory names, the lifecycle state
  rows and the `Final report` heading, a `When NOT to use` heading per skill, `openai.yaml`
  `short_description` (25 to 64 characters) and `default_prompt` (`$name`), the
  `\nEngineering baseline:` anchor, `Stack binding: ` prefixes, and every `{{token}}` and
  validator-bound heading in `alaa-workflow/assets/`.

## Phases

### Phase 0 — Baseline (lead)

1. Create the integration branch `work/core-skills-compression` from `main` in its own worktree.
   All later work happens there or in lane worktrees branched from it. `main` does not change
   until Phase 4.
2. Create `artifacts/core-skills-compression-20261116/` and write the three mapping reports
   from this planning session into it, together with Appendices A to C of this plan. Lanes read
   them from there.
3. Read `.agents/skills/beads/SKILL.md` and `alaa-workflow references/task-tracking.md`
   `## Agent identity and ownership`. Create one epic and one task per lane and per later phase
   under `repo:skills`; claim the first.
4. Record the baseline in the artifacts directory: words per load class per skill (description,
   `SKILL.md` body, each contract asset, each hand-written agent, each reference), excluding
   `CHANGELOG.md` and scripts; and the clause count per checker tuple.
5. Run every gate in the Verification section once and record the result. A gate that is not
   clean before any edit is recorded as pre-existing and is not repaired in this work unless it
   blocks a later gate.
6. Freshness check, one `alaa-researcher` dispatch: fetch the official pages listed in
   `43-fable-5-2.md`, `12-gpt-6.md`, `60-skill-authoring.md` and `61-skill-platform-mechanics.md`
   and report only differences from what those files state. The same dispatch resolves three
   known disagreements between copies: `70-agent-instruction-files.md:30` versus
   `11-codex-runtime-features.md:90` (which files are dropped at `project_doc_max_bytes`); the
   Claude subagent frontmatter list in `80-subagent-authoring.md` versus `41`; and the Codex
   skills URL in `alaa-low-noise references/90-source-map.md` versus
   `alaa-prompting-guide references/00-source-map.md`. An unresolved item stays marked open.

### Phase 1 — Per-skill lanes (parallel, one worktree each)

Each lane reads its whole skill, applies class 1 and the within-skill part of class 2, updates
the literals of checkers that live inside its own skill, runs its gates, and commits one
Conventional Commit per class. A sentence bound by a checker in another skill stays verbatim
and is listed for Phase 2. Each lane returns: before and after words per load class, relocations
with their pointers, retired files, literals changed, and sentences left for Phase 2.

| Lane | Scope | Main moves |
|---|---|---|
| L1 | `alaa-prompting-guide`, except the compression contract section of `60` | Retire the 6 superseded model files and repoint the topic map, after confirming that no live rule exists only there: check `06:99` (cites `40`), `12:3` (routes a documented legacy exception to `10`) and the policy-JSON note that `35` cites, and move any such rule to its current owner first; move the dated refresh log out of `00-source-map.md`; cut vendor restatement in `41` and `11` down to house decisions, pins and facts that change what an agent writes, each keeping its source and date, and keep every fact on the Appendix C keep-list; give the four-way artifact test, the wording failure modes and the ownership sentence one owner each; compress the rule-writer `contract.md` and copy it into both wrappers |
| L2 | `alaa-testing-strategy` | The body preloads into 13 agents with no trigger, so every always-apply rule keeps one compressed line in the body and loses its copy in the reference: the core rule, the owed-test decision, the 15 non-negotiables, the tier and validity rules with their checker-bound clauses, the output contract and the stop conditions. Lookup detail, catalogues and examples stay in or move to the references. Remove the second inline router in favour of `00-topic-map.md`, keeping each step's pointer trigger. Compress references 10 to 120 with their literals and the new hash |
| L3 | `alaa-workflow` | Collapse repeated pointers in the body; give each repeated task-tracking rule (heartbeat, guards, `--sandbox`, claim locks nothing) one owner inside `task-tracking.md`; shorten the rationale-only sections of `context-continuity.md` to the rules they justify; keep every cited heading, template token and version-provenance line |
| L4 | `alaa-code-intelligence-routing` and `alaa-low-noise` | Keep the operation card as the single statement of each operation and reduce references 10, 40 and 45 to what the card does not say; separate provenance from run-time rules in both source maps; compress the low-noise body and patterns file |
| L5 | `alaa-cc-orchestrator` and `alaa-codex-orchestrator`, one lane, mirrored | Compress `SKILL.md`, the references, the three contract assets, `profile-wrappers.json` descriptions and bindings, and the shared boilerplate blocks in every hand-written agent, with literals in both checkers; merge the overlap between `SKILL.md` stop conditions and `Final success criteria`; drop the history narrative in `agent-catalog.md` that the grants checker docstring already holds; re-render with `render_agents.py --write`; bump `VERSION` in both packs; add one changelog entry per pack |

Lane mechanics: each lane works in its own Git worktree on a lane branch from the latest commit
of `work/core-skills-compression`. The lead merges a lane into that integration branch with
`git merge --no-ff` only after the lane's gates pass in its worktree with the current
integration branch merged in, then removes the worktree and deletes the lane branch. `main`
and the installed agents stay consistent with each other throughout, because nothing reaches
`main` before Phase 4. Role, model and effort per lane are allocated at dispatch through
`alaa-cc-orchestrator references/routing-matrix.md`; instruction rewriting is a judgment lane,
not a mechanical one.

### Phase 2 — Cross-skill ownership (lead, sequential)

One commit per rule family, each with the literals it touches in every checker:

- orchestrator pair versus `alaa-workflow`: lane commits and checkpoints, plan header fields,
  `REVIEW_PENDING` closure, one writer per file;
- orchestrator pair versus `alaa-prompting-guide`: the alias-only model parameter, invocation
  effort precedence, the advisor pairing, the concurrency-limit error;
- orchestrator pair versus `alaa-testing-strategy`: tier rows and the fresh exhaustive run;
- orchestrator pair and `alaa-workflow` versus `alaa-low-noise`: return shape and the watchdog
  sentence;
- orchestrator pair versus `alaa-code-intelligence-routing`: grant scoping text in the catalog;
- `alaa-workflow` versus `alaa-testing-strategy`: never weaken an assertion.

The owner keeps the rule. The other site keeps a triggered pointer. Where a checker requires
the sentence at both sites, the pointer sentence becomes the new literal at the non-owner site.
Each such rule-to-pointer literal is listed in the report and enters the Phase 4 review. A rule
restated inside an agent file or a contract asset stays there in compressed form, because a
subagent does not load the owning reference.
The three disagreements from Phase 0 are corrected here from the fetched source.

### Phase 3 — Behaviour improvements and the contract file (lead)

1. Walk the carry-over table over the seven skills and the agent files: stale fact, standing
   delegation, absolute approval rule, thinking control in prose, token budget in text, hard
   style limit, expired caution. Known candidates from exploration: "Keep the whole report under
   40 lines" in the contracts (hard style limit, becomes a default with its exception);
   absolute "never" lines in lead-session text on actions the lead keeps through approval; the
   "legacy loading path" notes whose stated reason may have expired; the stale version line in
   codex `README-fa.md`.
2. Trim the seven descriptions to what triggers and what excludes, inside the 975-character
   target, keeping every negative and named alternative.
3. Compress `60-skill-authoring.md` itself, including the compression contract, last.
4. Re-render both packs if a contract or agent changed.

### Phase 4 — Final gate, review, install, report (lead)

1. Run every gate once on the final tree of the integration branch. Compare the clause counts
   with the baseline.
2. One `alaa-instruction-reviewer` dispatch. That role has only Read, Glob and Grep, so the
   lead first writes a review file to the artifacts directory with the before and after text
   of: authority and safety sections, the floors, the stop conditions, the three contract
   assets, every checker literal change and every rule-to-pointer literal. Apply blocker and
   major findings; record nits. No confirmation pass.
3. Re-run only the gates whose inputs step 2 changed.
4. Write `artifacts/core-skills-compression-20261116/report.md`: before and after words per
   load class per skill, every class 2 move with its reason, every class 3 change with its
   source row, the re-review and re-test rule proposals, gate results, open items. Add its row
   to `outputs/README.md`. Commit.
5. Merge `work/core-skills-compression` into `main` with `git merge --no-ff`, under the
   approval of this plan. Remove the integration worktree and delete the branch.
6. Install immediately after the merge, under the owner's authorization of 2026-11-16, limited
   to managed agent files in `~/.claude/agents` and `~/.codex/agents`: follow
   `install-skills.md` and `docs/install-skills/50-rule-writer.md`; run `validate_pack.py` and
   `check_agent_grants.py` before the copy; compare the SHA-256 of each installed file with
   `assets/manifest.json`; move any retired managed role out of the discovery directory. No
   other setting or agent changes. Append the install result to the report.
7. Close the Beads tasks with verdict, commit and evidence address. Move any `__pycache__`
   created by the gates into `_to_delete/`.

## Out of scope

- Any checker logic change, clause deletion, role roster change, or model and effort policy change.
- The other skills under `skills/sohrab/`, apart from a pointer that must follow a moved rule.
- `vendor/`, MCP, hook and CodeGraph configuration, push, tag and any remote sync.
- Fixtures, self-tests and before-and-after agent comparison runs.

## Verification

From the repository root, each exit `0` clean, `1` findings, `2` could not run; either nonzero
blocks completion:

- `python3 scripts/validate_sohrab_skill_pack.py`
- `python3 scripts/check_skill_index.py`
- `python3 scripts/check_fleet_references.py`
- `python3 scripts/check_lifecycle_contract.py`

From the named skill directory:

- `alaa-testing-strategy`: `python3 scripts/check_execution_contracts.py`
- each orchestrator pack: `python3 scripts/render_agents.py --write`, then
  `python3 scripts/render_agents.py --check`, `python3 scripts/validate_pack.py`,
  `python3 scripts/check_agent_contracts.py`, `python3 scripts/check_agent_grants.py`
- `alaa-prompting-guide`: `python3 scripts/check_rule_writer_grants.py`,
  `python3 scripts/check_claude_model_policy.py`,
  `python3 scripts/check_codex_model_policy.py --agent-root assets/rule-writer/codex`

Static evidence beyond the gates: every retired file present in `_to_delete/` at its original
size; every externally cited heading still present (one grep per heading in the list above);
`git status` clean after the last commit; installed agent hashes equal to the manifest.

These gates prove structure and source agreement. They do not prove live agent behaviour, and
the report says so.

## Appendix A — Headings cited from outside their skill (keep verbatim)

| File | Heading | Cited from |
|---|---|---|
| `alaa-workflow references/task-tracking.md` | `## Select before tracking-dependent work` | root `AGENTS.md`; `alaa-repo-docs` |
| same | `## Agent identity and ownership` | root `AGENTS.md`; both packs' `delegation-prompts.md` and `check_agent_contracts.py` |
| same | `## Beads capabilities in use`, `## Close reason`, `## Acceptance and evidence by level` | root `AGENTS.md` |
| same | `## Issue fields`, `## Outage and uncertain writes` | `alaa-memory-os/SKILL.md`; `alaa-repo-docs` |
| `alaa-workflow references/context-continuity.md` | `## Task resume and phase resume`, `## Cross-PC handoff record` | root `AGENTS.md` |
| `alaa-workflow references/workspace-and-integration.md` | `## Lane branches and commits` | both packs' `SKILL.md`, `verification-and-gates.md`, implementation contract, about 27 agent files, both `check_agent_contracts.py` |
| same | `## Before the first write`, `## The integration handshake` | both packs' `verification-and-gates.md` |
| `alaa-workflow references/review-mode.md` | `## Finding triage` | both packs' `verification-and-gates.md`, `delegation-prompts.md`, two delegation prompt files |
| `alaa-workflow references/companion-routing.md` | `## Mandatory Ponytail binding` | both packs' `SKILL.md`, `delegation-prompts.md`, `30-implementation.md` |
| `alaa-testing-strategy references/100-test-execution.md` | *Prepare the check list*, *Collect, repair, retest* | `alaa-laravel-upgrade-all-packages` |
| `alaa-testing-strategy/SKILL.md` | the three tier headings `Scope tiers…`, `A result stays valid…`, `A failing tier is classified…` | `100-test-execution.md:7`; checker lines 38 to 40 |
| `alaa-testing-strategy references/90-test-economy.md` | `## Existing tests on a touched topic` | checker line 210 |
| `alaa-code-intelligence-routing/SKILL.md` | `Operation card` | 38 agent files, three codex contract assets, cc `profile-wrappers.json` |
| `alaa-low-noise references/workflow-integration.md` | `Delegated lanes` | both packs' `delegation-prompts.md` |
| `alaa-prompting-guide references/41-claude-code-runtime-features.md` | `Native Advisor` | cc `model-effort-policy.md` |
| each pack's `SKILL.md` | `## Admission`, `Final report`; `routing-matrix.md` `## Batch allocation`, `## All-role task allocation` | the pack's `check_agent_contracts.py`; `check_lifecycle_contract.py` |

Headings cited only inside their own skill may change when the citing line changes in the same
commit: workflow `## Shared-file ownership…`, `## Record the tested state`, `## What not to
write`, `## Delegate selectively`, `## Plan kinds and approval`; testing *Setup once*, *Whether
a test is owed*, *Reachable failure*, *Owned by another skill*, *Anti-patterns*, *No shipped
surface is exempt*.

File names cited from other skills and fixed: testing references 10, 20, 40, 70, 80, 100, 110,
120; prompting-guide references 06, 11, 41, 50, 60, 70, 80, 90 and both policy JSON assets;
code-intelligence `80-agent-scoping.md`.

## Appendix B — Sentences bound by a checker in another skill

Phase 1 lanes leave these verbatim. Phase 2 may reword one together with its literal.

`COLLECTION_SEAMS` in both packs' `check_agent_contracts.py`, required in workflow files:

| Workflow file | Required clause |
|---|---|
| `SKILL.md` | "Record phase test-collection, repair/retest and review barriers" |
| `references/artifact-lifecycle.md` | "Record each phase's post-reconciliation test collection, combined repair/retest and declared review barriers"; "Workflow records barriers without redefining them" |
| `assets/plan-template.md` | "Phase collection, repair/retest and review barriers, owners and resume evidence" |
| `assets/phase-template.md` | "Collection/repair/retest barrier and evidence owner" |
| `references/phase-prompts.md` | "Carry the plan's phase collection and repair/retest barriers and their evidence owner" |
| `assets/phase-prompts-template.md` | "Run only assigned focused or bounded task-owner checks"; "centralized phase collection, repair/retest barriers and any review…" |

`COLLECTION_CONTRADICTIONS` (cc lines 531 to 543) are forbidden in those files.

`alaa-testing-strategy/scripts/check_execution_contracts.py` binds, outside its own skill:

- `workspace` (lines 211 to 230): 17 clauses and 2 file names in
  `alaa-workflow references/workspace-and-integration.md`, now at lines 9, 31, 37 to 41 and 55;
- `continuity` (line 231): 2 clauses in `alaa-workflow references/context-continuity.md`, line 128;
- `cc_` and `codex_` keys (lines 425 to 432): `/alaa-testing-strategy` and the three reference
  paths in each pack's `SKILL.md` and `verification-and-gates.md`; the 110 path in
  `resource-policy.md`; the 120 path in `failure-taxonomy.md`;
- `NORMATIVE_DUPLICATES` and `CONTRADICTIONS`: forbidden in seven files per pack and in the
  workflow files it loads.

`validate_workflow_files.py` requires "verify BOTH effective model and effort" in
`assets/phase-prompts-template.md`. `check_lifecycle_contract.py` allows the four state names
only in `workspace-and-integration.md`, workflow `SKILL.md` and each pack's `Final report`.
`check_agent_grants.py` requires `alaa-code-intelligence-routing` in implementer preloads.
`check_rule_writer_grants.py` requires both rule-writer wrapper bodies to equal `contract.md`
and bans model names in it. Each pack's `validate_pack.py` forbids the other runtime's vendor
and model names outside `CHANGELOG.md`.

## Appendix C — Keep-list for `41` and `11` (L1 does not cut these)

Facts that another skill cites or that Phase 2 will point to:

- `41`: the alias-only model parameter of the Agent tool; invocation effort and its precedence,
  with the version it dates from; the advisor pair table including the Fable 5.2 row; the
  concurrency limit values, the refusal at the limit and its error text; Workflow-run limits;
  fallback and safeguard disclosure; the `Native Advisor` section; the surface preflight and
  rejected-command procedure; the managed task-selected authority roles section.
- `11`: pin precedence and sandbox rules for subagents; the rejected tool input or patch
  context procedure; the `.git` read-only fact the codex gates file cites; the
  `project_doc_max_bytes` rule once Phase 0 resolves it; the managed task-selected authority
  roles section; the facts cited by codex `SKILL.md:68` and codex `model-effort-policy.md:30`.
- Both: every dated source line beside a kept fact.

Before cutting a paragraph of either file, L1 greps the other six skills and the agent files
for its key term. A hit keeps the paragraph.

## Addendum, 2026-11-17 — second pass (owner decision)

First-pass results: `alaa-workflow` 3.3 percent, `alaa-code-intelligence-routing` 3 percent,
`alaa-low-noise` 9 percent, `alaa-testing-strategy` 15 percent, orchestrator `SKILL.md` and
references about 4 percent. The lanes removed duplicates and reworded almost nothing.

The owner then decided, through two direct questions:

1. Run a second pass that rewrites every sentence and prunes rules under six stated criteria
   (default behaviour, itinerary, ceremony, restated platform fact, ownership noise, repeated
   disclaimer). A checker clause is deleted together with a pruned sentence. Each pruned rule
   goes in a ledger so the owner can restore it. Floors, authority limits, security rules and
   stop conditions are never pruned. This supersedes "no clause is deleted" and the
   clause-count comparison in this plan: a lower count is valid when the ledger accounts for it.
2. Fable 5.2 writes every second-pass lane (explicit owner model selection).

`lane-brief-2.md` in this directory is the controlling brief. The second pass also performs the
cross-skill ownership work of Phase 2 and the three corrections from `freshness.md`. Phase 3
keeps the carry-over walk, the descriptions and `60-skill-authoring.md`. Phase 4 is unchanged.
