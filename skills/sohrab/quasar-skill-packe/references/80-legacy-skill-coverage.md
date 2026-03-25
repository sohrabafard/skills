# Legacy Skill Coverage

This pack replaces a source inventory of 224 legacy `quasar-*` skills. Use this file when the user mentions an old skill name or when you need to prove coverage before deleting the old catalog.

## Coverage map by group

- `quasar-cli-vite-*` (77 skills)
  - covered by `10-cli-vite-and-config.md`, `11-cli-cookbook-and-examples.md`, `30-platform-modes.md`, and `70-upstream-deltas-and-live-checks.md`
- `quasar-component-*` (75 skills)
  - covered by `40-components-and-layouts.md`, `41-component-usage-atlas.md`, and `60-guardrails-a11y-performance-monorepo.md`
- `quasar-composable-*` (11 skills)
  - covered by `50-plugins-composables-directives-options-utils.md` plus `20-ssr-pwa-and-security.md`
- `quasar-directive-*` (10 skills)
  - covered by `50-plugins-composables-directives-options-utils.md`, `51-directive-usage-atlas.md`, plus `20-ssr-pwa-and-security.md`
- `quasar-layout-*` (10 skills)
  - covered by `40-components-and-layouts.md` plus `10-cli-vite-and-config.md`
- `quasar-options-*` (11 skills)
  - covered by `50-plugins-composables-directives-options-utils.md` plus `10-cli-vite-and-config.md`
- `quasar-utils-*` (8 skills)
  - covered by `50-plugins-composables-directives-options-utils.md` plus `20-ssr-pwa-and-security.md`
- `quasar-plugin-*` (7 skills)
  - covered by `50-plugins-composables-directives-options-utils.md`
- `quasar-ssr-*` (4 skills)
  - covered by `20-ssr-pwa-and-security.md`
- `quasar-pwa-*` (1 skill)
  - covered by `20-ssr-pwa-and-security.md`
- one-off cross-cutting skills:
  - `quasar-a11y-patterns` -> `60-guardrails-a11y-performance-monorepo.md`
  - `quasar-ui-patterns-a11y` -> `60-guardrails-a11y-performance-monorepo.md`
  - `quasar-security-basics` -> `20-ssr-pwa-and-security.md` and `60-guardrails-a11y-performance-monorepo.md`
  - `quasar-hydration-debugger` -> `20-ssr-pwa-and-security.md`
  - `quasar-qimg-smart-resize-placeholder` -> `40-components-and-layouts.md` and `60-guardrails-a11y-performance-monorepo.md`
  - `quasar-skillpack-shared` -> `00-topic-map.md` and `60-guardrails-a11y-performance-monorepo.md`

## How to search by old names

- If the old name starts with `quasar-cli-vite-`, search the feature phrase inside `10`, then open `11-cli-cookbook-and-examples.md` if the task needs exact wiring or example shape.
- If the old name starts with `quasar-component-`, search the exact symbol inside `40`, then open `41-component-usage-atlas.md`.
- If the old name starts with `quasar-composable-`, `quasar-plugin-`, `quasar-options-`, or `quasar-utils-`, search the exact API name inside `50`.
- If the old name starts with `quasar-directive-`, search the exact API name inside `50`, then open `51-directive-usage-atlas.md`.
- If the old name starts with `quasar-ssr-` or `quasar-pwa-`, start with `20`.
- If the old name is one of the one-off cross-cutting skills above, load the mapped reference directly.

## Deletion safety note

Deleting the old `quasar-*` skill folders is safe only after this pack exists in its target shared-skill location and the next maintenance pass updates any remaining references to point at `$quasar-skill-packe`.
