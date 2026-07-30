# Repository instructions

This repository is a skill pack for coding agents, not an application. It ships Agent Skills that
Claude Code and Codex both load. `CLAUDE.md` beside this file is a one-line import of this file, so
every shared rule is edited here and nowhere else.

## Layout

- `skills/sohrab/` — the first-party pack. `skills/sohrab/AGENTS.md` is the binding contract for any
  change inside it. Read that file before editing a skill, and do not restate its rules here.
- `vendor/` — upstream git subtrees, listed in `vendor/subtrees.json`. Off limits: never edit a file
  under it. `skills/sohrab/AGENTS.md` states that rule in full and owns it.
- `skills/.curated/`, `skills/.system/` — third-party skills. Referenceable, not pack-local.
- `scripts/` — this repository's checkers. `install-skills.md` is authoritative for install paths.
- `artifacts/`, `outputs/`, `test-results/` — scratch. Cluster the products of one piece of work into
  a single directory named for its subject under one of these, creating it if absent.

## Commands

Run from the repository root. Each was executed on 2026-07-30 and observed to work.

- `python scripts\validate_sohrab_skill_pack.py` — per-skill structure: frontmatter, description
  budget, the "When NOT to use" heading, `agents/openai.yaml` shape, and reference-path resolution.
- `python scripts\check_skill_index.py` — both skill indexes in `skills/sohrab/` against the
  directory, in both directions, plus this file and `CLAUDE.md`.
- `python scripts\check_fleet_references.py` — every cross-skill citation in the pack.
- `python scripts\vendor_subtrees.py refresh-docs` — regenerates the marked blocks in the root
  `README.md` and in `install-skills.md` from `vendor/subtrees.json`. Read the vendored-source-roots
  section of `install-skills.md` before running it: the command currently drops four working source
  roots, so its output is a regression until the generator is fixed.

Add `--self-test` to run a checker against its own red fixtures. Every script here shares one
exit-code contract — `0` clean, `1` findings, `2` could not run — and a `2` is a failed gate, never a
pass.

## Rules

- **Nothing is deleted.** Move a retired file to `_to_delete/<YYYYMMDD>-<reason>/` and confirm with
  `ls -la` that it arrived at its original size. `skills/sohrab/AGENTS.md` owns this rule; it is
  named here because `_to_delete/` is a root-level directory and `rm` fails on the Windows mount
  this repository is developed on.
- **Never name a model, an effort level, or a runtime capability.** That question has exactly one
  owner: `alaa-prompting-guide` — `/alaa-prompting-guide` in Claude Code, `$alaa-prompting-guide` in
  Codex — at `skills/sohrab/alaa-prompting-guide/references/50-effort-and-thinking.md`.
- **Write English into every file.** A Persian document is a mirror of an English source, and
  `alaa-repo-docs` owns when one is produced. A reply to the user may be Persian; a file is not.
- **Require an authoritative source for a concrete claim,** and never read a missing result as a
  negative result. Use a named placeholder rather than an invented specific.
- **Never write a path from one machine.** A `D:\...` path is wrong in a committed file; write it
  relative to the repository root.
- **Ask before an action with an effect outside this working tree** — commit, tag, publish, deploy,
  force-push, or credential rotation.
- **No emoji in any artifact.** When a request is ambiguous, contradictory, or unsafe, say so, ask
  the smallest question that resolves it, and stop.
