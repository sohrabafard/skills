# Knowledge Shape

What a durable note must contain, what vocabulary it uses, and what never enters the store. Store-agnostic:
every rule here is about the knowledge, not about the product holding it.

## Search before you create

Before creating a note, search for one that already covers the topic by title, project, domain,
canonical source path, synonym and any stable identifier the selected adapter supports. Update that note
instead of adding a second: duplicates create disagreement without a drift record, and the next agent
picks whichever it finds first.

## Required semantic metadata

Every note carries `title`, `type`, `status`, `confidence`, `canonical_source_paths` and `last_verified`.
These name knowledge properties, not API keys or a frontmatter requirement; the selected adapter owns
their representation and any product-specific identity or tags.

Use `last_curated` in place of `last_verified` for lessons and patterns drawn from processed evidence rather
than from a source file.

`canonical_source_paths` and `last_verified` are the fields that make staleness detectable. A note that
records a fact from a repository file and does not name that file cannot be re-verified by anything, so it
decays without a symptom. Preserve both through the selected adapter's serialization and verification.

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

## Source language of curated knowledge

For a source-derived candidate or note, choose the language for each prose span from its source. Keep
Persian prose in Persian. Render Arabic, Dari, Tajik, Luri, Bakhtiari, Tati, Talysh, Kurdish, Gilaki,
Mazandarani/Tabari, Balochi, Pashto, Ossetian, and Pamiri prose (including Shughni and Wakhi) in fluent
Persian. Render all other prose in English. Apply these rules separately to the parts of a mixed source;
do not impose one language on the whole document.

Keep names, code, paths, URLs, identifiers, and verbatim quotations exactly as in the source. Check
meaning and provenance against that source; script detection alone does not establish language or
accuracy. If the source or its language is ambiguous, leave the disputed text unchanged and mark the
candidate `needs_review` until the source can be checked.

This policy governs candidate authoring; it does not enforce server-side extraction. Where a store extracts
facts automatically, check each fact against its source and effective processing configuration before
claiming language compliance.

## Store this

- Architecture maps.
- Service ownership: who is accountable for a service. Not what it calls — see the derivation rule below.
- Contract cards: what a contract promises, and the repository path that proves it.
- Operations rules, with their requirement level routed rather than restated.
- Durable lessons and repeated work patterns.
- Project indexes and current-state summaries.
- Concise pointers to plan, state, and handoff files owned by `/alaa-workflow`.

## Never store this

One list, and it is the only one for what may never enter the memory store. Earlier versions of this skill carried four partial lists that disagreed
about their own membership, so an agent reading the shortest never learned that secrets were on it.

- Raw session transcripts.
- Raw logs.
- Whole source files.
- Whole documents.
- Whole Postman collections; `/alaa-postman-collections` owns those artifacts.
- Secrets, credentials, tokens, cookies, and private keys.
- Personal sticky notes and private prompt drafts.
- Draft skill contents, skill candidates as separate notes, and installed skills.
- Active `/alaa-workflow` phase checklists and validation logs.
- Whole work files from the evidence warehouse.
- Service-to-service dependency edges. These are derived; `alaa-signoz-clickhouse-docs`
  `references/50-service-topology.md` owns the derivation. A remembered edge is wrong silently, because
  nothing fails when the call graph changes underneath it.

Nothing on this list becomes storable by being summarised inline on the way in. A transcript, log, or
document reaches the store only as a candidate that `/alaa-extract-agent-lessons` already admitted and shaped. Bulk processing of past conversations is
that same path at volume, not an exception to it.

## Adapter serialization

The selected adapter owns serialization, publication destinations, product-specific identity, tags,
schema/search mechanics and applicable verification. These fields and observations remain store-neutral;
do not load an inactive store's upstream pack.
