# Dispatching `alaa-rule-writer`

Dispatch only after a draft exists. Initial authoring, and every decision about what a rule says, stays with the session that runs this skill.

## Task controls

The managed wrappers omit model and effort.

1. Choose an explicit model AND effort for the rewrite through the delegating parent's runtime orchestrator allocation procedure. That procedure does not require its full pipeline.
2. Normalize omitted fields through `alaa-codex-orchestrator references/model-effort-policy.md` or its `alaa-cc-orchestrator` mirror before validation.
3. When no durable plan is admitted, record both controls and the task reason in this dispatch.
4. Check the loaded model-neutral role and the effective controls. Validate the controls separately from role authority. The observed serving identity can stay unknown without a paid probe.

## Fields

Send lane facts only. The definition owns the role, the invariants, the doctrine order and the output contract; a restatement dilutes both copies.

| Field | Carries |
|---|---|
| `task_controls` | The exact model and a supported effort, the task reason and verified control-resolution evidence. The role title supplies neither choice. The caller records identity uncertainty, because replacement-only output carries no metadata |
| `item_id` | A stable id, echoed back unchanged. Required for a single item too, so a batch and a single item share one shape |
| `artifact_type` | One of: rule or prompt, `SKILL.md` section, subagent definition, `AGENTS.md` or `CLAUDE.md` section |
| `draft` | The drafted text verbatim, or the target path and the section within it |
| `immutable_behavior_and_decisions` | What the text must keep deciding, in the dispatcher's own words. The rewrite is checked against it; without it the agent has only the draft's wording as evidence of intent |
| `required_sources_of_truth` | The paths the agent may read to recover intent. An unlisted path is out of reach |
| `output_mode` | `single` or `batch` |

Send several items in one batch, not one dispatch per item. The agent treats them independently, and a blocked item blocks no other.
