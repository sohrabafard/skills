# Documentation and artifact alignment for PHP / Laravel work

## Contents
- Documentation language and boundary
- English docblock rules
- README and detailed docs
- Postman collection v2.1 rules
- Environment artifacts
- Flow diagrams
- Alignment and stale-doc cleanup
- When to use companion doc skills

## Documentation language and boundary
Use `/alaa-docs-farsi` (`$alaa-docs-farsi`) for the deterministic workflow that keeps docs, code, and Postman aligned.

When this skill is the active coding baseline:
- keep resulting docs in simple, fluent English unless the user explicitly asks for another language
- keep exact technical identifiers in the same spelling used by the codebase
- preserve detail; do not flatten useful operational or API nuance just to shorten the docs

Use `/openai-docs` (`$openai-docs`) when the documentation touches OpenAI APIs, models, prompts, tools, agent workflows, or product capabilities and you need authoritative current references or citations.

## English docblock rules
Add enough docblocks to serve two goals:
1. richer type information
2. better human understanding of the code

### Use docblocks for type information when native PHP types are not enough
Typical cases:
- array shapes
- collection item types
- template or generic hints used by static analysis
- callable signatures
- map structures and nested payloads
- mixed framework payload contracts that still need exact structure notes

### Use docblocks for understanding when the code is non-obvious
Typical cases:
- invariants and business rules
- side effects and transaction assumptions
- units, formats, encodings, and timezone assumptions
- why a strategy or repository exists here
- why a query path or caching rule is unusual
- what must already be validated or authorized before entry
- what exceptions may be thrown and why

### Docblock quality rules
- Write in simple, fluent English.
- Keep comments specific and technical, not decorative.
- Do not repeat what a clear method name and native types already say.
- Prefer short high-signal blocks over verbose commentary.
- Update or remove stale docblocks whenever the code changes.

## README and detailed docs
When behavior or developer usage changes, align README and detailed docs.

Minimum expectations when the change affects external usage:
- purpose or feature summary stays current
- request and response examples stay current
- env vars and setup steps stay current
- auth assumptions and flow ordering stay current
- diagrams reflect the current flow

Do not leave a high-level README pointing to old behavior while lower-level docs describe the new behavior.

## Postman collection v2.1 rules
Prefer one request item per operation.

For each operation:
- keep one canonical request item
- attach multiple saved response examples to that same request item for the important success and error variants
- do not clone multiple request items only to show different response outcomes for the same operation

### What to include
- realistic dummy payloads and IDs
- variables instead of secrets or machine-specific values
- useful pre-request and test scripts when they help demonstrate or validate the flow
- saved examples for the important success, validation, authorization, not-found, conflict, and server-failure cases when applicable
- headers and bodies that match the current implementation

### Response-example rule
Model the examples as one request with many saved responses, not many duplicated requests.

Good example names:
- `200 Success`
- `401 Unauthorized`
- `403 Forbidden`
- `404 Not Found`
- `409 Conflict`
- `422 Validation Error`
- `500 Internal Error`

## Environment artifacts
Store a separate Postman environment file next to the collection when the collection needs variables.

Typical variables:
- `baseUrl`
- auth token placeholders
- sample `project_id` or other public IDs
- reusable path or tenant variables

Keep environment values safe:
- no real secrets
- no private tokens
- no production-only hostnames unless explicitly intended

## Flow diagrams
Keep request-flow diagrams current whenever the order of calls, auth behavior, or dependency flow matters.

Typical locations:
- `README.md`
- `docs/*.md`
- design or API docs

Preferred format:
- Mermaid when practical, because it is editable and diff-friendly

Capture enough detail for implementers to understand:
- sequence of calls
- auth and validation checkpoints
- dependency ordering
- async steps or callbacks
- success and important failure branches when they change integration behavior

## Alignment and stale-doc cleanup
Treat docs alignment as part of the implementation, not as optional polish.

For every behavior-changing task:
- align code, docblocks, README/docs, Postman collection, environment file, and diagrams
- remove stale sections and duplicate fragments
- keep the most detailed current explanation; delete only outdated or redundant copies
- never leave contradictory examples in different files

A document is stale if it:
- describes an old request or response shape
- uses old field names
- shows outdated flow ordering
- mentions removed env vars, routes, or auth assumptions
- duplicates another document with conflicting detail

## When to use companion doc skills
- Use `/alaa-docs-farsi` (`$alaa-docs-farsi`) for repo-wide documentation passes, docs consistency checks, and docs/Postman sync workflow.
- While using this skill, override the docs output language to simple English unless the user explicitly requests Persian or another language.
- Use `/openai-docs` (`$openai-docs`) when any document needs official OpenAI references, current model guidance, current prompt guidance, or up-to-date product behavior.
