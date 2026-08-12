# Workflow Plan - alaa-repo-docs canonical ownership distinctions

- Task ID: `20260812-213031_alaa-repo-docs-canonical-ownership-distinctions`
- Mode: `plan`
- Profile: `direct`
- Status: complete
- Created: `2026-08-12T21:30:31Z`
- Parent plan: not created
- Prompt pack: not created
- Checkpoint: not created
- Machine state: not created
- Base branch and commit: `main` at `fc47d46f`
- Work branch: `agent/alaa-repo-docs-canonical-ownership-distinctions`
- Worktree: none

## Summary and Outcome

- Current repository truth: `skills/sohrab/alaa-repo-docs/references/10-language-and-links.md`
  section `## Canonical topic ownership and de-duplication` (lines 105-132) is the single owner of
  canonical-topic assignment and de-duplication. `SKILL.md:63` and `references/00-topic-map.md` row 1
  both route here, and `references/15-document-size-and-clustering.md:51` and
  `references/40-sync-workflow-and-evidence.md:55` both defer to it rather than restating it. Its
  step 6 currently forbids copying "normative rules" into several documents with no exception, and
  step 8 requires every non-canonical occurrence to become a summary or a link.
- Outcome: the de-duplication procedure names the unit it operates on and the two kinds of text it
  must not collapse, so an agent stops merging two audience-scoped normative records that happen to
  name the same release, and stops hand-authoring a value that exists only as a drift projection.
- Strategy: one subsection added to the existing owner, one scope line at the head of that section,
  and one ownership row in `SKILL.md`. No new reference, no new combined guide, no repository-specific
  example.

## Scope

- In scope: `skills/sohrab/alaa-repo-docs/references/10-language-and-links.md` and
  `skills/sohrab/alaa-repo-docs/SKILL.md`.
- Out of scope: `references/15-document-size-and-clustering.md` and
  `references/40-sync-workflow-and-evidence.md` — both already defer to the owner, so a copy here
  would be the defect this task removes. `alaa-go-chi-development` and every other skill.
- Constraints and assumptions: preserve the one-canonical-home doctrine; add no release-governance,
  version-selection, changelog-policy, or contract-classification rule; embed no `alaa-go-chi`
  version, decision id, or file name; `SKILL.md` stays routing-first. Local commit authorized on the
  work branch; merge and push are not.

## Handoff Package

Knowledge that lives only in the current agent's head and disappears on compaction. Fill a field when something is learned, not on a schedule; leave a field empty rather than padding it. Field semantics are in `alaa-workflow references/context-continuity.md`, which is in the skill, not in this repository.

- Confirmed facts (verified, each with how it was verified):
  - The single owner is `references/10-language-and-links.md`, section
    `## Canonical topic ownership and de-duplication`. Verified by reading `SKILL.md:63`,
    `references/00-topic-map.md:10`, `references/15-document-size-and-clustering.md:51-53`, and
    `references/40-sync-workflow-and-evidence.md:55-58`; all four route to it and none restates it.
  - "Reviewed together" already means "not necessarily edited together", and
    `references/40-sync-workflow-and-evidence.md:18` owns that sentence. Restating it in
    `10-language-and-links.md` would be a second copy, so this plan links to the owner instead.
  - `alaa-repo-docs` ships one script, `scripts/check_markdown_links.py`. Its `--help` shows link,
    anchor, `--localized-pair`, and `--line-budget` checks only.
- Open assumptions (believed but unverified, each with what would verify it): none.
- Ruled out (approach, reason, evidence):
  - A new reference file for the distinction: `SKILL.md:111` forbids a combined guide and the topic
    map routes each condition to exactly one file; a second file for a rule the owner already almost
    states would be the drift this skill was restructured to remove.
  - A mechanical check for this boundary: deciding whether two normative records carry different
    required semantics needs prose semantics. The only mechanically decidable proxy is a keyword
    test on document names, which WORKFLOW step 3 forbids, so no fixture is added.
- Read first on resume (ordered exact paths):
  - `skills/sohrab/alaa-repo-docs/references/10-language-and-links.md`
  - `skills/sohrab/alaa-repo-docs/SKILL.md`
  - `skills/sohrab/AGENTS.md`
- Environment notes (command shapes that work here, and ones that look right but fail):
  - The link checker takes the repository root as a positional argument and `--files` paths relative
    to it: `python skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py . --files <paths>`.
  - A commit in this repository triggers a hook that fetches every vendor subtree; the fetch is
    read-only and prints upstream sync lines that are not part of the commit.
- Traps (looks correct, is not):
  - The named "skills-repository handoff" from the completed `alaa-go-chi` goal is not in this
    repository. Searched `docs/_agent_plans/`, `docs/agents/`, `.codex/state/`, `artifacts/`,
    `outputs/`, every tracked `*.md`, and `git log --grep=go-chi`. Its absence is a missing result,
    not evidence that the problem it described is absent; the OWNER DECISION in the request is the
    authority this plan executes against.

## Ordered Work

### Phase 1 - Ground and implement

- Status: complete
- Depends on: none
- Owned scope: `skills/sohrab/alaa-repo-docs/references/10-language-and-links.md`,
  `skills/sohrab/alaa-repo-docs/SKILL.md`
- Excluded from this phase: every other skill, and both references that already defer to the owner
- Work:
  - [x] Confirm the single owner of canonical-topic and de-duplication rules, and that no other file
        states the distinction.
  - [x] Add the unit-of-de-duplication line and the three-kind classification to the owning section.
  - [x] Add one ownership row to `SKILL.md` for release governance and its neighbours.
  - [x] Scope step 6 to narrative documents, so it stops forbidding what the new classification
        permits. Without this the two statements contradict each other and the older one wins.
- Acceptance criteria: the rule exists in exactly one reference; `SKILL.md` gains routing only; no
  `alaa-go-chi` specific version, decision id, or file name appears in the pack's reusable doctrine.
- Validation commands:
  `grep -rniE "go-chi|D-33|\.rules/|v1\.x\.y|CONTRACTS\.md|configkit" skills/sohrab/alaa-repo-docs/`
- Evidence observed: the grep matched nothing (exit 1, no output). `SKILL.md` gained one table row
  and no prose. `references/10-language-and-links.md` gained one scope line, one subsection, and one
  word in step 6; no other file in the pack was touched.
- Commit: this task's single commit

### Phase 2 - Validate and reconcile

- Status: complete
- Depends on: Phase 1
- Owned scope: the validation surface for a `skills/sohrab/` prose change
- Excluded from this phase: any behavioural edit
- Work:
  - [x] Run the focused skill validation, fleet-reference validation, index validation, the
        alaa-repo-docs Markdown-link check, and `git diff --check`.
  - [x] Reconcile this plan's status, evidence, and remaining work.
- Acceptance criteria: required behavior and evidence agree.
- Validation commands:
  - `python scripts/validate_sohrab_skill_pack.py`
  - `python scripts/check_fleet_references.py --skill alaa-repo-docs`
  - `python scripts/check_fleet_references.py`
  - `python scripts/check_skill_index.py`
  - `python skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py . --files skills/sohrab/alaa-repo-docs/SKILL.md skills/sohrab/alaa-repo-docs/references/10-language-and-links.md`
  - `git diff --check`
- Evidence observed: every command above exited `0`, run after the final edit.
  `validate_sohrab_skill_pack.py` reported no finding and no size warning for `alaa-repo-docs`.
  `check_markdown_links.py` was run without `--line-budget`: that gate measures narrative documents
  in a documented repository, and these two files are skill instructions, not that repository's
  documents. No new check was added — deciding whether two normative records carry different
  required semantics needs prose semantics, and the only mechanical proxy is a filename keyword
  test, which the request forbids.
- Commit: this task's single commit

## Delegation

- Keep shared-context work in the main conversation.
- Independent lane ownership, if admitted: none. The user forbade an orchestrator, delegation, and
  subagents for this goal.
- Dispatches assume zero shared context: copy the relevant handoff-package facts into the dispatch text rather than referring to this conversation.
- Lanes report changed paths; this plan's owner stages and writes every commit.

## Blockers and Next Action

- Blockers: none known. The BLOCKED condition was evaluated and does not hold: exactly one canonical
  owner exists and it does not yet state the distinction. One sub-part of the owner decision — that
  reviewing paired documents is not editing them — is already owned by
  `references/40-sync-workflow-and-evidence.md:18`, so it is linked rather than copied.
- Next action: none. The work is committed on the work branch; merge and push were not authorized.
