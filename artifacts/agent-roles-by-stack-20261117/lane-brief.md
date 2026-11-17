# Specialist rewrite: shared lane brief

Read this file in full before the first edit. Your dispatch names your roles.

## Goal

Rewrite each assigned agent definition so that the executing agent behaves the same, or more reliably, with fewer words. Remove instructions that change nothing. Record every removed or merged rule in a ledger row. The pack owner asked for a rewrite with pruning, not a cautious dedup: a result that only removes duplicates is too light.

## Files

For each role you own two files, and you keep them equal in behaviour:

- Claude: `skills/sohrab/alaa-cc-orchestrator/agents/<role>.md` (YAML frontmatter, then the body).
- Codex: `skills/sohrab/alaa-codex-orchestrator/agents/<role>.toml`. The body is one JSON string. Read and write it only with the helper:
  - `python3 artifacts/agent-roles-by-stack-20261117/tools/codex_body.py get <toml>` prints the body.
  - `python3 artifacts/agent-roles-by-stack-20261117/tools/codex_body.py set <toml> <body-file>` replaces it. Write the body file under the scratch directory your dispatch names, never in the repository.

Three bodies come from an asset, not from the agent file. Edit the asset; the lead renders the agents:

- Planner, both packs: `assets/planner-contract.md`.
- Codex reviewer: `skills/sohrab/alaa-codex-orchestrator/assets/reviewer-contract.md`. The Claude reviewer is the hand-written `alaa-reviewer.md`.
- Rule-writer: `skills/sohrab/alaa-prompting-guide/assets/rule-writer/contract.md`. Its two wrappers under `assets/rule-writer/claude/` and `assets/rule-writer/codex/` must carry a body equal to the contract (check G5): update all three.

The Codex body differs from the Claude body only in mechanics. Keep these differences and add no other:

- Codex says "load /skill" where Claude says "apply the preloaded /skill", because Codex has no preload.
- Codex keeps `- Start no subagent: the lead owns every dispatch. Return work that needs another lane.` Claude enforces it through its tool list.
- Codex ends with the paragraph that begins "Before the first source search in a repository whose root holds `.codegraph/`".
- Codex says "the shell" where Claude says "Bash", and names `alaa-codex-orchestrator` where Claude names `alaa-cc-orchestrator`.
- Five Codex roles still fold "Use the shell only to inspect and to run authorized checks" into a read-only bullet. Remove that clause there: `Effective authority` now states it.

## Shared blocks: do not edit

The lead already rewrote these in every file. Leave each one byte-identical:

- the `Task controls:` paragraph;
- the `Effective authority:` paragraph, which now ends with the single read-only sentence of a read-only role;
- the `Output rule:` paragraph;
- the `Return protocol:` paragraph and the first-line token of the output contract;
- in `alaa-documenter`, the `Task tracking:` block and its checkpoint fence.

## What to remove or merge

Apply the compress pass of `skills/sohrab/alaa-prompting-guide/references/60-skill-authoring.md` (*The draft-then-compress loop*, *ASD-STE100 style*, *The wording is the mechanism*), then prune:

1. A read-only restatement. `Effective authority` states once that the role is read-only and what Bash may do. Remove "Read-only." and "Never edit a file" from the role's own bullets, and keep only what the bullet adds (for example "never apply a fix", "accept no intent as evidence").
2. A sentence that repeats the frontmatter `description`, another sentence of the same file, or an output-contract item.
3. A motivational or generic sentence that names no observable action ("its precision is the deliverable", "go breadth first").
4. In the Claude file only: "apply /X when installed" for a skill that `skills:` already preloads. Keep any scope the sentence carries ("for Go", "when the change touches its surface") as a condition.
5. List items that differ only in wording: merge them.
6. A generic method step that a capable model performs unprompted and that sets no threshold, scope or stop condition. Judge each one: when you can name what the agent would do differently without it, keep it.

## Never remove or weaken

- A verdict token, the first-line format, an output-contract item or `NOT ASSESSED`.
- A floor, a gate, an authority limit, a stop condition, a security clause, a threshold, a number, a dated source.
- The lens boundary against an adjacent role ("the adversarial lens belongs to `alaa-adversarial-reviewer`").
- "Report every finding, including uncertain and low-severity ones": the lead ranks later and never sees a withheld finding.
- `alaa-architecture-critic`: every clause of its cadence paragraph. A checker pins them.
- `alaa-verifier`: the execution protocol and the whole output schema. Both packs' checkers pin them, each for both runtimes.
- `alaa-verifier` and `alaa-instruction-reviewer` hold no `Skill` tool: never add a `/skill` call to their bodies, and never change their `skills:` list.
- The reason attached to a rule.

Change no rule's force: no new rule, no broader scope, no narrower exception.

## Words each pack forbids

A validator rejects these words anywhere in a pack's files:

- Claude pack: `codex`, `gpt-5`, `gpt-6`, `openai`, `sol`, `terra`, `luna`, `astra`.
- Codex pack: `claude`, `opus`, `sonnet`, `fable`, `haiku`, `anthropic`.

## Preload changes

Where your dispatch lists a preload change for a role, edit the Claude frontmatter `skills:` list and add one sentence to the body, in both runtimes, that calls each moved skill with an observable condition. Write it as a call, in this form:

> Before you judge, load the clean-code owner of each stack in the diff: /alaa-php-clean-code for PHP, /alaa-vue-typescript-clean-code for Vue or TypeScript, /alaa-golang-clean-code-principles for Go.

The Codex twin usually names these skills already; align its wording and conditions with the Claude sentence. A line that calls a skill must carry no backticked path, because the reference checker reads such a path as a claim about that skill.

## Worked example

Before (`alaa-spec-analyst`, 1,150 characters):

> You are the specification gate that runs before any implementation lane is dispatched. From the goal in the user's words and the repository, produce a checkable acceptance contract and a proposed lane decomposition. The rest of the pipeline is graded against your output, so its precision is the deliverable.
>
> Authority:
> - Read-only. Do not edit files, write tests, scaffold code or design the implementation. Name no internal class and prescribe no solution shape beyond what the boundary requires.
> - Invent no product decision and resolve no ambiguity by preference: present the alternatives with their tradeoffs and let the user decide.
> - Ground every criterion in repository state inspected in this run or in the request's own words. Label inferences.
> - Absence of evidence does not prove that a constraint is absent: record it as an unknown.

After (about 640 characters):

> You are the specification gate that runs before any implementation lane. From the goal in the user's words and the repository, produce a checkable acceptance contract and a proposed lane decomposition.
>
> Authority:
> - Write no test, scaffold no code and design no implementation: name no internal class and prescribe no solution shape beyond what the boundary requires.
> - Ground every criterion in repository state inspected in this run or in the request's own words. Label inferences. Absence of evidence is an unknown, never proof that a constraint is absent.

What went and why: the motivational sentence (rule 3); "Read-only. Do not edit files" (rule 1); the product-decision bullet, because the Method list already says "Stop at each decision that belongs to the user" (rule 2). What stayed: the design prohibition, the grounding rule and the unknown rule, each with its scope.

## Checks you run

Run these from the repository root after your last edit, and repair only failures in your own files:

- `python3 skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_contracts.py`
- `python3 skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_contracts.py`
- `python3 skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_grants.py`
- `python3 scripts/check_fleet_references.py`
- rule-writer owner only: `python3 scripts/check_rule_writer_grants.py`, run inside `skills/sohrab/alaa-prompting-guide`.

Do not run `render_agents.py` or `validate_pack.py`: the manifest hashes change with every edit, and the lead renders once after all lanes return. Another lane edits other files at the same time; a failure that names a file outside your set is not yours: report it and continue.

## Boundaries

- Edit only the files of your roles. Edit no checker, catalog, manifest, routing file, changelog or generated agent.
- Run no git command that writes. Return your work uncommitted; the lead commits it.
- Run no `bd` command.
- Create no fixture, self-test or comparison.

## Return

First line: `STATUS: COMPLETE`, `STATUS: INCOMPLETE` or `STATUS: BLOCKED`, then one sentence. Then:

1. One line per role: characters before and after for the Claude file and for the Codex body.
2. Ledger: one row per removed or merged rule, as `role | removed or merged text (short) | reason (rule number above) | where the behaviour now lives, or "none: no behaviour"`. Write the rows to `artifacts/agent-roles-by-stack-20261117/ledger-<lane>.md` and return the path.
3. Each frontmatter `skills:` change.
4. Check results: command and exit code.
5. Anything you kept although it looked removable, when the reason is not obvious, and anything you could not decide.
