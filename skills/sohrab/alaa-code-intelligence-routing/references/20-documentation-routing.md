# Documentation routing

This file routes evidence surfaces only. `/alaa-repo-docs` in Claude Code and `$alaa-repo-docs` in Codex owns repository Markdown authoring, canonical topic ownership, language, de-duplication, redaction, navigation, alignment, and deterministic link validation. `/alaa-frontend-doc-annotations` or `$alaa-frontend-doc-annotations` owns source comments and docblocks.

## Capability boundary

Do not assume CodeGraph covers Markdown. Confirm the current supported-language list before using it; when Markdown is unsupported or unindexed, use CodeGraph only for supported implementation claims described by documentation.

Repository Markdown is outside Serena in this pack. Use native scoped search, read, and patch tools for document content and structure, and use the repository documentation owner for governance and proof.

## Routes

| Question | Owner |
|---|---|
| Which Markdown file contains a phrase, identifier, endpoint, event, config key, or error string? | Native search restricted to Markdown |
| What headings or section boundaries exist in one known large document? | Native targeted read or heading-scoped search |
| Which document is canonical, what must change, or are links valid? | `/alaa-repo-docs` or `$alaa-repo-docs` |
| Does a documentation claim match implementation? | Documentation owner using the claim's code, config, contract, framework, generator, or runtime owner |
| Is generated Markdown current? | Source template and generator |
| What do current external vendor docs say? | Official version-aware source; Laravel Boost for installed Laravel packages |

## Repository documentation

Start repository-wide phrase, identifier, link, heading, and policy searches with native Markdown-scoped tools. Read or patch only the named document after search establishes its path. Route canonical ownership, de-duplication, navigation, alignment, and deterministic link checks to `/alaa-repo-docs` (`$alaa-repo-docs`). Route embedded YAML, JSON, shell, CI, or code examples to their native parser or domain owner.

Do not add a permanent documentation MCP merely to search repository Markdown. Consider a read-only retrieval service only for authoritative documents outside the repository or a measured corpus-scale gap that existing GitHub, Hindsight, service-catalog, and official-doc surfaces cannot close.
