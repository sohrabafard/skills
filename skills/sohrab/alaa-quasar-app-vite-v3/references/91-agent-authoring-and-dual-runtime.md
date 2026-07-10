# Agent Authoring and Dual-Runtime Notes

Use this file when **editing or extending this skill pack itself**, not when answering a Quasar question. It captures how the pack is written so it works well for both runtimes that consume it: Claude Code and the GPT-5 / Codex family.

If you only want Quasar guidance, you do not need this file.

## Table of contents

- Who consumes this pack
- The example convention used everywhere in this pack
- Rules that serve both runtimes
- Claude Code consumer specifics
- GPT-5 / Codex specifics
- Structure and progressive disclosure
- Maintenance checklist

## Who consumes this pack

Agents loading this pack are almost always one of:

- **Claude Code models** invoking the pack through Agent Skills. Keep model-specific tuning in `$alaa-prompting-guide`; this Quasar pack should stay model-family-neutral.
- **GPT-5 / Codex family** agents. In setups that expose these packs as skills to Codex — this repo ships an `agents/openai.yaml` interface per pack — Codex discovers and invokes them through `SKILL.md` frontmatter (`name`/`description`) and trigger quality. Frontmatter and `agents/openai.yaml` are first-class, not optional. Where no skill mechanism is available, the same content reaches Codex through repo instructions (`AGENTS.md`) or explicit file references. Either way, write for trigger quality and literal instruction-following.

Write for **the more literal, less-inferring reader**. Current Claude and GPT/Codex models follow scoped instructions closely and spend unnecessary reasoning on vague or contradictory rules. Content that satisfies both is explicit, scoped, and internally consistent.

Note: model lines move fast. Refer to runtime families ("GPT-5 / Codex", "Claude Code") and route exact model behavior to `$alaa-prompting-guide` instead of pinning it in this domain pack.

## The example convention used everywhere in this pack

Every high-value rule in this pack is shown as a contrast pair, because both Anthropic and OpenAI guidance favors concrete do/don't pairs in domain sections over prose alone.

```text
✅ Do — <the correct action, with the reason it is correct>
❌ Don't — <the wrong action the agent might take, with why it is wrong>
```

Rules for writing these pairs:

- Pair every `❌ Don't` with a concrete `✅ Do`. A prohibition with no positive alternative is the one form to avoid, because positive framing steers modern models better.
- Make the `❌` a realistic mistake the agent would actually make (a wrong code shape, a wrong import, a wrong assumption), not a strawman.
- Keep both sides short and, where it matters, show the literal code.
- The reason matters: "never X because Y" is followed more reliably than a bare "never X".

✅ Do — show a real wrong-vs-right shape with a reason.

```text
❌ Don't — `import { defineBoot } from '#q-app/wrappers'` in a v3 repo (the path moved to `#q-app`).
✅ Do — `import { defineBoot } from '#q-app'` once you confirm app-vite v3.
```

❌ Don't — write a pure prohibition with no alternative and no reason.

```text
"Never use the wrong import."   // tells the agent nothing actionable
```

## Rules that serve both runtimes

- **Be explicit and scoped.** State exactly where a rule applies. "Apply this to every boot file, not only the first" beats "apply this to boot files".
- **No contradictions.** If two statements can conflict, order them into precedence. Contradictions are actively harmful to GPT-5/Codex output quality.
- **One default with an escape hatch, not a menu.** "Use `srcset`/`sizes`; use a single resized URL only when width/height are fixed" beats listing five options with no default.
- **Consistent terminology.** Pick one term and keep it (always "boot file", always "reference", always "the line" for the app-vite major). Synonyms read as different concepts.
- **Forward-slash paths**, file references as clickable paths, no `file://`/`vscode://`/`https://` wrappers around local paths.
- **No time-relative phrasing in rules.** Convert "recently" / "since last month" into the absolute snapshot in `80-upstream-deltas-and-live-checks.md` or an "old pattern" note. The reader cannot resolve relative dates.
- **Bias to action, but never silently destructive.** Deliver the working change; confirm before hard-to-reverse operations.

## Claude Code consumer specifics

- Do not rely on one example to generalize a rule to a whole category — spell out the category.
- **Positive framing wins.** Prefer "do Y" over "don't do X"; when a prohibition is necessary, attach the reason and the positive alternative.
- **Drop aggressive imperatives.** Modern Claude models can over-trigger on `CRITICAL:` / `YOU MUST`. Normal imperatives ("Use this when…") steer them better. This pack intentionally avoids caps-lock urgency.
- **Avoid over-engineering prompts.** Claude models can add abstractions and files that were not requested; keep instructions to the minimum that preserves the contract.
- Examples are one of the most reliable steering tools; this pack uses small, concrete input/output and do/don't pairs rather than long prose.

## GPT-5 / Codex specifics

- Extremely receptive to instructions, but **contradictions cost reasoning tokens** and degrade output. Keep the pack conflict-free and hierarchically ordered.
- **Do not mandate preambles, upfront plans, or status chatter.** For Codex agentic rollouts, forcing those can cause the model to stop abruptly. At most a one-line acknowledgement.
- **Plan is not the deliverable.** Codex should deliver working changes; reconcile any stated TODOs as Done/Blocked/Cancelled; stop if re-reading the same files without progress.
- **Tool preferences** the pack assumes Codex honors: ripgrep over shell, dedicated tools over raw `cmd`, parallelize independent reads, cite paths as `path:line`.
- **Keep examples to a minimum** (format-only, and never contradicting a stated rule). A contradicting example is treated as a conflicting instruction.

## Structure and progressive disclosure

- `SKILL.md` is the router: triggers, package-manager rule, the app-vite version-detection rule, the convention note, and the routing table. Keep it lean.
- `references/05-authority-and-api-lookup.md` owns source boundaries, installed-API lookup, fallbacks, and disagreement handling.
- Detail lives in `references/*.md`, kept **one level deep** from `SKILL.md` so a partial read still captures scope.
- Any reference over ~100 lines gets a table of contents at the top.
- The version checker stays a script because live refresh is a determinism-worthy job.
- The installed-API bridge stays a script because resolving the target project's local CLI and preserving its exit status must be deterministic. Atlases stay references because they provide judgment, not exhaustive API data.
- Bundled-but-unread files cost zero context until read, so comprehensive references are fine as long as routing keeps them load-on-demand.

## Maintenance checklist

When you change this pack:

- Did a package version, import path, config key, or folder structure change? Update `80-upstream-deltas-and-live-checks.md`, the `SKILL.md` snapshot, and every reference that shows the old shape (search the whole pack for the old string).
- Is the app-vite v2-vs-v3 split still represented correctly in every config/CLI/mode/SSR/PWA example?
- Does every new rule have a `✅ Do` / `❌ Don't` pair where it earns one?
- Did you introduce any contradiction with an existing rule?
- Re-run `node scripts/check-upstream-versions.mjs` and refresh the snapshot date.
- Re-run `scripts/query-installed-quasar-api.mjs` against representative app-vite v2 and v3 projects plus a missing-project failure case.
- Would a realistic Quasar prompt still load the right reference via the routing table and `00-topic-map.md`?
