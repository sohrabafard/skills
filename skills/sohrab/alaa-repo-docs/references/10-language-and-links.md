# Language, redaction, and repository-safe links

Read this before writing any sentence, example, or link into a document. It binds every document
this skill produces, in every language.

## Language requirements

- Write documentation in simple, fluent, correct English. English is the source document.
- The user's chat language does not change the documentation language by itself. A Persian
  conversation with no Persian document in the repository still produces an English document.
- Never translate an identifier: enum, table, collection, index, cache-key prefix, header, route,
  class, queue, event, metric, or payload key. Keep technical tokens exactly as implemented in
  code, config, migrations, and Postman artifacts.

## The Persian mirror

The English document is the source and the Persian document is its mirror. This repository already
uses that pattern: `README.md` and `README.fa.md` sit side by side at the pack root.

### When a mirror is mandatory

Produce the mirror when either condition holds. Both are checkable before you start writing:

1. The target repository already contains at least one mirror document — a file whose name ends in
   `.fa.md` or `-fa.md` — or a `docs/fa/` directory. Then every document this skill creates or
   updates in this task ships with its mirror in the same change.
2. The user explicitly asks for a Persian document.

If neither condition holds, do not produce a mirror. An unrequested mirror in a repository that has
no Persian documents doubles the surface that can drift, and nobody asked for it.

### Naming

- Same directory, same stem: `README.md` pairs with `README.fa.md`; `docs/BIG_PICTURE.md` pairs
  with `docs/BIG_PICTURE.fa.md`.
- If the repository already uses `-fa.md` or a `docs/fa/` tree, follow the convention that
  repository already has. Never introduce a second convention beside an existing one.

### What the mirror must match

The mirror translates prose. It does not restructure, reorder, shorten, or extend the source.

- Same headings, in the same order, at the same levels. A section present in one and absent from
  the other is drift, not a translation choice.
- Byte-identical fenced code blocks. Identifiers, payloads, commands, and diagram source are never
  translated, so nothing inside a fence changes between the pair. When the mirror needs a
  translated caption for an example, put it in the prose beside the fence, never inside it.
- Same link targets, which resolve identically because both files sit in the same directory.

### The incompleteness condition

A change to an English document leaves the documentation set **incomplete** until its mirror
carries the same change. An incomplete set is a finding, not a preference: report it under the
output checklist in `references/40-sync-workflow-and-evidence.md` and close it in the same task.

`scripts/check_markdown_links.py` asserts the structural half mechanically:

| Finding | Condition | Fix |
|---|---|---|
| `PAIR-ORPHAN` | A mirror exists with no English source at the matching path. | Write the English source, or rename the file if it was never a mirror. |
| `PAIR-DRIFT` | A pair exists whose heading sequence or fenced-code blocks differ. | Bring the mirror back to the source's structure. The source wins. |
| `PAIR-MISSING` | The repository already has at least one mirror, and one of the documents listed in `SKILL.md` under `## Default document set` has none. | Write the missing mirror, or remove the mirror that made the rule apply. |

The checker cannot tell whether a translated sentence is accurate. It reports that the two
documents no longer describe the same structure, which is the drift class that actually occurs.

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
- Never make an existing strong document weaker, shorter, or more generic unless obsolete content
  is being removed with proof.
- Keep edits minimal and style-preserving: prefer corrections, additions, cross-links, and
  de-duplication over broad rewrites; do not reorder useful sections unless clarity improves; and
  preserve high-signal existing sections that are still accurate.
- If a claim is uncertain, remove the ambiguity and state the verification path instead of
  guessing.
- If you add or refresh any deep-dive document, repair README navigation and related links in the
  same task.

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

- `README.md` is the navigation hub. It links to every major document a new maintainer must read
  next.
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
- When two documents overlap, keep the summary in the broader document and the full detail in the
  narrower one.

## Link validation workflow

- Resolve every repo-local Markdown link before finishing, including same-file and cross-file
  heading anchors.
- Run `python scripts/check_markdown_links.py <repo-root>`, or
  `python scripts/check_markdown_links.py <repo-root> --files <paths>` for a narrow pass. Exit `0`
  is clean, `1` is findings, `2` means the check could not run and nothing was proven.
- That checker validates Markdown-link syntax and English-Persian pairs only. It does not see the
  inline-code path citations that carry most cross-skill references in this pack; those are the
  fleet checker `skills/scripts/check_fleet_references.py`'s subject.
- If Python is unavailable, the check did not run. Verify each touched link by opening its target,
  and record in the output report that the automated check was not available — never report the
  document as validated.
- If a link target is intentionally missing because the repository does not have that document yet,
  create the document or remove the link. Do not leave an aspirational broken link in committed
  documentation.
