# Skill-pack optimization change notes

This candidate updates 254 first-party skill-pack paths. The product manifest is `24aa88d79f4e483bac8946d045b5e4486f1d2c5847027350d620abd70bc8b878`. See the [optimization plan](../../docs/_agent_plans/20261018-000000_skill-pack-optimization.md), [proposal dispositions](./proposal-dispositions.md), and [final candidate manifest](./final-candidate.json) for scope and evidence navigation.

## Workflow cadence

The workflow now distinguishes a Beads-backed phase/task/subtask hierarchy from a direct, single-phase, nondelegated local plan. The bounded local exception remains available. New phased or delegated work requires an explicit Beads binding and the hierarchy; existing local, flat, and schema-2 history remains readable under its compatibility rules.

Task owners provide focused acceptance evidence. Independent review and commit stay at the inherited phase or whole-engagement boundary. Nested work inherits that boundary and final candidate; it cannot reset review cadence. Covered aggregate evidence may discharge narrower checks only when inputs, environment, flags, and required observer match. The workflow and mirrored orchestrators own details: read the [workflow lifecycle](../../skills/sohrab/alaa-workflow/references/artifact-lifecycle.md) for admission and state, and the [orchestrator verification contract](../../skills/sohrab/alaa-codex-orchestrator/references/verification-and-gates.md) when scheduling review or gates.

External topic maps remain in place, including the Bash map. A short triggered pointer routes readers to them; reference count alone does not justify moving their content into an always-loaded skill body.

## Compatibility and rollout

New hierarchy snapshots use schema 3 and preserve an exact phase/task/subtask cursor. Nested execution treats `Final phase` as the engagement boundary and `Local final phase` as the child's last local phase. Older families remain readable; rollback freezes execution of marked or nested families until compatible consumers return. Do not silently backfill or migrate authority. Read the [schema review](./review-schema.md) before changing consumers or rollback behavior.

The workflow CLI keeps direct one-phase plans distinct from phased/delegated plans, and requires explicit Beads binding for new phased/delegated work. Follow the [workflow skill](../../skills/sohrab/alaa-workflow/SKILL.md) and repository [Beads binding](../../AGENTS.md#beads) for invocation and live issue authority. Offline validation does not establish live Beads registration, readiness, installed activation, or agent compliance.

## Measured scope and limits

Across 46 recorded skill-body measurements, the net source UTF-8 body delta is **−17,878 bytes**. This is a source-size measurement only; no speed, context, cost, or runtime-compliance improvement is claimed. The three earlier reports ([contradictions](../skill-pack-review-20261018/01-contradictions-and-overlaps.md), [optimization](../skill-pack-review-20261018/02-optimization.md), and [new-skill proposals](../skill-pack-review-20261018/03-new-skill-proposals.md)) are empty; item evidence remains in the [intake snapshot](./intake-snapshot.json) and disposition register.

Independent review findings are resolved in the [clearance record](./review-clearance.md). Native acceptance evidence is recorded separately through the active plan's verification evidence. Review clearance alone does not establish release readiness.
