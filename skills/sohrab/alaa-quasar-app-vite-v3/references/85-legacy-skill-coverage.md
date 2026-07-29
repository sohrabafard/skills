# Legacy skill coverage

You are acting on a request that names a retired `quasar-*` skill. This pack replaces 224 of them. This file is a legacy-name index, not a router; skill-level routing is `references/00-topic-map.md`.

## Inventory map

| Legacy bucket | Count | Current coverage |
| --- | ---: | --- |
| `quasar-cli-vite-*` | 77 | `21-cli-vite-and-config.md`, `22-cli-cookbook-and-examples.md`, `35-platform-modes.md`, `80-upstream-deltas-and-live-checks.md` |
| `quasar-component-*` | 75 | `60-components-and-layouts.md`, `61-component-usage-atlas.md`, `62-layout-patterns-and-examples.md`, `63-image-delivery-and-placeholders.md`, `70-guardrails-a11y-performance-monorepo.md` |
| `quasar-composable-*` | 11 | `64-plugins-composables-directives-options-utils.md`, `66-api-usage-atlas.md`, `31-ssr-pwa-and-security.md` |
| `quasar-directive-*` | 10 | `64-plugins-composables-directives-options-utils.md`, `65-directive-usage-atlas.md`, `31-ssr-pwa-and-security.md` |
| `quasar-layout-*` | 10 | `62-layout-patterns-and-examples.md`, `61-component-usage-atlas.md`, `60-components-and-layouts.md`, `21-cli-vite-and-config.md` |
| `quasar-options-*` | 13 | `64-plugins-composables-directives-options-utils.md`, `66-api-usage-atlas.md`, `21-cli-vite-and-config.md` |
| `quasar-plugin-*` | 7 | `64-plugins-composables-directives-options-utils.md`, `66-api-usage-atlas.md` |
| `quasar-ssr-*` | 5 | `31-ssr-pwa-and-security.md`, `34-frontend-failure-and-degradation.md`, `70-guardrails-a11y-performance-monorepo.md` |
| `quasar-utils-*` | 9 | `64-plugins-composables-directives-options-utils.md`, `66-api-usage-atlas.md`, `31-ssr-pwa-and-security.md` |

## One-offs

| Old name | Current coverage |
| --- | --- |
| `quasar-a11y-patterns` | `70-guardrails-a11y-performance-monorepo.md` |
| `quasar-hydration-debugger` | `31-ssr-pwa-and-security.md`, `70-guardrails-a11y-performance-monorepo.md` |
| `quasar-pwa-injectmanifest-guard` | `32-pwa-injectmanifest-guard.md`, `30-service-worker-excellence.md` |
| `quasar-qimg-smart-resize-placeholder` | `63-image-delivery-and-placeholders.md`, `61-component-usage-atlas.md` |
| `quasar-security-basics` | `31-ssr-pwa-and-security.md`, `70-guardrails-a11y-performance-monorepo.md` |
| `quasar-skillpack-shared` | `00-topic-map.md` |
| `quasar-ui-patterns-a11y` | `70-guardrails-a11y-performance-monorepo.md` |

## Old-name search routing

Each line names the file to search and the file to open. The numbers below match the table above.

- `quasar-cli-vite-*`: search the feature in `21-cli-vite-and-config.md`; open `22-cli-cookbook-and-examples.md` for the exact wiring.
- `quasar-component-*`: search the exact symbol in `61-component-usage-atlas.md`; open `60-components-and-layouts.md` when you have a family rather than a symbol.
- `quasar-layout-*`: search the phrase in `62-layout-patterns-and-examples.md`; add `22-cli-cookbook-and-examples.md` for the route shape.
- `quasar-composable-*`, `quasar-plugin-*`, `quasar-options-*`, `quasar-utils-*`: search the exact API in `66-api-usage-atlas.md`; open `64-plugins-composables-directives-options-utils.md` when unsure which surface it is.
- `quasar-directive-*`: search the exact directive in `65-directive-usage-atlas.md`; open `64-plugins-composables-directives-options-utils.md` for the surface table.
- `quasar-ssr-*`: start in `31-ssr-pwa-and-security.md`; add `34-frontend-failure-and-degradation.md` for failure behaviour.
- `quasar-pwa-*`: start in `32-pwa-injectmanifest-guard.md`; open `30-service-worker-excellence.md` for the strategy, update flow, and debugging.
- A one-off: load the files its row maps to, directly.

Whatever the old name promised, the exact API still comes from the installed project through `references/05-authority-and-api-lookup.md`. An active reference must point at this skill; a historical plan or execution artifact may keep a legacy name for audit history.

Search: `legacy skill`, `retired skill name`, `quasar-cli-vite`, `quasar-component`, `quasar-ssr`, `quasar-pwa`, `coverage proof`.
