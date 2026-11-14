---
name: alaa-project-constitution
description: "Repository-root project constitution authoring and governance: CONSTITUTION.md plus its thin AGENTS.md and CLAUDE.md bindings. Use when a user asks to write, create, update, audit, ratify, bind, or enforce a project constitution, or hands over an RFP, a specification, an existing codebase, or reference articles and asks what the project must guarantee. Matches the repository's project archetypes from observable signals and prescribes the obligations an enterprise-grade service of those kinds owes, including obligations the code does not implement yet. Do not use it to implement the practices it prescribes, and do not use it as a standalone review: route security findings to /alaa-security-review, telemetry design to /alaa-observability-soc, and API or event shapes to /alaa-services-contract."
---

# Alaa Project Constitution

Author or amend one project constitution. The constitution states what this service owes. It binds
through the repository's agent instruction files. It stays honest about the difference between what the
repository does today and what a service of this kind must guarantee. The constitution becomes
binding only when its status, its binding effect, and its ratification evidence agree.

Two claim classes run through every phase. Never blend them. A **repository fact** is
never invented: it is inspected or it is unknown. A **domain obligation** is prescribed by the
project's archetypes and the service quality bar. Write it whether or not the code
implements it yet. `references/intent-and-risk-discovery.md` owns that seam. Every rule in this
skill is scoped to one side of it.

## What this skill does not own

This skill decides *that* an obligation is constitutional and *who* owns its detail. It does not
design or implement the detail.

| Not owned here | Owner |
|---|---|
| Threat modelling, vulnerability findings, auth implementation review | `/alaa-security-review` |
| Telemetry schema, dashboards, alert design, SOC workflow | `/alaa-observability-soc` |
| API, event, and DTO contract shapes and their compatibility mechanics | `/alaa-services-contract` |
| The design method that answers a constitutional obligation for one subsystem: bounding it, the seam, contract-before-code, single-writer data ownership, compared candidates, and the design record | `/alaa-system-design` |
| Language-level style, patterns, and refactoring | the per-language clean-code skills, named per stack |
| Model, effort, prompting, and runtime capability questions | `/alaa-prompting-guide` |

Name the owner in the constitution's canonical-source list and route the work. Do not perform it
here. Do not restate its rules.

## When not to use

- Do not use this skill to implement the practices it prescribes. Create or amend constitutional
  policy and report non-constitutional follow-ups.
- Do not use it as a generic architecture, security, performance, frontend, or operations review
  when no constitution lifecycle action was requested.

## Operating modes

- `CREATE` — no prior constitution; generate the first file.
- `UPDATE` — a prior constitution exists; preserve its intent and history, then amend.
- `AUDIT` — report correctness, drift, and proposed changes without editing any file.
- `INSTALL_TEMPLATE` — write the bundled template into a repository the user named. Use it for the
  one case that needs it: the template must be usable in a repository this skill is not installed in.
  Generate a constitution only if the user also asked for that. When a file already exists at the
  destination, never overwrite it unasked. Report its size and which sections of its generation
  contract differ from the bundled asset. Then offer exactly three actions: overwrite it; keep it
  unchanged; or write the bundled asset beside it as `constitution-template.updated.md` for the
  owner to merge. Act only on the answer.

Infer the mode from the request and the repository. Where the requested action is ambiguous but
safe and reversible, prefer `CREATE`/`UPDATE`; use `AUDIT` only for review-or-report-only requests.

## Template resolution and the launcher prompt

The output is always `./CONSTITUTION.md` at the repository root. Keep exactly one canonical,
correctly spelled `CONSTITUTION.md`. `references/update-versioning-and-binding.md` owns filename
correction.

Read the generation contract from `<skill-directory>/assets/constitution-template.md`, the same
skill directory that supplies the validator below. A repository is never required to hold its own
copy. A missing repository-root template never blocks a run. A copy taken at install time is
an unversioned fork that goes stale the next time this skill is upgraded. Reading from the skill
directory removes that failure.

Resolve the template in this order:

1. a template path the user named in this request;
2. `<skill-directory>/assets/constitution-template.md`.

When `./constitution-template.md` also exists in the repository root and the user did not name it,
read it as well and treat it as an owner overlay. Honour the rules it adds that the bundled asset
does not contradict. Where the two contradict, the bundled asset governs this run. Reason: it is
the version this skill's references and validator agree with. List every contradiction in the
final response with the owner's two follow-ups: refresh the root copy through
`INSTALL_TEMPLATE`, or remove it and rely on the bundled asset.

When the user asks which prompt starts a constitution run, or the final response must show them
how to launch one, quote the matching launcher verbatim from `assets/first-message-prompt.md`.

## Non-negotiables

1. The resolved template is the structure and policy-authoring contract. Read it in full before
   writing.
2. An existing constitution is prior governance and the durable record of decisions that survived
   refinement. It is never disposable generated text. Reuse it before asking the owner to repeat
   anything. Never claim to recover prompt details it did not retain.
3. Executable repository truth is authoritative for current behaviour.
4. Run every phase below in order. Phase 3 runs before phase 4. Skipping the archetype match
   produces a constitution that records the repository instead of governing it.
5. Run two writing passes, then the compression pass. Never present completion after pass 1.
6. The final document is law: durable authority, principles, canonical ownership, change control,
   amendments, exceptions, and one status footer. Keep authoring telemetry, evidence ledgers, claim
   labels, module classifications, decision state, and binding mechanics out of it.
7. Ask for explicit approval before you modify application code, dependencies, deployments,
   shared systems, or Git history; `## Safety and authority` lists the other gated actions. Modify `AGENTS.md` and `CLAUDE.md`, or the generator source that produces them, only under
   authorised binding.

## Phase order

1. **Preflight.** Resolve the repository root and applicable instructions. Inspect worktree status
   when Git is present, and preserve unrelated changes. Read any existing or misspelled legacy
   constitution, then the complete resolved template. Record user-provided scope, owner decisions,
   desired status, paths, and allowed files. An ordinary generation request is not approval or
   ratification. In `UPDATE`, build the prior-decision map first.
2. **Evidence ledger.** Inventory, then read the smallest high-signal set that establishes
   ownership, current behaviour, and real validation commands. Read
   `references/evidence-and-module-selection.md`.
3. **Archetype match — mandatory, before module classification.** Read
   `references/project-archetypes.md`. Match every archetype the signals support. Read only the
   matched sections. Carry each of their mandatory obligations forward as an
   `INFERRED_CANDIDATE` prescription. Walk the ten cross-cutting obligations in
   `references/quality-bar.md` over every owned journey and high-risk surface.
4. **Intent, research, and disposition.** Read `references/intent-and-risk-discovery.md`. Write the
   intent statement. Fetch the current value of every obligation's metric from primary sources per
   `references/freshness-source-map.md`. Give every candidate exactly one disposition. Then
   classify modules. Retention follows the matched archetypes, not the presence of existing code.
5. **Charter shape and canonical corpus.** Choose `THIN_CHARTER` or `FULL_CHARTER` and build the
   document-role map. Read `references/constitutional-corpus-and-upstream-contracts.md` when the
   repository already has canonical governance or consumes an upstream kit or framework.
6. **Essential owner decisions.** Read `references/interactive-decision-workflow.md`. Ask only
   material unresolved decisions, within the stated budget, in the stated question shape. Never ask
   whether a matched archetype's obligation applies.
7. **Writing pass 1.** Create or amend the output from the template. In `UPDATE`, patch only
   supported drift and preserve existing rules, ratification data, amendment history, exceptions,
   and TODO IDs. Fill retained sections with concrete testable rules and real repository commands.
   Write every obligation whose disposition is `REQUIRED_BY_ARCHETYPE`, `REQUIRED_BY_EVIDENCE`, or
   `OWNER_DECIDED`. Keep research notes and implementation follow-ups outside the file.
8. **Writing pass 2, then compression.** Reopen the drafted file from disk. Review it as
   independent work against the prior constitution, the intent statement, the matched archetypes
   and their dispositions, the template, the user request, the applicable instruction files, and
   executable truth. Fix unsupported specificity, generic filler, contradictions, unverifiable MUST
   statements, duplicate ownership, copied upstream contracts, and any prescription phrased as an
   observation. Then delete every sentence that does not change a decision, prevent a concrete
   failure, name a durable authority boundary, or govern amendments or exceptions. Record
   meaningful second-pass changes in the final response, never in the file.
9. **Finalize, bind, validate.** Branch on owner decision state without asking again. `COMPLETE`
   under a canonical launcher sets `BINDING` and aligns the root bindings in the same run.
   `DEFERRED` leaves a new or non-binding result `DRAFT` and unbound, or preserves an existing
   `BINDING` baseline unchanged. `references/update-versioning-and-binding.md` owns the version
   decision, the per-status adapter wording, binding a generated `AGENTS.md` or `CLAUDE.md`, and
   the delivery audit. Then run the validator.

## Validation

```text
python3 <skill-directory>/scripts/validate_constitution.py --final <path-to-constitution> --shape <thin|full> --archetypes <matched-ids> --check-bindings
```

Pass every matched archetype to `--archetypes` so its obligations are checked mechanically.
`--list-archetypes` prints the accepted identifiers. Use `--template <path>` to check a template
instead.

The validator gates structure, authoring residue, the footer, TODO shape, size budgets, threshold
provenance, archetype obligation markers, and the bindings. It cannot reach this judgment: whether each
obligation is correct rather than merely present, whether every candidate carries a disposition,
whether any prescription is phrased as an observation, whether retained modules and commands have
evidence, and whether ratification rests on recorded evidence rather than a date label. Verify it
by reading, and report the result.

Run only safe document checks. Do not run broad application test suites merely because the
constitution names them, unless the user asked for deeper verification.

## Stop conditions

Stop successfully only when all of these hold: both writing passes and the validator have run clean;
every matched archetype's obligations carry a disposition; the status and binding effect agree; and
either the bindings were aligned or binding was reported as deferred with the exact follow-up prompt.

Stop and report a partial or blocked state when any of these holds:

- The resolved template cannot be read from the path the user named or from the skill directory.
- The question budget is exhausted with an essential owner decision unresolved.
- An existing `BINDING` baseline would have to be demoted without explicit approval.
- Live verification of a required obligation value is impossible, and the owner must accept a pending value.
- A repository authority forbids an edit the task requires.
- The validator fails for a reason that needs an owner decision rather than a fix.

## Safety and authority

Allowed without extra approval when in scope:

- Reading and searching repository files and applicable documents.
- Inspecting Git status and diff.
- Fetching authoritative external sources.
- Creating or amending the constitution.
- Correcting one misspelled constitution filename to the canonical name, without leaving a duplicate active policy file.
- Running the bundled non-destructive validator.
- Minimally binding `AGENTS.md` and `CLAUDE.md` once the user has authorised binding. Use the
  generator's source and its regeneration command when a tool generates them.
- Minimally updating an existing README or docs index when its own contract requires new main documents to be registered.

Requires explicit approval:

- Writing or overwriting a `constitution-template.md` copy inside a repository.
- Deleting any file other than that one filename correction.
- Changing application code, dependencies, generated products, or project behaviour.
- Committing, pushing, deploying, posting externally, or mutating shared or production state.
- Weakening any security, privacy, auth, data, contract, deployment, or validation requirement.

## Final response

Lead with the outcome. Then include:

- mode, canonical path, status, binding effect, shape, and version;
- matched archetypes with the signals that matched them;
- obligations prescribed, with each fetched value's source and date, and any value left pending;
- the inferred intent, critical journeys, and quality-bar coverage with the count of recorded exclusions;
- incorporated canonical sources and upstream pins;
- included, removed, and unknown modules;
- preserved and changed governance;
- meaningful second-pass refinements;
- unresolved TODOs, proposals, exceptions, and conflicts;
- non-constitutional follow-ups intentionally excluded;
- questions asked with the selected answers and owner decision state;
- the `FINAL_BOUND` or `DRAFT_UNBOUND` outcome and its evidence;
- `AGENTS.md`/`CLAUDE.md` binding status;
- files changed and validation performed;
- for a draft, the unresolved IDs plus the paste-ready prompt that finalizes and binds it.

Do not claim completion until pass 2 and document validation both succeed.
