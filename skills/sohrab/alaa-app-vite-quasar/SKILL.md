---
name: alaa-app-vite-quasar
description: Use for coding, reviewing, or maintaining Alaa Quasar CLI with Vite apps still on the @quasar/app-vite v2 maintenance line, and as the verified v2->v3 delta source when planning a migration. Covers v2 quasar.config, imports/aliases, env, SSR, PWA, routing, boot files, Pinia, testing, CI validation, and upgrade guardrails. For v3 builds and the migration playbook use $alaa-quasar-app-vite-v3. Do not use for plain Vue/Vite apps that do not use Quasar CLI.
---

# Alaa App Vite Quasar Skill

Production-grade Quasar CLI with Vite assistant for Alaa projects **still on the `@quasar/app-vite` v2 maintenance line**. Since `3.0.1` (2026-07-07) **v3 is the stable production line**; this skill owns the v2 era and the verified v2->v3 deltas, while `$alaa-quasar-app-vite-v3` owns v3 posture and the migration playbook. Default posture:

- Repos on v2: keep them working on the latest v2 stable (`2.6.2`), pinned to `^2` (an unpinned install now pulls v3); make new v2 work migration-clean.
- Migration: v3 is stable — migration is a scheduled engineering task planned via `$alaa-quasar-app-vite-v3`, executed against the verified delta list in `references/review-and-upgrade-checklist.md`; never an opportunistic bump inside an unrelated change.
- New apps: scaffold on v3 via `$alaa-quasar-app-vite-v3`, not here.

Written for both GPT-5/Codex-family (e.g. `gpt-5.x-codex`) and Claude/Opus coding agents. Prefer the repo's actual files, lockfile, scripts, and test results over generic assumptions. High-value rules use a Correct / Wrong contrast pair: the Correct side is the action to take, the Wrong side is a guardrail.

## Current versions (verify live)

Snapshot 2026-07-08, re-check before version-sensitive work:

- `@quasar/app-vite` stable / production: **`3.0.1`** (v3, since 2026-07-07; holds npm `latest`).
- `@quasar/app-vite` maintenance: `2.6.2` — the last v2 stable, for repos this skill serves. Keep them pinned to `@quasar/app-vite@^2`.
- `quasar` `2.21.1`, `vue` `3.5.39`, `vue-router` `5.1.0`, `pinia` `3.0.4`, `vite` `8.1.3`, `workbox-build` `7.4.1` (all stable).

Refresh with the version checker shipped by `$quasar-skill-packe` (it reports `latestStableByMajor.v2` and `.v3` alongside `latest`).

## Required first move

Before changing code or giving a final recommendation, read the repo state and match it:

1. Package manager from lockfile (`pnpm-lock.yaml` / `yarn.lock` / `package-lock.json` / `bun.lock*`).
2. `package.json` versions: `@quasar/app-vite`, `quasar`, `vue`, `vue-router`, `pinia`, plus testing deps/scripts.
3. `quasar.config.*`, then only the source folders the task needs (`src/`, `src/router|boot|stores/`, `src-pwa|src-ssr|src-capacitor/`), and `AGENTS.md` / `CLAUDE.md` if present.
4. Propose the least invasive discovery commands (`quasar info`, `<pm> run lint|typecheck|test:unit|build`).
5. In Alaa repos, check `potential-bugs.md` first; report a related bug, do not fix it without confirmed scope.

Do not ask for clarification when the repo gives enough evidence. The full scan checklist and assessment-output template are in `references/review-and-upgrade-checklist.md`.

## Source freshness rule

Quasar versions move fast. For version-sensitive work, verify only against primary sources: quasar.dev, Quasar GitHub releases, npm metadata, and the official Vue Router / Vite / Vitest / Cypress / Playwright docs for their own behavior. Never trust blogs, StackOverflow, or generated snippets for migration rules unless the user explicitly asks for community experience. Without web access, treat the lockfile as truth and state which assumptions are unverified.

## When NOT to use

Do not use this skill when:

- The project is plain Vue/Vite and does not use Quasar CLI, `quasar.config.*`, or `@quasar/app-vite`.
- The task only needs exact Quasar API/component/config syntax and does not hinge on app-vite version posture; use `$quasar-skill-packe`.
- The task is broad frontend engineering with no app-vite v2/v3 production or migration decision; use `$alaa-frontend-developer`.

## Companion skills and ownership

This skill owns only the **app-vite v2-era semantics and the verified v2->v3 delta material** (v2 code contracts, migration guardrails, env/alias/wrapper deltas, mode-folder discipline). It is not a full Quasar API reference or a full frontend-engineering skill.

- **Require `$alaa-quasar-app-vite-v3`** for v3 posture, new v3 apps, and the v2->v3 migration playbook — that skill leads migrations and consumes this skill's delta list.

- **Require `$quasar-skill-packe`** when the task needs exact Quasar shapes: `quasar.config` keys, boot/router/Vite-extension snippets, component/layout/directive/plugin/composable/util usage, platform-mode structure, or InjectManifest. This skill decides *which line is safe*; `$quasar-skill-packe` gives the *exact, version-aware code shape*. Don't emit a config/boot/component snippet from memory without confirming it there.
- **Require `$alaa-frontend-developer`** when the task is broader frontend engineering: SSR auth/session, API data-shaping, performance/Web Vitals/realtime, QA/release-readiness, or package/asset contracts. Use it for the engineering decision and this skill for the v2-safe, v3-ready implementation.
- **Recommend:** `$alaa-frontend-devops` (CI/Docker; pin `@quasar/app-vite@^2`), `$alaa-mono-package` (`packages/*`), `$alaa-trust-gateway-auth` (gateway auth), `$playwright` / `$playwright-interactive` (browser validation), `$openai-docs` (OpenAI/Codex product facts).
- **Routing direction:** if a task at `$alaa-frontend-developer` or `$quasar-skill-packe` hinges on the v2-vs-v3 production/migration decision, it routes in here; if a task here is really about exact Quasar shape or broad frontend engineering, route out and keep this skill as the version-posture baseline.

## Core decision matrix

| Situation | Default action |
|---|---|
| Existing production app on `@quasar/app-vite` v2 | Keep v2 working with minimal, tested changes; treat the v3 migration as a scheduled task to plan via `$alaa-quasar-app-vite-v3`. |
| User asks "v2 or v3 in production?" | v3 is the stable production line (since `3.0.1`, 2026-07-07). Recommend migrating when the repo's Node floor, App Extensions, and release window allow; route the plan to `$alaa-quasar-app-vite-v3`. |
| User asks to make v2 code migration-clean | Keep it compatible with installed v2, avoid new v3-incompatible patterns, document the migration delta. |
| User asks to migrate to v3 | Route to `$alaa-quasar-app-vite-v3` for the playbook; supply this skill's `references/review-and-upgrade-checklist.md` §7–8 delta list; plan before implementing on nontrivial repos. |
| New app | Scaffold on v3 via `$alaa-quasar-app-vite-v3`; this skill is not the entry point. |
| Plain Vue + Vite app without Quasar CLI | Do not apply this skill except to explain the difference from `@quasar/vite-plugin`. |

## Hard rules

1. Do not bump a production app from v2 to v3 inside an unrelated task. v3 is stable, but the migration touches app code (imports, env, aliases, mode folders) and runs as its own planned change via `$alaa-quasar-app-vite-v3`.
2. Do not add `vite.config.*` to a Quasar CLI app. Use `quasar.config.*` and `build.extendViteConf` / `build.vitePlugins`.
3. Do not confuse `@quasar/app-vite` (the Quasar CLI app runner/build package) with `@quasar/vite-plugin` (for adding Quasar to a non-Quasar Vite app).
4. Do not edit generated `.quasar/` files. Use `quasar.config.*`, source files, or official extension config.
5. Do not introduce client-exposed secrets. Treat `QCLI_*` / client env prefixes as public.
6. Do not use browser-only APIs in SSR server execution paths.
7. Do not create global mutable singletons that hold per-user/per-request data in SSR.
8. Do not add old folder aliases to hide migration debt; prefer moving source imports to `@/` when the repo supports it.
9. Do not use the deprecated `@quasar/testing` umbrella extension; prefer the specific Quasar testing extensions.
10. Do not perform broad rewrites. Preserve local architecture; make minimal, clean, validated changes.

## Mode-specific reading (load the reference for the topic)

- v2 production + v3-readiness, compatibility policy, env/alias/boot/routing/Pinia, agent implementation rules: `references/quasar-v2-production-v3-ready-playbook.md`
- SSR and PWA details: `references/ssr-pwa-playbook.md`
- Testing and CI: `references/testing-ci-playbook.md`
- Repo scan + assessment template, migration/review checklist, and the verified v2->v3 deltas: `references/review-and-upgrade-checklist.md`
- Examples and anti-patterns: `references/examples.md`

## Final response contract

Always report: (1) what you found in the repo or docs; (2) what you changed or recommend; (3) why it is safe for app-vite v2 production; (4) what remains for v3 migration; (5) exact validation commands and results, or an honest statement that they were not run. For implementation tasks prefer patch-style summaries and cite file paths; if the user sent a diff to review, answer in git patch format.
