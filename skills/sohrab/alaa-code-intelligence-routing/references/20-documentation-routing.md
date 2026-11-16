# Documentation routing

This file selects evidence surfaces, not annotation policy. /alaa-repo-docs owns repository Markdown authoring, canonical topics, navigation, alignment, redaction and link validation. Before you route source comments or docblocks, use its `SKILL.md` section `Ground this skill does not own` for the stack-specific owner.

| Question | Surface |
|---|---|
| Which Markdown file contains a phrase, heading, endpoint, event or identifier? | Markdown-scoped native search and read |
| Which document is canonical, what must change, or are the links valid? | /alaa-repo-docs |
| Does a documentation claim match source behavior? | Name the implementation, runtime or configuration fact, then select its owner in `references/10-routing-contract.md` |
| Is generated Markdown current? | The source template and generator |
| What do installed Laravel package docs say? | Boost documentation |
| What do other current package docs say? | An official version-aware source |

CodeGraph does not own Markdown. This pack enables no Markdown backend in Serena by default: add one only for a named recurring gap, with verified health and an explicit project decision. Add no provider for repository text search.
