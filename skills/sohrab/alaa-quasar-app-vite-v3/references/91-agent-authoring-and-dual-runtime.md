# Authoring notes for this pack

You are about to edit this skill's own files or scripts. This file holds only what is **specific to this pack**.

General agent-authoring doctrine — how to write a skill, how to write an instruction file, runtime differences, effort and thinking budgets, trigger syntax, and model selection — is `/alaa-prompting-guide` (`$alaa-prompting-guide`): `references/06-invocation-and-composition.md`, `references/50-effort-and-thinking.md`, `references/60-skill-authoring.md`, `references/70-agent-instruction-files.md`. Read it there. **State no model name anywhere in this pack**; refer to runtime families when a distinction is genuinely needed, and route the question to the prompting guide.

## 1. The example convention, with Quasar examples

A high-value rule is written as a short reasoned contrast pair. Every ❌ needs a concrete ✅; a bare prohibition does not steer action.

```text
✅ Do — <correct action and the reason>
❌ Don't — <realistic wrong action and the failure it produces>
```

```text
❌ Don't — `import { defineBoot } from '#q-app/wrappers'` in v3; that path is v2 and the build fails at config load.
✅ Do — after confirming app-vite v3, `import { defineBoot } from '#q-app'`.
```

The Quasar-specific reason this convention earns its space: the two app-vite lines are shape-compatible enough that a wrong-line import reads as correct. A prohibition alone leaves the reader without the right shape, and the failure it produces is usually reported as a Vite error, not a Quasar one.

## 2. Why this pack ships two scripts

- `scripts/check-upstream-versions.mjs` exists because every version number in this pack expires, and a live registry read is deterministic while model memory is not. It is the fleet's only copy; `/alaa-frontend-developer` (`$alaa-frontend-developer`) routes here rather than keeping a duplicate.
- `scripts/query-installed-quasar-api.mjs` exists because exact Quasar APIs belong to the target project's installed version, not to this pack. It resolves the project-local CLI, preserves its exit status, and refuses to execute a binary that resolves outside the installed package. This script is why the atlases can be judgment references rather than API mirrors.

Both take `--help` and `--self-test`, and both distinguish "could not run" from "clean" in their exit codes. Keep those three properties in any change.

## 3. Structure rules for this pack

- `SKILL.md` is the lean entry: posture, version rules, authority, one pointer to the router, mandatory pairings, companion boundary, and the response contract. It carries no routing table and no version snapshot. The body ceiling is 6,700 bytes net of the frontmatter description.
- `references/00-topic-map.md` is the only routing surface. The family tables inside `60`, `64`, `35`, and `85` index symbols or legacy names within one topic; if one of them starts routing across the skill, fold it back into `00`.
- `references/05-authority-and-api-lookup.md` owns the authority ladder, the installed lookup, fallbacks, and disagreement handling.
- `references/80-upstream-deltas-and-live-checks.md` owns every version number and the canonical v2 -> v3 delta table. When a number is needed elsewhere, point here instead of copying it — the six-fold duplication of the delta set produced a factual contradiction in the `sourceFiles` default that survived undetected.
- Every reference states its trigger in its first paragraph as an observable situation, and ends with a `Search:` line.
- Details stay one level deep under `references/`. Unread bundled files cost no context, so a comprehensive reference set is acceptable when the routing is precise.
- Use absolute dates, never "recently". Use forward-slash local paths, never wrapped in `file://` or a URL scheme.
- A cross-skill reference names the owning skill beside the path, and gives both trigger forms: the slash form first, then the dollar form in parentheses, then the file path. `agents/openai.yaml` is a Codex-runtime file and stays dollar-form only.

## 4. Maintenance checklist

1. A version, import path, config key, or folder changed: update `references/80-upstream-deltas-and-live-checks.md` and every occurrence of the old string across the pack. Updating one place leaves the pack contradicting itself.
2. Recheck the v2 and v3 config, CLI, mode, SSR, and PWA examples; remove any contradiction; add a Do/Don't pair only where it changes behaviour.
3. Run `node scripts/check-upstream-versions.mjs --self-test`, then a live run; refresh the snapshot and its date.
4. Run `node scripts/query-installed-quasar-api.mjs --self-test`, then the project checks in `references/80-upstream-deltas-and-live-checks.md` §7.
5. Confirm realistic prompts still route correctly through `SKILL.md` and `references/00-topic-map.md`.
6. Confirm no file states a version number that `80` does not, and that no file states a model name.

Search: `authoring`, `do dont pair`, `router`, `body ceiling`, `snapshot ownership`, `self-test`, `trigger form`, `maintenance checklist`.
