# Documentation routing

/alaa-repo-docs owns repository Markdown authoring, canonical topic ownership, language, navigation, alignment, redaction and link validation. /alaa-frontend-doc-annotations owns source comments/docblocks. This reference selects their evidence surfaces.

| Question | Surface |
|---|---|
| Which Markdown file contains a phrase, heading, endpoint, event or identifier? | Markdown-scoped native search/read |
| Which document is canonical, what must change, or are links valid? | /alaa-repo-docs |
| Does a documentation claim match source behavior? | Documentation owner names the implementation/runtime/configuration fact, then selects its routing-contract owner |
| Is generated Markdown current? | Source template and generator |
| What do installed Laravel package docs say? | Boost documentation |
| What do other current package docs say? | Official version-aware source |

CodeGraph contributes supported implementation evidence; it does not own Markdown. This pack does not enable Markdown in Serena by default. Add a Markdown backend only for a named recurring gap, verified health and explicit project decision; documentation ownership remains unchanged. Do not add a provider merely for repository text search; use the bundled native guide.
