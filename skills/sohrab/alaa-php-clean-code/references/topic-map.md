# Topic Map — Shortest Reading Path

Match the task to the smallest set of files. When two rows match, read both; for a whole feature or a
whole-package review, follow the SKILL.md operating model order instead of assembling pieces.

| Task looks like | Read |
|---|---|
| New endpoint, controller, or route | `laravel-best-practices.md` + `design-patterns.md` (Service, Repository) |
| New or changed service / business rule | `design-patterns.md` (Service, DTO, Value object) + `solid-in-practice.md` |
| Persistence, query, or migration work | `design-patterns.md` (Repository, Query object) + `laravel-best-practices.md` |
| Adding caching to domain data | `design-patterns.md` (Decorator) — cache-decorator policy in SKILL.md is mandatory |
| Provider or vendor integration (SMS, payment, storage, external API) | `design-patterns.md` (Adapter, Strategy, Abstract factory, Exception translation) |
| Queued, retried, delayed, or audited action | `design-patterns.md` (Command) + `octane-clean-code.md` |
| Status or lifecycle modeling | `design-patterns.md` (State) |
| Refactor or cleanup of existing code | `refactor-modes.md` + `code-smells-and-refactoring-triggers.md` |
| Renaming, extracting, consolidating, normalizing shape | `consistency-and-naming.md` |
| Choosing, confirming, or reviewing a design pattern | `design-patterns.md` — run the symptom → pattern diagnostic at its top first |
| SOLID review or principle question | `solid-in-practice.md` |
| Octane worker, long-lived state, state-leak review | `octane-clean-code.md` |
| Modern PHP syntax, types, PSR/PER | `php-modern-and-psr.md` |
| Docs, Postman, or artifacts after behavior change | `documentation-and-artifacts.md` |
| Latest/current/version/security claims | `source-map.md` |
| Subagents or parallel work (only when explicitly requested) | `agent-orchestration.md` |
| At the start of every non-trivial task | `companion-skill-routing.md` |

Rule of thumb: the most expensive mistakes this skill prevents are persistence composed outside a
repository and cache calls outside a decorator — when the task touches persistence or caching in any way,
the Repository and Decorator sections are never optional reading.
