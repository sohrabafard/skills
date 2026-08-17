# Store Adapter: Hindsight

This adapter contains Hindsight mechanics only. `SKILL.md` and its policy references still decide what may be remembered, which source wins, and how failures or drift are handled.

## Current upstream surface

Verified 2026-08-15: stable Hindsight is `0.9.1`, and the official `@vectorize-io/hindsight-coding-agents` package is `0.3.4`. Re-check the official changelog, GitHub release, and npm registry before changing either exact pin; never infer a current version from this file alone.

Coding Agents owns Claude Code and Codex hooks, MCP wiring, its staged runtime and companion skill, config merging/backups, install/update/uninstall, bank resolution, retain/recall/reflect tools, session write-back, optional git seeding, and optional conversation import. Do not add a second hook, spool, transcript parser, MCP registration, or installer around it.

## Upstream skill routing

This adapter keeps policy authority: it decides whether memory work is admitted, which bank and scope are
legal, what must be verified against repository truth, and whether an external effect is authorized. After
that decision, invoke at most one vendored upstream skill for the product mechanics it owns:

- `/hindsight-docs` for current Hindsight architecture, API, SDK, deployment, configuration, debugging, or
  best-practice questions. Read only the references needed for the question; it does not decide what Alaa
  work may retain.
- `/hindsight-architect` when the user asks to design or review an application's Hindsight integration. It
  produces an implementation plan, not code; route accepted execution through `/alaa-workflow`, and verify
  its repository and security assumptions before implementation.
- `/hindsight-upgrade` only for an explicit installed-copy update request. Its network, setup, configuration,
  and replacement steps require the corresponding user authorization. It must never edit
  `vendor/hindsight-skills`; this repository updates that subtree through its vendor workflow.

Routine Alaa recall, retention admission, durable publication, and drift handling stay in `/alaa-memory-os`;
none of these upstream skills replaces them. If the named upstream skill is not installed, report that
mechanics are unavailable and continue only where this adapter's fail-open rule permits it.

## Installation and configuration

Install explicit targets and an explicit server mode:

```text
hindsight-coding-agents install claude-code codex --server self-hosted --api-url <url>
```

Use `cloud` or `daemon` only when current user/repository truth selects it. Non-interactive installation otherwise defaults to Cloud. The installer may change only its documented Hindsight-owned entries and backups.

The single trusted client configuration is `~/.hindsight/coding-agent.json`; there is no repository-carried config. Credentials belong only in this user-global file or persistent approved environment injection. Never pass a token on command argv: package managers and process surfaces may echo it. Never commit or print credentials.

## Scope and banks

With no override, both agents resolve the same harness-neutral bank `coding-agent::{gitProject}`. Worktrees resolve to their main repository by default. Use `mapPathToBank` for an explicit trusted path mapping and `banks.<resolved-id>.bank` when several resolved IDs must converge on one shared bank. Do not use per-harness bank names unless deliberate isolation is required.

`optInOnly: true` is the fail-closed admission switch. `optInPaths` and `mapPathToBank` are trusted prefix approvals; approving a parent approves repositories beneath it. Keep paths unapproved when real-data ingestion is not authorized.

`retainTags` and `retainMetadata` may add fixed-shape provenance to official session writes. They do not replace the bank boundary, and remembered service dependency edges remain prohibited because they are derived from live code/contracts.

## Recall and write mechanics

Use the official MCP tools exposed by the selected harness. Start with bounded recall/reflect for the current repository bank, verify important claims against repository truth, and expand only the specific memory needed. Recall failure fails open after the skill's budget; continue from current source and disclose the missing memory evidence.

Use official retain or document-ingest tools only after the policy admission test passes. A write is successful only when Hindsight reports terminal completion. If the intended write cannot complete, report the unwritten durable note in the handoff; never claim it was stored.

Official hook harnesses retain the completed session on `Stop` and ignore `retainSessions`. `autoSeed`, `gitIngest`, `codebaseSurvey`, and `autoReflect` are separate automatic behaviors. While ingestion is unapproved, keep `optInOnly: true` with no real paths, `gitIngest: "none"`, `autoSeed: false`, `codebaseSurvey: false`, and `autoReflect: false`.

## Import and migration

Historical import is optional. Use the upstream `--import-conversations` path only after explicit authorization and a current need; it is not a rollout prerequisite. Do not preserve or recreate a custom importer. Keep any previous store as a read-only archive until authorized migration evidence is complete.

## Self-hosted security

For self-hosted mode, require API authentication before any non-loopback bind. Keep the tracked default on loopback; use only a specific trusted-LAN address when explicitly selected, never `0.0.0.0`. Keep raw LLM traces disabled for normal operation. Tokens, transcripts, real sessions, and production/personal data are never test fixtures.

## Workflow boundary

Coding Agents session memory does not replace `alaa-workflow` plans, checkpoints, phase state, acceptance evidence, or handoffs. Store a concise durable lesson or pointer after the workflow proves it; never copy the active checklist into Hindsight.
