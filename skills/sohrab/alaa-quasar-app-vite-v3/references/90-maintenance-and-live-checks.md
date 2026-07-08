# Maintenance and live checks

This skill is version-sensitive by design. Its authority decays without refreshes.

## Snapshot discipline

- Canonical snapshot lives in `20-v3-config-and-features.md` (dated 2026-07-08). Refresh with:

```bash
node scripts/check-upstream-versions.mjs
```

- The script reports `latestStableByMajor.v2` and `.v3` for `@quasar/app-vite`. If a v4 line ever appears on `latest`, this whole skill's posture needs re-evaluation, not just a number bump.
- When any version, import path, config key, or folder changes upstream: grep the whole pack for the old string and update every occurrence plus the snapshot date. Never update the snapshot alone.

## Freshness triggers (verify live before answering)

- Any "latest"/"current" question; any claim after the snapshot date.
- Browser-support claims in `30`, `40`, and `45` (Baseline moves; iOS/Safari release cadence; permission prompt behavior changes almost yearly — one-time grants, quieter UI, auto-revocation windows, the `<geolocation>`/permission-element rollout). Items marked UNVERIFIED in research: Static Routing API outside Chromium, Declarative Web Push in Chromium, testing-extension v3 compatibility, exact default dotenv file list, exact Safari grant-expiry windows, `<geolocation>` element rollout percentage, camera/mic permission elements.
- Official sources only: quasar.dev, GitHub releases (quasarframework/quasar), npm registry, MDN, web.dev, developer.chrome.com, webkit.org. Community posts are troubleshooting hints, never migration rules.

## Posture history (so future edits keep context)

- 2026-07-06/07: `@quasar/app-vite` 3.0.0 then 3.0.1 released — v3 became the stable production line after a beta/RC run since 2026-05-06. v2 (last stable 2.6.2) entered maintenance (~until 2027-06 per upstream signals).
- 2026-07-08: this skill absorbed the full content of the former `quasar-skill-packe` (exact Quasar shapes, atlases, platform modes, guardrails) and `alaa-app-vite-quasar` (v2 playbook, verified delta checklist, testing/CI) — those two skills were retired. If you edit posture here, also sweep `$alaa-frontend-developer` (it cross-references this skill).

## Dual-runtime authoring rules

Match `references/91-agent-authoring-and-dual-runtime.md`: frontmatter `name` + `description` only; ✅ Do / ❌ Don't pairs on high-value rules; one default plus escape hatch; no contradictions between files; absolute dates, never "recently"; forward-slash paths; routing tables and search terms in every reference.
