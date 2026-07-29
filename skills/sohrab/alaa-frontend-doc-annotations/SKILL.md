---
name: alaa-frontend-doc-annotations
description: "Use this skill for a documentation-only pass over frontend code: JSDoc and inline comments on Vue, Quasar and Vite files, in a diff whose build output is byte-identical before and after. Use it when writing or auditing a JSDoc block on an exported function, store action, composable or fetch wrapper; when adding an SSR, hydration, store, auth or security note; when a comment asserts an authorization, trusted-header or secret-location assumption and must carry a verification date; and when an existing comment may no longer be true of the code beneath it. Do not use it when the task changes behavior: a rule whose violation the compiler, type checker or test suite catches belongs to /alaa-vue-typescript-clean-code ($alaa-vue-typescript-clean-code)."
---

# Frontend doc annotations

**The seam.** A rule whose violation can be caught by compiling, type-checking or running the code belongs
to `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`). A rule whose violation is visible
only by reading a comment against the code it claims to describe — in a diff whose build output must be
byte-identical before and after — belongs here. This pass changes comments; nothing else moves.

**Every comment in a file is English and ASCII-range** — no Persian text or digits, no
typographic dash or quote. Persian belongs in terminal replies and in Persian-language deliverables,
which are `/alaa-docs-farsi` (`$alaa-docs-farsi`).

**The prefix set is closed.** Five prefixes exist and no sixth may be invented: `SSR NOTE:`,
`HYDRATION NOTE:`, `STORE NOTE:`, `AUTH NOTE:`, `SECURITY NOTE:`. Closed means `grep -rn "AUTH NOTE:" src/`
returns every auth assumption in the repo. Every `AUTH NOTE:` and `SECURITY NOTE:` carries
`verified:<ISO-date>` in the same block.

**Run `node scripts/check-annotations.mjs src/ packages/*/src` before reporting done.** Exit `0`
clean, `1` findings as `path:line: RULE message`, `2` could not run — `2` is not `0` because an unparsed
file is not a clean file.

## When NOT to use

Stop when the diff would **change behaviour** — this skill runs only when the build output is byte-identical before and after — and when the rule's violation is already caught by compiling, type-checking or running the code. The section below names each owner.

## Router

| Condition | File |
|---|---|
| Before the first edit; a comment contradicts its code | `references/10-annotation-boundaries.md` |
| Writing a block; choosing a tag | `references/20-jsdoc-patterns.md` |
| SSR flag, lifecycle hook, or store read or write | `references/30-ssr-hydration-and-store-notes.md` |
| A comment names who is authorized, a gateway header, or a secret | `references/40-security-and-trust-annotations.md` |
| Is a tag checked by a tool; lint config for this repo | `references/50-checkable-annotations.md` |
| Judging a `verified:` date; the words current, latest, deprecated, unsupported | `references/60-staleness-and-verification.md` |
| A docblock states an invariant; a repo rule forbids comments | `references/70-invariant-docblocks.md` |
| What a comment may cite as its source | `references/00-source-map.md` |

## Ground this skill does not own

- Comment-versus-extract, SOLID, `any`, abort and double-fire correctness:
  `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`).
- Threat classes: `/alaa-security-review` (`$alaa-security-review`). Gateway and trusted-header facts:
  `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`).
- SSR, hydration, lifecycle: `/alaa-frontend-developer` (`$alaa-frontend-developer`). Quasar API and
  config: `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`).
- Every name and value a comment quotes: `/alaa-services-contract` (`$alaa-services-contract`).
- Model and effort: `/alaa-prompting-guide` (`$alaa-prompting-guide`), `references/50-effort-and-thinking.md`.
- Every other owner: the table in `references/10-annotation-boundaries.md`.
