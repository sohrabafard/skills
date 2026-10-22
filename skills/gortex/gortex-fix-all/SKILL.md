---
name: gortex-fix-all
description: "Clear LSP diagnostics — one error, a file, or source.fixAll."
---

<!-- Adapted from Gortex v0.64.8 generated skills; see ../provenance.json and ../LICENSE.md. -->

# Fix Diagnostics with Gortex

1. Read diagnostics using `change({operation: "diagnostics", source: {file: "<path>"}})`.
2. Fetch applicable fixes with `change({operation: "code_actions", source: {file: "<path>"}})`.
3. Apply one reviewed action with `refactor({operation: "apply_code_action", target: {file: "<path>"}, options: {...}})`, or use operation `fix_all` only when the user asked for all safe fixes.
4. Re-run diagnostics, then run `change` operations `detect` and `tests`.

## Shared execution contract

Before the task recipe, read /alaa-code-routing-gortex. It owns repository/view identity, capability and freshness checks, guarded mutation, bounded fallback, memory routing and native proof. Apply the recipe only to supported operations within the authorized task; a skill invocation grants no installation, service, index, write or delegation authority. Return the recipe's evidence and remaining coverage gaps; stop dependent work when its required evidence or safe operation is unavailable.

## When NOT to use

Use /alaa-code-routing-gortex for evidence-owner selection; this skill supplies only its named task recipe. Do not use it to authorize unrelated changes or claim runtime success from graph output.
