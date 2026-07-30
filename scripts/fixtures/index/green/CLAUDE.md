# Repository instructions

- `vendor/` is never edited; it holds upstream git subtrees that are periodically re-pulled.
- Nothing is deleted. A retired file moves to `_to_delete/<YYYYMMDD>-<reason>/`.
- The pack contract for work inside the skills is `skills/sohrab/AGENTS.md`.
- Validate with `python skills/scripts/validate_sohrab_skill_pack.py`: 0 clean, 1 findings, 2 could not run.
