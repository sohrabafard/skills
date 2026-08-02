# Documentation routing

This file routes evidence surfaces only. `/alaa-repo-docs` in Claude Code and `$alaa-repo-docs` in Codex owns repository Markdown authoring, canonical topic ownership, language, de-duplication, navigation, alignment, redaction, and deterministic link validation. `/alaa-frontend-doc-annotations` or `$alaa-frontend-doc-annotations` owns source comments and docblocks.

## Boundary

CodeGraph is not the repository Markdown owner. Use it only for supported implementation evidence needed to verify a documentation claim.

This pack does not enable Markdown in Serena by default. Repository text and heading navigation use native Markdown-scoped search and targeted reads. A project may add a Markdown semantic backend only after a named recurring gap, health verification, and explicit project decision; doing so does not transfer documentation ownership from `/alaa-repo-docs` or `$alaa-repo-docs`.

## Routes

| Question | Owner |
|---|---|
| Which Markdown file contains a phrase, endpoint, event, config key, or identifier? | Native search restricted to Markdown |
| What headings or section boundaries exist in one known document? | Native targeted read or heading-scoped search |
| Which document is canonical, what must change, or are links valid? | `/alaa-repo-docs` or `$alaa-repo-docs` |
| Does a documentation claim match source behavior? | Documentation owner using CodeGraph, the semantic owner, config or contract owner, Boost, generator, or runtime evidence for that one claim |
| Is generated Markdown current? | Source template and generator |
| What do current Laravel package docs say? | Laravel Boost Search Docs |
| What do other current vendor docs say? | Official version-aware source |

Do not add a permanent documentation MCP merely to search repository Markdown. Consider a read-only retrieval service only for authoritative content outside the repository or a measured corpus-scale gap that existing repository, catalog, memory, and official-doc surfaces cannot close.
