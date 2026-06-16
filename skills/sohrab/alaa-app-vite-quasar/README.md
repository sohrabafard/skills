# alaa-app-vite-quasar

A production-oriented Agent Skill for Alaa Quasar CLI with Vite projects.

Default posture:

- Keep production on `@quasar/app-vite` v2 unless the user explicitly asks for v3 migration.
- Make new work v3-ready without breaking the installed v2 runtime.
- Use official Quasar docs/release notes and the repository lockfile as sources of truth.

Install by placing this folder in one of the supported skills locations, for example:

- Codex repo-scoped: `.agents/skills/alaa-app-vite-quasar/`
- Codex user-scoped: `$HOME/.agents/skills/alaa-app-vite-quasar/`
- ChatGPT/API: upload the zipped top-level folder.

Main file: `SKILL.md`.

## Works alongside

This skill is the app-vite version-posture specialist and is meant to run next to:

- `quasar-skill-packe` — exact Quasar API / `quasar.config` / component / platform-mode shapes (per app-vite line). Required whenever a concrete Quasar code shape is needed.
- `alaa-frontend-developer` — broader app-family frontend engineering (SSR auth, data shaping, performance, QA). Required when the task is more than the app-vite version decision.

`SKILL.md` defines exactly when to recommend and when to require each companion.
