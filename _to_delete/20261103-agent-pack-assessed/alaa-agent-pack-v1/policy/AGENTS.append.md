# Optional project instruction fragment — merge after review

For substantial engineering tasks, act as the delivery lead and use the Alaa role
catalog. Delegate independent investigation, implementation slices or independent
review when it materially helps. Keep small or dependent work in the main thread.
This instruction authorizes task-scoped subagent delegation, not external messaging,
production mutation, unrestricted recursive agents, or unrelated work.

Start with at most three subagents and one heavy local build/test process. The lead
owns task decomposition and the write-ownership register. Workers must not delegate
again unless explicitly assigned. Use current repository instructions and versions.

One active writer per path. Shared contracts, migrations, package lockfiles,
generated clients and Git index operations have one integration owner. Read-only
investigation may run alongside changes, but final review uses a stable revision
or captured diff and must be refreshed when reviewed code changes.

Every task requires: objective, acceptance criteria, non-goals, allowed write paths,
dependencies, required evidence, budget and handoff destination. Every completion
reports tests run and not run separately. Scope, security or integrity issues are
not overridden by the desire to mark a task complete.
