# Alaa Laravel Architecture Topic Map

Use this file to choose the smallest relevant section in `full-guide.md`.

## Covered sections

- `# Purpose`
- `# Companion skill boundary`
- `# When to use`
- `# Constraints`
- `# Laravel 13 architecture stance`
- `# Architecture rules (strict)`
- `## Layering responsibilities`
- `## Allowed flow`
- `## Not allowed`
- `# API contracts (default Alaa/comment-service shape)`
- `## Request validation (mandatory)`
- `## Success envelope (mandatory)`
- `## Error envelope (stable code + safe message)`
- `### Error rules`
- `## Public ID policy (mandatory)`
- `## Persistence naming vs public contract naming`
- `## Pagination & filtering`
- `# Naming conventions (default)`
- `# Event-driven & outbox rules (Laravel layer)`
- `## Domain events`
- `## Listeners`
- `## Outbox pattern (if present in the repo)`
- `## Optional realtime`
- `## Observers vs Events`
- `## AuthorizationDenied event (observability hint)`
- `# Recommended workflow (deterministic)`
- `# Anti-patterns`

## Working rule

- Read only the sections you need from `full-guide.md`.
- Keep this topic map small and update it when major sections are added or renamed.
