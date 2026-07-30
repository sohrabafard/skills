# Implementation gap and remaining-task rules

Use this reference when the user asks for remaining work, or when a document or Postman artifact
describes behavior that current source code does not implement.

This file contains rules for producing a `remaining-task.md` in a target repository. It holds no
backlog items of its own, and none are ever added here: the backlog lives in the repository the
task is about.

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
- state the missing behavior in plain English,
- cite the promise and the current implementation evidence for each item,
- state whether the gap affects documentation only, Postman examples, the public API, storage, jobs, events, or operations,
- separate future proposals from the work required to make existing documents truthful.

## What not to include

- raw transcripts or command logs,
- an invented route name, payload, field, or business behavior,
- a broad "improve docs" task with no concrete implementation gap,
- a machine-local absolute path in a Markdown link.

## Postman handoff

When `/alaa-postman-collections` (`$alaa-postman-collections`) finds a documented-but-missing endpoint or example, it reports the gap and this skill owns the `remaining-task.md` backlog wording. That direction is reciprocal and already written on both sides; do not restate the Postman collection's own rules here.
