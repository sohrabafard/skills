# Alaa Services Contract Topic Map

Use this file to choose the smallest relevant section in `./full-guide.md`.

## Covered sections

- `# Purpose`
- `# When to use`
- `# Companion skill routing (mandatory)`
- `# Execution order for agents`
- `# Core service contract`
- `## Canonical service identity`
- `## Route family expectations`
- `## Operational caller expectations`
- `## Service-specific infrastructure modeling`
- `# Health and readiness contract`
- `## /api/health`
- `## /api/ready`
- `## Canonical check naming`
- `## Failure and code rules`
- `## Observability alignment`
- `## Laravel baseline for health and readiness`
- `# Inter-service HTTP and context`
- `## Baseline flow`
- `## Trust-boundary handoff`
- `## Correlation and probe traceability`
- `## Readiness boundaries`
- `## HTTP contract discipline`
- `# Laravel service rules`
- `## Scope`
- `## Core rule`
- `## Default behavior`
- `## Latest Laravel guidance worth using`
- `## Boundary rules`
- `## Testing and docs alignment`
- `## Auth reference precedent`
- `# Service implementation checklist`
- `# Review checklist for agents`
- `# Anti-patterns`

## Working rule

- Read only the sections you need from `./full-guide.md`.
- Keep this topic map small and update it when major sections are added or renamed.
- Keep the top-level contract framework-agnostic and scope Laravel-only rules explicitly.
