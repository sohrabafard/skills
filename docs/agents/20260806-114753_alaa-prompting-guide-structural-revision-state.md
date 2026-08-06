# Workflow Checkpoint - alaa-prompting-guide structural revision

- Plan: `docs/_agent_plans/20260806-114753_alaa-prompting-guide-structural-revision.md`
- Status: complete, pending the integration handshake
- Current phase: Phase 5 complete. All four content phases committed, independent review returned
  CHANGES-REQUESTED with 25 findings, one fix cycle applied, gates re-run clean.
- Last verified result: from the repository root on the final tree,
  `python scripts\validate_sohrab_skill_pack.py` exit 0 (18 body-length warnings, none for this
  skill), `python scripts\check_fleet_references.py` exit 0 with `FINDINGS: none` over 69 skills and
  3676 citations, `python scripts\check_skill_index.py` exit 0 with `FINDINGS: none`. Each checker's
  `--self-test` also exited 0.
- Blockers: none. One decision remains with the user: whether to merge into `main`.
- Touched surfaces: `skills/sohrab/alaa-prompting-guide/` in full; one repaired citation in
  `skills/sohrab/alaa-quasar-app-vite-v3/references/91-agent-authoring-and-dual-runtime.md`;
  `_to_delete/20260806-05-trigger-syntax-folded-into-06-invocation/` holding the retired
  `05-trigger-syntax.md` at its original 2826 bytes.
- Work branch and last commit: `work/prompting-guide-restructure` at `659ec33a`, five commits ahead
  of `main` at `d3fa52cd`.
- Contract files converted on the user's later instruction: `skills/sohrab/AGENTS.md` now requires a
  single `/name` call form, names `default_prompt` in `agents/openai.yaml` as the one bare `$` that
  rule V8 in `scripts/validate_sohrab_skill_pack.py` still requires, and states that an existing
  dual-form pair is legacy to convert in passing rather than a defect to sweep. The root `AGENTS.md`
  carries the same rule by pointer and lost its own two dual-form call sites. Neither `CLAUDE.md` was
  changed: both are import bridges holding no rules, both were verified sigil-free, and both are
  intact rather than the nine-byte form rule X7 fails on.
- Follow-up still not performed: the call sites inside roughly 100 other skills. They are now legacy
  under the contract rather than compliant with it, which is the stated transitional state, and no
  checker reports them. Converting them is its own change with its own review.
- Caveat on one edit: the code-intelligence binding in the root `AGENTS.md` sits inside
  `BEGIN/END ALAA CODE INTELLIGENCE BINDING` markers and no generator for it exists in this
  repository. If an out-of-repo installer owns that block, the same change must be made there or the
  next run restores the dual form.
- Updated: `2026-08-06T16:20:00Z`

Position only. The plan owns scope, phases, and acceptance criteria; the plan's handoff package owns what the work has learned. Record the actual command and what it returned under the last verified result, never a paraphrase.
