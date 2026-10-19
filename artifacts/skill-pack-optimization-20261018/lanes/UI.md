# UI source decisions

Date: 2026-10-18. Parent ratified these bounded decisions, closed the source leaf and confirmed the implementation leaf claim before product edits. All ratified UI edits are applied. Beads and the parent workflow own task state.

AGENT: alaa-implementer. CONFIGURED model/effort: absent in neutral source and installed definitions. REQUESTED: gpt-6.1-sol/medium. OBSERVED: unknown; no serving-identity evidence. Effective authority is limited to the five assigned UI skill trees and UI-prefixed lane artifacts, within workspace-write. External MCP enforcement is unknown. No nested agents, install, emission, commit or global edits.

## Sources and decisions

Original proposals are the immutable intake-snapshot.json report content, not a new transcript count. Paths below are relative to skills/sohrab/. Existing external routers remain in place; relocation is a separate semantic change. UI-read-provenance.json records hashes of all 131 fully read owned files (792,572 bytes). Full bodies, nested references, scripts, metadata and evaluations were read before product edits; truncated regions were completed with bounded continuation reads.

| Item | Original recommendation | Ratified decision and deciding evidence | Preserved invariants |
|---|---|---|---|
| 01:A19 | Sanitize through one render-time path; tighten security owner | Adapt frontend-developer ref25 to security-review ref25 Raw HTML: exactly one path and Vue ref72. SHARED owns security edits. | Output sanitization cannot be bypassed by another writer; optional input defense remains possible; no handwritten sanitizer or second raw-HTML path. |
| 01:A20 | Defer navigation strategy to Quasar ref30 section 1 | Accept for frontend ref30 standard contract AND its chunk-404 diagnostic, plus QA wording. Quasar ref30 already allows precached shell or NetworkFirst. | No unauthorized SW strategy change; never force network-only where the canonical strategy permits offline navigation; retain offline fallback and old-asset retention boundary. |
| 01:A22 | Permit built-ins outside config module | Adapt narrowly: installed-version framework-owned constants may be read locally; project-injected and runtime values stay behind one typed validated config module. Update frontend ref48, Vue ref50 and devops ref10/ref30 consistently. | BASE_URL derives from publicPath; no arbitrary QUASAR_* exemption; no project variable exemption or second runtime source. |
| 01:A23 | Remove frontend font figure, point Persian guidance to UI owner | Adapt: preserve historical <100 KB subset scope separately from 150 KB total transferred first-party fonts on the initial route; neither replaces the other. UI ref45 owns font limits; ref05 routes there. | Historical units, strictness and subset/whole-route scopes; three weights, woff2 support exception, two preloads, Arabic/Latin/U+200C subset and transferred-size measurement. |
| 01:A39 | Use package-manager placeholders and lockfile owner | Accept Vue ref60 script/local-exec equivalents selected by existing lockfile; Quasar body retains lockfile rule. | Existing script flags, final exhaustive tier authority, equivalent build/typecheck reuse; no package download or manager switch. |
| 01:B11 | Quasar ref30 owns Cache Storage; IndexedDB ref61 owns tokens | Adapt only UI consumers to those owners. Quasar ref34 Cache Storage contents becomes a pointer to ref30 section 2; body retains a short ownership boundary. PLAYER owns IndexedDB changes. | Credentialed request network-only/exception/logout-purge gates and app-local memory token posture survive. No cross-lane edit. |
| 01:B12; 02:O13 | Quasar ref75 owns SW runbook; frontend points | Adapt: transfer all five manual scenarios alongside automated regressions, then replace frontend list with triggered pointer. | Install/first-load, update waiting/SKIP_WAITING/reload-once/no missing chunk, offline reload/direct-navigation/no loop, allowed runtime-cache entries, online regression; production build only. |
| 01:B13 | Merge body routers into existing topic maps | Accept. Preserve external maps and original behavioral ordering, unique triggers and destinations; leave one short triggered body pointer. Move frontend ownership routes into its map and update ref70's owner-table location. | No reference-count retirement, no duplicate body router; reduced-motion gate, permission timing/recovery, custom-SW pairing order and operational record remain reachable. |
| 02:O6 | Add applies-when triggers to frontend QA | Adapt explicit mode plus affected-surface triggers; point to Quasar-owned runbook. | Render/hydration proof remains owed for changed SSR initial output/boot/auth paths; no unrelated SSR/SW execution for static-only or absent-mode work; unrun mandatory checks remain blockers. |
| 01:A21 consumer | Consolidate required browser signals under observability | Consume SHARED observability ref20 Browser client signals six conditional classes; remove competing local lists and unsupported local rates. Quasar retains mechanics and services owns emitted names. | Errors/rejections, Web Vitals, HTTP outcomes where HTTP exists, WS/SSE transitions where present, SW lifecycle and failed updates where present; missing names/rates remain gaps. |
| 03:N2 consumer | Extend existing Quasar ref36 section 5 after settling config ownership | Accept SHARED services ref21 and observability ref60 authority split; add pinned SDK selection and SPA/SSR wiring to existing ref36. | Approved target browser config keys only; public DSN is an event-submission credential with abuse exposure, never server SENTRY_DSN fallback; tokens stay CI/server; privacy uses installed SDK options and per-signal hooks; no installation or live emission proof. |

## Official source findings

- Quasar boot files document app/router access and client-only boot as server:false; client:true alone does not exclude SSR. Source: https://quasar.dev/quasar-cli-vite/boot-files/ (read: 2026-10-18).
- Vite distinguishes built-in constants from project variables. Source: https://vite.dev/guide/env-and-mode (read: 2026-10-18). Exact Quasar constants require installed-line evidence, not a wildcard.
- Sentry v11 replaces sendDefaultPii with dataCollection and changes defaults. Source: https://sentry.io/changelog/javascript-sdk-v11/ and https://github.com/getsentry/sentry-javascript/blob/develop/MIGRATION.md (read: 2026-10-18). Therefore do not prescribe one universal privacy option. Target pinned-version API inspection remains required.
- Sentry Vue pages returned unsupported text/markdown through web fetch; native HTTP retrieval failed authentication. The official GitHub documentation/source was the successful alternate: https://github.com/getsentry/sentry-docs/blob/master/docs/platforms/javascript/guides/vue/index.mdx and https://github.com/getsentry/sentry-javascript/blob/develop/packages/vue/src/sdk.ts. No package install ran. Node startup instructions remain version-matched: v11 migration changes preload behavior, so no universal preload command is prescribed.

## Verification boundary

Implementation touched 21 Markdown files listed in UI-changed-paths.json. No product script, vendor file, dependency, reference retirement, sibling or global configuration changed. UI-draft.json preserves pass-one text; pass two shortened the Quasar body companion catalog into an authority boundary, retained payload diagnostic content, and corrected the shared sampling/threshold gap pointer. UI-diff.json holds scoped diff evidence.

- `python -B scripts/check_fleet_references.py` with the five repeated exact skill selectors: exit 0, 120 Markdown files, 608 citations, no findings; one informational target path remains.
- `python -B skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py . --files` with the exact 21 changed paths: exit 0.
- `git diff --check --` with the exact 21 changed paths: exit 0, no output.
- UTF-8/no-BOM/LF/nonzero product and lane artifact assertion: the first pass flagged the empty diff-output log, not a product defect. Recorded its successful no-output result explicitly, then reran only the encoding assertion. Final result is in UI-verification.json.
- Frozen covered-input manifest and untouched owned-file baseline assertions passed. Commands, cwd `.` and bounded normal-priority resource policy are in UI-task-snapshot.json; product hashes are in UI-verification.json.

No browser QA, product build, live SDK emission, SDK installation or independent review ran: these are prose-only skill changes and their script inputs are unchanged. Parent owns Phase 4 aggregate review and acceptance. Growth adds the named capability: source-backed SPA/SSR Sentry wiring and preservation of manual SW scenarios at their canonical owner.

## Compatibility and counterexamples

- A second writer bypassing an input-only sanitizer still reaches the sanctioned output sanitizer.
- A precached navigation shell is judged against Quasar ref30, including the former chunk-404 network-only clause.
- A framework constant can be read locally; a project-defined similarly prefixed value still requires validated config.
- Both font measurement scopes survive; no historical threshold or unit was silently replaced.
- A CSS-only change with no SSR/SW impact does not trigger those runtime gates; an affected SSR or PWA path retains its required proof and missing-runner blocker.
- Manual SW install/update/offline/runtime-cache/online cases survive relocation, alongside remote-asset checks for InjectManifest when present.
- Custom SW/InjectManifest routes load ref32 before ref30 in symbol, situation and body-origin pairings; every other original mandatory trigger remains reachable from the same external map.
- Missing browser metric names, rates or collector-failure thresholds remain configuration gaps; no synthetic names or values were added.
- Browser SDK boot excludes SSR with server:false; server SDK uses request-isolated context and its pinned-version startup mechanism. beforeSend alone never proves privacy of other signals.

Rollback is a scoped local text revert; no published wire, runtime config or dependency was changed. No blocker remains in the UI lane; independent acceptance and Git effects remain parent-owned.

## Evidence ordering correction

The original combined digests used Windows pathlib.Path ordering, which compares paths case-insensitively. Replaying each stored files array reproduced both former digests; every individual file size and SHA-256 still matched current bytes. UI-evidence-correction.json preserves those former digests and the evidence-only correction command. No product or checker input changed, and fleet/link/product checks were not rerun.

Both manifests now use the plan's platform-independent convention: sort relative POSIX path strings ascending and case-sensitively; concatenate UTF-8 path, one NUL byte and raw file bytes for each entry, with no separator after the file bytes; SHA-256 the complete stream. UI-finalize.py now enforces this ordering explicitly but was not executed again. UI-diff.json points to the corrected changed-file digest.

- Task manifest: 753164595219d8d26a70bedfdfe5d06319193bbc35a0f11204a1040735023d2b (136 files).
- Changed-file manifest: 9f45c1a91449f05ac08a169c3902fdd4227e9bae4cb47eb4aacd8ac74efd1138 (21 files).
- Read provenance covers 131 fully read files in the five owned skill trees. The task manifest adds two checker inputs (fleet references and repository Markdown links) and three shared source dependencies (observability refs20/ref60 and services-contract ref21), totaling 136. This is a coverage-scope difference, not five missing owned reads.

UI-evidence-check.json records the final evidence-only digest, ordering, encoding and pointer assertions. Original product-validation results remain unchanged in UI-verification.json.
