---
name: gortex-pr-review-agent
description: "Coding-agent review verdict via the gortex review verb."
---

<!-- Adapted from Gortex v0.64.8 generated skills; see ../provenance.json and ../LICENSE.md. -->

# Review a Change as a Sub-Agent

## MCP-capable harness

Call `review({operation: "run", source: {scope: "<scope>"}})`, then use `change` operations `guards`, `tests`, and `contract`. When the proposed signature is known, run operation `verify` before mutation. If callable tools are unavailable, follow the routing owner's bounded failure procedure; the Bash-only path below is not an outage workaround.

## Bash-only harness

Use this path only when the harness has no MCP transport by design:

```bash
gortex review --audience agent --format json
```

In either mode, return `VERDICT: clean` or `VERDICT: findings` followed by actionable findings with severity and `file:line`. Distinguish graph-backed findings from native diff evidence and incomplete coverage.

## Shared execution contract

Before the task recipe, read /alaa-code-routing-gortex. It owns repository/view identity, capability and freshness checks, guarded mutation, bounded fallback, memory routing and native proof. Apply the recipe only to supported operations within the authorized task; a skill invocation grants no installation, service, index, write or delegation authority. Return the recipe's evidence and remaining coverage gaps; stop dependent work when its required evidence or safe operation is unavailable.

## When NOT to use

Use /alaa-code-routing-gortex for evidence-owner selection; this skill supplies only its named task recipe. Do not use it to authorize unrelated changes or claim runtime success from graph output.
