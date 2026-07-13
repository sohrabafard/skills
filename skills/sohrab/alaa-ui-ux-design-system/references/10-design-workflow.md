# Design Workflow

Use this file when starting a new product, site, page family, or redesign — anywhere a design direction must be chosen rather than inherited.

## Scale the process to the task

Do not run the full workflow for small work; that is process theater.

- New product, site, or major redesign: full brief -> direction -> tokens -> persist. All steps below.
- New page or feature inside an existing system: read the persisted design decisions first, write a short page-level spec, reuse existing tokens and style. No new direction.
- Component tweak or visual bug: follow existing tokens; load only the single relevant reference. No brief, no new tokens.

## Step 1 — Design brief

Extract from the request and the repo before proposing anything visual:

- product type and industry (SaaS, e-commerce, education, fintech, dashboard/ops, content/media, ...)
- audience and usage context (consumer vs professional; mobile-first vs desk-bound; casual vs high-stakes)
- tone keywords (trustworthy, playful, premium, technical, calm, bold, ...)
- density appetite (marketing-spacious vs dashboard-dense)
- motion appetite (subtle / standard / expressive)
- hard constraints: existing brand assets, Farsi/RTL requirement, dark-mode requirement, Tailwind vs Bootstrap, Quasar component set, accessibility level, performance target (default: Lighthouse >= 90 mobile — a direction whose hero cannot be server-rendered and budget-fit is not shippable)

Missing answers are decisions, not blanks: choose the most defensible default, state the assumption, and continue.

## Step 2 — Map product intent to direction

Use this mapping as a starting hypothesis, not a verdict. Each row is taste-tier — override freely with reasons.

| Product intent | Direction bias | Palette bias | Type bias | Motion |
|---|---|---|---|---|
| Trust-heavy (fintech, health, gov, edu-admin) | conservative, minimal or flat, high clarity | blue/teal/green, restrained accent | neutral sans, strong hierarchy | subtle |
| SaaS / productivity | modern minimal, generous whitespace, one signature effect | trust primary + one warm CTA accent | geometric or neutral sans | standard |
| Dashboard / ops / pro tools | dense, tabular, content-first; effects minimal | desaturated surfaces, semantic status colors | compact scale, tabular numerals | subtle; never animate data entry |
| E-commerce / conversion | clear hierarchy, strong CTA rhythm, social proof | high-contrast CTA accent, product imagery leads | confident sans, generous display sizes | standard |
| Premium / luxury | refined, editorial, restrained glass or aurora accents | deep neutrals + metallic/jewel accent, minimal | serif display + sans body | subtle, choreographed |
| Content / media / education (consumer) | content-first, imagery-led, readable measure | derived from content imagery, calm surfaces | readable body first, expressive display | standard |
| Playful / youth / creative | vibrant, rounded or bento, expressive | saturated multi-hue, still AA-compliant | rounded or display sans | expressive, still gated |

Decision-rule examples (apply when the brief triggers them):

- if conversion-focused -> exactly one high-contrast accent reserved for CTAs; never spend it on decoration
- if data-dense -> switch spacing scale to the dense tier (`20-design-tokens-and-theming.md`) and drop decorative effects
- if premium -> slow nothing down; premium reads as fast, decisive, and restrained, not as heavy animation
- if accessibility-critical audience -> exclude styles flagged "not for critical accessibility" in `40-styles-and-visual-language.md`

## Step 3 — Commit the direction as tokens

A direction is only real once it is expressed as tokens (`20-design-tokens-and-theming.md`): semantic colors, type scale, spacing tier, radius/shadow scale, motion tokens. Prose moodboards do not survive implementation; tokens do.

## Step 4 — Persist decisions (master + page overrides)

For multi-page or multi-session work, persist the design system in the repo so later sessions and other agents inherit it:

- `design-system/MASTER.md` (or the repo's existing equivalent) — the global source of truth: direction summary, token tables, style rules, forbidden patterns.
- `design-system/pages/<page>.md` — only genuine deviations for a specific page (e.g. checkout drops decorative effects; dashboard switches to the dense spacing tier).

Retrieval rule: when building a page, read `pages/<page>.md` first; if it exists, its rules override MASTER; otherwise MASTER applies exclusively. Never duplicate MASTER content into page files — record deviations only.

Repo truth stays canonical: if code and MASTER.md disagree, inspect which one the product actually ships, fix the stale one, and say so.

## Anti-patterns

- Generating a full design system for a one-line component tweak.
- Proposing a style before reading the repo's existing tokens and theme.
- A "direction" that lives only in chat prose and never becomes tokens.
- Restating the entire design system in every page file.
- Treating the mapping table above as law — it is a prior, and a well-argued departure from it is good design.

## Pairing guidance

- Token architecture and theming: `20-design-tokens-and-theming.md`
- Style trade-offs before committing: `40-styles-and-visual-language.md`
- Implementation in Vue/Quasar and SSR safety: `$alaa-frontend-developer`
