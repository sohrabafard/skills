# Sources, Freshness and Maintenance

Read this before asserting that something is current, and when updating this skill.

## No version snapshot ships here

This skill states no package versions. A version written into prose is stale the week after it is
written, and this skill previously carried five copies of one snapshot. The source of truth is the live
check, which belongs to `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`)
`scripts/check-upstream-versions.mjs` — the fleet's only copy. Run it from that skill's root before any
version-sensitive change; it takes `--help` and `--self-test`, honours `HTTPS_PROXY`, applies a request
timeout, and isolates a failing package so one unreachable registry entry does not lose the rest.

The `@quasar/app-vite` line in use, and what each line supports, is that skill's `references/00-topic-map.md`.

## Source order

1. **Repo-local contracts first**: `package.json`, the lockfile, the Quasar and Vite config, the SSR and
   PWA files, route guards, API clients, and the tests. What the repo does outranks what a doc says it
   should do.
2. **Official documentation** for the affected surface: Vue docs and release policy; Quasar docs and the
   Quasar CLI with Vite upgrade guide; Vite docs and migration guide; Workbox docs; MDN for a browser API;
   the Lighthouse repository for a scoring value.
3. **Official release notes, npm metadata and upstream changelogs** for a version-sensitive claim.
4. **Community posts and issue comments as leads only** — use them to find a reproduction, then verify.
   Do not encode an anecdote as durable policy.

Re-check an official source before claiming current behaviour for Vue lifecycle, hydration or watcher
semantics; Quasar SSR and PWA behaviour; Vite transforms; Workbox defaults; a browser API's availability;
or anything security-sensitive in auth.

## Freshness notation

A claim taken from a source carries the source and `read: <ISO date>`. A claim that could not be verified
ships as `read: unverified as of <ISO date>` rather than being stated plainly or silently dropped. "Not
documented" means searched and not found, not proof of absence.

Claims in this skill with a stated Baseline or availability tier — `scheduler.yield()`, Speculation Rules,
HTTP 103 Early Hints, Vue lazy hydration — are in `41-lighthouse-and-web-vitals.md` with their read dates.
Re-check them when a new browser Baseline year is published.

## Package manager

Stay Yarn-first when the repo has a `yarn.lock`. Upstream support for another package manager is not a
migration recommendation. A registry check is discovery, never a reason to change the package manager.
Workspace and package-manager mode questions are `/alaa-mono-package` (`$alaa-mono-package`)
`references/15-package-manager-modes.md`.

## Model and effort

Not decided here and not stated anywhere in this skill. Model selection, reasoning effort and prompt
contract are `/alaa-prompting-guide` (`$alaa-prompting-guide`) `references/50-effort-and-thinking.md` and
`references/90-model-selection.md`. Authoritative OpenAI and Codex product facts are `/openai-docs`
(`$openai-docs`).

## Maintenance workflow for this skill

1. Keep the body a set of gates and one router pointer. New detail goes into a reference file, never into
   `SKILL.md`.
2. Keep `references/00-topic-map.md` the only router, and keep every row an observable condition. A row
   that mirrors a heading is broken.
3. Re-verify every cross-skill path against the fleet on disk after any batch that moves files. A path
   that names an owner but no longer resolves is worse than no pointer.
4. Re-verify the perishable claims listed above, and any Lighthouse weight or audit ID, when a new major
   Lighthouse ships.
5. Re-check that the two skills consuming `41-lighthouse-and-web-vitals.md` still route here rather than
   restating it.
6. Re-test whether realistic prompts still load this skill implicitly after any change to the description.
7. Every cross-skill call site carries both trigger forms, ``/alaa-x` (`$alaa-x`)``. `agents/openai.yaml`
   is Codex-only and stays `$`-form.
