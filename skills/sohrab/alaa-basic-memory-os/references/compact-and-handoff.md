# Compact And Handoff

## Rule

For long work, write semantic state before context compaction can hurt continuity.

## Preferred state owner

`alaa-workflow` repo-local state is authoritative for active execution.

## Basic Memory handoff pointer

A handoff pointer should include:

- objective
- verified current state
- repo-local plan/state paths
- validation run and result
- next action
- risks/questions

Do not store raw transcript tails by default.

## PreCompact hook

Use `scripts/precompact_checkpoint.ps1` as an emergency checkpoint only. It stores metadata and git status by default, not raw transcript content.
