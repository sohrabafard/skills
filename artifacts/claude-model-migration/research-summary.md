# Official-source research - 2026-09-25

Researcher: temporary alaa-researcher, requested GPT-6 Sol/medium; observed identity unknown. Lead records this compact evidence from its returned official-source research. No live model calls or account checks ran.

| Model | Exact Anthropic API ID | Documented default effort | Supported efforts | API list input/output USD per million tokens | Vendor latency class |
|---|---|---|---|---|---|
| Opus 5.5 | claude-opus-5-5 | medium | low, medium, high, xhigh, max | 4 / 20 | moderate |
| Fable 5.1 | claude-fable-5-1 | high | low, medium, high, xhigh, max | 10 / 50 | slower |
| Sonnet 5 | claude-sonnet-5 | high | low, medium, high, xhigh, max | 2 / 10 | fast |
| Haiku 4.5 | claude-haiku-4-5-20251001 | not supported | none | 1 / 5 | fastest |

These are vendor specifications, not task measurements or account billing promises. The first three have 1M context/128K output; Haiku has 200K/64K. Opus/Fable adaptive thinking is always on; Sonnet permits disabling adaptive thinking; Haiku uses extended thinking. Source: https://platform.claude.com/docs/en/models/overview .

## Per-model and provider evidence

- https://platform.claude.com/docs/en/models/opus-5-5/overview : released 2026-09-22; Bedrock ID `anthropic.claude-opus-5-5`; other listed platforms expose the API spelling, subject to deployment/access configuration.
- https://platform.claude.com/docs/en/models/fable-5-1/overview : released 2026-09-01; Bedrock ID `anthropic.claude-fable-5-1`; other listed platforms use API spelling. Restricted workload safeguards apply.
- https://platform.claude.com/docs/en/models/sonnet-5/overview : released 2026-06-30; Bedrock ID `anthropic.claude-sonnet-5`; other listed platforms use API spelling.
- https://platform.claude.com/docs/en/models/haiku-4-5/overview : released 2025-10-15. Bedrock Converse `anthropic.claude-haiku-4-5`, InvokeModel `anthropic.claude-haiku-4-5-20251001-v1:0`; Google `claude-haiku-4-5@20251001`; Foundry/Claude Platform on AWS `claude-haiku-4-5`.
- https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions : dateless IDs for 4.6+ are version pins; Claude Code family aliases roll.
- https://platform.claude.com/docs/en/about-claude/model-deprecations : older Fable 5, Opus 5/4.8/4.7/4.6 and Sonnet 4.6/4.5 remain active; Mythos 5.1 is invitation-only, Mythos Preview deprecated. Older 4/4.1 and Sonnet 4/3.7, Haiku 3.5/3 are retired. Do not infer target-account access from these lifecycle labels.

## Runtime evidence

Sources: https://code.claude.com/docs/en/model-config and https://code.claude.com/docs/en/sub-agents .

Opus 5.5 requires CLI 2.1.280; Fable 5.1 requires 2.1.257. Provider aliases differ, including older Sonnet/Opus targets on some clouds and Fable 5 on the apps gateway. Full IDs are accepted in agent frontmatter but remain subject to provider mappings, allowlists and access. Since 2.1.251, subagent model selection orders invocation, frontmatter, environment, parent; older versions prioritize the environment. A force override exists from 2.1.257. Frontmatter effort outranks session effort but not its environment override or caps. Unsupported effort can step down, so a requested pair is not proof of effective selection.

Session /model, startup flag, model environment, settings, then default environment determine session selection; /model may persist settings. Observe session/subagent status and response modelUsage where available. Provider safety fallback and configured overload fallback are separate; neither permits bypassing safeguards. Fable noninteractive usage may bill credits without prompting. No fallback or consent setting is changed here.

## Prompting evidence

- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5 : begin effort calibration at medium; omit generic thinking reminders where effort already controls depth.
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 : outcome-led work, investigation and self-verification with less prompting; avoid carrying the old Fable verification-reminder exception into 5.1. Asynchronous delegation guidance is not a measured pack speedup.
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5 : literal instruction scoping; higher effort can increase tools and verification. No blanket high-effort ceiling is justified.
- https://platform.claude.com/docs/en/build-with-claude/effort : effort affects token use, distinct from supported thinking modes. Sonnet supports xhigh and max; an invalid-pair fixture must not reject xhigh.
- https://platform.claude.com/docs/en/models/sonnet-5/whats-new-sonnet-5 : tokenizer and parameter changes require recounting budgets and fresh compatibility checks.

Independent acceptance gates survive removal of redundant self-check reminders. Local role assignments are uncalibrated policy hypotheses, not vendor rankings.

## Release, migration and system-card checks

Lead additionally inspected https://www.anthropic.com/claude-opus-5-5 and https://www.anthropic.com/claude-fable-and-mythos-5-1 . The Opus release announces Sonnet/Haiku 5.5 as future releases, not currently selectable defaults. Its benchmark footnotes include safeguard fallback and effort differences, so aggregate scores do not prove one serving model or a pack-specific advantage. The Fable release acknowledges approval-bypass failures and limited long-context/multi-agent audit coverage; existing authority gates remain necessary.

The migration guides https://platform.claude.com/docs/en/models/opus-5-5/migration-guide and https://platform.claude.com/docs/en/models/fable-5-1/migration-guide were read. Opus 5.5 rejects forced tool choice, manual/disabled thinking and assistant prefill; it requires preserved thinking blocks in API tool loops. Those API facts are not assumed to be user-controlled Claude Code settings. Fable guidance requires a fresh effort sweep and warns that low effort can skip retrieval.

The official https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md was inspected; it reports 2.1.282 at its head, including fixes to thinking preservation and safety-related switches. Version-specific precedence claims above remain grounded in the current runtime documentation, not inferred from a failed text search of the changelog.

Full system cards were located through https://www.anthropic.com/system-cards but could not be fetched. Initial release-page links returned Internal Error; one different retrieval through the system-card index returned HTTP 400 content-length limits: 17,795,106 bytes for https://www.anthropic.com/claude-opus-5-5-system-card and 16,397,488 bytes for https://www.anthropic.com/claude-fable-5-1-mythos-5-1-system-card . No further retries; full-card conclusions are unavailable. The release-page summaries above are explicitly weaker evidence.

## Initial local observations

Lead ran `claude --version`: 2.1.221. Whitelisted user-settings projection: `model=opus[1m]`, `effortLevel=medium`, no settings env object; listed model/provider override environment variables absent in this Codex process. No account eligibility or serving identity observed. Installed Codex 3.6.0 differs from source 4.0.0; user explicitly authorized temporary GPT-6 agents for this task, without installation. Effective role restrictions are behavioral; runtime enforcement is unknown.

The user's subsequent CLI upgrade was independently observed as 2.1.282. [Runtime update](runtime-update.md) supersedes only the initial CLI-version limitation and records the separate Desktop evidence boundary. It does not prove model activation or account access.

## Claude Code alias matrix supplement

The independent researcher rechecked [model configuration](https://code.claude.com/docs/en/model-config) on 2026-09-25. These are documented mappings, not observed serving identities; deployments, account eligibility, overrides, allowlists and fallback still apply.

| Provider | `opus` | `sonnet` | `fable` |
|---|---|---|---|
| Anthropic API | Opus 5.5 | Sonnet 5 | Fable 5.1 |
| Claude Platform on AWS | Opus 5.5 | Sonnet 4.6 | Fable 5.1 |
| Amazon Bedrock | Opus 5.5 | Sonnet 4.5 | Fable 5.1 |
| Google Cloud Agent Platform | Opus 5.5 | Sonnet 4.5 | Fable 5.1 |
| Microsoft Foundry | Opus 4.6 | Sonnet 4.5 | Fable 5.1 |
| Claude apps gateway | Not specified | Not specified | Fable 5 |

`best` chooses available Fable, otherwise Opus; apps gateway documents Fable 5. `default` is the account default. `haiku` means latest fast Haiku, without an exact target on the configuration page. `opusplan` switches Opus planning to Sonnet execution; `[1m]` selects applicable context. `ANTHROPIC_DEFAULT_*_MODEL` overrides family targets. Opus 5.5 needs CLI 2.1.280, Fable 5.1 needs 2.1.257, Sonnet 5 needs 2.1.197. Earlier aliases differ. Full-ID frontmatter support and version-pin semantics are sourced above. Local CLI 2.1.282 clears these minima; account and Desktop activation remain unknown.
