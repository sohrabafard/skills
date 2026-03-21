# Agent orchestration for PHP / Laravel work

## Contents
- Single agent first
- When to split into subagents
- Preferred orchestration pattern
- Parallel local work
- Good PHP / Laravel split patterns
- Validation and review
- Anti-patterns
- Official references

## Single agent first
Start with one clear local plan.

Use a single agent when:
- the task is small or medium
- the immediate next step is blocked on one local inspection
- one agent can still hold the codebase context comfortably
- splitting would create more coordination cost than speed

A multi-agent workflow is justified when independent tracks exist or prompt and tool complexity are beginning to reduce quality.

## When to split into subagents
Use subagents only when both of these are true:
- the user explicitly asks for subagents, delegation, or parallel agent work, or the environment policy clearly allows it
- the work can be decomposed into bounded subtasks that materially help the main task

Good reasons to split:
- independent repository discovery questions
- separate implementation slices with disjoint write scopes
- independent validation or review passes
- external research that can run while the main agent keeps coding locally

Bad reasons to split:
- the task is trivial
- the very next action is blocked on the delegated result and no other meaningful local work exists
- multiple subagents would touch the same files without clear ownership
- the goal is only to sound busy rather than reduce cycle time or improve quality

## Preferred orchestration pattern
Prefer a manager pattern for coding tasks.

That means:
- one main agent keeps plan ownership, repository context, and final synthesis
- subagents behave like tools, workers, or focused reviewers
- the main agent integrates the results and stays responsible for the final answer and final diff

Prefer decentralized handoffs only when one agent truly should give up control to another specialist. For most repo coding tasks, the manager pattern is safer and easier to keep coherent.

## Parallel local work
Use parallel local work for independent operations.

In Codex desktop:
- use `multi_tool_use.parallel` for independent developer-tool calls
- parallelize read-only inspections such as file reads, searches, directory listings, or unrelated validation commands
- fan out first, then synthesize once in the main agent

Do not parallelize:
- overlapping writes
- commands that mutate shared state in conflicting ways
- tools that explicitly should not run in parallel
- steps where one command depends on the output of another

## Good PHP / Laravel split patterns

### Discovery fan-out
Use separate subagents for questions such as:
- routes, controllers, requests, and resources
- services, DTOs, repositories, and policies
- tests, docs, and existing conventions

### Implementation fan-out
Use separate subagents only when write scopes are disjoint, for example:
- worker A owns Form Requests and Resources
- worker B owns Services, DTOs, or Strategies
- worker C owns tests or documentation

### Validation fan-out
Use separate passes for:
- independent review of changed files
- verifying route-to-resource consistency
- checking whether new abstractions actually reduced duplication

## Validation and review
While subagents run:
- continue non-overlapping local work
- do not busy-wait
- do not duplicate the delegated work locally

For tricky changes, use a fresh subagent as an independent reviewer or forward-check. Give the minimum context needed and inspect the resulting reasoning, diff, or artifacts rather than leaking the intended answer.

## Anti-patterns
- spawning subagents for every task by habit
- delegating the immediate blocking step and then waiting idle
- sending vague, open-ended, overlapping assignments
- letting multiple agents edit the same files without ownership boundaries
- using subagents to bypass safety, approval, or repository policy
- parallelizing `apply_patch`, `js_repl`, or any tool that forbids parallel execution
- asking subagents to solve the same unresolved question redundantly

## Official references
This guidance is aligned with:
- OpenAI's practical guidance to start with a single agent first and add multi-agent orchestration only when the task structure justifies it
- OpenAI's manager vs decentralized orchestration patterns for agent systems
- OpenAI prompt guidance to keep instructions explicit and tool-oriented
- OpenAI evaluation guidance to validate workflow behavior, not just final text
