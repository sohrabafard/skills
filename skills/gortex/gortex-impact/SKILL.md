---
name: gortex-impact
description: "Assess what breaks if you change X before editing it."
---

<!-- Adapted from Gortex v0.64.8 generated skills; see ../provenance.json and ../LICENSE.md. -->

# Assess Change Impact with Gortex

1. Resolve the target with `search({operation: "symbols", query: "<name>"})`.
2. Query `relations` operations `usages`, `dependents`, and `implementations` for the resolved symbol.
3. Call `change({operation: "impact", source: {symbols: ["<id>"]}})`; add operation `api_impact` for a public API.
4. For a signature change, require `change({operation: "verify", source: {changes: [{symbol_id: "<id>", new_signature: "<signature>"}]}})`.
5. Report direct callers, transitive risk, interfaces, contracts, and the tests returned by `change({operation: "tests", source: {symbols: ["<id>"]}})`.

## Shared execution contract

Before the task recipe, read /alaa-code-routing-gortex. It owns repository/view identity, capability and freshness checks, guarded mutation, bounded fallback, memory routing and native proof. Apply the recipe only to supported operations within the authorized task; a skill invocation grants no installation, service, index, write or delegation authority. Return the recipe's evidence and remaining coverage gaps; stop dependent work when its required evidence or safe operation is unavailable.

## When NOT to use

Use /alaa-code-routing-gortex for evidence-owner selection; this skill supplies only its named task recipe. Do not use it to authorize unrelated changes or claim runtime success from graph output.
