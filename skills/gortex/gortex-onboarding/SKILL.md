---
name: gortex-onboarding
description: "Structured tour of an unfamiliar repo."
---

<!-- Adapted from Gortex v0.64.8 generated skills; see ../provenance.json and ../LICENSE.md. -->

# Onboard to a Repository with Gortex

1. Call `explore({operation: "outline"})`, then `explore({operation: "task", task: "explain the repository's main responsibilities and entry points"})`.
2. Run `analyze` with kinds `architecture`, `communities`, and `processes`.
3. Trace one representative request or job with `trace({operation: "call_chain", target: {symbol: "<entry-id>"}})`.
4. Read only the key returned symbols. Deliver a concise map of entry points, boundaries, data flow, tests, and operational risks.

## Shared execution contract

Before the task recipe, read /alaa-code-routing-gortex. It owns repository/view identity, capability and freshness checks, guarded mutation, bounded fallback, memory routing and native proof. Apply the recipe only to supported operations within the authorized task; a skill invocation grants no installation, service, index, write or delegation authority. Return the recipe's evidence and remaining coverage gaps; stop dependent work when its required evidence or safe operation is unavailable.

## When NOT to use

Use /alaa-code-routing-gortex for evidence-owner selection; this skill supplies only its named task recipe. Do not use it to authorize unrelated changes or claim runtime success from graph output.
