# Prompt 3 Publishing

Prompt 3 publishes curated self-improvement outputs from Prompt 1 and Prompt 2 into Basic Memory.

## Inputs

- `D:/Sohrab/Project/raw/processed/_global/lessons.md`
- `D:/Sohrab/Project/raw/processed/_global/work/`
- `D:/Sohrab/Project/raw/processed/_global/_index.md`
- affected project `_lessons.md`, `work/`, `_index.md` only when needed

## Outputs

- `lessons/Global Agent Lessons.md`
- `lessons/Project Lesson Index.md`
- `lessons/project-lessons/<project-key> Lessons.md`
- `patterns/Repeated Work Patterns.md`
- `projects/<project-key>/Learned Patterns.md`

## Do not publish

- raw sessions
- full work files
- draft skill contents
- skill candidates as separate notes
- installed skills

## Curation labels

- `[advisory_lesson]`
- `[promotion_candidate]`
- `[existing_skill_update_candidate]`
- `[project_specific_only]`

Lessons remain advisory unless promoted to AGENTS.md, CLAUDE.md, repo docs, or a skill.
