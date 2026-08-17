# hindsight-skills

AI coding agent skills for [Hindsight](https://github.com/vectorize-io/hindsight) — long-term memory for AI agents.

Works with **Claude Code**, **Codex**, **Gemini CLI**, **Cursor**, **Kiro**, and **Factory Droid**.

Most agents forget everything between sessions. Hindsight fixes that. It extracts facts, builds entity graphs, and synthesizes mental models from conversations — so your agent remembers users, learns patterns, and gets better over time.

These skills give your coding agent deep expertise in Hindsight's architecture, so you can go from "I want my agent to remember things" to working code in a single session.

## See it work

```
You:    /hindsight-architect

Claude: [reads README, package.json, scans directory structure, checks for LLM usage]

        I've looked at your project. It's a Next.js + Python customer support
        platform with OpenAI calls in the ticket handler and no existing
        Hindsight config.

        How do you want to approach adding memory?
        > A) Find opportunities for me
          B) I already know what I want
          C) Chat about it

You:    A

Claude: [examines handlers, routes, LLM calls, data flows]

        Here's how memory would work in this application:

        Memory flow: Retain full ticket conversations per-user, recall past
        context before each agent response, and synthesize patterns over time.

        Integration points:
        - api/chat.py:42 — add retain after each conversation turn
        - api/chat.py:18 — add recall before the LLM call
        - lib/agent.ts:31 — inject mental model content into system prompt

        What this enables: The agent remembers every user's history, learns
        each customer's product setup, and detects recurring issues across
        your entire base.

        Is this the direction you want, or would you adjust the scope?

You:    This is right. Let's do all of it.

Claude: Are there any of these considerations for your solution?
        > [ ] Enterprise security
          [ ] Data privacy / PII
          [ ] Regulatory compliance
          [x] None of these

Claude: [presents the three architecture decisions with reasoning]
        1. What to retain — full conversations, upsert on session_id
        2. Tag schema — userId:{id}, customerId:{id}
        3. Mental models — per-user preferences, per-customer usage, cross-customer issues

        Does this design work?

You:    Yes.

Claude: [asks about deployment: Cloud, Local, or Self-hosted]
        [asks about recall optimization: Balanced, Completeness, Cost, or Custom]

Claude: # Memory Implementation Plan: support-agent
        ## Bank Configuration — single bank, per-user tag isolation
        ## Tag Schema — userId:{id}, customerId:{id}
        ## Retain Strategy — full conversation upsert with document_id
        ## Recall Strategy — 10K token budget, any_strict tag matching
        ## Mental Models — 3 models with auto-refresh
        ## Client Setup — Python SDK with environment variables
        ## Implementation Checklist — 9 steps, executable in order

        Ready to implement this plan?
        > A) Yes, implement it
          B) Not now

You:    A

Claude: [installs SDK, adds env vars, wires up retain/recall, creates mental
        models, runs test scenario — committing as it goes]
```

A guided conversation. One implementation plan. Then it builds it for you.

## Skills

| Skill | What it does |
|-------|-------------|
| `/hindsight-architect` | Memory architecture design. Understands your application, identifies where memory adds value, produces a complete implementation plan, and optionally implements it — bank config, tag schema, retain/recall patterns, mental models, and working code. |
| `/hindsight-docs` | Full Hindsight reference. API operations, SDK guides, configuration, deployment, cookbook recipes. Your agent searches these docs to answer specific questions or debug your integration. |
| `/hindsight-upgrade` | Version check and upgrade. Detects when a newer version of hindsight-skills is available and offers to install it. Runs automatically in the background; can also be invoked directly. |

## Install

### Claude Code

```bash
git clone --depth 1 https://github.com/vectorize-io/hindsight-skills.git ~/hindsight-skills
cd ~/hindsight-skills && ./setup
```

Or add to your repo so teammates get it:

```bash
git clone --depth 1 https://github.com/vectorize-io/hindsight-skills.git .claude/skills/hindsight-skills
cd .claude/skills/hindsight-skills && ./setup
```

### Codex, Gemini CLI, or Cursor

These agents all follow the [SKILL.md standard](https://github.com/anthropics/claude-code) and discover skills from `.agents/skills/` or `~/.codex/skills/`.

Install to one repo:

```bash
git clone --depth 1 https://github.com/vectorize-io/hindsight-skills.git .agents/skills/hindsight-skills
cd .agents/skills/hindsight-skills && ./setup --host codex
```

Install globally:

```bash
git clone --depth 1 https://github.com/vectorize-io/hindsight-skills.git ~/hindsight-skills
cd ~/hindsight-skills && ./setup --host codex
```

### Kiro

```bash
git clone --depth 1 https://github.com/vectorize-io/hindsight-skills.git ~/hindsight-skills
cd ~/hindsight-skills && ./setup --host kiro
```

### Factory Droid

```bash
git clone --depth 1 https://github.com/vectorize-io/hindsight-skills.git ~/hindsight-skills
cd ~/hindsight-skills && ./setup --host factory
```

### Auto-detect

If you have multiple agents installed, setup will find and register with all of them:

```bash
git clone --depth 1 https://github.com/vectorize-io/hindsight-skills.git ~/hindsight-skills
cd ~/hindsight-skills && ./setup --host auto
```

### npx

```bash
npx skills add vectorize-io/hindsight-skills --skill hindsight-architect
npx skills add vectorize-io/hindsight-skills --skill hindsight-docs
```

## What the architect actually knows

The architect skill isn't a generic template generator. It has deep knowledge of Hindsight internals and makes real architecture decisions:

**Retain** — Knows that `document_id` enables conversation upsert (same ID = replace + re-extract), that content over 3K chars is auto-chunked, that `context` guides extraction quality, and that you send full conversations, not deltas.

**Recall** — Understands the 4 parallel retrieval strategies (semantic, BM25, graph, temporal), how `tags_match` modes work (`any` includes untagged, `any_strict` excludes), and how to size token budgets for your use case.

**Tags** — Knows tags are for identity scoping (userId, customerId), not content classification. Designs tag schemas that enforce memory isolation and prevent cross-user data leakage.

**Mental models** — Understands that `source_query` determines what to synthesize, `tags` filter whose memories to analyze, and `trigger: { refresh_after_consolidation: true }` enables auto-refresh. Designs retrieval strategies so your application can find the right model at runtime.

**Reflect** — Knows this is an expensive agentic loop (up to 10 iterations), not a routine pre-response call. Recommends recall + direct mental model fetch for the pre-response pattern, and reflect only for complex disposition-influenced reasoning.

**Deployment** — Detects your stack (Python, Node.js, framework) and generates code for your specific setup: Hindsight Cloud, self-hosted, or embedded.

## Troubleshooting

**Skills not showing up?** Re-run setup and restart your agent:
```bash
cd ~/hindsight-skills && ./setup        # or --host codex, --host auto, etc.
```

**Slash commands don't autocomplete?** Skills must be at `~/.claude/skills/{name}/SKILL.md` (Claude Code), `~/.codex/skills/{name}/SKILL.md` (Codex/Gemini/Cursor), `~/.kiro/skills/{name}/SKILL.md` (Kiro), or `~/.factory/skills/{name}/SKILL.md` (Factory Droid). The setup script handles this — run it again if something got out of sync.

**Want to update?** The `/hindsight-upgrade` skill checks automatically. To force-check or upgrade manually:
```bash
cd ~/hindsight-skills && git pull && ./setup --host auto
```

## Requirements

- An AI coding agent: [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Codex](https://openai.com/index/codex/), [Gemini CLI](https://github.com/google-gemini/gemini-cli), [Cursor](https://cursor.com), [Kiro](https://kiro.dev), or [Factory Droid](https://factory.ai)
- Either:
  - A [Hindsight Cloud](https://ui.hindsight.vectorize.io) account — sign up at [ui.hindsight.vectorize.io](https://ui.hindsight.vectorize.io)
  - A [Hindsight](https://github.com/vectorize-io/hindsight) self-hosted instance. 

## License

MIT. Free and open source.

[Documentation](https://hindsight.vectorize.io) · [GitHub](https://github.com/vectorize-io/hindsight) · [Sign up](https://ui.hindsight.vectorize.io)
