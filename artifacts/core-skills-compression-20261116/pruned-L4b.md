# Pruned rules, lane L4b

Scope: `skills/sohrab/alaa-code-intelligence-routing` and `skills/sohrab/alaa-low-noise`, second pass, base `37ce87a4`.

One row per pruned rule. Codes are the criteria of `lane-brief-2.md`: P1 default behaviour, P2 itinerary, P3 ceremony, P4 restated platform fact, P5 ownership noise, P6 repeated disclaimer. No clause checker binds these two skills, so the checker column is empty in every row. A sentence that duplicated a rule kept in the same skill has no row. To restore a rule, take its text from the same file at `37ce87a4`.

## alaa-code-intelligence-routing

| File | Pruned rule | Code | Checker clause |
|---|---|---|---|
| `SKILL.md` | Name each independently answerable question before you select an owner | P2 | none |
| `SKILL.md` | Treat editing, runtime observation and proof as separate questions | P2 | none |
| `SKILL.md` | Output fields: outcome, question, changed artifacts, each observed native command and result | P3 | none |
| `SKILL.md` | Success also requires "aligned artifacts" | P3 | none |
| `references/00-topic-map.md` | Third column "Decision owned there" of the router | P5 | none |
| `references/10-routing-contract.md` | Retrieve in parallel only for independently named questions | P4 | none |
| `references/10-routing-contract.md` | Capability checklist: check the installed operation and its transport, the backend's language coverage, authority and freshness (kept: verify only the needed capability; no blanket probe) | P1 | none |
| `references/10-routing-contract.md` | After a change of scope, branch, service or configuration, or a resume, check which evidence stays valid and invalidate only the affected entries | P1 | none |
| `references/10-routing-contract.md` | Ownership list: the CodeGraph installer, stack owners, `/alaa-repo-docs`, `/alaa-workflow`, `/alaa-low-noise` and the orchestrator each own a named ground | P5 | none |
| `references/10-routing-contract.md` | The stack reference owns operation fit; the native reference owns executable eligibility | P5 | none |
| `references/10-routing-contract.md` | Answer a missing dispatch fact through its eligible owner without restarting discovery | P1 | none |
| `references/10-routing-contract.md` | Mark each attempt before its call | P3 | none |
| `references/10-routing-contract.md` | Native-edit checklist: name the behaviour and scope, use adequate evidence, inspect contracts, callers and tests, verify the worktree, preserve unrelated changes, inspect the diff | P1 | none |
| `references/10-routing-contract.md` | Do not claim that native output is equivalent without evidence | P1 | none |
| `references/10-routing-contract.md` | After a semantic mutation, inspect the resulting diff and state | P1 | none |
| `references/10-routing-contract.md` | Missing native read or parser: use an available equivalent for the actual format and dialect, and state the lost parsing or search coverage | P1 | none |
| `references/30-artifact-boundaries.md` | Live Laravel schema: runtime evidence does not replace source or completion proof | P6 | none |
| `references/40-stack-bindings.md` | Reference 90 owns sources; reference 80 owns grants; the topic map routes interface mechanics and grant enforcement | P5 | none |
| `references/40-stack-bindings.md` | `/alaa-golang`, `/alaa-frontend-developer`, `/alaa-vue-typescript-clean-code` and `/alaa-laravel-architecture` own implementation doctrine | P5 | none |
| `references/40-stack-bindings.md` | Status and version establish index and installation information | P1 | none |
| `references/40-stack-bindings.md` | An absence of log entries does not prove an absence of failures | P1 | none |
| `references/40-stack-bindings.md` | More graph calls cannot supply type diagnostics or semantic-edit guarantees | P1 | none |
| `references/40-stack-bindings.md` | Use Serena symbol search, overview, declaration, references and implementations for a separately needed semantic fact | P1 | none |
| `references/40-stack-bindings.md` | Before a runtime claim from a native alternative, verify its working directory, container, application, environment and connection | P1 | none |
| `references/40-stack-bindings.md` | Vue and Quasar source questions follow the routing contract | P5 | none |
| `references/45-native-tools.md` | Bound the scope and the output of a native command | P1 | none |
| `references/45-native-tools.md` | Saved-file CLI results do not describe unsaved buffers; reuse a suitable authorized session | P1 | none |
| `references/45-native-tools.md` | Batch compatible diagnostics; rerun only after a relevant change or for a new question; avoid repeated cold loads | P1 | none |
| `references/45-native-tools.md` | Size concurrency to the available resources and the competing work | P1 | none |
| `references/45-native-tools.md` | Command recipes for `rg`, `fd`, a known-region read, `jq`, a TOML parser and the Git identity commands (`rev-parse`, `branch --show-current`, `diff`, `diff --cached`, `show`) | P1 | none |
| `references/45-native-tools.md` | Git identifies the saved worktree and history, not the runtime service or environment | P1 | none |
| `references/45-native-tools.md` | Resolve symlinks or root aliases where identity is ambiguous | P1 | none |
| `references/45-native-tools.md` | Inspect first: Composer scripts and test configuration, the `route:list` filter options, the Go module, workspace and build tags | P2 | none |
| `references/45-native-tools.md` | A script's success covers only the property and scope that it exercised | P1 | none |
| `references/45-native-tools.md` | Stack owners retain test, type and build policy | P5 | none |
| `references/50-hooks.md` | The matcher detail per client: every tool call, or the shell tool alone (kept: copy the vendor's matcher for the client) | P4 | none |
| `references/70-project-bindings.md` | Before writing, inspect the current instructions and the ownership of generated content | P1 | none |
| `references/70-project-bindings.md` | The binding fragment imposes no import between runtime instruction files | P3 | none |
| `references/70-project-bindings.md` | Choose the Serena context by client capabilities and project lifecycle, not by transport or window | P4 | none |
| `references/70-project-bindings.md` | Reference 90 owns sources and freshness; no external setup-tree file is needed | P5 | none |
| `references/75-serena-repl.md` | The routing contract selects each question's owner; reference 90 owns sources and refresh | P5 | none |
| `references/75-serena-repl.md` | Read the current Serena instructions and API overview; reuse session objects; bound paths, output and continuations | P1 | none |
| `references/75-serena-repl.md` | Validation steps: check the startup help and schema, parse the merged configuration, inspect a retained method's help, confirm that unsupported methods follow the fallback contract, compare results after a change of mode or project | P2 | none |
| `references/80-agent-scoping.md` | The installed orchestrator owns role assignments and definitions | P5 | none |
| `references/90-source-map.md` | Reference 45 bundles native command provenance; project recipes and installed help choose exact syntax | P5 | none |

Not pruned, moved inside the references: the table rows for generated artifacts and for runtime, external and cross-repository facts now live only in `references/30-artifact-boundaries.md`; the six fallback bullets of *Finite degraded operation* are merged into the fallback column of the selection table; "in the same environment" for a proof equivalent moved from `references/45-native-tools.md` to that table.

## alaa-low-noise

| File | Pruned rule | Code | Checker clause |
|---|---|---|---|
| `SKILL.md` | Complete the real task; keep repository files as the source of truth; follow repository conventions | P1 | none |
| `SKILL.md` | Batch independent reads, searches and checks; keep dependent operations and mutations sequential | P4 | none |
| `SKILL.md` | Summarize the result, not the material | P1 | none |
| `SKILL.md` | `/alaa-repo-docs` owns documents; domain skills own implementation | P5 | none |
| `SKILL.md` | This skill defines no universal behavioural guarantees | P5 | none |
| `SKILL.md` | `## Check`: confirm six results before finishing | P3 | none |
| `references/noise-control-patterns.md` | Claude Code: prefer file and search tools to shell commands; dispatch independent searches in one turn | P4 | none |
| `references/noise-control-patterns.md` | Raw output on request: state whether it is file-local or repository-wide, identify the most relevant section first, keep unrelated outputs separate | P1 | none |
| `references/noise-control-patterns.md` | Claude Code tool parameters change between releases | P1 | none |
| `references/90-source-map.md` | Source priority: the named instruction files and the file list of this skill as separate ranks | P1 | none |
| `references/90-source-map.md` | Start with the smallest instruction set and add a rule only for a demonstrated gap; state the output shape positively and avoid model-specific rituals. Owner: `alaa-prompting-guide references/60-skill-authoring.md` | P5 | none |
| `references/model-output-profiles.md` | Do not repeat discovery to appear thorough | P1 | none |

## Corrections

| File | Correction | Source |
|---|---|---|
| `alaa-code-intelligence-routing/references/50-hooks.md` | The adoption sentence of the candidate deviation named "the checker". No such checker exists in this repository. The sentence now says: change the hook file and the register together | First-pass return L4, item 8 |
| `alaa-low-noise/references/90-source-map.md` | The Codex skills URL `developers.openai.com/codex/skills` redirects permanently. It is replaced by `https://learn.chatgpt.com/docs/build-skills`, dated 2026-11-16 | `freshness.md`, fetched 2026-11-16 |
