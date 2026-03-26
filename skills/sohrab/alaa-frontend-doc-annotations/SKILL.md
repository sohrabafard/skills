---
name: alaa-frontend-doc-annotations
description: "Portable documentation-only skill for Vue, Quasar, and Vite frontends with SSR or PWA concerns. Use when the task is to add or improve English JSDoc and inline comments without changing runtime behavior."
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
3. Read `references/10-annotation-boundaries.md`.
4. Load only the smallest additional reference file needed for the code surface.
5. Keep diffs limited to comments and JSDoc.

## Companion routing

- Frontend policy, SSR behavior, or Quasar-specific context:
  - pair with `$alaa-frontend-developer`
- Quasar-specific API or config details:
  - pair with `$quasar-skill-packe`
- Broader repo docs and README alignment:
  - pair with `$alaa-docs-farsi`

## Reference navigation

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
- If the repo’s frontend architecture evolves, refresh the SSR and lifecycle notes first.
