# Source map

Use this file to ground the skill before loading deeper references.

## Local project sources inspected for this skill

- `skill-creator/SKILL.md`: skill structure, progressive disclosure, `SKILL.md` frontmatter, optional `agents/openai.yaml`, and reference-folder conventions.
- `skill-creator/references/openai_yaml.md`: UI metadata constraints for `agents/openai.yaml`.
- `codex_prompting_guide.md`: GPT-5.5 outcome-first skills, concise rules, retrieval budgets, validation gates, and restrained use of absolutes.
- `exist-skills.zip`: existing Alaa skill conventions, especially cross-agent `SKILL.md` + `agents/openai.yaml` layout and enforcement-oriented wording.
- `Vue_js_3_Design_Patterns_and_Best_Practi.pdf`, pages 42-71: Vue-oriented design principles and patterns requested by the user.


## Cross-agent packaging contract

- This skill is intentionally packaged as one portable folder with `SKILL.md` frontmatter and Markdown instructions.
- Claude Code/Opus reads the folder `SKILL.md` directly when installed under a Claude skills path.
- OpenAI Codex/GPT reads the same `SKILL.md`; `agents/openai.yaml` supplies Codex UI metadata and default prompt text.
- Keep all agent-neutral behavior in `SKILL.md` and `references/`. Keep OpenAI-specific display metadata only in `agents/openai.yaml`.

## Agent skill portability sources

- Agent Skills open specification: `https://agentskills.io/specification`
- OpenAI Codex skills: `https://developers.openai.com/codex/skills`
- Claude Code skills: `https://docs.anthropic.com/en/docs/claude-code/skills`

Keep the skill portable by using the shared `SKILL.md` core contract for instructions and by putting tool-specific metadata only in optional tool-specific folders such as `agents/openai.yaml`.

## Official docs to refresh when version-sensitive

- Vue style guide: `https://vuejs.org/style-guide/`
- Vue `<script setup>`: `https://vuejs.org/api/sfc-script-setup.html`
- Vue TypeScript Composition API: `https://vuejs.org/guide/typescript/composition-api`
- Vue composables: `https://vuejs.org/guide/reusability/composables`
- Vue provide/inject: `https://vuejs.org/guide/components/provide-inject`
- Vue performance: `https://vuejs.org/guide/best-practices/performance`
- Quasar Vue files: `https://quasar.dev/start/how-to-use-vue/`
- Quasar boot files: `https://quasar.dev/quasar-cli-vite/boot-files/`
- Quasar Pinia: `https://quasar.dev/quasar-cli-vite/state-management-with-pinia/`
- Quasar SSR: `https://quasar.dev/quasar-cli-vite/developing-ssr/introduction/`
- Pinia core concepts: `https://pinia.vuejs.org/core-concepts/`
- Vue Router docs: `https://router.vuejs.org/`
- Vitest docs: `https://vitest.dev/`
- Vue Test Utils docs: `https://test-utils.vuejs.org/`
- TypeScript handbook: `https://www.typescriptlang.org/docs/`

## Interpretation contract

Use official docs for current syntax and version-gated behavior. Use the PDF for the requested Vue-focused clean-code and pattern vocabulary. When the PDF uses older or plain-JavaScript examples, translate them to modern Vue 3, Quasar, Vite, Pinia, and TypeScript rather than copying the old style.

## Freshness rule

When the task depends on current framework behavior, installed package versions, or CLI syntax, inspect `package.json` and lockfiles first. Search official docs only when the installed version or requested feature makes the behavior uncertain.
