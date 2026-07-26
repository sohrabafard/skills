# Working in `skills/sohrab/`

You are maintaining and extending a production skill library. Every file here is executable logic for another agent: there is no compiler underneath, so a sentence that reads well but decides nothing becomes a behaviour defect on every future run. Treat prose as code.

The services these skills govern are production, security-sensitive, high-concurrency, and carry an SLA above 99.99%. A skill that produces inconsistent work across a growing microservice fleet costs more than any single clever local rule saves.

## Before you change anything

Read the skill you are changing in full — `SKILL.md`, every reference, every script as code. A skill is a single contract; editing one file without reading the others is how the same rule ends up stated twice and drifts.

Then read `README.fa.md` for the routing map, and the owning skill for anything your change touches. The ownership boundaries in the next section are settled; do not re-litigate them inside a file.

## Ownership — settled, and binding on both sides

A rule has exactly one owning file. When two skills state the same rule, one of them is wrong.

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

**Never state a model name.** Not in a skill, not in a script, not in an agent definition, not in a generated artifact. Route every model, effort, and runtime-capability question to `/alaa-prompting-guide` (`$alaa-prompting-guide` in Codex). A pinned model name goes stale silently and gets copied forward because it looks authoritative.

**Never delete a file.** The device mount forbids `unlink`, and history matters. Move a retired file into `_to_delete/<YYYYMMDD>-<reason>/` at the repository root and say what you moved.

**Never hardcode a machine path or a version-sensitive number.** `D:\…` breaks on every other machine; a threshold copied from memory is stale the day it is written. Take paths as arguments, and fetch a current value from its primary source with the source and date recorded beside it.

**State every instruction exactly once.** The one deliberate exception is `alaa-project-constitution/assets/constitution-template.md`, which is self-contained because it travels to other repositories and must stand alone there. Duplication between a skill and an artifact it emits is not duplication.

## Structure

**The body is always paid for; a reference is paid for only when read.** `SKILL.md` holds role, when the skill applies, the decision procedure, stop conditions, safety, and one-line pointers. Everything consulted rather than followed goes one hop away in `references/`.

**A pointer names its triggering condition.** `See also X` routes nothing. `When deciding which layer a behaviour is tested at, read X` is a routing rule.

**Routing convention — one router per skill, never two.** A skill with 8 or fewer references carries the router in `SKILL.md` as a table and ships no `references/00-topic-map.md`. A skill with 9 or more moves the router into `references/00-topic-map.md` and leaves exactly one pointer line in the body. The threshold is about always-loaded cost, not about whether routing matters. `00-topic-map.md` is a house filename that neither Claude Code nor Codex loads on its own — it is reachable only because `SKILL.md` points at it — so a router in the body reaches the agent with no second read and is the better placement whenever the body can afford it. Two routers in one skill is the defect: they drift, and the agent follows whichever it reads first.

**Every router row states an observable condition** — *"You are about to ⟨situation⟩ → read ⟨file⟩"* — never a heading mirror, because `grep '^#'` already produces a heading mirror and it routes nothing.

**Do not add a `00-topic-map.md` to a skill below the threshold, and do not delete one from a skill above it.** Crossing the threshold in either direction *moves* the router; it never duplicates it, and it never drops the routing content. Removing a topic map from a skill that fell below 9 references is correct only when every row survived into the body table.

**Both runtimes matter.** Claude Code and Codex both load these skills. Give both trigger forms at every cross-skill call site — `/name` and `$name`. `agents/openai.yaml` is Codex-only metadata and correctly uses the bare `$`.

**Cross-skill references name the owning skill**, always: `alaa-services-contract references/22-…`, never a bare `references/22-…`, because a bare path resolves inside the wrong skill.

**Deterministic work ships as a script**, referenced from the body with its exact invocation, its exit-code meanings, and what a failure obliges the agent to do. A regenerated implementation is not deterministic.

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

**Hard limit: 1024 characters. Author target: 950.** Plugin validation rejects anything longer outright, and it is stricter than the 1536-character listing cap the Claude Code documentation gives — that number governs how much of an entry survives truncation in the listing, not whether the skill installs at all. Write to 950 so adding one clause later does not break the build. `scripts/validate_sohrab_skill_pack.py` fails on the hard limit and warns past the target.

Neither runtime loads a body to decide whether to load that body. Write all three parts: what it is as a leading noun phrase so truncation cannot remove it; when to use it in the verbs a user would actually type; and when **not** to use it, naming the alternative skill. A description without a negative over-triggers, and over-triggering is what makes a library unusable.

## Before you finish

Run the skill's own validator if it ships one, and report what you observed rather than what you expect. Confirm every `references/*` path named anywhere resolves. Move any `__pycache__` your test runs created into `_to_delete/`. Then verify what actually landed on disk — a successful write is not evidence, and a file has silently reverted here before.

Growth needs a reason. A skill must not be larger than it was unless it gained a genuinely new capability; when it did, name the capability.

## Reporting

Lead with the outcome — the first sentence answers what happened. Then what changed, then what remains and why. State what you could not verify as unverified rather than asserting it; a fabricated finding costs more than a missing one, because it is acted upon. Commit messages carry no `Co-Authored-By` trailer.
