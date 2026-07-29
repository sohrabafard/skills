# Checkable annotations — which tool reports which defect

Read this when deciding whether a tag is checked by anything, or when configuring a repository's lint rules
for annotations.

**An annotation with no tool that reports its absence or its staleness is a preference, not a rule.** This
file is the map from each annotation class to the tool that reports it. Where no tool exists, this skill's
own checker is the tool, and where even that cannot reach, the file says so instead of implying coverage.

## The map

| Annotation class | Reported by | Not reported by |
|---|---|---|
| A parameter type in a JavaScript module | `tsc` / `vue-tsc`, but **only** under `checkJs` or a `// @ts-check` pragma | anything, when `allowJs` is on and `checkJs` is off |
| A parameter type in a TypeScript module | nothing — it is read and discarded | `tsc`, `vue-tsc`, `oxlint` |
| A redundant `@param {Type}` in a TypeScript module | `eslint-plugin-jsdoc` `check-tag-names` in `typed` mode; otherwise this skill's `ANN401` | the compiler |
| A `@param` naming a parameter that does not exist | `eslint-plugin-jsdoc` `check-param-names` | the compiler |
| A missing `@param` on a documented function | `eslint-plugin-jsdoc` `require-param` | the compiler |
| A docblock that only restates the signature | `eslint-plugin-jsdoc` `informative-docs` | the compiler |
| A missing docblock on a cross-file export | this skill's `ANN101` | every linter in the fleet's frontend repos |
| A `NOTE:` prefix outside the closed set | this skill's `ANN201` | everything else |
| A security annotation with no verification date | this skill's `ANN301` | everything else |
| A security annotation older than the file it documents | this skill's `ANN302` | everything else |
| A Stack Overflow or issue-tracker URL in a comment | this skill's `ANN501` | everything else |
| A non-ASCII comment body | this skill's `ANN601` | everything else |
| `@throws`, `@deprecated`, `@since`, `@example` content | **nothing anywhere** — these are prose | every tool |

`@throws` is the sharpest case. TypeScript has no checked-exception concept, so a `@throws` tag is never
compared against the function's behavior by any tool at any setting. It is the purest instance of this
skill's ground: its violation is visible only by reading the comment against the code.

## What `vue-tsc` does and does not check

**Tested against the live `client` on 2026-07-28**, with the repository's own installed toolchain —
`vue-tsc` 3.3.6 on TypeScript 6.0.3, Quasar `app-vite` 3.0.0 — by compiling fixtures outside the repository
with that binary. Not asserted from documentation.

| Configuration | JSDoc types in a `.js` file | JSDoc types in `<script>` with no `lang` | JSDoc types in `.ts` or `<script lang="ts">` |
|---|---|---|---|
| `allowJs: true`, `checkJs` unset | **not checked** — a wrong `@param {string}` called with a number produced zero diagnostics and exit 0 | **not checked** | not checked (types come from the signature) |
| `allowJs: true`, `checkJs: true` | **checked** — `TS2345` on the wrong argument | **checked** — `TS2345` inside the SFC | not checked |
| `checkJs` unset, `// @ts-check` at the top of the file | **checked** for that file | n/a | n/a |

In a `.ts` file, `@param {number}` on a `(x: string)` parameter, a `@throws` tag, and an entirely invented
`@nonsenseTag` all produced **zero diagnostics**. The type checker reads JSDoc in TypeScript and discards
it. That is why `ANN401` exists and why a JSDoc type in a `.ts` file is a second, unverified source of truth
rather than a harmless duplicate.

**What this means for the live `client` today:** `.quasar/tsconfig.json` sets `allowJs: true` and does not
set `checkJs`, and `npm run typecheck` is `vue-tsc --noEmit`. So **no JSDoc in the repository is
type-checked by anything at present.** A repository that wants its JavaScript JSDoc to mean something turns
on `checkJs` or adds `// @ts-check` per file; a repository that does not want that must not pretend its
JSDoc types are verified.

## The lint rule set, per repository language mode

`eslint-plugin-jsdoc` is the official capability for the lint-shaped assertions. Wrap it; do not
reimplement it. Re-verify the plugin major and the config form — flat `eslint.config.*` versus legacy
`.eslintrc` — against the repository at the time you configure it.

**TypeScript-first module (`.ts`, `<script lang="ts">`, `<script setup lang="ts">`):**

- `jsdoc/check-tag-names` with `{ "typed": true }` — reports a redundant `@param {Type}` / `@returns
  {Type}` and an invented tag. This is the rule that makes the TypeScript half of `ANN401` a lint error
  rather than a preference, and this skill's checker steps aside when it finds this rule configured.
- `jsdoc/check-param-names` — reports a `@param` whose name no longer matches the signature, which is the
  most common form of a comment that has silently gone stale.
- `jsdoc/informative-docs` — reports a docblock that only restates the identifier.
- Do **not** enable `jsdoc/require-param` or `jsdoc/require-returns` in a TypeScript module; they push
  toward the redundant tags the first rule forbids.

**JavaScript-plus-JSDoc module:**

- `jsdoc/check-tag-names` with `{ "typed": false }`.
- `jsdoc/require-param`, `jsdoc/require-param-type`, `jsdoc/require-returns`, `jsdoc/require-returns-type` —
  here the type in the tag is the only type that exists.
- `jsdoc/check-types`, `jsdoc/no-undefined-types`.
- `jsdoc/check-param-names`, `jsdoc/informative-docs`.

**The switch is per file, not per repository.** Both modes exist in the fleet's frontend repositories, so a
rule set applied repository-wide will be wrong for half the tree. Scope the TypeScript set with an ESLint
`files` override on `**/*.ts`, `**/*.tsx` and `**/*.vue`, and the JavaScript set on `**/*.js`, `**/*.mjs`
and `**/*.cjs`.

**When the repository does not use ESLint at all.** The live `client` lints with `oxlint` 1.73.0 through
`oxlint.config.ts` and ships no `eslint.config.*` and no `eslint-plugin-jsdoc`. `oxlint` has no JSDoc rule
set equivalent to the list above, so on that repository every lint-shaped assertion above is uncovered and
this skill's checker is the only thing asserting them. State that in the pass report rather than implying
lint coverage that does not exist. Adding a linter to a repository is a build-configuration change and
therefore outside a documentation-only pass — raise it, do not do it.

## Configuration this skill reads

| Setting | Where it lives | What it changes |
|---|---|---|
| `allowJs`, `checkJs` | the repo's `tsconfig.json` and whatever it extends | whether JavaScript JSDoc types are checked at all |
| Language mode of the file | the file extension and the `<script lang>` attribute | which lint rule set and which half of `ANN401` applies |
| `eslint-plugin-jsdoc` presence and `check-tag-names` `typed` | `package.json` plus `eslint.config.*` or `.eslintrc*` | whether the checker asserts `ANN401` itself or defers to the plugin |
| The prefix set | this skill, closed at five | never repo-configurable; a repo-local sixth prefix defeats the grep index |
