# Migration plan

## Phase 0: Verify the baseline
- confirm the currently pinned or intended Shaka version
- check `references/UPSTREAM_WATCHLIST.md`
- for `5.0.8` to `5.1.11`, read `references/MIGRATION_5_0_8_TO_5_1_11.md`
- note any upstream bug or PR that changes the migration risk

## Phase 1: Create a safe test surface
- build `PlayerLabPage.vue`
- verify one HLS stream
- verify destroy and route changes

## Phase 2: Build the core wrapper
- implement `useShakaCore.ts`
- implement `ShakaPlayer.vue`
- expose time and stats events

## Phase 3: Add a migration switch
- keep the old player temporarily
- add a feature flag or adapter layer
- compare behavior side by side if needed

## Phase 4: Add feature modules
- analytics
- subtitles and track UI
- 5.1 structured audio, text, and video preferences
- subtitle delay controls, if product scope needs them
- quiz overlays
- timeline markers
- ads
- conductor or playlist

## Phase 5: QA and rollout
- browser matrix
- Safari and iOS pass
- leak checks
- staged rollout
- remove the old player only after confidence is high
