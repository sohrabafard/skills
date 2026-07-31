# Workflow Plan - Fix alaa-repo-docs language preservation and documentation graph ownership

- Task ID: `20260730-230608_alaa-repo-docs-language-and-link-ownership`
- Mode: `execute`
- Profile: `resumable`
- Status: completed
- Created: `2026-07-30T23:06:08Z`
- Parent plan: not created
- Prompt pack: not created
- Checkpoint: `docs/agents/20260730-230608_alaa-repo-docs-language-and-link-ownership-state.md`
- Machine state: not created

## Summary and Outcome

- Current repository truth: `alaa-repo-docs` forces English as the canonical language, automatically requires Persian companions when any Persian document exists, and its checker emits `PAIR-MISSING` for otherwise valid unpaired documents. It already contains partial cross-link and role-separation rules, but no complete canonical-topic ownership procedure.
- Outcome: Existing documents retain their language; new localized companions are created only when explicitly requested; explicit Persian companions use the `.fa.md` form by default; documentation topics have one canonical home with summaries and relative links elsewhere.
- Strategy: Align the entrypoint, language/link reference, workflow reference, checker behavior and fixtures, and Codex metadata; then run narrow helper tests, pack validators, fleet references, workflow validation, diff hygiene, and a fresh-agent behavioral review.

## Scope

- In scope: `skills/sohrab/alaa-repo-docs/**`, its two pack routing entries in
  `skills/sohrab/README.md` and `skills/sohrab/README.fa.md`, plus this plan and checkpoint.
- Out of scope: other skills, target-project documentation, vendor content, commits, pushes, publication, and unrelated baseline findings.
- Constraints and assumptions: preserve dirty unrelated work; write committed files in English; keep Claude Code and Codex invocation forms correct; do not delete files; state each rule once; treat the user request as explicit authorization to change this existing skill.

## Handoff Package

Knowledge that lives only in the current agent's head and disappears on compaction. Fill a field when something is learned, not on a schedule; leave a field empty rather than padding it. See `references/context-continuity.md`.

- Confirmed facts (verified, each with how it was verified): `SKILL.md`, all nine references, the
  checker, fixtures, and `agents/openai.yaml` were read in full; the old prose and checker encoded
  automatic companion creation; the revised seven-case self-test passes; quick skill validation,
  workflow validation, target link checks, and diff hygiene pass; full pack, index, and fleet gates
  retain only findings outside the touched skill.
- Open assumptions (believed but unverified, each with what would verify it): none yet.
- Ruled out (approach, reason, evidence): keeping `PAIR-MISSING` while changing prose was rejected because the deterministic helper would continue enforcing the undesired behavior; forcing a new default language was rejected because the request requires language preservation.
- Read first on resume (ordered exact paths): `skills/sohrab/alaa-repo-docs/SKILL.md`; `skills/sohrab/alaa-repo-docs/references/10-language-and-links.md`; `skills/sohrab/alaa-repo-docs/references/40-sync-workflow-and-evidence.md`; this plan; the checkpoint.
- Environment notes (command shapes that work here, and ones that look right but fail): run repository validators from the repository root; `git status` emits permission warnings for pre-existing `.tmp-review-*` directories, so use path-scoped status and diffs for this task.
- Traps (looks correct, is not): an existing `.fa.md` file is evidence of an existing pair, not
  authorization to translate every other document; correct links do not prove good topic ownership
  or absence of semantic duplication; a bundled checker must be invoked through `$SKILL_DIR`, not
  as if it lived in the target repository.

## Ordered Work

### Phase 1 - Ground the behavioral contract

- Status: completed
- Depends on: none
- Owned scope: repository rules, requested skills, the complete `alaa-repo-docs` package, and relevant prior skill-pack validation notes.
- Excluded from this phase: edits.
- Work:
  - [x] Read the named sources and verify current behavior.
  - [x] Convert the user request into checkable acceptance criteria.
- Acceptance criteria: the current unwanted trigger, its deterministic enforcement, and the missing canonical-ownership procedure are identified from live files.
- Validation commands: `rg -n -i "English|Persian|mirror|pair-missing|duplicate|cross-link" skills/sohrab/alaa-repo-docs`
- Evidence observed: automatic Persian companion creation is encoded in `SKILL.md`, references, checker, fixture, and Codex metadata.

### Phase 2 - Implement the aligned contract

- Status: completed
- Depends on: Phase 1
- Owned scope: `skills/sohrab/alaa-repo-docs/**` and the skill's two pack routing entries.
- Excluded from this phase: other skills and target repositories.
- Work:
- [x] Preserve each existing document's language and select a new document's language from explicit request or local convention.
- [x] Require explicit user authorization before creating any translated/localized companion.
- [x] Remove `PAIR-MISSING` enforcement while retaining opt-in orphan and structural-drift checks for pairs that exist.
- [x] Add canonical-topic ownership, de-duplication, hub navigation, reciprocal related links, and semantic graph review rules without duplicating them across files.
- [x] Align `agents/openai.yaml` and both pack routing entries with the revised contract.
- Acceptance criteria: all five surfaces express one consistent language and document-graph contract for both runtimes.
- Validation commands: targeted searches and checker self-test.
- Evidence observed: old automatic-language wording is absent from the touched surfaces; the helper
  defaults to link checks and validates only pairs explicitly named with
  `--localized-pair <base> <companion>`.

### Phase 3 - Validate and forward-test

- Status: completed
- Depends on: Phase 2
- Owned scope: touched skill, workflow artifacts, and repository-native validators.
- Excluded from this phase: remediation of unrelated baseline failures.
- Work:
  - [x] Run helper self-tests and a direct fixture proving unpaired documents are valid.
  - [x] Run narrow skill validation, pack validation, index validation, fleet references, workflow validation, and `git diff --check`.
  - [x] Forward-test the revised skill with a fresh read-only agent against realistic language and documentation-graph scenarios.
  - [x] Reconcile findings, update workflow state, and re-open changed files.
- Acceptance criteria: requested behavior is present, deterministic checks agree, cross-runtime metadata is aligned, and no touched-scope validation remains red.
- Validation commands: `python skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py --self-test`; `python scripts/validate_sohrab_skill_pack.py`; `python scripts/check_skill_index.py`; `python scripts/check_fleet_references.py`; `python skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan docs/_agent_plans/20260730-230608_alaa-repo-docs-language-and-link-ownership.md`; `git diff --check`.
- Evidence observed: ten helper self-tests pass; quick validation passes; workflow validation
  passes; `git diff --check` passes; the forward-test confirmed implicit and explicit language
  behavior plus canonical ownership and found one `$SKILL_DIR` portability ambiguity, which was
  fixed. Review follow-up replaced suffix-specific repository-wide pair discovery with explicit
  `--localized-pair <base> <companion>` checks and rejects `--files` paths outside the repository
  root. Full pack validation remains red on unrelated skills; index has two unrelated missing
  metadata findings; fleet references has 17 unrelated failures and only informational unmarked
  target paths for `alaa-repo-docs`.

## Delegation

- Keep shared-context work in the main conversation.
- Independent lane ownership, if admitted: none.
- Dispatches assume zero shared context: copy the relevant handoff-package facts into the dispatch text rather than referring to this conversation.

## Blockers and Next Action

- Blockers: none for this task. Repository-wide baseline findings remain outside scope.
- Next action: none; implementation and validation are complete.
