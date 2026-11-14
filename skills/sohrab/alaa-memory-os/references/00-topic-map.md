# Memory topic map

Load only rows whose observable condition holds. This is the sole reference router.

| Read this | When |
|---|---|
| `references/knowledge-shape.md` | Before creating or updating any note. Owns search-before-create, required fields, status and confidence values, observation vocabulary, Extraction and Design mode, caution shape, and the single do-not-store list. |
| `references/drift-management.md` | Canonical sources disagree, or a memory-only mismatch must be classified as stale. |
| `references/store-local.md` | `ACTIVE_ADAPTER: local` for vault mechanics. |
| `references/store-hindsight.md` | `ACTIVE_ADAPTER: hindsight`, for its query and write mechanics only. |
| `references/checkers-and-hooks.md` | Running a checker, reading its exit code, installing a hook, or about to ship a checker or another pass over a history-growing store. |
| `references/skill-boundaries.md` | Unsure whether this skill or another owns a decision, or about to change the `ACTIVE_ADAPTER` selector, edit an adapter or a store-conditional policy, or edit a neutral knowledge or drift rule. |
| `references/prompt-3-publishing.md` | Publishing curated lessons from the evidence warehouse. |
| `references/hindsight-setup.md` | Hindsight is selected and you are deciding its setup, bank or tag configuration, ingestion, import, doctor or deepen recovery, or self-hosted security. The file preserves dated product mechanics. |
