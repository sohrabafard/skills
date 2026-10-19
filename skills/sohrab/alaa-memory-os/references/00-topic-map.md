# Memory topic map

Load only rows whose observable condition holds. This is the sole reference router.

| Read this | When |
|---|---|
| `references/knowledge-shape.md` | Before creating or updating any note. Owns search-before-create, required fields, status and confidence values, observation vocabulary, Extraction and Design mode, and the single do-not-store list. |
| `references/drift-management.md` | Canonical sources disagree, or a memory-only mismatch must be classified as stale. |
| `references/store-local.md` | `ACTIVE_ADAPTER: local` for vault mechanics; the Basic Memory adapter routes only its shared `File-vault serialization` section without activating local operations. |
| `references/store-basic-memory.md` | `ACTIVE_ADAPTER: basic-memory`. Retained while `bm` is installed; the CLI is being retired and its indexed vault is unchanged. |
| `references/store-hindsight.md` | `ACTIVE_ADAPTER: hindsight`; selected query/write mechanics only. |
| `references/checkers-and-hooks.md` | Running a checker, reading its exit code, or installing a hook. |
| `references/skill-boundaries.md` | Unsure whether this skill or another owns a decision. |
| `references/prompt-3-publishing.md` | Publishing curated lessons from the evidence warehouse. |
| `references/hindsight-setup.md` | Hindsight is selected and setup, banks/tags, ingestion, import, doctor/deepen recovery or self-hosted security is being decided; preserves dated product mechanics. |
