# Documentation evidence routing

This file routes evidence surfaces only. `/alaa-repo-docs` in Claude Code and `$alaa-repo-docs` in Codex owns repository Markdown authoring, canonical topic ownership, language, de-duplication, redaction, navigation, alignment, and deterministic link validation. `/alaa-frontend-doc-annotations` or `$alaa-frontend-doc-annotations` owns source comments and docblocks.

## Capability boundary

CodeGraph does not currently index Markdown as a supported language. Use it only to verify implementation claims described by documentation.

When `markdown` is enabled in `.serena/project.yml`, Serena can expose Markdown headings through the language server. Treat this as optional navigation for one known document, not as full-text search, link proof, canonical-document selection, or documentation governance.

## Routes

| Question | Owner |
|---|---|
| Which Markdown file contains a phrase, identifier, endpoint, event, config key, or error string? | Native search restricted to Markdown |
| What headings or section boundaries exist in one known large document? | Serena Markdown when healthy; otherwise targeted native read |
| Which document is canonical, what must change, or are links valid? | `/alaa-repo-docs` or `$alaa-repo-docs` |
| Does a documentation claim match implementation? | Documentation owner using the claim's code, config, contract, framework, generator, or runtime owner |
| Is generated Markdown current? | Source template and generator |
| What do current external vendor docs say? | Official version-aware source; Laravel Boost for installed Laravel packages |

Do not add a permanent documentation MCP merely to search repository Markdown. Consider a read-only retrieval service only for authoritative documents outside the repository or a measured corpus-scale gap that existing GitHub, Hindsight, service-catalog, and official-doc surfaces cannot close.
