# Routing-hook topology

This skill owns the interaction topology between evidence tools and the adoption and rollback checks for that topology. The user-level CodeGraph baseline remains the discovery governor. Keep Serena project activation and cleanup, but omit `serena-hooks remind` while CodeGraph routing is enabled because the reminder cannot recognize CodeGraph evidence as completed discovery.

Current official runtime documentation and the installed CodeGraph and Serena commands own exact hook events, schema, locations, matchers, trust behavior, lifecycle support, command shapes, and client compatibility. Verify both at adoption time; do not freeze executable JSON or TOML in this skill.

## Adoption

1. Verify the CodeGraph root and Serena active project resolve to the current Git worktree.
2. Inspect the installed CodeGraph and Serena command help and health output and the target runtime's current official hook schema before editing project-local configuration.
3. When the installed CodeGraph hook command declares compatible input for the target runtime and client, configure CodeGraph prompt injection; otherwise do not configure it. The currently observed `codegraph prompt-hook --help` identifies Claude `UserPromptSubmit` input; do not copy that hook to Codex unless the installed command declares Codex-compatible input.
4. Preserve existing Serena activation and cleanup behavior. Remove or omit only the project-local Serena reminder that competes with CodeGraph routing.
5. Parse or validate the project-local configuration against the current schema, then exercise each hook in a disposable or ordinary session while observing its exit and status behavior.
6. Exercise one CodeGraph discovery route, one Serena known-symbol route, and the named manual fallback.
7. Record only the project-local deltas. Keep the exact current JSON or TOML in the user handoff, not in this skill. Do not imply onboarding, memory writes, reindexing, initialization, dependency installation, or mutation authority.

If compatible CodeGraph prompt injection is unavailable or any routing hook fails, degrade to the named manual fallback: apply the global CodeGraph baseline for supported-source discovery, verify Serena activation before known-symbol work, and verify the worktree before native proof. Consume evidence already returned; fallback does not authorize duplicate discovery.

## Rollback

Remove only the project-local hook entries and files introduced by the adoption. Preserve user, managed, plugin, and unrelated project hooks. Re-parse or validate the effective configuration, inspect remaining command health, observe remaining hooks in a disposable or ordinary session, and verify that manual routing still works in the same worktree.

Passive instrumentation may observe routing, but it must not alter permissions, tool output, or the routing decision being measured.
