# Workflow plan-kind documentation outcome

The shipped workflow contract now separates local design discussion from execution of an approved design. The workflow skill and its references document admission, approval, tracking, continuity, skill bindings, and compatibility. The final independent instruction and correctness reviews both approved the frozen source snapshot.

This artifact records the documentation outcome; the workflow skill and its owner references remain the canonical operational guidance.

The 14-file source manifest was checked against the working tree. Its combined SHA-256 is `130f88682e51226f966706b21d85030b5ca7929898eab36a792b78c98604f6a5`.

## CLI shapes

Design initialization is local and resumable:

```text
python skills/sohrab/alaa-workflow/scripts/init_workflow_files.py --task "<title>" --plan-kind design
```

Execution initialization names a readable approved design and explicitly binds Beads:

```text
python skills/sohrab/alaa-workflow/scripts/init_workflow_files.py --task "<title>" --plan-kind execution --approved-design "<approved-design-path>" --task-store beads --beads-binding "<portable-reference>" [--profile <profile>] [--review-boundary phase|final] [--with-prompts]
```

The design family records scope, proposed design, dated attributed decisions, open questions, approval fields, handoff knowledge, and a design-position checkpoint. It has no execution hierarchy or cursor. Execution requires an approved design link, Beads binding, phase-task-subtask hierarchy, and exact skill mappings. Offline validation checks recorded approval structure; it does not authenticate human approval or prove live Beads readiness.

## Compatibility and path behavior

Every new plan requires `--plan-kind design|execution`; mode and profile do not select the kind. Existing unmarked families retain their recorded contract and are not migrated automatically. Existing standalone state snapshots remain historical input; new `--state-only` initialization is rejected. Deprecated aliases remain subject to kind checks. The `legacy` profile remains available for existing four-file consumers.

The validator expands installed skill-source home paths such as `~/.codex/.../SKILL.md` and `~/.claude/.../SKILL.md`, and accepts readable host Windows paths. It checks that each resolved file is named `SKILL.md` and its frontmatter name matches the mapped skill. Repository-owned references remain portable.

## Source files and evidence

Changed source files (relative to `skills/sohrab/alaa-workflow/`): `SKILL.md`; `assets/plan-template.md`, `assets/design-plan-template.md`, `assets/design-checkpoint-template.md`; `references/artifact-lifecycle.md`, `references/companion-routing.md`, `references/context-continuity.md`, `references/context-curation.md`, `references/phase-prompts.md`, `references/task-tracking.md`, `references/workspace-and-integration.md`; `scripts/init_workflow_files.py`, `scripts/validate_workflow_files.py`, `tests/test_workflow_files.py`.

The final source manifest contains 14 files and its combined digest matches this checkout. Both final independent review verdicts are `APPROVED`. Focused tests, repository gates, and temporary sample outcomes belong to the verifier record; this documentation lane did not rerun them. Sample approval metadata is synthetic, so verification proves neither actual user approval nor installed runtime activation.

No external links were added. The CLI examples are source-derived; the active verifier owns their final-snapshot sample and test validation. No commit, push, installation, or publication occurred in this lane.

## Expected but unchanged documents

The root README, workflow skill index, and `CLAUDE.md` remain unchanged because this updates the contract of an existing skill and does not add or rename a skill or change installation instructions. No release note is warranted for this local skill-pack change.

## Document classification

`documentation.md` is `EXEMPT-ATOMIC`: it is a single task outcome and evidence record intended to be consumed whole, rather than a maintained repository guide. No narrative size grade applies.
