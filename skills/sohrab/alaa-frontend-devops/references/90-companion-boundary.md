# Companion Boundary

Open this file to decide whether a rule belongs to this skill or to another owner, or when you need the file path inside that owner's skill.

Naming an owner is mandatory. A subject this skill does not cover and does not route is not delegated; it is dropped, and an agent will fill the silence with a guess.

## What this skill owns

The frontend delivery gate register — for each gate, the predicate it asserts, the command that evaluates it, and the artifact it inspects. The artifact contract. The build-time-versus-runtime configuration boundary. Artifact identity and provenance. The cache *policy* per response class. What may and may not be compiled into a client bundle. The deploy-failure playbook and the rollback path.

## What it does not own

| Subject | Owner | Where to start |
|---|---|---|
| how a gate is expressed on a runner: job graph, `rules:`, `needs:`, cache-key syntax, artifact retention, runner image | `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`) | its `SKILL.md` router |
| how the build and runtime images and any Compose file are expressed: Dockerfile authorship, layer ordering, multi-stage, minimisation | `/alaa-docker-production` (`$alaa-docker-production`) | its `SKILL.md` router |
| how a cache or routing decision is expressed as a directive: headers, compression, rewrites | `/alaa-haproxy` (`$alaa-haproxy`) | its `SKILL.md` router |
| CDN origin bucket, lifecycle rules, retention of superseded assets, invalidation calls | `/alaa-minio-object-storage` (`$alaa-minio-object-storage`); `/alaa-arvan-object-storage` (`$alaa-arvan-object-storage`) for an ArvanCloud-backed origin | their bucket and lifecycle references |
| what enters the bundling graph: package `exports`, peer contract, specifiers, asset reachability | `/alaa-mono-package` (`$alaa-mono-package`) | `references/00-topic-map.md` |
| Quasar and Vite configuration, `build.env` and the client prefix, service-worker implementation, Vite major-version consequences | `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`) | `references/21-cli-vite-and-config.md`, `references/32-pwa-injectmanifest-guard.md` |
| Make targets and how a command is invoked from a Makefile | `/alaa-makefile` (`$alaa-makefile`) | its `SKILL.md` router |
| test design, proof levels, what a given check proves | `/alaa-testing-strategy` (`$alaa-testing-strategy`) | its proof-level reference |
| threat classification, exposure severity, rotation and disclosure | `/alaa-security-review` (`$alaa-security-review`) | its `SKILL.md` router |
| retention of and alerting on build and deploy events | `/alaa-observability-soc` (`$alaa-observability-soc`) | its `SKILL.md` router |
| timeout, pool, and availability targets for the serving path | `/alaa-reliability-sla` (`$alaa-reliability-sla`) | its `SKILL.md` router |
| the canonical values shared across services: API prefixes, environment variable names, project identifiers | `/alaa-services-contract` (`$alaa-services-contract`) | its `SKILL.md` router |
| the quality bar every skill and change is held to | `/alaa-project-constitution` (`$alaa-project-constitution`) | its `SKILL.md` router |
| clean code, SOLID, and design-pattern judgement in frontend source | `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`) | its `SKILL.md` router |
| complexity bounds and structure choice, including chunking cost as input size grows | `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) | its `SKILL.md` router |
| frontend implementation policy and SSR behaviour in application code | `/alaa-frontend-developer` (`$alaa-frontend-developer`) | its `references/00-topic-map.md` |
| deployment notes written as inline documentation annotations | `/alaa-frontend-doc-annotations` (`$alaa-frontend-doc-annotations`) | its `SKILL.md` router |
| digit and text normalization at any input, including build-time text handling | `/alaa-input-normalization` (`$alaa-input-normalization`) | its `SKILL.md` router |
| current OpenAI or Codex product facts affecting tool integration | `/openai-docs` (`$openai-docs`) | its `SKILL.md` router |
| model selection and reasoning effort | `/alaa-prompting-guide` (`$alaa-prompting-guide`) | `references/50-effort-and-thinking.md` |

## Maintaining this skill

- A concrete path, value, or command written into a reference file states the repository it was read from, on the same line, with a `read: <ISO date>`.
- Every rule appears exactly once in this skill. If a rule needs to be visible in two places, state it in one and route to it from the other.
- The router is `references/00-topic-map.md` and there is exactly one. `SKILL.md` carries a pointer to it and no second table of routes.
- Before changing a version, security, or current-behaviour statement, follow `references/00-source-map.md`.
