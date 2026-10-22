---
name: gortex-co-change
description: "Find what changes together and hidden coupling."
---

<!-- Adapted from Gortex v0.64.8 generated skills; see ../provenance.json and ../LICENSE.md. -->

# Analyze Co-Change with Gortex

1. Resolve the anchor with `search({operation: "symbols", query: "<name>"})`.
2. Call symbol-scoped `analyze({kind: "co_change", target: {symbol: "<id>"}})` and repository-wide `analyze({kind: "churn"})`.
3. Compare structural coupling through `relations` operations `cluster` and `dependents`.
4. Report strong historical pairs, graph-confirmed dependencies, likely hidden coupling, and an actionable boundary or guard.

## Shared execution contract

Before the task recipe, read /alaa-code-routing-gortex. It owns repository/view identity, capability and freshness checks, guarded mutation, bounded fallback, memory routing and native proof. Apply the recipe only to supported operations within the authorized task; a skill invocation grants no installation, service, index, write or delegation authority. Return the recipe's evidence and remaining coverage gaps; stop dependent work when its required evidence or safe operation is unavailable.

## When NOT to use

Use /alaa-code-routing-gortex for evidence-owner selection; this skill supplies only its named task recipe. Do not use it to authorize unrelated changes or claim runtime success from graph output.
