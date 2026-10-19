# PLAYER source decisions

Parent ratified these source decisions and claimed PLAYER `.2`; product edits now implement them. PLAYER owns only
`skills/sohrab/alaa-shaka-player/`, `skills/sohrab/alaa-indexeddb-browser-storage/`, and this lane artifact.
Parent owns Beads, aggregate reports, checkpoints, and Git. The complete owned SKILL/ref/script read finished before
product edits.

AGENT: alaa-implementer-low. CONFIGURED: neutral installed role, model/effort unpinned; workspace-write.
REQUESTED: gpt-6-luna / medium. OBSERVED serving model/effort: unknown. Runtime tools expose no serving-identity
proof; this limits identity reporting, not implementation authority. Effective file scope is the repository
workspace; tool/MCP enforcement beyond that is unknown. No delegation or external effects.

The intake is immutable. `intake-snapshot.json` records source report SHA-256 values
`6de7223950f08711ad4946039995286cc7efafd4a1558f1876f8ddcf13f6e03a` (01, 89,165 bytes) and
`da0309f20c76b9bc98a3d3eda4e10ffcd8cdc2a3c815127a92c690e1ce06c7fa` (02, 33,447 bytes).
Original findings: 01:B23, 02:O4, 02:O27. The cited report content, not chat recounting, is the input.

## Ratified dispositions

| Finding | Source decision | Evidence and protected invariants |
|---|---|---|
| 01:B23 / 02:O27 | `alaa-indexeddb-browser-storage/references/72-offline-media-store.md` is the single owner of the browser-storage boundary and caller-side `persist()` fact. Remove the repeated quoted block and repeated substrate explanation in Shaka ref50, replacing them with one triggered pointer to IDB72. Retain every Shaka-specific API, partial-store detection/restart/cleanup, persistent DRM, and download behavior. | IDB72 states the seam once and already contains the reciprocal pointer and `persist()` obligations. Shaka ref50 repeats the identical quoted boundary and the no-`persist()` fact. Shaka owns player calls and format; IDB owns quota, persistence, eviction and cross-context substrate. Do not change browser behavior. |
| 02:O4 | Replace unconditional API-check/version-reference and QA burden with explicit triggers. Read Shaka ref80 and run `check-shaka-api.mjs` when the task changes an API surface recognized by the checker; cover every recognized family, including configure/errors, tracks, ads, offline, native HLS, gaps, UI and preferences. Use ref90's lightest fitting QA mode only when the changed behavior requires proof; report only changed-surface evidence. | Current SKILL.md steps 2 and 6 impose unconditional work. The checker’s `RULES` names the API families; limiting its trigger to configure/error would lose existing coverage. Ref90 selects modes and includes the API-check best-practice rationale. Preserve required evidence for any actual changed behavior. |

Alternatives rejected: keep the repeated block (declared reciprocal intent conflicts with AGENTS.md's one-owner rule and there is no drift checker); move the canonical boundary into Shaka (contradicts IDB72's established substrate ownership); trigger the API checker only for configure/errors (checker recognizes additional changed families); require it for every prose/config-only edit (does not match its API compatibility purpose); add a second body router or remove external maps (AGENTS.md requires preserving one existing external router absent relocation evidence).

Rollback is a local Markdown revert. No public runtime/API contract, wire data, or browser behavior changes. Compatibility risk is limited to missed skill triggers; retain a short triggered pointer, preserve reference destinations and router maps, and keep the checker contract broad enough to match its recognized families. Do not retire references based on link count.

## Source and boundary notes

Primary current evidence includes all files under both owned `SKILL.md`, `references/`, and `scripts/` trees, plus current cited sources from the immutable reports. The complete owned SKILL/ref/script read finished before product edits; no source outside the two assigned skills was edited.

UI's ratified owner anchor is Quasar30 §2 (CacheStorage); Quasar34 §3 routes there. Its credential distinction points to IndexedDB61; player work does not edit UI trees. The STORAGE source decision changes no browser behavior. Preserve both PLAYER external topic maps and IDB ownership distinctions; this lane does not alter any parent-owned artifact.
