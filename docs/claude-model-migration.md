# Claude model migration (2026-09-25)

This dated migration report records the source change on branch `codex/gpt6-agent-migration`, based on `4fdd8b709a745314a0575c25c06d0a390847bde6`. It is a historical snapshot, not a second live policy. The canonical current rules and machine-checked model/profile data live in [`alaa-prompting-guide`](../skills/sohrab/alaa-prompting-guide/SKILL.md) and [`claude-model-policy.json`](../skills/sohrab/alaa-prompting-guide/assets/claude-model-policy.json); the [dated plan](./_agent_plans/20260925-110010_claude-model-migration.md) owns the full decision record and rationale.

## Profile snapshot

The table records all 24 profiles in the policy after migration. “Before” is the inspected baseline; exact model names and local rationale are the plan’s dated proposal. The reviewer row covers both existing standard and deep scopes. No profile was calibrated.

| Profile | Before: model / effort | After: model / effort |
|---|---|---|
| Main lead | Opus 5 / xhigh | `claude-opus-5-5` / medium |
| Spec analyst | opus / high | `claude-opus-5-5` / medium |
| Explorer | sonnet / medium | `claude-sonnet-5` / medium |
| Researcher | sonnet / medium | `claude-sonnet-5` / medium |
| Implementer | sonnet / high | `claude-sonnet-5` / high |
| Difficult implementer | opus / xhigh | `claude-opus-5-5` / high |
| Failure analyst | opus / high | `claude-opus-5-5` / high |
| Verifier | sonnet / low | `claude-sonnet-5` / low |
| Test strategist | sonnet / high | `claude-sonnet-5` / high |
| Reviewer (standard and deep scopes) | opus / xhigh | `claude-opus-5-5` / high |
| Adversarial reviewer | opus / xhigh | `claude-opus-5-5` / high |
| Architecture critic | opus / xhigh | `claude-opus-5-5` / high |
| Security reviewer | opus / xhigh | `claude-opus-5-5` / high |
| Migration guardian | opus / high | `claude-opus-5-5` / high |
| API contract reviewer | opus / high | `claude-opus-5-5` / high |
| Dependency auditor | sonnet / high | `claude-sonnet-5` / high |
| Accessibility reviewer | sonnet / high | `claude-sonnet-5` / high |
| Browser QA | sonnet / medium | `claude-sonnet-5` / medium |
| Performance profiler | sonnet / high | `claude-sonnet-5` / high |
| Observability reviewer | sonnet / high | `claude-sonnet-5` / high |
| Release guardian | sonnet / high | `claude-sonnet-5` / high |
| Documenter | sonnet / medium | `claude-sonnet-5` / medium |
| Instruction reviewer | opus / xhigh | `claude-opus-5-5` / high |
| Rule writer | opus / high | `claude-opus-5-5` / high |

The role choices keep Opus for interacting judgment and Sonnet for bounded engineering or evidence work. Effort starts at the documented model guidance and escalates on a named unresolved gap. The [plan](./_agent_plans/20260925-110010_claude-model-migration.md#ratified-routing-hypothesis) records each role’s rationale and escalation condition. Fable 5.1 remains a possible explicit comparison/escalation candidate, with no default profile or automatic fallback. Haiku 4.5 remains a comparison candidate for exact verification or exploration, with no default pin because contract fidelity has not been shown. Restricted Mythos has no local profile. These are routing hypotheses, not rankings or measured advantages.

## Compatibility and availability

Official model and runtime documentation was checked on 2026-09-25. The [model overview](https://platform.claude.com/docs/en/models/overview) documents the model IDs and effort support. The [Claude Code model configuration](https://code.claude.com/docs/en/model-config) and [subagent documentation](https://code.claude.com/docs/en/sub-agents) support the CLI version requirements in the canonical policy:

| Model | API ID | Supported effort | Minimum Claude Code CLI |
|---|---|---|---|
| Opus 5.5 | `claude-opus-5-5` | low, medium, high, xhigh, max | 2.1.280 |
| Fable 5.1 | `claude-fable-5-1` | low, medium, high, xhigh, max | 2.1.257 |
| Sonnet 5 | `claude-sonnet-5` | low, medium, high, xhigh, max | 2.1.197 |
| Haiku 4.5 | `claude-haiku-4-5-20251001` | none | not specified in policy |

These IDs do not establish provider or account access. Provider mappings, allowlists, version-dependent selection precedence, effort caps, overrides, and fallbacks can change the effective selection; inspect the actual session and subagent evidence using the [Claude Code model configuration](https://code.claude.com/docs/en/model-config) and [subagent](https://code.claude.com/docs/en/sub-agents) documentation. On 2026-09-25, `claude --version` returned `2.1.282`; this clears the listed CLI minima, but does not prove account eligibility, Desktop version, effective settings, activation, or serving identity. Desktop update is user-reported; its version was not inspected.

Every profile has `confidence: low` and `calibration_status: unrun`. The migration did not run live comparisons or measure quality, speed, cost, or role-specific advantage. Published API rates and vendor latency labels are specifications, not task measurements or account billing promises. Full Opus 5.5 and Fable 5.1 system cards could not be retrieved after bounded attempts; conclusions use available official model, runtime, prompting, migration, and release pages, with release-page summaries treated as weaker evidence. See the [source research record](../artifacts/claude-model-migration/research-summary.md) for URLs and retrieval limits.

## Comparison design (unrun)

The canonical evaluation corpus defines eight tasks; each compares two configurations twice in fresh contexts, for 32 scenario/configuration/repetition records. A valid comparison keeps prompts, tools, authority, and acceptance criteria identical, changes only the declared factor, preserves outputs and tool evidence, and uses an independent reviewer to score every criterion and forbidden action. Compare cost only between quality-passing configurations; two runs are an initial bounded comparison, not universal evidence. The architecture case may compare Fable at shared effort without creating a default or fallback. Haiku needs a separate design because it has no effort control. No live evaluation, paid model call, or installation was run or authorized by source checks; see [`93-claude-evaluation.md`](../skills/sohrab/alaa-prompting-guide/references/93-claude-evaluation.md) for the execution and calibration contract.

## Source checks and review

Eleven baseline commands passed. The correctness reviewer found two calibration-checker defects in cycle 1; both were fixed before the nineteen integrated static verification commands passed against the frozen 482-file candidate. The instruction reviewer later found a scope drift in cycle 2; the one-file correction then passed two scoped gates and independent literal-text proof. Correctness review approved; the supplied final instruction text was approved and independently bound to disk; security review passed; release review found no remaining source defect after the correction. The cycle 2 scope check confirmed only `90-model-selection.md` changed. Final source manifest SHA-256: `9ac7145a6048d35118ba78f2d80d32ab2280a27b1b2181533815ef8d32a767e5`.

The Codex model policy and orchestrator were preserved. One shared rule-writer red fixture changed on the Codex side. No package artifact or plugin producer was established, and no installation, merge, publication, or runtime activation was performed. Existing source symlinks expose source edits; copied user-agent files remain stale. The worktree also contained staged task evidence of unknown origin, preserved without changing the index. No task commit was created; recovery currently depends on the retained worktree and evidence files, and the staged state must not be read as a task commit. Source verification therefore supports a local merge candidate only, not a package or runtime release. See [verification records](../artifacts/claude-model-migration/verification/command-summary.txt), [final literal-text proof](../artifacts/claude-model-migration/verification/final/literal-text-proof.txt), [review records](../artifacts/claude-model-migration/), and the [runtime update](../artifacts/claude-model-migration/runtime-update.md).
