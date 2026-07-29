# Sources and freshness

Read when the change turns on a version, when a response is about to contain the words "latest", "current",
"now supported", or "removed", or when a claim in this skill needs to be traced to where it came from.

## The freshness rule

Read the repository before reading the internet. `package.json` and the lockfile decide which APIs exist in
this repo; official docs decide what those APIs do. Search the web only when the installed version leaves
the behaviour genuinely uncertain, and when you do, record the URL and the date you read it.

Run `scripts/check-frontend-versions.mjs` to get installed-versus-latest for the packages whose versions
gate the rules in `20-typescript-composition-contract.md` and `50-quasar-vite-pinia-contract.md`. Its exit
codes distinguish "clean", "drift found", and "could not run"; a "could not run" is reported as unverified,
never rounded down to clean.

## Provenance discipline

Every version-sensitive statement in this skill carries one of three marks, and a statement with none of
them is a defect:

- a source URL plus `read: <ISO date>`, for a fact taken from upstream;
- `read: unverified as of <ISO date>`, for a fact that could not be checked from here — stated, not dropped
  and not asserted;
- nothing at all, for a rule that is this skill's own judgement and depends on no upstream fact.

"Not documented" means searched and not found, and is written that way. It is never used to mean proven
absent.

## Verified this revision

- Pinia 3 removes the `defineStore({ id: ... })` object-id form; `defineStore('id', ...)` is the surviving
  signature, and Pinia 3 is Vue 3 only. Source: `https://pinia.vuejs.org/cookbook/migration-v2-v3.html`,
  `read: 2026-07-28`.
- The Vue style guide's reason for preferring class selectors inside `scoped` is a performance claim about
  element-attribute selectors versus class-attribute selectors. Source:
  `https://vuejs.org/style-guide/rules-use-with-caution.html`, `read: 2026-07-28`. Upstream discussion
  questions how large the effect is on current engines, so `10-vue-style-contract.md` states the rule on
  explicitness and cites this page for the performance rationale rather than asserting a magnitude.
- Vue 3.6 is at release candidate with Vapor mode complete; it is not a released stable line.
  `read: 2026-07-28`. The rule that follows from it lives in `20-typescript-composition-contract.md`.

## Official docs to refresh when the behaviour is version-sensitive

- Vue style guide: `https://vuejs.org/style-guide/`
- Vue `<script setup>`: `https://vuejs.org/api/sfc-script-setup.html`
- Vue TypeScript with the Composition API: `https://vuejs.org/guide/typescript/composition-api`
- Vue composables: `https://vuejs.org/guide/reusability/composables`
- Vue provide/inject: `https://vuejs.org/guide/components/provide-inject`
- Vue performance: `https://vuejs.org/guide/best-practices/performance`
- Quasar boot files: `https://quasar.dev/quasar-cli-vite/boot-files/`
- Quasar with Pinia: `https://quasar.dev/quasar-cli-vite/state-management-with-pinia/`
- Pinia core concepts: `https://pinia.vuejs.org/core-concepts/`
- Vue Router: `https://router.vuejs.org/`
- Vitest: `https://vitest.dev/`
- Vue Test Utils: `https://test-utils.vuejs.org/`
- TypeScript handbook: `https://www.typescriptlang.org/docs/`

Quasar CLI, `quasar.config` semantics, and app-vite line detection are not refreshed from here.
`/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`) owns those facts and their freshness.

## Cross-agent packaging

This skill is one portable folder: `SKILL.md` frontmatter plus Markdown references. Claude Code and Codex
read the same `SKILL.md`; `agents/openai.yaml` carries Codex-only display metadata and nothing behavioural.
Keep every agent-neutral rule in `SKILL.md` and `references/`.

- Agent Skills specification: `https://agentskills.io/specification`
- Codex skills: `https://developers.openai.com/codex/skills`
- Claude Code skills: `https://docs.anthropic.com/en/docs/claude-code/skills`

## Note on derived design material

The clean-code and pattern vocabulary in `30-clean-code-solid-vue.md` and `41-`–`44-` was originally drawn
in part from a third-party Vue design-patterns text that does not ship with this skill and that a reader
cannot open to check. That text is therefore a note, not a source rank: every rule in those files is stated
so it can be judged on its own merits, in modern Vue 3, Quasar, Vite, Pinia, and TypeScript form. If a rule
there cannot be justified from the code it governs, delete the rule rather than citing the book.
