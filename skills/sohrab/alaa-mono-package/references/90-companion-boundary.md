# Companion Boundary

Open this file to decide whether a rule belongs to this skill or to another owner, or when you need the file path inside that owner's skill.

Naming an owner is mandatory. A subject this skill does not cover and does not route is not delegated; it is dropped, and an agent will fill the silence with a guess.

## What this skill owns

Everything that determines what enters the bundling graph: a package's declared `exports` and their conditions, entrypoint stability, dist-only consumption, the peer contract and the single-instance guarantee for shared runtimes, whether a package's CSS and assets are reachable from an entry, internal specifier syntax per detected manager, build order over the dependency graph and its acyclicity, the clean-island write lane, the package's supply-chain defaults, and its release and version gates.

## What it does not own

| Subject | Owner | Where to start |
|---|---|---|
| where the graph's output lands, how it is served, traced to a commit, and rolled back | `/alaa-frontend-devops` (`$alaa-frontend-devops`) | `references/00-topic-map.md` |
| bundler configuration: `resolve.dedupe` wiring, library mode, dependency optimisation, manual chunking | `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`) | `references/22-cli-cookbook-and-examples.md` |
| the application's build targets, client env prefix, and Vite major-version consequences | `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`) | `references/21-cli-vite-and-config.md` |
| every shared version value: framework ranges, Node floor, API prefixes, identifiers | `/alaa-services-contract` (`$alaa-services-contract`) | its `SKILL.md` router |
| release-gate vocabulary on the PHP and Composer side, mirrored here rather than routed to | `/alaa-controlled-ops` (`$alaa-controlled-ops`) | `references/40-validation-and-release-gates.md`; the reason for mirroring is in `references/45-release-and-version-gates.md` |
| test design, proof levels, what a given check proves | `/alaa-testing-strategy` (`$alaa-testing-strategy`) | its proof-level reference |
| supply-chain threat classification, severity, disclosure, and removal decisions | `/alaa-security-review` (`$alaa-security-review`) | its `SKILL.md` router |
| retention of and alerting on build events | `/alaa-observability-soc` (`$alaa-observability-soc`) | its `SKILL.md` router |
| complexity bounds, structure choice, and graph-traversal cost | `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) | its `SKILL.md` router |
| clean code, SOLID, design patterns, and TypeScript language practice | `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`) | its `SKILL.md` router |
| the quality bar every skill and change is held to | `/alaa-project-constitution` (`$alaa-project-constitution`) | its `SKILL.md` router |
| frontend implementation policy inside the application | `/alaa-frontend-developer` (`$alaa-frontend-developer`) | `references/00-topic-map.md` |
| digit and text normalization at any input, including a locale-dependent build step | `/alaa-input-normalization` (`$alaa-input-normalization`) | its `SKILL.md` router |
| how a package command is invoked from a Makefile | `/alaa-makefile` (`$alaa-makefile`) | its `SKILL.md` router |
| current OpenAI or Codex product facts affecting tool integration | `/openai-docs` (`$openai-docs`) | its `SKILL.md` router |
| model selection and reasoning effort | `/alaa-prompting-guide` (`$alaa-prompting-guide`) | `references/50-effort-and-thinking.md` |

## Maintaining this skill

- A concrete path, value, or command written into a reference file states the repository it was read from, on the same line, with a `read: <ISO date>`.
- Every rule appears exactly once in this skill. If a rule needs to be visible in two places, state it in one and route to it from the other.
- The router is `references/00-topic-map.md` and there is exactly one. `SKILL.md` carries a pointer to it and no second table of routes.
- Version values are not written into this skill's prose. Write them into the package manifest and route the range to its owner above, so this skill cannot go stale on a number it does not own.
- Before changing a resolution semantic, a manager protocol, or a current-behaviour statement, follow `references/00-source-map.md`.
