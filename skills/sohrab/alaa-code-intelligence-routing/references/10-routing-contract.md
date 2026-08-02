# Evidence-owner routing contract

Choose one primary owner for the current question. Evidence, edit, runtime observation, and proof may have different owners because they answer different questions.

## Decision order

1. Name the question: structural discovery, exact semantics, semantic edit, prose, effective configuration, generated output, runtime fact, external fact, review risk, or proof.
2. Verify worktree, freshness, generated owner, installed capability, environment, and authority.
3. Select the primary owner from the table and ask only the named question.
4. Record what the result established and stop that owner.
5. Open one secondary owner only for one recorded missing fact.
6. Treat the transition to editing, runtime observation, or proof as a new ordered question rather than repeated discovery.

Parallel retrieval is legal only when separately named questions are independent and neither answer can change the other's owner, scope, authorization, or query.

## Router

| Current question | Primary owner | Secondary only for a named gap |
|---|---|---|
| Unknown location, related symbols, source architecture, route-to-handler source path, callers, callees, execution flow, files to read, or likely impact in healthy indexed source | CodeGraph | One live read for a named stale or uncovered file; semantic owner for one exact symbol fact |
| Known file or symbol: outline, declaration, references, hierarchy, diagnostics, rename, or symbol-scoped edit | Stack-declared semantic owner; otherwise Serena when configured | CodeGraph only when a new wider-flow or impact question appears |
| Small textual change in one named hand-maintained non-semantic file | Native targeted read and patch | Semantic owner only when a separate symbol question appears |
| Laravel routes actually registered in the active application | `php artisan route:list` or an installed Boost inventory surface that proves the same runtime fact | CodeGraph for downstream source flow from a named handler |
| Laravel package or framework behavior and installed-version documentation | Laravel Boost Search Docs | Official source only when Boost lacks the installed package or required version context |
| Authorized Laravel application metadata, logs, schema, or database/runtime context | Installed Laravel Boost surface or repository-native command | CodeGraph to map an observed fact to source; semantic owner for a named symbol |
| Markdown phrase, heading, identifier, or link | Native Markdown-scoped search/read | `/alaa-repo-docs` or `$alaa-repo-docs` for canonical ownership, alignment, authoring, or proof |
| Source comment, docblock, or annotation | `/alaa-frontend-doc-annotations` or `$alaa-frontend-doc-annotations` | Semantic owner for the containing symbol |
| JSON, YAML, TOML, CI, environment template, manifest, or policy text | Native scoped read plus parser or repository checker | Domain owner for effective semantics |
| OpenAPI, AsyncAPI, Postman, protobuf, schema, or another machine-readable contract | Installed contract-owning skill or generator | `/alaa-repo-docs` or `$alaa-repo-docs` for prose only |
| Generated source or generated documentation | Source template and generator | Direct edit only when repository policy declares it hand-maintained |
| Runtime logs, traces, metrics, browser state, queue state, cache state, or database behavior outside Boost | Authorized runtime owner | CodeGraph to map the observation to source |
| Current external framework, package, protocol, or platform behavior | Official version-aware source | Repository evidence for local usage only |
| Current change review | Git diff first | One owner for one named risk, then native gates |
| Cross-repository ownership, consumer, compatibility, or handoff | Authoritative catalog, contract registry, hosting surface, or approved memory surface | A named repository after authority identifies it |
| Behavioral or artifact proof | Repository-native tests, builds, linters, type checks, generators, schema checks, and link checks | None |

## Named-gap record

Before switching owners, record:

- established evidence;
- the missing fact;
- why the primary owner cannot provide it;
- the next owner and the one question it must answer.

Habit, reassurance, tool availability, and independent repetition are not gaps.

## Degraded operation

- CodeGraph names stale or pending files: read only those live files; do not repeat graph discovery.
- An owner is empty, unavailable, or points at another worktree: perform one status, activation, root, or inventory check; do not repeat the evidence query.
- Broad-flow or impact coverage is unavailable: targeted reads may establish a narrower fact, but the broad conclusion remains partial or blocked.
- The semantic owner cannot preserve reference or refactor safety: native reads may provide partial evidence, but do not call them reference-complete or refactor-safe.
- A native proof gate cannot run: report the exact command, blocker, and remaining risk; static evidence is not proof.

## Handoff

Give the receiving agent the established evidence, source worktree, covered scope, freshness state, proof state, and one unresolved question. Prohibit rediscovery of covered files, symbols, flows, documents, and contracts. Route durable state to `/alaa-workflow` in Claude Code or `$alaa-workflow` in Codex; route fan-out mechanics to the installed runtime orchestrator.
