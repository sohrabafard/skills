# Independent instruction review of the 5.8.0 follow-ups: VERDICT: CHANGES-REQUESTED
## Findings to repair (apply each replacement text exactly unless a file forces a difference; report every deviation)

1. major. `alaa-cc-orchestrator/references/delegation-prompts.md`, the read-back paragraph, and the mirrored Codex copy.
   Why: the rule requires a model parameter "whose values equal the pair in `<task_controls>`". That field records the model ID, while `model-effort-policy.md` says the Claude Code Agent invocation accepts a family alias only. A correct invocation fails the read-back literally.
   Replace the second sentence in both runtimes: "It must carry a model parameter and an effort parameter that realize the pair in `<task_controls>`: the effort value equals the recorded effort, and the model value is the identifier or alias that `model-effort-policy.md` maps to the recorded model."
   Change `alaa-cc-orchestrator/references/delegation-prompts/30-implementation.md` to: "pass the recorded effort as the `effort` parameter and the recorded model's alias, as `model-effort-policy.md` maps it, as the `model` parameter of the verified Agent invocation."

2. major. `alaa-cc-orchestrator/references/model-effort-policy.md`, the new omission paragraph.
   Why: it is a runtime-control fact in an orchestrator file. `/alaa-prompting-guide` owns runtime control mechanics, and `alaa-prompting-guide references/41-claude-code-runtime-features.md` line 12 already states the precedence, with exceptions the copy drops (the version caveat about the environment variable's priority, `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`, the fork and `model: inherit` exceptions).
   Move the omission facts (the session effort fallback and the Workflow `agent()` model order) into file 41 beside line 12, with their sources and read date. Replace the paragraph in the orchestrator file with: "An omitted parameter does not resolve to this default. It falls through the runtime precedence that `alaa-prompting-guide references/41-claude-code-runtime-features.md` owns, which usually ends at the session's model and effort. Supply both parameters on every dispatch."

3. minor. `alaa-codex-orchestrator/SKILL.md` Dispatch discipline.
   Why: the documentation does not state Codex behaviour at the limit or the default number, and the paragraph restates the key and alias that prompting-guide file 11 owns.
   In the shared sentence, do not state as documented fact that a call at the limit fails in Codex. Replace the Codex mechanics, from "In Codex," to the stamp, with: "In Codex, the limit counts open spawned-agent threads, and closing a completed thread is its own operation. Read the effective limit from `agents.max_concurrent_threads_per_session` in the active configuration. When it is unset, treat the live count at the first limit error as the limit for this session. A call at the limit failed in observed sessions; the documentation does not describe that behaviour. To free a slot, close the thread of a completed lane that Gate economics in `references/verification-and-gates.md` will not continue. When none qualifies, wait for a running lane to finish. `alaa-prompting-guide references/11-codex-runtime-features.md` owns the key, its alias and the default."

4. minor. `alaa-cc-orchestrator/SKILL.md` Dispatch discipline.
   Why: the paragraph says file 41 owns the limit values and variables, then states runtime facts that file 41 does not hold (the error text; "a run can pause at a usage limit and continue after the reset").
   Move the error text and the Workflow pause fact into file 41 with their source and read date. Replace from "In Claude Code," to the stamp with: "In Claude Code, running subagents count against the limit, and the Agent tool refuses a spawn at the limit; its error says not to retry. Free a slot by waiting for a running lane to finish. `alaa-prompting-guide references/41-claude-code-runtime-features.md` owns the limit values, the error text and Workflow-run limits."

5. minor. Both SKILL.md files, the usage-limit sentence.
   Why: a usage-limited writer is a stopped writer, and `routing-matrix.md` requires the stopped-writer recovery before a writer is replaced.
   Replace in both: "On a usage-limit error, record the lane's last evidence in the plan or compact dispatch, apply section 3's interruption rule and the stopped-writer recovery that `routing-matrix.md` cites, then re-dispatch only the remaining scope."

6. minor. `alaa-prompting-guide/references/11-codex-runtime-features.md`, Caveats.
   Why: the sentence calls the item "the former `agents.max_threads` (6) default, now the legacy alias" and lists it among "current published values".
   Replace that item with: "the `agents.max_depth` (1) and `agents.job_max_runtime_seconds` (1800) defaults (the former `agents.max_threads` (6) default is superseded; see Subagents)".

7. nit. `alaa-prompting-guide/references/00-source-map.md` line 11.
   Add the two learn.chatgpt.com pages (subagents, config reference) to the Codex line, and keep the old entries.

## Also repair (reported earlier by the implementer, not yet changed)
8. `alaa-prompting-guide/references/41-claude-code-runtime-features.md`, the Workflow size guideline: it says `medium` is fewer than 15 agents and the default is `unrestricted`; the implementer read on the current workflows page that `medium` is fewer than 10 and the default is `medium` (`small` on Pro). Re-read the page and correct the statement with its source and read date; if the page does not state it, leave it and report.

## Accepted by the reviewer
The three binding repairs; the read-back rule does not conflict with "Normalize omitted controls"; the fan-out rule is observable in Claude Code and agrees with Gate economics; every `alaa-implementer*` Claude Code entry preloads the testing doctrine and the Codex catalog claims no preload; files 41 and 11 are internally consistent apart from finding 6.

## Dispositions
All eight items were repaired by the implementer lane. Deviations: file 41 already stated the session-effort fallback, so only the Workflow model order moved there; the shared fan-out sentence says a call at the limit "can fail". The reviewer's confirmation pass returned APPROVED-WITH-NITS: all seven findings confirmed; one minor contradiction and two nits in the new file-41 text were then repaired by the parent (the pause parenthesis, a doubled verification stamp, the Pro-plan wording). The reviewer also confirmed the three stack-binding repairs of its previous pass.
