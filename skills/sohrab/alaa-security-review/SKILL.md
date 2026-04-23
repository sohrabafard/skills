---
name: alaa-security-review
description: "Use this skill when the task involves authn or authz changes or tenant-isolation or trust-boundary review. Do not use it when pure style cleanup with no trust impact."
---




# Alaa Security Review

## Purpose

Use this skill when the task needs the architectural or policy guidance owned by Alaa Security Review.

Keep this top-level file small. Load the references for the full rules, examples, and checklists.

## When to use

- authn or authz changes
- tenant-isolation or trust-boundary review
- validation, file, URL, or secret handling changes
- security review requests before merge

## When NOT to use

- pure style cleanup with no trust impact
- non-security docs-only work

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Apply `$alaa-low-noise` when the task is non-trivial.
3. Read `references/00-topic-map.md`.
4. Load only the sections you need from `references/full-guide.md`.
5. Pair with the listed companion skills before making changes outside this skill's ownership.

## Trust-boundary checklist

- Input boundary: validate and normalize untrusted input before business logic.
- Identity boundary: confirm who authenticated the actor and what is trusted downstream.
- Tenant boundary: verify tenant derivation, isolation, and cross-tenant exceptions.
- File boundary: re-check upload, storage, and retrieval trust assumptions.
- Queue boundary: confirm idempotency, poison handling, and producer/consumer trust.
- Secret boundary: confirm storage, rotation, masking, and runtime exposure rules.

## Companion routing

- $alaa-trust-gateway-auth
  - Pair when the task also touches gateway and trusted-header security context.
- $alaa-observability-soc
  - Pair when the task also touches security logging, traceability, and incident evidence.

## Reference navigation

- Section map and fast routing:
  - `references/00-topic-map.md`
- Full preserved guidance, rules, examples, and checklists:
  - `references/full-guide.md`
- Official-first source map, freshness triggers, and community-source limits:
  - `references/90-source-map.md`

## Maintenance rules

- Keep this file routing-first and plain.
- Put detailed rules into `references/full-guide.md` instead of growing this file.
- Keep the topic map aligned with the actual headings in the full guide.
- Re-check companion-skill routing when ownership boundaries change.
