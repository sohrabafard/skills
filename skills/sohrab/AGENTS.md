# Working in `skills/sohrab/`

You are maintaining and extending a production skill library. Every file here is executable logic for another agent: there is no compiler underneath, so a sentence that reads well but decides nothing becomes a behaviour defect on every future run. Treat prose as code.

The services these skills govern are production, security-sensitive, high-concurrency, and carry an SLA above 99.99%. A skill that produces inconsistent work across a growing microservice fleet costs more than any single clever local rule saves.

## Before you change anything

Read the skill you are changing in full — `SKILL.md`, every reference, every script as code. A skill is a single contract; editing one file without reading the others is how the same rule ends up stated twice and drifts.

Then read `README.fa.md` for the routing map, and the owning skill for anything your change touches. The ownership boundaries in the next section are settled; do not re-litigate them inside a file.

## Ownership — settled, and binding on both sides

A rule has exactly one owning file. When two skills state the same rule, one of them is wrong.

**One pair is the deliberate exception.** `alaa-cc-orchestrator` and `alaa-codex-orchestrator` are one skill for two runtimes, and their behaviour is identical by design: a behavioural rule added to one is added to the other in the same change, and an unexplained divergence between them is drift, not ownership. Only two things may differ — the mechanics, expressed in each runtime's own idiom, and delegation polarity, which stays matched to each target family because flattening it yields either a swarm or a single-threaded session and neither errors. Do not "fix" that duplication. `alaa-workflow` is the layer above both — plans, resumable state, phase prompts — and takes no copy of an orchestrator rule; it points at the pair.

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
| **Model and effort**, every runtime capability claim | `alaa-prompting-guide` | no other skill states a model name |

`fail-closed` and `fail-open` conflict by design. A control deciding whether a caller may act denies when it cannot decide — that is `alaa-security-review`. A component that merely contributes degrades when it fails — that is `alaa-reliability-sla`. The deciding question is what the failure lets through, never how important the component is.

## Hard rules

**Never edit anything under `vendor/`.** Those are upstream git subtrees, re-pulled periodically. A local edit either collides on the next pull or is silently overwritten. Wrap a vendored skill from the owning `alaa-*` skill and point into it; never fork it.

**Never state a model name.** Not in a skill, not in a script, not in an agent definition, not in a generated artifact. Route every model, effort, and runtime-capability question to `/alaa-prompting-guide`. A pinned model name goes stale silently and gets copied forward because it looks authoritative.

**Never delete a file.** The device mount forbids `unlink`, and history matters. Move a retired file into `_to_delete/<YYYYMMDD>-<reason>/` at the repository root and say what you moved.

**Never hardcode a machine path or a version-sensitive number.** `D:\…` breaks on every other machine; a threshold copied from memory is stale the day it is written. Take paths as arguments, and fetch a current value from its primary source with the source and date recorded beside it.

**State every instruction exactly once.** Two deliberate exceptions: `alaa-project-constitution/assets/constitution-template.md`, which is self-contained because it travels to other repositories and must stand alone there; and the mirrored orchestrator pair recorded under Ownership above. Duplication between a skill and an artifact it emits is not duplication.

## Structure

**The body is always paid for; a reference is paid for only when read.** `SKILL.md` holds role, when the skill applies, the decision procedure, stop conditions, safety, and one-line pointers. Everything consulted rather than followed goes one hop away in `references/`.

**A pointer names its triggering condition.** `See also X` routes nothing. `When deciding which layer a behaviour is tested at, read X` is a routing rule.

**Routing convention — one router per skill, never two.** A skill with 8 or fewer references carries the router in `SKILL.md` as a table and ships no `references/00-topic-map.md`. A skill with 9 or more moves the router into `references/00-topic-map.md` and leaves exactly one pointer line in the body. The threshold is about always-loaded cost, not about whether routing matters. `00-topic-map.md` is a house filename that neither Claude Code nor Codex loads on its own — it is reachable only because `SKILL.md` points at it — so a router in the body reaches the agent with no second read and is the better placement whenever the body can afford it. Two routers in one skill is the defect: they drift, and the agent follows whichever it reads first.

**Every router row states an observable condition** — *"You are about to ⟨situation⟩ → read ⟨file⟩"* — never a heading mirror, because `grep '^#'` already produces a heading mirror and it routes nothing.

**Do not add a `00-topic-map.md` to a skill below the threshold, and do not delete one from a skill above it.** Crossing the threshold in either direction *moves* the router; it never duplicates it, and it never drops the routing content. Removing a topic map from a skill that fell below 9 references is correct only when every row survived into the body table.

**Both runtimes matter, and one call form serves both.** Claude Code and Codex both load these skills. Write a single `/name` at every cross-skill call site: the plugin build rewrites `$name` and `/name` alike to `/<plugin-namespace>:name`, so a second form reaches the agent as a duplicate of the first while spending characters against the description budget measured below. The one bare `$` that stays correct is `default_prompt` in `agents/openai.yaml` — Codex interface metadata that no build rewrites, and which `scripts/validate_sohrab_skill_pack.py` rule V8 requires to carry it. Remove it there and the gate fails.

**A dual-form call site is legacy, not an error.** Most of the pack still carries `/name` (`$name`) pairs written under the previous rule. Convert them in a file you are already editing for another reason, never write a new one, and do not open a file only to sweep it — a pack-wide rewrite is its own change and needs its own review. No checker reports the old form, so this converges only by being applied.

**What a generated prompt must carry is a different question.** The rule above governs Markdown in this repository. Which sigil an agent writes into a prompt aimed at a particular runtime is a runtime capability claim, owned by `alaa-prompting-guide references/06-invocation-and-composition.md`.

**Cross-skill references name the owning skill**, always: `alaa-services-contract references/22-…`, never a bare `references/22-…`, because a bare path resolves inside the wrong skill.

**Two path notations, because a citation into a target repository is otherwise indistinguishable from a broken one.** `$SKILL_DIR/<path>` is a file bundled with the citing skill and must resolve; `<repo>/<path>` is a path in the repository the agent is working on and is never resolved. Both markers were already in the tree before the notation was named — `$SKILL_DIR/` throughout `alaa-postman-collections`, counted with `grep -rc '\$SKILL_DIR/' skills/sohrab/alaa-postman-collections` — so this completes a convention rather than inventing one. `scripts/check_fleet_references.py` implements it, and its `--help` is the authority on every rule here.

**An unmarked target-repository path is reported informationally as `I1-UNMARKED-TARGET-PATH` and fails no run — but only while no other skill is named on the same line.** Name another skill there and the checker reads the path as a claim about that skill, finds nothing, and promotes the same path to `R1-DANGLING-NAMED`, which does fail. A routing sentence names another skill by definition, so **a routing sentence carrying a target-repository path has no passing unmarked state and must be marked when it is written.** Every other site can be marked one citation at a time, which is the only reason the notation is adoptable at all. Batch 8's own rewrites tripped this thirteen times, once in a four-item list that wrapped at column 88 and put one path in the informational class and the path beside it in the failing one — same list, same meaning, one line-wrap apart.

**`<repo>/` is therefore unavailable inside a frontmatter `description`**, whose no-angle-bracket rule under *The description is the highest-leverage line in a skill* forbids the marker's syntax. In a description, say in prose what the marker would have said.

**Deterministic work ships as a script**, referenced from the body with its exact invocation, its exit-code meanings, and what a failure obliges the agent to do. A regenerated implementation is not deterministic.

**More than one implementation of one wire format ships a conformance harness.** When a skill carries the same format in several runtimes — a codec, a signature, a cursor, an identifier — it ships a runnable harness that drives every implementation over one corpus and fails on any disagreement, and the body names its exact invocation. A contract document asserting that the implementations agree is not evidence that they do: the Crockford Base32 bundle shipped four implementations under a contract claiming parity, and the first execution of all four together found five divergences, two of which produced colliding identifiers at the edge. A harness that skips an absent runtime reports the skip and does not report a pass it did not observe.

## The wording test

Apply it to every sentence you write: **could a competent agent follow this exactly and still do the wrong thing?** If yes, the sentence is underspecified however well it reads. Six failures account for most of it:

- a preference verb where a constraint was meant — "should", "prefer", "try to" are the first words dropped under pressure;
- a rule with no stated scope — name where it applies;
- an abstract noun standing in for an observable condition — "handle errors properly" cannot be complied with or violated;
- a prohibition with no positive replacement — removing an option moves the model to a different fixed default, not to judgment;
- a constraint buried mid-paragraph — one rule per sentence, rule before rationale;
- a rule with no reason attached — an unexplained rule gets rationalised away the first time an agent meets a case you did not anticipate.

`alaa-prompting-guide/references/60-skill-authoring.md` has the full treatment and owns this subject.

## The description is the highest-leverage line in a skill

**Hard limit: 1024 characters, measured on the packaged description. Author target: 975.** Plugin validation rejects anything longer than the hard limit outright, and it is stricter than the 1536-character listing cap the Claude Code documentation gives — that number governs how much of an entry survives truncation in the listing, not whether the skill installs at all.

The number that limit applies to is not the length of the line in this repository. The plugin build rewrites every cross-skill call in a packaged Markdown file, frontmatter included, from `$name` or `/name` to `/<plugin-namespace>:name`, so each routing reference in a description costs the namespace plus a colon. That, and not a mysterious counting discrepancy, is what once put five descriptions measuring 921 to 1001 characters on disk over the limit at install time: the namespace was `sohrab-skills`, a call cost fourteen characters, and nine of them added 126. The namespace is now `so` and a call costs three, which is why the whole pack has room again — but the cost is a property of the plugin name, not a constant, and renaming the plugin moves it. `scripts/validate_sohrab_skill_pack.py` now computes the packaged length, reports it as `N chars (M on disk, +K from call rewriting)`, fails on the hard limit and warns past the target, and `--description-target` moves the target for one run without a code edit. The target leaves room for roughly one more routing reference; a shorter description with many references can be nearer the limit than a longer one with none.

**A description carries no angle bracket, anywhere, for any purpose.** Plugin validation reads the description as markup, so `<video>` written as prose is parsed as an XML tag and the skill is rejected at install time. Name the thing in words instead — "a plain HTML video element". Nothing in this repository reports this; `scripts/validate_sohrab_skill_pack.py` deliberately does not check it, so the author is the only control.

Neither runtime loads a body to decide whether to load that body. Write all three parts: what it is as a leading noun phrase so truncation cannot remove it; when to use it in the verbs a user would actually type; and when **not** to use it, naming the alternative skill. A description without a negative over-triggers, and over-triggering is what makes a library unusable.

## Before you finish

Run the skill's own validator if it ships one, and report what you observed rather than what you expect. Confirm every `references/*` path named anywhere resolves. Move any `__pycache__` your test runs created into `_to_delete/`. Then verify what actually landed on disk — a successful write is not evidence, and a file has silently reverted here before.

Growth needs a reason. A skill must not be larger than it was unless it gained a genuinely new capability; when it did, name the capability.

## Reporting

Lead with the outcome — the first sentence answers what happened. Then what changed, then what remains and why. State what you could not verify as unverified rather than asserting it; a fabricated finding costs more than a missing one, because it is acted upon. Commit messages carry no `Co-Authored-By` trailer.
