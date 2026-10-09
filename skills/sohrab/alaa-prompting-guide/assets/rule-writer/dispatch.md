# Dispatching `alaa-rule-writer`

Choose explicit model AND effort for the actual rewrite through the delegating parent's runtime orchestrator allocation procedure; using that procedure does not require its full pipeline. Record both controls and the task reason in this dispatch when no durable plan is admitted. Check the loaded model-neutral role and effective controls; observed serving identity may remain unknown without a paid probe.

Send lane facts only. The definition already owns the role, the invariants, the doctrine order, and
the output contract, so restating any of them here dilutes both copies.

| Field | Carries |
|---|---|
| `task_controls` | Explicit exact model and supported effort, task reason and verified control-resolution evidence; role title supplies neither choice. Caller records identity uncertainty because replacement-only output carries no metadata. |
| `item_id` | A stable id, echoed back unchanged. Required even for a single item, so a batch and a single share one shape. |
| `artifact_type` | One of: rule or prompt, `SKILL.md` section, subagent definition, `AGENTS.md` or `CLAUDE.md` section. |
| `draft` | The drafted text verbatim, or the target path and the section within it. |
| `immutable_behavior_and_decisions` | What the text must keep deciding, in the dispatcher's own words. This is what the rewrite is checked against; without it the agent has only the draft's wording as evidence of the draft's intent. |
| `required_sources_of_truth` | Paths the agent may read to recover intent. Anything not listed here is out of reach. |
| `output_mode` | `single` or `batch`. |

Send several items in one batch rather than one dispatch per item: the agent treats them
independently and a blocked item does not block the others, so batching costs nothing and saves the
per-dispatch context.

Dispatch only after a draft exists. Initial authoring, and every decision about what a rule should
say, stays with the session running this skill.
