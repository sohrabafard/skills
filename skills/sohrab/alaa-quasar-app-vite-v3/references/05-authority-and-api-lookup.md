# Authority and installed API lookup

You are about to assert an exact prop, event, slot, method, directive value, or plugin option name, or the repository, this skill, and upstream disagree. This control plane stores durable workflow, deltas, heuristics, guardrails, and high-value examples—not a frozen API copy; exact availability belongs to the target's installed line.

| Question | Authority | Fallback |
|---|---|---|
| Current app behavior | Live code/config/lockfile/tests/runtime | Maintained repo docs |
| Local props/events/slots/methods/options | Installed `@quasar/app-vite` project-local `quasar describe` | Installed types/API JSON, then version-matched official docs |
| Composables/utils and TS shapes | Installed `quasar` exports/types | Version-matched official docs |
| Current upstream/latest release | Official Quasar docs/releases/npm | Mark unverified; never substitute model memory |
| Approach/guardrails | This workflow and routed references | Explicitly scoped repo instructions override |

On disagreement, report drift and use the authority for that question; never silently replace project truth with a newer docs example.

## Exact workflow

1. Find app root; read lockfile and `package.json`.
2. Confirm installed `@quasar/app-vite` and `quasar`; a declared range is not installed-version proof.
3. For components, directives, and plugins, run `node <skill-dir>/scripts/query-installed-quasar-api.mjs` with minimal filters. It takes `--help` and `--self-test`; exit code 2 means the bridge could not run, which is never a clean result.
4. `-f` narrows; it never proves completeness. Query concepts separately or retry unfiltered—nested plugin config/method-option objects may not appear under `-p`.
5. For composables/utils, inspect installed exports/types plus version-matched docs; `quasar describe` does not cover them.
6. Use atlases for intent, alternatives, gotchas, a11y, performance, and vocabulary.
7. Use official docs for concepts/examples, verifying copied APIs against the installed line.
8. If lookup cannot run, explain why and mark exact syntax unverified.

```bash
node <skill-dir>/scripts/query-installed-quasar-api.mjs QTable -p -s -e -m
node <skill-dir>/scripts/query-installed-quasar-api.mjs --project <repo-root> QSelect -p -f map
node <skill-dir>/scripts/query-installed-quasar-api.mjs --project <repo-root> list storage
```

The bridge walks upward from the project path to an app declaring `@quasar/app-vite`, resolves its installed local CLI without downloads or package-manager switching, prints installed app-vite/Quasar versions, delegates to color-disabled `quasar describe`, and exits with its status.

## Direct fallback

If the bridge cannot resolve an existing local CLI but the repo's normal package-manager command can, follow the lockfile:

```bash
pnpm exec quasar describe QTable -p -s -e -m --no-color
yarn quasar describe QTable -p -s -e -m --no-color
node node_modules/@quasar/app-vite/bin/quasar.js describe QTable -p -s -e -m --no-color
```

First verify the executable exists. Never use `npm exec`/`npx`, install another manager, or fetch a floating CLI merely to answer.

## Blocked/unavailable cases

- Declared but uninstalled dependencies: do not run remote unpinned CLI; local verification waits for the normal install.
- Lockfile only: identify intended line, not installed runtime.
- Docs newer than repo: preserve mismatch; do not copy newer shapes into older code.
- App Extension API: prefer local `quasar describe`; core static JSON may omit extension contributions.

✅ Query `QTable -p -s -e -m` locally before asserting exact prop/slot/event/method names; ❌ never treat `61-component-usage-atlas.md`, `65-directive-usage-atlas.md`, or `66-api-usage-atlas.md` as exhaustive API specs.

✅ Retry `Notify` without `-p` for nested options such as `timeout`; ❌ never infer absence from a narrow section filter.

## MCP posture and search

No MCP is required: local lookup is the exact-API path; official web is freshness. A future Quasar-doc MCP may be an optional fast path only if it returns version, URL, and freshness metadata; retain local lookup as installed-API authority and a no-MCP fallback.

Search: `quasar describe`, `describe list`, `--props`, `--slots`, `--events`, `--methods`, `--filter`, `--no-color`, `installed Quasar version`, `App Extension API`, `dist/api`, `web-types`, `exact API`, `source drift`.
