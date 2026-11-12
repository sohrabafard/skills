# Version migration and release deltas

Historical API/migration baseline: `.../blob/v5.2.3/CHANGELOG.md` and
`.../blob/v5.2.3/docs/tutorials/upgrade.md`, both `verified`, read 2026-07-28.
Latest observed: **5.3.4** 2026-11-06, read 2026-11-12 (tag page
`https://github.com/shaka-project/shaka-player/releases/tag/v5.3.4`).
Release dates: **5.3.4** 2026-11-06 · **5.2.17** 2026-11-06 · **5.3.3** 2026-10-29 · **5.2.16** 2026-10-29 ·
**5.3.2** 2026-10-23 · **5.2.15** 2026-10-23 · **5.3.1** 2026-10-19 · **5.3.0** 2026-10-16 ·
**5.2.14** 2026-10-16 · **5.2.13** 2026-10-09 (CHANGELOG at tags `v5.3.4` and `v5.2.17`, read 2026-11-12) ·
**5.2.3** 2026-07-27 · **5.2.2** 2026-07-20 · **5.2.1** 2026-07-14 ·
**5.2.0** 2026-07-10 · **5.1.0** 2026-04-15 · **5.0.0** 2026-02-06.

## Which migrations are real

When deciding whether a version transition needs migration, read [Migration boundaries](./80-version-migration-and-release-deltas/10-migration-boundaries.md) for the verified major/minor distinctions.

## v4 → v5: the breaking changes most likely to bite

When moving from v4 to v5, read [v4-to-v5 breaking changes](./80-version-migration-and-release-deltas/20-v4-to-v5-breaking-changes.md) for config, UI, API, plugin, ad, and format deltas.

## Deprecated right now in 5.x, and v6.0 spellings

When preparing code for v6, or when a 5.x deprecation warning appears, read [Deprecations and v6 spellings](./80-version-migration-and-release-deltas/30-deprecations-and-v6.md) for current warnings, TypeScript limits, the v6.0 spelling to write now, and replacements.

## 5.2.0 — what is new

When reviewing changes introduced in v5.2.0, read [v5.2.0 features](./80-version-migration-and-release-deltas/40-v520-features.md) for the retained release details.

## 5.2.x patch releases

Before upgrading across v5.2 patch releases, read [v5.2.x patches](./80-version-migration-and-release-deltas/50-v52x-patches.md) for observed fixes (5.2.13 to 5.2.17 included) and required consumer proof.

## 5.3.0 — what is new

When moving a 5.2.x pin to 5.3, or reading a 5.3.0 CHANGELOG line, read [v5.3.0 features](./80-version-migration-and-release-deltas/45-v530-features.md) for changed defaults, new keys, new Player methods and events, removals and the 5.2.13 comparison base.

## 5.3.x patch releases

Before upgrading across 5.3.1 to 5.3.4, or when a fix ships in both lines, read [v5.3.x patches](./80-version-migration-and-release-deltas/55-v53x-patches.md) for the fixes, the consumer-proof scenarios and the 5.3.4 text-path evidence.

## 5.1.0 — what changed

When reviewing a v5.1.0 transition, read [v5.1.0 changes](./80-version-migration-and-release-deltas/60-v510-changes.md) for the recorded additions, removals, and deprecations.

## Upgrade procedure

When upgrading a consumer, follow the [Upgrade procedure](./80-version-migration-and-release-deltas/70-upgrade-procedure.md) for API scan, pin, and QA sequence.
