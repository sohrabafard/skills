# Upstream Deltas and Maintenance

Use this file when:

- the task asks for the latest guidance
- you are updating this skill itself
- you need current OpenAI or Codex prompting rules
- you are checking whether Vue, Quasar, Vite, or Workbox guidance may have drifted

## Live package snapshot

Captured on April 24, 2026 by `node scripts/check-upstream-versions.mjs`:

- `vue` -> `3.5.33` (published 2026-04-22)
- `quasar` -> `2.19.3` (published 2026-04-06)
- `@quasar/app-vite` -> `2.6.0` (published 2026-04-06)
- `vite` -> `8.0.10` (published 2026-04-23)
- `workbox-build` -> `7.4.0`

Refresh before version-sensitive work:

```bash
node scripts/check-upstream-versions.mjs
```

## Official-first source map

Use sources in this order:

1. Repo-local contracts: `package.json`, lockfile, Quasar/Vite config, SSR/PWA files, route guards, API clients, and tests.
2. Official docs for the affected surface:
   - Vue docs and release policy
   - Quasar docs and Quasar CLI with Vite upgrade guide
   - Vite docs and migration guide
   - Workbox docs for service-worker and PWA behavior
   - MDN for browser APIs
3. Official release notes, npm metadata, and upstream changelogs for version-sensitive claims.
4. Community posts, StackOverflow answers, and issue comments only as troubleshooting leads.

Re-check official sources before claiming current behavior for Vue lifecycle, hydration, watcher semantics, Quasar SSR/PWA behavior, Vite transforms, Workbox defaults, browser storage, service workers, or security-sensitive auth behavior.

Do not encode community anecdotes as durable frontend policy. Use them to find a reproduction, then verify locally or against official docs.

## OpenAI and Codex maintenance rules

Based on the official OpenAI docs and Codex docs reviewed on April 24, 2026:

- Agent Skills use progressive disclosure:
  - Codex starts from skill metadata and only loads full instructions when the skill is chosen.
- Skill trigger quality depends mainly on `name` and `description`.
- Keep `SKILL.md` focused and move detail into one-hop reference files.
- `agents/openai.yaml` can add UI metadata and invocation policy.
- For GPT-5.5 or fallback GPT-5.4 workloads, improve the prompt contract before simply raising reasoning effort.
- The current models docs are the source of truth for latest model choice. When the user is unsure and the task is complex, code-heavy, or tool-heavy, re-check the latest models page before hard-coding a model recommendation.
- For coding-specialized API use cases, re-check the current GPT-5 Codex model page before suggesting a codex-family API model.
- The highest-leverage GPT-5.5-ready additions for agentic workflows are:
  - explicit completeness rules
  - verification loop
  - tool-persistence rules
  - dependency checks
  - selective parallel tool calls
- Model policy from the current Codex models docs:
  - start with GPT-5.5 for complex Codex work when it is available
  - fall back to GPT-5.4 during rollout or when GPT-5.5 is unavailable
  - use GPT-5.4-mini only for lighter, lower-cost scans or subagent lanes
- Higher-priority developer and system instructions remain binding when instructions change mid-conversation.

## Codex prompting guidance to preserve

From the official Codex Prompting Guide and related Codex docs:

- prefer `rg` for search
- prefer dedicated tools over raw shell when the harness provides them
- parallelize independent reads and searches
- preserve autonomy and persistence through implementation and verification
- avoid forcing bulky upfront plans, preambles, or status chatter into the base harness prompt
- Windows and PowerShell behavior are now explicitly improved and should be treated as first-class

## Long-horizon task guidance to preserve

The official Codex long-horizon guidance reinforces:

- explicit milestone verification
- plans and runbooks for multi-step work
- a lightweight audit trail for continuation
- tests, lint, build, or equivalent checks at meaningful milestones

## Package-manager guidance

- If a repo uses Yarn or `yarn.lock`, stay Yarn-first.
- Upstream support for Bun, pnpm, or npm is not a migration recommendation.
- Use registry checks or the version script for discovery only, not to infer package-manager migration.

## Maintenance workflow for this skill

When updating this skill:

1. Re-check the official OpenAI/Codex docs for skill, prompting, or model-maintenance changes.
2. Refresh the Vue, Quasar, Vite, and Workbox version snapshot.
3. Keep the body routing-first and the references one hop away from `SKILL.md`.
4. Re-test whether realistic prompts still load this skill implicitly.
5. Re-run `quick_validate.py`.
6. Update `80-legacy-skill-coverage.md` if routing boundaries change.

## Useful official docs

- Agent Skills:
  - [https://developers.openai.com/codex/skills](https://developers.openai.com/codex/skills)
- Codex models:
  - [https://developers.openai.com/codex/models](https://developers.openai.com/codex/models)
- Prompt guidance:
  - [https://developers.openai.com/api/docs/guides/prompt-guidance](https://developers.openai.com/api/docs/guides/prompt-guidance)
- Models overview:
  - [https://developers.openai.com/api/docs/models](https://developers.openai.com/api/docs/models)
- GPT-5 Codex model page:
  - [https://developers.openai.com/api/docs/models/gpt-5-codex](https://developers.openai.com/api/docs/models/gpt-5-codex)
- Codex Prompting Guide:
  - [https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide)
- Codex app and CLI docs:
  - [https://developers.openai.com/codex/cli](https://developers.openai.com/codex/cli)
  - [https://developers.openai.com/codex/app/features](https://developers.openai.com/codex/app/features)
  - [https://developers.openai.com/codex/app/windows](https://developers.openai.com/codex/app/windows)
