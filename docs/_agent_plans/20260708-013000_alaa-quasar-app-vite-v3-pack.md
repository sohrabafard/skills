# Alaa Quasar app-vite v3 skill pack: new skill + frontend-skill gap closure

## Summary

Build a new skill `skills/sohrab/alaa-quasar-app-vite-v3` that makes agents produce the best, safest, most modern Quasar apps on `@quasar/app-vite` v3 (stable `3.0.1` since 2026-07-07), including the v2 -> v3 migration playbook entry point, full-featured service workers/offline, WebOTP (SMS OTP reading), device fingerprinting/device trust, and latest Quasar features — with token-efficient progressive disclosure. Then upgrade `alaa-frontend-developer` with modern CSS3 + classy animation guidance, and close gaps/stale content in five sibling skills. Strategy: parallel research lanes (live web + local gap analysis) feed a single authoring pass; every stale "v3 is RC" posture statement gets flipped to the new stable-v3 reality.

## Repository-grounded facts

- Verified live (scripts/check-upstream-versions.mjs, 2026-07-07T21:57Z): `@quasar/app-vite` `latest = 3.0.1` (stable, published 2026-07-07); v2 stable line `2.6.2`; quasar `2.21.1`; vite `8.1.3`; vue `3.5.39`; vue-router `5.1.0`; pinia `3.0.4`; workbox-build `7.4.1`.
- Existing trio ownership (per memory + SKILL.md files): `quasar-skill-packe` = exact Quasar shapes (routing-first, 18 references); `alaa-app-vite-quasar` = v2-production + v3-readiness posture (5 references); `alaa-frontend-developer` = broad app-family frontend policy (12 references).
- All three currently assert "v3 is RC, keep production on v2" — now stale.
- Skill-pack conventions: frontmatter `name`+`description` only; `agents/openai.yaml`; `references/00-topic-map.md`; Do/Don't contrast pairs; dual-runtime (Opus + Codex) wording; version-check scripts; `references/90-*` maintenance file.
- User goal: build best-in-class SPA/SSR/PWA/native apps on v3 and migrate their own app-vite v2 app to v3.

## Phases

### Phase 1 — Research (parallel lanes, running)
- Lane A: Quasar app-vite v3 migration + new features (web, primary sources).
- Lane B: Service worker / offline / update-flow best practices 2026 (web).
- Lane C: WebOTP + device fingerprinting/device trust (web).
- Lane D: Modern CSS3 + motion design (web).
- Lane E: Local gap analysis of all six skills incl. exhaustive stale-RC-posture list (read-only).
- Acceptance: all five lanes return structured reports; unverifiable claims marked.

### Phase 2 — Author `alaa-quasar-app-vite-v3` (new skill)
- Files: `SKILL.md` (lean, routing-first), `agents/openai.yaml`, `references/00-topic-map.md`, migration reference, v3 config/features reference, service-worker excellence reference, WebOTP+fingerprint/device-trust reference, modern-experience reference (latest Quasar features / app modes), `scripts/check-upstream-versions.mjs` (v3-aware), maintenance/90 reference.
- Route (not duplicate) to: quasar-skill-packe (exact shapes), alaa-app-vite-quasar (v2 legacy detail), alaa-indexeddb-browser-storage, alaa-frontend-developer, alaa-vue-typescript-clean-code, alaa-mono-package.
- Acceptance: token-efficient progressive disclosure; Do/Don't pairs; dual-runtime; stable-v3-first posture; description triggers reliably.

### Phase 3 — Upgrade `alaa-frontend-developer`
- Add a modern CSS + motion reference (View Transitions, scroll-driven animations, container queries, :has, @starting-style, popover/dialog, anchor positioning, oklch/light-dark, motion taste rules, reduced-motion, compositor-only perf) and wire it into SKILL.md routing/search rules.
- Refresh stale version/RC posture lines; add routing to the new v3 skill.
- Acceptance: new reference exists, routing updated, no stale RC claims remain.

### Phase 4 — Gap closure across siblings
- `quasar-skill-packe`: flip stable-first policy section to v3-stable reality; refresh snapshot; route v3 deep work to new skill.
- `alaa-app-vite-quasar`: reposition as v2-maintenance + migration-source skill now that v3 is stable; refresh versions; route to new skill.
- `alaa-vue-typescript-clean-code`: add gaps found by Lane E (e.g. modern CSS/TS notes) minimally; refresh stale claims.
- `alaa-indexeddb-browser-storage`: add SW-coordination/device-trust hooks if Lane E finds gaps; refresh stale claims.
- `alaa-mono-package`: close Lane-E gaps (likely small).
- Acceptance: every stale-posture line from Lane E's list is fixed or consciously kept with reason.

### Phase 5 — Validate + reconcile
- Run repo skill validators if present; check markdown links; confirm frontmatter shape; grep for leftover "rc" posture; update state artifacts; final report with commit message.

## Risks
- v3.0.1 is 1 day old: real-world migration gotchas are thin; mark community-unverified areas explicitly; keep v2 line documented for repos that cannot move yet.
- WebOTP is Chromium/Android-only; skill must teach the fallback chain, not pretend universality.
- Fingerprinting has privacy/legal constraints; skill must bound it to device-trust signal usage, never sole auth.

## Companion skills used
`$alaa-workflow`, `$alaa-low-noise`, `$anthropic-skills:skill-creator` (conventions), domain source skills listed above.
