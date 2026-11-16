# Evidence-owner routing contract

## Selection and identity

Select one primary owner per question. Reuse adequate fresh evidence first: never retrieve an answered fact again through a second surface or for reassurance.

**Eligibility.**

- Any combination of CodeGraph, Serena and Boost is valid, including one alone or none. Boost applies only to Laravel projects.
- "Not configured" and "not applicable" are normal ineligibility, not failures to repair. Skip an absent provider and never set it up. Establish an absence once, then make no call to that provider.
- Verify only the capability that the question needs. Run no blanket health probe.
- A native CLI or connected LSP operation needs no Serena, no hook and no failed Serena call first.

**Identity.** Reject evidence that comes from another Git root, worktree, branch, graph root, Serena active project or runtime environment than the claim is about. The lane-worktree rule is the one exception.

**Lane worktree.** `SKILL.md` *Operation card* owns the lane-local index. When that index could not be built, the main checkout's index answers with a different-worktree warning. Accept that result for location, relationships and impact in files the lane has not changed. Read from the worktree every file the lane changed and every region you will edit. A symbol missing from that result is not proven missing in the lane.

**Serena.** Before you select Serena, check `.serena` at the resolved project root of the target worktree, not in the shell's current directory.

- Absent: by pack policy Serena is inactive for that project, whatever host binary or MCP endpoint is exposed. Make no Serena call, activation or onboarding. Create no marker or integration without explicit setup scope.
- Status unreadable: unknown, not absent.
- Present: eligibility checks may run. Presence proves no connection, no operation support and no active-project identity. A copied marker cannot retarget an inherited HTTP binding; verify that binding separately.

**Shell.** Never use CodeGraph MCP or CLI for a Bash or shell question, also in an indexed mixed-language repository: CodeGraph does not support these languages (evidence: `references/90-source-map.md`). The rule covers discovery, source reads, relationships and impact for scripts, extensionless shell files and embedded shell commands. Use bounded native search and read. /alaa-bash-shell owns implementation and validation. Do not probe CodeGraph or retry through another graph operation. Non-shell source in the same repository keeps its normal route.

| Question | Primary owner | Fallback for a recorded gap, in order |
|---|---|---|
| Location, source, relationships, call paths or likely impact in supported indexed source, with the file or symbol known or unknown | An eligible CodeGraph MCP or CLI operation that fits the question | After an MCP transport failure, the CLI, only when it is usable against the same valid index. Another operation on that index. A supported Serena operation. Bounded native source for a narrower claim. Record the lost graph coverage |
| Binding-aware or build-aware semantics (complete references, the implementation hierarchy), diagnostics or a semantic mutation | The semantic owner that the stack declares; otherwise a supported Serena backend or an eligible native language operation. Make no graph call first | A language-native CLI or connected LSP operation that covers the same property. Targeted source for a partial read claim. A bounded native edit under *Authorized native continuation* |
| Dependency metadata, resolved module or workspace versions, or an authorized dependency upgrade | A native manifest read or parser for declared metadata; the stack's inspected dependency recipe for resolution or upgrade | An equivalent that proves the named metadata property. Discover source or semantics only for a separately named impact or API fact |
| Installed Laravel framework or package guidance | Configured Boost documentation, with the installed versions verified | Version-correct official documentation. Package source only for a separately named implementation question |
| Laravel application metadata, registered routes, URLs, logs or errors, schema or database context | An installed Boost operation or an equivalent authorized native observation | An equivalent observation in the same environment, under the failure domains of `references/40-stack-bindings.md` |
| Change review | Scoped Git diff | The selected owner for a named risk |
| Behavioral or artifact proof | Repository-native tests, types, lint, builds, generators, and schema or link checks | An authorized equivalent that proves the same acceptance property in the same environment; otherwise report the exact gate blocked |

`SKILL.md` *Operation card* owns literal text and configuration. `references/30-artifact-boundaries.md` owns generated, runtime, external and cross-repository evidence.

Known identity alone does not select Serena: for a source or structural answer, eligible CodeGraph comes first.

## Consume evidence

- A text-search miss does not establish unused code. Heuristic edges, runtime dispatch boundaries and unexplained path gaps do not establish a complete call path. Diagnostics alone do not establish complete references.
- An empty, unsupported, stale, paginated or truncated result proves neither absence nor completeness. Fetch only the continuation pages or regions that you need. When coverage cannot be established, mark the result unknown or partial.

## Finite degraded operation

Per question, keep the established evidence and the owner-operation pairs you tried. Try no pair twice, and skip one known to be unavailable. Before each fallback, record the missing fact, the failed capability and the guarantee you lose.

A failed operation gets at most one cause-specific, non-mutating repair and one materially different retry; otherwise move on. Activation, restart, unlock, sync and reindex are not non-mutating repairs. A fallback never resets the budget of the operation that failed. Missing coverage is a gap, not a health failure.

At exhaustion, give a partial answer or stop the dependent claim. Unrelated safe work may continue.

## Authorized native continuation

An authorized bounded local edit needs no Serena, gopls or other semantic provider, and no installation. Edit from adequate source evidence, then run every mandatory native gate.

- Source reads alone prove neither complete references, nor a binding-safe rename, nor refactor safety. When the action or claim requires such a property and no authorized equivalent proves it, block only that action or claim.
- Provider diagnostics are supplemental unless repository rules or the acceptance criteria require a semantic property beyond native proof. Missing optional diagnostics block neither the edit nor completion once the mandatory native gates pass. Record the gap and the lost guarantee.

## Mutation uncertainty

Before a semantic mutation, verify the task authorization, the supported operation and the target identity. After a timeout or an uncertain result of a possible mutation, reconcile the actual state before you continue. Never replay the mutation, and never substitute text editing automatically. When no safe resulting state can be established, stop that operation and report the unknown outcome. A fallback expands no authority.

A failed native gate gets one cause-specific repair and one retry within task authority; otherwise report the exact failure. No static or provider answer substitutes for an unrun gate.

## Handoff

Pass the established evidence with its owner, covered scope, worktree and environment identity and freshness, the proof state, the pairs you tried and the open facts. The recipient retrieves only the gaps.
