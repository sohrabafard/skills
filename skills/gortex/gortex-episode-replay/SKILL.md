---
name: gortex-episode-replay
description: "Reconstruct what changed in a window (postmortem, release, PR)."
---

<!-- Adapted from Gortex v0.64.8 generated skills; see ../provenance.json and ../LICENSE.md. -->

# Replay a Change Episode with Gortex

1. Run `analyze({kind: "replay", options: {from: "<start>", to: "<end>"}})` for the requested window.
2. Project the relevant diff with `change({operation: "detect", source: {scope: "<scope>"}})`.
3. Resolve prior decisions through the established memory owner selected by /alaa-code-routing-gortex; corroborate them against current source.
4. Trace important before/after paths using `trace` and identify which change altered behavior.
5. Produce a timestamped narrative with evidence links, impact, missed signals, and remaining uncertainty.

## Shared execution contract

Before the task recipe, read /alaa-code-routing-gortex. It owns repository/view identity, capability and freshness checks, guarded mutation, bounded fallback, memory routing and native proof. Apply the recipe only to supported operations within the authorized task; a skill invocation grants no installation, service, index, write or delegation authority. Return the recipe's evidence and remaining coverage gaps; stop dependent work when its required evidence or safe operation is unavailable.

## When NOT to use

Use /alaa-code-routing-gortex for evidence-owner selection; this skill supplies only its named task recipe. Do not use it to authorize unrelated changes or claim runtime success from graph output.
