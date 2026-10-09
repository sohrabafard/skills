# Rule preservation and migration map

Baseline: committed target packages at `52e576c31ca654e244a25657f8e8bca9bd3c32fe`; parent `baseline-manifest.json` records committed-byte hashes. Final `authoring-final-manifest.txt` records actual disk bytes, including retained CRLF in untouched files. Do not compare these aggregate hashes as if newline representation were semantic change.

## Preserved Go obligations

| Baseline rule | Final owner/reachability | Disposition |
|---|---|---|
| Front door, mechanics/platform/gap ownership | Go SKILL role, procedure 4; topic map and reference 05 | Preserved; opening narration compressed |
| Routed owner wins, report both files; repository truth wins | Go SKILL role/procedure 1; unchanged reference 05 and SOURCES | Preserved |
| Read module/directive, imports, tests, route registration and existing instruction files before source change | Go SKILL procedure 1 | Preserved for source changes; dependency-only metadata path is the separately ratified A4 exception |
| Kit active phase from kit repository before code/review; consumer stop; only project owner naming consumer reactivates | Go SKILL procedure 2 | Preserved with decision-record output and all four insufficient-reactivation cases |
| Load clean-code principles before first edit/review; P1-P13; add/override none | Go SKILL procedure 2 | Preserved |
| Route rather than restate; uncovered gap test/decision/report | Go SKILL procedure 4, unchanged reference 05 | Preserved; topic map retains fallback to reference 05 |
| Model, effort, thinking/runtime/invocation ownership | Go SKILL procedure 4; topic map, unchanged reference 05 and SOURCES | Preserved; no new capability claim |
| HTTP framework choice and kit governance | Unchanged references 30/31/46; same topic-map conditions | Preserved with original dates/source caveats |
| Deadline propagation, bounds, request decode, cancellation and drain | Unchanged reference 45, reached by same topic-map conditions | Preserved |
| Layer, repository, composition and use-case doctrine | Unchanged reference 60; reference 62 only changes evidence-surface pointer | Preserved |
| Redis cache failure, TTL, keys, invalidation, stampede, security, signals and six tests | Unchanged reference 61 | Preserved |
| Import direction and native transitive build-graph check | Reference 62 retains `go list -deps` recipe and all prohibitions | Preserved |
| Test-first sequence, inability-to-test stop, test boundaries and mechanics | Unchanged reference 63 | Preserved |
| Package ladder, defaults, conditional packages, kit capability check and dependency vulnerability gate | Reference 40 | Preserved; only provider-routing entry and invocation duplicates change |
| Directive restrictions, modern baseline and freshness | Unchanged reference 70 and all five subordinate references; unchanged SOURCES | Preserved; no domain/version refresh claimed |
| Build, vet, changed-package and full tests in order | Go SKILL validation | Preserved native order; provider-diagnostic removal is intentional delta D2 |
| Race for goroutine/channel/mutex/cache/worker pool/package variable; vulnerability check for module/sum | Go SKILL validation, unchanged reference 63 | Preserved |
| Command outcomes: passed/failed/blocked/skipped/not run, no fabricated execution | Go SKILL validation | Preserved |
| Four completion answers: proof, contract, operation and failure signals | Go SKILL completion | Preserved, including no-contract-change wording and owner shapes |

## Ownership changes and intentional deltas

These changes are not compression. Their authority is the ratified plan's decisions and A1-A6.

| ID | Baseline | Final canonical owner and behavior |
|---|---|---|
| D1 | Go body/metadata/references 00/10/11/40/62 repeat provider selection, priority and direct fallback | Routing reference 10 selects provider/order/eligibility/fallback; reference 40 owns Go fit. Go carries triggered pointers and factual catalogue/provenance only. A priority change in routing needs no Go edit. |
| D2 | Go requires Serena diagnostics after every edit and a fixed direct gopls diagnostic fallback | Routing reference 10: optional diagnostics are supplemental; absence is reported but does not block bounded authorized edits/completion after mandatory native gates. A specific required uncovered semantic property remains blocked. All Go native gates remain mandatory. |
| D3 | Known-symbol fallback describes source as partial read evidence without an explicit native-edit continuation path | Routing reference 10 explicitly permits bounded authorized native edits with adequate fresh evidence, target identity, contracts/callers/tests, preserved changes, diff and mandatory native proof. No complete-reference or binding-safe-rename guarantee follows from source reads alone. |
| D4 | General Go preflight requires source/route discovery for every change, including dependency-only tasks | Go procedure 1 and routing references 10/40/45 use native module/workspace metadata and inspected dependency/version recipes for dependency-only work. Graph/semantic questions need a separately named missing compatibility/API/impact fact. Declared manifests do not prove resolved versions. |
| D5 | Affected Markdown repeats slash/dollar forms and runtime-sigil prose | Pack instruction owns single `/name` call form. Normalize only already-edited Markdown; retain `$name` in Codex default_prompt. No runtime activation claim follows. |

## File disposition

Seven Go files changed: SKILL procedure/validation; metadata pointer; references 00/10/11 routing copies; reference 40 provider catalogue; reference 62 evidence pointer. Three routing references changed: 10 continuation/diagnostics/dependency selection; 40 conditional Go native recipe; 45 dependency effects and mechanics. All other 26 target-package files have unchanged Git content; see the exact list in `authoring-content-receipt.json`.

First complete revised drafts remain under `authoring-drafts/`. Revision 1 restores explicit baseline preflight before compression. Revision 2 distinguishes declared metadata from resolved-version proof. `authoring-compression.json` records 16 wording substitutions and the preflight restoration separately. Revised routing table wording shortens revision 2 without changing its declared/resolved distinction. Invocation normalization and D1-D5 precede compression and have their own review boundary.

No source package added a new reference or changed provider integration configuration. Routing grew to add the native-continuation capability and explicit diagnostic boundary; it is not growth justified by cosmetic wording.
