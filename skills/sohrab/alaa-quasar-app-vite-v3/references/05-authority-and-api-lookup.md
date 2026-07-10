# Authority and Installed API Lookup

Use this file when a task needs exact Quasar syntax or when repository, skill, and upstream sources appear to disagree.

## Scope boundary

This skill is a control plane, not a frozen copy of every Quasar API. Its references preserve durable workflow, migration deltas, decision heuristics, security/performance guardrails, and high-value examples. Exact API availability belongs to the target project's installed Quasar line.

## Source ownership

| Question | Primary authority | Fallback |
|---|---|---|
| What does this application currently do? | Live repo code, config, lockfile, tests, and runtime | Maintained repo docs |
| Which Quasar props/events/slots/methods/options exist here? | Project-local `quasar describe` from the installed `@quasar/app-vite` | Installed Quasar types/API JSON, then version-matched official docs |
| Which composables or utils exist, and what are their TypeScript shapes? | Installed `quasar` exports and type declarations | Version-matched official Quasar docs |
| What is current upstream behavior or the latest release? | Official Quasar docs, releases, and npm registry | Mark the claim unverified; do not substitute model memory |
| Which implementation approach and guardrails should the agent follow? | This skill's workflow and routed references | Repo-specific instructions override where explicitly scoped |

When sources disagree, report the drift and apply the authority for the exact question. Do not silently replace project truth with a newer documentation example.

## Exact API workflow

1. Locate the target Quasar app root and read its lockfile plus `package.json`.
2. Confirm the installed `@quasar/app-vite` and `quasar` versions; a declared range alone does not prove the installed version.
3. For a component, directive, or plugin, run the bundled `scripts/query-installed-quasar-api.mjs` with the narrowest useful filters.
4. Treat `-f` as a narrowing search, not completeness proof. Query each required concept separately or retry the symbol unfiltered; nested plugin configuration and method option objects may not appear under `-p`.
5. For a composable or util, inspect installed exports/type declarations and version-matched official docs; `quasar describe` does not cover these surfaces.
6. Use the relevant atlas for intent, alternatives, gotchas, accessibility, performance, and search vocabulary.
7. Use official Quasar docs for conceptual guidance and examples; verify that any copied API exists in the installed line.
8. If the exact lookup cannot run, state why and keep the syntax claim unverified.

From the target repo or with an explicit project path:

```bash
node <skill-dir>/scripts/query-installed-quasar-api.mjs QTable -p -s -e -m
node <skill-dir>/scripts/query-installed-quasar-api.mjs --project <repo-root> QSelect -p -f map
node <skill-dir>/scripts/query-installed-quasar-api.mjs --project <repo-root> list storage
```

The script:

- walks upward from the project path until it finds an app declaring `@quasar/app-vite`
- resolves the installed local CLI without switching package managers or downloading packages
- prints the installed app-vite and Quasar versions as evidence
- delegates to `quasar describe` and disables color noise
- exits with the local CLI's status

## Direct CLI fallback

If the bundled bridge cannot resolve the local CLI but the repository's normal package-manager command can, use the existing lockfile's package manager:

```bash
pnpm exec quasar describe QTable -p -s -e -m --no-color
yarn quasar describe QTable -p -s -e -m --no-color
node node_modules/@quasar/app-vite/bin/quasar.js describe QTable -p -s -e -m --no-color
```

Use these only after verifying the local executable exists. Do not use `npm exec`/`npx` or another command that may download a missing package, install a different package manager, or fetch a floating Quasar CLI just to answer the question.

## Missing dependencies or unavailable lookup

- If dependencies are declared but not installed, do not run an unpinned remote CLI. Report that exact project-local API verification is blocked until the repo's normal install completes.
- If only a lockfile is present, use it to identify the intended line but do not present that as proof of the installed runtime.
- If official docs only describe a newer line, preserve the mismatch and avoid copying the newer shape into the older repo.
- If an App Extension contributes an API, prefer project-local `quasar describe`; static core-package JSON may not include the extension.

✅ Do — query `QTable -p -s -e -m` in the target project before asserting exact prop, slot, event, or method names.

❌ Don't — treat `61-component-usage-atlas.md`, `65-directive-usage-atlas.md`, or `66-api-usage-atlas.md` as exhaustive API specifications; they are curated decision aids.

✅ Do — retry `Notify` without `-p` when an option such as `timeout` is nested under plugin configuration or a method argument.

❌ Don't — infer that a plugin option is absent solely because a narrow section filter returned no properties.

## MCP posture

No MCP server is required by this skill. The local lookup script is the default exact-API path and official web sources are the freshness path.

If a Quasar documentation MCP is introduced later, add it as an optional retrieval fast path only when it returns version, source URL, and freshness metadata. Preserve the project-local lookup as the final authority for installed API availability and keep a no-MCP fallback.

## Search terms

- `quasar describe`, `describe list`, `--props`, `--slots`, `--events`, `--methods`, `--filter`, `--no-color`
- `installed Quasar version`, `App Extension API`, `dist/api`, `web-types`, `exact API`, `source drift`
