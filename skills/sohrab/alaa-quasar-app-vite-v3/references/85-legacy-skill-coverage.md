# Legacy Skill Coverage

This pack replaces 224 legacy Quasar skills. Use for old skill names or coverage proof.

## Inventory map

| Legacy bucket | Count | Current coverage |
| --- | ---: | --- |
| `quasar-cli-vite-*` | 77 | `21-cli-vite-and-config.md`, `22-cli-cookbook-and-examples.md`, `35-platform-modes.md`, `80-upstream-deltas-and-live-checks.md` |
| `quasar-component-*` | 75 | `60-components-and-layouts.md`, `61-component-usage-atlas.md`, layout-adjacent `62-layout-patterns-and-examples.md`, image `63-image-delivery-and-placeholders.md`, `70-guardrails-a11y-performance-monorepo.md` |
| `quasar-composable-*` | 11 | `64-plugins-composables-directives-options-utils.md`, `66-api-usage-atlas.md`, SSR-sensitive `31-ssr-pwa-and-security.md` |
| `quasar-directive-*` | 10 | `64`, `65-directive-usage-atlas.md`, `31` |
| `quasar-layout-*` | 10 | `60`, `61`, `62`, `21` |
| `quasar-options-*` | 13 | `64`, `66`, `21` |
| `quasar-plugin-*` | 7 | `64`, `66` |
| `quasar-ssr-*` | 5 | `31`, SW-specific `32-pwa-injectmanifest-guard.md`, `70` |
| `quasar-utils-*` | 9 | `64`, `66`, SSR-sensitive `31` |

## One-offs

| Old name | Current coverage |
| --- | --- |
| `quasar-a11y-patterns` | `70` |
| `quasar-hydration-debugger` | `31`, `70` |
| `quasar-pwa-injectmanifest-guard` | `32`, `31` |
| `quasar-qimg-smart-resize-placeholder` | `63`, `61`, `70` |
| `quasar-security-basics` | `31`, `70` |
| `quasar-skillpack-shared` | `00-topic-map.md`, `70`, pack-wide `SKILL.md` routing |
| `quasar-ui-patterns-a11y` | `70` |

## Old-name search routing

- `quasar-cli-vite-*`: search its feature in `10`; open `22` for exact wiring/examples.
- `quasar-component-*`: search the exact symbol in `40`; open `61`.
- `quasar-layout-*`: search its phrase in `62`; add `10` for routing/config.
- `quasar-composable-*`, `quasar-plugin-*`, `quasar-options-*`, `quasar-utils-*`: search exact API in `50`; open `66`.
- `quasar-directive-*`: search exact API in `50`; open `65`.
- `quasar-ssr-*`: start `20`. `quasar-pwa-*`: start `20`, then `21` for InjectManifest/update flow.
- One-off: load its mapped references directly.

Active references must point to this skill; historical plan/execution artifacts may retain legacy names for audit history.
