@AGENTS.md

This file is an import bridge and holds no rules of its own. The line above imports `AGENTS.md`,
which is the single source of truth for working in `skills/sohrab/`; edit that file, not this one.
A rule that is true only under Claude Code, and under no other runtime, is the one thing that may
be added below.

Do not turn this file back into a symlink to `AGENTS.md`, which is what it was until 2026-07-30. A
symlink resolves only where the checkout has symlink support, and git-for-Windows does not grant it
without Developer Mode or Administrator; without it the file materialises as nine bytes of the
literal text `AGENTS.md`, and Claude Code loads those nine bytes in place of the contract with no
error and no warning. `alaa-prompting-guide references/70-agent-instruction-files.md` recommends
the import bridge for a mixed-OS team for exactly this reason, and `scripts/check_skill_index.py`
rule `X7` fails on the nine-byte form.
