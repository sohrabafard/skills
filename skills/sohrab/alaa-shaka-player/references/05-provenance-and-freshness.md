# Provenance, freshness, conflicts and open questions

Every upstream fact in this skill was read on **2026-07-28** from the tagged repository
`v5.2.3` (commit `25651923afafc7e39c736b46a377c3648b3aeb1a`) or from a live URL listed below.
A Shaka claim written anywhere in this skill without a URL and a read date is not yet a fact.

## Anchor

| Fact | Value | Source |
|---|---|---|
| Current release | **v5.2.3**, 2026-07-27 | `https://github.com/shaka-project/shaka-player/releases/latest` (read 2026-07-28) |
| `package.json` version at tag | `"5.2.3"` | `https://github.com/shaka-project/shaka-player/blob/v5.2.3/package.json` (read 2026-07-28) |
| Maintained branches | v5.2 (latest), v5.1 (previous), v4.16 (LTS until 2027-01-31), v4.15 (Cast Application Framework) | `.../blob/v5.2.3/maintained-branches.md` (read 2026-07-28) |
| Versioning policy | Semantic versioning since v3.0; any same-major upgrade is backward compatible | `.../blob/v5.2.3/docs/tutorials/upgrade.md` (read 2026-07-28) |

**Consequence for this skill's own history.** The `5.0.8 → 5.1.11` migration the previous edition of
this skill documented was never a migration: `5.0.x → 5.1.x` is a minor bump and backward compatible
by upstream's stated policy. Both versions are superseded. The two migrations that exist are
**v4.16 LTS → v5** and the announced **v5 → v6.0** preference-array change; both are in
`80-version-migration-and-release-deltas.md`.

## Grading vocabulary — carry it forward, do not flatten it

| Grade | Meaning |
|---|---|
| `verified` | A page or file states it; the URL is given. |
| `inferred` | Reasoned from something read; the basis is named. |
| `not documented` | **Searched and not found. This is not proof of absence.** The search is named. |
| `conflicting` | Two upstream sources disagree; both are recorded, neither is picked. |

A row graded `not documented` may not be rewritten into "Shaka does not support X". It means the search
named in the row did not find it, and the next agent may search differently.

## Re-read rule

Re-read the sources below and update this file when **any** of the following is true — these are
observable conditions, not a schedule:

1. You are about to change the pinned `shaka-player` version in any repository.
2. The anchor date above is more than **60 days** old and the task asserts a "current" or "latest"
   Shaka behaviour.
3. The task concerns DRM, iOS/Safari, a TV or console platform, ABR, ads, or a security property.
4. You are about to carry forward a workaround that this skill or a repository comment records.
5. A console deprecation warning names a key or method this skill still teaches.

Update procedure: re-read `releases/latest`, then `CHANGELOG.md`, then `docs/tutorials/upgrade.md`,
then the specific externs or `lib/` file for the claim. Record the new read date in this file's anchor
table. An open issue or PR may be cited as a **symptom**, never as fixed behaviour; only a release note
or an official doc records a fix. A local reproduction that no longer shows a symptom is evidence the
workaround can leave *this* repository, not evidence that upstream changed.

## Authoritative source order

1. `externs/shaka/*.js` and `lib/util/player_configuration.js` — the actual typedefs and the actual
   default values. **These win over the tutorials** (see conflict C6).
2. `lib/**` at the release tag — the actual behaviour.
3. `CHANGELOG.md` and `docs/tutorials/upgrade.md` — what changed and when.
4. `README.md` — the platform, DRM, format and codec matrices.
5. `docs/tutorials/*.md` — narrative guidance. **Two of these are stale at v5.2.3** (C2, C6).
6. The hosted API docs at `https://shaka-project.github.io/shaka-player/docs/api/` — note these are
   nightly docs tracking `main` and carry **no library version string** (read 2026-07-28, JSDoc
   generation date `Tue Jul 28 2026 07:23:33 GMT+0000`). The former host
   `shaka-player-demo.appspot.com/docs/api/` now 302-redirects there.

## Live reads, 2026-07-28

| URL | Read for | Result |
|---|---|---|
| `github.com/shaka-project/shaka-player/releases/latest` | version + date | v5.2.3, 2026-07-27 |
| `github.com/shaka-project/shaka-player/releases` | release cadence | OK |
| `registry.npmjs.org/shaka-player/latest` | npm metadata | reported **5.1.11** — conflict C1 |
| `registry.npmjs.org/-/package/shaka-player/dist-tags` | npm dist-tags | `latest: 5.2.2` — conflict C1 |
| `data.jsdelivr.com/v1/packages/npm/shaka-player@5.2.3?structure=flat` | published `dist/` listing | full listing; no `.mjs` ships |
| `shaka-player-demo.appspot.com/docs/api/index.html` | old docs host | **302** to `shaka-project.github.io` |
| `api.github.com/repos/shaka-project/shaka-player/releases` | release list via API | **HTTP 403, refused** |
| `api.github.com/.../contents/docs/tutorials` | tutorial list via API | **HTTP 403, refused** |
| `github.com/shaka-project/shaka-player/tree/main/docs/tutorials` | tutorial list via HTML | **ROBOTS_DISALLOWED, refused** |

Three retrieval refusals are recorded rather than worked around. An agent that needs the tutorial file
list must clone the tag.

## Repository reads at tag `v5.2.3`

Base: `https://github.com/shaka-project/shaka-player/blob/v5.2.3/`

`package.json` · `CHANGELOG.md` · `maintained-branches.md` · `README.md` ·
`docs/tutorials/{welcome,basic-usage,config,network-and-buffering-config,errors,upgrade,offline,fairplay,license-server-auth,ad_monetization,ui,ui-customization,text-displayer,preload,queue-manager,transmuxing-in-worker,faq}.md` ·
`externs/shaka/{player,net,offline,ads,abr_manager}.js` · `ui/externs/ui.js` ·
`lib/player.js` (9,692 lines) · `lib/util/{error,fake_event,player_configuration,state_history,stats,switch_history}.js` ·
`lib/net/networking_engine.js` · `lib/offline/{storage,stored_content_utils}.js` ·
`lib/offline/indexeddb/storage_mechanism.js` · `lib/text/*.js` · `lib/polyfill/` ·
`lib/ads/ad_utils.js` · `ui/{ui,controls,element,localization}.js` · `ui/locales/` (49 files) ·
`ui/*.less` · `build/{all.py,build.py,wrapper.template.js}`

## Recorded conflicts — carried forward, not resolved

| ID | Subject | A | B | What to do |
|---|---|---|---|---|
| **C1** | Current version | GitHub + jsDelivr: **5.2.3** | npm `dist-tags`: **5.2.2**; npm `/latest`: **5.1.11** | Pin an exact version. `npm i shaka-player@latest` may not give you 5.2.3. |
| **C2** | `adManager.initClientSide(...)` | `upgrade.md` §v5.0 removed it; `externs/shaka/ads.js` has no such method | `docs/tutorials/ad_monetization.md` §"Client Side Ads Insertion" **still shows the call** | The tutorial line is stale. **Do not copy it** — calling it throws. See `55-ads-vast-vmap-and-ima.md`. |
| **C3** | Player constructor | `upgrade.md`: "constructor no longer takes `mediaElement`" | `lib/player.js` L726–736 still declares it and calls `attach()` after a deprecation warning | Deprecated but functional. Write the no-argument form anyway. |
| **C4** | `streaming.gapPadding` default | externs: "0.01 for Xbox and Legacy Edge, Tizen at 2" | `player_configuration.js`: `gapPadding: 0` | A normal desktop browser gets `0`. Set it explicitly if it matters. |
| **C5** | `ManagedMediaSource` on iOS | `README.md`: supported since iOS 17.1 / iPadOS 17 | `faq.md`: "in a future version, we plan to support" | Unresolved. Branch on `player.getLoadMode()`, never on a version assumption. |
| **C6** | `config.md` example dump | shows `defaultBandwidthEstimate: 500000`, `segmentPrefetchLimit: 0`, `retryParameters.timeout: 0` | code: `1e6`, `1`, `30000` | The tutorial dump is several versions stale. **Trust the externs and `player_configuration.js`.** |
| **C7** | `abr.safeMarginSwitch` default | externs prose: "Defaults to `o`" | code: `0` | An `o`/`0` typo. The default is `0`. |
| **C8** | Which build `types` describes | `package.json` `"types": "dist/shaka-player.compiled.d.ts"` (**non-UI**) | the package also ships `dist/shaka-player.ui.d.ts` | Default TypeScript resolution gives non-UI types even when you load the UI bundle. See `12-bundling-and-vite-loading.md`. |

## Open questions — carried forward

Each is phrased so one pass with the right access could answer it. None may be silently closed.

1. Which npm dist-tag is authoritative now? Re-query `registry.npmjs.org/-/package/shaka-player/dist-tags`.
2. Is `initClientSide` in `ad_monetization.md` a documentation bug? Confirm against `lib/ads/`.
3. How do you delete a single **incomplete** offline entry? `StoredContent.offlineUri` is `null` while
   `isIncomplete` is `true`, and `storage.remove()` takes a URI.
4. What is upstream's position on `navigator.storage.persist()`? Shaka never calls it and the offline
   tutorial never mentions eviction.
5. What is the real default of `streaming.gapPadding` on a normal desktop browser? (C4)
6. Is `ManagedMediaSource` used on iOS 17.1+ today, or still planned? (C5)
7. Which Shaka version do the hosted API docs correspond to? The page carries only a JSDoc date.
8. Is there an officially recommended React integration pattern? Only Vue is documented, and only as a warning.
9. Is `abr.safeMarginSwitch`'s "Defaults to `o`" reported upstream? (C7)
10. What exactly changed in "net: isolate headers across retry attempts" (5.2.2, #10361)? Any app that
    mutated `request.headers` in a filter and relied on the mutation persisting across attempts may have
    silently changed behaviour on upgrade.
11. Does `shaka-player.ui.d.ts` fully type the UI namespace, or do UI consumers need ambient declarations?
12. Are the legacy `preferred*` keys typed anywhere for TypeScript users? They work at runtime via a shim
    but are absent from the `PlayerConfiguration` typedef.

**Best practice.** Cite the blob URL at the tag, not `main` — `main` moves and the citation stops
meaning what it meant.
**Common mistake.** Treating a `not documented` row as a documented absence, then writing "Shaka does
not support X" into a skill or a PR description.
