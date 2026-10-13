# Workflow Plan - beads workflow memory ownership

- Task ID: `20261013-140219_beads-workflow-memory-ownership`
- Mode: `plan`
- Profile: `resumable`
- Task store: `local`
- Task binding: not applicable
- Status: completed
- Created: `2026-10-13T14:02:19Z`
- Parent plan: not created
- Prompt pack: not created
- Checkpoint: `docs/agents/20261013-140219_beads-workflow-memory-ownership-state.md`
- Machine state: not created
- Base branch and commit: `main` at `daaa3694c744667975d187bcdb33eaae75d9e7fd`
- Work branch: `main` (current checkout; no commit authority)
- Worktree: none

## Summary and Outcome

- Current repository truth: `alaa-workflow` already supports a `beads` task store (`references/task-tracking.md`), but it keeps existing task acceptance in the plan, records issue-only evidence and knowledge together in issue notes, has no issue-field contract, close-reason shape, capability list, cross-project delivery rule or follow-up provenance rule, and does not define `bd remember`. `alaa-memory-os` defines no boundary between Hindsight, `bd remember` and issue notes. The client binding (`client/AGENTS.md`, read-only) says "never use `bd remember`", which contradicts owner decision 5.
- Outcome: the eleven owner decisions dated 2026-10-13 (recorded in the user's request; summarized in the trace matrix below) are each written exactly once in their owning file, no contradicting text remains in either skill, and all declared gates for the changed skills pass or are reported with their pre-existing cause.
- Strategy: one research task closes the last unverified `bd` behavior; two disjoint implementation lanes (workflow, memory-os) write to a fixed trace matrix and fixed cross-pointer anchors; an independent verifier runs the gates; `alaa-instruction-reviewer` gives the independent verdict.

## Scope

- In scope: `skills/sohrab/alaa-workflow/SKILL.md` (trigger and reference lines only); `skills/sohrab/alaa-workflow/references/task-tracking.md` (task and Beads policy); `skills/sohrab/alaa-workflow/references/context-continuity.md` (task-resume versus phase-resume boundary, cross-PC handoff record); any other `alaa-workflow/references/*.md` only to remove a contradiction; `skills/sohrab/alaa-memory-os/` (`SKILL.md`, `references/skill-boundaries.md`, and other files only to remove a contradiction).
- Out of scope: the upstream Beads skill; `alaa-repo-docs`; installation into `~/.claude/skills`; commit, push, `bd dolt push`/`pull`; any write to Beads, Hindsight or `bd remember`; `client` and `alaa-task-hub` files (read-only); `alaa-workflow` scripts, tests and assets unless a gate proves a contradiction there (then stop and ask); the pre-existing dirty paths of the markdown-link-checker task (`alaa-repo-docs`, `alaa-docker-production`, its plan and checkpoint).
- Constraints and assumptions: repository `AGENTS.md` and `skills/sohrab/AGENTS.md` bind; English in every file; one call form `/name`; no machine path; no emoji; each rule once; instruction text drafted then compressed under `alaa-prompting-guide references/60-skill-authoring.md`; every `bd` behavior claim verified from installed `bd` 1.3.1 help or v1.3.1 source; growth only for the new capability (Beads field/evidence policy, hub-reminder boundary).

## Decision trace matrix (acceptance map)

Each row is written once, in the named owner. Every other file points to that owner.

| # | Decision | Owner file and section (target) | Pointers only from |
|---|---|---|---|
| D1 | Information ownership map | `alaa-workflow references/task-tracking.md` `## Where task information lives` (task rows; durable-knowledge rows point to D10) | `context-continuity.md` |
| D2 | Acceptance and evidence by level; plan links, never copies; issue-only keeps all in the issue; no automatic migration | `task-tracking.md` `## Acceptance and evidence by level` | `context-continuity.md`, `workspace-and-integration.md`, `SKILL.md` |
| D3 | Issue field contract (`description`, `spec_id`, `acceptance`, `design`, `notes`, comments) | `task-tracking.md` `## Issue fields` | `context-continuity.md` |
| D4 | Close reason: verdict + reviewed version (commit or worktree snapshot hash) + evidence address; optional numbers labelled "at close" | `task-tracking.md` `## Close reason` | `workspace-and-integration.md` |
| D5 | `bd remember` allowed for shared hub reminders only, with source, scope and maintainer; forbidden contents; empty is correct; reason `bd prime` injects unfiltered | `alaa-memory-os SKILL.md` `## Beads hub reminders and issue notes` | `task-tracking.md` D1 row, `skill-boundaries.md` |
| D6 | Capabilities in use: `--spec-id`, types `decision`/`spike`, `discovered-from` for provenance (non-blocking; real prerequisites recorded separately), local-only `--if-assignee`/`--if-status` not combined with `--claim`, `bd lint`, `bd stale`, `bd ready --explain`; no formula, molecule or automatic gate | `task-tracking.md` `## Beads capabilities in use` | none |
| D7 | Cross-project work: a delivery task ("output available to consumer"); consumer depends on it | `task-tracking.md` `## Cross-project delivery` | none |
| D8 | Two PCs: handoff records responsible device, sync state, code and evidence availability; Dolt push/pull need explicit authorization | record fields: `context-continuity.md` handoff section; authorization: `task-tracking.md` existing cross-PC paragraph | each points to the other half |
| D9 | Thin decision wrapper: tracking, status, dependencies, ready/blocked, discovered work, task continuation context and new-task local evidence go to Beads; plan need/process size, goal/phases, skill/lane choice, conflict prevention, evidence validity, phase acceptance, four completion states, resume, handoff and lesson selection stay in the skill; no parallel Markdown tracker | `task-tracking.md` `## Division of labor` | `SKILL.md` trigger/reference line |
| D10 | Boundary among Hindsight, `bd remember` and issue notes | `alaa-memory-os SKILL.md` `## Beads hub reminders and issue notes` (same section as D5) | `skill-boundaries.md` row, `task-tracking.md` D1 row |
| D11 | Three lessons as rules: no repeated evidence; plan path not only in prose; follow-up linked to origin | `task-tracking.md`, each co-located with its rule: (a) with D2 link-not-copy, (b) with D3 `spec_id`, (c) with D6 `discovered-from` — pending open decision Q2 | none |

## Handoff Package

Knowledge held only in the current agent's head disappears on compaction. Fill a field when knowledge is learned, not on a schedule; leave unused fields empty. Field semantics are in the skill's `alaa-workflow references/context-continuity.md`, not in this repository.

- Confirmed facts (verified, each with how it was verified):
  - Installed `bd` is `1.3.1 (c1c4b642a)` — `bd --version`.
  - `bd create`/`bd update` accept `--spec-id`, `--acceptance`, `--design`, `--notes`, `--append-notes`; type list includes `decision` and `spike` — `bd create --help`, `bd update --help`.
  - `--if-assignee` and `--if-status` write nothing on mismatch, exit 13, require a field update, and "cannot combine with --claim" — `bd update --help`.
  - `bd dep add -t` accepts `discovered-from`; an untyped edge is `blocks` and "excludes the dependent from bd ready" — `bd dep add --help`. External references `external:<project>:<capability>` block until shipped — same help.
  - `bd remember` takes only `--key`; no label or project filter. `bd prime` appends memories, offers `--no-memories`, `--memories-only`, `--max-memories`, `--max-memory-chars`; no label filter — `bd remember --help`, `bd prime --help`.
  - `bd close` takes `--reason`/`--reason-file` — `bd close --help`. `bd lint` checks recommended sections per type; `bd stale --days` default 30; `bd ready --explain` shows dependency reasoning — respective `--help`.
  - Review correction: `bd gate --help` in 1.3.1 lists `human`, `timer`, `gh:run`, `gh:pr` and `bead`. The workflow's non-adoption policy is independent of those capabilities.
  - Client binding forbids `bd remember` (`client/AGENTS.md` line 51); hub `AGENTS.md` (generated by `bd setup codex`) says to keep persistent project memory via `bd remember`. Both contradict D5 and are out of scope — `grep` on both files.
  - Baseline on HEAD `daaa3694c` with the pre-existing dirty tree: `validate_sohrab_skill_pack.py` exit 0, its `--self-test` exit 2 (64 pass, 1 BLOCKED: fixture `scripts/fixtures/validator/red-empty-pack/skills/sohrab` missing); `check_skill_index.py`, `check_fleet_references.py`, `check_lifecycle_contract.py` exit 0 with self-tests exit 0; `python -m unittest skills/sohrab/alaa-workflow/tests/test_workflow_files.py` Ran 106, OK; `pwsh skills/sohrab/alaa-memory-os/test/run-tests.ps1` exit 1 (3 checker self-tests fail case "unresolvable vault is BLOCKED, not a finding: expected 2, observed 1"; memory-os files are unmodified on HEAD).
  - `skills/sohrab/alaa-memory-os/SHA256SUMS` is already stale on HEAD (`sha256sum -c` fails for SKILL.md and others) and no script consumes it — repository `grep`.
  - `validate_workflow_files.py` and the workflow tests pin no reference-file wording — `grep` on both.
- Open assumptions (believed but unverified, each with what would verify it): none.
  - Beads v1.3.1 (`gastownhall/beads`, tag commit `c1c4b642a`): `DependencyType.AffectsReadyWork()` returns true only for blocks, parent-child, conditional-blocks and waits-for, so `discovered-from` does not affect ready work — `internal/types/types.go` lines 1333-1337 at tag v1.3.1 (T1, `alaa-researcher`). The GetReadyWork query call site was not opened; the predicate's doc comment names it the ready-work predicate.
  - `bd prime` loads memories with an empty `memoryops.ListRequest{}` (`cmd/bd/prime.go` line 469 at v1.3.1); only `--max-memories`/`--max-memory-chars` caps apply, so every memory in the bound database is injected regardless of project label (T1).
- Ruled out (approach, reason, evidence):
  - Adding a ninth `alaa-memory-os` reference for the hub-reminder boundary: it crosses the router threshold and would force a `00-topic-map.md` move (`skills/sohrab/AGENTS.md` Structure). Use a short `SKILL.md` section instead.
  - Restating the D11 lessons as separate rules beside D2/D3/D6: violates "state every instruction exactly once".
  - `alaa-architecture-critic`: the design decisions are owner-final; a critic would relitigate settled ground.
- Read first on resume (ordered exact paths): this plan's trace matrix; `skills/sohrab/alaa-workflow/references/task-tracking.md`; `skills/sohrab/alaa-workflow/references/context-continuity.md`; `skills/sohrab/alaa-memory-os/SKILL.md`.
- Environment notes (command shapes that work here, and ones that look right but fail):
  - Run `bd ... --help` from a directory with no `.beads` to read help without touching a workspace.
  - A `find /` over the Windows mount exceeded the 120 s timeout; search a named directory instead.
  - Memory-os tests: `pwsh -NoProfile -File skills/sohrab/alaa-memory-os/test/run-tests.ps1`.
- Traps (looks correct, is not):
  - The installed `~/.claude/skills/alaa-workflow/SKILL.md` matches the repository copy today; edits here do not reach the installed copy (installation is out of scope).
  - The upstream hub `AGENTS.md` tells agents to store project memory in `bd remember`; it is generated guidance, not the owner decision.

## Skill Bindings

| Skill | Source | Load before | When | If unavailable |
|---|---|---|---|---|
| `alaa-prompting-guide` | `skills/sohrab/alaa-prompting-guide/SKILL.md` | Phase 2 | drafting and compressing instruction text (`references/60-skill-authoring.md`) | block Phase 2 |
| `alaa-workflow` | `skills/sohrab/alaa-workflow/SKILL.md` | every phase | plan, checkpoint, evidence | block |
| `alaa-memory-os` | `skills/sohrab/alaa-memory-os/SKILL.md` | Phase 2 lane M | memory boundary wording (no store write) | block lane M |
| `alaa-low-noise` | `skills/sohrab/alaa-low-noise/SKILL.md` | every dispatch | bounded returns | continue with explicit bounds |
| `alaa-code-intelligence-routing` | `skills/sohrab/alaa-code-intelligence-routing/SKILL.md` | Phase 1 | evidence-surface choice | fall back to bounded `grep` and report |
| `alaa-extract-agent-lessons` | `skills/sohrab/alaa-extract-agent-lessons/SKILL.md` | Phase 3 final gate | curation outcome | record deferred |

## Ordered Work

### Phase 1 - Close bd evidence

- Status: completed
- Depends on: none
- Reasoning and selection reason: missing facts to retrieve; two readiness and injection behaviors shape D5/D6 wording.
- Settled/open decisions and invariants: read-only; no Beads workspace access; source tag v1.3.1 only.
- Risk and required observers: low; lead accepts the citation.
- Owned scope: none (read-only).
- Excluded from this phase: any file edit.
- Required skills: `alaa-low-noise`, `alaa-code-intelligence-routing`
- Work:
  - [x] T1: Verify from Beads v1.3.1 source whether `discovered-from` affects ready work and whether `bd prime` filters memories by label; return file:line citations. [depends: none] [skills: inherit]
- Acceptance criteria: both open assumptions become confirmed facts or corrected facts with source citations.
- Validation commands: none (citation review by lead).
- Evidence observed: T1 citations accepted by lead; both assumptions confirmed (see Confirmed facts).
- Snapshot: none; this phase changed no files.

### Phase 2 - Write decisions into owners

- Status: completed
- Depends on: Phase 1
- Reasoning and selection reason: bounded semantic judgment; decisions are settled, wording and contradiction removal need discretion under the compression contract.
- Settled/open decisions and invariants: the trace matrix fixes owner, section heading and pointer sites; lane W never edits `alaa-memory-os`, lane M never edits `alaa-workflow`; cross-pointers use the exact headings in the matrix; no file outside scope; no growth beyond the new capability.
- Risk and required observers: instruction change consumed by 12 projects; `alaa-instruction-reviewer` required.
- Owned scope: lane W — `alaa-workflow/SKILL.md`, `references/task-tracking.md`, `references/context-continuity.md`, and only for contradiction removal `references/workspace-and-integration.md`, `references/context-curation.md`, `references/artifact-lifecycle.md`. Lane M — `alaa-memory-os/SKILL.md`, `references/skill-boundaries.md`, and only for contradiction removal `references/knowledge-shape.md`.
- Excluded from this phase: scripts, tests, assets, `SHA256SUMS`, `agents/openai.yaml` unless the validator fails on it; every out-of-scope path above.
- Required skills: `alaa-prompting-guide`, `alaa-low-noise`
- Work:
  - [x] T2: Lane W — write D1, D2, D3, D4, D6, D7, D8 (authorization half), D9, D11 into `task-tracking.md`; D8 record fields and the task-resume versus phase-resume boundary into `context-continuity.md`; trigger/reference line in `SKILL.md`; remove contradictions (task-tracking line 24 "Existing task acceptance stays in its canonical plan section", context-continuity lines 37 and 71 issue-notes-own-evidence wording, workspace-and-integration line 19 phase-only evidence). Return changed paths and a per-decision line map. [depends: T1] [skills: alaa-prompting-guide, alaa-low-noise]
  - [x] T3: Lane M — write D5 and D10 into one `alaa-memory-os SKILL.md` section; add a `skill-boundaries.md` row pointing to Beads for task state; adjust the description only if a trigger is missing and the packaged length stays within budget. Return changed paths and a line map. [depends: T1] [skills: alaa-prompting-guide, alaa-memory-os, alaa-low-noise]
- Acceptance criteria: each matrix row appears once at its owner; each pointer site names the owner without restating it; no contradiction search hit remains (see Phase 3 commands); lane line maps cover D1–D11.
- Validation commands: lane-focused `python scripts/validate_sohrab_skill_pack.py` and `python scripts/check_fleet_references.py`.
- Evidence observed: lane W (T2) and lane M (T3) focused checks: `validate_sohrab_skill_pack.py` 0, `check_fleet_references.py` 0, `check_skill_index.py` 0, workflow unittest Ran 106 OK; memory-os `run-tests.ps1` 1 (pre-existing case only). Owner lines: task-tracking.md D9 13-15, D1 30-43, D2+D11a 46-55, D3 57-66, D11b 68, D4 70-72, D6+D11c 80-89, D7 91-93, D8 authorization 99; context-continuity.md task/phase resume 65-67, Q3 69, D8 record 71-73; alaa-memory-os SKILL.md D5+D10 section at 128. Lead confirmed every cross-pointer heading exists. Lane W moved pre-existing `skills/sohrab/alaa-workflow/tests/__pycache__` (dated 2026-09-25) to `_to_delete/20261013-pycache-laneW/tests-pycache/` (58633 bytes, `ls -la`). Unpinned by owner decisions and left unstated: `spec_id` separator (D3), project that holds the delivery task (D7).
- Snapshot: HEAD daaa3694c744667975d187bcdb33eaae75d9e7fd; SHA-256 ee00b1f83c7bd2237aaf23f0f8877ed170971e84398e7062accfb9c91560c903; paths skills/sohrab/alaa-memory-os/{SKILL.md,references/skill-boundaries.md} and skills/sohrab/alaa-workflow/{SKILL.md,references/artifact-lifecycle.md,references/context-continuity.md,references/context-curation.md,references/task-tracking.md,references/workspace-and-integration.md}; manifest: sorted per-file sha256sum lines, then sha256sum; observed 2026-10-13T14:20:20Z; diffstat 8 files +114/-19.

### Phase 3 - Verify, review, reconcile

- Status: completed
- Depends on: Phase 2
- Reasoning and selection reason: independent authority; execution and judgment separated from authors.
- Settled/open decisions and invariants: verifier only runs commands; reviewer only judges; findings return to the owning lane; at most two fix cycles.
- Risk and required observers: `alaa-verifier`, `alaa-instruction-reviewer`; `alaa-reviewer` only if a script, test or asset changed.
- Owned scope: none (lead records evidence in this plan).
- Excluded from this phase: product edits by the verifier or reviewer.
- Required skills: `alaa-low-noise`, `alaa-extract-agent-lessons`
- Work:
  - [x] T4: Run the gate set below on a frozen snapshot and record exit codes against the baseline. [depends: T2, T3] [skills: inherit]
  - [x] T5: Independent instruction review against the trace matrix: once-only placement, no contradiction, compression fidelity, `bd` claims cited. [depends: T2, T3] [skills: inherit]
  - [x] T6: Reconcile findings, rerun affected gates, run the final curation gate, record the four completion states and the commit suggestion. [depends: T4, T5] [skills: inherit]
- Acceptance criteria: every D1–D11 row verified once at its owner by the reviewer; gates match or improve on baseline with every nonzero exit attributed to its pre-existing cause; reviewer verdict recorded; final report lists files, gate results and commit suggestion.
- Validation commands:
  - `python scripts/validate_sohrab_skill_pack.py` and `--self-test`
  - `python scripts/check_skill_index.py` and `--self-test`
  - `python scripts/check_fleet_references.py` and `--self-test`
  - `python scripts/check_lifecycle_contract.py` and `--self-test`
  - `python -m unittest skills/sohrab/alaa-workflow/tests/test_workflow_files.py`
  - `pwsh -NoProfile -File skills/sohrab/alaa-memory-os/test/run-tests.ps1`
  - `python skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan docs/_agent_plans/20261013-140219_beads-workflow-memory-ownership.md`
  - contradiction search over both skills: `rg -n "never use .bd remember|Existing task acceptance stays|evidence once in the admitted plan|issue notes own execution position, validation evidence" skills/sohrab/alaa-workflow skills/sohrab/alaa-memory-os` must return no stale hit
  - move any new `__pycache__` into `_to_delete/<YYYYMMDD>-pycache/` and confirm with `ls -la`
- Evidence observed:
  - Review cycle: `alaa-instruction-reviewer` (requested Sonnet 5.5 high; effort not observable) round 1 CHANGES-REQUESTED (F1-F4 major, F5-F22 minor/nit); fix cycle 1 by both lanes; round 2 APPROVED-WITH-NITS (N1-N8); fix cycle 2; round 3 APPROVED-WITH-NITS. Residual nits: `task-tracking.md:51` admissible-path branch may have no listed path (nit A); `task-tracking.md:89` lint wording rests on installed `bd lint --help` ("missing recommended sections", observed by the lead). OWNER-DECISION open: F5 `spec_id` separator (`task-tracking.md:62`), F6 project hosting a delivery task (`task-tracking.md:94`); text invents neither. Lead rulings: F4 close reason holds a closed task's result, comments hold events; N2 trigger wording accepted; N6 accepted per `alaa-memory-os references/knowledge-shape.md:81`; F22 `SHA256SUMS` stale on HEAD, out of scope.
  - Final gates (`alaa-verifier`, requested Haiku 5.5 medium; effort not observable) on the snapshot below, digest unchanged before and after: `validate_sohrab_skill_pack.py` 0; `--self-test` 2 (64 pass, 1 BLOCKED `red-empty-pack`, baseline); `check_skill_index.py` 0 and `--self-test` 0 (19/0/0); `check_fleet_references.py` 0 and `--self-test` 0 (24/0/0); `check_lifecycle_contract.py` 0 and `--self-test` 0 (8/0/0); workflow unittest Ran 106 OK; memory-os `run-tests.ps1` 1 (2 passed, 3 failed, baseline); `validate_workflow_files.py --plan` this plan 0; contradiction and dual-form `grep` exit 1 (no hits); no new `__pycache__`. An earlier round's `validate_workflow_files.py` exit 1 (`plan.phase-snapshot`) was a plan-record format defect, repaired by the lead.
  - Final curation (`/alaa-extract-agent-lessons`): no admitted candidates; bd v1.3.1 facts live in their canonical owners; other signals were one-off or cheaply recoverable. Nothing published.
  - Cold-start test: a fresh agent reading this plan, the checkpoint and the three read-first files can name the finished state, the snapshot, the open owner decisions and the next safe action (owner decisions F5/F6, then commit on explicit authorization); no expensive rediscovery needed.
  - Goal-message items not applicable here: `pnpm lint:check`, `pnpm check:size`, constitution validator, Beads tasks, an AGENTS.md Beads section and `bd show` belong to another plan; this repository has no `package.json`, no `CONSTITUTION.md`, no Beads binding, and this plan forbids Beads writes. Reported BLOCKED.
- Snapshot: HEAD daaa3694c744667975d187bcdb33eaae75d9e7fd; SHA-256 a05af9984dd6c9a15650c5954fc98686f58d37772d46222afd705811f9e0bd22; paths skills/sohrab/alaa-workflow and skills/sohrab/alaa-memory-os (the 9 files from `git diff --name-only -- skills/sohrab/alaa-workflow skills/sohrab/alaa-memory-os`); manifest: sorted per-file sha256sum lines, then sha256sum; observed 2026-10-13T14:47:41Z (after closing reviewer nits A and B and applying owner decisions F5 and F6; final gate run clean against baseline, digest unchanged before and after; final instruction review APPROVED with no open finding).

## Task Allocation

After finalizing tasks, dependencies and consolidation, record the runtime orchestrator's all-role allocation.
In Codex, `/alaa-codex-orchestrator` owns `references/routing-matrix.md`.
In Claude Code, `/alaa-cc-orchestrator` owns `references/routing-matrix.md`.
Prompting-guide supplies capability/mechanics evidence; workflow stores decisions. Unresolved controls or availability block the affected dispatch. Material changes reassess only affected remaining tasks.

Execution profile: `standard` (two implementation lanes; not `hardened`: no production data, auth, tenancy, public contract or deployment topology).

| Task/scope/complexity | Role authority | Priority/reason | Model | Effort | Selection/admission evidence and source date | Invocation/requested/effective controls | Availability/limits |
|---|---|---|---|---|---|---|---|
| T1 source retrieval, two named questions, unnamed upstream files | `alaa-researcher` | balanced | Sonnet 5.5 | medium | Haiku rejected: scope is not a finite named file set and needs readiness-semantics interpretation; `alaa-prompting-guide references/90-model-selection.md` read 2026-10-13 | Agent tool `model: sonnet`, `effort: medium`; effective identity reported by the lane | available; WebFetch to GitHub required |
| T2 lane W, 6 files, bounded semantic wording with settled decisions | `alaa-implementer-sonnet-high` | balanced | Sonnet 5.5 | high | Haiku rejected: compression and contradiction removal need semantic discretion across interacting files; Opus rejected: no unresolved design decision (owner-final); same source/date | `model: sonnet`, `effort: high` | available |
| T3 lane M, 2–3 files, one new section | `alaa-implementer` | balanced | Sonnet 5.5 | medium | Haiku rejected: wording discretion under compression contract; smaller scope than T2 | `model: sonnet`, `effort: medium` | available |
| T4 exact command execution | `alaa-verifier` | balanced | Haiku 5.5 | medium | exact commands, no discretion | `model: haiku`, `effort: medium` | available |
| T5 instruction review, 11-row trace across two skills | `alaa-instruction-reviewer` | balanced | Sonnet 5.5 | high | cross-file contradiction and fidelity judgment; Opus not required (no coupled design) | `model: sonnet`, `effort: high` | available; Read/Glob/Grep only |
| T6 reconcile, curation, report | lead (this session) | balanced | Opus 5.5 | session setting | lead authored no diff | main session; effort not observable | — |

## Delegation

- Keep shared-context work in the main conversation.
- Independent lane ownership, if admitted: lane W (T2) and lane M (T3) run in parallel after T1.
- Dependency edges and ready sets: Local task prerequisites above own dependency edges; derive readiness before dispatch.
- Disjoint writes and shared-resource conflicts: lanes write disjoint skill directories; the only coupling is cross-pointer headings, fixed in the trace matrix; no shared fixtures or ports.
- Integration barriers and parallel/serialized rationale: Phase 3 starts only after both lanes return line maps; the verifier runs once on the combined snapshot.
- Consolidated tasks/checks and preserved outcome/evidence mappings: one verifier run covers both lanes; lane-focused checks are not repeated if inputs are unchanged.
- Reusable evidence and invalidation conditions: Phase 1 citations stay valid while the source tag is v1.3.1; baseline gate results stay valid while the dirty paths of the other task are unchanged.
- Dispatches assume zero shared context: copy the relevant handoff-package facts into the dispatch text rather than referring to this conversation.
- Lanes report changed paths; this plan's owner records the validated snapshot and handles any explicitly authorized commit.

## Settled Decisions (user, 2026-10-13)

- Q1: keep the `local` task store for repositories without a Beads binding; it owns task state only when Beads is not selected, so it is not a parallel tracker.
- Q2: co-locate the three D11 lessons with their D2/D3/D6 rules; each rule is written once.
- Q3: task-specific learned knowledge (ruled-out approach, trap) goes to the plan handoff package when a plan exists, otherwise to issue comments; issue notes hold position and next step only. Lane W writes this in `context-continuity.md`.
- Q4: pre-existing gate failures (validator `--self-test` BLOCKED fixture; memory-os checker self-tests) are reported with their pre-existing cause and excluded from acceptance, provided this change makes no result worse than baseline.
- Execution start: wait for the user's goal message before dispatching T1.
- F5 (2026-10-13): `spec_id` = repository name, a colon, then the repository-relative plan path (e.g. `skills:docs/_agent_plans/<stem>.md`).
- F6 (2026-10-13): a cross-project delivery task is created in the producer project and carries the producer's label; the consumer depends on it.

## Follow-ups (out of scope, not authorized)

- `client/AGENTS.md` Beads binding forbids `bd remember`; align with D5 in a client task.
- `alaa-task-hub/AGENTS.md` (generated by `bd setup codex`) says to keep project memory in `bd remember`; conflicts with D5.
- `alaa-memory-os/SHA256SUMS` is stale and has no consumer.

## Execution Position

- Position owner: `docs/agents/20261013-140219_beads-workflow-memory-ownership-state.md` (current phase, blockers, next action).
