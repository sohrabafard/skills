# Official source map

Checked on 2026-08-01. Recheck official sources and the installed commands before changing a capability, configuration key, hook, path, or command. Adoption-time runtime and vendor truth wins when these sources drift.

- CodeGraph README for supported languages, MCP use, index health, and stale or pending-file signals: https://github.com/colbymchenry/codegraph#readme
- Serena language support: https://oraios.github.io/serena/01-about/020_programming-languages.html
- Serena client bindings and activation behavior: https://oraios.github.io/serena/02-usage/030_clients.html
- Serena project workflow and activation versus onboarding: https://oraios.github.io/serena/02-usage/040_workflow.html
- Serena current configuration surface: https://oraios.github.io/serena/02-usage/050_configuration.html
- Laravel Boost documentation, MCP tools, documentation API, and application-context tools: https://laravel.com/docs/boost
- Claude Code hook lifecycle, schema, paths, matchers, and trust: https://code.claude.com/docs/en/hooks
- Codex hook lifecycle, JSON/TOML schema, paths, trust, and command behavior: https://learn.chatgpt.com/docs/hooks
- Repository Markdown ownership and checker: installed `/alaa-repo-docs` (`$alaa-repo-docs`)

Do not copy volatile version numbers or complete hook payloads from these pages into this skill. If installed behavior conflicts with a source, record `NEEDS_CONFIRMATION`, keep the project-local manual fallback, and stop adoption before mutation.
