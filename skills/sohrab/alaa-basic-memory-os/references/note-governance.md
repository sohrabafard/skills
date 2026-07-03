# Note Governance

## Required frontmatter

```yaml
title:
type:
status:
confidence:
permalink:
tags:
canonical_source_paths:
last_verified:
```

Use `last_curated` for lessons/patterns from processed evidence.

## Status values

- `draft`
- `active`
- `needs_review`
- `stale`
- `archived`
- `superseded`

## Confidence values

- `low`
- `medium`
- `high`

## Observation labels

Use concise bullets under `## Observations` with labels such as `[rule]`, `[decision]`, `[ownership]`, `[contract]`, `[risk]`, `[validation]`, `[source]`, `[lesson]`, `[anti_pattern]`, `[boundary]`, `[todo]`, `[question]`, `[gap]`, `[proposal]`, `[draft_contract]`, and `[decision_needed]`.

## Relations

Use typed wiki links under `## Relations`:

```md
- governs [[Notification Command Contract]]
- depends_on [[Service Ownership Matrix]]
- relates_to [[Observability SOC Rules]]
```

## Extraction Mode

Extract only source-backed facts. Mark gaps.

## Design Mode

Only when explicitly requested. Proposed values are not canonical and must be labeled.
