# Install

This skill can be installed in a project-local or user-local Codex skills
directory.

## Recommended locations

Use one of these paths:

- `.codex/skills/alaa-shaka-player/`
- `~/.codex/skills/alaa-shaka-player/`

If you are working from the shared skills repository, the canonical source path
is:

- `D:/Sohrab/Project/skills/skills/sohrab/alaa-shaka-player/`

## Project-local installation

From the repository root:

1. create `.codex/skills/` if it does not exist
2. copy this entire folder into that directory
3. restart Codex so it re-scans available skills

## Alternative location

Some agent runtimes also support:

- `.agents/skills/alaa-shaka-player/`

## Notes

- Keep the folder structure intact.
- `references/`, `prompts/`, `assets/`, and `scripts/` are all part of the skill.
- If you update the skill, restart the agent session before relying on the new
  metadata or instructions.
