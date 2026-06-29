# Source priority and freshness

## Research policy

Browser storage behavior changes by browser engine, browser version, operating system, privacy mode, storage pressure, and embedder. For any task that asks for current limits, version support, Safari/iOS behavior, experimental APIs, or “latest” behavior, refresh sources before implementation.

## Source hierarchy

Use this order:

1. W3C/WHATWG specs for API semantics and terminology.
2. MDN Web Docs for cross-browser API behavior, compatibility, quota/eviction guides, and security notes.
3. Browser-vendor docs for engine-specific policy:
   - Chrome Developers / Chromium docs.
   - WebKit blog / WebKit bugs for Safari/WebKit.
   - Firefox/MDN/Bugzilla for Gecko-specific behavior.
4. Can I Use / Browser Compatibility Data for support tables and usage share.
5. Official library docs for wrappers (`idb`, Dexie, localForage, RxDB) when the task uses those libraries.
6. Issue trackers and community reports for bug symptoms only. Treat them as signals, not final truth, unless reproduced.

## Freshness gates

Refresh official sources when any of these are true:

- User asks for browser versions, current quotas, Safari/iOS behavior, storage persistence, experimental APIs, or “latest”.
- Source data is older than 6 months for compatibility/quota claims.
- The feature involves large offline storage, persistent storage, private mode, embedded webview, third-party iframe, or mobile Safari.
- The code will be released to production across broad browsers.
- A browser-specific workaround is proposed.

## What to record after research

For each browser-sensitive decision, record:

- Research date.
- Sources checked.
- Browser/OS versions or channels.
- Whether the claim is official, compatibility-data-backed, or empirical.
- Fallback behavior if the claim is wrong.
- Tests required to confirm in the target environment.

## Never overfit to one source

Do not implement a rule just because one blog post says so. Convert any community-reported bug into a test or feature probe. If official docs and empirical behavior conflict, document the conflict, prefer feature detection, and add a runtime fallback.

## Skill-authoring compatibility

This pack follows agent-skill best practices:

- Keep `SKILL.md` routing-first and concise.
- Put heavy context into `references/`.
- Put deterministic reusable code in `scripts/` or `examples/`.
- Use explicit workflows, checklists, and output contracts.
- Prefer source-linked maintenance notes over model-memory claims.
