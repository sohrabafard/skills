# Subagent workflows for documentation tasks

This file states what the tracks are, what each returns, and how the parent merges them. It does
not state how a runtime spawns a subagent: that mechanism belongs to the orchestrator, and a
runtime-specific instruction inside a rule makes the rule wrong on the other runtime. Claude Code
spawns parallel work with the Task tool; Codex spawns it from the parent thread. Both satisfy every
rule below.

## Why subagents help this skill

Documentation-alignment work is broad, read-heavy, and naturally separable: one track explores routes and caller contracts, another inspects storage and cache behavior, another traces errors, events, and logs, and another checks the document graph.

Subagents keep each discovery track bounded, reduce context pollution in the parent thread, and let the parent receive distilled findings instead of raw repository noise. Use them to gather context faster, never to create uncontrolled parallel edits.

## When to use subagents

Use explicit parallel subagents when one or more of these is true:

- the repository is large enough that one agent would spend too long exploring before writing,
- the task spans several documents such as `README.md`, `docs/BIG_PICTURE.md`, `docs/api-summary.md`, `docs/data-architecture.md`, and `docs/errors-events-observability.md`,
- the source-of-truth files are spread across independent surfaces such as routes, storage, and observability,
- you need a broader fact base before deciding the final wording or document split.

## When NOT to use subagents

- the task is a small single-file touch-up,
- the next step depends tightly on the previous result, so parallel work would idle or conflict,
- the work is write-heavy and two agents would likely edit the same file,
- the runtime does not support explicit parallel subagents.

## Parent-agent responsibilities

The parent owns the workflow and the final output. It decides which documents are in scope and whether the task is large enough for subagents; defines the work split, whether to wait for all results, and what each subagent must return; reconciles conflicting findings; writes the final documents or assigns isolated follow-up edits with a named merge owner; and runs the final validation.

## Recommended track split and fan-out bound

For a broad repository-documentation refresh, start with these four read-heavy tracks:

1. **Document graph and entrypoints** — scope: current `README.md`, `docs/BIG_PICTURE.md`, existing deep-dive documents, and the internal link graph. Output: navigation gaps, broken links, duplicated sections, and the required README or BIG_PICTURE updates.
2. **API surface and caller contracts** — scope: routes, validation, controllers, serializers, auth middleware, and Postman or contract artifacts. Output: canonical endpoint inventory, request-shape changes, caller-visible headers, and `docs/api-summary.md` recommendations.
3. **Storage and request flow** — scope: migrations, schema, models or entities, repositories, cache helpers, outbox or read models, and one representative request path. Output: store inventory, key tables or collections, cache namespaces, lifecycle or invalidation rules, and `docs/data-architecture.md` recommendations.
4. **Errors, events, and observability** — scope: exception handlers, error resources, event classes, listeners, jobs, schedulers, logging, tracing, metrics, alerts, and any dashboards or runbooks. Output: error-matrix candidates, event inventory, payload notes, log and trace fields, and `docs/errors-events-observability.md` recommendations.

Add a fifth track for final cross-checking or link validation only when the repository is especially large or the document graph is messy.

**Fan-out bound:** five concurrent tracks is the ceiling for this skill, and each track's scope must be disjoint from the others by directory or by surface. Splitting one surface across two agents duplicates the reading and doubles the context spent for no extra evidence; the context budget itself is `/alaa-low-noise`'s (`$alaa-low-noise`). If a track is too large for one agent, narrow its scope and run it twice in sequence rather than widening the fan-out.

## Return contract for each subagent

Each subagent returns a compact, source-backed handoff with: the source-of-truth files it checked; its concrete findings and verified claims; the exact documents and sections that should change; minimal proposed headings, bullets, or examples; the uncertainties that still need direct verification; and file references for the parent.

Default rule: subagents do not edit files. They gather evidence and propose updates, unless the parent delegates one isolated file with no overlap risk.

## When a subagent fails or returns nothing

An empty return is not a clean track. Treat it as uncovered ground and act in this order:

1. Re-run that one track once, with a narrower scope — one directory or one surface rather than the whole track.
2. If the second run also returns nothing, the parent reads that track's primary source-of-truth files directly, or removes the track's subject from this task's scope.
3. Either way, name the track and its outcome in the output checklist in `references/40-sync-workflow-and-evidence.md`. Never let an absent track read as a covered one: a section written from no evidence is the failure this rule prevents.
4. Never fill a missing track's section from the other tracks' findings or from plausible inference.

## Merge and conflict-resolution rules

- The parent agent is the merge owner for the final wording.
- When two subagents disagree, prefer code, config, migrations, tests, and runtime artifacts over any stale document.
- If the disagreement is still unresolved, keep the document precise about the uncertainty and state the verification path instead of guessing.
- Never let two subagents edit the same Markdown file concurrently.
- If you do delegate writing, split ownership by file, never by overlapping sections of one file.

## Example parent instruction

The wording below is runtime-neutral. Use it with whichever spawning mechanism the active runtime provides.

```text
Run this documentation refresh as four parallel read-only discovery tracks, and wait for all four
before any writing begins.
1) Document graph, README and BIG_PICTURE gaps
2) API surface and caller contracts
3) Storage, tables, cache, and one representative request flow
4) Errors, events, logs, traces, and observability
Each track returns: source-of-truth files checked, verified findings, the exact documents or
sections that should change, and unresolved questions. No track edits a file. I consolidate and
write every final document in the parent thread.
```

## Role selection

When the project or user has custom agent definitions, prefer the one whose description matches the track — a document explorer, API cartographer, storage mapper, or observability reviewer. When none fits, use a read-heavy exploration role for discovery and evidence gathering, a general role for follow-up when no sharper one exists, and a deterministic worker role only for isolated validation that cannot collide with another agent's edits.

## Validation after subagent work

1. Reconcile overlaps and contradictions in the parent thread.
2. Write or update the documents serially, with one merge owner per file.
3. Re-open the changed documents and verify the links between them.
4. Run `python $SKILL_DIR/scripts/check_markdown_links.py <repo-root>`, and treat exit `2` as "not
   checked".
5. Re-check the output checklist in `references/40-sync-workflow-and-evidence.md`, including the tracks that returned nothing.
