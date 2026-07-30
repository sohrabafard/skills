# Source map

Use this file when documentation work depends on repository behavior, an external documentation
format, or version-sensitive tooling.

## Source priority

1. **Target repository truth** — code, config, migrations and schema, routes, controllers or actions, validators, resources or serializers, tests, current documents, Postman artifacts, runtime wrappers, and `AGENTS.md`. Rank 1 always wins.
2. **The Ala skill that owns the domain being documented** — `/alaa-services-contract` (`$alaa-services-contract`), `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`), `/alaa-observability-soc` (`$alaa-observability-soc`), `/alaa-data-layer` (`$alaa-data-layer`), `/alaa-async-messaging` (`$alaa-async-messaging`), `/alaa-security-review` (`$alaa-security-review`), `/alaa-postman-collections` (`$alaa-postman-collections`), and the framework skills. The full ownership table is in `SKILL.md`.
3. **Official or primary documentation** for a format or tool, listed below.
4. **Community examples, forum answers, and generated snippets** — only to diagnose why a renderer or tool behaves unexpectedly. Never as source truth for product behavior.

## Official sources, each with the command that re-derives it

A URL and a version both go stale silently. The command beside each one does not.

| Source | URL | Re-derivation |
|---|---|---|
| CommonMark specification | `https://spec.commonmark.org/` | `curl -sSI https://spec.commonmark.org/` and read the linked current version |
| GitHub Markdown | `https://docs.github.com/get-started/writing-on-github` | fetch the URL and confirm it returns 200 without redirect |
| GitLab Flavored Markdown | `https://docs.gitlab.com/user/markdown/` | fetch the URL and confirm it returns 200 without redirect |
| Mermaid | `https://mermaid.js.org/` | `npm view mermaid version` for the current release, then check the syntax index for the diagram type you used |
| OpenAPI Specification | `https://spec.openapis.org/oas/latest.html` | fetch the URL; `latest.html` redirects to the current version, so read the version from the served page rather than pinning one here |
| Postman documentation | `https://learning.postman.com/docs/` | fetch the URL; `https://learning.postman.com/llms.txt` serves a machine-readable index of the same documentation |

Before citing a Mermaid diagram type, a Markdown extension, or an OpenAPI version in a document you produce, run the re-derivation command for that row. A rendering claim inherited from an older document is not verified.

## Freshness triggers

Re-check repository sources and the official documentation when the task mentions:

- current behavior, route changes, response examples, new errors, events, jobs, queues, metrics, deployment changes, API versions, or frontend integration changes,
- a Markdown rendering problem in GitHub or GitLab, Mermaid syntax, OpenAPI output, Postman examples, or link validation,
- a security-sensitive, auth-sensitive, or billing or entitlement-sensitive documentation claim.

## Community-source limits

- Never document behavior from a blog, issue comment, or forum answer unless the repository proves it.
- Use community material only to diagnose why a renderer or tool misbehaves, then convert the conclusion into repository-backed wording.

## Domain-bounded example

Good: for a new endpoint, update the route inventory, one representative request example, the related storage and error documents, README navigation, and the Postman sync note when applicable.

Bad: pasting a stale curl example from an old document because the path name looks similar.
