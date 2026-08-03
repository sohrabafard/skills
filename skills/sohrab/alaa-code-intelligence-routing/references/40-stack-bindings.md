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

Implementation doctrine routes to `/alaa-laravel-architecture` in Claude Code or `$alaa-laravel-architecture` in Codex and the other Laravel owners named by that skill.

## Go

Use CodeGraph for unknown package location, source flow, relationships, likely impact, and the files or regions to inspect.

Enable Go in Serena for repositories covered by this pack. Serena is the agent-facing owner for a known Go file or symbol: outline, declaration, references, implementation hierarchy, diagnostics, semantic rename, and symbol-scoped edits. Serena's Go backend uses `gopls`, so the backend is not a parallel evidence owner.

Invoke `/golang-gopls` in Claude Code or `$golang-gopls` in Codex directly only when Serena is unavailable or unhealthy, or after recording one required build-aware, generated-code, dependency-resolution, package-API, or code-action operation that Serena does not expose. Ask direct gopls only that missing question and do not repeat Serena evidence.

Implementation doctrine, framework choice, and package selection remain with `/alaa-golang`, which is the front door for Go and routes onward to the installed Go skills. Native Go commands and repository gates own proof.

## Vue and Quasar

Use CodeGraph for unknown page, route, component, composable, store, API-client, and static integration flow. Use Serena for a known Vue or TypeScript symbol only when the configured Vue backend exposes the required semantics and no project skill names another semantic owner. Do not add a second TypeScript backend merely because TypeScript files exist; use the project-generated Serena configuration and health result as authority. Browser evidence owns runtime UI behavior, and repository-native frontend gates own proof. Implementation doctrine routes to `/alaa-frontend-developer` or `$alaa-frontend-developer` and `/alaa-vue-typescript-clean-code` or `$alaa-vue-typescript-clean-code`.

## Other source repositories

CodeGraph owns unknown structural discovery in supported indexed source. The stack-declared semantic owner, otherwise configured Serena, owns known-symbol semantics and edits. The stack skill owns implementation doctrine. Native commands own proof. Unsupported or unindexed languages route to their language-native owner and retain a partial label when broad-flow or semantic guarantees are lost.
