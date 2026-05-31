# Agent Plan - Alaa Golang Vendor How-To Sync

- Task ID: `20260531-124751_alaa-golang-vendor-how-to-sync`
- Created: `2026-05-31T12:47:51+03:30`
- Mode: `execute`
- Status: `completed`
- Plan path: `docs/_agent_plans/20260531-124751_alaa-golang-vendor-how-to-sync.md`
- State path: `.codex/state/20260531-124751_alaa-golang-vendor-how-to-sync.json`

## Goal

Update `skills/sohrab/alaa-golang` after commit `16cac906147f73fd1c31c5d155697da60e685af9` added the vendor
`golang-how-to` orchestrator and related Go skill-pack refinements.

## Scope

- Keep `alaa-golang` compact and routing-first.
- Add exact route parity for the new vendor Go skill inventory.
- Preserve `skill-creator` progressive disclosure by moving detailed orchestration guidance into references.
- Keep Alaa platform rules stronger than generic vendor defaults.

## Non-goals

- Do not edit `vendor/cc-skills-golang`.
- Do not rewrite unrelated Sohrab skills.
- Do not run browser automation.
- Do not create project `AGENTS.md` / `CLAUDE.md` force-load blocks unless explicitly requested.

## Current findings

- Commit `16cac906147f73fd1c31c5d155697da60e685af9` added `vendor/cc-skills-golang/skills/golang-how-to`.
- Vendor Go skill folders with `SKILL.md`: `43`.
- Current `references/10-installed-golang-skills.md` route headings before this slice: `42`.
- Gap: `golang-how-to`.

## Execution steps

1. Update `SKILL.md` to mention `golang-how-to` orchestration and the local configure-mode boundary.
2. Add `golang-how-to` to `references/10-installed-golang-skills.md`.
3. Add a focused orchestration reference for primary plus secondary skill bundles and overlap boundaries.
4. Link the new reference from the topic map, full guide, and gap coverage.
5. Update plan/state and validate.

## Validation approach

- Run targeted `skill-creator` quick validation for `skills/sohrab/alaa-golang`.
- Run full `scripts/validate_sohrab_skill_pack.py`.
- Run semantic route audit: vendor skill names vs `references/10-installed-golang-skills.md` headings.
- Run `git diff --check`.

## Exit criteria

- `vendor=43 routed=43 missing=0 extra=0`.
- `alaa-golang` quick validation passes.
- Full pack validation passes or any unrelated pre-existing warnings are clearly identified.
- Diff hygiene passes.

## Timeline

- `2026-05-31T12:47:51+03:30` - Created plan after confirming the vendor gap and current route count.
- `2026-05-31T12:51:51+03:30` - Updated `alaa-golang` to route `golang-how-to`, added the orchestration reference, and validated the slice.

## Validation evidence

- `python C:\Users\CIT\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\sohrab\alaa-golang` passed with `Skill is valid!`
- `python scripts\validate_sohrab_skill_pack.py` passed with existing body-length warnings in unrelated skills.
- Semantic vendor route audit passed with `vendor=43 routed=43 missing=0 extra=0`.
- `git diff --check` passed.
- `rg -n "[ \t]+$"` on the new files returned no trailing-whitespace matches.

## Done / Remaining

### Done

- Added the new vendor `golang-how-to` route.
- Added Alaa-aware primary plus secondary skill orchestration guidance.
- Linked the new reference from `SKILL.md`, the topic map, the full guide, and gap coverage.
- Updated `agents/openai.yaml` so the default prompt nudges agents through `$golang-how-to` while keeping `$alaa-golang` active.
- Updated durable state for future continuation.

### Remaining

- None.
