# Alaa Quasar App-Vite v3 Evolution Forward Tests

Timestamp: `20260710-063323`

## app-vite v3 task

Task: use the Skill in `D:/Sohrab/Project/client` to verify the installed QTable row-selection API and recommend a repository-consistent direction without editing files.

Result: passed.

- Detected installed app-vite `3.0.0` and Quasar `2.21.1`.
- Verified `row-key`, `selection`, `selected`, `update:selected`, `selection`, `body-selection`, `header-selection`, and `top-selection` from the project-local API.
- Correctly preserved the repository's ID-based selection boundary instead of binding an ID array directly to QTable's row-object `v-model:selected` contract.
- Lookup lesson: `-f select` did not include `row-key`; filters are narrowing searches, not completeness proof.

## app-vite v2 task

Task: use the Skill in `D:/Sohrab/Project/entekhabat-front` to verify the installed boot import line and an exact Notify API detail without editing files.

Result: passed.

- Detected installed app-vite `2.4.0` and Quasar `2.18.6`.
- Correctly selected `#q-app/wrappers` for the v2 line and distinguished existing `quasar/wrappers` imports as compatibility debt rather than a proven runtime defect.
- Verified Notify `timeout` and `create(opts)` behavior from the project-local API.
- Lookup lesson: plugin configuration can be nested, so a filtered `-p` query returning no properties is not proof that an option is absent.

## Independent review

Four actionable findings were identified and fixed:

- removed the `npm exec` fallback because it could download a missing package
- scoped `quasar describe` to components, directives, and plugins; composables/utils now route to installed exports/types plus version-matched official docs
- corrected the stale live-snapshot table-of-contents date
- removed the stale Claude Opus-only consumer statement
