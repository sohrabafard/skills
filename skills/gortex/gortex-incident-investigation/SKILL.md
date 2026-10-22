---
name: gortex-incident-investigation
description: "Walk a production symptom back to its root cause."
---

<!-- Adapted from Gortex v0.64.8 generated skills; see ../provenance.json and ../LICENSE.md. -->

# Investigate an Incident with Gortex

1. Paste the exact symptom into `explore({operation: "task", task: "<alert, error, and time window>"})`.
2. Search exact error text with `search({operation: "text", query: "<literal>"})`.
3. Walk `relations` operation `callers` and `trace` operations `call_chain`, `flow`, or `taint` from symptom toward cause.
4. Correlate repository-wide `analyze({kind: "recent_changes"})` with prior decisions from the established memory owner selected by /alaa-code-routing-gortex.
5. Separate evidence, hypothesis, and unknowns. Gate any fix through `change` before and after the mutation.

## Shared execution contract

Before the task recipe, read /alaa-code-routing-gortex. It owns repository/view identity, capability and freshness checks, guarded mutation, bounded fallback, memory routing and native proof. Apply the recipe only to supported operations within the authorized task; a skill invocation grants no installation, service, index, write or delegation authority. Return the recipe's evidence and remaining coverage gaps; stop dependent work when its required evidence or safe operation is unavailable.

## When NOT to use

Use /alaa-code-routing-gortex for evidence-owner selection; this skill supplies only its named task recipe. Do not use it to authorize unrelated changes or claim runtime success from graph output.
