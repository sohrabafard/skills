# Alaa Prompting Guide GPT-5.6 Refresh

## Outcome

Updated the skill's Codex target from GPT-5.5 to GPT-5.6 and compacted the package while preserving target routing, trigger syntax, model selection, runtime-feature routing, authority boundaries, freshness checks, validation rules, and Claude coverage.

## Official sources checked live

- `https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6`
- `https://developers.openai.com/api/docs/models`
- `https://developers.openai.com/api/docs/models/gpt-5.6-sol`

## Compression

| Surface | Before | After | Reduction |
|---|---:|---:|---:|
| Whole skill lines | 693 | 621 | 72 (10.39%) |
| Whole skill characters | 72,570 | 54,719 | 17,851 (24.60%) |
| `SKILL.md` lines | 61 | 32 | 29 (47.54%) |
| `SKILL.md` characters | 6,912 | 2,296 | 4,616 (66.78%) |

## Preserved behavior checklist

- Four-model scope and runtime routing remain explicit.
- `$name` for Codex and `/name` for Claude Code remain explicit.
- Model-specific and runtime-specific progressive disclosure remains intact.
- `$alaa-workflow`, `$openai-docs`, and `$alaa-low-noise` companion routing remains intact.
- Agentic permission, parent synthesis, completion, evidence, and blocker rules remain explicit.
- GPT-5.6 guidance covers Sol/Terra/Luna, effort, Pro mode, concise-but-complete output, PTC, multi-agent beta, persisted reasoning, caching, and representative evals.
- The two remaining GPT-5.5 mentions are intentional migration context from the official GPT-5.6 guide.

## Validation

- Targeted `quick_validate.py`: passed (`Skill is valid!`).
- `git diff --check -- skills/sohrab/alaa-prompting-guide`: passed.
- Contract scan for target models, triggers, routing, effort/mode/context, PTC, multi-agent, and required-content preservation: passed.
- Repo-wide `validate_sohrab_skill_pack.py`: the target skill has no errors; the command still exits 1 for unrelated pre-existing errors in other skills.
