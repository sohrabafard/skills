# Source Map

Ground every version-sensitive claim here. This file decides which source wins and when recall is forbidden; `references/00-topic-map.md` decides which reference answers a question. They are different jobs and neither restates the other.

## Source priority

1. Explicit user instructions for the current task.
2. Current target-host tool schemas and effective configuration for runtime availability.
3. Live official documentation:
   - GPT-6: `https://developers.openai.com/api/docs/guides/latest-model`, `https://developers.openai.com/api/docs/models`
   - Codex and ChatGPT skills, commands, and agent files: `https://learn.chatgpt.com/docs/build-skills`, `https://learn.chatgpt.com/docs/developer-commands`, and the Codex pages under `https://developers.openai.com/codex/` for `use-cases/follow-goals`, `subagents`, `guides/agents-md`, and `config-reference`
   - Claude prompting: `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices` plus the model-specific Opus 5.5, Fable 5.1, Haiku 5.5, and Sonnet 5.5 pages under that path
   - Claude facts and runtime: `https://platform.claude.com/docs/en/models/overview`, `https://platform.claude.com/docs/en/build-with-claude/effort`, and the `https://code.claude.com/docs/en/` pages `model-config`, `skills`, `sub-agents`, `workflows`, `scheduled-tasks`, `permission-modes`, `ultraplan`, `goal`, and `desktop`
4. This skill's dated references and local policy; they do not override current official capability facts. Use `/openai-docs` for current OpenAI guidance. Use community sources only as corroboration after official sources fail to answer.

A redirect is a signal, not a detour: `developers.openai.com/codex/skills` now returns a permanent redirect to the `learn.chatgpt.com` skills page, so a citation to the old path is stale even though it still resolves. When a documented URL redirects across hosts, cite the destination and update the reference that named the origin.

## Freshness triggers

Re-fetch before stating any price, token limit, effort or verbosity name, version, default, flag, feature gate, goal or loop behavior, subagent nesting or concurrency limit, discovery path, or current-best recommendation, and before carrying forward any fact newer than the citing file's freshness stamp.

Three areas are volatile enough that carrying a value forward is a defect rather than a shortcut: harness version gates and hard limits in Claude Code, subagent spawning defaults and depth behavior, and the exact discovery paths for skills and agent definitions in both runtimes. Each has changed in ways that silently broke prompts written against the previous documentation — silently, because nothing errors when a prompt requests a capability the harness no longer exposes under that name.

## Cross-agent packaging contract

- Keep one portable `SKILL.md` package for Codex and Claude Code.
- Keep agent-neutral behavior in `SKILL.md` and `references/`. `agents/openai.yaml` is Codex interface metadata only, and is the one file in a skill that no build rewrites.
- Runtime and model differences change prompt content, not package format. Skill *frontmatter* surfaces are nevertheless asymmetric between the runtimes even where the body is portable; when you are about to add a frontmatter key, read `references/61-skill-platform-mechanics.md` for which runtime documents it.

## Interpretation contract

Carry caveats forward as caveats. Never convert uncertainty into a firm instruction, and never infer that something is false from an absence of evidence — say the documentation does not state it, and use a named placeholder rather than an invented specific.

Where official sources and `/alaa-workflow` disagree with this skill, report the drift, prefer current official and runtime truth for the task in hand, and reconcile the owning file afterwards. Silently choosing a side leaves two sources of truth and no record of which one was followed.

OpenAI active-model/subagent and Claude model, prompting, effort and selection sources were
refreshed 25 September 2026. Other harness mechanics retain their section-specific historical
dates until re-fetched. For lifecycle, use the official model-deprecations page; for API ID
semantics, use model-ids-and-versions. Full system cards were unavailable after bounded retrieval;
release summaries are weaker evidence. Vendor scores and source validation do not prove
local runtime activation, account access or a profile's comparative quality.

Sonnet 5.5 model, migration, prompting, effort and Claude Code selection sources were
refreshed 29 September 2026. Read `references/31-sonnet-5-5.md` for their exact URLs and
provider/API boundaries. Other dated model snapshots retain their own verification dates.

Claude goal, Desktop Code and slash-invocation sources refreshed 4 October 2026:
`https://code.claude.com/docs/en/goal`, `https://code.claude.com/docs/en/desktop`, and
`https://code.claude.com/docs/en/skills`. They establish the condition cap, three evaluator
verdicts, transcript-only evidence, permission/trust/hook boundaries and direct versus
mid-message invocation. They do not establish Chat/Cowork goal support, Unicode counting
semantics, a recent parser/cap change, or acceptance of an unprovided rejected prompt.
Source consistency and static fixtures do not prove live Desktop acceptance.

The Desktop command-composer error quoted in `references/41-claude-code-runtime-features.md`
is user-observed on 4 October 2026; no app version or official documentation of that exact
restriction was supplied. Keep this evidence separate from the official goal limit and
from any inferred release change. The rejected payload and live repaired submission remain unverified.

Haiku 5.5 launch, migration, prompting, effort and Claude Code selection/subagent sources were refreshed 8 October 2026. Read `references/36-haiku-5-5.md` for URLs, workload limits and API-versus-harness controls. Local calibration and installed activation remain unrun.

Sonnet 5.5 launch, overview, prompting, effort and Code selection sources were refreshed 8 October 2026 for the corrected active profiles. Its migration snapshot retains its 29 September date. Retained effort pins remain unrun workload hypotheses; vendor guidance proves no local calibration.

Plan-first selection and runtime-control sources were reverified 8 October 2026: current Claude Sonnet/Opus prompting, model selection, model overview, Code model controls/subagents, Codex models/subagent configuration and current GPT model pages. Read canonical policy source entries and `references/11-codex-runtime-features.md` or `references/41-claude-code-runtime-features.md` for exact surfaces and precedence. These sources inform unrun local admission boundaries; they do not establish model equivalence or live activation.
