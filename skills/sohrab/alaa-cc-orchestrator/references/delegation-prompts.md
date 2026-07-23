# Delegation Prompt Templates (Claude Code)

Build every dispatch from these templates. Be explicit and literal: Claude models follow instructions exactly and do not silently generalize, so state scope words like "every", "only", and "all files" when they apply. Trim blocks that do not apply.

## Implementer lane dispatch

```text
Lane <n> of goal: <goal one-liner>.

Implement: <concrete slice>.
Scope: edit only <files/modules>. Out of scope: <explicit exclusions>.
Acceptance criteria: <checkable criteria>.
Clean-code baseline: load /sohrab-skills:<matching-skill> and apply it to everything you write or change in this lane.

Work rules: default to the most reasonable low-risk interpretation and keep going; stop to ask only when a missing
detail changes correctness, safety, or an irreversible action. Resolve the lane fully — check follow-on breakage,
edge cases, and cleanup, not just the first plausible change. Do not guess repository facts; read the files.
No unrelated refactors, abstractions, or cleanup. Do not commit.

Verify before finalizing by running: <verification commands>. If a check fails, revise instead of reporting the first draft.

Return, in this order: 1. lane outcome in one sentence 2. touched files 3. verification evidence (commands + observed
results) 4. residual risks 5. blockers or boundary conflicts. A blocked lane is reported as blocked.
```

For an architecture-heavy or unusually subtle lane, dispatch the same prompt with the model overridden to Opus 4.8 per invocation.

## Fix-cycle dispatch (after CHANGES-REQUESTED)

```text
Fix reviewer findings in your lane <n> of goal: <goal one-liner>.

Findings to resolve (verbatim from reviewer):
<findings: file:line, severity, what goes wrong, concrete fix>

Scope and acceptance criteria are unchanged from the original lane. Re-run the lane verification commands after fixing.
A disputed finding needs evidence from this repository, not opinion.

Return, in this order: 1. per finding — fixed | disputed (with evidence) 2. touched files 3. verification evidence
4. anything the fix newly put at risk.
```

## Reviewer dispatch

```text
Review the full change set for goal: <goal one-liner>.

Lane plan and acceptance criteria: <plan summary>.
Change scope: <touched files / diff target>.
Languages in the diff and their clean-code baselines: <language → /sohrab-skills:skill pairs>.

Stance: fresh context, read-only conduct, coverage-first. Report every issue you find, including uncertain or
low-severity ones — do not filter for importance or confidence; include severity and confidence per finding so I can
filter. Ground every finding in inspected state; label inferences. After the first plausible issue, check second-order
failures: empty-state behavior, retries, stale state, partial failure, rollback paths.

Your first line must be exactly VERDICT: APPROVED | APPROVED-WITH-NITS | CHANGES-REQUESTED, followed by FINDINGS
(file:line, severity, confidence, what goes wrong, why, concrete fix — ordered by severity), RISKS, and GATE EVIDENCE.
```

Add for adversarial reviews (pre-ship pressure test or user-requested challenge):

```text
Additionally challenge the chosen design, not just the code: which assumptions stop being true under stress, whether
a simpler or safer approach existed, and the strongest reason this change should not ship yet. Do not give credit for
good intent or likely follow-up work.
```

## Researcher dispatch

```text
Research for goal: <goal one-liner>.

Question: <the exact question(s) to answer>.
Sources to prefer: <repo paths, official docs, URLs, project notes>.

Stance: read-only, evidence-first. Separate observed facts, reasoned inferences, and open questions. Prefer
breadth first, then go deeper only where the evidence changes the answer. Attach a source to every fact — file
path, URL, or document title — and prefer primary and official sources. No edits, no decisions, and no
recommendations unless options were explicitly requested.

Return, in this order: 1. the question as understood 2. observed facts with sources 3. inferences labeled as
inferences 4. open questions 5. options with trade-offs only if requested. Keep the report compact.
```

## Documenter dispatch

```text
Update documentation for shipped goal: <goal one-liner>.

Reconciled change summary: <per-lane outcomes + touched files>.
Reviewer verdict: <verdict line>.
Doc baseline: load /sohrab-skills:alaa-docs-farsi for Ala-style repos; otherwise follow repo conventions.

Documentation files only. Document what actually changed, never intentions. Keep edits scoped to affected sections.

Return, in this order: 1. outcome in one sentence 2. doc files touched with one-line summaries 3. expected-but-unchanged
sections with reasons.
```

## Fan-out authorization fragment (include once per orchestrated dispatch turn)

```text
Explicit authorization: you may use subagents, and you may run independent lanes of this task in parallel or in the
background, without asking again. Spawn one alaa-implementer per independent lane in the same turn, give every lane
the same constraints and a clearly scoped slice so nothing is duplicated or dropped, wait for all of them, and
reconcile the results yourself before moving on. Do not spawn a subagent for work you can complete directly.
```

## Reconciliation checklist (main session, after lanes return)

1. Every acceptance criterion mapped to lane evidence — commands and observed results, not intentions.
2. Cross-lane conflicts: two lanes touching one behavior → rerun the later lane with the earlier lane's outcome in context.
3. Failed or blocked lanes surfaced as failed; never silently re-implemented in the main session.
4. Reviewer verdict quoted verbatim in the final report; every blocker/major finding resolved or explicitly open.
5. Audit every progress claim against an actual tool result from this session before reporting it.
