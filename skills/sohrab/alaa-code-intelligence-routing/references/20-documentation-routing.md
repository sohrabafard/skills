# Documentation and document-heavy routing

This file routes evidence surfaces only. `/alaa-repo-docs` in Claude Code and `$alaa-repo-docs` in Codex owns repository Markdown authoring, canonical topic ownership, language, de-duplication, redaction, navigation, alignment, and deterministic link validation. `/alaa-frontend-doc-annotations` or `$alaa-frontend-doc-annotations` owns source comments and docblocks.

## Capability boundary

Do not assume CodeGraph covers Markdown. Confirm the current supported-language list before using it; when Markdown is unsupported or unindexed, use CodeGraph only for supported implementation claims described by documentation.

When `markdown` is enabled under `languages:` in Serena project configuration, Serena can expose headings and other supported language-server structure. Treat it as optional navigation for one known document, not as repository-wide search, link proof, canonical-document selection, policy interpretation, or documentation governance.

## Routes

| Question | Owner |
|---|---|
| Which Markdown file contains a phrase, identifier, endpoint, event, config key, or error string? | Native search restricted to Markdown |
| What headings or section boundaries exist in one known large document? | Serena Markdown when healthy; otherwise targeted native read |
| Which document is canonical, what must change, or are links valid? | `/alaa-repo-docs` or `$alaa-repo-docs` |
| Does a documentation claim match implementation? | Documentation owner using the claim's code, config, contract, framework, generator, or runtime owner |
| Is generated Markdown current? | Source template and generator |
| What do current external vendor docs say? | Official version-aware source; Laravel Boost for installed Laravel packages |

## Document-heavy repositories

Start repository-wide phrase, identifier, link, and policy searches with native Markdown-scoped tools. After a document is named, Serena may navigate headings or make a bounded structural edit when its Markdown backend is healthy. Route canonical ownership, de-duplication, navigation, alignment, and deterministic link checks to `/alaa-repo-docs` (`$alaa-repo-docs`). Route embedded YAML, JSON, shell, CI, or code examples to their native parser or domain owner; enabling Markdown or YAML in Serena does not transfer those semantics to Serena.

Use the document-heavy Serena profile and short binding in `references/70-project-bindings.md`. Do not enable a language merely because files with that extension exist; enable it only when the language is material to the task and its prerequisites are installed.

Do not add a permanent documentation MCP merely to search repository Markdown. Consider a read-only retrieval service only for authoritative documents outside the repository or a measured corpus-scale gap that existing GitHub, Hindsight, service-catalog, and official-doc surfaces cannot close.
