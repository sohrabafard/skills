# Implementation Gap And Remaining-Task Rules

Use this reference when the user asks for remaining work, or when docs/Postman artifacts describe behavior that current source code does not implement.

## When to create or refresh `remaining-task.md`

Create or refresh `remaining-task.md` when:

- the user explicitly asks for remaining tasks, missing implementation, or a backlog
- a docs refresh finds promised behavior that is not backed by routes, handlers, jobs, migrations, tests, or config
- Postman examples or request folders expose endpoints/actions that do not exist in current code
- a design doc must be preserved but its future-looking claims need a clear implementation backlog

Do not create it for ordinary docs polish when no implementation gap was found.

## Evidence standard

Each item must cite both sides:

- the source doc, Postman request, or design note that promises or implies the behavior
- the source-code evidence showing the behavior is absent, stubbed, fail-closed, or incomplete

Use code, route definitions, tests, migrations, config, and current artifacts as evidence. Do not list speculative product ideas as implementation gaps.

## Required shape

Keep the file concise and useful:

- group by service, module, or feature area
- number each task
- include the missing behavior in plain English
- include source references to the promise and to the current implementation evidence
- mention whether the gap affects docs only, Postman examples, public API, storage, jobs, events, or operations
- separate future proposals from work required to make existing docs truthful

## What not to include

- raw transcripts or command logs
- invented route names, payloads, fields, or business behavior
- broad "improve docs" tasks without a concrete implementation gap
- machine-local absolute paths in Markdown links

## Postman handoff

When `$alaa-postman-collections` finds a documented-but-missing endpoint or example, it should report the gap and let this skill own the `remaining-task.md` backlog wording.
