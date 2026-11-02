---
name: citing-skill
---
# Citing skill

Form 1 - the token-adjacency trap. An intervening backtick and closing parenthesis separate
the owner from the path, and a resolver requiring adjacency rejects this whole form:

| Subject | Owner and path |
| --- | --- |
| test design, layers, doubles, proof levels | `/owner-skill` (`$owner-skill`) `references/40-proof-strength.md` |

Form 2 - owner named after the path, in a two-column table:

| Identifier encode/decode, and `scripts/codec-conformance.sh` | `/other-owner` (`$other-owner`) |
| --- | --- |

Form 3 - owner as an explicit path prefix: `owner-skill/references/40-proof-strength.md`.

Form 4 - the extension-ordering trap: `owner-skill/references/arvan-caas-openAPI-1.25.json`.

Form 5 - an illustrative sentence inside a code span, which is not a citation:
`Read references/failure-taxonomy.md when a check fails`.

Form 6 - retirement prose. The exclusion is same-line only, so the retiring words and the
path must share a line: this replaces the former `references/full-guide.md` entirely.

Form 7 - a relative path resolved against the citing file's directory is exercised in
`references/30-relative.md`.
