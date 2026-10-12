# Execution preflight

Observed 2026-10-12, before source implementation. This record proves readiness facts only.

## Checkout and baseline

The clean `main` checkout was at `9086158d204e8015f7fd0c1e66f83f710bc0dfac`. Relative to planning HEAD `6f6c82facd91779bd3bec8e5c7028b499964091e`, changes were confined to the planning artifact family and unrelated output samples. All SHA-256 entries in `baseline.json` matched current bytes. Those historical measurements are retained unchanged.

## Codex controls

The active collaboration schema permits explicit model and reasoning effort with `fork_turns=none`. The selected Phase 1 test-strategist task requests `gpt-6.1-sol/high`; its spawn was accepted as `/root/acceptance_design`. This establishes accepted dispatch arguments, not serving identity.

Installed test-strategist, implementer-high/low, verifier, reviewer, instruction-reviewer, documenter and researcher definitions match source instruction bodies and omit both executable controls. Source and installed pack version are 5.3.0. No project agent directory override was found. User config main controls are Astra/high; managed parent permissions supersede the file's permission defaults. No settings were changed.

Definitions contain grant-template markers without materialized MCP tables. Therefore inherited MCP isolation is unverified; no configuration-enforced read-only claim is made. Each lane remains restricted to its authorized operations. Installation or materialization into user configuration is outside authority.

Current official [custom-agent precedence](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents) confirms explicit task controls precede parent/global defaults when custom pins are absent. The [selection guide](https://learn.chatgpt.com/docs/model-selection#how-to-think-about-models-and-reasoning-effort) supplies workload starting guidance, not local quality calibration. Both pages were fetched through official OpenAI documentation tools.

## Claude controls

`claude --version` reports 2.1.286. Read-only help exposes `--bare`, `--model`, `--effort`, `--tools`, `--no-session-persistence`, and structured output. User settings inspected for controls show main `opus[1m]`, medium effort, no listed hooks, plugins, available-model allowlist or model/effort override variables. Relevant process override variables are absent. No inference or comparison was run.

Further CLI preflight found `--safe-mode`, which disables user customizations/hooks/MCP while retaining authentication, unlike `--bare`, which requires API credentials. Only credential-presence booleans were inspected; neither API-key nor OAuth-token environment variables were present. `claude auth status` exited 0 and reported logged-in `claude.ai` authentication. No credential or account identity was retained. This permits preparing an allocation-only probe using `--safe-mode --tools "" --no-session-persistence --permission-mode plan --output-format json`, explicit model and effort, and frozen prompt text via stdin; actual model access remains unobserved until invocation.

Proposed Claude allocator task: `claude-sonnet-5-5/high`, balanced, one fixed configuration across two fresh runs. The task judges a finite but interacting routing/control matrix; Haiku fit is not established for this cross-rule judgment. Sonnet is supported by the dated capability registry and this host's effort CLI. No Opus/Fable escalation or worker-model comparison is proposed. The command is not an instruction to change installed definitions or shared settings.

The refreshed [Claude subagent documentation](https://code.claude.com/docs/en/sub-agents#choose-an-effort-level) places per-invocation child effort at 2.1.292 or later. This host therefore does not establish that exact control surface. Session-scoped main-model/effort allocation observation may be possible after a bounded authorized command is designed; that would not establish child-control realization. [Claude selection guidance](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model) retains efficiency-first and capability-first approaches.

## Evidence boundaries

- Source eligibility and contract gates: not yet run on changed source; none has changed.
- Observed allocation: only the Phase 1 task dispatch, not an R1-R15 post-change probe.
- Effective child configuration: explicit Codex arguments accepted; serving identity unknown; Claude child effort unresolved.
- Worker quality, comparative cost and savings: unrun; paid comparisons are not authorized.
- Hindsight: no callable tool exposed; resumed from repository artifacts without recall evidence.
- Local tools: Python 3.14, Git, ripgrep, Codex CLI and Claude CLI were found; no installation occurred.

The workflow validator reported no blocking errors after execution adoption. This was a workflow-artifact check, not a source acceptance gate. One mistyped numeric PowerShell read argument was corrected once; no state changed in that failed read.
