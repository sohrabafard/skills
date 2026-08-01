# Evidence-owner routing contract

Choose one primary owner for the current question. Evidence, edit, and proof may have different owners because they answer different questions.

## Decision order

1. Split the request into independently answerable questions: discovery, exact semantics, edit, prose, effective configuration, generated output, runtime fact, external fact, review risk, or proof.
2. Classify the current artifact and verify worktree, freshness, generated owner, installed capability, environment, and authority.
3. Select one primary owner from the table and issue one query for the named question.
4. Record what the result established and stop that owner.
5. Open one secondary owner only for one recorded missing fact.
6. Treat a move to exact semantics or editing, and then to proof, as a new ordered question.

Parallel execution is allowed only when separately named questions are independent: neither answer may change the other's owner, query, authorization, or scope. Otherwise sequence them in dependency order.

## Router

| Current question | Primary owner | Secondary only for a named gap |
|---|---|---|
| Unknown location, architecture, execution flow, relationship, or likely impact in indexed supported source | CodeGraph | Serena for one exact semantic fact; targeted live read for one named stale or uncovered file |
| Exact definition, reference, implementation, hierarchy, type-aware diagnostic, or known-symbol navigation | Serena | CodeGraph only when a new wider-flow or impact question appears |
| Known small textual change in one named hand-maintained non-semantic file | Native targeted read and patch | Serena only when a separately named semantic question appears |
| Semantic rename, symbol-body replacement, or reference-safe code edit | Serena | Native patch only after the exact range is established and Serena cannot perform the operation |
| Markdown phrase or identifier across repository documents | Native search restricted to Markdown | Serena Markdown for headings after one document is named |
| Heading outline or section navigation in one known Markdown file | Serena Markdown when healthy | Targeted native read |
| Repository Markdown creation, alignment, de-duplication, navigation, or link repair | `/alaa-repo-docs` in Claude Code or `$alaa-repo-docs` in Codex | Claim-specific code, config, contract, framework, or runtime evidence |
| Source comments, docblocks, or annotations | `/alaa-frontend-doc-annotations` or `$alaa-frontend-doc-annotations` | Serena for the exact containing symbol |
| JSON, YAML, TOML, CI, environment templates, manifests, or policy text | Native scoped search/read plus parser or repository checker | Serena only for one named diagnostic question when that language is enabled |
| OpenAPI, AsyncAPI, Postman, protobuf, schema, or another machine-readable contract | Installed contract-owning skill or generator | Repository docs owner for prose summaries only |
| Generated source or generated documentation | Source template and generator | Direct edit only when repository policy declares the artifact hand-maintained |
| Installed Laravel documentation, package behavior, or authorized Laravel application context | Laravel Boost | CodeGraph or Serena only for one named source-flow or semantic gap; native commands for proof |
| Runtime logs, traces, metrics, browser state, database behavior, queue state, or cache state outside Boost | Authorized runtime owner | CodeGraph to map the observed fact to source |
| Current external framework, package, protocol, or platform behavior | Official version-aware source | Repository evidence only for local usage |
| Current change review | Git diff first | Expand only for a named risk through CodeGraph, Serena, runtime evidence, docs owner, or targeted tests |
| Cross-repository ownership, consumer, compatibility, or handoff question | Authoritative service catalog, contract registry, hosting surface, or approved memory surface | A named repository only after the authority identifies it |
| Behavioral or artifact proof | Repository-native tests, builds, linters, type checks, generators, schema checks, and link checks | None |

## Ordered composition

`Discovery -> exact semantics or edit -> proof` is a change of question, not repeated discovery. Preserve the discovery result when moving forward.

- A Laravel source-flow question starts with CodeGraph even though the source is PHP.
- A known-symbol PHP question starts with Serena.
- A Boost answer moves to CodeGraph or Serena only for a recorded source-flow or semantic gap.
- Review starts with Git diff. A named risk may open one owner query; completion returns to native gates.

## Named-gap record

Before switching owners, record:

- established evidence;
- the missing fact;
- why the primary owner cannot provide it;
- the next owner and the single query it must answer.

Reassurance, habit, tool availability, and independent repetition are not gaps.

## Degraded operation

- CodeGraph explicitly names a stale or pending affected file: read that live file directly and do not retry the graph for freshness.
- An owner is empty, unavailable, or points at another worktree: perform at most one health attempt. A health attempt checks status, activation, or root identity; it does not repeat the evidence query.
- CodeGraph cannot cover the required broad flow or impact: a targeted fallback may answer a narrower fact, but the broad result remains partial or blocked.
- Serena cannot preserve the required semantic guarantee: targeted reads may provide partial evidence, but do not describe them as reference-complete, hierarchy-complete, or refactor-safe.
- A native proof gate cannot run: report the exact command and blocker; do not substitute static evidence for proof.

## Handoff

Give a subagent, reviewer, or cross-repository handoff the established evidence, source worktree, covered scope, freshness state, proof state, and one unresolved question. Prohibit rediscovery of covered files, symbols, flows, documents, and contracts. Evidence from another checkout is unavailable until reproduced in the receiving worktree. Route durable state to `/alaa-workflow` (`$alaa-workflow`) and fan-out mechanics to the installed runtime orchestrator.

## Worktrees and proof

Resolve the Git root first. Verify that CodeGraph's project root, Serena's active project, Git diff, generated state, runtime evidence, and validation working directory resolve to that same worktree. Tool output from another checkout is unavailable. Native gates decide completion.
