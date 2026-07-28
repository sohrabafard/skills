# Upgrade Batch 5 — Messaging, integrations, and trust

**Phase 1 analysis. Written 2026-07-27. This file is the executable input to Phase 2.**

Batch membership, per `UPGRADE-CARRYOVER.md` §5: `alaa-async-messaging`, `alaa-trust-gateway-auth`,
`alaa-bale-provider`, `alaa-sms-provider-mediana`, `tusd-upload-platform`, `jitsi-platform-architect`.

Method: one analysis lane per skill, each reading `SKILL.md`, every reference, every script as code,
and every asset. Scripts were executed where a runtime was available. Every claim below carries a file
and, where the lane could give one, a line. Claims that could not be checked this session are collected
in §11 and are marked unverified rather than asserted.

Repository state at the start of Phase 1: `git status --porcelain` scoped to the six skill directories
returned empty; `HEAD` is `47b0bbef fix prompt`, on top of `b920bfdb upgrade batch 4`.

Observed sizes before the rewrite:

| Skill | Body (`SKILL.md`) | References | Assets / scripts | Total |
|---|---:|---:|---:|---:|
| `alaa-async-messaging` | 11,926 B | 6,188 B (4 files) | 5,528 B (7 assets) | 23.9 KB |
| `alaa-trust-gateway-auth` | 12,262 B | 131,571 B (9 files) | — | 146 KB |
| `alaa-bale-provider` | 8,468 B | 16,052 B (2 files) | 8,328 B (1 script) | 33.1 KB |
| `alaa-sms-provider-mediana` | 15,095 B | 21,680 B (3 files) | 19,034 B (asset + script) | 56.3 KB |
| `tusd-upload-platform` | 7,571 B | 59,400 B (12 files) | ~40 KB (17 assets + script) | 151.5 KB |
| `jitsi-platform-architect` | 7,142 B | 43,682 B (6 files) | — | 63.4 KB |

---

## 1. The batch-level finding — doctrine silence, for the fourth wave running

The mandated doctrine-owner grep across all six skills, run before any lane started:

| Owner | Hits across the whole batch |
|---|---:|
| `alaa-project-constitution` | 0 |
| `alaa-reliability-sla` | 0 |
| `alaa-testing-strategy` | 0 |
| `alaa-system-design` | 0 |
| `alaa-controlled-ops` | 0 |
| `alaa-keyset-pagination` | 0 |
| `alaa-algorithms-data-structures` | 0 |
| `alaa-data-layer` | 0 |
| `alaa-prompting-guide` | 0 |
| `alaa-observability-soc` | 9 (8 of them in `alaa-trust-gateway-auth`, 1 in `tusd-upload-platform`) |
| `alaa-security-review` | 6 (all in `alaa-trust-gateway-auth`) |
| `alaa-services-contract` | 3 (2 in `alaa-trust-gateway-auth`, 1 in `tusd-upload-platform`) |

**Four of the six skills — `alaa-async-messaging`, `alaa-bale-provider`, `alaa-sms-provider-mediana`,
`jitsi-platform-architect` — name no doctrine owner at all.** This is worse than Batch 4's ten mentions
across five skills, and it is the same finding: silence reads as coverage. Every one of these skills
therefore legislates retry policy, idempotency, timeout discipline, telemetry vocabulary and test
obligations locally, at weaker strength than the owner states them, and with no precedence rule when
the two disagree.

Report it as **one** finding about the batch. The per-skill sections below give the specific lines where
each skill legislates an owner's ground, which is the actionable part.

**This batch contains one case where the local restatement does not merely weaken the owner — it
contradicts it, in the one sentence that decides whether a user receives one OTP or two.** See §5.2.

---

## 2. Criteria table — the whole batch

Legend: **S** satisfies · **F** fails · **N** not-its-ground (another named skill owns it; this skill must
route rather than state). **N** is recorded only where the owning skill is named in the per-skill notes.
A cell marked **F** for a criterion the skill genuinely owns is a coverage defect; a cell marked **F**
where the skill states an owner's rule locally is a boundary defect. Both are listed in §5.

| # | Criterion | async-messaging | trust-gateway-auth | bale-provider | sms-mediana | tusd-upload | jitsi-architect |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|
| 1 | Correctness and testability | F | F | F | F | F | F |
| 2 | Failure behaviour | F | F | F | F | F | F |
| 3 | Security | F | S | F | F | F | F |
| 4 | Observability | F | F | F | F | F | F |
| 5 | Concurrency and load | F | N | F | F | F | S |
| 6 | Clean code, SOLID, patterns | N | S | N | S | N | N |
| 7 | Algorithm and data-structure choice | N | F | N | N | F | N |
| 8 | Configurability | F | F | F | F | F | F |
| 9 | Speed of development and debuggability | F | F | F | F | F | F |
| 10 | Documentation | F | F | F | F | F | F |

Two readings of that table matter.

**Criterion 2 fails in all six.** Every skill in this batch governs a boundary between this platform and
something it does not control — a broker, a gateway, a vendor, an upload client, a media plane. Failure
behaviour is the whole reason these skills exist, and not one of them states what happens when the thing
on the other side stops answering. This is the batch's defining gap, and closing it is the largest single
piece of Phase 2 work.

**Criteria 1, 4, 9 and 10 fail in all six**, which is a shape defect rather than six separate omissions:
these are documentation-register skills that describe a system instead of constraining an agent. The
correction is the same everywhere — a required-test section, a routed telemetry contract, a failure-class
table, and an output contract stating what the agent must report.

**The one criterion that passes broadly is 6**, and it passes because the skills correctly decline to
restate code-shape doctrine. That is the right instinct; what is missing is the routing line that makes
the decline legible instead of silent.

---

## 3. Defect classes from §3 of the carry-over — what was actually found

| # | Class | Found? | Where |
|---|---|:--:|---|
| 1 | Stale hardcoded model pins | **No** | Grepped all six for every model-name pattern plus `ultrathink`/`ultracode`. Zero hits. This **corrects** the standing expectation carried in Batch 2 and Batch 3 memory that surviving pins live in "Batches 5 and 6" — none is in Batch 5. |
| 2 | Wrong trigger syntax | **Yes, inverted** | The batch does not use the *wrong* form; it uses only the `$` form or neither. `$alaa-*` appears at 20 sites; `/alaa-*` appears **once** in the entire batch, and that one occurrence (`tusd-upload-platform/references/alaa-trust-gateway.md`) names `/alaa-trust-gateway`, a skill that does not exist. Three skills contain zero cross-skill call sites of any form. |
| 3 | Duplication between body and references | **Yes, at every scale** | `alaa-trust-gateway-auth/references/full-guide.md`: **661 of 852 non-empty lines (77%)** appear elsewhere in the same skill — measured, not estimated. `alaa-sms-provider-mediana`: 43% of the always-loaded body restates `references/mediana-ippanel-api.md`, by paraphrase rather than by copy, so both copies have already drifted. `alaa-bale-provider`: three JSON blocks in the body are byte-identical to `references/examples.md`. `tusd-upload-platform`: four divergent copies of one upload state machine, five copies of "`pre-create` alone is not enough". `alaa-async-messaging`: two "mandatory" reliability lists six lines apart. `jitsi-platform-architect`: roughly a third of the body restates its references. |
| 4 | Project-specific content in an always-loaded body | **Yes, in five of six** | `alaa-trust-gateway-auth/SKILL.md:118-125` hardcodes a bitmap-id allocation register (`wa_get_watch_stats` id 1, `content_*` ids 64-78, tusd ids 92-95, entitlement ids 96-104) — service inventory in a trust-doctrine body. `alaa-async-messaging`: 87 of 248 body lines are Laravel-specific procedure. `alaa-sms-provider-mediana`: seven env values, three full JSON payloads, a ten-mode enumeration. `tusd-upload-platform/SKILL.md:27,40,43`. `jitsi-platform-architect/SKILL.md:8-31`. |
| 5 | Long numbered procedures where failure-class structure was needed | **Yes, in all six** | Every skill has at least one numbered "start sequence" or "validation checklist", and **not one** has a symptom → diagnosis → smallest safe retry → escalation structure anywhere. `alaa-async-messaging/references/troubleshooting.md` has the right shape and covers five Laravel symptoms, none of them a broker, outbox or DLQ failure. |
| 6 | Description that only says when to use | **One** | `alaa-async-messaging` (234 chars, no negative clause). The other five carry a negative clause. **All six are far under the 950-character author target**: 234 / 486 / 490 / 617 / 503 / 613. |
| 7 | Fragile tooling | **Yes** | `tusd-upload-platform/scripts/validate_pack.py:21` uses `Path(__file__).resolve().parents[1]`, and has no argument parsing at all, so `--help` is read as a root path and **exits 1 with `ERROR: SKILL.md is missing`** (observed). `alaa-trust-gateway-auth/references/30-…:5-10` gives six source documents as `D:\Sohrab\Project\auth\…` absolute paths, repeated at `full-guide.md:316-321` — the only surviving `D:\` paths in a skill body anywhere in `skills/sohrab/`. All seven `alaa-async-messaging/assets/` process files hardcode `/var/www/app`, `www-data` and `/usr/bin/php`. |
| 8 | Shipped `__pycache__` | **No** | Zero across the batch, verified on the real disk. |
| 9 | Gaps against §2 named explicitly | **Not done anywhere** | No skill in the batch states which criterion it does not own and which skill does. |
| 10 | Shrink where possible | **Yes, in all six** | Body reclaim available without deleting a rule: async-messaging ~7 KB, sms-mediana ~7.7 KB, trust-gateway ~4.6 KB, bale ~2 KB, tusd ~2 KB (33 lines), jitsi ~1.5 KB. |
| 11 | Companion boundary | **Absent in all six** | Not one skill contains a "what this does not own" section. `alaa-trust-gateway-auth/SKILL.md:136-156` lists nine companions as *pairing advice*, which routes a reader without transferring ownership, and does not name `alaa-services-contract` — the skill that owns the frozen header-name list its own body reproduces. |

### Two further classes, carried from Batch 2 and Batch 4, both found here

**12 — the self-granted exception.** The most common serious defect in the batch. Every instance below has
no external referent: no named artifact, no named approver, no checkable condition.

- `alaa-trust-gateway-auth/references/20-…:131` — "During migration, the gateway **tolerates an absent**
  `rol` claim for older tokens." No end date, no artifact, no observable that says migration is over.
  A permanent fail-open licence written as a temporary one, on a trust boundary.
- `tusd-upload-platform/references/hooks-auth.md:202` — "Avoid these suggestions **unless the user
  explicitly insists and understands the risk**", where the list beneath includes "authenticate only in
  `pre-create` for a security-sensitive public upload plane". A self-certifying waiver on the skill's
  central security rule.
- `tusd-upload-platform/references/constraints.md:3` — "Use these as hard constraints **unless the user
  is embedding tusd programmatically and changing the design deliberately**." An entire constraints file
  voided by the reader's own stated intent.
- `alaa-sms-provider-mediana/SKILL.md:59` — "**unless existing production code proves** a different
  account-specific format", on the recipient format. "Proves" has no checkable form.
- `jitsi-platform-architect/references/architecture-and-auth.md:159-160` — "bind them to one room
  **whenever possible**"; "avoid broad wildcard room claims **unless there is a very strong reason**".
  Room binding is the breach boundary.
- `alaa-async-messaging/SKILL.md:190` — "TLS for non-local traffic **if required**." A security control
  with a self-granted opt-out.

Full per-skill inventories are in §5. Count across the batch: **nine in `alaa-async-messaging`, six in
`alaa-trust-gateway-auth` (plus 37 soft preference verbs on constraint-shaped rules), four in
`alaa-bale-provider`, ten in `alaa-sms-provider-mediana`, six in `tusd-upload-platform`, six in
`jitsi-platform-architect`.**

**13 — the nominal owner that is factually empty, and its mirror, the stale vendor fact.**

- `alaa-async-messaging` is named by **ten other skills at fifteen call sites** as the owner of prefetch
  values, the acknowledgement point, publisher confirms, DLQ replay, consumer-side deduplication, outbox
  relay tuning and the outbox state set. It materially covers **one** of the fifteen. §5.1.
- `alaa-trust-gateway-auth` is named by `alaa-go-chi-development` and `alaa-controlled-ops` as the owner of
  **gateway TOTP step-up**, and by `alaa-golang` as the owner of **caching an authorization decision**. It
  contains zero material on either. §5.2.
- `tusd-upload-platform` is named by `alaa-golang` as the owner of resumable-upload behaviour and routes
  Go work straight back to `alaa-golang` — a circular pointer. It is also assigned four platform
  permissions by `alaa-services-contract` and mentions none of them. §5.5.
- **Both provider skills record no read date for any vendor fact.** `alaa-bale-provider` records neither a
  source URL nor a date and attributes facts to "the pasted docs", an artifact that no longer exists.
  `alaa-sms-provider-mediana` names two vendor documentation URLs and no version, commit or date, then
  labels the extracted facts "Key current official facts". An undated vendor fact looks authoritative and
  gets copied forward; this is the mechanism by which a provider skill rots without anyone noticing.
- `jitsi-platform-architect` records provenance in exactly one place — `references/source-map.md:24-30`,
  dated 2026-04-24 against release `stable-10888` — and nowhere else. That block is a real freshness
  mechanism in miniature, and it is three months stale with no expiry rule. Every other upstream Jitsi
  fact in the skill is undated, unsourced and unpinned.

---

## 4. Cross-cutting findings

**4.1 — The router convention is violated in two directions.**
`alaa-trust-gateway-auth` has **seven** content references and ships `references/00-topic-map.md`, so it is
below the nine-reference threshold and carries two routers that disagree: `SKILL.md:158-179` has ten rows,
`references/00-topic-map.md:18-37` has nine, and only the topic map routes to `../request-for-change.md`.
`tusd-upload-platform` has **twelve** content references and ships **no** topic map, so its router is a
bare bullet list in the body. Both must move, and the move must preserve every row.
Separately, `alaa-bale-provider` and `alaa-sms-provider-mediana` each carry two body routers (a numbered
"Start sequence" and a "Reference navigation" list) for two and three references respectively.
**Not one router row anywhere in the batch states an observable condition** — every row is a heading mirror.

**4.2 — Every provider and integration skill is missing the same section: the ambiguous outcome.**
An SMS send, a Bale send, a tusd hook call and a Jitsi mint call share one property: a timeout after the
request bytes were written tells you nothing about whether the work happened. `alaa-reliability-sla
references/20-retries.md:33` already states the rule — "A connect refusal and a timeout are not the same
event and must not share a code path" — and `alaa-services-contract references/22-…:149-151` already
states the consequence — a non-idempotent route records `idempotent: false` and every caller sets its
retry budget to `0`. Four of the six skills in this batch are silent on it, and one contradicts it.
Phase 2 gives each affected skill the same section, phrased for its own boundary, routed to the same owner.

**4.3 — Three shipped runtimes of one contract, with no conformance harness.**
`alaa-sms-provider-mediana` ships prose, a Python validator and a Go SDK asset that implement Iranian
mobile normalisation three different ways: the prose normalises, the Python validator only rejects, and
`assets/vendor-sdk.go` passes any string straight to the wire. `alaa-bale-provider` ships prose and a
Python validator with the same split. The two skills' canonical forms differ by exactly one character —
`+989xxxxxxxxx` for IPPanel, `989xxxxxxxxx` for Safir — and **both call their own output "Alaa canonical"**,
neither mentions the other, and neither cites the platform's inbound form. `AGENTS.md` already binds this
case: more than one implementation of one wire format ships a conformance harness, and a document
asserting parity is not evidence of parity.

**4.4 — Three of the six skills legislate an owner's ground while shipping the artifact that would
implement it.** `alaa-trust-gateway-auth` ships `references/permission-bitmap.php`, a fourth uncontrolled
implementation of a bit contract that `alaa-permission-generator` owns and emits for three languages,
untested, with an O(n)-per-check `has()`, sitting over an upstream catalog tool that has ten open bugs and
no CI. `alaa-sms-provider-mediana` ships `assets/vendor-sdk.go`, unlicensed, unpinned, three of fourteen
send modes, with stale in-file comments and a hardcoded `defaultBaseURL` whose base boundary (`/v1/api`)
conflicts with the skill's own env var (`/v1`) — an agent that reconciles the two builds
`…/v1/api/api/send`. `alaa-async-messaging` ships seven supervisor/systemd/compose files that encode a
worker-shutdown budget six times and state the behavioural rule behind it zero times.

**4.5 — `agents/openai.yaml` coverage is complete but inconsistent.** All six exist and all six use the
bare `$` form correctly. `tusd-upload-platform` and `jitsi-platform-architect` **lack** the
`policy: allow_implicit_invocation: true` block the other four carry. Nothing about either skill argues
against implicit invocation; uniformity settles it.

---

## 5. Per-skill analysis and rewrite specification

### 5.1 `alaa-async-messaging` — nominally the fleet's messaging owner, factually a Laravel queue tutorial

**What it is today.** A Laravel queue tutorial with a Kafka preamble. `SKILL.md` is 11,926 B against
6,188 B of references — the inversion the body/reference convention exists to prevent. Roughly 60% of the
body is step-numbered `php artisan` procedure. There is no ownership section, no output contract, no test,
no script, and no failure-class material for a broker, an outbox or a dead-letter queue.

**The nominal-owner finding, verified against disk.** Ten skills name this one at fifteen call sites:
prefetch values (`alaa-services-contract references/22-…:233,265`, `references/23-…:215`,
`alaa-reliability-sla/SKILL.md:117` and `references/40-admission-and-shedding.md:78`,
`alaa-system-design/SKILL.md:154`, `alaa-laravel-architecture/SKILL.md:65`); the acknowledgement point
(`alaa-golang references/05-…:32`, `references/60-…:117`); publisher confirms; **fleet-wide DLQ replay**
(`alaa-laravel-job-rabbitmq/SKILL.md:15,180`); consumer-side deduplication
(`alaa-reliability-sla references/60-idempotency.md:3`); outbox relay tuning and the row state set
(`alaa-data-layer references/30-…:31-32`, `alaa-laravel-architecture references/50-failure-recovery.md:25-27`);
transport choice and event versioning; quorum-queue policy; consumer concurrency; Redis and Horizon;
change-stream delivery handoff (`alaa-mongodb-patterns references/30-…:105`); reconnect behaviour.
**It materially covers one** — the Horizon-is-Redis-only constraint at `SKILL.md:44-55`, which is the best
content in the skill and survives intact.

The four reference files are not literally free of the vocabulary, but every occurrence is a mention rather
than a rule: `references/source-map.md:17,33` cites a prefetch doc URL and lists prefetch as a freshness
trigger; `references/rabbitmq-topology-and-policies.md:26-27,33` uses "unacked" as a monitoring noun;
`references/troubleshooting.md:10` says "before ack" in passing. The body states a prefetch value once,
hedged: `SKILL.md:135`, "**prefer** conservative `prefetch` (**often** prefetch=1)".

**Where it legislates an owner's ground.** Retry doctrine three times with no owner cited and no precedence
(`SKILL.md:205`, `:212`, `references/queues-best-practices.md:16`), all three weaker than
`alaa-reliability-sla references/20-retries.md` — none mentions a budget, none makes a retry legal before
making it, none handles the ambiguous timeout. Idempotency three times (`SKILL.md:204`, `:211`,
`references/queues-best-practices.md:4-7`), missing both the platform rule that the guarantee is a database
unique constraint and the consumer ordering contract this skill actually owns. Six value sites with zero
citations of `alaa-services-contract references/22-…`. Security posture three times in fail-open phrasing.
A local monitoring vocabulary competing with the `alaa_queue_*` / `alaa_outbox_*` families already
registered at `alaa-services-contract references/24-metric-registry.md:114-134`.

**The one direct conflict.** `references/rabbitmq-topology-and-policies.md:12-13` prescribes
`<app>.<domain>.<purpose>` naming with the examples `billing.payments.capture` and
`notifications.email.send`. `alaa-services-contract references/23-queue-and-exchange-registry.md:26-45`
prescribes a different grammar in kind: events on the producer's own `<service>.events` topic exchange with
each consumer declaring and binding its own queue; commands on `<service>.commands` landing in a
receiver-declared queue named `<service>.command.<family>.v<n>` — worked example
`notification.command.sms.send_pattern.v1`. The local grammar has no event/command segment and no version
segment, and both its examples name services that do not exist on this fleet. An agent following this
reference produces names the registry cannot record. This is the most damaging line in the skill, because
it sits in the file an agent opens exactly when naming a new queue.

**The Kafka question — answered with evidence.** `kafka` appears in seven files across the whole
repository. Four are this skill and its own metadata. The three independent mentions are conditional or
someone else's: `alaa-golang references/40-production-ready-package-catalog.md:97` names `franz-go` as the
default client "**when Kafka is the chosen broker**", one line below an unconditional
"`amqp091-go` — default, and what the kit's `mqkit` wraps"; `alaa-observability-soc
references/70-soc-evidence.md:62` describes a *customer's* SOC ingestion protocol;
`vector-rust-observability-pipelines/SKILL.md:201` lists it as one possible Vector sink. The negative
evidence is decisive: `alaa-services-contract` — the authoritative registry of every exchange and queue the
fleet has or is owed — contains no occurrence of `kafka`, no topic, no partition, no consumer group, no
offset; the kit ships `mqkit`, `outboxkit` and `jobkit` and no Kafka package; the registered async metric
family is entirely `alaa_queue_*` / `alaa_outbox_*` and defines consumer lag as the age of the oldest
unconsumed message, a queue notion rather than an offset; no `KAFKA_*` env key exists anywhere.
**Kafka is not deployed, not in the kit, and not in the contract**, while this skill's frontmatter and
`SKILL.md:102` present a Kafka-events / RabbitMQ-jobs hybrid as the recommended architecture. The two
defects compound: an agent following this skill designs against a broker the platform does not run *and*
names its queues in a grammar the registry rejects. **This is decision D-1 in §9.**

A second correction belongs beside it: **not every service has a broker at all.** `wa-api` runs on a
read-only analytical ClickHouse lane with no Postgres and no RabbitMQ. The rewritten skill needs a first
gate — read the service's configured lanes before assuming a broker exists.

**The assets question.** Retire all seven. They are Laravel-only; four are Horizon or worker command lines,
which is `alaa-laravel-job-rabbitmq`'s declared ground; the Go services do not run under supervisor or
systemd at all (shutdown is `runkit`'s, in four ordered phases against a 30 s budget), so
`stopwaitsecs=3600` is actively misleading if copied; container and Deployment expression belong to
`alaa-docker-production` and `alaa-k8s-helm`, and `alaa-laravel-job-rabbitmq` already ships the fleet's
real worker-deployment artifact. They are also stale on their own terms: an obsolete Compose `version:`
key, hardcoded `/var/www/app` and `www-data`, and an embedded `RABBITMQ_DEFAULT_PASS: "change-me"` in a
skill whose own body forbids committing secrets. **What must survive is the one behavioural fact they
encode and never state**: a worker's graceful-stop budget must exceed the longest handler's own deadline,
or a rolling restart converts in-flight work into redeliveries. Two sentences in `30-`, not six copies of
a number.

**Rewrite specification.**

*Body target: ≤ 5.0 KB net of the description, from 11,926 B — a ~58% cut.* Two genuinely new
capabilities are claimed and must be named in the final report: **the DLQ replay procedure** and **the
outbox operational surface**. Both are ground other skills already route here; neither exists on disk.

| Section | Budget | Content |
|---|---:|---|
| Description | ~950 chars | What it does, when to use, and a real negative clause folded from `SKILL.md:31-34` plus the Kafka and Laravel-driver boundaries. |
| Purpose | ~500 B | Three sentences: one broker; the seam between a transaction and a message; what must be true when it fails. |
| Gate: does this service have a broker lane | ~350 B | Read the configured lanes first. If there is no broker lane, this skill decides nothing. |
| Router table (8 rows, observable conditions) | ~900 B | Replaces both the bare list at `:225-229` and the section-pointing "Fast entry" table at `:243-248`. Eight references keeps the router in the body; no `00-topic-map.md`. |
| Hard constraints | ~1.6 KB | Six to seven numbered constraints, no preference verbs: at-least-once with the database-unique-constraint guarantee; explicit prefetch at every consumer construction site; receipt and business effect commit before the broker ack; bounded redelivery with a dead-letter route; publish only after commit, via the outbox when the fact must survive; a message payload is untrusted input. |
| Ownership boundary | ~1.0 KB | One line per owner, both trigger forms. |
| Required tests | ~350 B | Two named tests and what each asserts. |
| Script invocation | ~250 B | Exact command, three exit codes, the obligation each imposes. |
| Output contract | ~350 B | Prefetch with the measured p99 behind it; the ack route per outcome; the dead-letter target; the replay precondition if replay was used; every absent kit capability worked around. |

*References — eight files, router stays in the body:*

| File | Charter | ~size |
|---|---|---:|
| `10-transport-and-topology.md` | One broker on this fleet; event versus command decided by topology; why a log-structured broker is out of scope and the kit-change-request path if a design needs one; all naming routed to the registry. | 4 KB |
| `20-publishing-and-the-outbox.md` | Publisher confirms and what an unconfirmed publish obliges; publish-after-commit; when the outbox is required versus when after-commit dispatch suffices; the row state set and its transitions; relay tuning against `OUTBOX_BATCH`/`OUTBOX_TICK`; the four `outboxkit` absences stated as absences. | 5 KB |
| `30-consuming-ack-and-prefetch.md` | The acknowledgement point; ack / requeue / reject-without-requeue with one route and one crash window each; prefetch derived from measured handler p99 and the target unacked window; consumer concurrency bound; consumer-side dedupe via receipt; graceful-stop budget versus handler deadline; reconnect. | 5 KB |
| `40-dead-letter-and-replay.md` | **New.** DLQ topology against the registry's names; poison classification (permanent / transient / tenant-scoped); the replay procedure with preconditions, bounding, and proof the cause is gone; what makes a message unreplayable. | 4 KB |
| `50-failure-classes.md` | **Restructured from `troubleshooting.md`.** Eight classes, each symptom → diagnosis → smallest safe retry → escalation: broker unreachable; consumer stuck with growing unacked; poison redelivery loop; duplicate storm; outbox stalled or claimed-row orphan; DLQ filling; replay produced duplicates; publish-confirm timeout. Language-neutral. | 6 KB |
| `60-telemetry-and-proof.md` | Which registered observable proves which class, by name from `alaa-services-contract references/24-metric-registry.md`; the two required tests and their assertions; what a review must see. | 3 KB |
| `70-laravel-redis-and-horizon.md` | Everything framework-specific hoisted from the body, including `SKILL.md:44-69` intact, and the boundary line to `alaa-laravel-job-rabbitmq` for driver mechanics. | 3 KB |
| `90-source-map.md` | Survives, corrected: both trigger forms, Kafka links demoted, the duplicated after-commit PHP example at `:38-48` deleted. | 2 KB |

*Retired to `_to_delete/`:* `references/rabbitmq-topology-and-policies.md`, all seven `assets/` files.
`references/queues-best-practices.md` is retired **only as a stub** — see decision D-6 in §9, because
`alaa-laravel-architecture references/30-events-and-outbox-seam.md:14` cites it by filename and that skill
is out of batch.

*Script:* `scripts/check-consumer-bounds.sh`. Three deterministic checks: every consumer construction site
sets an explicit prefetch; every declared queue has a declared dead-letter target; every broker name
conforms to the registry grammar. Exit **0** clean, **1** findings printed with file and line and every
one must be resolved before reporting, **2** could not determine (no broker lane, or no recognisable
construction site) and the agent must perform and report a manual check rather than treat it as a pass.
`--help` and `--self-test` required, with fixtures covering one conforming and one violating case per
check. The body must state, next to the invocation, that static detection of a construction site is narrow
in the same way the kit's `pooledlane` analyzer is narrow — a constant, a wrapper or an indirection escapes
it — which is why exit 2 is a real outcome and not a formality.

---

### 5.2 `alaa-trust-gateway-auth` — correct on its subject, absent on its failure modes

**What it is today.** A careful, well-organised platform memo written almost entirely in the indicative
mood: it reports what the gateway does far more than it constrains what an agent may do. It is materially
correct on its core subject — what the gateway verifies, which compact claims project into which `X-*`
headers, how the `X-Access` bitmap decodes, the canonical `AUTH_*` / `TENANT_*` deny codes — and it is one
of the best-connected skills in the repository, named by fourteen others. It is 146 KB, of which
`references/full-guide.md` alone is 62.6 KB.

**Security passes; everything about failure does not.** The genuinely strong absolutes survive and must be
preserved: sanitize on every route (`references/20-…:87`, `references/10-…:80`), the closed reject list
(`20-…:86-106`), "Tenant context is derived from the verified token, not from request body, query string,
route params, or client-supplied headers" (`10-…:49`), and the frontend prohibition (`20-…:26`).

Against that: **"timeout", "retry", "backoff", "circuit", "idempoten", "unreachable", "unavailable",
"degrade" and "stale" appear zero times across all 146 KB.** The entire fail-closed posture is one bullet
inside a role list — `20-…:36`, "fail closed on deny or dependency failure" — with no scope, no named
dependency, no status code, no response body, no log event and no test.

The four fail-closed cases, as they stand:

| Case | What the skill says | Verdict |
|---|---|---|
| Gateway unreachable or absent from the path | Nothing. Zero occurrences of "unreachable", "unavailable", "down", "outage". | **Absent** — the most important failure mode on this skill's own ground is unwritten. |
| Request-time checker fails | `20-…:36`, one bullet. | Present, not in constraint form. |
| A claim is absent | Required claims fail closed and correctly (`20-…:74`, `10-…:59`, `50-…:81`, `50-…:90`). `rol` absent: `20-…:131` "the gateway **tolerates** an absent claim for older tokens". | Half-covered, with one **uncapped fail-open**. |
| A bitmap is stale | Nothing. `prv` and `av` are described as invalidation metadata for `prm` and are explicitly **not forwarded** to the service that would need them. | **Absent, and structurally so** — the metadata that would detect the condition is withheld from the only component that could act on it. |
| Downstream called directly, bypassing the gateway | Five places (`40-…:21-23`, `20-…:208`, `50-…:174,191,251`), but `40-…:22` is a disjunction — "either block that exposure or strip and reject internal auth headers at its own edge" — with no observable choosing the branch, and **none of it appears in `SKILL.md`**. | Present but soft, and invisible to a body-only reader. |

**`BYPASS_GATEWAY_PROOF` is the single most dangerous default on this skill's exact ground and the skill is
silent.** It defaults to `true` in the kit, its safety condition requires a recorded decision naming the
control, the verifier and the date, and any change to it is a `/alaa-security-review` trigger. It appears
once in the entire repository — in `alaa-go-chi-development references/12-kit-capability-map.md:191` — and
not once here.

**`references/full-guide.md` is an earlier draft, not a fuller one.** Measured line-by-line after
normalising heading and list markers: **661 of 852 non-empty lines (77%) appear verbatim elsewhere in the
same skill**; the lane's independent count was 675 (79%), and both readings agree on the conclusion. Where
it differs it is stale or weaker, and two proofs decide it: `full-guide.md:148-156` gives the canonical
custom-claim inventory as `m, prm, prv, av, pid, loc, fn, ln` — **`rol` is absent**, although the same file
projects `rol` to `X-User-Roles` fourteen lines later; and `full-guide.md:505` says `prv` and `av` stay out
of the forwarded contract "**unless a future revision explicitly adds them**", against `SKILL.md:102`'s
absolute "**never** forwarded as headers". One rule, two strengths, and the weaker one lives in the file
the topic map tells an agent to read for cross-cutting work.

**A header that one document says is not injected and another says is trusted.**
`references/20-…:114` injects `rol → X-User-Roles`, and `full-guide.md:506` lists it in the forwarded
surface, but `references/10-…:123` — "The current forwarded identity and token headers injected after
verification are …" — **omits `X-User-Roles`**, as does `request-for-change.md:22`. An agent auditing a
gateway sanitize list against `10-…:123` concludes the header is not part of the contract, while
`alaa-services-contract references/30-…:20` says it is and freezes it. That is a spoofing surface created
by a documentation inconsistency.

**Rewrite specification.**

*Body target: ≤ 7,500 chars from 11,717, with the description grown 486 → ~950 — a net shrink of roughly
3,700 chars.* Everything currently at `SKILL.md:47-134` leaves the body: both claim tables, the header
source-of-truth table, the bitmap-id allocation register, the route-family table. What comes in: the four
absolutes stated in constraint form with their reasons and observables; a five-row fail-closed case index
pointing at the file that holds each case; the single router table; and a ten-row "what this does not own"
table with both trigger forms.

*References — eight files, so the router moves into `SKILL.md` and `references/00-topic-map.md` is retired
with every row rewritten as an observable condition:*

| File | Charter | ~size | Provenance |
|---|---|---:|---|
| `10-verification-and-ingress.md` | What the gateway verifies, in order, and what it deliberately does not; sanitize-on-every-route; the `X-Forwarded-*` gap. | 9 KB | survives, edited |
| `20-claims-headers-and-sentinels.md` | The compact claim inventory, the claim→header projection, the null sentinels, what the gateway may and may not fabricate — header **names** routed, not restated. | 7 KB | survives, rewritten; absorbs the worked example JWT from `full-guide.md:160-185` corrected to include `rol`, and the sentinel definitions from `request-for-change.md:12-13` |
| `30-fail-closed-cases.md` | **New, written from scratch.** Every way the boundary fails, by class: symptom, diagnosis, smallest safe retry, escalation, and the test that proves it. Includes the gateway-unreachable case, the checker-failure case, the `rol` tolerance **rewritten with an external referent**, the stale-bitmap case and whether `prv`/`av` must be forwarded to make it detectable at all, `BYPASS_GATEWAY_PROOF`, and the client-supplied-opaque-value rule. | 9 KB | new |
| `40-downstream-normalization.md` | What a service behind the gateway does with trusted context: normalize once, scope every query, deny conflicting selectors, anonymous and accept-then-validate modes. | 10 KB | survives, edited |
| `50-deny-codes.md` | `AUTH_*` / `TENANT_*` meanings and status mapping; gateway-name → canonical translation; the response-code-equals-log-code rule. Envelope and field-set sections replaced by routing lines. | 7 KB | survives, trimmed |
| `60-auth-service-v3-contract.md` | v3 route families, gateway-facing versus service-local shapes, the client flow, direct-local-testing. **The six `D:\Sohrab\…` paths become repository-relative.** | 8 KB | survives, edited |
| `70-review-and-anti-patterns.md` | Trust-boundary review triggers and anti-patterns, each with the observable that decides it. | 6 KB | survives, rewritten |
| `90-source-map.md` | Source priority and freshness triggers; both trigger forms; the auth repository named rather than pathed. | 2 KB | survives, edited |

*Retired:* `references/full-guide.md` in full, after migrating four items by hand — the worked example JWT,
the sentinel definitions and the gateway-side sentinel-forwarding rule, the opaque-token-passthrough note
at `:454-455`, and the if-then routing prose at `:78-87`, which is the best-worded routing in the skill and
the only place that states a reading *order* obligation. `:505` and `:216` are deleted rather than migrated.
`request-for-change.md` is retired from the skill root after folding `:12-13` into `20-` and `:32-37` into
`30-` as test obligations. `references/permission-bitmap.php` is retired in favour of a routing line to
`alaa-permission-generator references/shared-consumer-contract.md` plus the conformance vectors in the
script — **decision D-2 in §9.**

*Script:* `scripts/trust_boundary_check.py`, four deterministic checks with `--help`, `--self-test`,
documented exit codes and a stated obligation each. (1) **Sanitize/inject symmetry** — every header the
gateway injects also appears in its delete list, and the delete list runs on public routes; failure means
the header is forgeable, stop and fix the config first. This is exactly the class of defect the
`10-…:123` versus `20-…:114` inconsistency proves prose cannot catch. (2) **Bitmap conformance vectors** —
id 1 → bit 0 of byte 0, id 8 → bit 7 of byte 0, id 9 → bit 0 of byte 1,
`permission_id = byte_index*8 + bit_index + 1`, padded input rejected, non-alphabet input rejected, a
bitmap mapping to zero known ids classified invalid rather than empty; failure means the decoder is not a
trusted-context reader and does not ship. (3) **Undeclared trusted-header read** — any `X-*` read outside
the frozen list resolved from `alaa-services-contract`. (4) **Bypass-flag audit** — `BYPASS_GATEWAY_PROOF`
truthy in any non-local environment file without an adjacent recorded decision naming the control, the
verifier and the date is a `/alaa-security-review` trigger.

*Also required:* rewrite the 37 preference-verb occurrences into constraints and eliminate all six
self-granted exceptions. `SKILL.md:76` — "only the gateway **should** treat it as raw bearer input" — is
the definition of the trust boundary written as a suggestion, and on a trust boundary a preference verb is
a security hole.

**One ownerless fact this skill should claim, in three lines.** The keyset cursor is unsigned base64-JSON
with no HMAC anywhere in the kit, binds only the sort token and not filters, direction, scope or tenant,
and `INVALID_CURSOR_CONTEXT` does not exist. `alaa-keyset-pagination` mandates all three as though they
were implemented. The **mechanism** stays with `alaa-keyset-pagination` and `alaa-services-contract`; the
**policy** belongs here and generalises beyond cursors: *a client-supplied opaque value carries no trust;
after decoding it, every scope-bearing field it yields is compared against the trusted request context and
the request is denied on mismatch, and the decoded value never becomes a source of tenant, actor or scope.*

---

### 5.3 `alaa-bale-provider` — a correct wire contract with no failure behaviour and no provenance

**What it is today.** A wire-format contract for one endpoint pair (`send_message`, `upload_file`),
accurate on payload shape and almost entirely silent on what happens when the request does not come back.
Two routers in the body for two references. No cross-skill call site of any form anywhere in the skill.

**The load-bearing gap.** `timeout` appears twice, both as a classification, never as a value or an
obligation to set one. Zero occurrences of `backoff` as a rule, `jitter`, `circuit`, `deadline`, `degrade`,
`partial`, `outbox`, `pool` or `Retry-After`. The single retry sentence,
`references/bale-safir-api.md:231`, conditions retryability on "the caller" having a bounded policy —
an unnamed other party — with no attempt count, no curve and no cap.

**The idempotency contradiction.** `references/bale-safir-api.md:241-242` instructs the agent to
"Generate a stable request ID from the business delivery intent, such as **notification ID, recipient ID,
template ID**". `alaa-reliability-sla references/60-idempotency.md:12` forbids exactly that: "**A key must
not be derived from the request content.** A content hash cannot distinguish an honest retry from an
intentional repeat … so it silently suppresses the second real operation." Recipient ID and template ID
*are* request content, so following this line produces a key that suppresses a legitimate second OTP to the
same recipient. The platform's own recorded rule differs again and is correct:
`alaa-golang-clean-code-principles references/20-domain-data-and-consistency.md:137` — "Bale's `request_id`
= the delivery's public id, unchanged across retries". **Decision D-8 in §9** settles which wins; the
recommendation is the Go skill's version, because it matches the doctrine.

The rule also changes strength three times across three artifacts: a preference in the body
(`SKILL.md:34`, "**Prefer** `request_id` for every non-test send"), advice in the reference
(`bale-safir-api.md:46`, "**Recommended** for production sends"), and a **non-blocking warning** in the
validator (`scripts/validate_bale_payload.py:62`), so a production payload with no `request_id` exits 0
and prints `[OK] Bale Safir payload is valid`. An agent that reads the body and runs the script ships
sends with no idempotency key and gets a green check for it.

**Two verified script defects.** Both were observed by running the script, not inferred.
(a) `scripts/validate_bale_payload.py:166` uses `otp.isdigit()`, and Python's `str.isdigit()` returns
`True` for Persian-Indic, Arabic-Indic and superscript digits: `"۱۲۳۴۵۶"`, `"١٢٣٤٥٦"` and `"²³⁴"` all exit
**0** as valid OTPs — in the one place a machine was supposed to be more reliable than the prose that
spends two paragraphs warning about exactly this input class for phone numbers. (b) The four field names
the body explicitly forbids — `chat_id`, `parse_mode`, `callback_data`, `disable_notification` — all pass;
the script has no unknown-key rejection, while the sibling script *does* ship `reject_bale_shape()`, so the
cross-provider guard exists in the library in one direction only. Also: `--self-test` does not exist
(argparse error, exit 2); exit code 2 is overloaded across usage error, file-not-found and malformed JSON;
no exit code is documented anywhere; `is_non_empty_string` accepts `"   "`.

**Provenance: none.** Zero dates, zero documentation URLs, zero version identifiers anywhere in the skill.
Facts are attributed to "the pasted docs" (`bale-safir-api.md:10,77`) — a referent no agent can check.

**Rewrite specification.** Body ≤ 7,929 B net of the description (no growth; the reclaim comes from three
duplicated JSON blocks ≈ 1,100 B, the second router ≈ 250 B, and five duplicated rule statements ≈ 500 B).
Sections: Purpose; **one** router table with observable conditions; hard wire rules with the endpoints as
configurable defaults rather than "hard rules"; a five-row variant-selection table with **no JSON in the
body**; idempotency stated once and corrected; secrets stated once with `$BALE_SAFIR_API_ACCESS_KEY` in
every example; **failure behaviour (new)** with four named classes and the one rule this skill genuinely
owns — a read timeout on `send_message` is retryable only with an unchanged `request_id`, because Safir may
have delivered; **observability (new)** naming the `alaa_dependency_*` families from
`alaa-services-contract references/24-metric-registry.md:107-110`; validation with the exact command and
the obligation per exit code; and an ownership table naming every owner with both trigger forms.

References: `bale-safir-api.md` survives with the idempotency and security sections deleted (they move to
the body, stated once) and **every table gaining a provenance line — source URL, document version if one
exists, and `read on YYYY-MM-DD`**. `examples.md` survives with env-var credentials and a `## Responses`
heading so a response shape is never fed to a request validator. Two new files:
`30-failure-classes.md` (symptom → diagnosis → smallest retry → escalation, vendor-specific only, all
policy routed) and `40-phone-and-conformance.md` (the shared conformance corpus — see §5.4 and §7).

Script must gain, in priority order: `--self-test`; the `isdigit()` fix (`re.fullmatch(r"[0-9]{4,8}", otp)`)
with a Persian-digit case in the self-test; unknown-top-level-key rejection naming each forbidden field;
`reject_mediana_shape()` so the guard exists in both directions; documented and disambiguated exit codes;
a `--mode request|response` switch; `request_id` promoted from warning to error; and the conformance corpus
read from the reference rather than duplicated in code.

---

### 5.4 `alaa-sms-provider-mediana` — a vendor catalogue that is wrong where it matters most

**What it is today.** A transcription of the IPPanel Edge catalogue with a thin policy layer. **43% of the
15.1 KB always-loaded body restates `references/mediana-ippanel-api.md`** — and by paraphrase rather than
by copy (verbatim 6-gram overlap is 1.0%), which is worse, because neither copy is canonical and they have
already drifted: body `:187` says "retry policy configurable" where the reference `:50` says
"retry/**backoff** policy configurable", and the body's test list omits the phone normalisation the
reference includes.

**The worst defect in the batch.** `references/mediana-ippanel-api.md:494`:

> `| Timeout / DNS / TLS / connection failure | Transport retryable if bounded |`

One table row collapses four events into one retryable class. `alaa-reliability-sla
references/20-retries.md:33` forbids exactly this by name — "A connect refusal and a timeout are not the
same event and must not share a code path. A refusal is a proof of non-execution… A timeout is the absence
of information" — and `:24` makes a read timeout retryable **only with an idempotency key**, which this
API does not have, as the skill itself admits at `SKILL.md:171`. `alaa-services-contract
references/22-…:149-151` closes it: a route that cannot be made idempotent records `idempotent: false` and
every caller sets its retry budget to `0`. So the reference instructs an agent to do the one thing that
double-sends an OTP, in the register of a considered classification table.

**Scope sprawl, with fleet evidence.** `alaa-services-contract
references/27-notification-service-contract.md:88-90` defines exactly two SMS command families the fleet
carries — `notification.command.sms.send_message.v1` and `…send_pattern.v1`. There is no votp,
peer-to-peer, phonebook, file, keyword, postal-code, country, geolocation or job command. Meanwhile the
always-loaded body spends 1,320 B enumerating ten targeting modes and 2,263 B on core variants including
one (votp) that is likewise absent. **And the one thing an Alaa agent must get right is documented
nowhere:** `pattern_values` is an **array of `{key, value}` pairs** in the fleet envelope while Mediana's
`params` is an **object**, and that mapping — with its ordering, duplicate-key and missing-variable
behaviour — appears in neither the body nor any reference. **Decision D-5 in §9.**

**Secrets.** No literal token is committed anywhere and every curl uses `$MEDIANA_SMS_API_TOKEN`, which is
better than the sibling. Two gaps: the prohibitions are scoped **only to logs** and name no mask form,
where `alaa-bale-provider references/bale-safir-api.md:250` correctly scopes it to "logs, traces,
exceptions, screenshots, and final reports" with a concrete mask; and
`references/mediana-ippanel-api.md:390` places the API token in a **GET query string**, which puts the
credential in access logs, proxy logs and shell history, and the skill objects to that endpoint on style
grounds only.

**`assets/vendor-sdk.go` should not ship.** 146 lines, no `go.mod`, no license, no SPDX, no version, no
commit — unknown provenance, unpinned, unattributed. Three of fourteen send modes; no cancel, no price, no
`context.Context`, no retry, a hardcoded 10 s timeout, no normalisation, no redaction, and a `fmt.Printf`
from library code. Its comments are already misleading: `:37` and `:58` annotate `sending_type` with
`// e.g. "sms"`, and `"sms"` is not a valid `sending_type` in this API. And `:13` hardcodes
`defaultBaseURL = "https://edge.ippanel.com/v1/api"` whose base boundary conflicts with the skill's own
`MEDIANA_SMS_API_BASE_URL` (`/v1`) — an agent reconciling the two builds `…/v1/api/api/send`. Every durable
fact it carries is already extracted into `references/vendor-go-sdk-notes.md:11-38`. **Retire the asset,
keep and strengthen the notes, and add the `/v1` versus `/v1/api` warning explicitly.**

**Rewrite specification.** Body 15,087 B → ~7,400 B (a 51% cut), description 617 → ~950 chars. Sections:
Purpose and ownership boundary (ten owners, both trigger forms); a four-row router with observable
conditions; **the two fleet send modes only** plus the `pattern_values[] → params{}` mapping;
non-negotiables (auth, the canonical recipient produced by exactly one normaliser, Bale's four-egress
secret scope with a mask form, the URL-send endpoint disqualified for authenticated production traffic,
the `/v1` versus `/v1/api` trap named); **the ambiguous send (new)**; recovery by failure class; the script
contract; and a trimmed negative clause.

References: `10-send-contract.md` (renamed from `mediana-ippanel-api.md`, absorbing the six body sections
that move out, every vendor fact carrying `[source: <url>, read <YYYY-MM-DD>]`);
`20-examples-and-rejects.md` (renamed from `examples.md`, gaining ambiguous-outcome and timeout fixtures);
`30-failure-and-ambiguity.md` (**new**); `40-vendor-contract-clues.md` (renamed from
`vendor-go-sdk-notes.md`, absorbing `SKILL.md:175-190` so the seven rules exist exactly once).

Script must gain: `--self-test`; documented exit codes with the obligation per code; **`--normalize
<raw-number>`, the single canonical normaliser** exported as a function and callable from the CLI; the
shared conformance corpus; the duplicate bulk warning fixed (`:254` and `:306` both fire), the
`$.files[][$0]` path bug at `:134` fixed, and the dead `or value is None` at `:180` removed; and either
validation of the bulk-targeting `params` contents or — preferably — deletion of those branches with an
outright rejection of the `sending_type` values the fleet does not command, which drops the script to
roughly 7 KB and removes its largest drift surface. Observed today: a `postal_code` payload with
`params:[{"garbage":"totally-unvalidated"}]` exits **0**.

---

### 5.5 `tusd-upload-platform` — three subjects welded together, missing every size and retention rule

**What it is today.** A tusd deployment guide, a partial restatement of the gateway trust boundary, and a
Vue/Quasar frontend SDK, in a consultant-advisory register: 45 hedged constructions across the body and
references, seventeen of them the word `unless`. Twelve content references and no topic map.

**No server-side size cap exists anywhere.** `-max-size` appears in zero CLI baselines
(`references/snippets.md:20,32`) and zero compose files. The only size check is
`assets/client/useTusUpload.ts:100-102`, client-side and bypassed by any non-browser client. On an upload
plane that accepts arbitrary bytes from an untrusted client, that is the security finding of the skill.

**The 64 MiB body cap is not mentioned at all** — zero occurrences of `MiB`, `HTTP_MAX_BODY_BYTES`, or any
body-cap concept across the body and all twelve references. The interaction is subtle and the skill makes
it worse: a tus `PATCH` carries a chunk, not a whole file, but when `chunkSize` is unset `tus-js-client`
streams the entire remaining file in one `PATCH`, and `references/client-side.md:49` actively discourages
setting `chunkSize`. So an agent following the skill hits the wall by default, and the two ways to get it
wrong are that uploads break or that the agent raises the fleet-wide cap and silently disables a platform
control on every route. The rewrite must state, as a constraint with its reason: tusd does not run on the
Go kit's HTTP server and is not itself subject to `HTTP_MAX_BODY_BYTES`; any Ala service that terminates or
proxies tus traffic is; on such a path `chunkSize` is set strictly below the smallest cap on the narrowest
hop, the value arrives in the upload-session response rather than as a client constant, and raising a
fleet-wide cap to admit an upload is prohibited — the correct move is a dedicated ingress.

**Hook failure posture is undefined, and undefined reads as fail-open.** `references/constraints.md:13-16`
gives the mechanism (15 s timeout, 5 KiB response cap, 3 retries, 1 s backoff) and never the outcome.
Nothing anywhere says what tusd does when the `pre-create` hook is unreachable. Nothing says the hook
endpoint must reject a call that did not come from tusd — `references/hooks-auth.md:92-98` describes tusd
forwarding the *client's* credentials to the hook, which is a different thing entirely. And the hook
endpoint's own authentication is stated only in preference verbs: "prefer mTLS or another service-to-service
auth layer" (`references/security.md:132-140`), naming no artifact. An upload that proceeds because the
authorization hook timed out is a security hole.

**Retention is the largest content gap.** No retention rule, no reaper specification, no disk-pressure
response. `references/topologies.md:91-98` names "a janitor or scheduled job" with no interval, no age
threshold, no owner, no metric and no failure behaviour; `:85` says "expire it later" with "later"
unbounded; `references/security.md:158` demotes "retention TTL for unfinished uploads" to optional; and
`references/observability.md:149` alerts on "stale unfinished uploads beyond retention" — an alert against
a policy the skill never defines. `Upload-Expires` is never mentioned server-side. Abandoned S3 multipart
uploads, which accrue cost invisibly and are untouched by a filesystem janitor, are never mentioned.

**Duplication at scale.** Four divergent copies of one upload state machine (11 / 12 / 9 / 10 states across
`client-side.md:63-79`, `vue-frontend.md:136-153`, `assets/client/useTusUpload.ts:4-13`,
`assets/client/useUploadQueueStore.ts:3-13`); three disagreeing ownership-record field lists; five copies
of "`pre-create` alone is not enough"; four copies of the per-method authorization rule.

**Three real code defects in the client assets**, read from source: `useTusUpload.ts:230-235` resumes
`previousUploads[0]` unconditionally with no check that the fingerprint belongs to the current
`appUploadId`, so after a project switch a stale fingerprint resumes the wrong upload;
`useTusUpload.ts:182-185` sets `status='paused'` on `navigator.onLine === false` and returns `false`, which
makes tus emit `onError`, which sets `status='failed'` at `:214`, so going offline mid-upload reports a
terminal failure instead of a pause; `useTusUpload.ts:66` hardcodes
`DEFAULT_RETRY_DELAYS = [0, 1000, 3000, 5000, 10000]` — a retry budget with no jitter, contradicting
`alaa-reliability-sla references/20-retries.md`. The assets are otherwise a **skill-owned reference
implementation, not a snapshot**: `useTusUpload.ts` imports only `vue` and `tus-js-client`, with no app
imports, no URL and no tenant.

**Object-storage ownership is genuinely vacant.** `alaa-data-layer` contains **zero** hits for S3, MinIO,
object storage or blob storage. Recommendation: this skill claims only the upload-plane slice — multipart
part sizing and its temp-disk cost, abandoned-multipart cleanup, server-side object-key generation and
tenant prefixing, and the fact that a finished object appears in the bucket only at completion — and
**explicitly disclaims** bucket lifecycle policy, replication, IAM shape, CDN origin and credential
rotation, naming them as currently unowned. A named gap is safe; a silently absorbed one is not.

**Rewrite specification.** Body ≤ 7,020 B net of the description (must not grow; the reference map and
asset list leave the body, freeing 33 lines, which pays for the failure posture, the size-limit chain and
the retention rule). Body sections: Mission; **what this skill does not own** (new, eight rows);
**binding rules** (twelve lines, zero hedges, each with scope and reason); default platform shape minus the
Ala-specific endpoint path; **exactly one line pointing at `references/00-topic-map.md`**; expected output.
Removed: "First decisions", "Subagent strategy" (generic orchestration — route to `/alaa-cc-orchestrator`),
"Assets", "Reference map".

References — thirteen files including the router, since twelve content references puts this skill above the
threshold: `00-topic-map.md` (**new**, one observable-condition row per reference *and* per asset);
`10-source-map.md`; `20-decision-matrix.md`; `30-topologies.md`; `35-storage-lifecycle.md` (**new** —
retention values, reaper contract, `Upload-Expires`, abandoned S3 multipart, disk-pressure thresholds and
the action at each); `40-authorization.md` (per-method authorization, the single ownership record, the
`upload_to_*` bitmap permissions, upload-ID entropy, metadata and path-traversal rules);
`45-hooks.md` (responsibilities, response shapes, blocking budgets, **failure posture**, hook-endpoint
authentication); `50-failure-modes.md` (**new in structure** — nine classes in symptom/diagnosis/retry/
escalation form); `55-tests.md` (**new** — named tests a broken implementation fails: kill the connection
at 40% and assert `HEAD` offset then completion; stop the hook endpoint and assert `POST` denied; replay
another tenant's upload id and assert denial before any byte is accepted; `Upload-Length` above `-max-size`
rejected at creation; a metadata filename containing `../` leaves the stored path unaffected; restart tusd
mid-upload and assert graceful drain); `60-browser-client.md` (one merged file replacing `client-side.md`
and `vue-frontend.md`, protocol behaviour only, one canonical state list); `70-front-door.md`;
`80-observability.md`; `90-constraints.md` without the "unless deliberate" waiver.

Retired: `references/alaa-trust-gateway.md` (consumption half into `40-`, boundary half becomes two routing
lines), `client-side.md` (merged), `snippets.md` (CLI baselines become the compose files' single source),
`security.md` (distributed across `40-`, `35-`, `60-` and a `/alaa-security-review` trigger line).

Assets: keep and fix `useTusUpload.ts` (all three defects), keep `uploadTelemetry.ts` with the base path
parameterised and `quasar.config.snippet.ts`; add `-max-size` to both Compose command blocks; replace the
knowingly-placeholder alert `tusd_connections_open > 500` (which says so in its own annotation) with a
documented variable. The four Vue-shape assets are **decision D-7 in §9.**

Script: rewrite `validate_pack.py` around `argparse` with `--help`, `--self-test`, `--root`, exit 0 clean /
1 violation with file and line / 2 misuse, and a stated obligation per failure. Nine checks: exactly one
router; every reference named in the topic map and every topic-map row resolving; no unpinned `tusd:` tag;
every CLI baseline and Compose `command:` contains `-max-size`, `-behind-proxy`, `-disable-download`; the
tusd version string in at most one file; no literal `/files/` in `assets/client/**`; description length and
a negative clause present; no `$name` trigger without its `/name` twin; `agents/openai.yaml` carries the
`policy` block. `--self-test` must build fixtures with `tempfile.mkdtemp()` **outside** the repository.

---

### 5.6 `jitsi-platform-architect` — decision-support written as description

**What it is today, and the framing error.** A genuinely good architectural memo — control plane versus
media plane, where a JWT is minted, which substrate can carry UDP — **about a system this platform does not
run.** Grepping the whole tree for `jitsi|videobridge|jicofo|prosody|jibri|JVB|jigasi` returns exactly
three files outside the skill's own folder, and all three are index entries: `README.md:178`,
`README.fa.md:109`, `UPGRADE-CARRYOVER.md:179`. No service, no contract, no telemetry name, no deployment
target and no kit fact references Jitsi anywhere; `alaa-services-contract` contains zero occurrences of
`jitsi`, `meeting`, `room` or `conference`. The skill nonetheless opens with present-tense assertions —
`SKILL.md:10`, "The product is platform-centric and Jitsi is one subsystem inside a larger system" — under
a heading that calls them assumptions. Being a considered-capability skill is legitimate; writing it as a
description of a deployment is not. **Decision D-3 in §9.**

**Criterion 5 is the one clear pass in the batch.** `references/scaling-stability-security.md:28-58`
separates four capacity domains and forbids inferring media capacity from web CPU; `:81-92` gives four
checks before claiming multi-bridge; `references/deployment-platforms.md:112-122` states the exposure-mode
consequence honestly. That material survives.

**The JWT trust domain is the seam, and the skill half-holds it.** It says the backend mints, lists the
claims, and says "keep tokens short-lived" and "use separate signing secrets or keys". It does not say
where the signing key lives, how it rotates, which algorithm is permitted, what the lifetime is in seconds,
or **what happens when the token expires while the conference is still running** — which is the operational
cliff, because a token is validated at join, so an expired token has no effect on a seated participant and
silently breaks reconnect after a network blip. The participant appears to be randomly kicked ten minutes
in and no log says why.

**Room-name guessability is absent entirely** — no occurrence of `guess`, `unguessable`, `random` or
`entropy` — and an unguessable room name is the whole access control of a default Jitsi deployment.
Default `anonymous` auth and guest-domain lockdown appear once, at
`references/architecture-and-auth.md:156`, as a permitted carve-out rather than a required configuration.

**Recording has mechanics and no governance.** The skill covers Jibri capacity and the recording event
flow, and never says who may start a recording, where the artifact lands, what retention applies, or who is
told. A recording is a data-protection event.

**Rewrite specification.** Body ≤ 820 words net of the description (from 877), description 613 → ~950.
Sections: **Status** (one paragraph: no Jitsi deployment exists in this repository, every rule here is a
decision to make, and nothing here may be cited as a fact about what the platform runs); **ownership and
routing table** — the one genuinely new capability, since the skill currently routes nowhere and names no
skill in any form; a seven-row router with observable conditions; **breach conditions** (five unhedged
rules with reasons: room-name entropy; `room` bound to exactly one room, never `*`; guest domain locked and
anonymous auth disabled with a named verification; no raw platform access token crosses into Jitsi; no
recording without an authorization check and a participant notice); a failure-class index; deliverable and
validation; and a freshness contract requiring every upstream fact to carry a source URL, a release tag and
a read date, with a 90-day re-read rule. Deleted from the body: `:8-31` (three sections restating the
description), `:59-68`, `:93-102` and `:104-109` (all duplicated into references), and `:111-119`
(generic orchestration — route to `/alaa-cc-orchestrator`).

References — seven content files, so the router stays in the body and no topic map is created. All six
existing tables of contents are deleted (46 lines of heading mirror).
`10-architecture-and-jwt-trust.md` (~7 KB, roughly half new: minting authority, key custody, rotation,
permitted algorithm, lifetime in seconds, room binding, mid-call expiry and renewal, room-name entropy,
guest-domain lockdown); `20-failure-classes.md` (~6 KB, **written from scratch**: bridge dies mid-conference;
Prosody restart; Jicofo bridge-state loss; JWT expiry mid-call; Jibri failure mid-recording; TURN relay
unreachable; planned shard drain); `30-deployment-substrate.md` (~6 KB, trimmed);
`40-embedding-contract.md` (~5 KB — the Jitsi half of the frontend file plus a ≤15-line lifecycle snippet);
`50-events-recording-governance.md` (~6 KB — the canonical event list in a single copy, plus new recording
governance); `60-scale-and-capacity.md` (~5 KB, trimmed); `90-source-map.md` (~5 KB, rewritten from a link
list into a **provenance ledger**: one row per upstream fact class, with fact, source URL, release it
applies to, date read, and expiry).

**The frontend split**, so Batch 6 does not have to re-litigate it. `references/frontend-vue-quasar-vite.md`
is roughly 55–60% this skill's ground. Stays: the IFrame-API-versus-`lib-jitsi-meet` decision, embed
lifecycle, SSR hazards, the PWA caching rules specific to `external_api.js` and websocket paths, the three
config layers, what cannot be overridden at embed time, and when to abandon the IFrame API. Goes to
Batch 6: the 64-line component (keep a ~15-line snippet showing only the Jitsi lifecycle contract), the
Quasar structure section except `QNoSsr`, the host-app ownership list, and generic permission UX. The
routing line in both directions is specified in the lane report and reproduced in Phase 2.

Script: `scripts/check_jitsi_jwt.py` — asserts the claim contract (`room` present, non-empty, not `*` and
not a prefix wildcard; `aud`/`iss` match the profile; `exp − iat` at or below the configured maximum; `sub`
matches the expected base domain; `alg` in an allowlist and never `none`; the `kid`-identified signing key
is not the platform access-token key; no role or moderator claim outside `context`), plus a `--room-name`
mode asserting entropy and rejecting tenant, date and sequential-id patterns. `--help`, `--self-test` with a
fixture per failure branch, exit 0 / 1 claim violation / 2 bad input / 3 self-test failure, with the
obligation stated per code.

---

## 6. Section 4 candidate new skills — verified against disk

**`alaa-design-patterns` — do not build. Confirmed absent, and correctly so.** This was settled in Batch 2
and nothing in Batch 5 disturbs it. Every skill in this batch that touches pattern choice defers to a
per-language clean-code skill, which is the correct behaviour; what is missing is the routing line, not a
central owner. A fourth claimant on ground three skills already share cleanly would make the library worse.

**`alaa-algorithms-data-structures` — exists, and Batch 5 confirms its boundary from the consumer side.**
`alaa-async-messaging` correctly states no complexity budget for the outbox claim query, which already
belongs to `alaa-data-layer references/30-concurrency-projections-and-pooling.md:25-32`.
`tusd-upload-platform` has one budget it genuinely owns — S3 part size × concurrency × instances is the
local temp-disk demand that its own `topologies.md:37` calls "a first-class resource" — and it is missing;
that is a coverage gap in `tusd-upload-platform`, not a case for a new skill. No change requested.

**`alaa-system-design` — exists, and this batch under-routes to it rather than duplicating it.** Zero
mentions across all six skills, while `jitsi-platform-architect references/scaling-stability-security.md:178-200`
performs SLA arithmetic and `deployment-platforms.md:15-19` makes a platform choice, both of which are
pre-implementation design. The correction is six routing lines, not a new skill.

**`alaa-reliability-sla` — exists, and this batch is the strongest evidence yet that it is the right
owner.** Zero mentions across all six skills, and in their place: three copies of retry doctrine in
`alaa-async-messaging`, one contradicting table row in `alaa-sms-provider-mediana`, one content-derived
idempotency rule in `alaa-bale-provider` that the owner explicitly forbids, one unjittered retry array in
`tusd-upload-platform/assets/client/useTusUpload.ts:66`, and one local load-shedding rule in
`jitsi-platform-architect`. Five skills independently reinventing one owner's rules, each more weakly, is
the pattern the ownership model exists to stop. No change requested to the skill; twenty-odd routing lines
requested from this batch.

**`alaa-testing-strategy` — exists, and every skill in this batch fails criterion 1 by listing test
*topics* rather than proofs.** Not one names a proof level. The correction is that each skill states which
tests its own domain requires — a redelivery test, an interrupted-upload test, a spoofed-header test, a
hook-timeout test, a rejected-JWT test — and routes layers, doubles and proof strength to
`references/40-proof-strength.md`. No new skill.

---

## 7. New-skill decision — none required

**No new skill is required to close any gap observed in Batch 5.** Every gap found is either (a) ground a
skill in this batch is already named as owning and simply has not written, or (b) ground an existing owner
holds cleanly and this batch fails to route to.

The one candidate that deserved a serious look, and is **rejected on the evidence**, is a shared
**`alaa-provider-integration`** skill owning the common ground of every third-party vendor call. Both
provider lanes examined it independently and both rejected it, for the same reason: strip out what an
existing owner already holds and almost nothing is left. Retry legality and the ambiguous outcome are
`alaa-reliability-sla references/20-retries.md:22-33`, which already states the rule better than either
provider skill would. Idempotency key mechanics are `references/60-idempotency.md`, with the Ala
consequence at `alaa-services-contract references/22-…:142-151`. The dedup seam already exists one layer
up: `22-…:152-153` — "Notification commands already carry `idempotency_key` inside the canonical envelope
… Do not add a second idempotency mechanism beside it." The `alaa_dependency_*` metric family already
exists at `references/24-metric-registry.md:107-110`. Secret handling and upload safety are
`alaa-security-review`. The queue seam is `alaa-async-messaging`. A new skill would either restate all of
that — creating a fourth strength for rules that already have three, which is the exact defect this
programme is fixing — or consist of nothing but a routing table, which is a section, not a skill.

What **is** genuinely shared and currently unowned is small, mechanical, and not doctrine: two Python
validators whose `main()`, `Reporter`, `is_non_empty_string` and 0/1/2 exit scheme are identical (verified
by diff — only an argparse description string and an `[OK]` message differ); two provider-specific
renderings of one Iranian mobile number with no shared normaliser and both claiming the word "canonical";
and two secret-handling sections of unequal strength on identical ground. The answer to all three is
**convergence inside the two existing skills plus a shared conformance corpus**: the same section order,
the same CLI contract, the same provenance convention, and one fixture file of
`{input, mediana_expected, bale_expected}` triples duplicated byte-for-byte into both skills' `scripts/`
directories, exercised by both `--self-test` runs and carrying a checksum line so drift is a test failure
rather than a review finding. That satisfies the `AGENTS.md` conformance-harness rule without adding a
boundary to police. Two skills that look the same are cheaper to keep correct than three skills with a new
seam between them.

---

## 8. Ownership boundaries this batch settles

| Ground | Owner after Batch 5 | Explicitly not owned by |
|---|---|---|
| Prefetch derivation, the acknowledgement point, publisher confirms, consumer-side deduplication, DLQ topology and the fleet-wide replay procedure, outbox relay tuning and the outbox row state set, reconnect | `alaa-async-messaging` | `alaa-reliability-sla` (doctrine), `alaa-services-contract` (every value and every name), `alaa-laravel-job-rabbitmq` (Laravel driver mechanics) |
| Who may assert a trusted header; the trust boundary itself; every fail-closed case at that boundary, including gateway-unreachable, stale bitmap, and `BYPASS_GATEWAY_PROOF`; the policy that a client-supplied opaque value carries no trust | `alaa-trust-gateway-auth` | `alaa-services-contract` (header names and wire shapes), `alaa-permission-generator` (bit contract, allocation, emission), vendored `openfga` (object-level relations), `alaa-security-review` (fail-closed doctrine), `alaa-keyset-pagination` (cursor mechanism) |
| One vendor's wire contract, its canonical recipient rendering, its idempotency capability or lack of one, and the failure classes specific to it | each provider skill, for its own vendor | `alaa-reliability-sla` (retry legality, backoff, idempotency mechanics), `alaa-services-contract` (values, metric names, the notification command envelope) |
| The tus size-limit chain end to end and its interaction with the fleet body cap; retention, reaper and disk-pressure response including abandoned S3 multipart; hook-endpoint failure posture and hook-caller authentication; the `Upload-Expires` contract; resume-matching correctness; **the upload-plane slice of object storage** | `tusd-upload-platform` | `alaa-haproxy` (directives), `alaa-docker-production` / `alaa-k8s-helm` (delivery), Batch 6 (Vue component and store shape), `alaa-trust-gateway-auth` (what a caller may be believed about) |
| The Jitsi JWT trust domain from the authorization decision onward — derivation, claim set and binding, key custody and rotation, lifetime, mid-call expiry; room-name entropy; guest-domain lockdown; recording governance; media-plane substrate demands | `jitsi-platform-architect` | `alaa-trust-gateway-auth` (everything up to "this caller may request a join for room R as role X"), `alaa-k8s-helm` / `caas-arvan-kuber` / `alaa-docker-production` (substrate mechanics), Batch 6 (Vue code shape) |
| Object-storage **platform** mechanics — bucket lifecycle policy, replication, IAM policy shape, CDN origin, credential rotation | **nobody, and this is now named** | `alaa-data-layer` has zero hits for S3, MinIO, object storage or blob storage |

---

## 9. Decisions for the owner

**D-1 — Demote Kafka in `alaa-async-messaging` from recommended architecture to an escalation path.**
Recommendation: yes. Evidence in §5.1 — no Kafka in the contract, the registry, the kit, the metric family
or any env key; the only unconditional broker fact on this fleet is that `mqkit` wraps RabbitMQ. The
replacement is one paragraph: RabbitMQ is the only broker; events and commands are distinguished by
topology, not transport; a log-structured broker answers a genuinely different problem (long-retention
replay to unknown future consumers, or fan-out beyond a topic exchange), and when a design needs one the
obligation is to file a kit change request and stop. *Cost of not doing it:* agents keep designing
two-broker systems against a one-broker platform. *Cost of doing it:* if Kafka is planned and I cannot see
it, the skill temporarily understates a roadmap item — recoverable in one paragraph.

**D-2 — Retire `alaa-trust-gateway-auth/references/full-guide.md` (62.6 KB) and `permission-bitmap.php`.**
Recommendation: yes to both. The guide is 77% duplicated, measured, and stale or weaker in three of the
places where it differs; four unique items migrate by hand and are listed in §5.2. The PHP file is a fourth
uncontrolled implementation of a contract `alaa-permission-generator` owns and emits for three languages,
untested, sitting over a catalog tool with ten open bugs and no CI. It is replaced by a routing line plus
an executable conformance-vector suite in the new script — which is the part this skill legitimately owns:
not "here is a decoder" but "here is the oracle any decoder must pass before its output is treated as
trusted context". *Risk:* something in the 62.6 KB is load-bearing and I did not spot it. Mitigation: both
files move to `_to_delete/` and both are recoverable from `git show 47b0bbef:<path>`.

**D-3 — Have `jitsi-platform-architect` declare itself decision-support for a capability under
consideration, in its first paragraph.** Recommendation: yes, unless Jitsi is deployed somewhere I cannot
see. Nothing in the mounted repository references it outside three index entries. If it is deployed, tell
me where and the rewrite states that instead; the rest of the specification is unaffected either way.

**D-4 — Is Bale live in production?** `alaa-services-contract references/23-…:183-194` documents `auth`'s
direct Mediana call path in detail and mentions no Bale client; `references/27-…:86-95` lists four
command families, all SMS or storage, none for Bale. I cannot tell from the skills repository whether Bale
is live, behind an unregistered path, or not yet integrated. It changes how much failure-behaviour material
the rewrite carries. My default if you do not answer: write it as though it is live, because the cost of
over-specifying failure behaviour is a few kilobytes and the cost of under-specifying it is a double-sent
OTP.

**D-5 — Narrow `alaa-sms-provider-mediana`'s always-loaded body to the two send modes the fleet actually
commands.** Recommendation: yes. `webservice` and `pattern` stay in the body with the
`pattern_values[] → params{}` mapping; `votp`, cancel, price and the URL-send endpoint move to a reference
behind a stated condition; the ten bulk and targeting modes become a single router row gated on explicit
product, legal and account-owner approval, with no field-level detail in the skill. Evidence is the
notification command contract, which is evidence about the command envelope rather than proof about every
call site — so if a service calls the provider client directly for votp or a bulk mode, say so and that
mode stays.

**D-6 — Keep `alaa-async-messaging/references/queues-best-practices.md` as a one-line pointer stub.**
Recommendation: yes. `alaa-laravel-architecture references/30-events-and-outbox-seam.md:14` cites it **by
filename**, Batch 2 is closed, and this batch may not edit it. A stub costs one line; a broken cross-skill
path costs an agent a wasted hop and will surface again in Batch 8's link check. The alternative is to let
Batch 8 fix the citation.

**D-7 — Do `tusd-upload-platform`'s four Vue-shape assets stay?**
(`TusUploadPanel.vue`, `useUploadQueueStore.ts`, `quasar.boot.uploads.ts`, `quasar.boot.sentry.ts`.)
Recommendation: **keep them and scope them**, rather than retire. Batch 6 has not run and cannot receive
them, so retiring now creates a real gap in a working reference implementation to satisfy a boundary that
does not yet have a home. The rewrite instead states the boundary explicitly — this skill owns tus-protocol
behaviour in these files and nothing about component structure, store shape, boot-file convention or SSR
wiring — and fixes the state-enum divergence so Batch 6 inherits one canonical list. The lane recommended
retiring them; I disagree on sequencing grounds and want your call.

**D-8 — Settle the Bale `request_id` derivation.** Two skills disagree.
`alaa-bale-provider references/bale-safir-api.md:241-242` says derive it from notification ID, recipient ID
and template ID; `alaa-golang-clean-code-principles references/20-…:137` says it is the delivery's public
id, unchanged across retries. Recommendation: **the Go skill's version wins**, because
`alaa-reliability-sla references/60-idempotency.md:12` forbids deriving a key from request content and the
Bale rule's inputs *are* request content — following it exactly suppresses a legitimate second OTP to the
same recipient. Batch 5 corrects the Bale side; the Go-side pointer is out of batch and should be turned
into a route rather than a restatement in whichever batch owns it next.

---

## 10. Out-of-batch findings — reported, not fixed

**Wrong or dangling inbound pointers into Batch 5 skills:**

- `alaa-go-chi-development references/12-kit-capability-map.md:35` routes "Trusted headers, `TrustCtx`,
  **TOTP step-up**, tenancy" to `/alaa-trust-gateway-auth`, which holds no gateway TOTP material at all.
  The owner is `alaa-services-contract references/32-auth-totp-and-step-up-contract.md`.
- `alaa-controlled-ops references/90-source-map.md:18` — same wrong TOTP pointer, and its bitmap half
  should point at `alaa-permission-generator`.
- `alaa-golang references/61-redis-cache-layer.md:117` routes "any need to cache authorization" to
  `/alaa-trust-gateway-auth`; that skill says nothing about caching a trust decision. Either the pointer
  moves to `/alaa-security-review` or the trust skill gains the rule.
- `alaa-golang references/20-sohrab-companions.md:42` routes "resumable upload behaviour or the tusd
  service" to `/tusd-upload-platform`, which routes Go work straight back to `$alaa-golang`. Circular; one
  side must state where Go-embedded-tusd code shape is decided.
- `alaa-services-contract references/30-…:77,80` delegates `X-User-Mobile` handling and "the exact auth
  error codes" to `$alaa-trust-gateway-auth` in `$`-form only, with no file path and no `/`-form.
- `alaa-golang-clean-code-principles references/90-source-map.md:43` and
  `alaa-golang references/20-sohrab-companions.md:43` route provider idempotency to both provider skills;
  neither routes back. The graph is one-directional.

**Gaps in `alaa-services-contract` found from the consumer side:**

- Bitmap ids `92-95` (`upload_to_content_service`, `upload_to_ticket_service`, `upload_to_auth_service`,
  `upload_to_comment_service`) are assigned to a `tusd` service at
  `references/35-permission-catalog-and-service-configs.md:65-66,87`, and **no skill anywhere states how a
  service consumes them.**
- `references/24-metric-registry.md` contains zero `upload` or `tusd` rows, and `alaa-observability-soc`
  contains none either — a service whose primary signals are `tusd_*` has no entry in the name registry or
  the requirement-level owner.
- `references/27-notification-service-contract.md` defines the SMS command families and names neither
  provider skill; the `pattern_values: [{key,value}]` array versus Mediana's `params` object mismatch lives
  exactly on that seam and is documented on neither side.
- `references/23-…:215` assigns "DLQ replay for any queue in this table" to `alaa-async-messaging` while
  `alaa-laravel-job-rabbitmq/SKILL.md:180-181` assigns DLQ *strategy* to `alaa-reliability-sla`. The split
  is consistent — mechanics here, strategy there — but the word "DLQ" appears on both sides of the line and
  deserves one clarifying clause.

**Machine-specific paths outside this batch:**

- `alaa-controlled-ops references/20-package-service-adoption.md:13` — "`SATIS_LOCAL_DIR` … Default
  `D:\satis-local`", a hardcoded machine path used as a real default on a release-operations skill.
- `alaa-cc-orchestrator references/resource-policy.md:22` and
  `alaa-codex-orchestrator references/resource-policy.md:22` — `-WorkingDirectory "D:\path\to\repo"` in a
  copy-pasteable block. Reads as an intentional placeholder, so this is the milder case.

**Other:**

- `alaa-golang references/40-production-ready-package-catalog.md:4,97,150` presents Kafka as part of the
  stack and `franz-go` as the **default** Kafka client. Given zero Kafka anywhere else, that reads as
  availability; it should be marked absent with a kit-change-request path, as the kit-gap files mark other
  absences.
- The Horizon-is-not-for-RabbitMQ rule is stated independently in three skills
  (`alaa-laravel-job-rabbitmq/SKILL.md:3`, `alaa-data-layer references/50-…:157-158`,
  `alaa-async-messaging/SKILL.md:44-51`) with no named owner. Batch 5's version is the fullest and both
  others route Horizon decisions here, so this batch takes ownership; converting the other two into
  pointers is out of batch.
- `README.md:178` and `README.fa.md:104,109` describe `alaa-async-messaging` as Kafka-for-events and list
  `jitsi-platform-architect` with no register marker. Batch 8's ground.
- `_to_delete/` currently holds four empty directories from Batches 1–4. Expected — the owner clears them
  before each commit, and recovery is `git show <pre-batch-commit>:<path>`, never `_to_delete/`.

---

## 11. Unverified this session

Only the skills repository is mounted. `alaa-go-chi`, every service repository, and the network were all
unreachable, so the following are stated as unverified rather than asserted:

- **Whether any Ala service runs Kafka in production.** Verified absent from the skills repository, the
  contract registry, the metric registry and the supplied kit facts. That is strong negative evidence, not
  a confirmation that it is absent from the estate.
- **Every vendor fact in both provider skills** — Bale Safir endpoints, the 500 MB upload ceiling, the
  seven error codes, the OTP numeric constraint, `request_id` replay semantics, and whether Safir publishes
  a rate limit; and for Mediana, the base URL, all fourteen `sending_type` values, the "API keys do not
  expire" claim, the single-recipient pattern limit, the five-minute cancel window, the operator IDs and
  the `message_code` values. None was checked. The answerable question was whether provenance is recorded,
  and it is not.
- **Every upstream Jitsi fact** — the nine IFrame event names, the five commands, the four functions, the
  `config.js` layering, the `jitsi-meet-tokens` claim set, the current `docker-jitsi-meet` release.
- **Whether tusd rejects an upload when a blocking `pre-create` hook times out.** The rewrite must make the
  agent verify this against the installed version rather than assert either posture.
- **Whether the gateway forwards `X-User-Roles` today.** The skill contradicts itself and
  `alaa-services-contract references/30-…:32-35` reports a 2026-07-25 fleet survey in which it was
  projected. The survey is the stronger evidence; it was not confirmed against gateway config.
- **Whether `alaa-permission-catalog` currently allocates the bitmap ranges `alaa-trust-gateway-auth` names**
  (64-78, 79-91, 92-95, 96-104). Given ten open bugs, no CI and unenforced id-reuse policy, every id range
  in that skill is treated as unverified regardless, which is why the rewrite routes rather than restates.
- **Whether the tusd client assets mirror a real frontend repository.** From content alone they read as
  skill-owned reference code; drift cannot be excluded by reading this repository.
- **`assets/vendor-sdk.go` was not compiled** (no Go toolchain) and `references/permission-bitmap.php` was
  not executed (no PHP). Both were read as source.
- **`mqkit`'s publisher-confirm surface**, its timeout behaviour and its nack behaviour. Phase 2 must
  verify against kit source before stating them, or say "unverified" in the file.
- **Whether `MQ_PREFETCH` exists as a key today.** Supplied as "ratified but not implemented"; not
  re-derived here.

---

## 12. Phase 2 execution plan

Six lanes, one per skill, all on the escalated implementer under the named criterion "authoring an artifact
whose deliverable is judgment itself". The lanes have disjoint write scopes and go out together, with two
sequencing constraints:

1. **`alaa-async-messaging` publishes one seam that three other lanes consume**: the rule that a provider
   send or an upload completion is dispatched from a durable row, never from inside the request that
   created it, and that the row's public id is what becomes the vendor idempotency key. Both provider lanes
   and the tusd lane route to it in one line each and none of them describes an outbox. That seam is
   currently stated nowhere — `alaa-async-messaging` contains zero occurrences of `provider`, `external
   send` or `third-party`.
2. **`alaa-trust-gateway-auth` publishes one anchor two other lanes consume**: the exact trusted-header set
   a service behind the gateway may believe, the obligation on a directly-reachable service to strip and
   reject those headers at its own edge, and whether per-resource authorization on a non-`POST` method is
   the gateway's or a sidecar's. `tusd-upload-platform`'s whole authorization model rests on the third
   point and currently asserts it without a source; `jitsi-platform-architect` needs the first for its mint
   boundary.

Both seams are one paragraph each and are written into the dispatch of the consuming lanes rather than
waited on, so the lanes still run concurrently.

Every lane finishes by: running its own script and reporting what it observed; confirming every
`references/*` path it names resolves; moving retired files to `_to_delete/20260727-batch5/` and listing
them; and reporting body size before and after, net of the description, with the named capability behind
any growth.

The batch finishes by re-running the repository pack validator, confirming `git status` scoped to the six
directories shows only intended changes, and verifying on disk that what was written actually landed.
