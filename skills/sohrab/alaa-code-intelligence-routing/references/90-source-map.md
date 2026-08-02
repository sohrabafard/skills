# Official source map

Sources were reviewed on 2026-08-02. Recheck the official documentation and installed command help before changing a capability, command, configuration key, hook, or path. Installed schema and repository truth win when published docs lag.

- CodeGraph repository, installer, MCP guidance, index behavior, supported languages, and benchmark links: https://github.com/colbymchenry/codegraph
- Serena installation and usage documentation: https://oraios.github.io/serena/
- Serena client contexts and project activation: https://oraios.github.io/serena/02-usage/030_clients.html
- Serena project workflow: https://oraios.github.io/serena/02-usage/040_workflow.html
- Serena configuration: https://oraios.github.io/serena/02-usage/050_configuration.html
- Serena language support and evaluation: https://oraios.github.io/serena/01-about/020_programming-languages.html
- Laravel Boost documentation, custom guidelines, update command, MCP tools, documentation search, and application context: https://laravel.com/docs/boost
- Laravel Boost upstream issue tracker for current tool-safety reports: https://github.com/laravel/boost/issues
- Claude Code hooks: https://code.claude.com/docs/en/hooks
- Codex hooks: https://learn.chatgpt.com/docs/hooks

Do not freeze external version pins, complete vendor hook payloads, or generated project schemas in this skill. When installed behavior and official sources disagree, record `NEEDS_CONFIRMATION`, preserve the manual fallback, and stop configuration mutation until the discrepancy is resolved.
