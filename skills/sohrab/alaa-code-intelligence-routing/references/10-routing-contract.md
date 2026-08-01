# Evidence and artifact router

Choose one primary owner for the current question. The owner of evidence may differ from the owner of the edit and the owner of proof.

## Decision order

1. Name the required answer: location, flow, exact symbol, prose, effective configuration, generated output, runtime fact, external fact, review risk, or proof.
2. Classify the artifact and check the active worktree, freshness, generated owner, installed version, environment, and authorization boundary.
3. Select one primary owner from the table.
4. Record what it established and stop when the next safe action is known.
5. Use one secondary owner only for one named missing fact.
6. Route authoring and validation to their owning skill or native gate.

## Router

| Current question | Primary owner | Secondary only for a named gap |
|---|---|---|
| Unknown location, architecture, execution flow, relationship, or likely impact in indexed source | CodeGraph | Serena for one exact semantic fact; native read for one specifically stale or uncovered file |
| Exact definition, reference, implementation, hierarchy, type-aware diagnostic, or known-symbol navigation | Serena | CodeGraph only when a new wider-flow or impact question appears |
| Known small textual change in one named hand-maintained file | Native targeted read and patch | Serena only when semantic boundaries materially reduce risk |
| Semantic rename, symbol-body replacement, or reference-safe code edit | Serena | Native patch only after the exact range is established and Serena cannot perform the operation |
| Markdown phrase or identifier across repository documents | Native search restricted to Markdown | Serena Markdown for headings after one document is named |
| Heading outline or section navigation in one known Markdown file | Serena Markdown when healthy | Targeted native read |
| Repository Markdown creation, alignment, de-duplication, navigation, or link repair | `/alaa-repo-docs` in Claude Code or `$alaa-repo-docs` in Codex | Claim-specific code, config, contract, framework, or runtime evidence |
| Source comments, docblocks, or annotations | `/alaa-frontend-doc-annotations` or `$alaa-frontend-doc-annotations` | Serena for the exact containing symbol |
| JSON, YAML, TOML, CI, environment templates, manifests, or policy text | Native scoped search/read plus parser or repository checker | Serena only for one named diagnostic question when that language is enabled |
| OpenAPI, AsyncAPI, Postman, protobuf, schema, or another machine-readable contract | Installed contract-owning skill or generator | Repository docs owner for prose summaries only |
| Generated source or generated documentation | Source template and generator | Direct edit only when repository policy declares the artifact hand-maintained |
| Installed Laravel package behavior or authorized application context | Laravel Boost | CodeGraph for source flow; native commands for proof |
| Runtime logs, traces, metrics, browser state, database behavior, queue state, or cache state outside Boost | Authorized runtime owner | CodeGraph to map the observed fact to source |
| Current external framework, package, protocol, or platform behavior | Official version-aware source | Repository evidence only for local usage |
| Current change review | Git diff first | Expand only for a named risk through CodeGraph, Serena, runtime evidence, docs owner, or targeted tests |
| Cross-repository ownership, consumer, or compatibility question | Authoritative service catalog, contract registry, GitHub, or existing Hindsight surface | Local CodeGraph only after repositories are named |
| Behavioral or artifact proof | Repository-native tests, builds, linters, type checks, generators, schema checks, and link checks | None |

## Named-gap record

Before switching owners, record:

- established evidence;
- the missing fact;
- why the primary owner cannot provide it;
- the next owner and the single query it must answer.

Reassurance, habit, tool availability, and independent repetition are not gaps.

## Handoff

Give a subagent or reviewer the established evidence, covered scope, freshness state, and one unresolved lane. Prohibit rediscovery of covered files, symbols, flows, documents, and contracts. Route multi-phase state to `/alaa-workflow` or `$alaa-workflow`, and fan-out mechanics to the runtime orchestrator.

## Worktrees and proof

Resolve index freshness, Serena activation, diff, generated state, runtime evidence, and validation against the active worktree. Tool output is evidence, not completion; native gates decide completion.
