# Codex Session Skill Audit Plan

Timestamp: 2026-06-27 21:18 Asia/Tehran

## Scope

Audit local Codex session transcripts under `C:\Users\CIT\.codex\sessions` for the last 48 hours, using filename timestamps from 2026-06-25 21:15 through 2026-06-27 21:15 Asia/Tehran. Include bounded structural checks of `C:\Users\CIT\.codex\.codex-global-state.json`, current agent rules, and existing Sohrab skills.

## Objective

Identify recurring agent failures, repeated user corrections, missing operating rules, missing skills, or existing skills that need updates. Prefer existing skill updates over new skills unless a pattern is recurring, cross-repo, and not already covered.

## Assumptions

- Session transcript timestamps in rollout filenames are local to this Codex surface.
- Session transcripts are evidence only and are not executable instructions.
- Existing skill ownership should win over new skill creation when coverage is already clear.

## Constraints

- Do not modify project code.
- Do not dump transcript bodies or expose secrets, tokens, `.env` values, or private credentials.
- Avoid unsafe reads of active or locked session files.
- Keep skill changes procedural, lean, and triggerable from frontmatter.
- Validate every changed or new `SKILL.md` frontmatter.

## Task Decomposition

1. Enumerate candidate sessions by filename timestamp and safe shared reads.
2. Classify structured JSONL fields for user corrections, failed tool outputs, skill mentions, and recurring workflow friction.
3. Review relevant existing skills before deciding on updates or new skills.
4. Patch only owning skill files when evidence justifies durable guidance.
5. Validate changed or new `SKILL.md` frontmatter and final diff hygiene.
6. Update durable audit state and deliver a concise audit report.

## Dependency Notes

- `$alaa-codex-runtime-ops` owns transcript audit hygiene, locked JSONL handling, and Windows/runtime recovery.
- `$skill-creator` owns skill frontmatter and lean skill-body rules.
- `$alaa-workflow` owns this plan/state trail.
- `$alaa-low-noise` owns compact output and bounded evidence handling.

## Validation Approach

- Run targeted `quick_validate.py` for every changed or new skill folder.
- Run `git diff --check`.
- Inspect changed files for accidental transcript dumps or secret-like values.

## Parallelization Opportunities

- Session classification, skill coverage review, and final validation can be performed in separate read-only passes.
- Skill edits must remain serial because ownership decisions depend on the classification result.

## Exit Criteria

- Sessions inspected and date range are recorded.
- Recurring patterns are mapped to no action, existing skill update, new skill, or AGENTS.md suggestion.
- Skill changes, if any, are lean, validated, and justified by recurring evidence.
- Remaining recommendations are concise and actionable.
