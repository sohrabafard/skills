### Historical npm snapshot, read 2026-07-28

The table and peer ranges below retain historical provenance; they are not the current release list
or verified peer ranges for 3.10. Read the intervening changelogs for a consumer upgrade.

| Package / line | Stable | Published | Note |
| --- | --- | --- | --- |
| `@quasar/app-vite` production | `3.2.0` | 2026-07-22 | holds `latest`; new-app default. 3.1.0 landed 2026-07-21 |
| `@quasar/app-vite` maintenance | `2.6.2` | 2026-06-03 | supported approximately until 2027-06 |
| `quasar` (UI) | `2.23.3` | 2026-07-28 | versioned independently of the CLI |
| `@quasar/extras` | `2.0.2` | 2026-07-02 | ESM-only; icon-library cuts require an audit |
| `vite` | `8.1.5` | 2026-07-16 | app-vite 3.2.0 depends on `vite ^8.1.5` |
| `vue` | `3.5.40` | 2026-07-16 | — |
| `vue-router` | `5.2.0` | 2026-07-15 | v5 required by app-vite v3 |
| `pinia` | `4.0.2` | 2026-07-15 | see the peer range below |
| `workbox-build` / `workbox-core` | `7.4.1` | 2026-05-04 | — |

Peer and engine ranges declared by `@quasar/app-vite@3.2.0`, read from the registry manifest on 2026-07-28:

```text
node       ^22.22.0 || ^24 || ^26 || ^28 || ^30
quasar     ^2.21.3
vue        ^3.2.29
vue-router >= 5
pinia      ^2.0.0 || ^3.0.0 || ^4.0.0   (optional peer)
workbox-build >= 7                       (optional peer)
typescript >= 5                          (optional peer)
@capacitor/cli >= 5                      (optional peer)
@electron/packager >= 19; electron-builder >= 22
```

**Pinia 4 is accepted by app-vite 3.2.0.** Do not tell a team the range is `^2 || ^3`; that was the 3.0.x range. Re-read the peer block of the installed version before advising a Pinia bump.

This snapshot expires. Between 2026-07-10 and 2026-07-28 app-vite moved 3.0.1 -> 3.2.0 and Quasar UI moved 2.21.1 -> 2.23.3. Run the script before quoting any number.
