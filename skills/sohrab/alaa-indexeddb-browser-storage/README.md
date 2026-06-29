# alaa-indexeddb-browser-storage

A skill pack for agents that need to design, implement, review, and test IndexedDB/browser-storage features for Alaa-style web applications.

This pack is browser-storage-first and media-player-agnostic. It focuses on IndexedDB rules, quotas, compatibility, security, schema migration, offline sync, test strategy, and progressive enhancement.

## Install/use

Place the folder as a skill directory in the target agent environment, or upload the zip where custom skills are accepted.

Required file:

- `SKILL.md`

Optional supporting directories included:

- `references/` — detailed guidance loaded on demand.
- `assets/` — reusable templates, policies, and capability contracts.
- `examples/` — TypeScript and test patterns agents can adapt.
- `scripts/` — deterministic validation helpers for the skill pack itself.
- `agents/` — OpenAI-style routing metadata.

## What this skill teaches

- IndexedDB mental model and boundaries.
- Browser/version differences and capability tiers.
- Storage quota, persistence, eviction, private browsing, and Safari/WebKit-specific behavior.
- Schema migrations, multi-tab handling, and concurrency.
- Transaction discipline, performance, durability, indexes, cursors, and workers.
- Security/privacy rules: what may and must not be stored.
- Offline outbox, local cache, drafts, learning state, and conflict handling.
- Testing, browser debugging, and observability.
- Alaa integration patterns for content, auth, watch analytics, upload metadata, tickets, comments, and notifications.

## Research date

Last researched: 2026-06-29.

Browser storage rules change. For version-sensitive work, refresh official MDN, W3C, Chrome Developers, WebKit, and Can I Use sources before relying on numbers.
