For exact version provenance and live-source authority, use [authority and API lookup](../05-authority-and-api-lookup.md); do not infer an unrecorded verification date from this split.

## 6. Verify live before answering

- Any "latest", "current", or post-snapshot claim.
- Quasar UI 2.22 and 2.23 release notes (see above).
- `@quasar/app-vite` 3.1 and 3.2 changelogs: config keys added or changed since 3.0, and whether §4 is still complete.
- Browser claims in `30`, `40`, `45`, dated 2026-07-08: Baseline status, iOS/Safari cadence, permission UI, grant expiry, auto-revocation, `<geolocation>` rollout.
- Still UNVERIFIED at 2026-07-28: Static Routing API outside Chromium; Declarative Web Push in Chromium; `@quasar/testing-*` extension v3 compatibility; the exact default dotenv file list; exact Safari grant-expiry windows; the `<geolocation>` recovery percentage; camera and microphone permission elements.
- **Resolved on 2026-07-28:** `@quasar/app-vite@3.2.0` still declares `bin: { quasar: "./bin/quasar.js" }` (registry manifest), and `quasar describe` ran against the live `client` checkout on installed 3.0.0. The exact-API authority chain in `references/05-authority-and-api-lookup.md` holds. Re-check this whenever a new app-vite major appears.

Use only quasar.dev, the `quasarframework/quasar` GitHub releases, the npm registry, MDN, web.dev, developer.chrome.com, and webkit.org. A community post is a troubleshooting hint, never a migration rule.


## 7. Skill maintenance

- When any upstream version, import path, config key, or folder changes: search the whole pack for the old string and update every occurrence plus the snapshot date in §2. Updating only the snapshot leaves the pack contradicting itself.
- Never snapshot component, directive, or plugin API output into a file. `scripts/query-installed-quasar-api.mjs` stays version-neutral and delegates to the target project's own CLI.
- If `latest` for `@quasar/app-vite` becomes v4, reassess the whole posture of this skill, not only the numbers.
- After changing `scripts/query-installed-quasar-api.mjs`: run `--self-test`, then run it against one installed app-vite v2 project and one v3 project, confirm the reported app-vite and Quasar versions match the projects' package metadata, confirm the missing-project failure message is actionable, and run both a narrow symbol query and a `list` query — one output shape is insufficient.
- After changing `scripts/check-upstream-versions.mjs`: run `--self-test`, then a live run, and confirm that a single unreachable package still prints the other results and exits `2`.
