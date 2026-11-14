# Implementation gap and remaining-task rules

Use this reference when the user asks for remaining work, or when a document or Postman artifact
describes behavior that current source code does not implement.

This file contains rules for producing a `remaining-task.md` in a target repository. It holds no
backlog items of its own, and none are ever added here: the backlog lives in the repository the
task is about.

`remaining-task.md` reports documentation gaps. Workflow owns task state.
For a Beads-bound repository, register each gap under `/alaa-workflow` `references/task-tracking.md`.
During an outage, keep the gap in the report and mark it unregistered until registration.
For active workflow work, use the pending location in that reference's `## Outage and uncertain writes`.
Reconcile at the next availability test or report refresh, whichever comes first, following
`## Select before tracking-dependent work` in the same reference.

## When to create or refresh `remaining-task.md`

Create or refresh it when:

- the user explicitly asks for remaining tasks, missing implementation, or a backlog,
- a documentation refresh finds promised behavior not backed by routes, handlers, jobs, migrations, tests, or config,
- Postman examples or request folders expose endpoints or actions that do not exist in current code,
- a design document must be preserved but its future-looking claims need an explicit implementation backlog.

Do not create it for ordinary documentation polish when no implementation gap was found.

## Evidence standard

Each item must cite both sides:

- the document, Postman request, or design note that promises or implies the behavior,
- the source-code evidence showing the behavior is absent, stubbed, fail-closed, or incomplete.

Use code, route definitions, tests, migrations, config, and current artifacts as evidence. Never list a speculative product idea as an implementation gap.

## Required shape

- group by service, module, or feature area,
- number each task,
- state the missing behavior in plain words,
- cite the promise and the current implementation evidence for each item,
- state whether the gap affects documentation only, Postman examples, the public API, storage, jobs, events, or operations,
- separate future proposals from the work required to make existing documents truthful.

## What not to include

- raw transcripts or command logs,
- an invented route name, payload, field, or business behavior,
- a broad "improve docs" task with no concrete implementation gap,
- a machine-local absolute path in a Markdown link.

## Postman handoff

When `/alaa-postman-collections` reports a documented-but-missing endpoint or example, this skill owns
the `remaining-task.md` wording. Keep collection rules with their owner.
