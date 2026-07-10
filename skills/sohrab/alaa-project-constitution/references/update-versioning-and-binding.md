# Update, Versioning, and Agent Binding

Read this reference whenever a constitution already exists or AGENTS.md/CLAUDE.md must be
created or amended.

## Updating an existing constitution

Treat the update as evidence revalidation plus a focused normative delta, not fresh
generation. Read the entire prior file before reading the template. Compare repository
changes since the last evidence review, then explicitly recheck high-risk surfaces whose
freshness cannot safely be inferred from a file diff. Do not rewrite unchanged rules for
style. Build an impact map with:

- rules preserved unchanged;
- rules clarified without normative change;
- rules added, strengthened, weakened, or removed;
- project facts that are stale or contradicted by executable truth;
- module additions/removals caused by actual repository ownership changes;
- TODOs/proposals/exceptions resolved, added, expired, or still open;
- binding and documentation drift.

Preserve stable rule IDs, TODO IDs, ratification date, amendment history, and approved
exceptions when still valid. Do not erase a prior agent's intentional concern merely because
the new template organizes it differently.

When repository truth conflicts with governance, do not silently rewrite the policy to match
the implementation. Record the conflict as one of:

- implementation drift: behavior violates a still-valid rule;
- constitution drift: policy describes a fact that is no longer true;
- decision needed: both states are plausible and owner approval is required.

## Semantic version decision

Use the normative diff, not the file-size diff.

- `MAJOR`: removes or weakens a principle/gate; changes authority, ownership, or trust;
  permits a previously prohibited class; makes governance incompatible.
- `MINOR`: adds a principle/module/mandatory gate or materially expands requirements.
- `PATCH`: clarifies wording or makes a rule more testable without changing obligations.
- No bump: evidence review or formatting with no normative text change. Update review metadata.

An unapproved PROPOSAL does not change the binding version until ratified. If a binding
change lacks an approver, set status `NEEDS_REVIEW` and explain whether prior rules remain in
force.

## Filename correction

Canonical names are `constitution-template.md` and `CONSTITUTION.md`.

- Read a misspelled legacy file as prior governance so its rules are not lost.
- Correct the misspelled file to the correctly spelled canonical file after reading it.
- Do not keep the misspelled path as an active alias.
- Update AGENTS.md/CLAUDE.md links to the corrected canonical filename.

## Thin AGENTS.md binding

Add or update one section; preserve all other instructions:

```md
## Project Constitution

Before planning, editing, reviewing, or changing runtime/deployment behavior, read
`CONSTITUTION.md` in full. Treat it as binding project policy within its scope. If it is
missing, stale, internally inconsistent, or conflicts with applicable higher-precedence
instructions or repository truth, surface the conflict before proceeding. Do not silently
weaken a constitutional gate; use its amendment or exception process.
```

Replace the path with the selected canonical filename. Do not use Markdown import syntax as
a substitute for the explicit read instruction unless the target agent runtime documents it.

The snippet above is for status `BINDING` only. For a new `DRAFT` or `NEEDS_REVIEW` result,
do not add or update a constitution adapter. Leave unrelated AGENTS.md content untouched and
report binding as deferred. For `SUPERSEDED`, remove the active reference or point it to the
successor and mark the old document inactive.

Codex loads a root-to-leaf AGENTS.md chain. Nested guidance may add stricter scoped rules;
it must not silently weaken the root constitution. Report conflicting nested instructions.
Place the root adapter within the first 8 KiB and keep the adapter itself under 1.5 KiB so
it remains visible under portable instruction budgets.

## Thin CLAUDE.md binding

Claude Code supports imports with `@relative/path`. Add the import outside code spans and
fenced blocks, then a short rule:

```md
@CONSTITUTION.md

## Constitution Binding

The imported constitution is binding project policy within its scope. Apply it before
planning, coding, reviewing, or changing runtime/deployment behavior. Surface conflicts and
use the constitution's amendment or exception process instead of silently weakening it.
```

If CLAUDE.md already imports AGENTS.md, keep that import and add the constitution import or
an explicit binding rule. Avoid cycles such as AGENTS.md importing CLAUDE.md while CLAUDE.md
imports AGENTS.md.

Place `@CONSTITUTION.md` within the first 20 lines and keep the binding section under 1.5 KiB.
Imported content consumes startup context, so a THIN_CHARTER must pass the bundled size gate.

Do not import a new DRAFT or NEEDS_REVIEW constitution. Add `@CONSTITUTION.md` only after
explicit final ratification. Preserve unrelated imports and guidance.

## Existing canonical corpus and upstream contracts

- Prefer a `THIN_CHARTER` when detailed local sources already own contracts/governance.
- Incorporate those sources by reference and assign one canonical owner per topic.
- Do not copy an upstream kit/framework contract into a consumer and adapt it locally.
- Record upstream identity, version pin, inherited/local boundary, contracttest, upgrade,
  deprecation, and change-request path in `UPSTREAM_KIT_FRAMEWORK_CONTRACTS`.
- A generated local snapshot is valid only when upstream owns the generator, provenance,
  read-only semantics, and drift check.

## Binding edit policy

Binding is a delivery concern, not a constitutional article. Never add an
"AGENTS.md and CLAUDE.md Binding" section, import syntax, adapter placement, or binding audit
results to CONSTITUTION.md; keep those details in the runtime guidance files and final report.

- Default review-only tasks to drift reporting.
- During authorized binding work, make the smallest patch that creates an unambiguous link.
- Never copy the full constitution into AGENTS.md or CLAUDE.md.
- Preserve existing guidance language and imports.
- Report missing roots and nested conflicts.
- Report portability/context-budget warnings without deleting unrelated guidance.
- Do not claim binding is active until the selected path and import/read instruction agree.
- Do not bind when owner decision state is DEFERRED or finalization outcome is DRAFT_UNBOUND.
