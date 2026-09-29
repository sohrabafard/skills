# Child pipelines and checklist

Open this guide when the task involves child pipelines, multi-file layout or the final authoring checklist. The topic map routes to this file.

For current feature claims and release qualifications, use the [source map](../00-source-map.md) and [version notes](../feature-version-notes.md).

## Child pipelines and multi-file layouts

Use a child pipeline when the subtree has materially different jobs, when the
configuration must be generated, or when the parent's job list would otherwise be
unreadable. Keep the parent responsible for orchestration and gating; keep each
child focused and named for its subtree; be explicit about which variables are
forwarded. Debug parent creation and child execution as two separate problems.

## Authoring checklist

Before finishing a pipeline design:

- Is pipeline creation controlled by `workflow:rules` with a terminal arm?
- Does every job that mutates a shared target set `interruptible: false` and a
  `resource_group` named after that target?
- Does every job set `timeout:`?
- Is `retry:` narrowed to infrastructure classes?
- Does every deploy job declare an `environment:` with a `url:`?
- Are images pinned in every place they appear, including runner-side?
- Are cache keys derived from what makes the cache stale, with an explicit
  `policy:`?
- Does every artifact set `expire_in`?
- Is every job's real precondition expressed as a `needs:` edge?
- Does the answer state which checks are gates and name the skill that decided
  that, rather than deciding it here?
