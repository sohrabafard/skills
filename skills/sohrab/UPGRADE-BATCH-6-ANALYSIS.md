# Upgrade Batch 6 — Frontend — Phase 1 Analysis

**Written 2026-07-28. Advisor mode. No skill file was changed in this phase; this file is the only artifact created.**

This document is the working input for Phase 2. Sections 1–9 are the lead's synthesis and carry the decisions. Appendices A–I are the nine lane reports in full, unedited, and hold the file-and-line evidence every decision rests on. Where a section here says "see Appendix X", the appendix is the authority for detail and this section is the authority for the ruling.

**Batch membership**, per `UPGRADE-CARRYOVER.md` §5: `alaa-frontend-developer`, `alaa-vue-typescript-clean-code`, `alaa-quasar-app-vite-v3`, `alaa-ui-ux-design-system`, `alaa-frontend-devops`, `alaa-frontend-doc-annotations`, `alaa-mono-package`, `alaa-indexeddb-browser-storage`, `alaa-shaka-player`. Nine skills, 173 files, 725,262 bytes.

**Method.** Every file of every skill was read in full — including the 74,929-byte `alaa-indexeddb-browser-storage/references/full-guide.md` and all nine of its TypeScript examples, all thirty `alaa-quasar-app-vite-v3` references, and all nine `alaa-shaka-player` templates. Both `alaa-quasar-app-vite-v3` scripts and both `alaa-indexeddb-browser-storage` scripts were executed. Four mechanical surveys were run across the batch as a whole before any lane opened a file, and their results are §2. Nine analysis lanes then ran in parallel, one per skill except that `alaa-frontend-devops` and `alaa-mono-package` shared a lane because they sit on one seam. No lane audited another lane.

---

## 1. Inventory

| Skill | Body (net of frontmatter) | References | Other | Total | Files |
|---|---:|---:|---:|---:|---:|
| `alaa-frontend-developer` | 13,146 | 63,739 (13) | 4,021 | 80,906 | 16 |
| `alaa-vue-typescript-clean-code` | 20,628 | 66,816 (9) | 3,862 | 91,306 | 12 |
| `alaa-quasar-app-vite-v3` | 6,716 | 142,129 (30) | 8,995 | 158,608 | 34 |
| `alaa-ui-ux-design-system` | 10,888 | 62,124 (13) | 313 | 74,012 | 15 |
| `alaa-frontend-devops` | 3,956 | 8,677 (5) | 272 | 13,298 | 7 |
| `alaa-frontend-doc-annotations` | 2,619 | 4,869 (4) | 286 | 8,082 | 6 |
| `alaa-mono-package` | 7,285 | 6,251 (5) | 286 | 14,108 | 7 |
| `alaa-indexeddb-browser-storage` | 8,883 | 150,450 (14) | 36,245 | 196,503 | 35 |
| `alaa-shaka-player` | 10,715 | 33,895 (17) | 28,948 | 74,719 | 41 |
| **Batch** | **84,836** | **538,950** | **83,228** | **725,262** | **173** |

Two numbers are worth holding. The **always-loaded cost of the batch is 84,836 bytes** — an agent that loads three of these skills for one frontend change pays for all three bodies before reading a single rule. And `alaa-quasar-app-vite-v3` carries 142 KB of references behind a 6.7 KB body while `alaa-mono-package` carries 6.3 KB of references behind a 7.3 KB body: the two extremes of the batch are inverted with respect to each other, and only one of them is the right way round.

Clean across all nine: **no `__pycache__`, no `.pyc`, no `node_modules`, no `.DS_Store`, no stray build artifact.** Defect class 8 does not appear in this batch.

---

## 2. The batch-level findings

Four defects are properties of the batch rather than of any skill in it. Reporting them nine times would be nine findings where there is one. Batch 4's memory mandates running the doctrine-owner grep before analysing anything; this is its result, plus three more surveys of the same kind.

### 2.1 The silence finding — the batch does not know the doctrine skills exist

One grep across all nine skills, for every doctrine and contract owner:

| Owner | Mentions across the whole batch |
|---|---:|
| `alaa-trust-gateway-auth` | 13 |
| `alaa-low-noise` | 6 |
| `alaa-data-layer` | 4 |
| `alaa-prompting-guide` | 3 |
| `alaa-algorithms-data-structures` | 2 |
| `alaa-workflow`, `alaa-services-contract`, `alaa-crockford-base32-codecs` | 1 each |
| **`alaa-reliability-sla`** | **0** |
| **`alaa-testing-strategy`** | **0** |
| **`alaa-system-design`** | **0** |
| **`alaa-security-review`** | **0** |
| **`alaa-observability-soc`** | **0** |
| **`alaa-project-constitution`** | **0** |
| **`alaa-keyset-pagination`** | **0** |
| **`alaa-controlled-ops`** | **0** |
| **`alaa-async-messaging`** | **0** |
| **`alaa-permission-generator`** | **0** |
| **`alaa-minio-object-storage` / `alaa-arvan-object-storage`** | **0** |
| **`tusd-upload-platform`** | **0** |

Per skill: `alaa-frontend-doc-annotations` and `alaa-mono-package` name **no** owner at all; `alaa-ui-ux-design-system`, `alaa-frontend-devops` and `alaa-shaka-player` name only `alaa-low-noise`; `alaa-indexeddb-browser-storage` names two, once each.

This is Batch 2's root cause repeating one batch later, and its consequence is identical: **every skill in this batch has legislated retry policy, test requirements, security rules, metric names and complexity budgets locally, at weaker strength than the owner states them.** The specific instances are in each appendix under "Boundary map (c)". The most consequential are:

- `alaa-frontend-developer/references/40-performance-and-realtime.md:59-62` writes exponential backoff, a delay cap and jitter in its own voice — `alaa-reliability-sla` ground.
- `alaa-vue-typescript-clean-code/references/20-typescript-composition-contract.md:178` — "transient transport/5xx failures **may** retry or degrade" — reliability doctrine at preference strength.
- `alaa-quasar-app-vite-v3/references/75-testing-ci-playbook.md:16` sets the test-layer minimum in its own voice — `alaa-testing-strategy` ground.
- `alaa-ui-ux-design-system/references/85-accessibility-patterns.md:47` is the batch's entire a11y test design and ends in "when tooling exists".
- `alaa-shaka-player` states no retry policy at all for a media stack whose defining failure mode is a segment fetch that did not arrive.

**The rule this produces for Phase 2:** every skill's body gains an explicit disclaimer block naming the owner of each criterion it does not own, and every local statement of an owner's ground is replaced by a routed obligation. Silence is not delegation. This is the single highest-value change available in the batch, and it is available in all nine skills.

### 2.2 The trigger-form finding — the batch is invisible from Claude Code

Across the nine skills, `$alaa-*` appears **197 times** and `/alaa-*` appears **twice**. Both slash-form occurrences are in `alaa-vue-typescript-clean-code` (`SKILL.md:14` and `:221`), and both correctly give the paired form.

| Skill | `$alaa-*` | `/alaa-*` |
|---|---:|---:|
| `alaa-frontend-developer` | 75 | 0 |
| `alaa-quasar-app-vite-v3` | 42 | 0 |
| `alaa-ui-ux-design-system` | 38 | 0 |
| `alaa-indexeddb-browser-storage` | 16 | 0 |
| `alaa-frontend-devops` | 7 | 0 |
| `alaa-shaka-player` | 7 | 0 |
| `alaa-mono-package` | 5 | 0 |
| `alaa-frontend-doc-annotations` | 4 | 0 |
| `alaa-vue-typescript-clean-code` | 3 | 2 |

Batch 5's memory recorded that trigger syntax "fails by absence, not by wrongness" — grep for the absence, not just the wrong form. That holds here in a stronger form: **the `$` form is not wrong, it is half a rule.** Every one of these skills is cross-runtime (each ships `agents/openai.yaml` for Codex and each is installed as a Claude Code skill under `sohrab-skills:`), so every cross-skill call site needs both forms. A Claude Code agent reading `pair with $alaa-frontend-developer` has no invocable token, and this is true at 195 of 197 sites.

The one correct exception, applied consistently across all nine: `agents/openai.yaml` is a Codex-only file and its `$`-only self-reference stays.

### 2.3 The model-pin finding — and the one instance the carry-over does not name

`UPGRADE-CARRYOVER.md` §5 says of this batch only that "`alaa-vue-typescript-clean-code` carries a stale hardcoded model name". That is now the least of it. The surviving pins:

| Location | Content | Severity |
|---|---|---|
| `alaa-shaka-player/assets/config-examples/agents/{ads,analytics,conductor,core,overlay,qa}.toml:1` | `model = "gpt-5.5"` ×6, plus `model_reasoning_effort` on line 2 of each | **Highest in the batch** — these are emitted config files an agent copies into a project the skill can never edit again |
| `alaa-frontend-developer/references/90-upstream-deltas-and-maintenance.md:53,55,56,63,64,65` | a full model-and-effort selection policy naming GPT-5.5 / GPT-5.4 / GPT-5.4-mini | High — a frontend skill legislating model routing |
| `alaa-ui-ux-design-system/SKILL.md:16` | "OpenAI Codex/GPT-5.x agents and Claude (Opus/Sonnet/Fable) agents" | Medium — also materially wrong today, listing Fable as a peer tier |
| `alaa-quasar-app-vite-v3/references/91-agent-authoring-and-dual-runtime.md:3,32` | "GPT-5 / Codex" | Medium — the same line also says "refer to runtime families, not fast-aging model IDs", so the file contradicts itself in one sentence |
| `alaa-vue-typescript-clean-code/references/00-source-map.md:9` | "GPT-5.5 outcome-first skills" | Low — but sits in the file `SKILL.md:50` tells the agent to load on every task |
| `alaa-indexeddb-browser-storage/references/99-sources-and-maintenance.md:32` and `references/full-guide.md:2128` | GPT-5 prompting-guide URL, twice | Low — and it is the direct proof that the `full-guide.md` duplication has already doubled a real defect rather than a hypothetical one |
| `alaa-shaka-player/agents/openai.yaml:3` | `"Shaka 5.1 migration and Quasar player pack"` | A **version** pin in UI metadata, same decay property, no benefit |

`SKILL.md:14` of `alaa-vue-typescript-clean-code` is confirmed clean — the pin the carry-over names was removed in the 2026-07-27 follow-up round and only the `00-source-map.md` occurrence survives. **Correction to the carry-over: the batch's worst model pin is in `alaa-shaka-player`, in a shipped artifact, and the carry-over does not mention it.**

The replacement is the same everywhere: route to `/alaa-prompting-guide` (`$alaa-prompting-guide`) and its `references/50-effort-and-thinking.md`, and describe a lane by the judgment it needs rather than by a tier. For the emitted TOMLs specifically, the ruling is in Appendix I §4(a): **emit no model key and no effort key, and replace them with a prohibition comment naming the owner** — a placeholder string is the worst option available, because TOML accepts it and the runtime rejects it later with an opaque error inside the user's project.

### 2.4 The second-router finding — seven of nine skills route twice

The convention is one router per skill, never two: at ≤8 reference files the router is a table in `SKILL.md` and no standalone topic map exists; at ≥9 the router lives in `references/00-topic-map.md` and `SKILL.md` carries one pointer line. Every row states an observable condition, never a heading mirror.

| Skill | Refs | Required location | Actual | Verdict |
|---|---:|---|---|---|
| `alaa-frontend-developer` | 13 | `references/00-topic-map.md` | topic map **plus three more routers in the body** (`SKILL.md:80-107`, `:68-78`, `:164-173`) | **four routers** |
| `alaa-vue-typescript-clean-code` | 9 | `references/00-topic-map.md` | router is `references/05-topic-map.md`, restated as prose at `SKILL.md:45-61`; `00-source-map.md` is a legitimate provenance ledger occupying the router's filename | **two routers, slots inverted** |
| `alaa-quasar-app-vite-v3` | 30 | `references/00-topic-map.md` | topic map plus a compressed second router at `SKILL.md:45`, plus a search-vocabulary dump duplicating `00-topic-map.md:35-43` | **two routers** |
| `alaa-ui-ux-design-system` | 13 | `references/00-topic-map.md` | topic map, then `SKILL.md:70-95` reproduces it verbatim (1,949 B) and `SKILL.md:97-123` reproduces its cross-topic rules verbatim (2,078 B) | **two routers, 37% of the body** |
| `alaa-frontend-devops` | 5 | body table | body table; `00-source-map.md` is a genuine provenance ledger | **conforms** |
| `alaa-frontend-doc-annotations` | 4 | body table | **two body routers** (`SKILL.md:39-47` and `:82-91`) that disagree with each other; `00-source-map.md` is a genuine ledger | **two routers** |
| `alaa-mono-package` | 5 | body table | body table; `00-source-map.md` is a genuine ledger | **conforms** |
| `alaa-indexeddb-browser-storage` | 14 | `references/00-topic-map.md` | topic map, and `SKILL.md:63-78` restates it | **two routers** |
| `alaa-shaka-player` | 17 | `references/00-topic-map.md` | **no topic map at all**; `references/README.md` is a bare filename list with no condition attached, and `SKILL.md:99-114` is a second list | **no conforming router** |

Two corollaries worth carrying forward. First, `references/00-source-map.md` is a **legitimate non-router artifact** and appears correctly in three skills as a source-provenance ledger — do not delete it on sight, and do not confuse it with the router. Second, the observable-condition test fails much more widely than the location test: in `alaa-vue-typescript-clean-code` five of eight rows are heading mirrors, in `alaa-frontend-doc-annotations` five of six, in `alaa-ui-ux-design-system` and `alaa-frontend-developer` the majority. The rows that pass are worth copying as templates — `alaa-frontend-developer/SKILL.md:133` ("Any UI change that appears 'frontend-only' but is really caused by backend query shape, count cost, or missing aggregation") is the correct shape in the batch.

### 2.5 A fifth finding, mechanical and undocumented: dangling internal pointers

Not one of the eleven defect classes, but the most immediately damaging thing found:

- `alaa-quasar-app-vite-v3/references/31-ssr-pwa-and-security.md:13` and `references/35-platform-modes.md:3` both say "First confirm the app-vite line (`70-…`)". File `70` is the a11y/performance/monorepo guardrails file and contains no line-detection content; the correct target is `80-upstream-deltas-and-live-checks.md`.
- `alaa-quasar-app-vite-v3/references/85-legacy-skill-coverage.md:33-38` routes retired skill names using a **dead numbering scheme** that contradicts its own table twenty lines above, sending six of nine buckets to the wrong file.
- `alaa-ui-ux-design-system/references/70-motion-and-modern-css.md:5` points at `alaa-frontend-developer references/25-modern-css-and-motion.md`, which does not exist.
- `alaa-vue-typescript-clean-code/references/00-source-map.md:7,8,10` cite three paths that do not ship in the package, in the file the body says to load on every task.
- `alaa-quasar-app-vite-v3` carries a **factual contradiction** born of six-fold duplication: `references/10-v2-to-v3-migration.md:51` gives the `sourceFiles` default as `pwaServiceWorker: 'src-pwa/custom-sw'` while `references/11`, `31` and `32` all give `'src-pwa/sw/custom-sw'`. An agent that reads `10` during a migration writes the wrong value and the custom service worker is silently ignored.

All **cross-skill** paths that name their owning skill were verified to resolve, with the one exception above. Batch 4's warning applies and was honoured: the resolver must not require the owning skill inside the same backtick span, because the house convention puts the owner in a separate span.

---

## 3. The ten-criteria table for the whole batch

Per `UPGRADE-CARRYOVER.md` §2, each cell is SATISFIED, FAILS, or NOT-OWNED — and NOT-OWNED is legitimate **only** where the skill actually names the owning skill. Where a skill is silent on a criterion it does not own, that is FAILS, because silence reads as coverage.

Legend: **S** satisfied · **F** fails · **N** not owned *and the owner is named*.

| # | Criterion | fe-dev | vue-ts | quasar | ui-ux | fe-devops | doc-ann | mono | idb | shaka |
|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 1 | Correctness and testability | F | F | F | F | F | F | F | F | F |
| 2 | Failure behavior | F | F | F | F | F | F | F | F | F |
| 3 | Security | F | F | F | F | F | F | F | F | F |
| 4 | Observability | F | F | F | F | F | F | F | F | F |
| 5 | Concurrency and load | **S** | F | **S** | F | F | F | F | F | F |
| 6 | Clean code, SOLID, patterns | F | **S** | **N** | **S** | F | F | F | F | F |
| 7 | Algorithm and data structures | F | F | F | F | F | F | F | F | F |
| 8 | Configurability | F | F | **S** | F | F | F | F | F | F |
| 9 | Speed and debuggability | **S** | F | **S** | **S** | F | F | F | **S** | **S** |
| 10 | Documentation | F | F | F | **S** | F | F | F | **S** | F |
| | **S / N / F** | 2/0/8 | 1/0/9 | 3/1/6 | 3/0/7 | 0/0/10 | 0/0/10 | 0/0/10 | 2/0/8 | 1/0/9 |

**Ninety cells: 12 SATISFIED, 1 NOT-OWNED-and-named, 77 FAILS.**

The single legitimate NOT-OWNED in the entire batch is `alaa-quasar-app-vite-v3` on criterion 6, which names `alaa-vue-typescript-clean-code` at three separate call sites (`SKILL.md:56`, `:62`, `references/00-topic-map.md:47`). Every other cell that could have been a clean delegation is a silence instead. That single cell is the model for the other seventy-six.

Four rows are **uniformly failed across all nine skills**: correctness and testability, failure behaviour, security, and observability. Those four rows are the batch's real deliverable. Criterion 7 is failed nine times as well, but it is the one row where the honest answer in most skills is a routed obligation to `alaa-algorithms-data-structures` plus a small language binding, not a body of new content.

Where the criteria are satisfied, they are satisfied well and the work must be preserved, not rewritten:

- `alaa-quasar-app-vite-v3/references/30-service-worker-excellence.md:34-58` — the waiting-worker contract, the `skipWaiting` chunk-404 hazard, the `controllerchange` reload-loop guard and the kill-switch service worker. This is the best failure-behaviour writing in the batch and it is also the batch's strongest concurrency content.
- `alaa-quasar-app-vite-v3/references/20-v3-config-and-features.md:34-56` — the build-time-versus-runtime environment contract, `clientPrefix`, "`QCLI_*` is PUBLIC; never secret", and the `define`-versus-`defineEnv` stringify semantics. The one SATISFIED configurability cell in the batch.
- `alaa-vue-typescript-clean-code/references/40-patterns-vue-quasar.md:5-45` and `references/30-clean-code-solid-vue.md:109-140` — a symptom→pattern diagnostic with look-alike disambiguation, and five smell families each with a named repair and an explicit "when NOT to fix". This is the assigned owner of per-language design-pattern judgment discharging its duty, and it is why `alaa-design-patterns` correctly does not exist.
- `alaa-ui-ux-design-system/references/55-component-library-and-governance.md:11-24` — closed enum variants mapped to tokens, "never accept raw visual values as props", slots for composition and props for configuration, and "wrap, don't fork: if a wrapper only forwards props with no design decision, delete it".
- `alaa-quasar-app-vite-v3/references/05-authority-and-api-lookup.md` — delegating the entire exact-API surface to the project's own `quasar describe` through a shipped script instead of mirroring it. This is standing preference 1 executed exactly, and it is the pattern other skills in the batch should copy rather than maintaining an atlas by hand.
- `alaa-indexeddb-browser-storage` on documentation, and `alaa-frontend-developer/references/60-browser-debug.md` plus `references/41-lighthouse-and-web-vitals.md` on speed.

---

## 4. Defect classes found, by class

Numbering follows `UPGRADE-CARRYOVER.md` §3. Only classes actually found are listed.

**1 — Stale model pins.** Seven locations across five skills, plus one version pin. Full table in §2.3. Worst instance: six emitted TOML files in `alaa-shaka-player`.

**2 — Trigger syntax.** 195 of 197 cross-skill call sites give one form where two are required. Full table in §2.2. Fails by absence, not by wrongness.

**3 — Duplication between body and references.** Present in eight of nine skills; the two extreme cases are structural rather than stylistic.
- `alaa-indexeddb-browser-storage/references/full-guide.md` is a **mechanical concatenation of the thirteen topic references at 99.75% whitespace-normalized similarity**, eleven of thirteen sections byte-identical, contributing zero unique content, unreachable from any router, and 38.1% of the pack's bytes. It even contains the router's own instruction not to load it. Ruled: retire. Full evidence and the two rejected alternatives in Appendix H §5.
- `alaa-ui-ux-design-system/SKILL.md:70-123` is 4,027 bytes — **37% of its always-loaded body** — reproducing `references/00-topic-map.md:5-51` verbatim.
- `alaa-vue-typescript-clean-code` has 11,769 of 20,628 body bytes duplicating six reference files.
- `alaa-quasar-app-vite-v3` states the v2→v3 delta set six times and it has already drifted into the `sourceFiles` contradiction in §2.5.
- `alaa-frontend-developer/scripts/check-upstream-versions.mjs` is a whitespace variant of `alaa-quasar-app-vite-v3/scripts/check-upstream-versions.mjs`, and its own header comment says it belongs to the other skill.

**4 — Project-specific content in an always-loaded body.** `alaa-vue-typescript-clean-code/SKILL.md:55-59` spends five lines on eight Alaa-repo-private pattern names and `:149` hardcodes a repo-specific file chain. `alaa-frontend-developer/SKILL.md:31,148` hardcodes a dated Quasar version fact already stated in two references, and `:142` carries local MCP browser-profile trivia. `alaa-ui-ux-design-system/SKILL.md:61,119` enumerate repo artefacts and hardcode another skill's reference filename plus a Lighthouse number.

**5 — Long numbered procedures nobody reads in order.** `alaa-quasar-app-vite-v3/references/11-review-and-upgrade-checklist.md` is ~45 unordered checkboxes with no priority, no failure signature and no stopping rule, and `references/10-v2-to-v3-migration.md` has **no failure-class recovery at all** — nothing on `quasar prepare` failing, a blocking App Extension, an SSR build that 500s, or a dirty Capacitor `www`, and a two-sentence rollback. `alaa-frontend-developer/references/30-pwa-sw-and-offline.md:37-79` is a five-step workflow where a failure-class table belongs. In both cases the skill demonstrably knows the right shape — `alaa-quasar-app-vite-v3/references/70-…:53-58` and `alaa-frontend-developer/references/40-…:76-86` are exactly symptom→cause — and simply does not apply it where recovery matters.

**6 — Description with no "do not use for".** Three of nine: `alaa-vue-typescript-clean-code` (has a `## When NOT to use` section in the body, which is not what drives triggering), `alaa-quasar-app-vite-v3` (one-dimensional negative clause that disclaims only "plain Vue/Vite without Quasar CLI"), `alaa-indexeddb-browser-storage`. The best description in the batch is `alaa-ui-ux-design-system/SKILL.md:3`, which carries a real exclusion and should be the model.

**7 — Fragile tooling.** `alaa-indexeddb-browser-storage/scripts/{check_references,validate_skill_pack}.py:5-6` use `Path(__file__).resolve().parents[1]`; both were executed and both exit 0, and the lane judged the pattern acceptable *as invoked* while noting it breaks if the scripts move. The real fragilities are elsewhere: **both** `check-upstream-versions.mjs` scripts use raw `https.get` with **no request timeout** and no proxy handling, so a stalled registry hangs the agent with no diagnostic; and six call sites across two skills invoke scripts by a bare relative path that only resolves when the working directory is the skill root. Neither script has `--help` or a self-test. `alaa-shaka-player/scripts/scaffold.sh` is 675 bytes and is audited in Appendix I §10.

**9 — Unnamed gaps against §2.** Seventy-seven of ninety cells. This is §2.1 and §3 restated as a defect class, and it is the batch's dominant finding.

**10 — Body larger than it needs to be.** `alaa-vue-typescript-clean-code` at 20,628 bytes is the batch's largest body and roughly 12.8 KB of it is duplication plus repo-private detail. `alaa-ui-ux-design-system` at 10,888 bytes carries 4,027 bytes of verbatim router duplication. `alaa-frontend-developer` at 13,146 bytes carries four routers. Note the inverse case: `alaa-mono-package`'s body (7,285 B) is **larger than its entire reference set** (6,251 B), and `alaa-frontend-devops`'s body contains no substantive rule at all — for these two the finding is not size but composition, and the correct remedy under the completeness law is reference growth with a body that does not grow.

**11 — No stated companion boundary.** `alaa-frontend-doc-annotations` and `alaa-mono-package` name no owner whatsoever. `alaa-frontend-developer` is silent on three siblings that route *into* it. `alaa-quasar-app-vite-v3` states its in-batch boundaries well and is silent on every out-of-batch owner, and on `alaa-shaka-player` and `tusd-upload-platform`, which it directly overlaps. `alaa-ui-ux-design-system` has the batch's most explicit boundary statement and **contradicts itself**: `SKILL.md:32` assigns `app.scss` and transition props to `alaa-quasar-app-vite-v3`, then `references/20-…:67` and `references/70-…:71` legislate both.

**Not found:** class 8 (`__pycache__`) anywhere in the batch.

---

## 5. Ownership boundaries settled

These bind both sides and are the input Phase 2 writes from.

| Skill | Owns | Explicitly does not own — and names the owner |
|---|---|---|
| `alaa-frontend-developer` | SSR/hydration determinism for the app family; the frontend-side auth/session **posture** (BFF vs token-mediating vs cookie-bridge vs PKCE) and which one this repo is on; PWA/SW **policy** (what may change and what must not); the canonical Lighthouse/Web-Vitals scoring model; the browser-automation opt-in gate and browser-debug evidence discipline; the client-side consequences of API shape; which frontend companion to load | SW **mechanism** (`alaa-quasar-app-vite-v3`); Vue/TS code shape and pattern judgment (`alaa-vue-typescript-clean-code`); browser storage (`alaa-indexeddb-browser-storage`); every doctrine owner in §2.1; the cursor contract (`alaa-keyset-pagination`); identifier parity (`alaa-crockford-base32-codecs`, **and its `scripts/codec-conformance.sh` is run, not reasoned about**) |
| `alaa-vue-typescript-clean-code` | **Design-pattern judgment for Vue/TS** — the assigned owner, which is why no `alaa-design-patterns` exists; Vue style-guide Priority A–D as gates; the TypeScript/Composition contract; composable shape and teardown; size and complexity budgets with named split seams; the code-smell vocabulary; the Alaa observed-antipattern ledger | SSR guard constants, PWA and browser-API mechanics (`alaa-quasar-app-vite-v3`); SSR auth/session and QA planning (`alaa-frontend-developer`); design tokens and motion (`alaa-ui-ux-design-system`); every doctrine owner in §2.1; comment and annotation **shape** (`alaa-frontend-doc-annotations` — see §5.1) |
| `alaa-quasar-app-vite-v3` | Everything reached through the Quasar CLI: the app-vite v2/v3 line and its detection, `quasar.config`, boot files, the env/`clientPrefix` contract, all platform modes, service-worker mechanics, the component/directive/API atlases, and upstream freshness | Vue/TS code quality (`alaa-vue-typescript-clean-code`, already named at three sites); visual design (`alaa-ui-ux-design-system`); IndexedDB semantics (`alaa-indexeddb-browser-storage`); CI **expression** (`alaa-gitlab-ci-cd`, Batch 7) while keeping the gates; media playback (`alaa-shaka-player`); upload transport (`tusd-upload-platform`); every doctrine owner in §2.1 |
| `alaa-ui-ux-design-system` | The visual and UX decision layer: tokens and theming, typography and colour, the designed component states, layout and IA, UX writing, motion language, icons and imagery, a11y patterns, and the component-API **shape** as a design decision; **and RTL/Persian as a first-class constraint** (new — see §6) | Quasar component mechanics (`alaa-quasar-app-vite-v3`); Vue/TS code (`alaa-vue-typescript-clean-code`); performance plumbing (`alaa-frontend-developer`); every doctrine owner in §2.1 |
| `alaa-frontend-devops` | **The frontend delivery gate register** — for each gate, the predicate it asserts, the command that evaluates it, and the artifact it inspects; build provenance and commit→bundle traceability; the artifact contract; runtime-versus-build-time configuration for a static bundle; rollback | **Writes no provider YAML and no Dockerfile.** `alaa-gitlab-ci-cd` owns how a gate is expressed on a runner and decides no gate; `alaa-docker-production` owns image and Compose expression and decides no gate; `alaa-haproxy` owns cache and routing directives and decides no policy; the object-storage skills own a CDN origin bucket |
| `alaa-frontend-doc-annotations` | The documentation-only diff **mode** contract; the closed `NOTE:` prefix taxonomy; JSDoc/TSDoc block shape for Vue surfaces; **the staleness contract for a comment asserting a security, auth or SSR assumption** (new, and unowned anywhere in the fleet today); the no-community-citation-inside-code rule | Comment-versus-extract and clean code (`alaa-vue-typescript-clean-code`); the SSR and auth **facts** a note may assert (`alaa-frontend-developer`, `alaa-quasar-app-vite-v3`, `alaa-trust-gateway-auth`); Persian-language deliverables (`alaa-repo-docs`) |
| `alaa-mono-package` | Everything that determines **what enters the bundling graph** — a package's declared exports and conditions, its peer contract, its specifiers, and whether its CSS and assets are reachable from an entry; workspace protocols and topological build order | Everything that happens to the graph's output after `build` exits (`alaa-frontend-devops`); Vue/TS code (`alaa-vue-typescript-clean-code`); PHP/Composer release gates (`alaa-controlled-ops`, as the analogue to mirror rather than restate) |
| `alaa-indexeddb-browser-storage` | Browser origin storage as a discipline: storage-API selection, capability tiers, quota/persistence/eviction, schema versioning and multi-tab upgrade safety, transaction/index/cursor cost, client-side data classification, the browser outbox and offline cache patterns, **and the service-worker-versus-tab concurrent-write intersection** (newly assigned) | Retry/backoff/timeout doctrine (`alaa-reliability-sla`); the server-side outbox surface and row-state vocabulary (`alaa-async-messaging`); the bitmap contract and decoder (`alaa-permission-generator`); whether a cached value carries trust (`alaa-trust-gateway-auth`); identifier generation (`alaa-crockford-base32-codecs`); SW context and Cache API (`alaa-quasar-app-vite-v3`) |
| `alaa-shaka-player` | The Shaka Player binding for Quasar: playback architecture, HLS/DASH specifics, the ABR and track model, the vendor error taxonomy **mapped onto** reliability doctrine, DRM and licence handling, the upstream watchlist and migration record, and the player's module seams as safe parallel-work boundaries | **Multi-agent orchestration** (`alaa-cc-orchestrator`, `alaa-codex-orchestrator`) — the current pack is retired; component and store shape (`alaa-vue-typescript-clean-code`); retry doctrine (`alaa-reliability-sla`); telemetry **names** (`alaa-services-contract`) and the WA pipeline schema; the media URL's read grant (`alaa-minio-object-storage` / `alaa-arvan-object-storage`) and its trust property (`alaa-trust-gateway-auth`); installation (`install-skills.md`) |

### 5.1 Four seams settled with a deciding test

Each is written as a one-sentence test in the same style as Batch 2's settled PHP test, so a future agent can apply it rather than re-litigate it.

**Design system versus Quasar mechanics.** *A rule that would still hold if the component library were replaced belongs to `alaa-ui-ux-design-system`; a rule that names a Quasar prop, plugin, directive or config key belongs to `alaa-quasar-app-vite-v3`.* This resolves the live contradiction at `alaa-ui-ux-design-system/SKILL.md:32` versus its own `references/20-…:67` and `references/70-…:71`: the token feeding `app.scss` is a design decision, the `setCssVar` call and the `transition-show` prop name are Quasar mechanics.

**Clean code versus annotations.** *A rule whose violation can be caught by compiling, type-checking or running the code belongs to `alaa-vue-typescript-clean-code`; a rule whose violation is visible only by reading a comment against the code it claims to describe — in a diff whose build output must be byte-identical before and after — belongs to `alaa-frontend-doc-annotations`.* This partitions the disputed cases correctly: "no `any`" is caught by `tsc` and stays with clean code; "comment why, not what" is caught by nobody and **moves out of** `alaa-vue-typescript-clean-code/references/30-clean-code-solid-vue.md:101`; "a `SECURITY NOTE:` must still be true" is the annotation skill's alone.

**Package versus delivery.** *`alaa-mono-package` owns whether a package asset is in the graph; `alaa-frontend-devops` owns whether the graph's output lands where the deployment serves it.* Exactly one rule straddles this seam — package assets landing in the final client asset output — and it is currently stated in four places across four skills. One rule is a seam, not a shared domain: each skill states its half and routes the other by skill name plus file path.

**Stack versus platform, for Batch 7.** The sentence Phase 2 writes into `alaa-frontend-devops`, carrying Batch 2's settled boundary forward to the frontend: *`alaa-frontend-devops` owns the frontend delivery gate register — for each gate, the predicate it asserts, the command that evaluates it, and the artifact it inspects — and writes no provider YAML and no Dockerfile.* The line-by-line disposition of `references/20-ci-docker-and-cache.md` is in Appendix F §A and must be executed as written, because Batch 7 will consume it and the two batches must never decide this independently.

---

## 6. The section 4 candidate skills

`UPGRADE-CARRYOVER.md` §4 lists five candidates. All five now exist except one, and the question for this batch is whether anything in the frontend domain changes that. Each paragraph below is grounded in what the lanes read, not in what the names suggest.

**`alaa-design-patterns` — do not build it, and this batch is the strongest evidence yet.** Batch 2 settled this and the frontend confirms it from the other side. `alaa-vue-typescript-clean-code/references/40-patterns-vue-quasar.md` is 24,645 bytes of genuinely good pattern judgment: a 26-row symptom→pattern diagnostic, a look-alike disambiguation table, twenty-three patterns each with its Vue form and its anti-uses, and a "confirming question" per row. That is criterion 6 SATISFIED and it is the only SATISFIED criterion-6 cell in the batch that is not a delegation. A central pattern skill would become a fourth claimant on ground that Go, PHP and Vue already hold cleanly, and it would have to be worse than this file to justify existing. The file's real defect is that it is one 24 KB reference where the completeness law prefers several smaller ones behind sharp router rows — a split, not a new skill.

**`alaa-algorithms-data-structures` — exists, and this batch is its largest unconnected consumer.** It is named exactly twice in 725 KB, both times in `alaa-vue-typescript-clean-code` and both times only for the N+1 case (`SKILL.md:221`). Criterion 7 fails in all nine skills, and the reason is uniform: the frontend has real complexity decisions — the row count at which virtualization becomes mandatory, the per-render computed cost, the DOM node ceiling, the IndexedDB index and cursor cost, the precache size cap, the theme matrix that is combinatorial in light × dark × three density tiers × LTR/RTL × `prefers-contrast` — and not one of them carries a stated budget. The gap is a missing **binding** in nine skills, not a missing skill. Note the one place the doctrine is genuinely applicable in its own terms: `alaa-indexeddb-browser-storage` on index design, key ranges and cursor cost, where a complexity budget is literally the right instrument.

**`alaa-testing-strategy` — exists, and is named zero times in the batch.** Criterion 1 fails in all nine skills, and the failures are the same shape everywhere: "lint and relevant tests if available" (`alaa-frontend-developer/references/50-…:27`), "has tests **or is simple enough to verify**" (`alaa-vue-typescript-clean-code/references/60-…:28`), "automated scan **when tooling exists**" (`alaa-ui-ux-design-system/references/85-…:47`), "run the lightest meaningful build or pipeline check" (`alaa-frontend-devops/references/40-…:7`). Each is a self-granted exception that voids the requirement for exactly the code that most needs it. The six proof levels (1 static, 2 unit, 3 parity, 4 local smoke, 5 in-runtime, 6 live dependency) are the vocabulary every one of these should be expressed in, and none of them is. Again: a missing binding, in nine skills.

**`alaa-reliability-sla` — exists, is named zero times, and is legislated against in five skills.** Criterion 2 fails in all nine. The instances are catalogued in §2.1. The frontend translation of the criterion is real and specific — a service-worker update that fails, an SSR render that 500s, an API that is unreachable, a segment fetch that times out mid-lecture, a `QuotaExceededError`, a deploy that half-propagates — and each skill has one of these and states no policy for it. `alaa-quasar-app-vite-v3` is the exception on one axis only (the service-worker lifecycle, which it handles better than anything else in the batch) and fails on every other.

**`alaa-system-design` — exists, is named zero times, and is the one candidate this batch does not need.** No lane found a frontend decision that required pre-implementation design ownership; the design decisions the batch actually faces are visual (owned by `alaa-ui-ux-design-system`) or structural-within-a-file (owned by `alaa-vue-typescript-clean-code`). Recording it here so a later wave does not re-ask.

---

## 7. New skill decision

**No new skill is required for Batch 6.** All nine lanes were asked independently to name a gap that no existing skill could own without violating its own boundary, and all nine returned "none". That is the recommended outcome and it is reported as such.

Five candidates were tested and rejected, each with the reason, so a later wave does not re-propose them:

1. **A browser-client telemetry emission contract** — what a frontend may emit, over `sendBeacon` versus `fetch(keepalive)`, at what sampling rate, with what PII exclusion, and how it degrades when the collector is unreachable. Genuinely unowned today: `alaa-services-contract` owns names not transports, `alaa-observability-soc` owns levels not client emission, and `alaa-frontend-developer` owns Web-Vitals *scoring*, which is measurement rather than a production emission path. **But it is reference-sized, not skill-sized.** It becomes `references/47-frontend-observability.md` in `alaa-frontend-developer` and `references/36-client-observability-contract.md` in `alaa-quasar-app-vite-v3`, each taking every name from `alaa-services-contract` and every requirement level from `alaa-observability-soc`. A new skill would add a seventh routing surface to a pack that already has six.
2. **A cross-language user-input normalization contract with a conformance harness** — the strongest candidate, and the closest to warranting a skill, because the structural precedent already exists in `alaa-crockford-base32-codecs` (a contract, a canonical implementation per language, and `scripts/codec-conformance.sh` proving parity). But the settled phone-normalisation rule and its 80-case corpus already live in `alaa-bale-provider` and `alaa-sms-provider-mediana`, and the value that must be byte-identical on both sides of the wire is a **value**, which `alaa-services-contract` owns. Resolution in §8, item 1: assign the owner, do not build a skill.
3. **A browser media-stack error taxonomy.** Looks unowned because nothing in the fleet names `shaka.util.Error`. Mapping a vendor's error categories onto reliability doctrine is precisely what a vendor skill is for; `alaa-shaka-player` owns the binding and cites `alaa-reliability-sla`.
4. **Build-time-to-runtime configuration for an immutable bundle** and **client-side supply chain (SRI, CSP, third-party script provenance)**. Both are properties of the artifact and of how it is served, which is `alaa-frontend-devops`'s ground once it has one. They become `references/15-build-time-vs-runtime-config.md` and `references/35-client-bundle-security.md`.
5. **A service worker and a tab writing the same IndexedDB concurrently.** An assignment failure, not an ownership vacuum: the SW context is `alaa-quasar-app-vite-v3`'s and the IndexedDB semantics are `alaa-indexeddb-browser-storage`'s, and today neither addresses the intersection. It becomes `references/41-multitab-versionchange-and-locks.md` in the storage skill with a reciprocal path-bearing pointer from the Quasar skill.

**One existing skill's right to exist was tested and upheld.** `alaa-frontend-doc-annotations` is 8,082 bytes of largely unenforceable preference and duplicates six comment rules that `alaa-vue-typescript-clean-code` already states better, so merging it was the live alternative. It survives on three grounds, set out in full in Appendix G §10: the two skills hold **contradictory mandates** — `alaa-vue-typescript-clean-code/SKILL.md:10` requires repairing violations in scope, while a documentation-only pass must forbid repair, and a merged skill could hold both only through a self-granted exception, which is itself a named defect class; the clean-code skill's four operating modes have no room for a fifth without body growth the completeness law forbids; and there is real unowned ground — **an annotation asserting a security or authorization assumption, and its staleness**, which no skill in the fleet owns and which has already shipped into `client` as an unprotected comment on the permission-bitmap decode site. The ruling is KEEP AND EXPAND, with the explicit condition that if Phase 2 keeps the skill without expanding it, the correct ruling reverses to MERGE.

---

## 8. Out of scope — items for the owner

These require a decision or an edit outside Batch 6 and were deliberately not made.

1. **Persian and Arabic text normalization has no owner, and it is a value, not a rule.** Arabic ي/ك versus Persian ی/ک, Arabic-Indic ٤ versus Persian ۴, and ZWNJ variants mean two strings that render identically do not compare, sort, index or deduplicate as equal. Three skills touch a face of this and none settles it: `alaa-ui-ux-design-system/references/35-…:27` requires correct ZWNJ in displayed copy, `references/30-…:33` picks a display digit system by `font-feature-settings` (which leaves the DOM value unchanged), and `alaa-data-layer` owns storage. The normalization form must be byte-identical on both sides of the wire, which makes it `alaa-services-contract` ground. **Recommendation: name `alaa-services-contract` the owner of the normalization form — one named Unicode form plus the character-folding table — and have the frontend skills cite it.** This is adjacent to the already-settled phone-separator rule (separators matched by Unicode category `{Cf, Zs, Zl, Zp, Pd}` plus `isspace()` plus the literal set `()._/`, never by an enumerated list) and should be settled in the same pass.
2. **Two in-batch skills must gain reciprocal pointers from skills outside the batch**, and Phase 2 will not write them: `alaa-async-messaging` should name `alaa-indexeddb-browser-storage` as the browser-side outbox owner so the two row-state vocabularies are reconciled rather than duplicated, and `alaa-permission-generator` should name the frontend as a consumer of its canonical TypeScript decoder.
3. **`alaa-gitlab-ci-cd` and `alaa-docker-production` (Batch 7) will inherit the disposition in Appendix F §A.** The carry-over already forbids running Batches 6 and 7 concurrently; this is the concrete reason. Batch 7 must be given Appendix F §A as an input.
4. **TypeScript 7 (the native compiler) reached GA in early July 2026.** `alaa-vue-typescript-clean-code/references/20-…:189-191` describes it as a future line, and — more consequentially — `references/60-…:77` prescribes `npx vue-tsc --noEmit` with no note on `vue-tsc`/tsgo compatibility. That is now the live typecheck question for every Quasar repository on the fleet, and it is bigger than a skill edit.
5. **`alaa-shaka-player`'s analytics templates and the WA pipeline have never been reconciled.** `references/ANALYTICS_WATCHTIME.md` and `assets/templates/services/AnalyticsTracker.ts` invent an event shape; `wa_raw.events_raw` and `wa_raw.watch_segments_raw` exist with a settled schema and two counting caveats. Phase 2 will make the skill *request* names from `alaa-services-contract` rather than define them, but whether the existing template shape should be migrated to the WA schema is a product decision.
6. **Two live `client` defects are named in this analysis and are not this batch's to fix**: the profile-completion `contact.phone` field with no `maxlength` whose submit path folds digits without stripping separators, and the permission-bitmap decode comment that documents a security assumption with no verification date and no mechanism to detect its staleness.
7. **A repository-wide question this batch raises but cannot settle:** six of nine skills would benefit from a shipped deterministic checker and only three ship any script at all. Batch 8's sweep should count checkers per skill alongside its link check.

---

## 9. Phase 2 lane plan

Nine writing lanes, each on the escalated implementer, under the named criterion "authoring an artifact whose deliverable is judgment itself". One agent per skill; `alaa-frontend-devops` and `alaa-mono-package` share a lane because they share a seam and a ruling.

**Ordering.** Three lanes must land before the six that depend on them, because they settle a boundary the others cite:

1. **Wave 1 (settles boundaries):** `alaa-vue-typescript-clean-code` (owns pattern judgment and code shape, cited by five siblings), `alaa-frontend-devops` + `alaa-mono-package` (settles the stack-versus-platform ruling Batch 7 inherits).
2. **Wave 2 (independent, dispatched together):** `alaa-quasar-app-vite-v3`, `alaa-ui-ux-design-system`, `alaa-indexeddb-browser-storage`, `alaa-shaka-player`, `alaa-frontend-doc-annotations`.
3. **Wave 3 (consumes all of the above):** `alaa-frontend-developer`, because it is the batch's routing hub and three siblings route into it; its companion table must reflect what the other eight actually became.

**Body budgets**, summed from the target sections in each appendix's rewrite brief and then increased 15% for the `/name` + `$name` duplication the conventions require. The completeness law governs: the body must not grow net of the frontmatter description, references must cover everything, and coverage is bought with routing rather than omission.

| Skill | Body today | Body budget | References today | References after |
|---|---:|---:|---:|---|
| `alaa-frontend-developer` | 13,146 | **≤ 9,600** | 63,739 | grows — six new capability files |
| `alaa-vue-typescript-clean-code` | 20,628 | **≤ 9,800** | 66,816 | ~85,000 — four new binding files, `40-` split into four |
| `alaa-quasar-app-vite-v3` | 6,716 | **≤ 6,700** | 142,129 | net flat — merges offset additions |
| `alaa-ui-ux-design-system` | 10,888 | **≤ 6,900** | 62,124 | grows — RTL/Persian, permission-affordance, states |
| `alaa-frontend-devops` | 3,956 | **≤ 4,000** | 8,677 | grows substantially — the skill is under-covered |
| `alaa-frontend-doc-annotations` | 2,619 | **≤ 2,900** | 4,869 | ~11,000 — four new files |
| `alaa-mono-package` | 7,285 | **≤ 4,200** | 6,251 | grows substantially — body content moves down |
| `alaa-indexeddb-browser-storage` | 8,883 | **≤ 8,900** | 150,450 | ~78,000 — `full-guide.md` retires |
| `alaa-shaka-player` | 10,715 | **≤ 8,000** | 33,895 | grows — failure taxonomy, security, telemetry |

**Retirements to `_to_delete/20260728-batch6/`** (the mount forbids `unlink`; nothing is deleted, and every destination is listed after the move because a lane's own "moved" report is not evidence):

- `alaa-indexeddb-browser-storage/references/full-guide.md` — 74,929 B, 99.75% duplicate, unreachable from any router. The reproduction command (`cat references/[0-9]*.md`) is recorded in `references/99-sources-and-maintenance.md` in its place.
- `alaa-shaka-player/prompts/MULTI_AGENT_PROMPT.md`, `references/MULTI_AGENT_SETUP.md`, all seven files under `assets/config-examples/`, and `INSTALL.md` — competing orchestration machinery and a third statement of an install policy that `install-skills.md` owns authoritatively.
- `alaa-shaka-player/references/README.md` — a bare filename list with no condition attached to any row; replaced by `references/00-topic-map.md`, not converted into it.
- `alaa-frontend-developer/scripts/check-upstream-versions.mjs` — duplicate of the Quasar skill's copy, which is fixed once (timeout, `--help`, `--self-test`) and routed to.
- `alaa-frontend-developer/references/80-legacy-skill-coverage.md` — maps ten skill names nothing in the fleet references; its search aliases fold into the topic map.
- `alaa-vue-typescript-clean-code/references/40-patterns-vue-quasar.md` — split into four files, nothing lost.

**Renames** (`alaa-shaka-player` only): seventeen ALL_CAPS reference files to numbered lowercase, plus a new `references/00-topic-map.md`. A grep across all of `skills/sohrab/` returns **zero** inbound paths from outside the skill, so the cost is ~20 internal pointer edits in files Phase 2 rewrites anyway. `alaa-vue-typescript-clean-code` swaps two slots: `05-topic-map.md` → `references/00-topic-map.md` and `00-source-map.md` → `references/05-sources-and-freshness.md`, matching the fleet convention where `00-` is the router and `05-` is the provenance ledger.

**Deterministic checks to ship.** Six of nine skills currently ship no script, and in this batch that is not a missing nicety — an annotation rule, a design rule or a delivery rule with no tool that reports a violation is a preference, not a rule. Each new checker must have `--help`, a `--self-test`, and documented exit codes where a "could not run" state is distinct from "clean", so CI can never mistake an unparsed file for a passing one. The specific checks, their assertions and what each would find on `client` today are in each appendix's tooling section.

**Live research required before Phase 2 ships a claim.** Each appendix §7 or §8 lists its version and browser-API claims graded as verified-from-files, needs-web-research, or not-verifiable. The largest research surfaces are `alaa-indexeddb-browser-storage` (every quota formula, eviction rule, Safari/ITP behaviour, `navigator.storage.persist()` behaviour and `Web Locks`/`BroadcastChannel` support claim), `alaa-shaka-player` (every version, API name, config key, error code and DRM support claim, including whether the 5.0.8→5.1.11 migration record still describes current versions), and `alaa-frontend-developer` (Lighthouse metric weights and audit IDs, CrUX thresholds, and several browser-API availability claims with no Baseline tier stated). Provenance discipline applies: a source URL where known, `read: unverified as of <date>` where the read date is genuinely unknown, and "not documented" means searched-and-not-found and is not proof of absence.

---

---

# Owner decisions — 2026-07-28, after the Phase 1 briefing

These override the Phase 1 synthesis wherever they differ. They are the binding input for Phase 2.

## D1 — `alaa-shaka-player` is one of the most important skills we have

The Phase 1 lane read the skill as teaching material for a subsystem of uncertain future. That reading is wrong. The owner's ruling:

> The player is very important and sensitive. This skill is to teach an agent to work with **every dimension, capability and feature of Shaka Player** — from the basics (subtitles, audio and video playback, bitrate, event tracking, multiple bitrate and multiple language, VAST, ads, analytics, playback speed) through skin and template work, to **in-app download, DRM, and combining those with the browser's IndexedDB**, and on to the advanced and professional material: implementation notes, handling unstable networks, switching source, adaptive bitrate, live. On the latest version, teaching the agent best practices.
> What matters is that it **routes well**, so the agent can learn and use exactly what it needs, fast, with code snippets and best practices.
> In the `client` project it is used at minimum on the content-show page and on news, and over time it will play a prominent and effective role in all of our projects.

Consequences that bind Phase 2:

- The skill is rebuilt as a **complete capability atlas with a sharp router**, not trimmed. The completeness law applies at full strength: if a Shaka capability is used tomorrow, the skill already has it and the agent finds it in one hop.
- Every capability area named above gets its own reference file with a router row stating an observable condition, and **each carries working code snippets**, not prose descriptions of code.
- The facts come from **live upstream research at the current version**, with provenance discipline: a source URL where known, `read: <ISO date>`, and "not documented" meaning searched-and-not-found rather than proof of absence.
- The `vod` deprecation does not reduce the skill's scope. `client` content-show and news are live consumers now.
- **In-app download is a first-class seam with `alaa-indexeddb-browser-storage`**, not an aside — see D5.
- The Phase 1 rulings on the model pins in the emitted TOMLs, the retirement of the competing multi-agent pack, the ALL_CAPS rename plus a real `references/00-topic-map.md`, and the retirement of `INSTALL.md` all stand. They are about structure, not scope, and they are what makes the expansion routable.

## D2 — Digit and text normalization becomes a new skill, and the rule is fleet-wide

Approved, and widened. The owner's ruling:

> All Persian, Arabic, Hindi and other non-ASCII digits must be converted to English digits **wherever we have input**. The conversion happens when the form is submitted — an OTP the user typed, a mobile number, the description of a content item or a news item with numbers in its text. Everything must be normalized to English digits before being sent to the server. **All backend services must also perform this normalization completely, in middleware.** File an RFC in every service that needs one.

So the contract has two enforcement points and they must agree byte for byte: the browser normalizes at submit, and every backend service normalizes in middleware. This is the same shape as the settled permission-bitmap and Crockford-codec contracts, and it gets the same machinery — one contract, a canonical implementation per language, one shared corpus, and a harness that drives every implementation over that corpus and fails on any disagreement. A document asserting parity is not evidence of it.

The skill is **new**, and is the fleet's single owner of the normalization form. The frontend skills cite it; they do not restate it. The existing 80-case phone corpus in `alaa-bale-provider/scripts/phone-conformance-corpus.json` and `alaa-sms-provider-mediana/scripts/phone-conformance-corpus.json` is prior art on separator folding and must be reconciled, not duplicated — those two skills keep phone-number canonicalisation, the new skill owns digit folding and text normalization generally.

This supersedes Phase 1 §7 candidate 2 and §8 item 1: the answer is a skill, not an owner assignment to `alaa-services-contract`.

## D3 — TypeScript 6 is the line; TypeScript 7 is not adopted

The owner's ruling:

> We are currently working with TypeScript 6 on Quasar + Vue + app-vite v3. Quasar has not officially said it supports TypeScript 7, so we must not mislead the agents. In its place, teach TypeScript professionally — the design patterns, the clean-code principles, the best practices and the bad practices, completely, with the surrounding detail the agent needs, and make it well routed and recognisable.

So Phase 1's finding that `references/20-typescript-composition-contract.md:189-191` is stale is **corrected in the opposite direction from what that lane proposed**. The skill states: TypeScript 6 is the fleet line; TypeScript 7 and the native compiler are **not adopted**, and the stated reason is that Quasar has not declared support. `vue-tsc --noEmit` stays as written. No tsgo guidance is written anywhere. The budget that would have gone to a version discussion goes instead into depth on TypeScript itself.

## D4 — The growth the completeness law requires is authorised

`alaa-frontend-devops`, `alaa-mono-package`, `alaa-frontend-doc-annotations` and `alaa-shaka-player` grow their reference sets substantially. Every body stays within the budget in §9, net of the frontmatter description.

## D5 — `alaa-indexeddb-browser-storage` is in scope at full depth

The owner's ruling:

> This skill must be fully reviewed in this batch, because the subject is the browser's own IndexedDB, and it is going to be very useful in caching requests, in the browser-side outbox, in in-app download on the Shaka Player side and elsewhere — we will use its capabilities to deliver an outstanding user experience.

So the three consumers are named and each is a seam this skill must state:
1. **Request caching** — with `alaa-quasar-app-vite-v3` owning the service-worker and Cache API side.
2. **The browser-side outbox** — with `alaa-async-messaging` owning the server-side surface and row-state vocabulary, reconciled rather than duplicated.
3. **In-app download for Shaka Player** — the offline media store. `alaa-shaka-player` owns what the player stores and how it is fetched and licensed; this skill owns the storage substrate, its quota, eviction and persistence semantics, and what happens when a stored asset is evicted mid-session. Neither restates the other.

Phase 1's assignment of the service-worker-versus-tab concurrent-write intersection to this skill stands and becomes more load-bearing, because an in-app download runs while tabs are open.

## D6 — Two out-of-batch skills are edited in this batch, narrowly

Authorised by name: `alaa-async-messaging` gains a pointer naming `alaa-indexeddb-browser-storage` as the browser-side outbox owner, and `alaa-permission-generator` gains a pointer naming the frontend as a consumer of its canonical TypeScript decoder. Nothing else in either skill is touched.

## D7 — RFCs are filed, not just reported

A complete RFC goes into the `client` repository for the two live defects — the profile-completion `contact.phone` field with no `maxlength` whose submit path folds digits without stripping separators, and the permission-bitmap decode comment that documents a security assumption with no verification date and no staleness detection. RFCs also go into every backend service that must gain the digit-normalization middleware under D2. Each is written for a zero-context reader: what is true, why it matters, the options, and what it would take to decide.

## D8 — The Batch 7 and Batch 8 handoffs are written into `UPGRADE-CARRYOVER.md`

Authorised, and it overrides the standing rule that this batch does not edit that file. The stack-versus-platform disposition in Appendix F §A, and the Batch 8 items — the per-skill checker count alongside the link check, and the rest — are recorded there so the agent that reaches those batches reads them and acts on them.

---

## D9 — the Devanagari case, settled 2026-07-28 after the batch closed

D2 left one measurement unresolved and it is now closed. Running the phone grammar over the `typed` output of all 80 phone-corpus inputs gave 49 accepted / 31 rejected against the recorded 48 / 32; the single divergence was `०९१२३८३००००`, Devanagari digits, which the phone corpus recorded as rejected because its fold covered two digit families only.

**The owner approved option (b): keep the wide fold and re-ratify the case as rendered.** It landed as one commit touching both provider skills and both copies of the phone corpus. `corpus_sha256` moved from `7a4250cf64e730d51ef92512975e864cbcfa5da919f658e0f974c50e8d54b548` to `80dcb3723e83d848236ab0cbfbfc62447eec524c62a434737d85682aa653d7dc`, and `corpus_version` from 3 to 4.

The deciding evidence was that `client/packages/digit-normalizer` already folds every `Nd` family, so the recorded rejection described a path no browser user could reach — the backend was already receiving `09123830000`. One half of the providers' original justification survives and is now stated explicitly in both skills: **superscripts are category `No`, not `Nd`**, this contract folds `Nd` alone, and the superscript case is still recorded as rejected and still rejected by both validators. A later proposal to widen the fold to `\p{N}` or any `isdigit()`-style predicate would break that case and must be refused.

Both providers' validators were changed from an enumerated two-family table to a category test — the enumerated list being a defect class rather than a fix is the same rule this batch wrote into four other skills. Both harnesses pass; the Bale harness verifies the digest inside its own self-test. Anywhere in this document that still quotes `7a4250cf…` is a record of what was true during Phase 1 and is left unedited on purpose.

---

## Appendices — the nine lane reports

Each appendix is the lane's report verbatim. Where an appendix and this synthesis differ on a ruling, this synthesis governs and the difference is noted in the section above; where they differ on a file, a line, or a byte count, the appendix governs.


---

## Appendix A — `alaa-frontend-developer`

### 1. What this skill is today

`alaa-frontend-developer` is the fleet's default *frontend engineering policy and routing hub* for Vue 3 + Quasar + Vite apps: it holds SSR/hydration determinism rules, SSR auth/session patterns, PWA/SW policy, the canonical Lighthouse/Web-Vitals playbook, frontend-facing API shaping, QA planning, and a browser-debug decision flow. Its register is **senior-engineer checklist with routing**, not production discipline — it reads as a well-organised handbook of preferences (`prefer` ×32, `avoid` ×14, `unless` ×11) rather than an execution contract with gates. Shape: `SKILL.md` 13,522 bytes (13,146 net of the frontmatter block), 13 reference files totalling 63,739 bytes, one 3,751-byte script, one 270-byte `agents/openai.yaml`. Siblings route *into* it (`alaa-quasar-app-vite-v3/SKILL.md:62`, `alaa-ui-ux-design-system/SKILL.md:31`, `alaa-indexeddb-browser-storage/SKILL.md:99`), so its silences propagate across Batch 6.

### 2. Ten-criteria verdict

| Criterion | Verdict | Evidence |
|---|---|---|
| 1. Correctness & testability | **FAILS** | `references/50-qa-and-verification.md:27` "lint and relevant tests if available" is the entire test requirement; no test-first rule, no layer/double/flake guidance, `alaa-testing-strategy` appears 0× in the whole skill — silence, not a disclaimer. |
| 2. Failure behavior | **FAILS** | Retry/backoff legislated in its own voice at `references/40-performance-and-realtime.md:59-62` and `references/21-ssr-auth-and-session-patterns.md:118-123`; zero occurrences of `timeout` as a policy (only `setTimeout(0)` at `41:46`), zero `idempot*`, no circuit breaking, no degraded-dependency UI contract; `alaa-reliability-sla` named 0×. |
| 3. Security | **FAILS** | `references/21-…:87-115` is genuinely good on token storage/PKCE, and `21:85` names `$alaa-trust-gateway-auth` for the trust boundary — but zero occurrences of `v-html`, `XSS`, `sanitiz*`, `CSP`, `postMessage` origin, tenant isolation, or the rule that the permission bitmap is a UI hint and not an authorization decision; `alaa-security-review` named 0×. |
| 4. Observability | **FAILS** | `references/40-…:70-74` is literally "add logging": "log connect, disconnect, and reconnect attempts at the right environment level". No log fields, no metric names, no `traceparent` propagation to the gateway, no RUM/error-reporting contract; `alaa-observability-soc` and `alaa-services-contract` named 0×. |
| 5. Concurrency & load | **SATISFIED** | Single-flight refresh `references/21-…:118-124` + code at `21:127-151`; abort-previous-fetch `references/20-vue-js-ssr-patterns.md:97`; N+1/batch/debounce `references/45-api-and-data-shaping.md:111-118`; backoff + jitter `40:59-61`. Gap noted: no cap on parallel in-flight requests and no WS/SSE message backpressure. |
| 6. Clean code, SOLID, patterns | **FAILS** | `references/20-…:102-105` ("prefer small pure functions", "avoid module-level side effects") is the whole of it; no SOLID, no component decomposition, no patterns. `alaa-vue-typescript-clean-code` — which `alaa-quasar-app-vite-v3/SKILL.md:62` calls "mandatory Vue/TS" — is named **0×** here. Silence, so FAILS not NOT-OWNED. |
| 7. Algorithm & data-structure choice | **FAILS** | `references/41-lighthouse-and-web-vitals.md:78` gives KB budgets only; virtualization advice at `41:49` has no size threshold; no complexity budget anywhere; `alaa-algorithms-data-structures` named 0×. |
| 8. Configurability | **FAILS** | Zero occurrences of `VITE_`, env-var discipline, build-time vs runtime config, boundary validation, or feature flags. The only configurability sentence is `references/10-contract-and-boundaries.md:92` "keep one canonical public/base-path source of truth". |
| 9. Speed of development & debuggability | **SATISFIED** | Symptom→cause tables at `references/20-…:125-134` and `40:76-86`; browser-debug decision flow `references/60-browser-debug.md:24-52`; weight-ordered attack order `41:31`. This is the skill's real strength. |
| 10. Documentation | **FAILS** | `references/20-…:108-117` covers JSDoc only. Nothing on what shipped, how it is operated, or how it fails; `90-upstream-deltas-and-maintenance.md:94-104` documents *skill* maintenance, not feature documentation. |

Headline: **no row can legitimately be NOT-OWNED**, because the skill names none of `alaa-testing-strategy`, `alaa-reliability-sla`, `alaa-security-review`, `alaa-observability-soc`, `alaa-services-contract`, `alaa-project-constitution`, `alaa-keyset-pagination`, `alaa-algorithms-data-structures`, `alaa-system-design`, or `alaa-vue-typescript-clean-code`.

### 3. Defect classes actually found

**1 — Stale hardcoded model pins.** `references/90-…:53` ("GPT-5.5 or fallback GPT-5.4"), `:55-56`, `:63-65` (start GPT-5.5 / fall back GPT-5.4 / GPT-5.4-mini for subagent lanes), plus model links at `:109-123`. Consequence: a frontend skill legislates model and effort selection, competing with `/alaa-prompting-guide` (`$alaa-prompting-guide`), which is named 0× here. Once the pins go, `90:44-66` collapses to two surviving sentences (`:48-52` skill mechanics, `:66` instruction precedence) — the rest is prompting-guide territory and should be deleted, not rewritten. Adjacent staleness: the version snapshot `90:12-18` is dated 2026-07-08 and `41:3` "Verified 2026-07-13" against today's 2026-07-28.

**2 — Trigger syntax.** 75 `$alaa-*` call sites, **zero** `/alaa-*`. The skill ships `agents/openai.yaml` (Codex) and is simultaneously installed as a Claude skill (`sohrab-skills:alaa-frontend-developer`), so every call site is cross-runtime and needs both forms. Consequence: a Claude Code agent reading `SKILL.md:70` sees only `$alaa-quasar-app-vite-v3` and has no invokable form.

**3 — Duplication between body and references.** See §5 — six distinct instructions live in both.

**4 — Project-specific / perishable content in the always-loaded body.** `SKILL.md:31` and again `:148` hardcode "`@quasar/app-vite` v3 stable production line since 3.0.1, 2026-07-07" — a dated version fact in the body of a skill that says at `:178` to route detail to references; it is already restated at `references/70-…:8` and `90:16`. `SKILL.md:142` "Do not select `MCP_DOCKER` only to get a headless browser" is harness-specific tooling trivia in the always-loaded body (restated at `50:96` and `60:63` and `70:20`). Consequence: three copies of a version fact go stale together and the body pays for local MCP configuration detail on every load.

**5 — Long numbered procedures nobody reads in order.** `references/30-pwa-sw-and-offline.md:37-79` is a five-step numbered implementation workflow followed by `:80-106` a four-section QA runbook; `40:9-37` is a three-step workflow; `50:18-46` a four-step workflow. Consequence: SW recovery is organised as "do steps 1-5" instead of by failure class — there is no "update flow reloads forever → diagnose `controllerchange` guard → smallest retry → escalate" entry, even though `40:76-86` and `20:125-134` prove the author can write the failure-class shape.

**7 — Fragile tooling.** `SKILL.md:162` and `90:23` invoke `node scripts/check-upstream-versions.mjs` as a bare relative path, which resolves only when cwd is the skill root; the script has no `--help`, no self-test, no request timeout (`scripts/check-upstream-versions.mjs:49-85` uses `https.get` with no `setTimeout`, so a hung registry hangs the agent), and its own header comment `:3` says it is "used by alaa-quasar-app-vite-v3". It is a whitespace-only variant of `alaa-quasar-app-vite-v3/scripts/check-upstream-versions.mjs` — same nine packages, same `showAllTags`, same `resolveStableMajors`, same output shape.

**9 — Unnamed gaps against section 2.** Eight of ten criteria, per §2. All are silences, none are disclaimers.

**10 — Body larger than it needs to be.** 13,522 bytes carrying **four** routers (see §8) and a duplicated version fact.

**11 — No stated companion boundary** with three siblings that route into it: `alaa-vue-typescript-clean-code` (0 mentions, owns the mandatory TS/clean-code gate), `alaa-indexeddb-browser-storage` (0 mentions, owns browser storage — while `21:102-115` legislates browser token storage), `alaa-shaka-player` (0 mentions, but `alaa-shaka-player/SKILL.md:29,97` names this skill as its SSR/hydration partner).

Not found: class 6 (the description at `SKILL.md:3` carries a real "Do not use it when…" clause and `:51-58` expands it), class 8 (no `__pycache__`).

### 4. Boundary map

**(a) Legitimately owns**
- SSR/hydration determinism and cleanup safety for the app family (`20-vue-js-ssr-patterns.md`).
- Frontend-side auth/session *posture* — BFF vs token-mediating vs cookie-bridge vs gateway-bearer vs PKCE, and which one this repo is on (`21-…`).
- PWA/SW *policy layer* — what may change and what must not (`30-…:29-33`), explicitly ceding implementation depth at `30:15`.
- The canonical Lighthouse/Web-Vitals scoring model and score-90 playbook (`41-…`), correctly declared canonical at `41:5` and consumed by both siblings.
- Browser-automation opt-in gate and browser-debug evidence discipline (`60-…`).
- Frontend-facing consequences of API shape (`45-…`) — the *client-side* half only.
- Which frontend companion skill to load (`70-…`).

**(b) Must explicitly disclaim, with the owner named**
- Test design, layers, doubles, proof levels → `alaa-testing-strategy`. Currently `50:26-31` invents its own selection matrix.
- Retry/backoff/timeout/circuit-breaking/degradation doctrine → `alaa-reliability-sla`.
- Log fields, metric names (`alaa_*`), `OTEL_*`, envelope keys, error codes → `alaa-services-contract`.
- Requirement levels and gates → `alaa-observability-soc`; the quality bar itself → `alaa-project-constitution`.
- Security review triggers, threat classes, fail-closed doctrine → `alaa-security-review`.
- Cursor/keyset pagination contract → `alaa-keyset-pagination`.
- TypeScript/SOLID/component-decomposition gates → `alaa-vue-typescript-clean-code`.
- Browser storage mechanics, quota, migrations → `alaa-indexeddb-browser-storage`.
- Complexity budgets → `alaa-algorithms-data-structures`; pre-implementation design → `alaa-system-design`.
- Identifier codec parity → `alaa-crockford-base32-codecs` **and its `scripts/codec-conformance.sh` must be run**, not reasoned about; `SKILL.md:76` names the skill but not the harness.
- Object storage / presigned URLs / `STORAGE_*` → `alaa-minio-object-storage` / `alaa-arvan-object-storage`; browser tus client → `tusd-upload-platform`. All four are 0× here despite the frontend being the client of all of them.
- Model and effort selection → `alaa-prompting-guide`.

**(c) Legislating an out-of-batch owner's ground in its own voice**
- `40-…:59-62`: "exponential backoff / max delay cap / jitter to avoid herd behavior / offline awareness when practical" — `alaa-reliability-sla` owns this doctrine.
- `21-…:118-123`: "Serialize concurrent refresh attempts so five failing requests do not trigger five refresh calls. … Do not keep retrying forever." — reliability doctrine written locally at weaker strength.
- `40-…:73`: "log connect, disconnect, and reconnect attempts at the right environment level" — `alaa-observability-soc` owns the level, `alaa-services-contract` owns the names.
- `45-…:20`: "Prefer one stable envelope style per repo." and `45:26-31` error-shape qualities — `alaa-services-contract` owns envelope keys and error codes.
- `45-…:44-58`: the entire cursor-pagination rule set ("sort by a stable unique order", "append a unique tie-breaker", "reject unsupported sort combinations") — `alaa-keyset-pagination` owns this verbatim.
- `50-…:26-31`: check-selection-by-surface matrix and `50:27` "lint and relevant tests if available" — `alaa-testing-strategy` owns test design and the six proof levels.
- `41-…:78`: performance budgets stated as local defaults — budget doctrine belongs with `alaa-project-constitution`/`alaa-observability-soc`; only the frontend *numbers* are this skill's.
- `21-…:102-109` storage preference ladder — the persistent-storage tiers are `alaa-indexeddb-browser-storage` ground.
- `90-…:53-65`: model/effort policy — `alaa-prompting-guide` ground.

### 5. Duplication

| Instruction | Location A | Location B | Survivor |
|---|---|---|---|
| The router itself (12 topic→file rows) | `SKILL.md:80-107` | `references/00-topic-map.md:5-32` | **B** (≥9 refs ⇒ router in `00-topic-map.md`); A becomes one pointer line |
| "Also load" cross-topic rules | `SKILL.md:109-151` | `references/00-topic-map.md:34-49` | **A** (these are gates, must be always-loaded) — delete B |
| Companion ownership/pairing | `SKILL.md:28-34` + `:68-78` + `:164-173` (three copies in one body) | `references/70-companion-skill-routing.md:5-53` | **A**, collapsed to one table; `70-…` keeps only conflict resolution + ownership notes |
| Required workflow defaults ("Read `AGENTS.md`, apply `$alaa-low-noise`, smallest safe change") | `SKILL.md:60-66` | `references/10-…:36-41` | **A** |
| SSR auth/session boundary + the five supported patterns | `references/10-…:43-68` | `references/21-…:20-100` | **B**; `10-…` keeps one routing line |
| SW QA runbook (install / update / offline / runtime-cache) | `references/30-…:80-106` | `references/50-…:56-62` | **B** (`50-…` owns verification); `30-…` keeps the policy |
| Search keyword list | `SKILL.md:158` | `00-topic-map.md:53-70` **and** `80-legacy-skill-coverage.md:96-113` (three copies) | **`00-topic-map.md`** |
| Quasar v3-is-stable-since-3.0.1-2026-07-07 | `SKILL.md:31` and `:148` | `references/70-…:8`, `90-…:16` | **`90-…`** only |
| MCP browser-profile selection rules | `SKILL.md:139-142` | `50-…:93-96`, `60-…:59-63`, `70-…:15-25` (four copies) | **`70-…`** |
| `check-upstream-versions.mjs` | this skill's `scripts/` | `alaa-quasar-app-vite-v3/scripts/` (functionally identical) | **quasar's**; this one retires |
| SW contract (`SKIP_WAITING`, `clientsClaim()`, one reload on `controllerchange`, exactly one `self.__WB_MANIFEST`) | `30-…:24-26`, `:66` | `alaa-quasar-app-vite-v3/references/30-service-worker-excellence.md:37-58` and `32-pwa-injectmanifest-guard.md:16` | **quasar's** (this file already says at `30:15` it is "the policy layer" — then restates the mechanism) |

### 6. Wording-test failures

1. `references/10-contract-and-boundaries.md:3` — "Treat these as defaults, not universal laws". **Self-granted exception (blanket).** It dissolves the "Hard constraints" section 24 lines below. → *"These are constraints. The only override is a repo-local `AGENTS.md` rule or an explicit user instruction that contradicts a named line here; cite the file and line you are overriding."*
2. `references/10-…:9` — "JavaScript plus JSDoc by default unless the repo already standardizes on TypeScript" (repeated `20-…:7`). **Wrong scope + contradicts the verified fleet fact that `client` is TypeScript and `alaa-vue-typescript-clean-code` is mandatory.** → *"All new and modified frontend code is TypeScript under `strict`; run the gates in `alaa-vue-typescript-clean-code` (`/alaa-vue-typescript-clean-code`, `$alaa-vue-typescript-clean-code`). JavaScript is permitted only in a file already listed under the repo's `allowJs` set."*
3. `SKILL.md:33` — "…or static analysis is no longer trustworthy for a browser-only bug." **Self-granted exception, no external referent** — the agent grades its own evidence. → *"…or you have completed one static pass and can name the single observation source cannot produce (exact console warning text, a computed style value, or an HTTP status). State that observation before opening the browser."*
4. `references/21-…:115` — "preserve behavior unless the user asks for a migration, but call out the security trade-off". **Self-granted exception + "record why not" escape.** → *"Do not add a new write of an access token to persistent browser storage. Where one exists, open a tracked migration item naming the file, the endpoint that mints the token, and the owning maintainer, before this change merges."*
5. `references/21-…:82` — "treat `localStorage` as legacy storage, not the default recommendation". **Preference verb where a constraint was meant.** → *"Do not write an access token to `localStorage` or `sessionStorage`. Hold it in a module-scoped variable owned by exactly one auth module."*
6. `references/40-…:62` — "offline awareness when practical". **Self-granted exception, abstract noun.** → *"Suspend reconnect attempts while `navigator.onLine === false`; resume on the `online` event; cap total reconnect duration and surface the `closed` state to the UI when the cap is hit."*
7. `references/40-…:73` — "log connect, disconnect, and reconnect attempts at the right environment level". **Abstract noun standing in for an observable condition; also legislates an owner's ground.** → *"Emit one structured event per connect, disconnect, and reconnect attempt using the event names and log fields defined by `alaa-services-contract`; the required level is set by `alaa-observability-soc`."*
8. `references/30-…:31` — "Do not silently broaden runtime caching for HTML, JS, CSS, images, workers, or APIs." **"Silently" is the self-granted exception** — broadening loudly is then unconstrained. → *"Do not add or widen a runtime-cache route matcher. A widening requires the four risk notes from §5 (rollback path, stale-asset, offline-regression, hydration) written in the merge request body."*
9. `references/41-…:78` — "Treat a budget breach like a failing test: justify it or fix it." **"Justify it" is a self-granted exception.** → *"A budget breach blocks merge. It clears only by a recorded exception in the repo's budget config naming the route, the new ceiling, and the approving maintainer."*
10. `references/50-…:27` — "UI-only change: lint and relevant tests if available". **"If available" makes the entire test requirement optional.** → *"Select the proof level from `alaa-testing-strategy` for the change surface and run it. If the repo has no runner for that level, that is a blocking finding, not a waiver — report it."*

Runners-up: `references/20-…:105` "unless the user explicitly asks or the task clearly justifies them" (self-granted); `references/60-…:22` "negotiate the design with `$alaa-ui-ux-design-system` guidance" (no named decider); `references/40-…:67` "log at debug level when useful" (self-granted).

### 7. Stale or unverifiable claims

**Verifiable from the files (internally inconsistent or dated):**
- `90-…:12-18` version snapshot dated 2026-07-08 (`vue 3.5.39`, `quasar 2.21.1`, `@quasar/app-vite 3.0.1`, `vite 8.1.3`, `workbox-build 7.4.1`) — 20 days stale as of 2026-07-28, and duplicated as prose in `SKILL.md:31`, `SKILL.md:148`, `70-…:8`, and inside `scripts/check-upstream-versions.mjs:5-11` and `:120`. Five copies to re-verify.
- `41-…:3` "Verified 2026-07-13 against the Lighthouse source" — 15 days stale.
- `90-…:46` "Based on the official OpenAI docs and Codex docs reviewed on April 24, 2026" — three months stale, and everything it introduces (`:53-65`) is model-pin content that must be deleted rather than refreshed.
- `90-…:102` "no dedicated validator script ships with this skill" — true, and a uniformity failure: sibling `alaa-indexeddb-browser-storage/scripts/check_references.py` proves the fleet has the capability.

**Needs live web research before Phase 2 ships:**
- `41-…:11-27` Lighthouse metric weights and the p10/median control points, and `41:34` the claim that "Lighthouse 13 (Oct 2025) replaced legacy opportunity audits with DevTools-aligned insight audits (`cls-culprits-insight`, `image-delivery-insight`, `render-blocking-insight`) — scoring unchanged". A Lighthouse 14 would invalidate both the weights table and the audit IDs.
- `41-…:38` CrUX thresholds (LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1) — currently correct but a Google threshold change is the exact failure mode.
- `41-…:45` "Vue 3.5+ lazy hydration … `hydrateOnVisible()` / `hydrateOnIdle()`" and `41:46` `scheduler.yield()` availability; `41:60` Speculation Rules `eagerness: "moderate"` and `document.prerendering`/`prerenderingchange`; `41:57` HTTP 103 Early Hints — all browser-API claims with no Baseline tier stated.
- `21-…:216` "OAuth browser-based applications **draft**" — likely to have been published as an RFC; the link and the word "draft" both need checking, as does whether its BFF recommendation still matches `21:20-25`'s decision order.
- `90-…:77` "Windows and PowerShell behavior are now explicitly improved" — an undated upstream claim with no referent.
- `30-…:24` "runtime caching is narrowly scoped, typically fonts only" and the Workbox 7.4.x strategy names — verify against Workbox current, or delete and route to `alaa-quasar-app-vite-v3`.

### 8. Router audit

- **Reference count: 13 files** (12 content + `00-topic-map.md`). ≥9, so the convention requires the router in `references/00-topic-map.md` with **one** pointer line in `SKILL.md`.
- **Conformance: FAILS — four routers exist.** (i) `references/00-topic-map.md:5-32` — the conforming one. (ii) `SKILL.md:80-107` "Routing map" — a full duplicate. (iii) `SKILL.md:164-173` "Companion chooser" table. (iv) `SKILL.md:68-78` "Also load companion skills when needed" list, which is itself a third copy of the companion routing already in `SKILL.md:28-34` and `references/70-…`. `SKILL.md:64` does contain the correct single pointer — it is simply followed by 43 more lines of router.
- **Rows are not observable conditions.** `SKILL.md:82` "Standard app-family contract, boundaries, monorepo rules, SSR auth/session boundaries, and workflow defaults: → `references/10-…`" is a heading mirror. `00-topic-map.md:7-32` uses "Need X: Open Y" — a topic noun-list, closer but still not "You are about to <observable situation>". The two rows that pass are `00-topic-map.md:29` ("Need to translate an old skill name…") and `SKILL.md:133` ("Any UI change that appears 'frontend-only' but is really caused by backend query shape, count cost, or missing aggregation"), which is exactly the right shape and should be the template for every row.
- **Path resolution: all in-skill paths resolve.** All 12 targets referenced from `SKILL.md` and `00-topic-map.md` exist on disk. All four cross-skill paths resolve and correctly name the owning skill: `alaa-ui-ux-design-system references/70-motion-and-modern-css.md` (`SKILL.md:123`), `alaa-ui-ux-design-system references/90-quality-gates-and-review.md` (`50-…:65`), `alaa-quasar-app-vite-v3 references/30-service-worker-excellence.md` (`30-…:15`). No dangling paths. `00-topic-map.md` covers all 12 non-router files — coverage is complete.
- Note for the lead: `alaa-quasar-app-vite-v3/SKILL.md:62` describes this skill as covering "CSS/motion", which moved to `alaa-ui-ux-design-system` (`60-…:5`, `90-…:104`). That stale row is quasar's lane, not this one, but the two must be swept together.

### 9. Scripts and assets audit

**`scripts/check-upstream-versions.mjs` (3,751 bytes) — the only script; no `assets/`, no `evals/`.**
- *What it does:* fetches nine npm registry documents over HTTPS (`quasar`, `@quasar/app-vite`, `@quasar/extras`, `vite`, `vue`, `vue-router`, `pinia`, `workbox-build`, `workbox-core`), prints JSON with `latest` + publish date, all dist-tags for `@quasar/app-vite`, and highest stable per major for v2/v3.
- *Would it run:* yes — Node ≥14, `node:https` only, no deps. Sequential (`:124-126`), so nine round-trips; would take a few seconds and, behind this environment's proxy, may need `HTTPS_PROXY` honouring which `node:https` does not do automatically — an unhandled failure mode.
- *Fragile paths:* no `__file__`/`parents[N]` pattern and no temp dirs (good), but both invocation sites (`SKILL.md:162`, `90-…:23`) use the bare relative `node scripts/check-upstream-versions.mjs`, which only works from the skill root.
- *`--help`:* absent. *Self-test:* absent. *Timeout:* absent — `https.get` at `:49-85` has no `request.setTimeout`, so a stalled registry hangs the agent indefinitely. *Exit contract:* `:131-134` sets `process.exitCode = 1` on the first failure, so one unreachable package loses the other eight results.
- *What it would find today:* newer versions than the 2026-07-08 snapshot in `90-…:12-18` for at least `vue`, `quasar`, and `vite` — i.e. it would immediately prove its own skill's documented snapshot stale, which is the correct behaviour and the reason the snapshot should not be prose at all.
- *Verdict:* it is a whitespace-and-comment variant of `alaa-quasar-app-vite-v3/scripts/check-upstream-versions.mjs` (identical package list, `showAllTags`, `resolveStableMajors`, output shape) and its own header comment `:3` says it belongs to that skill. Retire it here; route to the quasar skill's copy and fix the timeout/`--help`/`--self-test` there once.

### 10. Rewrite brief for Phase 2

**Target `SKILL.md` (always-loaded) sections and budget**

| Section | Bytes |
|---|---|
| Frontmatter description (use + do-not-use + dual-runtime naming) | 480 |
| Title, register, one-line subject | 320 |
| Ownership **and** explicit disclaimers naming all 12 out-of-batch/sibling owners | 1,900 |
| When to use / When NOT to use | 950 |
| Non-negotiable gates (SSR determinism; TypeScript-strict via `alaa-vue-typescript-clean-code`; no client-side authorization decision; browser automation opt-in; no SW-strategy drift; no second envelope; budget breach blocks merge) | 1,700 |
| One pointer line to `references/00-topic-map.md` | 110 |
| Mandatory cross-topic "also load" table (compressed from `SKILL.md:109-151`) | 1,850 |
| Search keys | 420 |
| Maintenance | 280 |
| **Subtotal** | **8,010** |
| **+15% for `/name` + `$name` dual forms** | **≈ 9,210** |

Target ceiling **9,600 bytes**, against today's 13,146 net-of-frontmatter — a 27% reduction achieved entirely by deleting three of four routers and the duplicated version fact, with **no** capability removed.

**Content moves**
- `SKILL.md:80-107` (Routing map) → delete; `references/00-topic-map.md:5-32` survives, every row rewritten to "You are about to <observable situation> → read `<file>`".
- `SKILL.md:68-78` + `:164-173` + `references/70-…:5-53` → one table in the body; `70-…` keeps only `:55-68` (ownership notes, conflict resolution).
- `references/00-topic-map.md:34-49` (Also-load) → merge up into the body table; the router does not carry gates.
- `references/10-…:43-68` (SSR auth boundary) → `21-…`, leaving one routing line.
- `references/30-…:80-106` (SW QA runbook) → `50-…`; `30-…` keeps policy only and its `:37-79` numbered workflow is rewritten as failure classes (update loop / stale chunk after deploy / offline page never appears / `__WB_MANIFEST` duplicated).
- `references/45-…:44-58` (cursor rules) → replaced by a routing line to `alaa-keyset-pagination`, keeping only the client-side cursor-handling delta.
- `references/90-…:44-66` model/effort content → delete outright, replaced by one line routing to `/alaa-prompting-guide` (`$alaa-prompting-guide`) and its `references/50-effort-and-thinking.md`. What survives from `90-…` after the pins go: `:26-42` (official-first source map) and `:88-104` (package-manager + maintenance workflow) — roughly 2.2 KB of the current 6.3 KB. That remnant is thin enough to fold into a renamed `95-sources-and-maintenance.md`.
- `90-…:12-18` version snapshot → delete the prose; the script output is the source of truth.

**New reference files (each one buys back a FAILS row)**
- `05-proof-and-tests.md` — routes test design/layers/proof levels to `alaa-testing-strategy`; keeps only the frontend delta (component vs SSR-render vs e2e boundary, hydration-mismatch assertion, contract mocks, and the rule that a test must fail against a plausible broken implementation). *Fixes criterion 1.*
- `25-frontend-security.md` — `v-html`/sanitisation, CSP and nonce handling, `target="_blank"` + `rel`, `postMessage` origin checks, untrusted URL rendering, secrets never in the client bundle, **and the binding statement that the 512-byte permission bitmap is a UI hint and never an authorization decision** (decode via `alaa-permission-generator`'s canonical TypeScript decoder under `assets/permission-bitmap/`); doctrine and threat classes route to `alaa-security-review`, trust boundary to `alaa-trust-gateway-auth`. *Fixes criterion 3.*
- `22-input-validation-and-normalization.md` — client-side input contracts: length caps on every free-text field, separator folding matched by **Unicode category** (`{Cf, Zs, Zl, Zp, Pd}` + `str.isspace()` + the literal set `()._/`) and never by an enumerated list, the rule that client normalization is a UX affordance and the server re-normalizes, and the 80-case conformance corpus (`corpus_sha256 = 7a4250cf64e730d51ef92512975e864cbcfa5da919f658e0f974c50e8d54b548`) as the oracle. Directly closes the live `client` `contact.phone` defect (no `maxlength`; separators reach the backend verbatim). **New capability.**
- `46-resilience-and-degradation.md` — per-request timeouts with configured defaults, idempotency keys on mutating requests, partial-failure and degraded-dependency UI states, offline behaviour of data fetches; all doctrine routed to `alaa-reliability-sla`, only the client-side expression kept. Absorbs and re-points `40-…:57-62`. *Fixes criterion 2.*
- `47-frontend-observability.md` — RUM/`web-vitals` field reporting, unhandled-rejection and error-boundary reporting, `traceparent` propagation from browser to gateway, WS/SSE connection-state events; every name routed to `alaa-services-contract`, every requirement level to `alaa-observability-soc`. Absorbs `40-…:70-74`. *Fixes criterion 4.*
- `48-config-and-environment.md` — `VITE_*` build-time vs runtime config, boundary validation of every injected value at boot with fail-fast, safe defaults, feature flags, consumption of `STORAGE_*` defaults (never a branch in code), and the canonical public/base-path rule moved from `10-…:92`. *Fixes criterion 8.*
- `55-i18n-locale-and-rtl.md` — locale/timezone-deterministic SSR formatting (currently only a one-line prohibition at `20-…:23` with no positive replacement), RTL layout and logical properties, number/date/currency formatting for fa-IR. **New capability.**
- `12-clean-code-boundary.md` — or, cheaper, a body line: TypeScript-strict, SOLID, component decomposition and Pinia store shape all route to `alaa-vue-typescript-clean-code`; this skill keeps only the SSR-imposed constraints. *Fixes criterion 6.*
- Add to `41-…`: complexity/size thresholds — the row count above which virtualization is mandatory, the DOM-node ceiling, list-render complexity budget; doctrine to `alaa-algorithms-data-structures`. *Fixes criterion 7.*
- Add to `50-…`: a "what shipped / how it is operated / how it fails" release-note requirement. *Fixes criterion 10.*

**Retire to `_to_delete/`**
- `references/80-legacy-skill-coverage.md` (2,553 bytes) — maps ten skill names deleted long enough ago that nothing in the fleet references them; its `:92-113` search-alias list is a third copy of the keywords in `SKILL.md:158` and `00-topic-map.md:53-70`. Fold the aliases into the topic map, delete the file.
- `scripts/check-upstream-versions.mjs` — duplicate of `alaa-quasar-app-vite-v3/scripts/check-upstream-versions.mjs`; route to that one and fix `--help`/`--self-test`/request timeout there.

**Genuinely new capabilities gained:** yes, six — client-side input-normalization conformance (`22-`), frontend security posture including the bitmap-is-not-authz rule (`25-`), resilience/idempotency/degradation at the client (`46-`), frontend observability and trace propagation (`47-`), runtime configuration with boundary validation (`48-`), and i18n/RTL/locale-deterministic rendering (`55-`). None of these exists anywhere in the skill today (0 occurrences of `XSS`, `sanitiz`, `CSP`, `idempot`, `traceparent`, `VITE_`, `i18n`, `RTL`, `maxlength`, `normaliz`).

### 11. Gap no existing skill can own

**One: a cross-language user-input normalization contract with a runnable conformance harness.**

Evidence: the settled fleet rule for the `client` `contact.phone` defect is that separators are matched by Unicode **category** (`{Cf, Zs, Zl, Zp, Pd}` plus `str.isspace()` plus the literal set `()._/`), never by an enumerated list, with an 80-case corpus (`corpus_sha256 = 7a4250cf64e730d51ef92512975e864cbcfa5da919f658e0f974c50e8d54b548`) as the oracle. That is a *both-sides* contract: the browser folds and the backend re-folds, and they must agree case-for-case. No file in `alaa-frontend-developer` mentions it (0 hits for `normaliz`, `corpus`, `maxlength`), and a repo-wide grep across all `sohrab/` skills for `corpus_sha256` / the digest / `separator` returns only an unrelated hit in `alaa-quasar-app-vite-v3/references/61-component-usage-atlas.md`.

No existing owner can take it without breaching its own boundary: `alaa-services-contract` owns *names and values*, not normalization algorithms plus a test harness; `alaa-security-review` owns review triggers and threat classes, not input semantics; `alaa-testing-strategy` owns test *design*, not a shipped corpus; `alaa-frontend-developer` can own the browser half but by definition cannot own the Python half. The exact structural precedent already exists in the fleet — `alaa-crockford-base32-codecs` owns an identifier codec contract, ships the canonical JavaScript implementation, and enforces parity with `scripts/codec-conformance.sh`. The same shape is needed for user-entered text, and nothing occupies it.

Everything else I looked for turned out to be a hole in *this* skill rather than a fleet gap: i18n/RTL and locale-deterministic SSR formatting are squarely this skill's own ground (it already prohibits "implicit locale/timezone formatting" at `20-…:23`); frontend RUM and Web-Vitals field telemetry split cleanly between `alaa-observability-soc` (levels) and `alaa-services-contract` (names); browser token storage belongs to `alaa-indexeddb-browser-storage` and `alaa-trust-gateway-auth`.


---

## Appendix B — `alaa-vue-typescript-clean-code`

### 1. What this skill is today

A single-runtime-portable, always-loaded 20,628-byte `SKILL.md` (21,149 total − 521 frontmatter) plus nine reference files (66,816 bytes), one `agents/openai.yaml` (308 B), and four evals. No `scripts/`, no `assets/`, no `__pycache__`.

Its real content is a **Vue/TS design-and-structure contract**: Vue style-guide Priority A–D enforcement, `<script setup lang="ts">` + type-only props/emits/models rules, composable shape rules, SOLID-for-Vue, a code-smell diagnosis vocabulary, hard numeric size budgets (400-line module / 300-line SFC / 60-line function), a 26-row symptom→pattern selection diagnostic, a 23-pattern catalog, and an Alaa-repo antipattern ledger (`65-…`) drawn from failures that actually shipped. That core is the best design-judgment material in the batch.

Everything else it touches — async failure policy, security, validation, observability, load — appears as scattered single lines inside sections whose real subject is something else. It names exactly two companion skills (`alaa-prompting-guide`, `alaa-algorithms-data-structures`) and zero of the eight owners it actually legislates against. Both siblings (`alaa-quasar-app-vite-v3` SKILL.md:56,62; `alaa-frontend-developer` — via its companion table) name **this** skill as mandatory; this skill names neither. The boundary is one-way.

The body is not a router into the references — it is a compressed **duplicate** of them. Sections `## Vue style-guide enforcement`, `## TypeScript and Composition API rules`, `## Clean-code and SOLID enforcement`, `## Design pattern selection`, `## Quasar, Vite, Pinia…`, and `## Validation and completion` (11,769 bytes combined, 57% of the body) are précis of `10-`, `20-`, `30-`, `40-`, `50-`, `60-` respectively. Every task pays for all six regardless of which one it needs.

### 2. Ten-criteria verdict

| # | Criterion | Verdict | Evidence |
|---|---|---|---|
| 1 | Correctness & testability | **FAILS** | Tests appear only as afterthought bullets: SKILL.md:235 "Add or update tests around changed behavior"; `60-validation-checklists.md:28` "Has tests **or is simple enough to verify** through component tests"; :37 "Tests cover state transitions or critical actions". No test-first rule, no failing-test-against-broken-impl requirement, no test-double doctrine, and `alaa-testing-strategy` and its six proof levels are named nowhere in the package. Silence = FAILS. |
| 2 | Failure behavior | **FAILS** | It writes reliability policy in its own voice and never names the owner: `20-typescript-composition-contract.md:178` "transient transport/5xx failures **may** retry or degrade"; SKILL.md:82 idempotency key rule; `65-alaa-observed-patterns.md:100-108`. No timeout value, no backoff shape, no retry ceiling, no degraded-dependency or dependency-gone behaviour. `alaa-reliability-sla`: zero mentions. |
| 3 | Security | **FAILS** | Total security surface is three lines: `50-quasar-vite-pinia-contract.md:127` (no secrets in `VITE_*`), :117 (route `meta` auth posture), :150 (permission denial in browser-API wrappers). **`v-html`, sanitization, and untrusted-input rendering are never mentioned anywhere in 90 KB of a Vue clean-code skill.** No trust boundary, no "a client-side permission check is a UI hint, not an authorization decision", no tenant isolation. `alaa-security-review`, `alaa-trust-gateway-auth`, `alaa-permission-generator`: zero mentions. |
| 4 | Observability | **FAILS** | The only occurrence of logging in the whole package is `30-clean-code-solid-vue.md:62` "Remove dead code, unused imports, stale comments, **console logs**" — it deletes telemetry and supplies no replacement contract. No log/metric/trace/correlation-id rule, no error-boundary reporting rule. `alaa-observability-soc` and `alaa-services-contract`: zero mentions. |
| 5 | Concurrency & load | **FAILS** (partial credit) | Real coverage exists: SKILL.md:221 (N+1 in `v-for`/`map`, correctly routed), `50-…:72-77` (never render unbounded lists; pagination vs virtual scroll), SKILL.md:82 + `20-…:176-177` (abort/race, in-flight dedupe), `40-…:140-142` (cache as a decorator with scoped keys and explicit invalidation). Missing entirely: debounce/throttle for input-driven fetch storms, any cap on parallel in-flight requests, cache TTL/staleness semantics, backpressure, load shedding, and any statement of what happens when 200 rows each fire a lazy-loaded sub-request. |
| 6 | Clean code, SOLID, patterns | **SATISFIED** | `30-clean-code-solid-vue.md:109-140` (five smell families with named repairs and an explicit "when NOT to fix"), `40-…:5-45` (symptom→pattern table + confirming question + look-alike disambiguation), SKILL.md:153-175 (numeric budgets with named split seams), `30-…:201-207` (DIP recognition signals, "the port belongs to the consumer"). This is genuinely production-grade design judgment. |
| 7 | Algorithm & data-structure choice | **FAILS** | Owner is named exactly once, correctly, at SKILL.md:221 — but only for the N+1 case, and the sentence claims "this skill owns the composable and component shape the resolution lands on" while **no reference file anywhere describes that shape**. No complexity budget for the frontend bindings the doctrine needs: per-render computed cost, sort/filter over N rows, memoization thresholds, virtual-list window sizing, tree-depth bounds (`40-…:245` says "guard depth" with no number). The doctrine is routed; the language binding this skill owns is absent. |
| 8 | Configurability | **FAILS** | Only `50-…:124-127` ("Keep aliases minimal", "Keep env access behind typed config modules"). No safe defaults, no boundary validation of config values, no environment/scale-varying behaviour (page sizes, poll intervals, cache TTLs, retry counts, virtual-scroll thresholds are all hard-coded in examples, e.g. `10-…:30` `pageSize: 20`). No feature-flag contract despite `40-…:225` using `userCan(...)` in a Builder example. |
| 9 | Speed of development & debuggability | **FAILS** | The diagnostic tooling is excellent (`40-…:11-45`, `30-…:109-140`) and genuinely makes an agent fast at design decisions. Against that: a 20,628-byte mandatory body on every invocation, plus SKILL.md:50 "Always skim `00-source-map.md`" and SKILL.md:55 "ALWAYS … read `65-…`" — two more unconditional loads. And no debugging guidance for the failure modes that actually cost frontend time in production (hydration mismatch, lost reactivity, stale closure in watcher, `dist`-vs-source package confusion), nor a pointer to `alaa-frontend-developer`'s `60-browser-debug.md` which owns it. |
| 10 | Documentation | **FAILS** | `60-…:92-99` defines a final-response format (changed files, repairs, validation, blockers) and `65-…:126` requires the package guide be updated in the same commit. Nothing covers how the shipped thing is operated or how it fails — no runbook, no ADR, no changelog rule, and the response format duplicates ground owned by `alaa-low-noise` (unnamed). |

### 3. Defect classes actually found

1. **Class 1 — stale model pin.** `references/00-source-map.md:9` "`codex_prompting_guide.md`: **GPT-5.5** outcome-first skills…". SKILL.md:14 is clean and explicitly explains why (confirmed: the earlier pin is gone). Consequence: the one surviving pin sits in the file SKILL.md:50 tells the agent to load on every task.
2. **Class 2 — trigger syntax: not wrong, absent.** Both existing cross-runtime call sites already give both forms — SKILL.md:14 ``/alaa-prompting-guide` (`$alaa-prompting-guide`)`` and SKILL.md:221 ``/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`)``. `agents/openai.yaml:4` uses `$` correctly (Codex-only file, self-reference). **No call site needs fixing; ~14 call sites need creating.** Consequence: an agent loading this skill has no path to the eight owners whose ground it legislates.
3. **Class 3 — body/reference duplication.** SKILL.md:87-116 ↔ `10-…` (whole file); SKILL.md:117-138 ↔ `20-…:1-179`; SKILL.md:139-184 ↔ `30-…`; SKILL.md:185-211 ↔ `40-…` catalog; SKILL.md:212-225 ↔ `50-…`; SKILL.md:249-259 ↔ `60-…:67-91`. 11,769 of 20,628 body bytes. Consequence: two sources of truth for every rule; the shorter one wins by proximity and drifts.
4. **Class 4 — project-specific content in the always-loaded body.** SKILL.md:55-59 spends five lines naming eight Alaa-repo-internal pattern names ("PRVM field resolution, no shadow adapters, orchestrator splits, navigation intents, presence-detection merges, failure classification, route sync, teardown guards"); SKILL.md:149 hard-codes the `CourseDto → mapCourseDtoToCourse → useCourseFilters → CourseTable → course.store.ts` family. Consequence: every non-Alaa Vue task pays for repo-private vocabulary it cannot act on.
5. **Class 5 — unordered long runs.** SKILL.md:87-116 is 22 consecutive undifferentiated bullets across three priority tiers; SKILL.md:185-210 is 20 pattern bullets already fully covered by `40-…`; `10-…:157-165` is a 7-step import-ordering list. Consequence: read as a wall, applied as a wall, or skipped.
6. **Class 6 — description with no "do not use for".** SKILL.md:3 ends "Use before changing Vue/Quasar/TypeScript code…" with no negative clause. The body has `## When NOT to use` (SKILL.md:26-33) but that is not what drives triggering. Sibling `alaa-frontend-developer/SKILL.md:3` does carry "Do not use it when the task is pure Quasar API lookup…". Consequence: fires on backend, infra, and design-only tasks.
7. **Class 7 — fragile/absent tooling.** No `scripts/` at all, while both siblings ship `scripts/check-upstream-versions.mjs` and `alaa-quasar-app-vite-v3` ships `scripts/query-installed-quasar-api.mjs`. `20-…:181-191` asserts four version gates (Vue 3.5, Vue 3.6, Pinia 3, TS 6/7) and tells the agent to "verify against installed versions" with no mechanism. `alaa-crockford-base32-codecs`'s `scripts/codec-conformance.sh` is never invoked despite this skill governing every frontend id-handling surface. Consequence: version claims rot unverified; uniformity across the fleet is broken.
8. **Class 8 — `__pycache__`.** None. Clean.
9. **Class 9 — unnamed gaps.** Eight owners with zero mentions (see §4b); `v-html`/sanitization absent entirely; permission bitmap framing absent; input-normalization-by-Unicode-category absent; observability absent.
10. **Class 10 — body oversized.** 20,628 bytes, of which ~11,800 is duplication and ~1,000 is repo-private detail. Genuinely body-resident content (see §10) sums to ~8.5 KB.
11. **Class 11 — no companion boundary.** `alaa-quasar-app-vite-v3`, `alaa-frontend-developer`, `alaa-ui-ux-design-system`, `alaa-indexeddb-browser-storage`, `alaa-mono-package`, `alaa-frontend-devops` all name this skill; it names none of them. Consequence: two skills each believe they own SSR guards, PWA caching, and browser-API wrappers.

### 4. Boundary map

**(a) Legitimately owns**
- Design-pattern judgment for Vue/TS: selection diagnostic, look-alike disambiguation, per-pattern Vue form, anti-uses (`40-…` in full). Per programme rule this is the assigned owner and it discharges it.
- Vue style-guide Priority A–D as enforceable gates (`10-…`).
- TypeScript/Composition API contract: type-only props/emits/models, `assertNever` exhaustiveness, `as const` vocabulary registries, reactive-destructure rules (`20-…:1-126`).
- Composable shape and lifecycle: `useX` naming, sync-from-setup, plain-object return, teardown (`20-…:128-160`, `65-…:132-138`).
- Size/complexity budgets and split seams (SKILL.md:153-175) — numeric, checkable, and the strongest gate in the skill.
- Code-smell vocabulary and boundary naming alignment (`30-…:109-156`).
- Alaa observed antipatterns (`65-…`) — provenance-backed, uniquely owned, correctly framed as blocking.
- Public-contract inventory before refactor (SKILL.md:74, `60-…:59`).

**(b) Must disclaim, and who owns it**
| Surface | Owner it must name |
|---|---|
| Retry, backoff, timeout, idempotency, degradation doctrine | `$alaa-reliability-sla` |
| Test design, layers, doubles, flake control, six proof levels | `$alaa-testing-strategy` |
| Threat classes, review triggers, fail-closed, secret handling | `$alaa-security-review` |
| Trust boundary; "a client-supplied opaque value carries no trust"; route auth posture | `$alaa-trust-gateway-auth` |
| Permission bitmap contract + canonical TS decoder (`assets/permission-bitmap/`) | `$alaa-permission-generator` |
| Log/metric/trace requirement levels and gates | `$alaa-observability-soc` |
| Every name and value (event names, storage keys, query params, timestamp format, page sizes) | `$alaa-services-contract` |
| Paginating any list endpoint | `$alaa-keyset-pagination` |
| Complexity budgets | `$alaa-algorithms-data-structures` (named once, for N+1 only) |
| Identifier codec + `scripts/codec-conformance.sh` | `$alaa-crockford-base32-codecs` |
| Pre-implementation design | `$alaa-system-design` |
| Output discipline / response format | `$alaa-low-noise` |
| `quasar.config`, app-vite v2/v3 line detection, boot shapes, SW depth, browser permissions | `$alaa-quasar-app-vite-v3` |
| SSR auth/session, PWA/offline policy, Web Vitals, QA planning, browser-debug flow | `$alaa-frontend-developer` |
| Design tokens, theming, motion, `prefers-reduced-motion` | `$alaa-ui-ux-design-system` |
| The quality bar itself | `$alaa-project-constitution` |

**(c) Legislating an owner's ground in its own voice** — quoted, with owner:

- SKILL.md:82 — "an idempotency key is passed when the backend supports one. A double-clicked submit must never create two records." → **reliability-sla** (idempotency doctrine).
- `20-…:177` — "disable the trigger or dedupe the in-flight request (one pending promise per action key) … Re-enable only in `finally`." → **reliability-sla**.
- `20-…:178` — "transient transport/5xx failures **may** retry or degrade with honest wording." → **reliability-sla**; also a preference verb where a constraint is required.
- `65-…:104-107` — "definitive backend denials (non-transient 4xx, auth/validation codes, never `retryable`) surface a message and SKIP the local mutation" → **reliability-sla** (classification taxonomy) + **security-review** (a 403 is a security event, not a transport event).
- SKILL.md:219 — "Declare per-route auth/permission posture in route `meta`; guards read the meta. Scattered per-component auth checks are a review failure." and `50-…:117-118` (fuller form) → **trust-gateway-auth** + **security-review**. Nothing here states that neither the guard nor the bitmap is an authorization decision.
- `50-…:127` — "Do not expose secrets through `VITE_*` variables; anything shipped to client is public." → **security-review**.
- `40-…:140` — "explicit cache keys that include **user/tenant scope**" → **security-review** / **trust-gateway-auth** (tenant isolation).
- `50-…:56-64` — the `import.meta.env.QUASAR_CLIENT` vs `process.env.CLIENT` table plus "app-vite v3 (stable line since 3.0.1)" → **quasar-app-vite-v3** (owns line detection and that dated fact; see its SKILL.md:12,22).
- `50-…:129-136` (PWA cache strategy, versioning, update prompts) and `50-…:138-150` (browser-API wrapper list incl. IndexedDB) → **quasar-app-vite-v3** (`30-service-worker-excellence.md`, `45-browser-apis-and-permissions.md`), **frontend-developer** (`30-pwa-sw-and-offline.md`), **alaa-indexeddb-browser-storage**.
- `50-…:74-77` — "server-side pagination when the backend can page and filter; virtual scrolling for … infinite scroll only with a bounded in-memory window" → **keyset-pagination** (the paging contract) + **frontend-developer** (which explicitly claims "UI-driven N+1 prevention", `70-companion-skill-routing.md` Ownership notes).
- `20-…:120-126` — "event names, storage keys, query-param names, and status codes live in `as const` registries"; "transport and store timestamps as UTC ISO strings (or epoch numbers)" → **services-contract** (owns every name and value; this skill owns only the TS mechanism that holds them).
- `60-…:67-88` + SKILL.md:251-257 — the validation command list and "run the most relevant available checks" → **testing-strategy** (proof levels) and **quasar-app-vite-v3** (build verification depth).
- `60-…:92-99` — "Failure response format for coding agents" → **alaa-low-noise**.
- `30-…:62` — "Remove … console logs" → **observability-soc** (removing telemetry is a telemetry decision).

### 5. Duplication

| Location A | Location B | Which survives |
|---|---|---|
| SKILL.md:87-116 (Priority A/B/C/D bullets) | `10-vue-style-contract.md` (entire file, with examples) | **B.** Keep only the five Priority A absolutes in the body as hard gates. |
| SKILL.md:117-138 | `20-…:1-179` | **B.** Body keeps one line: "`<script setup lang="ts">`, type-only props/emits, no `any`." |
| SKILL.md:139-152 + 177-184 (SoC, SOLID mapping, DRY/KISS, boundary naming) | `30-…:1-107, 142-209` | **B.** SKILL.md:149's `CourseDto` chain is verbatim `30-…:148`. |
| SKILL.md:153-175 (budgets + seams) | `65-…:66-75` (#3 God composable, same seams, same 400-line figure) | **A** (the body — numbers must be in-context); `65-…` #3 collapses to trigger + "why it shipped broken". |
| SKILL.md:185-211 (23 pattern bullets) | `40-…` (23 pattern sections) | **B.** Body keeps one pointer + the "run the diagnostic first" rule. |
| SKILL.md:212-225 | `50-…` | **B**, and most of `50-…` then routes out (see §4c). |
| SKILL.md:249-258 | `60-…:67-91` | **B**, rewritten against `$alaa-testing-strategy` proof levels. |
| SKILL.md:45-61 (per-file "Required reference loading" bullets) | `references/05-topic-map.md` (same rows) | **B.** A is a second router (see §8). |
| `40-…:42-45` (look-alike disambiguation) | `40-…:103-106`, :286, :307, :329, :443 (same distinctions restated per section) | **A** for the pairs table; per-section restatements trim to one clause. |
| `40-…:376-388` (Mediator = "the Alaa orchestrator-composable pattern viewed from the GoF side") | `65-…:64-75` (#3) + SKILL.md:165-172 | **`40-`** owns the GoF framing; `65-` owns the incident. Today all three describe the split. |
| `40-…:254-265` (Iterator: "pair unbounded sequences with pagination/virtual scrolling") | `50-…:72-77` + SKILL.md:220 | **`50-`**, then routed to `$alaa-keyset-pagination`. Three copies today. |
| `30-…:203` (DIP signal: imports Axios/SDK/localStorage) | `40-…:18` (same row in the diagnostic table) | **`40-`** (the table is the entry point). |
| `20-…:111-118` (`assertNever`) | `40-…:410-424` (Visitor), evals #2 | **`20-`** owns the mechanism; `40-` cites it. |
| `50-…:41-71` SSR guards + `50-…:129-136` PWA + `50-…:138-150` browser APIs | `alaa-quasar-app-vite-v3/references/31-ssr-pwa-and-security.md`, `30-service-worker-excellence.md`, `45-browser-apis-and-permissions.md`; `alaa-frontend-developer/references/20-vue-js-ssr-patterns.md`, `30-pwa-sw-and-offline.md` | **The siblings.** This skill keeps only the composable/component shape: "browser globals are read inside `onMounted` or a client-only boot file, never at module top level" — one sentence + `$alaa-quasar-app-vite-v3` for the per-line guard constant. |
| `50-…:117` (route meta auth chain) | `40-…:288-307` (CoR: router guard sequences) | Neither — both route to `$alaa-trust-gateway-auth`; `40-` keeps the CoR shape only. |
| `65-…:100-108` (#6 failure classification) | `20-…:178` | **`65-`** (it carries the incident); `20-…:178` becomes a pointer to `$alaa-reliability-sla` + `65-`. |
| `65-…:124-130` (#8 design-system emits are contracts) | `alaa-mono-package` (dist consumption, asset emission) | **`65-`** for the emit-additivity rule; the `dist`/rebuild half routes to `$alaa-mono-package`. |

### 6. Wording-test failures

1. **"Avoid `any`; use `unknown` only with narrowing; do not silence errors with casts unless the boundary is proven and localized."** — SKILL.md:83. *Preference verb + self-granted exception ("proven" by whom?).* → "`any` does not appear in touched code. An untyped third-party boundary is isolated in one adapter module that returns a declared domain type; the adapter file is the only file permitted an `any`, and it carries a one-line comment naming the library and version."
2. **"Files already over budget before your change: never silently grow them; bring the touched responsibility under budget or record explicitly why not."** — SKILL.md:175. *The Batch-2 defect exactly: "record explicitly why not" is a self-issued permit.* → "A file already over budget does not grow by even one line. Extract the touched responsibility into a new file under budget. If that is impossible, stop and report the blocker; do not ship the growth."
3. **"Validation runs before final response when tools allow it."** — SKILL.md:85. *Self-granted exception with no referent.* → "Before the final response, run the project's typecheck and lint scripts named in `package.json`. If a script is absent or the runtime rejects it, report the exact command and its exact failure text; an unrun check is reported as unrun."
4. **"Has tests or is simple enough to verify through component tests."** — `60-…:28`. *The escape clause voids the rule for exactly the code that most needs it.* → "Every new composable ships a unit test that fails when its teardown, error path, or guard is removed. Test design follows `$alaa-testing-strategy`."
5. **"transient transport/5xx failures may retry or degrade with honest wording."** — `20-…:178`. *Preference verb on failure behaviour; no retry count, no backoff, no ceiling.* → "Retry policy, backoff shape, and retry ceilings come from `$alaa-reliability-sla`; this skill's binding is that the retry lives in the transport adapter, never in a component or store, and that the composable exposes the in-flight state."
6. **"Add `any`, broad casts, disabled lint rules, or `// @ts-ignore` without a localized proof and reason."** — SKILL.md:242. *"Proof and reason" is an abstract noun with no artifact.* → "A disabled lint rule or `@ts-expect-error` carries a line-scoped comment with the rule name and the upstream issue or library version that forces it. `// @ts-ignore` is not used; `@ts-expect-error` is, because it fails when the cause is fixed."
7. **"Repair these in touched code unless doing so would change public behavior outside scope."** — `10-…:5`. *Scope is self-declared.* → "Repair these inside files the change already touches. A repair that would alter a published prop, emit, slot, route name, storage key, or i18n key is not made; it is reported as a blocker with the file and symbol."
8. **"Prefer outcome-first execution, small focused edits, repository evidence, and honest validation over process-heavy narration."** — SKILL.md:16. *Four abstract nouns, no observable condition, and it duplicates `$alaa-low-noise`.* → Delete; replace with "Output discipline follows `$alaa-low-noise` (`/alaa-low-noise`)."
9. **"Validate install/offline behavior in browser devtools when possible."** — `50-…:136`. *Self-granted exception; also not this skill's ground.* → "Service-worker install, update, and offline behaviour is verified per `$alaa-quasar-app-vite-v3`; this skill does not accept SW changes as validated by typecheck and lint alone."
10. **"Second time, wince but duplicate; third time, extract."** — `30-…:74`. *A feeling is not a condition, and it contradicts SKILL.md:148 ("extract duplicated behavior after the abstraction is stable").* → "Extract on the third occurrence, or on the second when the two copies encode the same domain rule and would have to change together. Two copies that change for different reasons stay separate."

### 7. Stale or unverifiable claims

**Verified live this session:**
- `20-…:189-191` "TypeScript 6+: several strict flags and ESM defaults flipped on; **TS 7 is the native (Go-based) compiler**." — directionally stale: TypeScript 7 (tsgo) reached **GA in early July 2026**, not a future line. The consequence is unhandled: `60-…:77` prescribes `npx vue-tsc --noEmit` with no note on `vue-tsc`/tsgo compatibility, which is now the live typecheck question for every Quasar repo. Needs rewrite, not just re-verification.
- `20-…:186-187` "Vue 3.6+: the reactivity core is rewritten (alien-signals) … Vapor mode is opt-in and experimental" — **still accurate**: Vue 3.6 was at RC as of mid-July 2026 with Vapor complete. The "do not adopt for production unless the repo explicitly opts in" framing holds; the wording should say RC, not imply released.

**Needs web research before Phase 2 ships:**
- `20-…:188` "Pinia 3+: … `defineStore({ id: ... })` object-id form is **removed**" (repeated at `50-…:80`) — verify against current Pinia majors; a wrong removal claim breaks working repos.
- `20-…:183-185` Vue 3.5 API list (`useTemplateRef`, `useId`, `onWatcherCleanup`, `watch` pause/resume, stable reactive props destructure) — plausible and stable, but the list is the kind that gains members; re-check.
- `50-…:56-64` "app-vite v3 (stable line since 3.0.1)" + the `QUASAR_CLIENT` / `process.env.CLIENT` split — currently consistent with `alaa-quasar-app-vite-v3/SKILL.md:12,22,26`, but it is a **duplicated dated fact in the wrong skill** and will drift. Delete rather than re-verify.
- `10-…:181` "Element selectors in scoped CSS **may be** slower and less explicit" — a Vue-docs-era performance claim; either verify against current Vue docs or restate as a legibility rule only.

**Unverifiable / dangling provenance:**
- `00-source-map.md:7-8,10` cite `skill-creator/SKILL.md`, `skill-creator/references/openai_yaml.md`, and `exist-skills.zip` — none of these ship in the package; an agent told to "always skim" this file is pointed at four paths it cannot open.
- `00-source-map.md:11` "`Vue_js_3_Design_Patterns_and_Best_Practi.pdf`, **pages 42-71**" — elevated to source-priority rank 4 at SKILL.md:41. Unverifiable third-party provenance driving a normative rank; the derived content in `30-`/`40-` is fine on its own merits and should not depend on a citation nobody can check.
- `00-source-map.md:23-25` three spec/doc URLs — check liveness; `docs.anthropic.com/en/docs/claude-code/skills` in particular has moved before.
- `00-source-map.md:9` "GPT-5.5" — stale pin, delete (all model/effort questions route to `$alaa-prompting-guide` → `references/50-effort-and-thinking.md`).

### 8. Router audit

- **Reference count: 9** → the ≥9 rule applies: the router must live in `references/00-topic-map.md` and `SKILL.md` must carry **one pointer line**.
- **Two routers, confirmed — but not the pair the brief anticipated.** `references/00-source-map.md` is a legitimate **non-router artifact**: a source-provenance ledger plus an interpretation contract and a freshness rule (`00-source-map.md:47-53`). It contains no task→file routing. The actual router is `references/05-topic-map.md`. The **second** router is `SKILL.md:45-61`, "Required reference loading", which re-states every row of `05-topic-map.md` as prose bullets — and then, at :49, tells the agent to start from the topic map anyway. An agent reading SKILL.md:49-61 has already been routed twice before it opens a reference.
- **Router filename and location do not conform.** Fleet convention across the pack is unambiguous: `alaa-frontend-developer`, `alaa-quasar-app-vite-v3`, `alaa-ui-ux-design-system`, `alaa-indexeddb-browser-storage` all use `references/00-topic-map.md`, and `05-*` is reserved for the secondary authority/source artifact (`alaa-quasar-app-vite-v3/references/05-authority-and-api-lookup.md`, `alaa-indexeddb-browser-storage/references/05-source-priority-and-freshness.md`). This skill has the two slots **inverted**. Fix: `05-topic-map.md` → `references/00-topic-map.md`; `00-source-map.md` → `references/05-sources-and-freshness.md` (uniformity across the fleet beats local optimality).
- **Observable-condition test — 5 of 8 rows fail.** `05-topic-map.md:8` "Component, template, or style work", :9 "TypeScript or Composition API work", :10 "Clean-code or SOLID refactor", :11 "Choosing … a design pattern", :12 "Quasar, Vite, Pinia, router, SSR, PWA, or boot files" are heading mirrors — they restate each file's title, so an agent that already knows which file it needs learns nothing and an agent that does not cannot decide. Passing rows: :13 "Finalizing any code change" and :14 "View mappers, flow composables, stores, SDK adapters, or design-system components" (names artifacts, not topics). :15 "Latest/current/version claims" is observable but points at a provenance ledger, not a topic. Replacement rows must name what is on screen: e.g. "The diff adds a `.vue` file, or changes a `v-for`, `:key`, prop declaration, or `<style>` block →"; "A `useX` returns more than one responsibility, or a file exceeds 400 lines / an SFC 300 →".
- **Conflict between the two routers.** SKILL.md:50 "**Always** skim `references/00-source-map.md`" vs `05-topic-map.md:15` which makes it conditional on "latest/current/version claims". SKILL.md:55 "**ALWAYS** … read `65-…`" vs `05-topic-map.md:14` which conditions it on Alaa-style repo surfaces. Two unconditional loads plus a conditional table is not progressive disclosure.
- **Dangling paths:** none among reference→reference links; all nine files are reachable. Four dangling paths point outside the package, all in `00-source-map.md:7,8,10` (see §7).

### 9. Scripts, assets and evals audit

**Scripts: none.** Both siblings ship `scripts/check-upstream-versions.mjs`; `alaa-quasar-app-vite-v3` additionally ships `scripts/query-installed-quasar-api.mjs` and references it from SKILL.md:24,33. This skill asserts four version gates (`20-…:181-191`) and one build-line fact (`50-…:56`) with no verification path. It also never invokes `alaa-crockford-base32-codecs`'s `scripts/codec-conformance.sh` despite governing every frontend module that formats or parses an identifier. **Assets: none**, correctly — the permission-bitmap decoder is `alaa-permission-generator`'s `assets/permission-bitmap/` and must not be restated here (it currently is not; that part is clean by accident, since the bitmap is never mentioned at all).

**Evals (`evals/evals.json`, 4 cases, skill-creator schema, `files: []` throughout — this is the only skill in the pack with an `evals/` dir):**

| id | Tests | Current? | Would pass? |
|---|---|---|---|
| 0 `monolithic-component-refactor` | 700-line page → service port, composable/store, prop-mutation removal, formatter extraction, budgets | Yes — matches SKILL.md:158-172 exactly | **Yes.** The skill's strongest ground. |
| 1 `sdk-port-injection` | typed port, promise-wrapping adapter, `Symbol` injection key, fake in tests, cleanup | Yes — matches `30-…:191-207` and `40-…:64-79, 426-443` | **Yes.** |
| 2 `kind-switch-strategy` | discriminated union + per-concern handler maps + `assertNever` | Yes — matches `20-…:111-118` and `40-…:410-424` | **Yes.** |
| 3 `alaa-observed-patterns-gate` | PRVM resolution, orchestrator, navigation intents, failure classification, teardown guards | Yes — mirrors `65-…` headings | **Yes**, but it is a retrieval test: it checks the agent loaded `65-…`, which SKILL.md:55 makes unconditional anyway. |

**Verdict: current but non-discriminating.** All four probe criterion 6 — the one criterion that already passes. **Zero** evals exercise a failure path, a security boundary, an observability contract, concurrency under load, SSR safety, the validation gate, the "when NOT to use" boundary, or the size budgets as a *rejection* (eval 0 only rewards respecting them). A skill with all eight FAILS above scores 4/4 today. `expected_output` is also free prose rather than checkable predicates, so scoring is judgment-dependent. Phase 2 must add at least: (a) a negative-trigger eval (a backend-only task the skill must decline), (b) a double-submit / abort-race eval, (c) a `v-html` + untrusted-content eval, (d) an eval where the correct answer is *"route to `$alaa-reliability-sla` / `$alaa-keyset-pagination` and do not decide it here"*, and (e) an over-budget-file eval where growing the file must be refused, not annotated.

### 10. Rewrite brief for Phase 2

**Target file list**

| File | Purpose | Bytes (target) |
|---|---|---|
| `SKILL.md` | frontmatter (with "Do not use for" clause) + invariants + budgets + companion table + one router pointer | **≤ 9,800** (body, net of frontmatter) |
| `references/00-topic-map.md` | **the** router; 12-14 rows, each an observable condition | 2,200 |
| `references/05-sources-and-freshness.md` | renamed `00-source-map.md`; GPT-5.5 pin deleted, dangling local paths deleted, PDF citation demoted to a note | 2,400 |
| `references/10-vue-style-contract.md` | unchanged in scope; absorbs SKILL.md:87-116 | 4,900 |
| `references/20-typescript-composition-contract.md` | keeps types/props/emits/models/refs/registries/time; **loses** :174-179 async block to `70-`; version gates keep a script | 5,400 |
| `references/30-clean-code-solid-vue.md` | unchanged in scope; absorbs SKILL.md:139-152,177-184 | 9,200 |
| `references/41-pattern-selection.md` | diagnostic table + look-alike pairs (from `40-…:1-45`) | 5,200 |
| `references/42-structural-patterns.md` | Adapter, Decorator, Proxy, Facade, Bridge, Composite, Flyweight | 6,500 |
| `references/43-behavioral-patterns.md` | Strategy, State, Command, CoR, Pipeline, Template Method, Mediator, Memento, Observer, Visitor, Iterator | 10,500 |
| `references/44-creational-and-async-idioms.md` | Singleton, DI, Factory, Abstract Factory, Builder, Prototype, Callbacks, Promises | 6,000 |
| `references/50-quasar-vite-pinia-contract.md` | **shrinks**: keeps Pinia store shape, router param typing, Vite alias/typed-config; SSR guard constants, PWA, browser-API list all become one-line routes | 2,300 |
| `references/60-validation-gates.md` | renamed; commands + checklists rewritten against `$alaa-testing-strategy` proof levels; response format routed to `$alaa-low-noise` | 3,200 |
| `references/65-alaa-observed-patterns.md` | unchanged content, minus the seam list duplicated from SKILL.md:165-172 | 8,000 |
| **`references/70-async-and-failure-binding.md`** *(new)* | Vue binding only: where the retry lives, abort ownership, in-flight dedupe key, teardown-guard-every-surface, what the composable exposes. Doctrine → `$alaa-reliability-sla` | 3,500 |
| **`references/72-frontend-security-binding.md`** *(new)* | `v-html`/sanitization; a client-side permission check is a UI hint and never an authorization decision (bitmap contract → `$alaa-permission-generator`, 512-byte cap, decoder not restated); no secrets in `VITE_*`; route trust posture → `$alaa-trust-gateway-auth`; ids → `$alaa-crockford-base32-codecs` + `scripts/codec-conformance.sh`; **input normalization matches separators by Unicode category (`{Cf, Zs, Zl, Zp, Pd}` + `isspace()` + `()._/`), never by an enumerated character list — an enumerated list is a defect class, not a fix**; values/limits (`maxlength`) → `$alaa-services-contract` | 4,000 |
| **`references/74-observability-binding.md`** *(new)* | what a component/composable/adapter may emit, error-boundary reporting, correlation-id propagation through the HTTP facade, why `console.log` is deleted *and what replaces it*. Levels/gates → `$alaa-observability-soc`; names → `$alaa-services-contract` | 3,000 |
| **`references/76-load-and-concurrency-binding.md`** *(new)* | debounce/throttle for input-driven fetches, parallel-request cap, cache TTL/invalidation at the adapter, virtual-list window sizing, per-render complexity budget, tree-depth bound. Pagination → `$alaa-keyset-pagination`; complexity → `$alaa-algorithms-data-structures` | 3,500 |
| **`references/78-testing-binding.md`** *(new)* | Vitest/VTU/`@pinia/testing` binding for the six proof levels; what a composable test must fail on. Design → `$alaa-testing-strategy` | 3,000 |
| **`scripts/check-frontend-versions.mjs`** *(new)* | mirrors the sibling script: reads `package.json`/lockfile, prints installed vs latest for vue, vue-router, pinia, vite, typescript, vue-tsc, `@quasar/app-vite`; drives `20-…` version gates | — |
| `evals/evals.json` | 4 existing + 5 new (see §9) | — |

**Body byte budget** — sum of retained sections: Purpose/posture 350 + portability & model routing 400 + when-to-use / when-NOT 700 + companion-ownership table 1,400 + source priority 400 + router pointer 150 + non-negotiable invariants 2,600 + size/complexity budgets 900 + task-mode + public-contract inventory 700 + validation gate 450 + stop rules 400 = **8,450 × 1.15 ≈ 9,720 → budget 9,800 bytes**, down from 20,628 (−52%), while the reference set grows from 66,816 to ~85,000 and gains four whole capabilities. Coverage is bought with routing, not omission.

**What moves where:** SKILL.md:87-116 → `10-`; :117-138 → `20-`; :139-152,177-184 → `30-`; :185-211 → `41-`/`42-`/`43-`/`44-`; :212-225 → `50-` (Pinia/router/Vite) and out to `$alaa-quasar-app-vite-v3` (SSR guards, PWA, browser APIs); :226-248 → dissolved into the files that own each line; :249-258 → `60-`; :45-61 → one pointer line. `20-…:174-179` → `70-`. `50-…:41-71,129-150` → mostly out of the skill. `65-…:66-75` seam list → deleted (body owns it).

**Files to retire:** `references/05-topic-map.md` (becomes `00-topic-map.md`), `references/00-source-map.md` (becomes `05-sources-and-freshness.md`), `references/40-patterns-vue-quasar.md` (split into `41-`/`42-`/`43-`/`44-`; nothing lost).

**Is a genuinely new capability gained? Yes — four.** (1) A frontend **security** binding, including the `v-html`/untrusted-content rule that is absent from all 90 KB today and the "client-side permission is a UI hint, never authorization" framing that the `client` bitmap requires. (2) An **observability** binding, replacing a skill that currently only deletes logs. (3) A **load/concurrency** binding beyond N+1 — debounce, request caps, cache TTL, render-cost budgets. (4) A **testing** binding to the six proof levels. Plus the input-normalization-by-Unicode-category rule, which converts a twice-repeated production defect into a compile-time-visible standing rule. Everything else in the rewrite is relocation, deduplication, and routing.

### 11. Gap no existing skill can own

**None.** Every gap found maps to an existing owner plus a missing *binding* in this skill:

- `v-html` / untrusted content rendering → threat class is `alaa-security-review`'s; the Vue-template binding is this skill's.
- Client-side permission checks → contract and decoder are `alaa-permission-generator`'s; trust rule is `alaa-trust-gateway-auth`'s; the "guards read route `meta`, and that decision is a UI hint" binding is this skill's.
- Phone/separator normalization → the category rule and the 80-case corpus are settled platform doctrine and the value belongs to `alaa-services-contract`; the "a validator/formatter never enumerates characters" rule belongs in this skill's Validator/Formatter lane (`30-…:14-15`), where no rule currently exists.
- Frontend observability, retry/timeout, complexity budgets, pagination, test design, output discipline → all have named owners; only the Vue-shaped binding is missing.
- Hydration-mismatch and browser debugging → `alaa-frontend-developer/references/60-browser-debug.md` owns it; this skill merely fails to name it.

No new skill is warranted. The correct Phase 2 move is fourteen `$`/`/` routes and four binding files, not a fifteenth skill.

Sources: [Vue 3.6 RC / Vapor status](https://repojournal.com/showcase/vuejs/2026-07-18), [vuejs/core releases](https://github.com/vuejs/core/releases), [TypeScript 7 GA](https://typescriptpro.com/blog/typescript-version-7-2026-07-08), [TypeScript 7 native compiler migration](https://www.digitalapplied.com/blog/typescript-7-0-ga-native-compiler-migration-playbook-2026)


---

## Appendix C — `alaa-quasar-app-vite-v3`

Read all 34 files in full, ran both scripts live, and verified sibling paths. Here is the audit.

### 1. What this skill is today

**Subject.** A version-aware control plane for `@quasar/app-vite` (v3 primary, v2 maintenance, v2→v3 migration), plus everything the Alaa frontend touches through Quasar: config/env/boot/routing, SPA/SSR/PWA/BEX/Capacitor/Cordova/Electron, service workers, WebOTP and device trust, browser permission APIs, component/directive/plugin atlases, a11y/perf guardrails, testing/CI, and upstream freshness.

**Register.** Senior, extremely compressed, declarative. Semicolon-dense prose with `✅ Do / ❌ Don't` pairs, `Search:` vocabulary trailers on most references, and absolute dates. It reads as a specification, not a tutorial. Quality of the *content* is high — the SW update-lifecycle section and the env/`clientPrefix` contract are the best writing in the batch. The problems are structural, not intellectual.

**Shape.**

| Part | Bytes | Notes |
|---|---|---|
| `SKILL.md` total | 7,484 | 70 lines |
| — frontmatter | 762 | `name` + `description` only; description 730 chars |
| — always-loaded body | **6,716** | 8 sections |
| `agents/openai.yaml` | 342 | 2 lines, valid, Codex-only by design |
| `references/` (30 files) | **142,129** | 00 (4,642) … largest `45-browser-apis-and-permissions.md` 10,827, `30-service-worker-excellence.md` 9,868, `61-component-usage-atlas.md` 9,048, `80-upstream-deltas…` 7,879, `10-v2-to-v3-migration.md` 7,054; smallest `63` 1,756, `32` 1,911 |
| `scripts/` (2 files) | 8,653 | `check-upstream-versions.mjs` 3,022; `query-installed-quasar-api.mjs` 5,631 |
| **Total** | **158,608** | No `__pycache__`, no `.pyc`, no `.DS_Store` |

Body is already lean for a 30-reference pack — the completeness law is not violated by size. It is violated by a **second router inside the body** and by cross-reference rot.

### 2. Ten-criteria verdict

| # | Criterion | Verdict | Evidence |
|---|---|---|---|
| 1 | Correctness and testability | **FAILS** | `references/75-testing-ci-playbook.md:16` sets test layers ("Minimum useful layers: type/lint; unit …; critical-flow E2E smoke") in its own voice; `:36–46` demands behavior-proving tests with a good negative example, but there is no failing-test-first rule, no SW/offline or hydration regression proof, and `alaa-testing-strategy` is named **nowhere** in the pack. Silence ≠ NOT-OWNED. |
| 2 | Failure behavior | **FAILS** | Best-in-class on one axis: `references/30-service-worker-excellence.md:34–58` (waiting-worker contract, `skipWaiting` chunk-404 hazard, `controllerchange` loop guard, kill-switch SW, `updateViaCache: 'none'`), `:22–24` ("Replays require server idempotency keys"), `:64` diagnosis list, `references/32-pwa-injectmanifest-guard.md:36–42` verification set. But **no SSR render-failure behaviour** (nothing on a 500 from `dist/ssr/index.js`, no fallback-to-SPA rule), **no API-unreachable UX contract**, no client fetch timeout/retry/backoff anywhere except the geolocation error-2 line at `references/45-browser-apis-and-permissions.md:25`, and `alaa-reliability-sla` is never named. |
| 3 | Security | **FAILS** | Strong core: `references/30-service-worker-excellence.md:74` ("SW never mints, attaches, or persists auth context", naming `$alaa-trust-gateway-auth`), `references/20-v3-config-and-features.md:55` (`clientPrefix` as a security boundary), `references/31-ssr-pwa-and-security.md:55–70`. But `references/33-ssr-pwa-playbook.md:128` "never cache authenticated APIs **unless explicitly safe**" is a self-granted exception on the security-critical rule; `references/11-review-and-upgrade-checklist.md:74` downgrades it to "not cached **by default**"; content safety is stated as a noun phrase, not a rule (`references/31-ssr-pwa-and-security.md:58`, `references/70-guardrails-a11y-performance-monorepo.md:89`); no CSP; `alaa-security-review` never named. |
| 4 | Observability | **FAILS** | The only occurrence of the word in 30 references is `references/32-pwa-injectmanifest-guard.md:32`, listing "logging/observability" as a *low-risk* change. No client error-reporting contract, no SW lifecycle telemetry, no web-vitals emission field names. Web Vitals *scoring* is correctly routed to `$alaa-frontend-developer` `references/41-lighthouse-and-web-vitals.md` (`references/50-modern-experience.md:26`), but that is scoring, not a telemetry contract. `alaa-services-contract` and `alaa-observability-soc` never named. |
| 5 | Concurrency and load | **SATISFIED** | `references/30-service-worker-excellence.md:34` ("wait until every old-SW client closes (refresh is insufficient)"), `:36` (`clientsClaim()` safe, unconditional `skipWaiting()` not), `:24` (schema coordination across SW/window via `BroadcastChannel`/`postMessage`), `:28` (cold-boot tax, navigation preload, `caches.match()` scoping); SSR request isolation as a hard rule in four places incl. `references/33-ssr-pwa-playbook.md:33–45` and `references/70-guardrails-a11y-performance-monorepo.md:50,57`. Gap noted: request coalescing/in-flight dedupe is absent. |
| 6 | Clean code, SOLID, patterns | **NOT-OWNED** (`alaa-vue-typescript-clean-code`) | `SKILL.md:56` "Vue/TS output -> `$alaa-vue-typescript-clean-code`"; `:62` "(mandatory Vue/TS)"; `references/00-topic-map.md:47` "any Vue/TS clean-code gates -> `$alaa-vue-typescript-clean-code`". Owner named at three call sites. |
| 7 | Algorithm/data structure with budgets | **FAILS** | Real structural choices exist — `references/61-component-usage-atlas.md:52–56` (virtualize vs infinite scroll, `virtual-scroll-item-size`, keep `items-fn` synchronous), `references/70-guardrails-a11y-performance-monorepo.md:23`, `references/30-service-worker-excellence.md:28` ("large unscoped caches slow lookups") — but **zero stated budgets**: no row count at which virtualization becomes mandatory, no bundle-size ceiling, no LCP/INP target, no precache-size cap beyond "set `maximumFileSizeToCacheInBytes`". `alaa-algorithms-data-structures` never named. |
| 8 | Configurability | **SATISFIED** | The build-time-vs-runtime translation is the skill's strongest section: `references/20-v3-config-and-features.md:34–56` (env contract, `clientPrefix: 'QCLI_'` default, "QCLI_* is PUBLIC; never secret", `define` vs `defineEnv` stringify semantics, single root `/env.d.ts`), `references/22-cli-cookbook-and-examples.md:56–96` with the double-stringify anti-pattern, `references/12-v2-maintenance-playbook.md:121–131` (secret exclusion + `.env.example`). Safe defaults are stated as defaults. Gap: no boundary *validation* — nothing requires fail-fast validation of config at boot, and nothing covers post-build runtime config (fetched `/config.json`) for a static bundle. |
| 9 | Speed and debuggability | **SATISFIED** | `references/05-authority-and-api-lookup.md:15–24` + the query script turn "what props does QTable have" into one command; `references/70-guardrails-a11y-performance-monorepo.md:53–58,82–89` are true symptom→cause tables; `references/30-service-worker-excellence.md:60–64` is unusually concrete (DevTools **Bypass for network** vs Network "Disable cache", `chrome://serviceworker-internals`, Safari 26 Develop → Inspect Apps, `self.__WB_DISABLE_DEV_LOGS`); `references/45-browser-apis-and-permissions.md:58–62` (`--use-fake-device-for-media-stream`, `--use-file-for-fake-audio-capture`). Counterweight: the 40-checkbox `11` and six competing routing tables. |
| 10 | Documentation | **FAILS** | Reporting-to-user is covered well — `SKILL.md:68–70` ("Never claim an unrun check passed"), `references/13-examples-review-style.md:148–175`, `references/75-testing-ci-playbook.md:100–110`. But nothing requires documenting **how the shipped thing is operated or how it fails**: no runbook artifact, no requirement to record the SW cache-name/version contract, the update UX, or the offline degradation matrix for an operator. `references/32-pwa-injectmanifest-guard.md:22–28` is the closest and is a per-change note, not a shipped artifact. |

**Standing preference 1 (wrap official capabilities): SATISFIED, exemplary.** `references/05-authority-and-api-lookup.md` delegates the entire exact-API surface to the project's own `quasar describe` instead of mirroring it; `references/30-service-worker-excellence.md:18` ("`workbox-recipes` … packages these primitives and is a valid start"); `references/21-cli-vite-and-config.md:38` ("do not replace Quasar's plugin"); `references/12-v2-maintenance-playbook.md:55`; `references/66-api-usage-atlas.md:21` ("prefer it to hand-rolled lifecycle"). **Standing preference 2 (uniformity): SATISFIED** — `references/21-cli-vite-and-config.md:34` ("Package manager is a repo contract"), `references/22-cli-cookbook-and-examples.md:195`.

### 3. Defect classes actually found

**Class 1 — stale model pins.** `references/91-agent-authoring-and-dual-runtime.md:3` ("targets Claude Code Agent Skills and **GPT-5**/Codex") and `:32` (table header "Claude Code | **GPT-5** / Codex"). Consequence: a generation pin that the file's own line 3 forbids ("Refer to runtime families, not fast-aging model IDs"). The file contradicts itself in the same sentence.

**Class 2 — trigger syntax.** 42 `$alaa-*`, zero `/alaa-*`. Cross-runtime call sites needing **both** forms: `SKILL.md:52,53,56,62`, `references/00-topic-map.md:47,48`, `references/30-service-worker-excellence.md:3`, `references/40-webotp-and-device-trust.md:3`, `references/45-browser-apis-and-permissions.md:3`, `references/50-modern-experience.md:30,32,34`, `references/20-v3-config-and-features.md:69,78`, `references/10-v2-to-v3-migration.md:5`, `references/91-agent-authoring-and-dual-runtime.md:3`. `agents/openai.yaml:1` is correctly `$`-only (Codex-runtime file). Consequence: a Claude Code agent reading any of these has no invocable form.

**Class 3 — duplication.** Exhaustive table in §5. Headline: the v2→v3 delta set is stated **six times**, and has already drifted into a **factual contradiction** — `references/10-v2-to-v3-migration.md:51` says `sourceFiles` default is `pwaServiceWorker: 'src-pwa/custom-sw'`, while `references/11-review-and-upgrade-checklist.md:99`, `references/31-ssr-pwa-and-security.md:17` and `references/32-pwa-injectmanifest-guard.md:7` all say `'src-pwa/sw/custom-sw'`. Consequence: an agent that reads `10` during a migration writes the wrong `sourceFiles` value and the custom SW is silently ignored.

**Class 4 — project-specific content in the always-loaded body.** Not found; the body is clean. But note `references/33-ssr-pwa-playbook.md:126` ("For educational **VOD** apps") is now stale platform content — `vod` is being deprecated.

**Class 5 — long numbered procedures.** `references/11-review-and-upgrade-checklist.md` is 148 lines of ~45 unordered checkboxes (`:9–16`, `:43–50`, `:53–62`, `:65–70`, `:73–78`, `:81–86`) with no priority, no failure signature, no stopping rule. `references/10-v2-to-v3-migration.md` is a legitimately sequential migration (`:17–24` sequence, `:62–68` per-mode gate) but has **no failure-class recovery at all**: nothing on `quasar prepare` failing, a blocking App Extension, SSR building but 500-ing, or a dirty Capacitor `www` — and `:72–74` "Rollback" is two sentences. `references/12-v2-maintenance-playbook.md` is correct/wrong pairs and reads fine. The skill demonstrably knows the right shape — `references/70-guardrails-a11y-performance-monorepo.md:53–58,82–89` and `references/30-service-worker-excellence.md:64` are exactly symptom→cause — it just does not apply it to the migration files.

**Class 6 — description without a "do not use for".** Partial. `SKILL.md:3` ends "…; not plain Vue/Vite without Quasar CLI." A negative clause exists but is one-dimensional: it does not disclaim Vue/TS code quality, broad frontend, CI/deploy, IndexedDB, or gateway auth — all of which the *body* disclaims at `:62,66`, i.e. after the skill has already triggered. Consequence: over-triggering against `alaa-vue-typescript-clean-code` and `alaa-frontend-developer`.

**Class 7 — fragile tooling.** Scripts themselves are solid (no `Path(__file__).parents[N]` equivalent; `query-installed-quasar-api.mjs:104–110` even refuses to execute a CLI resolved outside the installed package). Two real fragilities: (a) `scripts/check-upstream-versions.mjs:31–53` sets **no request timeout** and uses raw `https.get`, which ignores `HTTPS_PROXY` — it will hang or fail behind a proxy with no diagnostic; (b) invocation-path inconsistency — `SKILL.md:33` and `references/05-authority-and-api-lookup.md:27` correctly use `<skill-dir>/scripts/…`, while `SKILL.md:24`, `references/20-v3-config-and-features.md:7`, `references/80-upstream-deltas-and-live-checks.md:7` and `references/90-maintenance-and-live-checks.md:7` use bare `node scripts/check-upstream-versions.mjs`, which only works if cwd is the skill directory.

**Class 8 — `__pycache__`.** None. Clean.

**Class 9 — unnamed gaps against §2.** Criteria 1, 2, 3, 4, 7 and 10 fail with no owner named anywhere in the pack: `alaa-reliability-sla`, `alaa-testing-strategy`, `alaa-security-review`, `alaa-observability-soc`, `alaa-services-contract`, `alaa-project-constitution`, `alaa-system-design`, `alaa-keyset-pagination`, `alaa-permission-generator`, `alaa-crockford-base32-codecs`, `tusd-upload-platform`, both object-storage skills, `alaa-shaka-player`, `alaa-algorithms-data-structures` — zero mentions, total.

**Class 10 — body larger than needed.** Body is 6,716 B, which is proportionate. But it carries three things that belong elsewhere: the full version snapshot (`SKILL.md:26`, duplicated in `20:9–21` and `80:26–36`, and already 2 minors stale — see §7), a compressed **second router** (`:45`), and a search-vocabulary dump (`:60`, duplicating `references/00-topic-map.md:35–43`).

**Class 11 — companion boundary.** Stated and good *for in-batch companions*: `SKILL.md:62,64–66`, `references/00-topic-map.md:45–48`. Silent on every out-of-batch owner. Also silent on two in-repo neighbours it directly overlaps: `alaa-shaka-player` (media/VOD caching at `references/11-review-and-upgrade-checklist.md:75`, `references/33-ssr-pwa-playbook.md:126–130`, `references/30-service-worker-excellence.md:15`) and `tusd-upload-platform` (QUploader transport at `references/61-component-usage-atlas.md:44`).

**Additional defect — dangling internal references (not in the eleven classes, but the most damaging thing I found).**
- `references/31-ssr-pwa-and-security.md:13` — "First confirm the app-vite line (`70-...`)". File `70` is the a11y/performance/monorepo guardrails file and contains **no** line-detection content. Correct target is `80-upstream-deltas-and-live-checks.md`.
- `references/35-platform-modes.md:3` — identical broken pointer, "First confirm the `@quasar/app-vite` line (`70-...`)".
- `references/85-legacy-skill-coverage.md:33–38` — the entire "Old-name search routing" block uses a **dead numbering scheme** that contradicts its own table 20 lines above: "`quasar-component-*`: search the exact symbol in `40`" (40 is WebOTP/device trust), "search exact API in `50`" (50 is modern experience), "`quasar-ssr-*`: start `20`. `quasar-pwa-*`: start `20`, then `21` for InjectManifest/update flow" (20/21 are v3 config and CLI/Vite). Consequence: the file whose only job is routing 224 retired skill names routes six of nine buckets to the wrong file.

All **cross-skill** paths verified to exist: `$alaa-frontend-developer` `references/{21-ssr-auth-and-session-patterns,30-pwa-sw-and-offline,41-lighthouse-and-web-vitals,50-qa-and-verification}.md`, `$alaa-indexeddb-browser-storage` `references/{70-offline-sync-outbox-cache-patterns,95-alaa-integration-playbook}.md`, `$alaa-ui-ux-design-system` `references/70-motion-and-modern-css.md` — all present. No dangling *external* paths.

### 4. Boundary map

**(a) Legitimately owns.** `@quasar/app-vite` v2/v3 line detection and the entire delta set; `quasar.config` shapes, `build.env`/`define`/`defineEnv`, aliases, `extendViteConf`/`vitePlugins`; boot/`redirect` semantics; the seven platform modes and their v3 folder/config changes; Quasar-specific SSR wiring (`ssrContext`, `serve.devError()`, `/src-ssr/server-assets`); the Quasar PWA wiring surface (`pwa.workboxMode`, the v3 `extendPWA*` hook names, `src-pwa/sw/`) and — genuinely — deep Workbox/SW engineering; the installed-API lookup protocol and its script; component/directive/plugin intent atlases; Quasar-specific a11y/perf failure signatures; Vite 8/Rolldown migration input.

**(b) Must disclaim, and who owns it.**

| Ground | Owner it must name |
|---|---|
| Retry/backoff/timeout/idempotency/degradation doctrine | `alaa-reliability-sla` |
| Test design and the six proof levels | `alaa-testing-strategy` |
| Review triggers, threat classes, fail-closed doctrine | `alaa-security-review` |
| Requirement levels and observability gates | `alaa-observability-soc` |
| Every log field, event/code name, `alaa_*` metric, `OTEL_*` name, envelope key | `alaa-services-contract` |
| The quality bar itself | `alaa-project-constitution` |
| Pre-implementation design | `alaa-system-design` |
| Paginating any list endpoint (QTable server pagination, QInfiniteScroll) | `alaa-keyset-pagination` |
| Trusted headers, TOTP step-up trust semantics, "client-supplied opaque value carries no trust" | `alaa-trust-gateway-auth` |
| Bitmap contract + canonical TS decoder | `alaa-permission-generator` |
| Identifier codec + `scripts/codec-conformance.sh` | `alaa-crockford-base32-codecs` |
| Browser tus client, resume matching (QUploader) | `tusd-upload-platform` |
| Presigned URLs / object storage | `alaa-minio-object-storage` / `alaa-arvan-object-storage` |
| Player/DRM/VOD media | `alaa-shaka-player` |
| Provider CI YAML; the stack skill owns gates and predicates and emits no provider YAML | `alaa-gitlab-ci-cd` |
| Container expression | `alaa-docker-production` |
| Model and effort questions | `alaa-prompting-guide` (`references/50-effort-and-thinking.md`) — named once, `SKILL.md`-adjacent only via `references/91-agent-authoring-and-dual-runtime.md:3` |

**(c) Legislating an owner's ground in its own voice.**

`references/40-webotp-and-device-trust.md` against `alaa-trust-gateway-auth` — the worst case. Line 3 name-checks "auth-backend `$alaa-trust-gateway-auth`" in a header list, then §4 writes the gateway's policy itself:

- `:81` — "After first successful auth, **server sets** a random opaque ID in `Secure; HttpOnly; SameSite=Lax` first-party cookie; server-set cookies avoid Safari ITP's 7-day script-storage cap." (A frontend skill specifying server cookie attributes and issuance timing.)
- `:83` — "Send raw-ish fingerprint vector/BotD verdict with ID; **server fuses IP/ASN velocity/history using fuzzy similarity, never hash equality.**"
- `:84` — "**Server chooses** silent pass / OTP re-challenge / **TOTP or passkey step-up** / block; rotate ID after credential changes or suspected compromise."
- `:64` — "Chrome consent is user-mediated. **Auto-submit only if risk policy permits no value review.**"
- `:69` — "Origin binding blocks phishing-domain autofill, not manual code entry."

`:84` is the acute one: it names TOTP step-up as a server decision but the skill nowhere states the binding platform facts that make the frontend correct — the gateway is **non-blocking** for TOTP step-up, so an absent proof and an invalid proof are indistinguishable downstream and the backend denies in both cases (the client must render the backend's denial, never infer step-up state itself); and `X-TOTP-VERIFIED-UNTIL` is Unix epoch seconds while the response body's `verified_until` is ISO 8601 — a client parser written against the body reads the header wrong. A frontend written from `40` as it stands will build a client-side step-up state machine, which is exactly the failure the platform fact warns about.

`references/75-testing-ci-playbook.md` against the stack/platform CI seam — **half correct**. It correctly emits **no provider YAML**; every block (`:69–98`) is provider-agnostic shell. But it legislates the other side: `:7–14` sets the harness policy ("Prefer current specific extensions… never add deprecated umbrella `@quasar/testing`"), `:16` sets the required test layers, `:65` sets E2E priorities, `:80` requires "Lighthouse or app-specific PWA smoke". These are gates and predicates — the right thing for a stack skill to own — but they are written as prose lists, not as named gates a CI author can bind to, and the file names neither `alaa-testing-strategy` (test design) nor `alaa-gitlab-ci-cd` (provider expression) nor even `$alaa-frontend-devops`, which `SKILL.md:62` and `references/00-topic-map.md:48` both declare owns CI/Docker/deploy. So the pack contradicts its own boundary.

Other own-voice legislation:
- `references/33-ssr-pwa-playbook.md:149` — "For SSR behind Nginx/HAProxy verify: health endpoint/process manager; forwarded headers; known gzip/brotli/static serving; explicit cache headers; server-only secrets." Deploy/infra ground; `alaa-frontend-devops` and `alaa-haproxy` exist and are not named.
- `references/11-review-and-upgrade-checklist.md:48` — "No client-exposed secrets"; `:74` — "Private/auth/payment APIs are not cached by default." Security requirement levels stated as checkbox defaults; `alaa-security-review` not named.
- `references/40-webotp-and-device-trust.md:77` — "fingerprinting/assigned device IDs are terminal-equipment access under ePrivacy Art. 5(3) (EDPB Guidelines 2/2023 v2, Oct 2024)." Legal/compliance doctrine in a frontend stack skill. It is well-sourced, but it is not this skill's ground.
- `references/61-component-usage-atlas.md:9` — "treat server pagination as data flow" for QTable, with no route to `alaa-keyset-pagination`.

### 5. Duplication

Most valuable section. `→` marks the file that should survive.

| Rule | Every file:line stating it | Survives |
|---|---|---|
| **v2→v3 delta set** (wrapper, config ext, env keys, defines, aliases, `vueOptionsAPI`, removals) — the pack's single largest duplication, stated in full **6×** | `10-v2-to-v3-migration.md:27–45`; `11-review-and-upgrade-checklist.md:91–106`; `20-v3-config-and-features.md:56–66`; `21-cli-vite-and-config.md:12–13,20–28`; `22-cli-cookbook-and-examples.md:13–18,52,92–94,178–189`; `80-upstream-deltas-and-live-checks.md:44–72` | **`80`** (canonical delta table) + `22` (executable shapes only). Strip from `10`/`11`/`20`/`21`. |
| `#q-app/wrappers` → `#q-app` | `10:29`; `11:91`; `12-v2-maintenance-playbook.md:27,147`; `21:13,23`; `22:15,27`; `80:46,57,60,68`; `91-agent-authoring-and-dual-runtime.md:17–18` | **`80:46`** table row; `91` keeps it only as an authoring *example*. |
| `process.env.*` → `import.meta.env.QUASAR_*` | `10:30–33`; `11:93`; `12:114–119`; `13-examples-review-style.md:59–74`; `21:25`; `22:86–89`; `33-ssr-pwa-playbook.md:27–28`; `80:48,70` | **`80:48`** + `13:59–74` (the review-comment form). |
| `build.envFolder/envFiles` → `build.env.{folder,file}`; `clientPrefix` default `'QCLI_'`, never `'QUASAR_'` | `10:41`; `11:94`; `20:27,41,55`; `21:24`; `22:75,92`; `31-ssr-pwa-and-security.md:56`; `80:49,70` | **`20:34–56`** (the env contract, with its `✅/❌` pair). Others become pointers. |
| `build.rawDefine` → `build.define`; `build.env` injection → `build.defineEnv`; wrap only real string literals | `10:41`; `11:95`; `20:44–45`; `21:24`; `22:78–81,94`; `80:50,70` | **`22:78–94`** (the only place with the double-stringify anti-pattern). |
| `build.vueOptionsAPI` defaults `false` | `10:42`; `11:96`; `20:59`; `21:26`; `22:46`; `80:69` | **`20:59`**. |
| `build.analyze` / `build.polyfillModulePreload` removed | `10:43`; `11:96`; `21:26`; `80:69` | **`80:69`**. |
| Aliases collapse to sole `@/` | `10:34,37`; `11:97`; `12:79–95`; `13:31–56`; `20:61`; `21:25`; `22:178–189`; `80:51,68` | **`80:51`** + `13:31–56` (review form) + `12:79–95` (v2-only nuance). |
| Custom SW moves to `/src-pwa/sw/` — **and its `sourceFiles` default contradicts** | `10:51` (`'src-pwa/custom-sw'` ← **wrong**); `11:60,99` (`'src-pwa/sw/custom-sw'`); `30-service-worker-excellence.md:78`; `31:17,19`; `32-pwa-injectmanifest-guard.md:7–10`; `33:105`; `80:53,71` | **`32:7–10`** (versioned-location owner). Delete the contradicting `10:51` clause. |
| Exactly one `self.__WB_MANIFEST` | `30:79`; `31:76`; `32:16`; (+`00:38`, `SKILL.md:60` as search terms) | **`32:16`**. |
| `skipWaiting` / `controllerchange` / reload-once orchestration | `30:34–58`; `31:78`; `32:34,44`; `33:131` | **`30:34–58`** (only full treatment). `32` keeps the *risk boundary* framing only. |
| SSR server choice Hono/Express/Fastify/Koa + `/src-ssr/server-assets` | `10:50`; `11:98`; `20:29`; `31:15`; `35-platform-modes.md:20`; `50-modern-experience.md:10`; `80:54,71` | **`35:20`** (mode facts) + `50:10` (the *choice* heuristic). |
| `serve.error()` → `serve.devError()` | `10:50`; `11:98`; `31:16,19`; `80:71` | **`80:71`**. |
| Capacitor `capacitor.config.json` → `.ts`/`.js` via `defineCapacitorConfig()` | `10:12,52`; `11:101`; `20:64`(implied); `35:22,32`; `80:71` | **`35:22`**. |
| Electron preload `.cjs` + `#q-app/electron/preload` + `electron-assets` | `10:53`; `11:102`; `35:23,32`; `80:71` | **`35:23`**. |
| BEX `/src-bex/package.json` `"type": "module"`, default target `chrome` | `10:54,60`; `11:100`; `35:21,26–30`; `80:71` | **`35:21,26–30`**. |
| pnpm v11 `allowBuilds` (`rolldown`, etc.) + empty per-mode `pnpm-workspace.yaml` | `10:54`; `11:105`; `20:64`; `80:103` | **`20:64`**. |
| Node floor `^22.22.0 \|\| ^24 \|\| …`; peers `vue-router >= 5`, `pinia ^2\|\|^3` | `SKILL.md:26`; `10:9–10`; `11:106`; `20:21`; `70-guardrails…:71`; `80:55,72` | **`80`** (single snapshot). |
| **Full upstream version snapshot table** — stated 3× despite `90:7` declaring `20` canonical | `SKILL.md:26`; `20:5–21`; `80:26–36` | **`80:26–36`** only. `90:7` must then point at `80`. |
| "Detect the installed major before any config/env/alias advice" | `SKILL.md:22`; `00-topic-map.md:3`; `21:8–16`; `22:9–18`; `31:13`; `32:10`; `35:3`; `80:39–41`; plus `scripts/check-upstream-versions.mjs:80` | **`SKILL.md:22`** (body rule) + `80:39–57` (the signal table). All references become one-clause pointers. |
| "Follow the lockfile's package manager; never switch" | `SKILL.md:23`; `12:39`; `20:65`; `21:34`; `22:193–197`; `35:40`; `80:102` | **`SKILL.md:23`** + `22:193–197` (Yarn-first worked example). |
| No `vite.config.*` in a Quasar CLI app / `@quasar/vite-plugin` ≠ CLI | `11:45`; `12:49–59,71–74`; `13:9–17` | **`13:9–17`** (review-comment form). |
| Never replace `viteConf.resolve.alias`; merge or use `build.alias` | `21:37,47`; `22:157` | **`21:37,47`**. |
| Vite 8: object `manualChunks` removed; `rollupOptions`→`rolldownOptions`; Oxc/Lightning CSS; CJS interop | `70:27–42`; `80:84–89`; (`21:40`, `22:157` pointers) | **`70:27–42`** (has the code pair) — `80` keeps a one-line delta row. |
| SSR: never read `window`/`document`/`localStorage` in `setup()`/render; use `onMounted` | `11:65`; `12:163`; `13:78–98`; `31:22–39`; `33:5–29`; `45-browser-apis-and-permissions.md:15`; `70:48–49` | **`31:22–39`** (rule) + `13:78–98` (review form). Delete `33:5–29`. |
| SSR: no request/user state in mutable globals; per-request app/store/router/API factory | `11:49,67`; `12:29,135,163–173`; `13:100–119`; `31` (implied); `33:31–46`; `70:50,57` | **`33:31–46`** *or* **`12:163–173`** — pick `31` as the SSR owner and fold both. |
| SSR boot `defineBoot` + `ssrContext` cookie forwarding | `12:137–147`; `22:98–139`; `31:60–64`; `33:48–67` | **`22:98–139`** (exact shapes, both lines). |
| Hydration: keep time/locale/random/viewport out of SSR markup; `useId()`; `data-allow-mismatch` | `11:68`; `31:24,41–52`; `33:69–86`; `66-api-usage-atlas.md:12–17,60–68`; `70:48,53–58`; `80:96` | **`31:41–52`** (Vue 3.5 tools) + `70:53–58` (signature table). |
| `useMeta` for SEO, never `document.title` | `31:91`; `33:88–101`; `64-plugins…:8,10`; `66:7–9` | **`66:7–9`**. |
| Never cache authenticated/payment/profile APIs; purge on logout | `11:74`; `13:123–136`; `30:16,74`; `33:128` | **`30:74`** (§7 security invariants — the only one that states it without an exception). |
| Never blindly precache large media/VOD | `11:75`; `30:20`; `33:129` | **`30:20`**. |
| Install → update → offline verification triad | `SKILL.md:49`; `11:77–78`; `30:64`; `32:36–42`; `33:131`; `50:34`; `75-testing-ci-playbook.md:65` | **`32:36–42`**. |
| `GenerateSW` vs `InjectManifest` choice | `30:82`; `31:9,72–80`; `32` (whole file premise) | **`31:72–80`**. |
| Layout owns `QPageContainer` + `<router-view />`; pages own `QPage`; nested routes over conditional shells | `22:161–175`; `60-components-and-layouts.md:21–23`; `61-component-usage-atlas.md:60–71`; `62-layout-patterns-and-examples.md:36–46` | **`62:36–46`**. Strip the duplicate `Search:` lines at `22:175`/`62:46` (near-identical). |
| Lazy-load route components | `12:151–159`; `21:5`; `22:166–171`; `50:24`; `70:22` | **`70:22`** (perf rule) + `22:166–171` (shape). |
| "Query the installed API via `05` before trusting the atlas" | `SKILL.md:30,60`; `00:7`; `05:53`; `60:3,7`; `61:3`; `64-plugins…:3`; `65-directive-usage-atlas.md:3`; `66:3` | **`05:53`** + one pointer line per atlas. Currently stated 9×. |
| `client`/`server` boot side-scoping and secrets staying server-side | `12:121–131`; `20:55`; `22:100–107`; `31:55–70` | **`31:55–70`**. |
| A11y: overlays move focus in/out; icon-only controls need names; keyboard for virtualized rows | `60:28`; `61:60`; `64:9,17`; `65-directive-usage-atlas.md:39–47`; `70:5–17` | **`70:5–17`**. |
| Reduced motion | `50:26,34`; `64:17`; `65:47`; `66:56–58` | **`66:56–58`** + the existing route to `$alaa-ui-ux-design-system`. |
| Baseline floor Chrome/Edge 111, FF 114, Safari/iOS 16.4 | `20:74,78`; `30:66`; `50:26`; `70:33` | **`20:74`**. |
| Web Push / iOS 16.4 + Home-Screen install / Declarative Web Push | `30:68`; `45:25`; `50:20` | **`30:68`** (SW owner). |
| `setAppBadge` Chromium/WebKit only | `30:70`; `50:20` | **`30:70`**. |
| `beforeinstallprompt` / Richer Install UI / Safari 26 removed installability | `30:68`; `50:18` | **`50:18`** (install/engagement owner). |
| Freeze/avoid reactivity on large virtual-scroll arrays | `61:54`; `70:23` | **`70:23`**. |
| `*-html` props / `QEditor` / uploads as content-safety boundaries | `31:58`; `70:89`; `66:26–31` | **`66:26–31`** (only one with a code pair). |
| Peer/externalize `vue` + `quasar` in packages | `70:62–73` and the `$alaa-mono-package` route at `SKILL.md:56`, `00:48` | **`70:62–73`**, or delete entirely and route to `$alaa-mono-package`. |
| "Run `check-upstream-versions.mjs` before version-sensitive work" | `SKILL.md:24`; `20:7`; `80:7`; `90-maintenance-and-live-checks.md:7` | **`80:7`**. |
| Authority ladder (repo > installed CLI > official docs > references) | `05:5–13`; `80:22` | **`05:5–13`**. |
| Dual-runtime authoring contract | `80:101`; `90:31–33`; `91` (whole file) | **`91`** — or delete `91` and route to `$alaa-prompting-guide` (see §10). |

**Near-identically-named maintenance files.** `80-upstream-deltas-and-live-checks.md` (7,879 B) and `90-maintenance-and-live-checks.md` (2,708 B) overlap on: run-the-script (`80:7` / `90:7`), source allow-list (`80:22,105` / `90:19`), and recheck triggers (`80:24` / `90:14–17`). `90`'s unique content is the UNVERIFIED list (`:17`), posture history (`:21–25`), and script-verification protocol (`:27–29`) — all of which belong in `80` and `91`. **`90` should be retired.**

**The four SSR/PWA files.** `33-ssr-pwa-playbook.md` (3,927 B) contains **no rule not already in `30`, `31`, `32`, `12` or `13`**, except §9 deployment checks (`:139–149`, which is `$alaa-frontend-devops` ground) and the `register-sw` v2/v3 snippet (`:107–120`, which belongs in `22`). **`33` should be retired.** `30`/`31`/`32` have a clean division once `31`'s PWA half (`:72–80`) is trimmed to the `GenerateSW`-vs-`InjectManifest` decision.

**The three atlases.** Contrary to the obvious suspicion, `61`/`65`/`66` are **not** meaningfully duplicative of `60`/`64` — `60` and `64` are pure routing tables (family → file), the atlases carry intent/gotchas. The only real overlap is the `QPageContainer` rule (`60:21–23` vs `61:60` vs `62:36`) and the `05` pointer restated in all five. Per the completeness law, **keep all five**; merge only those two rules and sharpen the router rows. This is the one place where the pack's size is justified.

### 6. Wording-test failures

1. **"never cache authenticated APIs unless explicitly safe"** — `references/33-ssr-pwa-playbook.md:128`. *Self-granted exception* on the pack's most security-critical rule; "explicitly safe" has no external referent, so the agent grants itself the exception. → *"Cache no response whose request carried a credential (cookie, `Authorization`, or a trusted header). Route every such request `NetworkOnly`. To cache one, name the endpoint in `quasar.config` `pwa` config with a written justification and a logout-purge entry."*
2. **"Preserve established asset-base and placeholder-replacement variables unless intentionally changing the SW contract."** — `references/32-pwa-injectmanifest-guard.md:19`. The canonical *"unless intentional"* archetype: the agent editing the file always believes it is intentional. → *"Do not modify asset-base or placeholder-replacement variables in the same change as any other SW edit. Change them alone, and record the before/after values in the change note required at `32:22`."*
3. **"Private/auth/payment APIs are not cached by default."** — `references/11-review-and-upgrade-checklist.md:74`. *Preference verb where a constraint was meant* — "by default" turns an invariant into an overridable setting, and contradicts `30:74`. → *"No private, auth, or payment endpoint appears in any cache route."*
4. **"`*-html` props, `QEditor`, uploads, and custom slot rendering are content-safety boundaries."** — `references/31-ssr-pwa-and-security.md:58`. *Abstract noun standing in for an observable condition*; it names a category and prescribes nothing. → *"Never bind user-controlled text to a `*-html` prop, `Notify.create({ html: true })`, or `QEditor` output without sanitizing through the repo's sanitizer; if none exists, render as text."*
5. **"Auto-submit only if risk policy permits no value review."** — `references/40-webotp-and-device-trust.md:64`. *Abstract noun with no named owner* — "risk policy" is not an artifact an agent can read. → *"Do not auto-submit a WebOTP-filled code. Fill the field, leave the submit control to the user, and keep manual entry enabled."*
6. **"No new `components/`, `stores/`, `pages/` aliases unless local compatibility requires them."** — `references/11-review-and-upgrade-checklist.md:54`. *Self-granted exception*; the agent decides what "requires". → *"Add no alias other than `@/`. If an existing import cannot resolve through `@/`, leave the existing alias untouched and record it under 'migration debt' in the migration plan."*
7. **"Use Jest only when already entrenched or specifically justified"** — `references/75-testing-ci-playbook.md:14`. *Self-granted exception*; "specifically justified" is self-issued. → *"Use Jest only when `package.json` already declares a Jest dependency. Otherwise use `@quasar/testing-unit-vitest`."*
8. **"Prefer `@/` for new imports only when already supported or safely added in v2"** — `references/12-v2-maintenance-playbook.md:79`. *Self-granted exception* ("safely added") plus a *preference verb* on what should be a check. → *"Use `@/` for a new import only if `quasar.config` already declares the `@` alias. Do not add the alias during an unrelated patch."*
9. **"`getUserMedia()` does not formally require it, but out-of-gesture requests are punished/anti-patterns."** — `references/45-browser-apis-and-permissions.md:9`. *A preference where a constraint was meant* — states a fact, issues no rule, so an agent may legitimately call it on load. → *"Call `getUserMedia()` only inside a user-gesture handler, after the primer. Never call it during mount or route enter."*
10. **"keep large `QVirtualScroll` arrays frozen/non-reactive when possible"** — `references/70-guardrails-a11y-performance-monorepo.md:23` (and `references/61-component-usage-atlas.md:54` "when possible"). *"When feasible" family* — no checkable condition, and no threshold defines "large". → *"For any list bound to `QVirtualScroll` that can exceed 500 rows, pass the array through `markRaw`/`Object.freeze` unless a row field is mutated in place; if rows mutate, replace the row object rather than making the array reactive."*

Honourable mention (not in the top ten, same class): `references/10-v2-to-v3-migration.md:37` "A temporary `build.alias` + `ctx.appPaths` bridge **must be documented** migration debt" — documented *where*? No named artifact, though `11:108–148` supplies a plan template that would serve if `10` pointed at it.

### 7. Stale or unverifiable claims

I ran `scripts/check-upstream-versions.mjs` live. It executed cleanly and returned registry data for **2026-07-28**. Every version in this pack is stale, several materially.

| Claim in the skill | Stated at | Live registry, 2026-07-28 | Impact |
|---|---|---|---|
| `@quasar/app-vite` stable = **3.0.1** (2026-07-07) | `SKILL.md:12,26`; `20:11`; `80:31,45`; `10:3`; `11:89`; `21:20`; `22:11` | **3.2.0** (2026-07-22) | **Two minor releases behind.** Every "v3 capabilities" list (`20:23–31`) and the whole delta table predate 3.1 and 3.2. Any config surface added in those minors is invisible to the skill. |
| `quasar` UI = **2.21.1** | `SKILL.md:26`; `20:13`; `80:30,78` | **2.23.3** (2026-07-28, today) | **Two minors behind.** The "Quasar UI 2.18–2.21" section (`20:71–78`) and `80:76–78` are incomplete; `80:78` "No components/deprecations from 2.19–2.21" is now an unbounded claim. |
| `pinia` = **3.0.4**, peer `^2 \|\| ^3` | `SKILL.md:26`; `10:10`; `11:106`; `20:18`; `70:71`; `80:34` | **4.0.2** (2026-07-15) | **Highest-risk stale claim.** Pinia 4 exists; an agent following this skill will tell a team the accepted peer range is `^2 \|\| ^3` and may block or mis-plan a Pinia 4 bump. The actual app-vite 3.2.0 peer range must be re-read. Note `alaa-vue-typescript-clean-code/references/50-quasar-vite-pinia-contract.md:80` ("Pinia 3+ supports Vue 3 only") drifts the same way. |
| `vue-router` = **5.1.0** | `SKILL.md:26`; `20:17`; `80:34` | **5.2.0** (2026-07-15) | Minor; the `>= 5` floor claim survives. |
| `vite` = **8.1.4**, "v3 depends on `vite ^8.1.3`" | `SKILL.md:26`; `20:16`; `80:34,84` | **8.1.5** (2026-07-16) | Patch drift; the dependency-range claim needs re-reading against app-vite 3.2.0. |
| `vue` = **3.5.39** | `SKILL.md:26`; `20:17`; `31:43`; `80:34,96` | **3.5.40** (2026-07-16) | Patch drift; the 3.5 feature claims (`useId()`, `data-allow-mismatch`) remain correct. |
| `@quasar/app-vite` v2 = **2.6.2**, maintenance ~2027-06 | `SKILL.md:12,26`; `20:12`; `80:32,45` | **2.6.2** — confirmed unchanged | Accurate. The v2 posture is the one part of the snapshot still true. |
| `@quasar/extras` = **2.0.2** | `SKILL.md:26`; `20:14`; `80:33` | **2.0.2** — confirmed | Accurate. |
| `workbox-build` = **7.4.1** | `SKILL.md:26`; `20:19`; `80:35,97` | **7.4.1** — confirmed | Accurate; "safe bump, no InjectManifest/GenerateSW behavior change" (`80:97`) still holds. |
| "Quasar UI v3 only planned (input Q3–Q4 2026; hoped Q1 2027), not beta/RC" | `80:80–82` | Registry `beta` dist-tag on `@quasar/app-vite` is `3.0.0-beta.45` (stale tag); no `quasar` v3 line | Consistent with registry; still needs a docs check. |

**Verified from the files themselves (internally consistent, no live check needed):** the v2/v3 shape split (`80:44–56`); the `#q-app` / `#q-app/wrappers` split; `.cjs`/`.mjs` config drop; `clientPrefix` default `'QCLI_'`; `serve.error()`→`serve.devError()`; `defineCapacitorConfig()`; Electron `.cjs` preload; `/src-bex/package.json`. The **one internal inconsistency** is the `sourceFiles.pwaServiceWorker` default (`10:51` vs `11:99`/`31:17`/`32:7`) — this cannot be resolved from the files and needs a live docs check.

**Needs live web research before Phase 2 ships it** (the skill flags most of these itself at `references/90-maintenance-and-live-checks.md:17` — creditable honesty):
- `@quasar/app-vite` 3.1 and 3.2 changelogs: new/changed config keys, whether the delta table is still complete, and the current peer range for `pinia` (does 3.2.0 accept `^4`?) and `vite`.
- Quasar UI 2.22 and 2.23 release notes: components, deprecations, behaviour changes (`20:71–78` and `80:76–78` must be extended).
- `quasar describe` in app-vite v3.2: does the subcommand still exist, and does `@quasar/app-vite` still declare a `quasar` bin? **This is load-bearing** — `scripts/query-installed-quasar-api.mjs:98–102` fails hard if `bin` is absent, and the entire "authority" posture (`SKILL.md:28–36`, `references/05-authority-and-api-lookup.md`) collapses to the manual fallback.
- Node engine range for 3.2.0 (`^22.22.0 || ^24 || ^26 || ^28 || ^30` at `SKILL.md:26`).
- `@quasar/testing-*` extension v3 compatibility — explicitly UNVERIFIED at `10:11` and `90:17`.
- Browser claims in `30`/`40`/`45`, all dated 2026-07-08: Static Routing API outside Chromium (`30:28`); Declarative Web Push in Chromium (`30:68`); `<geolocation>` element ship version and rollout (`45:53`, claimed "around Chrome 144", "~54% recovery"); Safari grant-expiry windows (`45:9`); Chrome Local Network Access (`45:72`); Safari 26 Advanced Fingerprinting Protection and Firefox 145 canvas randomization (`40:73`); FingerprintJS v5 MIT licensing (`40:75`); the exact default dotenv file list (`20:53`, self-flagged).

### 8. Router audit

**Reference count:** 30 files (29 targets + the router itself). **Router location:** `references/00-topic-map.md` — correct for ≥9 references.

**Conformance: FAILS on "one router per skill, never two."** There are **six** routing surfaces:

1. `references/00-topic-map.md` — 25 table rows + 9 search-routing bullets + 2 route-out bullets. The intended router.
2. `SKILL.md:45` — a **complete second router** compressed into one line: *"Detailed routing is owned by `00`: exact APIs/source drift `05`; migration/v2 `10`–`13`; v3 config/CLI/shapes `20`–`22`; SSR/PWA/SW/platform modes `30`–`35`; OTP/device trust/permissions/modern UX `40`–`50`; components/layouts/directives/plugins/composables/options/utils `60`–`66`; quality/testing/live deltas/legacy/maintenance `70`–`91`."* It announces `00` owns routing and then routes anyway.
3. `SKILL.md:47–56` — "Mandatory pairings", 8 more routing rules.
4. `references/60-components-and-layouts.md:11–19` — family → file table (8 rows).
5. `references/64-plugins-composables-directives-options-utils.md:5–11` — surface → file table (5 rows).
6. `references/85-legacy-skill-coverage.md:7–39` — legacy-name → file, with a **broken** numbering scheme.

(`references/35-platform-modes.md:7–15` is a seventh, mode → also-load.)

**Observable-condition audit of the 25 `00` rows.** The prescribed form is *"You are about to `<observable situation>` → read `<file>`"*. **Zero rows use it.** Rows split roughly:

- **Observable enough to fire correctly (9):** `:7` "Exact installed component/directive/plugin props, events, slots, methods, values, options"; `:8` "v2 -> v3 plan/execute"; `:12` "`quasar.config`, aliases, `extendViteConf`, env, proxies, lazy loading, upgrades"; `:16` "Custom SW/InjectManifest boundary changes"; `:18` "SPA/SSR/PWA/BEX/Capacitor/Cordova/Electron choice"; `:19` "WebOTP/SMS autofill/fingerprinting/device trust/passkeys"; `:20` "Browser APIs/permissions: audio, camera, geolocation, …"; `:24` "Layouts/`view`/drawers/route-owned layouts"; `:30` "Old `quasar-*` skill names". These name a symbol, a file, or a user-visible task.
- **Heading mirrors that will not fire (10):** `:10` "Review style; correct/wrong examples"; `:11` "v3 capabilities/env/version truth/Quasar UI 2.18–2.21"; `:13` "Exact config/boot/env/alias shapes, either line"; `:21` "Mode/install UX/perceived performance/modern experience"; `:22` "Component family choice"; `:23` "Component intent/alternatives/gotchas/search terms"; `:27` "A11y/performance/monorepo/tree-shaking"; `:28` "Testing extensions/layers/CI"; `:29` "Versions/v2-v3 split/Vite 8/Router 5/Vue 3.5"; `:31` "Skill maintenance". These are the destination file's own title restated — an agent cannot recognise itself in "Component family choice."
- **Ambiguous / overlapping (6):** `:9` "Maintain v2 env/aliases/boot/routing/Pinia" vs `:8`; `:14` "SW/offline/cache/update/performance/debug/push/badging/background sync" vs `:15` vs `:16` vs `:17` — four adjacent rows all reachable from "I am editing a service worker", with no disambiguating condition; `:26` "Plugins/composables/directives/options/utils" vs `:23`.

The **search-routing block** (`:35–43`) is materially better than the table: it routes by literal symbol (`__WB_MANIFEST`, `OTPCredential`, `ssrContext`, `getUserMedia`, `clientPrefix`) and is the part of the router that will actually fire. With 30 references the symbol index, not the topic table, is doing the real work — Phase 2 should invert the emphasis.

**Dangling reference paths (internal):**
- `references/31-ssr-pwa-and-security.md:13` → `` `70-...` `` — should be `80-upstream-deltas-and-live-checks.md`.
- `references/35-platform-modes.md:3` → `` `70-...` `` — same.
- `references/85-legacy-skill-coverage.md:34` → `` `40` `` (should be `61`); `:35` → `` `10` `` (should be `21`/`62`); `:36` and `:37` → `` `50` `` (should be `66` / `65`); `:38` → `` `20` `` twice and `` `21` `` (should be `31`/`33` and `30`/`32`); `:33` → `` `10` `` (should be `21`).

**Dangling cross-skill paths:** none. All seven external `references/…` paths resolve, and each names its owning skill alongside the path (`references/30-service-worker-excellence.md:3`, `references/50-modern-experience.md:30–32`, `references/20-v3-config-and-features.md:78`) — this convention is followed correctly throughout.

### 9. Scripts audit

**`scripts/check-upstream-versions.mjs` (3,022 B, 90 lines)**

- **Does:** fetches full packuments for `quasar`, `@quasar/app-vite`, `@quasar/extras`, `vite`, `vue`, `vue-router`, `pinia`, `workbox-build`, `workbox-core` from `registry.npmjs.org`; prints JSON with `latest` + publish date per package, all dist-tags for `@quasar/app-vite`, and `latestStableByMajor.v2`/`.v3` (`:23–28` filters prereleases with `!v.includes('-')` and sorts by 3-segment numeric compare).
- **Would it run?** **Yes — verified.** Ran clean here, exit 0, ~4 s, correct output including `latestStableByMajor.v2 = 2.6.2` and `.v3 = 3.2.0`.
- **Fragile paths:** (a) **no request timeout** (`:31–53` sets no `timeout` option and no `request.setTimeout`) — a stalled registry connection hangs the agent indefinitely with no diagnostic; (b) **no proxy support** — raw `https.get` ignores `HTTPS_PROXY`/`NO_PROXY`, so it fails opaquely in proxied environments; (c) requests the **full packument** rather than sending `Accept: application/vnd.npm.install-v1+json`, so `quasar` alone transfers several MB (it needs `payload.time` for publish dates, so full is justified for the two packages using `latestStableByMajor`, but not for the other seven); (d) **fully sequential** (`:83` `for … await`) — 9 round trips where `Promise.all` would do one.
- **`--help` / self-test:** **neither.** Any argument is silently ignored. Compare with the sibling script, which has both.
- **What it would find today:** exactly the drift in §7 — app-vite 3.2.0 vs the pinned 3.0.1, quasar 2.23.3 vs 2.21.1, and **pinia 4.0.2 vs the documented `^2 || ^3` peer range**. Every file that carries a snapshot (`SKILL.md:26`, `20:5–21`, `80:26–36`) is wrong, and `references/90-maintenance-and-live-checks.md:9` ("update every occurrence and snapshot date, never only the snapshot") has not been executed since 2026-07-10.

**`scripts/query-installed-quasar-api.mjs` (5,631 B, 150 lines)**

- **Does:** walks upward from `--project` (default `cwd`) to the nearest `package.json` declaring `@quasar/app-vite` (`:43–58`), resolves the installed `@quasar/app-vite` and `quasar` via `createRequire` from that manifest (`:84–96`), locates the CLI bin from the package's own `bin` field (`:98–111`), prints the resolved project and both installed versions to **stderr** (`:130–132`, keeping stdout clean for the CLI's output), then `spawnSync`s `node <bin> describe …` with `--no-color` appended and `FORCE_COLOR=0`/`NO_COLOR=1`, propagating the child exit status (`:134–143`).
- **Would it run?** **Yes — verified.** `--help` prints usage and exits 0; run outside a Quasar project it fails with the correct actionable message ("No Quasar CLI + Vite project declaring @quasar/app-vite was found from /tmp upward"). Could not verify against a real Quasar project (none available here).
- **Quality — this is the best-engineered artifact in the pack.** No `__file__`-relative path fragility, no temp directories, no package-manager assumption, no network. `:104–110` is genuinely defensive: it `realpathSync`es the bin and **refuses to execute a CLI that resolves outside the installed package** — a symlink-escape guard most skill scripts lack. `:140–142` distinguishes "no exit status (signal)" from a nonzero exit.
- **Fragile paths:** one, and it is load-bearing. `:98–102` assumes `@quasar/app-vite` declares a `quasar` bin entry. If it does not (the Quasar global CLI is a separate package, `@quasar/cli`), the script fails with "does not expose a quasar CLI bin entry" and the pack's entire exact-API authority chain (`SKILL.md:28–36`) drops to the manual fallback at `references/05-authority-and-api-lookup.md:38–41`. `references/90-maintenance-and-live-checks.md:14` flags this as needing live verification and it has not been done. Secondary: `parseArguments` (`:60–82`) treats *any* non-`--project` argument as a describe arg, so a typo'd flag is passed through to the CLI rather than caught — acceptable by design (it is a bridge), but it means `--projct ../app` silently becomes a describe argument.
- **`--help` / self-test:** `--help`/`-h` present (`:65`, `:117–120`) with three worked examples. No self-test; the verification protocol is prose at `references/90-maintenance-and-live-checks.md:27–29` (test one v2 and one v3 project, a missing-project failure, a narrow symbol, and a `list` query) — correct content, but it is a checklist a human must run, not a script.
- **What it would find today:** on an Alaa `client` checkout, the installed app-vite/quasar versions and exact `QTable`/`QUploader`/`QSelect` APIs — the correct, non-staling answer. This script is the reason the pack can afford to be non-exhaustive, and it should be preserved unchanged apart from verifying the `bin` assumption.

### 10. Rewrite brief for Phase 2

**Body budget.** Current always-loaded body 6,716 B. Target sections:

| Section | Budget |
|---|---|
| Purpose and posture (drop the version snapshot, keep the v3-first stance) | 500 B |
| Version rules: detect installed major; lockfile package manager; pointer to `80` for all numbers | 700 B |
| Authority and exact APIs: the ladder in one sentence + the one command | 700 B |
| Routing: **one** pointer to `00-topic-map.md` + mandatory pairings | 1,400 B |
| Companions and disclaimers: in-batch + out-of-batch owners, **both** `$name` and `/name` forms | 1,600 B |
| When NOT to use | 350 B |
| Final response contract | 550 B |
| **Sum** | **5,800 B** |
| **+15%** | **6,670 B** |

**6,670 B ≤ 6,716 B — the body does not grow.** The space for the out-of-batch disclaimers and dual trigger forms is bought by deleting `SKILL.md:26` (snapshot → `80`), `:45` (second router → `00`), and `:60`'s concept-term dump (→ `00:35–43`).

**Target file list.**

*Retire to `_to_delete/`:*
- `references/33-ssr-pwa-playbook.md` (3,927 B) — every rule already lives in `30`/`31`/`32`/`12`/`13`. Move `:107–120` (`register-sw` v2/v3) → `22`; move `:139–149` (Nginx/HAProxy SSR deploy) → route to `$alaa-frontend-devops` / `/alaa-frontend-devops`; delete `:126` ("educational VOD apps" — `vod` is deprecated).
- `references/90-maintenance-and-live-checks.md` (2,708 B) — merge `:12–19` (verify-live triggers + UNVERIFIED list) and `:27–29` (script-verification protocol) into `80`; `:21–25` (posture history) into `80`; `:31–33` into `91` or `$alaa-prompting-guide`.

*Restructure (Class 5):*
- `references/10-v2-to-v3-migration.md` → keep §1 sequence and §6 per-mode gate; **delete §2/§3 delta tables** (canonical in `80`); **add a failure-class block**: `quasar prepare` fails / blocking App Extension / SSR builds but 500s / PWA registers but never updates / Capacitor `www` dirty — each as symptom → diagnosis → smallest retry → escalation. Fix `:51`'s wrong `sourceFiles` default.
- `references/11-review-and-upgrade-checklist.md` → delete §7 canonical deltas (`:88–106`, wholly duplicative of `80`); keep §1 repo-assessment emitter (`:18–40`) and §8 plan template (`:108–148`) — those are the file's real value; convert §§2–6 checkboxes into a short *"stop the migration if"* list.
- `references/85-legacy-skill-coverage.md` → fix `:33–38` to the current numbering.
- `references/31-ssr-pwa-and-security.md:13` and `references/35-platform-modes.md:3` → repoint `70-...` to `80-upstream-deltas-and-live-checks.md`.
- `references/91-agent-authoring-and-dual-runtime.md` → **survives, but only as a Quasar-specific delta.** `alaa-prompting-guide` owns agent authoring; `:22–37` (shared rules, runtime table) is generic and should be deleted with a route to `$alaa-prompting-guide` / `/alaa-prompting-guide` and its `references/50-effort-and-thinking.md`. What genuinely survives is `:5–20` (the `✅ Do / ❌ Don't` convention *with Quasar examples*), `:39–46` (why the two scripts exist), and `:48–54` (the version-sweep checklist). Delete the GPT-5 pins at `:3` and `:32`. Expected size after: ~1,600 B, down from 3,936.
- `references/00-topic-map.md` → **the main Phase-2 work.** Rewrite all 25 rows to observable conditions ("You are about to edit a file under `src-pwa/` → read `32`, then `30`"); disambiguate the four SW rows (`:14–17`); promote the symbol index (`:35–43`) above the topic table; extend `:45–48` "Route out" with every out-of-batch owner and both trigger forms.

*Merges (from §5, no content lost):* delta set → `80` only; version snapshot → `80` only; env contract → `20` only; boot shapes → `22` only; SSR browser-guard and request isolation → `31` only; layout ownership → `62` only; install/update/offline triad → `32` only; auth-cache invariant → `30:74` only, with the `unless explicitly safe` exception removed.

*Keep unchanged (completeness law):* `61`, `65`, `66`, `45`, `30`, `05`, `20`, `22`, `70` — all earn their length. **Do not shorten the atlases.**

**Genuinely NEW capability gained: yes, three files.**

1. `references/34-frontend-failure-and-degradation.md` — the §2 criterion-2 hole. SSR render failure (what the server returns, whether it falls back to SPA shell); API-unreachable UX contract; the offline degradation matrix (which routes work with no network, which degrade, which hard-fail); stale-precache recovery and the kill-switch SW (currently one clause at `30:56`); each as symptom → diagnosis → smallest retry → escalation. Routes all doctrine to `$alaa-reliability-sla` / `/alaa-reliability-sla`.
2. `references/36-client-observability-contract.md` — the §2 criterion-4 hole. What a browser client emits on an unhandled error, a SW lifecycle transition, and a failed update; sampling; PII exclusion; what happens when the collector is unreachable. **Emits no names** — every field name, event name and metric routes to `$alaa-services-contract`, requirement levels to `$alaa-observability-soc`.
3. `references/41-step-up-and-permission-hints.md` — **the highest-value single addition in this audit.** Three rules that exist nowhere in the pack and that a frontend agent will otherwise get wrong: (a) the gateway is non-blocking for TOTP step-up, so absent proof and invalid proof are indistinguishable downstream — the client renders the backend's denial and never infers step-up state itself; (b) `verified_until` in the response **body is ISO 8601** while the `X-TOTP-VERIFIED-UNTIL` header is Unix epoch seconds and is backend-only — a client parser must read the body as ISO 8601 and must never synthesize or forward the header; (c) the ≤512-byte permission bitmap is a **UI hint, not an authorization decision** — preserve that framing, and route the decoder to `$alaa-permission-generator` and the identifier codec to `$alaa-crockford-base32-codecs` (whose JS codec frontend code must match, enforced by `scripts/codec-conformance.sh`). Trust doctrine routes to `$alaa-trust-gateway-auth`; this file states only the frontend consequences. `40-webotp-and-device-trust.md` then sheds `:79–86` (server-side fusion pipeline) to that boundary.

Additionally, `references/00-topic-map.md`'s "Route out" section gains rows for `tusd-upload-platform` (QUploader/tus), `alaa-shaka-player` (VOD/media), `alaa-keyset-pagination` (QTable server pagination, QInfiniteScroll), and the object-storage skills — no new file needed.

**Net effect:** ~6.6 KB retired, ~10 KB of duplication collapsed, ~7 KB of genuinely new capability added, references land near 143 KB — flat in size, materially higher in coverage, with the body unchanged.

### 11. Gap no existing skill can own

**None that warrants a new skill.**

The closest candidate is a **browser-client telemetry emission contract**: what a frontend is permitted to emit (unhandled errors, web-vitals samples, SW lifecycle transitions), over what transport (`sendBeacon` vs `fetch(keepalive)`), at what sampling rate, with what PII exclusion, and how it degrades when the collector is unreachable. Evidence that it is genuinely unowned: `alaa-services-contract` owns names and values but not the browser transport or its failure mode; `alaa-observability-soc` owns requirement levels and gates, not client emission; `alaa-frontend-developer` `references/41-lighthouse-and-web-vitals.md` owns *scoring*, which is a measurement activity, not a production emission path; and this skill's only occurrence of the word "observability" (`references/32-pwa-injectmanifest-guard.md:32`) treats it as a low-risk cosmetic change.

But this is a reference-sized gap, not a skill-sized one. It should be filled as `references/36-client-observability-contract.md` in this skill (per §10), taking every *name* from `alaa-services-contract` and every *requirement level* from `alaa-observability-soc`. Creating a new skill for it would add a seventh routing surface to a pack that already has six.


---

## Appendix D — `alaa-ui-ux-design-system`

### 1. What this skill is today

**Subject.** The visual-design and UX decision layer for the Vue 3 + Quasar + Vite app family (Tailwind or Bootstrap per repo): direction-setting, design tokens/theming, typography and colour, visual-style vocabulary, layout and landing IA, component-state design, UX writing, motion language, modern-CSS adoption tiers, icons/assets, a11y patterns, and a blocking gate list.

**Register.** Senior design-lead prose, unusually good by fleet standards: a three-tier authority model (Gates / Defaults / Taste, `SKILL.md:22-26`) that is stated once and then actually honoured in the references; honest trade-off tables with a "Do not use for" column (`40-styles-and-visual-language.md:9-20`); explicit anti-pattern blocks in all 12 topic files; explicit anti-process-theatre rules (`10-design-workflow.md:6-11`). It reads like a design system, not a checklist.

**Shape.** 15 files, 74,012 bytes.

| File | Bytes |
|---|---|
| `SKILL.md` | 11,575 (frontmatter+description 687; **always-loaded body 10,888**) |
| `agents/openai.yaml` | 313 |
| `references/` (13 files) | **62,124** |
| — `70-motion-and-modern-css.md` | 8,677 (largest) |
| — `30-typography-and-color.md` | 5,593 |
| — `10-design-workflow.md` | 5,407 |
| — `60-components-states-and-ux.md` | 5,054 |
| — `20-design-tokens-and-theming.md` | 4,970 |
| — `80-icons-assets-and-imagery.md` | 4,732 |
| — `40-styles-and-visual-language.md` | 4,574 |
| — `85-accessibility-patterns.md` | 4,443 |
| — `55-component-library-and-governance.md` | 4,197 |
| — `90-quality-gates-and-review.md` | 3,984 |
| — `50-layout-landing-and-ia.md` | 3,700 |
| — `35-ux-writing-and-microcopy.md` | 3,444 |
| — `00-topic-map.md` | 3,349 |

Ships no `scripts/`, no `assets/`, no `templates/`, no `__pycache__`. Body-to-reference ratio 1:5.7 — the body is 17.5% of the pack, which is why class 10 bites: ~4,027 of those 10,888 body bytes are a verbatim second copy of `00-topic-map.md`.

Per-section body sizes (measured): Purpose 608, Cross-agent portability 806, Design authority model 891, Ownership 983, When to use 888, When NOT to use 381, Quick start 922, **Routing map 1,949**, **Mandatory cross-topic rules 2,078**, Companion chooser 782, Maintenance rules 600.

### 2. Ten-criteria verdict

| # | Criterion (domain translation) | Verdict | Evidence |
|---|---|---|---|
| 1 | Correctness/testability = visual-regression + a11y testing; is a token change provable? | **FAILS** | `85-accessibility-patterns.md:47` is the entire test design: "keyboard-only walk … automated scan (axe or equivalent) **when tooling exists** … screen-reader smoke". Zero occurrences of "visual regression", "snapshot baseline", "golden". No rule makes a token change provable — nothing says which surfaces a token edit touched or how the diff is shown. `alaa-testing-strategy` (owner of the six proof levels) is never named; silence, so FAILS not NOT-OWNED. |
| 2 | Failure behaviour = the designed states (empty, loading, partial, error, offline, permission-denied, slow-network) | **FAILS** (closest to passing) | Strong on seven of eight: `60-components-states-and-ux.md:7-10` (default/hover/focus-visible/active/disabled/loading/error/empty/partial-data), `:45` ("zero items, one item, thousands of items, slow network, offline"), `:43` error states offer recovery, `90:35` checklist row. But **"permission" appears zero times in the entire skill** — the permission-denied state, the one that matters on `client` with its 512-byte bitmap, is not designed. No stale-data or degraded-dependency state either, and `alaa-reliability-sla` (degradation doctrine) is never named. |
| 3 | Security = what a component may render from untrusted content; clipboard/paste; UI affordance implying an authorization it lacks | **FAILS** | Zero occurrences of `v-html`, "sanitiz", "XSS", "untrusted", "clipboard", "paste" (as an input event), "tenant". Nearest miss: `90-quality-gates-and-review.md:48` "the UI misleads (fake affordance…)" — that is visual honesty, not authorization. The correct `client` framing (permission bitmap is a UI hint, not an authorization decision) is nowhere, so an agent following this skill will hide a control and consider the capability gated. `alaa-security-review` never named. Note the sibling skill *does* carry the rule this one lacks: `alaa-quasar-app-vite-v3/references/70-guardrails-a11y-performance-monorepo.md:89` "Audit content-safety in `*-html` props, `QEditor`, uploads, and user-controlled labels in custom slots." |
| 4 | Observability = is a UI failure diagnosable at all? | **FAILS** | Zero occurrences of "trace", "correlat", "support ID", "request ID". `35-ux-writing-and-microcopy.md:19` correctly bans raw codes ("never raw codes alone") but never supplies the complement — a copyable reference the user can quote and support can join to a server trace. `60:29` toasts auto-dismiss in 3–5s and are the only error channel described for async failure: a UI failure that vanishes in 4 seconds leaves no artifact. `alaa-observability-soc` never named. |
| 5 | Concurrency/load = behaviour under slow networks and long lists | **FAILS** | Partial: `60:28` skeletons past ~300ms with reserved space; `60:18` press feedback within ~100ms; `60:45` "thousands of items, slow network"; `70:82` `content-visibility: auto`/`contain`. Missing: zero occurrences of "virtual"/"virtualization" — the design rule for when a list stops being a list is absent, and Quasar's official `QVirtualScroll`/`QInfiniteScroll` are never named even though the fleet preference is to wrap official capabilities. Zero occurrences of "optimistic"; no design for concurrent mutation (two tabs, conflicting edit), no interaction-latency budget beyond the 100ms press. |
| 6 | Clean code, SOLID, design patterns (design-layer: component API shape) | **SATISFIED** | `55-component-library-and-governance.md:11-18` is the strongest passage in the pack: closed enum variants mapped to tokens, "Never accept raw visual values as props (`color="#2563EB"`)", no boolean explosion, slots for composition / props for configuration, one namespace per repo. Rule of three at `:7`. Correctly delegates the code half: "`$alaa-vue-typescript-clean-code`" at `:16` and `:49`. |
| 7 | Algorithm/data-structure with stated complexity budgets (design-layer: rendering and asset budgets, theme-matrix size) | **FAILS** | Some numbers exist (`70:69` stagger 20–50ms, cap ~600ms, stop after ~10 items; `70:81` compositor-only). But no frame budget (16ms/60fps appears nowhere), no image weight ceiling (`80:29` says AVIF/WebP with no KB budget), no font byte budget (`30:34` says "subset" with no target). The Lighthouse budget is delegated with a live path (`90:19` → `$alaa-frontend-developer references/41-lighthouse-and-web-vitals.md`) — but the skill also *restates the number itself* twice (`90:19`, `10:22`), creating a second source of truth. Worst gap: the theme matrix is combinatorial (light × dark × 3 density tiers × LTR/RTL × `prefers-contrast` × `prefers-reduced-transparency` = 24+ renderings of every component) and the skill never acknowledges the explosion or says which cells must be verified. |
| 8 | Configurability = theming, density, RTL, locale as configuration with validated defaults and boundary validation | **FAILS** | Configuration axes are present and good: theming `20:5-35`, density three-tier table `20:47-54`, digits `30:33`, Jalali `35:30`. **Boundary validation is entirely absent.** `20:13-15` says "define all of these once per theme" with nothing that detects a missing role; `30:19` names the failure ("a second slightly-different gray because the token was not found") without stating the lookup or fallback rule; no rule rejects a theme whose pairs fail contrast. And the shipped defaults are themselves invalid — see §6 item 1. |
| 9 | Speed of development and debuggability | **SATISFIED** | Genuine speed instruments: `SKILL.md:63-67` and `10:6-11` scale-the-process (explicitly "that is process theater"), the copy-paste `oklch`/`light-dark()`/`@property` snippet `20:27-35`, the density table `20:47-54`, the four starter palettes `30:53-58` (correct in *form*, wrong in *values*), the style trade-off table `40:9-20`, the severity-ordered review pass `90:26`, and the 31-term "Good first searches" retrieval aid `00:53-83`. Caveat recorded under class 9: the trigger "a UI 'looks unprofessional' and the cause is unclear" (`SKILL.md:48`) has no matching diagnostic reference — the promise routes nowhere. |
| 10 | Documentation — what shipped, how operated, how it fails | **SATISFIED** | `10:51-60` MASTER.md + `design-system/pages/<page>.md` override model with an explicit retrieval rule and a no-duplication rule; `55:26-28` per-component docs (purpose, variants, state coverage, a11y notes, one ✅/❌ pair); `55:34` deprecate-loudly with migration and deletion; `80:45` "document the export set in MASTER.md"; `90:44` unchecked boxes are stated. |

**Standing preference 1 — wrap official capabilities:** SATISFIED and exemplary. `55:19-24` "Quasar posture: wrap, don't fork" ("If a wrapper only forwards props with no design decision, delete it"); `70:60` keep QMenu/QTooltip until anchor positioning settles; `70:71` refuses to add animation libraries; `80:17` prefers `@quasar/extras`.
**Standing preference 2 — uniformity over local optimality:** SATISFIED. `40:24` "One style per product"; `55:17` one namespace per repo; `55:33` never fork a shared component per page; `20:69` "One source of truth: semantic tokens feed Tailwind, Bootstrap, and Quasar".

**RTL / Persian verdict — afterthought, not first-class.** It is present in five scattered lines (`30:26-34`, `35:24-30`, `50:15`, `85:10`, `90:18`) and there is no RTL reference file. What is missing is exactly what breaks a Persian UI: `unicode-bidi` and "bidi" appear **zero times**, so the `client` house pattern (direction in CSS with `unicode-bidi: isolate`, inserting no characters) is not codified and an agent will reach for LRM/RLM control characters instead — `35:29` "mark direction so punctuation does not scramble" states no mechanism, and `85:57` bans "mixed-direction text left to the browser to guess" with no positive replacement. Icon mirroring is absent from `80-icons-assets-and-imagery.md` entirely — no rule that chevrons/arrows/back/undo mirror while clock/checkmark/play/logo do not, which is the single most common RTL design defect. Directional motion is never flipped (`70` has no `dir` awareness — a slide-in-from-left is wrong under RTL). LTR islands inside RTL forms (email, URL, phone, IBAN, code) are unaddressed. Chart axis order under RTL is unaddressed (`60:47-54`). Progress/slider direction unaddressed.

### 3. Defect classes actually found

**Class 1 — stale hardcoded model pins.** `SKILL.md:16` "OpenAI Codex/GPT-5.x agents and Claude (Opus/Sonnet/Fable) agents". Consequence: goes stale silently and gets copied forward; also materially wrong today, since Fable is an opt-in specialist and is listed here as a peer tier. The whole `## Cross-agent portability` block (`SKILL.md:14-18`, 806 bytes) is runtime/model doctrine owned by `/alaa-prompting-guide` (`$alaa-prompting-guide`) and should be one pointer line.

**Class 2 — trigger syntax.** 38 `$alaa-*` occurrences, **zero** `/alaa-*`. Every one of these is a cross-runtime call site and needs both forms: `SKILL.md:10, 31, 32(×2), 33, 54, 55, 64, 119, 123, 129, 130, 131, 133`; `00-topic-map.md:51`; `10:74`; `20:82(×2)`; `50:61`; `55:16, 49(×2)`; `60:71(×2)`; `70:7(×3), 83`; `80:31, 64(×2), 65`; `85:49`; `90:19, 28, 55, 56`. Exception, correctly: `agents/openai.yaml:4` is Codex-only metadata and stays `$`-only.

**Class 3 — duplication between body and references.** `SKILL.md:70-95` (Routing map, 1,949 B) is a verbatim second copy of `00-topic-map.md:5-30`; `SKILL.md:97-123` (Mandatory cross-topic rules, 2,078 B) is a verbatim second copy of `00-topic-map.md:32-51`. 4,027 B = **37% of the always-loaded body** is a duplicate of a file that is one hop away. This is also a **two-router violation**: `SKILL.md:67` tells the agent to start at `00-topic-map.md` and then immediately reproduces it.

**Class 4 — project-specific content in an always-loaded body.** `SKILL.md:61` enumerates repo artefacts (`DESIGN.md`, `design-system/`, `tailwind.config`/`@theme`, Bootstrap variable overrides, `app.scss`); `SKILL.md:119` hardcodes another skill's reference filename *and* a Lighthouse number. Both belong in `10-design-workflow.md` / `90-quality-gates-and-review.md` where they already partly live.

**Class 5 — competing ordered procedures.** `SKILL.md:59-68` "Quick start 1–5" and `10-design-workflow.md:13-60` "Step 1–4" are two ordered procedures for the same task with different step counts and different first steps ("read AGENTS.md" vs "design brief"). Related off-by-one: `90:34` checklist item reads "Gates 1–**10** above pass" while the gate list runs to **11** (`90:19`) — the performance gate is silently excluded from the pre-delivery check.

**Class 6 — description with no "do not use for": NOT FOUND.** `SKILL.md:3` ends with a real exclusion ("Do not use it for pure frontend engineering (SSR, hydration, auth, PWA, performance plumbing) with no visual-design decision"). This is the best description in the batch. Residual: the two other exclusions that exist in the body (`SKILL.md:55` exact Quasar API lookup, `:57` mechanically applying an existing complete system) are absent from the description, which is where triggering is decided.

**Class 7 — fragile tooling: NOT FOUND** (ships none — which is itself the §9 finding).

**Class 8 — shipped `__pycache__`: NOT FOUND.** Clean.

**Class 9 — unnamed gaps against §2.** Criteria 1, 3, 4, 5, 7, 8 fail with no gap named anywhere in the pack. Corroborating: `alaa-reliability-sla`, `alaa-testing-strategy`, `alaa-security-review`, `alaa-observability-soc`, `alaa-project-constitution` get **zero mentions**; only `alaa-low-noise` is named, once (`SKILL.md:64`). Plus the dangling trigger at `SKILL.md:48` ("a UI 'looks unprofessional' and the cause is unclear") with no diagnostic reference behind it.

**Class 10 — body larger than it needs to be.** 10,888 B against 13 references. 4,027 B is class-3 duplication; a further ~1,590 B (`When to use` 888 + `When NOT to use` 381 + part of `Purpose`) restates `SKILL.md:3`; `Companion chooser` (782 B) restates `Ownership` (983 B).

**Class 11 — no stated companion boundary: NOT FOUND, but self-contradictory.** `SKILL.md:28-34` + `126-133` is the batch's most explicit boundary statement. It contradicts itself: `SKILL.md:32` assigns "transition props, `app.scss`" to `$alaa-quasar-app-vite-v3`, then `20:67` legislates `app.scss` brand variables and `setCssVar`, and `70:71` legislates `transition-show`/`transition-hide` values. It also names only frontend siblings — no out-of-batch owner appears anywhere.

**Additional, not in the listed classes.** `70-motion-and-modern-css.md:5` points at `$alaa-frontend-developer` `references/25-modern-css-and-motion.md`, which **does not exist** in that skill's reference directory — a dangling cross-skill path, and a historical migration note that should simply be deleted.

### 4. Boundary map

**(a) Legitimately owns.** Design direction and the product-intent → direction mapping; the token architecture and semantic role set; density tiers; palette construction and contrast targets; type scale and Farsi/Latin pairing; the visual-style vocabulary with its "do not use for" column; layout/landing/IA defaults and CTA economy; the state-coverage deliverable; UX writing and Farsi register; the motion taste contract; icon/asset/favicon/OG discipline; the blocking gate list and the design-review severity model; MASTER.md persistence. **Plus, per this programme's assignment: RTL and Persian typography as a first-class configuration axis** — which it does not currently discharge.

**(b) Must disclaim, and who owns it.**

| Ground | Owner it must name |
|---|---|
| The quality bar itself | `alaa-project-constitution` (`/alaa-project-constitution`) |
| Every registered NAME and VALUE: metric/event names, Jalali-vs-Gregorian wire format, permission-bit meanings, digit-normalization form | `alaa-services-contract` |
| Requirement levels and gates for anything emitted from the UI | `alaa-observability-soc` |
| Review triggers and threat classes for untrusted content / `v-html` / paste | `alaa-security-review` |
| Degradation doctrine behind the offline/slow/partial states | `alaa-reliability-sla` |
| Test design and the six proof levels behind "keyboard walk + axe + SR smoke" | `alaa-testing-strategy` |
| Pre-implementation design of a page/flow before pixels | `alaa-system-design` |
| Output discipline | `alaa-low-noise` (already named, `SKILL.md:64`) |
| Quasar component and framework mechanics | `alaa-quasar-app-vite-v3` (named, then violated) |
| Vue/TS code shape, per-language pattern judgment | `alaa-vue-typescript-clean-code` (named, correctly) |
| Frontend delivery discipline, Lighthouse scoring, browser gating | `alaa-frontend-developer` (named, but its number is restated) |

**(c) Legislating an owner's ground in its own voice.**

1. `10-design-workflow.md:22` — "performance target (default: **Lighthouse >= 90 mobile** — a direction whose hero cannot be server-rendered and budget-fit is not shippable)". States another skill's number with no citation. Owner: `alaa-frontend-developer`.
2. `90-quality-gates-and-review.md:19` — "Performance-affecting design choices stay inside the Lighthouse budgets: … **target score >= 90 mobile**." Cites the playbook in the same sentence but still restates the value, creating a second source of truth that will drift.
3. `70-motion-and-modern-css.md:71` — "Restrict `transition-show`/`transition-hide` to subdued pairs (`fade`, `scale`, `jump-up`) with token durations". Quasar prop values; `SKILL.md:32` already assigns transition props elsewhere.
4. `20-design-tokens-and-theming.md:67` — "map the same tokens into **`app.scss`** brand variables (`$primary`, `$dark-page`, …) and **`setCssVar`**/CSS custom properties … **Quasar Dark plugin** state must follow the same theme source". Quasar API surface; `SKILL.md:32` assigns `app.scss` to the Quasar skill.
5. `80-icons-assets-and-imagery.md:17` — "`@quasar/extras` sets — Material Symbols (rounded/sharp/outlined) or MDI — **zero extra dependency, tree-shaken by name**". A build-behaviour claim; `SKILL.md:32` assigns build behaviour to the Quasar skill.
6. `85-accessibility-patterns.md:47` — "**Minimum pass:** keyboard-only walk of primary flows + automated scan (axe or equivalent) when tooling exists + screen-reader smoke of new flows". Test design; owner `alaa-testing-strategy`, uncited.
7. `85-accessibility-patterns.md:48` — "Automated scanners catch **at most ~40%** of issues". An unsourced statistic asserted as fact.
8. `55-component-library-and-governance.md:35` — "Contract changes to widely-used shared components (renamed props, removed variants) **are breaking changes**: search all usages first, migrate in the same change". Breaking-change doctrine; owner `alaa-project-constitution` / `alaa-services-contract`, uncited.
9. `35-ux-writing-and-microcopy.md:30` — "Dates and numbers localized deliberately (**Jalali vs Gregorian per product decision**), not left to library defaults." A wire-format VALUE decision; owner `alaa-services-contract`, uncited.
10. `30-typography-and-color.md:33` — "apply consistently (**`font-feature-settings`**/locale formatting)". Legislates a render mechanism, and the two options named have opposite consequences the file never states: a font feature leaves Latin digits in the DOM (copy-paste, screen-reader, search and sort all diverge from what is displayed), `Intl.NumberFormat('fa-IR')` does not.
11. `70-motion-and-modern-css.md:18` — "CSS anchor positioning (all engines ship it as of **Firefox 147/151**…)". Version-pinned web-platform facts asserted in a design skill on a 2026-07-08 timestamp.

**Deciding test for the design-system / Quasar-mechanics seam (one sentence):**

> *A rule that stays true if the component library were swapped for a different one belongs to `alaa-ui-ux-design-system`; a rule that must name a Quasar symbol, prop, slot or config key to be correct belongs to `alaa-quasar-app-vite-v3`.*

Applied: "focus returns to the trigger on close" and "the CTA accent is spent only on primary actions" are design-system rules; "`QDialog` restores focus, verify for custom overlays", "`transition-show="fade"`", "`app.scss` `$primary`", "`@quasar/extras` is tree-shaken by name" are Quasar-mechanics rules. Items 3, 4 and 5 in (c) above are on the wrong side of that line today; the model of the correct split already exists in the fleet — `alaa-quasar-app-vite-v3/references/60-components-and-layouts.md` is a pure symbol router and does not compete with `60-components-states-and-ux.md`, which is pure state design.

### 5. Duplication

**Internal (body ↔ references).**

| Rule | Locations | Survives |
|---|---|---|
| Routing map, 12 rows | `SKILL.md:70-95` + `00-topic-map.md:5-30` | `00-topic-map.md` (one router per skill); body keeps one pointer line |
| Also-load rules, 9 rows | `SKILL.md:97-123` + `00-topic-map.md:32-51` | `00-topic-map.md` |
| Scope / when-to-use | `SKILL.md:3` + `:36-49` + `:50-57` + `:10-12` | `SKILL.md:3` (description); body sections deleted |
| Companion table | `SKILL.md:28-34` + `:126-133` | one merged Ownership block |
| Contrast thresholds | `SKILL.md:24` + `30:62-66` + `90:9` — despite `90:3` claiming "This is the **single copy** of the gates" | `90:9` is the gate; `30:62-66` becomes the *how* (checker, recording adjusted values) |
| Touch target ≥44×44 / ≥8px gaps | `SKILL.md:24` + `60:18` + `90:14` | `90:14` |
| `prefers-reduced-motion` | `SKILL.md:24` + `:106` + `70:79` + `85:43` + `90:13` — five copies | `90:13` gate + `70:79` mechanism |
| Focus-visible ring | `60:15` + `85:24` + `90:10` | `90:10` gate + `85:24` mechanism |
| Colour never the only signal | `SKILL.md:24` + `30:47` + `50:14` + `60:33` + `60:50` + `90:12` — six copies | `90:12` |
| "CTA = verb + outcome, not Submit", same example "Start learning free" | `35:13` + `50:46` | `35:13` |
| "Empty states teach + one action" | `35:20` + `60:43` | `60:43` (state design), `35` keeps the wording |
| Placeholder is never the label | `60:22` + `35:36` | `60:22` |

**Cross-skill, with `alaa-quasar-app-vite-v3`.**

| Overlap | Here | There | Survives |
|---|---|---|---|
| A11y requirement set: overlay focus in/restore out, icon-only accessible names, placeholder≠label, colour-alone-is-not-status, keyboard operability, semantic elements over clickable `div` | `85:14-24`, `60:15-24`, `90:10-12` | `70-guardrails-a11y-performance-monorepo.md:6-17` | **This skill owns the requirement** (it is a gate); the Quasar file keeps only the symbol-specific audit (`QDialog` focus restore, virtualized rows, custom slots preserving role/name) and points here for *what* must be true |
| Image CLS / responsive delivery: reserve space via `aspect-ratio`/`ratio`, `srcset`+`sizes`, no desktop pixels to phones | `80:28-34` | `63-image-delivery-and-placeholders.md:7-10` + decision table `:24-28` | **Split by the seam test:** this skill keeps "every image declares dimensions or aspect-ratio; the LCP hero is eager with `fetchpriority="high"`, never `loading="lazy"`; meaningful alt / `alt=""`; one consistent treatment"; `63` keeps `QImg` props, placeholder-src, and CDN resize-param generation |
| Layout shell | `50:5-15` | `62-layout-patterns-and-examples.md` | **Low genuine overlap** — `62` is `QLayout` `view`-string semantics and drawer modes, `50` is breakpoints/measure/rhythm. One touching seam: `50:13` "Fixed headers/bars reserve space" vs `62:50` `QPageSticky` overlap with drawers/safe areas. Keep both; cross-link once |
| Component routing | `60-components-states-and-ux.md` | `60-components-and-layouts.md` + `61-component-usage-atlas.md` | **No overlap — this is the model split.** Symbol→API there, state→design here. Cite it as the precedent when fixing the others |
| Performance | `70:81-82` (compositor rule, `content-visibility`) | `70-guardrails…:20-25` (bottleneck triage, Vite 8) | Different levels; keep both |

**With `alaa-vue-typescript-clean-code`.** `55:11-18` (component API design: closed enums, no raw visual props, no boolean explosion, slots vs props) sits directly against `40-patterns-vue-quasar.md` (24,645 B) and `30-clean-code-solid-vue.md`. Survives here only as the *design* statement — "variants are meaning, resolved to tokens by the component" — with the prop-typing, emits and naming mechanics delegated, which `55:16` and `55:49` already do correctly.

**With `alaa-frontend-developer`.** The Lighthouse target is stated in three places (`SKILL.md:119`, `10:22`, `90:19`) and owned in one (`41-lighthouse-and-web-vitals.md`). Only the citation survives; the number is deleted from all three.

### 6. Wording-test failures

**1 — the shipped defaults fail the skill's own blocking gate (worst defect in the pack).**
> "| Playful / education | `#7C3AED` | `#FFFFFF` | `#F59E0B` | …" — `30-typography-and-color.md:53-58`

Failure mode: abstract-noun-adjacent, but worse — an **unvalidated default presented as a starting point**, immediately after `30:45` reserves the accent for primary actions and `50:44` puts the accent on the primary CTA. The table supplies `on-primary` but **no `on-accent`**, so the agent reuses white. Computed white-on-accent ratios for the four shipped rows: SaaS `#EA580C` **3.56:1**, Dashboard `#0D9488` **3.74:1**, Premium `#C9A962` **2.25:1**, Playful `#F59E0B` **2.15:1**. All four fail gate 1 (4.5:1); two fail even 3:1. Border-on-surface runs 1.15–1.48:1 in all four rows, failing `30:64`'s own 3:1 for meaning-bearing UI graphics where the border is an input's only boundary. **Replacement:** ship the table in `oklch()`, add an `on-accent` column, print the computed ratio beside every foreground/background pair, and add "these values are regenerated by `scripts/check-contrast.mjs`; a row with no printed ratio is not a starting point."

**2 — abstract nouns doing the operative work.**
> "It must raise the floor (accessibility, consistency, honest trade-offs) without lowering the ceiling (the agent's creative range)." — `SKILL.md:12`

Failure mode: four abstract nouns and no checkable value; a competent agent can follow it exactly and do anything. **Replacement:** "The floor is the eleven gates in `references/90-quality-gates-and-review.md`; no rule in this pack may forbid a visual choice that passes all eleven."

**3 — abstract noun where a token list was meant.**
> "Effects must match the style: shadow scale, blur, radius, and border treatment all come from the chosen style." — `40-styles-and-visual-language.md:25`

Failure mode: "match" is unmeasurable; "the chosen style" is a mental state, not an artefact. **Replacement:** "Radius, shadow, blur and border values come from the row of the table above that you recorded in MASTER.md; a value not derivable from that row is a defect."

**4 — self-granted exception with no external referent.**
> "automated scan (axe or equivalent) **when tooling exists**" — `85-accessibility-patterns.md:47`

Failure mode: the agent both defines and adjudicates the exception, so the scan is always optional. **Replacement:** "Run the repo's axe integration, or `npx @axe-core/cli <url>` if none exists. If neither can run, say so in the delivery note and list which flows were walked by keyboard instead — an unrun scan is reported, never assumed clean."

**5 — an escape hatch with no boundary.**
> "Escape hatch is `class`/`style` passthrough, **used consciously**." — `55-component-library-and-governance.md:14`

Failure mode: "consciously" is unobservable and reopens the raw-value hole the preceding sentence closed. **Replacement:** "`class`/`style` passthrough may set placement only (margin, grid area, width, order). A passthrough that sets colour, radius, shadow, border or font size is a defect — add a variant instead."

**6 — a checklist line that cancels eleven blocking gates.**
> "What was not checked gets said explicitly — an unchecked box is a statement, not a failure." — `90-quality-gates-and-review.md:44`

Failure mode: preference verb where a constraint was meant; it directly contradicts `90:7` ("A design is not done while any of these fails") by making every gate skippable with a disclosure. Compounded by the off-by-one at `90:34` ("Gates 1–10") which drops gate 11 outright. **Replacement:** "Gates 1–11 are not skippable; an unverified gate blocks delivery. The remaining checklist items may be reported unchecked with a reason."

**7 — prohibition with no positive replacement, on the fleet's load-bearing constraint.**
> "Farsi pages without `lang`/`dir`, or **mixed-direction text left to the browser to guess**." — `85-accessibility-patterns.md:57`; paired with "**mark direction** so punctuation does not scramble" — `35-ux-writing-and-microcopy.md:29`

Failure mode: names the wrong outcome, supplies no mechanism, and "mark direction" is an abstract noun with two very different implementations. An agent will insert LRM/RLM control characters, which corrupt copy-paste, search and stored values. **Replacement:** "Isolate mixed-direction runs in CSS only: wrap the run in an element with `unicode-bidi: isolate` and the correct `dir`. Never insert U+200E/U+200F/U+2066-2069 into content — `client` does direction entirely in CSS, which inserts no characters, and that is the house pattern."

**8 — unmeasurable magnitude plus an unspecified verification.**
> "Farsi needs larger line-height than Latin (1.7–2.0 body) and **slightly larger sizes at equal perceived scale**; **verify the scale with real Farsi copy**, not lorem." — `30-typography-and-color.md:31`

Failure mode: the one checkable number is in parentheses; the operative instruction is a comparative adjective with no baseline and a verification with no method or artefact. **Replacement:** "Set Farsi body line-height to 1.8 and Farsi body size one step above the Latin equivalent in the same scale. Before approving a scale, render the longest real label in the product plus a 200-word real Farsi paragraph at 375px and confirm no clipping, no `text-overflow`, and no horizontal scroll."

**9 — a licence condition with no adjudicator.**
> "Primary Farsi families: Vazirmatn (general UI, variable), IRANSansX-class faces **where licensed**" — `30-typography-and-color.md:30`

Failure mode: self-granted exception — nothing states who checks, what evidence counts, or where the answer is recorded, so the agent will assume licensed. **Replacement:** "Use Vazirmatn (SIL OFL) by default. A non-OFL face may be used only if the repo contains a licence file naming this product; if it does not, use Vazirmatn and state the substitution."

**10 — an invented-assumption licence that outranks asking.**
> "Missing answers are decisions, not blanks: choose the **most defensible default**, state the assumption, and continue." — `10-design-workflow.md:24`

Failure mode: abstract noun ("most defensible") with no external referent, applied to brief inputs that include audience, tone and accessibility level — so the agent silently invents product constraints. **Replacement:** "For each unanswered brief question, take the value from the matching row of the Step 2 table, list it under 'Assumptions' at the top of the deliverable, and continue. If the *product type* itself is unknown, ask that one question and stop."

**11 — an unbounded override of a stated constraint.**
> "These are **hard defaults** for app-family UIs; **repo design tokens may override them**." — `70-motion-and-modern-css.md:64`

Failure mode: constraint verb immediately dissolved by an override with no named artefact. **Replacement:** "A repo overrides a duration or easing only by defining `--motion-duration-*` / `--motion-ease-*` in its theme file; a per-component literal duration remains a defect regardless."

### 7. Stale or unverifiable claims

Everything below is version-sensitive and **needs live web research before Phase 2 ships**; none should be re-asserted from memory.

- **`70-motion-and-modern-css.md:11-18` — the entire three-tier Baseline table, timestamped 2026-07-08.** Specific falsifiable claims: same-document View Transitions "cross-browser since Firefox 144, Oct 2025"; anchor positioning "all engines ship it as of Firefox 147/151 but spec-compliance gaps remain; Interop 2026 focus"; scroll-driven animations "Firefox still flagged"; cross-document View Transitions "no Firefox"; `text-wrap: pretty` "no Firefox"; `interpolate-size`/`calc-size()` "Chromium only". **Verify against `web-features`/Baseline and MDN BCD, not blog posts.** I checked `text-wrap`/`text-wrap-style` live: MDN now reports `text-wrap-style` as Baseline 2024 (newly available since Oct 2024) *for the property*, while noting "some parts of this feature may have varying levels of support" and not publishing per-value Firefox/Safari numbers on the page body — i.e. the skill's flat "no Firefox" for the `pretty` value is at minimum unresolvable from the citation given and must be re-checked in caniuse/BCD per value. Tier 2 vs Tier 3 placement of `text-wrap: pretty` is therefore live.
- **`70:3, 5` and `SKILL.md:139` — the "verified 2026-07-08 / last verified 2026-07-08" freshness stamps.** Twenty days stale at the time of this audit and attached to the fastest-moving content in the pack. The re-verification instruction exists (`SKILL.md:139`) but has no trigger condition an agent can observe.
- **WCAG version and criteria numbers.** The skill states WCAG-derived thresholds (`SKILL.md:24`, `30:62-66`, `90:9-19`) and cites exactly one criterion number — "**WCAG 1.4.12**" at `85:42` — **without ever naming the WCAG version or conformance level it targets**. Live research is needed to fix the target explicitly: WCAG 2.2 is the current W3C Recommendation and WCAG 3.0 remained a Working Draft as of its March 2026 update, so the pack should pin "WCAG 2.2 Level AA" and add the criterion numbers behind each gate (1.4.3 contrast minimum, 1.4.11 non-text contrast, 2.4.7/2.4.11 focus, 1.4.10 reflow, 1.4.4 resize, 2.5.8 target size, 2.3.3 animation from interactions). Note that gate 6's "≥44×44px" is an Apple HIG figure, not the WCAG 2.5.8 Level AA minimum (24×24) — the pack should say it is deliberately stricter rather than implying it is the standard.
- **`85:48` — "Automated scanners catch at most ~40% of issues".** A commonly repeated figure with no source given; either cite a primary study or convert it to a qualitative statement.
- **Font and icon licensing, unverified.** `30:30` "IRANSansX-class faces **where licensed**" — IRANSans/IRANSansX licensing is not open and this is the single most likely licence violation the skill can cause; Vazirmatn's SIL OFL status should be stated explicitly as the safe default. `30:22-24` names Inter, Geist, Playfair Display, Fraunces, Nunito, Baloo, IBM Plex Sans, JetBrains Mono without licences; `80:17-19` names Material Symbols, MDI, Phosphor, Lucide, Heroicons, Tabler, Bootstrap Icons without licences (Heroicons/Tabler/Lucide/Phosphor are MIT-family, Material Symbols Apache-2.0 — but the pack asserts none of it). `80:24` "never recolor, stretch, or redraw third-party logos" is correct and should carry the licence rule with it.
- **`80:17` — "`@quasar/extras` … zero extra dependency, tree-shaken by name".** A build-behaviour claim that belongs to `alaa-quasar-app-vite-v3` and is version-dependent under Vite 8/Rolldown (see that skill's `70-guardrails…:27-33`).
- **`80:38-44` — the favicon/app-identity set** (SVG favicon with `prefers-color-scheme`, 32px `.ico`, `apple-touch-icon` 180×180, manifest 192/512 + maskable at 80% safe zone, `theme-color` with `media`, `og:image` 1200×630). Plausible and stable, but every number is a platform convention that should be re-verified once rather than carried on trust.

Sources consulted live: [MDN `text-wrap-style`](https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap-style), [MDN `text-wrap`](https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap), [caniuse `text-wrap: pretty`](https://caniuse.com/mdn-css_properties_text-wrap_pretty), [AbilityNet — WCAG 3.0 status and 2026 update](https://abilitynet.org.uk/resources/digital-accessibility/what-expect-wcag-30-web-content-accessibility-guidelines), [WCAG 3.0 March 2026 working-draft summary](https://ratedwithai.com/blog/wcag-3-0-march-2026-update-timeline).

### 8. Router audit

- **Reference count: 13** (12 topic files + the map itself) → ≥9, so the router must live in `references/00-topic-map.md` with **one** pointer line in `SKILL.md`.
- **Router location: violated — two routers ship.** `00-topic-map.md:5-30` (12 rows) and `SKILL.md:70-95` (12 rows, same targets), plus the also-load block duplicated at `00:32-51` / `SKILL.md:97-123`. `SKILL.md:67` even instructs the agent to use the other one.
- **Conformance of the pointer:** `SKILL.md:67` is a usable pointer ("Start with `references/00-topic-map.md` unless you already know the exact reference to load, and load only the smallest relevant reference file") but it is buried as step 4 of a 5-step Quick start and is followed by the full duplicate map.
- **Observable-condition test, row by row (`00-topic-map.md:7-30`):** every row opens with "**Need** <abstract noun>", which is a mental state, not an observable situation. Scoring: **0 of 12 rows** use the prescribed "You are about to <observable situation> → read `<file>`" form. **3 marginal** (`:7` new product/redesign, `:15` picking a style, `:29` the gates) encode a real situation and only need rephrasing. **9 are heading mirrors** — the worst is `:27` "Need accessibility patterns: semantic structure, ARIA, focus management, keyboard, live regions", which is a verbatim list of `85-accessibility-patterns.md`'s own H2s (`:6, :12, :20, :27, :34`); `:9` mirrors `20`'s headings, `:21` mirrors `60`'s, `:23` mirrors `70`'s, `:25` mirrors `80`'s.
  Example rewrites: `:9` → "You are about to write a colour, spacing, radius, shadow or z-index value into a component → read `20-design-tokens-and-theming.md`"; `:27` → "You are about to add `@click` to a non-`<button>`, open an overlay, or change route in an SPA → read `85-accessibility-patterns.md`"; `:21` → "You are about to ship a component whose only designed state is the happy path → read `60-components-states-and-ux.md`".
- **"Also load" rules (`00:34-51`, 9 rows):** these are materially better — most already state an observable trigger ("Any new palette, theme, or dark-mode task", "Any icon or image task"). They should be merged into the main rows as second-order conditions rather than kept as a separate list that duplicates `SKILL.md:97-123`.
- **"Good first searches" (`00:53-83`, 31 terms):** the most useful retrieval device in the pack and the only place with genuinely observable hooks (`نیم‌فاصله`, `oklch`, `do not use for`, `rule of three`, `og:image`). Keep and extend; nominate to the lead as a fleet-wide pattern.
- **Dangling paths: one.** `70-motion-and-modern-css.md:5` → `$alaa-frontend-developer` `references/25-modern-css-and-motion.md` — **does not exist** (that skill ships `00, 10, 20, 21, 30, 40, 41, 45, 50, 60, 70, 80, 90` only). All 13 intra-skill paths resolve. The two other cross-skill paths resolve: `41-lighthouse-and-web-vitals.md` (`SKILL.md:119`, `90:19`) and `50-qa-and-verification.md` (`70:83`, `90:55`).
- **Cross-skill citation form: conformant.** Every cross-skill path names its owning skill alongside it (`$alaa-frontend-developer` `references/41-…`), with the single ambiguity of `playwright_visual` (`SKILL.md:33, 132`; `50:61`; `90:28, 56`), which is an MCP server name presented in the same slot as a skill name.

### 9. Assets and tooling audit

Ships **no `scripts/`, no `assets/`, no `templates/`** — and by the standing rule (*a design rule with no tool that reports a violation is a preference, not a rule*), that reclassifies most of §6 and all of the gate list as preferences. Three deterministic checks it should ship, in priority order:

**(1) `scripts/check-contrast.mjs` — the minimum viable one.** Read the theme source (`app.scss` brand vars, Tailwind `@theme`, or `:root` custom properties), resolve `light-dark()` into both themes, then compute WCAG contrast for every pair the semantic role names imply — `on-primary`/`primary`, `on-accent`/`accent`, `foreground`/`background`, `foreground`/`surface`, `muted-foreground`/`surface`, `destructive`/`surface`, `border`/`surface`, each status colour against its surface — and exit non-zero below 4.5:1 (text) / 3:1 (non-text). It emits a table that is the artefact `30:65` demands ("record adjusted values in the token file") and that makes a token change *provable*, closing criterion 1. **What it finds today:** run against this skill's own four starter palettes (`30:53-58`) it fails four times — white-on-accent at 3.56, 3.74, 2.25, 2.15:1 — and flags all four `border`/`surface` pairs at 1.15–1.48:1. On `client`, run it across the Quasar brand variables in both `color-scheme` states; the dark theme is where it will report, because `20:41` says light-passing values "routinely fail on dark surfaces" and nothing today checks that claim.

**(2) `scripts/check-tokens.mjs` — the drift detector.** Walk `src/**/*.{vue,scss,css,ts}` and fail on: any hex/`rgb()`/`hsl()` literal or `oklch()` literal outside the theme file; any raw `px` radius, box-shadow or `z-index` in a component; any Tailwind arbitrary value (`bg-[`, `z-[`, `text-[`); any physical direction property (`margin-left`, `padding-right`, `left:`, `right:`, `text-align: left|right`, `border-left`) in a file belonging to an RTL product; and any `transition`/`animation` duration literal not referencing `--motion-duration-*`. Emits `file:line`. This converts `20:19`, `20:58`, `20:65`, `30:72`, `50:12`, `55:24` and `70:73` from preferences into rules in one pass. **What it finds on `client` today:** the physical-property scan is the high-yield rule — it will separate genuine RTL drift from the correct `unicode-bidi: isolate` declarations, which the script must allowlist explicitly (and by allowlisting them it documents the house pattern the skill currently does not state).

**(3) `scripts/check-rtl.mjs` — the first-class-RTL prover.** Drive Playwright over the route list twice, `dir="ltr"` then `dir="rtl"`, with real Persian strings and the longest real label, at 375px and at 200% zoom; assert `scrollWidth <= clientWidth` on every scroll container, assert no clipped focus ring, and diff the two screenshots for icons in a `must-mirror` allowlist (chevron, arrow, back, forward, undo, redo, indent, list-bullet, send) that failed to mirror and for icons in a `must-not-mirror` denylist (clock, checkmark, play, media transport, logo, magnifier with a neutral handle) that did. This is the only proposed check that discharges gate 10 (`90:18`), which today is verified by a human saying yes.

A fourth, cheap and high-value: **`scripts/token-usage-report.mjs`** — count every token's usages, print zero-usage tokens (dead design system) and single-use tokens (premature abstraction), and print the affected-file list for a proposed token change so a reviewer can see the blast radius before the change lands.

Ship all four with the fleet's existing tooling rule from carryover §3.7 — no `Path(__file__).parents[N]`, no temp directories inside the repository; take the repo root as an argument with `process.cwd()` as the default.

### 10. Rewrite brief for Phase 2

**Target file list.**

| File | Purpose | Δ |
|---|---|---|
| `SKILL.md` | Description; authority tiers; ownership + every out-of-batch disclaimer; the one-sentence Quasar seam test; **one** router pointer; the five non-negotiables that must survive without a file read; repo-evidence-first quick start; freshness pointer | **10,888 → ~3,420 B** |
| `references/00-topic-map.md` | The **only** router. Absorbs `SKILL.md:70-123`; every row rewritten to "You are about to <observable situation> → read `<file>`"; also-load rules merged as second-order conditions; "Good first searches" kept and extended | 3,349 → ~5,800 |
| `references/05-rtl-and-persian.md` | **NEW.** RTL as a first-class configuration axis: `unicode-bidi: isolate` as the house pattern (no control characters, ever); icon must-mirror / must-not-mirror lists; directional motion flip; `dir="ltr"` islands for email/URL/phone/IBAN/code inside RTL forms; chart axis and progress/slider direction; Persian digit mechanism decision with the copy-paste/screen-reader/sort consequence stated; Jalali dates citing `alaa-services-contract` for the wire format; نیم‌فاصله/ZWNJ; the logical-property lint rule | +~4,200 |
| `references/15-designed-failure-states.md` | **NEW.** Split from `60`. The full matrix incl. **permission-denied**, offline, partial, stale-while-revalidate, slow-network tiers with millisecond thresholds and the empty-vs-error-vs-not-permitted distinguishability rule; degradation posture cites `alaa-reliability-sla` | +~3,800 |
| `references/25-untrusted-content-and-ui-authority.md` | **NEW.** What a component may render from user content; `v-html` / `*-html` props / `QEditor` / uploads policy citing `alaa-security-review` and `alaa-quasar-app-vite-v3:70-guardrails…:89`; **a hidden control is not an authorization decision** — the 512-byte permission bitmap is a UI hint, the server re-checks, never design a flow whose safety depends on a hidden button; paste handling (strip styles, preserve ZWNJ, normalize digits) | +~3,000 |
| `references/28-ui-diagnosability.md` | **NEW.** Every error surface carries a copyable correlation reference; a toast that vanishes in 4s is not a log; which UI events are worth emitting, with every NAME delegated to `alaa-services-contract` and every requirement level to `alaa-observability-soc` | +~2,400 |
| `references/32-starter-palettes.md` | **NEW, split from `30`.** The four palettes re-expressed in `oklch()`, with an `on-accent` role and a printed contrast ratio beside every pair, regenerated by `scripts/check-contrast.mjs` | +~2,200 |
| `references/70-motion-contract.md` | **SPLIT from `70`.** Motion intensity tiers, duration/easing tokens, choreography, do-not-animate list, reduced-motion gate, compositor rule — the durable half | ~4,000 |
| `references/72-modern-css-baseline-tiers.md` | **SPLIT from `70`.** The three-tier Baseline table alone, with its own timestamp and re-verify trigger, so the calendar-stale content can be replaced without touching the motion contract | ~4,700 |
| `references/95-design-proofs.md` | **NEW.** What proves a design change: contrast report artefact, RTL screenshot pair, reduced-motion pair, 375px + 200%-zoom pair, axe run, visual-regression baseline and flake policy — mapped onto the six proof levels owned by `alaa-testing-strategy` | +~2,800 |
| `scripts/check-contrast.mjs`, `check-tokens.mjs`, `check-rtl.mjs`, `token-usage-report.mjs` | **NEW**, per §9 | +~14 KB |
| `30`, `35`, `50`, `85` | RTL/Persian fragments removed; each keeps one pointer to `05-rtl-and-persian.md` | −~1,200 net |
| `60` | Failure-state matrix moves to `15`; keeps interaction states, forms, navigation, charts | −~1,400 |
| `90` | Gate numbering fixed to 1–11; `:44` rewritten so gates are not disclosure-skippable; the Lighthouse *number* deleted, citation kept; `:3`'s "single copy of the gates" claim made true by deleting the duplicates in `SKILL.md`, `30` and `60` | ~4,000 |
| `agents/openai.yaml` | Unchanged (Codex-only; `$` form correct) | 313 |

**Body byte budget.** Summed from sections: Purpose + authority tiers 600 · Ownership + out-of-batch disclaimers 700 · Quasar seam test 200 · router pointer 120 · five non-negotiables 600 · quick start 450 · maintenance/freshness 300 = **2,970 + 15% = ~3,420 B**, plus a ~700 B description → `SKILL.md` ≈ **4,120 B total**, down from 11,575. Net of the description the always-loaded body drops 69%, and every removed byte lands in a reference — nothing is deleted for size.

**What moves where.** `SKILL.md:70-95` + `:97-123` → `00-topic-map.md` (rewritten as observable conditions). `SKILL.md:14-18` → one pointer to `/alaa-prompting-guide` (`$alaa-prompting-guide`) and its `references/50-effort-and-thinking.md`; no model named. `SKILL.md:36-57` → deleted, absorbed by the description. `SKILL.md:61` repo-artefact list → `10-design-workflow.md`. `SKILL.md:119` + `10:22` + `90:19` Lighthouse number → citation only. `SKILL.md:126-133` → merged into Ownership. RTL fragments from `30:26-34`, `35:24-30`, `50:15`, `85:10`, `90:18` → `05-rtl-and-persian.md` (gate 10 stays in `90`). Failure states from `60:42-45` → `15`. Starter palettes from `30:49-60` → `32`. `70` → `70-motion-contract.md` + `72-modern-css-baseline-tiers.md`.

**Files to retire.** None outright. Delete: the dangling migration note `70:5`; the four raw-hex starter-palette rows *as written* (replaced in `32`); the duplicated router and also-load block in the body; the "Gates 1–10" off-by-one; the restated Lighthouse number in three places.

**Genuinely NEW capability gained: yes, four.** (i) RTL/Persian as an enforced configuration axis with a bidi mechanism, an icon-mirroring policy and a direction-aware motion rule — none of which exists anywhere in the fleet today. (ii) Untrusted-content rendering plus the UI-affordance-is-not-authorization rule, which preserves the correct `client` framing that no frontend skill currently states. (iii) UI diagnosability — a UI failure that can be joined to a server trace. (iv) Four deterministic checks that convert the pack's largest block of preferences into rules and make a token change provable. Items (i) and (iv) are the two that most change what an agent actually produces on `client`.

### 11. Gap no existing skill can own

**Effectively none — with one narrow item that needs an owner assigned rather than a skill built.**

Each candidate I tested lands inside an existing owner once this skill's disclaimers are written: visual-regression baselining → `alaa-testing-strategy` (design) + `alaa-frontend-devops` (CI storage); the permission-hint-vs-authorization seam → this skill owns the affordance rule, `alaa-services-contract` owns the bit meanings, `alaa-trust-gateway-auth` owns the server-side boundary; Jalali/Gregorian round-tripping → `alaa-services-contract` owns the wire value, this skill owns the render; design-token drift enforcement → this skill, once it ships §9's scripts.

The one genuinely unowned item, with evidence: **Persian text normalization at the input boundary has no owner.** Arabic ي/ك versus Persian ی/ک, Arabic-Indic ٤ versus Persian ۴, and ZWNJ variants mean two strings that render identically do not compare, sort, index or deduplicate as equal. The skill touches all three surfaces of this problem and settles none — `35:27` requires correct ZWNJ in *displayed* copy, `30:33` picks a *display* digit system and offers `font-feature-settings` as one mechanism (which leaves the DOM value unchanged), and `60:52` requires locale-aware formatting — while `client` must store, search and compare one canonical form. `alaa-data-layer` owns storage, `alaa-services-contract` owns names and values, this skill owns paste and display; but the normalization form itself is a single VALUE that must be byte-identical on both sides of the wire, and nothing states it. **This does not warrant a new skill.** Nominate `alaa-services-contract` as the owner of the normalization form (one named Unicode form plus the character-folding table), and have this skill cite it from `references/05-rtl-and-persian.md` for the paste-and-display half. Flag it to the lead as a cross-batch item, since `alaa-services-contract` is out of Batch 6.


---

## Appendix E — `alaa-frontend-devops`

Read all 14 files in full, plus the four sibling files named for overlap checking, the carry-over document, and ran two live checks (Node LTS status, Vite 8 status). Confirmed there is no `client` repository mounted in this session — only `/mnt/user-data/uploads/skills` and `cowork-folders/` exist — which constrains section 9 to prediction rather than execution, and I say so there.

---

### alaa-frontend-devops

### 1. What this skill is today

Subject: frontend delivery safety — CI, Docker, artifact contract, proxy/public-path, deploy verification and rollback. Register: flat imperative bullets, present tense, no code, no commands, no values. Shape: `SKILL.md` 4,349 B on disk / **3,956 B net of frontmatter**; five references totalling **8,677 B** (00-source-map 2,529 / 10-build-contract 1,997 / 20-ci-docker-cache 1,508 / 30-proxies 1,499 / 40-verification 1,144); `agents/openai.yaml` 272 B. No scripts, no assets, no `__pycache__`.

**The split is the right way round** — references carry 2.2× the body. But it is right for the wrong reason. The body is small because it contains *nothing but routing*: eight sections, of which purpose/when/when-not/quick-start/matrix/companions/nav/maintenance are all meta. There is not one substantive rule an agent must obey in the always-loaded body. For a skill whose worst failure is a secret compiled into a client bundle, the one rule that must never cost a hop is absent from the body entirely — and absent from the references too. The body is not too big; it is empty of content and the references are too thin to compensate. Total skill = 13 KB for the entire delivery surface of a 99.99% frontend.

### 2. Ten-criteria verdict

| # | Criterion | Verdict | Evidence |
|---|---|---|---|
| 1 | Correctness and testability | **FAILS** | `references/40-verification-and-rollback.md:7-11` is the whole test story: "Run the lightest meaningful build or pipeline check. Inspect the final output tree." No assertion is named, no exit code, no failing-case design. `references/10-build-contract-and-artifacts.md:36-39` restates the same four steps. Nothing that would fail against a plausible broken build. The six proof levels owned by `alaa-testing-strategy` are never mentioned; that skill is never named. |
| 2 | Failure behavior (failed deploy, half-propagated CDN, stale `index.html`, rollback) | **FAILS** | Only `references/40:20-24` touches it: "be ready to describe which config changed / which output path changed / which file should be reverted first". "Be ready to describe" is not a rollback path. No half-propagated-CDN handling, no stale-HTML-referencing-dead-hashes case (the single most common frontend deploy failure), no service-worker-pinned-old-base recovery, no atomic-swap or two-version-overlap discipline. `references/30:33` names the symptom "app shell loads but chunks 404" and gives no procedure. |
| 3 | Security (what may be baked into a bundle, SRI, CSP) | **FAILS** | Zero occurrences of secret, CSP, integrity, SRI, SBOM, `import.meta.env`, or a client env prefix anywhere in the skill (grepped). The client bundle is a public artifact and this skill never says so. `alaa-quasar-app-vite-v3/references/21-cli-vite-and-config.md:59` states the actual rule ("only client-prefixed vars may enter client bundles") — the delivery skill does not, and does not route to it. `alaa-security-review` unnamed. |
| 4 | Observability (build provenance, artifact identity, commit→bundle traceability) | **FAILS** | Not one word. No commit SHA in the artifact, no build metadata file, no image label, no sourcemap policy, no way to answer "which commit produced the bundle currently serving production". `alaa-observability-soc` unnamed. |
| 5 | Concurrency and load | **FAILS** | Cache headers are the frontend's entire load-shedding story and `references/30:19-23` gives three sentences, none of them a directive or a value. No origin-shield, no thundering-herd on cache invalidation, no concurrent-deploy interlock (two pipelines publishing to one asset root is a real corruption path). |
| 6 | Clean code, SOLID, design patterns | **NOT-OWNED** — `alaa-vue-typescript-clean-code` and `alaa-project-constitution` | Legitimate domain-wise, **but scored FAILS on the naming test**: neither owner is named anywhere in the skill. Silence, not disclaim. |
| 7 | Algorithm and data-structure choice | **NOT-OWNED** — `alaa-algorithms-data-structures` | Same defect: not named. The one in-domain analogue that *is* this skill's (chunking strategy and its cost) is absent too. |
| 8 | Configurability (build-time vs runtime config; how a runtime value reaches a static bundle) | **FAILS** | The distinction is never drawn. `references/30:26` says "Confirm the asset origin and path prefix are computed correctly for deployed environments" without saying whether that computation happens at build or at serve time — which is the entire question. No runtime-config mechanism (config endpoint, placeholder substitution in `index.html`, injected `window.__CFG__`). The skill's own description promises Compose (`SKILL.md:3,28`) and no reference file mentions Compose at all, so the fail-closed `${VAR:?}` / `${VAR:-}` invariant is absent despite being binding. |
| 9 | Speed of development and debuggability | **FAILS** | Not one command, path, filename, or runnable check in 13 KB. `SKILL.md:49` "Validate in the same environment shape that would catch the delivery risk" leaves an agent to invent the command. `references/30:31-36` lists four symptoms with no diagnostic sequence attached to any of them. |
| 10 | Documentation (what shipped, how operated, how it fails) | **FAILS** | `references/40:28-33` asks for four bullets in the chat reply. Nothing durable: no deploy note, no runbook, no rollback record, no artifact manifest. "What shipped" cannot be answered because criterion 4 is absent. |

Satisfied: **0/10**. Not-owned-and-named: **0**. Not-owned-but-silent: 2.

### 3. Defect classes actually found

**Class 1 (stale model pins) — CONFIRMED ABSENT.** Grepped; no model name anywhere. Correct as-is; Phase 2 should add the routing line to `/alaa-prompting-guide` (`$alaa-prompting-guide`) that currently does not exist.

**Class 2 (trigger syntax).** `SKILL.md:40,45,63,65,67,69` and `agents/openai.yaml:4` — seven `$alaa-*` / `$openai-docs` call sites, **zero `/alaa-*`**. Consequence: every companion hand-off is silently unreachable from Claude Code; an agent there reads a routing instruction it cannot execute and proceeds without the companion.

**Class 3 (duplication).** (a) `SKILL.md:46-47` Quick-start steps 3–4 route to `00-source-map.md` and `10-build-contract…` — the same two routes appear again at `SKILL.md:75-78`; two routers, one body. (b) `SKILL.md:57` PWA row ("service worker scope, update UX, offline boundaries, asset versioning") vs `references/40:15`. (c) `references/10:32` "reverse proxy rewriting paths in a way that breaks hashed chunks" vs `references/30:16`. (d) `references/10:34-39` "Minimum verification" vs `references/40:5-11` "Minimum verification loop" — two competing minimum lists in one skill. Consequence: an agent that loads only `10` and an agent that loads only `40` run different closeouts.

**Class 4 (project-specific in always-loaded body).** Mild here. `references/20:28` "Yarn-first when the repo is already Yarn-based" is repo-shaped and, worse, **contradicts** `alaa-mono-package/SKILL.md:53` "detect first; never assume yarn" — an inter-skill contradiction inside one batch.

**Class 5 (long numbered procedures).** Three: `SKILL.md:44-49` (6 steps), `references/10:14-17` (4 steps), `references/40:6-11` (4 steps). None keyed to a failure class; all three are "read config, then look at output".

**Class 6 (description with no do-not-use) — CONFIRMED ABSENT.** `SKILL.md:3` carries a proper negative clause. Not a defect here.

**Class 7 (fragile tooling) — n/a**, no scripts. See §9 for the consequence.

**Class 8 (`__pycache__`) — CONFIRMED ABSENT.** Tree is clean.

**Class 9 (unnamed gaps).** Ten of ten rows in §2; the skill names not one owner for anything it does not do.

**Class 10 (body larger than needed).** Inverted. The body is *under*-loaded on content and over-loaded on meta: `SKILL.md:86-92` is 450 B of maintainer-facing prose ("Prefer one-hop references instead of growing this file") paid on every single invocation by an agent who is not the maintainer.

**Class 11 (no stated companion boundary).** `SKILL.md:60-71` names five companions, **all inside Batch 6**. Zero out-of-batch owners: no `alaa-gitlab-ci-cd`, no `alaa-docker-production`, no `alaa-haproxy`, no `alaa-minio-object-storage`/`alaa-arvan-object-storage`, no `alaa-testing-strategy`, `alaa-security-review`, `alaa-reliability-sla`, `alaa-observability-soc`, `alaa-project-constitution`, `alaa-services-contract`. This is the class that causes the §4(c) violations below.

### 4. Boundary map

**(a) Legitimately owns.** The frontend artifact contract (what a build must emit and where); the gate register and predicates for a frontend pipeline, plus the commands that evaluate them; the build-time-versus-runtime configuration boundary and how a runtime value reaches an immutable bundle; artifact identity and provenance for a shipped bundle; the cache-policy *decision* per response class (derived from whether the filename is content-hashed); the deploy-failure playbook and rollback path; what may and may not be compiled into a client bundle.

**(b) Must disclaim and to whom.** Provider YAML expression, job graph, cache-key syntax, artifact retention → `alaa-gitlab-ci-cd`. Dockerfile authorship, layer ordering, multi-stage, image minimisation, Compose file authorship → `alaa-docker-production`. Proxy directives, compression config, header emission → `alaa-haproxy`. CDN origin bucket, lifecycle, invalidation API → `alaa-minio-object-storage` / `alaa-arvan-object-storage`. Make targets → `alaa-makefile`. Test design and proof-level naming → `alaa-testing-strategy`. Threat classification of a leaked value → `alaa-security-review`. Retention and alerting on build provenance → `alaa-observability-soc`. The literal values `dist/ssr/index.js`, `dist/ssr/client/assets`, the client env prefix → `alaa-services-contract`. The quality bar → `alaa-project-constitution`. Model/effort → `/alaa-prompting-guide` (`$alaa-prompting-guide`). Quasar `build.env.*` and SW implementation → `alaa-quasar-app-vite-v3`. Package graph membership → `alaa-mono-package`. **None of these is disclaimed today except the last two.**

**(c) Legislating an owner's ground in its own voice.**
- `references/20-ci-docker-and-cache.md:12-17`, the entire "Docker rules" block: *"Keep dependency install layers driven mainly by manifest files and lockfiles."*, *"Separate build-time tooling from the runtime image whenever the repo architecture supports it."*, *"Keep images minimal and predictable."* — container expression, `alaa-docker-production`'s ground, stated as this skill's own rule.
- `references/20:39` *"Docker layers that copy the full repo before dependency install"* — same.
- `references/30-proxies-public-path-and-remote-assets.md:15` *"Verify compression settings do not corrupt or mis-serve built files."* — proxy configuration, `alaa-haproxy`'s ground.
- `references/30:19-23`, "Cache header rules": *"Hashed browser assets can be long-lived and immutable."* / *"HTML and SSR responses should follow the project's shorter cache policy."* — the *policy* is legitimately this skill's (it follows from content hashing); the phrasing presents it as a serving rule with no owner named for the directive.
- `references/00-source-map.md:19` lists *"GitHub Actions, GitLab CI, Docker, Nginx, HAProxy, Kubernetes, CDN"* as documentation to consult — routing an agent to upstream vendor docs for exactly the four domains that have in-fleet owners, none of which is named. This is the class-11 defect made concrete: the skill sends agents to the internet instead of to `alaa-gitlab-ci-cd`, `alaa-docker-production`, `alaa-haproxy`, and the object-storage skills.
- `SKILL.md:58` *"| package-consumer | emitted JS/CSS assets, peer dependencies, and import paths |"* — `alaa-mono-package`'s whole domain, restated as a verification row in this skill's always-loaded body, two lines below a routing entry that already hands the same subject to `$alaa-mono-package` (`SKILL.md:64-65`).

### 5. Duplication

| Rule | Locations | Survives in |
|---|---|---|
| Minimum verification loop | `references/10:34-39`, `references/40:5-11` | `40` (its file is named for it); `10` keeps only the artifact assertions |
| PWA/SW update + offline verification | `SKILL.md:57`, `references/40:15` | Neither — the depth lives in `alaa-quasar-app-vite-v3/references/30-service-worker-excellence.md` and `32-pwa-injectmanifest-guard.md`; devops keeps one routed obligation ("a deploy that changes the asset base must invalidate the precache manifest → `$alaa-quasar-app-vite-v3` `references/32-pwa-injectmanifest-guard.md`") |
| Proxy path rewrite breaking hashed chunks | `references/10:32`, `references/30:16` | `30` |
| Route to `00-source-map` / `10-build-contract` | `SKILL.md:46-47` and `SKILL.md:75-78` | The single router table |
| Package assets must land in the final client asset output | `references/10:10,23,32`, and in three other skills: `alaa-mono-package/references/30:7,22-26`, `alaa-frontend-developer/references/10-contract-and-boundaries.md:84`, `alaa-quasar-app-vite-v3/references/70-guardrails…:63-65` | **Four-way duplication.** Survives in `alaa-mono-package` (it owns graph membership); devops keeps only the output-side assertion, which is a different sentence |
| Concrete artifact paths `dist/ssr/index.js`, `dist/ssr/client/assets` | Stated **only** in `alaa-frontend-developer/references/10-contract-and-boundaries.md:90-91`; devops states them nowhere | Must move **into** devops (or into `alaa-services-contract` with devops routing to it) — the owner of the build contract currently has no value for it while a general skill does |

### 6. Wording-test failures

| # | Quoted | file:line | Failure mode | Replacement |
|---|---|---|---|---|
| 1 | "Separate build-time tooling from the runtime image whenever the repo architecture supports it." | `references/20:16` | Self-granted exception, no external referent | "The runtime image contains no package manager, no compiler, and no devDependencies. If a single-stage build is unavoidable, name the blocking constraint in the merge request and obtain `alaa-docker-production`'s exemption before merging." *(and the whole rule then routes out — see §A)* |
| 2 | "Prefer explicit runtime versions for Node and package managers." | `references/20:9` | Preference verb where a constraint was meant; "explicit" is an abstract noun | "Pin CI Node to an exact `major.minor.patch` on a Node Active-LTS or Maintenance-LTS line, and fail the build if it differs from `engines.node` / `.nvmrc`. A floating tag such as `node:lts` fails the gate." |
| 3 | "Keep the pipeline deterministic." | `references/20:8` | Abstract noun standing in for an observable condition | "Install from the lockfile with the frozen flag for the detected manager (`npm ci`, `yarn install --immutable`, `pnpm install --frozen-lockfile`). A run that modifies the lockfile fails the build." |
| 4 | "If the repo uses SSR, the runtime entry path must stay stable unless maintainers explicitly change the contract." | `references/10:8` | Abstract noun with no value; "maintainers explicitly change the contract" names no artifact | "The SSR runtime entry is `dist/ssr/index.js` and the client asset root is `dist/ssr/client/assets` unless the repo's `AGENTS.md` states otherwise. Changing either requires editing `AGENTS.md` in the same commit." |
| 5 | "Do not move runtime-only files into browser-visible outputs unless required." | `references/10:23` | Prohibition + self-granted exception + no positive replacement | "Server-only modules must not be reachable from the client entry graph. Assert it by scanning every emitted client chunk for the server entry's exported symbol names; keep server-only code reachable from the SSR entry alone." |
| 6 | "Prefer one source of truth for the browser asset base." | `references/30:6` | Preference verb; abstract | "The browser asset base is declared in exactly one place, `quasar.config`'s `build.publicPath`. Any other file needing an asset URL reads `import.meta.env.BASE_URL` and never re-derives it." |
| 7 | "Hashed browser assets can be long-lived and immutable." | `references/30:20` | Capability statement, not a rule — an agent can follow it and configure nothing | "Files matching `assets/*.[0-9a-f]{8,}.*` are served `Cache-Control: public, max-age=31536000, immutable`; `index.html` and every SSR HTML response are served `Cache-Control: no-cache`. The directives themselves are `alaa-haproxy`'s to write." |
| 8 | "Do not claim deployment safety without checking the path that was originally broken or most at risk." | `references/40:16` | "most at risk" is unfalsifiable | "Before reporting a delivery change as verified, re-run the exact reproduction that opened the task and include its output. If no reproduction existed, state that no pre-change failure was observed." |
| 9 | "Validate in the same environment shape that would catch the delivery risk." | `SKILL.md:49` | Abstract-noun stack; no observable condition | "Build in the deployment mode named in the task (`quasar build -m ssr` or `-m pwa`) and inspect the emitted tree. A dev-server check does not satisfy this step." |
| 10 | "Keep examples plain and portable; do not hard-code one repo unless the example is explicitly repo-scoped." | `SKILL.md:90` | Self-granted exception, "explicitly" by no named party; and it is maintainer prose in an always-loaded body | Move to a maintenance reference; rewrite as "A concrete path or command in a reference file states the repo it came from on the same line." |

### 7. Stale or unverifiable claims

- **Node.** `references/20:9,22,30` and `references/00:26` reference Node versions abstractly and pin nothing. Live check run: as of 2026-07-28, Node 26 is the newest LTS line (26.5.0, active support to 2027-10-27), Node 24 is Active LTS until 2026-10-20, and **Node 22 left Active LTS on 2025-10-21** (security-only to 2027-04-30). Node has moved to one major per year from Node 27. Phase 2 must state the Active/Maintenance-LTS rule rather than a version, so the rule does not age.
- **Vite.** Not mentioned outside `references/00:13`'s doc URL. Vite 8 (Rolldown-powered) is confirmed shipped. The Vite-8 consequences that touch delivery — `build.rollupOptions` → `build.rolldownOptions`, object `manualChunks` removed, default browser targets raised — are stated in `alaa-quasar-app-vite-v3/references/70-guardrails…:27-42` and are correctly that skill's; devops must route, not restate.
- **npm/pnpm/yarn.** `references/20:28` "Yarn-first when the repo is already Yarn-based" is the only manager statement and it conflicts with `alaa-mono-package/SKILL.md:53`. Needs no web research — it needs deleting and routing to the detection rule.
- **Docker and CDN.** Neither is described behaviourally, so nothing is stale; everything must be *added*. **Compose interpolation needs live re-verification at write time** (`${VAR:?message}` mandatory, `${VAR:-default}` deliberately optional, no default permitted where the default would silently disable a safety control, and interpolation reading only the shell and `--env-file` and never the service-level `env_file:` key) — it is binding from Batch 2 and currently absent despite `SKILL.md:3,28` promising Compose coverage.
- **Needs live web research in Phase 2:** current Compose interpolation and `--env-file` precedence; current CSP and Subresource Integrity guidance for bundler-emitted hashed assets; current Vite/Rolldown sourcemap-publication defaults; the Node LTS table at write time.

### 8. Router audit

Five reference files → **the router belongs in the body, and it is in the body** (`SKILL.md:73-84`). No `references/00-topic-map.md` exists. Correct on location today.

**`references/00-source-map.md` is NOT a router.** It contains a source-priority ladder (`:7-20`), freshness triggers (`:22-30`), a community-evidence boundary (`:32-46`), and an anti-pattern (`:48-52`). No row points at a sibling reference. It is a genuine source-provenance ledger and is legitimate; the one-router rule is not violated. **But it squats the `00-` slot** that the fleet reserves for the router — `alaa-frontend-developer/references/00-topic-map.md` and `alaa-quasar-app-vite-v3/references/00-topic-map.md` both use it that way. An agent carrying fleet habits opens `00-*` expecting routes and gets bibliography. Rename to `05-source-map.md`, matching `alaa-quasar-app-vite-v3/references/05-authority-and-api-lookup.md`. Uniformity over local optimality.

**Observable-condition test: every router row fails.** All five rows in `SKILL.md:75-84` are heading mirrors — "Build contract, artifact rules, SSR runtime entry, and final asset expectations: `references/10-build-contract-and-artifacts.md`" is the file's own title expanded. Contrast the correct form in `alaa-frontend-developer/references/00-topic-map.md:7-32`, which opens every row with "Need …". The devops rows should read "You are about to change `publicPath`, an asset base, or a CDN origin → read `references/30-…`".

**Two more routing structures compete with the router.** `SKILL.md:44-49` "Quick start" routes to two of the five files, and `SKILL.md:51-58` "Verification matrix" is a table shaped like a router that routes nowhere — it names four delivery shapes and the things to verify, with no file attached to any row. That matrix is the best raw material in the skill and it is wasted as prose.

**Dangling paths: none** — all five referenced files exist. **But zero cross-skill paths exist:** every companion at `SKILL.md:60-71` is named by trigger alone. An agent sent to `$alaa-quasar-app-vite-v3` for "exact Quasar build behavior" faces 29 reference files with no entry point. The correct pattern is already demonstrated in this batch at `alaa-frontend-developer/references/50-qa-and-verification.md:65`, which names the skill *and* the file.

### 9. Scripts and assets audit

Ships nothing. It should ship one script, and the absence is why criteria 1, 4 and 9 all fail together.

**`scripts/verify-artifact-contract.mjs`** — argument: the build output root, default `dist/ssr`. Asserts:
1. The SSR runtime entry exists at the declared path.
2. Every `src`, `href`, and `modulepreload` URL in the emitted HTML and in the client manifest resolves to a file that exists on disk under the client asset root. **This is the stale-`index.html`-pointing-at-dead-hashes check, and it is the single highest-value assertion in the lane.**
3. No emitted asset path escapes the client asset root, and every absolute URL matches the declared base.
4. No value of a build-time environment variable whose key lacks the client prefix appears verbatim in any emitted client chunk. Secret-leak gate.
5. Every emitted chunk filename matches `\.[0-9a-f]{8,}\.(js|css)$`, so the immutable cache header is safe to apply.
6. A provenance file sits beside the artifact carrying commit SHA, build timestamp, Node version, package-manager version, and lockfile hash.

Exit codes: `0` all pass; `1` a contract assertion failed, each printed with the offending path; `2` the output root is absent or unreadable — deliberately distinct so a pipeline can tell "nothing was built" from "the wrong thing was built"; `3` invocation or config error.

**On `client` today:** I could not run it — no `client` repository is mounted in this session, only the skills tree. Stated as prediction to confirm in Phase 2: assertion 6 fails certainly, because no skill in the fleet mentions provenance so no repository has been asked to emit it; assertion 4 is the one to run first, because Quasar app-vite v3 changed env injection from v2's `process.env.*` / `build.env` to `build.env.clientPrefix` with default `QCLI_` (`alaa-quasar-app-vite-v3/references/21-cli-vite-and-config.md:24-26`), and a repo carrying a v2-era injection forward is exactly how a non-prefixed variable reaches a public bundle.

### 10. Rewrite brief for Phase 2

**Target reference set** (10 files; growth is the point):

| File | Purpose | Source |
|---|---|---|
| `05-source-map.md` | Source priority, freshness triggers, evidence boundary | renamed from `00-source-map.md`; vendor-doc list at `:19` replaced by in-fleet owner names |
| `10-build-contract-and-artifacts.md` | The artifact contract with concrete paths and the hashing requirement | existing, minus its duplicate verification list `:34-39` |
| `15-build-time-vs-runtime-config.md` | **NEW.** Criterion 8: what is fixed at build, what varies at runtime, and the three mechanisms by which a runtime value reaches an immutable bundle; the fail-closed Compose interpolation invariant for the serving container | new |
| `20-ci-gates-and-predicates.md` | Gate register, predicates, commands. No provider YAML, no Dockerfile | rewritten from `20-ci-docker-and-cache.md` |
| `25-artifact-identity-and-provenance.md` | **NEW.** Criterion 4: commit→bundle traceability, build metadata, image labelling, sourcemap publication policy | new |
| `30-serving-caching-and-public-path.md` | Cache-policy decision per response class; public-path single source of truth; directives routed to `alaa-haproxy`, CDN origin to the object-storage skills | from `30-proxies-…` |
| `35-client-bundle-security.md` | **NEW.** Criterion 3: nothing secret in a client bundle, CSP, SRI, third-party script policy; threat classification routed to `alaa-security-review` | new |
| `40-verification-and-rollback.md` | Verification mapped to the six proof levels owned by `alaa-testing-strategy` | existing, tightened |
| `45-deploy-failure-playbook.md` | **NEW.** Criterion 2 by failure class: failed deploy, half-propagated CDN, stale HTML on dead hashes, SW pinned to old base, concurrent-publish corruption — each with symptom, smallest diagnostic, rollback decision | new |
| `90-companion-boundary.md` | Full ownership map with skill-plus-path for every companion; maintainer prose moved off the always-loaded body | new, absorbs `SKILL.md:86-92` |

**Router relocation trigger.** With five references today the router stays in the body. This set is ten, which crosses the ≥9 threshold, so the router moves to `references/00-topic-map.md` and `SKILL.md` carries one pointer line. Renaming `00-source-map.md` → `05-source-map.md` is what frees the slot, and it is required either way.

**Body byte budget.** Sections: H1 + one-line subject 120 B; ownership-and-disclaim block naming all fourteen owners 700 B; the delivery contract as three concrete values 400 B; the three non-negotiables that must never cost a hop (no secret in a client bundle; every artifact carries provenance; a change to an asset URL states its rollback file before it ships) 500 B; router pointer line 120 B; model/effort routing line 100 B. Sum 1,940 B, plus 15% = **2,231 B**, against today's 3,956 B net. The body shrinks 44% while the skill roughly doubles in coverage. The `SKILL.md:51-58` verification matrix converts into router rows in `00-topic-map.md` rather than dying.

**Retire to `_to_delete/`:** nothing. `00-source-map.md` is renamed, `20-ci-docker-and-cache.md` and `30-proxies-…` are rewritten under new names — the device mount forbids `unlink`, so the superseded originals move to `_to_delete/` once their content has landed.

**Genuinely new capability: yes, four.** Client-bundle security (criterion 3), artifact provenance (criterion 4), build-versus-runtime configuration including the Compose invariant (criterion 8), and a failure-class deploy playbook (criterion 2). Each is a capability the skill does not have in any form today, so the coverage growth is declarable under the definition of done.

---


---

## Appendix F — `alaa-mono-package (with the shared closing sections A, B and C of the joint lane)`

### alaa-mono-package

### 1. What this skill is today

Subject: workspace package boundaries in a frontend monorepo — `packages/*` consumption, dist-only entrypoints, peer/dedupe, asset emission, clean-island write lanes. Register: mixed — the body is the densest, most operational prose in the batch (real `pnpm --filter` syntax, real specifier protocols, a migration rule), while the references drop to the same flat abstract bullets as its sibling. Shape: `SKILL.md` 7,742 B on disk / **7,285 B net of frontmatter**; five references totalling **6,251 B** (00-source-map 1,951 / 10-boundary 1,479 / 20-peers 836 / 30-assets 745 / 40-audit 1,240); `agents/openai.yaml` 286 B. No scripts, no `__pycache__`.

**The split is the wrong way round, confirmed.** The always-loaded body is 17% larger than everything it routes to, and the two references covering the skill's two named domains — peers and assets — are 836 B and 745 B, the smallest files in the batch. `SKILL.md:53-70` alone (package-manager modes plus build order, ~2,600 B) is a third of the body and is needed only when an agent is writing a dependency specifier or ordering a build, which is a subset of tasks, not all of them. Class 4 and class 10 together, exactly as the brief anticipated. The material itself is good; its location is wrong.

### 2. Ten-criteria verdict

| # | Criterion | Verdict | Evidence |
|---|---|---|---|
| 1 | Correctness and testability (public entrypoints provably importable in every declared condition) | **FAILS** | The word `exports` appears four times and never once as a rule: `references/00:9` (a thing to read), `:24` (a freshness trigger), `:37` (an anti-pattern aside), `SKILL.md:90` (a symptom-table cell). No condition ordering, no `types`-first rule, no subpath exports, no `default`-last, no `main`/`module` fallback prohibition, no self-reference. `references/40:18` "package public entrypoint still resolves" is the entire test and does not say resolves *under which condition* or *with which resolver*. `SKILL.md:69` gets closest — "validate the built entrypoint from `dist` imports successfully" — but names one condition, singular. |
| 2 | Failure behavior (dual-package hazard, duplicated peer at two versions, SSR/client asset divergence) | **FAILS** | Dual-package hazard: never named; `references/20:13` mandates ESM "unless the repo explicitly requires something else" and does not say what goes wrong when both are emitted. Duplicated peer: `references/20:19-20` names "duplicate Vue runtime / duplicate Quasar runtime" as failure modes and gives no detection method and no resolution — `references/00:37` says "inspect the final bundle for duplicate framework instances" without saying how. SSR/client asset divergence: `references/30:20` names "runtime URLs that point outside the deployed asset root" and stops. Three named failure classes, zero procedures. |
| 3 | Security | **FAILS** | `references/00:27` lists "security or supply-chain claims about hoisting, dedupe, transitive dependencies, or package provenance" as a *freshness trigger* — the one place supply chain appears, and it is an instruction to re-read docs, not a rule. No install-script policy, no transitive-dependency review, no lockfile-integrity gate, no `publishConfig`/registry scoping. `alaa-security-review` unnamed. |
| 4 | Observability | **FAILS** | Absent. A package cannot be traced to a build; no version stamping, no `dist` metadata. `alaa-observability-soc` unnamed. |
| 5 | Concurrency and load | **NOT-OWNED** — but **FAILS on the naming test**. The in-domain analogue is real and unstated: parallel package builds racing on a shared `dist/`, and the parallel-agent lane that `SKILL.md:72-81` explicitly contemplates ("part of parallel package work") without one word about two agents building the same graph concurrently. Runtime load is `alaa-reliability-sla`'s, unnamed. |
| 6 | Clean code, SOLID, design patterns | **NOT-OWNED** — `alaa-vue-typescript-clean-code`, `alaa-project-constitution` | **Silent, so FAILS the naming test.** The in-domain analogue this skill *does* own — package public surface as an interface-segregation decision — is one line at `references/10:22` "keep package public surface small and explicit", with no criterion for small. |
| 7 | Algorithm and data-structure choice | **NOT-OWNED** — `alaa-algorithms-data-structures`, unnamed | The in-domain analogue is the dependency graph and its topological order, which the skill handles well at `SKILL.md:63-70` without ever naming it as such or stating a cycle-detection rule. |
| 8 | Configurability (`exports` conditions and build targets) | **FAILS** | Both halves absent. Conditions: see criterion 1. Build targets: no `target`, no `moduleResolution` consequence, no browser-vs-node condition, no `development`/`production` condition. `references/20:13` "stable ESM outputs" is the whole build-target story. |
| 9 | Speed of development and debuggability | **PARTIAL → FAILS** | The body is genuinely fast: `SKILL.md:57` gives real pnpm commands, `:70` gives the topological shortcut, `:83-90` gives a symptom→cause table. This is the best content in the batch. It fails only because every one of the five symptoms in that table routes to a reference that does not contain the answer — "missing CSS in consumer app → asset emission or package export wiring" leads to `references/30`, 745 B that never mentions `sideEffects`, the exact field that causes it. |
| 10 | Documentation | **FAILS** | `references/40:22-28` asks for four chat bullets. No package README contract, no changelog, no export-surface documentation requirement, no consumer migration note when an entrypoint changes. |

Satisfied: **0/10**. Not-owned-and-named: **0**. Not-owned-but-silent: 3.

### 3. Defect classes actually found

**Class 1 — CONFIRMED ABSENT.** No model pin. No routing to `/alaa-prompting-guide` either; add it.

**Class 2 (trigger syntax).** `SKILL.md:95,97,99,101` + `agents/openai.yaml:4` — five `$alaa-*`, **zero `/alaa-*`**. Same consequence as the sibling.

**Class 3 (duplication).** (a) The clean-island rule appears **four times**: `SKILL.md:47`, `SKILL.md:74-80` (as a 5-step guard), `references/10:8`, `references/40:10,16-17`. (b) The `link:` → `workspace:*` migration rule twice: `SKILL.md:61` and `references/10:12`. (c) Dist-entrypoint-then-assets validation three times: `SKILL.md:69`, `references/30:22-26`, `references/40:11,18-20`. (d) `SKILL.md:99` and `SKILL.md:101` are **two router rows pointing at the same skill**, `$alaa-quasar-app-vite-v3` — a literal duplicate entry in a five-row table. (e) Cross-skill: `references/20:8` and `references/10:9-11` are restated almost verbatim at `alaa-quasar-app-vite-v3/references/70-guardrails-a11y-performance-monorepo.md:61-73` and at `alaa-frontend-developer/references/10-contract-and-boundaries.md:77-84`. The Quasar file additionally carries the concrete peer JSON and the dedupe pointer that `alaa-mono-package` — the owner — does not.

**Class 4 (project-specific in always-loaded body).** `SKILL.md:57` embeds the repo scope `"@alaa/<x>"`. `SKILL.md:100` embeds four version values — `vue-router >= 5`, `pinia ^2 || ^3`, `Node 22+`, `Vite 8/Rolldown` — every one of them owned by `alaa-quasar-app-vite-v3` (`references/21-cli-vite-and-config.md:20-28`) and, as values, by `alaa-services-contract`. `SKILL.md:53-70` is a 2,600 B stack-specific block loaded on every invocation including invocations that never touch a specifier.

**Class 5 (long numbered procedures).** Three, all in or adjacent to the body: `SKILL.md:45-51` (7 steps), `SKILL.md:74-80` (5 steps), `references/40:8-12` (5 steps). The 7-step quick start and the 5-step lane guard overlap at steps 2–3 and 1–2 respectively.

**Class 6 — CONFIRMED ABSENT.** `SKILL.md:3` carries a proper "Do not use it when…" clause.

**Class 7 — n/a**, no scripts. See §9.

**Class 8 — CONFIRMED ABSENT.**

**Class 9 (unnamed gaps).** Ten of ten. Zero owners named outside Batch 6 — this skill names **no out-of-batch owner at all**, and only three distinct in-batch ones.

**Class 10 (body larger than needed).** Confirmed and quantified: 7,285 B body against 6,251 B of references. `SKILL.md:53-70` (2,600 B) and `SKILL.md:116-122` (330 B of maintainer prose) are the two clearest movable blocks.

**Class 11 (no stated companion boundary).** Worst in the batch. `SKILL.md:92-101` lists four rows, one a duplicate. `alaa-controlled-ops` — the PHP/Composer package-release skill and the nearest structural analogue in the fleet — is not named, so the JS side has no release-gate vocabulary and no statement of whether it mirrors or defers.

### 4. Boundary map

**(a) Legitimately owns.** What a workspace package declares and emits: `exports` map and its conditions, entrypoint stability, dist-only consumption, the peer contract and the single-instance guarantee for shared runtimes, package asset and CSS membership in the bundling graph, internal specifier syntax per detected manager, build order over the dependency graph, and the clean-island write lane.

**(b) Must disclaim and to whom.** Where the graph's output lands and how it is served → `alaa-frontend-devops`. Quasar/Vite bundler configuration, dedupe wiring, `resolve.dedupe`, library-mode config → `alaa-quasar-app-vite-v3` (`references/22-cli-cookbook-and-examples.md`, which `alaa-quasar-app-vite-v3/references/70-…:80` names as the place the exact wiring lives). All version values → `alaa-services-contract`. Release-gate vocabulary → `alaa-controlled-ops` (see §B note). Test design and proof levels → `alaa-testing-strategy`. Supply-chain threat classes → `alaa-security-review`. The quality bar → `alaa-project-constitution`. Model/effort → `/alaa-prompting-guide` (`$alaa-prompting-guide`). **None disclaimed today.**

**(c) Legislating an owner's ground in its own voice.**
- `SKILL.md:100` *"Packages consumed by a Quasar app-vite v3 app (peer expectations: `vue-router >= 5`, `pinia ^2 || ^3`, Node 22+, Vite 8/Rolldown)"* — four values owned by `alaa-quasar-app-vite-v3` and by `alaa-services-contract`, asserted in this skill's own always-loaded voice inside what is nominally a *routing* row to that very skill.
- `SKILL.md:61` *"Peer-dependency and `resolve.dedupe` rules (§20) still apply on top of this"* — `resolve.dedupe` is bundler configuration; `alaa-quasar-app-vite-v3/references/70-…:80` explicitly routes dedupe wiring to `22-cli-cookbook-and-examples.md`. This skill claims it and then supplies nothing: `references/20` never mentions `resolve.dedupe`, so the cited §20 does not contain what the body promises. **A dangling internal promise.**
- `SKILL.md:88` *"| wrong SSR asset path | public-path or dist contract mismatch |"* — public path is `alaa-frontend-devops`'s ground, diagnosed here in this skill's own table.
- `references/30:20` *"runtime URLs that point outside the deployed asset root"* — the deployed asset root is `alaa-frontend-devops`'s value; used here without attribution.
- `SKILL.md:57` *"pnpm's isolated (non-flat) `node_modules` blocks phantom deps, so declare every used dependency explicitly."* — correct, and legitimately this skill's, but stated as fleet doctrine with no source and no freshness marker in an always-loaded body.

### 5. Duplication

| Rule | Locations | Survives in |
|---|---|---|
| Clean-island write boundary | `SKILL.md:47`, `SKILL.md:74-80`, `references/10:8`, `references/40:10,16-17` | The body, once, as a three-step guard — it constrains *writes*, so it is genuinely always-needed. All three other statements go. |
| `link:` → `workspace:*` migration | `SKILL.md:61`, `references/10:12` | New `references/15-package-manager-modes.md` |
| Dist-entrypoint-then-assets validation | `SKILL.md:69`, `references/30:22-26`, `references/40:11,18-20` | `references/40`, expressed as the script's assertion list |
| Route to `$alaa-quasar-app-vite-v3` | `SKILL.md:99` **and** `SKILL.md:101` | One row, with a file path attached |
| `vue`/`quasar` externalised as peers | `references/20:8`, `references/00:37`, `alaa-quasar-app-vite-v3/references/70-…:61,68,73`, `alaa-frontend-developer/references/10-contract-and-boundaries.md:83` | **`alaa-mono-package` must win** — it is the owner. The Quasar and frontend-developer copies become one-line routed pointers. This is a cross-lane recommendation; those files are not this lane's to edit. |
| Package CSS/assets stay in the bundling graph | `references/30:7`, `alaa-frontend-devops/references/10:10,23`, `alaa-frontend-developer/references/10:84`, `alaa-quasar-app-vite-v3/references/70-…:63` | `alaa-mono-package/references/30` (graph membership is its call); devops keeps only the output-side assertion |
| Manager detection before advice | `SKILL.md:53-61` vs `alaa-frontend-devops/references/20:28` "Yarn-first" | `alaa-mono-package` — and the devops line is a **contradiction**, not a duplicate, and must go |

### 6. Wording-test failures

| # | Quoted | file:line | Failure mode | Replacement |
|---|---|---|---|---|
| 1 | "package-local build/check scripts should either build required upstream packages first or fail with a clear message." | `SKILL.md:68` | Preference verb; a disjunction that lets the agent pick either branch; "clear message" unfalsifiable | "A package's `build` script must not read an upstream package's `dist/` without first building it. Under pnpm, run `pnpm --filter \"<pkg>^...\" build` before the local build; an absent upstream `dist/` exits non-zero naming the missing package." |
| 2 | "Packages should emit stable ESM outputs unless the repo explicitly requires something else." | `references/20:13` | Preference verb + self-granted exception | "Every package emits ESM only. `exports` declares no `require` condition unless the package `README.md` names a CommonJS consumer, because a dual ESM/CJS build of a package holding module state creates a dual-package hazard: two copies of that state in one process." |
| 3 | "Package entry files should be predictable and documented." | `references/20:14` | Two abstract nouns, no checkable condition | "Every importable path is listed in `exports`. Do not add `main` or `module` alongside `exports`; a consumer importing a path absent from `exports` must fail at resolution time rather than fall through to a legacy field." |
| 4 | "Imports that reach into `packages/<name>/src/*` are boundary violations unless the repo explicitly allows them." | `references/10:11` | Self-granted exception naming no artifact | "No file outside a package may import `packages/<name>/src/**`. Enforce with a root `no-restricted-imports` ESLint rule; record any exemption as an inline `eslint-disable` carrying the owning issue ID." |
| 5 | "Shared frontend dependencies such as `vue` and `quasar` should not be bundled into internal package outputs." | `references/20:8` | "such as" leaves the set open; preference verb | "`vue`, `quasar`, `vue-router`, and `pinia` appear in every internal package's `peerDependencies`, in none of its `dependencies`, and in its build's `external` list. Assert exactly one resolved realpath per name across the workspace." |
| 6 | "Use `peerDependencies` where that is the repo contract." | `references/20:9` | Circular — defers to a contract it neither names nor locates | Delete; superseded by #5. |
| 7 | "…treat sibling packages, the root app, `src/*`, legacy files, and root config as read-only unless the user widens scope." | `SKILL.md:47` | "legacy files" is an abstract noun defined nowhere in the skill; an agent cannot tell whether a file is one | "…treat every path outside the named package directory as read-only, including the root app, sibling packages, and root config, until the user names an additional path." |
| 8 | "use deterministic asset paths" | `references/30:12` | Abstract noun for an observable condition | "Reference a package asset with a static specifier the bundler resolves at build time — a plain `import`, or `new URL('./x.png', import.meta.url)`. A path assembled from a runtime variable is invisible to the bundler and will not be emitted." |
| 9 | "package public entrypoint still resolves" | `references/40:18` | Untestable as written: resolves under which condition, with which resolver, and does resolution imply loadability? | "For every subpath and every condition in `exports`, resolve the target with Node's own resolver and then import it in a subprocess. A target that resolves but throws on evaluation fails this check." |
| 10 | "…or is an explicitly allowed package-owned doc/test/build artifact." | `SKILL.md:79` | Self-granted exception; "explicitly allowed" by no named party | "…or matches one of the package-owned paths the user named when opening the lane. If no such path was named, the package directory is the whole allowance." |

### 7. Stale or unverifiable claims

- **Node.** `SKILL.md:100` "Node 22+". Live check: Node 22 left Active LTS on 2025-10-21 and is security-only until 2027-04-30; Node 24 is Active LTS to 2026-10-20 and Node 26 is the newest LTS line at 26.5.0. As a *floor* the claim is still literally true, which is precisely why it will rot unnoticed. It is also not this skill's value. Delete and route.
- **Vite.** `SKILL.md:100` "Vite 8/Rolldown" — confirmed correct today (Vite 8.0 shipped, Rolldown-powered). Still owned by `alaa-quasar-app-vite-v3/references/21-cli-vite-and-config.md:20-28`. Delete and route.
- **`vue-router >= 5`, `pinia ^2 || ^3`** — `SKILL.md:100`, restating `alaa-quasar-app-vite-v3/references/21-…` and `70-…:71`. Same treatment. **Needs live verification at Phase 2 write time if retained anywhere.**
- **npm / pnpm / yarn.** `SKILL.md:53-61` is the most accurate package-manager content in the batch and I found nothing wrong in it: the `workspace:*` protocol under pnpm, `workspace:^` under Yarn Berry, `link:`/`file:` under Yarn classic and npm, `pnpm --filter "<pkg>..."` for a package plus dependents, and pnpm's isolated `node_modules` blocking phantom dependencies all check out. Flag one nuance for Phase 2 to verify live: `pnpm --filter "<pkg>..."` selects the package **and its dependencies** while `"...<pkg>"` selects the package and its **dependents** — `SKILL.md:70` glosses `"<pkg>..."` as "a package plus its dependents", which is the reverse of the pnpm convention. **This is the one substantive technical error I found and it needs a live check against current pnpm filtering docs before Phase 2 rewrites it.**
- **`exports` semantics.** Nothing stated, so nothing stale — everything to add. Everything Phase 2 writes here (condition matching being first-match and order-sensitive, `types` needing to precede `import`/`require`, `default` last, subpath and pattern exports, `moduleResolution: bundler` versus `node16` consequences) must be verified against `nodejs.org/api/packages.html` and the current TypeScript module-resolution documentation at write time. This is the area of the JS ecosystem where blog-era advice is most often wrong and most often copied.
- **Docker and CDN.** Out of this skill's scope; correctly absent.

### 8. Router audit

Five reference files → **the router belongs in the body, and it is there** (`SKILL.md:103-114`). No `references/00-topic-map.md`. Correct on location.

**`references/00-source-map.md` is NOT a router**, same finding as the sibling: source ladder `:7-17`, freshness triggers `:19-27`, community boundary `:29-31`, anti-pattern `:33-37`. No row points at a sibling file. Legitimate provenance ledger. **Same `00-` slot squatting**, same remedy: rename to `05-source-map.md`.

**Observable-condition test: all five rows fail.** `SKILL.md:105-114` are heading mirrors — "Peer dependencies, dedupe, and package build output: `references/20-peer-deps-dedupe-and-build-output.md`" is the filename in prose. Correct form: "You are about to add or move a dependency between `dependencies` and `peerDependencies` → read `references/20-…`".

**Competing routing structures in the body: three.** `SKILL.md:45-51` "Quick start" routes to two files; `SKILL.md:83-90` "Symptom map" is a five-row table that routes to *causes* and never to a file, despite being the best-shaped router material in either skill; `SKILL.md:103-114` is the nominal router. Converting the symptom map into router rows — symptom → file — is the single highest-leverage structural change available in this skill.

**Dangling paths.** All five reference files exist; no broken file path. **One dangling internal cross-reference:** `SKILL.md:61` cites "§20" for `resolve.dedupe` rules, and `references/20-peer-deps-dedupe-and-build-output.md` contains no occurrence of `dedupe` as a rule — only the word in its title. An agent following that pointer arrives at nothing. **Zero cross-skill paths:** all four companion rows name a trigger and no file, so `$alaa-quasar-app-vite-v3` sends an agent into 29 files with no entry point.

### 9. Scripts and assets audit

Ships nothing. Criterion 1 fails *because* nothing mechanises it.

**`scripts/verify-package-entrypoints.mjs`** — argument: a package directory, or all workspace members when omitted. Asserts:
1. For every subpath and every condition in `exports`, the resolved target exists on disk after build. Criterion 1's "provably importable in every declared condition".
2. `types` is the **first** key in every conditions object. Condition matching is first-match, so a `types` key placed after `import` is unreachable and TypeScript silently falls back to `any` — invisible in review, caught in one line here.
3. The package actually loads, not merely resolves: spawn `node --input-type=module -e "import('<pkg>')"` for the import condition, and a `require` probe for any require condition.
4. No file under `dist/` carries a bare specifier for `vue`, `quasar`, `vue-router`, or `pinia` while that name sits in `dependencies` rather than `peerDependencies`. Dual-runtime gate.
5. `sideEffects` is absent, or explicitly lists every CSS file the package emits. A blanket `"sideEffects": false` on a package that ships entry CSS is exactly the "missing CSS in consumer app" row at `SKILL.md:87`, whose stated cause the current references never name.
6. Every internal workspace specifier matches the manager detected from the lockfile — `workspace:*` under pnpm, no `link:` or `file:`. `SKILL.md:61`'s migration rule made mechanical instead of aspirational.
7. Resolve `vue` and `quasar` from each package and from the root app and assert one realpath each. The duplicated-peer-at-two-versions gate, which `references/00:37` asks for in prose and gives no method for.

Exit codes: `0` pass; `1` a contract assertion failed, each printed with package, subpath, and condition; `2` `dist/` absent or the package is unbuilt — deliberately distinct so a build-order bug reads differently from a contract bug; `3` invocation error.

**On `client` today:** not runnable — no `client` repository is mounted in this session. Prediction to confirm in Phase 2: assertions 2 and 5 are the highest-yield, because both are silent-by-construction (a misordered `types` and a blanket `sideEffects: false` each produce zero build errors and a broken consumer), and neither is mentioned anywhere in the skill that owns them, so nothing has ever prompted anyone to check. Assertion 6 is the cheapest, and `SKILL.md:61`'s existence as a written migration rule is evidence that a `link:` specifier has already been carried into this workspace at least once.

### 10. Rewrite brief for Phase 2

**Target reference set** (10 files):

| File | Purpose | Source |
|---|---|---|
| `05-source-map.md` | Source priority, freshness triggers, evidence boundary | renamed from `00-source-map.md` |
| `10-package-boundary-and-entrypoints.md` | Boundary rules and dist-only consumption | existing, minus the duplicated clean-island rule `:8` and specifier rule `:12` |
| `12-exports-map-and-conditions.md` | **NEW.** Criterion 1 and half of 8: condition ordering, `types` first, `default` last, subpath and pattern exports, self-reference, no `main`/`module` fallback, dual-package hazard | new |
| `15-package-manager-modes.md` | pnpm / Yarn Berry / Yarn classic / npm specifier protocols, filter syntax, migration rule | absorbs `SKILL.md:53-61` verbatim, with the `"<pkg>..."` gloss corrected |
| `18-build-order-and-graph.md` | Topological order, upstream-dist guards, cycle detection, concurrent-build safety for parallel lanes | absorbs `SKILL.md:63-70` |
| `20-peer-deps-dedupe-and-build-output.md` | Peer contract, single-realpath rule, externalisation, version-range contract; dedupe *wiring* routed to `alaa-quasar-app-vite-v3` `references/22-cli-cookbook-and-examples.md`, closing the `SKILL.md:61` dangling promise | existing, expanded |
| `30-assets-css-and-ssr-client-assets.md` | Asset and CSS graph membership, `sideEffects` and CSS, static-specifier rule | existing, expanded |
| `35-types-and-declaration-output.md` | **NEW.** Rest of criterion 8: `.d.ts` emission, project references, `moduleResolution` consequences, build targets | new |
| `40-audit-and-verification.md` | Audit loop bound to the script's assertions and to the six proof levels owned by `alaa-testing-strategy` | existing, tightened |
| `45-release-and-version-gates.md` | **NEW.** Version bump, changelog, consumer migration note when an entrypoint changes, publish gates — adopting `alaa-controlled-ops`' gate names rather than inventing parallel ones | new |
| `90-companion-boundary.md` | Ownership map with skill-plus-path for every companion; maintainer prose off the body | new, absorbs `SKILL.md:116-122` |

That is 11; the router therefore moves to `references/00-topic-map.md` with one pointer line in `SKILL.md`, and the `00-` rename is what frees the slot.

**Body byte budget.** Sections: H1 + subject 110 B; ownership-and-disclaim naming every owner 650 B; the one always-needed manager rule ("read the lockfile before writing any dependency specifier or any command; the file that exists decides the syntax") 250 B; clean-island lane guard tightened to three steps 600 B; three non-negotiables (never import `packages/*/src` from outside the package; `vue`/`quasar`/`vue-router`/`pinia` are peers and never dependencies; a package is not done until its `exports` targets are imported under every declared condition) 450 B; router pointer 120 B; model/effort routing 100 B. Sum 2,280 B, plus 15% = **2,622 B**, against today's 7,285 B net. **A 64% body reduction** while references roughly double. The symptom map at `SKILL.md:83-90` survives as router rows in `00-topic-map.md`; the manager and build-order blocks survive verbatim in references. Nothing is deleted.

**Retire to `_to_delete/`:** nothing outright; `00-source-map.md` is renamed and the superseded originals of rewritten files move there after their content lands.

**Genuinely new capability: yes, three.** The `exports` conditions contract (criterion 1 and half of 8), declaration output and build targets (the other half of 8), and release/version gates (criterion 10 and the `alaa-controlled-ops` alignment). None exists in any form today.

---

### Shared closing

### A. The stack-versus-platform ruling

**The sentence Phase 2 writes into `alaa-frontend-devops`, in the body's ownership block:**

> `alaa-frontend-devops` owns the frontend delivery gate register — for each gate, the predicate it asserts, the command that evaluates it, and the artifact it inspects — and writes no provider YAML and no Dockerfile: `alaa-gitlab-ci-cd` owns how a gate is expressed on a runner and decides no gate, `alaa-docker-production` owns how the build and runtime images and any Compose file are expressed and decides no gate, and `alaa-haproxy` owns how a cache or routing decision is expressed as a directive and decides no policy.

**Line-by-line disposition of `references/20-ci-docker-and-cache.md`:**

*Stays — gate, predicate, or command, all frontend-owned:*
- `:8` determinism → becomes the frozen-lockfile predicate plus the three manager commands.
- `:10` "verify outputs, not just exit codes" → **the defining gate of this skill**; becomes the artifact-contract gate backed by the §9 script.
- `:9` Node pinning → becomes the predicate "CI Node equals `engines.node` and sits on an Active or Maintenance LTS line". The value is a gate; the image tag carrying it is provider.
- `:21-24` cache-key invalidation predicates (lockfile change ⇒ key change; toolchain change ⇒ key change; a workspace manifest is a dependency-layer input). These are predicates *on* a key, and only the frontend skill knows that a stale install changes the emitted bundle. The key's syntax is provider.
- `:29-33` the command register — install command, build command, artifact verification step — minus `:28`'s Yarn-first assumption, which is deleted as contradicting `alaa-mono-package/SKILL.md:53`.
- `:37` "upload jobs that assume a folder exists without checking" → becomes the gate "the publish step asserts the artifact tree before uploading".

*Moves out to `alaa-gitlab-ci-cd` as a routed obligation:* every expression of a cache key (`cache: key: files:`, `policy:`), the job graph, `rules:` / `needs:`, artifact retention and `expire_in`, and the runner image reference. `alaa-frontend-devops` states only *when* the gates must run — "on every merge request touching `src/**`, `packages/**`, `quasar.config.*`, or the lockfile" — and stops. `:36` "floating toolchain versions in CI" splits: the prohibition is a frontend gate, the pinning mechanism is provider.

*Moves out to `alaa-docker-production` as a routed obligation:* the entire Docker-rules block `:14-17` (layer ordering by manifest and lockfile, layer-invalidation avoidance, multi-stage separation, image minimisation) and `:39` (copying the full repo before dependency install). All five are Dockerfile authorship. What `alaa-frontend-devops` keeps in their place is the frontend-specific obligation the container must *satisfy*: the runtime image contains the complete client asset tree and the SSR entry at the declared paths; no build-time environment variable survives into the runtime image except those carrying the client prefix; the image is labelled with the commit SHA that produced the bundle.

*Also moving out, from the sibling reference files:* `references/30:12-17` proxy verification and `:19-23` cache directives → the *policy* stays with `alaa-frontend-devops` (it follows from content hashing, which the build owns), the *directive* routes to `alaa-haproxy`; `references/30:25-29` remote-asset origin → CDN origin bucket, lifecycle, and invalidation route to `alaa-minio-object-storage` / `alaa-arvan-object-storage`.

*And one thing must move **in**, not out:* `alaa-frontend-devops` promises Compose in `SKILL.md:3` and `:28` and covers it nowhere. The fail-closed interpolation invariant belongs in the new `references/15-build-time-vs-runtime-config.md` — a mandatory variable is `${VAR:?message}`, a deliberately optional one is `${VAR:-default}`, a variable whose default would silently disable a safety control takes `:?` with no default permitted, and interpolation reads the shell and `--env-file` only, never the service-level `env_file:` key — stated as the *frontend runtime container's* configuration gate, with the Compose file's authorship routed to `alaa-docker-production`.

### B. Should these two skills remain separate?

**Yes, separate — with one sentence written into both to make the seam explicit.**

The boundary: **`alaa-mono-package` owns everything that determines what enters the bundling graph — a package's declared exports, its peer contract, its specifiers, and whether its CSS and assets are reachable from an entry — while `alaa-frontend-devops` owns everything that happens to that graph's output after `build` exits: where it lands, how it is served, how it is traced to a commit, and how it is rolled back.**

The evidence for separation, from what I read. The two skills' substantive majorities do not touch: `alaa-mono-package`'s best content (`SKILL.md:53-70` on manager protocols and topological build order) has no delivery dimension, and `alaa-frontend-devops`'s largest gaps (provenance, CSP/SRI, deploy-failure classes, runtime config) have no package dimension. Their trigger descriptions already discriminate cleanly and each carries a working negative clause pointing at the other (`alaa-frontend-devops/SKILL.md:40` explicitly excludes package-boundary work; `alaa-mono-package/SKILL.md:39` explicitly excludes generic CI and deployment). Merging would produce one ~25 KB skill firing on both "change the GitLab cache key" and "add a subpath export", which over-triggers in both directions and destroys the description discrimination that already works.

The evidence for the seam being *real but currently unmarked*: exactly one rule genuinely straddles it — package assets landing in the final client asset output — and it is stated in **four** places (`alaa-mono-package/references/30:7`, `alaa-frontend-devops/references/10:10,23,32`, `alaa-frontend-developer/references/10-contract-and-boundaries.md:84`, `alaa-quasar-app-vite-v3/references/70-…:63`). One rule is a seam, not a shared domain. The fix is a sentence, not a merge: `alaa-mono-package` owns whether a package asset is *in* the graph; `alaa-frontend-devops` owns whether the graph's output *lands where the deployment serves it*. Each states its half and routes the other by skill name plus file path.

### C. Gap no existing skill can own

**None.** Two candidates surfaced and both are absorbable without any skill violating its boundary, so proposing a skill for either would be padding.

The first was build-time-to-runtime configuration for a static bundle — how a value unknown at build time reaches an already-immutable artifact. It looked ownerless: `alaa-services-contract` owns names and values but not mechanisms, and `alaa-quasar-app-vite-v3` already owns the *build-side* mechanism (`references/21-cli-vite-and-config.md:24` on `build.env.{folder,file,clientPrefix}` and `:59` on client-prefix gating). But what remains — a runtime config endpoint, entrypoint-substituted placeholders in `index.html`, a serving-layer-injected global — is a property of the artifact and of how it is served, which is squarely `alaa-frontend-devops`'s ground. It becomes `references/15-build-time-vs-runtime-config.md`, not a skill.

The second was client-side supply chain: SRI attributes, CSP for a hashed-asset bundle, third-party script provenance. `alaa-security-review` owns review triggers and threat classes and does not own emitting an integrity attribute — but the emission is an artifact property, so `alaa-frontend-devops` owns it and routes the classification. It becomes `references/35-client-bundle-security.md`, not a skill.

The real deficiency in this lane is not a missing skill. It is that two skills covering the entire build-and-package seam of the live frontend total 26 KB between them, satisfy zero of twenty quality-bar criteria, name zero of the fourteen owners they depend on, ship zero executable checks, and are invisible from Claude Code at all twelve of their call sites. Every one of those is fixable inside the two directories.

**Sources consulted for the freshness checks:** [Node.js EOL table](https://endoflife.date/nodejs), [Node.js release schedule change](https://www.infoq.com/news/2026/06/nodejs-release-changes/), [Vite 8.0 announcement](https://vite.dev/blog/announcing-vite8), [Node.js Modules: Packages](https://nodejs.org/api/packages.html).


---

## Appendix G — `alaa-frontend-doc-annotations`

### 1. What this skill is today

`/mnt/user-data/uploads/skills/skills/sohrab/alaa-frontend-doc-annotations/`

| File | Bytes |
|---|---|
| `SKILL.md` | 2,927 |
| `agents/openai.yaml` | 286 |
| `references/00-source-map.md` | 1,817 |
| `references/10-annotation-boundaries.md` | 997 |
| `references/20-jsdoc-patterns.md` | 1,009 |
| `references/30-ssr-hydration-and-store-notes.md` | 1,046 |
| references subtotal | 4,869 |
| **total** | **8,082** |

No `scripts/`, no `evals/`, no `__pycache__`.

**Subject.** A documentation-only diff mode for Vue/Quasar/Vite code: English JSDoc, narrow inline comments, and SSR/hydration/store/auth notes, with an explicit prohibition on touching logic, templates, or CSS.

**Register.** Advisory throughout. The one genuinely constraint-shaped passage in the skill is `references/10-annotation-boundaries.md:6-20` (allowed changes / not allowed). Everywhere else the verbs are `prefer`, `use ... when it adds real value`, `worth capturing`, `note whether`. It names zero tools, zero commands, zero doctrine-owner skills, and zero `alaa-*` names outside its three-row companion list.

**Shape.** Four references, two routers in the body (`Quick start` at `SKILL.md:39-47` and `Reference navigation` at `SKILL.md:82-91`), and a Good/bad-examples block in the body that duplicates work the references already do.

**The one good idea it already has and does not exploit.** The closed-looking prefix set at `references/20-jsdoc-patterns.md:32-37` — `SSR NOTE:`, `HYDRATION NOTE:`, `STORE NOTE:`, `AUTH NOTE:` — is a greppable retrieval index. The skill never tells an agent to grep it, never forbids a fifth prefix, and never attaches a checker to it.

---

### 2. Ten-criteria verdict

| # | Criterion | Verdict | Evidence |
|---|---|---|---|
| 1 | Correctness and testability (is an annotation CHECKABLE?) | **FAILS** | Zero occurrences of `tsc`, `vue-tsc`, `eslint`, or any command in the whole skill. `references/20-jsdoc-patterns.md:32-37` defines four prefixes with no rule that reports their absence, their misuse, or a fifth invented prefix. `references/20-jsdoc-patterns.md:42` says "repeating type information that is already clear from JSDoc tags" — the actual checkable rule (in a `.ts` file `@param {Type}` is redundant and `eslint-plugin-jsdoc`'s `check-tag-names` with `typed` reports it) is never stated. |
| 2 | Failure behavior | **FAILS** | The skill has no rule for the annotation-pass failure mode that actually occurs: encountering a comment that is now false. `references/10-annotation-boundaries.md:40` ("Re-open the target file before editing if time has passed") governs the editing session, not the repository's existing stale comments. Nothing defines what a documentation pass does when the code and its docblock disagree. |
| 3 | Security | **FAILS** | `references/30-ssr-hydration-and-store-notes.md:24-28` reaches the right subject — "mark server-only token handling clearly", "note which auth assumptions come from gateway, BFF, or cookie-backed flows" — but as preference verbs, with no rule that a stale auth annotation is a defect, no verification date, and no owner named. `alaa-security-review` and `alaa-trust-gateway-auth` appear nowhere. |
| 4 | Observability | **FAILS** (silence, not disclaimer) | No annotation class for a log line's meaning, a metric's contract, a trace attribute, or a correlation id. `alaa-observability-soc` is not named. |
| 5 | Concurrency and load | **FAILS** (silence) | Frontend translation — annotating abort/race/double-fire assumptions — is absent. `alaa-vue-typescript-clean-code/SKILL.md:82` owns double-fire safety; this skill never names it, so silence, not NOT-OWNED. |
| 6 | Clean code, SOLID, design patterns | **FAILS** (silence) | The most damning row. `alaa-vue-typescript-clean-code` already holds comment policy at `references/30-clean-code-solid-vue.md:62,67,68,101,130-131` and `references/20-typescript-composition-contract.md:97`. The skill whose entire subject is comments never names it. Its companion list (`SKILL.md:75-81`) names `$alaa-frontend-developer`, `$alaa-quasar-app-vite-v3`, `$alaa-repo-docs` — none owns clean code. |
| 7 | Algorithm and data-structure choice | **FAILS** (silence) | Genuinely not this skill's ground, but `alaa-algorithms-data-structures` is not named, and under the batch rule silence is FAILS. |
| 8 | Configurability | **FAILS** | An annotation pass has a real configuration surface — repo language mode (JS+JSDoc vs TS), which lint rules are on, the prefix set, density thresholds. `references/20-jsdoc-patterns.md` states none of it, so the same skill produces different output on two repos with no rule saying why. |
| 9 | Speed of development and debuggability | **FAILS** (nearest miss) | `references/10-annotation-boundaries.md:22-29` ("Good targets": boot files, store actions, fetch wrappers, SSR data-loading, lifecycle-heavy components, auth/hydration bridges) is a genuine speed heuristic and the best content in the skill. But the skill never connects an annotation to a question a future agent asks, never makes the prefix set a retrieval channel, and asserts value only as "where they help future agents and maintainers" (`SKILL.md:19`). The affordance exists; it is not operational. |
| 10 | Documentation — what shipped, how it is operated, how it fails | **FAILS** | This is the criterion the skill exists for and it fails against the criterion's own text. The skill documents *code reasoning*; it has no contract for *what shipped* (`@deprecated`, `@since`), *how it is operated* (`@example`, the run-phase of an exported wrapper), or *how it fails* (`@throws`, error contract). `references/20-jsdoc-patterns.md:13` offers "one or two `@see` references when useful" as the entire tag vocabulary. |

**0 SATISFIED / 10 FAILS / 0 NOT-OWNED.** No row is legitimately NOT-OWNED, because the skill names no owner for anything: zero `alaa-*` doctrine names appear in any file.

---

### 3. Defect classes actually found

**Class 2 — trigger syntax.** `SKILL.md:77`, `SKILL.md:79`, `SKILL.md:81`, `agents/openai.yaml:4`. Four `$alaa-*` forms, zero `/alaa-*`. The skill uses the core Agent Skills format with no Claude-only frontmatter, so it is cross-runtime and every call site must give both forms. *Consequence:* a Claude Code agent reading `pair with $alaa-frontend-developer` has no invocable token.

**Class 3 — duplication between body and references.** Four instances.
- `SKILL.md:66` `// Keep this branch client-only so SSR never touches browser storage.` vs `references/00-source-map.md:46` `// Keep this client-only because SSR cannot read browser storage.` — the same example twice, worded differently, so the two will drift.
- `SKILL.md:13` "documentation-only annotation pass" + `SKILL.md:34` "the task changes behavior" vs `references/10-annotation-boundaries.md:6-20`, which holds the full allowed/not-allowed lists.
- `SKILL.md:48-72` (Good/bad JSDoc and inline examples, ~590 B of always-loaded body) does the job of `references/20-jsdoc-patterns.md:39-44` and `references/00-source-map.md:35-49`.
- Two routers inside the body: `SKILL.md:39-47` and `SKILL.md:82-91` both route into `references/`. *Consequence:* "one router per skill, NEVER TWO" is violated inside a single file, and the two disagree — `Quick start` mandates `00` and `10`, `Reference navigation` presents all four as peers.

**Class 5 — numbered procedure.** `SKILL.md:41-46`, six ordered steps. Step 5, "Load only the smallest additional reference file needed for the code surface", is an unobservable instruction embedded in an ordered list, which is exactly the failure the class names. *Consequence:* the router's selection logic is hidden inside a procedure instead of being a condition table.

**Class 9 — unnamed gaps against section 2.** All ten rows above. Additionally the batch's own verified worked example — the `client` permission bitmap documented as a UI hint that is not an authorization decision — appears nowhere in the skill, despite being the exact annotation class it should mandate. *Consequence:* the skill's flagship case is invisible to an agent using it.

**Class 10 — body larger than it needs to be (narrow form).** The body is the smallest in the batch at 2,927 B, so this is not a size problem in the usual sense; it is a *composition* problem. `SKILL.md:48-72` (examples, ~590 B) and `SKILL.md:93-99` (Maintenance rules, ~430 B — authoring meta addressed to the skill's maintainer, not to the agent) are ~1,020 B of always-loaded body carrying no instruction the agent can act on. *Consequence:* the budget that should hold the owner-disclaimer table and the checker invocation is spent on decoration.

**Class 11 — no stated companion boundary (partial).** `SKILL.md:75-81` names three skills, and the one it most overlaps — `alaa-vue-typescript-clean-code`, which already legislates comment policy in six places — is absent. *Consequence:* two Batch-6 skills both answer "should this comment exist" and neither cedes.

**Not found (verified clean):** Class 1 (no model pin anywhere), Class 6 (the description at `SKILL.md:3` does carry "Do not use it when the task changes behavior"), Class 8 (no `__pycache__`).

**Class 7 (fragile tooling)** is not found only because there is no tooling — see section 9, where its absence is the finding.

---

### 4. Boundary map

**(a) Legitimately owns — nobody else does or can**
1. The documentation-only diff boundary: what a comment-only pass may and may not touch (`references/10-annotation-boundaries.md:6-20`). This is a *mode* contract, not a code-quality rule, and it is the skill's real asset.
2. The frontend annotation taxonomy — the closed `NOTE:` prefix set and its grammar (`references/20-jsdoc-patterns.md:32-37`).
3. JSDoc/TSDoc block shape for Vue/Quasar surfaces: composables, store actions, boot files, fetch wrappers.
4. The staleness contract for a comment that asserts a security, auth, or SSR assumption — currently unowned by any skill in the fleet.
5. The source-citation boundary *inside code comments*: `references/00-source-map.md:31`, "Do not cite community material inside JSDoc or inline comments." This single line is the only content in that file that is genuinely this skill's.

**(b) Must disclaim, with the owner named**

| Ground | Owner it must name |
|---|---|
| Comment-vs-extract, SOLID, clean code | `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`) |
| Threat classes; what counts as a security assumption | `/alaa-security-review` (`$alaa-security-review`) |
| Gateway/trusted-header facts an `AUTH NOTE:` may assert | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) |
| SSR, hydration, lifecycle behavioural facts | `/alaa-frontend-developer`, `/alaa-quasar-app-vite-v3` |
| Every NAME and VALUE a comment quotes (header names, route names, storage keys) | `/alaa-services-contract` |
| Persian-language documentation | `/alaa-repo-docs` |
| Test design and proof levels | `/alaa-testing-strategy` |
| The quality bar itself | `/alaa-project-constitution` |
| Output discipline | `/alaa-low-noise` |
| Model and effort | `/alaa-prompting-guide` and its `references/50-effort-and-thinking.md` |

**(c) Where it legislates an owner's ground in its own voice**
- `references/30-ssr-hydration-and-store-notes.md:7-9` states SSR law as fact — "browser-only APIs must stay out of SSR render paths", "request-scoped state must not leak through module globals". These are substantively `alaa-vue-typescript-clean-code/SKILL.md:217` and `:191`, uncited.
- `references/30-ssr-hydration-and-store-notes.md:28` asserts gateway/BFF/cookie-flow taxonomy — `alaa-trust-gateway-auth` ground and `alaa-frontend-developer/references/21-ssr-auth-and-session-patterns.md` ground, uncited.
- `references/10-annotation-boundaries.md:41` — "If the file is actively changing for unrelated reasons, avoid mixing documentation edits into it" — is change-control doctrine (`alaa-workflow` / `alaa-controlled-ops`), stated uncited.
- `references/00-source-map.md:7-17` is a third source-priority ladder in one batch, alongside `alaa-vue-typescript-clean-code/SKILL.md:36-43` and `alaa-mono-package/references/00-source-map.md:7-19`.

---

### 5. Duplication

| # | Location A | Location B | Survives |
|---|---|---|---|
| 1 | `alaa-vue-typescript-clean-code/references/30-clean-code-solid-vue.md:101` ("Comment why a non-obvious constraint exists, not what the code says") and `:130` ("Comments explaining *what* unclear code does → extract and name after the comment; keep *why* comments") | `alaa-frontend-doc-annotations/references/20-jsdoc-patterns.md:40-44` + `SKILL.md:57-72` | **doc-annotations.** Clean-code keeps only the *smell name* in its Dispensables catalogue (the catalogue's completeness matters) and routes the rule out. |
| 2 | `alaa-vue-typescript-clean-code/references/30-clean-code-solid-vue.md:62` (remove stale comments), `:67` (no commented-out implementations), `:68` (no broad TODOs without owner/reason/boundary) | `alaa-frontend-doc-annotations/references/10-annotation-boundaries.md:33-36` ("Bad targets") | **doc-annotations**, expanded into explicit rules with a checker. Clean-code drops to a one-line pointer. |
| 3 | `alaa-vue-typescript-clean-code/references/20-typescript-composition-contract.md:97` — `any` allowed only "with a comment and immediate typed wrapper" | nothing in doc-annotations | **Both, split.** Clean-code keeps the *requirement* (a `tsc`-adjacent rule); doc-annotations gains the *shape* of that docblock. This is the Batch-2 invariant-docblock precedent in frontend form and is a seam, not duplication. |
| 4 | `alaa-frontend-developer/references/20-vue-js-ssr-patterns.md:107-117` — "JSDoc default ... prefer English JSDoc that explains: what it does, why it exists, how it works, usage shape, constraints or trade-offs" | `alaa-frontend-doc-annotations/references/20-jsdoc-patterns.md:6-27` | **doc-annotations.** `alaa-frontend-developer` already delegates at `:117` ("For documentation-only changes, pair with `$alaa-frontend-doc-annotations`") but states the content first — it should state the pointer only. Out-of-batch note: it is in Batch 6, so this is in scope. |
| 5 | `alaa-frontend-doc-annotations/references/00-source-map.md:7-17` (source ladder) | `alaa-vue-typescript-clean-code/SKILL.md:36-43`; `alaa-frontend-developer` | **the two larger skills.** doc-annotations cuts its ladder to a pointer and keeps only `:31` (no community citations inside comments) and the freshness-trigger list at `:21-27`, which is genuinely comment-specific. |
| 6 | `SKILL.md:66` | `references/00-source-map.md:46` | **`00-source-map.md`** (it carries the contrast with the anti-pattern). Body example deleted. |
| 7 | `SKILL.md:39-47` | `SKILL.md:82-91` | **one merged observable-condition table.** |
| 8 | `alaa-ui-ux-design-system/references/55-component-library-and-governance.md:27` requires each shared component to document purpose/variants/states/a11y "docblock or co-located md" | `alaa-frontend-doc-annotations/references/20-jsdoc-patterns.md:6-14` (file-level header) | **ui-ux-design-system** for *what a component must document*; **doc-annotations** for *the docblock's form*. Currently neither cites the other. Flag for the design-system lane. |

---

### 6. Wording-test failures

1. `references/20-jsdoc-patterns.md:18` — "Use JSDoc for functions, actions, helpers, or composables **when it adds real value**."
 *Failure:* the self-granted exception with no external referent; an agent that writes zero docblocks has complied.
 *Replacement:* "Write a JSDoc block on every exported function, store action, and composable. For a non-exported function, write one only when its behavior depends on a precondition the caller must satisfy, and state that precondition in the first line."

2. `SKILL.md:19` — "SSR, hydration, store, auth, and lifecycle notes **where they help future agents and maintainers**."
 *Failure:* an abstract condition standing in for an observable one; unfalsifiable.
 *Replacement:* "Annotate a function when its correctness depends on a fact not visible inside the function: the render phase it may run in, the auth state it assumes, or the store that must already be hydrated."

3. `references/20-jsdoc-patterns.md:7` — "Use a short file header when a file has **non-obvious** responsibility, lifecycle constraints, or SSR behavior."
 *Failure:* abstract noun (`non-obvious`) as the trigger condition.
 *Replacement:* "Write a file header when the file registers a side effect at import time, is imported by a boot file or a router guard, or branches on an SSR flag."

4. `SKILL.md:96` — "Keep comments **plain, useful, and short**."
 *Failure:* three abstract adjectives, no scope, no measurable bound.
 *Replacement:* "An inline comment is at most two lines. A comment that needs more than two lines becomes a function-level or file-level block."

5. `references/30-ssr-hydration-and-store-notes.md:12` — "**deterministic rendering matters**."
 *Failure:* a statement of fact standing in for a rule; there is no action an agent can take or omit.
 *Replacement:* "Where a render path reads `Date`, `Math.random`, `window`, or a locale-dependent formatter, annotate that line with `HYDRATION NOTE:` naming the value that must be identical on server and client."

6. `references/30-ssr-hydration-and-store-notes.md:26` — "**note whether** a fetch wrapper runs in SSR, client, or both."
 *Failure:* preference verb where a constraint was meant; no consequence for omission.
 *Replacement:* "Every exported fetch wrapper carries a JSDoc line stating exactly one of `runs: server`, `runs: client`, or `runs: both`. A wrapper without that line is a finding of the annotation pass."

7. `references/10-annotation-boundaries.md:42` — "Keep comment wording **simple and stable across future refactors**."
 *Failure:* an unverifiable prediction about the future, and a prohibition with no positive replacement.
 *Replacement:* "Do not name a local variable, a file path, or a line number inside a comment. Refer to the exported symbol or the module's public name, which survive a rename."

8. `references/10-annotation-boundaries.md:36` — "comments inside templates **unless the repo explicitly wants them**."
 *Failure:* an exception whose referent does not exist — nothing tells the agent where a repo would say so.
 *Replacement:* "Do not add comments inside `<template>` unless the repo's `AGENTS.md` names template comments as a convention or the existing template already contains them."

**Passes worth preserving:** `SKILL.md:98` ("Re-check official sources before writing comments that claim current, latest, deprecated, or unsupported behavior") states its trigger as four literal words an agent can match — this is the correct form and should be the model for the rewrite. `references/10-annotation-boundaries.md:9-20` (the allowed/not-allowed lists) also passes.

---

### 7. Stale or unverifiable claims

The skill makes no version-sensitive claim, because it names no tool — which is why section 9 exists. What the expanded skill will assert, and what each needs:

| Claim it will need | Status | Research needed |
|---|---|---|
| `eslint-plugin-jsdoc` rule names `check-tag-names`, `check-param-names`, `require-param`, `informative-docs` | **Verified live today.** `check-tag-names` "Reports invalid block tag names" and carries a `typed` option that reports *redundant* tags under TypeScript — directly relevant, since it makes `@param {Type}` in a `.ts` file a lint error rather than a preference. Registry mirror shows the plugin at 54.x. | Re-verify the major and the flat-config vs eslintrc form against the `client` repo's ESLint major at authoring time. |
| `vue-tsc` type-checks JSDoc in `.js` and in `.vue` `<script>` blocks under `allowJs`/`checkJs` | **UNVERIFIED — do not assert.** `vuejs/language-tools` issue #3192 records that Volar historically did not take over `.js` type-checking. Whether current `vue-tsc` does is version-dependent. | Must be tested against the `client` repo and its installed `vue-tsc`, not asserted from docs. This is the single claim most likely to become a false rule. |
| `@throws`, `@deprecated`, `@example`, `@since` are honoured by the repo's editor tooling and by `check-tag-names` defaults | Unverified. `@throws` in particular is **not** enforced by TypeScript — a `@throws` tag is prose unless a lint rule checks it. | Live check of `check-tag-names` default tag set. |
| Quasar's SSR discriminator (`process.env.SERVER` vs `import.meta.env.SSR`) | Owner is `alaa-quasar-app-vite-v3`. | Cite, do not restate. Restating it here creates the fourth copy of a Quasar fact in Batch 6. |
| The four URLs at `references/00-source-map.md:11-15` | **Current.** `https://vite.dev/` is the live Vite domain (not `vitejs.dev`), and `https://vuejs.org/about/releases` resolves. | None. |

Sources: [eslint-plugin-jsdoc check-tag-names](https://github.com/gajus/eslint-plugin-jsdoc/blob/main/docs/rules/check-tag-names.md), [check-param-names](https://github.com/gajus/eslint-plugin-jsdoc/blob/main/docs/rules/check-param-names.md), [require-param](https://github.com/gajus/eslint-plugin-jsdoc/blob/main/docs/rules/require-param.md), [rules index mirror, 54.3.0](https://tessl.io/registry/tessl/npm-eslint-plugin-jsdoc/54.3.0/files/docs/rules.md), [vuejs/language-tools #3192](https://github.com/vuejs/language-tools/issues/3192), [vue-tsc package](https://github.com/vuejs/language-tools/blob/master/packages/tsc/README.md).

---

### 8. Router audit

**Reference count.** 4 today, 8 after the expansion in section 11 — still ≤8, so the router stays a table in `SKILL.md` under the binding convention, and no `references/00-topic-map.md` may be created.

**Router location — VIOLATION.** Two routers, both in the body: `SKILL.md:39-47` (`Quick start`) and `SKILL.md:82-91` (`Reference navigation`). They disagree: the first mandates `00` and `10` in sequence; the second presents all four as equal peers. One merged table must survive.

**The `00-source-map.md` question — LEGITIMATE, keep the name.** It is *not* a router. It routes to no reference file; it contains a source-priority ladder (`:7-17`), freshness triggers (`:21-27`), a citation boundary (`:31-33`), and an anti-pattern pair (`:37-49`). That is a source-provenance ledger. It also matches a fleet convention: `alaa-mono-package/references/00-source-map.md` and `alaa-vue-typescript-clean-code/references/00-source-map.md` occupy the same slot for the same purpose. No violation.

**Observable-condition test — 1 of 6 rows passes.**
- `SKILL.md:43` — "when a comment depends on current Vue, Quasar, Vite, SSR, or browser behavior → `references/00-source-map.md`" — **PASSES**, states a condition.
- `SKILL.md:44` — "Read `references/10-annotation-boundaries.md`" — no condition at all.
- `SKILL.md:84-85`, `86-87`, `88-89`, `90-91` — **all four are heading mirrors.** "JSDoc shapes, comment styles, and comment density rules → `references/20-jsdoc-patterns.md`" restates the file's title; it never tells the agent what situation it is in.

**Dangling paths — none.** All four `references/*.md` resolve on disk. No bare cross-skill `references/…` path appears. Of the three companion skills named, `alaa-frontend-developer` and `alaa-quasar-app-vite-v3` are present in Batch 6; `alaa-repo-docs` is Batch 8 and out of this tree, not dangling.

**Inbound pointers to this skill — seven, across two skills, all `$`-only:** `alaa-frontend-developer/SKILL.md:77`, `:170`; `alaa-frontend-developer/references/10-contract-and-boundaries.md:111`; `:20-vue-js-ssr-patterns.md:117`; `:70-companion-skill-routing.md:47`; `:80-legacy-skill-coverage.md:86`; `alaa-frontend-devops/SKILL.md:69`.

**Cross-lane observation, offered as fact and not as judgment:** `alaa-vue-typescript-clean-code` ships both `references/00-source-map.md` and `references/05-topic-map.md`, and routes into the latter from `SKILL.md:49` while also carrying a body-level `Required reference loading` list at `SKILL.md:45-61`. That lane owns the question.

---

### 9. Tooling audit

The skill ships no script. For a skill whose every rule is a text convention, that is not a missing nicety — it is the reason all ten criteria fail. An annotation rule with no checker is a preference.

**Ship `scripts/check-annotations.mjs`.** Node, no dependencies beyond what a Quasar repo already has, invoked as `node scripts/check-annotations.mjs <src-dir>`.

**What it asserts**

1. **Cross-file surface has a docblock.** Every exported function, arrow-const, and store action in a module imported by two or more other modules carries a leading `/** … */`. Scoped to the cross-file surface so it does not become noise on local helpers.
2. **The prefix set is closed.** Every `NOTE:`-suffixed prefix in a comment is one of `SSR NOTE:`, `HYDRATION NOTE:`, `STORE NOTE:`, `AUTH NOTE:`, `SECURITY NOTE:`. A sixth invented prefix is an error — this is what turns the taxonomy into a reliable `grep` index.
3. **Security-bearing annotations carry a verification date and cannot go stale silently.** Every `AUTH NOTE:` and `SECURITY NOTE:` carries `verified:<ISO-date>`. Error when `git log -1 --format=%cI -- <file>` is newer than that date. This is the assertion that makes a security comment load-bearing rather than decorative, and it is the one thing no other skill in the fleet does.
4. **Types belong to the type checker.** In a `.ts` file or a `<script lang="ts">` block, no `@param {Type}` / `@returns {Type}`. The script does not reimplement this — it asserts that `eslint-plugin-jsdoc` is configured with `check-tag-names` in `typed` mode and defers, honouring the standing "wrap the official capability" preference.
5. **No community citation inside code.** No comment contains a `stackoverflow.com` or an issue-tracker URL — the mechanical form of `references/00-source-map.md:31`, which is today an unenforced sentence.
6. **Comments in files are English.** Every comment body is ASCII-range. On a Persian/RTL repository this is the assertion that mechanically settles the seam with `alaa-repo-docs`: files are English, only terminal replies to the owner are Persian.

**Exit codes**

- `0` — every assertion passed.
- `1` — annotation defects found. One `path:line: <rule-id> <message>` per line on stdout, machine-readable, so CI and an agent read the same output.
- `2` — could not run: no source directory, unreadable `tsconfig`, or a file that failed to parse. Deliberately distinct from `1` so CI can never mistake "did not check" for "clean". The script must never exit `0` with an unparsed file.

**What it would find on `client` today**

- The permission-bitmap decode site documents the 512-byte-capped bitmap as a UI hint that is not an authorization decision. That comment is **prose with no prefix and no verification date**, so assertion 3 cannot protect it and assertion 2 does not fire. It is precisely the annotation whose staleness would be a security defect — if the backend ever stopped re-checking, the comment would still read as reassurance. After the rewrite it becomes `SECURITY NOTE: permission bitmap is a UI hint, not an authorization decision; the server re-checks every mutation. verified:2026-07-28`, and assertion 3 fails the build the next time the file changes without re-verification.
- Assertion 6 is where the real volume of findings will be on a Persian/RTL codebase, and it is the cheapest to fix.
- Assertion 4 will produce a large first-run count on any TypeScript surface where JSDoc was ported from a JavaScript-first era — `alaa-frontend-developer/references/10-contract-and-boundaries.md:9` states the app family default is "JavaScript plus JSDoc ... unless the repo already standardizes on TypeScript", so both modes exist in the fleet and the checker must switch on the file, not on the repo.

---

### 10. THE EXISTENCE RULING

### **KEEP AND EXPAND.**

**The deciding test for this seam, one sentence:**

> **A rule whose violation can be caught by compiling, type-checking, or running the code belongs to `alaa-vue-typescript-clean-code`; a rule whose violation is visible only by reading a comment against the code it claims to describe — in a diff where the build output must be identical before and after — belongs to `alaa-frontend-doc-annotations`.**

It partitions cleanly and predicts the disputed cases. "No `any`" → `tsc` catches it → clean-code. "Typed props via `defineProps<Props>()`" → `vue-tsc` → clean-code. "Comment why, not what" → only a human or an agent reading comment against code → annotations, and it therefore *moves out of* `alaa-vue-typescript-clean-code/references/30-clean-code-solid-vue.md:101`. "A `SECURITY NOTE:` must still be true" → nothing compiles it → annotations. "`@param {string}` is redundant in a `.ts` file" → an ESLint rule, not the compiler → annotations, which is right, because the annotation skill should own its own lint configuration.

**The evidence for keeping**

1. **The two skills hold contradictory mandates and cannot merge without a self-granted exception.** `alaa-vue-typescript-clean-code/SKILL.md:10` states: "The skill is mandatory quality control, not optional advice: **repair violations inside the task scope** or clearly mark them as blockers." A documentation-only lane must *forbid* repair — `references/10-annotation-boundaries.md:18-20` bars logic, template, and CSS changes outright. A merged skill would carry "repair violations" and "change nothing but comments" in the same body, resolvable only by an exception clause with no external referent, which the wording test names as a defect class. That is not a stylistic objection; it is the merge failing on its own terms.

2. **The clean-code skill's operating model has no room for the mode.** `alaa-vue-typescript-clean-code/SKILL.md:67-72` enumerates exactly four modes — new feature slice, local refactor, review, repo-wide normalization. A documentation-only mode is a fifth, and adding it grows a body already at 21,149 B. The completeness law forbids body growth net of the description. The merge is blocked by the law that would otherwise motivate it.

3. **Seven inbound pointers across two Batch-6 skills** (`alaa-frontend-developer/SKILL.md:77`, `:170`, `references/10-contract-and-boundaries.md:111`, `references/20-vue-js-ssr-patterns.md:117`, `references/70-companion-skill-routing.md:47-49`, `references/80-legacy-skill-coverage.md:86`; `alaa-frontend-devops/SKILL.md:69`). Two of these — `70-companion-skill-routing.md:47-49` and `SKILL.md:170` — are *ownership statements*, not conveniences: the frontend skill has already ceded this ground by name. Merging would require rewriting the routing tables of two other skills in the same batch, and `alaa-frontend-devops` is another lane's file.

4. **There is real, unowned ground and it is security ground.** No skill in the fleet owns "an annotation that states an authorization assumption must be verified and must fail a check when stale". A grep across all nine Batch-6 skills for `jsdoc|docblock|invariant` returns only advisory mentions: `alaa-shaka-player/SKILL.md:161`, `alaa-frontend-developer/references/20-vue-js-ssr-patterns.md:107-115`, `alaa-ui-ux-design-system/references/55-component-library-and-governance.md:27`. The `client` permission-bitmap comment is a live instance of the class and has no owner. This is not a gap invented to justify a skill; it is a gap that already shipped into production code.

5. **The Batch-2 precedent points this way.** An upstream `rules/style.md` forbidding comments was overridden *by name* because invariant docblocks are load-bearing safety documentation. That precedent creates a category — the comment that is not decoration — and a category with a doctrine-level override needs a named owner. `alaa-vue-typescript-clean-code/references/20-typescript-composition-contract.md:97` already implies one (`any` permitted only "with a comment and immediate typed wrapper") and specifies no shape for it.

**The cost I am accepting by not merging.** The skill as it stands is 8,082 B of almost entirely unenforceable preference, it duplicates six comment rules that `alaa-vue-typescript-clean-code` already states better, and it names no owner for anything. Keeping it means a *rewrite*, not a preservation — nearly every sentence in `references/20-jsdoc-patterns.md` and `references/30-ssr-hydration-and-store-notes.md` fails the wording test. If Phase 2 keeps the skill and does not expand it, the correct ruling reverses to MERGE, because a mode contract with no checkable rules is worth less than a paragraph inside a skill agents already load.

**The cost of MERGE, which I did not choose.** Seven inbound pointers rewritten across two skills, one of which is another lane's. `alaa-vue-typescript-clean-code`'s body grows by a fifth mode against the completeness law. The documentation-only *authority boundary* — the single genuinely valuable thing here — dissolves into a skill whose stated mandate is to repair what it finds, which is exactly the behavior a documentation pass must not exhibit. And the security-annotation staleness contract, currently unowned, would have to be hosted by a skill that has no security ground and correctly does not want any.

---

### 11. Rewrite brief for Phase 2

**Body byte budget: ≤ 2,900 B, net of the frontmatter description.** The current body is 2,927 B. Freed: Good/bad examples `SKILL.md:48-72` (~590 B), Maintenance rules `SKILL.md:93-99` (~430 B, authoring meta not addressed to the agent), one of the two routers (~250 B) = ~1,270 B. Spent: closed prefix taxonomy (~250 B), owner-disclaimer table (~350 B), checker invocation line (~120 B), English-in-files rule (~100 B), merged observable-condition router (~400 B) ≈ 1,220 B. **Net ≈ −50 B.** The body shrinks slightly while gaining three capabilities.

| File | Action | Purpose |
|---|---|---|
| `SKILL.md` | rewrite, ≤2,900 B | Both trigger forms at every call site. One observable-condition router table. The closed `NOTE:` prefix set. The owner-disclaimer table from section 4(b). The `node scripts/check-annotations.mjs` line. Delete the examples block and Maintenance rules. |
| `agents/openai.yaml` | one-line edit | `default_prompt` keeps `$`-form (Codex-only file, correct as is); `short_description` widens to name the security-annotation capability. |
| `references/00-source-map.md` | cut ~1,817 → ~800 B | Keep `:21-27` (freshness triggers, comment-specific) and `:31-33` (no community citations in code — the skill's own rule). Replace the ladder at `:7-17` with a pointer to `alaa-frontend-developer`. Keep the anti-pattern pair at `:37-49` as the sole home of that example. |
| `references/10-annotation-boundaries.md` | keep, extend | Add the missing failure rule: what the pass does when it finds a comment that is now false. Replace `:42` and `:36` per section 6. |
| `references/20-jsdoc-patterns.md` | rewrite | Preferences → constraints. Add the `@throws` / `@deprecated` / `@example` / `@see` / `@since` contract (criterion 10). State the TS-vs-JS split: `@param {Type}` forbidden in TypeScript, required in a JS+JSDoc module. |
| `references/30-ssr-hydration-and-store-notes.md` | rewrite | Every "worth capturing" bullet becomes a constraint bound to its prefix. Cite `alaa-frontend-developer` / `alaa-quasar-app-vite-v3` for the SSR facts instead of restating them (section 4(c)). |
| **NEW** `references/40-security-and-trust-annotations.md` | create | The load-bearing class. The `client` permission-bitmap worked example in full. `verified:<date>` fields. Names `/alaa-security-review` and `/alaa-trust-gateway-auth` as the owners of what may be asserted. States that a stale security annotation is worse than none. |
| **NEW** `references/50-checkable-annotations.md` | create | Which annotation participates in which tool. The exact `eslint-plugin-jsdoc` rule set per repo language mode. What `vue-tsc` does and does not check — flagged as requiring live verification per section 7. Closes criteria 1 and 8. |
| **NEW** `references/60-staleness-and-verification.md` | create | The staleness contract, the git-mtime-vs-`verified:`-date test, and the checker's exit-code meanings. Closes criterion 2. |
| **NEW** `references/70-invariant-docblocks.md` | create | The Batch-2 precedent ported to frontend: a docblock stating an invariant is load-bearing safety documentation and overrides any repo rule forbidding comments outside config files. Names the rule it overrides. Pairs with `alaa-vue-typescript-clean-code/references/20-typescript-composition-contract.md:97`. |
| **NEW** `scripts/check-annotations.mjs` | create | Section 9 in full. |
| `alaa-vue-typescript-clean-code/references/30-clean-code-solid-vue.md:62,67,68,101` | in-batch edit | Replace the four comment rules with one pointer. Keep the smell *name* at `:130` for catalogue completeness; move the repair to doc-annotations. |
| `alaa-frontend-developer/references/20-vue-js-ssr-patterns.md:107-117` | in-batch edit | Reduce the JSDoc-content list to the existing pointer at `:117`. |

**Files to retire: none.** All four existing references earn their place after rewrite; nothing goes to `_to_delete/`.

**Genuinely new capability gained — three, and they must be stated as such in the batch report:**
1. A mechanical staleness check for security-bearing annotations (`verified:` date vs git mtime). No skill in the fleet has this.
2. A closed, greppable annotation taxonomy that doubles as a retrieval index for the next agent — the direct answer to criterion 9.
3. An English-only-in-code-comments assertion that mechanically settles the `alaa-repo-docs` seam on a Persian/RTL repository, without either skill legislating the other's ground.

The skill will grow from 8,082 B to roughly 14,000 B across body and references. Under the completeness law this is correct: the body does not grow, the references become complete, and three named capabilities are gained.

**Collision check against `alaa-repo-docs` (Batch 8):** one live risk, at `SKILL.md:79-80` — "Broader repo docs and README alignment: pair with `$alaa-repo-docs`". That row invites an agent to treat `alaa-repo-docs` as the README owner and, by association, to write Persian into files. The programme rule is that everything written into a file is English and only terminal replies are Persian. The skill states "English JSDoc" once at `SKILL.md:17` and never for inline comments. Fix: state the English-in-files rule once in the body for all comment forms, and narrow the `alaa-repo-docs` row to Persian-language *deliverables only*.

---

### 12. Gap no existing skill can own

**None.**

The one candidate I tested and rejected: *an annotation asserting a fact whose truth can change without the annotated file changing* — a comment in `client` stating that the gateway strips a header, invalidated by a config change in a different repository. That is real (the permission-bitmap comment is exactly this class: its truth depends on the Laravel side continuing to re-check every mutation), and no skill currently detects it.

But it is ownable within the existing map, and inventing a skill for it would be the failure mode the brief warns against. `alaa-services-contract` already owns every NAME and VALUE, so a comment quoting a header name or a route name is already its ground. The correct resolution is a rule inside `references/40-security-and-trust-annotations.md`: *a comment asserting a cross-service fact cites `/alaa-services-contract` as the source of that value rather than restating the value inline* — which converts the invalidation problem into an existing skill's existing responsibility, and makes the checker's assertion 5 (no inline restatement of a contract value) enforce it.


---

## Appendix H — `alaa-indexeddb-browser-storage`

### 1. What this skill is today

**Subject.** IndexedDB and browser origin-storage as a discipline: storage-API selection, capability tiers, quota/persistence/eviction, schema versioning and multi-tab upgrade safety, transaction/index/cursor performance, client-side data classification and token boundaries, offline cache/outbox/draft patterns, and browser test strategy. It is explicitly written as a general web-storage skill with an Alaa integration layer bolted on (`references/95-alaa-integration-playbook.md`) rather than as a repo-bound skill.

**Register.** Declarative rule prose with heavy use of bullet policy lists, decision tables, and code fences containing type declarations rather than runnable code. It is the most *documented* skill in the batch and the least *executable* — nine TypeScript examples exist but nothing in the pack runs them, type-checks them, or drives them against each other.

**Shape and byte sizes.**

| Segment | Files | Bytes | Share |
|---|---:|---:|---:|
| `SKILL.md` (always-loaded body) | 1 | 9,267 (frontmatter description 323) | 4.7% |
| `agents/openai.yaml` | 1 | 541 | 0.3% |
| `skill-pack-manifest.json` | 1 | 1,915 | 1.0% |
| `references/` — 13 topic files | 13 | 75,521 | 38.4% |
| `references/full-guide.md` | 1 | 74,929 | **38.1%** |
| `examples/` | 9 | 21,421 | 10.9% |
| `assets/` | 7 | 10,623 | 5.4% |
| `scripts/` | 2 | 2,286 | 1.2% |
| **Total** | **35** | **196,503** | |

No `__pycache__`, no stray build artifacts, no orphan directories. `scripts/validate_skill_pack.py` and `scripts/check_references.py` both exit 0 today.

---

### 2. Ten-criteria verdict

| # | Criterion | Verdict | Evidence |
|---|---|---|---|
| 1 | Correctness and testability | **FAILS** | `references/40-schema-versioning-migrations-and-concurrency.md:95` creates `byStatusRetryAt` over `['status','retryAt']` while the record type at `references/70-offline-sync-outbox-cache-patterns.md:58` has `nextAttemptAt` and `examples/migration-pattern.ts:23` indexes `['status','nextAttemptAt']` — an agent following the reference builds an index over a missing key path, records are silently unindexed, and `examples/outbox-pattern.ts:28` returns an empty batch forever. `examples/browser-capabilities.ts:73-78` can never return tier 3. No harness drives the three capability-contract declarations. |
| 2 | Failure behavior | **FAILS** | Prose is strong and correctly failure-class-shaped (`references/80-testing-debugging-and-observability.md:151-183` is a real symptom→diagnosis→action tree). But `examples/outbox-pattern.ts:46` marks items `inflight` and no shipped code or written rule ever re-claims an item orphaned by a reload — permanent silent loss of user mutations; `examples/outbox-pattern.ts:104-106` counts HTTP 401/403 into `dead` while writing status `pending`; `examples/outbox-pattern.ts:100` awaits `send` with no timeout. `alaa-reliability-sla` is named zero times. |
| 3 | Security | **FAILS** | Domain content is the pack's best (`references/60-security-privacy-and-data-classification.md:16-31`, `:38-47`, `:69-73`). But it runs its own "Security review checklist" at `:161-176` and mints `security_review_required` at `assets/data-classification-policy.yaml:25` without naming `alaa-security-review`; it legislates entitlement-snapshot caching at `:65` and `:47` without naming `alaa-permission-generator`; and `examples/alaa-client-storage.ts:55-64` performs the logout purge as four independent transactions, so a crash mid-purge leaves the previous account's records readable. Silence on an owner is FAILS, not NOT-OWNED. |
| 4 | Observability | **FAILS** | `references/80-testing-debugging-and-observability.md:84-93` mints nine event names (`idb_open_success`, `storage_quota_exceeded`, `outbox_backlog`, …) in the skill's own voice. `alaa-services-contract` owns every registered event and log-field name and is named once at `SKILL.md:102` — for API envelopes, not for these names. `alaa-observability-soc` (requirement levels and gates) is named zero times; there is no MUST/SHOULD level and no gate on any of the nine events. |
| 5 | Concurrency and load | **FAILS** | Covers `versionchange`/`blocked` (`references/40-…:134-169`), a `BroadcastChannel` message vocabulary (`:157-167`), and `navigator.locks`-or-lease (`:209-220`). Missing entirely: a service worker writing while a tab writes is named nowhere as a concurrency case — `serviceWorker` appears only as a capability flag at `examples/browser-capabilities.ts:53`. The lease type at `references/40-…:213-220` has `heartbeatAt` with no renewal interval, no expiry rule, and no takeover rule. `examples/outbox-pattern.ts:46` mutates an index key inside the cursor iterating that index and is only safe because `'inflight'` sorts before `'pending'`; nothing states that invariant, so renaming the status to e.g. `'processing'` yields an infinite claim loop. |
| 6 | Clean code, SOLID, design patterns | **FAILS** | `examples/fallback-memory-store.ts:1-6` defines `KeyValueStore<T>` and `MemoryStore` implements it, but `examples/alaa-client-storage.ts:20` implements no interface at all, so the Tier 0 fallback the file exists to provide cannot be substituted for the real facade. The facade boundary at `references/95-alaa-integration-playbook.md:139-177` is sound but has no code counterpart. |
| 7 | Algorithm/data-structure choice with stated complexity budgets | **FAILS** | Index-design guidance exists (`references/50-transactions-performance-and-query-patterns.md:103-140`) and latency budgets exist (`references/80-…:98-117`), but no complexity budget is stated anywhere — no O() claim, no bound on records scanned. `examples/alaa-client-storage.ts:73` performs a full-store cursor scan per store on every logout across four stores, and `examples/migration-pattern.ts:17-33` creates no `accountKey` index on `drafts` or `upload_resume_state`, so the purge is unbounded by construction. The comment at `examples/alaa-client-storage.ts:71` ("Prefer account indexes in production") acknowledges it and stops there. This is the one place in the batch where complexity budgets are literally applicable and the skill does not state one. |
| 8 | Configurability with safe defaults and boundary validation | **FAILS** | `examples/quota-manager.ts:55` hardcodes `0.85` and `50 * 1024 * 1024` as unnamed literals; `examples/outbox-pattern.ts:72,77` hardcodes a 1-hour backoff cap and a 10-attempt limit. `references/30-…:99-106` gives `softStop`/`hardStop` formulas in a `text` fence that no code consumes. `assets/storage-budget-policy-template.md:9-15` ships empty cells with no validation rule and no bounds. |
| 9 | Speed of development and debuggability | **SATISFIED** | `references/80-…:151-183` is a genuine symptom-indexed decision tree; `:60-77` gives the exact DevTools path per engine; `:84-93` gives a copyable telemetry union; `SKILL.md:108-117` ships grep-bait exact-search terms. Both scripts run clean. Caveat, not disqualifying: `references/80-…:25` says "quota/low-storage simulation where possible" and never states how, so the one failure the skill cares most about has no local reproduction recipe. |
| 10 | Documentation | **SATISFIED** | Three output contracts (`references/90-…:35-108`), a release checklist (`references/80-…:132-149`), four templates plus an Alaa ADR starter in `assets/`, a dated source list with per-claim attribution (`references/99-sources-and-maintenance.md:36-48`) and a maintenance schedule (`:50-59`). |

**Standing preference 1 (wrap official capabilities).** Partially honoured. `examples/idb-core.ts` is a thin wrapper over native IDB and labels itself "examples for agents to adapt, not a required library" (`:2-3`), and `references/05-source-priority-and-freshness.md:18` lists `idb`/Dexie as authoritative sources. But the skill nowhere says "use `idb` unless X" — it reimplements the promise wrapper and the `getAll` fallback that `idb` already ships. **Standing preference 2 (uniformity over local optimality).** Violated three ways: the capability contract is declared three times with three different field sets (below); `dataClass` has two incompatible taxonomies; `retryAt` vs `nextAttemptAt`.

---

### 3. Defect classes actually found

**Class 1 — stale hardcoded model pins.** Confirmed at `references/99-sources-and-maintenance.md:32` and `references/full-guide.md:2128`, both citing the GPT-5 prompting guide as the current authority. *Extension:* no third instance exists — grep for `GPT-5|gpt-5` returns exactly those two lines. `agents/openai.yaml` carries no model pin. Consequence: an agent asked to align this skill's own authoring register fetches a superseded guide, and the model/effort question is answered from a stale source instead of routed to `/alaa-prompting-guide`.

**Class 2 — wrong/absent trigger syntax.** `$alaa-*` appears 16 times (`SKILL.md:99-106` ×5, `references/90-…:113,128,141,150,159` ×5, `references/full-guide.md:1783,1798,1811,1820,1829` ×5, `agents/openai.yaml:4`); `/alaa-*` appears **zero** times. Consequence: every cross-runtime call site — five prompt patterns in `references/90-…` written to be pasted by a user, and the entire companion-pairing table — is unusable verbatim in Claude Code.

**Class 3 — duplication between body and references.** Two instances. (a) `references/full-guide.md` is a 74,929-byte concatenation of the thirteen topic references at 99.75% whitespace-normalized identity — section 5 below. (b) `SKILL.md:63-78` reproduces all twelve rows of `references/00-topic-map.md:7-20` verbatim, and `SKILL.md:82-93` restates `references/60-…:16-31`, `references/30-…:110`, `references/40-…:5-13` and `references/50-…:22-27`. Consequence: 4.9 KB of the 9.3 KB always-loaded body is a second copy of routed content, and every rule now has two homes that can drift.

**Class 4 — project-specific content in an always-loaded body.** `SKILL.md:60` (`@alaa/sdk` / `@alaa/sdk-vue` route composition), `SKILL.md:82` (`X-Access`, OpenFGA), `SKILL.md:84` (the exact three-header allowlist `Authorization: Bearer`, `X-Request-Id`, `traceparent`). Consequence: three values owned by `alaa-trust-gateway-auth` and `alaa-services-contract` are pinned in the body, so a gateway header change silently invalidates the always-loaded text of an unrelated skill.

**Class 5 — long numbered procedures nobody reads in order.** `references/95-alaa-integration-playbook.md:179-190` ("Implementation sequence", 10 steps), `references/90-…:20-33` ("Default task workflow", 12 steps), `SKILL.md:51-61` ("Quick start workflow", 9 steps), `references/60-…:76-90` (logout purge, 7 steps). Consequence: the logout purge — a security operation — is a 7-step linear list rather than a failure-class entry, so nothing in it states what to do when step 3 fails after step 2 succeeded. Counter-example worth preserving: `references/80-…:151-183` and `references/30-…:110-124` *are* correctly failure-class-shaped and should be the model.

**Class 6 — description with no "do not use for" clause.** `SKILL.md:3`, 323 bytes, entirely "Use this skill when…". The body does carry a "When NOT to use" section at `SKILL.md:41-49`, but that is not what drives triggering. `agents/openai.yaml:7` sets `allow_implicit_invocation: true` with `primary_domains` and no negative domains. Consequence: this skill fires on any Quasar service-worker or Cache API task that mentions offline, competing with `alaa-quasar-app-vite-v3` — whose own SKILL.md correctly routes *to* this one.

**Class 7 — fragile tooling.** The flagged `Path(__file__).resolve().parents[1]` at `scripts/check_references.py:5` and `scripts/validate_skill_pack.py:6` is **not** the defect: it is CWD-independent and resolves correctly from `/tmp`, from the pack root, and from `scripts/` — I ran all three. It is the right idiom. The real defect is at `scripts/check_references.py:8`: the regex requires a backticked `` `references/…` `` prefix, but `references/00-topic-map.md:9-20` writes bare filenames (`` `05-source-priority-and-freshness.md` ``). The first alternation therefore matches **nothing** — the script validates 16 paths, all of them examples and assets, and **zero reference files**, then prints `OK: topic-map references exist`. Consequence: the one tool named for reference integrity is structurally incapable of detecting a broken reference link and reports green while doing so. Secondary: neither script has `--help`, argparse, exit-code documentation, or a self-test; `scripts/validate_skill_pack.py:14-18` scans only `examples/*.ts` for token patterns and never scans `references/` or `assets/`.

**Class 8 — shipped `__pycache__`.** None. Clean.

**Class 9 — unnamed gaps against section 2.** `alaa-reliability-sla`, `alaa-testing-strategy`, `alaa-security-review`, `alaa-observability-soc`, `alaa-async-messaging`, `alaa-data-layer`, `alaa-permission-generator`, `alaa-keyset-pagination`, `alaa-crockford-base32-codecs`, `alaa-project-constitution` — ten owners, zero mentions, while the skill legislates on the ground of at least six of them (section 4c).

**Class 10 — body larger than it needs to be.** 9,267 bytes, of which `SKILL.md:63-78` (routing duplicate, ~1,050 B), `SKILL.md:80-93` (rules duplicated from references, ~1,900 B) and `SKILL.md:108-117` (search terms, ~900 B, arguably earns its place) are recoverable. Section 11 budgets a replacement at ≤ 6,100 B.

**Class 11 — no stated companion boundary.** Partially present and partially absent. `SKILL.md:27` disclaims "Vue, Quasar, service-worker, API-gateway, or backend implementation details" and `SKILL.md:97-106` names five companions, three of them with a specific risk. But `SKILL.md:103-104` says "Alaa observability/analytics skill **if available**" and "Alaa upload/tusd/service-contract skill **if available**" — the owners exist (`alaa-observability-soc`, `tusd-upload-platform`) and are not named, so those two rows are boundary statements that resolve to nothing.

---

### 4. Boundary map

### (a) Legitimately owns

IndexedDB API semantics and the storage-API selection decision (`references/10-…:62-72`); browser capability tiers and the runtime probe (`references/20-…:28-129`); origin quota model, persistence request timing, eviction resilience, and the `QuotaExceededError` cleanup ladder (`references/30-…` in full); client-side schema versioning, upgrade branching, `blocked`/`versionchange` handling (`references/40-…:1-169`); transaction lifetime discipline, index and compound-key design, cursor-vs-`getAll`, structured-clone limits, durability hints (`references/50-…`); which data classes may be written to browser storage at all (`references/60-…:38-47`); the local cache/draft/read-through patterns and offline UX wording (`references/70-…:11-42, 166-181`); browser-side debugging and the cross-browser test lane matrix (`references/80-…`, `assets/browser-test-matrix.yaml`). None of this has another owner in the fleet.

### (b) Must disclaim, and who owns it

| Ground | Owner to name |
|---|---|
| Retry, backoff, timeout, idempotency, degradation doctrine; fail-open for availability | `alaa-reliability-sla` |
| Outbox row-state vocabulary, consumer-side dedupe, DLQ/dead-letter replay | `alaa-async-messaging` |
| Every registered metric, event and log-field name | `alaa-services-contract` |
| Requirement levels and observability gates | `alaa-observability-soc` |
| Security review triggers, threat classes, fail-closed doctrine | `alaa-security-review` |
| Test design and the six proof levels | `alaa-testing-strategy` |
| Permission bitmap contract and the canonical decoder | `alaa-permission-generator` |
| Trust boundary; "a client-supplied opaque value carries no trust" | `alaa-trust-gateway-auth` (named once, `SKILL.md:101`) |
| Identifier codec and its JS implementation | `alaa-crockford-base32-codecs` |
| Paginating unbounded collections | `alaa-keyset-pagination` |
| The quality bar itself | `alaa-project-constitution` |
| Service-worker implementation depth / SW policy | `alaa-quasar-app-vite-v3` / `alaa-frontend-developer` (both named, `SKILL.md:100`) |

### (c) Places it legislates an owner's ground in its own voice

**Against `alaa-reliability-sla`:**

- `references/70-…:74` — "Use backoff with jitter." No base, no cap, no attempt limit, no timeout; retry doctrine stated as a bare imperative with no owner.
- `references/70-…:126-140` — the eight-step "Outbox sync algorithm" including `retryable error -> pending with backoff`, `conflict -> failed/conflict`, `forbidden -> dead/failed after server confirmation`. This is a degradation and classification policy written in this skill's voice.
- `examples/outbox-pattern.ts:72` — `Math.min(60 * 60 * 1000, Math.pow(2, attempts) * 1000 + Math.floor(Math.random() * 1000))` and `:77` `attempts >= 10 ? 'dead' : 'pending'`. Three reliability constants minted here. Note against the verified platform fact: the *server-side* outbox has no timeout, attempt cap, backoff or quarantine, so this browser outbox is strictly more elaborate than the system it feeds and the skill never says so.

**Against `alaa-async-messaging`:**

- `references/70-…:54` — `status: 'pending' | 'inflight' | 'done' | 'failed' | 'dead';` and `references/95-…:79` repeats the same five-state set. This is a row state set for an outbox, minted in this skill's voice, with `dead` implying a dead-letter concept whose replay semantics live in `alaa-async-messaging`.
- `references/70-…:68` — "Every network mutation must be idempotent or have a client mutation ID," and `references/70-…:145` "Idempotent append with event IDs; server dedupe." Consumer-side dedupe is the owner's ground.
- **Required disclosure that is missing:** the skill never says whether a *browser* outbox shares vocabulary with the server-side one or is deliberately distinct. My reading of the evidence: it must be **deliberately distinct**, because the server outbox claims rows with `DELETE … FOR UPDATE SKIP LOCKED … RETURNING` (the row ceases to exist on claim) whereas the browser outbox mutates a status field in place and therefore has an orphan-`inflight` class the server outbox structurally cannot have. Reusing `pending/inflight/done/failed/dead` invites an agent to assume the server's claim semantics and skip the reaper. Phase 2 must state the distinction explicitly and rename the browser states or annotate them.

**Against `alaa-services-contract`:**

- `references/80-…:84-93` — nine event names minted as a TypeScript union.
- `references/40-…:17-21` and `references/95-…:23-29` — `DB name: alaa-client-storage`, `accountKey = publicProjectId:userId`. A delimiter-joined identifier composition scheme with no stated codec, escaping rule, or collision behaviour, minted here.
- `references/40-…:40-52` — eleven object-store names fixed in this skill's voice.

**Against `alaa-observability-soc`:** `references/30-…:196-212` and `references/80-…:79-96` state what to log with no requirement level and no gate.

**Against `alaa-security-review`:** `references/60-…:161-176` "Security review checklist"; `references/60-…:85` "do not store it in IndexedDB without a security review"; `assets/data-classification-policy.yaml:25` `indexeddb: security_review_required`. Three review triggers with no named approver and no named owning skill.

**Against `alaa-permission-generator` and `alaa-trust-gateway-auth`:** `references/60-…:65` — "IndexedDB may store `entitlementSnapshot` only as a non-authoritative UX cache with TTL and server revision" and `references/60-…:47` — "Cache display hints only with TTL/server revision; never authoritative." The verified platform fact is that `client` decodes a permission bitmap capped at 512 bytes, documented as a UI hint that is not an authorization decision. This skill is legislating the caching policy for exactly that artifact, under a name it invented (`entitlementSnapshot`), without naming the bitmap, the 512-byte cap, the canonical decoder, or `alaa-permission-generator`.

**Identifier and bitmap handling in `examples/`:** no example decodes a permission bitmap — good. No example generates or parses a domain identifier: `examples/vitest-idb-pattern.test.ts:10` uses `crypto.randomUUID()` only to name a throwaway test database, which is not a domain identifier and does not require routing to `alaa-crockford-base32-codecs`. `examples/outbox-pattern.ts:8` declares `idempotencyKey: string` and never produces one — the field is a hole where an identifier will be generated by whoever copies the file, and nothing routes them. That is the one place a codec route is owed.

**Against `alaa-keyset-pagination`:** `references/50-…:76-96` teaches cursor-and-`IDBKeyRange` pagination over potentially unbounded local collections without naming the owner of pagination doctrine. Lower severity — local cursors are genuinely this skill's ground — but the *contract* (page size, continuation token shape) is not.

---

### 5. The `full-guide.md` ruling

**Finding: `references/full-guide.md` is a mechanical concatenation of the thirteen topic references at 99.75% whitespace-normalized similarity, contributing zero unique content.**

Empirical method and result. I split `full-guide.md` on its own `<!-- source: references/… -->` markers (13 markers, at lines 8, 61, 122, 238, 393, 611, 851, 1105, 1277, 1478, 1668, 1882, 2094) and diffed each section against the file it names:

| Source file | Raw similarity | Whitespace-normalized |
|---|---:|---:|
| `00-topic-map.md` | 1.0000 | 1.0000 |
| `05-source-priority-and-freshness.md` | 1.0000 | 1.0000 |
| `10-indexeddb-mental-model-and-boundaries.md` | 0.9001 | 0.9795 |
| `20-browser-compatibility-and-capability-tiers.md` | 1.0000 | 1.0000 |
| `30-storage-quota-persistence-and-eviction.md` | 1.0000 | 1.0000 |
| `40-schema-versioning-migrations-and-concurrency.md` | 1.0000 | 1.0000 |
| `50-transactions-performance-and-query-patterns.md` | 1.0000 | 1.0000 |
| `60-security-privacy-and-data-classification.md` | 0.9560 | 0.9894 |
| `70-offline-sync-outbox-cache-patterns.md` | 1.0000 | 1.0000 |
| `80-testing-debugging-and-observability.md` | 1.0000 | 1.0000 |
| `90-agent-workflows-prompts-and-output-contracts.md` | 1.0000 | 1.0000 |
| `95-alaa-integration-playbook.md` | 1.0000 | 1.0000 |
| `99-sources-and-maintenance.md` | 1.0000 | 1.0000 |
| **Weighted** | | **0.9975** |

Eleven of thirteen sections are byte-identical. The two that are not differ only by hard-wrap reflow and markdown table-column padding: compare `references/10-…:5-7` (wrapped at ~118 columns) against `references/full-guide.md:129` (one line), and `references/10-…:64-72` (padded table) against `references/full-guide.md:183-191` (unpadded). Not one sentence, rule, table row, code fence, or claim exists in `full-guide.md` that does not exist in a topic file. The only unique text in the entire 74,929 bytes is the two-line header at `references/full-guide.md:1-3`.

**Specific overlapping section pairs, as evidence:**

- `references/30-…:37-47` "Browser quota notes researched 2026-06-29" ↔ `references/full-guide.md:432-442`. Identical Firefox 10%/10 GiB/50%/8 TiB, Chromium 60%, Safari 60/15/80/20 figures. Both are quota claims that Phase 2 must re-research, so today the freshness surface is doubled.
- `references/60-…:16-31` "Never store" ↔ `references/full-guide.md:1120-1135`. The pack's single most security-critical list, in two places.
- `references/99-…:32` ↔ `references/full-guide.md:2128`. The confirmed class-1 stale pin, in two places — this is the direct proof that duplication has already produced a doubled defect rather than a hypothetical one.
- `references/00-topic-map.md:3` ↔ `references/full-guide.md:13`. The concatenation contains the router's instruction *"Do not load the full guide unless necessary"* — the file instructs the agent not to load the file it is inside.

**Ruling: retire `references/full-guide.md` to `_to_delete/`.**

It is not coverage; it is the exact case the completeness law names — "a second file shares most of its ground with one already covered … that is not coverage, it is drift with extra steps." It shares 99.75% of its ground. It is also structurally unreachable: no router row anywhere points to it. `references/00-topic-map.md` lists twelve reference rows, nine examples and seven assets, and omits `full-guide.md`; `SKILL.md:63-78` omits it; only `skill-pack-manifest.json:39` mentions the path, and manifests are not routers. It is 38.1% of the pack's bytes reachable only by directory listing. And it defeats the routing the skill exists to provide: an agent that finds it and reads it loads 75 KB to answer a question the router would have answered with 6 KB.

**The options not chosen, and their cost.**

*Keep `full-guide.md` as the single source, topic files become generated views.* Cost: you must ship a generator plus a CI drift check, because a view that can be edited independently is the same duplication in the other direction. The router must still address the topic files (that is what progressive disclosure requires), so you pay to maintain two artifacts to deliver one, and every browser claim in section 8 below acquires two edit sites — which is precisely how `references/99-…:32` and `references/full-guide.md:2128` came to hold the same stale pin. Rejected.

*Keep it as a deliberately different register — a linear narrative for a human reader.* This would be defensible **if** it were written as one, but it is not: it is 99.75% identical, ordered by filename rather than by argument, and it carries the router table at `references/full-guide.md:15-30` including a row telling the reader to load a different file. There is no register difference to preserve. Rejected.

*Cost of the retirement I did choose.* An agent or human wanting one linear read loses the artifact. This is small and fully mitigated: `references/00-topic-map.md` already provides the ordered index, and the exact file is reproducible on demand — `cat references/[0-9]*.md > /tmp/full-guide.md` — which is how it was produced in the first place (`references/full-guide.md:3`, "Generated from references on 2026-06-29"). Phase 2 should record that command in `references/99-sources-and-maintenance.md` rather than the output.

---

### 6. Other duplication

| Content | Location A | Location B | Which survives |
|---|---|---|---|
| Router table, 12 rows verbatim | `SKILL.md:63-78` | `references/00-topic-map.md:7-20` | **B.** ≥9 references means the router lives in `00-topic-map.md`; `SKILL.md` keeps one pointer line. `SKILL.md:55` already carries that pointer, so A is pure surplus. |
| Never-store / token rules | `SKILL.md:82-84` | `references/60-…:16-31`, `:69-73` | **B** for the full list. The body keeps one constraint sentence with the reference path, since the prohibition must survive without a reference load. |
| Quota-error handling rule | `SKILL.md:85` | `references/30-…:110-124` | **B.** The ordered ladder is reference material; the body keeps the one-line constraint. |
| `versionchange`/`blocked` rule | `SKILL.md:88` | `references/40-…:5-13, 134-169` | **B.** |
| Transaction-await prohibition | `SKILL.md:89` | `references/40-…:173-197`, `references/50-…:22-27` | **B**, and note A/B/C: this rule exists in *three* places, twice inside `references/`. `references/40-…:173-197` (with bad/good fences) survives; `references/50-…:26` becomes a pointer. |
| `BrowserStorageCapabilities` interface | `references/20-…:112-127` (13 fields, incl. `workerIdb`) | `examples/browser-capabilities.ts:5-21` (15 fields, incl. `locks`, `serviceWorker`, `opfs`, no `workerIdb`, `transactionDurability` widened to `boolean \| 'unknown'`) and `assets/capability-tier-contract.json:67-80` (12 detection targets, incl. `Background Sync` which neither of the others has) | **Three-way divergence, not duplication.** The example survives as the implementation; the reference row becomes a pointer to it; the JSON becomes the contract the new harness enforces over both. |
| `dataClass` value set | `references/30-…:171` (`'critical' \| 'draft' \| 'outbox' \| 'cache' \| 'prefetch'`) | `assets/data-classification-policy.yaml:1-39` (`public_cache`, `user_private_low_risk`, …), written by `examples/alaa-client-storage.ts:36` | **The YAML.** Consequence today: the facade writes `'user_private_low_risk'` into the field that `examples/migration-pattern.ts:14` indexes as `byDataClassLastAccessedAt`, while the cleanup order at `references/30-…:175-187` keys on `'cache'`/`'prefetch'` — values no shipped code ever writes. The LRU cleanup index is functional and permanently empty. |
| Outbox record type | `references/70-…:46-62` | `references/95-…:69-82` (`WatchAnalyticsOutboxItem`) and `examples/outbox-pattern.ts:3-16` | **The example.** The two reference copies become pointers; `references/95-…` keeps only the Alaa-specific fields (`eventType`, `contentId`, `occurredAt`) as a delta. |
| Prompt patterns using `$alaa-indexeddb-browser-storage` | `references/90-…:113,128,141,150,159` | `references/full-guide.md:1783-1829` | **A**, with both trigger forms added. B dies with `full-guide.md`. |

**Against `alaa-quasar-app-vite-v3` (service workers and offline).** The boundary is **clean from the other side and thin from this side.** `alaa-quasar-app-vite-v3/references/30-service-worker-excellence.md:3` and `:24` name `$alaa-indexeddb-browser-storage` *with the specific file path* (`references/70-offline-sync-outbox-cache-patterns.md`) and explicitly assign "Drafts, entity caches, outbox records, and sync cursors" to it — a correct cross-skill reference in exactly the required form. `alaa-quasar-app-vite-v3/references/45-browser-apis-and-permissions.md:3` likewise routes storage here. This skill reciprocates only with a bare `$alaa-quasar-app-vite-v3` at `SKILL.md:100` and no path. Not the prohibited bare-`references/…` form, but asymmetric: Phase 2 owes the reciprocal path.

Two substantive overlaps to resolve, and in both the **non-owner is currently more precise than the owner**, which must be corrected in the owner's favour:

- **Safari ITP eviction window.** `alaa-quasar-app-vite-v3/references/45-…:38` states "Safari 7-day ITP eviction still affects non-persistent storage". This skill, which owns eviction, states only "origins without recent user interaction" (`references/30-…:141`) and never gives the number. **This skill must carry the figure**; the quasar file should reduce to a pointer.
- **Background Sync availability.** `alaa-quasar-app-vite-v3/references/30-…:24` states "Firefox and all Safari/iOS lack Background Sync; Workbox falls back to replay on SW start". This skill says only "Background Sync / Periodic Sync when supported" (`references/20-…:82`) and "browser support varies" (`references/70-…:122`). Background Sync is the SW skill's ground, so the **quasar file survives** and this skill must route to it by path rather than hedge.

**Against `alaa-frontend-developer/references/30-pwa-sw-and-offline.md`.** No overlap. I read the file in full: it contains no mention of IndexedDB, quota, outbox, eviction, `navigator.storage`, `BroadcastChannel` or Web Locks. It is a pure SW-policy and QA-runbook file and correctly delegates depth to `$alaa-quasar-app-vite-v3` at `:15`. Nothing to deduplicate; the only gap is that it does not name this skill, so an agent arriving via `alaa-frontend-developer` for an offline task is not routed here.

---

### 7. Wording-test failures

| # | Quoted sentence | Location | Failure mode | Replacement |
|---|---|---|---|---|
| 1 | "prefer IndexedDB for structured records and metadata, and choose Cache API or OPFS when those are the right abstraction." | `SKILL.md:91` | Abstract noun ("the right abstraction") standing in for an observable condition, plus a preference verb where a constraint was meant. | "Store a value in IndexedDB when you will retrieve it by key or index. Store it in Cache API when it is an HTTP Request/Response pair. Store it in OPFS when you will read it by byte range. Do not write a value over 1 MB to IndexedDB unless that value has a line in the feature's `storage-budget-policy.md`." |
| 2 | "Migrations must be deterministic, idempotent **where possible**, and tested from every supported old schema." | `references/40-…:7` | Self-granted exception with no external referent, attached to the pack's own non-negotiable list. | "Every migration must be idempotent: running it twice against the same database must leave the same state as running it once. If a migration cannot be made idempotent, it must write a `migration_journal` record with `nonIdempotent: true` and name the approver recorded in the feature ADR." |
| 3 | "Every **serious** feature should expose a capability object like:" | `references/20-…:109` | Unobservable qualifier ("serious") plus a preference verb; an agent can classify any feature as not serious. | "Any code path that writes to IndexedDB and can be reached by a user must call `detectBrowserStorageCapabilities()` before its first write and persist the returned tier to the `capabilities` store." |
| 4 | "Every storage write should be inside **a path that can catch and classify** quota errors." | `references/30-…:112` | Abstract noun for an observable condition; "a path that can catch" is not checkable in review. | "Every `put`, `add`, or `delete` must be issued inside a function that awaits `txDone(tx)` and routes a `QuotaExceededError` through the cleanup ladder below. A write not wrapped this way fails review." |
| 5 | "Ensure logout/account deletion clears local data on next app open **where feasible**." | `references/60-…:157` | Self-granted exception on a security rule, with no named artifact or approver. | "On the first app open after a session whose purge did not complete, delete every record whose `accountKey` differs from the current session before rendering any user-scoped view, and record `logout_purge_deferred` in `meta`." |
| 6 | "Low-priority telemetry may be dropped after retention/backlog limits **if product accepts it**." | `references/70-…:179` | Self-granted exception whose referent ("product") is a role, not an artifact or approver. | "Drop outbox items with `priority: 'low'` once the queue exceeds the `hardStop` value in the feature's `storage-budget-policy.md`, and only for the data classes that file marks droppable. If the file marks none, do not drop." |
| 7 | "compression/encryption work, **if justified**" | `references/50-…:214` | Self-granted exception with no checkable condition. | "Move compression or encryption to a worker when one main-thread invocation exceeds 16 ms measured on the lowest-capability lane in `assets/browser-test-matrix.yaml`." |
| 8 | "Use user-agent/version checks only as a last-resort workaround for a **reproduced** engine bug." | `references/20-…:12` | Passive abstraction — reproduced by whom, recorded where, removed when. | "A user-agent check is permitted only when a test in this repository reproduces the engine bug, the code comment links that test by path, and the same PR that fixes or retires the bug deletes the check." |
| 9 | "Minimize, encrypt only with **meaningful key model**, TTL, purge controls, **security review**" | `references/60-…:44` | Abstract noun ("meaningful key model") plus a review requirement naming no owner and no approver. | "Do not store moderate or high PII in IndexedDB. If a feature requires it, obtain a review under `/alaa-security-review` (`$alaa-security-review`) and record in the ADR: where the key is generated, where it is stored, and whether JavaScript in the origin can read it." |
| 10 | "Do not rely on user-agent sniffing **except for documented product analytics or known WebKit/iOS mitigations**." | `SKILL.md:58` | Prohibition whose exception is self-granted ("known"), with no positive replacement stated. | "Branch on the object returned by `detectBrowserStorageCapabilities()`, never on `navigator.userAgent`. The one exception is the reproduced-bug case defined in `references/20-…`; product analytics may read the user agent but must not branch storage behaviour on it." |

---

### 8. Stale or unverifiable claims

The skill's research date is 2026-06-29 (`references/99-…:3`, `skill-pack-manifest.json:5`), and its own freshness gate at `references/05-…:26` fires at six months — so as of 2026-07-28 the pack is inside its window but every claim below is within one month of expiry. Phase 2 can research this list directly.

**Quota formulas**

| Claim | Location | Status |
|---|---|---|
| Firefox best-effort = min(10% of total disk, 10 GiB group limit) | `references/30-…:43` | **Verified from the files** — attributable to the MDN "Storage quotas and eviction criteria" page cited at `references/99-…:15`. Needs live re-verification; MDN has revised these figures before. |
| Firefox persistent = up to 50% of disk, capped 8 TiB, exempt from group limit | `references/30-…:43` | **Verified from the files** (same MDN page). Re-verify. |
| Chromium origin ≈ 60% of total disk in both persistent and best-effort | `references/30-…:44` | **Verified from the files** (same MDN page). Re-verify — the "same in both modes" claim is the part most likely to have shifted. |
| Safari/WebKit ≥ macOS 14 / iOS 17: ~60% per origin (browser app), ~15% (embedded), ~80% browser-wide, ~20% embedded-wide | `references/30-…:45` | **Verified from the files** — attributable to webkit.org/blog/14403 cited at `references/99-…:17`. Re-verify against any post-14403 WebKit storage post. |
| "Cross-origin frames get a fraction of main-frame quota" | `references/30-…:45` | **Not verifiable as written** — "a fraction" is unquantified. Phase 2 must obtain the number or delete the row. |
| Earlier Safari: initial origin quota ~1 GiB before a permission prompt | `references/30-…:46`, `references/20-…:21` | **Needs live research.** No source in `references/99-…` covers pre-17 Safari quota. Also needs the version boundary stated. |
| "Private/incognito — quota can be reduced" | `references/30-…:47`, `references/20-…:24` | **Not verifiable as written** — unquantified and un-sourced per engine. |
| `softStop = min(200MB, 5% of estimated quota)` / `hardStop = min(500MB, 10%)` | `references/30-…:99-101` | **Not a browser claim** — a house policy presented in the same register as the vendor figures above. Phase 2 should label it as policy, not fact. |

**Eviction rules**

| Claim | Location | Status |
|---|---|---|
| "Eviction can delete all data for an origin at once" | `references/30-…:16` | **Verified from the files** (MDN quota/eviction page). |
| Safari/WebKit proactively evicts script-created data for origins "without recent user interaction" when cross-site tracking prevention is on | `references/30-…:141` | **Needs live research and is under-specified.** The window (7 days of no user interaction) is stated by the *sibling* skill at `alaa-quasar-app-vite-v3/references/45-…:38` and not by the owner. Phase 2 must obtain and state the current figure, its trigger, and whether `persist()` exempts it. |
| Persistent storage "means browser should not silently evict; user can still delete data" | `references/30-…:35` | **Verified from the files** (MDN Storage API). |
| Chrome/Edge LRU-under-pressure eviction order | absent | **Gap.** The skill states cleanup order for its own data but never states the browser's eviction order across origins. Needs research. |

**Safari / ITP behaviour**

| Claim | Location | Status |
|---|---|---|
| "Safari 17/iOS 17 introduced updated quota and Storage API support" | `references/20-…:21` | **Needs live research** for precision — which Storage API surfaces landed in which version (`persist`, `persisted`, `estimate`, `getDirectory`). |
| "iOS/iPadOS third-party browsers historically WebKit-based; EU iOS 17.4+ may allow alternate engines" | `references/20-…:22` | **Needs live research.** A regulatory/platform claim that has moved and is hedged with "may". |
| "WebKit/Safari are stricter about transaction inactivity" | `references/40-…:173` | **Not verifiable as written** — no version, no reproduction, no bug link. Either cite a WebKit bug or convert to "verify with the transaction-inactivity test in the safari-macos lane". |
| Safari Web Inspector → Storage as the debug path | `references/80-…:74-77` | **Needs live research** — the quasar sibling notes Safari 26+ moved to Develop → Inspect Apps and Devices for some surfaces. |

**`navigator.storage.persist()` behaviour**

| Claim | Location | Status |
|---|---|---|
| "In Firefox, a user prompt may appear" | `references/30-…:33` | **Verified from the files** (MDN). |
| "In many Chromium/Safari cases, the browser decides automatically based on user interaction/history" | `references/30-…:34` | **Needs live research** — the specific Chrome heuristics (bookmarked, high site engagement, PWA installed, push permission granted) are the actionable content and are absent, so an agent cannot decide when to call `persist()`. |
| `requestPersistentStorageAfterUserIntent` returns `'denied'` on a thrown exception | `examples/quota-manager.ts:48-49` | **Code defect, not a browser claim** — a throw is not a denial; this conflates unsupported/blocked with refused. |

**Web Locks / BroadcastChannel support**

| Claim | Location | Status |
|---|---|---|
| "`navigator.locks` … or robust app-level coordination" (Tier 3) | `references/20-…:84` | **No support claim is made at all.** Needs live research: Web Locks is now widely available (Safari ≥ 15.4 among others), which likely makes the lease-record fallback at `references/40-…:213-220` dead weight. State the baseline and either keep the fallback with a stated trigger or delete it. |
| "For cross-tab singleton sync jobs, use `navigator.locks` if available, otherwise a lease record with expiry and owner ID" | `references/40-…:209` | **Needs live research** — same. The lease record also has no renewal interval or takeover rule, so it is unimplementable as written. |
| "Better multi-tab coordination with `BroadcastChannel` or similar" (Tier 2) | `references/20-…:68` | **No support claim.** Needs live research; if BroadcastChannel is baseline, the "Fallback to `storage` events or polling" at `references/40-…:169` should be deleted rather than carried. |

**Browser-version and API claims**

| Claim | Location | Status |
|---|---|---|
| "Chrome changed default readwrite durability to relaxed from Chrome 121" | `references/20-…:19`, `references/99-…:47` | **Verified from the files** — Chrome Developers blog cited at `references/99-…:24`. Lowest-risk claim in the pack. |
| "Firefox has relaxed durability guarantees since Firefox 40" | `references/20-…:20` | **Needs live research** — no source in `references/99-…` supports it; the version number appears nowhere else. |
| "`getAllKeys()` widely available in modern browsers" | `references/20-…:100` | **Verified from the files** (MDN cited at `references/99-…:26`). |
| "`getAllRecords()` is experimental/limited; never require it" | `references/20-…:101`, `references/50-…:100`, `references/99-…:46` | **Needs live research** — MDN page cited at `references/99-…:27`, but this API has been shipping in Chromium and the "experimental" framing may already be stale. |
| "`indexedDB.databases()` … Feature-detect" | `references/20-…:105` | **Needs live research** — which engines lack it (historically Firefox) is the actionable part and is absent. |
| "`IDBTransaction.commit()` Feature-detect; do not require" | `references/20-…:106` | **Needs live research** — no support data given. |
| "IndexedDB is available in workers in modern browsers" | `references/50-…:209` | **Not verifiable as written** — "modern" is unbounded; and `workerIdb` is in the reference's capability interface but is not probed by `examples/browser-capabilities.ts`. |
| Background Sync / Periodic Sync "when supported" | `references/20-…:82`, `references/70-…:121-122` | **Needs live research**, and see section 6 — the sibling skill already states the answer (Firefox and all Safari/iOS lack it). Route rather than restate. |
| OPFS availability | `references/20-…:81`, `references/50-…:189` | **No support claim.** Needs research if OPFS stays in Tier 3. |
| Storage Buckets API | **absent everywhere** | **Coverage gap.** `references/30-…:9` is titled "Storage bucket model" and uses the term throughout without ever mentioning that a Storage Buckets API exists with per-bucket durability, persistence and eviction-priority controls. For a skill bound by the completeness law this is the single largest missing capability. |
| "Browser vendors intentionally pad/alter quota estimates to reduce fingerprinting" | `references/99-…:78` | **Verified from the files** and consistent with `references/30-…:44`. |

---

### 9. Router audit

**Reference count.** 14 files in `references/` — thirteen numbered topic files plus `full-guide.md`. Thirteen is ≥ 9, so the binding rule applies: the router lives in `references/00-topic-map.md` and `SKILL.md` carries one pointer line.

**Router location — non-conforming on two counts.**

1. **Two routers.** `references/00-topic-map.md:7-20` (12 rows) and `SKILL.md:63-78` (12 rows) are the same table. The rule is one router per skill, never two. `SKILL.md:55` already contains the correct pointer line ("Load `references/00-topic-map.md` and then only the smallest relevant reference files"), so the duplicate table at `SKILL.md:63-78` is surplus that must be deleted, not merged.
2. **One reference is unrouted.** `references/full-guide.md` appears in no router. `references/00-topic-map.md:3` mentions "the full guide" in prose with no path and no condition; `skill-pack-manifest.json:39` lists the path but a manifest is not a router. 38.1% of the pack's bytes are reachable only by directory listing.

**Observable-condition test — 0 of 12 rows pass, in both routers.** Every row is a heading mirror or a noun phrase, not "You are about to <observable situation> → read `<file>`":

| Row as written | Location | Why it fails |
|---|---|---|
| "Authoritative source order, freshness, current browser claims" | `00-topic-map.md:9` | Noun list; mirrors the target's title. |
| "Decide whether IndexedDB is the right storage API" | `:10` | Closest to passing — it is a verb — but "the right storage API" is an abstract noun, not an observable situation. |
| "Browser/version compatibility, progressive enhancement, feature probes" | `:11` | Heading mirror. |
| "Quotas, persistent storage, eviction, private mode, cleanup budgets" | `:12` | Heading mirror. |
| "DB schema, object stores, migrations, multi-tab upgrade safety" | `:13` | Heading mirror. |
| "Transactions, performance, indexes, read/write patterns, durability" | `:14` | Heading mirror. |
| "Security, privacy, auth-token, PII, logout purge, shared device" | `:15` | Heading mirror. |
| "Offline sync, outbox, drafts, local cache, conflict handling" | `:16` | Heading mirror. |
| "Testing, DevTools, instrumentation, release readiness" | `:17` | Heading mirror. |
| "Agent workflow, prompt patterns, output templates" | `:18` | Heading mirror. |
| "Alaa integration and service-boundary mapping" | `:19` | Heading mirror. |
| "Source map and maintenance schedule" | `:20` | Heading mirror. |

The `SKILL.md:67-78` rows are the same content with slightly different wording and fail identically. For contrast, a passing row for the same target would read: "You are about to write a `put` on a path that can run while the device is low on disk → read `references/30-…`."

The Code-examples table (`00-topic-map.md:24-34`) and Templates/assets table (`:38-46`) are *inventories*, not routers, and are correctly shaped as such — they should survive.

**Dangling paths.** None. All 12 reference paths, 9 example paths and 7 asset paths named in `00-topic-map.md` resolve; all 5 companion skills named in `SKILL.md:99-106` exist under `/mnt/user-data/uploads/skills/skills/sohrab/`. Two rows resolve to nothing by design: `SKILL.md:103` "Alaa observability/analytics skill **if available**" and `SKILL.md:104` "Alaa upload/tusd/service-contract skill **if available**" — both owners exist (`alaa-observability-soc`, `tusd-upload-platform`) and are not named.

**Running the logic of `scripts/check_references.py` mentally — and what it actually reports.** The script reads `references/00-topic-map.md` and applies

```python
re.findall(r'`(references/[^`]+\.md)`|`(examples/[^`]+\.ts)`|`(assets/[^`]+)`', ...)
```

The first alternation requires a literal `` `references/ `` prefix. The router writes its reference rows as bare filenames — `` `05-source-priority-and-freshness.md` `` at `references/00-topic-map.md:9` — so **that alternation matches zero times**. The script therefore collects exactly 16 paths: the nine `examples/*.ts` and the seven `assets/*`. All 16 exist, `missing` is empty, and it prints `OK: topic-map references exist`. I confirmed this by executing it (exit 0) and by re-running the regex in isolation: 16 matches, none of them a reference.

So the script would report **green today, and would still report green if every one of the twelve reference files were deleted.** The one tool named for reference integrity cannot detect a broken reference. It also never inspects `SKILL.md`'s router, never notices that `full-guide.md` is unrouted, and never checks the inline `` `references/…` `` mentions scattered through `references/20-…:129`, `references/95-…:205` and elsewhere.

---

### 10. Scripts, examples and assets audit

### Scripts

**`scripts/check_references.py`** (550 B). *What it does:* resolves the pack root from `Path(__file__).resolve().parents[1]`, regex-scans `references/00-topic-map.md` for backticked paths, and exits non-zero listing any that do not exist. *Would it run:* yes — exit 0 from `/tmp`, from the pack root, and from `scripts/`; no third-party imports; Python 3 stdlib only. *Fragile paths:* `parents[1]` at `:5` is **not** fragile — it is file-relative and therefore CWD-independent, which is the correct idiom; it would only break if the script moved out of `scripts/`, which the manifest pins. Judgement: **acceptable, keep it.** *`--help` / self-test:* neither. No argparse, no `-h`, no documented exit codes, no fixture that proves it fails when it should. *What it would find today:* nothing — see section 9. It validates 16 example and asset paths and zero references, then prints a success message about references. Phase 2 must fix the regex (accept bare filenames and resolve them under `references/`), extend it to `SKILL.md`, add an orphan check (every file in `references/` must be named by the router), and ship a negative fixture so the green is earned.

**`scripts/validate_skill_pack.py`** (1,736 B). *What it does:* asserts four required files exist and are non-empty (`:7-12, 27-32`); asserts `SKILL.md` opens with `---\n`, contains the exact `name:` line, and contains `description:` (`:34-40`); walks every `.md`/`.ts`/`.yaml`/`.json` and fails on any that is whitespace-only (`:42-46`); concatenates `examples/*.ts` and fails on three token-storage regexes (`:14-18, 48-51`). *Would it run:* yes, exit 0, stdlib only. *Fragile paths:* `parents[1]` at `:6` — same judgement, acceptable. Note the inconsistent indentation at `:42-43` (two-space `if` inside a four-space `for`) — legal Python, but it signals the file has not been linted. *`--help` / self-test:* neither. *What it would find today:* nothing. The three forbidden patterns (`refreshToken\s*[:=]`, `accessToken\s*[:=]`, `localStorage.setItem(...token`) are trivially evaded by `const t = resp.access_token`, by a computed property, or by writing to IndexedDB rather than `localStorage` — which is the actual risk this skill exists to prevent, and which no pattern covers. The scan is also restricted to `examples/*.ts`, so `references/` and `assets/` are never checked. It does not validate the description length, the presence of a "do not use for" clause, the trigger-syntax rule, or that `skill-pack-manifest.json:7-43` matches the filesystem (it currently does, by luck).

**Missing script — the conformance harness the precedent requires.** Three implementations of one capability contract exist (`references/20-…:112-127`, `examples/browser-capabilities.ts:5-21`, `assets/capability-tier-contract.json:67-80`) and they disagree: the reference has `workerIdb` and the others do not; the example has `locks`, `serviceWorker` and `opfs` and the reference does not; the JSON requires detecting `Background Sync` and neither of the other two mentions it; `transactionDurability` is `boolean` in the reference and `boolean | 'unknown'` in the example. No document asserts parity and no harness proves it. Phase 2 owes a harness that drives all three over one corpus of field names and tiers and fails on any disagreement, reporting a skip (never a pass) for any runtime it cannot observe.

### Examples

| File | Correct? | Compiles? | Failure mode or happy path? | Boundary |
|---|---|---|---|---|
| `idb-core.ts` (4,343 B) | Mostly. Cleanest file in the pack: `txDone` at `:15-21` observes `oncomplete`/`onabort`/`onerror` rather than request success — exactly what `references/50-…:27` demands; `:74-77` actively aborts and throws if the transaction callback returns a Promise, enforcing `references/40-…:176` in code; `:89-94` try/catches unsupported transaction options. Defect: a throw inside the `onupgradeneeded` handler at `:44` escapes into event dispatch rather than rejecting the open request directly — it happens to reject via transaction abort, but that is incidental. | Yes on TypeScript ≥ 5.2 (`IDBTransactionOptions` at `:67` is a recent `lib.dom` addition); fails on older libs with no stated minimum. | **Both** — `probeIndexedDbWrite` at `:122-146` is a real degradation path, and `getAllBounded` at `:97-120` ships the cursor fallback the compatibility reference mandates. Best example in the pack. | Clean. |
| `alaa-client-storage.ts` (3,034 B) | No. `:36` writes `dataClass: 'user_private_low_risk'` while `references/30-…:171` types the field as `'critical'\|'draft'\|'outbox'\|'cache'\|'prefetch'` and the cleanup order at `references/30-…:175-187` keys on `'cache'`/`'prefetch'` — so the `byDataClassLastAccessedAt` index built at `migration-pattern.ts:14` is permanently empty for cleanup purposes. `:55-64` runs the logout purge as four independent transactions, so a crash mid-purge leaves the prior account's records readable. `:73` full-scans each store with no `accountKey` index. | Yes. | **Happy path only.** No quota handling on `saveLearningState` despite `SKILL.md:85`. | Implements no shared interface with `MemoryStore`, so the Tier 0 substitution cannot happen (criterion 6). Mints `dataClass` values that disagree with the reference. |
| `browser-capabilities.ts` (2,962 B) | No. `chooseCapabilityTier` at `:73-78` can never return `3` — `assets/capability-tier-contract.json:52-65` defines `tier3_enhanced_offline` and no shipped code can reach it. Its interface at `:5-21` diverges from `references/20-…:112-127` in four fields. It probes `locks`, `serviceWorker`, `opfs` but not `Background Sync`, which the contract requires. | Yes. | **Both** — the private-mode inference at `:59-71` is honest about being a weak signal and says so in a comment. | Clean, but is the third divergent copy of the capability contract. |
| `fallback-memory-store.ts` (684 B) | Yes. | Yes. | Neither — a data structure. | Clean. Defines the `KeyValueStore<T>` interface that `AlaaClientStorage` should have implemented and does not. |
| `migration-pattern.ts` (1,795 B) | Mostly. Correct `oldVersion <` branching, correct compound indexes, correct `onBlocked`/`onVersionChange` wiring at `:35-42`. Defects: no `migration_journal` store despite `references/40-…:122` requiring one and `references/40-…:50` listing it; `meta.put` of `schemaVersion` happens only in the `oldVersion < 3` branch at `:31-32`, so a future v4 that adds a branch will not update it unless the author remembers. | Yes. | **Happy path only** — no shadow-copy or lazy-migration example despite `references/40-…:116-133` teaching both; no failed-migration recovery. | Clean. Its `['status','nextAttemptAt']` at `:23` is the *correct* form; `references/40-…:95` is the wrong one. |
| `outbox-pattern.ts` (3,910 B) | No — most defective file. (i) `:104-106` classifies HTTP 401 and 403 into the `dead` counter while writing status `pending`, so the return value lies and an expired session burns retry attempts; `references/70-…:136-137` says unauthorized should pause sync and forbidden should go dead. (ii) `:46` marks items `inflight` and nothing ever re-claims an item orphaned by reload — permanent silent loss. (iii) `:100` awaits `send` with no timeout. (iv) `:46` mutates the index key inside a cursor over that index, safe only because `'inflight'` sorts before `'pending'`; unstated. (v) `:59` and `:69` await an IDB request inside an open transaction — legal on spec-compliant engines but the exact shape `references/40-…:176` prohibits, with no note reconciling the two. (vi) No lease acquisition despite `references/70-…:127` step 1. | Yes. | **Nominally a failure-mode example, actually a happy path with a broken error branch.** | Legislates retry/backoff/attempt-cap (`alaa-reliability-sla`) and the five-state row set (`alaa-async-messaging`). `idempotencyKey` at `:8` is declared and never generated — the hole where an identifier appears, with no route to `alaa-crockford-base32-codecs`. |
| `vitest-idb-pattern.test.ts` (988 B) | As a shape, yes. | Yes, but does not *run*: `fake-indexeddb` is never imported (`:2-3` says configure it in setup), so in a plain node/jsdom environment `indexedDB` is undefined and it throws. | **Happy path only** — open, write, read. Covers 1 of the 15 scenarios its own `references/80-…:42-58` demands. Nothing for upgrade, `blocked`, quota, stale records, or purge. | Clean. |
| `playwright-quota-smoke.spec.ts` (1,739 B) | No. `:32` asserts `expect(result).toHaveProperty('ok')` — both branches of the code above return an object with `ok`, so the assertion **cannot fail**. `:47` is similarly near-vacuous. The file is named "quota-smoke" and never induces a quota condition, never calls `estimate()` against a budget, and never triggers `QuotaExceededError`. `:4` uses `page.goto('/')` requiring a `baseURL` that nothing documents. | Yes. | **Neither** — a test that asserts nothing. | Clean. |

**Placement on the `alaa-testing-strategy` six-level ladder** (which the skill never names): `vitest-idb-pattern.test.ts` sits at **level 2 (unit)** only once `fake-indexeddb` is configured, and at level 0 as shipped. `playwright-quota-smoke.spec.ts` sits at **level 4 (local smoke)**, and delivers no assertion at that level. **Level 3 (parity) is empty** — which is precisely where the missing capability-contract harness belongs. **Level 5 (in-runtime) is empty** despite `references/80-…:29-38` and `assets/browser-test-matrix.yaml:30-37` requiring real iOS/iPadOS device runs for offline-critical features; the skill demands a proof level it ships no artifact for. Level 6 is not applicable.

### Assets

All seven are emittable: `indexeddb-decision-record-template.md`, `indexeddb-feature-plan-template.md`, `storage-budget-policy-template.md` and `alaa-indexeddb-adr.md` are heading skeletons with pre-filled yes/no boundary questions (`assets/indexeddb-decision-record-template.md:21-24`, `assets/alaa-indexeddb-adr.md:47-48`) that an agent can fill directly and a reviewer can check. `assets/storage-budget-policy-template.md:9-15` ships the data-class rows pre-populated with cleanup rules and empty caps — good shape, but no bounds and no validation, so an agent can emit a policy with every cap blank and nothing objects.

**Does `assets/capability-tier-contract.json` agree with `assets/browser-test-matrix.yaml`? No — they do not intersect at all.** The contract is organised by tier (`tier0`…`tier3`) and lists twelve `must_feature_detect` targets (`:67-80`). The matrix is organised by browser lane (`:3-58`) and carries **no tier dimension whatsoever**. Consequently:

- Six of the twelve `must_feature_detect` entries — `IDBObjectStore.getAllRecords`, `transaction durability options`, `indexedDB.databases`, `BroadcastChannel`, `navigator.locks`, `OPFS`, plus `Background Sync` — have **no test in any lane**. The matrix's 33 test entries never name them.
- `tier3_enhanced_offline` (`capability-tier-contract.json:52-65`) has no lane and, as noted, no reachable code path in `examples/browser-capabilities.ts:73-78`. It is declared, untested, and unreachable.
- Conversely, the matrix tests things the contract does not govern: `relaxed-durability-assumptions` (`browser-test-matrix.yaml:19`), `inactivity-return-check` (`:29`), `app-background-foreground` (`:37`).
- The only genuine agreement is on tier 0/1 basics: `idb-open-write-probe` (`:48`) ↔ `"IndexedDB missing or open/write probe fails"` (`capability-tier-contract.json:6`), and `offline-promise-disabled` (`:51`) ↔ `forbidden_promises` (`:12-15`).

Both files carry `last_researched: "2026-06-29"` and neither references the other. Phase 2 must add a tier column to the matrix or a lane list to the contract, and the harness must enforce the join.

---

### 11. Rewrite brief for Phase 2

### Target file list

**Body — `SKILL.md`, target ≤ 6,100 bytes**

| Section | Purpose | Budget |
|---|---:|---:|
| Frontmatter `name` + `description` | Trigger surface, with an explicit "Do not use for" clause naming service workers/Cache API routing (→ `alaa-quasar-app-vite-v3`), server-side store selection (→ `alaa-data-layer`), and token/session handling (→ `alaa-trust-gateway-auth`) | 520 |
| H1 + Purpose | What the skill decides | 260 |
| Ownership and companion boundary | What it owns; what it does not, each disclaimer naming the owning skill with both trigger forms | 900 |
| Router pointer | One line to `references/00-topic-map.md` | 120 |
| Mandatory rules | The six constraints that must survive without a reference load, each with a positive replacement and a checkable scope | 900 |
| Companion pairing table | 11 rows, both `/name` and `$name` forms, paths for cross-skill file references | 1,000 |
| Quick start workflow | 9 steps → 6 | 700 |
| Output default | 250 |
| Search terms | Grep bait; earns its place | 500 |
| **Subtotal** | | **5,150** |
| **+15%** | | **≈ 5,930 → cap at 6,100** |

This is 3,167 bytes *below* today's 9,267 and 3,014 below net of description — the completeness law's "body must not grow" holds with room, because the routing table and the reference-duplicated rules leave.

**References — 19 files (13 → 19 by split, 1 retired)**

| File | Purpose | Origin |
|---|---|---|
| `00-topic-map.md` | The single router. Every row rewritten as "You are about to <observable situation> → read `<file>`". Keeps the examples and assets inventories. | rewrite |
| `05-source-priority-and-freshness.md` | unchanged in scope; drop the "Skill-authoring compatibility" section (`:46-54`) → `/alaa-prompting-guide` | trim |
| `10-indexeddb-mental-model-and-boundaries.md` | unchanged | — |
| `20-browser-compatibility-and-capability-tiers.md` | capability tiers; the interface row becomes a pointer to the example | trim |
| `25-storage-buckets-api.md` | **new** — the Storage Buckets API, per-bucket durability/persistence/eviction priority; the gap named in section 8 | new |
| `30-quota-model-and-budgets.md` | quota model, per-engine figures, budget tables | split of 30 |
| `31-quota-exceeded-and-cleanup.md` | `QuotaExceededError` as a failure class: symptom, diagnosis, smallest retry, escalation | split of 30 |
| `32-eviction-and-recovery.md` | eviction, Safari ITP window, private mode, boot-time recovery | split of 30 |
| `40-schema-and-migrations.md` | upgrade branching, additive/shadow/lazy, `migration_journal` | split of 40 |
| `41-multitab-versionchange-and-locks.md` | `blocked`/`versionchange`, Web Locks vs lease, **and the service-worker-writes-while-tab-writes seam** (criterion 5 gap) | split of 40 |
| `50-transactions-performance-and-query-patterns.md` | + stated complexity budgets per read/write shape (criterion 7) | extend |
| `60-data-classification.md` | the class table and what may land on a shared device | split of 60 |
| `61-authority-boundary.md` | tokens, JWT claims, trusted headers, entitlement/bitmap caching — each disclaiming to `alaa-trust-gateway-auth` / `alaa-permission-generator` | split of 60 |
| `62-xss-poisoning-and-purge.md` | third-party scripts, storage poisoning, **atomic** logout purge, shared devices | split of 60 |
| `70-cache-and-drafts.md` | read-through cache, drafts, invalidation, offline UX wording | split of 70 |
| `71-browser-outbox.md` | the browser outbox, disclaiming retry/backoff/timeout doctrine to `alaa-reliability-sla` and stating explicitly how its vocabulary relates to `alaa-async-messaging`'s server-side one | split of 70 |
| `80-testing-and-proof-levels.md` | test matrix placed on `alaa-testing-strategy`'s six levels by name | rewrite of 80 |
| `81-debugging-runbook.md` | the symptom→diagnosis tree (`80-…:151-183`) preserved as the model for failure-class organisation | split of 80 |
| `90-agent-workflows-prompts-and-output-contracts.md` | both trigger forms in all five prompt patterns | trim |
| `95-alaa-integration-playbook.md` | store map and package boundary; store names disclaimed to `alaa-services-contract` | trim |
| `99-sources-and-maintenance.md` | class-1 pin removed; every claim from section 8 re-researched and dated | rewrite |

**Scripts — 3 files**

- `check_references.py` — fix the regex (section 9), extend to `SKILL.md`, add an orphan check (every `references/*.md` must be named by the router), add `--help`, add a negative fixture.
- `validate_skill_pack.py` — add: description carries a "do not use for" clause; every `$alaa-` occurrence has a `/alaa-` sibling at the same call site; forbidden-pattern scan extended to `references/` and `assets/` and to IndexedDB writes (not just `localStorage`); manifest matches the filesystem; `--help`.
- `capability-contract-conformance.mjs` — **new harness.** Drives `references/20-…`'s declared field set, `examples/browser-capabilities.ts`'s interface, and `assets/capability-tier-contract.json`'s `must_feature_detect` over one corpus; fails on any disagreement in field name, type, or tier reachability; asserts every `must_feature_detect` entry has at least one lane in `assets/browser-test-matrix.yaml`; reports a skip (never a pass) for any runtime it cannot observe, and states that a green run bounds only what its corpus covers.

**Examples — 9 files, 4 amended, 1 added**

`outbox-pattern.ts`: fix the 401/403 classification, add a stuck-`inflight` reaper with a stated staleness threshold, add a timeout to `send`, document the `'inflight' < 'pending'` sort invariant, add lease acquisition. `browser-capabilities.ts`: make tier 3 reachable, add Background Sync, converge the interface. `alaa-client-storage.ts`: implement a shared interface with `MemoryStore`, make the purge atomic or journalled, converge `dataClass` onto the YAML taxonomy, add `accountKey` indexes. `playwright-quota-smoke.spec.ts`: assert something, and actually induce a quota condition. **New** `examples/outbox-reaper.ts` or fold into the above.

**Assets — 7 files, 2 amended**

`capability-tier-contract.json` and `browser-test-matrix.yaml`: add the joining dimension so the harness can enforce agreement.

**Files to retire to `_to_delete/`**

- `references/full-guide.md` (74,929 B) — section 5. This alone removes 38.1% of the pack.

### Is a genuinely NEW capability gained?

**Yes, four:**

1. **The capability-contract conformance harness.** Today three declarations of one contract disagree and nothing detects it. A harness converts an assertion of parity into evidence of it — a capability the pack does not have in any form.
2. **Storage Buckets API coverage.** `references/30-…:9` uses the words "storage bucket" throughout without the API existing anywhere in the pack. An agent asked tomorrow to give one data class a different eviction priority than another currently has nothing to read.
3. **The stuck-`inflight` reaper, and the explicit browser-outbox ↔ `alaa-async-messaging` vocabulary mapping.** The orphaned-inflight failure class is structurally absent from the server outbox (which deletes on claim) and therefore genuinely new ground; today it is neither documented nor implemented, and the shared five-state vocabulary actively conceals it.
4. **Stated complexity budgets** on read/write shapes and on the logout purge — the criterion-7 gap.

Everything else in this brief is re-routing, de-duplication, owner-naming, and freshness. The byte total should fall from 196,503 to roughly 125,000–135,000 while *increasing* coverage — which is the completeness law working as intended: coverage bought back with routing, and the 75 KB that bought no coverage at all removed.

---

### 12. Gap no existing skill can own

**None.**

Every gap I found resolves to an existing owner or to this skill by amendment:

- The browser outbox's operational surface, orphan-`inflight` class, and reaper → **this skill**, with retry/backoff/timeout doctrine disclaimed to `alaa-reliability-sla` and the row-state vocabulary reconciled against `alaa-async-messaging`.
- Storage Buckets API, quota, eviction, ITP → **this skill**; it is squarely inside the ownership statement at `SKILL.md:19`.
- Client-side data classification and the entitlement/bitmap caching rule → **this skill** for *where it may be stored*, `alaa-permission-generator` for the bitmap contract and decoder, `alaa-trust-gateway-auth` for whether a cached value carries trust. A three-way seam, but every side has an owner.
- Telemetry event names → `alaa-services-contract`; requirement levels and gates → `alaa-observability-soc`.
- The proof-level placement of the two test examples → `alaa-testing-strategy`.
- Background Sync and Cache API routing → `alaa-quasar-app-vite-v3`, which already claims them and already routes storage back here correctly.

The closest thing to an unowned seam is **a service worker and a tab writing the same IndexedDB concurrently** — the SW context belongs to `alaa-quasar-app-vite-v3`, the IndexedDB semantics belong here, and today neither file addresses the intersection. But that is an assignment failure, not an ownership vacuum: the natural home is `references/41-multitab-versionchange-and-locks.md` in this skill, with a reciprocal path-bearing pointer from `alaa-quasar-app-vite-v3/references/30-service-worker-excellence.md`. It does not warrant a new skill, and inventing one would violate the fleet-uniformity preference for no gain.


---

## Appendix I — `alaa-shaka-player`

### 1. What this skill is today

**Subject.** A Shaka Player 5.x integration pack for Vue 3 + Quasar + Vite: playback-engine architecture, HLS-first streaming, a 5.0.8→5.1.11 migration guide, and five product modules (analytics, ads, quiz, markers, schedule conductor).

**Register.** Mixed, and that is the core diagnosis: it is roughly 45% **teaching material** (`ARCHITECTURE.md`, `PATTERNS_AND_ANTI_PATTERNS.md`, `PLAYLIST.md`, `QUIZ_OVERLAY.md` — competent generic advice, no Alaa platform anchoring), 30% **scaffold generator** (nine templates + `scaffold.sh` + `AGENT_PROMPT.md` deliverables list), 20% **upstream-tracking runbook** (`UPSTREAM_WATCHLIST.md`, `MIGRATION_5_0_8_TO_5_1_11.md`, `OFFICIAL_LINKS.md` — the strongest material in the skill), and ~5% **production discipline**. It is not a production-discipline skill for a 99.99% service. It has no error taxonomy, no retry policy, no security rule, no load model, and zero references to the WA pipeline, the `client` repo, Pinia, `quasar.config`, or any fleet contract owner beyond `alaa-low-noise` and `alaa-frontend-developer`.

**Shape and byte sizes** (file-content sums, total 74,719 B):

| Path | Bytes | Files |
|---|---|---|
| `SKILL.md` | 11,075 | 1 (14.8% of the pack, always loaded) |
| `references/` | 33,895 | 17 (ALL_CAPS, unnumbered, incl. `README.md`) |
| `assets/templates/` | 18,755 | 9 (`.vue` ×2, `.ts` ×7) |
| `prompts/` | 3,911 | 2 |
| `checklists/` | 2,804 | 2 |
| `assets/config-examples/` | 2,413 | 7 (1 root + 6 agent TOMLs) |
| `INSTALL.md` | 910 | 1 |
| `scripts/` | 675 | 1 |
| `agents/` | 281 | 1 |

Five top-level content directories where the batch convention is two (`references/`, `scripts/`). No `evals/`. No `__pycache__`. No numbered files anywhere.

### 2. Ten-criteria verdict

| # | Criterion | Verdict | Evidence |
|---|---|---|---|
| 1 | Correctness and testability | **FAILS** | Only manual browser matrices exist: `checklists/QA_CHECKLIST.md:7-16`, `references/QA_MODES.md:1-45`. Zero occurrences of `vitest`, unit test, component test, or test double across the pack; no `.spec`/`.test` template beside the nine shipped modules. `alaa-testing-strategy` is named 0 times, so this is FAILS, not NOT-OWNED. |
| 2 | Failure behavior | **FAILS** | Zero occurrences of `shaka.util.Error`, `MediaError`, `severity`, `category`, `retryParameters`, `backoff`, `idempot`, `degrad`, `circuit` in the entire pack. `useShakaCore.ts:99-104` is the whole error path: forward `event.detail` to a callback. `references/TROUBLESHOOTING.md` has good symptom/fix shape but names no error code, no class, no retry bound. Manifest 404, segment timeout, licence-server failure, ABR downshift under loss and mid-stream token expiry are nowhere. `alaa-reliability-sla` named 0 times. |
| 3 | Security | **FAILS** | One CORS sentence (`references/HLS_NOTES.md:10-12`). No rule that a signed manifest URL is a bearer credential, no licence-request handling rule, no secret-logging prohibition. `assets/templates/PlayerLabPage.vue:59` prints `JSON.stringify(error)` — which for a Shaka network error carries the failing request URI and its query-string token — into an on-page `<pre>`. `assets/templates/types/player.ts:6` and `ShakaPlayer.vue:24` carry `headers?: Record<string,string>` as a Vue prop, i.e. a credential through devtools. `alaa-security-review` and `alaa-trust-gateway-auth` named 0 times. |
| 4 | Observability | **FAILS** | `AnalyticsTracker.ts:1-15` invents a heartbeat field contract (`contentId`, `positionSec`, `watchedDeltaSec`, `timestampMs`) and `:129-153` invents event names (`play`, `pause`, `seeked`, `ratechange`, `volumechange`), joined by `quiz_open`/`quiz_close` (`QuizEngine.ts:55,63`) and `ads_requested`/`ad_started`/`ad_ended` (`AdsManager.ts:43,53,58`). No `project_id`, no session id, no event id. QoE is "ideas" (`ANALYTICS_WATCHTIME.md:41`), not a field contract: no named rebuffer-ratio or startup-time field. `alaa-services-contract` and `alaa-observability-soc` named 0 times. |
| 5 | Concurrency and load | **FAILS** | Zero occurrences of `concurren`, `presigned`, backpressure, thundering herd. `CDN` appears once (`HLS_NOTES.md:15`, about range requests); `cache` once (`UPSTREAM_WATCHLIST.md:38`, about text-region cache keys). Heartbeats fire on an unjittered fixed interval (`AnalyticsTracker.ts:39,89`), so N viewers who started together POST together forever. Nothing on per-viewer signed URLs destroying the CDN cache key. |
| 6 | Clean code, SOLID, patterns | **FAILS** | The layering is genuinely good (`SKILL.md:204-252`, `ARCHITECTURE.md:13-79`), but the shipped templates contradict the fleet owner it never names: `useShakaCore.ts:25` `type ShakaNamespace = any`, plus `:29,:30,:93,:99,:116`; `AdsManager.ts:2,5,6,7`; `PlayerLabPage.vue:58,62,66`; `player.ts` has no player type at all. `alaa-vue-typescript-clean-code/references/20-typescript-composition-contract.md:97` permits `any` only "isolating an untyped third-party boundary with a comment and immediate typed wrapper" — none of these has either. `alaa-vue-typescript-clean-code` named 0 times. |
| 7 | Algorithm and data-structure choice | **FAILS** | No complexity budget anywhere. `QuizEngine.ts:36-42` linear-scans every cue on every `timeupdate` (~4 Hz, unbounded n) with no index and no sorted cursor. `PlaybackConductor.ts:37-46` re-`map`s, re-parses two ISO dates per item and re-`sort`s the whole schedule every 1000 ms (`:22`) to find one active item that changes once an hour. |
| 8 | Configurability, safe defaults, boundary validation | **FAILS** | Shaka's `configure()` is the official capability this skill exists to wrap. It appears exactly twice: `useShakaCore.ts:79-84` (`streaming.preferNativeHls` only) and one migration example (`MIGRATION_5_0_8_TO_5_1_11.md:68-78`). No `bufferingGoal`, `rebufferingGoal`, `bufferBehind`, `retryParameters`, `abr.*`, `drm.*` anywhere. Defaults are scattered magic numbers with no validation: `AdsManager.ts:70` `?? 12000`, `AnalyticsTracker.ts:89` `?? 15`, `:39` `1000`, `PlaybackConductor.ts:22` `?? 1000`, `useShakaCore.ts:113` `500`, `:118` `2000`. `startTime`, `heartbeatIntervalSec` and `adTimeoutMs` are accepted unvalidated. Linking the config tutorial (`OFFICIAL_LINKS.md:12`) is not wrapping it. |
| 9 | Speed of development and debuggability | **SATISFIED** | The one criterion genuinely met for its domain: an isolated harness (`PlayerLabPage.vue`, `MIGRATION_PLAN.md:9-12`), a template copier (`scripts/scaffold.sh`), symptom-first diagnosis (`TROUBLESHOOTING.md:1-71`), a cheapest-evidence rule (`QA_MODES.md:24-25`), and debug-build log level (`TROUBLESHOOTING.md:78`). Caveat: `scaffold.sh` copies 2 of 9 templates (`scaffold.sh:20-24`). |
| 10 | Documentation | **FAILS** | Criterion 10 is what shipped, how it is operated, **and how it fails**. `SKILL.md:149-158` ends its deliverables at "a migration plan and QA checklist"; no operator note, no player-config document, no error/telemetry contract document is ever required of the produced work. `alaa-frontend-doc-annotations` named 0 times. |

Nine FAILS, one SATISFIED, zero legitimate NOT-OWNED — the skill names no out-of-batch owner at all, so every gap it does not fill is a failure rather than a delegation.

### 3. Defect classes actually found

1. **Stale hardcoded model pins.** `assets/config-examples/agents/ads.toml:1`, `analytics.toml:1`, `conductor.toml:1`, `core.toml:1`, `overlay.toml:1`, `qa.toml:1` — all six open `model = "gpt-5.5"`. Lines 2 of each add `model_reasoning_effort = "high"|"medium"`, an effort vocabulary the carry-over already supersedes. `config.toml` carries no model key. Consequence: the pin is not merely stale, it is stale in a file whose purpose is to be copied into a user repository, where no future upgrade of this skill can reach it.
2. **Wrong/absent trigger syntax.** `$` form only, 7 sites, `/` form zero: `SKILL.md:29,39,96,97`, `prompts/AGENT_PROMPT.md:33`, `references/QA_MODES.md:49`, `agents/openai.yaml:4` (plus `$playwright` `SKILL.md:35`, `QA_MODES.md:48`; `$openai-docs` `SKILL.md:41`). Consequence: every companion routing instruction is inert in Claude Code.
3. **Duplication between body and references.** `SKILL.md:204-252` ≈ `ARCHITECTURE.md:13-79`; `SKILL.md:271-278` ≈ `QA_MODES.md`; `SKILL.md:45-67` ≈ `UPSTREAM_WATCHLIST.md:6-18`; `SKILL.md:99-114` ≈ `references/README.md:8-23`; `SKILL.md:280-299` ≈ `MULTI_AGENT_SETUP.md:26-38`; `QUIZ_OVERLAY.md:10-21` is a verbatim copy of `types/player.ts:15-24`; `CONDUCTOR_SCHEDULE.md:10-18` of `types/player.ts:35-41`. Consequence: five of eleven body sections pay always-loaded bytes for content that already exists one hop away.
4. **Project-specific content in an always-loaded body.** `SKILL.md:47-58` pins a dated upstream fact ("As of **2026-06-28** … `v5.1.11`, published on **2026-06-24**") into the body; `SKILL.md:116-147` is a 32-line intake questionnaire; `SKILL.md:301-315` an 11-step sequence. Consequence: the body goes stale on a schedule and burns context on every invocation regardless of task.
5. **Long numbered procedures nobody reads in order.** `MIGRATION_5_0_8_TO_5_1_11.md:29-165` is a ten-part numbered audit (8,648 B, the largest reference), `SKILL.md:301-315`, `checklists/MIGRATION_PLAN.md` phases 0-5, `checklists/QA_CHECKLIST.md` 9 flat lists. `TROUBLESHOOTING.md` is the counter-example and shows the right shape. Consequence: the migration file is read start-to-finish or not at all; there is no "you are seeing X → read section Y" entry.
6. **Description with no "do not use for".** Not found — `SKILL.md:3` ends "Do not use it for simple MP4-only playback or non-Vue stacks", and `SKILL.md:87-91` expands it. This class is clean.
7. **Fragile tooling.** `scripts/scaffold.sh:16` resolves `${SCRIPT_DIR}/../assets/templates` with `cd … && pwd`, which aborts under `set -e` if the layout changes; `:18` `mkdir -p "$TARGET_DIR"` accepts any absolute path, so `./scaffold.sh /etc/x` writes outside any repository; `:20-21` overwrite unconditionally with no `-n`, no backup, no diff. No `--help`, no `--dry-run`, no self-test, and the file is not executable in this tree (`-r--r--r--`). Consequence: an agent can silently clobber a modified `useShakaCore.ts`.
8. **Shipped `__pycache__`.** None. Clean.
9. **Unnamed gaps against section 2.** Nine of ten criteria fail with no owner named; the skill names exactly two companions (`alaa-frontend-developer`, `alaa-low-noise`) and one anti-companion (`openai-docs`). Consequence: an agent following this skill has no route to the retry, security, telemetry-naming or testing doctrine that the fleet already settled.
10. **Body larger than it needs to be.** 11,075 B, 1,613 words, eleven H2 sections, of which five are duplicates (class 3) and two are questionnaires. Consequence: ~4 KB of always-loaded text buys nothing.
11. **No stated companion boundary.** `SKILL.md:25-43` states ownership against two skills only; `alaa-vue-typescript-clean-code` owns the shape of the very files this skill ships and is never named. Consequence: the templates and the owning contract will drift with nothing to detect it.

### 4. The four structural rulings

### (a) The model pins in the emitted TOMLs

**Evidence.** `model = "gpt-5.5"` at line 1 of all six of `agents/{ads,analytics,conductor,core,overlay,qa}.toml`; `model_reasoning_effort` at line 2 of each (`high` ×4, `medium` ×2); `qa.toml:3` adds `sandbox_mode = "read-only"`. `config.toml` has no model key. `agents/openai.yaml:3` separately hardcodes a *version*: `"Shaka 5.1 migration and Quasar player pack"`.

**Ruling — emit no model key and no effort key at all, and replace them with a single comment line pointing at the owner.** Concretely, if any config example survives ruling (b), each file opens with:

```
### Model and reasoning effort are not pinned here.
### Take both from /alaa-prompting-guide ($alaa-prompting-guide),
### references/50-effort-and-thinking.md, at the time you run this lane.
```

Two reasons the pointer beats the alternatives. A **placeholder** (`model = "<see /alaa-prompting-guide>"`) is the worst option available: TOML accepts it as a valid string, the runtime rejects it at spawn time with an opaque error, and the failure surfaces in the user's project rather than in the skill. **Omission alone** is safe — the runtime falls back to the session/profile default — but silent, and a future editor re-adds a pin because nothing said not to. Omission *plus* the prohibition comment is the only form that survives being copied into a repository the skill can never edit again, which is precisely the property that makes this instance of defect class 1 the most durable in the batch.

**Cost of the option not chosen.** Keeping a pin, even a corrected one, means the fleet has model pins in three places instead of one: the two orchestrator packs (enforced by `scripts/validate_pack.py`) and here, unenforced. `gpt-5.5` is already wrong twice over — wrong generation, and an effort vocabulary the current guide replaces — which is the whole argument made concrete.

**Additionally**: strip the version from `agents/openai.yaml:3`. `"Shaka 5.1 migration and Quasar player pack"` becomes `"Shaka Player integration for Quasar apps"`. A version number in UI metadata is a pin with the same decay property and no benefit.

### (b) The multi-agent machinery

**Ruling: retire and route. The content is generic orchestration, not a Shaka-specific division of labour.**

Evidence, file by file:

- `references/MULTI_AGENT_SETUP.md` contains no Shaka noun below the role list. `:19-23` "Enable the experimental feature in Codex and restart the session. You can also enable it in your Codex config via the `multi_agent` feature flag" is Codex runtime configuration. `:40-46` "1. Ask the parent agent to spawn one sub-agent per track 2. Let each agent work independently 3. Wait for all results 4. Consolidate…" is the fan-out/join pattern verbatim. `:48-51` "Mark exploration-oriented roles as read-only" is sandbox policy. Every one of those sentences is owned by `alaa-codex-orchestrator` / `alaa-cc-orchestrator`, and each is stated there with enforcement this file does not have.
- `prompts/MULTI_AGENT_PROMPT.md:12-45` — the seven tracks are one-to-one with the five product modules plus QA that `references/ARCHITECTURE.md:30-68` already defines. Track 1 "Implement the Shaka core wrapper / Handle attach, load, destroy, networking filters, and stats" is `ARCHITECTURE.md:15-25` restated as an imperative. There is no scheduling constraint, no shared-artifact protocol, no merge-conflict rule, no ordering dependency between tracks — nothing an orchestrator could not express.
- `assets/config-examples/agents/*.toml` — the `developer_instructions` bodies are 2-4 lines each and each is a compression of an existing reference: `ads.toml:4-6` compresses `ADS_VAST_VMAP.md:49-52`; `analytics.toml:4-5` compresses `ANALYTICS_WATCHTIME.md:5-14,51-54`; `core.toml:4-6` compresses `ARCHITECTURE.md:15-28`.
- `SKILL.md:280-299` is a fourth copy of the same six-role list.

So the pack is four restatements of one module decomposition wearing an orchestration costume. The single fact worth preserving is genuinely Shaka-specific and is one sentence long: **the player's module seams (core / ads / analytics / overlay+markers / conductor / QA) are the safe parallel-work boundaries because each consumes player events and none mutates core internals** — which is a lane *definition*, and it belongs in the architecture reference, one paragraph, with a routed pointer to `/alaa-cc-orchestrator` (`$alaa-cc-orchestrator`) and `/alaa-codex-orchestrator` (`$alaa-codex-orchestrator`) for how lanes are spawned, pinned and sandboxed.

**Retire to `_to_delete/`:** `prompts/MULTI_AGENT_PROMPT.md`, `references/MULTI_AGENT_SETUP.md`, all seven files under `assets/config-examples/`, and `SKILL.md:280-299`.

**Cost of the option not chosen (keep it as a lane definition).** Two role vocabularies for one fleet — six here, twenty-one there — with no mapping between them, so an agent given "spawn the overlay agent" cannot tell which orchestrator role that is. Model pins in a second, unvalidated location that `validate_pack.py` does not scan. A sandbox rule (`MULTI_AGENT_SETUP.md:48-51`) that quietly competes with the orchestrators' settled routing policy. And a maintenance surface that goes stale on the orchestrators' release cadence, not this skill's.

### (c) ALL_CAPS unnumbered filenames and the missing topic map

**Ruling: rename to numbered lowercase and add `references/00-topic-map.md`. The rename breaks nothing outside the skill.**

Count: 17 files in `references/`, above the ≥9 threshold, so the router must live at `references/00-topic-map.md` with a single pointer line in `SKILL.md`.

Full inbound-pointer inventory (everything the rename touches):

| Where | Lines | What |
|---|---|---|
| `SKILL.md` | 61-62, 65, 99, 100-101, 103-114, 278, 297-299 | 16 filename mentions plus the "Quick start" list |
| `checklists/MIGRATION_PLAN.md` | 5, 6 | `UPSTREAM_WATCHLIST.md`, `MIGRATION_5_0_8_TO_5_1_11.md` |
| `references/UPSTREAM_WATCHLIST.md` | 17-18 | `MIGRATION_5_0_8_TO_5_1_11.md` |
| `references/README.md` | 8-23 | all 16 |
| `references/MULTI_AGENT_SETUP.md` | 38 | `assets/config-examples/` |
| `references/QA_MODES.md` | 48-49 | skill names only, no paths |

`scripts/scaffold.sh` references no file under `references/` — it touches only `assets/templates/ShakaPlayer.vue` and `useShakaCore.ts` (`:20-21`). A grep across all of `skills/sohrab/` for `alaa-shaka-player` paths returns **zero** hits outside the skill and `UPGRADE-CARRYOVER.md:183` (a membership list, not a path). So the rename cost is roughly twenty pointer edits, all internal, in files that Phase 2 rewrites anyway.

Against that: leaving it is the batch's only non-conforming naming scheme, in the batch's largest reference set, next to `alaa-quasar-app-vite-v3` (29 numbered files, `00-topic-map.md`) and `alaa-frontend-developer` (13 numbered files, `00-topic-map.md`). Uniformity beats local optimality, and the local optimum here is worth nothing — ALL_CAPS filenames carry no ordering information, which is exactly why `references/README.md:8-23` lists them in an order matching neither the alphabet nor the reading path.

**`references/README.md` is not a router** and must be retired, not converted: it is a bare bullet list of sixteen filenames with no condition attached to any of them, preceded by "Open only the ones needed for the current task" (`:3-4`) — an instruction an agent cannot execute, because nothing tells it which one is needed. It is also a second router alongside `SKILL.md:99-114`, violating one-router-per-skill.

### (d) `INSTALL.md`

**Ruling: redundant, and contradictory in two places. Retire it.**

It is the third statement of the same policy, exactly as in the earlier batch:

1. `install-skills.md` at the repository root is authoritative (carry-over §6: "correct and worth treating as authoritative for install paths … If any skill's own installation docs disagree with it, the skill is wrong, not this file").
2. `SKILL.md:330-336` states it a second time ("Keep it in a Codex-discoverable skills location, typically `~/.codex/skills/alaa-shaka-player` or a repo-local skills directory. See `INSTALL.md`…").
3. `INSTALL.md` states it a third time, at 910 B.

The contradictions:

- `INSTALL.md:8-11` presents `.codex/skills/alaa-shaka-player/` and `~/.codex/skills/alaa-shaka-player/` as co-equal "Recommended locations", and `:18-23` gives project-local its own procedure. The field-verified location for a personal skill is `~/.codex/skills` alone; `.agents/skills` — offered at `:28-30` as merely an "Alternative location" that "Some agent runtimes also support" — is in fact the *reserved* location for skills that travel with a repository. The file inverts the rule into a menu.
- `INSTALL.md:16` hardcodes an absolute authoring-machine path, `D:/Sohrab/Project/skills/skills/sohrab/alaa-shaka-player/`, into a shipped artifact. That is the same defect class as a model pin: a fact true only where it was written, presented as canonical.
- `INSTALL.md:25` and `:36-37` ("restart Codex so it re-scans available skills", "restart the agent session before relying on the new metadata") are runtime operations, owned by `alaa-codex-runtime-ops`.

Retire `INSTALL.md` to `_to_delete/` and delete `SKILL.md:330-336` with it, replacing both with nothing — installation is not this skill's subject and the authoritative file already covers it. Freed always-loaded body: ~250 B.

### 5. Boundary map

### (a) Legitimately owns

- Shaka `configure()` surface and its safe defaults for this stack — the official capability it exists to wrap (currently unfilled, criterion 8).
- The `shaka.util.Error` / `MediaError` taxonomy and its *binding* to `alaa-reliability-sla` doctrine: which category is recoverable, which retry class each maps to, which is terminal for the session.
- Player lifecycle in a Vue/Quasar SPA: dynamic import, polyfill order, attach, non-reactivity, teardown ordering.
- HLS/DASH/DRM behavioural caveats per browser and platform, and the Safari/iOS native-HLS constraint.
- Version migration across Shaka releases and the upstream watchlist.
- The module seams (core / ads / analytics / overlay / conductor) as a decomposition — not as an agent roster.
- Player-specific QA mode selection: which evidence proves which class of player defect.

### (b) Must disclaim, and who owns it

| Ground | Owner it must name |
|---|---|
| Every metric, event and log-field name in the telemetry payload | `alaa-services-contract` (request, never invent), landing in the WA `wa_raw.events_raw` / `wa_raw.watch_segments_raw` schema |
| Telemetry requirement levels and gates | `alaa-observability-soc` |
| Retry, backoff, timeout, degradation doctrine | `alaa-reliability-sla` (this skill states only the Shaka-specific binding) |
| Threat classes, review triggers, fail-closed doctrine | `alaa-security-review` |
| Trust boundary; that a client-supplied opaque value carries no trust | `alaa-trust-gateway-auth` |
| Presigned media URLs and the `STORAGE_*` contract | `alaa-minio-object-storage` / `alaa-arvan-object-storage` |
| Test design and the six proof levels | `alaa-testing-strategy` |
| The quality bar itself | `alaa-project-constitution` |
| Vue component and Pinia store shape, TypeScript strictness | `alaa-vue-typescript-clean-code` |
| Quasar/Vite build, SSR/PWA config | `alaa-quasar-app-vite-v3`, `alaa-frontend-developer` |
| Multi-agent orchestration | `alaa-cc-orchestrator` / `alaa-codex-orchestrator` |
| Long-task planning, phasing, state | `alaa-workflow` |
| Art direction and design system | `alaa-ui-ux-design-system` |
| Output discipline | `alaa-low-noise` (already named, `SKILL.md:39`, `:96`) |
| Install paths | repository `install-skills.md` |

### (c) Where it legislates an owner's ground in its own voice

**Against `alaa-services-contract` and the WA pipeline (names and values):**

- `assets/templates/services/AnalyticsTracker.ts:1-15` — `export type AnalyticsHeartbeat = { contentId: string; positionSec: number; watchedDeltaSec: number; playbackRate: number; muted: boolean; volume: number; quality?: {...}; isAdPlaying: boolean; timestampMs: number }`. Nine invented field names in a shipped, copyable artifact. It carries no `project_id` — the column that sits **first in `ORDER BY`** in both raw WA tables — and no event or session identifier at all. Against a sink that retries 20× into a plain `MergeTree` with block deduplication off, a heartbeat with no idempotency key makes over-count structural rather than incidental, on top of the `count()`-is-an-upper-bound property WA already has.
- `AnalyticsTracker.ts:129,133,137,143,148` — `sendEvent?.('play')`, `('pause')`, `('seeked')`, `('ratechange')`, `('volumechange')`; `QuizEngine.ts:55,63` — `('quiz_open')`, `('quiz_close')`; `AdsManager.ts:43,53,58` — `('ads_requested')`, `('ad_started')`, `('ad_ended')`. Eleven invented event names in two naming styles (bare verb vs `snake_case` noun_verb), neither requested from the owner.
- `references/ANALYTICS_WATCHTIME.md:17` — *"Send a heartbeat every 10 to 15 seconds with at least:"* followed by an eight-item payload contract (`:19-26`). A cadence and a payload are a service contract.
- `references/ANALYTICS_WATCHTIME.md:5-14` — *"Count watch-time only when content is genuinely being watched. A practical baseline is: the video is playing / the content is not buffering / …"* — a metric definition stated locally, and implemented divergently at `AnalyticsTracker.ts:95-104`, which adds `readyState >= 2` and `readyState < 3` thresholds the prose never mentions.

**Against `alaa-reliability-sla` (retry/timeout/degradation doctrine):**

- `SKILL.md:187-191` — *"Keep networking auth and retries explicit. Register filters before `load()`. Since request filters run on every attempt in v5.x, use that to refresh expired credentials safely."* A retry-and-credential-refresh policy in the always-loaded body with no citation.
- `assets/templates/services/AdsManager.ts:70` — `const timeoutMs = this.config.adTimeoutMs ?? 12000`. A concrete timeout value, unsourced, unvalidated.
- `references/ADS_VAST_VMAP.md:49-52` — *"Required fail-safe. If an ad request fails, the ad response is empty, or the ad never starts, resume the content path instead of leaving the session stuck."* This is degradation doctrine, correctly reasoned and wrongly located.
- `references/TROUBLESHOOTING.md:58-60` — *"Fix: add a watchdog timeout / force recovery into the content path."*

**Against `alaa-trust-gateway-auth` and the object-storage skills (media URL handling):**

- `references/HLS_NOTES.md:10-12` — *"If manifests, segments, or licenses require signed requests or custom headers, register networking filters in the Shaka core wrapper."* The entire treatment of signed media access in the pack, and it treats a signed URL as a transport detail rather than as a bounded, named, expiring read grant.
- `assets/templates/types/player.ts:5-6` — `manifestUri: string` and `headers?: Record<string, string>` on the same shipped `MediaItem`, with no statement of which of the two carries the credential or how long either is valid.
- `assets/templates/ShakaPlayer.vue:24` / `useShakaCore.ts:8,93-97` — `extraHeaders` travels as a Vue component prop into `registerRequestFilter`, so a bearer token is visible in devtools and in any component-tree dump.
- `references/TIMELINE_MARKERS.md:30-32` — *"A practical share URL pattern is: `/watch/<id>?t=123.4`"* — a URL contract; and if `<id>` ever resolves to a presigned asset, a share link becomes a transferred read grant.
- `SKILL.md:145` — *"token refresh and signed URL policy"* listed as an input to *collect*, never as a rule to *obey*.

**Against `alaa-ui-ux-design-system`:**

- `references/QA_MODES.md:50` — *"treat pure art direction as outside the Sohrab pack unless a separate design skill is explicitly available in the session."* Repeated at `prompts/AGENT_PROMPT.md:32` and `SKILL.md:264-267`. The claim is factually wrong — `alaa-ui-ux-design-system` ships in this very batch — and its form is the self-granted exception: the escape clause is conditioned on the agent's own session state rather than on a named owner.

**Against the orchestrators:** `references/MULTI_AGENT_SETUP.md:19-23`, `:40-46`, `:48-51` (see 4(b)).

**Against `install-skills.md`:** `INSTALL.md` entire, `SKILL.md:330-336` (see 4(d)).

### 6. Duplication

| Content | Location A | Location B (and C…) | Survives |
|---|---|---|---|
| Three-layer architecture + five module responsibility lists | `SKILL.md:204-252` (49 lines) | `references/ARCHITECTURE.md:13-79` | **B** — body keeps one sentence naming the seams |
| QA mode selection (headless vs visual) | `SKILL.md:271-278` | `references/QA_MODES.md:5-45`; `checklists/QA_CHECKLIST.md:3-5` | **B** (`QA_MODES`); C folds in |
| Upstream baseline, version + date | `SKILL.md:45-58` | `references/UPSTREAM_WATCHLIST.md:6-18` | **B** — a dated fact must never sit in an always-loaded body |
| Reference file list | `SKILL.md:99-114` | `references/README.md:8-23` | **Neither** — replaced by `references/00-topic-map.md` |
| Multi-agent role list | `SKILL.md:280-299` | `MULTI_AGENT_SETUP.md:26-38`; `MULTI_AGENT_PROMPT.md:12-45`; `config.toml:6-28` + six TOMLs | **None** — retired per 4(b) |
| Implementation constraints | `SKILL.md:167-202` | `prompts/AGENT_PROMPT.md:22-33` | **A** |
| Implementation sequence | `SKILL.md:301-315` | `checklists/MIGRATION_PLAN.md:3-39`; `MIGRATION_5_0_8_TO_5_1_11.md:198-214` | **A** for the generic order; the 5.0.8→5.1.11 checklist stays in the migration reference |
| `QuizCue` type, verbatim | `references/QUIZ_OVERLAY.md:10-21` | `assets/templates/types/player.ts:15-24` | **B** — reference cites the template path |
| `ScheduleItem` type, verbatim | `references/CONDUCTOR_SCHEDULE.md:10-18` | `assets/templates/types/player.ts:35-41` | **B** |
| Conductor offset formula | `references/CONDUCTOR_SCHEDULE.md:28-32` | `PlaybackConductor.ts:54-55` | **B** (code) — reference states the invariant, not the arithmetic |
| Deprecated-preference migration | `SKILL.md:192-196` | `ABR_AND_TRACKS.md:13-24`; `MIGRATION_5_0_8_TO_5_1_11.md:41-63`; `UPSTREAM_WATCHLIST.md:11-14` | **`MIGRATION…`** — the other three become pointers |
| Browser/device matrix | `checklists/QA_CHECKLIST.md:7-16` | `SKILL.md:127-134` | **A** |
| Installation | `INSTALL.md` | `SKILL.md:330-336`; repo `install-skills.md` | **`install-skills.md`** |

**Against `alaa-vue-typescript-clean-code`** — this is the more damaging axis, because it is duplication *plus* contradiction:

- Props typing: `ShakaPlayer.vue:19-28` uses `type Props = {…}` with `defineProps<Props>()` and per-use `?? false` fallbacks (`:49-53`), where `alaa-vue-typescript-clean-code/references/10-vue-style-contract.md:19-33` prescribes `interface Props` with `withDefaults`. Defaults are consequently stated twice — once in `ShakaPlayer.vue:49-53` and once again in `useShakaCore.ts:69` (`config.autoplay ?? false`).
- `any`: eleven sites (§2 criterion 6) against `20-typescript-composition-contract.md:97`.
- Composable and teardown shape: `useShakaCore` returns `{ init, load, destroy }` while `init` returns a *second* API object with its own `load`/`destroy` (`useShakaCore.ts:125-140` vs `:178-182`) — two divergent handles to the same lifecycle, so `ShakaPlayer.vue:72-74` calls `core.destroy()` while the consumer holds `api.destroy`. That is the "teardown guard" antipattern `65-alaa-observed-patterns.md` catalogues.
- Store shape: absent entirely. The pack ships five stateful services as hand-rolled classes with constructor-injected callbacks and no Pinia store anywhere (`pinia` appears 0 times), while `50-quasar-vite-pinia-contract.md` owns that decision. The reference-side statement survives; the templates must be rewritten to obey it.

### 7. Wording-test failures

| # | Quoted sentence | file:line | Failure mode | Replacement |
|---|---|---|---|---|
| 1 | "Use `$alaa-low-noise` when the task spans many player files, noisy logs, or a large browser matrix." | `SKILL.md:39` | Three abstract nouns standing in for observable conditions ("many", "noisy", "large"); plus Codex-only trigger | "Invoke `/alaa-low-noise` (`$alaa-low-noise`) when the task will touch more than three player files, or when you are about to paste browser console output into your reply." |
| 2 | "Use a plain variable, closure state, or `markRaw` only if needed." | `SKILL.md:174` | Self-granted exception with no external referent — "if needed" is judged by the agent against nothing | "Hold the Shaka instance in a module- or closure-scoped `let`. Use `markRaw` only when the instance must be passed into an existing reactive container you are not allowed to change; record that container's path in the PR description." |
| 3 | "Destroy aggressively and completely." | `SKILL.md:182` | Preference adverb where a constraint and an ordering were meant; no enumeration of what must be released | "Before the component unmounts, release in this order: clear every interval and timeout, remove every listener you registered on the player, on the `<video>` element and on `document`, then `await player.destroy()`. `onBeforeUnmount` must not return until `destroy()` resolves." |
| 4 | "Do not hard-code old 5.0.x versions in new work." | `SKILL.md:60` | Prohibition with no positive replacement, and no scope (a lockfile? a doc? a comment?) | "Pin `shaka-player` in `package.json` to the version recorded in `references/…-upstream-watchlist.md` under 'verified baseline'. If that entry is older than 30 days, re-read the releases page before pinning and update the entry with the release URL and today's date." |
| 5 | "Decide early whether hidden-tab playback counts as watch-time. This should be a product-level decision, not an accidental implementation detail." | `ANALYTICS_WATCHTIME.md:53-54` | A rule that produces no behaviour — an agent that follows it exactly can ship either answer; no default, no owner, no escalation | "Default: hidden-tab time does not accumulate. `ignoreHiddenTab` is `true` unless a written product requirement says otherwise; record which requirement changed it in the config comment." |
| 6 | "resume the content path instead of leaving the session stuck." | `ADS_VAST_VMAP.md:52` | "Stuck" is unobservable; no bound, and the pack's only actual bound (12,000 ms) lives in a template that this sentence never cites | "If no `ad-playing` event arrives within `adTimeoutMs` of the ad request, cancel the ad, emit the ad-failure telemetry event, and resume content. `adTimeoutMs` defaults to 12000 and is validated to the range 2000–30000 at construction." |
| 7 | "Make sure your origin or CDN correctly supports range requests and streaming headers." | `HLS_NOTES.md:15-16` | "Correctly" is not checkable; no command, no expected response, no failure signature | "Verify with `curl -sI -H 'Range: bytes=0-1' <segment-url>` that the response is `206 Partial Content` and carries `Content-Range` and `Accept-Ranges: bytes`. A `200` here means the CDN is ignoring ranges; report it before tuning buffer configuration." |
| 8 | "treat pure art direction as outside the Sohrab pack unless a separate design skill is explicitly available in the session." | `QA_MODES.md:50` (also `AGENT_PROMPT.md:32`, `SKILL.md:264-267`) | Self-granted exception conditioned on the agent's own session state; and factually wrong — the owner exists | "Visual direction, colour, type and component styling belong to `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`). Route there and do not decide them here." |
| 9 | "Prefer `.js` plus JSDoc if the repo is JavaScript-first. Use `.ts` only if the repo already uses TypeScript or the user asks for it." | `SKILL.md:161-162` | Preference verb where another skill states a constraint, with no conflict rule; the live frontend repository is TypeScript | "The frontend target is Quasar + Vue 3 + TypeScript. Emit `.ts` and `.vue` with `lang=\"ts\"`, and follow `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`) for typing, props and store shape. If the host repository is JavaScript-only, say so and stop before generating files." |
| 10 | "Treat a note as fixed only after it is confirmed in an official release note, official doc, or focused local reproduction on the target version." | `UPSTREAM_WATCHLIST.md:63-65` | Scope-free ("a note"), and the third disjunct inverts the source hierarchy `OFFICIAL_LINKS.md:27-36` sets — a local repro can now overrule an official doc | "An open issue or PR may be cited as a symptom, never as a fixed behaviour. Record it as fixed only when an official release note or the official docs say so; a local reproduction that no longer shows the symptom is evidence the workaround can be removed from this repository, not evidence upstream changed." |

Runner-up, worth fixing in Phase 2: `TROUBLESHOOTING.md:28` "verify the current Shaka release first" — no action, no source, no acceptance criterion.

### 8. Stale or unverifiable claims

Read date claimed by the skill: **2026-06-28** (`SKILL.md:47`, `UPSTREAM_WATCHLIST.md:8`), one month before this audit. Nothing in the pack carries a per-claim source URL; `OFFICIAL_LINKS.md` carries URLs with no read dates and no claim attached. Every item below is therefore *verified from the files* only in the sense that the file asserts it.

**Version claims**

| Claim | file:line | Status |
|---|---|---|
| `v5.1.11` is the latest release, published `2026-06-24` | `SKILL.md:49-50`, `UPSTREAM_WATCHLIST.md:10-11` | **needs live web research** — a one-month-old "latest" claim on a project with a weekly patch cadence is presumptively stale |
| `v5.0.8` is the skill's older coverage baseline | `SKILL.md:64`, `MIGRATION_5_0_8_TO_5_1_11.md:1-4` | **needs live web research** — and, separately, needs a *reason*: nothing states why 5.0.8 rather than any other 5.0.x, so if no repository is actually pinned there the whole 8.6 KB file may be addressed to nobody |
| `v5.1.10` fixes a hang loading a second asset after DRM playback | `MIGRATION_5_0_8_TO_5_1_11.md:117` | **needs live web research** (specific patch attribution) |
| `v5.1.11` fixes captions line-through styling | `MIGRATION…:157`, `UPSTREAM_WATCHLIST.md:22` | **needs live web research** |
| `v4.16.24` notes remain useful for repos pinned there | `UPSTREAM_WATCHLIST.md:15-16` | **needs live web research** |
| Old individual preference fields "are documented as being removed in the next major version" | `SKILL.md:194-195`, `ABR_AND_TRACKS.md:21-24`, `MIGRATION…:26` | **needs live web research** — verify against the upgrade guide; "next major" is unnamed |

**API names**

`new shaka.Player()` then `await player.attach(video)` (`SKILL.md:170`, `useShakaCore.ts:75-76`, `UPSTREAM_WATCHLIST.md:69`); `shaka.polyfill.installAll()` (`useShakaCore.ts:61`); `shaka.Player.isBrowserSupported()` (`:63`); `player.getNetworkingEngine()` / `registerRequestFilter` (`:86,:93`); `player.getStats()` (`:117`) — **needs live web research** but low risk; these are long-standing. `player.updateStartTime()` (`useShakaCore.ts:148-149`, `MIGRATION…:97`, `QA_CHECKLIST.md:24`) — **needs live web research**, this is a comparatively recent addition and the template calls it *after* the player exists but guards on truthiness rather than on version. `player.getChaptersAsync` (`MIGRATION…:89`) — **needs live web research**. `adManager.setContainers(...)` and `adManager.requestClientSideAds(...)` (`AdsManager.ts:30-42`) — **needs live web research**; the `IAdManager` surface has changed across 4.x→5.x. `shaka.extern.AudioPreference` / `TextPreference` / `VideoPreference` (`MIGRATION…:61-63`) — **needs live web research**.

**Config keys**

`streaming.preferNativeHls` (`useShakaCore.ts:79-82`) — **needs live web research**; historically this key has been spelled `useNativeHlsOnSafari` and later `useNativeHlsForFairPlay`, and the skill's own rule is that no lane invents a flag spelling. `manifest.hls.liveSegmentsDelay` (`HLS_NOTES.md:35`) — **needs live web research**. `networking.commonAccessTokenHeaderName` (`MIGRATION…:109`) — **needs live web research**. `subtitleDelay` (`MIGRATION…:88`, `UPSTREAM_WATCHLIST.md:48`) — **needs live web research**; unclear whether it is a config key or a method. `chaptersUri` (`HLS_NOTES.md:41`, `MIGRATION…:90`) — **needs live web research**. UI options `mute_volume`, `showUIOnPaused`, `showMenusOnTheRight`, `mediaSession.allowAutoPiP`, `controlPanelElements` (`MIGRATION…:151-156`, `UPSTREAM_WATCHLIST.md:23-24`) — **needs live web research**. The `preferred*` deprecation list of fifteen names (`MIGRATION…:43-57`) — **needs live web research**, name by name; a wrong spelling here produces a silent no-op migration.

**Error codes and taxonomies**

**None exist.** Zero occurrences of `shaka.util.Error`, error `category`, error `code`, `severity`, `MediaError`, `retryParameters`. This is *not* a staleness problem — it is the absence noted in §2 criterion 2, and it means Phase 2 must research the taxonomy from scratch rather than refresh it.

**Ad events** — `ad-playing`, `ad-interstitial-preloaded`, `ad-break-started` with a `startedAt` payload (`ADS_VAST_VMAP.md:22-26`, `MIGRATION…:138-143`) — **needs live web research**; event-name strings are exactly the class of fact no lane may invent, and the pack gives no URL for any of the three.

**Browser / DRM / platform support**

iOS support depends on Apple's native HLS path, so no DASH parity (`HLS_NOTES.md:30-31`, `UPSTREAM_WATCHLIST.md:72-73`) — **needs live web research**, long-standing and probably still true. The FAQ warns against wrapping the player in a Vue reactive object (`UPSTREAM_WATCHLIST.md:70-71`) — **needs live web research**; this one carries the most weight in the skill (`SKILL.md:173-175`) and should be quoted with its FAQ anchor. FairPlay differs between Modern EME and legacy Apple Media Keys (`UPSTREAM_WATCHLIST.md:76-77`, `TROUBLESHOOTING.md:62-71`) — **needs live web research**. PlayReady on Windows browsers beyond Edge (`MIGRATION…:119`) — **needs live web research**. Playback rate clamped to 16× (`MIGRATION…:99-100`) — **needs live web research**. HLS Interstitials, `X-ASSET-LIST`, `X-PLAYOUT-LIMIT`, `_HLS_start_offset`, `CAN-SKIP-DATERANGES`, SGAI, AC-4 immersive stereo, `audio/x-mpegurl` (`ADS_VAST_VMAP.md:37-38`, `MIGRATION…:129-146`, `UPSTREAM_WATCHLIST.md:28-30,57-59`) — **needs live web research** as a block. TiVo OS, Titan OS, DASH JSON, XLink auto-processing, MoQT/MSF (`MIGRATION…:183-196`, `UPSTREAM_WATCHLIST.md:56-59`) — **needs live web research**; these read as release-note skimming and several may be experimental flags rather than supported surfaces.

**Chrome chunk-demuxer-append failure when HLS codec info is missing** (`HLS_NOTES.md:21-23`) — **not verifiable**: a browser-specific failure mode asserted with no error string, no Chrome version, and no source.

**Documentation host** — every URL in `OFFICIAL_LINKS.md:7-18` points at `shaka-player-demo.appspot.com/docs/api/…`. **needs live web research**: confirm the canonical docs host has not moved, since a stale host silently invalidates all ten links at once.

**Provenance ledger audit.** `UPSTREAM_WATCHLIST.md` + `OFFICIAL_LINKS.md` are a proto-ledger and fail the standard on four counts: (i) **no source URL per claim** — the watchlist makes ~40 factual assertions and carries zero links, while the links file carries ten links and zero claims, so nothing joins them; (ii) **no read dates and no `read: unverified as of <date>` markers** — one global date at `:8` covers assertions of visibly different vintage; (iii) **no re-read interval** — `:83` "Whenever you update this skill" is not an observable condition, since a skill can sit untouched for a year while its subject ships forty releases; (iv) **no searched-and-not-found convention**, so absence of a claim is indistinguishable from a claim of absence. What they get *right* and Phase 2 must keep: `MIGRATION_5_0_8_TO_5_1_11.md:6-16` ("Do not derive migration requirements from source-code diffs alone … release notes and official docs are the migration contract") and `OFFICIAL_LINKS.md:38-46` (freshness triggers plus the community-sources-are-symptoms-only rule) are exactly the right doctrine, stated well, in the wrong shape.

### 9. Router audit

- **Reference count:** 17 files in `references/` (16 content + `README.md`). Above the ≥9 threshold, so the router must be `references/00-topic-map.md`. **That file does not exist.**
- **Router location:** currently two, both wrong. `SKILL.md:99-114` lists twelve filenames inside "Quick start"; `references/README.md:8-23` lists sixteen. Two routers violates one-router-per-skill; neither is at the required path.
- **Is `references/README.md` a router?** No. It is a bare bullet list of filenames — no condition, no task, no symptom attached to any entry, and its order matches neither the alphabet nor any reading path. Its instruction "Open only the ones needed for the current task" (`:3-4`) is unexecutable, because nothing in the file says which are needed. It also omits `README.md` itself and lists `MULTI_AGENT_SETUP.md` third, above `HLS_NOTES.md`, implying an orchestration file outranks the core streaming reference.
- **Observable-condition test:** both candidate routers fail on every row. `SKILL.md:103-114` is a naked filename list with no conditions at all. The nearest thing to a condition anywhere in the pack is `SKILL.md:61-62` ("For version-sensitive tasks, always read `references/UPSTREAM_WATCHLIST.md` before choosing a pinned version") and `:64-65` (the 5.0.8→5.1.11 trigger) — two conditions for seventeen files, and "version-sensitive" is itself an abstract noun.
- **Dangling paths:** none. All sixteen names in `references/README.md` and all twelve in `SKILL.md` resolve. `MULTI_AGENT_SETUP.md:38` → `assets/config-examples/` resolves. `checklists/MIGRATION_PLAN.md:5-6` and `UPSTREAM_WATCHLIST.md:17-18` resolve. `SKILL.md:336` → `INSTALL.md` resolves. Path hygiene is the one thing that is currently sound and will need re-checking after the rename.
- **Cross-skill reference form:** every companion mention is a bare skill name with no path (`SKILL.md:29,35,39,41,96,97`; `QA_MODES.md:48-49`), and no cross-skill reference anywhere in the pack cites a file inside another skill. The convention "a cross-skill reference always names the owning skill alongside the path" is not violated so much as never exercised — which is itself the symptom of §2's nine unnamed owners.
- **Content not routable at all:** `checklists/` (2 files) and `prompts/` (2 files) are outside `references/` entirely and are reachable only through `SKILL.md:317-328`'s "Skill file map", which describes directories rather than conditions.

Required shape after Phase 2 — one `references/00-topic-map.md`, one pointer line in the body, and rows of the form:

> You are about to ship a change to how the player handles a failed manifest, segment or licence request → read `20-failure-classes-and-retry.md`
> You are seeing `shaka.util.Error` in a console or bug report and need to know whether to retry → read `20-failure-classes-and-retry.md`
> You are about to send a playback event or heartbeat to a backend → read `40-telemetry-contract.md` and request the field names from `alaa-services-contract`
> You are about to put a signed or tokenised URL into a manifest, a share link or a component prop → read `30-media-url-trust.md`

### 10. Scripts, templates and assets audit

### `scripts/scaffold.sh` (675 B, 24 lines)

**What it does:** takes `$1` as a target directory, resolves `SCRIPT_DIR/../assets/templates`, `mkdir -p`s the target, copies exactly two files (`ShakaPlayer.vue`, `useShakaCore.ts`), prints a message telling the human to copy the rest by hand (`:24`).

**Would it run:** yes, under bash, given a writable target. `set -euo pipefail` (`:2`) is correct; the usage guard (`:10-13`) is correct.

**Defects:** (i) **not executable** in this tree — mode `-r--r--r--`, so `./scripts/scaffold.sh` fails and only `bash scripts/scaffold.sh` works; nothing documents that. (ii) **Writes outside a repository** — `:18` `mkdir -p "$TARGET_DIR"` accepts any absolute path with no check that the target is inside a git working tree or even that it is relative. (iii) **Unconditional overwrite** — `:20-21` `cp` with no `-n`, no backup, no diff, no confirmation; running it twice silently destroys local edits to the two most-edited files in the integration. (iv) **Fragile path resolution** — `:16` `cd "${SCRIPT_DIR}/../assets/templates"` aborts the script under `set -e` if the layout moves, with no message. (v) **No `--help`, no `--dry-run`, no `--list`, no self-test**; `:11` prints usage only on the empty-argument path. (vi) **Copies 2 of 9 templates** and delegates the other seven to a human instruction inside a script an agent is running — a hand-off with no receiver. Phase 2 should either make it complete and safe (copy all nine into the layout `ARCHITECTURE.md:86-100` already specifies, refuse to overwrite without `--force`, refuse a target outside the repository root, support `--dry-run`) or retire it, since `ARCHITECTURE.md:86-100` plus the template files already give an agent everything it needs.

### Templates

**`ShakaPlayer.vue` (2,052 B).** Would compile. Correct: `shallowRef` for element refs (`:37-38`), `onBeforeUnmount` teardown (`:72-74`), typed emits (`:29-35`). Defects: **props shape violates the owner** — `type Props` + inline `??` defaults (`:19-28,49-53`) instead of `interface Props` + `withDefaults` (`alaa-vue-typescript-clean-code/references/10-vue-style-contract.md:19-33`); `stats: any` (`:34`). **Failure modes: none handled.** `await core.init(config)` at `:60` is unguarded — an init rejection (unsupported browser, `useShakaCore.ts:65`; manifest 404 via the awaited `load()` at `:120`) becomes an unhandled promise rejection inside `onMounted`, and `emit('ready')` at `:61` never fires, so the parent sees neither ready nor error. The `watch` at `:64-70` calls `core.load` with no `try`/`catch`, so a mid-session source switch that 404s rejects into the void. **Race:** if `src` changes before `init` resolves, `load` runs against a null player and throws `'Shaka has not been initialized yet.'` (`useShakaCore.ts:145`). **Credential leak:** `extraHeaders` as a prop (`:24`). No `flush: 'post'` or unmount guard on the watcher.

**`useShakaCore.ts` (4,254 B).** Would compile only with `noImplicitAny` tolerance; `any` at `:25,29,30,93,99,116` plus `onStats: (stats: any)` at `:13` — six violations of `20-typescript-composition-contract.md:97`, none with the required comment or typed wrapper. Correct: SSR guard (`:38-40`), dynamic import (`:42`), polyfill-before-support-check ordering (`:61-63`), disposer array (`:33,:158-164`), timer cleanup (`:47-57`). Defects: (i) **two lifecycle handles** — `init` returns `{getPlayer, load, play, pause, seek, destroy}` (`:125-140`) while the composable returns `{init, load, destroy}` (`:178-182`), so two callers can destroy the same player; (ii) **error handling is a pass-through** (`:99-104`) with no classification, no severity check, no retry, and `event?.detail ?? event` typed `any`; (iii) **`registerRequestFilter` captures `config.extraHeaders` by closure** (`:93-96`) and mutates `request.headers` — so the token is fixed at init time and can never be refreshed, which directly contradicts `SKILL.md:189-191`'s own rule that filters exist to refresh expired credentials on retry; (iv) **no `player.configure()` for buffering, retries or DRM** — the single `configure` call (`:79-84`) sets one flag; (v) **two polling timers** at 500 ms and 2000 ms (`:106-118`) drive time and stats instead of `timeupdate` and event-driven stats, burning wakeups on every viewer device; (vi) `videoEl.currentTime = seconds` (`:135-136`) for seeking, against the pack's own anti-pattern at `HLS_NOTES.md:56-57`; (vii) `shaka = null` in `destroy` (`:175`) discards the module cache so remount re-imports; (viii) `load()` is called inside `init` (`:120-123`) *before* the returned API exists, so the first load's failure has no caller.

**`PlayerLabPage.vue` (1,476 B).** Would compile. **Leaks a credential**: `:59` `appendLog(\`Player error: ${JSON.stringify(error)}\`)` renders the full Shaka error — including `data[]`, which for a network error contains the failing URI and its query string — into a visible `<pre>` (`:37`). `any` at `:58,62,66`. `onReady()` (`:54`) discards the emitted API so the lab page cannot exercise `destroy`, `seek` or `play`. Hardcoded `https://example.com/master.m3u8` (`:45`) is a correct placeholder. Imports `src/components/player/ShakaPlayer.vue` (`:43`) — a repo-specific alias path in a template `scaffold.sh` does not place there.

**`types/player.ts` (749 B).** Compiles. Clean and useful. Gaps: no player, error, stats or QoE type — the four things `any` is standing in for elsewhere; `headers?: Record<string,string>` on `MediaItem` (`:6`) with no documented lifetime; `manifestUri` (`:5`) with no statement of whether it is a bearer credential.

**`services/AnalyticsTracker.ts` (4,306 B).** Compiles. The most consequential file in the pack, and the one most in conflict with the fleet: invented field and event names (§5c). Bugs: `flush()` zeroes `accumulatedSec` *before* the await (`:76-77`), so a rejected `sendHeartbeat` loses the interval permanently — no retry, no buffer, no `sendBeacon`; the visibility flush (`:155-159`) fires on `hidden` but nothing handles `pagehide`/`unload`, so a closed tab drops up to a full interval; `isBuffering = videoEl.readyState < 3` (`:98`) makes `isPlaying`'s `readyState >= 2` (`:97`) partially unreachable and encodes a buffering definition the prose never states; `tick()` accumulates wall-clock delta (`:82`) and ignores `playbackRate`, so 2× playback under-counts content time by half; no jitter on the interval (`:39,89`). No `project_id`, no session id, no idempotency key.

**`services/AdsManager.ts` (1,840 B).** Compiles. Sound fail-open shape (watchdog `:67-75`, error paths `:61-65`). Defects: five `any` (`:2,5,6,7` + `:35`); the watchdog fires `onError` but never resumes content itself, so the "required fail-safe" of `ADS_VAST_VMAP.md:49-52` depends on a caller that no template provides; `12000` unvalidated (`:70`); event names invented (`:43,53,58`); `onAdEnded` (`:56-59`) does not stop the watchdog.

**`services/PlaybackConductor.ts` (1,583 B).** Compiles. O(n log n) with 2n date parses per second (`:37-46`, tick at `:22`). No `try`/`catch` around `await this.config.load(...)` (`:57`), so one failed manifest rejects inside `setInterval` and — because `activeItemId` was already set at `:51` — the item is never retried; the channel goes dark until the next item. No fallback despite `PLAYLIST.md:12-14` and `CONDUCTOR_SCHEDULE.md:38` both promising one. `new Date(item.startAtIso)` unvalidated → `NaN` comparisons silently select nothing. Trusts client wall-clock (`:35`) with no server-time skew correction, in a feature whose entire premise is wall-clock alignment.

**`services/QuizEngine.ts` (1,839 B).** Compiles. Defects: `onTimeUpdate` is `async` and awaited per cue inside a `for` loop (`:36-42`), while `timeupdate` continues to fire — so two overlapping invocations can fire the same cue twice before `triggered.add` lands, and `lastTimeSec` is written at `:44` after an await, losing intervening progress. Linear scan per tick, no sorted cursor. `videoEl.play().catch(() => {})` (`:68`) silently swallows an autoplay-policy rejection, leaving the video paused with the overlay gone. `triggered` never clears on source change, so a conductor switch carries stale cue state. `enforceOnSeek`, `required` and `allowSkip` exist in the type (`player.ts:22-24`) and are never read — the seek policy `QUIZ_OVERLAY.md:34-39` demands be explicit is unimplemented.

**`services/TimelineMarkers.ts` (656 B).** Compiles. A pure pass-through: four methods that each call one injected callback with no added behaviour (`:13-27`). It has no reason to exist as a class — it is the "abstraction with no invariant" that `alaa-vue-typescript-clean-code`'s SOLID reference warns against. `buildShareUrl` (`:7,26`) is where the presigned-URL question lives and it is delegated to the caller unremarked.

**Do the templates obey `alaa-vue-typescript-clean-code`?** No, on four counts: `any` without the escape's conditions (11 sites), props typing without `withDefaults`, no Pinia store for five stateful services, and teardown split across two handles. And the skill never names the owner, so nothing flags the divergence.

### Checklists and prompts

**`checklists/QA_CHECKLIST.md` (1,720 B).** Current and useful — the strongest checklist in the pack. Duplicates `QA_MODES.md` at `:3-5` and `SKILL.md:127-134` at `:7-16`. Should survive as `references/70-qa-checklist.md` with the mode block removed and, per criterion 1, a proof-level column requested from `alaa-testing-strategy`.

**`checklists/MIGRATION_PLAN.md` (1,084 B).** Current but a third sequence alongside `SKILL.md:301-315` and `MIGRATION…:198-214`. Fold into the migration reference.

**`prompts/AGENT_PROMPT.md` (2,109 B).** Retire. `:22-33` restates `SKILL.md:167-202`; `:36-44` restates `SKILL.md:151-157`; `:32` carries the art-direction wording failure (§7 #8); and a skill whose body is already an execution contract does not need a prompt that re-issues it. Nothing in it is unrecoverable.

**`prompts/MULTI_AGENT_PROMPT.md` (1,802 B).** Retire per 4(b).

**`assets/config-examples/` (2,413 B, 7 files).** Retire per 4(a)/4(b). Note `config.toml:3-4` also ships `[features] multi_agent = true`, a runtime feature flag, into a user's `.codex/config.toml`.

### 11. Rewrite brief for Phase 2

**Target file list.**

*Always loaded:*

| File | Purpose | Budget |
|---|---|---|
| `SKILL.md` frontmatter | Description with trigger, "do not use for", and the one-line companion boundary | 700 B |
| `SKILL.md` §Purpose | The engine/shell/modules thesis, three sentences | 400 B |
| `SKILL.md` §Ownership and boundary | Table naming all fourteen owners from §5(b), each with `/name` and `$name` | 1,400 B |
| `SKILL.md` §When not to use | Trimmed; most of it lives in the description | 400 B |
| `SKILL.md` §Non-negotiable rules | Eight constraint-verb rules, each surviving the wording test | 1,800 B |
| `SKILL.md` §Freshness | The re-read trigger and the pointer to the provenance ledger | 400 B |
| `SKILL.md` §Router pointer | One line to `references/00-topic-map.md` | 120 B |
| `SKILL.md` §Implementation order | Six steps, not eleven | 500 B |
| `SKILL.md` §Output expectations | Deliverables including the operations note criterion 10 requires | 400 B |
| **Sum** | | **6,120 B** |
| **+15%** | | **≈ 7,040 B — hard ceiling 7,200 B** |

That is a **35% reduction** from 11,075 B, achieved entirely by moving duplicated content one hop, not by deleting rules.

*References (numbered lowercase, ~22 files, growing from 33,895 B):*

`00-topic-map.md` (new, router) · `05-provenance-ledger.md` (new — merges `UPSTREAM_WATCHLIST.md` + `OFFICIAL_LINKS.md` with a URL and read-date per claim and a stated re-read interval) · `10-architecture-and-module-seams.md` (from `ARCHITECTURE.md` + `SKILL.md:204-252` + the one surviving orchestration paragraph) · `11-patterns-and-anti-patterns.md` · **`20-failure-classes-and-retry.md` (new)** · **`21-configure-surface-and-defaults.md` (new)** · **`30-media-url-trust-and-drm.md` (new)** · `40-hls-and-live.md` · `41-abr-and-tracks.md` · **`50-telemetry-contract.md` (new, replacing `ANALYTICS_WATCHTIME.md`)** · `55-ads-vast-vmap.md` · `60-quiz-overlay.md` · `61-timeline-markers.md` · `62-playlist-and-conductor.md` (merging `PLAYLIST.md` + `CONDUCTOR_SCHEDULE.md`, both under 900 B) · `70-qa-modes.md` · `71-qa-checklist.md` (from `checklists/`) · `75-test-design.md` (new, thin — binds to `alaa-testing-strategy`) · `80-troubleshooting.md` (already the right shape) · `85-migration-5-0-8-to-5-1-11.md` (split into per-symptom sections with a routing header) · `90-platform-matrix.md` (from `SKILL.md:116-147`).

**What moves where.** `SKILL.md:45-58` → `05-provenance-ledger.md`. `SKILL.md:99-114` + `references/README.md` → `00-topic-map.md` as observable conditions. `SKILL.md:116-147` → `90-platform-matrix.md`. `SKILL.md:204-252` → `10-architecture-and-module-seams.md`. `SKILL.md:271-278` → `70-qa-modes.md`. `SKILL.md:280-299` → one paragraph in `10-…`. `SKILL.md:330-336` → deleted. `checklists/*` → `71-`, `85-`. `prompts/AGENT_PROMPT.md` constraints → already in the body. Duplicate types in `QUIZ_OVERLAY.md:10-21` and `CONDUCTOR_SCHEDULE.md:10-18` → replaced by a path citation to `assets/templates/types/player.ts`.

**Retire to `_to_delete/` (11 files, 8,864 B):** `INSTALL.md`, `prompts/MULTI_AGENT_PROMPT.md`, `prompts/AGENT_PROMPT.md`, `references/MULTI_AGENT_SETUP.md`, `references/README.md`, `assets/config-examples/config.toml`, and the six `assets/config-examples/agents/*.toml`. The `checklists/` and `prompts/` directories disappear as top-level content directories; their surviving content lands under `references/`.

**Templates.** All nine need rewriting, not editing: remove all eleven `any` sites behind a typed Shaka boundary; unify `useShakaCore` on one lifecycle handle; make `registerRequestFilter` read a token *getter* rather than a captured value so refresh-on-retry actually works; wrap `player.configure()` with named, validated defaults; add error classification at the single error site; delete `JSON.stringify(error)` from the lab page; make `AnalyticsTracker` buffer-and-retry with an idempotency key and request its field names from `alaa-services-contract`; give `PlaybackConductor` a precomputed sorted schedule with epoch-ms boundaries, a `try`/`catch` and a fallback; give `QuizEngine` a sorted cursor and a re-entrancy guard; collapse `TimelineMarkers` or give it an invariant to hold. `scaffold.sh` either becomes complete and safe or retires.

**Is a genuinely new capability gained?** **Yes, four**, and they must be declared as the justification for any growth outside the body: (1) a **failure-class taxonomy** over `shaka.util.Error` and `MediaError` bound to `alaa-reliability-sla` doctrine — currently zero coverage; (2) a **wrapped `configure()` surface** with named safe defaults and boundary validation — currently one flag; (3) a **media-URL trust rule** binding `alaa-trust-gateway-auth` and the object-storage skills to manifest, segment, licence and share URLs — currently one CORS sentence; (4) a **telemetry contract** that requests names from `alaa-services-contract` and lands in the WA schema with `project_id` and an idempotency key — currently eleven invented names. Everything else is redistribution, and the body shrinks by 35% while references grow, which is exactly the completeness-bought-with-routing trade the law requires.

### 12. Gap no existing skill can own

**None.**

Three candidates were tested and each falls inside an existing boundary:

- *A browser media-stack error taxonomy.* Looks like a gap because nothing in the fleet names `shaka.util.Error`. It is not one: `alaa-reliability-sla` owns retry, backoff, timeout and degradation *doctrine*, and mapping a specific vendor's error categories onto that doctrine is precisely what a vendor skill is for. `alaa-shaka-player` owns the binding and cites the doctrine.
- *Playback QoE telemetry.* `alaa-services-contract` owns every name and value; `alaa-observability-soc` owns requirement levels; the WA pipeline owns the destination schema and its two counting caveats. The player skill's job is to state which *quantities* playback can produce (rebuffer ratio, startup time, error class, downshift count) and to request names for them — a request, never a definition.
- *Presigned-URL lifetime versus playback-session length.* The sharpest near-miss: a read grant shorter than a lecture cannot serve segment fetches to the end, and nobody currently states the rule. But it decomposes cleanly — the object-storage skills own the grant and its TTL, `alaa-trust-gateway-auth` owns the trust property, `alaa-reliability-sla` owns what happens when a request fails mid-stream — and the *binding* ("the grant's remaining TTL must exceed the longest expected single segment request, and renewal happens inside the networking request filter, not in component state") is a player-side statement this skill can and should own, naming all three.

Proposing a new skill here would create the fourth competing statement of ground that three owners already hold, which is the same failure `alaa-shaka-player` already committed once with its orchestration pack.
