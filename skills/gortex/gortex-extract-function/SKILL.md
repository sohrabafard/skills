---
name: gortex-extract-function
description: "Extract code into a function or method via LSP refactor."
---

<!-- Adapted from Gortex v0.64.8 generated skills; see ../provenance.json and ../LICENSE.md. -->

# Extract a Function with Gortex

1. Inspect the file with `read({operation: "editing_context", target: {file: "<path>"}})`.
2. Resolve the selected range with `change({operation: "ranges", source: {file: "<path>", range: {...}}})`.
3. Request extraction actions with `change({operation: "code_actions", source: {file: "<path>", range: {...}}})`.
4. Apply the selected action through `refactor({operation: "apply_code_action", target: {file: "<path>"}, options: {...}})`.
5. Run `change` operations `detect`, `tests`, `guards`, and `contract`.

## Shared execution contract

Before the task recipe, read /alaa-code-routing-gortex. It owns repository/view identity, capability and freshness checks, guarded mutation, bounded fallback, memory routing and native proof. Apply the recipe only to supported operations within the authorized task; a skill invocation grants no installation, service, index, write or delegation authority. Return the recipe's evidence and remaining coverage gaps; stop dependent work when its required evidence or safe operation is unavailable.

## When NOT to use

Use /alaa-code-routing-gortex for evidence-owner selection; this skill supplies only its named task recipe. Do not use it to authorize unrelated changes or claim runtime success from graph output.
