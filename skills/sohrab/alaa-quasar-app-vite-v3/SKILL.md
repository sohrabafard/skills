---
name: alaa-quasar-app-vite-v3
description: "Version-aware control plane for Quasar CLI plus Vite on @quasar/app-vite v3, v2 maintenance and the v2-to-v3 migration. Detect the installed line first, then query exact component, directive and plugin APIs through the project-local Quasar CLI rather than bundled Markdown. Covers quasar.config, env and defines, boot and routing, components and layouts, every platform mode, service workers, offline and update UX, SSR render failure, client telemetry, WebOTP, browser permissions, and accessibility and performance budgets. Not for plain Vue and Vite without the Quasar CLI, code quality (/alaa-vue-typescript-clean-code), broad frontend work (/alaa-frontend-developer), CI or deploy (/alaa-frontend-devops), browser storage (/alaa-indexeddb-browser-storage), or gateway auth (/alaa-trust-gateway-auth)."
---

# Alaa Quasar App-Vite v3

## Purpose and posture

This skill is the version-aware Quasar CLI and Vite control plane, v3 first, and owns:

- v2 -> v3 decisions and deltas;
- local exact-API lookup;
- `quasar.config`, env, boot, routing, layout, composable and mode patterns;
- production service workers with their offline, update, and failure behaviour;
- WebOTP and device-trust-bounded signals;
- permission-gated browser APIs;
- Quasar-shaped accessibility, performance, and testing guardrails.

This is not exhaustive Quasar documentation. The references own workflows, deltas, guardrails, and high-value examples. The installed project and the official Quasar sources own exact API availability and current upstream behaviour. In Do and Do not pairs, Do is normative and Do not preserves a real failure.

## Version rules

- New apps use v3. Treat a production v2 migration as scheduled engineering through `references/10-v2-to-v3-migration.md`. Never make it an opportunistic bump inside unrelated work.
- A stated blocker, such as a Node floor, an incompatible App Extension, or a frozen release window, may keep a repo pinned to `@quasar/app-vite@^2`. Unpinned installs now resolve v3. In a pinned repo use `references/12-v2-maintenance-playbook.md` shapes.
- **Detect the installed major before any config, import, env, alias, or mode advice.** Read `@quasar/app-vite` in `package.json`. A declared range is not proof of the installed version. v2 and v3 differ on `#q-app/wrappers` versus `#q-app`, `process.env.*` versus `import.meta.env.QUASAR_*`, legacy aliases versus `@/`, and mode folders.
- Follow the lockfile's package manager, because it is a repository contract: a Yarn workspace or `yarn.lock` means Yarn. Never switch it during a Quasar task, even when upstream supports another.
- **Every version number, peer range, and Node floor lives in `references/80-upstream-deltas-and-live-checks.md`.** State none from memory. Run `node $SKILL_DIR/scripts/check-upstream-versions.mjs` first. Treat exit code `2` as "could not run", not as "clean".

## Authority and exact APIs

Query exact props, events, slots, methods, directive values, and plugin options through the project-local `quasar describe` bridge:

```bash
node $SKILL_DIR/scripts/query-installed-quasar-api.mjs --project <repo-root> QTable -p -s -e -m
```

When a question's authority is unclear, sources disagree, or the lookup fails, read `references/05-authority-and-api-lookup.md` for the authority table and fallbacks. No MCP is required.

## Workflow and routing

1. Read the repo-local `AGENTS.md` and `CLAUDE.md`, the lockfile, `package.json`, `quasar.config.*`, and only the mode folders you touch. Repo instructions override this skill.
2. For exact APIs, query the installed API before any atlas example or model memory.
3. Before acting on a Quasar surface, read `references/00-topic-map.md`. Follow every matching route and
   mandatory pairing in its stated order.

## Companion boundary

This skill owns Quasar wiring and mechanics. External doctrine, values, package and storage boundaries, and
runtime policy stay with the owners that the topic map names. Cite the owner. Never restate its rule here.

## When NOT to use

Do not use for plain Vue or Vite without the Quasar CLI. `@quasar/vite-plugin` is not app-vite. Do not use for broad non-Quasar frontend work, Vue or TypeScript code-quality review, CI or deployment authoring, browser storage design, gateway authentication, or backend and infrastructure tasks. Route to the canonical external owner.

## Final response contract

Report:

- the repo evidence you read (installed line, modes, blockers);
- which exact-API or official source you queried, when syntax mattered;
- the line-specific change or recommendation, and why it is safe on the detected line;
- the commands you actually ran and their outcomes;
- the modes, App Extensions, and claims you did not verify.

For a migration, report every mode separately. Never claim an unrun check passed.
