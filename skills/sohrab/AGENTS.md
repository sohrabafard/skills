# Working in `skills/sohrab/`

You maintain and extend a production skill library. Every file here is executable logic for another agent. No compiler runs underneath. A sentence that reads well but decides nothing becomes a behaviour defect on every future run. Treat prose as code.

The services these skills govern are production, security-sensitive and high-concurrency. They carry an SLA above 99.99%. A skill that produces inconsistent work across a growing microservice fleet costs more than any single clever local rule saves.

## Before you change anything

Read the skill you are changing in full: `SKILL.md`, every reference, and every script as code. A skill is a single contract. Editing one file without reading the others can state the same rule twice, and the copies then drift.

Then read `README.fa.md` for the routing map. Read the owning skill for anything your change touches. The ownership boundaries in the next section are settled. Do not re-litigate them inside a file.

## Ownership — settled, and binding on both sides

A rule has exactly one owning file. When two skills state the same rule, one of them is wrong.

**One pair is the deliberate exception.** `alaa-cc-orchestrator` and `alaa-codex-orchestrator` are one skill for two runtimes. Their behaviour is identical by design. A behavioural rule added to one is added to the other in the same change. An unexplained divergence between them is drift, not ownership. Only two things may differ:

- the mechanics, expressed in each runtime's own idiom;
- delegation polarity, which stays matched to each target family, because flattening it yields either a swarm or a single-threaded session, and neither errors.

Do not "fix" that duplication. `alaa-workflow` is the layer above both: plans, resumable state, phase prompts. It takes no copy of an orchestrator rule. It points at the pair.

| Contested ground | Owner | The other side |
|---|---|---|
| Telemetry **names and values** — log fields, event and code names, metric families, `OTEL_*` defaults | `alaa-services-contract` | `alaa-observability-soc` points here |
| Telemetry **requirement levels, gates, reasons** | `alaa-observability-soc` | `alaa-services-contract` points here |
| Contract **shapes** — wire formats, header names, activation gates | `alaa-services-contract` | `alaa-security-review` points here |
| Security **review triggers, threat classes, fail-closed doctrine** | `alaa-security-review` | `alaa-services-contract` points here |
| Shared-infra **canonical names, ports, reuse obligation** | `alaa-services-contract` | `service-runtime-kit-governance` owns only which generator variable expresses each |
| **Ala platform values** — timeouts, pool sizes, retry budgets | `alaa-services-contract` `references/22-…` | `alaa-reliability-sla` owns the doctrine and states no Ala number |
| Reliability **doctrine** — why a mechanism exists, how to shape it | `alaa-reliability-sla` | every other skill points here |
| The **ten-point quality bar** | `alaa-project-constitution` `references/quality-bar.md` | every other skill points here instead of restating |
| **Model/effort capability evidence, runtime mechanics and checked neutral projections** | `alaa-prompting-guide` | runtime orchestrators own actual task allocation/admission for every role; workflow records it |
| The **completion lifecycle** — what `IMPLEMENTED`, `MERGE_CANDIDATE`, `RELEASE_CANDIDATE`, and `PUBLISHED` each require | `alaa-workflow` `references/workspace-and-integration.md` | both orchestrators report the four states and point here; no skill restates a definition |

`fail-closed` and `fail-open` conflict by design. A control deciding whether a caller may act denies when it cannot decide. `alaa-security-review` owns that case. A component that merely contributes degrades when it fails. `alaa-reliability-sla` owns that case. The deciding question is what the failure lets through, never how important the component is.

## Hard rules

**Never edit anything under `vendor/`.** Those are upstream git subtrees, re-pulled periodically. A local edit collides on the next pull or is silently overwritten. Wrap a vendored skill from the owning `alaa-*` skill and point into it. Never fork it.

**Keep capability and task-selection ownership separate.** `/alaa-prompting-guide` owns supported pairs, runtime capability evidence and checked model-neutral projections. The runtime orchestrator owns the actual task model/effort and admission for every authority role. `/alaa-workflow` records it. Role identities, including model-named compatibility IDs, select no pair. Main-session configuration stays external.

**Never delete a file.** History matters. Move a retired file into `_to_delete/<YYYYMMDD>-<reason>/` at the repository root and say what you moved.

**Never hardcode a machine path or a version-sensitive number.** `D:\…` breaks on every other machine. A threshold copied from memory is stale the day it is written. Take paths as arguments. Fetch a current value from its primary source, and record the source and date beside it. The single exception is `alaa-legacy-path-map`. It alone holds legacy Windows paths and the WSL locations they map to, because translating them is its whole purpose.

**State every instruction exactly once.** Two deliberate exceptions:

- `alaa-project-constitution/assets/constitution-template.md`, which is self-contained because it travels to other repositories and must stand alone there;
- the mirrored orchestrator pair recorded under Ownership above.

Duplication between a skill and an artifact it emits is not duplication.

## Structure

**The body is always paid for; a reference is paid for only when read.** `SKILL.md` holds role, when the skill applies, the decision procedure, stop conditions, safety, and one-line pointers. Everything consulted rather than followed goes one hop away in `references/`.

**A pointer names its triggering condition.** `See also X` routes nothing. `When deciding which layer a behaviour is tested at, read X` is a routing rule.

**One router per skill.** Preserve an existing external router unless evidence justifies relocation. Choose a body table or external router by actual always-loaded cost and selective routing needs, never reference count alone. An external router has one short triggered pointer in `SKILL.md`. Relocation is a separate justified change. Preserve every trigger and destination without a second router. Follow the repository's retirement rule for superseded files.

**Every router row states an observable condition** — *"You are about to ⟨situation⟩ → read ⟨file⟩"* — never a heading mirror, because `grep '^#'` already produces a heading mirror, and it routes nothing.

**Both runtimes matter, and one call form serves both.** Claude Code and Codex both load these skills. Write a single `/name` at every cross-skill call site. The plugin build rewrites `$name` and `/name` alike to `/<plugin-namespace>:name`. A second form therefore reaches the agent as a duplicate of the first, and spends characters against the description budget measured below. The one bare `$` that stays correct is `default_prompt` in `agents/openai.yaml`. That is Codex interface metadata. No build rewrites it. `scripts/validate_sohrab_skill_pack.py` rule V8 requires it to carry the `$`. Remove it there and the gate fails.

**A dual-form call site is legacy, not an error.** Most of the pack still carries `/name` (`$name`) pairs written under the previous rule. Convert them in a file you are already editing for another reason. Never write a new one. Do not open a file only to sweep it. A pack-wide rewrite is its own change and needs its own review. No checker reports the old form, so this converges only by being applied.

**What a generated prompt must carry is a different question.** The rule above governs Markdown in this repository. Which sigil an agent writes into a prompt aimed at a particular runtime is a runtime capability claim. `alaa-prompting-guide references/06-invocation-and-composition.md` owns it.

**Cross-skill references name the owning skill**, always. Write `alaa-services-contract references/22-…`, never a bare `references/22-…`, because a bare path resolves inside the wrong skill.

**Two path notations, because a citation into a target repository is otherwise indistinguishable from a broken one.**

- `$SKILL_DIR/<path>` is a file bundled with the citing skill. It must resolve.
- `<repo>/<path>` is a path in the repository the agent is working on. It is never resolved.

Both markers were already in the tree before the notation was named. `$SKILL_DIR/` appears throughout `alaa-postman-collections` (counted with `grep -rc '\$SKILL_DIR/' skills/sohrab/alaa-postman-collections`), so this completes a convention and does not invent one. `scripts/check_fleet_references.py` implements it. Its `--help` is the authority on every rule here.

**An unmarked target-repository path is reported informationally as `I1-UNMARKED-TARGET-PATH` and fails no run — but only while no other skill is named on the same line.** Name another skill there, and the checker reads the path as a claim about that skill. It finds nothing. It promotes the same path to `R1-DANGLING-NAMED`, which does fail. A routing sentence names another skill by definition. So **a routing sentence carrying a target-repository path has no passing unmarked state and must be marked when it is written.** Every other site can be marked one citation at a time. That is the only reason the notation is adoptable at all. Batch 8's own rewrites tripped this thirteen times. One was a four-item list that wrapped at column 88. The wrap put one path in the informational class and the path beside it in the failing one. Same list, same meaning, one line-wrap apart.

**`<repo>/` is therefore unavailable inside a frontmatter `description`.** The no-angle-bracket rule under *The description is the highest-leverage line in a skill* forbids the marker's syntax. In a description, say in prose what the marker would have said.

**Deterministic work ships as a script.** Reference it from the body with its exact invocation, its exit-code meanings, and what a failure obliges the agent to do. A regenerated implementation is not deterministic.

**More than one implementation of one wire format ships a conformance harness.** When a skill carries the same format in several runtimes (a codec, a signature, a cursor, an identifier), it ships a runnable harness. The harness drives every implementation over one corpus and fails on any disagreement. The body names its exact invocation. A contract document asserting that the implementations agree is not evidence that they do. The Crockford Base32 bundle shipped four implementations under a contract claiming parity. The first execution of all four together found five divergences. Two of them produced colliding identifiers at the edge. A harness that skips an absent runtime reports the skip. It does not report a pass it did not observe. Existing harnesses (Crockford, input-normalization, permission-generator) stay, and the pack adds no new test runner; a wire format with several implementations and no harness records its corpus-parity check in its own reference, as `alaa-sms-provider-mediana` and `alaa-bale-provider` do by verifying the provider phone corpus with `cmp`.

## The wording test

Apply it to every sentence you write: **could a competent agent follow this exactly and still do the wrong thing?** If yes, the sentence is underspecified however well it reads. Six failures account for most of it:

- a preference verb where a constraint was meant — "should", "prefer", "try to" are the first words dropped under pressure;
- a rule with no stated scope — name where it applies;
- an abstract noun standing in for an observable condition — "handle errors properly" cannot be complied with or violated;
- a prohibition with no positive replacement — removing an option moves the model to a different fixed default, not to judgment;
- a constraint buried mid-paragraph — one rule per sentence, rule before rationale;
- a rule with no reason attached — an unexplained rule gets rationalised away the first time an agent meets a case you did not anticipate.

`alaa-prompting-guide/references/60-skill-authoring.md` has the full treatment and owns this subject, including the ASD-STE100 style every skill text follows: short sentences, one idea each, active voice, one term per concept.

## The description is the highest-leverage line in a skill

**Hard limit: 1024 characters, measured on the packaged description. Author target: 975.** Plugin validation rejects anything longer than the hard limit outright. It is stricter than the 1536-character listing cap the Claude Code documentation gives. That cap governs how much of an entry survives truncation in the listing, not whether the skill installs at all.

The limit applies to the packaged length, not to the length of the line in this repository. The plugin build rewrites every cross-skill call in a packaged Markdown file, frontmatter included, from `$name` or `/name` to `/<plugin-namespace>:name`. So each routing reference in a description costs the namespace plus a colon. That cost, not a mysterious counting discrepancy, once put five descriptions measuring 921 to 1001 characters on disk over the limit at install time. The namespace was `sohrab-skills`. A call cost fourteen characters. Nine calls added 126. The namespace is now `so`, and a call costs three. That is why the whole pack has room again. The cost is a property of the plugin name, not a constant. Renaming the plugin moves it. `scripts/validate_sohrab_skill_pack.py` computes the packaged length. It reports it as `N chars (M on disk, +K from call rewriting)`. It fails on the hard limit and warns past the target. `--description-target` moves the target for one run without a code edit. The target leaves room for roughly one more routing reference. A shorter description with many references can be nearer the limit than a longer one with none.

**A description carries no angle bracket, anywhere, for any purpose.** Plugin validation reads the description as markup. `<video>` written as prose is parsed as an XML tag, and the skill is rejected at install time. Name the thing in words instead: "a plain HTML video element". Nothing in this repository reports this. `scripts/validate_sohrab_skill_pack.py` deliberately does not check it. The author is the only control.

Neither runtime loads a body to decide whether to load that body. Write all three parts:

- what it is, as a leading noun phrase, so truncation cannot remove it;
- when to use it, in the verbs a user would actually type;
- when **not** to use it, naming the alternative skill.

A description without a negative over-triggers. Over-triggering is what makes a library unusable.

## Before you finish

Run the skill's own validator if it ships one. Report what you observed, not what you expect. Confirm every `references/*` path named anywhere resolves. Move any `__pycache__` your test runs created into `_to_delete/`. Then verify what actually landed on disk. A successful write is not evidence. A file has silently reverted here before.

Growth needs a reason. A skill must not be larger than it was unless it gained a genuinely new capability. When it did, name the capability.

## Reporting

Lead with the outcome. The first sentence answers what happened. Then report what changed, then what remains and why. State what you could not verify as unverified. Do not assert it. A fabricated finding costs more than a missing one, because it is acted upon. Commit messages carry no `Co-Authored-By` trailer.
