## Goal
Extend `alaa-trust-gateway-auth` so it captures the auth project's concrete API contract, request sequencing, and implementation guidance from the auth repo's Postman/docs, and strengthen the skill so agents explicitly read companion skills before doing related work.

## Assumptions
- The auth project exists in a nearby workspace and is readable with escalated shell access.
- The auth project's Postman collections and docs are more authoritative for API flow than older assumptions.
- The target edit is limited to `skills/sohrab/alaa-trust-gateway-auth/` unless related references are clearly needed.

## Constraints
- Preserve the existing trust model and error contract unless auth-repo evidence requires additive clarification.
- Prefer minimal, reviewable edits to the skill rather than broad rewrites.
- Keep companion-skill guidance explicit enough that agents do not skip the prerequisite skill reads.

## Closest existing patterns
- `skills/sohrab/alaa-trust-gateway-auth/SKILL.md`
- `skills/sohrab/alaa-workflow/SKILL.md`
- `skills/sohrab/alaa-security-review/SKILL.md`
- `skills/sohrab/alaa-laravel-architecture/SKILL.md`

## Phases (with dependencies)
1. Discover auth project materials
Inputs it depends on: auth repo path, readable docs/Postman/routes
Output artifacts: notes on endpoint contract, route shapes, and request order
Validation: confirm endpoint and flow facts are grounded in auth repo files
Not parallel-safe

2. Gap analysis against the current skill
Inputs it depends on: current `alaa-trust-gateway-auth` skill, auth repo findings
Output artifacts: concrete list of missing sections and wording changes
Validation: each planned addition maps back to an auth repo source
Parallel-safe

3. Patch the skill
Inputs it depends on: phases 1-2
Output artifacts: updated `SKILL.md` and any needed companion reference text
Validation: read back the edited sections and confirm the trust model still stays internally consistent
Not parallel-safe

4. Final review
Inputs it depends on: patched skill
Output artifacts: concise summary of what the skill now teaches and any remaining auth-repo follow-ups
Validation: verify the skill now covers endpoint contract, request order, and companion skill invocation
Parallel-safe

## Parallel-safe work split
- Auth repo discovery and local skill gap analysis can overlap mentally, but file edits should wait until the auth evidence is collected.

## Commands to run
- Read auth repo Postman collection(s)
- Read auth repo docs/README/OpenAPI if present
- Read auth repo route declarations or controller docs for auth endpoints
- Read back the updated `alaa-trust-gateway-auth/SKILL.md`

## Files touched (append-only log)
- `docs/_agent_plans/20260321-000000_alaa-trust-gateway-auth.md`
- `skills/sohrab/alaa-trust-gateway-auth/SKILL.md`

## Done / Remaining
- Done: created plan anchor
- Done: inspected auth repo docs, Postman, routes, and request validators
- Done: patched `alaa-trust-gateway-auth` with concrete auth-service flow and companion-skill routing rules
- Remaining: optional follow-up review against the gateway repo once route drift changes are applied
