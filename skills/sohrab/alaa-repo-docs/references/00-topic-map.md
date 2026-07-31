# Topic map

Each row is a condition and the one file that answers it. Read the row whose condition holds, and
only that row. No other file in this skill repeats this routing, and no combined guide exists.
A path prefixed `<repo>/` names a file in the repository being worked on; a path beginning
`references/` names a file this skill ships.

| Condition | File |
|---|---|
| You are about to choose a document language, create a localized companion, place a topic, remove duplication, or write a link | `references/10-language-and-links.md` |
| The task touches `<repo>/README.md` or `<repo>/docs/BIG_PICTURE.md`, or the reader cannot tell which of the two a fact belongs in | `references/20-readme-big-picture-contract.md` |
| The repository exposes HTTP routes and needs `<repo>/docs/api-summary.md`, or an OpenAPI contract and a summary sheet disagree | `references/30-api-summary-contract.md` |
| You need the paired-document matrix, the production workflow, the output checklist, the evidence checks, or the failure classes of this skill's own run | `references/40-sync-workflow-and-evidence.md` |
| The repository persists state and needs `<repo>/docs/data-architecture.md`, or a storage, cache, or request-walkthrough claim must be written | `references/50-data-architecture-contract.md` |
| The repository has error contracts, events, jobs, logs, traces, or metrics and needs `<repo>/docs/errors-events-observability.md` | `references/60-errors-events-observability-contract.md` |
| The refresh is broad enough to split across parallel read-only subagents, or a subagent failed or returned nothing | `references/70-subagent-doc-workflows.md` |
| A document or Postman request promises behaviour the code does not implement, and `<repo>/remaining-task.md` is needed | `references/80-implementation-gap-backlog.md` |
| A claim depends on an external format or tool rather than on repository truth | `references/90-source-map.md` |

## Working rules

- Read the smallest set of rows whose conditions hold. Loading a file whose condition does not
  hold spends context on rules that cannot bind this task, and that budget belongs to
  `/alaa-low-noise` (`$alaa-low-noise`).
- If two rows both hold, both files apply and neither overrides the other. They partition the
  subject; they do not restate each other.
- If a rule you need is in none of these files, it is not this skill's rule. Check the ownership
  table in `SKILL.md` before writing it here.
