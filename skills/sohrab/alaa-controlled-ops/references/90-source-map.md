# Source Map

Use this file when freshness matters, or when a surface belongs to another skill. The source ranking lives in `references/10-source-priority-and-boundaries.md` and nowhere else.

## Freshness triggers

Refresh from source before answering when the task mentions latest package version, current route count, current Postman count, permission ID allocation, Satis tag visibility, Composer lock source, or a specific ControlledOps phase.

## Companion skills

Load one when its condition holds. Companions cited inside a rule elsewhere in this skill — `/alaa-reliability-sla`, `/alaa-postman-collections`, `/alaa-repo-docs` — carry their condition at that rule and are not repeated here.

- `/alaa-project-constitution` — owns the fleet quality bar. Read when judging whether a package change is fit to release, or when the repository carries a `CONSTITUTION.md`.
- `/alaa-services-contract` — platform service contracts and public API shape. Its `references/22-failure-load-and-deprecation-contract.md` owns failure, load, and deprecation: read before changing how a ControlledOps operation behaves under load, or before deprecating a package contract an adopter uses.
- `/alaa-security-review` — read before adding, rotating, or relocating any credential the release path touches: Git remote authentication, deploy keys, or registry credentials for the Satis build. Never write one into a tracked file, a tag message, or your report.
- `/alaa-observability-soc` — owns the contract for the package's audit, structured-log, metric, progress, and lifecycle-outbox value objects. Read before adding, renaming, or widening the cardinality of a field on one of them.
- `/service-runtime-kit-governance` — read before you generate a local runtime or a Docker wrapper, or diff generated output.
- `/alaa-trust-gateway-auth` — gateway context and trusted headers. The permission bit contract, its id allocation, and the canonical decoders are `/alaa-permission-generator`; the TOTP proof's contract shape is `/alaa-services-contract` `references/32-auth-totp-and-step-up-contract.md`.
- `/alaa-php-clean-code` — read before you write or review Laravel or PHP code in either repository.
- `/alaa-data-layer` — read before you change persistence, a transaction, or a fact that Postgres owns.
- `/alaa-prompting-guide` — every model and reasoning-effort question. Pin no model name in this skill or in work produced under it.
