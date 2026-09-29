# Frontend modernization evidence

> Citation notation: `<repo>/` denotes this repository root; resolve it before invoking a command. Path lists use this display prefix only; strip it when reproducing a recorded hash manifest. [Original exact evidence](./frontend-evidence.raw.txt.gz) preserves the pre-normalization text.

- Date: 2026-09-29. Lane: frontend_implementation; configured alaa-implementer-sol, gpt-6-astra/high; observed model/effort unknown.
- Base: `0e9681c8253de0373a9bbbe4a9ff24a91b38c6db`; current shared checkout. No commit, install, dependency update, consumer change, service operation or publication.
- Ownership: only alaa-quasar-app-vite-v3, alaa-shaka-player, alaa-vue-typescript-clean-code and alaa-indexeddb-browser-storage under skills/sohrab, plus this evidence file. Parent owns plan/checkpoint/assessment and independent review.
- Runtime: workspace-write sandbox, network enabled; scoped discipline enforced by lane instructions. Runtime isolation beyond the reported sandbox is unknown.

## Acceptance and authoring record

- [x] Reloaded parent plan/checkpoint after context recovery; read frontend-research.json and all files in the four owned skills, including references, examples, assets and scripts, before edits.
- [x] Applied frontend-developer, Vue clean-code, services-contract, trust-gateway-auth and low-noise boundaries, and prompting-guide alaa-prompting-guide/references/60-skill-authoring.md.
- [x] Draft decisions before compression: retain installed-package authority and historical provenance; replace unsupported current claims with dated official evidence; make consumer checks observable; keep optional enhancement fallback and trust boundaries.
- [x] Compression review: preserved triggers, scope, owner routes, safety, fallback, failure handling, proof limits and authority; normalized duplicate runtime call forms only in touched files. Replaced duplicate Shaka lifecycle implementation in reference 11 with canonical template links and an await-before-removal example.
- [x] Parent explicitly expanded scope for discovered lifecycle, null-source, queue-concurrency and IndexedDB fixture correctness defects; bounded regression examples added without dependencies.
- [x] Reviewed scoped diffs and caller/seam compatibility. IndexedDB inventory manifest includes its new regression script; no owned content-hash manifest exists.
- [ ] Independent integrated pack gates and review: parent gate, not claimed here.

## Sources and resulting changes

All following sources were read on 2026-09-29. Release evidence is not consumer runtime evidence.

| Official source | Observation and application |
| --- | --- |
| [Quasar app-vite 3.10.0](https://github.com/quasarframework/quasar/releases/tag/@quasar%2Fapp-vite-v3.10.0) | September 22 release: PWA/SSG InjectManifest exclusion, generated mode icons and Capacitor splash default. Added precache/offline/update and asset/config checks without installation authority. |
| [Quasar UI 2.33.2](https://github.com/quasarframework/quasar/releases/tag/quasar-v2.33.2) | September 23 tagged release, retained as observed version, not an instruction to upgrade. |
| [Quasar MCP 1.1.0](https://github.com/quasarframework/quasar/releases/tag/@quasar%2Fmcp-v1.1.0) | Multiple app selection and versioned answer provenance; explicit app selection avoids first-app ambiguity. Already configured optional lookup only; installed local API remains authority. |
| [app-vite 3.10.0 manifest](https://registry.npmjs.org/@quasar%2Fapp-vite/3.10.0), registry metadata for [Quasar](https://registry.npmjs.org/quasar), [Vite](https://registry.npmjs.org/vite), [Vue](https://registry.npmjs.org/vue) | Live owner script at 2026-09-29T09:19:40.081Z: latest app-vite 3.10.0, Quasar 2.33.2, Vite 8.3.1, Vue 3.5.43; v2 maintenance 2.6.2. Exact app-vite peer/engine ranges recorded in reference 80; old July table explicitly historical. |
| [TypeScript 7.0 release](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/) | Stable release does not supply stable programmatic API for Vue/Volar integration. Retain fleet TS6 and vue-tsc; an explicit migration must establish matched tooling, SFC/editor/build proof. Removed unsupported Quasar-support rationale and blanket ban on researching migration. |
| [Shaka 5.2.12](https://github.com/shaka-project/shaka-player/releases/tag/v5.2.12) | September 25 fixes inform retry, destruction/DRM, key-ID and caption scenarios. API baseline remains honestly v5.2.3; intervening patch review and runtime tests required for consumer upgrades. |
| [Vue lifecycle API](https://vuejs.org/api/composition-api-lifecycle.html#onbeforeunmount), [Vue 3.5.43 renderer](https://raw.githubusercontent.com/vuejs/core/v3.5.43/packages/runtime-core/src/renderer.ts) | unmountComponent invokes before-unmount hooks without awaiting returned promises. Removed false blocking claim. One exposed, shared disposal promise covers current destruction and pending initialization; owner awaits before removal when completion is required. Hook handles asynchronous rejection safely. |
| [StorageBucket browser compatibility data](https://raw.githubusercontent.com/mdn/browser-compat-data/main/api/StorageBucket.json) | Chrome 122 entries include indexedDB, caches and getDirectory; Firefox/Safari version_added false is dated evidence, not a timeless or guessed version claim. Market-share snapshot is historical, not fleet coverage. |
| [WICG Storage Buckets draft](https://wicg.github.io/storage-buckets/), [Chrome introduction](https://developer.chrome.com/docs/web-platform/storage-buckets) | Draft defines expiry; failed historical search was not absence proof. Check actual persistence grant; expiry can delete persistent data. Chrome IndexedDB-only wording conflicts with newer BCD; durability option remains implementation-specific. Probe operations, recover to default storage only with location reconciliation for unsynced work. |

## Correctness decisions and boundaries

- Shaka: null source previously returned without unloading active playback. It now unloads while keeping the handle reusable. Disposing twice returns the same promise and destroys once; pending attach is awaited and destroys unpublished instances. Raw teardown errors are classified, not logged. No API name, auth contract or consumer dependency changed.
- QoE: after sending a batch, slicing pending by its old length could delete newly enqueued entries when capacity eviction happened in flight. Acknowledgement now removes exact queue-entry identities, including repeated enqueues of the same object. Positive integer capacity is checked. Existing bounded oldest-entry eviction remains intentional; this is not a durable delivery guarantee.
- IndexedDB: `sending` sorts after `queued`. Safety is the exact-status bounded range, not a lexical-direction claim. Reaper and claim guidance/tests now agree. Production open helper always closes on versionchange; blocked-upgrade fixture uses a deliberately held raw connection instead of pretending an empty notification callback disables close.
- IndexedDB tests: prior quota fixture did not reliably induce quota failure; now injects quota rejection and asserts exactly one cleanup/retry and user notification. Prior logout test seeded one database but tested another and accepted zero deletions; optional database-opener injection preserves default API behavior and tests the seeded database with exact deletion/retention assertions.
- Vue checker: fixed hardcoded Router 4 gate conflicting with app-vite v3 Router >=5. Router major compatibility delegates to the installed app-vite peer authority; the checker remains discovery, not a peer solver. Pinia 3 gate is retained because reference 20 explicitly scopes its rules to that line.
- Rejected alternatives: blanket version replacement would falsify historical API/measurement proof; awaiting an async Vue hook cannot delay unmount; slicing by count cannot track ownership after eviction; disabling production versionchange cleanup to satisfy a broken fixture would regress multi-tab upgrades; installing test packages was unnecessary for bounded source-function proof and was not authorized.

## Verification

Commands below ran from repository root unless stated otherwise. Node v24.18.0 and Python 3.13 were observed. Python used `-B`. Node regression scripts executed through the supplied Invoke-AlaaLowPriority.ps1 with `-Priority BelowNormal -CpuCount 2 -TimeoutSeconds 45`; bounded unit work only.

| Command | Observed result |
| --- | --- |
| `node skills/sohrab/alaa-quasar-app-vite-v3/scripts/check-upstream-versions.mjs --package @quasar/app-vite --package quasar --package vite --package vue` | Exit 0; all four metadata lookups succeeded, exact versions above. Initial invocation wrongly included --timeout-ms and failed; one corrected invocation succeeded. No dependency mutation. |
| `node --experimental-vm-modules skills/sohrab/alaa-shaka-player/scripts/check-template-regressions.mjs` | Exit 0, PASS: concurrent queue-cap/send, repeated entry identity, retry retention, null unload, shared disposal, pending attach and hook rejection. Actual template functions loaded with Node TS stripping and Vue/Shaka doubles. Expected experimental Node warnings only. |
| `node skills/sohrab/alaa-indexeddb-browser-storage/scripts/check-storage-regressions.mjs` | Exit 0, PASS: bounded claims/reaping, quota cleanup plus exactly one retry, close-before-notify. Actual example functions with IDB doubles. |
| `python -B skills/sohrab/alaa-indexeddb-browser-storage/scripts/validate_skill_pack.py --root skills/sohrab/alaa-indexeddb-browser-storage` | Exit 0; structure, reference and manifest validation. |
| `python -B skills/sohrab/alaa-indexeddb-browser-storage/scripts/check_references.py --root skills/sohrab/alaa-indexeddb-browser-storage` | Exit 0; 21 reference files routed and paths resolve. |
| `python -B skills/sohrab/alaa-indexeddb-browser-storage/scripts/capability_contract_conformance.py --root skills/sohrab/alaa-indexeddb-browser-storage` | Exit 0; capability fields, tier contract and matrix agree; every index key path declared. Static consistency only. |
| `node skills/sohrab/alaa-vue-typescript-clean-code/scripts/check-frontend-versions.mjs --self-test` | Exit 0; 18 existing checks after changed router-major policy. |
| `git diff --check -- skills/sohrab/alaa-quasar-app-vite-v3 skills/sohrab/alaa-shaka-player skills/sohrab/alaa-vue-typescript-clean-code skills/sohrab/alaa-indexeddb-browser-storage` | Exit 0; no whitespace errors. |

Optional unchanged Python validator `--self-test` failed with WinError 5 creating nested fixture directories in its temporary directory. One cause-specific retry using process-local TEMP/TMP under the allowed cache root failed identically; no further retry. Validator code is unchanged, so its self-test is not a required gate under the parent plan. Only Vue's version checker changed; its self-test passed. The two new Node scripts are the executed regression tests themselves.

No fake-indexeddb runtime was found in bounded installed-tool discovery. Consumer Vitest tests, SFC typechecking, real browser blocked-upgrade behavior, media/DRM/network shutdown, device compatibility and deployed performance remain unrun. No claim that in-memory doubles establish those properties. Shaka API scanner requires a consumer package manifest and retains its historical baseline; no fake consumer project was created merely to claim a scan pass. Independent integrated review remains the parent's gate.

## Changed-scope snapshot

The following list records raw-file SHA-256 at lane handoff; paths are repository-relative. This evidence file is excluded from its own digest. No other lane's changes are included.

```text
74a966ae17916b91d0cd947984b66818e5a0cb1cc769fd93a63bc478b72855fb  skills/sohrab/alaa-indexeddb-browser-storage/SKILL.md
fed8ad42e3fced3977c7cd8d734376411184b7017d7e34405546788c72bf5870  <repo>/skills/sohrab/alaa-indexeddb-browser-storage/assets/capability-tier-contract.json
f18e6c4dd183dd4aa1ea4d5631e12a0ed9490068ac05b7b52dc357d0c307433c  <repo>/skills/sohrab/alaa-indexeddb-browser-storage/examples/alaa-client-storage.ts
f37e8e638b797338618bc411fd8366483adecca01c6880d35c28c232d2b9d940  <repo>/skills/sohrab/alaa-indexeddb-browser-storage/examples/browser-capabilities.ts
753edce11167dd9386cafcc6184cac6944f2fcd00219d8286661fd2e329c2336  <repo>/skills/sohrab/alaa-indexeddb-browser-storage/examples/outbox-pattern.ts
7c40b7616f86fa95af48d09c00e268f2bd12f7ea3f6a1fc0138ce17a1900d1ef  <repo>/skills/sohrab/alaa-indexeddb-browser-storage/examples/outbox-reaper.ts
d81f12f6a04b53b9c48caec8e34b7669652b5f79f2f08ee2518f5fae92affa3d  <repo>/skills/sohrab/alaa-indexeddb-browser-storage/examples/vitest-idb-pattern.test.ts
b55863888586deeaa47d288aa594636446f67d1efcda5722498f8605cbc73311  <repo>/skills/sohrab/alaa-indexeddb-browser-storage/references/20-browser-compatibility-and-capability-tiers.md
3757a73cb92f47907bc4f0f4eaf12a036d01dcfb834978fca62a16d5bc28a156  <repo>/skills/sohrab/alaa-indexeddb-browser-storage/references/25-storage-buckets-api.md
9b03f383a1da52fea3ead124e41bb296ef09be5a67186eef96157bfc9b8402e8  <repo>/skills/sohrab/alaa-indexeddb-browser-storage/references/71-browser-outbox.md
14d12602a60876453c966a350e1a9116360bff9eb301497174b61dd81d5a7b4b  <repo>/skills/sohrab/alaa-indexeddb-browser-storage/references/99-sources-and-maintenance.md
8010558b85bdb4cea21541b1bac2495c7ab14235154d8529750794e381dbb36c  <repo>/skills/sohrab/alaa-indexeddb-browser-storage/scripts/check-storage-regressions.mjs
854268b36e9ea7ec450df62b118a4970ae60421f266101e678a1a09a58faf9a1  skills/sohrab/alaa-indexeddb-browser-storage/skill-pack-manifest.json
e3606222214ea5ca3e37a1d27047d8648bf01b6028c156d9f512fce7571ba24c  skills/sohrab/alaa-quasar-app-vite-v3/SKILL.md
ff6a2453a26852a359930518b28dcf8a74c20917669ad01333283890bdac61e8  <repo>/skills/sohrab/alaa-quasar-app-vite-v3/references/05-authority-and-api-lookup.md
63f31c3ba7764742ddd1bd36bf1e08eb05405ceb7c53397e510f1702b531f249  <repo>/skills/sohrab/alaa-quasar-app-vite-v3/references/80-upstream-deltas-and-live-checks.md
7ee67cb881170bb4bf592b1cb7da180038e97e14f0716b13c8b8ebe7f3e32056  skills/sohrab/alaa-shaka-player/SKILL.md
7683ac3d33155e2caf2b282d00043d05128919fd1f2f28bfaae473fad82255ad  skills/sohrab/alaa-shaka-player/assets/templates/ShakaPlayer.vue
e233ac88026b13ad61b562a1156f4d8099874487e248619b834fd27a041ecb75  <repo>/skills/sohrab/alaa-shaka-player/assets/templates/playbackQoe.ts
838b4cca3c979772465f8e62ef0420abc88908d0cb46943dc9d38b0951358cce  <repo>/skills/sohrab/alaa-shaka-player/assets/templates/useShakaPlayer.ts
bcf55ed3435440c6105e5910259c42fd72d989d691887e23e585c906b253995a  <repo>/skills/sohrab/alaa-shaka-player/references/05-provenance-and-freshness.md
2701ea3ece72f646e05855ed1a074aa2bdf447d54669b114243c0f22f64aa168  <repo>/skills/sohrab/alaa-shaka-player/references/11-vue-quasar-binding.md
ed10158e3c195691945fe117e2601ce3b64fbfff26ee752ea4dd91d5e8ecafa5  <repo>/skills/sohrab/alaa-shaka-player/references/80-version-migration-and-release-deltas.md
18598647c03809e3544354d0f6890254986ad9dc67373d22d9733a29286fa54f  <repo>/skills/sohrab/alaa-shaka-player/references/85-troubleshooting-by-symptom.md
b682ea1ab00f0e9ac90d871a67f9fb7f76873405fc18649e70772151dff2c1b5  <repo>/skills/sohrab/alaa-shaka-player/references/90-qa-modes-and-checklist.md
caae61c419bb47af2231cdf15234b3b03ffb1640e299e5b3949c217612f69f12  <repo>/skills/sohrab/alaa-shaka-player/scripts/check-template-regressions.mjs
786b681a774fb98e74e522ee97c968544ffa09ba7a10d585268eeb0afa5a712a  <repo>/skills/sohrab/alaa-vue-typescript-clean-code/references/24-typescript-project-and-antipatterns.md
26f648de0774e52f0dea3f066b122e13a96a871604ee90e6a9d889bed7add30e  <repo>/skills/sohrab/alaa-vue-typescript-clean-code/scripts/check-frontend-versions.mjs
```

Changed files: 28. Digest of the UTF-8 manifest above (including each final newline): `5444db89240e1a982a1fce53efaebbf368272967f64872e1c8d57c4a5f2cc220`.

Snapshot reconciliation: `git diff --cached --name-only` returned no owned paths; `git diff HEAD` covers the same 26 tracked paths plus the two untracked regression scripts. Index was not modified. Focused validation accounting: 8 distinct required checks, 11 executions (including one rejected registry argument and two Vue self-test / whitespace-check executions); 2 optional unchanged-validator self-test attempts failed with WinError 5. Version/help discovery is excluded.
