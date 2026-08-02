# Document size and topic-clustering contract

Read this file whenever this skill creates or refreshes a main document or any child document
extracted from it. The create-or-refresh triggers remain in `SKILL.md`; once a document is in scope,
this file owns its size state and decomposition.

## Size states

Count physical lines after final Markdown formatting, including headings, blank lines, tables,
diagrams, and fenced blocks.

| State | Physical lines | Decision |
|---|---:|---|
| Green | 0-49 | Target state. Stop splitting when the document is coherent. |
| Yellow | 50-100 | Acceptable only when another split would make the topic harder to understand. |
| Orange | 101-200 | Accept only when no coherent green or yellow decomposition exists. |
| Red | 201 or more | Blocked without explicit human approval for the named file and current line count. Prefer restructuring even when approved. |

Every main document this skill creates or refreshes, and every child it creates, must be measured.
The agent's objective is green for every measured file. Yellow or orange requires a concise reason
in the final report explaining why the next split would damage comprehension. Human approval for a
red document expires when its line count or content materially changes.

## Recursive clustering procedure

1. Group the document by cohesive reader questions, source owners, and change cadence. A cluster is
   one related subject set that a reader normally needs together; it is never an arbitrary line
   range.
2. Keep the parent as the compact orientation and routing document. Preserve the minimum summary
   needed to understand the system and decide which child to open.
3. Move each dense cluster into one child document, preserve every verified fact, and replace the
   moved detail with one informative routing sentence and a relative link.
4. Measure the parent and every child. Stop on green documents.
5. For each non-green child, repeat the same semantic clustering and linking procedure recursively.
6. Stop at yellow only when a further split would separate one flow, invariant, decision, or mental
   model that must be read together. Stop at orange only when no coherent green or yellow split
   exists. Never stop at red without the explicit approval defined above.

Splitting authorizes the child documents needed to preserve the in-scope document's existing
knowledge; it does not authorize new product claims or unrelated documentation. The required
structure and coverage in the document-specific contracts may be distributed across the parent
and its linked cluster tree. The parent must still answer each coverage question with a compact
summary or an informative route to exactly one canonical child.

## Routing-sentence contract

Every link from a parent to a child must state both the reader condition and the topics the child
owns. Write it so an agent can decide whether to load the child without opening it.

Good: `When changing runtime modes or deployment topology, read [Runtime and deployment](./big-picture/20-runtime-and-deployment.md) for process roles, readiness dependencies, and environment differences.`

Bad: `See [more details](./big-picture/20-runtime-and-deployment.md).`

Do not use a bare filename, `See also`, or `More information` as the only description of a child.
Do not duplicate the child detail in the parent to make the link self-explanatory; name the owned
topics instead.

## Directory and filename hierarchy

- Keep the established main filenames such as `<repo>/README.md` and
  `<repo>/docs/BIG_PICTURE.md`; they are exempt from the numeric-prefix rule.
- Place first-level children under `<repo>/docs/<parent-stem>/`. Normalize the parent stem to
  lowercase kebab-case: `BIG_PICTURE.md` becomes `docs/big-picture/`.
- Name every child `NN-<cluster-name>.md`, using two digits and lowercase kebab-case. Allocate
  stable ordering slots in tens, such as `10-`, `20-`, and `30-`, so a later file can be inserted
  without renumbering unaffected siblings.
- When a child must split again, create a sibling directory named after that child's full stem and
  apply the same rule inside it. Example:
  `docs/data-architecture/20-cache/10-invalidation.md`.
- Follow a stronger repository-owned documentation directory only when it preserves the same
  explicit hierarchy and two-digit child filenames. Repair all affected relative links in the same
  task.

## Deterministic check

Run the link check required by `references/10-language-and-links.md`, then measure every created or
refreshed document and child with:

`python $SKILL_DIR/scripts/check_markdown_links.py <repo-root> --files <paths> --line-budget`

The command reports every file's state. Exit `1` on an unapproved red document is a failed gate;
exit `2` means nothing was proven. Use `--allow-red <paths>` only after the human explicitly
approves each named file at its current count. Yellow and orange remain reportable exceptions, not
proof that the green objective was attempted.
