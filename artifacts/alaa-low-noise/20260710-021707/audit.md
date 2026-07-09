# Alaa Low Noise Compression Audit

## Scope

- Primary target: `skills/sohrab/alaa-low-noise/SKILL.md`
- Freshness target: `skills/sohrab/alaa-low-noise/references/90-source-map.md`
- Constraint: reduce loaded instructions without removing any distinct responsibility.

## Responsibility preservation

| Existing responsibility | Disposition |
|---|---|
| Complete the real task; reduce output rather than diligence | Preserved as the lead contract. |
| Keep repository files and normal diffs as implementation truth | Preserved. |
| Search first, read bounded excerpts, avoid duplicate reads | Preserved in one rule. |
| Limit commentary to milestones and avoid duplicate harness status | Preserved in one rule. |
| Store useful bulky output in existing repo/workflow artifacts and remove throwaways | Preserved in one rule. |
| Prefer changed paths, stats, scoped diffs, and concise final evidence | Preserved across terminal and final-report rules. |
| Bound shell output and use purpose-built tools | Preserved. |
| Route Windows runtime failures to `alaa-codex-runtime-ops` | Preserved and generalized to the existing failure classes. |
| Keep domain and workflow ownership separate | Preserved in the companion statement and workflow rule. |
| Keep subagent discovery and reporting quiet | Preserved in one rule. |
| Honor explicit raw-output requests | Preserved. |
| Keep progressive-disclosure references discoverable | Preserved with shorter routing text. |

No distinct responsibility was deleted. Repeated trigger, anti-trigger, operating-rule, and self-check wording was consolidated.

## Fresh guidance applied

- OpenAI recommends focused skills, concise trigger descriptions, progressive disclosure, and the smallest prompt that reliably works.
- Current OpenAI model guidance warns that generic brevity instructions can suppress required artifacts; the revised skill prioritizes required evidence before trimming noise.
- Anthropic likewise recommends concise, well-structured skills and clear, direct, positively stated output requirements.

Sources:

- https://developers.openai.com/codex/skills/
- https://developers.openai.com/api/docs/guides/prompt-guidance
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices

## Size result

- Before: 101 lines, 842 words, 5,476 characters.
- After: 37 lines, 447 words, 3,115 characters.
- Reduction: 64 lines (63.4%), 395 words (46.9%), and 2,361 characters (43.1%).

## Validation

- Portable `quick_validate.py`: passed.
- Repository `validate_sohrab_skill_pack.py`: no `alaa-low-noise` error or warning; the pack command still exits non-zero for unrelated existing errors in other skills.
- `agents/openai.yaml`: unchanged and not flagged by the repository validator.
- Responsibility mapping: every original responsibility remains represented above.
- Referenced paths: not flagged by the repository validator.
- Focused `git diff --check`: passed.
