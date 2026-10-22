---
name: gortex-rename
description: "Rename a symbol and update every reference atomically."
---

<!-- Adapted from Gortex v0.64.8 generated skills; see ../provenance.json and ../LICENSE.md. -->

# Rename a Symbol with Gortex

1. Resolve exactly one symbol with `search({operation: "symbols", query: "<old name>"})`.
2. Enumerate references and implementations with `relations` operations `usages` and `implementations`.
3. Run `change({operation: "impact", source: {symbols: ["<id>"]}})`. For a public signature rename, also run `change({operation: "verify", source: {changes: [{symbol_id: "<id>", new_signature: "<signature with new name>"}]}})`.
4. Preview with `refactor({operation: "rename", target: {symbol: "<id>"}, new_name: "<new>", dry_run: true})`, then repeat it with `dry_run: false` to apply.
5. Require `change` operations `detect`, `guards`, and `tests`; confirm no old usages remain.

## Shared execution contract

Before the task recipe, read /alaa-code-routing-gortex. It owns repository/view identity, capability and freshness checks, guarded mutation, bounded fallback, memory routing and native proof. Apply the recipe only to supported operations within the authorized task; a skill invocation grants no installation, service, index, write or delegation authority. Return the recipe's evidence and remaining coverage gaps; stop dependent work when its required evidence or safe operation is unavailable.

## When NOT to use

Use /alaa-code-routing-gortex for evidence-owner selection; this skill supplies only its named task recipe. Do not use it to authorize unrelated changes or claim runtime success from graph output.
