---
name: gortex-architecture-review
description: "Graph-grounded architectural read of a repo."
---

<!-- Adapted from Gortex v0.64.8 generated skills; see ../provenance.json and ../LICENSE.md. -->

# Review Architecture with Gortex

1. Build the map with `explore({operation: "outline"})` and `analyze` kinds `architecture` and `communities`.
2. Measure boundaries with `analyze({kind: "coupling"})` and cycles with `analyze({kind: "cycles"})`.
3. Trace representative paths with `trace` and inspect public boundaries with `analyze({kind: "contracts", options: {action: "list"}})`.
4. Deliver observed structure, intended structure, violations, consequences, and prioritized changes. Cite graph evidence for every finding.

## Shared execution contract

Before the task recipe, read /alaa-code-routing-gortex. It owns repository/view identity, capability and freshness checks, guarded mutation, bounded fallback, memory routing and native proof. Apply the recipe only to supported operations within the authorized task; a skill invocation grants no installation, service, index, write or delegation authority. Return the recipe's evidence and remaining coverage gaps; stop dependent work when its required evidence or safe operation is unavailable.

## When NOT to use

Use /alaa-code-routing-gortex for evidence-owner selection; this skill supplies only its named task recipe. Do not use it to authorize unrelated changes or claim runtime success from graph output.
