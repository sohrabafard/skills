# Orchestrator follow-ups and stale-fact repair (2026-11-14)

Fifth engagement of the day, after the [stack-bound roles](../orchestrator-stack-roles-20261114/report.md). Beads issue: `alaa-toicj`. This record is dated evidence; verify current repository and upstream facts before reusing a conclusion.

## Why

The stack-roles record listed five open items. Three were follow-ups a maintainer could do. The wording pass had also reported dated facts and internal contradictions in many skills and had left them, because a wording pass changes no fact. This engagement did both.

## Outcome

- **Orchestrator pair at pack version 5.8.0.** The dispatch envelope has a read-back rule for the model and effort parameters. Dispatch discipline has a rule for the runtime's concurrency limit and for a lane that ends on a usage limit. The seven generic Claude Code implementer wrappers preload the testing doctrine. Runtime mechanics live in `alaa-prompting-guide`, which the orchestrators point to.
- **Runtime facts in `alaa-prompting-guide`** re-read from the official Claude Code and Codex documentation.
- **About forty-five repairs in thirty skills**: dated external facts re-read from primary sources, and contradictions settled by each skill's own files.
- **Six late binding edits of the stack-bound roles** received their independent read; three small repairs followed.
- **Runtime load observed.** A fresh Claude Code process, asked for the agent types it has, listed all eleven `alaa-implementer*` roles, including the four stack-bound ones. This shows the definitions parse and register. It does not show how a role behaves on a task.

## Lanes and reviews

| Work | Agent | Result | Record |
|---|---|---|---|
| B: three orchestrator follow-ups and the runtime facts | general-purpose, opus/high | COMPLETE | `lanes/B.md` |
| C1: infrastructure skills | general-purpose, opus/medium | INCOMPLETE as returned; see open items | `lanes/C1.md` |
| C2: frontend skills | general-purpose, opus/medium | COMPLETE | `lanes/C2.md` |
| C3: data, messaging and Go skills | general-purpose, opus/medium | COMPLETE | `lanes/C3.md` |
| C4: backend and governance skills | general-purpose, opus/medium | COMPLETE | `lanes/C4.md` |
| External facts | `alaa-researcher` with web access, opus/medium | every fact CONFIRMED | `lanes/review-facts.md` |
| Internal repairs | `alaa-instruction-reviewer`, opus/high | CHANGES-REQUESTED (1 major, 4 minor, 3 nits), repaired, then APPROVED | `lanes/review-internal.md` |
| Orchestrator follow-ups | `alaa-instruction-reviewer`, continued | CHANGES-REQUESTED (2 major, 4 minor, 1 nit), repaired, then APPROVED-WITH-NITS, nits repaired | `lanes/review-orchestrator.md` |

Each reviewer self-reported `claude-opus-5-5` with effort unknown. A lane made no commit; the parent committed each topic.

## What the reviews caught

- A read date that covered a claim nobody had re-read (the PostgreSQL lock mode with `NOT VALID`). The sentence now attributes that part to the older measurement.
- A read-back rule that a correct Claude Code invocation could never satisfy, because the invocation carries a model alias and the plan records a model ID.
- Runtime facts written into orchestrator files. They moved to `alaa-prompting-guide`, which already held the precedence rule with its exceptions.
- A Codex statement presented as documented although it rests on observed sessions. The text now says so.
- A header that claimed a whole table was refreshed when only one column was.

## Validation observed

On `main` after the last commit of this engagement, each exited `0`: the four root checkers, the installer unittest, both orchestrators' `render_agents.py --check`, `validate_pack.py`, `check_agent_grants.py` and `check_agent_contracts.py`, the three `alaa-prompting-guide` checkers, `check_execution_contracts.py`, the constitution template check and the memory checksum. Skill validators observed at `0`: the Docker image-pinning version register, the HAProxy structure check, the design-system palette check, the IndexedDB offline validators, the repository-docs link checker on the changed files, and `shellcheck` on the POSIX template.

Not `0`, and not caused by this engagement:

- `caas-arvan-kuber` `summarize-openapi.sh --check` exits `1` on a capability-matrix row. It fails the same way before these changes.
- The `alaa-input-normalization` conformance harness exits `3` on this host: Python, TypeScript and PHP match 290 of 290, and the Go driver does not build. The Go implementation is unproven here.

No fixture, self-test or model comparison was run; the pack owner excludes them.

## Installation

The pack owner authorized installation earlier the same day. After the 5.8.0 commit the Claude Code installer updated 9 files and the Codex installer updated 2 of 37. A final Claude Code dry run reported 34 unchanged.

## Open items

### Owner decisions

1. **Lanes that commit.** The implementer contract and the commit protocol say a lane never commits. The owner's global runtime rule says lanes commit locally. In one week 145 of 209 Claude Code implementation lanes ran `git commit`.
2. **Lane start-up cost.** Carrying the admission predicates in the dispatch would cut a median of 26 to 32 tool calls before the first edit. It changes a deliberate guard.
3. **Workflow-tool effort.** The public Claude Code documentation names no effort option on a Workflow `agent()` call. The orchestrator's restricted-surface rule could therefore block Workflow lanes on effort.
4. **Kubernetes patch pins.** The kubernetes.io releases page and the project's repository tags disagree on the latest patch of each minor. The pins were left. The authoring floor of 1.34 also still covers an end-of-life minor.
5. **Domain and policy questions the files do not settle.** The keyset-pagination measurement figures; the throttle-hint wait across three provider skills; an undefined "below the floor" in the Laravel upgrade triage; a RATIFY mode the constitution workflow names and its SKILL.md does not define; the PHPantom `.lsp.json` absolute path that a test asserts; five GitLab parent guides that act as second routers; the Octane drill sentence "installing it is part of the task"; the IndexedDB thresholds; the Arvan object-storage default prompt against its SKILL.md; whether object keys count as secrets in the MinIO skill; a security fast-gate clause that names sections the table lacks; the design-system skill's downloading package runner against the Vue skill's rule; a HAProxy source row that pins a value no file contains; the caas capability-matrix row behind the failing check.
6. **`alaa-trust-gateway-auth`.** Three reported items were skipped because another session is editing that skill.

### Unverified

- `alaa-octane-performance references/full-guide.md` cites an upstream issue that now returns 404 and 410.
- One Crockford source-map finding could not be located at its cited line.

### Carried over

- The canonical "scheduling of phases and reviews" clause against five carriers that still say "phase/review scheduling".
- The Lua implementation in `alaa-crockford-base32-codecs` and the Go implementation in `alaa-input-normalization` are unproven on this host.

## Not done

No push. No tag. No change to commit authority.
