---
name: alaa-frontend-doc-annotations
description: "Use this skill when the task involves JSDoc on frontend files or inline comments without logic changes. Do not use it when the task changes behavior."
---




# Alaa Frontend Doc Annotations

## Purpose

Use this skill when the task is a documentation-only annotation pass for frontend code.

This skill adds:

- English JSDoc
- narrow inline comments at reasoning hotspots
- SSR, hydration, store, auth, and lifecycle notes where they help future agents and maintainers

## When to use

Use this skill when the user asks for:

- JSDoc on frontend files
- inline comments without logic changes
- code explanation support through comments
- documentation-only clarity improvements in Vue, Quasar, or Vite code

## When NOT to use

Do not use this skill when:

- the task changes behavior
- the task needs template copywriting or UI text changes
- the task is broader docs work for README or docs pages
- the task is backend-only

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Confirm the task is documentation-only.
3. Read `references/00-source-map.md` when a comment depends on current Vue, Quasar, Vite, SSR, or browser behavior.
4. Read `references/10-annotation-boundaries.md`.
5. Load only the smallest additional reference file needed for the code surface.
6. Keep diffs limited to comments and JSDoc.

## Good vs bad examples

**Good JSDoc**
```js
/**
 * Rebuilds the SSR-safe redirect target from the current route and auth state.
 */
```

**Bad JSDoc**
```js
/**
 * This function does stuff.
 */
```

**Good inline comment**
```js
// Keep this branch client-only so SSR never touches browser storage.
```

**Bad inline comment**
```js
// set value
```
## Companion routing

- Frontend policy, SSR behavior, or Quasar-specific context:
  - pair with `$alaa-frontend-developer`
- Quasar-specific API or config details:
  - pair with `$alaa-quasar-app-vite-v3`
- Broader repo docs and README alignment:
  - pair with `$alaa-docs-farsi`

## Reference navigation

- Official-first source priority, freshness triggers, and community-troubleshooting boundary:
  - `references/00-source-map.md`
- What is allowed in a documentation-only pass:
  - `references/10-annotation-boundaries.md`
- JSDoc shapes, comment styles, and comment density rules:
  - `references/20-jsdoc-patterns.md`
- SSR, hydration, store, auth, and lifecycle notes to capture:
  - `references/30-ssr-hydration-and-store-notes.md`

## Maintenance rules

- Keep this skill documentation-only.
- Keep comments plain, useful, and short.
- Do not let examples drift into behavior changes.
- Re-check official sources before writing comments that claim current, latest, deprecated, or unsupported behavior.
- If the repo’s frontend architecture evolves, refresh the SSR and lifecycle notes first.
