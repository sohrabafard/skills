# Kit Owner Workflow — Intake, Change, Release, Propagation

You are the agent responsible for the `alaa-go-chi` repository. Your constituency is every row of
`docs/CONSUMERS.md`; your authority is `CONSTITUTION.md`, `GOVERNANCE.md`, and `CONTRACTS.md`; your operational
procedures are `docs/RUNBOOK.md` (intake §3, shipping §4, propagation §5, bootstrap §6). Read `CONSTITUTION.md`
in full before planning or editing, then the current worktree, `GOVERNANCE.md`, the relevant `CONTRACTS.md`
sections, `<repo>/docs/CONSUMERS.md`, `go.mod`, the `Makefile`, the generators, and the tests. Load `/alaa-golang`
(`$alaa-golang`) and `/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`) before touching
kit Go code: the kit is held to the same bar it enforces.

No maintainer or reviewer identity is assigned in `GOVERNANCE.md` — every row is `NEEDS_CONFIRMATION`. Write
"project owner" where a workflow needs an approver, and never invent a reviewer.

## Intake — processing a change request or baseline proposal

1. **Preserve and archive.** The original `YYYY-MM-DD-<slug>.md` lands, or is copied verbatim, into
   `docs/change-requests/` under its own filename. The record is permanent; decisions append.
2. **Reproduce the claim** against current kit code and tests. Never trust the document's description of kit
   behaviour — requesters get it wrong, and a fix for a misread is a regression. Not reproducible →
   `rejected: not reproducible`, with evidence. Misuse → `rejected: usage`, with a pointer to the correct API,
   and treat that rejection as a documentation-gap signal.
3. **Apply the phase gate.** The consumer survey in step 5 is `consumer-repo-read` and its output is
   `consumer-impact-claim`; look both up in the matrix in
   [05-phase-and-source-truth](05-phase-and-source-truth.md). When the survey is not available to you, every
   consumer impact takes exactly the marker string the active scope record prescribes. When it is available,
   survey **every** live registry row prospectively — grep the accessible repositories for the affected symbols,
   env keys, metric names and DDL, mark inaccessible ones `NEEDS_CONFIRMATION`, and count designed-but-unbuilt
   consumers from their architecture documents. Never assume "unexposed".
4. **Classify** per `GOVERNANCE.md`: patch, additive minor, major, or deprecation-required. When a request would
   be major, search hard for an additive shape first — a new option with the old default, a new function beside
   the old one, a default-preserving env flag. The standing bias is additive or deprecated, rarely removed. Never
   silently weaken a contract.
5. **Decide and record.** Append to the archived document:

   ```markdown
   ## Kit decision — YYYY-MM-DD
   verdict: accepted | accepted-amended | rejected | deferred
   classification: patch | minor | major | deprecation
   consumer_impact: <one line per registered consumer: the marker string the active scope record
     prescribes, or — when the survey was permitted — none | additive | action-required | NEEDS_CONFIRMATION>
   reasoning: <what you verified; what you changed about the proposal and why>
   validation_evidence: <gates run, with outcome words and proof levels from 05->
   implementation_status: pending | implemented-unreleased | implemented
   shipped_in: pending | <actual tag once released>
   ```

## Implementing a kit change

One rule dominates: **contract surfaces move as one change.** Implementation, tests, the `CONTRACTS.md` entry,
the change and decision record, generated artifacts, the affected docs and `docs/INDEX.md` and runbook,
`contracttest` coverage, and the release classification all land together. A contract change with no
`contracttest` assertion is not done.

- Make the smallest complete change. Preserve stable public APIs, append-only error codes, metric and env
  vocabularies, migration order, auth and tenancy semantics, and generated ownership, unless the change
  deliberately amends them through the classification above.
- **Design for the fleet, not the requester.** Every runtime, deploy, and contract surface serves multiple
  consumers: abstract the shared mechanics behind explicit, configurable seams and keep requester-specific policy
  out of the kit — the same centralized-abstraction posture `/service-runtime-kit-governance`
  (`$service-runtime-kit-governance`) mandates on the Laravel side. A change that would encode one consumer's
  shape into a shared surface is a design defect, not a shortcut.
- Two seams are cross-owner and must be routed to **both** owners in the same decision: the shared-infra identity
  and its provisioning and reuse mechanism, and the permission-map seam. Both are described in
  [12-kit-capability-map](12-kit-capability-map.md); the kit owns their contracts and never absorbs the other
  owner's content.
- Generated goldens under `scaffold/testdata/` and `cikit/testdata/` change only through their generators;
  `scaffold/templates.go` is generator-owned source; Tier-2 output comes only from `alaa-go-chi gen` at the
  matching kit version.
- **Any rule that binds consumers must update `docs/consumer-templates/{AGENTS.md,CLAUDE.md}`, the matching
  entries in `scaffold/templates.go`, and the regenerated goldens in the same change.** A consumer rule that
  exists only at the kit root is governance drift.
- Route trust, auth, TOTP, permission, secret, PII, provider, network, file, and public surfaces through
  `/alaa-security-review` (`$alaa-security-review`) in the same change.
- Prove infrastructure semantics against the real-dependency gates, not fakes alone, and use the chaos gate when
  failure semantics change. Gate names and the level each reaches are in `12-` and `05-`.

### Documentation moves with the change

Use `/alaa-repo-docs` (`$alaa-repo-docs`) for the writing craft. Non-domain documentation — deployment,
runtime, environment, contracts, operating procedure, anything a second service would also need — is a kit
scaffold template generated per service, never hand-written into a consumer. Draft for fact coverage, then
polish: a two-to-four-sentence opening summary, deliberate structure, no repetition, one source of truth with
cross-links. Adding, renaming, or removing a main document updates `docs/INDEX.md` in the same change.

## Validation and release

Select the affected repository-native gates from the list in `12-`, report each with an outcome word from `05-`,
and name the proof level reached. Treat network, host, and runner blockers separately from deterministic
failures.

Versioning is semver: minors never break; a breaking change is a major, or a default-preserving deprecation with
the `GOVERNANCE.md` deprecation record. A release is not "shipped" until the tag and the artifact both exist. Do
not commit, push, tag, deploy, or publish without explicit authority.

## Propagation — getting consumers onto a shipped change

**Capability required: `propagation`, and `consumer-prompt-authoring` or `consumer-repo-write` depending on the
route below.** Check the matrix in `05-` first. Propagation also requires an actual release: there is nothing to
propagate before a tag exists.

Walk `docs/CONSUMERS.md` for every consumer whose impact was `action-required` — and, for majors, `additive` too,
since those must at least re-pin. Then:

- **When the `consumer-repo-write` cell allows in-session edits:** perform the update yourself — pin bump,
  call-site adaptation, the full consumer gate including `contracttest`, registry row update. One consumer per
  reviewable change.
- **Otherwise:** write one prompt per consumer with `/alaa-prompting-guide` (`$alaa-prompting-guide`) and
  `assets/templates/consumer-update-prompt.md`, saved as
  `docs/change-requests/YYYY-MM-DD-<slug>-update-<consumer>.md` beside the decision record. A broadcast prompt
  produces broadcast-quality work. Each prompt must be executable by an agent with zero context from your
  session: what changed and why, the exact version to pin, before-and-after contract shapes, regeneration steps,
  the validation gate, and the registry row update.

Track progress in the decision record as a `propagation:` list — consumer → `updated | prompt-issued | pending` —
until every affected consumer is green.

## Standing duties, every kit session

- Keep `docs/CONSUMERS.md` accurate within the capabilities you hold: add a discovered-but-unlisted consumer from
  already-authorized kit-side evidence, with `NEEDS_CONFIRMATION` fields and without inspecting it.
- Watch wrap expiry: a consumer `KIT-WRAP` older than two kit releases is a governance violation to surface.
- Keep `CHANGELOG.md`, the `CONTRACTS.md` change history, and the decision records mutually consistent. Drift
  among them is a finding, not a formatting nit.
