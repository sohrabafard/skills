# Knowledge Shape

What a durable note must contain, what vocabulary it uses, and what never enters the store. Store-agnostic:
every rule here is about the knowledge, not about the product holding it.

## Search before you create

Before creating a note, search for one that already covers the topic by title, permalink, project, domain,
canonical source path, and synonym. Update that note instead of adding a second. Two notes on one topic do not
merely waste space; they create a disagreement with no drift record, and the next agent picks whichever it
found first.

## Required frontmatter

```yaml
title:
type:
status:
confidence:
permalink:
tags:
canonical_source_paths:
last_verified:
```

Use `last_curated` in place of `last_verified` for lessons and patterns drawn from processed evidence rather
than from a source file.

`canonical_source_paths` and `last_verified` are the fields that make staleness detectable. A note that
records a fact from a repository file and does not name that file cannot be re-verified by anything, so it
decays without a symptom. `scripts/alaa_memory_staleness.ps1` is the checker that enforces both, and it is the
reason these two fields are required rather than recommended.

- `status`: `draft`, `active`, `needs_review`, `stale`, `archived`, `superseded`.
- `confidence`: `low`, `medium`, `high`.

## Observation vocabulary

Observations are concise bullets, each carrying exactly one label from this closed set. The set is closed so
that a label can be queried; inventing a new one makes the note invisible to every existing query. Published
lessons carry one additional label from a separate curation axis, which `references/prompt-3-publishing.md`
owns and which does not replace the type label below.

`[rule]`, `[decision]`, `[ownership]`, `[contract]`, `[risk]`, `[validation]`, `[source]`, `[lesson]`,
`[anti_pattern]`, `[boundary]`, `[todo]`, `[question]`, `[gap]`, `[drift]`, `[impact]`, `[stale]`,
`[proposal]`, `[draft_contract]`, `[decision_needed]`.

## Extraction Mode and Design Mode

Extraction Mode is the default. Read the source, record only facts the source supports, and label every hole
`[todo]`, `[question]`, or `[gap]`. An unlabelled hole reads as a fact to the next agent.

Design Mode applies only when explicitly asked to design, standardise, complete, or harden a contract. Every
proposed value carries `[proposal]`, `[draft_contract]`, or `[decision_needed]`, and the note stays `draft` or
`needs_review` until the decision is recorded in repository truth. A Design Mode value that reaches `active`
without that record has become a fact nobody agreed to.

## Store this

- Architecture maps.
- Service ownership: who is accountable for a service. Not what it calls — see the derivation rule below.
- Contract cards: what a contract promises, and the repository path that proves it.
- Operations rules, with their requirement level routed rather than restated.
- Durable lessons and repeated work patterns.
- Project indexes and current-state summaries.
- Concise pointers to plan, state, and handoff files owned by `/alaa-workflow` (`$alaa-workflow`).

## Never store this

One list, and it is the only one. Earlier versions of this skill carried four partial lists that disagreed
about their own membership, so an agent reading the shortest never learned that secrets were on it.

- Raw session transcripts.
- Raw logs.
- Whole source files.
- Whole documents.
- Whole Postman collections; `/alaa-postman-collections` (`$alaa-postman-collections`) owns those artifacts.
- Secrets, credentials, tokens, cookies, and private keys.
- Personal sticky notes and private prompt drafts.
- Draft skill contents, skill candidates as separate notes, and installed skills.
- Active `/alaa-workflow` (`$alaa-workflow`) phase checklists and validation logs.
- Whole work files from the evidence warehouse.
- Service-to-service dependency edges. These are derived; `alaa-signoz-clickhouse-docs`
  `references/50-service-topology.md` owns the derivation. A remembered edge is wrong silently, because
  nothing fails when the call graph changes underneath it.

## Mechanics belong to the vendored pack

The syntax of frontmatter, observations, and wiki-link relations is documented upstream and is not restated
here. Route to the vendored pack by path:

- `vendor/basic-memory/memory-notes/SKILL.md` — note structure, observation categories, relation syntax.
- `vendor/basic-memory/memory-schema/SKILL.md` — schema definitions, validation, schema-versus-usage drift.
- `vendor/basic-memory/memory-metadata-search/SKILL.md` — querying by custom frontmatter fields.

`references/skill-boundaries.md` lists every skill in that pack and which of them are gated.

## Human editing surface

Where the store is file-backed and opened in an editor such as Obsidian, that surface is for navigation and
review, not runtime truth. Two conventions matter there:

- Quote wiki links inside YAML values, because an unquoted `[[…]]` is not valid YAML.
- Keep typed relations in the note body, not in frontmatter, so they stay queryable as relations.

Use the editor's backlink and orphan views to find notes nothing points at, then fix the graph with
`scripts/alaa_obsidian_linkcheck.ps1` rather than by eye. Do not turn graph neatness into an end in itself:
an orphan note that is correct and findable by search is not a defect.
