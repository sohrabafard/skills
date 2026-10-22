---
name: gortex-cli
description: "Bash-only mirror of Gortex MCP tools for harnesses without MCP support."
---

<!-- Adapted from Gortex v0.64.8 generated skills; see ../provenance.json and ../LICENSE.md. -->

# Gortex from a Bash-Only Harness

Use this skill only in a harness that has no MCP transport by design. If a Gortex MCP server is configured but its callable tools are missing, report an integration failure; do not use this skill as a fallback.

Every public MCP tool has the same name through `gortex call`:

```bash
gortex call explore --arg task='locate the authentication flow'
gortex call search --arg operation=symbols --arg query=UserStore
gortex call read --arg target='{"symbol":"internal/store.go::UserStore"}'
gortex call relations --arg operation=usages --arg target='{"symbol":"internal/store.go::UserStore"}'
gortex call change --arg operation=impact --arg target='{"symbol":"internal/store.go::UserStore"}'
gortex call edit --arg target='{"file":"internal/store.go"}' --arg match='old text' --arg replacement='new text'
gortex call change --arg operation=detect --arg source='{"scope":"all"}'
```

For an exact operation schema:

```bash
gortex call capabilities --arg domain=read --arg operation=source --arg detail=schema
```

The required order is `explore` → targeted `search/read/relations/trace` → pre-change `change` → `edit/refactor` → post-change `change`.

## Shared execution contract

Before the task recipe, read /alaa-code-routing-gortex. It owns repository/view identity, capability and freshness checks, guarded mutation, bounded fallback, memory routing and native proof. Apply the recipe only to supported operations within the authorized task; a skill invocation grants no installation, service, index, write or delegation authority. Return the recipe's evidence and remaining coverage gaps; stop dependent work when its required evidence or safe operation is unavailable.

## When NOT to use

Use /alaa-code-routing-gortex for evidence-owner selection; this skill supplies only its named task recipe. Do not use it to authorize unrelated changes or claim runtime success from graph output.
