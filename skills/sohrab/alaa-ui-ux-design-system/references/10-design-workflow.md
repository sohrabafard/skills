# Design Workflow

This file holds the only ordered design procedure in this pack. Read it when a design direction must be chosen rather than inherited.

## Scale the process to the task

Running the full procedure on small work is process theatre. Pick the row that matches what you were asked for.

| The task is | Do |
|---|---|
| a new product, site, or major redesign, or the repo has no persisted design decisions | all four steps below |
| a new page or feature inside an existing system | read the persisted decisions, write a page-level spec, reuse the existing tokens and style. No new direction, no new tokens |
| a component tweak or a visual bug | follow the existing tokens, load the single relevant reference. No brief, no spec, no new tokens |

## Step 0 — Read the repository first

Before proposing anything visual, read what already exists. Existing repo tokens outrank every default in this pack, and a proposal that ignores them will be rejected on sight.

Look for, in this order: the repo-local `AGENTS.md`; `design-system/MASTER.md` or the repo's equivalent; a design-system package or token file; `tailwind.config` or an `@theme` block; Bootstrap variable overrides; the Quasar brand variable file; the app's global stylesheet. On `client` the token source of truth is the `@alaa/design-system` package's stylesheet, and the Quasar brand file and global stylesheet consume it.

If code and `MASTER.md` disagree, inspect which one the product actually ships, fix the stale one, and say which you changed.

## Step 1 — Design brief

Extract from the request and the repo:

- product type and industry
- audience and usage context: consumer or professional, mobile-first or desk-bound, casual or high-stakes
- tone keywords
- density appetite: marketing-spacious, standard, or dashboard-dense
- motion appetite: subtle, standard, or expressive
- hard constraints: existing brand assets, the RTL and Persian requirement, dark-mode requirement, Tailwind or Bootstrap, the Quasar component set, the accessibility target, the performance budget

The performance budget is not this skill's number. Take it from `/alaa-frontend-developer` (`$alaa-frontend-developer`) `references/41-lighthouse-and-web-vitals.md`, cite it, and do not restate the value here or anywhere else in this pack. The design consequence that *is* ours: a direction whose hero cannot be server-rendered and fit inside that budget is not shippable, so choose the hero treatment with the budget already in hand.

**Unanswered questions are handled by a rule, not by judgement.** For each brief question the request does not answer, take the value from the matching row of the Step 2 table, list it under "Assumptions" at the top of the deliverable, and continue. If the *product type itself* is unknown, that one question is asked and the work stops until it is answered — every row of Step 2 keys off it.

## Step 2 — Map product intent to direction

A starting hypothesis, taste tier. Every row may be overridden with a stated reason.

| Product intent | Direction bias | Palette bias | Type bias | Motion |
|---|---|---|---|---|
| Trust-heavy (fintech, health, government, education administration) | conservative, minimal or flat, high clarity | blue, teal or green; restrained accent | neutral sans, strong hierarchy | subtle |
| SaaS / productivity | modern minimal, generous whitespace, one signature effect | trust primary plus one warm accent | geometric or neutral sans | standard |
| Dashboard / ops / pro tools | dense, tabular, content-first; effects minimal | desaturated surfaces, semantic status roles | compact scale, tabular numerals | subtle; never animate data entry |
| E-commerce / conversion | clear hierarchy, strong action rhythm, social proof | high-contrast accent, product imagery leads | confident sans, generous display sizes | standard |
| Premium / luxury | refined, editorial, restrained glass or aurora accents | deep neutrals plus one metallic or jewel accent | serif display plus sans body | subtle, choreographed |
| Content / media / education (consumer) | content-first, imagery-led, readable measure | derived from content imagery, calm surfaces | readable body first, expressive display | standard |
| Playful / youth / creative | vibrant, rounded or bento, expressive | saturated multi-hue, still passing the contrast gate | rounded or display sans | expressive, still gated |

Decision rules that fire from the brief:

- conversion-focused: exactly one high-contrast accent, reserved for primary actions, never spent on decoration
- data-dense: the dense spacing tier (`20-design-tokens-and-theming.md`) and no decorative effects
- premium: slow nothing down. Premium reads as fast, decisive and restrained, never as heavy animation
- accessibility-critical audience: exclude every style whose "Do not use for" column names critical accessibility (`40-styles-and-visual-language.md`)
- Persian-first: `05-rtl-and-persian.md` is not optional and its font byte budget constrains the type choice before the type choice is made

## Step 3 — Commit the direction as tokens

A direction is real only once it is tokens (`20-design-tokens-and-theming.md`): semantic colors with their `on-*` pairs, type scale, spacing tier, radius and shadow scales, motion tokens. Prose moodboards do not survive implementation; tokens do. Run `scripts/check-design-system.mjs` on the result before showing it to anyone — a direction that fails the contrast gate is not a direction.

## Step 4 — Persist the decisions

For multi-page or multi-session work, persist the system in the repo so later sessions and other agents inherit it.

- `design-system/MASTER.md`, or the repo's existing equivalent — the global source of truth: direction summary, token tables, style rules, terminology list, forbidden patterns, shared component index, icon family, motion tier.
- `design-system/pages/<page>.md` — genuine deviations for one page only, such as checkout dropping decorative effects or a dashboard switching to the dense tier.

**Retrieval rule:** when building a page, read `pages/<page>.md` first. If it exists, its rules override `MASTER.md` for that page; otherwise `MASTER.md` applies alone. Never copy `MASTER.md` content into a page file — a page file records deviations and nothing else.

Documentation of individual components lives with the components (`55-component-library-and-governance.md`), not here.

## Anti-patterns

- Generating a full design system for a one-line component tweak.
- Proposing a style before reading the repo's existing tokens.
- A direction that lives in chat prose and never becomes tokens.
- Restating the whole design system in every page file.
- Treating the Step 2 table as law. It is a prior, and a well-argued departure from it is good design.
- Inventing a product constraint the brief did not state, instead of taking the Step 2 default and listing it as an assumption.

## Pairing

- Token architecture and theming: `20-design-tokens-and-theming.md`
- Style trade-offs before committing: `40-styles-and-visual-language.md`
- RTL and Persian constraints that bind the direction: `05-rtl-and-persian.md`
- Implementation in Vue and Quasar, SSR safety: `/alaa-frontend-developer` (`$alaa-frontend-developer`)
- Designing the flow before the pixels: `/alaa-system-design` (`$alaa-system-design`)
