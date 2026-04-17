# Subagent workflows for documentation tasks

## Includes these full-guide sections

- `# Standard subagent workflow for documentation tasks`
- `## Why subagents help this skill`
- `## When to use subagents`
- `## When NOT to use subagents`
- `## Parent-agent responsibilities`
- `## Recommended subagent split`
- `## Return contract for each subagent`
- `## Merge and conflict-resolution rules`
- `## Example parent prompts`
- `## Custom-agent guidance`
- `## Validation after subagent work`

# Standard subagent workflow for documentation tasks

## Why subagents help this skill
Documentation-alignment work is usually broad, read-heavy, and naturally separable: one track explores routes and caller contracts, another inspects storage and cache behavior, another traces errors and events and logs, and another checks the document graph.

Subagents help by keeping each discovery track bounded, reducing context pollution in the parent thread, and letting the parent agent receive distilled findings instead of raw repo noise. Use them to gather context faster, not to create uncontrolled parallel edits.

## When to use subagents
Use explicit parallel subagents when one or more of these are true:
- the repository is large enough that one agent would spend too long exploring before writing,
- the task spans several docs such as `README.md`, `docs/BIG_PICTURE.md`, `docs/api-summary.md`, `docs/data-architecture.md`, and `docs/errors-events-observability.md`,
- the relevant source-of-truth files are spread across independent surfaces such as routes, storage, and observability,
- you need a broader fact base before deciding the final wording or document split.

## When NOT to use subagents
Avoid subagents when:
- the task is a small single-file touch-up,
- the next step depends tightly on the previous result and parallel work would just idle or conflict,
- the work is write-heavy and multiple agents would likely edit the same file,
- the environment does not support explicit subagent spawning.

## Parent-agent responsibilities
The parent agent owns the workflow and final output. It must:
- decide which docs are in scope,
- decide whether the task is large enough for subagents,
- explicitly ask Codex to spawn the subagents,
- define the work split, whether Codex should wait for all results, and what each subagent must return,
- reconcile conflicting findings,
- write the final docs or assign isolated follow-up edits with a clear merge owner,
- run final validation.

## Recommended subagent split
For a broad repository-doc refresh, start with four read-heavy tracks:

1. **Doc graph and entrypoints**
   - Scope: current `README.md`, `docs/BIG_PICTURE.md`, existing deep-dive docs, and internal link graph.
   - Output: navigation gaps, broken links, duplicated sections, and required README or BIG_PICTURE updates.

2. **API surface and caller contracts**
   - Scope: routes, validation, controllers, serializers, auth middleware, and Postman or OpenAPI artifacts.
   - Output: canonical endpoint inventory, request-shape changes, caller-visible headers, and `docs/api-summary.md` recommendations.

3. **Storage and request flow**
   - Scope: migrations, schema, models or entities, repositories, cache helpers, outbox or read models, and one representative request path.
   - Output: store inventory, key tables or collections, cache namespaces, lifecycle or invalidation rules, and `docs/data-architecture.md` recommendations.

4. **Errors, events, and observability**
   - Scope: exception handlers, error resources, event classes, listeners, jobs, schedulers, logging, tracing, metrics, alerts, and dashboards or runbooks when available.
   - Output: error matrix candidates, event inventory, payload notes, log or trace fields, and `docs/errors-events-observability.md` recommendations.

Add a fifth subagent for final cross-checking or link validation only when the repo is especially large or the doc graph is messy.

## Return contract for each subagent
Each subagent should return a compact, source-backed handoff with:
- source-of-truth files checked,
- concrete findings and verified claims,
- exact docs and sections that should change,
- minimal proposed headings, bullets, or examples to add,
- uncertainties that still need direct verification,
- file references for the parent agent.

Default rule: subagents should not edit files. They should gather evidence and propose updates unless the parent agent delegates one isolated file with no overlap risk.

## Merge and conflict-resolution rules
- The parent agent is the merge owner for final wording.
- When two subagents disagree, prefer code, config, migrations, tests, and runtime artifacts over stale docs.
- If the disagreement remains unresolved, keep the doc precise about the uncertainty and include the verification path instead of guessing.
- Do not let multiple subagents edit the same Markdown file concurrently.
- If you do delegate writing, split ownership by file, not by overlapping sections of the same file.

## Example parent prompts
Use prompts like these from the parent thread when the environment supports subagents:

```text
Use parallel subagents for this documentation refresh. Spawn four read-only subagents and wait for all results before writing.
1) Doc graph and README/BIG_PICTURE gaps
2) API surface and caller contracts
3) Storage, tables, cache, and one representative request flow
4) Errors, events, logs, traces, and observability
Each subagent must return: source-of-truth files checked, verified findings, exact docs or sections that should change, and unresolved questions. Do not edit files. I will consolidate and write the final docs in the parent thread.
```

```text
Use one explorer subagent per documentation surface. Wait for all of them, then merge the findings into `README.md`, `docs/BIG_PICTURE.md`, `docs/api-summary.md`, `docs/data-architecture.md`, and `docs/errors-events-observability.md` as needed. Keep all writes in the parent thread unless a delegated file is fully isolated.
```

## Custom-agent guidance
If the project or user has custom agents under `.codex/agents/` or `~/.codex/agents/`, prefer the one whose description best matches the track, such as a doc explorer, API cartographer, storage mapper, or observability reviewer.

If no custom agent fits, start with built-in roles this way:
- `explorer` for read-heavy discovery and evidence gathering,
- `default` for general follow-up when no sharper role exists,
- `worker` for isolated deterministic validation or implementation follow-up after the evidence is already gathered.

## Validation after subagent work
After all subagents return:
1. Reconcile overlaps and contradictions in the parent thread.
2. Write or update the docs serially with one clear merge owner per file.
3. Re-open the changed docs and verify the links between them.
4. Run `scripts/check_markdown_links.py` when Python is available.
5. Re-check the output checklist in `references/40-sync-workflow-and-evidence.md`.
