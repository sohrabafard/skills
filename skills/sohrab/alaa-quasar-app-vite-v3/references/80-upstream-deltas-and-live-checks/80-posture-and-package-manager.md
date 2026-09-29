## 8. Posture history

- 2026-07-06/07: app-vite `3.0.0` then `3.0.1`; v3 became stable after beta and RC from 2026-05-06. v2 `2.6.2` entered maintenance, approximately through 2027-06.
- 2026-07-08: absorbed the retired `quasar-skill-packe` (Quasar shapes, atlases, modes, guardrails) and `alaa-app-vite-quasar` (v2 playbook, deltas, testing, CI).
- 2026-07-10: became a control plane rather than an API mirror — exact APIs route to the project-local `quasar describe`; atlases keep intent, alternatives, gotchas, and search vocabulary; no MCP is required.
- 2026-07-28: the SSR/PWA playbook (33) and the maintenance file (90) were retired into this file and into `30`/`31`/`32`/`22`; failure, observability, step-up, and operations references added; the delta set and the version snapshot consolidated here.


## 9. Package managers

A repo's package manager is a contract: a Yarn workspace or `yarn.lock` means Yarn. Registry queries discover versions, not manager policy; upstream support for Bun or pnpm never justifies switching during a Quasar task. pnpm v11 with app-vite v3 needs the `allowBuilds` entries in §4.

Docs: `vite.dev/llms.txt` and `vite.dev/llms-full.txt`; stable `vite.dev`, not the ahead-of-release `main.vite.dev`; Quasar docs for API plus releases and npm for freshness; the upgrade guide at `quasar.dev/quasar-cli-vite/upgrade-guide/`.

Search: `latest version`, `dist-tags`, `peer range`, `pinia 4`, `Node engines`, `v2 v3 delta`, `Rolldown`, `Oxc`, `Lightning CSS`, `rolldownOptions`, `filenameBasedRouting`, `serve.devError`, `defineCapacitorConfig`, `upgrade guide`.
