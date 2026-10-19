# Workflow Plan - skill-pack-review-verification

- Task ID: `20261018-134259_skill-pack-review-verification`
- Mode: `plan`
- Profile: `resumable`
- Task store: `beads`
- Task binding: AGENTS.md#beads
- Status: complete
- Created: `2026-10-18T13:42:59Z`
- Parent plan: not created
- Prompt pack: not created
- Checkpoint: `docs/agents/20261018-134259_skill-pack-review-verification-state.md`
- Machine state: not created
- Base branch and commit: `main` at `1a0799de7` (worktree clean at start)
- Work branch: `main` (no commit authorized)
- Worktree: none

## Summary and Outcome

- Current repository truth: `artifacts/skill-pack-review-20261018/` holds three unverified review files (01 contradictions and overlaps, 02 optimization, 03 new-skill proposals) produced by a Haiku 5.5 agent. Most items are tagged `[R]` (reviewer-reported, never re-read).
- Outcome: the same three files, rewritten. False items deleted. Partly true items corrected. Extra evidence added in the existing item template. Each surviving item ends with a `sonnet Recommendation:` box. Numbering stays clean.
- Strategy: read-only verification lanes check every item against current sources and return a verdict with `file:line` evidence. The parent applies verdicts and writes the three files.

## Scope

- In scope: the three files under `artifacts/skill-pack-review-20261018/`; this plan and its checkpoint.
- Out of scope: any edit under `skills/sohrab/`, `vendor/`, or global rules; fixing the findings themselves; commit or push.
- Constraints and assumptions: files are written in English (repository rule); no emoji; no machine-specific paths; no frozen volatile facts. The reply to the user is Persian. A `[V]` tag from the Haiku agent is a lead until re-read. Chat-evidence counts in file 03 depend on local transcripts that may not be re-checkable; mark them unverified rather than false.

## Handoff Package

Knowledge held only in the current agent's head disappears on compaction. Fill a field when knowledge is learned, not on a schedule; leave unused fields empty. Field semantics are in the skill's `alaa-workflow references/context-continuity.md`, not in this repository.

- Confirmed facts (verified, each with how it was verified): Beads workspace matches the binding (`bd where` returned the expected hub). The user decided (scope: this engagement) that transcript counts need no re-check, only the reasoning and the conclusions drawn from skill references. Issues `alaa-jjd`, `alaa-dc6`, `alaa-37s`, `alaa-kzj` exist with blocking edges 37s -> jjd, 37s -> dc6, kzj -> 37s.
- Open assumptions (believed but unverified, each with what would verify it): the gateway timeout status (file 01 A8), tusd `StopUpload` from post-receive (A27) and whether a client Sentry name registry exists (03 N2) are not verifiable in this repository.
- Ruled out (approach, reason, evidence): re-verifying transcript counts from the first draft; the user said only reasoning and conclusions from skill references matter. Draft items C-12, N-8, M1-25, O-04 and sub-claims C-43(a), C-44(d) were false or not defects and were removed.
- Read first on resume (ordered exact paths): this plan; its checkpoint; `artifacts/skill-pack-review-20261018/01-contradictions-and-overlaps.md`; `.../02-optimization.md`; `.../03-new-skill-proposals.md`; lane verdict files under `artifacts/skill-pack-review-20261018/verification/` when present.
- Environment notes (command shapes that work here, and ones that look right but fail): run each `bd` command alone, no chaining. Bash tool works for `bd` and `python`.
- Traps (looks correct, is not): file 01 counts "[V]" as parent-verified, but the parent was an agent that may not have re-read; treat every tag as a lead. Line numbers drift after edits such as commit `4d5f295aa`; verify by content, not by line number alone.

## Skill Bindings

| Skill | Source | Load before | When | If unavailable |
|---|---|---|---|---|
| alaa-workflow | skills/sohrab/alaa-workflow/SKILL.md | planning | always | stop |
| alaa-prompting-guide | skills/sohrab/alaa-prompting-guide/SKILL.md | rewriting any instruction-like text or stating model/effort facts | when a Recommendation touches model or effort | report the gap |
| alaa-repo-docs | skills/sohrab/alaa-repo-docs/SKILL.md | writing the final files | only if a file needs doc-structure judgment | proceed with repository rules |

## Ordered Work

### Phase 1 - Verify every item

- Status: complete
- Depends on: none
- Reasoning and selection reason: independent read-only checks across many skills; no shared state; verdicts are evidence for the rewrite.
- Settled/open decisions and invariants: verdict vocabulary is CONFIRMED, PARTIAL (true but wrong detail), FALSE, UNVERIFIABLE. Verify by content, not by line number alone. Lanes write nothing under `skills/`.
- Risk and required observers: low risk (read-only). The parent spot-checks at least three CONFIRMED and every FALSE verdict before using it.
- Owned scope: lane reports only, returned in the dispatch result (parent saves them under `artifacts/skill-pack-review-20261018/verification/`).
- Excluded from this phase: any edit to the skill pack.
- Required skills: alaa-workflow
- Work:
  - Issue: alaa-jjd [skills: inherit]
  - Issue: alaa-dc6 [skills: inherit]
- Acceptance criteria: every C-, M1-, M2-, O-, N- item and every row of the verification table has a verdict with `file:line` evidence.
- Validation commands: parent re-reads cited lines for all FALSE and PARTIAL verdicts and a sample of CONFIRMED.
- Evidence observed: eight lane reports saved as `artifacts/skill-pack-review-20261018/verification/L1..L8*.md`. Parent re-read: workflow `SKILL.md:71` (draft item C-12 false), `service-runtime-kit-governance/SKILL.md:55`, `alaa-codex-runtime-ops/references/40-project-fallbacks.md:5-7`, partitioned-FK quote absent by grep, `drop_newest` only in the vector skill, `should not implement` at `alaa-cc-orchestrator/SKILL.md:39`, `phase-prompts.md:29` and `workspace-and-integration.md:8,15` (draft N-8 false).
- Snapshot: HEAD 1a0799de71254427973f1253d80b846fea9acf10; SHA-256 95fe19f59d882b033e1c64feb5f7446fff1aade6f3408c42936078bdda92a472; paths artifacts/skill-pack-review-20261018/verification/*.md (no commit)

### Phase 2 - Rewrite, validate and report

- Status: complete
- Depends on: Phase 1
- Reasoning and selection reason: single writer, shared context with the verdicts.
- Settled/open decisions and invariants: keep each file's name and the item template. Add a `sonnet Recommendation:` box under every surviving item. Delete false items and renumber. Add evidence the lanes found.
- Risk and required observers: low. Observer: workflow validator plus an independent re-read of a sample of rewritten items.
- Owned scope: the three files under `artifacts/skill-pack-review-20261018/` and the verification notes folder.
- Excluded from this phase: fixing any finding in the pack.
- Required skills: alaa-workflow
- Work:
  - Issue: alaa-37s [skills: inherit]
  - Issue: alaa-kzj [skills: inherit]
  - Issue: alaa-4s0 [skills: inherit]
- Acceptance criteria: required behavior and evidence agree.
- Validation commands: `python C:/Users/Alaa/.claude/skills/alaa-workflow/scripts/validate_workflow_files.py --plan docs/_agent_plans/20261018-134259_skill-pack-review-verification.md`; grep the new files for `D:\` and for emoji.
- Evidence observed: three files rewritten (79 + 27 + 8 items, each with a `sonnet Recommendation` box). Grep for machine paths returned nothing; emoji scan 0 in all files. Follow-up on request (alaa-4s0): added cadence findings (file 01 A49-A51, file 02 section P1-P7, file 03 N6 revised); snapshot digest refreshed. Final curation gate: no admitted durable candidates; one engagement-local fact parked in the handoff package.
- Snapshot: HEAD 1a0799de71254427973f1253d80b846fea9acf10; SHA-256 527aa4b7b708b28a58fc6377ecc0065e55a31ac5bc3d35411dee700693848758; paths artifacts/skill-pack-review-20261018/*.md and verification/*.md (no commit)

## Task Allocation

Lane allocation is by the parent for read-only verification. No lane edits files. Lanes use `alaa-explorer` (read-only) with explicit `sonnet` selection, because the work is bounded claim-checking against named files.

| Task/scope/complexity | Role authority | Priority/reason | Model | Effort | Selection/admission evidence and source date | Invocation/requested/effective controls | Availability/limits |
|---|---|---|---|---|---|---|---|
| Lanes L1-L8: claim verification, bounded semantic judgment with named files | `alaa-explorer` (read-only) | priority 2; independent claims | sonnet | runtime default | user asked for a Sonnet recommendation; effort not set by parent | Agent tool, `model: sonnet`, effort omitted | available in this session |

## Delegation

- Keep shared-context work in the main conversation.
- Independent lane ownership, if admitted: L1 C-01..C-09; L2 C-10..C-19; L3 C-20..C-34; L4 C-35..C-44 and M2-01..M2-05; L5 M1-01..M1-16; L6 M1-17..M1-32; L7 file 02 O-01..O-28; L8 file 03 table and N-1..N-9.
- Dependency edges and ready sets: Beads owns issue dependencies and readiness; the plan owns phase barriers and shared-resource conflicts.
- Disjoint writes and shared-resource conflicts: no lane writes. The parent alone writes the three files.
- Integration barriers and parallel/serialized rationale: lanes run in parallel; Phase 2 starts after all verdicts return.
- Consolidated tasks/checks and preserved outcome/evidence mappings: all eight lanes map to issues alaa-jjd (L1-L6) and alaa-dc6 (L7-L8).
- Reusable evidence and invalidation conditions: verdicts stay valid until a file under `skills/sohrab/` changes.
- Dispatches assume zero shared context: copy the relevant handoff-package facts into the dispatch text rather than referring to this conversation.
- Lanes report findings in the return; this plan's owner records the validated snapshot and handles any explicitly authorized commit.

## Execution Position

- Position owner: `docs/agents/20261018-134259_skill-pack-review-verification-state.md` (current phase, blockers, next action).
