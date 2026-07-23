# Topic Map — Shortest Reading Path

Match the task to the smallest set of files. When two rows match, read both; for a whole feature, follow
the SKILL.md operating model order instead of assembling pieces.

| Task looks like | Read |
|---|---|
| Component, template, or style work | `10-vue-style-contract.md` |
| TypeScript or Composition API work | `20-typescript-composition-contract.md` |
| Clean-code or SOLID refactor | `30-clean-code-solid-vue.md` |
| Choosing, confirming, or reviewing a design pattern; architecture change | `40-patterns-vue-quasar.md` — run the pattern selection diagnostic at its top first |
| Quasar, Vite, Pinia, router, SSR, PWA, or boot files | `50-quasar-vite-pinia-contract.md` |
| Finalizing any code change | `60-validation-checklists.md` |
| View mappers, flow composables, stores, SDK adapters, or design-system components in an Alaa-style repo | `65-alaa-observed-patterns.md` — ALWAYS, before writing or reviewing; every antipattern there has shipped broken once |
| Latest/current/version claims | `00-source-map.md` |

Rule of thumb: the most expensive mistakes this skill prevents are the Alaa observed antipatterns in
`65-alaa-observed-patterns.md` — when the task touches an Alaa-style repo surface, that file is never
optional reading, whatever else the row says.
