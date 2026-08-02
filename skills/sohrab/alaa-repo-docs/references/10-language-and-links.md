# Language, topic ownership, redaction, and repository-safe links

Read this before writing any sentence, example, or link into a document. It binds every document
this skill produces, in every language.

## Language preservation

- Preserve the language of each existing document. Do not translate it, rewrite it into a preferred
  language, or create another language variant unless the user explicitly requests that output.
- The user's chat language does not change a document's language by itself.
- For a new document, use an explicitly requested language first. When the request names no
  language, match the established language of the nearest equivalent document, documentation hub,
  or repository instruction; never impose English or Persian as a fleet-wide default.
- If the local documentation uses several languages and no nearest convention resolves a new
  document's language, ask only when the choice materially changes the requested deliverable.
- Never translate an identifier: enum, table, collection, index, cache-key prefix, header, route,
  class, queue, event, metric, or payload key. Keep technical tokens exactly as implemented.

## Explicit localized companions

Create or update a translated or localized companion only when the user explicitly includes that
companion in scope. The existence of `.fa.md`, `-fa.md`, or `docs/fa/` content is evidence of an
existing document, not authorization to create or update another one.

### Naming

- For an explicitly requested Persian companion, use the same directory and the `.fa.md` suffix by
  default: `README.md` pairs with `README.fa.md`, and `docs/BIG_PICTURE.md` pairs with
  `docs/BIG_PICTURE.fa.md`.
- Follow a different naming layout only when a repository instruction or the user's request
  explicitly makes it binding. Do not infer authorization to create companions from that layout.

### Companion structure

When a localized companion is explicitly in scope, translate prose without restructuring,
reordering, shortening, or extending the base document.

- Keep the same headings in the same order and at the same levels.
- Keep fenced code blocks byte-identical.
- Keep link targets identical when the pair shares a directory; recalculate relative targets when
  an explicitly required repository convention places the companion elsewhere.
- Run
  `python $SKILL_DIR/scripts/check_markdown_links.py <repo-root> --files <base> <companion>
  --localized-pair <base> <companion>`. Repeat `--localized-pair` for each additional companion
  explicitly in scope. Pair paths are explicit, so any language suffix or repository-owned layout
  is supported and unrelated companions are not checked.

The checker reports:

| Finding | Condition | Fix |
|---|---|---|
| `PAIR-ORPHAN` | A localized companion has no explicitly named base document. | Create the base only when it belongs in scope, or correct the pair paths. |
| `PAIR-DRIFT` | An explicitly named pair has different heading levels or fenced-code blocks. | Align the explicitly scoped pair; the named base document defines the structure. |

The checker cannot judge translation accuracy. A clean result proves only link resolution and the
structural parity of localized pairs that the command was explicitly asked to check.

### Persian prose rules

- Persian technical terms keep their English forms. Do not translate a term the fleet uses in
  English, such as `middleware`, `outbox`, `idempotency`, `trace`, or `queue`, and never translate
  any identifier named above.
- A Persian sentence that mixes the two starts with a Persian word, so the paragraph reads
  right-to-left from its first character.
- Digits inside identifiers, versions, status codes, and code spans stay ASCII.

## Redaction in committed examples

Documents produced here are committed and often published. Every example is a publication.

| Never in a committed example | Use instead |
|---|---|
| A real bearer token, API key, session cookie, or signature | `Authorization: Bearer PLACEHOLDER_TOKEN` |
| A value copied from `.env`, a vault, or a running container | the variable name and its documented default, with no value |
| A production hostname or internal DNS name | the verified local example host, or `api.example.com` |
| An internal IP address or private CIDR block | `10.0.0.0/8` written explicitly as an illustrative range |
| A real tenant, organisation, account, or user identifier | an obviously synthetic identifier such as `tenant_example` |
| A real customer name, phone number, national ID, or email | a synthetic value in the same format |

- The rule binds every example in every document, including request bodies in
  `docs/api-summary.md`, record shapes in `docs/data-architecture.md`, and log or payload samples
  in `docs/errors-events-observability.md`.
- A placeholder must be recognisable as a placeholder from the value alone. A realistic-looking
  fake is worse than an obvious one, because a reader cannot tell it is not live.
- When you cannot determine whether a value is safe to publish, do not publish it. Whether a
  disclosure is acceptable is `/alaa-security-review`'s (`$alaa-security-review`) decision, not
  this skill's.

## Hard constraints

- Do not patch business logic in a documentation-only request.
- Every statement must be traceable to source code, config, migrations, schema, tests, current
  documents, or runtime artifacts.
- Never make an existing strong document weaker or more generic. Shorten it only by removing
  provably obsolete content or by losslessly extracting clusters under
  `references/15-document-size-and-clustering.md`.
- Keep edits minimal and style-preserving: prefer corrections, additions, cross-links, and
  de-duplication over broad rewrites; do not reorder useful sections unless clarity improves; and
  preserve high-signal existing sections that are still accurate.
- If a claim is uncertain, remove the ambiguity and state the verification path instead of
  guessing.
- If you add or refresh any deep-dive document, repair README navigation and related links in the
  same task.

## Canonical topic ownership and de-duplication

Apply this procedure in every documentation task:

1. Inventory the current documentation hubs, deep dives, contracts, runbooks, and decision records
   before writing.
2. Search the documentation tree for the topic and its canonical identifiers before adding text.
3. Assign the full explanation to exactly one canonical document based on role: README or the
   repository index owns navigation; BIG_PICTURE owns the system map; a topic deep dive owns dense
   detail; a runbook owns procedures; an ADR owns a decision and its rationale; a machine-readable
   contract owns exact schemas.
4. Preserve unique verified facts from every overlapping section. Consolidate the full detail into
   the canonical owner, then replace repeated detail elsewhere with the smallest useful summary and
   a relative link to the canonical section.
5. Do not copy tables, payloads, step lists, diagrams, or normative rules into several documents.
   If two audiences need the same detail, link both audiences to one owner.
6. When no canonical document exists, place the topic in the strongest existing equivalent rather
   than creating a near-duplicate. Create a new deep dive only when its role is distinct and the
   task authorizes that document.
7. Re-run the search after editing. Any remaining repeated detail must either have a distinct
   audience-specific purpose stated in the text or be reduced to a link.

## Repository-safe links in generated documents

- Every link must be repo-portable: valid after clone, valid in a GitHub or GitLab web viewer, and
  independent of the local machine path.
- Never use a local filesystem absolute path such as `D:/...`, `C:\...`, `/home/...`, or
  `file:///...` in generated Markdown.
- Use POSIX-style separators only. Never use a Windows backslash in a link.
- Prefer a relative link from the current document location, such as `./file.md`, `../file.md`, or
  `../../platform/openfga/model.fga`.
- Before finalising, confirm the target exists in the repository, the relative path is correct from
  the current document's directory, and any heading anchor points at a real heading.
- If a correct Markdown link cannot be guaranteed, fall back to a plain inline code path such as
  `platform/openfga/model.fga` instead of inventing a broken hyperlink.
- Correct: `OpenFGA model -> ../../platform/openfga/model.fga`;
  `Data architecture -> ./data-architecture.md#representative-request-walkthrough`;
  `platform/openfga/model.fga`.
- Incorrect: `model.fga -> D:/repo/platform/openfga/model.fga`;
  `model.fga -> C:\repo\platform\openfga\model.fga`;
  `model.fga -> file:///D:/repo/...`.

## Documentation graph and internal linking rules

- Use the repository's declared documentation index as the navigation hub. Use `README.md` when no
  separate index is declared.
- Make every major maintained document reachable from the hub through repo-relative Markdown
  links. A new or changed deep dive is incomplete while it is orphaned.
- `docs/BIG_PICTURE.md` is the architecture and runtime map. It summarises and points to deeper
  documents rather than copying every table, cache key, event, or error matrix.
- `docs/api-summary.md` links back to `README.md` and `docs/BIG_PICTURE.md`, and to the deep-dive
  documents when those links materially help a caller understand side effects, storage, or error
  behaviour.
- `docs/data-architecture.md` links to `README.md`, `docs/BIG_PICTURE.md`, `docs/api-summary.md`
  when API requests drive the walkthrough, and `docs/errors-events-observability.md` when async
  handoff or correlation matters.
- `docs/errors-events-observability.md` links to `README.md`, `docs/BIG_PICTURE.md`,
  `docs/api-summary.md` when error contracts are caller-visible, and `docs/data-architecture.md`
  when event payloads or failures depend on stored state.
- Prefer a small `Related docs` or `See also` block near the top or end of each document over
  repeated navigation paragraphs.
- Give each changed deep dive a link back to the hub and links to the canonical neighboring
  documents needed to understand its inputs, outputs, or side effects.
- Link directly to the owning section when the target renderer supports stable heading anchors;
  otherwise link to the owning document and name the section in prose.

## Link validation workflow

- Resolve every repo-local Markdown link before finishing, including same-file and cross-file
  heading anchors.
- Run `python $SKILL_DIR/scripts/check_markdown_links.py <repo-root>`, or
  `python $SKILL_DIR/scripts/check_markdown_links.py <repo-root> --files <paths>` for a narrow
  pass. Exit `0` is clean, `1` is findings, `2` means the check could not run and nothing was
  proven.
- By default the checker validates Markdown-link syntax only. Add
  `--localized-pair <base> <companion>` only when that localized companion is explicitly in scope;
  repeat the option for more explicitly scoped pairs. It does not see the inline-code path citations
  that carry most cross-skill references in this pack; those are the fleet checker
  `skills/scripts/check_fleet_references.py`'s subject.
- If Python is unavailable, the check did not run. Verify each touched link by opening its target,
  and record in the output report that the automated check was not available — never report the
  document as validated.
- If a link target is intentionally missing because the repository does not have that document yet,
  create the document or remove the link. Do not leave an aspirational broken link in committed
  documentation.
