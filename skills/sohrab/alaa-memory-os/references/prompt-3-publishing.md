# Curated Publishing From The Evidence Warehouse

The self-improvement pipeline has three stages: two produce evidence into a warehouse outside this
repository, and the third publishes curated lessons from that evidence into the memory store. That third
stage is what this file governs.

The stage numbers belong to the owner's external prompt pack, which is not in this repository and which this
skill does not locate. The rules below hold whatever invokes them.

## Every path here is unconfirmed, and must be checked before use

The warehouse is on a volume this skill cannot reach from a normal session, so none of the paths below was
verified when this file was written. **Treat each as a candidate, not a fact.** Resolve `$warehouseRoot` from the task or user, then run the check first:

```powershell
# Exit 0 and a listing means the path is real. Anything else means stop.
Get-ChildItem -LiteralPath (Join-Path $warehouseRoot '_global') -ErrorAction Stop
```

If that fails, do not proceed on the assumption that the layout matches. Ask the user for the current
warehouse root, or for read access to it, and record the answer in a note with `canonical_source_paths` set to
the confirmed path so the next session inherits a checked fact rather than this caveat.

Resolve input paths using the confirmed warehouse layout and platform. These input examples impose no
path syntax or destination on the selected memory adapter.

Candidate inputs, in the order they are read:

- `_global\lessons.md` — cross-project lessons.
- `_global\work\` — per-session work products.
- `_global\_index.md` — the warehouse index, including when the pipeline last ran.
- A specific project's `_lessons.md`, `work\`, and `_index.md`, only when that project is in scope.

The warehouse index carries a session count and a last-run date. Both are claims about disk, not about this
file: read them, do not restate them here, and never plan a publication on a remembered figure.

## What publishing produces

Curated global lessons, project lesson indexes and collections, repeated work patterns and project-scoped
learned patterns. The selected adapter maps these topics to its publication destinations; no vault path is
required by this policy.

Publish only curated lessons and repeated patterns. What must never be published is the single do-not-store
list in `references/knowledge-shape.md`; it is not restated here, and it already covers raw sessions, whole
work files, draft skill contents, skill candidates as separate notes, and installed skills.

## Curation labels are a second axis

These four are not observation labels and do not replace one. An observation carries its type label from the
closed set in `references/knowledge-shape.md`; a published lesson additionally carries exactly one of these,
recording what should happen to it next:

- `[advisory_lesson]` — useful, stays advice, no further action.
- `[promotion_candidate]` — should become a rule somewhere durable.
- `[existing_skill_update_candidate]` — belongs in a skill that already exists.
- `[project_specific_only]` — do not generalise it to the fleet.

## A lesson is advisory until it is promoted

A published lesson carries no authority on its own. It becomes binding only when it is written into the
repository's own authority files, its documentation, or a skill — and `/alaa-project-constitution` owns which files those are.

This is the rule that keeps the warehouse from becoming a second constitution. An agent that treats
`[advisory_lesson]` as a requirement is enforcing something no human approved; an agent that ignores
`[promotion_candidate]` is losing the pipeline's whole output. The label is the difference, so a lesson
published without one is a defect.

## Do not

- Do not publish from the warehouse without first confirming the warehouse path, as above.
- Do not publish a lesson without exactly one curation label.
- Do not create a separate note per skill candidate; record the candidacy on the lesson.
- Do not overwrite a curated note wholesale on re-publication. Update it and keep `last_curated` current
  through the selected adapter so curation age remains verifiable.
