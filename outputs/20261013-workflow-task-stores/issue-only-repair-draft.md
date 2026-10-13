# Issue-only sink repair draft

Status: draft only; source remains frozen until parent supplies accepted compression.
Scope: SKILL.md, references/context-continuity.md and directly related references/context-curation.md in alaa-workflow. No admission, templates, scripts, tests or lifecycle definitions change.
Baseline: `repair-draft-baseline/skills/sohrab/alaa-workflow/` contains the three source files before this repair.

## SKILL.md - Curate reusable context paragraph

At a completed or failed phase, or a material decision boundary, run an intermediate scan through `/alaa-extract-agent-lessons` only when that boundary carries one of the seven signals `references/context-curation.md` lists, and record admitted candidates through that reference. Before completion, run the same skill's final full-engagement gate even when the expected result is empty, and record its outcome through that reference. Its recording rules use admitted workflow artifacts or canonical issue notes for issue-only work; they do not expand artifact admission.

## SKILL.md - Validate the workflow artifacts paragraphs

When a workflow artifact family is admitted, run `scripts/validate_workflow_files.py --plan <path>` before handoff and completion. It correlates explicit references or the selected stem, validates marked task-store families and snapshots offline, and preserves unmarked completed history. Its structural result proves no live Beads binding or readiness. Issue-only work creates no plan merely to run this artifact validator; required behavior validation still runs and its evidence is recorded in canonical issue notes through `references/context-continuity.md`.

For admitted artifact families, exit `0` is clean, and warnings alone do not fail it. Exit `1` is a blocking artifact error, repaired before advancement rather than reported as a pass. Exit `2` means validation failed to run; a missing selected plan, uncorrelatable companion or unreadable file is a failed gate, never evidence that the artifacts are clean. No artifact validation was run for issue-only work; report that distinction without implying its required behavior validation passed.

## context-continuity.md - Recovery goal paragraph

Treat all four as the same problem. The design target is a task any competent agent can resume from canonical task/workflow owners and available source/evidence, without conversation history. The cold-start test below checks this recovery goal.

## context-continuity.md - Artifact division introduction and issue-only addition

For admitted families, the three artifacts divide the work accordingly:

Keep the existing table and handoff-package rationale unchanged. Add immediately after that rationale:

For issue-only Beads work, canonical issue notes own execution position, validation evidence and learned knowledge. Record required outcomes there without creating a plan, checkpoint or six-field handoff package. Link canonical evidence rather than maintaining editable copies in both issue notes and workflow artifacts.

## context-continuity.md - When to write items 3 and 4

3. **A validation runs.** Record its evidence once in the admitted plan, or canonical issue notes for issue-only work. When a checkpoint is admitted, point its last verified result to that evidence. `references/workspace-and-integration.md` owns tested identity, write isolation and reuse; a result without attributable inputs cannot be cited on resume.
4. **Something is learned that would be expensive to rediscover.** Add it immediately to the matching handoff field when a plan is admitted, or canonical issue notes for issue-only work, while the detail is still exact.

## context-curation.md - Intermediate parking paragraph

Park each admitted candidate in the matching handoff-package field when a plan is admitted, or in canonical issue notes for issue-only work; `references/context-continuity.md` owns these recording locations and handoff-field semantics. Record a judgment as a confirmed fact about who chose what and why, never as a universal fact — a preference recorded as a law is applied unchanged in the next repository, where it is wrong and carries no trace of who decided it. Do not duplicate a candidate between owners; link its canonical record instead.

## context-curation.md - Final gate item 3

3. Record the outcome — persisted, deferred, rejected, or no admitted candidates — once in the admitted plan's final phase evidence, with a reference from its checkpoint when admitted, or in canonical issue notes for issue-only work. Do not create artifacts outside admission or copy the outcome into another editable owner.

## context-curation.md - Reopening paragraphs

A `pipeline reopen required` verdict means the gate changed something the already-closed evidence described. Reopen the owning phase, or the issue-only task when no plan is admitted, perform the authorized repository promotion, rerun every affected validation, review, documentation, and documentation-check gate, then rerun final curation.

Never close a plan or issue-only task against evidence the curation gate changed. Closing against superseded evidence reports a state never observed, and that is the report a reader trusts.

## Preserved obligations

- Behavior implementation, proportional required validation and attributable evidence remain required; no issue closure substitutes for workflow acceptance.
- Intermediate scans still require the existing seven signals; final full-engagement curation still runs even for an empty expected result.
- Four lifecycle verdicts, permission boundaries, artifact admission and conditional JSON remain unchanged.
- Plan-family outcomes/evidence remain canonical in the plan; checkpoint/issue links carry references, not duplicate editable evidence.
