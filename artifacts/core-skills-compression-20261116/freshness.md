# Official-source freshness check

Read-only researcher lane, pages fetched 2026-11-16. Dated evidence. Open items stay open until a later fetch.

STATUS: COMPLETE. Question answered: where official Anthropic/OpenAI pages differ from four alaa-prompting-guide reference files, plus disagreements A, B, C and five missing-guidance items. All pages fetched 2026-11-16. Paths are relative to skills/sohrab/alaa-prompting-guide/references/ unless stated.
Metadata: AGENT alaa-researcher; REQUESTED sonnet/medium; OBSERVED claude-sonnet-5-5, effort unknown. Read-only; no repository content sent out.

## Q1 Per-file differences
Confirmed (one line): 43-fable-5-2.md rows (API ID, Bedrock ID, thinking, effort levels, defaults, v2.1.321, alias gateway caveat, 30-day retention, computer_toolset_20260801, ~30% finish-rule cost, reasoning_extraction) all match models/overview, effort, model-config, migration-guide and the prompting page.

43-fable-5-2.md
- L44, extends (not contradicts): page says the opening line plus recap adds about 20% output tokens, and Anthropic "recommends the model for work where nobody needs frequent updates". Also says to set `display: "updates"` (beta) or the client looks silent. URL: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2 . Verdict: extends.
- L40, extends: ownership sentence raised output tokens "about 70 to 80 percent" and the model "made changes nobody had asked for"; a PR summary "often left out small changes". Same URL. Verdict: extends.
- L42, extends: page has a subagent-cost section ("subagents can account for a large part of what a session costs"; a cost-focused tool description "roughly halved" subagent count). The file delegates this to 06-invocation-and-composition.md. Verdict: extends.
- Page also carries a "treat that answer as done" line warning (reduces self-correction) that the file omits. Verdict: extends.
- L13: the Claude Code default of `medium` matches model-config ("Fable 5.2, Opus 5.5, Sonnet 5.5, and Haiku 5.5 default to `medium`"). Verdict: matches.
- Not fetched in full: model-config was read to char 100000 of 135412; the whats-new page was not fetched.

12-gpt-6.md
- L17, differs (weak): file says official Codex guidance "recommends GPT-6.1 Sol for complex coding and demanding agents". https://learn.chatgpt.com/docs/models says "Astra: For the most demanding work across code, apps, and research" and "GPT-6.1 Sol: Near-Astra performance at lower cost, suited to repeated, long-running work". The "complex coding" wording was not found there. Verdict: differs.
- L17/L51: Luna High and Astra low defaults match the models page ("Luna: High", "Astra: Light (`low` in configuration)"). Terra needs CLI 0.159.0, matches. Verdict: matches.
- L41-44: matches. The latest-model guide says Astra and 6.1 Sol do not support `none`, and Terra, 6.0 Sol and Luna do. https://developers.openai.com/api/docs/guides/latest-model
- Extends: models page says "Ultra: splits work across subagents. Luna supports Max but not Ultra." The file says only that Ultra is subject to delegation authority. https://learn.chatgpt.com/docs/models . Verdict: extends.
- Extends: subagents page says custom agents "can't override `sandbox_mode`, `approval_policy`, `model_provider`, or `mcp_servers`". It also gives the model/effort resolution order (spawn value, then `[agents]` default, then parent). https://learn.chatgpt.com/docs/agent-configuration/subagents . Verdict: extends.
- OPEN: the five per-model API pages (Astra, Sol, 6.1 Sol, Luna, Terra) and the model-selection guide (cited at L69-77, L55) were not fetched. The L77-79 Luna medium/low and Sol/Luna selector cells are unchecked.

60-skill-authoring.md (sections named in dispatch)
- L111-114: the claim that OpenAI favors "small routers, precise triggers, conditional reads" matches the blog https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra. The latest-model guide itself gives no length or lean-prompt guidance. Verdict: matches (blog only).
- L27-35 Progressive disclosure: matches the Claude Code skills page ("every line is a recurring token cost"). It lacks the explicit 500-line cap (see Q5). Verdict: extends.
- L20-25 Description: matches the Claude Code and OpenAI pages (front-load, state when and when not). The "activation side effect" part (item 4) has no support on any listed page. Verdict: open (unsourced, not contradicted).
- L77: the "20 words or fewer" style is stated as a default with an exception, so it is compatible with the Fable page's warning against a hard cap. Verdict: matches.

61-skill-platform-mechanics.md
- L32 frontmatter list: identical to https://code.claude.com/docs/en/skills (19 keys; unrecognized ignored without error). Verdict: matches.
- L45-46: 1,536 cap, `skillListingMaxDescChars`, 1% budget, `skillListingBudgetFraction` and `SLASH_COMMAND_TOOL_CHAR_BUDGET` all match the skills page troubleshooting section. Verdict: matches.
- L24: the skills page also lists an "Additional directory" path (`.claude/skills/` in a `--add-dir` directory). The file omits it. Verdict: extends.
- L44: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices says `description` "Maximum 1,024 characters" and `name` "Maximum 64 characters, lowercase letters, numbers, hyphens; cannot contain reserved words: anthropic, claude". The file ties 1,024 only to plugin validation and omits the name rules. That page is not in the file's Sources. Verdict: extends.
- L47: the 2% / 8,000 chars Codex budget matches https://learn.chatgpt.com/docs/build-skills. The page adds "`skills.max_context_tokens` can raise the budget, up to 10,000 tokens". Verdict: extends.
- L26: `$HOME/.codex/skills` is absent from the official list. The file already says so. Verdict: matches.
- L34 (six keys outside Claude Code): open. The skills page anchors "using-skill-frontmatter-outside-claude-code", which I did not read.

## Q2 Disagreement A (AGENTS.md over `project_doc_max_bytes`)
- Page: "stops adding files once the combined size reaches the limit"; files are concatenated from the root down. So the files added last (nearest the working directory) are the ones left out. Default 32 KiB. The page's own advice is "Raise the limit or split instructions across nested directories". https://learn.chatgpt.com/docs/agent-configuration/agents-md (the old developers.openai.com/codex/guides/agents-md returns a 308 to it).
- 70-agent-instruction-files.md:30: the tail of the merge order is lost and the leaf file is evicted. Verdict: matches.
- 11-codex-runtime-features.md:90: "can silently drop the outermost files". Verdict: differs. Outermost files (root) load first and are the least likely to drop.
- Page gaps: it does not say whether a file crossing the limit is cut mid-file or skipped whole. The "up to 65536" in 11:90 comes from the page's example value, not a stated maximum. Verdict: open.

## Q3 Disagreement B (subagent frontmatter)
Official list (https://code.claude.com/docs/en/sub-agents; "Only `name` and `description` are required"): name, description, tools, disallowedTools, model, permissionMode, maxTurns, autoCompactWindow, skills, mcpServers, hooks, memory, background, omitClaudeMd, effort, isolation, color, initialPrompt, experimental.
- 80-subagent-authoring.md:22: has all 17 optional fields. Verdict: matches.
- 41-claude-code-runtime-features.md:107: it is a "frontmatter of interest" subset and is missing `autoCompactWindow`, `omitClaudeMd`, `experimental`. It has no extra field. Verdict: differs (incomplete).
- The page adds version gates (`autoCompactWindow` v2.1.296+, `omitClaudeMd` v2.1.271+, `experimental.cacheTtl` v2.1.248+), `name` up to 256 characters with no `:`, and a warning when combined subagent descriptions exceed 15,000 tokens. The last 16,540 characters of this page were not read.

## Q4 Disagreement C (Codex skills URL)
- https://learn.chatgpt.com/docs/build-skills resolves (200) and holds the Codex skills documentation (required `name`/`description`, discovery list, 2%/8,000 budget). Verdict: current.
- https://developers.openai.com/codex/skills (used in alaa-low-noise/references/90-source-map.md lines 24 and 59) returns 308 Permanent Redirect to the URL above. It resolves only through the redirect, so alaa-prompting-guide/references/00-source-map.md calling it stale is correct. Verdict: low-noise copy differs (stale); prompting-guide copy matches.

## Q5 Guidance the four files lack (grep in the four files plus 70-agent-instruction-files.md found none of these)
1. SKILL.md length: "Keep `SKILL.md` under 500 lines. Move detailed reference material to separate files." https://code.claude.com/docs/en/skills ; same in https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
2. Reference depth: "Keep references one level deep from `SKILL.md`"; "For reference files longer than 100 lines, include a table of contents". Same best-practices page.
3. Description wording: "Always write in third person" (it is injected into the system prompt). Name rules as in Q1 (64 chars, reserved words). Same best-practices page.
4. Compaction: Claude Code "can keep only the start of an invoked skill, so put the most important instructions near the top of `SKILL.md`"; word guidance to cover the whole task ("Run the tests after every edit"). https://code.claude.com/docs/en/skills (Troubleshooting)
5. OpenAI: "Avoid writing skills as step-by-step itineraries"; remove instructions for behavior the model now does itself; make AGENTS.md references contextual rather than "read several docs before every edit"; revisit "ask first" language. https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra (12-gpt-6.md L21 partly overlaps on fixed ordering).

## Unknowns
Items 12-gpt-6.md L55-79 (OpenAI API model pages, selection guide) and 61 L34 (six-key claim) are open. The two partial reads above (model-config, sub-agents) are noted inline.

## Decision impact
Fix 11-codex-runtime-features.md:90 ("outermost" is wrong), the low-noise Codex skills URL, and the 41:107 field list, then verify the open OpenAI items before the pack rewrite.
