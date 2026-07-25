# Output Quality and Context Budget

Read this for every CREATE, UPDATE, RATIFY, or binding operation. It converts common
forward-test failures into acceptance gates for the reusable system.

## Authority truth

- `LOCAL_CANONICAL` identifies topic ownership; it does not prove approval or ratification.
- Record authority/approval status separately for every governing source.
- Do not create or update a constitution adapter/import for DRAFT or NEEDS_REVIEW output.
- Use “ratified” or “approved” only when a named repository source records that decision.
- A BINDING constitution requires a non-placeholder ratification-evidence path or explicit
  recorded owner decision in addition to status, date, and approving role.
- A create/update request, permission to edit bindings, or current code enforcement is not
  ratification. Preserve an existing evidenced BINDING status; otherwise require an explicit
  approval decision or use DRAFT/NEEDS_REVIEW.
- Ask explicit owner questions only after evidence discovery. A `Decide later` answer makes
  owner decision state DEFERRED. It forces DRAFT/NON_BINDING for CREATE or an already
  non-binding baseline; during an existing BINDING update it preserves the binding baseline
  and adapters unchanged unless the owner explicitly approved replacement with a draft.

## Closed delegation

Every durable phrase that delegates behavior to another source must close over the source
registry. Replace vague text such as “follow maintained guidance” with a repository path,
versioned upstream source, or structured TODO. The registry records topic ownership,
authority status, incorporation mode, and freshness/validation.

## THIN_CHARTER compression profile

A thin charter is an authority/index layer, not a compressed copy of the repository docs.

- Keep only scope, precedence, durable principles, source ownership, risk gates, amendment,
  exception, and review rules.
- Fold load-bearing module rules into the core principles; do not emit a module inventory.
- Put exact commands in one location at most. Prefer a canonical Makefile, manifest, CI, or
  runbook reference over repeating command catalogs in module sections and a matrix.
- Keep only constitution-defining evidence; do not restate general project inventories.
- Delete repeated source descriptions, protocol catalogs, thresholds, and procedures.
- The bundled validator rejects a THIN_CHARTER above 12 KiB or 160 physical lines. If the
  policy genuinely needs more detail, move it to a canonical source or select FULL_CHARTER
  with evidence; do not relabel an oversized duplicate as thin.

Reject authoring residue from the final constitution: metadata tables, Sync Impact Reports,
evidence ledgers, module inventories, validation matrices or transcripts, agent operating
tutorials, finalization narratives, and AGENTS.md/CLAUDE.md binding sections. Keep that
information in working state and the final response.

## Instruction delivery audit

- Put the root AGENTS.md adapter within its first 8 KiB and keep the adapter under 1.5 KiB.
- Put `@CONSTITUTION.md` within the first 20 lines of CLAUDE.md and keep its binding section
  under 1.5 KiB.
- Never copy the constitution body into either adapter.
- Report, but do not silently rewrite, pre-existing instruction-budget risks: AGENTS.md
  above Codex's portable default combined budget or CLAUDE.md substantially above current
  official concision guidance.
- A portability warning is not permission to delete existing guidance. Record it as drift
  or a follow-up unless the user authorized broader guidance refactoring.

## Final acceptance

The generated file is acceptable only when it reads as durable law, structural validation
passes, the footer status is truthful, thin-charter limits pass when selected, all delegated
sources are named, DRAFT guidance remains unbound, BINDING has recorded launcher authority
plus complete thin adapters outside the constitution, and portability warnings are reported.
