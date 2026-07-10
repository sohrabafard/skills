---
name: alaa-project-constitution
description: Create, update, audit, ratify, or bind a portable repository-root project constitution from constitution-template.md. Use when an agent must generate or maintain CONSTITUTION.md by preserving prior governance, inferring project intent from user and repository evidence, researching current domain risks and missing obligations, asking only essential unresolved owner decisions through bounded recommended choices, pruning irrelevant modules, selecting THIN_CHARTER versus FULL_CHARTER, distinguishing authority from ratification, refining twice, keeping deferred drafts unbound, or aligning thin AGENTS.md and CLAUDE.md bindings after authorized finalization without changing application code.
---

# Alaa Project Constitution

Create or update one evidence-backed project constitution. It becomes binding only when
its status, binding effect, and ratification evidence agree.

## When NOT to use

- Do not use this skill to implement the technical practices it discovers; create or update
  constitutional policy and report non-constitutional follow-ups only.
- Do not use it as a generic architecture, security, performance, frontend, or operations
  review when no constitution lifecycle action is requested.
- Do not invent a missing root template unless the user explicitly asks to install or create
  one; use the bundled asset only through the documented install path.

## Core contract

- Treat the root template as the structure and policy-authoring contract.
- Treat the existing constitution as prior governance, never as disposable generated text.
- Treat the existing constitution as the durable record of prior project decisions and
  context that survived refinement; reuse it before asking the owner to repeat information.
- Never claim to recover prior prompt details that were not retained in the constitution or
  another named source.
- Treat UPDATE as evidence revalidation and focused delta maintenance, never regeneration.
- Treat executable repository truth as authoritative for current behavior.
- Detect the repository's existing constitutional corpus before authoring new policy.
- Prefer a thin charter over existing canonical sources to duplicated policy.
- Treat canonical ownership, active status, approval, and ratification as separate facts.
- Treat ordinary generation/update/binding authorization as distinct from ratification.
- Close every delegated rule over a compact canonical-source list; do not cite unnamed
  “maintained guidance.”
- Keep a thin charter compact enough for reliable cross-agent delivery and avoid repeated
  command catalogs, evidence tables, and module prose.
- Keep the final constitution purely constitutional: durable authority, principles,
  canonical ownership, change control, amendments, exceptions, and one status footer.
- Keep authoring telemetry, evidence ledgers, validation results, module classifications,
  decision-state metadata, and AGENTS.md/CLAUDE.md binding mechanics out of CONSTITUTION.md.
- Treat upstream kit/framework contracts as versioned references, not consumer-local copy.
- Use repository evidence or explicit owner decisions; never invent project facts.
- Infer the project's owned outcomes and material failure modes, then research current
  authoritative domain guidance to discover candidate obligations beyond the user's wording.
- Keep `OBSERVED`, `INHERITED`, `INFERRED_CANDIDATE`, and `OWNER_DECIDED` claims distinct.
- External knowledge may identify a risk or option; it does not prove current behavior or
  authorize a new binding product, security, cost, privacy, or operational commitment.
- Inspect evidence before asking anything. Ask only owner decisions that materially affect
  product promise, scope, authority, security/privacy, cost, data lifecycle, compatibility,
  risk, validation, exceptions, status, or ratification and cannot be resolved from
  repository truth or still-valid prior governance.
- Ask bounded multiple-choice questions with one evidence-backed recommendation and a
  `Decide later` option. Never turn the template into a long interview.
- Treat any `Decide later` answer as deferred. For CREATE or an already non-binding baseline,
  create DRAFT/NON_BINDING with a blocking TODO and no bindings. For an existing BINDING
  baseline, preserve it and report the unresolved delta externally unless the owner explicitly
  approves replacement with a draft.
- Under the canonical launcher, treat completion of all essential decisions without any
  deferral as authorization to finalize and bind; do not ask a redundant approval question.
- Keep only relevant conditional modules and remove irrelevant template content.
- Complete two writing passes: evidence-backed draft, then full independent reread/refine.
- Keep exactly one canonical `CONSTITUTION.md`.
- Do not modify application code, dependencies, deployments, shared systems, or Git history.
- Modify AGENTS.md and CLAUDE.md only when the user authorizes binding updates.

## Read-first resources

1. Read the selected root template in full. It is self-contained and outranks bundled
   template copies for the current repository.
2. For every CREATE/UPDATE/RATIFY operation, read
   [references/interactive-decision-workflow.md](references/interactive-decision-workflow.md).
3. For evidence discovery and module selection, read
   [references/evidence-and-module-selection.md](references/evidence-and-module-selection.md).
4. For every CREATE/UPDATE operation, read
   [references/intent-and-risk-discovery.md](references/intent-and-risk-discovery.md).
5. When a prior constitution exists or guidance files must be bound, read
   [references/update-versioning-and-binding.md](references/update-versioning-and-binding.md).
6. When the repository already has canonical governance/contracts or consumes an upstream
   kit/framework, read
   [references/constitutional-corpus-and-upstream-contracts.md](references/constitutional-corpus-and-upstream-contracts.md).
7. When rules depend on current vendor/model/framework/security standards, read
   [references/freshness-source-map.md](references/freshness-source-map.md) and verify live
   authoritative sources when tools are available.
8. For every CREATE/UPDATE/BIND operation, read
   [references/output-quality-and-context-budget.md](references/output-quality-and-context-budget.md).
9. Use [assets/constitution-template.md](assets/constitution-template.md) only when the
   repository has no template and the user asked to install or create one.

## Path resolution

Honor explicit user paths first. Otherwise resolve in this order:

Default paths:

- template: `./constitution-template.md`
- output: `./CONSTITUTION.md`

Correct misspelled names during authoring. If a repository already contains a misspelled
constitution filename, read it as prior context and correct it to the correctly spelled
canonical file. Do not maintain two active policy files.

## Operating modes

- `CREATE`: no prior constitution; generate the first file.
- `UPDATE`: prior constitution exists; preserve intent and history, then amend.
- `AUDIT`: report correctness, drift, and proposed changes without editing.
- `INSTALL_TEMPLATE`: copy the bundled asset to a requested repository root without
  generating a constitution unless the user also asks for generation.

Infer the mode from the request and repository. If the requested action is ambiguous but
safe and reversible, prefer CREATE/UPDATE. Use AUDIT only for review/report-only requests.

## Required workflow

### 1. Preflight

1. Resolve the repository root and applicable instructions.
2. Inspect worktree status when Git is present and preserve unrelated changes.
3. Read the existing constitution and any misspelled legacy file before the template.
4. Read the complete selected template.
5. Record user-provided scope, owner decisions, desired status, path, and allowed files.
   Do not interpret an ordinary generation/update request as approval or ratification.
6. In UPDATE mode, build a prior-decision map before searching for new policy: preserved
   principles, open TODOs/proposals, exceptions, canonical-source pointers, status/version,
   and any rule whose original rationale is no longer recoverable.
7. If no template exists and template creation was not requested, stop with the missing
   path and offer the bundled asset as the next action.

### 2. Build the evidence ledger

Inventory first, then read high-signal files. Classify evidence by:

- project identity and owned runtime surfaces;
- instructions, architecture, contracts, governance, and generated owners;
- existing constitutional sources and their single-topic ownership boundaries;
- upstream kits/frameworks, version pins, contract locations, and conformance gates;
- manifests/source/routes/data/messaging/integrations;
- tests, validation commands, CI, deployment, and observability;
- security, privacy, identity, tenant, billing, and destructive-data boundaries.

For each material claim, capture source path, what it proves, freshness, and confidence.
Do not read secrets or reproduce private production data.

Canonical does not mean ratified. Record each governing source's ownership classification
and its separately evidenced authority/approval status. Never upgrade “active,” “canonical,”
or “code-enforced” into “ratified” without an explicit decision source.

Classify each governing source as `LOCAL_CANONICAL`, `INCORPORATED_BY_REFERENCE`,
`UPSTREAM_CANONICAL`, `GENERATED`, `ADVISORY`, or `HISTORICAL`. Detect overlapping
canonical claims as drift.

Choose the constitution shape before module classification:

- `THIN_CHARTER`: mature canonical sources already own detailed contracts/governance.
  Define authority, durable principles, incorporation, risk, and amendments; link detail.
- `FULL_CHARTER`: the repository lacks an adequate constitutional corpus.

Prefer `THIN_CHARTER` whenever a full document would restate canonical sources.

### 3. Infer project intent and expand the risk horizon

Use the intent-and-risk discovery reference to synthesize the current request, prior
constitution, repository truth, and current authoritative domain knowledge.

1. Write an internal project-intent statement: owned outcome, users/consumers, critical
   journeys, owned runtime/data surfaces, trust boundaries, and load-bearing qualities.
2. Test each evidenced surface against applicable correctness/concurrency, availability,
   overload, connectivity/offline, data-lifecycle, security/privacy, scale/cost,
   accessibility, operations/change-safety, and domain-specific continuity horizons.
3. Use counterfactual failure scenarios to find missing concerns, not to invent current
   implementation or numeric requirements.
4. Research a material gap with current primary/authoritative sources when available.
   Record provenance, applicability, date, and uncertainty in working state.
5. Disposition every candidate as evidence-required law, owner decision, canonical-source
   delegation, non-constitutional follow-up, not applicable, or unknown.

Do not write generic best-practice catalogs. A candidate becomes binding only through
repository evidence, still-valid prior governance, or an explicit owner decision.

### 4. Classify modules

Use three states:

- `INCLUDE`: positive repository evidence or explicit owner scope.
- `EXCLUDE`: positive evidence the module is outside owned scope.
- `UNKNOWN`: inspection is insufficient; this is not proof of absence.

Remove EXCLUDE modules. For material UNKNOWN modules, add a reasoned TODO rather than
silently deleting or inventing rules. Use the template’s detection table and the evidence
reference; do not classify from filenames alone when executable ownership is unclear.

When `UPSTREAM_KIT_FRAMEWORK_CONTRACTS` applies, record the canonical upstream source,
consumer version pin, inherited/local ownership split, upgrade path, and conformance test.
Do not copy the upstream contract into a locally editable consumer file.

### 5. Resolve essential owner decisions interactively

Build the decision-gap list only after repository reconnaissance. Ask no question whose
answer is already evidenced, inherited from a still-valid prior constitution, safely
omittable, or representable as a non-blocking factual TODO.

- Ask at most three questions per batch. Recompute the decision gaps after each answer batch;
  normally stop after two batches, with one contradiction follow-up allowed. If more
  essential gaps remain, leave a structured DRAFT rather than running an unbounded interview.
- Use the runtime's structured question UI when available. Every question has 2-3 mutually
  exclusive choices, puts the recommended choice first with `(Recommended)`, explains the
  project-specific reason and trade-off, and includes `Decide later` (or the exact user-
  language equivalent). Allow a free-form alternative when the runtime supports it.
- If evidence cannot support a recommendation, recommend `Decide later` rather than
  disguising a generic preference as project truth.
- If the owner selects `Decide later`, stop nonessential questioning, record a stable
  blocking TODO, set owner decision state `DEFERRED`, and follow the draft path.
- Pause for the user's interactive answer. If the runtime resumes without one, treat it as
  DEFERRED; never select the recommendation on the user's behalf.
- If no material gap exists, ask no questions and continue to finalization under the launcher.

Use the exact filter, question shape, budgets, and edge-case handling from the interactive
decision reference.

### 6. Writing pass 1

Create/update the selected output from the template.

- In UPDATE mode, start from the existing constitution, compare evidence since its last
  review, and patch only supported drift. Recheck high-risk surfaces even when a file diff
  is inconclusive. Do not rewrite unchanged policy for style.
- Preserve existing project-specific rules, ratification data, amendment history,
  exceptions, decisions, and TODO IDs unless evidence justifies changing them.
- Fill retained sections with concrete, testable rules and real repository commands.
- Add only intent-derived rules whose disposition is `REQUIRED_BY_EVIDENCE` or explicitly
  `OWNER_DECIDED`; keep research notes and implementation follow-ups outside the constitution.
- In THIN_CHARTER mode, incorporate detailed canonical sources by reference. Do not copy
  wire shapes, route/queue/header/error catalogs, env keys, metric names, thresholds, or
  long operating procedures into the constitution.
- In THIN_CHARTER mode, fold load-bearing module rules into the core principles and compact
  canonical-source list. Do not emit a module inventory or evidence table. Keep exact
  validation commands with their canonical owner. The final validator's thin-charter
  budget is a blocking gate.
- Ensure every delegated phrase such as “follow the maintained guidance” names a registered
  source with an authority status, owner/topic, and freshness rule.
- Keep temporary generation-task authorization and the evidence ledger in internal working
  state and the final response; do not put them in CONSTITUTION.md or convert them into
  durable project policy without repository evidence or an owner decision.
- Separate project facts, binding requirements, proposals, exceptions, and unknowns.
- Remove template-only comments, unused modules, unused validation rows, examples, and
  unexplained placeholders.
- Do not add a Sync Impact Report, metadata table, validation report, module inventory, or
  binding-status section to CONSTITUTION.md.
- Do not present completion yet.

### 7. Writing pass 2

Reopen and reread the entire drafted file from disk. Review it as independent work against:

- the prior constitution and amendment history;
- the project-intent statement, risk-horizon coverage, candidate dispositions, and research
  provenance;
- the root template and user request;
- applicable AGENTS.md/CLAUDE.md and canonical docs;
- manifests, code, tests, CI, generated outputs, and safe runtime evidence;
- shape selection, document-role ownership, upstream pins, module inclusion, commands,
  budgets, version/date, TODOs, and exception records.

Fix unsupported specificity, generic filler, contradictions, missing exception conditions,
unverifiable MUST statements, stale modules, duplicate ownership, copied upstream
contracts, and guidance drift.
Explicitly remove unsupported “ratified/approved” adjectives, repeated commands, repeated
source descriptions, and detail that belongs in a canonical contract, runbook, manifest,
generator, or CI file.
Record meaningful second-pass changes in the final response, not in CONSTITUTION.md.

Then perform a constitutional compression pass: reread the file as permanent context that
will accompany coding tasks, and delete every sentence that does not change a decision,
prevent a concrete failure, name a durable authority boundary, or govern amendments or
exceptions. Remove generation history, terminal/runtime mechanics, tutorial prose, and
facts already owned by a canonical source.

### 8. Finalize and bind conditionally

After Pass 2, use owner decision state as the branch; do not ask another confirmation.

- COMPLETE: the canonical launcher plus completion of every essential question without
  deferral is the explicit finalization decision. Keep launcher/answer evidence in working
  state and the final response, record only the durable normative change in any existing
  amendment record, set BINDING, then align root bindings in the same run.
- DEFERRED on CREATE or an already non-binding baseline: set DRAFT/NON_BINDING, leave
  AGENTS.md and CLAUDE.md unbound to the draft, and provide the exact follow-up prompt.
- DEFERRED while updating an existing BINDING constitution: preserve the binding baseline,
  version, and adapters unchanged unless the owner explicitly approves replacing it with a
  draft. Report the proposed delta and unresolved IDs outside the canonical file.
- A different/noncanonical request does not imply this authorization; require explicit
  finalization intent or leave the result DRAFT.

- AGENTS.md: add a short “Project Constitution” rule that requires reading the selected
  constitution before planning/editing/reviewing/runtime changes and states its effect.
  Put the adapter near the top so default instruction budgets cannot hide it.
- CLAUDE.md: import the selected constitution with `@<relative-path>` where supported,
  near the top, then add the same status-aware rule.
- Preserve all existing guidance. Do not duplicate the constitution body.
- Keep these binding mechanics entirely in AGENTS.md/CLAUDE.md and the final report; never
  document import syntax, adapter placement, or binding status inside CONSTITUTION.md.
- Nested guidance may add stricter scoped rules but must not silently weaken the root.
- When an existing README/docs index declares itself the map for main documents, add or
  refresh one constitution pointer. If repository authority forbids that edit, report drift.

Binding effect must match status:

- `BINDING` -> `Binding effect: BINDING`; adapters call it binding.
- `DRAFT` or `NEEDS_REVIEW` -> `Binding effect: NON_BINDING`; do not create or update a
  constitution adapter/import. Report binding as deferred. Preserve unrelated guidance.
- `SUPERSEDED` -> `Binding effect: INACTIVE`; adapters point to the successor.

Use exact snippets and conflict rules from the update/binding reference.

### 9. Validate

Run the bundled validator:

```text
python <skill-directory>/scripts/validate_constitution.py --final <path-to-constitution> --shape <thin|full> --check-bindings
```

Also verify:

- the canonical output is `CONSTITUTION.md` and no misspelled active policy remains;
- the first visible heading is the project constitution title;
- the document contains no Sync Impact Report, Constitution Metadata table, evidence ledger,
  module inventory, validation matrix/transcript, agent operating tutorial, finalization
  narrative, or AGENTS.md/CLAUDE.md binding section;
- no template-only marker or unexplained `{{PLACEHOLDER}}` remains;
- every TODO has stable ID, reason, owner, and blocking status;
- retained modules and commands have repository evidence;
- every material intent-derived candidate has a recorded disposition and provenance;
- external research is not presented as proof of current behavior or owner approval;
- each evidenced critical journey and high-risk surface received an applicable risk-horizon
  review, with irrelevant horizons explicitly excluded in working state;
- the constitution shape and canonical-source non-duplication boundary are explicit;
- upstream contracts are referenced with provenance/version instead of copied locally;
- the single footer contains version, status, ratification date, last-amended date, and last
  evidence-review date;
- BINDING has explicit ratification evidence in working state, not merely a date or owner
  label; the final constitution keeps only the status/date footer;
- BINDING has complete owner decisions in working evidence and no blocking TODO in the file;
- new policy remains DRAFT/NEEDS_REVIEW unless decisions are COMPLETE under the canonical
  launcher or an authorized owner separately ratified it;
- DRAFT/NEEDS_REVIEW is not imported or activated by AGENTS.md/CLAUDE.md;
- BINDING AGENTS.md/CLAUDE.md adapters are present and accurate;
- adapter placement and portability warnings are reported;
- THIN_CHARTER meets the deterministic 12 KiB/160-line size and non-duplication budget;
- final file is self-contained without this skill.

Do not run broad application tests merely because the constitution names them. Run only
safe document checks unless the user asks for deeper verification.

## Update and version decisions

- Never reset an existing version to `1.0.0`.
- Preserve the original ratification date unless evidence proves it was wrong.
- Classify prior rules as preserved, clarified, added, strengthened, weakened, removed,
  or unresolved; weakening/removal requires explicit rationale and approval.
- MAJOR removes/weakens principles, changes authority/ownership, or permits a previously
  prohibited risk class.
- MINOR adds principles/modules/mandatory gates or materially expands requirements.
- PATCH clarifies without changing required behavior.
- Evidence refresh with no normative change does not require a version bump.
- Unapproved policy changes remain PROPOSALs; they do not become binding through generation.
- When a BINDING baseline exists, an unapproved proposal does not demote or replace it and
  does not change its version; keep the proposal outside the canonical file until resolved.
- DRAFT and NEEDS_REVIEW are always NON_BINDING; BINDING requires ratification evidence;
  SUPERSEDED is INACTIVE.

## Safe autonomy

Allowed without extra approval when in scope:

- read/search repository files and applicable docs;
- inspect Git status/diff;
- create/update the constitution;
- correct one misspelled constitution filename to the canonical filename without keeping
  a duplicate active policy file;
- run the bundled non-destructive document validator;
- minimally bind AGENTS.md/CLAUDE.md when the user authorized binding updates.
- minimally update an existing README/docs index when its own contract requires new main
  documents to be registered;

Require explicit approval for:

- deleting files other than correcting a misspelled constitution filename to the single
  canonical filename;
- changing application code, dependencies, generated products, or project behavior;
- committing, pushing, deploying, posting externally, or mutating shared/production state;
- weakening security/privacy/auth/data/contract/deployment/validation requirements.

## Final response

Lead with the outcome. Include:

- mode, canonical path, status, binding effect, shape, and version;
- detected project type and evidence summary;
- inferred project intent, critical journeys, investigated risk horizons, and source-backed
  candidate dispositions;
- incorporated canonical sources and upstream contract pins;
- included, removed, and unknown modules;
- preserved and changed governance;
- meaningful second-pass refinements;
- unresolved TODOs, proposals, exceptions, and conflicts;
- non-constitutional implementation or research follow-ups that were intentionally excluded;
- questions asked, selected answers, recommendation reasons, and owner decision state;
- automatic FINAL_BOUND or DRAFT_UNBOUND outcome and its evidence;
- AGENTS.md/CLAUDE.md binding status;
- files changed and validation performed;
- authoring telemetry and binding results in this response rather than in CONSTITUTION.md;
- for a draft, the exact unresolved IDs and a paste-ready prompt that finalizes, ratifies,
  and binds it after the owner answers them;
- exact blocker and next action when incomplete.

Do not claim completion until Pass 2 and document validation both succeed.
