---
name: gortex-refactor
description: "Rename, extract, split, or restructure code safely."
---

<!-- Adapted from Gortex v0.64.8 generated skills; see ../provenance.json and ../LICENSE.md. -->

# Refactor with Gortex

1. Call `explore({operation: "task", task: "<refactor goal>"})` and resolve every target with `search`.
2. Run `change({operation: "impact", source: {symbols: ["<id>"]}})`. Before altering a signature, also run `change({operation: "verify", source: {changes: [{symbol_id: "<id>", new_signature: "<signature>"}]}})`.
3. Choose exactly one `refactor` operation: `rename`, `move`, `inline`, `delete`, or `apply_code_action`. For example: `refactor({operation: "rename", target: {symbol: "<id>"}, new_name: "<name>"})`.
4. Require `change` operations `detect`, `tests`, `guards`, and `contract` after the mutation. Resolve every violation before finishing.

## Shared execution contract

Before the task recipe, read /alaa-code-routing-gortex. It owns repository/view identity, capability and freshness checks, guarded mutation, bounded fallback, memory routing and native proof. Apply the recipe only to supported operations within the authorized task; a skill invocation grants no installation, service, index, write or delegation authority. Return the recipe's evidence and remaining coverage gaps; stop dependent work when its required evidence or safe operation is unavailable.

## When NOT to use

Use /alaa-code-routing-gortex for evidence-owner selection; this skill supplies only its named task recipe. Do not use it to authorize unrelated changes or claim runtime success from graph output.
