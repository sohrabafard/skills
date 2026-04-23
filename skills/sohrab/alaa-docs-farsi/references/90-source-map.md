# Source Map

Use this file when documentation work depends on current repo behavior, external documentation formats, or version-sensitive tooling.

## Source priority

1. Target repo truth: code, config, migrations/schema, routes, controllers/actions, validators, resources/serializers, tests, current docs, Postman artifacts, runtime wrappers, and `AGENTS.md`.
2. Companion Ala skills that own the domain being documented, such as `$alaa-services-contract`, `$alaa-trust-gateway-auth`, `$alaa-observability-soc`, `$alaa-postman-collections`, and framework skills.
3. Official or primary docs for documentation formats and tools:
   - CommonMark: https://spec.commonmark.org/
   - GitHub Markdown: https://docs.github.com/get-started/writing-on-github
   - GitLab Markdown: https://docs.gitlab.com/user/markdown/
   - Mermaid docs: https://mermaid.js.org/
   - OpenAPI Specification: https://spec.openapis.org/oas/latest.html
   - Postman docs: https://learning.postman.com/docs/
4. Community examples, StackOverflow answers, and generated snippets only for troubleshooting formatting or renderer quirks. Do not use them as source truth for product behavior.

## Freshness triggers

Re-check source files and official docs when the task mentions:

- latest/current behavior, route changes, response examples, new errors, events, jobs, queues, metrics, deployment changes, API versions, or frontend integration changes
- Markdown rendering problems in GitHub/GitLab, Mermaid syntax, OpenAPI output, Postman examples, or link validation
- security-sensitive, auth-sensitive, or billing/entitlement-sensitive documentation claims

## Community-source limits

- Do not document behavior from a blog, issue comment, or StackOverflow answer unless the repo proves it.
- Use community material only to diagnose why a renderer or tool behaves unexpectedly, then convert the conclusion into repo-backed wording.

## Domain-bounded example

Good: for a new endpoint, update the route inventory, one representative request example, related storage/error docs, README navigation, and Postman sync note when applicable.

Bad: pasting a stale curl example from old docs because the path name looks similar.
