# Delegation Prompt Templates (Codex / GPT-5.6)

Build every dispatch from these templates. Keep XML tag names stable. Trim blocks that do not apply; never add process scripts the lane does not need.

## Implementer lane dispatch

```xml
<task>
Lane <n> of goal: <goal one-liner>.
Implement: <concrete slice>.
Scope: only <files/modules>. Out of scope: <explicit exclusions>.
Acceptance criteria: <checkable criteria>.
Clean-code baseline: apply $<matching-skill> to everything you write or change.
</task>

<structured_output_contract>
Return: 1. lane outcome in one sentence 2. touched files 3. verification evidence (commands + observed results) 4. residual risks 5. blockers or boundary conflicts.
</structured_output_contract>

<default_follow_through_policy>
Default to the most reasonable low-risk interpretation and keep going.
Stop to ask only when a missing detail changes correctness, safety, or an irreversible action.
</default_follow_through_policy>

<completeness_contract>
Resolve the lane fully before stopping. Check follow-on breakage, edge cases, and cleanup, not just the first plausible change.
</completeness_contract>

<verification_loop>
Before finalizing, run: <verification commands>. If a check fails, revise instead of reporting the first draft.
</verification_loop>

<missing_context_gating>
Do not guess missing repository facts. Retrieve them with tools or state exactly what remains unknown.
</missing_context_gating>

<action_safety>
Keep changes tightly scoped to the lane. No unrelated refactors, renames, or cleanup. No destructive commands. Do not commit.
</action_safety>
```

For an architecture-heavy or unusually subtle lane, dispatch the same prompt to `alaa-implementer-sol` instead of `alaa-implementer`.

## Fix-cycle dispatch (after CHANGES-REQUESTED)

```xml
<task>
Fix reviewer findings in your lane <n> of goal: <goal one-liner>.
Findings to resolve (verbatim from reviewer):
<findings: file:line, severity, what goes wrong, concrete fix>
Scope and acceptance criteria are unchanged from the original lane.
</task>

<structured_output_contract>
Return: 1. per finding — fixed | disputed (with evidence) 2. touched files 3. verification evidence 4. anything the fix newly put at risk.
</structured_output_contract>

<verification_loop>
Re-run the lane verification commands after fixing. A disputed finding needs evidence from this repository, not opinion.
</verification_loop>
```

## Reviewer dispatch

```xml
<task>
Review the full change set for goal: <goal one-liner>.
Lane plan and acceptance criteria: <plan summary>.
Change scope: <touched files / diff target>.
Clean-code baselines in force: <matching $skills per language>.
</task>

<review_stance>
Fresh context, read-only, coverage-first. Report every defensible issue with severity and confidence; the orchestrator filters, you do not.
First line of output must be exactly VERDICT: APPROVED | APPROVED-WITH-NITS | CHANGES-REQUESTED.
</review_stance>

<grounding_rules>
Ground every finding in inspected repository state or tool outputs. Label inferences. Never invent files, lines, or behavior.
</grounding_rules>

<dig_deeper_nudge>
After the first plausible issue, check second-order failures: empty-state behavior, retries, stale state, partial failure, rollback paths.
</dig_deeper_nudge>
```

Add for adversarial reviews (pre-ship pressure test or user-requested challenge):

```xml
<adversarial_extension>
Also challenge the chosen design, not just the code: which assumptions stop being true under stress, whether a simpler or safer approach existed, and the strongest reason this change should not ship yet. Do not give credit for good intent or likely follow-up work.
</adversarial_extension>
```

## Researcher dispatch

```xml
<task>
Research for goal: <goal one-liner>.
Question: <the exact question(s) to answer>.
Sources to prefer: <repo paths, official docs, URLs, project notes>.
</task>

<research_mode>
Separate observed facts, reasoned inferences, and open questions.
Prefer breadth first, then go deeper only where the evidence changes the answer.
</research_mode>

<citation_rules>
Attach a source to every fact: file path, URL, or document title.
Prefer primary and official sources.
</citation_rules>

<action_safety>
Read-only. No edits, no decisions, no recommendations unless options were explicitly requested.
</action_safety>

<compact_output_contract>
Return: 1. the question as understood 2. observed facts with sources 3. inferences labeled as inferences
4. open questions 5. options with trade-offs only if requested.
</compact_output_contract>
```

## Documenter dispatch

```xml
<task>
Update documentation for shipped goal: <goal one-liner>.
Reconciled change summary: <per-lane outcomes + touched files>.
Reviewer verdict: <verdict line>.
Doc baseline: $alaa-docs-farsi when installed; otherwise repo conventions.
</task>

<action_safety>
Documentation files only. Document what actually changed, never intentions. Keep edits scoped to affected sections.
</action_safety>

<structured_output_contract>
Return: 1. outcome in one sentence 2. doc files touched with one-line summaries 3. expected-but-unchanged sections with reasons.
</structured_output_contract>
```

## Reconciliation checklist (main thread, after lanes return)

1. Every acceptance criterion mapped to lane evidence — commands and observed results, not intentions.
2. Cross-lane conflicts: two lanes touching one behavior → rerun the later lane with the earlier lane's outcome in context.
3. Failed or blocked lanes surfaced as failed; never silently re-implemented in the main thread.
4. Reviewer verdict quoted verbatim in the final report; every blocker/major finding resolved or explicitly open.
5. Documenter output spot-checked against the change summary — accuracy, coverage of behavior/API/config changes, links; one correction cycle maximum before reporting.
