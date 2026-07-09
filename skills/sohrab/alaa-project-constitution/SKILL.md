---
name: alaa-project-constitution
description: Create, update, audit, or bind a repository-root project constitution from constitution-template.md. Use when an agent must generate CONSTITUTION.md from repository evidence, preserve and semantically version an existing constitution, prune irrelevant stack modules, run a two-pass draft and independent refinement, validate project rules and real commands, or align thin AGENTS.md and CLAUDE.md constitution bindings without changing application code.
---

# Alaa Project Constitution

Create or update one evidence-backed project constitution. It becomes binding only when
its status, binding effect, and ratification evidence agree.

## Core contract

- Treat the root template as the structure and policy-authoring contract.
- Treat the existing constitution as prior governance, never as disposable generated text.
- Treat UPDATE as evidence revalidation and focused delta maintenance, never regeneration.
- Treat executable repository truth as authoritative for current behavior.
- Detect the repository's existing constitutional corpus before authoring new policy.
- Prefer a thin charter over existing canonical sources to duplicated policy.
- Treat upstream kit/framework contracts as versioned references, not consumer-local copy.
- Use repository evidence or explicit owner decisions; never invent project facts.
- Keep only relevant conditional modules and remove irrelevant template content.
- Complete two writing passes: evidence-backed draft, then full independent reread/refine.
- Keep exactly one canonical `CONSTITUTION.md`.
- Do not modify application code, dependencies, deployments, shared systems, or Git history.
- Modify AGENTS.md and CLAUDE.md only when the user authorizes binding updates.

## Read-first resources

1. Read the selected root template in full. It is self-contained and outranks bundled
   template copies for the current repository.
2. For evidence discovery and module selection, read
   [references/evidence-and-module-selection.md](references/evidence-and-module-selection.md).
3. When a prior constitution exists or guidance files must be bound, read
   [references/update-versioning-and-binding.md](references/update-versioning-and-binding.md).
4. When the repository already has canonical governance/contracts or consumes an upstream
   kit/framework, read
   [references/constitutional-corpus-and-upstream-contracts.md](references/constitutional-corpus-and-upstream-contracts.md).
5. When rules depend on current vendor/model/framework/security standards, read
   [references/freshness-source-map.md](references/freshness-source-map.md) and verify live
   authoritative sources when tools are available.
6. Use [assets/constitution-template.md](assets/constitution-template.md) only when the
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
6. If no template exists and template creation was not requested, stop with the missing
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

Classify each governing source as `LOCAL_CANONICAL`, `INCORPORATED_BY_REFERENCE`,
`UPSTREAM_CANONICAL`, `GENERATED`, `ADVISORY`, or `HISTORICAL`. Detect overlapping
canonical claims as drift.

Choose the constitution shape before module classification:

- `THIN_CHARTER`: mature canonical sources already own detailed contracts/governance.
  Define authority, durable principles, incorporation, risk, and amendments; link detail.
- `FULL_CHARTER`: the repository lacks an adequate constitutional corpus.

Prefer `THIN_CHARTER` whenever a full document would restate canonical sources.

### 3. Classify modules

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

### 4. Writing pass 1

Create/update the selected output from the template.

- In UPDATE mode, start from the existing constitution, compare evidence since its last
  review, and patch only supported drift. Recheck high-risk surfaces even when a file diff
  is inconclusive. Do not rewrite unchanged policy for style.
- Preserve existing project-specific rules, ratification data, amendment history,
  exceptions, decisions, and TODO IDs unless evidence justifies changing them.
- Fill retained sections with concrete, testable rules and real repository commands.
- In THIN_CHARTER mode, incorporate detailed canonical sources by reference. Do not copy
  wire shapes, route/queue/header/error catalogs, env keys, metric names, thresholds, or
  long operating procedures into the constitution.
- Keep temporary generation-task authorization in the Sync Impact Report; do not convert
  it into durable project policy without repository evidence or an owner decision.
- Separate project facts, binding requirements, proposals, exceptions, and unknowns.
- Remove template-only comments, unused modules, unused validation rows, examples, and
  unexplained placeholders.
- Add the Sync Impact Report as the first HTML comment.
- Do not present completion yet.

### 5. Writing pass 2

Reopen and reread the entire drafted file from disk. Review it as independent work against:

- the prior constitution and amendment history;
- the root template and user request;
- applicable AGENTS.md/CLAUDE.md and canonical docs;
- manifests, code, tests, CI, generated outputs, and safe runtime evidence;
- shape selection, document-role ownership, upstream pins, module inclusion, commands,
  budgets, version/date, TODOs, and exception records.

Fix unsupported specificity, generic filler, contradictions, missing exception conditions,
unverifiable MUST statements, stale modules, duplicate ownership, copied upstream
contracts, and guidance drift.
Record meaningful second-pass changes in the Sync Impact Report.

### 6. Bind agent guidance

Default to reporting binding drift. Edit guidance only when the user asked for binding or
authorized the constitution-generation prompt to do it.

- AGENTS.md: add a short “Project Constitution” rule that requires reading the selected
  constitution before planning/editing/reviewing/runtime changes and states its effect.
- CLAUDE.md: import the selected constitution with `@<relative-path>` where supported,
  then add the same status-aware rule.
- Preserve all existing guidance. Do not duplicate the constitution body.
- Nested guidance may add stricter scoped rules but must not silently weaken the root.
- When an existing README/docs index declares itself the map for main documents, add or
  refresh one constitution pointer. If repository authority forbids that edit, report drift.

Adapter effect must match status:

- `BINDING` -> `Binding effect: BINDING`; adapters call it binding.
- `DRAFT` or `NEEDS_REVIEW` -> `Binding effect: NON_BINDING`; adapters require reading
  for review/context and explicitly say existing ratified sources remain in force.
- `SUPERSEDED` -> `Binding effect: INACTIVE`; adapters point to the successor.

Use exact snippets and conflict rules from the update/binding reference.

### 7. Validate

Run the bundled validator:

```text
python <skill-directory>/scripts/validate_constitution.py --final <path-to-constitution> --check-bindings
```

Also verify:

- the canonical output is `CONSTITUTION.md` and no misspelled active policy remains;
- the Sync Impact Report is an HTML comment at the top;
- the first visible heading is the project constitution title;
- no template-only marker or unexplained `{{PLACEHOLDER}}` remains;
- every TODO has stable ID, reason, owner, and blocking status;
- retained modules and commands have repository evidence;
- the constitution shape and canonical-source non-duplication boundary are explicit;
- upstream contracts are referenced with provenance/version instead of copied locally;
- version/status/dates and amendment history agree;
- AGENTS.md/CLAUDE.md binding status is accurate;
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
- incorporated canonical sources and upstream contract pins;
- included, removed, and unknown modules;
- preserved and changed governance;
- meaningful second-pass refinements;
- unresolved TODOs, proposals, exceptions, and conflicts;
- AGENTS.md/CLAUDE.md binding status;
- files changed and validation performed;
- exact blocker and next action when incomplete.

Do not claim completion until Pass 2 and document validation both succeed.
