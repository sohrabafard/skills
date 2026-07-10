# Agent Authoring and Dual-Runtime Notes

Use only when editing/extending this pack. It targets Claude Code Agent Skills and GPT-5/Codex; keep model-specific tuning in `$alaa-prompting-guide`. Codex discovery uses `SKILL.md` `name`/`description` plus `agents/openai.yaml`; without skills, content may arrive via `AGENTS.md` or explicit references. Treat both interfaces as first-class. Write for the more literal, less-inferring reader: explicit scope, consistency, and strong triggers. Refer to runtime families, not fast-aging model IDs.

## Example convention

High-value rules use realistic, short, reasoned contrast pairs:

```text
✅ Do — <correct action and reason>
❌ Don't — <realistic wrong action and failure>
```

Every Don't needs a concrete Do; show literal code when valuable. Bare prohibitions do not steer action.

```text
❌ Don't — `import { defineBoot } from '#q-app/wrappers'` in v3; that path is v2.
✅ Do — after confirming app-vite v3, `import { defineBoot } from '#q-app'`.
```

## Shared rules

- Scope literally (“every boot file”, not “boot files”). Resolve possible conflicts by explicit precedence; contradictions waste reasoning and degrade output.
- Give one default + escape hatch, not an unranked menu: default `srcset`/`sizes`; one resized URL only for fixed width/height.
- Use one term consistently (`boot file`, `reference`, app-vite `line`).
- Use forward-slash clickable local paths; never wrap them with `file://`, `vscode://`, or `https://`.
- Use absolute dates or the snapshot in `80-upstream-deltas-and-live-checks.md`, never “recently”.
- Bias to the working change, but confirm hard-to-reverse actions.

## Runtime-specific guidance

| Claude Code | GPT-5 / Codex |
| --- | --- |
| Spell out a category; one example may not generalize. Prefer positive framing; pair necessary prohibitions with reason + alternative. | Keep hierarchy conflict-free; contradictions cost reasoning tokens. |
| Avoid `CRITICAL:`/`YOU MUST` urgency; normal imperatives steer better. | Do not require preambles, upfront plans, or status chatter; at most one-line acknowledgement, because forced chatter can halt agentic runs. |
| Prevent unrequested abstraction/files with the minimum contract-preserving instruction. | A plan is not delivery: make working changes; reconcile TODOs as Done/Blocked/Cancelled; stop rereading without progress. |
| Small concrete input/output and Do/Don't examples steer reliably. | Prefer ripgrep, dedicated tools over raw `cmd`, parallel independent reads, and `path:line` citations. Keep only format-critical, non-conflicting examples. |

## Structure and progressive disclosure

- `SKILL.md` is the lean router: triggers, package-manager rule, app-vite detection, convention, routing table.
- `references/05-authority-and-api-lookup.md` owns authority, installed lookup, fallbacks, and disagreement handling.
- Details stay one level deep in `references/*.md`; add a table of contents above approximately 100 lines.
- Keep the version checker as a script because live refresh needs determinism.
- Keep the installed-API bridge as a script because local-CLI resolution and exit-status preservation need determinism; atlases remain judgment references, not API mirrors.
- Unread bundled files cost no context; comprehensive on-demand references are acceptable when routing is precise.

## Maintenance checklist

- Version/import/config/folder changed: update `80-upstream-deltas-and-live-checks.md`, `SKILL.md` snapshot, and every old-shape occurrence.
- Recheck v2/v3 config/CLI/mode/SSR/PWA examples; remove contradictions; add Do/Don't only where valuable.
- Run `node scripts/check-upstream-versions.mjs`; refresh snapshot date.
- Run `scripts/query-installed-quasar-api.mjs` against representative v2/v3 projects, missing-project failure, narrow symbol, and `list` query.
- Confirm realistic prompts still route via `SKILL.md` and `00-topic-map.md`.
