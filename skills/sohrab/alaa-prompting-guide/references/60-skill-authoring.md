# Skill Authoring

A skill is an execution contract, not a document. It states the agent's role for the task, the outcome that counts as done, what the agent may and may not touch, how it validates its work, and when it stops. The frontmatter lets the runtime find the contract, the `description` lets the model decide that it applies, and the body is the contract. One package serves both runtimes.

- For a directory layout, a discovery path, a frontmatter key or a description length, read `references/61-skill-platform-mechanics.md`. It holds every per-runtime value; this file states none.
- When an example must name a skill so that the skill activates, read `references/06-invocation-and-composition.md`.

## Should this be a skill at all?

Decide by the answer to "when does this apply?" and by who owns the context.

| Answer | Artifact | Notes |
|---|---|---|
| "Never again": one task, no reuse | A plain instruction in the prompt | Keep work inline when the current agent has the context and the authority and would finish in a handful of tool calls |
| The steps never vary and need no judgment | A deterministic script | More reliable than an agent, and it costs no tokens |
| "Always": true for every task in the repository | An instruction file (`AGENTS.md`, `CLAUDE.md`) | It always loads and always costs context. Read `references/70-agent-instruction-files.md` |
| "Sometimes, and here is the trigger" | A skill | It costs nothing until it applies. A `CLAUDE.md` section that has grown into a procedure becomes a skill |
| "When someone other than me must judge it" | A subagent | Read `references/80-subagent-authoring.md` |

A subagent is right when at least one condition holds:

- the work would flood the caller's context with search results, logs or file contents it never uses again;
- the work needs a different tool set, above all a narrower one;
- an agent that did not produce the work must judge it. Only a subagent meets this condition.

A skill changes how the current agent behaves; a subagent is a different agent, and its definition can preload skills. An unneeded subagent multiplies latency and tokens, and a missing one collapses an authority boundary.

## The description carries the activation decision

Write all four parts:

1. **What it is,** in one leading noun phrase, so truncation cannot remove it.
2. **When to use it,** in the verbs a user types, not the verbs of your architecture. Without this part the skill under-triggers: the model has no phrase to match a request against.
3. **When not to use it,** naming the alternative skill where one exists. Without this part the skill over-triggers; a named alternative gives the model somewhere to go.
4. **Any activation side effect.** A skill whose activation writes files says so here, where the model reads before it decides.

## Progressive disclosure

The body is always paid for, and a loaded skill stays in context across turns. A reference is paid for only when read.

- **Body:** the role and its authority limits; the operating modes; the decision procedure the agent walks every time; the pipeline or phase order; stop conditions; safety rules; and one pointer per reference.
- **Reference:** anything consulted, not followed: lookup tables, per-ecosystem command matrices, failure taxonomies, catalogs of roles or triggers, long worked examples, installation detail. Content the agent needs in one run out of five is a reference.
- **Script:** deterministic work, because a regenerated implementation is not deterministic. The body names its exact invocation and what a failure obliges the agent to do, and `allowed-tools` pre-approves it.

## Reference decomposition

Apply this when a skill's subject is larger than one file.

1. **Partition the subject into topics that do not overlap.** A topic is a question the agent arrives with, not a heading you want to write. Two topics overlap when one rule would be correct in either file: merge them, or move the rule to the topic that owns the decision it drives.
2. **Give each topic exactly one reference file.** A topic split across two files drifts, and the agent follows the file it reads first. Two topics in one file make the agent load both to use either.
3. **Write each pointer with three parts:** the observable situation that triggers the read, the path, and what the file decides. *"When you are about to choose a frontmatter key, read `references/61-skill-platform-mechanics.md`; it holds every per-runtime value"* routes. *"See also `references/61-skill-platform-mechanics.md` for platform details"* names no situation and no decision, so it fires never or on every run.
4. **Leave in the body no value that a reference now owns.** A value left behind is a second owner, and it drifts.

**Router.** Keep one router: a body table, or an external file with one short triggered body pointer. Choose by the always-loaded cost and the routing the skill needs, never by reference count alone. Keep an existing external router unless evidence justifies a move. Repository routing and retirement rules govern.

**Relocation is a separate justified change, never compression.** Preserve every trigger and destination. Write the new pointer's trigger as the union of the situations in which each moved item applied, and add no rule during the move. A narrower pointer reaches the moved content in fewer situations, and nothing errors.

## The draft-then-compress loop

**The first text you write for an artifact that controls another agent is a draft, never the deliverable.** Ship a deliberate rewrite of it: fewer words, equal or greater power. A first draft reads fine and survives review, yet it is two to three times as long as the contract inside it. A repair follows the same loop: an edited paragraph is a draft until it passes pass two.

**Power is execution fidelity to the same intent:** clearer, more exact wording that makes the same behavior more reliable. It authorizes no stronger normative force, no new rule, no broader scope, no narrower exception, and no change to a threshold, an authority, a precedence or a behavior. A change in a rule's force fails, weaker or stronger alike.

**Pass one: draft.** Write every decision down: the rule, its scope, its reason, its stop condition, and the case that made you write it. Do not compress yet. No later pass recovers a decision that was never written, and the decision omitted as obvious is the one the agent gets wrong.

**Pass two: compress.** Rewrite the draft. Remove:

1. a sentence that states a rule already stated in the file; keep the statement in the section that owns the rule;
2. a sentence that explains why the skill is worth having, reassures the reader, or previews the next section;
3. an example that repeats a rule and adds no case the rule does not cover;
4. list items that differ only in wording; merge them into one;
5. narration; replace it with the rule it narrated, stated before its rationale;
6. a qualifier that changes no behavior ("generally", "it is worth noting", "in most cases"), unless the qualifier is the rule's scope.

**Never remove or weaken any of these, at any compression ratio:**

- a rule or obligation;
- a condition or trigger;
- an exception;
- a decision boundary or threshold;
- the scope a constraint applies to;
- the alternative a prohibition names;
- the reason attached to a rule;
- a stop condition;
- an authority limit;
- a source or verification date;
- any other text whose change can alter agent behavior. This item governs; the others are examples.

Weakening is removal by another route: a constraint verb replaced by a preference verb, a scope or a trigger replaced by silence, two rules merged into one general rule that decides neither case. Each item looks like padding while you cut, and each carries the load when a conflicting instruction presses the agent.

**A compress pass relocates nothing.** A move can change a rule's scope, precedence, loading condition or ownership with no word lost. A move is a separate change with its own reason and its own review. To cut a rule because another file should own it, without the edit that puts it there, is to delete it.

**The done-test: the executing agent's behavior is unchanged.** Walk the shipped text as the agent. For each cut and each substitution, name what the agent would now do differently, and restore the original wherever you can name something. The rewrite is finished when the next change you can find fails this test. A word count is not this test: a file can lose 40% of its words and one stop condition.

**A soft target yields; a hard limit does not.**

- A soft target is an author target, a recommended line count or a default word budget. When required behavior-affecting content does not fit, exceed the target, say so, and keep compressing the rest.
- A hard limit rejects or truncates the artifact: a packaging validator, a runtime byte budget. Meet it by restructuring without semantic loss, and report blocked when no restructuring satisfies both. Restructuring moves content, so it is a separate change, not a compress pass.

## ASD-STE100 style

Write every controlling text in ASD-STE100-style English. The style never overrides the done-test: a shorter text that changes agent behavior fails.

- Put one idea in each sentence. Write complete sentences with their articles and verbs. A slash-joined noun stack or a clause with no verb makes the reader guess how its terms relate.
- Aim for 20 words or fewer in a procedure sentence. Exceed that when a split would separate a rule from its condition, scope or reason.
- Use the active voice, and the command form for an action.
- Use one term for one concept. Never rotate synonyms.
- Remove filler and idioms.
- Keep technical names, paths, commands and numbers exact.

## The wording is the mechanism

In a skill the words are the executable logic. No compiler enforces what a sentence failed to say. Test each sentence: **could a competent agent follow this exactly and still do the wrong thing?** If yes, the sentence is underspecified however well it reads. That question outranks any style rule. Six failure modes cause most hits, and each reads fine in review:

| Failure | What happens | Write instead |
|---|---|---|
| A preference verb where a constraint was meant: "should ideally", "try to", "prefer to avoid" | It reads as optional and is dropped first under a conflicting instruction | "never", "must not", "always", or a fact about the system |
| A rule with no stated scope: "Keep it concise" | A model applies an instruction where it appears and nowhere else, above all at lower effort | Name the scope: every section, every file, each finding, the final report only |
| A negative-only instruction: "Do not use a purple gradient" | The model moves to a different fixed default, not to judgment | Pair the prohibition with what to do, or write the positive rule that makes it unnecessary. Keep a bare prohibition only for a real boundary, where no alternative action exists |
| An abstract noun for an observable condition: "handle errors properly", "write clean code" | It can be neither complied with nor violated | The observable: which envelope, which budget, which rule. If you cannot name one, you have found a decision you have not made |
| A constraint buried mid-paragraph | It is weighted like explanation | One rule per sentence, the rule before its rationale |
| A rule that looks arbitrary and has no reason | It is rationalized away at the first unanticipated case | One clause of reason. A rule whose rationale is obvious needs none; a rule that looks like a preference needs one |

When prose and example disagree, the example wins. Never ship an example that contradicts its rule.

## Evidence for instruction changes

- Extend the done-test walk to the ordinary, ambiguous and conflicting cases that the change touches. Choose cases in proportion to the changed decisions and the cost of a wrong outcome.
- For each case, trace which owner the recipient selects and loads, what scope and authority it has, when inherited review runs, and what evidence it can report. Compare each decision with the intended contract, and resolve discrepancies before you ship.
- Report static checks, source walkthroughs and observed agent runs separately. A static check establishes only the properties it checks. A walkthrough traces expected decisions from source. A claim about actual execution needs an observed run on the target surface.

**Optional comparative evaluation.** This protocol is optional and is no dispatch admission requirement. When a comparison is authorized:

- define the question and the acceptance criteria before the run;
- use representative tasks, held-out cases included;
- match initial state, context, tools and authority across variants, except for the factor under comparison;
- separate first-attempt success from success after repair;
- record whole-task cost, elapsed time, interventions, failures and supporting evidence, repairs included;
- disclose differences that limit attribution;
- apply `alaa-testing-strategy references/110-execution-resources.md` for comparative timing.

## Carry-over review for a new model generation

Run this review when a controlling text written for an earlier model will run on a newer one: a prompt, a skill, an agent file, an instruction file, a memory or a note.

- **A carry-over repair is a deliberate behavior change, and the done-test does not judge it.** Judge it against the target model's reference and the declared intent of the text. Leave every other rule's behavior unchanged.
- **Record each removal:** the rule removed and the reason.
- **Apply a check only when the target model's reference documents the behavior,** and take the repair from that reference: `references/43-fable-5-2.md` for Fable 5.2, `references/12-gpt-6.md` for GPT-6. Report an undocumented check as not applicable. The stale-fact check applies to every model: replace the fact from the current source and date it.
- **A model upgrade removes no required test, independent gate, stop condition or authority limit.** `references/80-subagent-authoring.md` owns that distinction.

| Check | Hit |
|---|---|
| Stale fact | A model name, version gate, default, limit or runtime behavior that the current source contradicts |
| Standing delegation | A line that tells the agent to delegate and states no cost, no criteria and no case for inline work |
| Absolute approval rule | "never" on an action the agent must keep through approval. A "never" that states a true invariant is not a hit |
| Thinking control in prose | A line that asks for less thinking, or asks the agent to write out its reasoning |
| Token budget in the text | A token budget shown to the executing agent |
| Hard style limit | A word or sentence cap with no exception |
| Expired caution | A caution, note or stop condition whose stated reason no longer holds, or that states no scope or no reason |
| Default-behaviour instruction | A line that tells the model to do what the weakest model loading the file does without being told. Source: [OpenAI skills blog](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), 16 November 2026 (remove instructions for behavior the model now does itself) |
| Step-by-step itinerary | A procedure that fixes an order where order does not affect correctness. Source: the same blog, 16 November 2026 ("Avoid writing skills as step-by-step itineraries") |

When a caution or stop condition states no reason, add its scope and reason, or ask its owner. Delete it only when its reason is stated and the evidence shows that the reason no longer holds.

## Defects and fixes

| Symptom | Fix |
|---|---|
| The skill runs only when typed manually | Front-load a noun phrase and add the user's own trigger verbs. Confirm that the listing does not shorten the entry away |
| The skill loads on unrelated requests | Add explicit negatives and name the alternative skill. Narrow the scope noun. Make the skill manual-only when it must never load automatically |
| After compression the file has the same rules with softer verbs, and it passes review | Diff the verbs, the scopes and the conditions, not the word count |
| The body sprawls into phases, state files and resumable plans | Split it, and route the durable multi-phase part to a workflow skill by name in the description |
| The agent runs past the goal, or loops on an unreachable bar | Define a success stop and a blocked stop. Require a new stated reason for each further fix or review round, and a change of approach when the same kind of defect returns |
| The agent troubleshoots mid-goal and does not report | State the retry budget and the fallback in one sentence |
| A destructive or external action runs without a question | List what proceeds freely and what needs permission. Scope installation authority to named files |

## Freshness

Authoring structure was verified 6 August 2026 and GPT-6 guidance 25 September 2026. The carry-over review and the sentence-length default follow the Fable 5.2 prompting page fetched 14 November 2026. `references/12-gpt-6.md` holds the vendor lean-prompt guidance; percentages measured on earlier prompts forecast nothing for this pack.

## Sources

- [Extend Claude with skills (Claude Code)](https://code.claude.com/docs/en/skills)
- [How Claude remembers your project (Claude Code)](https://code.claude.com/docs/en/memory)
- [Build skills (OpenAI)](https://learn.chatgpt.com/docs/build-skills)
- [Latest model guide (OpenAI)](https://developers.openai.com/api/docs/guides/latest-model)
- [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
