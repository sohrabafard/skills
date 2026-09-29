For the v5.2.3 API/migration baseline and 2026-07-28 read date, consult [provenance and freshness](../05-provenance-and-freshness.md); source context stays canonical there.

## Upgrade procedure

1. Read `05-provenance-and-freshness.md` and confirm the current release.
2. Run `scripts/check-shaka-api.mjs --repo <path>` — it reports every call site using an API removed
   or deprecated between the installed version and current.
3. Fix each finding against the section above. **An optional-chained call to a removed method is still
   a finding** — it converts a loud failure into a silent one.
4. Change the pin to an exact version and record the release URL and date in
   `05-provenance-and-freshness.md`.
5. Re-run the QA matrix in `90-qa-modes-and-checklist.md`, with iOS Safari as its own row.

**Best practice.** Pin an exact version. Three vendor endpoints disagreed about "latest" on
2026-07-28 (conflict C1), so `npm i shaka-player@latest` may not give you what the release page shows.
**Common mistake.** Treating `5.0.x → 5.1.x` as a breaking migration and writing shims for it. There
is nothing to shim; the cliffs are v4 → v5 and the announced v5 → v6.
