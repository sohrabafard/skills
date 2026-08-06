# Workflow Plan - alaa-prompting-guide structural revision

- Task ID: `20260806-114753_alaa-prompting-guide-structural-revision`
- Mode: `plan`
- Profile: `resumable`
- Status: executing
- Created: `2026-08-06T11:47:53Z`
- Parent plan: not created
- Prompt pack: not created
- Checkpoint: `docs/agents/20260806-114753_alaa-prompting-guide-structural-revision-state.md`
- Machine state: not created
- Base branch and commit: `main` at `d3fa52cd`
- Work branch: `work/prompting-guide-restructure`
- Worktree: none

## Summary and Outcome

- Current repository truth: `skills/sohrab/alaa-prompting-guide` ships `SKILL.md` (49 lines) plus 14
  references totalling ~1600 lines. It carries no `references/00-topic-map.md` even though the pack
  rule in `skills/sohrab/AGENTS.md` requires one at 9 or more references. Five files state the
  delegation-polarity rule, four state the Opus-4.8 retirement, three state each model's effort
  starting point. Several files are framed as migration diffs against a superseded model generation.
- Outcome: the same skill, restructured so the always-loaded body is a contract plus one router
  pointer, every topic has exactly one owning reference reached by a pointer that names its
  triggering condition, no file narrates its own history, and the invocation rule is single-form.
  Two named new capabilities are added; see Scope.
- Strategy: fix the conventions in the routing and invocation lane first, then run three disjoint
  content lanes against those conventions in parallel, then validate with the pack's own checkers.

## Scope

- In scope: every file under `skills/sohrab/alaa-prompting-guide/`, including `agents/openai.yaml`.
- Out of scope: the other skills in the pack, `skills/sohrab/AGENTS.md`, and `scripts/`. The
  single-form call-site convention conflicts with the dual-form rule at `skills/sohrab/AGENTS.md`
  line 55 and with ~100 other skills' call sites; the user scoped this run to the owning skill and
  the pack-wide sweep is reported as a follow-up, not performed.
- Constraints and assumptions:
  - Two genuinely new capabilities justify any growth, and are named: the **draft-then-compress
    loop** (the first text written is a draft; the shipped text is its compressed rewrite) and the
    **reference-decomposition procedure** (split by topic, then write a pointer that states why and
    when to read each file).
  - Removals must pay for the additions. Target: total line count at or below the 1600 baseline.
  - No file states a model name outside this skill; this skill is the owner and may.
  - Nothing is deleted. A retired file moves to `_to_delete/<YYYYMMDD>-<reason>/`.

## Handoff Package

- Confirmed facts (verified, each with how it was verified):
  - Official OpenAI documentation states Codex invokes a skill by running `/skills` or typing `$` to
    mention it, and ChatGPT by typing `@`. Verified by fetching `learn.chatgpt.com/docs/build-skills`
    on 2026-08-06; `developers.openai.com/codex/skills` now 308-redirects there, so that page is the
    current official source and the old URL is stale in every file that cites it.
  - Codex's `/` palette does list skills as selectable entries. Verified from `openai/codex` issue
    22626 (Codex app 26.506.31421), which reproduces by opening the slash picker with `/`.
  - This pack's plugin build rewrites both `$name` and `/name` to `/<namespace>:name`, so dual-form
    call sites are already redundant in the packaged artifact. Recorded at `skills/sohrab/AGENTS.md`
    line 86 and implemented in `scripts/validate_sohrab_skill_pack.py` around line 99.
  - `scripts/validate_sohrab_skill_pack.py` rule V8 hard-codes a `$` sigil: it requires
    `interface.default_prompt` in `agents/openai.yaml` to contain `"$" + name`. Verified by reading
    lines 865-881. A single-form rewrite of that file's `default_prompt` therefore fails the checker.
  - `agents/openai.yaml` `default_prompt` names "Claude Opus 4.8", which `SKILL.md` retired. Verified
    by reading the file.
- Open assumptions (believed but unverified, each with what would verify it):
  - That no consumer outside this pack parses the retired `references/05-trigger-syntax.md` path.
    A repository-wide search for the filename would verify it before the file moves.
- Ruled out (approach, reason, evidence): treating `/name` as a universal raw-prompt invocation form
  and deleting the `$` and `@` facts. The official page documents those sigils for prompt text, and
  this skill is the fleet's only owner of that fact, so deleting it would strand every generated
  prompt aimed at a runtime outside this plugin. The user chose the formulation that keeps it.
- Read first on resume (ordered exact paths):
  1. `docs/agents/20260806-114753_alaa-prompting-guide-structural-revision-state.md`
  2. `skills/sohrab/AGENTS.md`
  3. `skills/sohrab/alaa-prompting-guide/references/00-topic-map.md`
- Environment notes: the pack's checkers run from the repository root as
  `python scripts\<name>.py`, and share one exit-code contract - `0` clean, `1` findings, `2` could
  not run. A `2` is a failed gate.
- Traps (looks correct, is not):
  - Rewriting `agents/openai.yaml` to a single `/` form passes review and fails rule V8.
  - Dropping a reference below 9 files would move the router back into the body; the count after
    this restructure is 14, so the router stays in `references/00-topic-map.md`.

## Ordered Work

### Phase 1 - Routing, invocation, and the body

- Status: pending
- Depends on: none
- Owned scope: `SKILL.md`, `references/00-topic-map.md` (new), `references/00-source-map.md`,
  `references/06-invocation-and-composition.md`, `references/05-trigger-syntax.md` (retired into it),
  `agents/openai.yaml`
- Excluded from this phase: every other reference file.
- Work:
  - [ ] Fold `05-trigger-syntax.md` into `06-invocation-and-composition.md` and retire the file.
  - [ ] State the invocation rule once: pack text uses `/name`; the picker-versus-prompt-text
        distinction and the `$` and `@` sigils are recorded as the raw-runtime nuance.
  - [ ] Add `references/00-topic-map.md` as the single router, every row an observable condition.
  - [ ] Reduce `SKILL.md` to role, when-not-to-use, decision procedure, principles as one-liners
        naming their owner, one router pointer, freshness, style.
  - [ ] Strip the changelog section from `00-source-map.md` and correct the stale Codex skills URL.
  - [ ] Fix the stale model name in `agents/openai.yaml` without breaking rule V8's `$` sigil.
- Acceptance criteria: exactly one router exists; no rule is stated in both the body and a
  reference; no `$name` or `@name` appears in pack call sites, only in the nuance statement.
- Validation commands: `python scripts\validate_sohrab_skill_pack.py`,
  `python scripts\check_fleet_references.py`, `python scripts\check_skill_index.py`
- Evidence observed: not run
- Commit: none yet

### Phase 2 - The two new capabilities

- Status: pending
- Depends on: Phase 1 conventions (stated in the dispatch, so it runs in parallel)
- Owned scope: `references/60-skill-authoring.md`, `references/61-skill-platform-mechanics.md` (new)
- Excluded from this phase: every other file.
- Work:
  - [ ] Split the platform lookup content - discovery paths, frontmatter key surfaces, description
        caps and listing budgets - out of `60` into `61`, leaving `60` as the authoring procedure.
  - [ ] Add the draft-then-compress loop with an observable test for when the rewrite is done.
  - [ ] Add the reference-decomposition procedure, including what a pointer sentence must contain.
- Acceptance criteria: both capabilities are procedures an agent can execute and fail, not advice;
  `60` is shorter than the 155-line file it replaces.
- Validation commands: same as Phase 1.
- Evidence observed: not run
- Commit: none yet

### Phase 3 - Model and runtime files

- Status: pending
- Depends on: Phase 1 conventions (stated in the dispatch)
- Owned scope: `references/10-gpt-5-6.md`, `11-codex-runtime-features.md`, `20-opus-5.md`,
  `30-sonnet-5.md`, `40-fable-5.md`, `41-claude-code-runtime-features.md`,
  `50-effort-and-thinking.md`, `90-model-selection.md`
- Excluded from this phase: every file owned by Phases 1, 2, and 4.
- Work:
  - [ ] Remove every section framed as a diff against a superseded generation, restating the
        surviving behaviour in the present tense.
  - [ ] Collapse the five-way delegation-polarity duplication to one owner plus pointers.
  - [ ] Stop restating per-model effort levels in `50`.
- Acceptance criteria: no migration checklist, no "what changed in this revision", no
  "behaviours that inverted relative to" framing; every surviving behavioural fact still present.
- Validation commands: same as Phase 1.
- Evidence observed: not run
- Commit: none yet

### Phase 4 - Instruction-file and subagent references

- Status: pending
- Depends on: Phase 1 conventions (stated in the dispatch)
- Owned scope: `references/70-agent-instruction-files.md`, `references/80-subagent-authoring.md`
- Excluded from this phase: every file owned by Phases 1, 2, and 3.
- Work:
  - [ ] Point delegation polarity at its single owner instead of restating it.
  - [ ] Apply the single-form call-site convention.
- Acceptance criteria: no duplicated rule survives; both files keep their own subject intact.
- Validation commands: same as Phase 1.
- Evidence observed: not run
- Commit: none yet

### Phase 5 - Reconcile, validate, review

- Status: pending
- Depends on: Phases 1-4
- Owned scope: cross-file reconciliation and the validation surface.
- Excluded from this phase: new content.
- Work:
  - [ ] Reconcile each lane's diff against its declared scope.
  - [ ] Run all three checkers and record observed output.
  - [ ] Independent review of the complete change.
- Acceptance criteria: three checkers at exit `0`; total line count at or below 1600; review
  findings resolved or explicitly accepted.
- Validation commands: the three checkers above, plus `--self-test` on each.
- Evidence observed: not run
- Commit: none yet

## Delegation

- Independent lane ownership, if admitted: Phases 2, 3, and 4 have disjoint write scopes and run in
  parallel. Phase 1 is kept in the main conversation because it fixes the conventions the other
  three must apply.
- Dispatches assume zero shared context: the conventions, the confirmed facts, and the scope
  exclusions are copied into each dispatch rather than referenced.
- Lanes report changed paths; this plan's owner stages and writes every commit.

## Blockers and Next Action

- Blockers: none known.
- Next action: execute Phase 1 in the main conversation while Phases 2-4 run as dispatched lanes.
