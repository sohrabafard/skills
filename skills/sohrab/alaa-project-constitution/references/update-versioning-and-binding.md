# Update, Versioning, and Agent Binding

Read this reference whenever a constitution already exists, or when `AGENTS.md` and `CLAUDE.md`
must be created or amended.

## Updating an existing constitution

Treat an update as evidence revalidation plus a focused normative delta, not fresh generation.
Read the entire prior file before reading the template. Compare repository changes since the last
evidence review, then explicitly recheck high-risk surfaces whose freshness cannot safely be
inferred from a file diff. Do not rewrite unchanged rules for style. Build an impact map with:

- rules preserved unchanged;
- rules clarified without normative change;
- rules added, strengthened, weakened, or removed;
- project facts that are stale or contradicted by executable truth;
- module additions and removals caused by an actual change in repository ownership or in the
  matched archetype set;
- obligations that a newly matched archetype makes mandatory and the prior version lacks;
- obligation values whose fetched source has changed since the last review;
- TODOs, proposals, and exceptions resolved, added, expired, or still open;
- binding and documentation drift.

Before asking the owner for context, build a prior-decision map from the existing constitution:
durable intent, project-specific rules, open questions, proposals, exceptions, canonical-source
pointers, version and status, and recorded rationale. Reuse that map so the owner does not repeat
information already refined into the previous version. A prior constitution cannot recover
discarded chat context; mark missing provenance as unknown and ask only when it changes the
normative outcome.

Preserve stable rule IDs, TODO IDs, the ratification date, amendment history, and approved
exceptions while they remain valid. Do not erase a prior agent's intentional concern merely
because the new template organises it differently.

When repository truth conflicts with governance, do not silently rewrite policy to match the
implementation. Record the conflict as exactly one of:

- **implementation drift** — behaviour violates a still-valid rule;
- **constitution drift** — policy describes a fact that is no longer true;
- **decision needed** — both states are plausible and owner approval is required.

An archetype obligation that the code does not satisfy is implementation drift, not constitution
drift. Keep the rule and report the gap; weakening the rule to match the code is the failure this
distinction exists to prevent.

## Semantic version decision

Use the normative diff, not the file-size diff.

- `MAJOR`: removes or weakens a principle or gate; changes authority, ownership, or trust; permits
  a previously prohibited class; makes governance incompatible.
- `MINOR`: adds a principle, module, or mandatory gate, or materially expands requirements. A newly
  matched archetype's obligations are `MINOR`.
- `PATCH`: clarifies wording or makes a rule more testable without changing obligations. Refreshing
  a fetched obligation value without changing the obligation is `PATCH`.
- No bump: evidence review or formatting with no normative text change. Update review metadata.

Never reset an existing version to `1.0.0`. Preserve the original ratification date unless evidence
proves it was wrong.

An unapproved PROPOSAL does not change the binding version until ratified. Where no binding
baseline exists, a proposed constitution may use `NEEDS_REVIEW`. Where a BINDING baseline exists,
preserve that canonical file, its version, status, and adapters unchanged, and keep the unapproved
delta in working state, the final response, or an owner-authorised separate proposal artifact until
resolved. Do not demote the only canonical constitution because its proposed amendment lacks
approval.

## Authority and status truth

- Canonical ownership identifies topic ownership; it never proves approval or ratification.
- Use "ratified" or "approved" only where a named repository source records that decision.
- A `BINDING` constitution requires a non-placeholder ratification-evidence path or an explicit
  recorded owner decision, in addition to status, date, and approving role.
- A create/update request, permission to edit bindings, or current code enforcement is not
  ratification. Preserve an existing evidenced `BINDING` status; otherwise require an explicit
  approval decision or use `DRAFT`/`NEEDS_REVIEW`.
- `DRAFT` and `NEEDS_REVIEW` are always `NON_BINDING`; `SUPERSEDED` is `INACTIVE`.

## Filename correction

Canonical names are `constitution-template.md` and `CONSTITUTION.md`.

- Read a misspelled legacy file as prior governance so its rules are not lost.
- Correct the misspelled file to the correctly spelled canonical file after reading it.
- Do not keep the misspelled path as an active alias.
- Update `AGENTS.md` and `CLAUDE.md` links to the corrected canonical filename.

## Thin AGENTS.md binding — status BINDING

Add or update one section and preserve every other instruction:

```md
## Project Constitution

Before planning, editing, reviewing, or changing runtime/deployment behavior, read
`CONSTITUTION.md` in full. Treat it as binding project policy within its scope. If it is
missing, stale, internally inconsistent, or conflicts with applicable higher-precedence
instructions or repository truth, surface the conflict before proceeding. Do not silently
weaken a constitutional gate; use its amendment or exception process.
```

Replace the path with the selected canonical filename. Do not use Markdown import syntax as a
substitute for the explicit read instruction unless the target agent runtime documents it.

Codex loads a root-to-leaf `AGENTS.md` chain. Nested guidance may add stricter scoped rules; it
must not silently weaken the root constitution. Report conflicting nested instructions.

## Thin CLAUDE.md binding — status BINDING

Claude Code supports imports with `@relative/path`. Add the import outside code spans and fenced
blocks, then a short rule:

```md
@CONSTITUTION.md

## Constitution Binding

The imported constitution is binding project policy within its scope. Apply it before
planning, coding, reviewing, or changing runtime/deployment behavior. Surface conflicts and
use the constitution's amendment or exception process instead of silently weakening it.
```

If `CLAUDE.md` already imports `AGENTS.md`, keep that import and add the constitution import or an
explicit binding rule. Avoid cycles such as `AGENTS.md` importing `CLAUDE.md` while `CLAUDE.md`
imports `AGENTS.md`.

## Non-BINDING statuses

**`DRAFT` or `NEEDS_REVIEW`.** Do not add, update, or activate a constitution adapter or import.
Leave unrelated content untouched and report binding as deferred. A pre-existing historical mention
of the constitution elsewhere in `AGENTS.md` is preserved as-is: it is not an adapter, and removing
it would delete guidance the user did not authorise touching.

**`SUPERSEDED`.** Point the runtime at the successor rather than deleting the reader's only
signpost. Replace the `## Project Constitution` section in `AGENTS.md` and the
`## Constitution Binding` section in `CLAUDE.md` with wording that names the file inactive and
names the successor, and remove the `@CONSTITUTION.md` import from `CLAUDE.md`:

```md
## Project Constitution

`CONSTITUTION.md` is SUPERSEDED and inactive historical policy. Read `<successor-path>` instead
and treat that file as binding project policy within its scope.
```

Use the same two sentences under `## Constitution Binding` in `CLAUDE.md`, importing the successor
with `@<successor-path>` if it is itself BINDING. Removing the sections entirely is also valid when
the repository has no successor; state which path you took in the final report.

## Runtime binding references

These URLs are needed to bind a constitution correctly and are not model questions:

- Codex `AGENTS.md` discovery and precedence:
  <https://learn.chatgpt.com/docs/agent-configuration/agents-md>
- Codex skills:
  <https://learn.chatgpt.com/docs/build-skills>
- Claude Code memory and `CLAUDE.md` imports:
  <https://code.claude.com/docs/en/memory>
- Claude Code skills:
  <https://code.claude.com/docs/en/skills>

Durable implications that follow from them: Codex loads applicable `AGENTS.md` automatically, so a
separate constitution needs an explicit read rule there; Claude Code supports importing the
constitution with `@relative/path`; imported content consumes startup context, which is why a thin
charter has a size gate.

## Instruction delivery audit

- Place the root `AGENTS.md` adapter within the first 8 KiB of the file and keep the adapter itself
  under 1.5 KiB, so it stays visible under portable instruction budgets.
- Place `@CONSTITUTION.md` within the first 20 lines of `CLAUDE.md` and keep its binding section
  under 1.5 KiB.
- Never copy the constitution body into either adapter.
- Report, without silently rewriting, pre-existing instruction-budget risks: an `AGENTS.md` above
  the runtime's portable default budget, or a `CLAUDE.md` substantially above current official
  concision guidance. A portability warning is not permission to delete existing guidance; record
  it as drift or a follow-up unless the user authorised broader guidance refactoring.

## Binding edit policy

Binding is a delivery concern, not a constitutional article. Never add an "AGENTS.md and CLAUDE.md
Binding" section, import syntax, adapter placement, or binding audit results to
`CONSTITUTION.md`; those details live in the runtime guidance files and the final report.

- Default review-only tasks to drift reporting.
- During authorised binding work, make the smallest patch that creates an unambiguous link.
- Preserve existing guidance language and imports.
- Report missing roots and nested conflicts.
- Do not claim binding is active until the selected path and the read or import instruction agree.
- Do not bind when the owner decision state is DEFERRED or the finalization outcome is
  DRAFT_UNBOUND.
- When an existing README or docs index declares itself the map for main documents, add or refresh
  one constitution pointer. Where repository authority forbids that edit, report drift.
