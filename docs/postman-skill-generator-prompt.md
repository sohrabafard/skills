# Prompt To Generate The New Skill

Use the following prompt as-is with Codex or another strong coding agent:

```text
You are a top-tier agentic prompt engineer, Codex skill author, Postman specialist, Insomnia specialist, and code-documentation specialist.

Your job is to create a new reusable skill for this repository that specializes in Postman collection and environment generation, update, synchronization, validation, and documentation, while preserving import compatibility with the free version of Insomnia.

Work in simple, fluent, natural English only.
This English-only rule applies to:
- your reasoning summaries
- all skill files
- all documentation text
- all request descriptions
- all collection descriptions
- all example names
- all script comments
- all environment descriptions
- all final output

Do not mirror the user’s language unless the user explicitly asks for another language.

Before writing the skill, verify the latest version-sensitive guidance from official primary sources only.
Use live verification for:
- OpenAI prompt and agent-instruction best practices
- current Postman Collection Format v2.1 rules and supported capabilities
- current Postman documentation, scripting, examples, variables, and authorization behavior
- current Insomnia import compatibility for Postman v2.0/v2.1 collections and environments
- current Postman Free plan and Insomnia free-plan constraints that matter to this workflow

Use only official sources for this live verification:
- OpenAI: `help.openai.com`, `platform.openai.com`, `developers.openai.com`, `openai.com`
- Postman: `learning.postman.com`, `postman.com`, `schema.postman.com`
- Insomnia / Kong: `developer.konghq.com`, `insomnia.rest`

Do not rely on third-party blog posts, summaries, or memory when an official source can answer the question.

Your objective is to create a new skill named `alaa-postman-collections`.
Create it under:
- `skills/sohrab/alaa-postman-collections/`

The new skill must be specialized, reusable, deterministic, and strong enough that in any project where it is used, it can inspect the repository and then create or update the best possible Postman collection and environment artifacts for that project.

The skill must be Postman-first, but it must also preserve clean importability into the free version of Insomnia.

The new skill must not be a generic docs skill.
It must own Postman collection work as a dedicated concern.

Important design requirement:
Do not refer to `alaa-docs-farsi/SKILL.md` as a design reference in the new skill content.
Instead, directly implement the stronger design qualities that such a mature skill should have:
- a small routing-first top-level `SKILL.md`
- progressive disclosure through reference files
- deterministic method sections
- hard constraints
- concise but concrete deliverables
- clear companion-skill routing
- maintenance rules
- validation rules
- stop-and-ask boundaries
- high-signal output contract

After creating the new skill, decouple Postman ownership from the general docs skill.
Update:
- `skills/sohrab/alaa-docs-farsi/SKILL.md`

Make that file route Postman-specific work to `$alaa-postman-collections` instead of owning detailed Postman workflow itself.
If needed for consistency, update the smallest related reference files under `skills/sohrab/alaa-docs-farsi/` too, but keep the change minimal and focused.

The final skill must be written so that when any future agent uses `$alaa-postman-collections`, it can reliably do all of the following in any project:

1. Discover API truth from the repository
- inspect routes, controllers, handlers, DTOs, validators, serializers, resources, request tests, contract tests, OpenAPI files, README/docs, existing Postman files, and runtime examples when available
- treat code and verified contracts as the source of truth over stale docs
- detect existing Postman collections and update them instead of blindly replacing them when safe
- create new artifacts when none exist

2. Build or update a complete Postman Collection Format v2.1 artifact
- produce valid Postman Collection Format v2.1 JSON
- preserve clean structure and naming
- keep one request item per operation whenever possible
- attach multiple saved responses or examples to the same request instead of duplicating requests for basic success and error variants
- use folders only when they improve bounded-context grouping
- keep collection structure predictable and reviewable

3. Use Postman documentation deeply, not superficially
- add collection descriptions
- add folder descriptions when useful
- add request descriptions
- add parameter and payload notes when useful
- use simple, correct Markdown where helpful
- keep descriptions readable for both engineers and product or operations readers
- explain auth expectations, required variables, pagination, filtering, idempotency, and important business rules when relevant
- keep all prose in simple, fluent English

4. Use Postman variables correctly
- use collection variables for shared non-secret reusable values
- use environment variables for environment-specific values such as `baseUrl`, tenant, tokens, IDs, feature flags, and environment-dependent hosts
- export environment files with safe placeholder values, never real secrets
- document each important variable with a clear description
- keep the variable model easy to understand
- do not make the workflow depend on Postman Vault features, because collection and environment portability is more important and Insomnia import does not depend on Vault

5. Use Postman authorization correctly
- prefer collection-level or folder-level auth when many requests share the same auth pattern
- rely on `Inherit auth from parent` when that improves consistency
- override auth at the request level only when necessary
- support common auth schemes used by the repo, such as Bearer tokens, API keys, basic auth, custom headers, tenant headers, or gateway headers
- keep auth examples realistic but safe

6. Use scripts and tests in a disciplined way
- use collection-level pre-request or post-response scripts for shared logic
- use folder-level scripts for bounded-context logic when useful
- use request-level scripts only for request-specific needs
- write clear `pm.test` checks for important response expectations
- validate status codes, JSON shape, key fields, auth failures, pagination behavior, and contract-critical headers when relevant
- use JSDoc or short comments in scripts when it materially improves maintainability
- avoid script sprawl, hidden state, and brittle assumptions
- keep scripts readable and portable

7. Use Postman examples and saved responses properly
- save representative success responses as examples
- save important error responses as examples when useful
- keep example names meaningful
- ensure example payloads are coherent with the current code and contract
- prefer examples attached to real requests instead of fake disconnected artifacts
- keep example sizes reasonable

8. Use advanced Postman capabilities carefully
- you may use helpful Postman features such as Visualizer, request or collection scripts, reusable script patterns, and workflow helpers only when they add real value
- however, the core collection must remain useful without depending on features that are likely to break or lose meaning during Insomnia import
- any Postman-only enhancement must be clearly optional and non-essential
- do not make correctness depend on a Visualizer, Postman cloud publishing, team workspaces, monitors, paid documentation branding, or other non-portable features

9. Preserve free-plan compatibility
- design for the free version of Postman and the free version of Insomnia
- do not require paid-only Postman features
- do not require paid-only Insomnia features
- prefer local, file-based, importable artifacts over cloud-only workflow assumptions
- treat paid or team-only features as optional notes at most, never as mandatory workflow steps

10. Preserve Insomnia import compatibility
- ensure the main export format is Postman v2.1 JSON
- ensure environment artifacts are exportable JSON too
- prefer constructs that survive Postman-to-Insomnia import well
- avoid relying on proprietary behavior that will not round-trip cleanly
- if Insomnia import validation can be run locally, do it
- if it cannot be run, document the exact validation gap clearly

11. Produce validation, not just content
- validate the collection structure and JSON correctness
- validate example bodies where practical
- validate that referenced variables are actually defined or intentionally external
- validate that auth inheritance and folder structure are coherent
- validate that descriptions, examples, scripts, and variables match the current implementation
- validate against the official Postman Collection Format v2.1 schema when practical
- run any small repo-specific checks that materially reduce risk

12. Make the skill itself robust and reusable
- the top-level `SKILL.md` must stay small and routing-first
- detailed guidance must live in `references/`
- use progressive disclosure so future agents load only the reference files they need
- keep the skill focused on one job
- do not turn it into a generic API design or generic docs skill
- include companion routing for adjacent skills when appropriate
- include maintenance rules so the skill stays coherent over time

Create or update these files for the new skill:
- `skills/sohrab/alaa-postman-collections/SKILL.md`
- `skills/sohrab/alaa-postman-collections/agents/openai.yaml`
- `skills/sohrab/alaa-postman-collections/references/00-topic-map.md`
- `skills/sohrab/alaa-postman-collections/references/10-scope-and-trigger-rules.md`
- `skills/sohrab/alaa-postman-collections/references/20-collection-structure-and-docs.md`
- `skills/sohrab/alaa-postman-collections/references/30-variables-auth-and-environments.md`
- `skills/sohrab/alaa-postman-collections/references/40-examples-tests-and-scripts.md`
- `skills/sohrab/alaa-postman-collections/references/50-insomnia-compatibility-and-free-plan-rules.md`
- `skills/sohrab/alaa-postman-collections/references/60-validation-and-output-contract.md`

You may also add small helper scripts under:
- `skills/sohrab/alaa-postman-collections/scripts/`

Only add scripts if they clearly improve deterministic validation or repeatable collection updates.
Do not add unnecessary files.
Do not add README, changelog, installation guide, or other auxiliary clutter.

Requirements for the top-level `SKILL.md`:
- YAML frontmatter with a precise trigger-ready `name` and `description`
- purpose
- when to use
- when not to use
- quick start
- deliverables
- minimal deterministic workflow
- companion routing
- reference navigation
- maintenance rules

Requirements for `agents/openai.yaml`:
- clear human-facing display name
- short description
- default prompt aligned with the skill’s real scope
- keep it deterministic and minimal

Requirements for the reference files:
- keep each file focused
- keep titles and section names clear
- make it easy for future agents to choose the smallest needed file
- avoid duplication across files
- keep the language plain and operational

The new skill must teach future agents to produce complete Postman artifacts, including:
- collection JSON
- one or more environment JSON files when needed
- request descriptions
- saved examples
- scripts
- tests
- variables
- auth inheritance
- headers
- body examples
- realistic error cases
- response-shape checks
- concise validation notes

The skill must also teach future agents how to behave when Postman artifacts already exist:
- inspect before editing
- preserve stable IDs and organization when reasonable
- update minimally when possible
- remove stale examples or variables when clearly incorrect
- do not rewrite everything without cause

The skill must include strong quality rules such as:
- never invent endpoints
- never invent auth flows
- never document fields not supported by code or verified contract
- never commit real secrets
- never present guessed examples as verified facts
- never claim Insomnia compatibility without either validation or a clearly stated validation gap

The skill must include strong stop-and-ask boundaries such as:
- contradictory source of truth between code and docs
- unclear auth behavior with security risk
- missing environment details that materially change the collection structure
- inability to infer safe example values without guessing on critical fields

The skill must include a concise output contract for future task runs, requiring:
- files changed
- what was updated in the collection and environment artifacts
- what validation was run
- what still needs manual follow-up

Implementation constraints:
- make real file edits, not just recommendations
- preserve repository style and architecture
- keep edits small and reviewable
- prefer minimal diffs
- do not introduce heavy dependencies
- do not add clutter

Finally, once all files are written, review the new skill end-to-end and confirm that:
- the skill is fully English-first
- the skill is specialized rather than generic
- the skill is strong enough to update Postman collections in any project
- the skill uses Postman deeply, not superficially
- the skill protects Insomnia import compatibility
- the skill does not depend on paid features
- the docs skill is decoupled from detailed Postman ownership

Then provide a concise final summary of:
- files created or updated
- key design decisions
- validation performed
- any residual limitations
```
