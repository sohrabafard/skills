# Legacy Skill Coverage

This pack replaces a source inventory of 224 legacy Quasar skills. Use this file when the user mentions an old skill name or when you need to prove that the new pack still covers the deleted catalog.

## Coverage map by inventory bucket

- `quasar-cli-vite-*` (77 skills)
  - covered by `10-cli-vite-and-config.md`, `11-cli-cookbook-and-examples.md`, `30-platform-modes.md`, and `70-upstream-deltas-and-live-checks.md`
- `quasar-component-*` (75 skills)
  - covered by `40-components-and-layouts.md`, `41-component-usage-atlas.md`, `42-layout-patterns-and-examples.md` for layout-adjacent components, `43-image-delivery-and-placeholders.md` for image-delivery cases, and `60-guardrails-a11y-performance-monorepo.md`
- `quasar-composable-*` (11 skills)
  - covered by `50-plugins-composables-directives-options-utils.md`, `52-api-usage-atlas.md`, plus `20-ssr-pwa-and-security.md` for SSR-sensitive APIs
- `quasar-directive-*` (10 skills)
  - covered by `50-plugins-composables-directives-options-utils.md`, `51-directive-usage-atlas.md`, plus `20-ssr-pwa-and-security.md`
- `quasar-layout-*` (10 skills)
  - covered by `40-components-and-layouts.md`, `41-component-usage-atlas.md`, `42-layout-patterns-and-examples.md`, plus `10-cli-vite-and-config.md`
- `quasar-options-*` (13 skills)
  - covered by `50-plugins-composables-directives-options-utils.md`, `52-api-usage-atlas.md`, plus `10-cli-vite-and-config.md`
- `quasar-plugin-*` (7 skills)
  - covered by `50-plugins-composables-directives-options-utils.md` and `52-api-usage-atlas.md`
- `quasar-ssr-*` (5 skills)
  - covered by `20-ssr-pwa-and-security.md`, `21-pwa-injectmanifest-guard.md` for SW-specific cases, and `60-guardrails-a11y-performance-monorepo.md`
- `quasar-utils-*` (9 skills)
  - covered by `50-plugins-composables-directives-options-utils.md`, `52-api-usage-atlas.md`, plus `20-ssr-pwa-and-security.md`

## One-off legacy buckets

- `quasar-a11y-patterns`
  - covered by `60-guardrails-a11y-performance-monorepo.md`
- `quasar-hydration-debugger`
  - covered by `20-ssr-pwa-and-security.md` and `60-guardrails-a11y-performance-monorepo.md`
- `quasar-pwa-injectmanifest-guard`
  - covered by `21-pwa-injectmanifest-guard.md` plus `20-ssr-pwa-and-security.md`
- `quasar-qimg-smart-resize-placeholder`
  - covered by `43-image-delivery-and-placeholders.md`, `41-component-usage-atlas.md`, and `60-guardrails-a11y-performance-monorepo.md`
- `quasar-security-basics`
  - covered by `20-ssr-pwa-and-security.md` and `60-guardrails-a11y-performance-monorepo.md`
- `quasar-skillpack-shared`
  - covered by `00-topic-map.md`, `60-guardrails-a11y-performance-monorepo.md`, and the pack-wide routing rules in `SKILL.md`
- `quasar-ui-patterns-a11y`
  - covered by `60-guardrails-a11y-performance-monorepo.md`

## How to search by old names

- If the old name starts with `quasar-cli-vite-`, search the feature phrase inside `10`, then open `11-cli-cookbook-and-examples.md` if the task needs exact wiring or example shape.
- If the old name starts with `quasar-component-`, search the exact symbol inside `40`, then open `41-component-usage-atlas.md`.
- If the old name starts with `quasar-layout-`, search the feature phrase inside `42-layout-patterns-and-examples.md`, then load `10` if routing or config is involved.
- If the old name starts with `quasar-composable-`, `quasar-plugin-`, `quasar-options-`, or `quasar-utils-`, search the exact API name inside `50`, then open `52-api-usage-atlas.md`.
- If the old name starts with `quasar-directive-`, search the exact API name inside `50`, then open `51-directive-usage-atlas.md`.
- If the old name starts with `quasar-ssr-`, start with `20`.
- If the old name starts with `quasar-pwa-`, start with `20`, then open `21` for InjectManifest or update-flow work.
- If the old name is one of the one-off buckets above, load the mapped reference directly.

## Reference status

Active skill references should now point at `$quasar-skill-packe`. Historical plan and execution artifacts may still mention legacy names to preserve audit history.
