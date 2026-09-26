# Store Adapter: Hindsight

This adapter contains Hindsight mechanics only. `SKILL.md` and its policy references still decide what may be remembered, which source wins, and how failures or drift are handled.

## Current upstream surface

Verified 2026-09-26: the official `@vectorize-io/hindsight-coding-agents` package is `0.7.0`, and core Hindsight server is `0.10.1`. Re-check the official changelog, GitHub release, and npm registry before changing either exact pin; never infer a current version from this file alone.

Coding Agents owns Claude Code and Codex hooks, MCP wiring, its staged runtime and companion skill, config merging/backups, install/update/uninstall, bank resolution, retain/recall/reflect tools, session write-back, optional git seeding, and optional conversation import. Its own `install`/`update`/`uninstall` commands are user-scope only: they write `~/.claude/settings.json`, register the MCP server with `claude mcp add --scope user`, and read config only from `HINDSIGHT_CONFIG` or `~/.hindsight/coding-agent.json` — there is no project-scope install path, no project config search, and no dotenv reader. Alaa service repositories never run those commands; each adopts Hindsight through the project-scoped launcher and hook wiring in "Installation and configuration" below, which calls the same official dist script directly. Do not add a second hook, spool, transcript parser, or MCP registration around it.

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

Hindsight is set up per project, never globally. Use the official installer's user-scope path and its
`~/.hindsight/coding-agent.json` default only for a genuinely personal, cross-project setup outside any Alaa
service repository; every Alaa service repository uses the project-scoped pattern below instead, built from
official pieces where they exist and custom code only for the gaps the installer leaves.

Project-scoped pattern (identical launcher and doctor script across repositories):

- An exact devDependency pin on `@vectorize-io/hindsight-coding-agents` in the repository's `package.json`.
- `.hindsight/coding-agent.json` as the repository-committed policy file (bank, scope, opt-in paths, retain
  tags); it carries no token.
- `.hindsight/hook.cjs`, a launcher that only sets `HINDSIGHT_CONFIG` to the repository's policy file, lifts
  `HINDSIGHT_API_TOKEN` and `HINDSIGHT_API_URL` from the gitignored `.env`, and execs the official dist script.
  The launcher always passes `--preserve-symlinks-main`; it is required under pnpm — measured on `0.7.0`,
  without it the MCP server never answers `initialize` — and a no-op under a flat npm install. It adds no
  memory behavior of its own.
- Repository `.claude/settings.json` and `.codex/hooks.json` entries that call the launcher for the same
  official events and timeouts the upstream installer would wire: `SessionStart` (30s), `UserPromptSubmit`
  (30s), `Stop` (60s).
- MCP registration in `.mcp.json` and `.codex/config.toml`, through the same launcher, with
  `HINDSIGHT_MCP_HARNESS` set to `claude-code` or `codex`. This variable is required since `0.7.0`: without
  it the MCP server exits while the hooks keep running, so the failure is silent unless the doctor check below
  is run.
- `.hindsight/doctor.cjs`, exposed as the `hindsight:doctor` npm script, is the health gate. Upstream ships no
  doctor, only `stats`; treat a passing `hindsight:doctor` as the adoption proof this adapter requires. It also
  checks (g) this repo's `customPages` all exist as knowledge pages on the server, and (h) whether the shared
  bank's deepen lock (see below) is currently held — both WARN, never FAIL, since neither blocks normal use.
- `.hindsight/deepen.cjs`, exposed as the `hindsight:deepen` npm script, waits out a held deepen lock (polling,
  default 20 minutes) and then runs the official `deepen.js` engine for this repository. Use it to force-seed a
  repository's knowledge pages and git history on a shared bank instead of waiting on the next `SessionStart`.

Credentials belong only in the repository's gitignored `.env`, read by the launcher, or in persistent approved
environment injection. Never pass a token on command argv: package managers and process surfaces may echo it.
Never commit or print credentials, and never put a token in `.hindsight/coding-agent.json`.

Config layering in `0.7.0`: the environment layer applies first, then the file layer, and the file wins for
any key it sets. `bankId` set in the file is honored with `dynamicBankId: false`. `autoReflect` is deprecated
in favor of `autoInject` (`reflect` | `pages` | `recall` | `none`; unset defaults to `reflect`).
`retainSessions` is the Stop-hook retention kill switch (default `true`, from `raw.retainSessions ?? true`):
`claude-stop-hook.js` and `codex-stop-hook.js` both return early with diagnostic `retain_disabled` when it is
`false`, so setting it `false` suppresses session retention on `Stop` entirely. `customPages` with `tags` give
a service its own knowledge pages on a shared bank — tags match `"all"`, and seeding never deletes another
service's pages. Auto-injection runs once per session, and the page roster repeats every
`pageRefreshEveryTurns` turns.

## Scope and banks

Alaa's decision is one shared, fixed bank across services rather than the installer's per-repository default:
set `bankId` explicitly in each service's `.hindsight/coding-agent.json` (with `dynamicBankId: false`) to the
same shared bank id, and distinguish services on that bank through `retainTags` and `retainMetadata`
provenance, not through separate banks. Do not use per-harness or per-repository bank names for services that
share this decision.

`optInOnly: true` is the fail-closed admission switch, kept per this adapter's default. `optInPaths` holds only
the current repository's own path; approving a parent approves repositories beneath it, so do not approve
above the current repository. Keep a repository's path unapproved when real-data ingestion is not authorized
for it.

`retainTags` and `retainMetadata` add fixed-shape service provenance to official session writes on the shared
bank; they do not replace the opt-in boundary, and remembered service dependency edges remain prohibited
because they are derived from live code/contracts. Every repository's `retainTags` carries its catalog tag
(`service:<name>` or `area:<name>`, as the hindsight project's `service-catalog.json` assigns it) plus the
official template `project:{gitProject}`, which resolves to the main worktree's directory name. A page about one
repository is tagged with that repository's unique tag — `service:<name>` where the catalog gives the repository
its own service, otherwise `project:<repo>` — so it is built only from that repository's memories; an area page
(for example octane-base's `shared libraries: …`) is tagged with the area tag and asks area-wide questions. Name
each page distinctively, because page search is bank-wide (BM25 plus vector, no tag filter) and near-identical
names such as `comment:` and `content:` are confused.

A shared bank has one consequence the per-repository default does not: `deepen.js` (the engine that seeds
knowledge pages, including `customPages`, and git history) takes a single lock file keyed by bank id, stale
after 30 minutes, and a second run for the same bank exits immediately with no retry — so when the
`SessionStart` hook fires for two repositories on the same bank close together, only the first repo's session
actually seeds; the other's pages and git ingest are silently skipped. `hindsight:deepen` (above) is the
recovery: it waits out a lock that is fresh and whose holder process is alive (the same rule as `deepen.js`),
then runs `deepen.js` for that repository, and retries if it loses the race for the lock in between. `hindsight:doctor`'s checks (g)
and (h) surface the two symptoms (missing pages, a held lock) as WARNs pointing at `hindsight:deepen`.

## Recall and write mechanics

Use the official MCP tools exposed by the selected harness. Start with bounded recall/reflect for the current repository bank, verify important claims against repository truth, and expand only the specific memory needed. Recall failure fails open after the skill's budget; continue from current source and disclose the missing memory evidence.

Use official retain or document-ingest tools only after the policy admission test passes. A write is successful only when Hindsight reports terminal completion. If the intended write cannot complete, report the unwritten durable note in the handoff; never claim it was stored.

Official hook harnesses retain the completed session on `Stop` unless `retainSessions: false` disables it (see
Config layering above). `autoSeed`, `gitIngest`, `codebaseSurvey`, and `autoInject` (the successor to the
deprecated `autoReflect`) are separate automatic behaviors. While ingestion is unapproved, keep `optInOnly:
true` with no real paths, `gitIngest: "none"`, `autoSeed: false`, `codebaseSurvey: false`, `autoInject:
"none"`, and `retainSessions: false`.

## Import and migration

Historical import is optional. Use the upstream `--import-conversations` path only after explicit authorization and a current need; it is not a rollout prerequisite. Do not preserve or recreate a custom importer. Keep any previous store as a read-only archive until authorized migration evidence is complete.

## Self-hosted security

For self-hosted mode, require API authentication before any non-loopback bind. Keep the tracked default on loopback; use only a specific trusted-LAN address when explicitly selected, never `0.0.0.0`. Keep raw LLM traces disabled for normal operation. Tokens, transcripts, real sessions, and production/personal data are never test fixtures.

## Workflow boundary

Coding Agents session memory does not replace `alaa-workflow` plans, checkpoints, phase state, acceptance evidence, or handoffs. Store a concise durable lesson or pointer after the workflow proves it; never copy the active checklist into Hindsight.
