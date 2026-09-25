# Skill Authoring

A skill is an execution contract, not a document. It states who the agent is for the duration of the task, what outcome counts as done, what it may and may not touch, how it validates its own work, and when it stops. The frontmatter is how the runtime finds and loads that contract, the `description` is how the model decides the contract applies, and the body is the contract itself. One package serves both runtimes: Claude Code implements the Agent Skills open standard and Codex reads the same `SKILL.md` shape.

When you are about to choose a directory layout, a discovery path, a frontmatter key, or a description length, read `references/61-skill-platform-mechanics.md` — every per-runtime value lives there and none is restated here. When a generated example must name a skill so that the skill actually activates, read `references/06-invocation-and-composition.md` for the invocation rule.

## Should this be a skill at all?

Four artifacts compete for the same job, and choosing wrong is the most common authoring defect. Decide by what the content is conditional on and who owns the context.

- **A plain instruction** belongs in the prompt when it applies to one task and will never be reused. Do not package a one-off.
- **An instruction file** (`AGENTS.md`, `CLAUDE.md`) holds what is true for *every* task in the repository, because it is always loaded and therefore always costs context. When the content is unconditional, read `references/70-agent-instruction-files.md` instead of continuing here.
- **A skill** holds a procedure or body of knowledge that applies *conditionally* — to some tasks, in some repositories — and costs nothing until it applies. Claude Code's own guidance is explicit: a section of `CLAUDE.md` that has grown into a procedure should become a skill, because a skill's body loads only when used.
- **A subagent** is right when the work needs its own context window, its own tool set, or an authority boundary the caller cannot cross. A skill changes how the current agent behaves; a subagent creates a different agent. When the answer is a subagent, read `references/80-subagent-authoring.md`.

The test in one line: if the answer to "when does this apply?" is "always," it is an instruction file; if it is "never again," it is a prompt; if it is "sometimes, and here is the trigger," it is a skill; if it is "when someone other than me must judge it," it is a subagent.

## The description carries the activation decision

A description that only says what a skill does under-triggers, because the model has no phrase to match a user's actual request against. A description that only says "use when" over-triggers, because nothing tells the model where the boundary is. Write all three parts:

1. **What it is**, in one noun phrase, first, so truncation cannot remove it.
2. **When to use it**, in the verbs a user would actually type, not the verbs you would use to describe your own architecture.
3. **When not to use it**, naming the alternative skill where one exists. This is the part authors skip and the part that stops over-triggering, because naming the alternative gives the model somewhere to go instead of only somewhere not to go.
4. **Any activation side effect.** A skill whose activation writes files must say so where the model reads before deciding, not only in the body it reads afterwards.

## Progressive disclosure

The body is always paid for; a reference is paid for only when read. Once a skill loads its content stays in context across turns, so every body line is a recurring cost.

**In the body:** the role and its authority limits; the operating modes; the decision procedure the agent walks every time; the pipeline or phase order; stop conditions; safety rules; and one-line pointers naming each reference and the condition under which to read it.

**In a reference:** anything consulted rather than followed — lookup tables, per-ecosystem command matrices, failure taxonomies, catalogs of roles or triggers, long worked examples, installation detail. If the agent needs it in one run out of five, it is a reference.

Ship deterministic work as a script rather than as prose, because a script is deterministic where a regenerated implementation is not. Reference its exact invocation from the body, state what a failure obliges the agent to do, and pre-approve it with `allowed-tools` so it runs without prompting.

## Reference decomposition

This is the procedure for designing a low-volume, high-power skill: a body small enough to pay for on every run, with the detail still reachable when it is needed. Run it whenever a skill's subject is larger than one file.

1. **Partition the subject into topics that do not overlap.** A topic is a question the agent arrives with, not a heading you would like to write. Two topics overlap when the same rule would be correct in either file; merge them, or move the rule to whichever topic owns the decision it drives.
2. **Give each topic exactly one reference file.** One topic split across two files drifts, and the agent follows whichever it reads first. Two topics packed into one file force the agent to load both to use either, which is the cost the split existed to avoid.
3. **Write the pointer from the body.** A pointer sentence carries three things: the observable situation that triggers the read, the path, and what the file decides once read. Without the situation the agent cannot know when to fire it; without what it decides the agent cannot tell whether reading it would answer the question in front of it.
4. **Confirm the body now decides nothing it delegated.** A value left behind in the body after its topic moved is a second owner, and it will drift from the first.

This routes: *"When you are about to choose a frontmatter key or a description length, read `references/61-skill-platform-mechanics.md` — it holds every per-runtime value and this file states none."* This does not: *"See also `references/61-skill-platform-mechanics.md` for platform details."* Same file, same topic. The second names no situation, so it fires either never or on every run, and "details" describes no decision the agent could be looking for.

The cost model decides it. Inlining a failure taxonomy into the body charges every run for it, including the four runs in five that never fail a check; moving it behind a pointer charges one line and buys the whole file conditionally.

Where the router itself lives — as a table in the body, or in its own file — is set by reference count, not by feel. **A skill with eight or fewer references carries the router in the body as a table and ships no separate router file; a skill with nine or more moves it into `references/00-topic-map.md` and leaves exactly one pointer line in the body.** The threshold is about always-loaded cost, not about whether routing matters: a router in the body reaches the agent with no second read and is the better placement whenever the body can afford it. Crossing the threshold in either direction *moves* the router and never duplicates it, because two routers in one skill drift and the agent follows whichever it reads first. A repository may pin a different threshold or filename in its own contract; where it does, that contract wins.

## The draft-then-compress loop

**The first text you write for any artifact that controls another agent's behavior is a draft, never the deliverable.** The shipped text is a deliberate rewrite of that draft: shorter, denser, fewer words, equal or greater power. Power is execution fidelity to the same intent — clearer, more precise, less ambiguous wording that makes the same behavior more reliable. It never authorizes stronger normative force, a new rule, a broader scope, a narrower exception, or a change to a threshold, an authority, a precedence, or a behavior; any change in a rule's force fails, weaker or stronger alike. A first draft shipped unrewritten is the defect this procedure exists to catch, and it survives review because a first draft reads fine — it is complete, it is accurate, and it is two to three times longer than the contract inside it. This applies to a repair as much as to a new artifact: an edited paragraph is a draft until it has been through pass two.

**Pass one — draft.** Get every decision onto the page. Write the rule, the scope it applies to, its reason, its stop condition, and the case that made you write it. Do not compress, do not remove a repetition, do not stop to phrase anything well. A decision omitted because it seemed obvious is the one the agent will get wrong, and no later pass can recover a decision that was never written down.

**Pass two — compress.** Rewrite the draft, applying these in order:

1. Delete a sentence stating a rule already stated elsewhere in the file, keeping the statement in the section that owns it.
2. Delete a sentence that explains why the skill is worth having, reassures the reader, or previews what the next section will say.
3. Delete an example that repeats a rule already given in prose without adding a case the rule does not cover.
4. Collapse list items that differ only in wording into one item.
5. Replace a paragraph of narration with the rule it was narrating, stated before its rationale.
6. Cut a qualifier that changes no behavior — "generally", "it is worth noting", "in most cases" — unless the qualifier is the rule's scope.

**Never remove or weaken any of these, at any compression ratio:** a rule or obligation; a condition or trigger; an exception; a decision boundary or threshold; the scope a constraint applies to; the alternative a prohibition names; the reason attached to a rule; a stop condition; an authority limit; a source or verification date; or any other text whose change can alter agent behavior. The catch-all governs and the examples are non-exhaustive, because no list of kinds can cover every way a sentence carries behavior. Weakening is removal by another route — a constraint verb replaced by a preference verb, a scope or a trigger replaced by silence, two rules merged into one general rule that decides neither case. Each is load-bearing exactly when the agent is under pressure from a conflicting instruction, and each looks like padding while you are cutting. A shorter file that lost one of them is a worse file, not a leaner one.

**A compress pass relocates nothing.** Moving a rule can change its scope, its precedence, its loading condition, or its ownership, and each of those alters behavior with no word lost. A move is a separate change with its own reason and its own review. Cutting a rule because another file should own it, without the edit that puts it there, deletes it.

**The done-test for the rewrite: the executing agent's behavior is unchanged.** Every sentence removed and every word replaced must leave it unchanged. Apply the test by walking the shipped text as the agent and naming, for each cut and each substitution, what it would now do differently; restore the original whenever you can name something. The rewrite is finished when the next change you can find fails this test. A word count is not this test — a file can lose 40% of its words and one stop condition, and the word count reports a success.

**A soft target yields; a hard limit does not.** An author target, a recommended line count, or a default word budget yields when required behavior-affecting content does not fit: exceed it, say so, and compress the rest as normal — yielding is never permission to stop compressing. A limit that rejects or truncates the artifact, such as a packaging validator or a runtime byte budget, cannot yield: meet it by restructuring without semantic loss, and report blocked when no restructuring satisfies both. Restructuring moves content, so it is a separate change with its own reason and not a compress pass.

## Lean prompts require measured behavior preservation

Current OpenAI guidance favors small routers, precise triggers, conditional reads, and lean
instructions. This supports removing duplicated instructions and irrelevant examples; it does
not prove a fixed quality or cost gain for every task. Keep every load-bearing condition,
authority boundary, required check, and caveat through the compression test above. Evaluate
changed prompts on representative tasks before calling them better.

When selecting GPT-6 guidance or evaluation criteria, read `references/12-gpt-6.md` and
`references/92-agent-evaluation.md`. Historical percentages measured on earlier prompts are
not forecasts for this pack.

## The wording is the mechanism

**In a skill the words are the executable logic**, where in ordinary software prose is only commentary around it. There is no compiler underneath to enforce what the sentence failed to say, so a rule phrased ambiguously executes ambiguously — every time the skill loads, in every session, for as long as the file survives.

Six failure modes account for most of it, and each is invisible in review because the sentence reads fine.

**Preference verbs where a constraint was meant.** "Should ideally", "try to", "prefer to avoid" are read as optional and are the first things dropped when the model is under pressure from a conflicting instruction. Write a non-negotiable rule as non-negotiable — "never", "must not", "always" — or state it as a fact about the system rather than as a request.

**Rules with no stated scope.** "Keep it concise" leaves the model to guess where. Models apply an instruction precisely where it appears and nowhere else, especially at lower effort. Name the scope: every section, every file, each finding, the final report only.

**Negative-only instruction.** "Do not use a purple gradient" moves the model to a different fixed default rather than to good judgment, because the instruction removed one option without supplying a decision procedure. Pair every prohibition with what to do instead, or replace it with the positive rule that makes the prohibition unnecessary.

**Abstract nouns standing in for observable conditions.** "Handle errors properly", "ensure good performance", "write clean code" cannot be complied with or violated, so they are decorative. Replace each with the observable: which envelope, which budget, which rule. If you cannot make it observable, you have found a decision you have not yet made.

**Constraints buried mid-paragraph.** A rule inside a long explanatory sentence is weighted like explanation. One rule per sentence, and put the rule before its rationale — the reader who stops early should still have the rule.

**Arbitrary-looking rules with no reason attached.** A rule whose purpose is invisible gets rationalized away the first time the model meets a situation the author did not anticipate. One clause of reason is usually enough to survive contact with a novel case. This is also why an example that contradicts its rule is so costly: when prose and example disagree, the example wins.

The test to apply sentence by sentence: **could a competent agent follow this exactly and still do the wrong thing?** If yes, the sentence is underspecified however well it reads. That question is worth more than any style rule, and it is why skill authoring is a judgment lane rather than a transcription lane.

## Defects and fixes

| Defect | Symptom | Fix |
|---|---|---|
| Description never triggers | The skill runs only when typed manually | Front-load a noun phrase and add the user's own trigger verbs; confirm the entry is not being shortened out of the listing |
| Description over-triggers | The skill loads on unrelated requests | Add explicit negatives and name the alternative skill; narrow the scope noun; make the skill manual-only when it should never load automatically |
| First draft shipped | The body reads well and is two to three times the length of the contract inside it | Run the compress pass and hold it to the done-test before shipping |
| Rule weakened during compression | Same rules, softer verbs; the file passes review | Diff the verbs, the scopes, and the conditions, not the word count |
| Reference nobody reads | A reference file exists and never loads | Rewrite the pointer to name the triggering situation and what the file decides |
| Lookup table in the body | Every run pays for a matrix used in one run out of five | Move the table to its own reference and leave a pointer |
| Body duplicates a reference | The same rule in two files, drifting apart | Assign one owner per rule; leave a one-line pointer where the rule used to be |
| Instruction stated more than once | Long body, degraded compliance | State each rule once; measure fidelity and required coverage |
| Skill tries to be a whole workflow | The body sprawls into phases, state files, resumable plans | Split it, and route the durable multi-phase part to a workflow skill by name in the description |
| Missing stopping conditions | Runs past the goal, or loops on an unreachable bar | Define both success-stop and blocked-stop; cap fix cycles by number |
| No failure behavior | The agent troubleshoots mid-goal instead of reporting | State the retry budget and the fallback in one sentence |
| Unbounded authority | A destructive or external action taken without asking | Enumerate what proceeds freely and what requires permission; scope installation authority to named files |
| Invented frontmatter key | Ignored in silence, or a hard packaging error | Use only documented keys — the surface per runtime is in `references/61-skill-platform-mechanics.md` |

## Checklist

1. The artifact passes the "should this be a skill" test rather than belonging in an instruction file, a prompt, or a subagent.
2. Frontmatter uses documented keys only, and any runtime-specific key is deliberate and known to be inert or rejected elsewhere.
3. The `description` front-loads what it is, gives the user's own trigger verbs, states at least one negative, names the alternative where one exists, and declares any activation side effect.
4. The description fits the caps with room to spare, and the key use case survives shortening.
5. The body carries role, goal, success criteria, constraints, authority limits, tool usage, retrieval rules, validation, output format, stop conditions, and failure behavior — each stated once.
6. Every topic has exactly one owning file, and every pointer names the situation that triggers reading it and what the file decides.
7. The shipped text is a compressed rewrite of a draft, and every cut and every substitution passes the done-test.
8. No duplicated instruction, no decorative example, no explanation of why the skill is worth having.
9. Deterministic work ships as a script with its exact invocation, pre-approved rather than described in prose.
10. Every example that names a skill follows `references/06-invocation-and-composition.md`, and every version-sensitive claim carries a source or is marked unverified.

## Freshness

Authoring structure was verified on 6 August 2026; GPT-6 guidance refreshed on 25 September 2026. No earlier generation's evaluation percentages are promised here. Every runtime value this procedure depends on — caps, budgets, frontmatter surfaces, discovery paths — is held and dated in `references/61-skill-platform-mechanics.md`.

## Sources

- [Extend Claude with skills (Claude Code)](https://code.claude.com/docs/en/skills)
- [How Claude remembers your project (Claude Code)](https://code.claude.com/docs/en/memory)
- [Build skills (OpenAI)](https://learn.chatgpt.com/docs/build-skills)
- [Latest model guide (OpenAI)](https://developers.openai.com/api/docs/guides/latest-model)

- [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
