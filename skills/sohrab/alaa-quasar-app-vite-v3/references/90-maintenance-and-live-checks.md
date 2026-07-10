# Maintenance and Live Checks

This version-sensitive skill loses authority without refreshes.

## Snapshot discipline

- Canonical snapshot: `20-v3-config-and-features.md`, dated 2026-07-10; refresh with `node scripts/check-upstream-versions.mjs`.
- The script reports `@quasar/app-vite` `latestStableByMajor.v2`/`.v3`; if `latest` becomes v4, reassess the whole posture, not just versions.
- Any upstream version/import/config/folder change: search the whole pack for the old string; update every occurrence and snapshot date, never only the snapshot.
- Do not snapshot component/directive/plugin API output. Keep `scripts/query-installed-quasar-api.mjs` version-neutral and delegate to the target project's CLI.

## Verify live before answering

- Any latest/current or post-snapshot claim.
- Any `quasar describe` arguments/output/project detection/package-bin assumption used by the query script.
- Browser claims in `30`, `40`, `45`: Baseline, iOS/Safari cadence, permission UI/expiry/auto-revocation, `<geolocation>`/permission elements.
- Still UNVERIFIED: Static Routing API outside Chromium; Declarative Web Push in Chromium; testing-extension v3 compatibility; exact default dotenv list; exact Safari grant-expiry windows; `<geolocation>` rollout percentage; camera/mic permission elements.

Use only quasar.dev, quasarframework/quasar GitHub releases, npm registry, MDN, web.dev, developer.chrome.com, webkit.org. Community posts are troubleshooting hints, never migration rules.

## Posture history

- 2026-07-06/07: app-vite `3.0.0` then `3.0.1`; v3 became stable after beta/RC from 2026-05-06. v2 `2.6.2` entered maintenance (approximately through 2027-06).
- 2026-07-08: absorbed retired `quasar-skill-packe` (Quasar shapes/atlases/modes/guardrails) and `alaa-app-vite-quasar` (v2 playbook/deltas/testing/CI). Posture edits must also sweep `$alaa-frontend-developer`.
- 2026-07-10: became a control plane, not exhaustive API mirror: exact APIs route to project-local `quasar describe`; atlases retain intent/alternatives/gotchas/search vocabulary; no MCP required.

## Query-helper verification

When changing `scripts/query-installed-quasar-api.mjs`, test one installed app-vite v2 and v3 project; match reported app-vite/Quasar versions to package metadata; test actionable missing/non-Quasar failure; run both a narrow symbol and `list` query (one output shape is insufficient).

## Dual-runtime contract

Follow `references/91-agent-authoring-and-dual-runtime.md`: frontmatter only `name` + `description`; high-value ✅ Do/❌ Don't pairs; one default + escape hatch; no cross-file contradictions; absolute dates; forward-slash paths; routing tables and search terms in every reference.
