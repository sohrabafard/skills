# Alaa Services Contract Coverage Repair

## Goal

Restore `skills/sohrab/alaa-services-contract` so `references/full-guide.md` is again a preserved whole-contract document, while keeping the newer compact trusted-context model that replaces `X-Profile` and `X-Project-ID`.

## Assumptions

- The active compact trust model is intentional and should remain the normative contract.
- The regression to repair is loss of preserved contract coverage, not the existence of split references.
- Purposeful duplication between split references and `references/full-guide.md` is acceptable for this skill.

## Constraints

- Preserve the existing dirty worktree and layer the repair on top of it.
- Keep `SKILL.md` lean and routing-first.
- Keep documentation in simple, fluent English.
- Use only repo-portable relative paths in skill docs.

## Closest existing patterns

- `skills/sohrab/alaa-trust-gateway-auth` keeps `SKILL.md` lean, `references/00-topic-map.md` as the router, and `references/full-guide.md` as the preserved whole-guide reference.
- `skills/sohrab/alaa-workflow` requires repo-local task memory for non-trivial multi-file work.
- `skills/sohrab/alaa-repo-docs` requires rich documentation to stay strong rather than being compressed into lower-signal summaries.

## Phases (with dependencies)

1. Task memory bootstrap
   - Depends on: none
   - Output: this plan file and a durable state file
   - Validation: files exist and capture current assumptions
   - Parallel-safe: no
2. Contract audit and repair
   - Depends on: task memory bootstrap
   - Output: repaired `SKILL.md`, `references/00-topic-map.md`, `references/full-guide.md`, and any split refs that need wording alignment
   - Validation: manual diff review against the current worktree and companion skills
   - Parallel-safe: no
3. Validation and close-out
   - Depends on: contract audit and repair
   - Output: updated state file with validation summary
   - Validation: `quick_validate.py` plus targeted readback of the repaired documents
   - Parallel-safe: no

## Parallel-safe work split

- Keep this task single-authored.
- The same normative wording is shared across multiple files, so parallel writes would increase merge risk and wording drift.

## Commands to run

- `git diff -- skills/sohrab/alaa-services-contract`
- `python C:\Users\CIT\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\sohrab\alaa-services-contract`
- targeted `Get-Content` reads for `SKILL.md`, `references/00-topic-map.md`, `references/full-guide.md`, and companion-skill source files

## Files touched (append-only log)

- `docs/_agent_plans/20260404-212209_alaa-services-contract-coverage-repair.md` — created task plan
- `docs/agents/alaa-services-contract-coverage-repair-state.md` — created durable task state
- `skills/sohrab/alaa-services-contract/SKILL.md` — tightened maintenance rules so split refs and the full guide stay synchronized
- `skills/sohrab/alaa-services-contract/references/00-topic-map.md` — clarified that `full-guide.md` is the preserved whole-contract view
- `skills/sohrab/alaa-services-contract/references/25-end-to-end-flow-and-boundaries.md` — aligned the frontend-forbidden header list with the compact trust model
- `skills/sohrab/alaa-services-contract/references/full-guide.md` — restored lost normative contract coverage while keeping the compact trust model

## Done / Remaining

- Done:
  - audited the current dirty worktree
  - confirmed the compact trust model should be preserved
  - identified that the main regression is loss of preserved whole-guide coverage
  - repaired the router files and rehydrated `references/full-guide.md`
  - validated the skill with `quick_validate.py` and `git diff --check`
- Remaining:
  - no implementation work remains for this repair task
