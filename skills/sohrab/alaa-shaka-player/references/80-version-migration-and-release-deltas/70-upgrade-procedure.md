For the v5.2.3 API/migration baseline and 2026-07-28 read date, consult [provenance and freshness](../05-provenance-and-freshness.md); source context stays canonical there.

## Upgrade procedure

1. Read `05-provenance-and-freshness.md` and confirm the current release.
2. Run `scripts/check-shaka-api.mjs --repo <path> --target <new version>`. It reports call sites that use APIs
   removed or deprecated up to v5.2.3, plus the error names retired and the keys deprecated in v5.3. It does not
   report changed defaults: read [v5.3.0 features](./45-v530-features.md) and search the repository for
   `useNativeHlsForFairPlay`, `fallbackToNativeHlsOnMseError` and `com.apple.fps`.
3. Fix each finding against `20-v4-to-v5-breaking-changes.md`, `30-deprecations-and-v6.md` and `45-v530-features.md`. **An optional-chained call to a removed method is still
   a finding** — it converts a loud failure into a silent one.
4. Change the pin to an exact version and record the release URL and date in
   `05-provenance-and-freshness.md`.
5. When the target is 5.3.x, compare the UI bundle size with the consumer size budget. The measured growth is in
   `12-bundling-and-vite-loading.md`, "Bundle size and CSP, 5.2.13 to 5.3.4".
6. Run every consumer-proof scenario in [v5.2.x patches](./50-v52x-patches.md) and
   [v5.3.x patches](./55-v53x-patches.md#consumer-proof-for-the-shared-fixes) whose fix the target pin contains and
   the installed pin lacks.
7. Re-run the QA matrix in `90-qa-modes-and-checklist.md`, with iOS Safari as its own row.

**Best practice.** Pin an exact version. Three vendor endpoints disagreed about "latest" on
2026-07-28 (conflict C1), so `npm i shaka-player@latest` may not give you what the release page shows.
**Common mistake.** Treating `5.0.x → 5.1.x` as a breaking migration and writing shims for it. There
is nothing to shim; the cliffs are v4 → v5 and the announced v5 → v6.
