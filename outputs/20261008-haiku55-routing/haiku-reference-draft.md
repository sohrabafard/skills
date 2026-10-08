# Claude Haiku 5.5

Use for bounded retrieval, exact-procedure execution and documentation from verified behavior. `assets/claude-model-policy.json` owns assigned role pins, effort, availability and calibration. The launch's fast agentic-work claims support candidate workload selection; they do not prove local quality, latency or equivalence to a GPT model.

## Prompting and work boundaries

For each bounded task, the dispatch must explicitly give one outcome, named inputs or retrieval starts, required evidence/checks, allowed tools and side effects, and explicit completion and failure conditions. Require retrieval before factual conclusions and observed checks before success. Keep narrow lanes complete: report every requested item as evidenced or unresolved, and stop at the acceptance criteria. Return missing scope/evidence, wider architecture judgment or ambiguous failures to the lead rather than inventing facts or expanding the task.

The orchestrator owns role triggers and independent gates. Use its registered bounded explorer, verifier, browser-evidence and documenter profiles; general research, policy design and difficult review need their own registered profiles. Do not make Haiku the lead or a universal fallback from a vendor benchmark. Unknown serving identity remains unknown; missing target access blocks dispatch.

## API and Claude Code controls

Verified 8 October 2026: exact ID `claude-haiku-5-5`; supported efforts `low`, `medium`, `high`, `xhigh`, `max`; default `medium`. Adaptive thinking is supported and manual token budgets are unsupported. The API permits disabled thinking through `high`; `xhigh` and `max` require adaptive. Claude Code prevents disabling thinking for this model and requires version 2.1.293 or later. The fact that an API control is documented does not establish a Claude Code setting.

Treat the assigned medium effort as an unrun workload hypothesis. Compare one factor at a time on representative tasks before claiming quality or savings. Inspect account/provider mapping, override precedence, caps and effective tools before activation through `references/41-claude-code-runtime-features.md`. Historical Haiku 4.5 has no effort parameter; its controls never govern this generation.

## Sources and unrun limits

- [Launch and stated workloads](https://www.anthropic.com/claude-haiku-5-5)
- [Migration and API controls](https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide)
- [Prompting Haiku 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5)
- [Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Code model configuration](https://code.claude.com/docs/en/model-config)
- [Code subagents](https://code.claude.com/docs/en/sub-agents)

No live model calls, installation, account entitlement checks or local calibration ran. Static policy agreement proves source consistency only.
