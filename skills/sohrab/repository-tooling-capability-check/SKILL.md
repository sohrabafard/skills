---
name: repository-tooling-capability-check
description: Verify CodeGraph, Codex hook/approval scope, and Hindsight connectivity in a worktree with live evidence rather than configuration-only claims.
argument-hint: "[worktree path]"
user-invocable: false
allowed-tools: Read, Grep, Glob, Bash
---

# Repository Tooling Capability Check

## When to use

Use for questions such as “is CodeGraph active?”, “does this Codex hook need approval?”, or “can Hindsight connect now?” in a repository.

## When NOT to use

Do not use it to configure, upgrade, or remove those systems unless that work is explicitly requested.

## Inputs / context to gather

1. Resolve the target worktree: `$ARGUMENTS` or the current directory.
2. Identify whether the question concerns CodeGraph, hooks/approval, Hindsight, or all three.
3. Capture only current-session evidence; index state, tool exposure, and configuration are checkout/session-specific.

## Procedure

1. For CodeGraph, inspect the available MCP tool surface and `.codegraph` at the worktree. If `codegraph_explore` is available, run one meaningful structural query using exact symbols or filenames when known.
2. If the result says no `.codegraph`/not indexed, stop CodeGraph attempts for that session and use Read/Grep/Glob. Mention `codegraph init` only as the user-controlled indexing action.
3. For hooks, inspect active project sources (`.codex/hooks.json`, `.codex/config.toml`) plus relevant Git configuration such as `core.hooksPath`. Distinguish active configuration from templates, global feature flags, and Git hooks.
4. If approval behavior is in scope, inspect the active hook’s approval/trust evidence. State separately what project files establish and what remains runtime/user-scope policy.
5. For Hindsight, inspect active tool names/descriptions and MCP resources/templates. Then inspect project wiring only as supporting evidence: `.hindsight`, `.mcp.json`, `.codex/config.toml`, `.codex/hooks.json`, and launcher/doctor scripts where present.
6. Where a project exposes `node .hindsight/doctor.cjs`, run it for configuration, dependency, authentication, and handshake diagnostics. Do not print credentials. A live-connectivity claim requires an exposed working tool or successful handshake, not config/API reachability alone.
7. Report per capability: evidence checked, outcome, precise scope, and the smallest next action when unavailable.

## Efficiency plan

1. Use one repository scan for the named configuration paths and one tool inventory check before opening broader documentation.
2. For CodeGraph, query once with exact identifiers; do not retry semantic wording after a no-index result.
3. Reuse the same evidence matrix: index/tool/query; active hook/trust; Hindsight tool/resources/config/doctor/handshake.
4. Stop once the requested capability is proven or disproven at the stated scope; do not turn a check into setup work.

## Pitfalls and fixes

- Missing `codegraph` CLI -> MCP can still be active; test `codegraph_explore` before concluding it is unavailable.
- Broad natural-language CodeGraph result -> retry with exact symbols/files; treat unrelated lexical source only as smoke-query evidence.
- Template or `features.hooks = true` -> not an active project hook; find the effective source and trust state.
- Git pre-commit hook -> not a Codex approval hook; report it separately.
- `ACTIVE_ADAPTER: hindsight`, `.env`, or a reachable API -> not a live memory connection; require tool exposure and successful operation/handshake.
- `mcp-server.js is not installed` or HTTP 401 -> install dependencies/configure the token through approved secret handling, then rerun the doctor; never store or print the token.

## Verification checklist

- A CodeGraph conclusion includes index status and, when indexed, a meaningful live query.
- A hook conclusion names the active configuration scope and distinguishes Git/template/global sources.
- A Hindsight conclusion states whether tools/resources were exposed and whether a doctor/handshake was successful.
- The report labels all session-/checkout-specific evidence and does not claim unavailable memory is empty.
