## 2. Release refresh, read 2026-09-29

Official releases observed: [app-vite 3.10.0](https://github.com/quasarframework/quasar/releases/tag/@quasar%2Fapp-vite-v3.10.0)
(2026-09-22), [Quasar UI 2.33.2](https://github.com/quasarframework/quasar/releases/tag/quasar-v2.33.2)
(2026-09-23), and [MCP 1.1.0](https://github.com/quasarframework/quasar/releases/tag/@quasar%2Fmcp-v1.1.0)
(2026-09-22). Installed packages still decide consumer availability; recheck before calling these latest.

Registry read on 2026-09-29 confirmed `@quasar/app-vite 3.10.0`, `quasar 2.33.2`,
`vite 8.3.1`, and `vue 3.5.43` as each package's `latest`; app-vite v2 remains `2.6.2`.
The [3.10.0 manifest](https://registry.npmjs.org/@quasar%2Fapp-vite/3.10.0) declares
Node `^30 || ^28 || ^26 || ^24 || ^22.22.0`, Quasar `^2.24.0`, Vue `^3.2.29`,
Router `>=5`, Pinia `^2 || ^3 || ^4`, and TypeScript `>=5`. Peer acceptance is not
proof that a consumer's plugins, SFC typechecker, or runtime work together; keep the
Vue owner's TypeScript compatibility gate. No upgrade or installation is implied.

Material app-vite 3.10 changes and agent checks:

- PWA + SSG `InjectManifest` excludes renderer `__ssg__` files from precaching, as `GenerateSW` does.
  Inspect the built precache, then exercise offline navigation and the update path; do not infer
  correct caching from a successful build alone.
- Newly generated PWA/BEX modes include additional icon entries. Existing manifests need an explicit
  asset/manifest migration; a package bump does not rewrite them. Verify icon paths and PWA purposes.
  Icon Genie v7 execution or installation needs the task's authority.
- Capacitor splash configuration defaults `androidScaleType` to `CENTER_CROP`, preserving explicit
  values and other plugin settings. Check explicit overrides and the shipped device aspect ratios.

MCP 1.1.0 can serve multiple workspace apps. Its five local docs/API tools accept `app`; omitting it
selects the first app. Verify answer app/version, using `05-authority-and-api-lookup.md`. Update
discovery covers distinct installed versions, not proof of upgrade compatibility. No MCP is required.
