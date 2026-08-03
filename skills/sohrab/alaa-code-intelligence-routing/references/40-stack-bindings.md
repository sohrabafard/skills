# Stack fast paths

These rows select evidence owners. The named stack skill still owns implementation doctrine.

## Laravel

Three servers, and the failure to avoid is asking the wrong one and then paying for a grep sweep to
recover. The split is by question, not by preference.

Framework and package questions go to Laravel Boost first, and this is the row most often skipped.
`search-docs` answers against the versions this project actually installed, so an API written from it is
right the first time instead of right for whichever major the model remembers; `application-info`
supplies those versions and the installed package list. Reading one framework file, or inferring a
signature, is the more expensive path and it is also the one that produces a review cycle. Reach for
Boost before reading `vendor/`, and before assuming a convention.

Structure goes to CodeGraph and exact semantics go to Serena, unchanged by the presence of Boost:
neither of them knows what the framework does, and Boost does not know how this application is wired.

| Question | Owner |
|---|---|
| Where is the behavior, what symbols are related, what is the route-to-handler and downstream call path, who calls whom, what is the likely blast radius, and which files should be read? | CodeGraph in a healthy index |
| What is the outline of this known PHP file, where is this declaration, what references it, what diagnostics apply, or how should this symbol be renamed or edited semantically? | Serena when the PHP backend is configured and healthy |
| What does the installed framework or package do, what is its current signature, and what convention applies? | Boost `search-docs`, before reading `vendor/` and before inferring |
| Which framework and package versions are installed here? | Boost `application-info`, which is what makes any other answer version-correct |
| Which routes are registered, and what URL does this route or path resolve to? | `php artisan route:list`, or Boost `get-absolute-url` for one resolution |
| What is the live schema, and which connections exist? | Boost `database-schema` and `database-connections` |
| What just failed, and what does the application or browser log say? | Boost `last-error`, `read-log-entries`, `browser-logs` |
| Did the change work? | Repository-native Laravel gates |

Serena cannot see inside `vendor/` unless the project has explicitly enabled it, and the empty result it
returns for a framework symbol is indistinguishable from a true negative. Treat an empty semantic result
on a framework name as unknown rather than absent, and re-ask Boost.

Laravel Boost does not own source call graphs or symbol refactors. CodeGraph and Serena do not prove runtime registration, framework behavior, database state, or completion.

Boost's own surface is not uniform in authority, and a read-only label on it is a claim rather than a boundary. Its documentation and application-metadata tools are safe to reach for early and are usually the cheapest correct answer for a framework question. Its query tool returns whatever the application can read, including data a lane has no reason to see, and its guard is a statement-keyword check rather than a database-level restriction. Two further tools are not evidence surfaces at all: one executes arbitrary application code, and one writes durable rule files that other agents then follow. Verify environment and statement effect before any Boost database operation, and keep code execution and rule writing out of every lane whose contract is to observe or to judge.

Implementation doctrine routes to `/alaa-laravel-architecture` in Claude Code or `$alaa-laravel-architecture` in Codex and the other Laravel owners named by that skill.

## Go

Use CodeGraph for unknown package location, source flow, relationships, and likely impact. `/alaa-golang` in Claude Code or `$alaa-golang` in Codex owns the semantic interface for definitions, references, hierarchy, diagnostics, and Go-aware edits and routes those questions to its gopls owner. Do not enable Serena merely to duplicate that owner. A project may select Serena only for a measured recurring gap that `/alaa-golang` does not cover and records that exception in its binding. Native Go commands and repository gates own proof.

## Vue and Quasar

Use CodeGraph for unknown page, route, component, composable, store, API-client, and static integration flow. Use Serena for a known Vue or TypeScript symbol only when the configured Vue backend exposes the required semantics and no project skill names another semantic owner. Do not add a second TypeScript backend merely because TypeScript files exist; use the project-generated Serena configuration and health result as authority. Browser evidence owns runtime UI behavior, and repository-native frontend gates own proof. Implementation doctrine routes to `/alaa-frontend-developer` or `$alaa-frontend-developer` and `/alaa-vue-typescript-clean-code` or `$alaa-vue-typescript-clean-code`.

## Other source repositories

CodeGraph owns unknown structural discovery in supported indexed source. The stack-declared semantic owner, otherwise configured Serena, owns known-symbol semantics and edits. The stack skill owns implementation doctrine. Native commands own proof. Unsupported or unindexed languages route to their language-native owner and retain a partial label when broad-flow or semantic guarantees are lost.
