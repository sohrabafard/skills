# Go routing ownership and native continuation

The Go skill now delegates provider selection to the canonical routing skill while retaining
Go doctrine and native validation. This is a local source change, not an installed-runtime update.
Baseline: `52e576c31ca654e244a25657f8e8bca9bd3c32fe` on `main`.

## Why the finalized routing skill changed

Removing Go's duplicate provider rules alone would not require reopening routing. Two earlier
user requirements also remained relevant: keep editing without configured Serena, and avoid
unnecessary semantic/graph discovery for dependency upgrades. The baseline had generic provider
absence and partial-read fallbacks, but did not explicitly authorize grounded native editing.
Go separately required Serena diagnostics after every edit, with a fixed gopls fallback.

The routing change therefore makes one missing continuation path explicit and defines the
diagnostic boundary centrally. The dependency row clarifies an existing native-artifact concept;
it is not a claim that native metadata reading was previously impossible. Writing these rules
inside Go would recreate the policy duplication the user explicitly rejected.

This is a real policy change: optional provider diagnostics no longer block adequately grounded
authorized editing or completion after required native proof. Explicitly required uncovered
semantic properties still block their dependent operation or claim. The continuation rule is
generic and affects other stacks too. It does not weaken required repository/task proof.

Before closure, the user explicitly clarified that CodeGraph should be preferred whenever it
can answer adequately, including known files/symbols. That later A9 instruction separately
authorized changing the old known/unknown selection boundary in routing references 10/40.
Reuse now precedes preference: an answered fact is not retrieved again. Required semantics
beyond graph capabilities select a capable semantic owner directly, avoiding a futile graph call.
This later authorization is distinct from the earlier continuation rationale.

Final routing scope is three existing references, 39 inserted lines and ten removed.
Routing SKILL.md and Laravel/Boost-specific rules remain unchanged. The source-lookup preference
and generic continuation apply across eligible stacks. The exact baseline comparison and scope
rationale are in [the reviews](review.md); the latest delta is in [the steering report](steering-report.md).

## Changed scope and expected behavior

- Seven Go files: SKILL.md, agents/openai.yaml, and references 00, 10, 11, 40 and 62.
  Provider sequence/fallback copies became triggered owner pointers. Prose was reorganized into
  procedure, authority, validation and completion; affected Markdown uses the pack's single call
  form and Codex metadata retains its native prompt form.
- Three routing references: 10 owns native continuation and diagnostic eligibility; 40 connects
  stack operations to that owner; 45 specifies native dependency metadata/resolution and effect boundaries.
- Adequate source lookup: prefer eligible CodeGraph for known or unknown source; use Serena for
  its distinct semantic operation or an eligible source fallback. Configured gopls remains the
  Go semantic fallback. No automatic provider setup, blanket health probes or reassurance reads.
- Without Serena: reuse adequate CodeGraph evidence or retrieve bounded current source with
  native tools; inspect contracts/callers/tests as needed; edit locally, inspect the diff and run
  required native gates. Missing reference completeness is not silently treated as proven.
- Dependency upgrades: inspect declared module/workspace metadata and use the authorized native
  resolution/upgrade recipe. Ask CodeGraph or a semantic owner only for a separate missing code,
  compatibility, API-use or impact fact. No universal provider sequence was introduced.

Preserved Go obligations include kit-phase stops, P1-P13, owner precedence, TDD, domain rules,
build/vet/changed-package/full tests, conditional race/vulnerability checks and four completion
answers. See [the rule map](authoring-rule-map.md) for intentional changes D1-D5 versus compression.

## Acceptance and proof

| Contract | Evidence |
|---|---|
| A1: one provider-policy owner | Complete package inspection, ten-file diff, independent review |
| A2: Go obligations preserved | Baseline-to-final rule map and both independent reviews |
| A3: no-provider native editing with limits | Routing 10; static S1-S4/S6-S9 |
| A4: metadata-first dependency route | Routing 10/40/45 and Go procedure; static S5 |
| A5: lean portable common contract | Draft/compression evidence, structure/metadata/link gates |
| A6: explicit policy deltas and sourced authoring | Rule map, full drafts, source notes |
| A7: independent acceptance | [Reviews](review.md), [initial receipt](verification/receipt.json), [fix verification](verification/fix-receipt.json), [steering verification](verification/steering-receipt.json) |
| A8: scope and closure | Plan/checkpoint, final artifact receipt and curation below |
| A9: user-preferred source selection | Canonical references 10/40, S11-S13; all Go files unchanged in this revision |

Independent instruction review and parent correctness review approved the frozen product without
findings. S1-S13 passed static conformance review, including incremental A9 review. Commands, exits and snapshot checks are recorded
in the independent receipt; parent artifact checks are in `final-artifact-receipt.json`.
The writer's refreshed focused fleet-reference receipt is cited without a redundant rerun.
Its initial content checker misclassified CRLF/Git bytes; one checker-only repair and retry passed
30 checks. This is recorded as fail-then-pass, not an initially clean run.

Independent V2 initially failed because two Go citations used a local-looking path for another
skill's resource. The author corrected exactly those two citations; the original failure and
pre-fix manifest remain intact. This fix changed no routing policy. A separate verification
receipt records the retry and affected checks; unaffected index/lifecycle/agent-contract evidence
is reused with an explicit impact assessment.

Frozen product: 36 files, SHA256
`ee706eae796c874bc68c91740fa2203b4c1316b2cc41a8d54fa65aaa68994024`;
[final manifest](steering-final-manifest.txt). Twenty-six files retain unchanged Git content.
Source compatibility is reviewed for both runtimes. Live activation, provider execution,
behavioral compliance and speed/token improvements were not tested. No Go application changed,
so application tests were not run. No installation, reindexing, config mutation or commit occurred.

## Closure and recovery

Lifecycle: IMPLEMENTED and MERGE_CANDIDATE proven on the final identified source snapshot;
RELEASE_CANDIDATE and PUBLISHED not requested. Changes remain uncommitted; retain the working tree
and task artifacts for recovery. Existing staged state was preserved, not reset or committed.

Final curation: no additional memory candidate admitted. The user's single-owner preference is
implemented in its canonical skills; the finalized-skill concern and rationale belong in this
task's review record. The newline-checker incident is local verification history, not fleet policy.
No memory publication or pipeline reopening is required.

Documentation scope is instruction architecture and this maintenance record. API, data,
operations deep dives, Postman and a remaining-task backlog are not applicable. English was
preserved; no localized file was requested. Task reports/plans are exempt atomic evidence;
the history index is the only eligible narrative document for line grading: GREEN, 23 physical
lines, link/line-budget check exit 0. No extra documentation split is needed.

Current authoring sources and limitations: [source notes](source-notes.md).
Resume/closure: [plan](../../docs/_agent_plans/20261009-222708_go-routing-ownership.md) and
[checkpoint](../../docs/agents/20261009-222708_go-routing-ownership-state.md).
Return to [upgrade history](../README.md).
