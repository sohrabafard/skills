# Upgrade Batch 8 — Observability, documentation, and knowledge

**Analysis draft, written 2026-07-29. Phase 1 output. This file is the working input Phase 2
executes from.**

Membership, from `UPGRADE-CARRYOVER.md:197`: `alaa-signoz-clickhouse-docs`,
`vector-rust-observability-pipelines`, `alaa-docs-farsi`, `alaa-postman-collections`,
`alaa-basic-memory-os` — plus the repository-level cleanup in section 6 and a link check that every
cross-skill path in `skills/sohrab/` resolves.

Seven analysis lanes ran concurrently and read every file of every member in full: 84 files,
411 KB of skill material, plus a fleet-wide survey over all 67 skill directories and 4,328
git-tracked files. Every version, endpoint, table name, column name, flag and vendor claim asserted
by these five skills was checked against upstream on 2026-07-29. Each lane's full evidence is
appended verbatim as Appendices A through G; this front section holds only what is true of the batch
as a whole, and the decisions Phase 2 needs before it starts.

---

## 1. The ten-criteria table for the whole batch

Section 2 of the carry-over, fifty cells. **SATISFIED** means the skill answers the criterion for its
own domain with evidence in the file. **FAIL** means it does not. **DELEGATED** means it names, at a
call site, the skill that legitimately owns the criterion — naming is the test, so a skill that
merely omits a subject someone else owns scores FAIL, not DELEGATED. **PARTIAL** means it answers
part of the criterion and leaves the rest neither answered nor routed. **n/a** means the criterion
has no referent in the domain.

| # | Criterion | `alaa-signoz-clickhouse-docs` | `vector-rust-observability-pipelines` | `alaa-docs-farsi` | `alaa-postman-collections` | `alaa-basic-memory-os` |
|---|---|---|---|---|---|---|
| 1 | Correctness and testability | FAIL | FAIL | FAIL | FAIL | FAIL |
| 2 | Failure behaviour | FAIL | FAIL | FAIL | **SATISFIED** | FAIL |
| 3 | Security | FAIL | FAIL | FAIL | **SATISFIED** | FAIL |
| 4 | Observability | DELEGATED (partial) | PARTIAL | DELEGATED (defective) | **DELEGATED** | FAIL |
| 5 | Concurrency and load | FAIL | FAIL | FAIL | FAIL | FAIL |
| 6 | Clean code, SOLID, patterns | n/a | PARTIAL | DELEGATED | **SATISFIED** | FAIL |
| 7 | Algorithms and data structures | FAIL | DELEGATED (unnamed → FAIL) | DELEGATED (weak) | FAIL | FAIL |
| 8 | Configurability | FAIL | FAIL | FAIL | **SATISFIED** | PARTIAL |
| 9 | Speed and debuggability | SATISFIED (weak) | FAIL | FAIL | **SATISFIED** | FAIL |
| 10 | Documentation | FAIL | PARTIAL | **SATISFIED** | **SATISFIED** | PARTIAL |
| | **Totals** | 1 S / 7 F / 1 D / 1 n-a | 0 S / 6 F / 3 P / 1 D-unnamed | 1 S / 6 F / 3 D | **6 S / 3 F / 1 D** | 0 S / 8 F / 2 P |

**Batch totals across fifty cells: 8 SATISFIED, 30 FAIL, 6 DELEGATED, 5 PARTIAL, 1 n/a.**

### 1.1 What the columns say

**One column is not like the others, and that is the batch's most useful finding.**
`alaa-postman-collections` scores 6 of 10 while the other four score 0 or 1 between them. It is also
the only member whose files were rewritten inside this programme's own timeframe — all 21 of them in
a single pass on 2026-07-25, four days ago. The difference is not subject matter and not author
talent; it is that the standard was applied. Its frontmatter carries a "do not use" clause, its
description is 889 characters, it has a `## When NOT to use` heading, its thirteen references sit
behind a `00-topic-map.md`, it names both trigger syntaxes, it pins no model, it ships two real
checkers, and it delegates observability to `alaa-services-contract` by name with three file paths.
Phase 2 must therefore **not** treat this skill like the other four. Most of it is already done, and
the work order in Appendix D is deliberately narrow: three assertions, one self-test harness, one
boundary correction, +3.6% net.

### 1.2 What the rows say

Two rows fail in **all five** members: **correctness and testability (1)** and **concurrency and
load (5)**. Two more fail in four of five: **failure behaviour (2)** and **security (3)**. Row 7,
algorithms and data structures, is satisfied by nobody — three outright failures and two delegations
so weak that neither names an owner at a call site.

This reproduces, for the sixth consecutive wave, the reading Batch 7 settled and which should now be
treated as a law of this corpus rather than a recurring surprise: **the quality bar's hardest
criteria are the ones that require the author to state a number, a budget, or a machine-checkable
predicate, and a skill assembled from vendor documentation never contains one.** Four of these five
skills are assemblies of vendor documentation. The fifth is not, and it is the one that passes.

Batch 8 adds a sharpening that is specific to its subject, and Phase 2 should carry it into the
rewrites as a stated principle:

> **A skill that teaches observability and cannot describe its own failure modes is not merely
> incomplete — it is self-refuting.** `vector-rust-observability-pipelines` is the clearest case. It
> exists to move telemetry, its entire value is what happens under load and under failure, and
> `references/BUFFERS_AND_ACKS.md` is 742 bytes that state no default, no third `when_full` value,
> no retry option name, and nothing about what happens when the sink is gone. Meanwhile the fact
> that most needs saying — that a full disk buffer makes Vector forcefully stop itself — appears
> only inside `COMMUNITY_NOTES.md:12`, hedged, in a file whose own header declares its contents
> non-normative. A log pipeline that drops silently under load is an observability outage that
> hides itself, which is the exact failure the skill was created to prevent.

### 1.3 Cells that are not this batch's to own

Six cells are legitimate delegations and Phase 2 must preserve them rather than fill them:

- **Observability requirement levels and gates** belong to `alaa-observability-soc`; **observability
  names and values** belong to `alaa-services-contract`. Three members trespass on one or the other
  and the trespasses are itemised in §3 below.
- **Clean code, SOLID and patterns (6)** for `alaa-docs-farsi` correctly belongs elsewhere — the
  skill produces documents, not code.
- **Algorithms and data structures (7)** genuinely belongs to `alaa-algorithms-data-structures` for
  four of the five, but **no member names it at any call site**, so no member currently gets credit
  for the delegation. The fix is one sentence per skill, not new content.
- **Failure behaviour (2) and security (3)** are *not* delegable for
  `vector-rust-observability-pipelines` or `alaa-basic-memory-os`. Buffering, acknowledgement and
  backpressure are Vector's whole subject; an unauthenticated memory API on a LAN is a trust
  boundary. Both must answer these themselves.

---

## 2. Defect classes from section 3 — only those actually found

### Class 1 — Stale hardcoded model pins: **NOT PRESENT in this batch**

Zero hardcoded model names across all 84 files of all five members, verified by grep. This is the
second consecutive batch in which the carry-over's expectation of stale pins did not materialise;
Batch 7 recorded the same correction for its own three named skills. The defect class has been
cleared fleet-wide by earlier sweeps and should be demoted from "check all of them every time" to a
one-line grep.

One inherited instance survives **outside this repository** and is reported, not fixed:
`gateway/scripts/postman/generate_gateway_collection.sh` around line 1799 writes a model name into
generated Postman environment files. `alaa-postman-collections` is the skill that should have caught
it — it claims Postman environment JSON as its artifact at `references/10-scope-and-trigger-rules.md:10`,
owns the generated-artifact rule at `:61-69`, and **names that generator by path** at
`references/70-aggregate-collections-and-consumer-repos.md:77`. Neither of its scripts detects it: a
fixture environment containing `llm_model = "gpt-4o-mini"` produces no finding of any kind. Phase 2
adds the assertion; the regeneration remains the owner's.

### Class 2 — Wrong trigger syntax: **the batch's worst defect, in four of five members**

Measured in both directions, excluding `agents/openai.yaml` (Codex-only, correctly bare `$`) and
excluding shell variables:

| Skill | Codex `$name` | Claude Code `/name` | Verdict |
|---|---|---|---|
| `alaa-docs-farsi` | 14 (9 in the always-loaded body) | **0** | invisible from Claude Code |
| `vector-rust-observability-pipelines` | 4 | **0** | invisible from Claude Code |
| `alaa-signoz-clickhouse-docs` | 3 | **0** | invisible from Claude Code |
| `alaa-basic-memory-os` | **0** | **0** | routes to nothing at all |
| `alaa-postman-collections` | present | present | correct |

Fleet-wide the two syntaxes stand at 2,934 and 2,788 occurrences, so this is not drift — it is a
batch-local authoring artifact in four files that nobody has opened since before the convention was
written. `alaa-basic-memory-os` is the severe form: zero triggers of either syntax anywhere in
sixteen files means it names no companion skill at any call site, which is also why it scores zero
delegations in §1.

Additionally, `alaa-signoz-clickhouse-docs/SKILL.md:3` names its companion skill in the frontmatter
description **with no sigil at all**, so the description over-triggers and under-routes at once.

### Class 3 — Duplication between body and references: **found, and one instance is extreme**

- **`alaa-docs-farsi/references/full-guide.md` is 96.43% verbatim duplicate.** Measured both
  directions: 648 of 672 content lines from the seven split references appear verbatim in the guide
  (97.92% heading-normalised); 95.50% of the guide's 689 lines are reproduced by the references.
  Exactly **five lines** of unique rule text exist, all at
  `20-readme-big-picture-contract.md:21-26`. The name promises everything and the file delivers a
  stale copy: it omits `90-source-map.md` entirely and carries a lossy, **already-diverging** copy of
  `80-implementation-gap-backlog.md`, so `40-sync-workflow-and-evidence.md:73` and
  `full-guide.md:766` now point step 12 of the same workflow at two different rule sets. Retiring it
  recovers 52,953 bytes — 39.6% of the skill — while deleting no rule. `SKILL.md:127-128` is the
  standing instruction that produced it and must go with it.
  This is the Batch 6 pattern (99.75% overlap, retired) rather than the Batch 7 one (18.3% overlap,
  correctly kept). The number, not the impression, decides it.
- **`vector-rust-observability-pipelines` duplicates in the opposite direction.** Its body is 9,487
  bytes and its eleven references total ~13 KB, median 971 bytes against a fleet median of 6,522.
  Only 20 of the fleet's 669 other reference files are smaller than this skill's *largest*. It has
  the highest body-to-total ratio in the fleet, 0.368. The content is not duplicated so much as
  never moved down.
- **`alaa-postman-collections` is clean**: an automated probe found 1 duplicated sentence in 60 body
  sentences.

### Class 4 — Project-specific content in an always-loaded body: **found**

Four of five members exceed the repository validator's 120-line body warning:
`vector-rust-observability-pipelines` **227** (the fleet record), `alaa-postman-collections` **154**,
`alaa-basic-memory-os` **140**, `alaa-docs-farsi` **127**. `alaa-signoz-clickhouse-docs` is the only
member under the line. Fleet-wide 22 skills carry this warning, so Phase 2 treats it as a batch
obligation and reports it as a fleet convention question rather than fixing it outside the batch.

### Class 5 — Long numbered procedures: **found in one member**

`vector-rust-observability-pipelines/SKILL.md` carries a 0.53 migration checklist as a linear
numbered list at `:96-99`, which is exactly the recovery-shaped content the carry-over says to
restructure by failure class. It is also **wrong in three of its four claims** — see §4.

### Class 6 — Descriptions that only say when to use: **not present, mechanically**

All five members carry a heading matching `^#+\s+.*\b(when not to use|do not use)\b`, verified by
grep. All five descriptions are under the 900-character mandate and contain no angle brackets:
signoz 423, vector 237, docs-farsi 737, postman **889**, basic-memory 569. Postman sits 11
characters under the ceiling, so any Phase 2 edit to its description must re-measure.

### Class 7 — Fragile tooling: **found in three of the four script-bearing members**

- `alaa-docs-farsi/scripts/check_markdown_links.py` — `WINDOWS_ABS_RE` at `:17` is **dead code**:
  `is_external` matches `D:` as a URI scheme first, so both `D:/repo/x.md` and `C:\repo\x.md` pass
  clean. Those are verbatim the two counter-examples the skill's own
  `references/10-language-and-links.md:68-69` gives.
- `vector-rust-observability-pipelines/scripts/validate-and-test.sh` — cannot run in PowerShell at
  all, and `set -e` means `vector test` never runs once validate fails.
- `alaa-basic-memory-os/scripts/alaa_obsidian_linkcheck.ps1` — ends with **two NUL bytes**.
- Neither Postman script uses `Path(__file__).parents[N]` and neither writes temp directories inside
  the repository. Both use `encoding="utf-8-sig"` and survive a CRLF+BOM fixture cleanly, so the
  second Windows defect class the carry-over names is already closed there.

Outside the batch and reported, not fixed: the repository's own
`scripts/validate_sohrab_skill_pack.py` uses `Path(__file__).resolve().parents[1]` — defect class 7
verbatim, in the flagship tool.

### Class 8 — Shipped `__pycache__`: **NOT PRESENT**

Zero `__pycache__` directories and zero `.pyc` files across all five members, verified by `find`.

### Classes 9, 10, 11 — measured against section 2, shrunk, boundaries checked

Covered in §1, §5 and the per-lane appendices. On class 10, three of five members **shrink** under
the Phase 2 plan (docs-farsi −39.6% net, signoz −8%, basic-memory restructured) and two grow with a
named capability: `vector-rust-observability-pipelines` roughly 3.4× because it currently states
almost none of its own subject, and `alaa-postman-collections` by 3.6% for a self-test harness it
does not have.

### The class this batch adds: **the checker that cannot fail**

Batch 7 named the checker-returns-clean-on-unparsed-input defect. Batch 8 found a strictly worse
sibling in three separate places, and it deserves its own name because the fix is different — the
input parses fine, and the assertion is simply unreachable.

1. **`alaa-postman-collections` — a gate no conforming collection can fail.**
   `references/42-scripts-and-state-capture.md:74-77` makes a capture success-guard mandatory. Both
   scripts enforce it by substring-searching the *whole* test script for `pm.response.code`
   (`validate_postman_artifacts.py:88-93`, `audit_collection_contract.py:294-299`). Separately,
   `references/43-response-tests.md:60` mandates `pm.expect(pm.response.code).to.eql(200)` on every
   request. So the string is always present and the guard check always passes. Proved with a fixture
   that writes the token unconditionally on line 1: `Validation passed with no issues. EXIT=0`.
2. **`alaa-postman-collections` — clean on an artifact with nothing in it.** A valid v2.1 collection
   with two folders and zero requests, run with *every* `--require-*` flag:
   `Validation passed with no issues. EXIT=0`. Every flag is vacuous because each fires per request
   item while `validate_postman_artifacts.py:659-661` only checks that the top-level `item` array is
   non-empty. This is not hypothetical —
   `references/70-aggregate-collections-and-consumer-repos.md:60-63` names two merge-program
   invariants that produce exactly this artifact. The auditor already catches it at `:373-374`, so
   the fix is a five-line port.
3. **`alaa-basic-memory-os` — the one checker is wrong in both directions.**
   `alaa_obsidian_linkcheck.ps1` on a *clean* vault prints a correct report, then errors and
   **exits 1**. Strip its two trailing NUL bytes and it **exits 0 on a vault with a broken link** —
   it contains no `exit` statement at all. In neither state does it report the truth. And
   `alaa_memory_health.ps1:48` captures `bm`'s stdout into `$code`, so `$code -ne 0` is truthy
   whenever `bm` prints anything: every schema type reports failure on every clean run, while
   `-Strict`'s `exit $code` on an array **exits 0**, so a CI gate reads validation failure as a pass.
   All reproduced under PowerShell 7.4.6.

**The rule Phase 2 writes into every checker it ships:** an assertion must be shown to fail on an
input that violates it, in a committed fixture, before the checker is allowed to report clean on
anything. A green checker with no red fixture is decoration.

---

## 3. Boundary trespass and the boundaries this batch settles

### 3.1 Observability trespass — three members, one owner pair

`alaa-services-contract` owns every observability NAME and VALUE; `alaa-observability-soc` owns every
REQUIREMENT LEVEL, GATE and REASON. On conflict SOC wins on whether something is required and the
contract wins on what it is called. Three members break this:

- **`alaa-signoz-clickhouse-docs`** states cardinality guidance in preference form ("avoid
  high-cardinality") where `alaa-observability-soc` already states a hard ceiling of 50 distinct
  label values. A preference verb standing where a constraint exists is the wording-test failure
  the carry-over names, and here it also contradicts a binding rule.
- **`vector-rust-observability-pipelines`** offers `block` and `drop_newest` neutrally, while
  `alaa-observability-soc/SKILL.md:36` already binds the fleet: *"Telemetry is fail-open for product
  traffic: a failed … Vector sidecar … degrades."* SOC wins on requirement level, so the skill does
  not merely omit a rule — it contradicts one.
- **`alaa-docs-farsi/references/60-errors-events-observability-contract.md:104`** states
  `request-id`, where `alaa-services-contract references/20-operational-and-observability-contract.md:12`
  owns the name `X-Request-Id`. That is a **wrong value**, not just a missing citation. Note the
  lane's own correction to its brief: this file states no requirement level and no gate, and every
  obligation in it binds the *document* rather than the service, so the two name citations are its
  only trespass.
- **`alaa-basic-memory-os/references/drift-management.md:11`** sets SOC severity levels, a
  requirement level it does not own.

### 3.2 The three-way ClickHouse boundary — proposed, needs the owner's ratification

Three skills touch ClickHouse and none of them knows the others exist. `grep -rni signoz` over all
eighteen files of `clickhouse-performance-schema-ops` returns zero;
`grep -rn clickhouse-performance-schema-ops` over `alaa-signoz-clickhouse-docs` returns zero.
Meanwhile that skill's rule 2 makes a tenant predicate mandatory on every query, and **not one of
`alaa-signoz-clickhouse-docs`'s eleven example queries has one.**

The proposed line, written in the same words on all three sides:

> **`clickhouse-performance-schema-ops` owns what a ClickHouse table must be** — engine, sorting key,
> partitioning, TTL, compression, and the tenant predicate — **for tables the fleet controls.**
> **`alaa-signoz-clickhouse-docs` owns how a SigNoz-owned table is queried**, and states explicitly
> that those tables are **vendor-owned and read-only to the fleet**, which is a third audience
> `clickhouse-performance-schema-ops` does not have and which is why the tenant rule does not
> transfer unchanged. **`vector-rust-observability-pipelines` owns what the pipeline writes into a
> ClickHouse table and how it behaves when that table is unreachable**, and decides no schema.

`clickhouse-performance-schema-ops/SKILL.md:49-51` already names the Vector skill as the owner of
"what the pipeline writes", so one third of this boundary is already agreed from the far side. The
other two thirds are proposed, not settled, and `clickhouse-performance-schema-ops` is outside Batch
8's membership — so Phase 2 writes the two in-batch halves and the third stays a reported item.

### 3.3 The Persian-documentation contradiction — the batch's sharpest ownership defect

`grep -rnP '(*UTF)[\x{0600}-\x{06FF}]'` over `alaa-docs-farsi`, on the staged copy **and** on the
device original, returns **zero matches**. A byte-level scan finds zero non-ASCII characters in all
fourteen files. `SKILL.md:12` and `:63` mandate **English** output.

Meanwhile six fleet call sites route Persian deliverables to this skill, two of them inside
`alaa-frontend-doc-annotations`, which Batch 6 shipped at standard:
`alaa-frontend-doc-annotations/SKILL.md:13-15` reads *"Persian belongs in … Persian-language
deliverables, which are `/alaa-docs-farsi`"*, and `references/10-annotation-boundaries.md:86` repeats
it. `UPGRADE-BATCH-6-ANALYSIS.md:2118` records that Batch 6 saw this seam and settled it on the wrong
assumption, because the skill was out of its tree at the time. `README.fa.md:120` describes the skill
as writing Persian documentation while its own frontmatter says it produces simple-English docs.

**Persian deliverables are currently unowned, and a skill named `alaa-docs-farsi` is the reason
nobody noticed.** This needs the owner's decision — see §6, Q3.

### 3.4 Other boundaries, each with the evidence

- **`alaa-postman-collections` ↔ `alaa-laravel-public-api-contract-pack`.** One-sided: the Laravel
  pack delegates "collection and environment generation to /alaa-postman-collections" in its
  frontmatter and names it at five call sites; this skill names it **zero** times while
  `references/25-public-api-contract-and-sdk-readiness.md:3` claims public-contract synchronisation
  is "mandatory for this skill" and `:20-22` prescribes a competing location. Proposed: the Laravel
  pack owns *what the contract is* — its gate is route-inventory-driven from
  `php artisan route:list --json`, evidence this skill cannot obtain — and this skill owns *how the
  collection proves it*, running that pack's `contract_pack_audit.py` for parity.
- **`alaa-basic-memory-os` ↔ `alaa-workflow`.** `references/compact-and-handoff.md` (625 bytes)
  restates material that `alaa-workflow/references/artifact-lifecycle.md:61` explicitly closes:
  *"Do not restate them here."* Retire it.
- **`alaa-docs-farsi` ↔ `alaa-postman-collections`.** API documentation is the overlap: the docs
  skill produces `docs/api-summary.md` and the Postman skill produces request documentation blocks,
  and **neither mentions the other's artifact anywhere.** Proposed and flagged as needing reciprocal
  agreement; both are in this batch, so Phase 2 can write both halves.
- **`alaa-signoz-clickhouse-docs` should gain the service-topology material.** SigNoz's dependency
  graph API is verified at source (§4) and the skill mentions none of it. It belongs here as
  `references/50-service-topology.md`, because a missing span is exactly what erases an edge — the
  same failure class the skill already diagnoses.

---

## 4. Factual currency — everything checked on 2026-07-29

Decision D10 requires every skill to cover the latest stable release, verified on the day, and to
state the command that re-derives each pin. Full per-claim tables with source URLs and re-derivation
commands are in the appendices; this is what changes Phase 2's work.

### 4.1 Stale, and stale in a way that produces wrong work

**`vector-rust-observability-pipelines` is the worst-affected file set in the batch.**

- Current Vector is **0.57.0, 14 July 2026**. The skill is pinned to **0.53.0**, dated 2026-03-01.
- **All three shipped config templates fail `vector validate`.** VRL diagnostic E651 ("unnecessary
  error coalescing operation") is a compile-time error, and `string!(x) ?? "default"` triggers it
  because `string!` is infallible. Six occurrences: `vector-basic.yaml:12,13`,
  `vector-clickhouse.yaml:12,13,14`, `common.vrl:5`. `vector-clickhouse.yaml:14`
  (`.ts = .timestamp ?? now()`) additionally does not do what it appears to, because `??` coalesces
  errors, not null. `SKILL.md:49` instructs the agent to run `vector validate` and
  `scripts/validate-and-test.sh` exists to do exactly that — running the skill's own script over the
  skill's own templates once would have found all six.
- **0.57.0 disabled `${VAR}` interpolation by default**, which silently breaks
  `vector-clickhouse.yaml:26-28`: validation still passes and the sink authenticates with the
  literal string `${CLICKHOUSE_PASSWORD}`.
- 0.57.0 also added sink-template confinement, rejecting a templated `table:` at startup —
  `SKILL.md:131` recommends exactly that pattern — and fixed a ClickHouse SQL injection.
- **The 0.53 migration checklist is wrong in three of four claims** (`SKILL.md:96-99`,
  `INTERNAL_MONITORING.md:21-25`). The actual renames are `buffer_max_byte_size` →
  `buffer_max_size_bytes` and `buffer_byte_size` → `buffer_size_bytes`; the skill states the *old*
  names wrongly in both. Buckets went 20 → 26, not 10 → 26, and across all internal histograms.
  Two renames are missing entirely, as is the fact that old gauges survive a transition period. An
  agent following `SKILL.md:100` greps for names that never existed, finds nothing, and reports the
  migration clean.
- Caution for Phase 2: GitHub's `/releases/latest` for Vector returns `vdev-v0.3.3` and must not be
  used to derive the version.

**`alaa-postman-collections`: 12 VERIFIED, 3 STALE.** Every Insomnia importer claim verified verbatim
against current `master` source — the four accepted schema strings, the seven mapped auth types,
`.find()` taking only the first `prerequest`/`test` per scope, the `pm.`→`insomnia.` regex,
`item.response` never being read, and the whole 57-line environment importer. The mock matching
algorithm and its tie-break verified verbatim. `pm.sendRequest` is **not** deprecated. Stale:
Postman's current collection schema is **3.0.0** and the skill never mentions it exists (pinning 2.1
remains correct but now needs its reason and a re-derivation command); **`insomnia-importers@3.6.0`,
the skill's portability proof in two places, is deprecated on npm** — last published 2022-09-27,
"Package no longer supported"; and the Insomnia docs no longer show `insomnia.response.code`, they
show `insomnia.response.status`, which may invert the skill's entire portable-assertion-form rule.
Newman 6.2.2 (2026-01-16) appears at zero call sites; Insomnia 12.6.0 (2026-05-22) is unpinned.

**`alaa-basic-memory-os`: the store it wraps is being replaced, and its own facts have moved.**
Basic Memory 0.22.1 / 2026-06-13 / AGPL-3.0-or-later VERIFIED (PyPI is authoritative; GitHub
Releases stops at 0.21.6). Issue **#980 still open** — 3–7 s reads, ~12 s search. Issue **#959 now
closed**, and the fix makes `bm status --wait` a **compatibility no-op on `main`** — a command this
skill asserts in seven places and which three of its scripts treat as fatal. `bm mcp --host` already
**defaults to `0.0.0.0`**, so the LAN capability the skill never uses is the default, and its
`127.0.0.1` is load-bearing and unexplained given there is no auth. Hindsight shipped **0.8.6 today,
2026-07-29T16:11:32Z**, one patch past the recorded 0.8.5; its ingest contract, `/mcp/{bank_id}/`,
`tags`/`all_strict`, `document_id` upsert, `chunks` = zero LLM cost and all four environment-variable
defaults (32 / true / 300 / hostname) VERIFIED against the 0.8.6 OpenAPI spec. Two corrections to the
carried record: **issue #1680 is closed, not open** — 0.8.6 ships an `agent_name` narrator override,
so the practice stands but the citation is stale — and `requestTimeoutSeconds` is recall **10 s** /
retain **15 s** with default `null`, not a flat 10 s. Codex CLI ≥ v0.116.0 is UNVERIFIABLE; the docs
gate on a `codex_hooks` feature flag instead.

**`alaa-signoz-clickhouse-docs`: every schema claim VERIFIED, stale by omission in six places.** All
table names, column names, time macros, the `$$` materialized-column convention and the `- 1800`
bucket idiom check out against both the docs and `signoz-otel-collector`'s schema migrator on
`main`. What is missing is newer than the skill: `samples_v4_agg_5m` / `samples_v4_agg_30m` rollups
(`metrics_migrations.go:759,782,794`) that **none** of the skill's metrics examples use — every one
scans raw `distributed_samples_v4`; `distributed_metadata`, which is the only executable answer to
the skill's own unexecutable rule *"confirm metric name, temporality, type, units"*
(`clickhouse-metrics-reference.md:74-82`); `distributed_exp_hist`, so the skill refuses to write
exponential-histogram SQL for want of a table that exists; `body_v2` with its JSON full-text index;
and the `MaxDynamicPaths: 100` cap on the `resource` JSON column. Versions: SigNoz **v0.135.0**,
`signoz-otel-collector` **v0.144.6**, SigNoz ships ClickHouse **25.12.5** against an upstream
ClickHouse of **26.7 (2026-07-22)** — seven minors of drift the skill pins nowhere.

**`alaa-docs-farsi`: nothing stale, because nothing is pinned.** All six URLs in
`references/90-source-map.md` resolve today. Zero version pins anywhere in the skill, so D10 is unmet
by absence rather than by staleness.

### 4.2 One claim reported UNVERIFIABLE because the vendor contradicts itself

`alaa-signoz-clickhouse-docs/SKILL.md:45`, `query-language-routing.md:9` and `:66`,
`validation-checklists.md:60` and both signal references all assert that ClickHouse SQL serves
"Dashboards **and ClickHouse-backed alerts**". Fetched today,
`signoz.io/docs/operate/clickhouse/clickhouse-queries/` states verbatim *"ClickHouse queries are only
supported in **Dashboards**"* — while that same page's opening paragraph and
`signoz.io/docs/alerts-management/log-based-alerts/` say the opposite. The skill silently resolves a
vendor coin-flip in favour of "alerts work". An agent that hands over alert SQL for a surface which
rejects it has produced unshippable work. This is a thirty-second check in the fleet's own SigNoz UI
and it is listed as owner decision Q5.

### 4.3 Corrections to the project-memory record on the SigNoz dependency-graph API

The route, `ViewAccess` requirement, request body and response shape are all confirmed at source, so
the capability stands. Two details in the record are wrong and one caveat resolves:

- It is registered at `pkg/query-service/app/http_handler.go:**527**`, not 531.
- The read path is `distributed_dependency_graph_minutes_**v2**` (`options.go:27`), not
  `dependency_graph_minutes`; v1 is being dropped (`traces_migrations.go:533`).
- The `db.system` collapse is confirmed verbatim in the materialized view
  (`dest = attribute_string_db$$system`).
- **The "async/queue edges unverified" caveat resolves, and the answer is half good:** a
  `messaging_calls_mv_v2` exists, so producer→broker edges *are* recorded, collapsed per messaging
  system — but there is **no broker→consumer edge**, because the service-calls materialized view
  requires `A.span_id = B.parent_span_id`. The graph is a lower bound in a specific, nameable way.

---

## 5. The two repository-level deliverables

### 5.1 The link check — the headline number was a measurement artifact

The carry-over assigns Batch 8 "a link check that every cross-skill path in `skills/sohrab/`
resolves". Two lanes measured it independently and disagreed by two orders of magnitude, so this
section records the reconciliation rather than the louder number.

The first resolver reported **582 unresolved bare paths across 223 files**. The survey lane
reproduced it (getting 619 on its own implementation, close enough to confirm the method) and then
found what both resolvers were rejecting. `alaa-frontend-developer/SKILL.md:33` reads:

```
`/alaa-testing-strategy` (`$alaa-testing-strategy`) `references/40-proof-strength.md`
```

The owner **is** named alongside the path. What breaks the match is the intervening backtick and
closing parenthesis, which defeat token adjacency. Four resolver generations produced a bit-identical
`references/` census once that was handled, so this is not regex luck.

**The corrected census, over 2,955 citations:**

| Class | Count |
|---|---|
| Citations scanned | 2,955 |
| Under `references/` (unambiguously skill-bundled) | 2,252 |
| RESOLVES-LOCALLY | 1,469 |
| RESOLVES-CROSS-SKILL, owner correctly attributed | 625 |
| Owner named nearby (the adjacency case above) | 150 |
| AMBIGUOUS-BARE | 3 |
| AMBIGUOUS-MULTI | 4 |
| **DANGLING** | **1** |
| Dangling with an owner named | 0 |

**Eight real `references/` defects fleet-wide.** The link check Batch 8 owes is, in substance,
already passing.

The 89 non-`references/` danglings are target-repository paths — `charts/gateway/…`,
`service-runtime-kit/…`, `$SKILL_DIR/…` — and adding `docs/` to the scan raises them to 520, of
which 422 are `docs/…`. **Any checker that fails on those gets switched off within a week**, which
is why §5.3 specifies a notation decision rather than a stricter regex.

### 5.2 The executable-check census

101 scripts across 43 skills; **24 skills ship zero**. 63 of 101 have a demonstrable exit-2 path; 49
of 101 implement all three of 0/1/2. Four of this batch's five members are in the zero-checker group
or ship a checker that cannot report the truth, which is why every Phase 2 work order in the
appendices ends with a named checker rather than a rule.

### 5.3 The tooling Phase 2 ships at fleet scope

Neither of these is a skill. Both are scripts under `skills/scripts/`, and both exist because a
human maintaining a list by hand is the cause of every index defect in §5.4.

- **`skills/scripts/check_fleet_references.py`** — the permanent cross-reference checker. Specified
  down to flags, six rule ids, the 0/1/2 triggers, and a baseline whose key deliberately excludes
  line numbers and which must *shrink*: a stale baseline entry exits 1, so the baseline cannot
  become a permanent amnesty. Seed baseline today is **8 entries** with `--strict-owner` off — small
  enough that it could ship with no baseline at all.
- **`skills/scripts/check_skill_index.py`** — asserts the two-way README ↔ directory identity in
  both directions and the normalised `AGENTS.md` / `CLAUDE.md` equality.

And three repairs to the repository's own **`scripts/validate_sohrab_skill_pack.py`**, whose defects
matter more than the errors it reports:

1. `:196` extracts `short_description` with a regex requiring **double quotes**, producing four
   false errors against valid YAML — two of them against `alaa-signoz-clickhouse-docs`, a member of
   this batch. Confirmed directly: that file's `short_description` is "SigNoz docs routing and
   ClickHouse SQL" (38 characters) and its `default_prompt` does mention
   `$alaa-signoz-clickhouse-docs`. Both reported errors are false.
2. `:221` is `return 1 if errors else 0` — **no exit code 2**, in the flagship tool of a programme
   whose defining deliverable is the 0/1/2 contract.
3. It uses `Path(__file__).resolve().parents[1]` (defect class 7), warns at 950 characters where the
   mandate is 900, and inspects only `SKILL.md` and `references/00-topic-map.md` — never the other
   738 Markdown files.

Current validator state, run today:
**51 errors across 30 of 67 skills, 26 warnings, exit 1** — of which 4 errors are false positives
from defect 1, so **47 real**. This corrects the carry-over's recorded 77.
`agents/openai.yaml`: 65 of 67 present, **50 fully valid**, 15 failing, 2 missing.
Batch 8's own five: `alaa-signoz-clickhouse-docs` 2 errors (both false),
`alaa-basic-memory-os` 2 errors (both **real** — its `openai.yaml` has no `interface:` block at all
and uses a `version`/`name`/`description` shape no other skill uses), and body-line warnings on four
of five.

### 5.4 The index audit

- **`README.md`'s headline defect is already fixed.** All ~20 phantom skills the carry-over lists now
  sit correctly in a "Consolidated or removed" section at `README.md:189-196`, each verified absent
  from disk. What remains false is `README.md:93` — *"Every folder in this directory appears exactly
  once below"* — where the map holds 65 names against 67 directories. The two missing are
  `alaa-input-normalization` and **`alaa-haproxy-lua`**. `README.fa.md` omits the same two and is
  otherwise a name-for-name match, so the two indexes tell the same lie rather than two different
  ones.
- **`alaa-haproxy-lua` is the entire remaining backlog, and nobody had written it down.**
  `grep -c "haproxy-lua" UPGRADE-CARRYOVER.md` returns **0**. It is in no batch membership, no
  candidate table, and neither README. It arrived in commit `b920bfdb "upgrade batch 4"` while not
  being a Batch 4 member, has been untouched since 2026-07-26, holds 138,994 bytes across 11
  references, and fails the validator on two rules. Batch 7 wired `alaa-haproxy` to route into it
  from four call sites, so it is reachable, never audited, and unlisted. The arithmetic closes
  exactly: 51 batch-assigned + 7 pre-programme + 8 programme-created = 66; disk holds 67; the
  residual is this one directory.
- **The count is 67.** The carry-over's "sixty-three" (and its own contradictory "sixty-eight" ninety
  lines later), one lane's 69 and project memory's 68 are all wrong.
- **`AGENTS.md` / `CLAUDE.md` have already begun to drift**, and the drift is invisible. The root
  pair share one git blob (`52209cfa…`), but the working tree has diverged: `AGENTS.md` is CRLF and
  shows ` M`, `CLAUDE.md` is LF and is clean; `core.autocrlf` is unset and there is no
  `.gitattributes`. Worse, `skills/sohrab/CLAUDE.md` is committed as mode `120000` with a **9-byte
  blob containing the literal text `AGENTS.md`** — on any Windows checkout without `core.symlinks`
  (git-for-Windows' default absent Developer Mode) that materialises as a 9-byte text file, and
  Claude Code loads it instead of the 10,205-byte contract **with no error**. The repository's own
  authority already rules on this: `alaa-prompting-guide/references/70-agent-instruction-files.md:80`
  names the Windows privilege requirement and `:78` directs mixed-OS teams to the **import bridge**
  as the documented recommendation, while `:82` calls the two-maintained-files pattern now in use at
  the root the worst option and `:98` lists it as a defect whose fix is "collapse to the import
  bridge".
- **Root `README.md` opens by declaring the repository deprecated**, inherited verbatim from the
  `openai/skills` fork, and points at a `skills/.experimental/` directory that does not exist. It is
  assigned to no rule and no batch, which is likely why it survived seven batches.
- **`install-skills.md:16` points the installer at `vendor\basic-memory\basic-memory`**, a nested
  duplicate holding **5** skills, while the real 14 sit one level up. The documented installer
  therefore links 5 of 14 basic-memory skills — directly relevant to `alaa-basic-memory-os`, whose
  wrap-don't-fork obligation is against that pack.
- `alaa-go-chi-development` ships **no `agents/openai.yaml`**, making `README.md:14` one exception
  short of true.
- `vector-rust-observability-pipelines/INSTALL.md` is **1 of 67** — no other skill ships one — and it
  is wrong on both of its claims: it names `~/.agents/skills` against the authoritative
  `install-skills.md` (`~/.codex/skills`), and asserts `allow_implicit_invocation: false` while its
  own `agents/openai.yaml:7` says `true`. Its `prompts/` directory is likewise 1 of 67
  (`alaa-shaka-player/prompts` is empty), duplicating `SKILL.md:196-212` on a subject the
  orchestrators and `alaa-prompting-guide` own. Its `references/README.md` is 1 of 67.

### 5.5 Carry-over items that can be closed

- **`UPGRADE-CARRYOVER.md:210` — the duplicate-script retirement landed.** Verified on disk today:
  `alaa-frontend-developer/scripts/` is empty, and both skills now route to the
  `alaa-quasar-app-vite-v3` copy correctly. No diff is possible because the duplicate is gone. Close
  the item.
- **`UPGRADE-CARRYOVER.md` Batch 7 memory item — the twenty `.fuse_hidden*` `AD` entries are gone**
  from both the worktree and the index. No `git rm --cached` is needed.
- **Router convention:** 29 of 67 skills carry a topic map (the carry-over records 28). Against the
  ≤8 / ≥9 rule, 61 conform and 6 violate, three in each direction. The rule survives contact with
  the data; what it does not answer is whether the topic map counts toward its own threshold, and
  three skills sit exactly on that seam.
- **Body-line warnings:** 22 skills, confirming the carry-over's count exactly.
  `vector-rust-observability-pipelines` holds the record at 227 lines, and four of five Batch 8
  members are in the table.
- **`_to_delete/` holds four dated batch directories — batch4, batch6, batch7, fuse-artifacts —
  containing zero files.** The "nothing is ever deleted" convention has no evidence behind it for
  three of seven batches. This is worth the owner knowing before Batch 8 retires ~76 KB into it.

One measurement failed and is reported unmeasured rather than estimated: `git status --porcelain`
timed out at 42 seconds through the device bridge and **was not retried**, per the carry-over's
warning about `index.lock`. No stale lock was left. `git ls-files` (4,328 files) succeeded and
supplied the index facts instead.

---

## 6. Section 4 candidate skills — verified against what was actually read

The carry-over's candidate table lists five. Four now exist on disk as skills this programme built,
and their presence is what makes most of Batch 8's gaps delegations rather than holes.

**`alaa-algorithms-data-structures` — exists, 80,233 bytes, and is the single most under-used skill
in this batch.** It is on disk and at standard, and **no Batch 8 member names it at any call site**,
which is precisely why criterion 7 scores zero satisfied across all five columns. This is not a
missing skill; it is five missing sentences. Note that two of the five domains genuinely need it:
`alaa-signoz-clickhouse-docs` writes SQL whose cost is a scan-versus-rollup choice with a real
complexity budget, and `alaa-postman-collections` ships a 37.6 KB validator whose per-item scanning
has a stated shape and no stated bound.

**`alaa-system-design` — exists, 82,953 bytes.** Covered. No Batch 8 member needs to own design
guidance, and the correct action is a routing sentence in `vector-rust-observability-pipelines`,
whose topology-shaping content at `references/TOPOLOGY_WORKFLOW.md` (862 bytes) is design guidance
wearing a pipeline label.

**`alaa-reliability-sla` — exists, 112,479 bytes, the largest of the four.** Covered, and it is the
correct owner of the buffering and degradation *reasoning* that
`vector-rust-observability-pipelines` currently omits. The division is already settled by Batch 1:
`alaa-reliability-sla` owns why a mechanism exists and how to choose its shape and states no Ala
number; `alaa-services-contract references/22-failure-load-and-deprecation-contract.md` owns every
Ala value. The Vector skill owns neither — it owns which Vector option expresses the chosen shape.
That is the third half of a boundary whose other two halves already exist.

**`alaa-testing-strategy` — exists, 82,284 bytes.** Covered. `alaa-postman-collections`
`references/43-response-tests.md` correctly does not restate it, and the remaining work is a naming
sentence.

**`alaa-design-patterns` — never built, and it should stay unbuilt.** This is the one candidate that
was never converted into a skill, and the evidence supports that decision rather than reversing it.
Design-pattern guidance is taught at five call sites on disk today —
`alaa-algorithms-data-structures/SKILL.md`, `alaa-golang-clean-code-principles/SKILL.md`,
`alaa-php-clean-code/SKILL.md`, `alaa-vue-typescript-clean-code/SKILL.md` and
`alaa-haproxy-lua/SKILL.md` — each binding the advice to a language whose idioms decide which
patterns earn their place. A cross-language pattern skill would have to state its advice in the
abstract, which is exactly the over-patterning failure mode the candidate row itself warns about.
Nothing in Batch 8 needed it: not one of the fifty criterion cells failed for want of pattern
guidance. **Recommendation: strike the row.**

---

## 7. Is a new skill required? **No — and that is the considered answer, not the easy one.**

Every one of the seven lanes reached this independently, from different evidence. The rule the batch
was given is that a new skill is justified only when an existing skill cannot own an observed gap
without violating its own boundary. Four gaps came close enough to test the rule, and all four
resolve inside existing boundaries:

1. **Persian deliverables are genuinely unowned** (§3.3). But the owner exists — the skill is named
   `alaa-docs-farsi`, six fleet call sites already route Persian to it, and the defect is that its
   own body mandates English. That is a contradiction to resolve inside one skill, not a second
   skill to create. Creating an `alaa-docs-persian` alongside it would leave two skills whose names
   both promise Persian and neither of which owns it unambiguously.
2. **`alaa-basic-memory-os` wraps a product being replaced.** The strongest case for a new skill in
   the batch, and it still fails the test: what the fleet actually routes to is the *capability*, not
   the store. The only upgraded skill that routes here describes it without naming a product —
   `alaa-golang/references/20-sohrab-companions.md:19`, "record a drift note, a decision, or context
   that a later session must find". That contract is unchanged by the swap. The answer is a rewrite
   and a rename, not an addition — see §8.
3. **The three-way ClickHouse boundary** (§3.2) needs a line drawn between three existing skills, not
   a fourth to arbitrate. A boundary skill is how a fleet acquires a fourth party to every argument.
4. **Fleet-scope cross-reference and index checking** (§5.3) is tooling under `skills/scripts/`. A
   script is not a skill, and dressing one as a skill would put executable logic behind a trigger
   condition that CI cannot evaluate.

The one thing this batch *should* create is two scripts and three script repairs, all named in §5.3.

---

## 8. The `alaa-basic-memory-os` decision — the batch's one structural change

This is set out separately because it is the only Phase 2 item that changes a skill's identity rather
than its contents, and because it must not be decided by inertia.

**The store is being replaced.** Basic Memory is AGPL-3.0 and still maintained, but its centre of
gravity has moved to a paid cloud tier, upstream issue #980 (open) records 3–7 second reads and ~12
second searches, and the local `sync` command was removed. Hindsight is the decided successor, and
its deployment is already designed and shipped as `D:\Sohrab\Project\raw\hindsight-setup.zip`.

**Three options, and the recommendation.**

| Option | What it costs |
|---|---|
| Rewrite in place as a Hindsight skill | Every fact in the body becomes a 0.x mechanic. Hindsight shipped **0.8.6 today**, one patch past the version recorded four hours earlier. A body made of Hindsight mechanics needs re-verification weekly. |
| Keep Basic Memory, add a successor skill | Two skills claiming one capability during a migration, and every routing sentence in the fleet has to name which one. This is the ambiguity §7 exists to avoid. |
| **Rewrite as a store-agnostic memory operating model, renamed `alaa-memory-os`, with Basic Memory and Hindsight as two adapter references** | A bounded rename — 4 call sites plus 3 carry-over mentions, fully enumerated in Appendix E. Everything durable in the current directory (the drift model, the Extraction and Design modes, repo-is-truth) is already store-independent; everything `bm`-shaped is where every defect in the skill lives. Store churn then lands in one adapter file instead of in the body. |

**Recommended: the third.** The evidence for it is in the fleet rather than in taste — what routes
here already describes the capability without naming a product.

Two sub-decisions gate Phase 2 and are the owner's:

- **The drift mechanism does not survive the move intact.** `drift-management.md:7` forbids silently
  picking a side; Hindsight's Reflect supersedes on latest `mentioned_at`, resolving disagreements
  by timestamp automatically. And because only `tags` are filterable at recall — `metadata` is not —
  `drift_status` becomes unqueryable. **Recommendation: the drift registry stays in the repository
  under version control**, where "do not delete" is a fact rather than a request. This also aligns
  with the standing rule that dependency edges are derived and never remembered.
- **Migration must use a custom timestamp-bearing import script.** The official Claude Code and
  Codex plugins never send `timestamp`, which would flatten all history into a single instant and
  destroy the supersession ordering that makes two-machine history resolve correctly.

---

## 9. Decisions that belong to the owner

Each carries a recommendation and the cost of the alternative. Q1 blocks part of Phase 2; the rest
can be answered while it runs.

**Q1 — The edit prohibition on `README.md` and `AGENTS.md`.** `UPGRADE-CARRYOVER.md:158` says these
files "belong to the human between batches, **and to Batch 8 at the end**"; `:216` says "Fix it in
Batch 8"; `:222` assigns `install-skills.md` likewise. The session prompt's hard rules say "never
edit README.md or UPGRADE-CARRYOVER.md". The prohibition's stated cause is concurrent batches, and
`:153` says Batch 8 runs alone — but it is a standing instruction and not mine to lift.
**Recommendation: a narrow lift covering exactly five files** — `skills/sohrab/README.md`,
`README.fa.md`, root `AGENTS.md`, root `CLAUDE.md`, `install-skills.md` — with the prohibition on
`UPGRADE-CARRYOVER.md` kept intact. The cost of the alternative is specific: a corrected inventory
shipped as a *new* file would be a third index in a tree whose own `AGENTS.md:15` says "A rule has
exactly one owning file", and nothing would route to it, because the thing that would route to it is
the file we may not edit. It would be correct and unreachable.

**Q2 — `alaa-basic-memory-os` → `alaa-memory-os`.** §8. **Recommendation: yes**, with the store-agnostic
rewrite. The cost is a rename touching 4 call sites and 3 carry-over mentions; the cost of not doing
it is a skill whose body needs re-verification every week against a 0.x product.

**Q3 — Who owns Persian deliverables?** §3.3. **Recommendation: the skill is right and the fleet is
wrong** — `alaa-docs-farsi` produces simple-English documentation by design, and the six call sites
that route Persian to it should be corrected. Two of those six are inside `alaa-frontend-doc-annotations`,
which is outside this batch, so they become a reported carry-over item rather than an edit. The
alternative — making the skill produce Persian — would contradict `SKILL.md:12` and `:63` and
invalidate its four contract references.

**Q4 — Does the fleet's SigNoz accept ClickHouse alert SQL?** §4.2. A thirty-second check in the
SigNoz UI closes it. **Recommendation: check before Phase 2 writes the routing rule**, because the
skill currently resolves a vendor self-contradiction silently and either answer produces a different
rule.

**Q5 — Is the fleet's SigNoz single-tenant?** This is the one place the two ClickHouse skills give an
agent directly contradictory instructions: `clickhouse-performance-schema-ops` makes a tenant
predicate mandatory on every query, and none of `alaa-signoz-clickhouse-docs`'s eleven examples has
one. **Recommendation: state the answer explicitly in both skills** rather than leaving the agent to
infer it.

**Q6 — `insomnia.response.code` versus `.status`.** Blocking for Appendix D: both bundled Postman
assets and a validator warning push every agent toward the form the current Insomnia documentation no
longer shows. The lane could not locate the SDK source file (404 on both `master` and `main`).
**Recommendation: settle it from the Insomnia SDK source before Phase 2 touches either asset**, since
guessing wrong changes the skill's entire portable-assertion rule.

**Q7 — The `alaa-` prefix, still deferred since Batch 1.** Seven skills lack it, one of which is in
this batch. **Recommendation: rename all seven together, after Batch 8, not inside it** — the
validator hardcodes a prefix list, and renaming exactly one makes the set less consistent rather than
more.

**Q8 — Does the topic map count toward its own ≤8 / ≥9 threshold?** The rule is silent and three
skills sit exactly on the seam. **Recommendation: no, it does not count.**

**Q9 — A distinct notation for target-repository paths.** §5.1. **Recommendation: yes** — that
ambiguity is the sole reason the fleet checker would otherwise need an 88-item exclusion list, and an
exclusion list is how a checker starts lying.

**Q10 — `alaa-haproxy-lua` needs a batch.** §5.4. 139 KB, never audited, in no plan, reachable from
four call sites in a skill that Batch 7 shipped at standard. **Recommendation: assign it a Batch 9
of one**, and add it to both READMEs in the same pass as `alaa-input-normalization`.

**Q11 — Read-only access to `D:\Sohrab\Project\raw\processed`.** Not mounted this session, so every
claim `alaa-basic-memory-os` makes about the Prompt 1/2/3 pipeline is UNVERIFIABLE. One read-only
grant closes it.

---

## 10. Phase 2 work order — summary

Per-file plans, target byte budgets and the capability earning any growth are in the appendices. In
brief:

| Skill | Direction | Named capability earning any growth |
|---|---|---|
| `alaa-signoz-clickhouse-docs` | **−8%** (retire 20.6 KB of link list, add 13.6 KB of references) | three checkers: link, schema, and SQL-rule |
| `vector-rust-observability-pipelines` | **≈3.4× (25.7 KB → ~88 KB)**, still under the fleet median | it currently states almost none of its own subject: buffers, acknowledgements, backpressure, sink failure |
| `alaa-docs-farsi` | **−39.6% net** | retire `full-guide.md`; the cross-reference checker moves to fleet scope |
| `alaa-postman-collections` | **+3.6%** | a self-test harness with red fixtures it does not have today |
| `alaa-basic-memory-os` → `alaa-memory-os` | restructured, not grown | store-agnostic operating model with two adapter references |

Cross-cutting, applied to all five: both trigger syntaxes at every call site; a routing sentence to
`alaa-algorithms-data-structures`, `alaa-reliability-sla`, `alaa-system-design` and
`alaa-testing-strategy` wherever a criterion is delegated; every observability name and requirement
level routed to its owner rather than restated; every version pin accompanied by the command that
re-derives it; every body brought under 120 lines; and every shipped assertion accompanied by a
committed fixture that makes it fail.

---

## Appendices

Each lane's complete evidence follows verbatim, unedited. These are the working documents Phase 2
executes from; the front section above is a reading of them, not a replacement for them.

- **Appendix A** — `alaa-signoz-clickhouse-docs`
- **Appendix B** — `vector-rust-observability-pipelines`
- **Appendix C** — `alaa-docs-farsi`
- **Appendix D** — `alaa-postman-collections`
- **Appendix E** — `alaa-basic-memory-os`
- **Appendix F** — Repository hygiene and cross-reference survey
- **Appendix G** — Repository index and inventory audit



---

# Appendix A — `alaa-signoz-clickhouse-docs`

# Lane L1 — `alaa-signoz-clickhouse-docs`

Phase 1 analysis. Read-only. Analysis date **2026-07-29**. Every version, table, column and
endpoint below was checked on that date against the sources named beside it; nothing is asserted
from memory.

Staged copy read in full: `/home/claude/b8/src/alaa-signoz-clickhouse-docs/` (13 files, 63,135 B).
Device original `D:\Sohrab\Project\skills\skills\sohrab\alaa-signoz-clickhouse-docs\` was reached
read-only through `mcp__remote-devices__device_bash`; nothing was written to the device.

---

## 1. Inventory

| File | Bytes | What it actually contains |
|---|---:|---|
| `SKILL.md` | 5,608 | Frontmatter (423-char description), a 4-step quick start, a "Do not use for" list, a 10-row mode-routing table, 12 ClickHouse operating rules, a 5-step missing-spans workflow, an output contract, stop rules. 83 lines total, 78 body lines. |
| `agents/openai.yaml` | 330 | Codex metadata only: `display_name`, 38-char `short_description`, `default_prompt` naming `$alaa-signoz-clickhouse-docs`, `brand_color`, `allow_implicit_invocation: true`. Valid against the pack validator's two extra rules. |
| `references/00-topic-map.md` | 2,307 | Two lists: a heading-mirror list of the ten sibling files, then a "Fast routing" list of ten quoted user questions mapped to a file. The second list is the only part that routes; the first is a `ls` in prose. |
| `references/source-map.md` | 3,470 | 19 official URLs, a five-bullet "checked baseline" with no date and no re-derivation command, four freshness triggers, a troubleshooting-source rule. |
| `references/docs-routing.md` | 7,614 | An 18-row table of SigNoz doc URLs with a "use it when" column, four page-selection rules, five `site:` search patterns, an `Accept: text/markdown` fetch note. Pure link list — no SigNoz behaviour is stated, only where to read about it. |
| `references/instrumentation-routing.md` | 3,437 | A four-question decision flow over SigNoz doc URLs, a "when to prefer the Collector" list, an eleven-item language list, answering rules. Contains one factual assertion: the Cloud OTLP endpoint shape `https://ingest.<region>.signoz.cloud:443`. |
| `references/log-collection-routing.md` | 3,272 | An eight-row situation→page table, three hub URLs, five routing rules, a production log-safety note. Link list plus five soft rules. |
| `references/query-language-routing.md` | 3,720 | Surface-selection rules (Explorer vs Dashboard vs Alert), five doc URLs, Query Builder v5 use cases, filtering/aggregation/variable/field-ambiguity rules, an answer shape. The only file that decides *which surface*, and it is the file whose central claim is contradicted upstream (§5.7). |
| `references/clickhouse-logs-reference.md` | 7,541 | The real thing: `signoz_logs` tables, 12 columns, four "non-negotiable patterns", a materialized-column preference table, three panel-shape templates, three worked queries, a final checklist, a "2026 production update" section appended after a `# `-level heading. |
| `references/clickhouse-traces-reference.md` | 9,165 | Same shape for `signoz_traces`: three tables, 16 columns, four patterns, a five-row materialized-column table, three panel shapes, three worked queries including the missing-parent anti-join, a Laravel/PHP root-cause note, a checklist, a "2026 production update". |
| `references/clickhouse-metrics-reference.md` | 10,029 | Same shape for `signoz_metrics`: four tables, two column lists, five patterns, a `SHOW/DESCRIBE` discovery block, five worked queries (fingerprint lookup, gauge, counter rate, error-rate ratio, histogram p99), a repair checklist, four refusal conditions. |
| `references/observability-guardrails.md` | 3,974 | Not a SigNoz file. Generic observability doctrine: signal choice, OTel rules, Collector mental model, correlation, missing-spans causes, field quality, cardinality and privacy, defaults. Line 4 states its own provenance: "distills the most useful generic guardrails from the merged observability skill". |
| `references/validation-checklists.md` | 2,668 | Eight numbered checks (surface, signal/table, time bounds, output shape, safety, performance, schema uncertainty) plus a final-answer template. No tool evaluates any of them. |

No `scripts/`, no `assets/`, no `__pycache__`, no `INSTALL.md`. 11 references → the
`references/00-topic-map.md` router placement is **correct** under the `AGENTS.md:49` threshold
("9 or more moves the router into `references/00-topic-map.md`"), and the body correctly keeps a
pointer at `SKILL.md:2`. But the body *also* carries a full 10-row `## Mode routing` table
(`SKILL.md:29–41`), which is a second router. `AGENTS.md:49`: *"Two routers in one skill is the
defect: they drift, and the agent follows whichever it reads first."* They have already drifted —
see §3, D-3a.

---

## 2. Is this a documentation-routing skill or a query skill?

**It is both, badly separated, and the split is roughly 40/60 by bytes.**

- **Link-list half — 20,043 B (32%)**: `docs-routing.md`, `instrumentation-routing.md`,
  `log-collection-routing.md`, `source-map.md`, `00-topic-map.md`. These files contain **36 distinct
  URLs and almost no rules**. `docs-routing.md` is an 18-row table whose every cell is a URL plus a
  restatement of that URL's own title. Follow every sentence in it exactly and the agent has opened a
  web page; it has not decided anything a competent agent would not have decided from
  `site:signoz.io/docs <topic>` — which the file itself supplies at line 40 as a fallback, making
  most of the table redundant with its own escape hatch.
- **Rules half — 26,735 B (42%)**: the three ClickHouse references. These *do* teach an agent to
  query the schema: they name tables, columns, the bucket-filter idiom, the resource-CTE shape, the
  `GLOBAL IN` requirement, and three panel output shapes. This half is genuinely load-bearing and
  its factual content is, with two exceptions, correct today (§5).
- **Trespassing half — 6,642 B (11%)**: `observability-guardrails.md` and the safety sections of
  `validation-checklists.md` restate telemetry requirement levels owned elsewhere (§4.2).

**The plain statement the brief asks for.** The routing half has no rules and therefore fails
section 2 by construction: a page pointer has no failure behaviour, no security property, no
concurrency semantics, no complexity budget and no test. It cannot be checked, and it goes stale
silently — `docs-routing.md:5` even admits its own decay model: *"All links below are official
`signoz.io/docs` pages that were useful and reachable when this skill was built."* No date, no
re-derivation command. That sentence is the skill's own confession that the largest third of it is
unverifiable by design.

**What it would have to become.** The link half must shrink to one file that states *how to find the
current page*, not *which page existed once*: the `site:` patterns (already at `docs-routing.md:40`),
the `Accept: text/markdown` trick (already at `docs-routing.md:48`), the three canonical per-signal
schema pages that have survived every rename, and a link-checker script (§6, §7-S1) that resolves
every remaining URL and exits 1 on any non-200. Everything else in `docs-routing.md`,
`instrumentation-routing.md` and `log-collection-routing.md` is a mirror of a navigation menu that
the vendor rearranges without notice, and mirroring a menu is not a rule.

The rules half must grow one thing it does not have: **the reason behind each non-negotiable
pattern**, which is the table's `ORDER BY` (§5.4). `AGENTS.md:72` — *"a rule with no reason attached
gets rationalised away the first time an agent meets a case you did not anticipate."* The skill
currently says "Always pair the time filter with the bucket filter" and gives the reason as "SigNoz
stores 30-minute buckets" (`clickhouse-traces-reference.md:48`), which explains the `1800` but not
the "always". The real reason is that `ts_bucket_start` is the **first column of the primary key** —
verified at source in §5.4 — so a query without it reads every part in the partition.

---

## 3. The ten-criteria verdict table

Legend: **S** satisfied, **F** fail, **D** delegated (only counts when the skill *names* the owner
at a call site — `LANE-BRIEF.md:50`).

| # | Criterion | Verdict | Evidence | What a fix must add |
|---|---|---|---|---|
| 1 | Correctness and testability | **F** | Zero scripts in the tree (`ls -R` §1). `validation-checklists.md:1–69` is eight prose checks with no evaluator. `clickhouse-metrics-reference.md:298–308` is a nine-item "Query repair checklist" that no tool runs. The only self-verification anywhere is `SKILL.md:66`, a manual curl-and-look ("verify with a direct request that has no inbound `traceparent`"). | A `check-signoz-schema.py` that executes the reference's own assertions against a live `DESCRIBE TABLE` or a captured fixture, and a `check-signoz-sql.py` that parses each shipped example and asserts the invariants the reference declares. §7-S2, §7-S3. |
| 2 | Failure behaviour | **F** | Nothing in the skill says what an agent does when ClickHouse is unreachable, when a query trips `max_execution_time`, when `DESCRIBE TABLE` is refused, or when the docs and the live schema disagree. `clickhouse-metrics-reference.md:310–318` is the closest and it only refuses to *finalize*; it does not say what to return instead. `SKILL.md:47` says "inspect current docs or live `SHOW TABLES`/`DESCRIBE TABLE`" with no branch for "the reader has no ClickHouse credentials", which is the ordinary case for a dashboard author. | A degraded-mode rule: when live schema is unreachable, emit the query with an explicit `-- UNVERIFIED SCHEMA: <table>` marker and a named verification command, and never silently drop to the reference's assumption. Plus the SigNoz-side timeout facts (query-service default read timeout, ClickHouse `max_execution_time`) with the command that reads them. |
| 3 | Security | **F** | The rules exist but are all preference verbs. `SKILL.md:56` "Never include credentials…" is the only hard one. `validation-checklists.md:33` "No secrets, credentials, raw payloads, emails…" has no scope and no enforcement. Nothing addresses the actual trust boundary: **who may run these queries**. The dependency-graph endpoint is `ViewAccess` (§5.6), a viewer key reads every service topology; the skill never mentions SigNoz RBAC, Service Accounts, or that a ClickHouse panel query runs with the *dashboard's* credentials, not the viewer's. Multi-tenant isolation is absent — none of the 11 example queries filters by tenant. | A trust-boundary section: which SigNoz role each surface requires, that a saved ClickHouse panel executes with backend credentials for every viewer of that dashboard (an authorization-bypass class), and a mandatory tenant predicate in every example where the fleet is multi-tenant. Route the doctrine to `/alaa-security-review`. |
| 4 | Observability | **D**, partially | Correctly hands the *design* question off: `SKILL.md:27` names `$alaa-observability-soc` for "cardinality policy, exemplar architecture… alert severity policy". But the delegation is incomplete — the skill then restates SOC's own rules in weaker words (§4.2), so it is delegated on paper and duplicated in fact. | Delete `observability-guardrails.md`'s cardinality/privacy/correlation sections and replace each with a one-line pointer naming the SOC reference file. Keep only the missing-spans reasoning, which is genuinely SigNoz-specific. |
| 5 | Concurrency and load | **F** | The skill writes queries against a table whose read path is shared with every other dashboard in the fleet and says nothing about it. No `max_execution_time`, no `max_result_rows`, no `max_memory_usage`, no concurrent-query budget, no statement that a 30-day panel over `distributed_samples_v4` scans raw samples when `samples_v4_agg_5m` and `samples_v4_agg_30m` exist (§5.3). `validation-checklists.md:38–45` is a six-bullet "Performance check" whose strongest verb is "Prefer". | A read-lane budget: the rollup-selection rule (window > N hours → `samples_v4_agg_5m`; > M days → `agg_30m`), stated `LIMIT` and `max_result_rows` defaults, and the boundary handoff to `/clickhouse-performance-schema-ops` for the read-lane settings it already owns (§4.1). |
| 6 | Clean code, SOLID, patterns | **n/a** | The skill emits SQL, not application code. No finding. | — |
| 7 | Algorithm and data-structure choice | **F** | This is a schema skill; the data structure *is* the subject, and the skill never states one. It names no `ORDER BY`, no `PARTITION BY`, no skipping index, no engine, no TTL — verified by grep, §5.4. `clickhouse-logs-reference.md:60` "Prefer indexed columns when they exist" is the abstract noun `AGENTS.md:69` forbids: an agent cannot determine from this skill which columns are indexed. | State the primary key of each of the three main tables verbatim, with the `ORDER BY` prefix rule that follows from it, and derive the existing "non-negotiable patterns" from it rather than asserting them. §5.4 supplies the exact tuples. |
| 8 | Configurability | **F** | Every environment-varying value is hardcoded into prose: `1800` appears 44 times across the three references as a literal, and `clickhouse-traces-reference.md:48` explains it as "SigNoz stores 30-minute buckets" — true today but a schema constant, not a law. Database names `signoz_logs` / `signoz_traces` / `signoz_metrics` are hardcoded; SigNoz's own reader takes them as options (`options.go`, §5.6) so a self-hosted install can rename them. `instrumentation-routing.md:29` hardcodes `https://ingest.<region>.signoz.cloud:443`. | Name each of these as a deployment-varying value with its default and the command that reads the actual value from the target install (`SELECT name, value FROM system.settings`, the query-service `--config` flags). |
| 9 | Speed of development and debuggability | **S**, weakly | `SKILL.md:29–41` mode table and `00-topic-map.md:28–49` fast-routing list do get an agent to one file in one hop, and the three panel-shape templates are copy-paste ready. This is the skill's real strength. | Preserve it. The Phase 2 rewrite must not trade the templates for prose. |
| 10 | Documentation | **F** | The skill documents *SigNoz*; it does not document *itself*. No statement of what it ships, no version pins with re-derivation commands (D10, `LANE-BRIEF.md:112`), no operational note, no failure description. `source-map.md:27` "Checked baseline for this pack" carries no date and no command. | A `references/90-versions.md` carrying the four pins in §5.1 with the exact commands that re-derive each, plus a one-paragraph "what this skill ships and how it fails" in `SKILL.md`. |

**Counts: 1 satisfied (weakly), 7 failed, 1 delegated (partially), 1 not applicable.**

---

## 4. Defect-class findings (only classes actually found)

### D-1. Stale hardcoded model names — **not found**
`grep -rniE 'gpt|claude|opus|sonnet|haiku|o[34]-|model' .` returns nothing outside the word
"modern" at `docs-routing.md:11`. Clean.

### D-2. Wrong trigger syntax — **FOUND, one-directional**
Three Codex-form call sites, zero Claude Code forms:

- `SKILL.md:27` — ``use `$alaa-observability-soc` ``
- `references/observability-guardrails.md:72` — ``pair with `$alaa-observability-soc` ``
- `references/log-collection-routing.md:58` — ``Pair with `$alaa-observability-soc` ``

`AGENTS.md:55`: *"Give both trigger forms at every cross-skill call site — `/name` and `$name`."*
`grep -rn '/alaa-'` across the skill returns **zero** matches. This is exactly the pattern the brief
warns about at `LANE-BRIEF.md:59–60`. The counterpart skill gets it right in both directions —
`alaa-observability-soc/SKILL.md:52` reads ``/alaa-signoz-clickhouse-docs`
(`$alaa-signoz-clickhouse-docs`)`` — so the asymmetry is this skill's alone.

Additionally, the frontmatter description at `SKILL.md:3` names the companion with **no sigil at
all**: *"Pair with alaa-observability-soc for signal design…"*. A bare name in a description routes
in neither runtime.

### D-3. Duplication between body and references — **FOUND, three instances**

**D-3a. Two routers, already drifted.** `SKILL.md:29–41` is a 10-row mode table; the skill also ships
`references/00-topic-map.md`, whose lines 28–49 are a competing 10-entry fast-routing list. Both
claim to be the entry point (`SKILL.md:2` "If the task is broad, read `references/00-topic-map.md`
first"; the table below it routes directly). They disagree:

| Situation | `SKILL.md:40` says | `00-topic-map.md:46–47` says |
|---|---|---|
| missing spans | `observability-guardrails.md` **+** `clickhouse-traces-reference.md` | start with `observability-guardrails.md`, *then* traces |
| broad docs lookup | `docs-routing.md` **plus a specific routing file** | `docs-routing.md` alone |

And `00-topic-map.md:5–26` is a pure heading mirror of `ls references/`, which `AGENTS.md:51`
names as routing nothing.

**D-3b. The missing-spans workflow is stated three times.** `SKILL.md:58–66` (5 numbered steps),
`references/observability-guardrails.md:39–48` (7 bullets), `references/clickhouse-traces-reference.md:198–239`
(the anti-join plus a Laravel note). All three state the same rule — *do not extract a locally
generated `traceparent` as a parent; root the server span instead* — in three different phrasings.
`AGENTS.md:41`: *"State every instruction exactly once."*

**D-3c. `1800` and the bucket rule.** The literal `$start_timestamp - 1800` appears **44 times**
across the three ClickHouse references (`grep -c` on `$start`/`$end` gives 44 each). The rule behind
it is stated at `clickhouse-logs-reference.md:33`, again at `clickhouse-traces-reference.md:41–48`,
again at `validation-checklists.md:22`, and again in both "final checklist" sections
(`clickhouse-logs-reference.md:245`, `clickhouse-traces-reference.md:270`). Four statements of one
rule. Signal-specific repetition of the *SQL literal* inside examples is fine; four independent
statements of the *rule* is not.

### D-4. Project-specific content in an always-loaded body — **FOUND**
`SKILL.md:58–66` is the missing-spans workflow, and step 4 is Ala-fleet-specific instrumentation
advice — *"preserve inbound `traceparent`; do not generate a fake parent span"*. This is loaded on
every invocation, including the 60%+ of invocations that are docs lookups or metrics SQL. Its
detailed form already lives in `observability-guardrails.md:39–48` and
`clickhouse-traces-reference.md:239`. The body should carry one routing line.

### D-5. Long numbered procedures nobody reads in order — **FOUND**
`clickhouse-metrics-reference.md` is organised as "First decision → Current table family → Important
columns → Non-negotiable patterns 1–5 → Schema discovery → Common query patterns → Query repair
checklist → When to refuse". An agent arriving with a broken p99 query must read ~250 lines to reach
`298–308`. Restructured by failure class it would be: *symptom* (p99 wrong / rate negative / no rows
/ query times out) → *diagnosis* (wrong temporality / counter reset / fingerprint window narrower
than sample window / raw table where a rollup exists) → *smallest retry* → *escalation*. The four
diagnoses are all present in the file; none is reachable by symptom.

### D-6. Description that only says when to use — **PARTIALLY FOUND**
`SKILL.md:3` has a genuine negative ("Pair with alaa-observability-soc for…") and the body has a
`## Do not use for` heading at line 22, which satisfies the validator regex
`^#+\s+.*\b(when not to use|do not use)\b`. But the description's negative is a *pairing*, not an
exclusion: "Pair with X" tells the agent to load both, which is the opposite of not triggering.
Measured: **423 characters**, well inside the 900 target; no angle brackets. Room to add a real
exclusion clause naming `/clickhouse-performance-schema-ops` and `/vector-rust-observability-pipelines`.

### D-7. Fragile tooling — **not found** (no scripts to be fragile)
### D-8. Shipped `__pycache__` — **not found**

### D-9. Section-2 gaps — see §3. Seven fails.

### D-10. Shrink where possible — **applicable**
`docs-routing.md` (7,614 B), `instrumentation-routing.md` (3,437 B) and `log-collection-routing.md`
(3,272 B) together are 14,323 B — 23% of the skill — and are a mirror of a vendor navigation menu.
Collapsing them to one `references/10-docs-navigation.md` of ~3,000 B, keeping the `site:` patterns,
the markdown-fetch trick, the three canonical per-signal schema URLs and the Cloud/self-host endpoint
distinction, recovers ~11,000 B to spend on §7's new content at zero net growth.

### D-11. Companion boundary — **FOUND, three failures.** See §4 below.

---

## 5. Boundary analysis

### 5.1 vs `clickhouse-performance-schema-ops` — neither names the other

**Evidence, both directions.**

- `grep -rni "signoz" clickhouse-performance-schema-ops/` over all 18 files on the device:
  **zero matches.**
- `grep -rn "clickhouse-performance-schema-ops" alaa-signoz-clickhouse-docs/`: **zero matches.**

Two skills, both about ClickHouse, both in the same library, mutually invisible. That is the finding.
It matters because `clickhouse-performance-schema-ops` states rules that *contradict* what this skill
tells an agent to do, and an agent loading either alone will not learn of the other.

`clickhouse-performance-schema-ops/SKILL.md` rule 2:

> *"Put the tenant column first in `ORDER BY` on every tenant-scoped table and filter every query by
> it, because a table or query without it scans every tenant's rows to answer one tenant's question."*

Not one of the eleven example queries in `alaa-signoz-clickhouse-docs` carries a tenant predicate.
Rule 4 of the same skill:

> *"Run `scripts/review_clickhouse_ddl.py` over every `CREATE TABLE` you write or review and paste
> its output into the answer, because a design argument no checker has read is an opinion."*

`alaa-signoz-clickhouse-docs` ships no checker and pastes no output.

**Which one owns what — decided with evidence.**

`clickhouse-performance-schema-ops/SKILL.md` already draws exactly the line this case needs, for a
different neighbour:

> *"Vector source, transform, sink, and buffer internals: `/vector-rust-observability-pipelines`
> (`$vector-rust-observability-pipelines`) — **that skill owns what the pipeline writes, this one
> owns what the table must be.**"*

Apply the same sentence shape. `clickhouse-performance-schema-ops` owns **what a ClickHouse table
must be** — engine, `ORDER BY`, `PARTITION BY`, TTL, projections, materialized views, part counts,
merge backlog, the `readonly=2` read lane, and `max_execution_time` / `max_result_rows` behaviour.
`alaa-signoz-clickhouse-docs` owns **how a SigNoz-owned table is queried for an incident or a
panel** — which of the three signal families answers the question, which surface accepts the SQL,
the resource-CTE and bucket-filter idioms, the panel output shapes.

But note the asymmetry that makes this line unusual and worth stating explicitly: **SigNoz's tables
are not owned by the Ala ingest-pipeline repository at all.** `clickhouse-performance-schema-ops`
opens by declaring two audiences — the ingest-pipeline repository that owns the DDL, and a `chkit`
consumer pinned to `readonly=2`. SigNoz is a *third* audience it does not model: an upstream vendor
owns the DDL, nobody in the fleet may alter it, and the schema changes when SigNoz is upgraded. So
the correct routing sentence is not "ask the ingest pipeline for a rollup"; it is **"the SigNoz
schema is vendor-owned and read-only to this fleet; propose no DDL against `signoz_*`, and take
read-lane settings and scan-cost reasoning from `/clickhouse-performance-schema-ops`."** Both skills
must state this, in these words, because neither states it today.

### 5.2 vs `alaa-observability-soc` and `alaa-services-contract` — trespass on requirement levels

`AGENTS.md:19–20` settles it: names and values belong to `alaa-services-contract`, **requirement
levels, gates and reasons** belong to `alaa-observability-soc`.

**Metric names — clean.** `grep -rn "alaa_"` returns nothing. The skill invents no metric name; it
uses `{{metric_name}}` placeholders throughout. No trespass on the contract's NAME authority. One
borderline case: `clickhouse-metrics-reference.md:217` writes
``JSONExtractString(labels, 'status_code') = 'STATUS_CODE_ERROR'`` inside a comment — a concrete
label name and value in an example. It is inside a `/* … */` block presented as a template, so it
reads as illustrative rather than authoritative, but it is the exact class the contract owns and
should carry a pointer.

**Requirement levels — clear trespass, in four places.**

| Where | Text | Who owns it |
|---|---|---|
| `observability-guardrails.md:34` | *"Do not put `trace_id`, `span_id`, `user_id`, or other unbounded request identifiers into metric labels."* | SOC `references/30-quantitative-budgets.md` |
| `observability-guardrails.md:59` | *"Avoid high-cardinality metric labels such as raw user IDs, emails, UUIDs, full URLs with IDs, or request IDs."* | same |
| `observability-guardrails.md:74` | *"Metric labels must stay bounded."* | same |
| `observability-guardrails.md:15–18` | four "Core OpenTelemetry rules" including *"Use OpenTelemetry semantic conventions where practical"* and *"Preserve W3C trace context across hops when possible."* | SOC `references/20-instrumentation-gates.md` |

The counterpart's own words, read from the device, show how much is lost in the restatement.
`alaa-observability-soc/references/30-quantitative-budgets.md:13–47` gives **hard numbers**:

> *"Series count is the product of the cardinalities of a metric's labels, not their sum. Five
> labels at ten values each produce 100,000 series from a single metric family… That blast radius
> is why these are hard ceilings and not guidance."*

with a table capping *distinct values of one label* at **50**, the templated-route label at **200**,
and labels beyond service and environment at **5**; plus the attack-traffic clause
(`30-quantitative-budgets.md:44`): *"a label that is bounded by a valid client can be unbounded by a
hostile one, and a metrics backend is a denial-of-service target through any label an attacker can
set."* And `20-instrumentation-gates.md:16` and `:21` make W3C propagation and semantic conventions
**mandatory** gates with stated reasons.

`observability-guardrails.md` reduces "hard ceiling of 50" to "Avoid high-cardinality" and "mandatory
gate" to "where practical" / "when possible". That is not delegation; it is a weaker fork that will
be followed instead of the real one, because it is the one loaded. `observability-guardrails.md:4`
admits the provenance itself: *"This file distills the most useful generic guardrails from the merged
observability skill."*

**Verdict:** `observability-guardrails.md` must lose its "Core OpenTelemetry rules", "Correlation
rules", "Cardinality and privacy rules", "Field-quality rules" and "Helpful defaults" sections —
about 2,400 B — each replaced by one pointer naming `/alaa-observability-soc` (`$alaa-observability-soc`)
and the exact reference file. What survives is the missing-spans reasoning (lines 39–48), which is
SigNoz-behaviour-specific and belongs here; and it should be the file's whole subject, renamed
`references/40-missing-spans.md`.

### 5.3 vs `vector-rust-observability-pipelines` — proposed, needs reciprocal agreement

Both skills write ClickHouse observability data. The overlap is real but narrower than it looks once
the artefacts are read.

`vector-rust-observability-pipelines/references/CLICKHOUSE_SINK.md` (1,160 B, read in full) contains
**no table name, no column name, no SQL**. It is a list of eleven sink options
(`endpoint`, `database`, `table`, `auth`, `tls`, `compression`, `batch.max_bytes`, `batch.max_events`,
`batch.timeout_secs`, `buffer.type`, `buffer.when_full`, `acknowledgements.enabled`), a
JSON-vs-`arrow_stream` encoding decision, `date_time_best_effort` for timestamps, and
`skip_unknown_fields` for drift. Its sibling `SKILL.md:186–194` adds the same list again.

So the two skills are **not** competing over schema. They are adjacent on exactly one seam: the
**event shape the sink emits versus the column set the query reads**.

**Proposed boundary — written in the words I would want the other side to adopt verbatim:**

> `vector-rust-observability-pipelines` owns **how bytes reach a ClickHouse table**: source,
> transform, VRL, batching, buffering, acknowledgement, encoding, retry and the sink's own failure
> behaviour. It writes to tables the fleet's ingest pipeline owns and names no `signoz_*` table.
>
> `alaa-signoz-clickhouse-docs` owns **how SigNoz's own vendor-owned `signoz_logs`, `signoz_traces`
> and `signoz_metrics` tables are read** for a dashboard panel, an alert or an incident. It writes
> no pipeline config and proposes no DDL.
>
> **Vector never writes into a `signoz_*` table.** SigNoz's collector owns those tables' write path
> and its schema migrator creates them; a Vector sink pointed at `signoz_logs.logs_v2` bypasses the
> collector's fingerprinting and materialized-column population and produces rows that the SigNoz
> UI cannot filter. When telemetry must pass through Vector on its way to SigNoz, Vector's sink is
> **OTLP to the SigNoz collector**, not ClickHouse. The ClickHouse sink is for the fleet's own
> analytical tables only.

That last paragraph is the substantive claim, and it is the one that needs the other lane's
agreement. It is grounded in the schema facts verified in §5.4 — `resource_fingerprint`,
`ts_bucket_start` and the `attribute_*_*$$*` materialized columns are populated by the SigNoz
collector's exporter, and no Vector sink configuration in `CLICKHOUSE_SINK.md` can produce them —
but I have not read the Vector lane's evidence and I am **not** asserting it settled.
`UPGRADE-CARRYOVER.md` decision D8 is the precedent: *"a boundary asserted from one side only is a
boundary the other side has not agreed to."* Flagging it for reciprocal ratification.

### 5.4 What the skill should own but does not

**The physical layout of the three tables it queries.** Verified at source today (§6.4). The skill
states no `ORDER BY`, no `PARTITION BY`, no TTL, no index — grep confirms: the word "index" appears
only as part of the table name `signoz_index_v3` and in the phrase "prefer indexed columns".

This is the highest-value missing content in the whole skill, because every "non-negotiable pattern"
it already asserts is a *consequence* of the primary key, and stating the key turns four unexplained
commandments into one derivable rule.

**The dependency-graph read path** (§5.6) — the fleet's only pre-aggregated service topology, and
the skill mentions neither the endpoint nor the table.

**The field-discovery path.** The skill's own frontmatter sells "field ambiguity" as a use case
(`SKILL.md:3`), and `query-language-routing.md:56–62` handles it with four soft rules and a doc link.
SigNoz now ships an authoritative answer: the `signoz_metadata` database with
`distributed_field_keys` (columns `signal`, `field_context`, `field_name`, `field_data_type`,
`last_seen`), verified §6.4. That is a query an agent can run to resolve ambiguity in one hop
instead of reading a doc page.

---

## 6. Version and factual currency — checked 2026-07-29

### 6.1 Versions the skill does not state (and must)

The skill pins **nothing**. `source-map.md:27` "Checked baseline for this pack" is five prose bullets
with no version and no date, which is exactly the D10 failure at `LANE-BRIEF.md:112`.

| Fact | Value as of 2026-07-29 | Source | Command that re-derives it |
|---|---|---|---|
| SigNoz application | **v0.135.0** | `SigNoz/charts` `charts/signoz/Chart.yaml` `appVersion: "v0.135.0"`, chart `version: 0.135.0`; corroborated by `values.yaml:768` `tag: v0.135.0` | `curl -s https://raw.githubusercontent.com/SigNoz/charts/main/charts/signoz/Chart.yaml \| grep appVersion` |
| SigNoz changelog latest dated entry | **v0.133.0, 2026-07-15** | https://signoz.io/changelog/ | `WebFetch https://signoz.io/changelog/` |
| `signoz-otel-collector` | **v0.144.6** | `SigNoz/charts` `charts/signoz/values.yaml:1088` | `curl -s https://raw.githubusercontent.com/SigNoz/charts/main/charts/signoz/values.yaml \| grep -A2 'signoz-otel-collector' \| grep 'tag:'` |
| ClickHouse **as SigNoz ships it** | **25.12.5** | `values.yaml:204`, with the vendor's own caveat at `:201`: *"ClickHouse image tag to use. SigNoz is not always tested with the latest version of ClickHouse. Only override if you know what you are doing."* | `curl -s https://raw.githubusercontent.com/SigNoz/charts/main/charts/signoz/values.yaml \| grep -B8 'tag: 25' \| head` |
| ClickHouse **upstream latest** | **26.7, released 2026-07-22** | https://clickhouse.com/docs/whats-new/changelog — heading "ClickHouse release 26.7, 2026-07-22" | `WebFetch https://clickhouse.com/docs/whats-new/changelog` |

**Consequential.** SigNoz pins ClickHouse **25.12.5** while upstream is at **26.7** — seven minor
versions of drift, with the vendor explicitly disclaiming testing on newer builds. An agent that
reaches for a ClickHouse function from current upstream docs may write SQL the target server cannot
parse. The skill states no ClickHouse version at all, so nothing warns it. This belongs in the new
`references/90-versions.md` as a hard rule: *check the target server with `SELECT version()` before
using any ClickHouse feature; the SigNoz-shipped baseline is 25.12.5.*

Note the discrepancy between the chart (v0.135.0) and the public changelog (v0.133.0, 2026-07-15):
the chart is ahead. I report both rather than reconciling them, because I could not reach
`api.github.com/repos/SigNoz/signoz/releases/latest` (HTTP 403, session-scoped GitHub access) to
confirm which is the tagged release. Treat **v0.135.0** as the shipped image and **v0.133.0** as the
last publicly documented release.

### 6.2 Logs schema claims — all VERIFIED

Source A: https://signoz.io/docs/userguide/logs_clickhouse_queries/ (fetched 2026-07-29).
Source B: `signoz-otel-collector` `cmd/signozschemamigrator/schema_migrator/logs_migrations.go`
(`main`, fetched 2026-07-29).
Re-derivation: `curl -s https://raw.githubusercontent.com/SigNoz/signoz-otel-collector/main/cmd/signozschemamigrator/schema_migrator/logs_migrations.go | grep -o 'Table: *"[a-z0-9_]*"' | sort -u`

| Claim (file:line) | Verdict | Note |
|---|---|---|
| database `signoz_logs` (`clickhouse-logs-reference.md:5`) | **VERIFIED** | Both sources. |
| `distributed_logs_v2` (`:9`) | **VERIFIED** | Both. |
| `distributed_logs_v2_resource` (`:24`) | **VERIFIED** | Docs. |
| columns `timestamp` (ns), `ts_bucket_start`, `trace_id`, `span_id`, `severity_text`, `severity_number`, `body`, `attributes_string/number/bool`, `resource`, `scope_name`, `scope_version` (`:14–22`) | **VERIFIED** | Docs list all twelve, plus `observed_timestamp`, `id`, `trace_flags`, `scope_string`, `resource_fingerprint` that the skill omits. |
| `$start_timestamp_nano`, `$end_timestamp_nano`, `$start_timestamp`, `$end_timestamp` (`:36–39`) | **VERIFIED** | Docs verbatim. |
| bucket idiom `ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp` (`:38`) | **VERIFIED** | Docs verbatim. |
| resource CTE on `fingerprint` / `labels` / `seen_at_ts_bucket_start`, joined by `resource_fingerprint GLOBAL IN` (`:46–56`) | **VERIFIED** | Docs. |
| materialized-column form `attribute_string_method`, `attribute_number_response$$time`, `attribute_bool_is_error` (`:62–66`) | **VERIFIED** | Docs give the convention `attribute_<dataType>_<keyname>` plus `_exists`, with `$$` substituting `.`. The skill never states the `_exists` companion column — an omission, not an error. |
| `resource.service.name::String` access syntax (`:81`) | **VERIFIED** | `resource` is a native ClickHouse `JSON` column: `logs_migrations.go:208–210` `{Name: "resource", Type: JSONColumnType{MaxDynamicPaths: 100}}`. |

**Two omissions that are now defects, not gaps.**

1. **`body_v2`.** `signoz-otel-collector/constants/constants.go:4` defines
   `BodyV2Column = "body_v2"`, and `logs_migrations.go:387/397/407` create
   `JSONFullTextIndexExpr(constants.BodyV2Column)` and `JSONPathsIndexExpr(...)` over it. There is
   also `BodyPromotedColumn = "body_promoted"`. The skill's logs reference names only `body`, and
   its rule `clickhouse-logs-reference.md:257` *"Keep `body` scans narrow… "* and
   `validation-checklists.md:45` *"Avoids unbounded `LIKE '%...%'` over large log bodies"* are
   written as if no full-text index existed. It does. An agent following the skill writes a slower
   query than the schema supports.
2. **`MaxDynamicPaths: 100`.** The `resource` JSON column caps distinct dynamic paths at 100
   (`logs_migrations.go:209`, and identically for traces at `traces_migrations.go:919`). Resource
   attributes beyond that threshold land in the shared dynamic store and query differently. This is
   a hard production limit on `resource.<anything>::String` access and the skill states nothing.

### 6.3 Traces schema claims — all VERIFIED, one omission

Source A: https://signoz.io/docs/userguide/writing-clickhouse-traces-query/ (2026-07-29).
Source B: `traces_migrations.go` (`main`, 2026-07-29).

| Claim (file:line) | Verdict | Note |
|---|---|---|
| database `signoz_traces` (`clickhouse-traces-reference.md:5`) | **VERIFIED** | Both. |
| `distributed_signoz_index_v3` (`:9`) | **VERIFIED** | Both. |
| `distributed_traces_v3_resource` (`:29`) | **VERIFIED** | Both. |
| `distributed_signoz_error_index_v2` (`:33`) | **VERIFIED by docs, UNCONFIRMED in migrator** | The docs page lists it. `traces_migrations.go` on `main` does **not** create it — the current migrator creates `signoz_index_v3`, `traces_v3_resource`, `tag_attributes_v2`, `span_attributes_keys`, `trace_summary`, `dependency_graph_minutes*`. It is a legacy v2-era table, present on upgraded installs and possibly absent on fresh ones. The skill presents it unconditionally at `:33` — *"Useful when the user asks for exception-event style data"*. Phase 2 must mark it conditional and give the existence check. |
| columns `ts_bucket_start`, `resource_fingerprint`, `timestamp`, `trace_id`, `span_id`, `name`, `kind`, `kind_string`, `duration_nano`, `status_code`, `status_code_string`, `attributes_*`, `resource`, `http_method`, `http_url`, `http_host`, `db_name`, `db_operation`, `has_error` (`:12–27`) | **VERIFIED** | Docs list all, plus `parent_span_id`, `trace_state`, `response_status_code`, `external_http_url`, `external_http_method`, `is_remote` that the skill omits. `parent_span_id` is used in the anti-join at `:204` but never listed in the column table — a small internal inconsistency. |
| `$start_datetime`, `$end_datetime`, `$start_timestamp`, `$end_timestamp` (`:44–45`, `:268`) | **VERIFIED** | Docs verbatim: *"SigNoz dashboards provide the variables `$start_datetime`, `$end_datetime`, `$start_timestamp`, and `$end_timestamp` automatically."* |
| the `- 1800` / 30-minute bucket rationale (`:48`) | **VERIFIED** | Docs: the offset ensures you *"do not miss spans that started in an earlier bucket but fall within your time range."* |
| materialized columns `attribute_string_http$$route`, `attribute_string_db$$system`, `attribute_string_rpc$$method`, `attribute_string_peer$$service`, `resource_string_service$$name` (`:75–79`) | **VERIFIED** | Docs list all five plus `attribute_string_messaging$$system`, `attribute_string_messaging$$operation`, `attribute_string_rpc$$system`, `attribute_string_rpc$$service`. |

### 6.4 Physical layout — VERIFIED at source, and absent from the skill

From `traces_migrations.go` (`main`, 2026-07-29), the `signoz_index_v3` `MergeTree` settings:

```
PartitionBy: "toDate(timestamp)"
OrderBy:     "(ts_bucket_start, resource_fingerprint, has_error, name, timestamp)"
TTL:         "toDateTime(timestamp) + toIntervalSecond(1296000)"        // 15 days
```

and for `traces_v3_resource`:

```
PartitionBy: "toDate(seen_at_ts_bucket_start)"
OrderBy:     "(labels, fingerprint, seen_at_ts_bucket_start)"
TTL:         "toDateTime(seen_at_ts_bucket_start) + INTERVAL 1296000 SECOND + INTERVAL 1800 SECOND DELETE"
```

Re-derivation:
`curl -s https://raw.githubusercontent.com/SigNoz/signoz-otel-collector/main/cmd/signozschemamigrator/schema_migrator/traces_migrations.go | grep -n 'OrderBy\|PartitionBy\|TTL:'`

Three consequences the skill must state and currently does not:

1. **`ts_bucket_start` is the first primary-key column.** That is the reason the bucket filter is
   non-negotiable, and it is a stronger reason than "SigNoz stores 30-minute buckets".
2. **`resource_fingerprint` is second.** That is why the resource CTE plus `GLOBAL IN` is fast —
   it turns a resource-attribute filter into a primary-key range. It also explains the inverse rule
   the skill states at `:67` ("Do not add the CTE if the query does not filter on resource
   attributes") without a reason.
3. **`has_error` and `name` are third and fourth.** Filtering on `has_error` or `name` is
   index-supported; filtering on `http_method`, `duration_nano` or a map key is not. The skill's
   `:69` *"Prefer indexed or pre-extracted columns"* is unactionable without this; with it, the rule
   becomes a lookup.

Also verified: the resource table's TTL is the index table's TTL **plus 1800 seconds** — the same
1800 that appears in the query idiom. That is a designed safety margin, and it is worth one sentence.

### 6.5 Metrics schema claims — VERIFIED but materially incomplete

Source A: https://signoz.io/docs/userguide/write-a-metrics-clickhouse-query/ (2026-07-29).
Source B: `metrics_migrations.go` (`main`, 2026-07-29).
Re-derivation: same `grep -o 'Table: *"[a-z0-9_]*"' | sort -u` on `metrics_migrations.go`.

| Claim (file:line) | Verdict |
|---|---|
| database `signoz_metrics` (`clickhouse-metrics-reference.md:11`) | **VERIFIED** |
| `distributed_samples_v4`, `distributed_time_series_v4`, `distributed_time_series_v4_6hrs`, `distributed_time_series_v4_1day` (`:13–16`) | **VERIFIED** |
| samples columns `env`, `temporality`, `metric_name`, `fingerprint`, `unix_milli`, `value` (`:24–29`) | **VERIFIED** by docs; migrator adds `flags` (`metrics_migrations.go:719`, `UInt32`, default 0) which the skill omits and which the vendor's own rollup MVs filter on (`WHERE bitAnd(flags, 1) = 0`) |
| time-series columns `env`, `temporality`, `metric_name`, `description`, `unit`, `type`, `is_monotonic`, `fingerprint`, `unix_milli`, `labels` (`:33–42`) | **VERIFIED** by docs; migrator adds `__normalized` |
| `{{.start_timestamp_ms}}` / `{{.end_timestamp_ms}}` (`:56–58`) | **VERIFIED** — docs also document `{{.service_name}}` |
| 1-day alignment `intDiv({{.start_timestamp_ms}}, 86400000) * 86400000` (`:63`) | **VERIFIED** as consistent with the 1-day granularity table; not quoted verbatim by the docs |
| *"The docs warn that schemas can change"* (`:18`) | **VERIFIED** — docs verbatim: *"The schemas are not final. We might change it in the future."* |

**Six tables the live schema has and the skill does not name.** From the migrator:

| Table | Why it matters |
|---|---|
| `signoz_metrics.samples_v4_agg_5m`, `samples_v4_agg_30m` | Pre-aggregated 5-minute and 30-minute rollups with `last`/`min`/`max`/`sum`/`count`, maintained by `samples_v4_agg_5m_mv` and `samples_v4_agg_30m_mv` (`metrics_migrations.go:759`, `:782`, and `FROM signoz_metrics.samples_v4_agg_5m` at `:794`). **The skill's every metrics example scans raw `distributed_samples_v4`.** For a 7- or 30-day panel that is the scan-amplification defect criterion 5 is about. |
| `distributed_exp_hist` | The exponential-histogram table (`metrics_migrations.go`, `Table: "exp_hist"` / `"distributed_exp_hist"`). The skill lists `ExponentialHistogram` as a metric `type` at `:38` and then refuses to write SQL for it at `:315` — *"the query depends on histogram/exponential-histogram internals not confirmed by docs or live schema"*. The table is confirmed at source. The refusal is now unnecessary caution rather than honest uncertainty. |
| `distributed_metadata`, `distributed_updated_metadata` | Metric metadata (`description`, `unit`, `temporality`, `type`, `resource_attrs`, `first_reported_unix_milli`, `last_reported_unix_milli`). The skill's rule 4 at `:74–82` — *"Do not infer metric type blindly… confirm metric name, temporality, type, label keys, units"* — is a rule with no method. `distributed_metadata` **is** the method. |
| `distributed_time_series_v4_1week` | A fourth granularity the skill omits, relevant to long-window fingerprint lookups. |
| `distributed_samples_v4_reduced_*` (six tables: `last_60s/5m/30m`, `sum_60s/5m/30m`) and `distributed_time_series_v4_reduced*` | The metric-reduction family, driven by `metric_reduction_rules`. A reduced series has a `reduced_fingerprint`, not a `fingerprint`; a query joining on the wrong one silently returns nothing. |
| `signoz_meter.samples`, `samples_agg_1d` (`meter_migrations.go`) | An entire additional database and signal family (metering) that did not exist when this skill was written. Out of scope, but it is the clearest single proof that the "checked baseline" at `source-map.md:27` has decayed. |

**Verdict on §6.5:** every claim the skill makes is **VERIFIED**; the file is **STALE by omission**
in six places, one of which (the `agg_5m`/`agg_30m` rollups) is a production performance defect and
one of which (`distributed_metadata`) leaves an existing rule unexecutable.

### 6.6 The dependency-graph API — VERIFIED, with two corrections

Checked against `SigNoz/signoz` `main`, 2026-07-29.

| Memory claim | Verdict | Evidence |
|---|---|---|
| `POST /api/v1/dependency_graph` | **VERIFIED** | `pkg/query-service/app/http_handler.go:527`: `router.HandleFunc("/api/v1/dependency_graph", am.ViewAccess(aH.dependencyGraph)).Methods(http.MethodPost)` |
| registered at `http_handler.go:531` | **STALE — now line 527** | Same file, 4,695 lines. The line moved; the route did not. This is why a line number is a bad pin and the route string is a good one. |
| body `{"start","end","tags"}` | **VERIFIED** | Handler calls `parseGetServicesRequest`; `pkg/query-service/model/queryParams.go:83` `type GetServicesParams struct { StartTime string \`json:"start"\`; EndTime string \`json:"end"\`; Period int; Start *time.Time; End *time.Time; Tags []TagQueryParam \`json:"tags"\` }` |
| returns `{Parent, Child, CallCount, CallRate, ErrorRate, P50..P99}` | **VERIFIED**, JSON keys are lowerCamel | `pkg/query-service/model/response.go:328–339` `ServiceMapDependencyResponseItem` with tags `parent`, `child`, `callCount`, `callRate`, `errorRate`, `p99`, `p95`, `p90`, `p75`, `p50` |
| from pre-aggregated `dependency_graph_minutes` | **STALE — the read path is `distributed_dependency_graph_minutes_v2`** | `pkg/query-service/app/clickhouseReader/options.go:27` `defaultDependencyGraphTable string = "distributed_dependency_graph_minutes_v2"`. `traces_migrations.go:533` drops `distributed_dependency_graph_minutes` (v1) with the comment `// remove dependency_graph_minutes later`. Querying the v1 name returns stale or empty data on a current install. |
| a viewer-level Service Account key suffices | **VERIFIED** | `am.ViewAccess(...)` at `http_handler.go:527` |
| lower bound only — shows only traffic that actually ran | **VERIFIED, and now explainable** | `traces_migrations.go:490–506`, `dependency_graph_minutes_service_calls_mv_v2`: a self-join `FROM signoz_index_v3 AS A, signoz_index_v3 AS B WHERE (A.resource_string_service$$name != B.resource_string_service$$name) AND (A.span_id = B.parent_span_id)`. An edge exists only when **both** spans were collected and the child's `parent_span_id` matches. Any sampled-away, dropped or never-exported span erases the edge — the same failure this skill's own missing-spans workflow diagnoses. |
| DB nodes collapse per `db.system` (issue #178) | **VERIFIED at source** | `traces_migrations.go:444–449`, `dependency_graph_minutes_db_calls_mv_v2`: `resource_string_service$$name AS src, attribute_string_db$$system AS dest`. Every PostgreSQL instance in the fleet collapses to one node named by `db.system`. Also `WHERE (dest != '') AND (kind != 2)` — SERVER spans excluded, so only client-side spans contribute. |
| async/queue edges unverified | **RESOLVED — they exist, and their limitation is precise** | `traces_migrations.go:465–470`, `dependency_graph_minutes_messaging_calls_mv_v2`: `resource_string_service$$name AS src, attribute_string_messaging$$system AS dest`. Producer→broker edges **are** recorded, collapsed per messaging system (every RabbitMQ vhost and queue becomes one node `rabbitmq`). There is **no broker→consumer edge**, because the service-calls MV requires a direct `A.span_id = B.parent_span_id` parent link and a consumer that starts a new root span with a span *link* rather than a parent produces no such row. |

Re-derivation commands:

```
curl -s https://raw.githubusercontent.com/SigNoz/signoz/main/pkg/query-service/app/http_handler.go \
  | grep -n 'dependency_graph'
curl -s https://raw.githubusercontent.com/SigNoz/signoz/main/pkg/query-service/app/clickhouseReader/options.go \
  | grep -n 'defaultDependencyGraphTable'
curl -s https://raw.githubusercontent.com/SigNoz/signoz/main/pkg/query-service/model/response.go \
  | grep -n -A12 'ServiceMapDependencyResponseItem'
curl -s https://raw.githubusercontent.com/SigNoz/signoz-otel-collector/main/cmd/signozschemamigrator/schema_migrator/traces_migrations.go \
  | grep -n -A24 'dependency_graph_minutes_.*_mv_v2'
```

**Should the skill carry this, and where?** Yes, in a new `references/50-service-topology.md`,
for three reasons, each grounded above.

1. It is the **only pre-aggregated service topology in the fleet**, and the skill's stated job is
   "writing/repairing SigNoz ClickHouse SQL" for exactly this kind of question. An agent asked "what
   calls the payments service?" currently has no path except a hand-written self-join over
   `distributed_signoz_index_v3` — the expensive form of the query the vendor already materialised.
2. Its limitations are **the same failure this skill already diagnoses**. `SKILL.md:58–66` is a
   missing-spans workflow. A missing span is precisely what erases a dependency-graph edge. The two
   belong in one file with one causal explanation, not in two places with none.
3. It is an **undocumented endpoint**, which is the class of fact a skill exists to carry. It appears
   in no SigNoz doc page; it exists only in source. Written down with its re-derivation command it
   becomes durable; left in project memory it is available to one session.

The file must state the **lower-bound property as a constraint, not a caveat**: *"the dependency
graph is a lower bound on the true call graph. Never conclude from a missing edge that a call does
not happen; conclude only that no trace recording it was collected in the window."* That sentence
survives the wording test; "it is a lower bound" does not.

### 6.7 Surface claims — one CONTRADICTED upstream

The skill asserts throughout that ClickHouse SQL serves **both** dashboards and alerts:

- `SKILL.md:45` — *"ClickHouse SQL is for SigNoz Dashboards and ClickHouse-backed alerts"*
- `query-language-routing.md:9` — *"use ClickHouse alert queries only when the alert type/surface explicitly supports them"*
- `query-language-routing.md:66` and `validation-checklists.md:60` — both offer `Alert ClickHouse` as a named surface
- `clickhouse-logs-reference.md:253`, `clickhouse-traces-reference.md:278` — *"Dashboard/Alert ClickHouse SQL"*

Upstream contradicts itself today. https://signoz.io/docs/operate/clickhouse/clickhouse-queries/
(fetched 2026-07-29) states, verbatim:

> *"ClickHouse queries are only supported in **Dashboards**."*

while its own opening paragraph on the same page says:

> *"You can write ClickHouse SQL queries directly to build custom dashboard panels and alerts when
> the visual Query Builder does not cover your use case."*

and https://signoz.io/docs/alerts-management/log-based-alerts/ (fetched 2026-07-29) states:

> *"You can define your log query using **Query Builder** or **ClickHouse queries**."*

**Verdict: UNVERIFIABLE from documentation — the vendor's docs disagree with themselves.** The skill
currently resolves the ambiguity silently in favour of "alerts work", which is a coin-flip presented
as fact. Phase 2 must carry the contradiction explicitly, both URLs, and a live check the agent runs
against the target install (open the alert-rule editor and observe whether a ClickHouse Query tab is
offered) before promising an alert path. This is the single most user-visible correctness risk in
the skill: an agent that hands over ClickHouse alert SQL for a surface that will not accept it has
produced work that cannot ship.

### 6.8 URL currency — partially checked

36 distinct URLs are asserted across the skill. Bulk verification by `curl` was not possible: the
agent proxy returns `000` for `signoz.io` (all 33 SigNoz/OTel URLs) — this is a proxy restriction,
**not** evidence the pages are gone. Five were verified individually through `WebFetch`:

| URL | Verdict |
|---|---|
| `https://signoz.io/docs/userguide/logs_clickhouse_queries/` | **VERIFIED** (content quoted §6.2) |
| `https://signoz.io/docs/userguide/writing-clickhouse-traces-query/` | **VERIFIED** (§6.3) |
| `https://signoz.io/docs/userguide/write-a-metrics-clickhouse-query/` | **VERIFIED** (§6.5) |
| `https://signoz.io/docs/operate/clickhouse/clickhouse-queries/` | **VERIFIED** — exists, title *"ClickHouse Queries for Dashboards and Alerts"* |
| `https://signoz.io/docs/userguide/traces/#missing-spans` | **VERIFIED** — page exists, heading *"Missing Spans"* present. Content confirms the skill's causes and adds one it omits: *"tail sampling, spans dropped in transit, and services that never export."* |
| `https://code.claude.com/docs/en/skills` | **VERIFIED** — HTTP 200 |
| remaining 29 | **UNVERIFIABLE in this environment** — proxy blocks direct fetch; individual `WebFetch` per URL was not run for all of them within this lane's budget |

This is precisely why the skill needs a link checker (§7-S1): the question "do these 36 URLs still
resolve?" must be answerable by a command, not by an analyst's afternoon.

---

## 7. Executable-check inventory

**The skill ships zero scripts.** `find . -type f` returns 13 files: one `SKILL.md`, one
`agents/openai.yaml`, eleven `references/*.md`. No `scripts/`, no `assets/`, nothing executable.
Nothing to run, nothing to report verbatim, no exit-code contract to assess.

Under `LANE-BRIEF.md:115` — *"A skill whose rules have no tool that reports a violation is shipping
preferences, not rules"* — every rule in this skill is currently a preference. The three checkers
below are what would make them rules. Each honours **0 clean, 1 findings, 2 could not run**, each
takes its target as an argument (no `Path(__file__).parents[N]`, `AGENTS.md:39`), and each runs on
Windows PowerShell (pure Python 3, `pathlib`, no shell pipelines, no `os.sep` assumptions).

### S1 — `scripts/check-signoz-links.py`

**Input:** `--skill-dir <path>` (default: the directory containing `scripts/`, resolved via
`pathlib.Path(sys.argv[0]).resolve().parent.parent` only as a *default*, always overridable).

**Asserts:** every `https://` URL appearing in any `*.md` under `--skill-dir` resolves to HTTP 200
after following redirects, and — for `signoz.io/docs/*` URLs — that the final URL after redirects
equals the asserted URL, because a silent redirect to a docs index is how a moved page hides.

**Flags:** `--skill-dir PATH`, `--timeout SECONDS` (default 20), `--concurrency N` (default 4),
`--allow-redirect` (downgrade final-URL mismatch from finding to note), `--json`, `--self-test`,
`--help`.

**Exit codes:** `0` every URL 200 and no unexpected redirect. `1` one or more URLs non-200 or
redirected to a different path — prints `file:line  URL  →  status/final-URL` per finding.
`2` no network, DNS failure, or `HTTPS_PROXY` unreachable — i.e. *cannot distinguish a dead link
from a dead network*, which must never be reported as clean. Honours `HTTPS_PROXY`/`NO_PROXY`.

**Self-test:** a fixture directory with one known-200 URL, one known-404, and one
unreachable host; asserts the harness reports 1, and asserts that with the network disabled it
reports **2, recorded as BLOCKED not FAIL** (`LANE-BRIEF.md:110`).

### S2 — `scripts/check-signoz-schema.py`

**Input:** either `--describe-dir <path>` holding captured `DESCRIBE TABLE` output (one
`<db>.<table>.tsv` per table, so the checker runs with no ClickHouse access), or
`--dsn <clickhouse-dsn>` to query live. Exactly one required.

**Asserts,** for each of the three signal families, that every table and column name the references
claim exists in the target:

- `signoz_logs.distributed_logs_v2` has `timestamp`, `ts_bucket_start`, `resource_fingerprint`,
  `trace_id`, `span_id`, `severity_text`, `severity_number`, `body`, `attributes_string`,
  `attributes_number`, `attributes_bool`, `resource`, `scope_name`, `scope_version`
- `signoz_logs.distributed_logs_v2_resource` has `fingerprint`, `labels`, `seen_at_ts_bucket_start`
- `signoz_traces.distributed_signoz_index_v3` has the nineteen columns at
  `clickhouse-traces-reference.md:12–27` **plus `parent_span_id`**, which the anti-join uses and the
  column table omits
- `signoz_traces.distributed_traces_v3_resource` has `fingerprint`, `labels`, `seen_at_ts_bucket_start`
- `signoz_metrics.distributed_samples_v4` has `env`, `temporality`, `metric_name`, `fingerprint`,
  `unix_milli`, `value`, `flags`
- each of `distributed_time_series_v4{,_6hrs,_1day,_1week}` has the ten columns at `:33–42`
- **presence probes, reported as notes not findings**: `signoz_metrics.samples_v4_agg_5m`,
  `samples_v4_agg_30m`, `distributed_exp_hist`, `distributed_metadata`,
  `signoz_metadata.distributed_field_keys`, `signoz_traces.distributed_dependency_graph_minutes_v2`,
  `signoz_traces.distributed_signoz_error_index_v2`
- when `--dsn` is used and `system.tables` is readable, that `signoz_index_v3`'s sorting key begins
  `ts_bucket_start, resource_fingerprint` — the fact the whole reference's rule set rests on

**Flags:** `--describe-dir PATH`, `--dsn URL`, `--signal {logs,traces,metrics,all}` (default `all`),
`--json`, `--self-test`, `--help`.

**Exit codes:** `0` every asserted name present. `1` any asserted table or column absent, or the
sorting-key prefix differs — this is the *skill is stale* signal and it is the whole point.
`2` neither input supplied, DSN unreachable, credentials refused, or `DESCRIBE` denied.

**Self-test:** two fixture `--describe-dir` trees, one complete (expects 0) and one with
`ts_bucket_start` removed from the traces table (expects 1, with that exact column named); plus a
non-existent `--describe-dir` (expects 2).

### S3 — `scripts/check-signoz-sql.py`

**Input:** `--sql FILE` (repeatable), or `--skill-dir PATH` to extract and check every ```sql block
in the references — so the skill's own examples are the first corpus, and the checker regression-tests
the skill against itself.

**Asserts,** per statement, after determining the signal family from the `FROM` clause:

1. a bounded time predicate is present, using the family's correct variables — `$start_timestamp_nano`/
   `$end_timestamp_nano` for logs, `$start_datetime`/`$end_datetime` for traces,
   `{{.start_timestamp_ms}}`/`{{.end_timestamp_ms}}` for metrics
2. for logs and traces, a `ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp`
   predicate exists on the main table
3. no statement mixes two `signoz_*` databases without an explicit `JOIN … ON`
4. any subquery over `*_resource` is joined with `GLOBAL IN`, never plain `IN`
5. a resource CTE is present **iff** the query filters a resource attribute — both directions, since
   the reference states both (`clickhouse-traces-reference.md:50`, `:67`)
6. a metrics query whose time window exceeds `--rollup-threshold-hours` (default 24) that reads
   `distributed_samples_v4` and not an `agg_5m`/`agg_30m` rollup — **finding**, per §6.5
7. no `GROUP BY` on a denylisted high-cardinality expression: `trace_id`, `span_id`, `user_id`,
   `request_id`, raw `http_url`, `body`, or any `attributes_string['…']` key matching
   `--cardinality-denylist` (default drawn from `/alaa-observability-soc`'s list, not restated here)
8. no `INSERT`, `ALTER`, `DROP`, `TRUNCATE`, `OPTIMIZE`, `CREATE`, `SYSTEM`, or `KILL` — the skill's
   *"Never include… destructive SQL"* rule (`SKILL.md:56`) made enforceable
9. every timeseries-shaped query returns aliases `ts` and `value`; every value-widget query returns
   exactly one column aliased `value`; every table-shaped query carries a `LIMIT`
10. no bare credential-looking literal (`password=`, `Bearer `, `AKIA`, a JWT-shaped token)

**Flags:** `--sql FILE`, `--skill-dir PATH`, `--panel {timeseries,value,table,auto}` (default `auto`,
inferred from aliases), `--rollup-threshold-hours N`, `--cardinality-denylist FILE`, `--json`,
`--self-test`, `--help`.

**Exit codes:** `0` all statements pass. `1` any assertion fails — prints `file:line  rule-id
message`. `2` no input, unparseable SQL, or a missing denylist file.

**Self-test:** an inline corpus of eight statements, one violating each of rules 1, 2, 4, 6, 7, 8, 9,
plus one clean statement; asserts the exact rule-ids fired and that the clean one did not.

**Expected first run:** rule 6 will fire on `clickhouse-metrics-reference.md`'s counter-rate and
histogram-p99 examples (both read raw `distributed_samples_v4` with no rollup path), and rule 9 will
fire on the traces table-panel example at `clickhouse-traces-reference.md:154–172`, which returns
`http_method` and `avg_duration_nano` and carries **no `LIMIT`** despite the skill's own rule at
`SKILL.md:54` requiring "table: labeled columns and bounded `LIMIT`". That is a real defect the skill
states and violates in its own example — found by reading, and it is exactly what S3 would catch on
every future edit.

---

## 8. The Phase 2 work order

Current total: **63,135 B**. Target: **≤ 63,000 B for the prose**, plus scripts, which are the
genuinely new capability that earns growth (`AGENTS.md:86`, `LANE-BRIEF.md:95`). Name the capability
in the commit: **three executable checkers where the skill previously shipped none, and a verified
service-topology read path that did not exist in the skill before.**

### Files retired to `_to_delete/20260729-batch8/`

| File | Bytes | Reason | Content disposition |
|---|---:|---|---|
| `references/docs-routing.md` | 7,614 | Vendor navigation mirror; self-admittedly undated (`:5`) | `:29–34` page-selection rules, `:36–44` `site:` patterns, `:46–50` markdown-fetch note → new `10-docs-navigation.md`. The 18-row URL table is dropped except the four canonical schema URLs. |
| `references/instrumentation-routing.md` | 3,437 | Same | `:25–32` Cloud vs self-host endpoint distinction and `:45–54` "when to prefer the Collector" → `10-docs-navigation.md`. Rest dropped; the language list is a mirror of `signoz.io/docs/instrumentation/`. |
| `references/log-collection-routing.md` | 3,272 | Same | `:42–48` routing rules and `:56–58` safety note → `10-docs-navigation.md`, with the safety note's requirement level replaced by a pointer to `/alaa-observability-soc`. |
| `references/observability-guardrails.md` | 3,974 | Trespasses on SOC's requirement levels (§5.2) | `:39–48` missing-spans reasoning → new `40-missing-spans.md`. Everything else replaced by pointers; nothing is lost, because SOC states each rule more precisely. |
| `references/00-topic-map.md` | 2,307 | Router count falls to 8 after consolidation, crossing below the `AGENTS.md:49` threshold, which *moves* the router into the body | Every row of `:28–49` must survive into the `SKILL.md` mode table with an observable condition each. Verify none is dropped — `AGENTS.md:53` is explicit that crossing the threshold never drops routing content. |

Retired subtotal: **20,604 B**.

### Files rewritten

**`SKILL.md`** — target ~5,600 B, no growth.
- Description: keep the 423-char text's first two sentences; replace *"Pair with alaa-observability-soc…"* with a real negative naming three skills in **both** trigger forms — SOC for requirement levels, `/clickhouse-performance-schema-ops` for table shape and read-lane settings, `/vector-rust-observability-pipelines` for pipeline config. Stay ≤900 chars, no angle brackets.
- Fix D-2: every cross-skill mention becomes `/name` (`$name`).
- Absorb the surviving `00-topic-map.md` rows into the single mode table; delete the pointer at `:2`. One router (`AGENTS.md:49`).
- Reduce `:58–66` missing-spans workflow to one routing line pointing at `40-missing-spans.md` (D-4).
- Add a "Not owned here" section in `clickhouse-performance-schema-ops`'s own sentence shape, carrying the §5.1 and §5.3 boundary statements.
- Add the three checker invocations with their exact commands and exit-code meanings (`AGENTS.md:59`).
- Add the vendor-owned-schema rule: *propose no DDL against `signoz_*`; the schema changes only when SigNoz is upgraded.*

**`references/clickhouse-logs-reference.md`** — ~8,200 B (+660).
- Add the physical-layout block (§6.4 shape) and derive the bucket rule from it, replacing the bare assertion at `:33`.
- Add `body_v2`, `body_promoted`, and the JSON full-text index; rewrite `:257` and `validation-checklists.md:45` to prefer the index over a narrowed `LIKE`.
- Add the `MaxDynamicPaths: 100` limit on `resource`.
- Add `attribute_<type>_<key>_exists` beside the materialized-column table at `:62–66`.
- Merge the orphan `# 2026 production update` section (`:251–260`) into the body; a `#`-level heading mid-file is a structural defect.

**`references/clickhouse-traces-reference.md`** — ~9,600 B (+435).
- Physical-layout block: the `ORDER BY` tuple, and the three consequences in §6.4.
- Add `parent_span_id` to the column list at `:12–27`.
- Mark `distributed_signoz_error_index_v2` conditional with its existence check (§6.3).
- Add a `LIMIT` to the table-panel example at `:154–172`, which violates `SKILL.md:54` today.
- Merge the orphan `# 2026 production update`.

**`references/clickhouse-metrics-reference.md`** — ~11,000 B (+970).
- Add the six omitted table families (§6.5), each with its trigger condition.
- Add the **rollup-selection rule**: window ≤ 24 h → `distributed_samples_v4`; ≤ 30 d → `samples_v4_agg_5m`; beyond → `samples_v4_agg_30m`. Threshold configurable, defaults stated, matching S3 rule 6.
- Replace rule 4's unexecutable *"confirm metric name, temporality, type, units"* (`:74–82`) with the `distributed_metadata` query that answers it.
- Downgrade the exponential-histogram refusal at `:315` from "cannot" to "query `distributed_exp_hist`, and state the uncertainty".
- Add the `flags` column and the vendor's own `bitAnd(flags, 1) = 0` filter.

**`references/query-language-routing.md`** — ~3,900 B (+180).
- Carry the §6.7 contradiction explicitly: both URLs, both quotes, and the live check the agent runs before promising a ClickHouse alert path. Remove every unqualified "Alert ClickHouse" surface claim.

**`references/validation-checklists.md`** — ~2,400 B (−268).
- Every check that S2 or S3 now evaluates becomes a one-line reference to the checker's rule id. What remains is only what a tool cannot judge.

### Files created

| File | ~Bytes | Contents |
|---|---:|---|
| `references/10-docs-navigation.md` | 3,000 | The surviving navigation rules from the three retired routing files: `site:` search patterns, `Accept: text/markdown`, the four canonical per-signal schema URLs, Cloud-vs-self-host endpoint shape, when to prefer the Collector. States that URLs are checked by S1 and gives its invocation. |
| `references/40-missing-spans.md` | 2,000 | The consolidated missing-spans content (D-3b): the three current statements merged into one, plus the fourth cause the vendor documents and the skill omits (*"tail sampling, spans dropped in transit, and services that never export"*, §6.8), plus the anti-join cross-reference, plus the causal link to the dependency graph's lower-bound property. |
| `references/50-service-topology.md` | 2,800 | The §6.6 content: endpoint, method, auth level, request body, response shape, the `distributed_dependency_graph_minutes_v2` table, the three feeding MVs quoted, the `db.system` and `messaging.system` collapse, the absent broker→consumer edge, and the lower-bound rule stated as a constraint. Every fact with its re-derivation command. |
| `references/90-versions.md` | 1,800 | The five pins in §6.1 with their re-derivation commands, the ClickHouse 25.12.5-vs-26.7 drift warning, and the `SELECT version()` rule. |
| `scripts/check-signoz-links.py` | ~7,000 | S1 |
| `scripts/check-signoz-schema.py` | ~11,000 | S2 |
| `scripts/check-signoz-sql.py` | ~14,000 | S3 |

**Prose budget:** 63,135 − 20,604 retired + 13,600 created + ~1,980 net growth in rewritten files
= **≈ 58,100 B**, an 8% reduction. Scripts add ~32,000 B and are the named new capability.

### Reciprocal edits required in other skills

1. **`clickhouse-performance-schema-ops/SKILL.md`** — add to its "Not owned here" section:
   SigNoz's `signoz_logs`/`signoz_traces`/`signoz_metrics` schemas are vendor-owned and read-only to
   this fleet; `/alaa-signoz-clickhouse-docs` (`$alaa-signoz-clickhouse-docs`) owns how they are
   queried; this skill still owns read-lane settings and scan-cost reasoning over them.
2. **`alaa-observability-soc`** — already correct in both directions; no edit needed, but confirm
   after this skill's rewrite that nothing it points at was retired.
3. **`vector-rust-observability-pipelines`** — the §5.3 boundary, pending that lane's agreement.
4. **`skills/sohrab/README.md`** — already listed in `UPGRADE-CARRYOVER.md:216` as omitting this
   skill; Batch 8 owns the fix.

---

## 9. Open questions for the owner

**Q1. Does the fleet's SigNoz install accept ClickHouse SQL in alert rules?**
The vendor's docs contradict themselves (§6.7). This is not a research question; it is a
thirty-second check in the fleet's own SigNoz UI.
*Recommendation:* the owner (or anyone with alert-editor access) opens a new alert rule and reports
whether a ClickHouse Query tab is offered, for which signals. Phase 2 writes the answer as a fact
with the install's version beside it.
*Trade-off:* leaving it ambiguous costs the agent a wrong deliverable each time it hands over alert
SQL for a surface that rejects it; resolving it costs one minute.

**Q2. Should `references/50-service-topology.md` ship at all, given the endpoint is undocumented and
could be removed without notice?**
*Recommendation:* ship it, with the re-derivation commands in §6.6 and an explicit statement that the
endpoint is not in the public docs.
*Reason:* the fleet already depends on it. An undocumented dependency that lives only in project
memory is available to one session; written down with the command that re-checks it, it survives.
*Trade-off:* Option A (ship it) risks the skill asserting an endpoint SigNoz later removes — mitigated
because S1/S2 would report the absence. Option B (omit it) keeps the skill purely
documentation-grounded but leaves the agent hand-writing an expensive self-join for a question the
vendor already materialised.

**Q3. Is the router convention mandatory fleet-wide?**
This skill sits exactly on the boundary: 11 references today (topic map correct), 8 after
consolidation (topic map must move into the body). `UPGRADE-CARRYOVER.md` records the convention as
undecided across the tree — 28 of 68 skills carry a topic map, 40 do not.
*Recommendation:* mandatory, threshold at 9, as `AGENTS.md:49` already states.
*Reason:* `AGENTS.md:49`'s own argument — the topic map is a house filename no runtime loads on its
own, so a body router reaches the agent with no second read.
*Trade-off:* mandating it costs a one-time pass over 40 skills; leaving it optional means every future
skill re-litigates it, and this skill has already shipped two routers that drifted (D-3a).

**Q4. Should the docs-routing content be retired as aggressively as §8 proposes?**
Roughly 14 KB of curated SigNoz URLs would go, replaced by ~3 KB of search patterns.
*Recommendation:* yes.
*Reason:* the file dates itself only as "when this skill was built" (`docs-routing.md:5`), 29 of its
URLs could not be verified in this environment, and SigNoz reorganises its docs tree between minor
releases — three of the paths it asserts
(`/docs/opentelemetry-collection-agents/...`) are already from a naming scheme that replaced an
earlier one.
*Trade-off:* Option A (retire) makes the skill smaller, truer and checkable, at the cost of the agent
running one search instead of reading one table. Option B (keep and add S1) preserves the shortcut
but commits the fleet to re-verifying 36 URLs on every SigNoz release, forever, for a gain a
`site:signoz.io/docs` query already delivers.

**Q5. Multi-tenancy.** Not one of the eleven example queries filters by tenant, while
`clickhouse-performance-schema-ops` makes the tenant predicate a rule that "holds on every task"
(§5.1).
*Recommendation:* the owner states whether SigNoz in this fleet is single-tenant. If it is, say so in
the skill and the question closes. If it is not, every example needs a tenant predicate and S3 needs
a rule 11 asserting it.
*Reason:* this is the one gap where the two ClickHouse skills give an agent contradictory
instructions, and an agent cannot resolve it from the files.


---

# Appendix B — `vector-rust-observability-pipelines`

# L2 — `vector-rust-observability-pipelines`

Lane: `vector-rust-observability-pipelines`. Phase 1, read-only. Analysed 2026-07-29.
Staged copy: `/home/claude/b8/src/vector-rust-observability-pipelines/` (21 files, 25,769 bytes).
Device original: `D:\Sohrab\Project\skills\skills\sohrab\vector-rust-observability-pipelines\`.
Nothing was written to the device.

**Headline.** This skill is 25,769 bytes — the third smallest of 69 skills in the fleet — and it is
shaped backwards: a 9,487-byte always-loaded body over eleven reference stubs averaging 1,049 bytes,
against a fleet reference median of 6,522. It has the highest body-to-total ratio in the fleet
(0.368). It carries three structural anomalies no other skill has. Its version guardrails state four
facts about Vector 0.53 and **three of them are wrong**, verified against the upstream release notes
today. All three shipped config templates **fail `vector validate`** on a VRL compile error. Its one
executable check exits 127 when Vector is absent. And its subject — buffering, acknowledgements,
backpressure — the three section-2 criteria it must not delegate, is the thinnest part of the pack.

---

## 1. Inventory

Byte sizes from `find -printf '%s'` on the staged copy; contents from reading each file in full.

### Top level

| File | Bytes | What it actually contains |
| --- | ---: | --- |
| `SKILL.md` | 9,487 | 227-line body (230 with frontmatter). Frontmatter, a six-bullet scope list, "Source freshness", five numbered "Core operating principles", "When NOT to use", a "Fast entry" table naming no file paths, three Codex-only companion routes, "Version guardrails (Vector 0.53.0+)", a six-step "Default workflow", "Delivery guarantee rules", "ClickHouse sink rules", a "Multi-agent plan" listing six agent roles, an "Output contract", and an "Included resources" list of 15 paths. Substantially a complete restatement of every reference file. |
| `INSTALL.md` | 429 | Install instructions naming `<repo>/.agents/skills/` and `~/.agents/skills/`. Claims the skill is `allow_implicit_invocation: false`. Both claims are false — see §3.1 and §3.2. |
| `agents/openai.yaml` | 298 | `display_name`, `short_description` (38 chars, inside the validator's 25–64 band), `default_prompt` containing `$vector-rust-observability-pipelines`, and `policy.allow_implicit_invocation: true`. Passes the validator. |

### `references/` — eleven files, 12,258 bytes total

The "new vs body" column is the count of distinct content terms (length > 3, stop-words removed)
present in the file but absent from `SKILL.md`. It measures what a reader gains by taking the hop.

| File | Bytes | Rules it actually states | New vs body | % new |
| --- | ---: | ---: | ---: | ---: |
| `OFFICIAL_LINKS.md` | 2,106 | 16 URLs + 1 freshness-trigger rule + 1 precedence rule. The only reference that is not a stub; it is a link list. | 46 | 43% |
| `HELM_CHART_OPERATIONS.md` | 1,915 | ~18 rules across 7 sections. The most substantive reference. | 80 | 55% |
| `COMMUNITY_NOTES.md` | 1,175 | 6 numbered "sharp edges", all hedged as non-normative. | 42 | 41% |
| `CLICKHOUSE_SINK.md` | 1,160 | A 13-item option checklist + 3 Arrow preconditions + 2 one-line notes. | 47 | 51% |
| `VRL_GUIDE.md` | 1,040 | 5 principles, 7 task names, a 4-step workflow, 3 metric-function names, 3 sharp edges. | 46 | 51% |
| `INTERNAL_MONITORING.md` | 971 | 2 source names, 8 "watch for" nouns, 3 migration claims (2 wrong), 1 startup rule. | 34 | 39% |
| `TOPOLOGY_WORKFLOW.md` | 862 | 6 per-edge contract fields, 3 deployment shapes, 1 fanout caution. | 36 | 47% |
| `BUFFERS_AND_ACKS.md` | 742 | **11 bullets total.** See §5 — this is the critical gap. | 22 | 39% |
| `TROUBLESHOOTING.md` | 739 | 4 symptoms × 4–5 "inspect X" bullets. Every bullet is a noun to look at; none is a diagnosis, a threshold, or a command. | 16 | 31% |
| `VALIDATION_AND_TESTING.md` | 549 | 3 commands + 5 "why it matters" bullets. | 19 | 44% |
| `README.md` | 288 | A bare list of the other ten filenames. **Adds 2 new terms.** | 2 | 14% |

### `prompts/` — two files, 1,639 bytes

| File | Bytes | Contents | New vs body | % new |
| --- | ---: | ---: | ---: | ---: |
| `AGENT_PROMPT.md` | 941 | A mission statement, 5 "hard constraints", 7 required output sections. Duplicates `SKILL.md` "Output contract" (lines 205–212) and the core principles. | 21 | 26% |
| `MULTI_AGENT_PROMPT.md` | 698 | A six-agent fan-out list. Duplicates `SKILL.md` "Multi-agent plan" (lines 196–203) one-for-one. | 10 | 16% |

### `assets/templates/` — four files, 2,129 bytes

| File | Bytes | Contents |
| --- | ---: | --- |
| `vector-clickhouse.yaml` | 927 | `demo_logs` → `remap` → `clickhouse`. Contains a VRL compile error (§3.3) and `${CLICKHOUSE_USER}`/`${CLICKHOUSE_PASSWORD}` interpolation that Vector 0.57.0 disabled by default (§5.2). |
| `vector-tests.yaml` | 429 | One `vector test` case asserting `.level`, `.service`, `.message`. Syntax verified current. References transform `normalize`, which is defined only in `vector-basic.yaml`; nothing in the skill says the two files must be passed together. |
| `common.vrl` | 389 | Four snippets: downcase level, safe JSON parse, routing key, token redaction. Contains the same VRL compile error. |
| `vector-basic.yaml` | 384 | `demo_logs` → `remap` → `console`. Contains the same VRL compile error. |

### `scripts/` — one file, 240 bytes

| File | Bytes | Contents |
| --- | ---: | --- |
| `validate-and-test.sh` | 240 | `set -euo pipefail`; arity check → `exit 1`; `vector validate "$@"`; `vector test "$@"`. No `--help`, no `--self-test`, no exit-code mapping. See §6. |

---

## 2. The inversion, quantified

This is lane instruction 1. The programme's shape is: the body holds only what is always needed,
detail lives one hop away. This skill is the exact inverse, and the numbers are unambiguous.

| Measure | This skill | Fleet (68 others) |
| --- | ---: | ---: |
| `SKILL.md` bytes | 9,487 | — |
| `SKILL.md` body lines | 227 | validator warns above 120 |
| Reference file median bytes | **971** | **6,522** |
| Reference file mean bytes | 1,049 | 7,547 |
| Largest reference | 2,106 | — |
| Fleet reference files smaller than this skill's *largest* | — | **20 of 669** |
| Body ÷ total skill bytes | **0.368 — highest in the fleet** | next highest 0.317 |
| Total skill bytes | 25,769 | 3rd smallest of 69 |

Derivation: `device_list_dir` recursive over `D:\Sohrab\Project\skills\skills\sohrab\` (1,716
entries, not truncated), aggregated by skill directory.

**Read that third row twice.** The median reference file in this skill is 971 bytes; the median
reference file everywhere else in the fleet is 6,522. Only 20 of the fleet's 669 other reference
files are smaller than this skill's *biggest* one. Eleven of the fleet's smallest reference files
are in this one directory.

**What the hop buys.** The last column of §1 measures it directly. `references/README.md` adds two
new terms — taking that hop is a pure loss. `prompts/MULTI_AGENT_PROMPT.md` adds ten.
`TROUBLESHOOTING.md` adds sixteen. No reference exceeds 55% new content; the body has already said
most of what each one says, in fewer words. An agent that reads `SKILL.md` and then opens
`BUFFERS_AND_ACKS.md` learns 22 new terms for 742 bytes of context. That is the inversion: the
references are not one hop away from the body, they are a lossy echo of it.

### 2a. Body content that must move down

| `SKILL.md` lines | Content | Destination |
| --- | --- | --- |
| 61–66 | Core principle 5, "Treat Helm as part of pipeline correctness" — role→workload map, `values.yaml` minimalism, `customConfig` completeness, template escaping, private registry | `HELM_CHART_OPERATIONS.md`, which already says all five |
| 92–108 | "Version guardrails (Vector 0.53.0+)" — 17 lines of one-release migration detail, wrong in three places | a new `references/80-version-and-upgrade-deltas.md`, corrected and extended through 0.57.0 |
| 110–167 | "Default workflow" steps 1–6 — 58 lines of a linear procedure | steps 1–3 to `TOPOLOGY_WORKFLOW.md`, step 4 to `VRL_GUIDE.md`, step 5 to `VALIDATION_AND_TESTING.md`, step 6 to `INTERNAL_MONITORING.md` |
| 169–184 | "Delivery guarantee rules" — acks, buffers, health checks | `BUFFERS_AND_ACKS.md`, which is where a reader would look |
| 186–194 | "ClickHouse sink rules" — 8 bullets | `CLICKHOUSE_SINK.md`, which restates 6 of the 8 |
| 196–203 | "Multi-agent plan" — six agent roles | retire; orchestration is owned by `alaa-cc-orchestrator` / `alaa-codex-orchestrator` (§4) |
| 205–212 | "Output contract" | keep in body — it is genuinely always needed — but state it once, not also in `prompts/AGENT_PROMPT.md` |
| 214–230 | "Included resources" — a flat 15-path list with no trigger conditions | replace with `references/00-topic-map.md` (§3.6) |

That is roughly 150 of 227 body lines. A body of 70–90 lines is achievable and would clear the
validator's 120-line warning.

### 2b. Stub references — fill or retire

| Reference | Disposition | Reason |
| --- | --- | --- |
| `README.md` | **Retire to `_to_delete/`** | Adds 2 new terms. Duplicates `SKILL.md` lines 214–230. Its function is replaced by `00-topic-map.md`. No other skill in the fleet has one (§3.6). |
| `BUFFERS_AND_ACKS.md` | **Fill — highest priority** | 742 bytes for the skill's whole subject. §5 lists what it omits. |
| `TROUBLESHOOTING.md` | **Fill and restructure** | Defect class 5: "inspect X" is not a diagnosis. Needs symptom → diagnosis → smallest retry → escalation, with the metric or command that discriminates each branch. |
| `CLICKHOUSE_SINK.md` | **Fill** | Names 13 options and the *semantics of none of them*. No defaults, no retry options, no confinement rule. |
| `VALIDATION_AND_TESTING.md` | **Fill** | 549 bytes; must gain the 0.57 interpolation flag, the exit-code contract, and the pairing rule for split config/test files. |
| `INTERNAL_MONITORING.md` | **Fill and correct** | Two of three migration claims are wrong (§5.1). Metric names must route to `alaa-services-contract`. |
| `VRL_GUIDE.md` | **Fill** | Must gain the E651 rule that its own templates violate. |
| `TOPOLOGY_WORKFLOW.md` | **Fill** | Absorbs body steps 1–3. |
| `HELM_CHART_OPERATIONS.md` | **Keep, verify, absorb** | Most substantive reference; absorbs body lines 61–66; chart version claims need pinning (§5.5). |
| `COMMUNITY_NOTES.md` | **Merge into `TROUBLESHOOTING.md`** | Its six items are troubleshooting hypotheses. Item 2 ("disk buffer is not magic") is a hedged, non-normative version of a fact upstream states outright (§5.3). |
| `OFFICIAL_LINKS.md` | **Keep, rename `90-source-map.md`** | Aligns with `clickhouse-performance-schema-ops/references/90-source-map.md`. Add the re-derivation command per D10. |

---

## 3. The three structural anomalies, plus what the survey found

Lane instruction 2. Survey method: `device_list_dir` recursive over
`D:\Sohrab\Project\skills\skills\sohrab\`, 1,716 entries, `truncated: false`, aggregated by
directory. Counts are over 69 skill directories.

### 3.1 Top-level `INSTALL.md` — **1 of 69. Drift, and its content is wrong.**

No other skill in the fleet carries one. The only other non-`SKILL.md` top-level Markdown files
anywhere in the tree are `alaa-cc-orchestrator/CHANGELOG.md`, `alaa-codex-orchestrator/CHANGELOG.md`,
`alaa-codex-orchestrator/README-fa.md` and `alaa-laravel-job-rabbitmq/CHANGELOG.md` — changelogs and
a translation, not install docs.

It is not merely anomalous, it is **wrong on both of its claims**:

- `INSTALL.md:5-6` names `<repo>/.agents/skills/` and `~/.agents/skills/`. `UPGRADE-CARRYOVER.md:222`
  says: *"`install-skills.md` is correct and worth treating as authoritative for install paths — it
  already targets `~/.codex/skills`, which is the field-verified location. If any skill's own
  installation docs disagree with it, the skill is wrong, not this file."* I confirmed the
  authoritative path by reading the staged `install-skills.md:268`: *"`list` shows available vendored
  skills plus whether each one is already linked into `~/.codex/skills`"*. `.agents/skills` appears
  nowhere in it.
- `INSTALL.md:12` states the skill is *"explicit-first (`allow_implicit_invocation: false`)"*.
  `agents/openai.yaml:7` states `allow_implicit_invocation: true`. **The two files in this skill
  contradict each other.** An agent reading `INSTALL.md` concludes the skill will not auto-trigger;
  the runtime will auto-trigger it.

**Verdict: drift. Retire to `_to_delete/`.** Install paths are owned by the repository's
`install-skills.md`. The implicit-invocation policy is owned by `agents/openai.yaml`. Neither
belongs in a per-skill file, and this copy of both is false.

### 3.2 `prompts/` with files — **1 of 69. Drift.**

Two directories named `prompts` exist in the tree: this skill's and `alaa-shaka-player/prompts`.
The recursive listing shows `alaa-shaka-player/prompts` with **no child entries** — it is an empty
directory (as are `alaa-shaka-player/checklists`, `assets/config-examples/agents`,
`assets/templates/types` and `assets/templates/services`). So this skill is the **only** skill in the
fleet shipping prompt files.

Both files are also redundant *and* out of jurisdiction:

- `prompts/MULTI_AGENT_PROMPT.md` duplicates `SKILL.md:196-203` role-for-role and adds ten new terms
  (16%). Multi-agent orchestration is owned by `alaa-cc-orchestrator` and `alaa-codex-orchestrator`.
  `clickhouse-performance-schema-ops/SKILL.md:51-53` states the convention in the fleet's own words:
  *"Multi-agent plans: `/alaa-cc-orchestrator` (`$alaa-cc-orchestrator`), or `/alaa-codex-orchestrator`
  (`$alaa-codex-orchestrator`) in Codex."* This skill instead invents its own six-agent taxonomy
  (`topology_architect`, `vrl_engineer`, `delivery_guarantees`, `sink_specialist`,
  `ops_observability`, `troubleshooting_risk_reviewer`) that appears nowhere else in the fleet.
- `prompts/AGENT_PROMPT.md` duplicates `SKILL.md` "Output contract" and the core principles, adding
  21 new terms (26%). Prompt authoring is owned by `alaa-prompting-guide`.

**Verdict: drift on both counts — uniqueness and ownership.** Retire both to `_to_delete/`. Move the
five "hard constraints" from `AGENT_PROMPT.md:14-19` into the body's numbered rules first, since
they are the closest thing in the pack to executable constraints and must not be lost. Note that the
repository validator's `PATH_RE` does not cover `prompts/`, so a broken path under it is never
checked — another reason not to have the directory.

### 3.3 `references/README.md` — **1 of 69. Drift.**

No other skill has one. Twenty-nine of 69 carry `references/00-topic-map.md` instead, which is the
fleet's actual routing file and which the validator *does* check (`validate_sohrab_skill_pack.py`
lines 206–212 verify every path a topic map names exists). `references/README.md` gets no such check.
It adds 2 new terms over the body.

**Verdict: drift. Retire to `_to_delete/`, replaced by `references/00-topic-map.md`.**

### 3.4 Summary of anomaly counts

| Anomaly | Skills carrying it | Verdict |
| --- | ---: | --- |
| top-level `INSTALL.md` | **1** (this one) | drift; content also factually wrong |
| `prompts/` containing files | **1** (this one) | drift; also out of jurisdiction |
| `references/README.md` | **1** (this one) | drift; superseded by `00-topic-map.md` |

All three are unique to this skill across 69 directories. None is a deliberate fleet pattern.

---

## 4. Ten-criteria verdict

Section 2 of the brief. Verdict + evidence + what a fix must add.

| # | Criterion | Verdict | Evidence | A fix must add |
| --- | --- | --- | --- | --- |
| 1 | Correctness and testability | **FAIL** | `SKILL.md:157` says "run `vector test`" and `assets/templates/vector-tests.yaml` ships one happy-path case asserting three field values. No test would fail against a plausible broken implementation. Worse, the three shipped templates **do not compile** (§5.4), so the skill's own artefacts fail the skill's own gate. | A test set covering the failure classes: malformed JSON into `parse_json`, a missing `.level`, a hyphenated field name, a coercion failure. The rule that `vector test` needs the transform-defining config passed alongside the test file. A checker that runs `vector validate` over every shipped template in CI. |
| 2 | Failure behaviour | **FAIL** | This is the skill's own subject and it is answered in slogans. `SKILL.md:180-181` gives `when_full` two values; upstream documents **three** (§5.3). `BUFFERS_AND_ACKS.md` (742 B) states no default, no sizing rule, no behaviour when the disk fills, no retry option name. `SKILL.md:193` says "document auth, TLS, retries, and timeout behavior" — naming no option, which is a reminder, not a rule. `TROUBLESHOOTING.md:16-19` on data loss says "revisit acknowledgement settings". | §5.3 and §5.6 in full: the third `when_full` value, the documented hard-stop on a full disk buffer, the worst-status fanout rule, `request.retry_attempts` / `request.retry_initial_backoff_secs` / `request.retry_max_duration_secs` / `request.concurrency` by name with defaults, and the fail-open/fail-closed discrimination for a telemetry path. |
| 3 | Security | **FAIL** | The word "secret" appears once, in `common.vrl:17` ("Redact simple secret patterns", redacting exactly one field, `.token`). `vector-clickhouse.yaml:26-28` puts credentials in `${VAR}` interpolation that Vector 0.57.0 disabled by default (§5.2) — the config now silently authenticates with the literal string `${CLICKHOUSE_PASSWORD}`. No mention of `SECRET[backend.key]`. No tenant isolation. No mention of the ClickHouse sink SQL-injection fix shipped in 0.57.0 (§5.2). | The secrets-management path (`SECRET[...]` backends, not env interpolation), a redaction rule that names the fields rather than one example, tenant scoping on the sink `table`/`database` templates, and the 0.57 template-confinement boundary as a security control, not a config note. Route trust-boundary review to `alaa-security-review`. |
| 4 | Observability | **PARTIAL FAIL** | `INTERNAL_MONITORING.md` names `internal_logs` and `internal_metrics` and eight nouns to "watch for". It states no metric name to alert on, no threshold, no burn rate. The three metric-migration claims it does state are wrong in two of three (§5.1). It names no owner for metric naming. | Correct metric names; the new `component_cpu_usage_ns_total` and its `measure_cpu_usage: true` opt-in (§5.2); and a call site routing every Ala-side metric/log-field name to `alaa-services-contract` and every requirement level to `alaa-observability-soc`. |
| 5 | Concurrency and load | **FAIL** | Backpressure is named at `SKILL.md:44,133,180` and never specified. No connection-pool guidance, no `request.concurrency` (which upstream defaults to `adaptive`), no load-shedding rule, no throughput budget. `SKILL.md:126` asks the agent to "collect or infer" throughput and gives no way to act on the answer. | `request.concurrency` semantics and when to pin it off `adaptive`; buffer sizing arithmetic tied to throughput and outage duration; `overflow` buffer topology as the load-shedding mechanism; and the explicit statement that `when_full: block` propagates backpressure to the *producing service*, which is a product decision, not a pipeline one. |
| 6 | Clean code, SOLID, patterns | **PARTIAL** | `VRL_GUIDE.md:5-9` ("keep programs short", "give transforms clear names", "normalize and enrich in steps") is proportionate for a config DSL. But these are preference verbs, not constraints — the wording test fails: an agent can follow "keep programs short" exactly and still write an unmaintainable transform. | Turn each into a checkable constraint (one responsibility per `remap`; every transform named for its output, not its input) with the reason attached. |
| 7 | Algorithm / data-structure choice | **DELEGATED — but not named** | No complexity budget appears anywhere. VRL cost is mentioned once, `TROUBLESHOOTING.md:24` "inspect VRL cost". | Delegation only counts when the skill names the owner at a call site. `alaa-algorithms-data-structures` is named nowhere in the skill. Either name it, or state the per-event CPU budget as a pipeline concern this skill does own. |
| 8 | Configurability | **FAIL** | The skill's whole subject is configuration and it states **no default for anything**. Upstream documents `buffer.type: memory`, `buffer.max_events: 500` for sinks, `when_full: block`, `compression: gzip`, `batch.max_bytes: 1e7`, `batch.timeout_secs: 1`, `healthcheck.enabled: true`, `date_time_best_effort: false` (§5.6) — none appear. `vector-clickhouse.yaml:19-20` hardcodes `max_bytes: 10000000`, which *is* the default, without saying so. No boundary validation (disk `max_size` has a documented minimum). | Every option the skill tells an agent to "set deliberately" needs its upstream default, its safe value for a high-SLA path, and its valid range, so "deliberately" becomes a decision instead of an instruction to have an opinion. |
| 9 | Speed and debuggability | **FAIL** | `SKILL.md:74-82` "Fast entry" is the skill's routing surface and it names **no file paths** — it routes to "topology and role guidance" and "the VRL reference and validation flow". Those are abstract nouns; the agent must then read the 15-item flat list at lines 214–230 and guess. The 227-line body must be loaded on every invocation. `TROUBLESHOOTING.md` gives no command that discriminates any branch. | `references/00-topic-map.md` mapping observable situations to exactly one file (the `clickhouse-performance-schema-ops` topic map is the fleet's model); a body under 120 lines; and at least one command per troubleshooting branch. |
| 10 | Documentation | **PARTIAL FAIL** | `SKILL.md:205-212` "Output contract" is genuinely good and is the strongest thing in the skill — six required sections including rollback. But `INSTALL.md` documents the install path wrongly and contradicts `agents/openai.yaml` on invocation policy (§3.1). Documentation that contradicts itself inside one directory is worse than none. | Retire `INSTALL.md`. Keep the output contract, stated once (it is currently also in `prompts/AGENT_PROMPT.md:22-29`). |

**Counts: SATISFIED 0 · PARTIAL 3 (4, 6, 10) · FAIL 6 (1, 2, 3, 5, 8, 9) · DELEGATED 1 (7) — and
the one delegation does not name its owner, so it does not yet count as delegation under the brief's
rule.** Strictly: 0 satisfied, 9 failed or partial, 1 unnamed delegation.

---

## 5. Version and factual currency

Lane instruction 4. Everything below was checked on **2026-07-29**. `vector` is **not installed** in
this container and was **not installed** — runtime re-derivation commands are given for the owner to
run on a host that has it.

**Current release: Vector 0.57.0, released 14 July 2026.**
Source: <https://vector.dev/releases/> and <https://vector.dev/releases/0.57.0/>.
Re-derive: `curl -s https://api.github.com/repos/vectordotdev/vector/releases | jq -r '[.[]|select(.tag_name|test("^v[0-9]+\\.[0-9]+\\.[0-9]+$"))]|.[0]|"\(.tag_name) \(.published_at)"'`
— note plain `/releases/latest` returns `vdev-v0.3.3` (the vdev tool tag) and must not be used.

Release line: 0.53.0 (27 Jan 2026) · 0.54.0 (10 Mar) · 0.55.0 (22 Apr) · 0.56.0 (3 Jun) · 0.57.0 (14 Jul).
`SKILL.md:11` is dated `2026-03-01` and `SKILL.md:92` is titled "Version guardrails (Vector 0.53.0+)".
**The skill is pinned four releases and six months behind.**

### 5.1 The 0.53 migration claims — **STALE, and wrong as originally written**

`SKILL.md:96-99` and `INTERNAL_MONITORING.md:21-25` state the same four claims. Checked verbatim
against <https://vector.dev/releases/0.53.0/>.

| Skill's claim | Location | Upstream | Verdict |
| --- | --- | --- | --- |
| `buffer_max_size` → `buffer_max_size_bytes` | `SKILL.md:97`, `INTERNAL_MONITORING.md:22` | `buffer_max_size_bytes` deprecates **`buffer_max_byte_size`** | **STALE — old name wrong** |
| `buffer_size` → `buffer_size_bytes` | `SKILL.md:98`, `INTERNAL_MONITORING.md:23` | `buffer_size_bytes` deprecates **`buffer_byte_size`** | **STALE — old name wrong** |
| histogram buckets for `buffer_byte_size` changed 10 → 26 | `SKILL.md:99`, `INTERNAL_MONITORING.md:25` | *"Increased the number of buckets in internal histograms…"* — **20 → 26**, and it applies to **all internal histograms**, not to `buffer_byte_size` specifically | **STALE — count wrong and scope wrong** |
| (not stated) | — | `buffer_max_size_events` deprecates `buffer_max_event_size`; `buffer_size_events` deprecates `buffer_events` | **MISSING — two of four renames absent** |
| (not stated) | — | *"…while keeping the old related gauges available for a transition period."* | **MISSING — the fact that makes a safe migration possible** |

Re-derive: `curl -s https://vector.dev/releases/0.53.0/ | grep -iE 'buffer_(max_)?(size|byte|event)' `

**Why this matters more than a typo.** `SKILL.md:100` instructs: *"dashboards/alerts using old metric
names must be migrated."* An agent following lines 97–98 searches its dashboards for
`buffer_max_size` and `buffer_size` — names that never existed — finds nothing, reports the migration
clean, and leaves the two real deprecated names (`buffer_max_byte_size`, `buffer_byte_size`) plus the
two the skill never mentions in place. The check passes and the dashboards break at the end of the
transition period. That is a checker whose "found nothing" is indistinguishable from "clean", written
in prose.

Three VRL metric helpers — `get_vector_metric`, `find_vector_metrics`, `aggregate_vector_metrics`
(`SKILL.md:104`, `VRL_GUIDE.md:28-30`) — **VERIFIED**. Added in 0.53.0 per the release notes.

### 5.2 Vector 0.57.0 breaking changes the skill does not know about — **STALE**

Source: <https://vector.dev/releases/0.57.0/>, confirmed against
<https://vector.dev/docs/reference/cli/>.

1. **Environment-variable interpolation is disabled by default.** *"Environment variable
   interpolation in configuration files is now disabled by default."* Restore with
   `--dangerously-allow-env-var-interpolation` or `VECTOR_DANGEROUSLY_ALLOW_ENV_VAR_INTERPOLATION=true`;
   the old `--disable-env-var-interpolation` flag was removed. Both `vector validate` and `vector test`
   now carry the new flag.
   **Direct impact:** `assets/templates/vector-clickhouse.yaml:26-28` uses `${CLICKHOUSE_USER}` and
   `${CLICKHOUSE_PASSWORD}`. On 0.57.0 these are literal strings. `vector validate` still passes —
   the config is syntactically fine — and the sink then authenticates to ClickHouse with the literal
   text `${CLICKHOUSE_PASSWORD}`. A silent credential failure that the skill's own validation step
   cannot catch.
   Also deprecated in 0.57.0: *"Placeholders (`${VAR}` and `SECRET[backend.key]`) in structural
   positions of a Vector configuration file are deprecated and will be removed in a future release."*
2. **Sink routing template confinement.** *"Sinks that accept `{{ field }}` references in routing
   templates now enforce a confinement boundary: the rendered value must stay within the literal
   prefix declared in the template."* Templates without a literal prefix are **rejected at startup**;
   HTTP/HTTPS URI templates cannot contain `?` or `#` with field references; override with
   `dangerously_allow_unconfined_template_resolution: true`.
   **Direct impact:** `SKILL.md:131` tells the agent to determine "whether per-event routing or
   dynamic tables/indexes are used" — the ClickHouse sink's `table` and `database` both accept
   template syntax. A `table: "{{ tenant }}"` config that worked on 0.53 now fails to start on 0.57.
   The skill says nothing about it.
3. **ClickHouse SQL-injection fix.** 0.57.0 lists *"ClickHouse SQL injection fixes via parameterized
   queries"* among its security fixes. A skill that ships a ClickHouse sink and has no security
   section should state the minimum patched version.
4. **New opt-in metric** `component_cpu_usage_ns_total`, enabled by `measure_cpu_usage: true` —
   directly relevant to `TROUBLESHOOTING.md:21-25` "OOM or high CPU" and `INTERNAL_MONITORING.md:17`
   "CPU/memory trends", neither of which names a metric.
5. **VRL 0.34.0**: dynamic regex in `parse_regex`; `parse_cef` gains `strict` (default `true`);
   panic fixed on inputs ≥65,535 bytes. None affects the shipped snippets.

Re-derive: `curl -s https://vector.dev/releases/0.57.0/`

### 5.3 Buffer semantics — **STALE / INCOMPLETE**

Source: <https://vector.dev/docs/architecture/buffering-model/>.

| Fact | Skill | Upstream | Verdict |
| --- | --- | --- | --- |
| `when_full` allowed values | `block`, `drop_newest` (`SKILL.md:180-181`, `BUFFERS_AND_ACKS.md:15-24`, `CLICKHOUSE_SINK.md:14`) | `block`, `drop_newest`, **`overflow`** — routes to a secondary buffer in a buffer topology chain | **INCOMPLETE — a third value, and it is the one a high-SLA pipeline wants** |
| `when_full` default | not stated | `block` | **MISSING** |
| buffer type default | not stated | memory | **MISSING** |
| sink memory buffer default size | not stated | 500 events | **MISSING** |
| behaviour when the disk buffer fills | *"can still stall under capacity/pathology conditions"* (`COMMUNITY_NOTES.md:12`, hedged as non-normative) | *"Vector forcefully stops itself"* when writes cannot guarantee durability | **STALE — the real behaviour is a hard stop, stated as documented fact, not a community hypothesis** |
| `data_dir` requirement | stated (`SKILL.md:54`, `BUFFERS_AND_ACKS.md:12`) | *"You **must** ensure that the data directory … is on a storage volume with enough free space."* | **VERIFIED** |

The `overflow` omission and the hard-stop omission are the two that change an architecture. `overflow`
is the mechanism that lets a pipeline take memory-buffer latency in the normal case and disk
durability in the outage case — the exact trade-off `BUFFERS_AND_ACKS.md` presents as binary.

### 5.4 The shipped templates do not compile — **STALE / BROKEN**

Source: <https://vector.dev/docs/reference/vrl/errors/>, diagnostic **651**: *"You've used a coalescing
operation (`??`) to handle an error, but in this case the left-hand operation is infallible, and so
the right-hand value after `??` is never reached."* It is a compile-time error, not a warning. `??`
coalesces **errors only, not null** — a missing path returns null without erroring, so `??` never
fires. Corroborated by a real-world instance: `vectordotdev/vector` ecosystem issue *"Fix error
unnecessary error coalescing operation with Vector 0.24"*.

`string!(...)` aborts rather than returning an error, so it is infallible and `?? "default"` after it
is dead code — E651. Every occurrence:

| File | Line | Text | Why it fails |
| --- | --- | --- | --- |
| `assets/templates/vector-basic.yaml` | 12 | `.service = string!(.service) ?? "unknown"` | E651 — `string!` infallible |
| `assets/templates/vector-basic.yaml` | 13 | `.level = downcase(string!(.level) ?? "info")` | E651 |
| `assets/templates/vector-clickhouse.yaml` | 12 | `.service = string!(.service) ?? "unknown"` | E651 |
| `assets/templates/vector-clickhouse.yaml` | 13 | `.level = downcase(string!(.level) ?? "info")` | E651 |
| `assets/templates/vector-clickhouse.yaml` | 14 | `.ts = .timestamp ?? now()` | E651 — a path lookup is infallible; this does **not** default a missing timestamp |
| `assets/templates/common.vrl` | 5 | `.level = downcase(string!(.level) ?? "info")` | E651 |

The fix is to drop the `!`: `string(.service) ?? "unknown"` is the fallible form the coalesce needs.
For the timestamp, `??` must be replaced with an explicit null check.

**This is the sharpest finding in the pack.** `SKILL.md:49` instructs *"use `vector validate` and
`vector test` before rollout"*, and `scripts/validate-and-test.sh` exists to do exactly that. Had
anyone once run the skill's own script over the skill's own templates, all six errors would have
surfaced. `VRL_GUIDE.md:35-37` even lists "do not leave fallible root expressions unhandled" as a
sharp edge — the templates fail the inverse rule, which the guide never states.

Re-derive on a host with Vector: `vector validate --no-environment assets/templates/vector-basic.yaml`
(expect a non-zero exit and an `error[E651]` diagnostic).

### 5.5 ClickHouse sink options — **mostly VERIFIED, with gaps**

Source: <https://vector.dev/docs/reference/configuration/sinks/clickhouse/>.

| Skill's claim | Verdict |
| --- | --- |
| `endpoint`, `table` required; `database` optional | **VERIFIED** — `SKILL.md`/`CLICKHOUSE_SINK.md` list all three flatly without marking which are required |
| `compression` accepts `gzip`, `zstd` | **VERIFIED** — full enum is `gzip` (default), `none`, `snappy`, `zlib`, `zstd`; the skill's "(`gzip`, `zstd`, etc.)" at `SKILL.md:190` hides the default and three values |
| `batch.max_bytes`, `batch.max_events`, `batch.timeout_secs` | **VERIFIED** — defaults `1e7` and `1`s are not stated by the skill; the template hardcodes the default |
| `date_time_best_effort` | **VERIFIED** — bool, default `false`, sets `date_time_input_format=best_effort` |
| `skip_unknown_fields` | **VERIFIED** — sets `input_format_skip_unknown_fields`. The skill's "use only if you are intentionally tolerating schema drift" (`SKILL.md:192`) is correct but names no consequence: fields silently vanish |
| `acknowledgements.enabled` | **VERIFIED** |
| `auth` strategies | **VERIFIED** — `aws`, `basic`, `bearer`, `custom`; skill names none |
| `batch_encoding.codec = "arrow_stream"` | **VERIFIED but ambiguous** — `batch_encoding.codec` exists and is marked **beta**, and separately `format` also accepts `arrow_stream`. The skill (`SKILL.md:106,188`, `CLICKHOUSE_SINK.md:25`) presents only the `batch_encoding` path and never says it is beta |
| `format: json_each_row` as default | **VERIFIED** — full enum `arrow_stream`, `json_as_object`, `json_as_string`, `json_each_row`; the skill omits `json_as_object` |
| retry/timeout behaviour | **UNSPECIFIED BY THE SKILL** — upstream documents `request.retry_attempts`, `request.retry_initial_backoff_secs` (default 1s), `request.retry_max_duration_secs` (default 30s), `request.concurrency` (default `adaptive`). The skill says "document … retries, and timeout behavior" and names not one of them |
| `insert_random_shard`, `healthcheck.enabled` (default `true`), `proxy`, `encoding` | **MISSING from the skill entirely** |

### 5.6 Acknowledgements — **VERIFIED but under-specified**

Source: <https://vector.dev/docs/architecture/end-to-end-acknowledgements/>.

Upstream states the fanout rule concretely: *"If an event is sent to three sinks, and is only
processed successfully by two of them, we mark that event as having failed which ensures it can be
sent again"*, and *"Vector only notifies the source once all copies of an event have been processed
… the 'worst' status is the status reported to the source."* Not all sources can acknowledge — the
`socket` source cannot; Kafka and AWS SQS can.

The skill's version, `SKILL.md:174`: *"In fanout, remember sinks can influence source acknowledgement
behavior."* **VERIFIED as directionally true and useless as a rule.** It fails the wording test: an
agent can follow it exactly and still build a fanout that duplicates every event to two healthy
sinks each time a third fails. The concrete consequence — worst-status means retry means duplication
at the healthy sinks — is the thing `TROUBLESHOOTING.md:16-19` ("Data loss / duplication") should
say and does not.

### 5.7 CLI — **VERIFIED**

Source: <https://vector.dev/docs/reference/cli/>.

- `vector validate` — exists. Flags: `--deny-warnings/-d`, `--no-environment/-ne`,
  `--skip-healthchecks`, and now `--dangerously-allow-env-var-interpolation`. **VERIFIED.**
- `vector test` — exists. Now carries `--dangerously-allow-env-var-interpolation`. **VERIFIED.**
- `vector vrl` (`SKILL.md:48`, `VRL_GUIDE.md:21`) — exists, with `--program` and `--input`. **VERIFIED.**
- `--require-healthy` (`SKILL.md:57,184`, `INTERNAL_MONITORING.md:30`) — **VERIFIED**, and correctly
  placed: it is a flag on the **root** `vector` command (*"Exit on startup if any sinks fail
  healthchecks"*), not on `validate`. The skill writes `vector --require-healthy`, which is right.
- `vector top` — the lane brief asks about its flags. **The skill never mentions `vector top`**
  (`grep -rn 'vector top'` returns nothing). For the record it exists with `--human-metrics/-H`,
  `--no-reconnect/-n`, `--components/-c`, `--interval/-i`, `--url/-u`. Its absence is a gap:
  `TROUBLESHOOTING.md` has no live-inspection command at all, and `vector top` is the official one.

### 5.8 Unit-test syntax — **VERIFIED**

Source: <https://vector.dev/docs/reference/configuration/unit-tests/>. `tests[].name`,
`inputs[].insert_at`, `inputs[].type`, `inputs[].log_fields`, `outputs[].extract_from`,
`outputs[].conditions[].type: "vrl"`, `conditions[].source`, and `assert!` / `assert_eq!` are all
current. `assets/templates/vector-tests.yaml` is syntactically correct. Upstream also documents
`no_outputs_from[]`, which the skill never mentions — the only way to assert an event was *dropped*,
which is precisely what a routing or filtering transform needs.

### 5.9 Helm chart — **PARTIALLY VERIFIED**

`charts/vector/Chart.yaml` on the `develop` branch today declares `version: 0.57.0`,
`appVersion: 0.56.0-distroless-libc`.
Re-derive: `curl -s https://raw.githubusercontent.com/vectordotdev/helm-charts/develop/charts/vector/Chart.yaml`

`HELM_CHART_OPERATIONS.md` claims, assessed:

| Claim | Line | Verdict |
| --- | --- | --- |
| `Agent`→DaemonSet, `Aggregator`→StatefulSet, `Stateless-Aggregator`→Deployment | 6-8 | **VERIFIED** — this is the chart's documented `role` mapping |
| `existingConfigMaps` takes precedence over inline/custom config | 18 | **PLAUSIBLE, UNVERIFIED** — I did not reach a chart README statement of precedence today. Needs the owner to confirm against the chart README before Phase 2 restates it |
| `customConfig` replaces chart-generated defaults | 25 | **VERIFIED** in substance — consistent with the chart's documented behaviour |
| Escape Vector templates in Helm values, e.g. `{{ print "{{ host }}" }}` | 28-29 | **VERIFIED** as a standard Helm escaping idiom |
| Prefer digest pinning via `image.sha` | 34 | **PLAUSIBLE, UNVERIFIED** — the values key name needs confirming against the current chart's `values.yaml` |
| `helm template`, `helm lint`, `vector validate` before deploy | 45-48 | **VERIFIED** as commands |

The file states **no chart version at all** and therefore no re-derivation command — a direct D10
miss. Note also that the chart's `appVersion` (`0.56.0`) trails the current Vector release (`0.57.0`),
so a Helm-deployed pipeline is on a different Vector version from a package-installed one. Nothing in
the skill warns of that, and it is exactly the kind of drift that makes the 0.57 interpolation change
bite in one environment and not another.

---

## 6. Section 2 criteria 2, 5 and 8 — what `BUFFERS_AND_ACKS.md` actually answers

Lane instruction 5. This is the most important gap to characterise, because a log pipeline that
silently drops under load is an observability outage that hides itself.

`references/BUFFERS_AND_ACKS.md` is 742 bytes and 11 substantive bullets. Read in full.

### What it answers

| Question | Answered? | Its exact words |
| --- | --- | --- |
| Is a memory buffer less durable than a disk buffer? | **Yes** | *"faster / less durable / data can be lost on crash/restart"* vs *"more durable / slower"* |
| Does a disk buffer need `data_dir`? | **Yes** | *"requires `data_dir`, writable disk, and monitoring"* |
| What does `when_full = block` do? | **Partially** | *"backpressure propagates upstream"* — true, but does not say **to where**, and the "where" is the producing service |
| What does `drop_newest` do? | **Yes** | *"intentionally loses events"* |
| Are acknowledgements free? | **Yes** | *"Do not assume acknowledgements are free; they can materially affect throughput and failure semantics."* |

### What it does not answer

| Question | Status |
| --- | --- |
| **What is the default?** — buffer type, `when_full`, buffer size | **Absent.** Upstream: memory, `block`, 500 events for sinks. An agent that writes no `buffer` block gets a 500-event memory buffer that blocks — and this file never tells it that. |
| **What is the third `when_full` value?** | **Absent.** `overflow` exists and chains to a secondary buffer. Omitting it presents the choice as durability-vs-liveness binary when upstream offers both. |
| **What happens when the disk buffer fills?** | **Absent from this file.** It appears only in `COMMUNITY_NOTES.md:12` as a hedged hypothesis, *"can still stall under capacity/pathology conditions"*, in a file whose header says its contents are *"not normative Vector guidance"*. Upstream states it outright: **Vector forcefully stops itself.** The single most important failure fact about disk buffers is filed under "community notes I should not trust". |
| **How large should the buffer be?** | **Absent.** No arithmetic — no ingest-rate × tolerable-outage-duration sizing, no minimum, no disk headroom rule. |
| **Which sources support end-to-end acks?** | **Absent.** *"the source and sink path support them"* names no source. Upstream: Kafka and SQS yes, `socket` no. |
| **What does fanout actually do to acks?** | **Absent.** *"you understand fanout implications"* — an instruction to already know the answer. Upstream states it in one sentence: worst status wins; 2-of-3 success is a failure and is re-sent. |
| **What happens when ClickHouse is gone?** | **Absent from the entire skill.** Not one sentence anywhere describes the end-to-end behaviour when the sink is unreachable: sink retries with backoff → buffer fills → `when_full` decides → `block` back-pressures the source or `drop_newest` discards → disk full stops Vector. That chain is the skill's reason to exist. |
| **What are the retry and backoff options?** | **Absent.** `request.retry_attempts`, `request.retry_initial_backoff_secs` (1s), `request.retry_max_duration_secs` (30s), `request.concurrency` (`adaptive`) — none named here or anywhere in the skill. |
| **Is a telemetry path a gate or a contributor?** | **Absent — and this is the omission that matters most.** See below. |

### The discrimination the skill never makes

`alaa-reliability-sla` frames it as: *when this dependency cannot answer, does proceeding without it
let something through that must not get through?* Yes → gate, fails closed. No → contributor, fails
open.

For a Vector pipeline the answer is **not uniform, and it is knowable per path**:

- **Application logs and metrics → contributor → fail open.** Losing telemetry does not let anything
  through that must not get through. The correct configuration is `drop_newest` or an `overflow`
  chain, never `block`, because `block` propagates backpressure into the producing service and turns
  a telemetry outage into a product outage.
- **Audit and SOC evidence → gate → fail closed.** Losing an audit record does let something through
  unrecorded. The correct configuration is a disk buffer with end-to-end acknowledgements and
  `block`, accepting the backpressure.

`SKILL.md:38-45` calls buffering and acks "product decisions" and `SKILL.md:176-181` lists the options
neutrally. Nowhere does the skill give the agent a rule for choosing. An agent that reads
`BUFFERS_AND_ACKS.md` and picks `block` for an application-log path — a defensible reading of *"block:
preserve data, propagate backpressure"*, which the file lists first and describes favourably — has
just wired a ClickHouse outage into a latency spike on the product's request path.

**And this collides with a doctrine owner.** `alaa-observability-soc/SKILL.md:36` states:
*"Telemetry is fail-open for product traffic: a failed backend, Collector, Vector sidecar, or SOC
destination degrades…"* SOC owns requirement levels and, per the brief, **SOC wins on whether
something is required**. So the fleet has already decided that a Vector path carrying product
telemetry must fail open — and this skill offers `block` as a co-equal option with no reference to
that decision. The skill does not merely omit the rule; it contradicts a binding one.

---

## 7. Boundary analysis

Lane instruction 6, plus defect class 11.

### What the skill currently says

`SKILL.md:83-90`, the entire boundary surface:

```
## Companion routing
- `$clickhouse-performance-schema-ops`
  - Pair when Vector output shape or ClickHouse ingestion behavior is part of the root cause.
- `$alaa-observability-soc`
  - Pair when alerting, incident visibility, or SOC-grade logging expectations change.
- `$caas-arvan-kuber`
  - Pair when the rollout target is Arvan CaaS or Kubernetes platform constraints matter.
```

Three routes, all phrased as "pair when" — a suggestion to consult, not a statement of ownership. The
skill never says what it does **not** own. It names none of `alaa-services-contract`,
`alaa-reliability-sla`, `alaa-security-review`, `alaa-testing-strategy`, `alaa-project-constitution`,
`alaa-prompting-guide`, `alaa-k8s-helm`, `alaa-docker-production`, `alaa-signoz-clickhouse-docs`,
`alaa-cc-orchestrator` or `alaa-codex-orchestrator`. That is the finding the last five batches all
reported.

### The boundary is asserted from the other side and not reciprocated

`clickhouse-performance-schema-ops` — Batch 4, already at standard — states its half twice, and
names this skill explicitly:

- Its description: *"…nor for Vector transform internals, which belong to
  /vector-rust-observability-pipelines."*
- Its `SKILL.md:49-51`: *"Vector source, transform, sink, and buffer internals:
  `/vector-rust-observability-pipelines` (`$vector-rust-observability-pipelines`) — **that skill owns
  what the pipeline writes, this one owns what the table must be.**"*

That last clause is the cleanest statement of the boundary in either direction, and it was written by
the counterparty. This skill has never said it back.

`alaa-observability-soc` also claims territory here. Its description covers *"Collector and Vector
topology"* — a direct overlap with `SKILL.md:28-36` ("Treat Vector as a topology"). Under the brief's
tie-break, SOC owns the **requirement level** ("must this path fail open?") and this skill owns the
**mechanism** ("which `when_full` value implements that"). Neither file says so.

### The three-way ClickHouse boundary — proposed, in the words I would want the other sides to use

Offered as a proposal requiring reciprocal agreement, **not** as settled. `alaa-signoz-clickhouse-docs`
is being analysed concurrently in another lane and has not agreed to any of this.

> **`vector-rust-observability-pipelines` owns the write path.** Sources, transforms, VRL, buffers,
> acknowledgements, backpressure, sink retry and batching, and what the pipeline does when ClickHouse
> is unreachable. It owns the *shape and timing of the bytes arriving* at a ClickHouse table. It
> writes no DDL, chooses no `ORDER BY`, `PARTITION BY`, engine or column type, and tunes no read
> query.
>
> **`clickhouse-performance-schema-ops` owns the table and the read path.** DDL, engine, ordering,
> partitioning, retention, part counts and merges, query tuning, and what a *service* does when
> ClickHouse is slow or gone. In its own words: *"that skill owns what the pipeline writes, this one
> owns what the table must be."* When a Vector sink produces too many parts, the part-count budget is
> its rule and the batch settings that satisfy the budget are ours.
>
> **`alaa-signoz-clickhouse-docs` owns the SigNoz-managed schema and its query surface.** The
> OpenTelemetry logs, traces and metrics tables SigNoz creates and migrates, Query Builder v5
> routing, and panel and alert SQL over them. Neither of the other two writes DDL against a
> SigNoz-owned table or invents a SigNoz table name.
>
> **The two seams, stated as rules rather than principles.** (1) When a Vector sink writes into a
> SigNoz-managed table, SigNoz's schema is the contract and this skill's VRL must produce exactly the
> columns it declares; a schema change request is filed against SigNoz, never worked around with
> `skip_unknown_fields`. (2) When a Vector sink writes into a fleet-owned table, the ingest-pipeline
> repository owns the DDL per `clickhouse-performance-schema-ops`, and this skill's batch and buffer
> settings are chosen to meet that repository's stated part-count and latency budget.

**Status: needs reciprocal agreement.** `clickhouse-performance-schema-ops` has already written a
compatible half. `alaa-signoz-clickhouse-docs` has not been asked. Phase 2 must not ship this as
settled in one file only — that is precisely the error decision D8 was written to prevent.

### What the skill should own and does not

- **The Ala ingest pipeline itself.** `clickhouse-performance-schema-ops`' description refers to *"the
  ingest-pipeline repository — the one that owns the ClickHouse DDL directory **and the Vector
  topology writing into it**"*. So a real Ala Vector topology exists and this skill is its owner.
  This skill contains **zero** Ala-specific content: no `alaa_*` metric names, no reference to the
  services contract, no mention of the `chkit` read lane or the ingest-pipeline repository, no tenant
  column. It is a generic Vector tutorial sitting in a position of fleet responsibility.
- **The fail-open/fail-closed rule per telemetry path** (§6), owned jointly with
  `alaa-observability-soc` on requirement level.
- **Secrets in Vector configuration** — `SECRET[backend.key]` versus env interpolation. Nobody else
  owns Vector's config secret surface, and 0.57 changed it.

---

## 8. Defect-class findings

Only classes actually found. Section 3 of the brief.

**Class 2 — wrong trigger syntax. CONFIRMED, one-directional.**
`grep -rn '\$[a-z][a-z0-9-]*'` → 3 hits in `SKILL.md` (lines 85, 87, 89), all Codex `$name`.
`grep` for `/name` form → **zero hits**. This skill is loaded in Claude Code (it appears in the
runtime skill list as `sohrab-skills:vector-rust-observability-pipelines`), where `$name` is not a
trigger. Every cross-skill route in this skill is unusable from Claude Code. Compare
`clickhouse-performance-schema-ops/SKILL.md:52-53`, which writes both:
`` `/alaa-cc-orchestrator` (`$alaa-cc-orchestrator`) ``.
`INSTALL.md:10` compounds it: *"invoke via `/skills` or `$vector-rust-observability-pipelines`"* —
`/skills` is not a trigger form used anywhere in this fleet.

**Class 3 — duplication between body and references. CONFIRMED, measured.**
Whole-section restatements: `SKILL.md:61-66` ↔ `HELM_CHART_OPERATIONS.md`; `SKILL.md:169-184` ↔
`BUFFERS_AND_ACKS.md`; `SKILL.md:186-194` ↔ `CLICKHOUSE_SINK.md`; `SKILL.md:155-160` ↔
`VALIDATION_AND_TESTING.md`; `SKILL.md:162-167` ↔ `INTERNAL_MONITORING.md`; `SKILL.md:96-108` ↔
`INTERNAL_MONITORING.md:20-27` + `VRL_GUIDE.md:26-32` + `CLICKHOUSE_SINK.md:23-29`; `SKILL.md:196-203`
↔ `prompts/MULTI_AGENT_PROMPT.md`; `SKILL.md:205-212` ↔ `prompts/AGENT_PROMPT.md:22-29`;
`SKILL.md:214-230` ↔ `references/README.md`.
Exact line-level duplicates include `SKILL.md:97` / `INTERNAL_MONITORING.md:22` (similarity 1.00) and
`SKILL.md:137` / `TOPOLOGY_WORKFLOW.md:6` (1.00). Aggregate measure: no reference file exceeds 55%
new content over the body; `references/README.md` is 14%.

**Class 5 — long numbered procedure nobody reads in order. CONFIRMED.**
`SKILL.md:110-167`, "Default workflow", six sequential steps over 58 lines. `SKILL.md:112-121` alone
asks the agent to pick among eight topology shapes before any symptom is known. `TROUBLESHOOTING.md`
is structured by symptom but each branch is a list of nouns to "inspect" with no discriminating
command, threshold, or escalation.

**Class 6 — description that only says when to use. PARTIAL — present but weak.**
`SKILL.md:3` does carry a negative clause: *"Do not use it for generic logging advice that ignores
Vector pipeline mechanics."* One clause, and it excludes only the obvious case. It routes to no other
skill. Compare `alaa-observability-soc`, whose description routes three named alternatives. Length is
237 characters — well inside the 900 ceiling, so there is ample budget to add routing.

**Class 9 — measure against section 2 and name the gaps. CONFIRMED.** §4: 0 satisfied, 6 fail,
3 partial, 1 unnamed delegation.

**Class 10 — shrink where possible. CONFIRMED, in the unusual direction.** The body must shrink
(227 → under 120 lines) while the *skill* must grow, because eleven stub references cannot carry the
domain. See §10 for the budget.

**Class 11 — companion boundary. CONFIRMED.** §7. Three "pair when" suggestions, no statement of
non-ownership, no reciprocation of a boundary the counterparty has already written.

**Not found:** class 1 (no model names — `grep` for `gpt|claude|opus|sonnet|o1|o3` returns nothing);
class 4 (no project-specific content in the body — the opposite problem, §7); class 7 (no Python, no
`Path(__file__)`, no temp dirs); class 8 (no `__pycache__` in this skill — though one does exist at
`D:\Sohrab\Project\skills\scripts\__pycache__`, which belongs to the repository-cleanup lane).

**Additional defects outside the numbered classes:**

- **D-A. Internal contradiction.** `INSTALL.md:12` says `allow_implicit_invocation: false`;
  `agents/openai.yaml:7` says `true`.
- **D-B. Wrong install path.** `INSTALL.md:5-6` contradicts the authoritative `install-skills.md`.
- **D-C. Shipped templates do not compile.** §5.4, six occurrences of VRL E651.
- **D-D. Stale factual claims presented as a migration checklist.** §5.1, three of four wrong.
- **D-E. `references/OFFICIAL_LINKS.md` is referenced at `SKILL.md:23` but omitted from the
  "Included resources" list at `SKILL.md:214-230`**, which lists 9 of the 11 reference files.
  `references/README.md` is likewise absent from it. The skill's own index of itself is incomplete.
- **D-F. Validator warning.** Observed by running the repository validator (§9): *"top-level body is
  227 lines"* against a 120-line threshold.

---

## 9. Executable-check inventory

Lane instruction 7. The skill ships exactly **one** script, 240 bytes.

### `scripts/validate-and-test.sh`, read in full

```bash
#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <vector-config-file> [more config/test files...]"
  exit 1
fi

echo "==> vector validate $*"
vector validate "$@"

echo "==> vector test $*"
vector test "$@"
```

### Observed behaviour

`bash -n` passes. `vector` is **not installed** in this container and was **not installed**. Run
read-only; observed output verbatim:

```
=== case 1: no args ===
Usage: .../scripts/validate-and-test.sh <vector-config-file> [more config/test files...]
EXIT=1

=== case 2: arg given, vector absent ===
==> vector validate /tmp/nonexistent.yaml
.../scripts/validate-and-test.sh: line 11: vector: command not found
EXIT=127

=== case 3: --help ===
==> vector validate --help
.../scripts/validate-and-test.sh: line 11: vector: command not found
EXIT=127
```

### Verdict against the exit-code contract

**It does not honour 0/1/2, and it fails in the exact way the contract exists to prevent.**

| Situation | Required | Observed |
| --- | ---: | ---: |
| Clean | 0 | 0 (only if Vector present and config valid) |
| Findings (config invalid / test failed) | 1 | **Vector's own exit code, passed through unmapped** |
| Could not run (Vector absent) | 2 | **127** |
| Could not run (no arguments) | 2 | **1 — reported as "findings"** |

Two distinct misclassifications. A missing `vector` binary yields 127, which no gate in this
programme is written to interpret. A usage error yields **1**, which a gate reads as "the config has
findings" — a wrong argument list and a broken pipeline config are indistinguishable to any caller.

Three further defects:

- **`set -e` couples the two checks.** If `vector validate` fails, `vector test` never runs. A single
  invocation cannot report both classes of finding, so an agent fixing a validation error learns
  nothing about its tests until the next round trip.
- **No `--help`, no `--self-test`.** `--help` is passed straight to `vector validate` as a config
  path. The fleet's pattern — established by `alaa-quasar-app-vite-v3/scripts/check-upstream-versions.mjs`
  and carried by the nine Batch 6 checkers — is `--help`, `--self-test`, per-request timeout, and
  proxy handling.
- **It has never been run against the skill's own templates.** Doing so would have found all six
  E651 errors in §5.4. This is the concrete instance of the carry-over's rule: *a skill whose rules
  have no tool that reports a violation is shipping preferences, not rules.* Here the tool exists and
  was never pointed at the artefacts.

### Windows

**It does not run on Windows PowerShell or `cmd`.** `#!/usr/bin/env bash`, `set -euo pipefail` and
`[[ ]]` require Git Bash or WSL. The definition of done requires bundled scripts to run on Windows,
and the device is `win32` (confirmed via `get_device_info`). The fleet's answer is Node `.mjs`
(29 skills ship one). No CRLF was found in any file in this skill (checked with `file` across all 21
files), so the CRLF defect class does not apply here.

### Repository validator — run, observed

Reconstructed a minimal tree and ran the real validator, staged from
`D:\Sohrab\Project\skills\scripts\validate_sohrab_skill_pack.py`:

```
Warnings:
- vector-rust-observability-pipelines: top-level body is 227 lines
EXIT=0
```

**Passes with one warning.** Specifically confirmed by reading the validator source:

- The heading rule at line 184 uses `re.I | re.M`, so `## When NOT to use` (`SKILL.md:68`) **does**
  satisfy it despite the casing. Not a defect.
- `agents/openai.yaml` passes: `short_description` is 38 chars (band 25–64), and `default_prompt`
  contains `$vector-rust-observability-pipelines`.
- Description is 237 chars, far inside both the 900 target and the 1024 hard limit, and contains no
  angle brackets.
- The 120-line body warning at line 187 is the one finding.
- Note the validator's `PATH_RE` (line 10) covers `references|docs|examples|scripts|assets|output|test|tests`
  but **not `prompts`**, so the two `prompts/` paths at `SKILL.md:229-230` are never existence-checked.

### Checkers this skill should ship and does not

Zero of the following exist. Each is deterministic and would have caught a live defect:

1. **`check-vector-configs.mjs`** — run `vector validate` over every file in `assets/templates/`.
   Would have caught all six E651 errors. Exit 2 if `vector` is absent.
2. **`check-upstream-version.mjs`** — resolve the current Vector release and the current chart
   version, compare against the pins in the skill, exit 1 on drift. Would have caught the four-release
   lag and the 0.57 interpolation change.
3. **`check-metric-names.mjs`** — assert every internal metric name the skill asserts appears in
   current upstream documentation. Would have caught §5.1's three wrong claims.
4. **`check-cross-skill-links.mjs`** — assert every cross-skill route gives both `/name` and `$name`
   and names a directory that exists. Would have caught the zero-`/name` finding.

---

## 10. Phase 2 work order

File-by-file, executable without re-deriving the analysis.

### Retire to `_to_delete/20260729-b8/`

| File | Bytes | Reason |
| --- | ---: | --- |
| `INSTALL.md` | 429 | 1-of-69 anomaly; install paths owned by `install-skills.md`; both its claims are false (§3.1) |
| `prompts/AGENT_PROMPT.md` | 941 | 1-of-69 anomaly; 26% new; prompt authoring owned by `alaa-prompting-guide`. **Move its five "hard constraints" (lines 14–19) into the body's numbered rules before retiring.** |
| `prompts/MULTI_AGENT_PROMPT.md` | 698 | 1-of-69 anomaly; 16% new; orchestration owned by `alaa-cc-orchestrator` / `alaa-codex-orchestrator` |
| `references/README.md` | 288 | 1-of-69 anomaly; 14% new; superseded by `00-topic-map.md` |
| `references/COMMUNITY_NOTES.md` | 1,175 | Merge its 6 items into `TROUBLESHOOTING.md` first; item 2 must be **promoted to normative** and corrected (§5.3) |

Retire 3,531 bytes. Delete nothing.

### Rewrite

**`SKILL.md` → target ≤ 120 body lines, ~5,000 bytes.** Keep: frontmatter (rewritten), scope, the
five core principles compressed to numbered rules each carrying its reason, "When NOT to use", the
output contract, a "Not owned here" section, and a pointer to the topic map. Move out everything in
§2a. Specifically:
- Frontmatter description: add routing clauses naming `/clickhouse-performance-schema-ops`,
  `/alaa-signoz-clickhouse-docs`, `/alaa-observability-soc`. Budget: 237 → up to 900 chars.
- Every cross-skill reference in dual form: `` `/name` (`$name`) ``.
- Replace `SKILL.md:74-82` "Fast entry" (which names no paths) with a pointer to
  `references/00-topic-map.md`.
- Delete `SKILL.md:196-203` "Multi-agent plan" entirely; route to the orchestrators.
- Add the fail-open/fail-closed rule (§6) as a numbered body rule, with SOC named as the owner of the
  requirement level.

### Create

| File | Contents |
| --- | --- |
| `references/00-topic-map.md` | Situation → one file, in the `clickhouse-performance-schema-ops` format. Required: the skill has 10 references after retirement, over the ≥9 threshold. Validator checks every path it names. |
| `references/80-version-and-upgrade-deltas.md` | Absorbs `SKILL.md:92-108`. **Corrected** 0.53 renames (all four pairs, correct old names, 20→26 buckets, transition-period gauges), plus 0.54–0.57 deltas, with 0.57's interpolation default, template confinement, and the ClickHouse SQL-injection fix. Each pin carries its re-derivation command (D10). |
| `references/85-security-and-secrets.md` | `SECRET[backend.key]` versus env interpolation and the 0.57 default change; redaction rules naming fields; sink credential handling; tenant scoping on templated `table`/`database`; the 0.57 confinement boundary as a control. Routes trust-boundary review to `/alaa-security-review`. |
| `scripts/check-vector-configs.mjs` | Runs `vector validate` over every `assets/templates/*.yaml` and `common.vrl`. **0** all valid, **1** any invalid, **2** `vector` absent or unrunnable. `--help`, `--self-test`. Node, so it runs on Windows. |
| `scripts/check-upstream-version.mjs` | Resolves current Vector release (filtering `vdev-*` tags) and chart version; compares to the skill's pins; **0** current, **1** drift, **2** network/proxy failure. `--help`, `--self-test`, per-request timeout, `HTTPS_PROXY`/`NO_PROXY`. |

### Rewrite and expand references

| File | From | Target | Must gain |
| --- | ---: | ---: | --- |
| `BUFFERS_AND_ACKS.md` | 742 | **~7,000** | Every item in §6's "does not answer" table: defaults, `overflow`, disk-full hard stop, sizing arithmetic, ack-capable sources, worst-status fanout, the full ClickHouse-is-gone chain, retry/backoff option names, and the gate-vs-contributor rule with SOC named. **The single highest-priority file in this work order.** |
| `CLICKHOUSE_SINK.md` | 1,160 | ~6,500 | Required vs optional; every default from §5.5; the four `request.*` retry options; full `compression` and `format` enums; `batch_encoding` marked beta; 0.57 template confinement; `insert_random_shard`, `healthcheck.enabled`, `proxy`; the three-way boundary (§7). |
| `TROUBLESHOOTING.md` | 739 | ~6,500 | Restructure per defect class 5: symptom → diagnosis → smallest retry → escalation. Every branch gets a discriminating command — `vector top` (currently absent from the whole skill), the internal metric to read, the log field to grep. Absorbs `COMMUNITY_NOTES.md`. |
| `VRL_GUIDE.md` | 1,040 | ~6,000 | The E651 rule the templates violate; fallible-vs-infallible (`f!` aborts, `f` returns an error, `??` coalesces errors not null); `no_outputs_from[]`; the 0.53 metric helpers (already correct); VRL 0.34 changes. |
| `INTERNAL_MONITORING.md` | 971 | ~5,500 | Corrected renames (§5.1); `component_cpu_usage_ns_total` and `measure_cpu_usage`; alertable metric names with thresholds; route Ala-side names to `/alaa-services-contract` and requirement levels to `/alaa-observability-soc`. |
| `VALIDATION_AND_TESTING.md` | 549 | ~5,000 | Absorbs `SKILL.md:155-160`; the 0.57 interpolation flag on both `validate` and `test`; the rule that split config and test files must be passed together (which `vector-tests.yaml` silently requires); the exit-code contract; failure-case test design. |
| `TOPOLOGY_WORKFLOW.md` | 862 | ~6,000 | Absorbs `SKILL.md:112-145` steps 1–3; per-path delivery-contract template; fanout isolation as a rule with its reason. |
| `HELM_CHART_OPERATIONS.md` | 1,915 | ~5,000 | Absorbs `SKILL.md:61-66`; pin the chart version with its re-derivation command; **verify the two PLAUSIBLE claims in §5.9 before restating them**; warn that chart `appVersion` trails the Vector release. |
| `OFFICIAL_LINKS.md` → `90-source-map.md` | 2,106 | ~2,500 | Rename for fleet consistency; add re-derivation commands per D10. |

### Fix the templates

All three, per §5.4: `string!(x) ?? d` → `string(x) ?? d`; replace `.timestamp ?? now()` with an
explicit null check. Replace `${CLICKHOUSE_USER}`/`${CLICKHOUSE_PASSWORD}` with the `SECRET[...]`
form, or keep env interpolation and state the 0.57 flag requirement in a comment beside it. Then run
`scripts/check-vector-configs.mjs` and paste its output into the Phase 2 report.

### Byte budget

| | Bytes |
| --- | ---: |
| Current total | 25,769 |
| Retired | −3,531 |
| `SKILL.md` reduced (9,487 → ~5,000) | −4,500 |
| References expanded to fleet norm | +45,000 |
| New references (80-, 85-, topic map) | +12,000 |
| New scripts | +14,000 |
| **Target total** | **~88,000** |

This is a **3.4× increase** and the definition of done requires naming the capability that earns it.
It is earned by four things the skill does not currently have: (1) a correct and complete account of
buffering, acknowledgement and backpressure failure behaviour, which is the skill's declared subject
and is currently 742 bytes; (2) a security surface, currently absent, in a skill that ships
credentials in a template; (3) two executable checkers, where the skill currently has one broken
shell script; (4) version currency through 0.57.0 including two breaking changes that silently break
the skill's own templates. The result would sit at roughly half the fleet median (~150 KB) — still
one of the smaller skills, appropriately.

---

## 11. Open questions for the owner

### Q1. The `alaa-` prefix — deferred by Batch 1, still open

Seven of 69 skills lack the prefix: `vector-rust-observability-pipelines`, `ansible-generator`,
`ansible-validator`, `caas-arvan-kuber`, `clickhouse-performance-schema-ops`,
`jitsi-platform-architect`, `service-runtime-kit-governance`, `tusd-upload-platform`.
**I am not deciding this.** Recording it with a recommendation, as instructed.

**Recommendation: rename all seven together, in a dedicated pass, after Batch 8 ships — not inside
Batch 8.**

Reason: the prefix carries real meaning — it marks a skill as fleet doctrine rather than a
general-purpose tool — and `clickhouse-performance-schema-ops`' description proves these seven are
already doctrine, since it defines Ala-fleet policy (the `readonly=2 chkit` lane) under an unprefixed
name. So the naming currently lies about what the skills are. But a rename touches every cross-skill
reference in the tree, every `agents/openai.yaml` `default_prompt`, both READMEs, `install-skills.md`,
the validator's `SKILL_NAME_RE` (which hardcodes the prefix list
`alaa|golang|caas|ansible|clickhouse|jitsi|service|tusd|vector|playwright|openfga|openai`), and any
`~/.codex/skills` symlink on the owner's machine. Doing that inside a content batch mixes a mechanical
rename with substantive edits and makes the diff unreviewable.

Trade-offs:
- **Rename now, inside Batch 8** — one less pass, but Batch 8's real work (correcting three false
  Vector facts and six broken templates) gets buried in a tree-wide rename diff, and only 1 of the 7
  affected skills is in this batch, so the tree would be *more* inconsistent mid-flight, not less.
- **Rename later, all seven at once** — the tree stays inconsistent for one more cycle, but the
  rename is a single reviewable mechanical change with a single link-check to prove it. Batch 8
  already owns a tree-wide link check, which is the natural place to *measure* the cost and hand the
  owner an exact file list.
- **Never rename; drop the convention** — cheapest, and defensible if the prefix is read as "authored
  by Alaa" rather than "fleet doctrine". But then `README.md` should say so explicitly, because
  today's tree implies a rule it does not follow.

### Q2. Is `references/00-topic-map.md` mandatory at ≥9 references?

The carry-over flags this as unresolved fleet-wide. Measured today: **29 of 69** skills carry one.
Three skills have ≥9 references and no topic map: `alaa-prompting-guide` (14), **this skill (11)**,
and `alaa-async-messaging` (9).

**Recommendation: mandatory at ≥9, and add one here regardless of the fleet decision.** Even if the
convention stays optional, this skill needs it: its current routing surface (`SKILL.md:74-82`) names
no file paths at all, and the validator existence-checks topic-map paths but does not check the
`prompts/` paths this skill currently relies on. Trade-off: making it mandatory obliges two other
skills outside Batch 8's membership to gain one, which is scope the owner may not want to authorise.

### Q3. Does the Ala ingest pipeline belong in this skill?

`clickhouse-performance-schema-ops` states that an ingest-pipeline repository owns *"the ClickHouse
DDL directory and the Vector topology writing into it"*. This skill contains nothing Ala-specific.

**Recommendation: yes, add a reference — `references/70-ala-ingest-pipeline.md` — naming the
repository, its ClickHouse targets, its delivery contract per path, and which paths are gates and
which are contributors.** Reason: a generic Vector tutorial cannot answer "should this path block?"
for the Ala fleet, and that is the question the skill exists to answer. Trade-off: it requires the
owner to supply facts I cannot derive (repository name, table targets, current topology), and getting
them wrong is worse than omitting them. If the owner cannot supply them this cycle, the correct
interim move is a placeholder that names the repository and says the contract is unrecorded — never
invented specifics.

### Q4. Reciprocal agreement on the three-way ClickHouse boundary

§7 proposes wording. `clickhouse-performance-schema-ops` has already written a compatible half;
`alaa-signoz-clickhouse-docs` has not been consulted and is in a concurrent lane.

**Recommendation: have both Batch 8 lanes write their halves in the same pass, and have the
`clickhouse-performance-schema-ops` half re-read (not re-written — it is already correct) to confirm
the three statements compose.** Reason: decision D8 exists because a boundary asserted from one side
is a boundary the other side has not agreed to. Trade-off: this couples two lanes that are otherwise
independent, so it should be the last edit in each, not the first.

### Q5. Should the shell script be replaced by Node, or dropped?

**Recommendation: replace with Node `.mjs`.** Reason: the device is Windows, the definition of done
requires scripts to run there, and 29 skills already ship `.mjs`. The current script cannot run in
PowerShell and misclassifies both failure modes. Trade-off: a Node checker that shells out to
`vector` still needs `vector` on PATH — but that is exactly what exit code 2 is for, and the shell
script's 127 is the bug being fixed.


---

# Appendix C — `alaa-docs-farsi`

# Batch 8 — Lane L3 analysis: `alaa-docs-farsi`

Analysis date **2026-07-29**. Phase 1, read-only. Nothing on the device was modified.
Staged copy read in full: `/home/claude/b8/src/alaa-docs-farsi/` (14 files, 133,756 bytes).
Device original verified byte-identical by size, file for file, at
`D:\Sohrab\Project\skills\skills\sohrab\alaa-docs-farsi\` (reached read-only through
`mcp__remote-devices__device_bash` at
`/sessions/rcw-01nfpk8ndxrrswndyp6txjwc/mnt/skills/skills/sohrab/alaa-docs-farsi`).

**Headline.** The lane premise that this is the fleet's Persian-documentation skill is empirically
false, and that falsehood is the single most consequential finding in this lane. The skill contains
**zero Persian characters — zero non-ASCII bytes of any kind** — and its body mandates English
output twice. Meanwhile thirty-odd call sites across the rest of the fleet, including two in
`alaa-frontend-doc-annotations` which Batch 6 shipped *at standard*, route Persian deliverables to
this skill. The fleet and the skill contradict each other on the skill's central premise.

---

## 1. Inventory

| File | Bytes | What it actually contains |
|---|---:|---|
| `SKILL.md` | 10,703 | 130-line body. Purpose, when/when-not, 9-step quick start, doc-set trigger rules, non-negotiables, doc-impact checklist, 8-entry companion routing (all `$name`, no `/name`), subagent strategy, **a full 13-line reference-navigation list that duplicates `references/00-topic-map.md`**, maintenance rules. |
| `agents/openai.yaml` | 669 | Codex interface block. `short_description` 51 chars (valid, 25–64). `default_prompt` names `$alaa-docs-farsi`. `allow_implicit_invocation: true`. |
| `references/00-topic-map.md` | 3,902 | Not a topic map with trigger conditions — a **table of contents listing the headings of the other reference files**. 93 content lines, none of which is a rule. Contains no routing predicate ("read X when Y"); it lists filenames and their headings. |
| `references/10-language-and-links.md` | 6,355 | Purpose, when/when-not (a third copy), language rules, hard constraints, repo-safe link rules with correct/incorrect examples, doc-graph linking rules, link-validation workflow. The link rules here are the ones `scripts/check_markdown_links.py` actually enforces. |
| `references/20-readme-big-picture-contract.md` | 11,750 | Largest numbered reference. README/BIG_PICTURE role split, four-audience requirement, richness-protection rule, required section lists for both files, quality-bar question lists, Mermaid diagram coverage rules, architectural-patterns section, frontend-integration coverage, new-service baseline extraction, shared section extensions. |
| `references/30-api-summary-contract.md` | 6,674 | Purpose and required structure of `docs/api-summary.md`, formatting rules, example-selection rules, quality bar. Names no OpenAPI artifact and no Postman artifact path. |
| `references/40-sync-workflow-and-evidence.md` | 8,249 | Provenance list of seven source repos, the 9-row repository sync matrix, AGENTS-alignment notes, the 13-step production workflow, an 11-item output checklist, 9 evidence checks, 12 anti-patterns. |
| `references/50-data-architecture-contract.md` | 6,746 | Why/when `docs/data-architecture.md` exists, filename preservation, separation-of-roles list, 12-heading required structure, table and cache inventory column lists, storage coverage rules, request-walkthrough rules, diagram rules, quality bar. |
| `references/60-errors-events-observability-contract.md` | 7,404 | Same shape for `docs/errors-events-observability.md`: 12-heading structure, error-matrix and event-inventory column lists, error/event/observability coverage rules, diagram rules, quality bar. **Names `request-id` and `traceparent` without citing their owner, and spells the first one wrong.** |
| `references/70-subagent-doc-workflows.md` | 7,003 | Four-track read-heavy subagent split, when/when-not, parent responsibilities, per-subagent return contract, merge rules, two verbatim example parent prompts, `explorer`/`default`/`worker` role guidance, post-merge validation. **Codex-specific throughout** ("explicitly ask Codex to spawn the subagents", `.codex/agents/`). |
| `references/80-implementation-gap-backlog.md` | 2,041 | Rules for producing `remaining-task.md`: when to create, evidence standard (cite both the promise and the code), required shape, exclusions, Postman handoff. **Not state — it is instruction.** The lane brief's premise that this file is a backlog is wrong; it is the *contract for writing* a backlog and contains no backlog items. |
| `references/90-source-map.md` | 2,194 | Four-rank source priority, six external URLs, freshness triggers, community-source limits, one good/bad example. The **only** reference file that names companion skills. |
| `references/full-guide.md` | 52,953 | 39.6% of the skill and 45.9% of `references/`. A single concatenation of references 10, 20, 30, 50, 60, 70 and 40 in that order, plus a table of contents and a **lossy, divergent condensation of 80**. Contains nothing from 90. |
| `scripts/check_markdown_links.py` | 7,113 | 207-line stdlib-only Markdown link and anchor validator. Honours 0/1/2 for its anticipated failure paths, crashes to exit 1 on an unreadable file. No `Path(__file__)`, no temp dirs, no writes. Details in section 6. |

No `__pycache__`, no `.pyc`, no `assets/`, no `agents/claude.*`.

---

## 2. The ten-criteria verdict table

The question is: does an agent using this skill produce work fit for a service that must not fail?
For a documentation skill the criteria bind on **what the produced document must say about** each
concern, and on the skill's own operational safety.

| # | Criterion | Verdict | Evidence | What a fix must add |
|---|---|---|---|---|
| 1 | Correctness and testability | **FAIL** | The only executable check is `scripts/check_markdown_links.py`, invoked at `SKILL.md:69`, `10-language-and-links.md:84`, `40-sync-workflow-and-evidence.md:97`, `70-subagent-doc-workflows.md:116`. It validates **link syntax only**. Every substantive rule — "required sections in README", "12-heading structure for `docs/data-architecture.md`", "include at least one state-snapshot table" — has **no checker**. `40:74` states the done criterion as "confirm the new docs are richer or clearer than before", which is not a predicate an agent can fail. | A `check_doc_contract.py` that, given a repo, asserts the presence of each required heading in each of the five named docs, asserts every fenced `json` example parses, asserts every `See also` block resolves, and exits 0/1/2. The heading lists at `20:76-93`, `20:110-133`, `50:48-63`, `60:49-63` are already machine-checkable as written — that is the whole point of writing them as numbered heading lists. |
| 2 | Failure behaviour | **FAIL** | The skill tells the agent to *document* failure (`60:87-92`, `60:94-100`) but states no failure behaviour of its own. There is no rule for: the target repo has no `AGENTS.md`; two source-of-truth files disagree; Python is absent — `10:85` says "verify the path and heading manually", with no bound on what "manually" means for 400 links; a subagent returns nothing (`70:111-117` assumes all return). `40:98` says "reconcile conflicting subagent findings against source-of-truth files" with no rule for when the source of truth is itself ambiguous. | A failure-class table: symptom → diagnosis → smallest retry → escalation, covering absent `AGENTS.md`, absent Python, contradictory sources, a subagent that fails or returns empty, and a doc whose existing content contradicts current code. And the fail-closed discrimination: when the agent cannot verify a claim, does publishing it let something wrong through? For a security or auth claim, yes — so it is a gate and the doc must not ship the claim. That rule is absent. |
| 3 | Security | **FAIL** | Three security-adjacent rules exist and all three are about accuracy, not about disclosure: `40:105` "Inventing performance or security guarantees without proof", `10:43` traceability, `60:90` verified status codes only. **Nothing anywhere in the skill says a generated document must not contain a secret, a real token, a real internal hostname, a production tenant identifier, or a real user identifier.** Yet `30:48-52` mandates fenced `json` request-body examples and `30:59` mandates "realistic path values and query strings", and `50:88` mandates "a minimal realistic example" of serialized record shapes. This skill instructs an agent to paste realistic payloads into a file that is committed and often published, with no redaction rule. `alaa-security-review` is named nowhere in the skill. | A redaction contract: what an example may contain (placeholder identifiers, documented example hosts) and what it may never contain (real bearer tokens, API keys, `.env` values, production hostnames, real tenant or user identifiers, internal IPs), with the positive replacement for each, and a grep-based checker. Route threat classes to `/alaa-security-review`. |
| 4 | Observability | **DELEGATED, defectively** | `SKILL.md:96-97` names `$alaa-observability-soc` — "Pair when logs, traces, metrics, SOC evidence paths, or operational event naming are in scope" — which is a genuine call site and counts as delegation. But `60-errors-events-observability-contract.md`, the file that actually writes observability documentation rules, contains **zero cross-skill citations** (measured: section 4 below) and states an observability **name** on its own authority at `60:104`. See defect D-6. | Cite `alaa-services-contract references/20-operational-and-observability-contract.md` at `60:104` as the owner of the field names, and `/alaa-observability-soc` as the owner of whether a signal is required, at the point of use rather than only in the SKILL.md routing list. |
| 5 | Concurrency and load | **FAIL** | The only concurrency in scope is the skill's own: parallel subagents. `70:80-85` gives merge rules and forbids concurrent edits to one file, which is correct and is the skill's strongest passage. But nothing bounds the **fan-out** — `70:49` says "start with four" and `70:67` says add a fifth, with no upper bound and no rule about context budget. `alaa-low-noise`, the fleet's owner of context economy, is named nowhere. Nothing addresses documenting the *system's* concurrency: `50` requires a request walkthrough but never requires it to state what happens under concurrent requests to the same record. | Name `/alaa-low-noise` for the fan-out budget. Add to `50` a required subsection: which of the walkthrough's steps are safe under concurrent execution of the same flow, and which store enforces that. |
| 6 | Clean code, SOLID, design patterns | **DELEGATED** | `SKILL.md:88-91` names `$alaa-php-clean-code` and `$alaa-laravel-architecture` with trigger conditions. `20:177-193` asks for a module map and layer boundaries but stops at describing them, correctly leaving the judgement to the owners. | Nothing. This row is satisfied by delegation. Add the `/name` form. |
| 7 | Algorithm and data-structure choice | **DELEGATED, weakly** | `50:55-63` requires a "Key data structures and record shapes" heading; `50:64-81` gives inventory columns. No complexity budget is required and `alaa-algorithms-data-structures` and `alaa-keyset-pagination` are named nowhere — notable because `50` mandates documenting list endpoints' storage without ever requiring the pagination strategy to be documented. | Require the walkthrough to state the access pattern and its index, and route the choice to `/alaa-keyset-pagination` and `/alaa-algorithms-data-structures`. |
| 8 | Configurability | **FAIL** | The skill hardcodes five document paths — `docs/api-summary.md`, `docs/data-architecture.md`, `docs/errors-events-observability.md`, `docs/BIG_PICTURE.md`, `README.md` — in `SKILL.md:49-58` and in all seven contract references. There **is** an escape hatch, stated three times (`SKILL.md:59`, `50:34-37`, `60:35-38`): use a stronger existing doc under another name. That is the right rule. But the repo-local override mechanism is a single line at `SKILL.md:122` ("Use the active repository `AGENTS.md` as a repo-local override") with no statement of which rules `AGENTS.md` may override and which are non-negotiable. | State the override surface explicitly: `AGENTS.md` may rename or relocate any of the five docs and may add required sections; it may not waive the link-validation gate or the traceability rule. |
| 9 | Speed of development and debuggability | **FAIL** | This is the skill's worst structural row. To write one `docs/api-summary.md` an agent is told to read `references/00-topic-map.md` (`SKILL.md:39`), which lists headings rather than routing, then `30-api-summary-contract.md`, and is separately told at `SKILL.md:121` to read `full-guide.md` "when multiple topics overlap heavily" — 53 KB that restates what it just read. The 13-step workflow at `40:56-74` and the 9-step quick start at `SKILL.md:36-45` are two different orderings of the same procedure. An agent that follows the skill literally loads the same rules two to three times. | Retire `full-guide.md`; make `00-topic-map.md` a condition→file router; delete the duplicated navigation list from `SKILL.md`; reconcile the two workflows into one. Measured recoverable: 52,953 bytes plus ~14 lines of body. |
| 10 | Documentation | **SATISFIED** | This is the skill's subject and it is genuinely strong here. `40:76-88` is an 11-item output checklist that names each artifact and requires an explicit "intentionally not needed" rather than silence. `40:90-99` gives nine evidence checks. `20:43-58` is a richness-protection rule that forbids replacing a strong document with a shorter standardized one — a rule most documentation guidance lacks. `50:106-115` and `60:117-126` state quality bars as reader questions, which is a testable form. | Nothing. This row is the skill's asset and must survive Phase 2 intact. |

**Counts: SATISFIED 1 · FAIL 6 · DELEGATED 3** (one of the three delegations, criterion 4, is
defective at its point of use).

---

## 3. Defect-class findings

Only classes actually found are listed.

### D-1 (class 2) — Wrong trigger syntax: 14 `$name`, **zero** `/name`

Exactly the pattern the brief warned about. Every companion citation is Codex-only.

```
SKILL.md:78   `$alaa-postman-collections`      SKILL.md:84   `$alaa-frontend-doc-annotations`
SKILL.md:86   `$alaa-frontend-developer`       SKILL.md:88   `$alaa-php-clean-code`
SKILL.md:90   `$alaa-laravel-architecture`     SKILL.md:92   `$alaa-services-contract`
SKILL.md:94   `$alaa-trust-gateway-auth`       SKILL.md:96   `$alaa-observability-soc`
SKILL.md:98   `$alaa-postman-collections`      80-implementation-gap-backlog.md:45  `$alaa-postman-collections`
90-source-map.md:8  `$alaa-services-contract`, `$alaa-trust-gateway-auth`,
                    `$alaa-observability-soc`, `$alaa-postman-collections`
```

Command that reproduces: `grep -rnoE '(^|[^a-zA-Z0-9_/\`.-])/alaa-[a-z0-9-]+' .` → **zero matches**.

The Codex-only assumption is not merely syntactic. It is baked into rules:
`70-subagent-doc-workflows.md:41` — "explicitly ask **Codex** to spawn the subagents";
`70:42` — "define the work split, whether **Codex** should wait for all results";
`70:104` — "custom agents under `.codex/agents/` or `~/.codex/agents/`";
`SKILL.md:103` — "Use subagents only when the active **Codex surface** supports them".
In Claude Code the mechanism is the Task tool, and an agent reading `70` in Claude Code is told to
do something it cannot do and given no alternative.

### D-2 (class 3) — Duplication: **96.43%** of the split references is verbatim inside `full-guide.md`

Measured, not estimated. Method: strip each reference's `## Includes these full-guide sections`
block, take all non-empty lines, match verbatim against `full-guide.md`'s non-empty lines.

| Reference | Content lines | Verbatim in `full-guide.md` | % |
|---|---:|---:|---:|
| `10-language-and-links.md` | 67 | 58 | 86.6 |
| `20-readme-big-picture-contract.md` | 167 | 159 | 95.2 |
| `30-api-summary-contract.md` | 87 | 85 | 97.7 |
| `40-sync-workflow-and-evidence.md` | 90 | 88 | 97.8 |
| `50-data-architecture-contract.md` | 85 | 84 | 98.8 |
| `60-errors-events-observability-contract.md` | 94 | 93 | 98.9 |
| `70-subagent-doc-workflows.md` | 82 | 81 | 98.8 |
| **Seven combined** | **672** | **648** | **96.43** |
| `00-topic-map.md` | 93 | 0 | 0.0 |
| `80-implementation-gap-backlog.md` | 29 | 0 | 0.0 |
| `90-source-map.md` | 24 | 0 | 0.0 |

Normalising heading depth (`## X` in a reference vs `# X` in the guide) raises the seven-file figure
to **97.92%** and leaves **14** genuinely unique lines, of which 7 are the references' own title
lines and 2 are punctuation variants. **Only five lines of real rule text exist in a numbered
reference and not in `full-guide.md`**, all in one block:

```
20-readme-big-picture-contract.md:21-26
  ### Core rule
  `README.md` is the onboarding and operations entrypoint.
  `docs/BIG_PICTURE.md` is the operational and architecture contract map.
  They must not become duplicates.
  For any service or project where both exist, review both in the same task when behavior, trust,
  API shape, storage shape, deployment expectations, or operating assumptions change.
```

The reverse direction: **95.50%** of `full-guide.md`'s 689 content lines are reproduced by the
numbered references. The 31 lines that are not consist of the file's own title (1), its usage note
(2), its 21-entry table of contents (22), one punctuation variant, and the **six-line condensed
re-statement of `80-implementation-gap-backlog.md` at `full-guide.md:766-777`**.

Hand-sampled rule check, as the brief requires. Twenty-five distinct named rules drawn from all
eleven references, located in both sets:

| # | Rule | Numbered ref | `full-guide.md` |
|---:|---|---|---|
| 1 | Do not patch business logic in a docs-only request | 10:42 | 57 |
| 2 | The user's chat language does not change the documentation language | 10:37 | 52 |
| 3 | POSIX separators only, never Windows backslashes | 10:56 | 71 |
| 4 | Uncertain claim → add the verification path, do not guess | 10:49 | 64 |
| 5 | Summary in the broader doc, full detail in the narrower | 10:80 | 95 |
| 6 | Never use machine-local absolute paths | 10:54 | 69 |
| 7 | Do not copy deep-dive content into README or BIG_PICTURE | 20:74 | 148 |
| 8 | A rewrite that helps one audience and hurts others is incomplete | 20:41 | 117 |
| 9 | Skip api-summary only with no meaningful HTTP surface | 30:41 | 323 |
| 10 | Do not merge these roles together | 30:25 | 307 |
| 11 | Exclude health/readiness/metrics endpoints by default | 30:77 | 359 |
| 12 | Do not turn data-architecture into a second API summary | 50:46 | 427 |
| 13 | One excellent walkthrough over many shallow ones | 50:97 | 478 |
| 14 | Only verified columns, TTLs, lifecycle rules | 50:87 | 468 |
| 15 | Do not invent errors that merely seem likely | 60:92 | 572 |
| 16 | Distinguish synchronous from async dispatch | 60:97 | 577 |
| 17 | Correlation-path diagram when tracing+logging+metrics exist | 60:112 | 592 |
| 18 | Never let two subagents edit one Markdown file concurrently | 70:84 | 674 |
| 19 | Subagents do not edit files by default | 70:78 | 668 |
| 20 | Paired docs must be reviewed together in the same task | 40:47 | 741 |
| 21 | Always document runtime-mode differences explicitly | 40:52 | 746 |
| 22 | Anti-pattern: translating or renaming technical identifiers | 40:106 | 809 |
| 23 | Use `rg` for contract-term evidence checks | 40:91 | 794 |
| 24 | Do not create `remaining-task.md` for ordinary docs polish | 80:14 | **ABSENT** |
| 25 | Never document behaviour from a blog or StackOverflow answer | 90:28 | **ABSENT** |

**23 of 25 sampled rules exist in both places.** The two exceptions are the load-bearing ones: they
prove `full-guide.md` is **not** the complete guide its name promises. It omits `90-source-map.md`
entirely — the whole source-priority, freshness-trigger and community-source-limit contract — and
carries a *shortened, drifted* version of `80`. The drift is already visible:

```
40-sync-workflow-and-evidence.md:73   "...create or refresh `remaining-task.md` using
                                       `references/80-implementation-gap-backlog.md`."
full-guide.md:766                     "...create or refresh `remaining-task.md` using
                                       the implementation-gap rules below."
```

The same step 12 of the same workflow now points at two different rule sets, one of which is a lossy
copy of the other. `full-guide.md:769-777` drops four rules that `80` states: the "do not create it
for ordinary docs polish" negative trigger (`80:14`), the "what not to include" list (`80:36-41`),
the raw-transcript exclusion, and the Postman handoff (`80:43-45`).

**Recommendation: RETIRE `full-guide.md`** to `_to_delete/20260729-batch8/alaa-docs-farsi/`.
The number behind it: 96.43% verbatim overlap forward, 95.50% backward, five lines of unique rule
text, and one already-live divergence. This is far closer to Batch 6's 99.75% retire case than to
Batch 7's 18.3% keep case. Before retiring, move the five-line `### Core rule` block — it already
lives in `20:21-26`, so nothing is lost — and confirm the `80` condensation adds nothing (it
subtracts). Recovers **52,953 bytes, 39.6% of the skill**, deleting no rule.

`SKILL.md:127-128` is the mechanism that produced this and must go with it:
> "Put detailed rules into `references/full-guide.md` instead of growing this file."
> "Keep the split topic references in `references/` aligned with `references/full-guide.md`."

That is an explicit standing instruction to maintain two copies of every rule.

### D-3 (class 3, second instance) — The routing table exists twice

`SKILL.md:109-122` is a 13-entry reference-navigation list. `references/00-topic-map.md` is a
106-line file whose stated job (`00:3`) is "jump directly to the most relevant topic reference
first". Both are routers. `SKILL.md:39` tells the agent to read `00-topic-map.md`, then
`SKILL.md:111` repeats that instruction inside the duplicate router. Under the fleet convention
(≥9 references → separate `00-topic-map.md`) this skill, with 11 references, should have exactly one
of these. It has both, and the one it keeps in the body is the better of the two — `SKILL.md:112-121`
carries trigger conditions ("Read `references/30-…` for `docs/api-summary.md`") whereas
`00-topic-map.md` carries only heading inventories, which is precisely the information made
worthless by retiring `full-guide.md`.

### D-4 (class 5) — Two orderings of the same procedure

`SKILL.md:36-45` (9 steps) and `40-sync-workflow-and-evidence.md:56-74` (13 steps) are the same
workflow at different granularity, and they disagree on order: the body puts subagent split at step 4
(before reading topic references), the reference puts it at step 6 (after verifying behaviour from
code). An agent following both does discovery twice.

### D-5 (class 4) — Project-specific content in a reference, un-scoped

`40-sync-workflow-and-evidence.md:14-22` names seven private repositories — `auth`,
`comment-service`, `gateway`, `ticket`, `vod`, `wa`, `entekhabat-front` — as the provenance of the
standard. `30-api-summary-contract.md:82` instructs: "Model `docs/api-summary.md` after the same
pattern as **the comment-service example**", naming a repository the agent may not have access to,
with no statement of what that example *is*. The rule is unfollowable outside that workspace. This
is not a body-vs-reference misplacement — it is already in a reference — but it fails the wording
test: a competent agent can follow the sentence exactly and be unable to act.

### D-6 (class 11 / criterion 4) — Observability trespass, and the trespassed name is wrong

`60-errors-events-observability-contract.md:104`:
> "- Include correlation and context fields such as **`request-id`**, `traceparent`, tenant
>   identifiers, actor identifiers, event identifiers, or job identifiers only when they are
>   verified."

and the same names again at `20-readme-big-picture-contract.md:160`, `full-guide.md:228`,
`full-guide.md:583`:
> "- Include correlation path covering **`request-id`**, `traceparent`, logs, metrics, tracing, and
>   SOC or monitoring handoff when implemented."

The owner is unambiguous. `alaa-services-contract`'s own description:
> "Route … observability gates and alerts to /alaa-observability-soc"

and `alaa-services-contract references/20-operational-and-observability-contract.md:12-13` lists the
canonical headers as **`X-Request-Id`** and **`traceparent`**, with `:21` "Exact `X-Request-Id`
rules" and `:37` "Exact `traceparent` rules", and `:18` requiring migration off `X-Correlation-Id`.
`alaa-observability-soc`'s description states it owns "what requirement level binds, and which gate
blocks a ship" and routes "exact Alaa metric, event, code, and log-field names to
/alaa-services-contract".

So `alaa-docs-farsi` states an observability **NAME** on its own authority — the thing
`alaa-services-contract` owns — and states it in a casing (`request-id`) that does not match the
contract (`X-Request-Id`). An agent writing a `docs/errors-events-observability.md` from this rule
documents a header the fleet does not emit. This is the sharpest single defect in the skill: not a
missing citation, a **wrong value** introduced by the missing citation.

To be precise about the rest of the file, because the lane brief flagged it as highest-risk:
`60-errors-events-observability-contract.md` states **no observability requirement level and no
gate**. Every "must"/"include at least one" in it binds the *document* (`60:110` "Include at least
one focused diagram for a representative error path"), never the service. On the requirement-level
axis it does not trespass on `alaa-observability-soc`. The trespass is confined to the two name
citations above, and is fixed by one clause each.

### D-7 (class 11) — Eight of eleven references cite no skill at all

Measured across every reference file:

| File | Cross-skill citations |
|---|---|
| `00-topic-map.md` | NONE |
| `10-language-and-links.md` | NONE |
| `20-readme-big-picture-contract.md` | NONE |
| `30-api-summary-contract.md` | NONE |
| `40-sync-workflow-and-evidence.md` | NONE |
| `50-data-architecture-contract.md` | NONE |
| `60-errors-events-observability-contract.md` | NONE |
| `70-subagent-doc-workflows.md` | NONE |
| `full-guide.md` (52,953 bytes) | NONE |
| `80-implementation-gap-backlog.md` | `$alaa-postman-collections` |
| `90-source-map.md` | `$alaa-services-contract`, `$alaa-trust-gateway-auth`, `$alaa-observability-soc`, `$alaa-postman-collections` |

Doctrine-owner coverage across the entire skill, by occurrence count:

```
alaa-project-constitution        0     alaa-reliability-sla       0
alaa-prompting-guide             0     alaa-security-review       0
alaa-low-noise                   0     alaa-testing-strategy      0
alaa-workflow                    0     alaa-system-design         0
alaa-data-layer                  0     alaa-async-messaging       0
alaa-controlled-ops              0     alaa-algorithms-…          0
alaa-services-contract           2     alaa-observability-soc     2
```

Two are structural, not cosmetic. `50-data-architecture-contract.md` is the fleet's instruction for
documenting storage and never names `alaa-data-layer`. `60-errors-events-observability-contract.md`
is the instruction for documenting events and never names `alaa-async-messaging`. In both cases the
skill tells an agent what to write about a domain whose doctrine owner it does not know exists.
`alaa-project-constitution references/quality-bar.md` — which owns the very bar this programme
measures against — appears nowhere.

### D-8 — The name asserts a capability the skill forbids

`SKILL.md:12`:
> "Despite the historical folder name, documentation output is **always** simple, fluent English with
> complete sentences unless the user explicitly asks for another documentation language."

`SKILL.md:63`:
> "Keep documentation in simple, fluent English **regardless of the user message language** unless the
> user explicitly requests another documentation language."

`10-language-and-links.md:36-37` states it a third time. `agents/openai.yaml:2` sets
`display_name: "Alaa Docs Standard"` — the interface layer has already renamed it. Full treatment in
section 4.

### D-9 — Validator warning: body over the 120-line guidance

`skills/scripts/validate_sohrab_skill_pack.py` run against the live tree on 2026-07-29 returns, for
this skill, no errors and exactly one warning:

```
Warnings:
- alaa-docs-farsi: top-level body is 127 lines
```

`SKILL.md` is 130 physical lines; the validator counts 127 after the frontmatter. The description is
737 characters (under the 900 practical ceiling), contains no angle brackets, and `## When NOT to
use` satisfies the `(when not to use|do not use)` heading rule. `agents/openai.yaml`
`short_description` is 51 characters and the `default_prompt` names `$alaa-docs-farsi`. The pack
otherwise passes.

**Classes checked and NOT found:** class 1 (no model name anywhere — `grep -rniE
'gpt-[0-9]|claude-[0-9]|opus|sonnet|haiku|gemini'` → zero); class 6 (the description does carry a
"Do not use it for…" clause at `SKILL.md:3`); class 7 (no `Path(__file__)`, no `tempfile`, no
`mkdtemp`, no writes of any kind — verified by grep and by reading the script in full); class 8 (no
`__pycache__`, no `.pyc`).

---

## 4. Boundary analysis

### 4.1 The Persian question — the fleet believes something the skill denies

The lane brief asked me to establish the legitimate English-artifact exception for the fleet's
Persian-documentation skill. There is no exception, because there is no Persian.

**Measurement.** `grep -rnP '(*UTF)[\x{0600}-\x{06FF}]'` across the staged skill: **zero matches,
exit 1**. The same grep run against the device original at
`.../skills/sohrab/alaa-docs-farsi`: **zero matches, exit 1**. Widening to the Arabic Supplement,
Arabic Extended-A, Presentation Forms blocks and ZWNJ: zero. A byte-level scan
(`LC_ALL=C grep -rnP '[\x80-\xFF]'`) and an independent Python codepoint audit over all 14 files:
**zero non-ASCII characters of any kind**. There is no Persian hit to classify as legitimate or
defective, because there is not one character of Persian in the skill.

The `grep -P` in the brief needs `(*UTF)` on this platform, or it aborts with
`character code point value in \x{} or \o{} is too large` and **exit 2** — a false clean if anyone
reads exit 1 as the only failure. Worth recording for the other lanes.

The skill is not merely Persian-free; it **forbids** Persian output by default, three times
(`SKILL.md:12`, `SKILL.md:63`, `10-language-and-links.md:36`), and its Codex display name has
already been changed to `"Alaa Docs Standard"` (`agents/openai.yaml:2`).

**The fleet disagrees.** `grep -rn 'docs-farsi'` across `skills/sohrab/`, excluding the skill's own
folder, returns 30 call sites. Six of them assert Persian ownership:

```
alaa-frontend-doc-annotations/SKILL.md:13-15
  "Every comment in a file is English and ASCII-range — no Persian text or digits …
   Persian belongs in terminal replies and in Persian-language deliverables,
   which are `/alaa-docs-farsi` (`$alaa-docs-farsi`)."

alaa-frontend-doc-annotations/references/10-annotation-boundaries.md:86
  "| Persian-language deliverables. Never Persian inside a source file
     | `/alaa-docs-farsi` (`$alaa-docs-farsi`) |"

alaa-golang/references/20-sohrab-companions.md:51
  "| `/alaa-docs-farsi` (`$alaa-docs-farsi`)
     | write repository documentation or a human-facing note in Persian |"

alaa-laravel-public-api-contract-pack/SKILL.md:168
  "| The ten-criterion quality bar; Farsi docs and backlog wording
     | `alaa-project-constitution references/quality-bar.md`, `/alaa-docs-farsi` |"

alaa-workflow/references/companion-routing.md:27
  "- Documentation: `alaa-docs-farsi` when the document language or task requires it."

README.fa.md:120
  "| `alaa-docs-farsi` | نگارش مستندات فارسی |"     (= "writing Persian documentation")
```

Two get it right:

```
alaa-php-clean-code/references/00-topic-map.md:74
  "| README, docs, Postman collection, env docs, or a diagram
     | `/alaa-docs-farsi` — output in English unless the user asks otherwise |"

alaa-php-clean-code/SKILL.md:189
  "… the repo-wide docs workflow belongs to `/alaa-docs-farsi`, with output in simple,
   fluent English unless the user asks for another language."
```

The rest route documentation work generically without asserting a language.

**This was seen and entrenched rather than resolved.** `UPGRADE-BATCH-6-ANALYSIS.md:2118` records
the collision check verbatim:
> "**Collision check against `alaa-docs-farsi` (Batch 8):** one live risk … That row invites an agent
> to treat `alaa-docs-farsi` as the README owner and, by association, to write Persian into files. …
> Fix: … narrow the `alaa-docs-farsi` row to Persian-language *deliverables only*."

and `:2045`:
> "On a Persian/RTL repository this is the assertion that mechanically settles the seam with
> `alaa-docs-farsi`: files are English, only terminal replies are Persian."

Batch 6 resolved the seam on the correct axis — *inside a source file* vs *a deliverable* — but on
the wrong assumption about what the deliverable's language is. Because `alaa-docs-farsi` was out of
tree for Batch 6, nobody opened it. The result is a skill that Batch 6 shipped *at standard*
asserting a fact about a skill that contradicts it.

**The consequence is concrete.** An agent in `alaa-frontend-doc-annotations` that hits a Persian
requirement is routed to `/alaa-docs-farsi`, loads it, and reads at line 12 that output is "always
simple, fluent English". It now has two binding instructions in conflict and no tiebreak. Under the
programme's own fail-closed discrimination — *does proceeding without resolution let something
through that must not?* — a document in the wrong language delivered to a Persian-reading operator
during an incident is exactly that.

**The answer to the lane's question, restated correctly:** the artifact-language split this skill
*should* own is not English-instructions vs Persian-output. It is:

| Artifact | Language | Owner |
|---|---|---|
| The skill's own body, references, script, comments | **English, ASCII-range** | this skill (already satisfied, measured) |
| Repository documentation committed to a repo — `README.md`, `docs/*.md`, `remaining-task.md` | **English by default**, another language only on explicit user request (`SKILL.md:12`) | this skill |
| Identifiers inside any document — enum, table, header, route, class, queue, event, payload keys | **Never translated, in any output language** (`10:38-39`) | this skill states the rule; `alaa-services-contract` owns the values |
| A comment inside a source file | **English, ASCII-range, never Persian** | `alaa-frontend-doc-annotations` |
| Terminal replies to the owner | Persian permitted | not this skill |
| A Persian-language deliverable, if one is ever requested | **currently unowned** | see open question 1 |

The last row is the gap. Every skill that routes Persian here is routing into a void.

### 4.2 Boundary against `alaa-frontend-doc-annotations` — written, bidirectional, and wrong on one axis

Both sides name each other, which is more than most pairs in this fleet manage.

From `alaa-frontend-doc-annotations` (quoted at 4.1): `SKILL.md:13-15` and
`references/10-annotation-boundaries.md:86`. Its seam sentence is exact and correct on the axis that
matters:
> "A rule whose violation can be caught by compiling, type-checking or running the code belongs to
> `/alaa-vue-typescript-clean-code`. A rule whose violation is visible only by reading a comment
> against the code it claims to describe — in a diff whose build output must be byte-identical before
> and after — belongs here."

From `alaa-docs-farsi`, `SKILL.md:84-85`:
> "- `$alaa-frontend-doc-annotations`
>    - Pair when the task also touches docblocks and inline code annotations."

and the negative half, `SKILL.md:30`: "pure inline code annotation passes" under "When NOT to use",
restated at `10-language-and-links.md:31`.

**Verdict: the file-boundary is written and reciprocal and correct.** In-code annotations →
`alaa-frontend-doc-annotations`; repository `.md` files → `alaa-docs-farsi`. The predicate is
observable: which file the diff touches. No overlap found on this axis after reading both.

**One asymmetry.** `alaa-frontend-doc-annotations` gives both trigger forms
(`/alaa-docs-farsi` (`$alaa-docs-farsi`)) at every call site; `alaa-docs-farsi` gives only `$name`.
And `alaa-docs-farsi`'s "Pair when" is an invitation, not a boundary — it never states what it does
*not* own to the other skill. The one axis where the pair is genuinely broken is language (4.1), and
the break is on `alaa-frontend-doc-annotations`'s side of the sentence.

### 4.3 Boundary against `alaa-postman-collections` — API documentation is a three-way overlap, and nobody owns the tiebreak

Read from the staged copy at `/home/claude/b8/src/alaa-postman-collections/`.

`alaa-docs-farsi` states its side clearly. `30-api-summary-contract.md:16`:
> "`docs/api-summary.md` is the fast contract sheet for humans and agents who need the endpoint map
> and a few verified request examples **without reading a full Postman collection, OpenAPI document,
> `README.md`, or `docs/BIG_PICTURE.md`**."

and `30:25`: "Do not merge these roles together."

`alaa-postman-collections` states its side, `references/25-public-api-contract-and-sdk-readiness.md:6`:
> "Leave one canonical, machine-readable public API contract and the Postman artifacts synchronized
> to the same verified external behavior."

`:20`: "OpenAPI 3.1 is preferred when the repository has no stronger canonical format."
`:22`: "create the smallest explicit pack at `docs/contracts/<service>/openapi.yaml` … Link it from
an existing API/docs index when one exists; **do not introduce a competing documentation root**."

And `references/44-request-documentation-blocks.md:29-33` claims a third layer:
> "Put a fact at the smallest level where it is true, once: **collection description**: the
> environment contract, the base URL and prefix model, the auth model at the boundary…"
> "A fact stated at two levels drifts."

**Measurement of the gap.** `grep -rn 'api-summary'` across the whole of
`alaa-postman-collections`: **zero matches**. `grep -rn 'openapi\|docs/contracts'` across the whole
of `alaa-docs-farsi`: `OpenAPI` appears four times, always as a thing a reader might otherwise have
to read (`30:16`, `70:56`, `full-guide.md:297,645`), never as an artifact this skill coordinates
with; `docs/contracts` appears **zero** times.

So each skill knows the other exists and neither knows the other's artifact. Run both on one
API-bearing repository and it produces three descriptions of the same endpoints —
`docs/api-summary.md`, `docs/contracts/<service>/openapi.yaml`, and the Postman request
descriptions — under two rules that each forbid the drift the pair creates: `postman
44:33` "A fact stated at two levels drifts", `docs-farsi 10:80` "keep the summary in the broader doc
and the full detail in the narrower doc". Neither rule can be applied, because neither skill knows
the other level exists.

**Proposed boundary, from this side. Flag as needing reciprocal agreement with the
`alaa-postman-collections` lane before either is written.**

| Artifact | Owner | Rule |
|---|---|---|
| `docs/contracts/<service>/openapi.yaml` — the machine-readable contract | `alaa-postman-collections` | Authoritative for request/response schemas, status codes, error shapes. `alaa-docs-farsi` never edits it. |
| The Postman collection, environments, examples, tests, request descriptions | `alaa-postman-collections` | Sole owner. |
| `docs/api-summary.md` — the human endpoint sheet | `alaa-docs-farsi` | **Derived, never authoritative.** When it disagrees with the OpenAPI contract, the contract wins and `api-summary.md` is the defect. |
| Whether `docs/api-summary.md` should exist at all when an OpenAPI contract exists | **unresolved — owner decision** | See open question 3. |
| `remaining-task.md` backlog wording | `alaa-docs-farsi` | Already reciprocal and correct: `postman SKILL.md:82,142` and `postman references/10-scope-and-trigger-rules.md:59` route it here; `docs-farsi 80:43-45` accepts it. This is the pair's one clean seam. |
| README navigation linking to any of the above | `alaa-docs-farsi` | `10:73` "README.md is the navigation hub." |

The precedence rule the pair needs and neither has: **when `docs/api-summary.md` and the canonical
contract disagree, the contract is right.** That is already the fleet's general shape —
`alaa-controlled-ops references/10-source-priority-and-boundaries.md:11` states it for exactly this
case:
> "Generated public artifacts — Postman collections, route inventories, API summaries. When one
> disagrees with rank 1 or 2 the code is correct and the artifact is the defect: fix it through
> `/alaa-postman-collections` ($alaa-postman-collections) or `/alaa-docs-farsi` ($alaa-docs-farsi),
> never your claim."

`alaa-controlled-ops` already legislates the precedence both skills lack. Neither cites it.

### 4.4 Are the six `*-contract.md` files contracts?

A contract is a checkable predicate about a produced document. A style guide is a preference about
how it reads. Measured by preference-verb density (`should|prefer|may|consider|typically|ideally|
recommended|usually|where practical`) against hard-constraint density (`must|never|do not|always|
required|exactly|only when`) over rule lines:

| File | Rule lines | Preference verb | Hard constraint | Verdict |
|---|---:|---:|---:|---|
| `20-readme-big-picture-contract.md` | 165 | 14 (8.5%) | 20 (12.1%) | **Mixed** |
| `30-api-summary-contract.md` | 86 | 8 (9.3%) | 8 (9.3%) | **Mixed** |
| `50-data-architecture-contract.md` | 84 | 5 (6.0%) | 5 (6.0%) | **Contract** |
| `60-errors-events-observability-contract.md` | 93 | 8 (8.6%) | 8 (8.6%) | **Contract** |

Reading rather than counting, the answer is more useful than the ratio, and it is the same for all
four: **each file is a genuine contract in its structural half and a style guide in its quality-bar
half.**

- **The contract half is real and checkable.** `20:76-93` and `20:110-133` are numbered required
  section lists. `30:43-53` is a six-item required structure. `50:48-63` and `60:49-63` are
  twelve-heading structures given as ordered lists of literal heading strings. A script can assert
  every one of these against a produced `.md` file — presence, spelling, order. `50:64-81` and
  `60:65-84` give required table columns, equally checkable. These are contracts by the strict
  definition and none of them currently has a checker.

- **The quality-bar half is a style guide wearing the word.** `20:96-108` ("`README.md` should be
  concise, but not shallow"), `30:104-114` ("It should not read like generated sludge"),
  `50:106-115` ("The doc should make the system feel inspectable, not mysterious"),
  `60:117-126` ("The doc should make failures and side effects understandable and debuggable"). Each
  is a list of reader questions followed by an aesthetic verdict. The reader questions are the
  salvageable part — "Which cache keys or derived records exist, and how are they invalidated?"
  (`50:110`) is a testable coverage requirement if restated as one. The aesthetic verdicts fail the
  wording test outright: no agent can determine whether a document "feels inspectable", and none can
  be told it violated the rule.

Specifically on `60`, the highest-risk file: it is a contract about the document and **states no
observability requirement level and no gate** — every obligation in it binds the `.md` file, not the
service. Its only trespass is the two name citations in D-6. On the axis the brief was worried
about, it is clean.

`20-readme-big-picture-contract.md` is the weakest of the four. Two of its sections are not contracts
at all: `20:177-193` ("Architectural patterns section") and `20:207-220` ("New-service baseline
extraction") are checklists of topics to cover with no observable completion condition, and
`20:150-175` mixes a hard requirement (`20:152` "must include diagrams for all major behavioral
families") with five diagram-aesthetics bullets.

### 4.5 `references/80-implementation-gap-backlog.md` — the lane premise is wrong; it is instruction, not state

The lane brief characterised this file as "a backlog inside a skill … state, not instruction". I read
it in full. It contains **no backlog items**. It is 2,041 bytes of rules for producing a
`remaining-task.md` in a *target repository*:

- `80:5-14` when to create or refresh one, including the negative trigger `80:14` "Do not create it
  for ordinary docs polish when no implementation gap was found";
- `80:16-23` the evidence standard — "Each item must cite both sides": the doc or Postman request
  that promises the behaviour, and the source-code evidence that it is absent, stubbed, fail-closed
  or incomplete;
- `80:25-34` the required shape — group by area, number each task, state whether the gap affects docs
  only, Postman, public API, storage, jobs, events or operations;
- `80:36-41` exclusions — no raw transcripts, no invented routes, no broad "improve docs" tasks, no
  machine-local absolute paths;
- `80:43-45` the Postman handoff, which is the reciprocal half of `alaa-postman-collections
  SKILL.md:142` and `references/10-scope-and-trigger-rules.md:59`.

Every line is a general rule applicable to any repository. There is no project state in it, no task
list, no dated entry, no repo name.

**Recommendation: KEEP it in `references/`, unchanged in substance.** It is the second-densest
hard-constraint file in the skill (26.1% hard-constraint lines, the highest of all eleven) and one of
only two that cites a companion skill. It is also the *anchor* of the pair's one clean seam with
`alaa-postman-collections` — deleting or relocating it would break an inbound pointer that another
Batch 8 skill depends on. What must change is small: retire its lossy twin at `full-guide.md:769-777`
along with the rest of that file, and add the `/name` form to `$alaa-postman-collections` at `80:45`.

If the owner ever *does* accumulate real backlog state, that state belongs in the target repository's
own `remaining-task.md` — which is exactly what this reference already instructs.

---

## 5. Version and factual currency

Every external claim the skill makes, checked today, 2026-07-29.

**First, what the skill does *not* claim.** `grep -rnoE '\b(v?[0-9]+\.[0-9]+(\.[0-9]+)?)\b'` across
all 14 files returns **zero version numbers**. The skill names no Markdown linter — no
`markdownlint`, no `remark`, no `prettier`, no `vale` (grepped, zero hits). Its only tool dependency
is `python3` (`scripts/check_markdown_links.py:1`, stdlib only, `from __future__ import annotations`
so it runs on 3.7+; verified running on 3.11 in-container and 3.10.12 on the device). This means
there is **nothing stale** — and also **nothing pinned**, which is a D10 gap: the skill states no
version and therefore ships no re-derivation command.

| Claim | Status | Checked against | Re-derivation |
|---|---|---|---|
| `https://spec.commonmark.org/` resolves and is the CommonMark source | **VERIFIED** | Page served 2026-07-29; latest spec **0.31.2, 2024-01-28** | `curl -sSI https://spec.commonmark.org/` |
| `https://docs.github.com/get-started/writing-on-github` resolves | **VERIFIED** | HTTP 200, no redirect, title "Writing on GitHub - GitHub Docs" | fetch the URL |
| `https://docs.gitlab.com/user/markdown/` resolves | **VERIFIED** | Title "GitLab Flavored Markdown (GLFM) \| GitLab Docs" | fetch the URL |
| `https://mermaid.js.org/` resolves | **VERIFIED** | Current Mermaid **11.16.0** shown on the page | fetch the URL, or `npm view mermaid version` |
| `flowchart LR` / `flowchart TD` / `sequenceDiagram` are valid Mermaid types (`20:166-168`, `50:100-101`, `60:113`) | **VERIFIED** | All three current in Mermaid 11.x | `npm view mermaid version` + mermaid.js.org syntax index |
| `https://spec.openapis.org/oas/latest.html` resolves | **VERIFIED** | Now serves **OpenAPI 3.2.0, released 2025-09-19** | fetch the URL |
| `https://learning.postman.com/docs/` resolves | **VERIFIED** | Title "Get started in Postman \| Postman Docs"; canonical `…/docs/getting-started/overview`. The page now advertises a machine-readable index at `/llms.txt` | fetch the URL |
| Postman Collection v2.1 is the current schema (implicit; the skill never states it — `alaa-postman-collections` does) | **NOT CLAIMED HERE** | out of this lane's scope; flagged to the postman lane | — |
| CommonMark/GFM anchor-slug algorithm implemented in `slugify_heading` (`scripts/check_markdown_links.py:32-38`) matches GitHub | **PARTIALLY VERIFIED / STALE** | Duplicate-heading numbering (`#setup`, `#setup-1`) matches GitHub and was confirmed by execution. **Non-ASCII headings do not**: `re.sub(r"[^a-z0-9_\-\s]", "", text)` strips all Persian, so a Persian heading slugs to the empty string. GitHub preserves Unicode letters in anchors. Confirmed by execution — see 6.4. | run the script against a file with a Persian heading |

**Cross-lane note.** `alaa-postman-collections references/25-public-api-contract-and-sdk-readiness.md:20`
states "OpenAPI 3.1 is preferred". `spec.openapis.org/oas/latest.html` served **3.2.0 (2025-09-19)**
today. That is that lane's finding, recorded here because I verified it while checking this skill's
URL list.

**No claim in `alaa-docs-farsi` was found STALE. No claim was UNVERIFIABLE.** All six URLs resolve.

---

## 6. Executable-check inventory

One script: `scripts/check_markdown_links.py`, 207 lines, Python 3 stdlib only
(`argparse`, `re`, `sys`, `dataclasses`, `pathlib`, `typing`). Read in full.

**What it asserts.** For every Markdown-syntax link `[text](target)` and every resolved
reference-style link, outside fenced ``` blocks: no `file://` scheme (`:137`); external schemes
skipped (`:139`); no Windows-drive or `/`-rooted absolute path (`:141`); no backslash (`:143`); the
target resolves inside the repo root (`:148-151`); the target file exists (`:153`); and if an anchor
is present, the target is `.md` (`:157`) and the anchor matches a real heading slug with GitHub-style
duplicate numbering (`:159-161`). These are exactly the rules stated in
`10-language-and-links.md:52-70` — the script is a genuine executable checker for its own skill's
link contract, which puts it ahead of most of the fleet.

### 6.1 Observed run against the whole staged tree — verbatim

```
$ cd /tmp && python3 /home/claude/b8/src/alaa-docs-farsi/scripts/check_markdown_links.py /home/claude/b8/src/
EXIT=0
STDOUT:
Validated Markdown links successfully for: AGENTS.md, UPGRADE-CARRYOVER.md,
alaa-basic-memory-os/SKILL.md, alaa-basic-memory-os/references/cli-and-mcp.md,
… [66 files, full list omitted for length] …
vector-rust-observability-pipelines/references/VRL_GUIDE.md
STDERR: (empty)
```

66 Markdown files, exit **0**, 0.074 s wall clock.

### 6.2 Observed run against the real device tree — verbatim

```
$ cd /tmp && python3 .../skills/sohrab/alaa-docs-farsi/scripts/check_markdown_links.py \
      .../skills/sohrab
EXIT=1
STDOUT:
alaa-golang/references/45-failure-behavior-at-the-call-site.md:127: target file does not exist: r
alaa-golang/references/45-failure-behavior-at-the-call-site.md:131: target file does not exist: r
alaa-golang/references/45-failure-behavior-at-the-call-site.md:144: target file does not exist: r, httpkit.AllowUnknownFields(
STDERR:
Found 3 Markdown link issue(s).
```

814 Markdown files scanned. **All three findings are false positives.** The source lines are Go
generic call syntax inside single-backtick inline code spans, which `INLINE_LINK_RE` matches as
`[T](r)`:

```
alaa-golang/references/45-failure-behavior-at-the-call-site.md:127
  …and `httpkit.Bind[T](r)` requires the JSON content type,
alaa-golang/references/45-failure-behavior-at-the-call-site.md:131
  **Rule:** in a kit service, decode with `httpkit.Bind[T](r)` and return its error unchanged…
alaa-golang/references/45-failure-behavior-at-the-call-site.md:144
  **Rule:** `httpkit.BindWith[T](r, httpkit.AllowUnknownFields())` is the only sanctioned way…
```

A CI gate built on this script is permanently red on a correct repository. Corroboration: run against
the directory holding **this analysis file**, the same bug produces four more false positives
(`EXIT=1`), every one of them a link-shaped token inside a backtick span quoted from the source under
review. The false-positive rate on prose that discusses code or links is not marginal.

Running against the repository root `skills/` (which adds 1,614 vendored Markdown files) **exceeded
300 s** on the device mount and was abandoned; the same 66-file staged run in-container takes 0.074 s.
The mount, not the script, is the bottleneck — but any tree-wide gate must exclude `vendor/`.

### 6.3 Exit-code contract

| Condition | Observed exit | Correct? |
|---|---:|---|
| Clean tree | 0 | yes |
| Link issues found | 1 | yes |
| `repo_root` does not exist | 2 | yes (`:175-177`) |
| `repo_root` is a file, not a directory | 2 | yes |
| `--files` names a missing file | 2 | yes (`:180-184`) |
| **A Markdown file cannot be decoded as UTF-8** | **1** | **NO** |

The last row is a real breach of the programme's defining rule. Observed verbatim:

```
$ python3 check_markdown_links.py t1        # t1 contains one UTF-16-ish .md file
EXIT=1
Traceback (most recent call last):
  File ".../check_markdown_links.py", line 206, in <module>
    raise SystemExit(main(sys.argv[1:]))
  File ".../check_markdown_links.py", line 191, in main
    for line_no, target in extract_targets(path)
  File ".../check_markdown_links.py", line 64, in read_lines
    return path.read_text(encoding="utf-8").splitlines()
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 2: invalid start byte
```

`read_text` at `:64` is unguarded, and Python's uncaught-exception exit status is 1. On Windows the
same path is reached by a `PermissionError` on a file held open by an editor or by OneDrive. "Could
not run" is reported as "found a problem", and a harness that maps 1→fail and 2→blocked records the
wrong one. Every call to `read_lines` — `:71`, `:106` — needs a guard that returns exit 2.

### 6.4 Correctness matrix, all observed by execution

| Behaviour | Result |
|---|---|
| Rejects `docs\x.md` — "use POSIX-style forward slashes in links" | correct |
| Rejects `D:/repo/x.md` and `C:\repo\x.md` | **BOTH silently accepted, exit 0** — see below |
| Rejects `/etc/passwd` | correct |
| Rejects `file:///D:/x` | correct |
| Rejects `../outside.md` — resolves outside root | correct |
| Resolves cross-skill relative links `../../skB/references/x.md` | correct, verified by fixture |
| Same-file anchors `#heading` | correct |
| Cross-file anchors `./x.md#heading` | correct |
| Duplicate-heading numbering `#setup`, `#setup-1` | correct, matches GitHub; `#setup-2` correctly flagged |
| **Inline code spans** — `` `Bind[T](r)` `` | **false positive**, 3 live instances |
| **`~~~` fences** | **false positive** — only ``` is recognised (`:72`, `:93`, `:111`) |
| **Indented (4-space) code blocks** | **false positive** |
| **Setext headings** (`Title` / `=====`) | **false negative** — `HEADING_RE` is ATX-only, so `#title` is reported missing |
| **Explicit HTML anchors** `<a id="custom">` | **false negative** — `#custom` reported missing |
| **Non-ASCII headings** | **false negative** — `slugify_heading` `:35` strips all non-`[a-z0-9_\-\s]`, so a Persian heading slugs to empty and every Persian anchor is reported missing. The repo ships `skills/sohrab/README.fa.md` and `alaa-codex-orchestrator/README-fa.md`. |

**The drive-letter bypass, in detail — the sharpest script defect.** `WINDOWS_ABS_RE` at `:17`
(`^[A-Za-z]:[\/]`) is **dead code**. `validate_target` calls `is_external(target)` at `:139` and
returns clean before ever reaching the `WINDOWS_ABS_RE` test at `:141`, because `SCHEME_RE`
(`^[a-zA-Z][a-zA-Z0-9+.-]*:`, `:18`) matches `D:` as a URI scheme. The backslash test at `:143` is
unreachable for the same reason. Observed:

```
$ printf '# T\n[b](D:/repo/x.md)\n[c](C:\\repo\\x.md)\n' > a.md
$ python3 check_markdown_links.py .
Validated Markdown links successfully for: a.md
EXIT=0
```

These are, verbatim, the two forms this skill's own contract gives as its canonical failures:

```
10-language-and-links.md:68-69
  - `model.fga -> D:/repo/platform/openfga/model.fga`
  - `model.fga -> C:epo\platform\openfga\model.fga`
```

The skill ships a checker that passes its own documented counter-examples clean. Fix: test
`WINDOWS_ABS_RE` **before** `is_external`, and exclude single-letter schemes from `SCHEME_RE`.

**Defect class 7: absent.** No `Path(__file__)`, no `parents[N]`, no `tempfile`, no `mkdtemp`, no
`TemporaryDirectory` — grepped, zero hits. The script takes its root from `argv` and never writes
anything, anywhere. It creates no temp directory inside or outside the repository.

**Windows PowerShell: would run.** Pure `pathlib` + `argparse`, no `subprocess`, no shell, no `os.sep`
assumption, explicit `encoding="utf-8"` on every read (so no cp1252 default-encoding trap),
`splitlines()` handles CRLF. Invocation `python scripts\check_markdown_links.py <root>` works. Two
Windows caveats: the `PermissionError` → exit 1 path in 6.3, and `Path.resolve()` case-folding could
in principle make `relative_to(root)` at `:29` raise on a substituted drive — not reproducible here.

### 6.5 The central question: can this be the batch's tree-wide link checker?

**No, not as written — and the gap is not the false positives. It is the shape of the deliverable.**

`UPGRADE-CARRYOVER.md:198` specifies:
> "Plus the repository-level cleanup in section 6, and **a link check that every cross-skill path in
> `skills/sohrab/` resolves**."

and `:149`:
> "Before renaming or restructuring a reference file, grep `skills/sohrab/` for inbound pointers to
> it … **Batch 8 runs a link check over the whole tree at the end as the backstop.**"

Cross-skill paths in this fleet are almost never written as Markdown links. The convention the brief
states — `` `alaa-services-contract references/22-…` `` — is **inline code**. Measured across
`skills/sohrab/` (814 `.md` files, `vendor/` excluded):

| Path-assertion form | Occurrences | Seen by `check_markdown_links.py`? |
|---|---:|---|
| Markdown links to `.md` targets — `[text](x.md)` | **24** | **yes** |
| Inline-code same-skill reference paths — `` `references/NN-x.md` `` | 2,501 | no |
| Inline-code cross-skill paths — `` `alaa-xxx references/NN-x.md` `` | 163 | no |
| Inline-code script paths — `` `scripts/x.py` `` | 324 | no |

The script validates **24 of roughly 3,012 path assertions — about 0.8%**, and **none** of the 163
cross-skill citations the carryover deliverable names. Its whole coverage of the deliverable is zero.

To prove the deliverable is worth doing, I ran a throwaway inline-code resolver against the live tree
(read-only, written to `/tmp` on the device, nothing in the repo touched):

```
cross-skill inline paths scanned: 182, unresolved: 2
  UPGRADE-BATCH-6-ANALYSIS.md -> alaa-frontend-developer  references/25-modern-css-and-motion.md
  UPGRADE-BATCH-6-ANALYSIS.md -> alaa-ui-ux-design-system references/70-motion-and-modern-css.md
same-skill inline paths scanned: 2,911, unresolved: 582, across 223 files
```

The 582 are the real prize. Spot-checking them, the dominant class is not a broken link — it is a
**bare cross-skill path**, the exact convention violation the lane brief names ("never a bare
`references/…`"):

```
alaa-data-layer/references/40-redis-verification-and-anti-patterns.md
   cites bare `references/22-failure-load-and-deprecation-contract.md`  → owned by alaa-services-contract
   cites bare `references/24-metric-registry.md`                        → owned by alaa-services-contract
   cites bare `references/40-proof-strength.md`                         → owned elsewhere
alaa-bash-shell/SKILL.md
   cites bare `references/50-effort-and-thinking.md`                    → owned by alaa-prompting-guide
alaa-data-layer/SKILL.md, alaa-crockford-base32-codecs/SKILL.md
   cite bare `references/quality-bar.md`                                → owned by alaa-project-constitution
```

Each of these reads, to an agent inside the citing skill, as a pointer to a file in **its own**
`references/` directory that does not exist. That is a silent routing failure at 582 sites, and no
tool in the fleet reports it.

The classification was spot-verified by resolving each sampled bare path against every skill root —
all seven sampled paths exist in exactly one other skill, so none of them is dangling; every one is a
missing owner prefix:

```
`references/22-failure-load-and-deprecation-contract.md`  -> alaa-services-contract     EXISTS
`references/24-metric-registry.md`                        -> alaa-services-contract     EXISTS
`references/quality-bar.md`                               -> alaa-project-constitution  EXISTS
`references/50-effort-and-thinking.md`                    -> alaa-prompting-guide       EXISTS
`references/20-retries.md`                                -> alaa-reliability-sla       EXISTS
`references/60-idempotency.md`                            -> alaa-reliability-sla       EXISTS
`references/40-proof-strength.md`                         -> alaa-testing-strategy      EXISTS
```

The last one is the case that proves the checker is needed rather than a convention reminder:
`alaa-data-layer` and `alaa-controlled-ops` both cite `` `references/40-proof-strength.md` `` bare,
and the file belongs to **`alaa-testing-strategy`** — not to `alaa-reliability-sla`, which is the
skill a reader would guess from the surrounding retry and degradation citations. A bare path is not
merely unhelpful; it is unresolvable by inference.

The full 582-item classification pass exceeded 300 s against the device mount and was abandoned; the
sampled verification above stands in its place, and reproducing the complete split is Phase 2's
first-run baseline for `check_skill_xrefs.py`.

**Decision. Phase 2 must write a second checker.** `check_markdown_links.py` should be kept, fixed,
and kept in its lane — it is a correct Markdown-link validator and it enforces this skill's own link
contract. It should not be stretched to cover inline-code path citations, because that is a different
grammar with a different resolution rule (relative to the *skill root*, not the file's directory) and
a different finding class (bare-cross-skill vs dangling).

**What the new checker must gain over `check_markdown_links.py`, exactly:**

1. Recognise the inline-code path grammar: `` `<skill-name> <relative-path>` `` and bare
   `` `references|scripts|assets|agents/<file>` ``.
2. Resolve bare paths against the **citing skill's own root**, and classify each failure into
   **DANGLING** (the file exists nowhere in the tree) vs **BARE-CROSS-SKILL** (it exists in exactly
   one other skill, and the citation omits the owner). These need different fixes and must not be
   reported as one number.
3. Exclude `vendor/` and `_to_delete/` by default, with a flag to include them. Without this the run
   exceeds 300 s on the device mount and reports retired files.
4. Honour 0/1/2 **including** the unreadable-file path that `check_markdown_links.py` gets wrong.
5. Emit `path:line: CLASS message` so findings are greppable and diffable between runs.

**And what `check_markdown_links.py` itself must gain in Phase 2**, independent of the above:

1. Guard `read_lines` (`:63-64`) and return **2** on `UnicodeDecodeError`, `PermissionError`, `OSError`.
2. Strip inline code spans before matching links — removes the three live false positives.
3. Recognise `~~~` fences and 4-space indented blocks.
4. Collect setext headings and explicit `<a id="…">`/`{#…}` anchors.
5. Preserve non-ASCII letters in `slugify_heading` so Persian anchors resolve.
6. Check `WINDOWS_ABS_RE` **before** `is_external`, so `D:/repo/x.md` is caught — `10:69` forbids it
   and the checker currently lets it through.
7. Default-exclude `vendor/` and `_to_delete/`.
8. A self-test with fixtures for each of the above, whose target-exit-2 case records **BLOCKED**.

---

## 7. The Phase 2 work order

Target: **≤ 78,000 bytes** (from 133,756, a 42% reduction) with **no rule deleted**, plus two
genuinely new capabilities that earn a small part of it back — a doc-contract checker and a
redaction rule.

### 7.1 Retire

| File | Bytes | To | Why |
|---|---:|---|---|
| `references/full-guide.md` | 52,953 | `_to_delete/20260729-batch8/alaa-docs-farsi/` | 96.43% verbatim duplicate forward, 95.50% backward, 5 unique rule lines (already present at `20:21-26`), and one live divergence from `80`. Before moving: confirm `20:21-26` is intact, and confirm nothing outside the skill points at it (`grep -rn 'full-guide' skills/sohrab/`). |

Nothing else is retired. `00-topic-map.md` is rewritten, not retired.

### 7.2 Rewrite

**`SKILL.md`** — target ≤ 105 lines (from 130; clears the 120-line validator warning).
- Rename the concept in the body: state once, in the first line under the heading, that this skill
  produces **English** repository documentation and that the folder name is historical. Keep
  `agents/openai.yaml`'s `display_name: "Alaa Docs Standard"`.
- Add both trigger forms at all 9 companion call sites: `/alaa-x` (`$alaa-x`).
- Delete the duplicate reference-navigation list at `:109-122`; keep its trigger conditions by moving
  them into the rewritten `00-topic-map.md`.
- Delete `:127-128` (the "put detailed rules into `full-guide.md`" and "keep the split references
  aligned with `full-guide.md`" maintenance rules) — they legislate the duplication.
- Reconcile the 9-step quick start with `40:56-74`: keep the body's version as a 5-step orientation,
  keep the 13-step production workflow in `40` alone, and make the body point at it once.
- Add a "Ground this skill does not own" block naming, with both trigger forms: observability names →
  `alaa-services-contract references/20-operational-and-observability-contract.md`; observability
  requirement levels and gates → `/alaa-observability-soc`; storage doctrine → `/alaa-data-layer`;
  event doctrine → `/alaa-async-messaging`; threat classes and redaction verdicts →
  `/alaa-security-review`; the quality bar → `alaa-project-constitution references/quality-bar.md`;
  model and effort → `/alaa-prompting-guide`; context and fan-out budget → `/alaa-low-noise`;
  the Postman collection, its request descriptions and the OpenAPI contract →
  `/alaa-postman-collections`.
- Replace the Codex-only subagent paragraph at `:101-107` with runtime-neutral wording, pointing to
  the rewritten `70`.

**`references/00-topic-map.md`** — rewrite from a heading inventory into a condition→file router.
Two columns: "Condition" and "File". Ten rows, one per numbered reference, each condition an
observable trigger. Drop every heading list (they existed to index `full-guide.md`). Target ≤ 1,600
bytes, from 3,902.

**`references/60-errors-events-observability-contract.md`** — fix D-6 at `:104`, and only that plus
citations:
> "- Include correlation and context fields **only when verified in the repository. The canonical
>   names are owned by `alaa-services-contract references/20-operational-and-observability-contract.md`
>   — use `X-Request-Id` and `traceparent` exactly as that file spells them, never a local variant.
>   Whether a given signal is required at all is `/alaa-observability-soc`'s, not this skill's.**"

Same fix at `20-readme-big-picture-contract.md:160`. Cite `/alaa-async-messaging` once in the event
inventory rules at `:94`.

**`references/50-data-architecture-contract.md`** — cite `/alaa-data-layer` once in the storage
coverage rules at `:82`; cite `/alaa-keyset-pagination` once in the request-walkthrough rules at
`:90` for list-flow access patterns. Add one required subsection to the 12-heading structure:
concurrency behaviour of the walked-through flow.

**`references/30-api-summary-contract.md`** — add the precedence rule agreed with the postman lane
(4.3): `docs/api-summary.md` is derived; when it disagrees with the canonical contract, the contract
wins. Cite `/alaa-postman-collections` and
`alaa-controlled-ops references/10-source-priority-and-boundaries.md`. Replace `:82`'s
"the comment-service example" with the pattern itself, so the rule is followable outside that
workspace.

**`references/40-sync-workflow-and-evidence.md`** — at `:14-22` scope the seven repository names as
provenance, not as a lookup an agent is expected to reach. At `:73` the pointer to `80` is already
correct; leave it.

**`references/70-subagent-doc-workflows.md`** — de-Codex it. Replace "explicitly ask Codex to spawn"
(`:41`), "whether Codex should wait" (`:42`) and `.codex/agents/` (`:104`) with runtime-neutral
wording that names the Claude Code mechanism and the Codex mechanism side by side. Add a fan-out
bound citing `/alaa-low-noise`. Add the missing failure rule: what to do when a subagent returns
nothing or fails.

**`references/80-implementation-gap-backlog.md`** — one edit: both trigger forms at `:45`.

**`references/90-source-map.md`** — both trigger forms at `:8`; add a re-derivation command beside
each of the six URLs (D10); add the Postman `/llms.txt` index discovered today.

**`references/10-language-and-links.md`** — becomes the language authority. State the artifact-language
table from 4.1 here, in full, including the row that says a Persian deliverable is **not** this
skill's output and naming whatever the owner decides on open question 1. Delete the duplicated
`## Purpose` / `## When to use` / `## When NOT to use` block at `:14-33` (a third copy of `SKILL.md`).

**`references/20-readme-big-picture-contract.md`** — split the contract half from the style half.
Keep `:76-93` and `:110-133` (the required section lists) as hard requirements. Convert the four
quality-bar sections' reader questions into coverage requirements and delete the aesthetic verdicts.

**`scripts/check_markdown_links.py`** — the eight fixes in 6.5.

### 7.3 Create

| New file | Contents | Est. bytes |
|---|---|---:|
| `scripts/check_doc_contract.py` | Given a repo root, asserts the required-heading lists from `20:76-93`, `20:110-133`, `30:43-53`, `50:48-63`, `60:49-63` against whichever of the five docs exist; asserts every fenced `json` block parses; asserts every `See also` target resolves; asserts no example contains a bearer token, an API key, a `.env` value, a private IP, or an absolute local path. Prints `path:line: RULE message`. Exit 0/1/2. Ships a self-test whose exit-2 fixture records BLOCKED. | ~9,000 |
| `scripts/check_skill_xrefs.py` | **The batch deliverable.** The five capabilities in 6.5. Runs over `skills/sohrab/` in seconds with `vendor/` and `_to_delete/` excluded. Known first-run findings to reproduce: 2 dangling named cross-skill paths, 582 bare same-skill-shaped paths across 223 files. | ~7,500 |
| `references/15-security-and-redaction.md` | The rule missing at criterion 3: what a committed example may and may not contain, with a positive replacement for each prohibition; route verdicts to `/alaa-security-review`. | ~2,500 |
| `references/45-failure-classes.md` | The rule set missing at criterion 2: symptom → diagnosis → smallest retry → escalation for absent `AGENTS.md`, absent Python, contradictory sources, failed subagent, doc contradicting code; plus the fail-closed discrimination for an unverifiable security or auth claim. | ~3,000 |

`check_skill_xrefs.py` is arguably repository-level rather than skill-level. If the owner prefers, it
belongs at `skills/scripts/` beside `validate_sohrab_skill_pack.py` rather than inside this skill —
see open question 4.

### 7.4 Byte budget

```
current                                          133,756
  − full-guide.md retired                        −52,953
  − 00-topic-map.md rewritten as a router         −2,300
  − SKILL.md duplicate router + maintenance rules −1,200
  − 10-language-and-links.md duplicated block     −1,100
  − 20-*.md aesthetic verdicts                      −800
                                        subtotal   75,403
  + references/15-security-and-redaction.md       +2,500
  + references/45-failure-classes.md              +3,000
  + boundary/citation edits across 8 references   +2,000
  + check_markdown_links.py fixes                 +2,500
                                        subtotal   85,403
  + scripts/check_doc_contract.py                 +9,000
  + scripts/check_skill_xrefs.py                  +7,500   (or 0, if hosted at skills/scripts/)
                                           total  101,903   (94,403 if xrefs moves out)
```

Larger than 78,000, and the growth is entirely two new executable checkers and two new rule sets that
close criteria 2 and 3. Per the definition of done, the capability that earns the growth, named:
**the skill gains its first checker for its own document contract, the fleet gains its first checker
for cross-skill path citations, and the skill gains failure-behaviour and redaction rules it has
never had.** Prose alone falls from 126,643 to ~85,400 bytes — a 33% reduction with no rule deleted.

---

## 8. Open questions for the owner

**1. Who owns Persian-language deliverables?** *(The decision this lane exists to surface.)*
Six call sites across the fleet, two of them in a Batch-6 at-standard skill, route Persian
deliverables to `alaa-docs-farsi`. `alaa-docs-farsi` mandates English three times. One of the two
statements is wrong and only the owner can say which.
- **Option A (recommended): the skill is right, the fleet is wrong.** Keep the English default,
  rename the skill's *concept* to "Alaa Docs Standard" (already its Codex display name), and correct
  the six call sites to say "repository documentation, output in English unless the user asks
  otherwise" — the wording `alaa-php-clean-code` already uses correctly at `SKILL.md:189` and
  `references/00-topic-map.md:74`. *Trade-off:* touches five skills outside Batch 8, three of which
  are already at standard. It also leaves Persian deliverables genuinely unowned — which is honest,
  and is better than a routing target that refuses the job.
- **Option B: the fleet is right.** Give this skill a real Persian mode: an explicit trigger, a rule
  for which artifacts may be Persian (prose only, never identifiers — `10:38` already says so), a
  bidi/ZWNJ rule, and an anchor-slug rule for Persian headings that the link checker can enforce.
  *Trade-off:* materially grows the skill and adds a capability the owner may not want.
- **Option C: rename the folder.** Cleanest conceptually, most disruptive: 30 inbound call sites plus
  `README.md:44,187`, `README.fa.md:120` and `alaa-cc-orchestrator/agents/alaa-documenter.md:7,17`.
  Under the never-delete rule the old folder would move to `_to_delete/`, breaking any external
  installation that pins the path. **Not recommended in this batch.**

My recommendation is **A**, executed as: fix the skill's own wording and the two Batch-8-adjacent
call sites now, and list the four out-of-batch call sites as a carry-over rather than editing skills
this batch does not own.

**2. Retire `full-guide.md`?** Recommend **yes**, on 96.43% forward / 95.50% backward overlap with
five unique rule lines that already exist elsewhere. *Trade-off:* an agent that genuinely wants every
rule in one buffer loses that option — but `full-guide.md` never was that file, since it omits
`90-source-map.md` entirely and carries a lossy copy of `80`. Keeping it means maintaining two
diverging copies of 96% of the skill, which `SKILL.md:128` currently *instructs* an agent to do.

**3. Should `docs/api-summary.md` exist when the repo has an OpenAPI contract?** Both artifacts
describe the same endpoints and neither skill knows the other's exists (measured: zero cross-mentions
in both directions). Recommend **yes, keep both, with an explicit precedence rule** — the OpenAPI
contract is authoritative and `api-summary.md` is a derived human sheet that loses on disagreement,
which is what `alaa-controlled-ops references/10-source-priority-and-boundaries.md:11` already says.
*Trade-off:* two artifacts to keep in sync. The alternative — deleting `api-summary.md` in favour of
generated OpenAPI docs — is cheaper to maintain but loses the "readable in thirty seconds" property
that `30:16` is explicitly built for. **This needs reciprocal agreement with the
`alaa-postman-collections` lane before either skill is written.**

**4. Where should `check_skill_xrefs.py` live?** It validates the whole tree, not this skill.
Recommend `skills/scripts/`, beside `validate_sohrab_skill_pack.py`, so the repository validator can
call it and it is not shipped to every consumer of `alaa-docs-farsi`. *Trade-off:* this skill then
ships one checker instead of two, and the "every skill ships an executable check" survey counts it
against the repository rather than the skill.

**5. Do the 582 bare cross-skill path citations get fixed in this batch?** They span 223 files across
roughly 40 skills, most already at standard. Recommend **no** — ship the checker in Batch 8, record
the 582 as its first-run baseline in the carry-over, and fix them as a dedicated pass. *Trade-off:*
the tree carries a known 582-item defect for one more cycle. Fixing them now means editing dozens of
at-standard skills inside a batch that does not own them, which is the failure mode
`UPGRADE-CARRYOVER.md:149` warns against.


---

# Appendix D — `alaa-postman-collections`

# Batch 8 — Lane L4 analysis: `alaa-postman-collections`

Analyst: lane L4. Date of all upstream checks: **2026-07-29**.
Staged copy read in full: `/home/claude/b8/src/alaa-postman-collections/` (21 files, 173 KB).
Device original: `D:\Sohrab\Project\skills\skills\sohrab\alaa-postman-collections\`, read-only via
`mcp__remote-devices__device_bash`. Nothing was written to the device.

Every script run reported below was executed in the container against fixtures in `/tmp/pm/`.
Observed stdout and exit codes are reproduced verbatim.

---

## 0. Answer to the lane's framing question: which parts are already at standard

All 21 files were rewritten in one pass on **2026-07-25**, in a window from 12:07 to 15:06
(`find -printf '%TY-%Tm-%Td %TH:%TM'` on the device). `scripts/audit_collection_contract.py` at
12:07 is 2h43m older than everything else — consistent with it being the frozen, consumer-copied
script that `references/60-validation-and-output-contract.md:148-154` says must not grow.

This is **not** uniform staleness. Item by item against section 7:

| Definition-of-done item | State | Evidence |
|---|---|---|
| Description says what / when / **when not** | **CONFORMS** | `SKILL.md:3` ends `…do not use for generic docs work with no Postman or public-API ownership.` 889 chars raw (≤900 budget), zero angle brackets. |
| `## When not to use` heading for the repo validator | **CONFORMS** | `SKILL.md:32` `## When NOT to use`; the validator's regex at `skills/scripts/validate_sohrab_skill_pack.py:184` carries `re.I \| re.M`, so the capitalisation passes. |
| `agents/openai.yaml` 25–64 char `short_description`, `$name` in `default_prompt` | **CONFORMS** | 62 chars; `$alaa-postman-collections` present at line 4. |
| ≥9 references ⇒ separate `references/00-topic-map.md` | **CONFORMS** | 13 references; `00-topic-map.md` routes by "About to write → Read" (lines 15-25), not by file number. This is the programme's convention, already correct. |
| Cross-skill references name the owning skill beside the path | **CONFORMS** | `41-response-contract-and-error-coverage.md:44-48` — "`alaa-services-contract` owns the exact codes… Read that skill's `references/10-core-service-contract.md`". |
| Every instruction exactly once | **CONFORMS (one exception)** | Automated sentence-overlap probe: **1 duplicated sentence out of 60 body sentences**, and that one is a cross-skill restatement (§3, D3). Body↔reference duplication is effectively zero. |
| Cross-runtime trigger syntax given both ways | **CONFORMS** | `SKILL.md:125-127` gives `/name` and `$name` and both self-forms; `41:50` and `43:29` each give both forms for `alaa-services-contract`. Grep both directions: 4 `$alaa-*`, 3 `/alaa-*`, difference explained entirely by `agents/openai.yaml` being Codex-only. |
| No hardcoded model name | **CONFORMS** | Zero matches for model/GPT/Claude/Opus/Sonnet across the whole skill; `SKILL.md:143-144` routes the question to `alaa-prompting-guide` and says "this skill pins no model". |
| No `Path(__file__).parents[N]`, no repo temp dirs, no `__pycache__` | **CONFORMS** | Zero matches for `parents[`, `tempfile`, `mkdtemp`; neither script opens any file for writing; `find -name __pycache__` empty. |
| Repository plugin validator passes | **CONFORMS with one warning** | `python3 scripts/validate_sohrab_skill_pack.py` on the device: `Errors:` (none) / `Warnings: - alaa-postman-collections: top-level body is 154 lines`. |
| Body ≤120 lines | **FAILS** | 157 lines / 154 by the validator's count. |
| Scripts run on Windows | **PARTLY** | See §6. Encoding and CRLF handling are Windows-correct and deliberately so; the *documented invocation* is not. |
| Exit-code contract 0/1/2 | **ONE SCRIPT FAILS** | `audit_collection_contract.py:409` returns `1` for every "could not run". See §6. |
| Not larger than before | n/a | No prior version in the staged tree to diff against. |

**Conclusion for Phase 2: do not rewrite the routing layer, the frontmatter, the trigger syntax, the
topic map, or the duplication structure. They are already at standard.** The defects are concentrated
in three places: the two scripts' assertion strength, the boundary with
`alaa-laravel-public-api-contract-pack`, and version currency (§5), which is where the newest file in
this batch has aged fastest.

---

## 1. Inventory

| File | Bytes | What it actually contains |
|---|---|---|
| `SKILL.md` | 9 271 | Routing-first body. Its load-bearing section is "What complete means" (lines 41-68): seven numbered properties, each with the reference file that owns it. Also a 9-step deterministic workflow (94-111) and a 15-line companion-routing block (123-144). 157 lines. |
| `agents/openai.yaml` | 673 | Codex interface block: display name, 62-char `short_description`, one long `default_prompt` restating the seven properties. `allow_implicit_invocation: true`. |
| `assets/request-documentation-block.md` | 4 215 | The eight-heading request-description template, with per-heading instructions on what each must answer. Contains a worked three-row `## Errors` table with placeholder codes. |
| `assets/response-tests-post-response.js` | 2 728 | Runnable `pm.*` test skeleton, five `pm.test` blocks, four numbered EDIT points. Includes a defensive `pm.response.json()` wrapper and a `readPath` reducer. |
| `assets/token-capture-post-response.js` | 3 718 | Runnable capture template: a `CAPTURE_MAP`, an explicit `SUCCESS_CODE` guard, an empty-value skip, a Set-Cookie refresh-token branch, and two failing-test reporters. Four EDIT points. |
| `references/00-topic-map.md` | 2 477 | Routing table keyed on "About to write". Also lists the three assets and the two scripts with a one-line trigger each. |
| `references/10-scope-and-trigger-rules.md` | 6 252 | Owns/does-not-own list, strong triggers, a six-level source-of-truth order for API behaviour separated from a two-level order for artifact ownership, the generated-artifact rule, a discovery checklist, six hard constraints, and five stop-and-ask conditions. |
| `references/20-collection-structure-and-docs.md` | 3 207 | `info` block requirements, folder-depth-2 rule, request ordering so a top-to-bottom run works, and a "where a shared fact lives" three-level split. |
| `references/25-public-api-contract-and-sdk-readiness.md` | 9 969 | The largest doctrine file. Claims mandatory ownership of the repository's canonical machine-readable public API contract, prescribes OpenAPI 3.1 and a location (`docs/contracts/<service>/openapi.yaml`), a route-and-variant coverage matrix, request/response/cross-cutting completeness lists, a 7-question SDK-readiness test, and 7 stop conditions. |
| `references/30-variables-auth-and-environments.md` | 6 457 | Five checkable environment-completeness conditions, the per-developer-vs-shared test, committed-value safety rules, `snake_case` naming, environment-file shape, dynamic variables, and auth-level selection. |
| `references/41-response-contract-and-error-coverage.md` | 5 590 | The saved-example coverage rule, a four-source error-enumeration procedure, example naming as an addressable identifier, five coherence rules, two legitimate "cannot get an example" cases, and a mechanical gate command. |
| `references/42-scripts-and-state-capture.md` | 7 836 | The no-manual-copy rule, the variable-scope decision (`environment` vs `collectionVariables` vs never `globals`), script placement, six things a capture must do, the never-hardcode-a-credential list with positive replacements, an allow/avoid API list, and a dependency audit. |
| `references/43-response-tests.md` | 4 754 | The "test that is not a test" doctrine, the five minimum assertions, assertions to keep out, the portable assertion form, and placement. |
| `references/44-request-documentation-blocks.md` | 4 297 | Two named readers, where each fact goes, writing constraints, "length is a floor not a target", and the eight `--require-doc-section` flags. |
| `references/45-mock-servers.md` | 5 295 | What a mock is here, when it is worth defining, the five-step Postman matching algorithm with an authoring consequence per step, the tie-break rule, variables inside a mocked example, naming, and the Insomnia consequence. |
| `references/50-insomnia-compatibility-and-free-plan-rules.md` | 9 637 | A 13-row preserve/drop table dated "Verified 25 July 2026" against two named importer source files, the four accepted `info.schema` strings, scripting rules that follow from the `pm.`→`insomnia.` rewrite, environment-importer rules, Postman and Insomnia free-plan claims, and a portability-proof command. |
| `references/60-validation-and-output-contract.md` | 10 275 | The 8-step validation ladder, the full flag table for both scripts, both exit-code tables, the "why this script does not grow" rule, how to choose between the two, external checks, manual follow-ups, stop-before-close checks, and a 7-item output contract. |
| `references/70-aggregate-collections-and-consumer-repos.md` | 7 909 | Aggregate-vs-service-local artifact table, the ownership split that keeps one platform's service registry out of the skill, the four-term rule for a consumer repo holding a copy of a script, eight merge-program invariants, and a which-repository-to-fix decision list. Names `gateway/scripts/postman/generate_gateway_collection.sh` as the reference implementation at line 77. |
| `references/90-source-map.md` | 3 795 | Four-level source priority, 13 primary source URLs, freshness triggers, and a domain-bounded anti-pattern. |
| `scripts/audit_collection_contract.py` | 17 068 | The strict gate. 445 lines, stdlib only. |
| `scripts/validate_postman_artifacts.py` | 37 649 | The broad sweep. 946 lines, stdlib plus optional `jsonschema`. |

---

## 2. The ten-criteria verdict table

**Counts: SATISFIED 6 · FAIL 3 · DELEGATED 1.**

| # | Criterion | Verdict | Evidence | What a fix must add |
|---|---|---|---|---|
| 1 | Correctness and testability | **FAIL** | The doctrine is strong: `43-response-tests.md:9` and `:15-17` state the anti-decoration rule, and `assets/response-tests-post-response.js:1-10` encodes it. But (a) **nothing in the skill ever executes a collection** — Newman and the Postman CLI appear at zero call sites across all 21 files, and the 8-step validation ladder at `60-…:5-22` contains no run step; (b) neither script ships a self-test; (c) the one gate that protects the skill's most important script rule is **provably vacuous on conforming collections** — see D-A in §3. | A `newman run` (or Postman CLI) step in the ladder with its exit-code mapping; a `scripts/selftest.py` fixture pair (one clean, one broken) whose broken case must exit non-zero; and a structural, not textual, success-guard check. |
| 2 | Failure behaviour | **SATISFIED** | `41-…:36-41` makes dependency failures one of four mandatory error sources and says "the retryability of that status is part of the contract". `25-…:114-118` requires an explicit safe-retry matrix by method/status/error code, rate-limit status and headers. `assets/request-documentation-block.md:66-70` puts "Caller does" in the `## Errors` table with a `503 DEPENDENCY_UNAVAILABLE` row. Values delegated to `alaa-services-contract references/22-failure-load-and-deprecation-contract.md` at `41-…:47-48`. | Nothing required for the verdict. Optional: a `--require-retry-column` gate so the "Caller does" column cannot be left blank. |
| 3 | Security | **SATISFIED** | `42-…:95-108` lists four credential defects and gives the positive replacement for each ("reference a variable, declare that variable in the environment with a placeholder value, and populate it from a capture script"). `30-…:51-62` forbids realistic-looking sample values and production hostnames. `44-…` mandates a `## Security notes` heading; `assets/request-documentation-block.md:83-92` requires the isolation identifier, the stripped gateway headers, the IDOR/BOLA surface, and replay/expiry. Mechanically enforced: `validate_postman_artifacts.py:99-108` (7 credential-shape patterns plus an entropy rule) with a dedicated `EXIT_SECRET = 4`. Proved in RUN 2 below. | Nothing required for the verdict. Named gap: the **strict gate** (`audit_collection_contract.py`) contains no secret check at all, so the script CI actually blocks on is the one that cannot find a leaked credential. |
| 4 | Observability | **DELEGATED** | `43-…:33-36` makes `X-Request-Id` one of the five mandatory assertions and names the owner and file: "`alaa-services-contract` makes it mandatory on every response, in that skill's `references/20-operational-and-observability-contract.md`". `41-…:44-48` routes codes, envelopes and headers to the same owner with three specific file paths and both trigger forms. All three cited files exist on the device. | Nothing required. Named gap: `traceparent` is required at `41-…:46` but only `X-Request-Id` has a `--require-correlation-assertion` flag. |
| 5 | Concurrency and load | **FAIL** | The *caller-facing* semantics are covered (`25-…:115-118`: idempotency-key scope/retention/replay/conflict, rate-limit headers, optimistic concurrency). What is entirely absent is the **artifact's own** concurrency: `42-…` mandates `pm.environment.set` for every credential but never addresses two developers sharing one environment, a Collection Runner running folders in parallel over one environment, or a capture race where request B reads `access_token` while request A is rewriting it. `30-…:36-38` defines "per-developer" by "if two developers running this collection at the same time would need different values" — which raises the question and does not answer it. | A rule in `42-…` for capture-under-concurrency: one writer per variable name, a namespaced variable when a folder may run in parallel, and an explicit statement that the collection's correctness assumes serial execution within a folder (`20-…:35-37` already assumes it implicitly). |
| 6 | Clean code, SOLID, patterns | **SATISFIED** | Both scripts are flat, stdlib-only, take every input as an argument (`70-…:41` states this is deliberate so no repo-specific constant is ever added to a consumer copy), and separate collection/environment/schema concerns into distinct functions. The ~8 helpers duplicated between the two scripts (`script_lines`/`script_text_of`, `written_variable_names`, `is_correlation_variable`, `raw_url`, `description_text`, `VARIABLE_SET_RE`, `SUCCESS_GUARD_MARKERS`) are justified by the no-shared-import constraint at `60-…:148-154`. | Nothing required. Named gap: the duplicated pair has already drifted — `audit_collection_contract.py:19-21` omits `globals` from `VARIABLE_SET_RE` while `validate_postman_artifacts.py:81-83` includes it, so the strict gate does not see a `pm.globals.set` write at all. |
| 7 | Algorithm and data-structure choice | **FAIL** | No complexity budget is stated anywhere in the skill. `validate_postman_artifacts.py:675` calls `variable_refs(collection)` which runs `iter_strings` over **every string in the entire document** including all saved-example bodies, then a regex over each; `:517-519` runs `json.dumps(body)` and 7 regex searches per request. Project memory records the live gateway collection at **8.3 MB / 73 requests**; no runtime figure for that size appears anywhere, and `60-…` gives no guidance on running either script against a collection of that size. | A stated budget ("linear in document bytes, one pass; measured at N seconds on an 8 MB / 73-request collection on <host>") and a `--max-bytes` guard that exits 2 rather than silently taking minutes. |
| 8 | Configurability | **SATISFIED** | Every threshold is a documented flag with a default (`60-…:57-72`). `--allow-external-var` exists for a legitimately external variable; `--schema-url` overrides the pinned schema; `--skip-schema` for an offline host; `--max-findings` caps output. Boundary validation is present and correct: `validate_postman_artifacts.py:874-876` rejects negative thresholds and `--max-findings 0` with `EXIT_INPUT`. Configurability is bounded by a rule: `60-…:112-114` — "Never lower a threshold or drop a flag to make a run pass." | Nothing required. |
| 9 | Speed of development and debuggability | **SATISFIED** | `00-topic-map.md:15-25` routes by "About to write", not by topic name, which is the fastest possible index for this domain. Every reference opens with "Read this file when…". Both scripts print counts alongside findings, and `--json` exists on both for evidence attachment. | Nothing required for the verdict. Two concrete debuggability defects, both fixable: undeclared-variable findings name no request (see D-D in §3), and the body is 157 lines against a 120-line warn threshold. |
| 10 | Documentation | **SATISFIED** | `44-…` plus `assets/request-documentation-block.md` define eight observable headings with per-heading content requirements, and `44-…:24-26` states why: "'Document it well' is not a rule an agent can comply with or violate. The eight headings in the asset are." `60-…:201-212` gives a 7-item output contract for the task itself. `70-…:77` names the two operational files a reader must open before changing an aggregate. | Nothing required. |

---

## 3. Defect-class findings

Only classes actually found are listed. Classes 1, 2, 4, 7, 8 were checked and are **clean** (§0).

### D3 — Duplication between skills, at a boundary the other side has already declared

`references/43-response-tests.md:9`
> `A test that still passes against a plausible broken implementation is not a test.`

`alaa-testing-strategy/SKILL.md:22` (device):
> `**A test names the broken implementation it defends against. A test that still passes against a plausible broken implementation is not a test — it is an execution of the code under a different name…**`

The sentence is restated a third time in `assets/response-tests-post-response.js:7-8`. `43-…` never
names `alaa-testing-strategy` at any call site. This is the **only** duplicated sentence in the whole
skill (automated probe: 1 hit / 60 body sentences), which makes it easy to fix.

### D5 — A long procedure that will not be read in order

`references/25-public-api-contract-and-sdk-readiness.md` is 10 KB of nine consecutive bulleted
completeness lists (`## Request completeness` 10 bullets, `## Response completeness` 10,
`## Cross-cutting SDK semantics` 13, `## Validation evidence` 9, `## Stop conditions` 7). There is no
failure-class structure — no symptom, no smallest retry. Compare `41-…:14-51`, which does the same
job in the correct shape (four enumerated *sources*, each with the class of error it produces and the
consequence of collapsing it). `25-…` is the file `SKILL.md:75-77` tells an agent to read on **every**
public-API task, so it is the most-loaded reference in the skill and the least navigable.

### D6 — Description clause present but under-specified for the actual overlap

`SKILL.md:3` ends: `do not use for generic docs work with no Postman or public-API ownership.`
That clause excludes the wrong neighbour. The real over-trigger risk is the **public-API contract**
clause earlier in the same description — `Whenever the repository owns a public HTTP API, also create
or synchronize its SDK-ready public API contract` — which collides head-on with
`alaa-laravel-public-api-contract-pack`. See §4.

### D9 — Section-2 gaps

Criteria 1, 5 and 7 (§2). The most consequential is criterion 1: a skill whose central deliverable is
"tests that would fail against a broken implementation" and which ships zero means of executing them.

### D10 — Stale version and vendor facts

Six claims are stale or wrong as of 2026-07-29. See §5.

### D11 — Companion boundary is one-directional

`alaa-postman-collections` names 8 companion skills. It does **not** name
`alaa-laravel-public-api-contract-pack`, `alaa-testing-strategy`, `alaa-project-constitution`,
`alaa-observability-soc`, `alaa-reliability-sla`, or `alaa-low-noise` at any call site
(grep count: 0 each). Two of those name it:

- `alaa-testing-strategy/SKILL.md:3` — `Postman request tests to /alaa-postman-collections`; and
  `:119` — "`/alaa-postman-collections` (`$alaa-postman-collections`) owns API-level request tests,
  their five minimum assertions, examples, and scripts. This skill owns the layer that work sits at."
- `alaa-laravel-public-api-contract-pack/SKILL.md:3` — `collection and environment generation to
  /alaa-postman-collections`, plus four in-reference call sites.

### D-A (new class) — **A gate that cannot fail on any collection that follows this skill**

The single most consequential finding in this lane.

`references/42-scripts-and-state-capture.md:74-77` makes the success guard the first of six
mandatory capture properties: *"Guard on an explicit success status… Without it, an intentional error
response overwrites a working token and every later request fails for the wrong reason."*
Both scripts enforce it by **substring search over the whole test script**:

`scripts/validate_postman_artifacts.py:88-93`
```python
SUCCESS_GUARD_MARKERS = (
    "pm.response.code",
    "pm.response.to.be.success",
    "pm.response.to.have.status",
    "pm.expect(pm.response.code",
)
```
(identical list at `scripts/audit_collection_contract.py:294-299`), tested at
`validate_postman_artifacts.py:382` with `if not any(marker in script_text …)`.

`references/43-response-tests.md:60` **mandates on every request** the assertion
`pm.expect(pm.response.code).to.eql(200)`. That string contains `pm.response.code`. Therefore any
request that complies with the skill's own five-assertion minimum satisfies the guard check
regardless of whether the capture is guarded at all.

Proved. `/tmp/pm/fakeguard.postman_collection.json` writes the token on line 1, unconditionally, then
carries the two mandated assertions:

```
########## VALIDATOR: unguarded capture that merely mentions pm.response.code ##########
Counts: requests=1 saved_responses=2 with_success_example=1 with_error_example=1 with_tests=1 with_captures=1
Validation passed with no issues.
EXIT=0
########## AUDITOR: same ##########
f: requests=1 saved_responses=2 scripted_requests=1 errors=0
EXIT=0
```

Both gates pass. The rule has no tool that reports its violation.

### D-B (new class) — **Checker returns clean on an artifact containing nothing to check**

`/tmp/pm/empty.postman_collection.json` is a valid v2.1 collection whose `item` array holds two
folders, each with `"item": []`. Zero requests. Run at **full strength**, every `--require-*` flag on:

```
########## VALIDATOR vs empty.postman_collection.json ##########
Counts: requests=0 saved_responses=0 with_success_example=0 with_error_example=0 with_tests=0 with_captures=0
Validation passed with no issues.
EXIT=0
```

This is the batch-7 class exactly. Every `--require-*` flag is vacuously satisfied because
`walk_items` (`validate_postman_artifacts.py:441-628`) only fires them per request item, and
`validate_collection:659-661` only checks that the **top-level** `item` array is non-empty — folders
satisfy it. A CI gate built on this script reports PASS on a collection with no requests.

This is not hypothetical for this skill's own stated domain.
`references/70-aggregate-collections-and-consumer-repos.md:60-63` names two merge-program failures
that produce exactly this artifact — invariant 7 (an over-broad exclusion filter) and invariant 5
(saved-response conservation) — and says of them: *"Invariants 4, 5, and 6 each produce an artifact
that looks correct and does not work."*

The auditor **does** catch it, at `audit_collection_contract.py:373-374`:
```
########## AUDITOR vs empty (folders only) ##########
empty: requests=0 saved_responses=0 scripted_requests=0 errors=1
  ERROR: collection: collection contains no request items
EXIT=1
```
So the fix is a five-line port of a check the skill already owns.

### D-C (new class) — The eight-heading documentation gate is satisfiable by empty headings

`44-…:56-61` says plainly: *"Meeting it with padding is worse than failing it, because a padded
description passes the gate and still leaves both readers guessing."* The gate does not detect it.
`/tmp/pm/padded.postman_collection.json` carries the eight heading lines and nothing else but 400
characters of `x `:

```
Counts: requests=1 saved_responses=2 with_success_example=1 with_error_example=1 with_tests=1 with_captures=1
Validation passed with no issues.
EXIT=0
```

`heading_names()` (`:261-262`) collects heading text only; nothing measures the body under a heading.

### D-D — Exit-code contract violated by the strict gate

`scripts/audit_collection_contract.py:407-409`
```python
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
```
`references/60-validation-and-output-contract.md:122` documents this as intended: *"An input it
cannot read also exits `1`."* Documented is not the same as correct. Under the programme's contract
a "could not run" must exit 2 so a harness records BLOCKED rather than FAIL. Observed for every
could-not-run case — missing file, malformed JSON, truncated JSON, empty file, JSON array, and an
unreadable `--environment` while the collection itself was fine — all `EXIT=1` (§6, run table).

### D-E — Findings that name no location, on the collection size this skill exists for

`validate_postman_artifacts.py:676-680` emits undeclared-variable errors scoped to the string
`collection:` with no item path, and `variable_refs` scans **every** string including prose
descriptions and saved-example bodies. Observed:

```
Errors (2):
- collection: variable `{{docs_url}}` is referenced but declared in neither the collection nor any environment input; declare it or pass --allow-external-var
- collection: variable `{{tenant_id_example}}` is referenced but declared in neither the collection nor any environment input; declare it or pass --allow-external-var
EXIT=1
```
`{{tenant_id_example}}` was inside a request **description** (prose, never executed);
`{{docs_url}}` was inside a saved example **body**. Both are blocking errors, neither names the
request that caused it. On a 73-request, 8.3 MB collection this is the noise profile that gets a gate
switched off.

### D-F — Typo in an executable-adjacent path reference

`references/43-response-tests.md:35`
> `` `references/20-operational-and-observability-contract.md`,, which makes its absence a contract failure ``

Double comma.

---

## 4. Boundary analysis

### 4.1 `alaa-laravel-public-api-contract-pack` — a real, two-sided ownership collision

**The other side, quoted.** `alaa-laravel-public-api-contract-pack/SKILL.md:3` (device, mtime
2026-07-26 — *newer* than this skill):

> `Build and audit a Laravel service's public client API contract pack from executable repository
> truth: route inventory, versioning and breaking-change classification, per-route write and retry
> semantics, consumer-visible pagination and limits, **OpenAPI plus Postman plus TypeScript SDK input
> docs**, and a gate that refuses to emit a pack while any route's version, deprecation status, or
> sunset date is unresolved. … Do not use to decide fleet contract values … **collection and
> environment generation to /alaa-postman-collections**; …`

And `references/40-consumer-discovery-pinning-and-secret-hygiene.md:61-62`:
> `Postman files are `alaa-postman-collections` (`/alaa-postman-collections`,
> `$alaa-postman-collections`) `references/30-variables-auth-and-environments.md`, **which wins on**…`

That skill has made a clean, explicit, one-way delegation: *it* owns the contract, *this* skill owns
the collection and environment. It also already ships `scripts/contract_pack_audit.py`, whose
docstring (line 7) reads `parity   route inventory vs OpenAPI operations vs Postman requests` and
which emits an `openapi_postman_divergence` finding (cited at
`10-versioning-and-breaking-change-classification.md:91`).

**This side, quoted.** `references/25-public-api-contract-and-sdk-readiness.md:3`:
> `Read this file whenever the repository owns a public HTTP API. **Public-contract synchronization is
> mandatory for this skill**, even when the user's immediate wording mentions only Postman.`

`:20-22`:
> `**OpenAPI 3.1 is preferred** when the repository has no stronger canonical format. … If the repo
> clearly owns public routes but has no contract convention, **create the smallest explicit pack at
> `docs/contracts/<service>/openapi.yaml`**`

`:140-152` then defines a 7-question **SDK-readiness test** and forbids labelling the contract
SDK-ready until all answers are yes.

`alaa-postman-collections` names `alaa-laravel-public-api-contract-pack` **zero times** in all 21
files. So on any Laravel repository with a public API, two skills each claim to own the canonical
OpenAPI document, each prescribe a location, each define a completeness gate, and only one of them
knows the other exists. `SKILL.md:132-134` even routes Laravel work to `alaa-laravel-architecture`,
which is the *code* skill, not the contract-pack skill.

**The line I recommend, and it is drawn by capability, not by politeness.** The Laravel pack's gate
is *emission-blocking on unresolved version/deprecation/sunset* and its parity check is
route-inventory-driven from `php artisan route:list --json`. This skill has no route inventory and
cannot get one. Therefore:

- **`alaa-laravel-public-api-contract-pack` owns "what the contract is"** for any Laravel service:
  the canonical document, its location, its versioning and deprecation classification, the route
  inventory it is proved against, and the emission gate.
- **`alaa-postman-collections` owns "how the collection proves it"**: the Postman/environment
  projection, saved examples, scripts, tests, request documentation, mock servers, secret typing,
  and Insomnia portability. Its SDK-readiness questions become *Postman-side* questions —
  "does every operation in the canonical contract have a request item, and does every response
  branch have a saved example" — checked against the contract, not derived independently.
- For a **non-Laravel** repository with no contract owner, `25-…` remains this skill's, unchanged,
  because no other skill covers that case. The file must say so in its first paragraph.

Phase 2 must therefore rewrite `25-…`'s opening scope paragraph, not delete the file.

### 4.2 `alaa-services-contract` — correct and already at standard

The routing is exemplary and needs no change. `41-…:42-51` names the owner, three specific reference
files, and both trigger forms, then states the non-restatement rule explicitly at `:53-57`:
> `Never restate the envelope in this skill's files or in a request description. Assert and document
> the shape that skill declares. When the route's real response disagrees with it, that is drift…`

Grepped both directions. This skill never states an error code, an envelope key, or a header value
of its own; the only literal it asserts is `X-Request-Id`, and it asserts it *with* the owner and
file (`43-…:34-35`). All three cited `alaa-services-contract` reference files exist on the device.
The reverse direction is looser — `alaa-services-contract` mentions Postman at nine call sites
(e.g. `references/20-operational-and-observability-contract.md:19`, "not in code, config, docs,
tests, fixtures, Postman artifacts, or emitted response headers") but never names
`alaa-postman-collections`. That asymmetry is acceptable: the contract skill is the fleet authority
and does not need to route outward.

**One fix required:** the double comma at `43-…:35`.

### 4.3 `alaa-testing-strategy` — restatement without a call site

Quoted both sides in D3. `alaa-testing-strategy` has already drawn the line twice and named this
skill in its own frontmatter description. This skill does not name it once.

`43-…` does not restate the *whole* of testing-strategy — its five-assertion minimum and its
"assertions to keep out" list are genuinely Postman-specific and belong here, which
`alaa-testing-strategy/SKILL.md:119` confirms ("owns API-level request tests, their five minimum
assertions, examples, and scripts"). The only content that must move is the doctrine sentence, which
becomes a routed pointer.

### 4.4 `alaa-docs-farsi` — clean from their side, needs one reciprocal sentence

`alaa-docs-farsi/references/10-language-and-links.md:32` already excludes this skill's territory:
> `- Postman-only collection or environment maintenance with no Markdown doc work.`

and `references/30-api-summary-contract.md:16` positions `docs/api-summary.md` as the sheet for
readers "who need the endpoint map and a few verified request examples **without reading a full
Postman collection**". A grep of the whole `alaa-docs-farsi` tree for "request description",
"request-level" or "per-request" returns **nothing**, so there is no competing claim on request-level
documentation.

**Boundary I propose from this side, flagged as needing reciprocal agreement with the concurrent
`alaa-docs-farsi` lane:**

- `alaa-postman-collections` owns documentation **inside** a Postman artifact: the eight-heading
  `request.description`, folder descriptions, and the collection description. Its unit is one HTTP
  operation.
- `alaa-docs-farsi` owns documentation **about** the repository: `README.md`,
  `docs/BIG_PICTURE.md`, `docs/api-summary.md`, runbooks, and `remaining-task.md`. Its unit is the
  repository.
- The seam is `docs/api-summary.md`: it summarises the endpoint map, it does not restate the eight
  headings, and it links to the collection. Where a fact appears in both, the collection is the
  source and the summary is derived.
- `remaining-task.md` is already correctly delegated in this direction —
  `SKILL.md:141-142` and `10-…:59` both route documented-but-not-implemented gaps to
  `alaa-docs-farsi`, and `alaa-docs-farsi/references/40-sync-workflow-and-evidence.md:73` accepts it.
  **That is the one reciprocal pair already working; the rest needs agreement.**

### 4.5 What the skill should own and does not

- **The environment file as a configuration artifact.** It owns "Postman environment JSON artifacts"
  (`10-…:10`) and has five completeness rules (`30-…:12-32`), but no rule and no check on whether a
  committed environment value is a *hardcoded implementation constant* that belongs in the
  generator's inputs. See §7 item 3 — this is the live gateway defect.
- **Execution of the collection.** See criterion 1.

---

## 5. Version and factual currency — every asserted fact, checked today (2026-07-29)

| # | Claim (file:line) | Verdict | Source | Re-derivation command |
|---|---|---|---|---|
| 1 | `info.schema` must be `https://schema.getpostman.com/json/collection/v2.1.0/collection.json` (`20-…:14`, `50-…:76`, `audit:15`, `validate:27`) | **VERIFIED** | Insomnia importer master source: `POSTMAN_SCHEMA_URLS_V2_1` at `packages/insomnia/src/main/importers/importers/postman.ts:104-107` contains exactly this string plus the `schema.postman.com` twin. | `curl -s https://raw.githubusercontent.com/Kong/insomnia/master/packages/insomnia/src/main/importers/importers/postman.ts \| grep -A4 POSTMAN_SCHEMA_URLS_V2_1` |
| 2 | The four accepted `info.schema` strings (`50-…:62-67`) | **VERIFIED, exact** | Same file, lines 100-107: two v2.0 strings and two v2.1 strings, no others; `convert()` returns `null` otherwise (`:969`). | as above |
| 3 | **v2.1 is the current Postman collection format** (implicit throughout; `20-…:11` "Target format… Postman Collection Format v2.1 JSON") | **STALE** | Postman Docs, *Postman Collections schemas*: **"The current version of Postman uses schema 3.0.0."** and "Collections schema 3.0.0 defines a collection with multiple YAML files organized on disk, so humans, AI agents, and automation tools can read, diff, review, and safely change collections." Also: "In Postman v12, Newman can run a Postman Collection exported to the 2.1.0 format, but it can't run 3.0 collections. To run 3.0 collections, use the Postman CLI instead of Newman." | `WebFetch https://learning.postman.com/docs/use/use-collections/collections-schemas` |
| | | | **Assessment:** the *choice* of v2.1 remains correct — Insomnia's importer accepts only v2.0/v2.1 (claim 2), and Newman runs only 2.1. But the skill never says 3.0 exists, never states why it pins 2.1, and 3.0's stated design goal ("so humans, AI agents, and automation tools can read, diff, review") is this skill's entire premise. Phase 2 must add the pin **with its reason and its re-derivation command**, per D10. | | |
| 4 | JSON-Schema validation URL `https://schema.getpostman.com/collection/json/v2.1.0/draft-04/collection.json` (`validate:26`, `90-…:27`, `50-…:79`) | **VERIFIED, with a caveat** | 302-redirects to `https://schema.postman.com/collection/json/v2.1.0/draft-04/collection.json`. The `getpostman.com` host is legacy-but-live. `urllib.request.urlopen` follows the redirect, so `validate_postman_artifacts.py:771` still works. A **draft-07** variant also exists at `https://schema.postman.com/collection/json/v2.1.0/draft-07/docs/index.html`. | `curl -sIL https://schema.getpostman.com/collection/json/v2.1.0/draft-04/collection.json \| grep -i '^location\|HTTP/'` |
| 5 | Insomnia preserves collection-level `auth`, applied to the imported folder (`50-…:30`) | **VERIFIED** | `postman.ts:304-327` — `importCollection` destructures `auth`, calls `importAuthentication(auth)`, and assigns `authentication` onto `collectionFolder`. | `curl -s …/postman.ts \| sed -n '304,340p'` |
| 6 | Seven mapped auth types: `basic bearer apikey digest oauth1 oauth2 awsv4` (`50-…:32`, `validate:77-79`) | **VERIFIED, exact** | `postman.ts:535-583` — `case 'awsv4' 'basic' 'bearer' 'digest' 'oauth1' 'oauth2' 'apikey'`, and nothing else. | `curl -s …/postman.ts \| grep -n "case '"` |
| 7 | Collection `variable` → Insomnia environment named `Variables`, wired as Base Environment (`50-…:35`) | **VERIFIED, verbatim** | `postman.ts:329-337` — `// Mapping postman collection variables to collection base environment`, `name: 'Variables'`, `_id: '__BASE_ENVIRONMENT_ID__'`. | as above |
| 8 | Only the **first** `prerequest` and **first** `test` event per scope survive (`50-…:37`, `42-…:57-60`) | **VERIFIED** | `postman.ts:164` `events.find(event => event.listen === 'prerequest')`; `:186` `events.find(event => event.listen === 'test')`. `.find` returns the first match; the rest are dropped. | `curl -s …/postman.ts \| grep -n "events.find"` |
| 9 | Scripts are rewritten: legacy forms translated, then `pm.` textually replaced with `insomnia.` (`50-…:38`, `:85-87`) | **VERIFIED, verbatim** | `translate-postman-script.ts:203-205`: `// Replace \`pm.\` to \`insomnia.\`. Doesn't support \`µpm\`.` / `translated = translated.replace(/(?<![\.\$\-"'])\bpm\./g, 'insomnia.');` | `curl -s https://raw.githubusercontent.com/Kong/insomnia/master/packages/insomnia/src/main/importers/importers/translate-postman-script.ts \| tail -20` |
| 10 | `item.response` (saved examples) is **not read at all** (`50-…:39`, `:44-55`, `45-…:99-103`) | **VERIFIED** | `grep -n '\.response\b' postman.ts` over all 970 lines returns no read of `item.response`. | `curl -s …/postman.ts \| grep -n "item.response\|\.response\b"` |
| 11 | Environment importer: `_postman_variable_scope` must be `environment` or `globals` or the file is rejected; only truthy `enabled` imported; `type` and `description` ignored (`50-…:110-121`, `30-…:29-32`, `30-…:74-75`) | **VERIFIED, verbatim, all three** | `postman-env.ts` in full (57 lines): `if (!validPostmanEnvTypeList.includes(_postman_variable_scope)) { return null; }`; `values.reduce((acc, { enabled, key, value }) => { if (!enabled) return acc; …})`; the `EnvVar` interface declares only `enabled`, `key`, `value`. | `curl -s https://raw.githubusercontent.com/Kong/insomnia/master/packages/insomnia/src/main/importers/importers/postman-env.ts` |
| 12 | **"Insomnia's own documented example is `insomnia.expect(insomnia.response.code).to.eql(201)`"** (`50-…:102-103`); and the derived rule "prefer `pm.expect(pm.response.code)`" (`43-…:60-70`, `validate:319-325`) | **STALE — and the rule it justifies may now be inverted** | `https://developer.konghq.com/insomnia/scripts/` today documents **`insomnia.response.status`**, not `.code`. Its verbatim example is:<br>`const status = insomnia.response.status;`<br>`const responseTime = insomnia.response.responseTime;`<br>The page contains **no** `insomnia.response.code` and no `insomnia.expect(insomnia.response.code)…` example. Its only `expect` example is `insomnia.expect(200).to.eql(200)`. | `WebFetch https://developer.konghq.com/insomnia/scripts/` |
| | | | **Consequence, which Phase 2 must resolve before touching either asset.** The skill's *recommended* form `pm.expect(pm.response.code).to.eql(200)` rewrites (claim 9) to `insomnia.expect(insomnia.response.code)…`. If `insomnia.response` exposes `status` and not `code`, the recommended form is the **non-portable** one and the discouraged `pm.response.to.have.status(200)` may be no worse. Both assets (`response-tests-post-response.js:31,44`, `token-capture-post-response.js:80`) and the validator's `CHAI_RESPONSE_CHAINS` warning at `validate:75,319-325` push agents toward it. I could not reach the Insomnia SDK source to settle `code` vs `status` (`packages/insomnia-sdk/src/objects/response.ts` → 404 on both `master` and `main`), so this is **STALE-and-unresolved**, not merely stale. | | |
| 13 | Mock matching algorithm: method → `x-mock-response-code` → `x-mock-response-id` → `x-mock-response-name` → URL path score → query → headers/body; tie-break sorts by ID and returns the first `200` (`45-…:45-65`) | **VERIFIED, including the tie-break** | Postman Docs, mock matching algorithm: *"If more than one example has the highest score, Postman sorts the examples by ID and returns the first example in the list with a `200` response status code. If none of the highest-scoring examples has a `200` response status code, Postman returns the first example in the sorted list."* | `WebFetch https://learning.postman.com/docs/design-apis/mock-apis/matching-algorithm/` |
| 14 | **`npx --yes insomnia-importers@3.6.0 …` is the portability proof** (`50-…:158`, `60-…:170`), and "A successful conversion is stronger evidence than JSON or schema validation" (`50-…:161-162`) | **STALE — the package is deprecated** | npm registry: `insomnia-importers` latest is **3.6.0, published 2022-09-27**, `"deprecated": "Package no longer supported. Use at your own risk."`, registry `modified` 2023-05-23. It is ~4 years old and cannot reflect the current importer whose source this skill itself calls authoritative (`90-…:59-61`: *"Re-read Insomnia's two importer files rather than its documentation… The importer is the answer"*). The skill's own source-priority rule contradicts its own portability command. | `curl -s https://registry.npmjs.org/insomnia-importers \| python3 -c "import json,sys;d=json.load(sys.stdin);l=d['dist-tags']['latest'];print(l,d['time'][l],d['versions'][l].get('deprecated'))"` |
| 15 | Newman: any version, any flag | **NOT ASSERTED — and that is the finding** | Newman appears at **zero** call sites in all 21 files. Current release: **newman 6.2.2, published 2026-01-16, not deprecated, `engines: node >=16`**. `postman-collection` 5.3.1 (2026-07-21). | `curl -s https://registry.npmjs.org/newman \| python3 -c "import json,sys;d=json.load(sys.stdin);l=d['dist-tags']['latest'];print(l,d['time'][l],d['versions'][l].get('engines'))"` |
| 16 | Postman free plan: "API client, collections and environments, collection generation and sync, Native Git, the Postman CLI, and unlimited Collection Runner and Performance Testing runs" (`50-…:127-129`) | **VERIFIED but materially incomplete** | postman.com/pricing today lists on Free: `API client & core tools`, `Specs & mock servers`, `Native Git`, `Collection Runner & Performance Testing runs` (unlimited), `Postman CLI`, `Postman Local Vault`, `Secret Scanner - Local Secret Protection`, `Manual Flows`, `50 AI credits`, **`1,000 requests` monitoring per month**, **`10,000` monthly Postman API calls**, **single user**, up to 5 integrations, **`1 day` collection recovery**. The four bolded limits are absent from the skill. | `WebFetch https://www.postman.com/pricing/` |
| 17 | "mock-server call volume is metered per Postman plan" (`45-…:40`, `50-…:133`) | **UNVERIFIABLE as stated** | The current Postman pricing page lists no explicit mock-server call cap on Free; mock servers appear as an included capability ("Specs & mock servers"). The metering claim may be true but carries no number and no source. | `WebFetch https://www.postman.com/pricing/` — re-derive and pin the number or drop the claim |
| 18 | Insomnia free tier: "unlimited Cloud and Local projects, unlimited collection runs, unlimited environments, Inso CLI access, and plugin access" (`50-…:139-140`) | **VERIFIED but incomplete** | insomnia.rest/pricing today, free tier now branded **Essentials**: `Unlimited Cloud/Local projects for all users`, `Unlimited collection runs`, `Unlimited environments`, `Access to Inso CLI for CI/CD automation`, `Unlimited access to plugins or build your own`, `End-to-end encryption (E2EE)`. Two new limits the skill does not name: **`Unlimited Git Sync projects for up to 3 users`** and **`1,000 mock server requests per month`**. RBAC/SSO Enterprise-only, as the skill says. | `WebFetch https://insomnia.rest/pricing` |
| 19 | Current Insomnia release | **NOT ASSERTED — should be** | **12.6.0, released 2026-05-22** (three most recent: 12.6.0 2026-05-22, 12.6.0-beta.0 2026-05-11, 12.5.1-alpha.0 2026-04-11). The skill's compatibility table is dated "Verified 25 July 2026" against `master` with no version pin, so a reader cannot tell which Insomnia release the table describes. | `WebFetch https://github.com/Kong/insomnia/releases` |
| 20 | `pm.sendRequest`, `pm.test`, `pm.expect`, `pm.response`, `pm.variables`, `pm.environment`, `pm.collectionVariables`, `pm.cookies` are current (`42-…:112-113`, `50-…:89-91`) | **VERIFIED — not deprecated** | Postman Sandbox API reference documents all of them today with **no deprecation notice**; `pm.sendRequest` is actively documented ("Use the `pm.sendRequest` method in your scripts to send requests in Postman"). The lane brief's hypothesis that `pm.sendRequest` is being deprecated does **not** hold. | `WebFetch https://learning.postman.com/docs/tests-and-scripts/write-scripts/postman-sandbox-api-reference/` |
| 21 | `pm.vault`, `pm.require`, `pm.state`, `pm.datasets`, `pm.visualizer` are to be avoided (`42-…:118-120`, `50-…:98-100`, `validate:74`) | **VERIFIED, and the stated reason is the correct one** | All five are current, documented Postman members. The skill avoids them for **portability**, not deprecation, and says so. That reasoning is correct and needs no change. Two documented members the skill's allow-list omits: `pm.info` and `pm.message`. | as above |
| 22 | All 13 URLs in `90-source-map.md` | **9 VERIFIED reachable, 4 unverifiable from this host** | The four `learning.postman.com` / `schema.postman.com` URLs return `CONNECT tunnel failed, 403` through this container's egress proxy but resolve through WebFetch, so they are live; the two GitHub importer paths return HTTP 200 on `master`. | `for u in …; do curl -sIL "$u"; done` (proxy-blocked) or WebFetch per URL |

**Net: 12 VERIFIED, 3 STALE (claims 3, 12, 14), 2 incomplete-but-true (16, 18), 2 unverifiable (17, 22-partial), 2 not-asserted-but-should-be (15, 19).**

---

## 6. Executable-check inventory

Two scripts. Both are pure-stdlib Python (the validator optionally imports `jsonschema`). Neither
writes any file. Neither uses `Path(__file__)` at all — both take every input as an argument, which
`70-…:41` states is deliberate. No `__pycache__` shipped.

### 6.1 `scripts/validate_postman_artifacts.py` — 946 lines

**What it asserts, rule by rule.**

*Unconditional (no flag):*
1. The collection file parses and is a JSON object — else `EXIT_INPUT` (`:880-893`).
2. `info` exists and is an object; `info.name` is a non-empty string (`:641-646`).
3. `info.schema` contains `v2.1.0` **and** equals the canonical export marker exactly, with the
   Insomnia `No importers found for file` failure named in the message (`:649-657`).
4. Top-level `item` is a non-empty array (`:659-661`).
5. Each item is an object, has a name (warn if not), and contains either `request` or nested `item`
   (`:452-467`).
6. `request` is an object or a URL string (`:472-473`).
7. No executable script under `request.event` (`:493-498`).
8. Per scope, at most one `prerequest` and one `test` event, with the Insomnia-drops-the-second
   reason in the message (`:348-352`); unknown listeners warn.
9. `script.exec` is an array of strings (error) or a single string (warn) (`:365-375`).
10. No deprecated `postman.*` interface — 7 patterns (`:63-71`, `:305-310`).
11. No `pm.globals.` (`:311-315`).
12. Warn on `pm.vault`, `pm.require(`, `pm.state`, `pm.datasets`, `pm.visualizer` (`:74`, `:316-318`).
13. Warn once on `pm.response.to.have.` / `pm.response.to.be.` as an Insomnia-portability concern
    (`:75`, `:319-325`). — **see currency claim 12; this warning may now be pointing the wrong way.**
14. Every variable a script writes is declared in the collection or a supplied environment
    (`:387-391`).
15. Every `{{name}}` anywhere in the document is declared, `$`-prefixed dynamic variables excluded
    (`:164-172`, `:675-680`). — **see D-E.**
16. Saved responses: numeric `code`; a `body` key; an `originalRequest` whose method and raw URL
    match the request; no two examples sharing `(status, name)`, with the `x-mock-response-name`
    addressability reason given (`:556-606`).
17. Collection variables: secret-shaped value ⇒ secret finding; secret-like key with a non-placeholder
    value ⇒ warning; hyphenated key ⇒ Insomnia bracket-notation warning (`:682-702`).
18. Environments: `_postman_variable_scope == "environment"` (error, with the rejection reason);
    duplicate keys (error); hyphenated key (warn); `enabled: false` (warn, with the Insomnia drop
    reason); secret-shaped value (secret finding) (`:705-761`).
19. Credential shapes: JWT, `sk-…`, GitHub `ghp/gho/ghu/ghs/ghr/github_pat`, AWS `AKIA/ASIA`, Slack
    `xox[abprs]`, Google `AIza`, PEM private key, plus a high-entropy-under-a-secret-key heuristic
    (`:99-108`, `:232-250`) — scanned in auth blocks, headers, request bodies, example bodies,
    scripts, collection variables and environment values.
20. `Authorization` header with a literal value (no `{{`) ⇒ secret finding with the positive
    replacement in the message (`:429-434`).
21. Auth type outside the seven Insomnia-mapped types ⇒ warning (`:394-403`).
22. Official schema validation when `jsonschema` is installed and the URL is fetchable (`:764-779`).

*Flag-gated:* `--require-saved-responses`, `--require-success-example` (with the mock-default
consequence in the message), `--require-error-examples N`, `--require-tests`,
`--require-correlation-assertion`, `--require-token-capture` (fires only when a 2xx example body
contains one of `"access_token" "refresh_token" "id_token" "accessToken" "refreshToken"`),
`--require-success-guarded-captures`, `--require-doc-section HEADING` (repeatable, exact heading-text
match), `--require-secret-typing`, `--min-description-chars N`.

**Exit-code contract: HONOURED, with one hole.** `0/1/2` plus a documented `3` (schema failed) and
`4` (credential), priority `2 > 4 > 3 > 1 > 0` (`:935-941`, doc `60-…:99-111`). All could-not-run
paths return 2. **The hole:** when `jsonschema` is missing *or the fetch fails*, the strongest
structural check is downgraded to a **warning** and the run exits **0** (`:764-774`). Observed on
this host, at full strength, on a clean collection:

```
########## RUN 1: clean, full-strength ##########
Warnings (1):
- schema: skipped official schema validation because schema fetch failed: <urlopen error Tunnel connection failed: 403 Forbidden>
Counts: requests=1 saved_responses=2 with_success_example=1 with_error_example=1 with_tests=1 with_captures=1
Validation passed with no issues.
EXIT=0
```

`60-…:116-117` tells the *agent* to report the skip as a gap. There is no `--require-schema` flag, so
a **CI gate** on an air-gapped runner silently never validates against the schema and reports pass.
That is the exit-code contract's own stated failure mode: "A checker whose 'could not run' is
indistinguishable from its 'clean' is worse than no checker."

**Malformed / truncated / unexpected-schema input — the batch-7 defect class.** Observed verbatim:

```
########## VALIDATOR vs empty.postman_collection.json ##########   (valid v2.1, folders only, 0 requests)
Counts: requests=0 saved_responses=0 with_success_example=0 with_error_example=0 with_tests=0 with_captures=0
Validation passed with no issues.
EXIT=0                                                            <-- DEFECT (D-B)

########## VALIDATOR vs openapi.json ##########                    (an OpenAPI 3.1 document)
Errors (3):
- collection.info: missing `name`
- collection.info: expected a Postman Collection Format v2.1 schema URL
- collection: missing non-empty `item` array
EXIT=1

########## VALIDATOR vs insomnia.json ##########                   (an Insomnia v4 export)
Errors (2):
- collection: missing `info` object
- collection: missing non-empty `item` array
EXIT=1

########## VALIDATOR vs array.json ##########                      (top-level JSON array)
ERROR: collection `array.json` must contain a JSON object
EXIT=2

########## VALIDATOR vs malformed.json ##########
ERROR: cannot read JSON `malformed.json`: Expecting property name enclosed in double quotes: line 1 column 23 (char 22)
EXIT=2

########## VALIDATOR vs truncated.json ##########                  (first 400 bytes of a valid collection)
ERROR: cannot read JSON `truncated.json`: Expecting property name enclosed in double quotes: line 15 column 10 (char 400)
EXIT=2

########## VALIDATOR vs zero.json ##########                       (empty file)
ERROR: cannot read JSON `zero.json`: Expecting value: line 1 column 1 (char 0)
EXIT=2

########## VALIDATOR vs missing.json ##########
ERROR: cannot read JSON `missing.json`: [Errno 2] No such file or directory: 'missing.json'
EXIT=2
```

**Verdict on parse handling: correct in every case except the zero-request collection.** Truncation,
malformation, wrong top-level type, missing file and unexpected schema all produce a distinguishable
non-zero code. The single failure is D-B: a *structurally valid* collection with nothing in it.

**Does it find real defects?** Yes — 17 errors, 2 secret findings and 4 warnings on the broken
fixture, exit 4:

```
########## RUN 2: broken collection, full-strength ##########
Secret findings (2):
- collection.item[0] `Get Thing`: auth.hawk.authId carries a AWS access key id
- collection.item[0] `Get Thing`: header `Authorization` has a literal value; reference a declared variable such as `Bearer {{access_token}}` and populate it from a capture script
Errors (17):
- collection.info: use the Postman v2.1 export marker `https://schema.getpostman.com/json/collection/v2.1.0/collection.json`; Insomnia compares this string exactly and reports `No importers found for file` for any other value
- collection.item[0] `Get Thing`.event[0]: deprecated Postman interface `postman.setEnvironmentVariable`; Insomnia does not support it. Use the modern `pm.environment.*` equivalent.
- collection.item[0] `Get Thing`.event[0]: `pm.globals.*` is not part of either committed artifact and Insomnia does not support it. Write to `pm.environment.*` instead.
- collection.item[0] `Get Thing`.event[0]: script writes undeclared variable `g`; declare it in the collection or the environment
- collection.item[0] `Get Thing`.event[0]: script writes undeclared variable `undeclared_thing`; declare it in the collection or the environment
- collection.item[0] `Get Thing`.event[1]: a second `test` event in one scope is dropped by Insomnia's importer; merge it into the first one
- collection.item[0] `Get Thing`.request.event: Postman v2.1 never executes scripts here; move them to the request item's own `event` array
- collection.item[0] `Get Thing`: request description has 5 characters; minimum is 400
- collection.item[0] `Get Thing`: description has no `Purpose` section heading
- collection.item[0] `Get Thing`: description has no `Errors` section heading
- collection.item[0] `Get Thing`: tests never reference `X-Request-Id`, so the mandatory correlation header is unasserted
- collection.item[0] `Get Thing`.response `Error`: saved response has no numeric `code`
- collection.item[0] `Get Thing`.response `Error`: saved response has no `body` field
- collection.item[0] `Get Thing`.response `Error`: originalRequest method `POST` does not match `GET`
- collection.item[0] `Get Thing`.response `Error`: originalRequest URL does not match the request URL
- collection.item[0] `Get Thing`: no saved example with a 2xx status; a mock server would serve an error example as its default response
- collection: variable `{{thing_id}}` is referenced but declared in neither the collection nor any environment input; declare it or pass --allow-external-var
Warnings (4):
- collection.info: no collection description; the environment contract has nowhere to live
- collection.item[0] `Get Thing`.event[0]: `pm.response.to.have.` is Postman-current but unverified after Insomnia's `pm.`-to-`insomnia.` rewrite; prefer `pm.expect(pm.response.code)`
- collection.item[0] `Get Thing`: auth type `hawk` is not mapped by Insomnia's importer and arrives as no auth; use basic, bearer, apikey, digest, oauth1, oauth2, or awsv4
- collection.variable `base-url`: Insomnia rewrites a hyphenated name into bracket notation; use snake_case
Counts: requests=1 saved_responses=2 with_success_example=0 with_error_example=1 with_tests=1 with_captures=1
EXIT=4
```

Every message names the failure *and* its consequence. This is the strongest checker in the batch by
message quality.

**Flag-value validation.** Correct, and exits 2:
```
$ python3 validate_postman_artifacts.py clean.postman_collection.json --max-findings 0
ERROR: --min-description-chars and --require-error-examples must be >= 0, --max-findings >= 1
EXIT=2
$ … --require-error-examples -1        → same message, EXIT=2
$ … --min-description-chars abc        → argparse: invalid int value: 'abc'   EXIT=2
```

### 6.2 `scripts/audit_collection_contract.py` — 445 lines

**What it asserts.** A strict subset, every finding an error: exact `info.schema`; per-request
minimum description length (default 120); no scripts under `request.event`; event structure —
listener in `{prerequest, test}`, no duplicate listener per scope, `script.exec` an array of strings;
no deprecated `postman.*` interface (4 patterns, `:16-18`); no script writing an undeclared variable;
`--require-success-guarded-captures`; `--require-saved-responses`; each saved response has a numeric
`code`, a `body` key, and an `originalRequest` whose method and URL match;
`--forbid-description-hint TEXT` scanned across **every** description in the document
(`walk_descriptions`, `:198-211`); and per-collection counts. Accepts multiple `LABEL=path` inputs
for an aggregate run.

**What it deliberately does not assert:** no secret checks, no environment file checks beyond reading
declared keys, no `pm.globals` check (its `VARIABLE_SET_RE` at `:19-21` excludes `globals` — drift
from the validator), no schema validation, no doc-section headings, no example coverage by status.

**Exit-code contract: VIOLATED.** Line 440 returns `1 if any finding else 0`; line 409 returns `1`
for every could-not-run. Observed verbatim — note that the last two cases are "the tool could not
run", not "the artifact is bad":

```
########## AUDITOR vs clean ##########
sample: requests=1 saved_responses=2 scripted_requests=1 errors=0
EXIT=0

########## AUDITOR vs broken ##########
broken: requests=1 saved_responses=2 scripted_requests=1 errors=10
  ERROR: collection: info.schema must equal `https://schema.getpostman.com/json/collection/v2.1.0/collection.json`
  ERROR: GET Get Thing: description has 5 characters; minimum is 120
  ERROR: GET Get Thing: scripts are under request.event; Postman v2.1 executes item-level event scripts
  ERROR: GET Get Thing.event[1]: duplicate `test` listener in the same scope
  ERROR: GET Get Thing: script uses a deprecated Postman interface
  ERROR: GET Get Thing: script writes undeclared variable `undeclared_thing`
  ERROR: GET Get Thing: saved response 1 has no numeric HTTP code
  ERROR: GET Get Thing: saved response 1 method `POST` does not match `GET`
  ERROR: GET Get Thing: saved response 1 originalRequest URL does not match the request URL
  ERROR: GET Get Thing: saved response 1 has no body field
EXIT=1

########## AUDITOR vs empty (folders only) ##########
empty: requests=0 saved_responses=0 scripted_requests=0 errors=1
  ERROR: collection: collection contains no request items
EXIT=1                                                             <-- correct; the validator misses this

########## AUDITOR vs malformed.json ##########
ERROR: cannot read Postman JSON `malformed.json`: Expecting property name enclosed in double quotes: line 1 column 23 (char 22)
EXIT=1                                                             <-- should be 2

########## AUDITOR vs truncated.json ##########
ERROR: cannot read Postman JSON `truncated.json`: Expecting property name enclosed in double quotes: line 15 column 10 (char 400)
EXIT=1                                                             <-- should be 2

########## AUDITOR vs zero.json ##########
ERROR: cannot read Postman JSON `zero.json`: Expecting value: line 1 column 1 (char 0)
EXIT=1                                                             <-- should be 2

########## AUDITOR vs array.json ##########
ERROR: Postman artifact `array.json` must contain a JSON object
EXIT=1                                                             <-- should be 2

########## AUDITOR vs missing.json ##########
ERROR: cannot read Postman JSON `missing.json`: [Errno 2] No such file or directory: 'missing.json'
EXIT=1                                                             <-- should be 2

########## AUDITOR vs openapi.json ##########
x: requests=0 saved_responses=0 scripted_requests=0 errors=2
  ERROR: collection: info.schema must equal `https://schema.getpostman.com/json/collection/v2.1.0/collection.json`
  ERROR: collection: collection contains no request items
EXIT=1

########## AUDITOR vs insomnia.json ##########
x: requests=0 saved_responses=0 scripted_requests=0 errors=2
  ERROR: collection: info.schema must equal `https://schema.getpostman.com/json/collection/v2.1.0/collection.json`
  ERROR: collection: collection contains no request items
EXIT=1

########## AUDITOR: unreadable ENVIRONMENT, valid collection ##########
ERROR: cannot read Postman JSON `malformed.json`: Expecting property name enclosed in double quotes: line 1 column 23 (char 22)
EXIT=1                                                             <-- should be 2; the collection was never audited

########## AUDITOR: --summary-only on unreadable input ##########
ERROR: cannot read Postman JSON `malformed.json`: …
EXIT=1
```

**No parse failure yields exit 0 in either script.** The batch-7 signature — "No issues found, exit
0, on input it silently abandoned" — is **absent for malformed input in both scripts**. It is present
only in the two structural forms D-B (zero-request collection, validator) and D-A (vacuous success
guard, both scripts), and in the schema-skip hole. That is a materially better result than batch 7's
finding, and Phase 2 should close the three remaining holes rather than rebuild.

### 6.3 Windows

**What is already Windows-correct, and deliberately so.**
- `path.read_text(encoding="utf-8-sig")` in both (`validate:146`, `audit:93`) strips the UTF-8 BOM
  that PowerShell `Out-File` and `Set-Content` emit by default. Without it every collection written
  from PowerShell would fail to parse.
- No `os.path` separators, no `subprocess`, no shell out, no `Path(__file__)`, no file writes.
- CRLF is handled correctly. `HEADING_RE` (`validate:37`) captures `Purpose\r` under
  `re.MULTILINE`, and `heading_names()` (`:262`) calls `.strip()`, which removes the `\r`. Verified
  with a CRLF + BOM fixture; both scripts pass it:
```
########## CRLF + UTF-8 BOM collection (Windows PowerShell Out-File shape) ##########
Counts: requests=1 saved_responses=2 with_success_example=1 with_error_example=1 with_tests=1 with_captures=1
Validation passed with no issues.
EXIT=0
########## auditor on same ##########
w: requests=1 saved_responses=2 scripted_requests=1 errors=0
EXIT=0
```
  This closes the second of the two Windows-only defect classes the brief names.

**What is not Windows-correct: the documented invocation.**
`60-…:32-33` says: *"Invoke with `python3`; `python` is absent on many hosts and resolves to Python 2
on some."* Both bullets are Unix reasoning. On Windows, `python3` is commonly the Microsoft Store
alias stub, which opens the Store and exits without running anything; the reliable launcher is
`py -3`. Every one of the six command blocks in the skill (`41-…:104`, `42-…:147`, `43-…:85`,
`44-…:72`, `60-…:78`, `60-…:134`) uses `python3` and a `$SKILL_DIR/...` path. `$SKILL_DIR` happens
to interpolate in PowerShell but not in `cmd.exe`, and the forward slashes are fine.

**Minimum Python.** `str.removeprefix` (`validate:243`) requires **3.9+**. Nothing in the skill
states a minimum. On a Windows host with 3.8 the validator raises `AttributeError` mid-run.

### 6.4 Checker count for the batch survey

**Two executable checkers.** Both run. Both find real defects on first execution against a
deliberately broken artifact. Neither ships a self-test, so neither satisfies the "per-script
self-test whose target exits 2 records BLOCKED" clause of the exit-code contract.

---

## 7. The inherited live defect — hardcoded model name in a generated environment file

Project memory records: `gateway/scripts/postman/generate_gateway_collection.sh` around line 1799
hardcodes a model name into generated environment files, and needs a regeneration to fix. That file
is outside this repository and was **not** edited, inspected or reachable — the `gateway` repository
is not among the four folders mounted on this device (`alaa-go-chi`, `service-ci-kit`,
`service-runtime-kit`, `skills`).

**Is `alaa-postman-collections` the skill that should have caught it? Yes, on three of its own
statements.**

1. `references/10-scope-and-trigger-rules.md:10` — *"This skill owns: … Postman environment JSON
   artifacts"*. A generated environment file is a Postman environment JSON artifact.
2. `references/10-scope-and-trigger-rules.md:61-69`, the generated-artifact rule — *"treat the script
   and its declared inputs as the editable source of truth… Patch the generator… Regenerate… Review
   the generated JSON diff"*. A hardcoded constant in a generator is precisely the class this rule
   governs.
3. `references/70-aggregate-collections-and-consumer-repos.md:77` **names the exact file**:
   > `The \`gateway\` repository is the reference implementation. \`scripts/postman/generate_gateway_collection.sh\` merges eight service-local collections into one gateway-facing aggregate under \`docs/postman/\`…`

So the skill names the defective generator as its reference implementation and has no rule and no
check that would find the defect in it.

**Would either script detect it today? No.** Grep for `model|gpt|claude|sonnet|opus|llm` across both
scripts: **zero matches**. Proved with a fixture environment carrying `llm_model = "gpt-4o-mini"`
alongside a real-shaped key and two known-detectable defects, so the run is not silent for the wrong
reason:

```
########## VALIDATOR vs gateway env (hardcoded model + real key + parked + hyphen) ##########
Secret findings (1):
- environment `gateway.postman_environment.json` `openai_api_key`: carries a high-entropy value under a secret-like key
Errors (2):
- environment `gateway.postman_environment.json` `openai_api_key`: secret-like variable is not typed `"type": "secret"`, so Postman shows its value in plain text
- collection.item[0] `Create Token`.event[0]: script writes undeclared variable `access_token`; declare it in the collection or the environment
Warnings (2):
- environment `gateway.postman_environment.json` `parked_var`: `enabled` is false, so Insomnia's importer drops it; delete it or give it a placeholder value
- environment `gateway.postman_environment.json` `base-url`: Insomnia rewrites a hyphenated name into bracket notation; use snake_case
EXIT=4
```
and with the API key removed, isolating the model name:
```
Errors (1):
- collection.item[0] `Create Token`.event[0]: script writes undeclared variable `access_token`; …
Warnings (2):
- … `parked_var`: `enabled` is false …
- … `base-url`: Insomnia rewrites a hyphenated name …
EXIT=1
```
**`llm_model = "gpt-4o-mini"` produces no finding of any kind.** The auditor is worse: it reads an
environment only to harvest declared keys (`:390-393`) and never validates a single value.

**The assertion Phase 2 must add.** A new validator check —
`--forbid-pinned-vendor-identifier` (default **on**, since it is a correctness rule, not a
preference) — that fails any collection variable or environment value matching a vendor-model or
vendor-version identifier pattern, with the message naming the positive replacement: *declare the
value as a generator input and reference `{{model_name}}`*. The rule text belongs in
`30-variables-auth-and-environments.md` as a sixth environment-completeness condition:
**"No committed environment value is an implementation constant the generator should own."**

The check must be added to `validate_postman_artifacts.py`, **not** `audit_collection_contract.py`,
per `SKILL.md:151-153` and `60-…:148-154`, because the auditor has byte-identical copies in consumer
repositories that cannot be updated from here.

The **model-name pattern list itself must not be written into this skill** — that is defect class 1.
Route it: the rule detects *any pinned vendor identifier in a committed environment value*, and where
a model name is legitimately needed, `alaa-prompting-guide` `references/90-model-selection.md` owns
which one. `SKILL.md:143-144` already establishes that routing.

---

## 8. The Phase 2 work order

Target: **no growth**. Current total 173 KB. Every addition below is paid for by a subtraction.

### 8.1 Files rewritten

| File | Change | Δ bytes |
|---|---|---|
| `SKILL.md` | Cut the body from 157 to ≤120 lines by moving the 9-step "Minimal deterministic workflow" (lines 94-111) into `10-scope-and-trigger-rules.md` as `## The deterministic workflow`, leaving a one-line pointer. Add `alaa-laravel-public-api-contract-pack` and `alaa-testing-strategy` to the companion-routing block. Amend the description's final clause to name the Laravel contract-pack boundary. | −900 |
| `references/25-public-api-contract-and-sdk-readiness.md` | Rewrite the opening scope paragraph (lines 1-3, 20-22): on a Laravel service, `alaa-laravel-public-api-contract-pack` owns the canonical contract, its location, versioning and emission gate — this skill owns the Postman projection and proves parity against it, and runs *that* skill's `scripts/contract_pack_audit.py` for `openapi_postman_divergence` rather than defining a competing gate. Keep the file whole for non-Laravel repositories, and say so. Restructure `## Request completeness` / `## Response completeness` / `## Cross-cutting SDK semantics` (D5) from three flat bullet lists into failure classes: what an SDK author gets wrong, how you detect it, the smallest fix. | −1 200 |
| `references/43-response-tests.md` | Replace the doctrine sentence at line 9 with a routed pointer to `alaa-testing-strategy` `SKILL.md` (both trigger forms), keeping the five Postman-specific minimum assertions and the keep-out list, which that skill explicitly cedes. Fix the double comma at line 35. **Hold the "portable assertion form" section (lines 58-70) pending open question Q1** — do not rewrite it until `insomnia.response.code` vs `.status` is settled from source. | −500 |
| `references/50-insomnia-compatibility-and-free-plan-rules.md` | Re-date the verification block to the Phase 2 date and pin **Insomnia 12.6.0 (2026-05-22)** alongside the `master` reference. Replace the `insomnia-importers@3.6.0` command (line 158) — the package is deprecated (currency claim 14). Add the two missing Insomnia free-tier limits (Git Sync ≤3 users; 1,000 mock requests/month) and the four missing Postman free-plan limits (10,000 API calls/month, 1,000 monitoring requests/month, single user, 1-day recovery). Add a one-paragraph note that **collection schema 3.0.0 is Postman's current format** and state why this skill pins 2.1 (Insomnia's importer accepts only v2.0/v2.1; Newman runs only 2.1) with the re-derivation command. | +400 |
| `references/60-validation-and-output-contract.md` | Correct the auditor exit-code table: 2 for could-not-run, not 1. Add a `newman run` step to the validation ladder between steps 6 and 7, with its exit-code mapping and the note that Newman cannot run 3.0 collections. Replace the deprecated `insomnia-importers` command. Add the Windows invocation form (`py -3`) beside `python3` and state the Python 3.9 minimum. Document the new flags. | +600 |
| `references/30-variables-auth-and-environments.md` | Add a sixth environment-completeness condition: no committed environment value is an implementation constant the generator should own (§7), with the positive replacement and the routing for model names. | +400 |
| `references/42-scripts-and-state-capture.md` | Add the concurrency rule missing under criterion 5: one writer per variable name; a namespaced variable where a folder may run in parallel; an explicit statement that within a folder the collection assumes serial execution. | +400 |
| `references/90-source-map.md` | Add `https://learning.postman.com/docs/use/use-collections/collections-schemas` (the 3.0 page) and the npm registry endpoints used to re-derive the Newman and importer pins. Mark the two `insomnia-importers` references retired. | +300 |
| `scripts/validate_postman_artifacts.py` | Five changes, §8.3. | +2 000 |
| `scripts/audit_collection_contract.py` | **One change only, and it must be propagated in the same task.** `:409` → `return 2`. Nothing else, per `SKILL.md:151-153`. The change requires a byte-identical re-sync of every consumer copy and a rerun of that repository's gate before closing (`70-…:37-48`). | +1 |

### 8.2 Files created

| File | Contents | Bytes |
|---|---|---|
| `scripts/selftest.py` | The missing per-script self-test. Ships two in-memory fixture pairs per script — one clean, one deliberately broken — asserts the clean pair exits 0 and the broken pair exits non-zero with the expected finding substrings, and asserts that a truncated fixture exits **2**. A target that exits 2 records **BLOCKED**, and the harness then exits 2 rather than 1. Writes only to `tempfile.mkdtemp()` outside the repository. | ~5 000 |

**No file is retired to `_to_delete/`.** Every reference earns its place; the changes are edits.

### 8.3 What the new script assertions must be

In `validate_postman_artifacts.py`:

1. **Close D-B.** After `walk_items`, if `report.counts["requests"] == 0`, emit an error:
   `collection: contains no request items, so every --require-* flag passed vacuously`. Port the
   check from `audit_collection_contract.py:373-374`. Five lines; closes the clean-on-empty hole.
2. **Close D-A.** Replace the textual `SUCCESS_GUARD_MARKERS` test with a structural one: the guard
   is satisfied only when a `pm.response.code` comparison appears **before** the first
   `pm.environment.set` / `pm.collectionVariables.set` in the script text *and* that comparison is
   part of a control-flow construct (`if (`, `? :`, or an early `return`). A bare assertion after the
   write must fail. Add the regression fixture from `/tmp/pm/fakeguard.postman_collection.json` to
   `selftest.py` — the fixture that currently passes both gates must fail after the fix.
3. **Close the schema hole.** Add `--require-schema`: when set, a skipped schema validation (missing
   `jsonschema` or a failed fetch) returns **2**, not 0. Document it as the CI-recommended flag.
4. **Close D-C.** Extend `--require-doc-section HEADING` so a heading with fewer than N non-whitespace
   characters of body before the next heading fails, with N a new `--min-section-chars` (default 0,
   so existing invocations do not change behaviour).
5. **Close D-E.** Attach an item scope to every undeclared-variable finding, and split the check into
   two severities: a reference in an *executable* position (URL, header, query, body, auth, script)
   is an **error**; a reference inside a `description` or a saved-example body is a **warning**
   naming the request. Add `--strict-prose-variables` to raise the warning to an error.
6. **Add §7's assertion.** `--forbid-pinned-vendor-identifier`, default on.

### 8.4 Byte budget

Rewrites net **−700**; creations add **~5 000**; script growth adds **~2 000**. Net **+6 300** on
173 000, i.e. **+3.6 %**.

**The capability that earns it:** the skill gains a self-test harness it does not have today, and
three assertions that close three proven holes — a checker that passed a zero-request collection at
full strength, a gate that could not fail on any collection following this skill's own template, and
a CI path that reported pass while the strongest structural check never ran. That is a genuinely new
capability under section 7's growth clause, and it should be named as such in the Phase 2 report.

---

## 9. Open questions for the owner

**Q1. Is `insomnia.response.code` real?** *(Blocking for two files and both assets.)*
`50-…:102-103` and `43-…:60-70` build the "portable assertion form" rule on a documented Insomnia
example that is no longer on the page; the page now shows `insomnia.response.status`. If `code` does
not exist on Insomnia's response object, the skill's recommended form is the non-portable one and its
discouraged form is no worse.
**Recommendation:** settle it from the SDK source before Phase 2 edits either asset — the skill's own
rule (`90-…:59-61`) says the source is the answer. I could not reach
`packages/insomnia-sdk/src/objects/response.ts` (404 on `master` and `main`); it has moved.
**Trade-off:** guessing either way is cheap to write and expensive to unwind, because both bundled
assets and a validator warning currently push every agent toward `pm.response.code`. If the source
cannot be located, the honest interim is to state **both** forms as unverified and drop the warning
at `validate:319-325` rather than keep asserting a preference the evidence no longer supports.

**Q2. Who owns the canonical public API contract on a Laravel service?**
`alaa-laravel-public-api-contract-pack` has already declared the split in its own frontmatter and
four reference call sites; this skill has not acknowledged it and claims mandatory ownership at
`25-…:3`.
**Recommendation:** the Laravel pack owns *what the contract is*; this skill owns *how the collection
proves it*, and runs the Laravel pack's `contract_pack_audit.py` for parity instead of defining a
competing SDK-readiness gate. **Reason:** that pack's gate is route-inventory-driven from
`php artisan route:list --json`, evidence this skill cannot obtain.
**Trade-off:** the alternative — this skill keeps `25-…` whole and the Laravel pack drops its OpenAPI
claim — would need edits to a Batch 2 skill already at standard, and would remove the emission gate
on unresolved deprecation, which is the stronger control. I do not recommend it.

**Q3. Should the collection actually be executed, and by what?**
Newman appears at zero call sites. Newman 6.2.2 (2026-01-16) runs 2.1 collections; the Postman CLI is
required for 3.0.
**Recommendation:** add a Newman step to the validation ladder, optional but with a stated exit-code
mapping, and a rule that a collection whose tests have never been executed is reported as such in the
output contract.
**Trade-off:** running the collection needs a live service, which the skill has so far deliberately
avoided depending on — every current check is static and offline-capable. Adding an execution step
that is *required* would make the skill unusable in a repository with no runnable environment. Adding
it as *reportable* costs nothing and closes criterion 1.

**Q4. Should the exit-code correction to `audit_collection_contract.py` ship now?**
It is a one-character fix that closes a contract violation, but `70-…:37-48` requires every consumer
copy to be re-synced byte-identically **in the same task**, and no consumer copy is reachable from
this device (`find` over all four mounts: zero hits).
**Recommendation:** ship it, and make the Phase 2 report list the re-sync as an explicit outstanding
obligation on the `gateway` repository rather than closing the task silently.
**Trade-off:** deferring keeps the copies in sync at the cost of leaving a documented contract
violation in the strict gate; shipping fixes the gate at the cost of a known-divergent copy until the
gateway repository is next touched. The divergence is one return value and is detectable by the
`diff -u` command the skill already prescribes at `70-…:45`.

**Q5. Should the routing convention (≥9 references ⇒ `00-topic-map.md`) be mandatory fleet-wide?**
This skill is evidence *for*: 13 references, and its topic map is keyed on "About to write", which is
faster than a file-number index. Deferred to the survey lane; recorded here as a data point.


---

# Appendix E — `alaa-basic-memory-os`

# Lane L5 — `alaa-basic-memory-os`

Analysis date: **2026-07-29**. Read-only phase. Nothing on the device was modified.

Staged copy read in full: `/home/claude/b8/src/alaa-basic-memory-os/` (16 files, 29,757 bytes).
Device original inspected read-only through `mcp__remote-devices__device_bash` at
`/sessions/rcw-01nfpk8ndxrrswndyp6txjwc/mnt/skills/skills/sohrab/alaa-basic-memory-os/`.

PowerShell 7.4.6 was installed into this container (`/opt/pwsh/pwsh`, from the official
`powershell-7.4.6-linux-x64.tar.gz`) so that every claim about the six scripts is executed, not
inferred. Every script result below was observed, not reasoned about.

---

## 0. The store-replacement recommendation (read this first)

### Recommendation: rewrite this skill as the **memory operating model**, store-agnostic, and give it a new name

Of the three candidates in the lane brief, take the third: **the skill owns what is remembered, when,
in what shape, and what is derived rather than remembered — and the backing store is a swappable
implementation detail behind a thin adapter reference.** Basic Memory and Hindsight each get one
adapter reference; neither owns the body.

**Why, from the evidence in this directory rather than from taste:**

1. **The fleet's inbound contract is already store-agnostic.** The only upgraded skill that routes to
   this one describes it without naming a store:
   `alaa-golang/references/20-sohrab-companions.md:19` —
   `| `/alaa-basic-memory-os` (`$alaa-basic-memory-os`) | record a drift note, a decision, or context that a later session must find |`
   and `alaa-golang/references/05-what-this-skill-does-not-own.md:77` — "a durable record belongs in
   the reference file that now states the rule, or in a note through `/alaa-basic-memory-os`
   (`$alaa-basic-memory-os`) when the decision outlives the task." Neither sentence would change if
   the store changed. Both sentences break if the *skill name* changes — so the rename has a
   measurable, enumerable cost (see below) and the store swap does not.

2. **The durable value in this directory is store-independent, and the store-dependent parts are the
   defective ones.** The drift model (`references/drift-management.md`, 2,285 bytes), the
   Extraction/Design mode split (`SKILL.md:61-72`), the "repo is truth, memory is a map" rule
   (`SKILL.md:31`), and the do-not-store list (`references/operating-model.md:30-41`) are policies
   about *knowledge*. Every one survives the swap unchanged. By contrast every asserted CLI command,
   every script, and `references/cli-and-mcp.md` in its entirety are `bm`-shaped and die with the
   store — and those are exactly the files carrying the defects in §3 and §6.

3. **Rewriting in place as a Hindsight skill imports Hindsight's instability into the fleet.**
   Hindsight is 0.x. `hindsight-api` shipped **0.8.6 today, 2026-07-29** (§5) — one patch newer than
   the version the project-memory record names, released while this batch was being planned. A skill
   whose body is Hindsight mechanics needs re-verification on roughly a weekly cadence. A skill whose
   body is the memory operating model needs re-verification when the owner's *policy* changes, which
   is roughly never, and whose single adapter reference carries the weekly churn in one file.

4. **The one thing that must not be lost is the drift model, and it is the thing Hindsight most
   directly threatens** (§2). Making it store-owned would put it at risk in the migration. Making it
   store-independent protects it.

**Concretely:** retire `alaa-basic-memory-os`, create `alaa-memory-os` with the body owning the
operating model, `references/store-basic-memory.md` and `references/store-hindsight.md` as the two
adapters, and one line in the new skill's frontmatter description naming both stores so the trigger
still fires on either. Keep a 3-line `alaa-basic-memory-os/SKILL.md` stub pointing at the new name
until the two `alaa-golang` call sites and the two READMEs are updated, then move the stub to
`_to_delete/`.

**What each option costs:**

| Option | Cost | What it buys |
|---|---|---|
| **Rewrite in place as a Hindsight skill under a new name** (`alaa-hindsight-memory`) | Same rename cost. Body churns with a 0.x product on a weekly release cadence; D10 re-verification becomes a recurring tax on every future batch. Basic Memory knowledge is deleted before the migration has actually run, so a rollback has nothing to roll back to. | Shortest file. Simplest to write. |
| **Keep the Basic Memory skill, add a separate successor skill** | Two skills asserting the same policy in two places — the exact duplication defect class 3 exists to catch, but across a skill boundary where no checker can see it. The fleet then has two answers to "where does a decision go", which is the failure `alaa-golang:79-80` explicitly names ("which is how one platform grows two answers to one question"). Doubles the boundary-statement surface that §4 shows is already stale. | Zero migration risk; both stores work on day one. |
| **Store-agnostic memory operating model** (recommended) | Rename cost: 4 known call sites (`alaa-golang/references/05-...md:77`, `alaa-golang/references/20-...md:19`, `skills/sohrab/README.md:117`, `skills/sohrab/README.fa.md`) plus `UPGRADE-CARRYOVER.md:107,197,216`. One extra indirection hop for anyone who only wants the `bm` command list. Requires the owner to state the migration cutover date so the adapter files can be marked active/deprecated. | Policy survives the swap. Weekly Hindsight churn is confined to one reference. Both stores documented during the transition without duplicating policy. |

**One decision that is genuinely the owner's and that this recommendation depends on:** whether the
`alaa-memory` Basic Memory vault's existing notes are migrated into the `alaa-memory` Hindsight bank
or left as a frozen archive. It matters here because the historical import is the one operation that
*cannot* go through the official plugins — they never send `timestamp`, so a plugin-driven import
would stamp every historical note with import time and hand Reflect's "latest `mentioned_at` wins"
rule a flat, useless ordering. See §8 Q1.

---

## 1. Inventory

Total 29,757 bytes. All files are LF-terminated; none carry a UTF-8 BOM.

| File | Bytes | What it actually contains |
|---|---:|---|
| `SKILL.md` | 6,326 | Frontmatter (569-char description) plus a 140-line body holding nine rule blocks: purpose, use/do-not-use, core rules, task-start, note creation, contract mode (Extraction vs Design), drift, Prompt-3 publishing, end-of-work, a 13-name vendored-skill routing list, a bare reference index, and eight completion checks. Roughly half of it is restated in `references/`. |
| `agents/openai.yaml` | 224 | Three keys: `version`, `name`, `description`. **No `interface:` block** — no `short_description`, no `default_prompt`. Fails the repository validator twice. |
| `references/cli-and-mcp.md` | 1,196 | Seven `bm` health commands, a "do not use `basic-memory sync`" block, six `bm tool` search/context invocations, one `bm mcp` streamable-HTTP invocation bound to `127.0.0.1:8000`, and one `codex mcp add` line. Entirely store-specific; dies with the store. |
| `references/compact-and-handoff.md` | 625 | Restates that long work needs state written before compaction, concedes `alaa-workflow` is authoritative, then defines a six-field handoff pointer that duplicates `alaa-workflow`'s six-field handoff package, and points at `scripts/precompact_checkpoint.ps1`. The only file in the repository that mentions that script. |
| `references/drift-management.md` | 2,285 | The drift mechanism: definition, the never-silently-pick-a-side rule, four high-priority domains with default severities, the note model and its `drift_status` lifecycle, the registry, the prompt 13/14/15 workflow, three queries, and four prohibitions. The most valuable file here. |
| `references/note-governance.md` | 1,419 | Required frontmatter keys, status and confidence enumerations, an 18-label observation vocabulary, typed-relation examples, and a repeat of the drift-marker rule. Substantially restates the vendored `memory-notes` skill. |
| `references/obsidian-usage.md` | 807 | Vault roles, YAML link-quoting rule, template location (`00-control/templates/`), graph-hygiene advice. |
| `references/operating-model.md` | 1,187 | The four-surface model as a fenced text block, four absolute `D:/Sohrab/Project/...` vault paths, an eight-item store list and an eleven-item do-not-store list. |
| `references/prompt-3-publishing.md` | 944 | Prompt-3 inputs (three `raw/processed/_global/*` paths), five output note paths, a five-item do-not-publish list, four curation labels, and the "lessons stay advisory until promoted" rule. |
| `references/skill-boundaries.md` | 814 | Four ownership paragraphs (`alaa-workflow`, `alaa-low-noise`, Basic Memory, Basic Memory skills) and a verbatim repeat of the 13-name vendored-skill list already in `SKILL.md:104-119`. |
| `scripts/alaa_memory_health.ps1` | 1,762 | Runs `bm status --wait`, `bm doctor`, then `bm schema validate` over 12 hardcoded note types, optional `bm orphans`, then lists drift notes. **Contains a reproduced logic bug (§6-A) and a reproduced exit-code inversion (§6-B).** |
| `scripts/alaa_memory_post_task.ps1` | 974 | `Push-Location` into a hardcoded `D:\Sohrab\Project\agent-memory`, optional `bm reindex`, `bm status --wait`, per-type `bm schema validate`, `bm doctor`, then `git status --short` and `git diff --stat`. |
| `scripts/alaa_memory_reindex.ps1` | 522 | `bm reindex -p`, `bm status --wait`, `bm doctor`; throws on any failure. |
| `scripts/alaa_obsidian_linkcheck.ps1` | 5,173 | A read-only wikilink/orphan/missing-Relations checker over the vault. The only real checker in the skill. **Ends with two NUL bytes; observed to exit 1 on a clean vault and, once the NULs are stripped, 0 on a vault with a broken link (§6-C).** O(notes × links) incoming-link crediting. |
| `scripts/precompact_checkpoint.ps1` | 3,887 | A `PreCompact` hook: reads hook JSON from stdin, derives repo/branch/git status, writes a `type: inbox_capture` note file into `<vault>/inbox/agent-captures/`, optionally appends a redacted 40-line transcript tail behind `ALAA_MEMORY_INCLUDE_TRANSCRIPT_TAIL=1`, then emits hook JSON and always exits 0. |
| `scripts/session_start_context.ps1` | 1,612 | A `SessionStart` hook: emits a seven-line governance reminder on stdout, optionally noting that open drift notes may exist. Always exits 0. |

Two structural facts about the inventory:

- **Neither hook script is registered anywhere in the repository.** A narrow device grep over
  `skills/` and `docs/` returned exactly one hit outside the scripts directory —
  `references/compact-and-handoff.md:26` — and it is prose, not a `settings.json` hooks entry. There
  is no installation snippet in the skill. An agent reading this skill cannot install the hooks.
- **No `__pycache__`, no temp dirs inside the repository, no `Path(__file__).parents[N]`** — defect
  classes 7 and 8 are clean.

---

## 2. `references/drift-management.md` — the mechanism, and whether it survives Hindsight

### What it actually defines

Not a checker, and not a Basic Memory feature. It defines a **human-arbitrated two-source
reconciliation protocol with a mandatory audit trail**, in five parts:

1. **A definition** (`:3`): "Drift = a recorded mismatch between two sources of truth: doc vs code,
   memory vs repo, service vs service, shared architecture doc vs actual behavior."
2. **A prohibition with a positive replacement** (`:7`): "Never silently pick a side when sources
   disagree. Record the drift, keep working on the safest verified behavior, and let the human
   decide." This sentence is the strongest in the skill — it survives the wording test intact.
3. **A durable record with a state machine** (`:19`):
   `drift_status: open → analyzed → decided → fixing → resolved`, severity `low|medium|high|critical`.
4. **Bidirectional marking** (`:20-22`): each affected note gets exactly one
   `- [drift] see [[<drift note>]]` observation and `status: needs_review`; the drift note carries
   `part_of`, `conflicts_with`, later `resolved_by`; `drift/Drift Registry.md` keeps the open list.
5. **A separation of powers** (`:26-28`, `:40-41`): prompt 13 records, prompt 14 analyses and waits
   for human approval, prompt 15 fixes code **and** docs per repository. "Do not fix code during
   prompts 13/14." "Do not resolve a drift note while any affected project remains unfixed."

The mechanism's real content is: **a disagreement becomes a first-class, queryable, non-deletable
object with an owner and a lifecycle, and no agent may close it.**

### Does it survive the move to Hindsight? Partly — and the part that does not is the part that matters

| Component | Survives? | Why |
|---|---|---|
| The definition and the never-pick-a-side rule | **Yes** | Store-independent policy. Move verbatim into the new body. |
| Extraction vs Design mode | **Yes** | Store-independent. |
| The `[drift]` marker on affected notes | **No, not as written** | There are no author-controlled notes in Hindsight. You retain *content*; Hindsight extracts facts. You cannot append an observation to a memory you did not shape. The nearest primitive is `PATCH /v1/default/banks/{bank_id}/memories/{memory_id}` (curation: edit/invalidate/restore — verified in the 0.8.6 OpenAPI spec, §5). |
| `drift_status` as a queryable field | **No** | Verified: only `tags` are filterable at recall; `metadata` is not (`developer/api/recall.md:28` documents `metadata` as returned, and the whole tag-filter section `:327-527` is about `tags` alone). A lifecycle carried in `metadata` becomes invisible to the query that drives the workflow. It must be carried in `tags` — e.g. `drift:open`, `drift:analyzed` — and re-tagging means re-retaining the document under the same `document_id`. |
| `bm tool search-notes --type drift --meta drift_status=open` | **No** | Has no Hindsight equivalent. Replaced by recall with `tags=["drift","drift:open"]` and **`tags_match="all_strict"`** — verified `developer/api/recall.md:480-497`: `any` (the default) "Returns memories that have at least one matching tag, plus untagged memories", and `all_strict` "Returns memories that have every specified tag, and excludes untagged memories". Using the default here would return the entire bank. |
| The registry file and the audit trail | **No** | "Do not delete drift notes; archive them (audit trail)" (`:42`) cannot be enforced inside Hindsight. Consolidation actively rewrites: observations are "refined — not overwritten — when new evidence supports, contradicts, or extends them" (`best-practices.md:39`), which is the opposite of an immutable audit record. |

### The collision with Reflect's supersession rule

Hindsight's supersession is **latest `mentioned_at` wins**, and `mentioned_at` comes from the item's
`timestamp` (verified: `MemoryItem.timestamp` exists in the 0.8.6 OpenAPI schema;
`developer/api/retain.md:136` describes the timestamp as the temporal anchor; `recall.md:33`
documents `mentioned_at` as "ISO datetime of when the fact was retained").

Drift is the case where **the newest statement is not the true one.** A drift note exists precisely
because two sources disagree and nobody has yet decided which is right. Feed both sides into one
bank and Hindsight will silently resolve the disagreement by timestamp — which is exactly the
behaviour `drift-management.md:7` forbids: "Never silently pick a side when sources disagree." The
mechanism and the store's default semantics are in direct opposition.

Worse, consolidation compounds it: `configuration.md:1556` states that by default "Contradictions are
tracked with temporal markers rather than overwriting the prior belief" — good — but the
observation that results is a *synthesised belief*, not the two original claims plus an open
question. The refine-rather-than-overwrite model produces a smoothed narrative; the drift model
requires an unsmoothed, explicitly-unresolved record.

**Consequence for Phase 2, stated as a rule:** *drift records must not live in the same store as
recalled knowledge.* Keep the drift registry as repository files under version control — where the
audit trail is enforced by git rather than by policy — and let the memory store hold, at most, one
tagged pointer per open drift. This is a strengthening of the mechanism, not a concession: it moves
the audit trail from a place where "do not delete" is a request to a place where it is a fact.

### Against the derive-don't-remember rule

The standing rule — **service dependency edges must be derived, never remembered** — is checked
against this file, and `drift-management.md` **does not violate it.** It never instructs an agent to
remember a dependency edge; it records *mismatches between stated and actual behaviour*, which is
the derived-versus-remembered comparison itself.

Two nearby files do get close, and one earns a quote:

- `references/operating-model.md:20` — "service ownership" is listed under **Store in Basic Memory**.
  A service-ownership matrix is one derivation away from a dependency graph, and
  `references/note-governance.md:44` shows the pattern in a relation example:
  `- depends_on [[Service Ownership Matrix]]`. Ownership (who is accountable) is a human fact and is
  legitimately remembered; **`depends_on` between services is not**. The rule Phase 2 must add is the
  discriminating sentence, not a ban: *remember who owns a service; derive what it calls.*
  `POST /api/v1/dependency_graph` (SigNoz) derives the edges, oasdiff detects prospective OpenAPI
  breaks, Serena/ast-grep resolve symbol references — and this skill currently names none of them.
- `references/note-governance.md:12` — `canonical_source_paths` plus `:13` `last_verified` is the
  skill's own honest admission that stored facts decay. The field exists; **no shipped script checks
  it.** `alaa_obsidian_linkcheck.ps1` checks links and Relations sections, not whether
  `last_verified` has aged past a threshold or whether the paths in `canonical_source_paths` still
  exist. That is the single highest-value checker this skill could ship and does not — and it is
  fully store-agnostic, because it reads note frontmatter and the filesystem.

The lane brief's framing is right: **memory that goes stale silently is worse than no memory.** This
skill states the rule that prevents it and ships no tool that enforces it.

---

## 3. The ten-criteria verdict

| # | Criterion | Verdict | Evidence | What a fix must add |
|---|---|---|---|---|
| 1 | Correctness and testability | **FAIL** | The skill ships no test of any kind: no `tests/` directory, no per-script self-test. `alaa_obsidian_linkcheck.ps1` — the one checker — was run against a synthetic vault (§6-C) and its exit code is wrong in **both** directions. `alaa_memory_health.ps1:48` misreports clean schema validations as failures (§6-A, reproduced). | A `tests/` harness that runs each script against a fixture vault with a known-bad note and a known-good note, asserting exit 1 on the first and 0 on the second, and BLOCKED→2 when `bm`/the store is absent. |
| 2 | Failure behaviour | **FAIL** | No timeout, retry, or degraded-store behaviour is stated anywhere for the store. `SKILL.md:38-47` (task-start) tells the agent to search memory but never says what to do when the search times out — which, given upstream basic-memory issue #980's measured "3–7s and search ~12s" (§5, still open), is the common case, not the edge case. `alaa_memory_post_task.ps1:23,31` and `alaa_memory_reindex.ps1:13,16,19` `throw` on any non-zero exit, conflating "store unreachable" with "store reports a problem". | The fail-open/fail-closed discrimination applied explicitly: memory recall is a **contributor** (proceeding without it does not let anything through that must not get through) → it fails **open**, with a stated timeout budget and a required line in the final report saying memory was unavailable. Drift *recording* is a **gate** → it fails **closed**: if the drift record cannot be written, the work stops. Route the reasoning to `alaa-reliability-sla`; it is currently named nowhere in this skill. |
| 3 | Security | **FAIL** | One genuine control exists: `precompact_checkpoint.ps1:9-22` redacts api key / token / password / secret / cookie / Bearer patterns, and `:56-57` keeps transcript-tail capture off by default. But the redaction is **regex-on-a-tail only** and never applied to the note body, the git status block, or the branch name; and `operating-model.md:36` states "secrets/credentials/tokens/cookies/private keys" as a do-not-store bullet with no mechanism behind it. `references/cli-and-mcp.md:35` binds the MCP server to `127.0.0.1` — correct — but the skill never states *why*, and Basic Memory's own default is `0.0.0.0` (verified, §5), so an agent that drops the flag exposes an **unauthenticated** MCP server on the LAN. Nothing routes to `alaa-security-review`. | A trust-boundary statement: the memory store is an untrusted sink (anything written may be read by any agent later) and an untrusted source (recalled text is model-authored, not verified). A rule that any HTTP transport binding beyond loopback requires authentication, with the fail-closed default. A named route to `alaa-security-review`. |
| 4 | Observability | **FAIL** | No log, metric, or trace contract for memory operations. `SKILL.md:143` requires the final response to report "notes changed, source paths, validation, drift recorded" — a report contract, which is real but is not observability. `drift-management.md:11` asserts default severity high/critical for "SOC/observability log contracts" — a **requirement level**, which `alaa-observability-soc` owns and which this skill sets unilaterally. | Route the requirement level to `alaa-observability-soc` and every field name to `alaa-services-contract` rather than asserting either here. |
| 5 | Concurrency and load | **FAIL** | Nothing. No statement of what happens when two agents write the same note, or when a hook fires while an indexing pass is running. `precompact_checkpoint.ps1:114` writes `"$title.md"` where the title embeds a `yyyyMMdd-HHmmss` stamp — two compactions inside the same second collide silently. | A concurrency rule per store: for a file-backed store, last-writer-wins is the actual semantics and must be stated; for Hindsight, `document_id` **is** the concurrency primitive (verified `retain.md:185`: providing it upserts and deletes the prior version; `:187`: omitting it "assigns a random UUID per request, so re-ingesting the same content will create duplicate memories"). |
| 6 | Clean code, SOLID, patterns | **FAIL** | `alaa_memory_health.ps1:28-40` `Invoke-Bm` mixes the output stream with its return value — the direct cause of §6-A. `Redact-Line` (`precompact_checkpoint.ps1:9`) uses an unapproved PowerShell verb. `alaa_memory_reindex.ps1` is a strict subset of `alaa_memory_post_task.ps1` with no shared module. | One shared `_common.ps1` owning store invocation, exit-code mapping and reporting; the three health/reindex/post-task scripts become thin parameterisations. |
| 7 | Algorithm and data-structure choice | **FAIL** | `alaa_obsidian_linkcheck.ps1:61-63` credits an incoming link by iterating **every note** for **every matched link**: `foreach ($k in $noteInfo.Keys) { if ($noteInfo[$k].Base -ieq $target) ... }`. That is O(notes × links). On the ~4,000-note vault upstream issue #980 describes, at ten links per note, that is ~1.6×10⁸ hash lookups per run. A base-name→note index built once makes it O(links). | A stated complexity budget and the index. The `HashSet` at `:26` shows the author knew the pattern; it just was not applied to the crediting loop. |
| 8 | Configurability | **PARTIAL / FAIL** | Good: every script parameterises `-Project`; `precompact_checkpoint.ps1:56` gates transcript capture on an environment variable with the safe default off. Bad: `alaa_memory_post_task.ps1:4` and `precompact_checkpoint.ps1:4` hardcode `D:\Sohrab\Project\agent-memory` as a parameter default, `alaa_obsidian_linkcheck.ps1:3` does the same, and `alaa_obsidian_linkcheck.ps1:119` hardcodes `--project alaa-memory` **ignoring** the script's own parameters. No boundary validation on any parameter. | Resolve the vault root from an environment variable with the current path as documented fallback; validate that it exists and is a directory; make `:119` use the resolved project. |
| 9 | Speed of development and debuggability | **FAIL** | The task-start rule (`SKILL.md:38-47`) makes an agent run a five-step memory-and-repo reconciliation before *any* non-trivial task, against a store whose search latency upstream measures at ~12 s, with no budget and no skip condition. `SKILL.md:14` defines the trigger as work that is "non-trivial, cross-service, contract-sensitive, architecture-sensitive, continuation-likely, or memory-sensitive" — six adjectives, no observable condition, which fails the wording test outright: a competent agent can follow it exactly and either always or never trigger. This is the criterion that gets a skill bypassed. | An observable trigger ("the task names a service, a contract, or a prior session"), a stated search budget, and an explicit "proceed without memory and say so" path. |
| 10 | Documentation | **PARTIAL** | `SKILL.md:134-143` completion checks are genuinely good — eight checkable statements, most of them observable. But nothing documents how the two hook scripts are **installed** (§1), and no `bm` version is pinned anywhere, so D10 fails: no version, therefore no re-derivation command. | Hook registration snippets for Claude Code and Codex; a pinned store version with the command that re-derives it beside it. |

**Counts: SATISFIED 0 · PARTIAL 2 (8, 10) · FAIL 8 · DELEGATED 0.**

The zero in the DELEGATED column is itself the finding. Delegation only counts when the skill names
the owner at a call site. This skill names exactly two other Alaa skills anywhere — `alaa-workflow`
(6 occurrences) and `alaa-low-noise` (2) — and **zero** of `alaa-project-constitution`,
`alaa-services-contract`, `alaa-observability-soc`, `alaa-reliability-sla`, `alaa-security-review`,
`alaa-testing-strategy`, `alaa-controlled-ops`, `alaa-prompting-guide`. It nonetheless asserts SOC
severity levels (`drift-management.md:11`) and notification-contract severities (`:12`), both of
which belong to owners it never names. This is the finding the last five batches all reported.

---

## 4. Defect-class findings

Only classes actually found are listed.

**Class 2 — wrong trigger syntax (severe form: neither runtime).** Measured across all 16 files:
**0 occurrences of `/alaa-…` and 0 of `$alaa-…`.** Every cross-skill mention is a bare name:
`SKILL.md:25` "`alaa-workflow`", `:26` "`alaa-low-noise`", `:98`, `:121`, `:140`,
`references/skill-boundaries.md:3,7`, `references/compact-and-handoff.md:9`,
`references/operating-model.md:41`, `scripts/session_start_context.ps1:24`. The comparison skill
`alaa-low-noise` writes it correctly in its own frontmatter: "…for /alaa-workflow ($alaa-workflow),
which owns durable planning and state." Every one of the ten sites above needs both forms.

**Class 3 — duplication between body and references.** Measured:

- The 13-name vendored-skill list appears **twice, verbatim**, in the same order and the same
  Install-now/Gated split: `SKILL.md:100-121` and `references/skill-boundaries.md:15-34`. Roughly
  480 duplicated bytes, in a 6,326-byte body.
- The `bm` health-command line is stated in **three** places: `SKILL.md:35`,
  `references/cli-and-mcp.md:6-12`, `scripts/session_start_context.ps1:27`.
- "Do not use unsupported `basic-memory sync`" is stated **four** times: `SKILL.md:36`,
  `SKILL.md:138`, `references/cli-and-mcp.md:15-19`, `scripts/session_start_context.ps1:27`.
- The drift-marker rule is stated **three** times: `SKILL.md:80`,
  `references/drift-management.md:20`, `references/note-governance.md:56-58`.
- The do-not-store list is stated **four** times with four different memberships: `SKILL.md:27`
  (6 items), `SKILL.md:90` (5), `references/operating-model.md:30-41` (11),
  `references/prompt-3-publishing.md:20-26` (5), plus a fifth partial at
  `scripts/session_start_context.ps1:24`. Four lists that disagree about their own contents is worse
  than one list, because an agent that reads only `SKILL.md:27` will not learn that
  secrets/credentials are on the list at all — that item appears **only** in
  `operating-model.md:36`.

**Class 4 — project-specific content in an always-loaded body.** `SKILL.md:35` embeds the literal
project name `alaa-memory` five times inside a command line, and `:10` binds the whole skill to it.
`SKILL.md:82` names "prompt 14" and "prompt 15" — an external prompt pack that is not in this
repository and that the body never locates.

**Class 5 — long procedures nobody reads in order.** `SKILL.md:38-47`, `:48-59`, `:74-84` are three
consecutive numbered procedures totalling 22 steps in a 140-line body. None is organised by failure
class. The correct restructure for `:74-84` is by symptom: *doc contradicts code* → …; *memory
contradicts repo* → …; *two services contradict each other* → …

**Class 6 — description that only says when to use.** Not found; `SKILL.md:3` ends with "Do not use
for tiny code edits or as a second task system." Description measures **569 characters** collapsed,
well under the 900 ceiling, and contains **no angle brackets**. Passes.

**Class 10 — shrink where possible.** The body is **140 lines**, over the validator's 120-line
warning threshold (`validate_sohrab_skill_pack.py:187`). Removing only the two verbatim duplications
above (the 13-name list and the health-command line) reclaims ~24 lines with no rule lost.

**Class 11 — companion boundary.** Present but stale; see §5-B below.

**Not previously enumerated, but the most serious single defect in the directory — a shipped binary
defect.** `scripts/alaa_obsidian_linkcheck.ps1` ends with the byte sequence
`... -ForegroundColor Green\n\x00\x00\n` — two NUL bytes after the last statement (`file` reports the
script as `data`, not `ASCII text`; every other file in the skill reports as text). PowerShell
*parses* the file cleanly but *executes* the NULs as a command name. Observed, verbatim:

```
lc.ps1: The term ' ' is not recognized as a name of a cmdlet, function, script file, or executable program.
```

with exit code **1**, on a vault with **zero** broken links. See §6-C.

**Validator failures (two errors, one warning), against
`skills/scripts/validate_sohrab_skill_pack.py:196-204,187`:**

- `alaa-basic-memory-os: short_description must be 25-64 chars` — `agents/openai.yaml` has no
  `short_description` key at all; the regex matches nothing, `len("") == 0`.
- `alaa-basic-memory-os: default_prompt must mention $alaa-basic-memory-os` — no `default_prompt`
  key. Compare the passing shape at `alaa-golang/agents/openai.yaml`, which has an `interface:`
  block with `display_name`, `short_description` (49 chars) and a `default_prompt` naming
  `$alaa-golang`, plus a `policy: allow_implicit_invocation: true`.
- Warning: `top-level body is 140 lines`.

**Routing-convention deviation.** Eight references means the ≤8 rule applies: list them in `SKILL.md`
**with a trigger condition each**. `SKILL.md:123-132` lists all eight as bare paths with no trigger
condition on any of them. Two more references are named inline instead (`:59`, `:84`, `:92`), so the
index is also not the only route.

---

## 5. Boundary analysis

### A. What the skill owns, and legitimately

The knowledge-shape policy: what is worth remembering, in what form, with what confidence, and the
drift protocol. Nothing else in the fleet owns this. `alaa-workflow` explicitly disclaims it —
`references/artifact-lifecycle.md:29`: "Three owners, three questions, no overlap: the plan owns the
destination and route, the checkpoint owns position, and the plan's handoff package owns knowledge."
All three of those are *within one engagement*. Cross-engagement durability is unowned by anyone
else, and this skill should keep it.

### B. `references/skill-boundaries.md` checked claim by claim against the current fleet

| Claim (file:line) | Verdict |
|---|---|
| `:5` `alaa-workflow` "Owns long-running execution, phase prompts, repo-local plans, continuation state, validation evidence, subagent orchestration, and handoff safety." | **Accurate but understated.** `alaa-workflow/SKILL.md:3` claims "durable continuation across compaction or a fresh agent" — compaction specifically, which this file's own `compact-and-handoff.md` then re-enters. |
| `:9` `alaa-low-noise` "Owns bounded terminal and output discipline, avoiding raw dumps and noisy logs." | **Stale.** `alaa-low-noise/SKILL.md:3` now describes **two** levers, and names context economy as the more valuable: "**Context economy** governs what enters the context window at all; **output noise** governs what gets printed for the user. Context economy is the more valuable of the two." This boundary statement names only the second lever. That matters directly: a memory skill that injects recalled context is spending context economy, which is the lever this file does not know exists. |
| `:13` Basic Memory "Owns cross-session recall, contract maps, lesson recall, project indexes, decision pointers, and concise handoff pointers." | **Half wrong.** "concise handoff pointers" is the trespass; see below. |
| `:17-34` The 13 named vendored skills | **Incomplete.** Fourteen distinct skills exist in the pack; **`memory-literary-analysis` is named nowhere** in this skill. Listed as bare names with no path, so an agent cannot open any of them. |
| `:36` "`memory-tasks` is not an execution-state owner in Alaa coding work." | **Accurate, and one of the better sentences here.** Duplicated at `SKILL.md:121`. |

The file names **four** owners. The fleet has 68 skills, of which this skill's own domain touches at
least eight doctrine owners it does not name (§3, criterion count). A boundary statement listing
four of eight-plus is the failure mode the lane brief predicts: written before seven batches of
rewrites, and now naming a version of `alaa-low-noise` that no longer exists.

### C. What it must stop owning, and to whom

**`references/compact-and-handoff.md` trespasses on `alaa-workflow`, and the counterpart says so in
its own words.** The file concedes authority at `:9` ("`alaa-workflow` repo-local state is
authoritative for active execution") and then, at `:13-20`, defines a six-field handoff pointer
anyway: objective, verified current state, repo-local plan/state paths, validation run and result,
next action, risks/questions. `alaa-workflow/references/context-continuity.md:37-39` opens with
"## The handoff package / Six fields. Each exists because a real resume fails without it." and
`alaa-workflow/references/artifact-lifecycle.md:61` says, of exactly this material: "`references/context-continuity.md`
owns the read order, the cold-start test, the post-compaction rules, and what a handoff must
contain. **Do not restate them here.**" That prohibition is addressed to a sibling file inside
`alaa-workflow`; it applies with more force across a skill boundary. The two six-field lists do not
even agree — `alaa-workflow`'s six are confirmed facts / open assumptions / ruled out / read first on
resume / environment notes / traps, which is a strictly better decomposition.

**Retire `compact-and-handoff.md` to `_to_delete/`.** What survives is one sentence in the new body:
*a memory store holds a pointer to the plan and its handoff package; `alaa-workflow`
`references/context-continuity.md` owns what the handoff contains.*

**`references/note-governance.md` restates the vendored `memory-notes` skill.** Upstream's own
description: "How to write well-structured Basic Memory notes: frontmatter, observations with
semantic categories, relations with wiki-links, and best practices for building a rich knowledge
graph." That is a complete match for `note-governance.md:3-46`. What is genuinely Alaa's and must be
kept is the *vocabulary* — the 18-label observation set at `:35`, the status/confidence enumerations
at `:18-32`, and `canonical_source_paths`/`last_verified` at `:12-13`. What must go is the mechanics.

### D. The vendored-pack rule — does it wrap, or does it fork?

**Verified inventory.** `vendor/subtrees.json` pins `basic-memory` at
`prefix: vendor/basic-memory`, `source_path: skills`, `pinned_commit:
a1e0987eaf5ac9853c32fed5d907b1451e7a90df`. `find vendor/basic-memory -name SKILL.md` returns **19**
files, matching the carry-over's count. They are 14 distinct skills at the top level plus a nested
`basic-memory/` directory re-containing five of them:

Top level (14): `memory-capture`, `memory-ci-capture`, `memory-continue`, `memory-curate`,
`memory-defrag`, `memory-ingest`, `memory-lifecycle`, **`memory-literary-analysis`**,
`memory-metadata-search`, `memory-notes`, `memory-reflect`, `memory-research`, `memory-schema`,
`memory-tasks`.
Nested duplicates under `vendor/basic-memory/basic-memory/` (5): `memory-capture`,
`memory-continue`, `memory-metadata-search`, `memory-notes`, `memory-schema`.

**Verdict: it half-wraps and half-forks.**

*Wrapping, correctly:* it names 13 of the 14 by name and splits them into recommended versus
gated/manual (`SKILL.md:100-121`), and it adds a genuine opinion the upstream does not have —
`SKILL.md:121` "`memory-tasks` must not duplicate active `alaa-workflow` execution state", and
`drift-management.md:43` "Do not treat `bm schema diff` output (schema-vs-usage drift) as contract
drift — that is metadata maintenance." Both are exactly the right kind of local opinion over a
vendored pack.

*Forking, incorrectly:* it names them **only as bare names, never as paths**, so no agent can route
into them — there is not one `vendor/basic-memory/...` path anywhere in the skill. And it restates
their mechanics in `note-governance.md` (vs `memory-notes`) and partly in `drift-management.md`'s
schema-validation queries (vs `memory-schema`, whose own description already covers "validate notes,
and detect drift").

**The same rule binds the successor.** Hindsight ships a first-party documentation skill —
`vectorize-io/hindsight` `skills/hindsight-docs/SKILL.md`, verified present today, whose
`references/` tree carries `openapi.json` (0.8.6), `best-practices.md`, `developer/api/*.md`,
`developer/configuration.md` and `sdks/integrations/*.md`. If that pack is vendored, the Alaa skill
must wrap it: own the operating model and the bank/tag layout, and point at
`hindsight-docs references/developer/api/retain.md` for the ingest mechanics — never restate them.
The whole of §6's verification below came out of that pack, which is itself the argument.

### E. What it should own and does not

- **A staleness checker.** `last_verified` and `canonical_source_paths` are declared and never
  enforced (§2).
- **The derive-don't-remember discrimination** for service topology (§2).
- **A recall budget and a fail-open rule** (§3, criterion 2).
- **Its own installation.** Two hook scripts with no registration path (§1).

---

## 6. Version and factual currency — checked today, 2026-07-29

Every row was checked today. Re-derivation commands are given so no reader has to trust the row.

### Basic Memory (the store being replaced)

| Claim | Verdict | Evidence / re-derive |
|---|---|---|
| Current release **0.22.1**, published **2026-06-13** | **VERIFIED** | `curl -s https://pypi.org/pypi/basic-memory/json \| python -c "import json,sys;d=json.load(sys.stdin);print(d['info']['version'], d['releases'][d['info']['version']][0]['upload_time_iso_8601'])"` → `0.22.1 2026-06-13T03:35:17Z`. Note the GitHub Releases page stops at v0.21.6 (2026-06-05) — PyPI is the authoritative surface here, and a skill that pinned from GitHub would be two releases stale. |
| License **AGPL-3.0** | **VERIFIED** | Same call, `info.license_expression` → `AGPL-3.0-or-later`. |
| `basic-memory sync` removed | **VERIFIED** | `curl -s https://raw.githubusercontent.com/basicmachines-co/basic-memory/v0.22.1/src/basic_memory/cli/commands/__init__.py` — the command list is `ci, status, db, doctor, import_memory_json, mcp, import_claude_conversations, orphans, import_claude_projects, import_chatgpt, man, tool, project, config, format, schema, update, workspace`. No `sync`. `SKILL.md:36` is correct. |
| `bm reindex -p <project>` is the replacement | **VERIFIED** | It lives in `db.py`, not its own module: `commands/db.py:262` `def reindex(...)`, with `:290` documenting `bm reindex -p claw --full`. `SKILL.md:35` is correct. |
| `bm status --project X --wait --timeout 60` | **VERIFIED for 0.22.1, STALE ON MAIN — flagged** | At tag v0.22.1, `commands/status.py:215` still reads `"--wait", help="Block until indexing is complete (no pending changes)"`. On `main` the same option is now `:118` `help="Compatibility option for --wait"` and the code emits `"status --wait is a compatibility no-op for event-based project indexing"` (`main:97`). **The next Basic Memory release turns this command into a no-op.** It is asserted in 7 places across this skill (`SKILL.md:35`, `cli-and-mcp.md:6`, and four scripts), and three scripts `throw` on its exit code. Re-derive: `curl -s https://raw.githubusercontent.com/basicmachines-co/basic-memory/main/src/basic_memory/cli/commands/status.py \| grep -n "compatibility"`. |
| `bm doctor`, `bm orphans`, `bm schema validate/diff`, `bm format`, `bm tool …` all exist | **VERIFIED** | Each has a module in the v0.22.1 command list above (HTTP 200 on `.../v0.22.1/src/basic_memory/cli/commands/{orphans,schema,format,tool}.py`). Individual sub-flags (`--hybrid`, `--meta`, `--include-frontmatter`, `--page-size`) were **not** individually verified — **UNVERIFIABLE** at this depth; Phase 2 should pin them with `bm tool search-notes --help`. |
| Issue **#980** (read 3–7 s, search ~12 s) still open | **VERIFIED — still OPEN** | `https://github.com/basicmachines-co/basic-memory/issues/980`, opened 2026-06-11, title "Upstream a BMQ3-style read cache: MCP tool latency is product-defining for multi-agent use", reporting "3–7s and search ~12s through the standard path" at ~4,000 notes and calling it "effectively unusable" for multi-agent use. The owner's "it is slow" complaint is confirmed upstream and unfixed. |
| Issue **#959** (removed `sync`, `--wait` cannot finish) still open | **STALE — now CLOSED** | `https://github.com/basicmachines-co/basic-memory/issues/959`, opened 2026-06-11, title "CLI-only local sync is a dead end: docs reference removed 'basic-memory sync', status --wait can never finish, bm reindex is the undiscoverable answer" — **state: closed**. The `main`-branch no-op above is what closed it. |
| `bm mcp --transport streamable-http --host 0.0.0.0` exists (the underused LAN capability) | **VERIFIED, and stronger than recorded** | `commands/mcp.py:28-33`: `transport` default `"stdio"` with `"Transport type: stdio, streamable-http, or sse"`; `host` **default `"0.0.0.0"`** with help `"use 0.0.0.0 to allow external connections"`; `port` default `8000`; `path` default `"/mcp"`. The capability is not merely present — external binding is the **default**, and `references/cli-and-mcp.md:35` overrides it to `127.0.0.1` without saying why. Given there is no authentication on that endpoint, the 127.0.0.1 there is load-bearing and undocumented. |

### Hindsight (the replacement)

| Claim | Verdict | Evidence / re-derive |
|---|---|---|
| Current release **v0.8.5, 2026-07-22** | **STALE — 0.8.6 shipped today, 2026-07-29T16:11:32Z** | `curl -s https://pypi.org/pypi/hindsight-api/json \| python -c "import json,sys;d=json.load(sys.stdin);v=d['info']['version'];print(v,d['releases'][v][0]['upload_time_iso_8601'])"` → `0.8.6 2026-07-29T16:11:32.242717Z`. Corroborated independently: the vendored OpenAPI spec's `info.version` is `0.8.6`. This is the concrete case for "pin the image version, because Hindsight is 0.x with weekly breaking changes" — the pin went stale inside one week. |
| MCP server at `/mcp`, per-bank `/mcp/{bank_id}/` | **VERIFIED** | `hindsight.vectorize.io/developer/mcp-server` — mounted at `/mcp`; per-bank `http://localhost:8888/mcp/{bank_id}/`; multi-bank mode at `/mcp/` with no bank in the path. |
| MCP/API **unauthenticated by default** | **VERIFIED, verbatim** | Same page: "By default, the MCP endpoint is **open** (no authentication required)." |
| `HINDSIGHT_API_TENANT_EXTENSION=hindsight_api.extensions.builtin.tenant:ApiKeyTenantExtension` + `HINDSIGHT_API_TENANT_API_KEY` | **VERIFIED, exact string match** | `hindsight-docs references/developer/configuration.md:1034-1035` and the table at `:1049-1050`. Default for both: *(none; auth disabled)*. Clients send `Authorization: Bearer <key>`. |
| Ingest is `POST /v1/default/banks/{bank}/memories` | **VERIFIED** | The 0.8.6 OpenAPI spec lists `POST, DELETE /v1/default/banks/{bank_id}/memories`. Re-derive: `curl -s https://raw.githubusercontent.com/vectorize-io/hindsight/main/skills/hindsight-docs/references/openapi.json \| python -c "import json,sys;d=json.load(sys.stdin);print([p for p in d['paths'] if p.endswith('/memories')])"` |
| Body `{"items":[…],"async":true}` | **VERIFIED** | `RetainRequest` properties are exactly `['items','async','document_tags','operation_id']`, `required: ['items']`. `retain.md:533-534` shows the literal body. (The Python SDK spells the same flag `retain_async=True` — same wire field.) |
| `items[].timestamp` accepts ISO 8601 or the literal `"unset"`, and carries occurrence time | **VERIFIED** | `MemoryItem.timestamp` is `anyOf[date-time string, string, null]`. `retain.md:134`: `"unset"` — "Stores the content **without any timestamp**… for timeless material". `:136`: the timestamp is injected into the extraction prompt as the temporal anchor. `MemoryItem` required is `['content']` only; every other field is optional. |
| `timestamp` maps to `mentioned_at` | **VERIFIED (documented on the recall side)** | `recall.md:33`: `mentioned_at: ISO datetime of when the fact was retained`, and `:671` a dedicated section. |
| `document_id` is the upsert key; omitting it duplicates | **VERIFIED, verbatim** | `retain.md:185`: "if a document with that ID already exists in the bank, it and all its associated memories are deleted before the new content is processed and inserted"; `:187`: "If you omit `document_id`, Hindsight assigns a random UUID per request, so re-ingesting the same content will create duplicate memories." Also `:191-198`: `update_mode` `replace` (default) / `append`, where append **requires** a `document_id`. |
| Only `tags` are filterable at recall; `metadata` is not | **VERIFIED** | `retain.md:222`: "Tags control **visibility scoping** — which memories are visible during recall." The recall filter section `:327-540` covers `tags`/`tags_match` exclusively; `metadata` appears only as a returned field (`recall.md:28`, `:655`). |
| `tags_match="any"` also returns untagged; real filtering needs `all_strict` | **VERIFIED, verbatim** | `recall.md:348-350`: "`any` — OR matching, includes untagged (default) … Returns memories that have **at least one** matching tag, plus untagged memories." `:480-482`: "`all_strict` … Returns memories that have **every** specified tag, and excludes untagged memories." Also `:526`: extra tags on the memory are fine under `all_strict`. |
| Bank `name` must be left unset (issue **#1680**, "open") | **PARTLY STALE** | Issue #1680 exists and its title is exactly "Discussion: Narrator line ties first-person attribution to banks.name (often bank_id), causing entity pollution and transcript misclassification", opened 2026-05-21 — but its **state is closed**, not open. The 0.8.6 API now carries an explicit override: schema `DryRunExtractRequest.agent_name`, described as `"Narrator override (memory owner) primed in the prompt."` The underlying behaviour (a Narrator line derived from the bank name enters the extraction prompt) is still real, so the *practice* of leaving `name` unset remains sound; the *citation* is stale and must be re-derived before Phase 2 writes it down. |
| `enable_auto_consolidation: false` during bulk import, then one consolidate, then re-enable | **VERIFIED, with a name correction** | The knob is `HINDSIGHT_API_ENABLE_AUTO_CONSOLIDATION`, default **`true`**, "Configurable per bank" — `configuration.md:1527`. The manual trigger is `POST /v1/default/banks/{bank_id}/consolidate` (`operations.md:63`, and present in the 0.8.6 OpenAPI paths), which "Pass `observation_scopes` to consolidate only memories matching specific tag combinations". |
| `retain_extraction_mode: "chunks"` costs zero LLM calls | **VERIFIED, verbatim** | `configuration.md:1219`: "Store chunks as-is, zero LLM cost \| `HINDSIGHT_API_RETAIN_EXTRACTION_MODE=chunks`". Full value set at `:1144`: `concise` (default), `verbose`, `verbatim`, `chunks`, `custom`. Note `:1224`: a `retain_mission` is **ignored** in `chunks` mode. |
| `HINDSIGHT_API_LLM_MAX_CONCURRENT` default 32 | **VERIFIED** | `configuration.md:175` — "Max concurrent LLM requests \| `32`". `:446,454` recommend `2` for a shared llama.cpp server. Three per-operation sub-caps also exist (`RETAIN_`/`REFLECT_`/`CONSOLIDATION_`), unset by default and composed on top (`:537-546`). |
| `HINDSIGHT_API_LLM_TRACE_ENABLED` defaults true, writes full prompts to a local table | **VERIFIED, verbatim** | `configuration.md:1779`: "**LLM request tracing is enabled by default**, with traced rows retained for 1 day." `:1781`: "Traced rows contain the full prompt and model output, which may include sensitive memory content". `:1785` table: default `true`. |
| `HINDSIGHT_API_RERANKER_MAX_CANDIDATES` default 300 | **VERIFIED** | `configuration.md:1083` — "Max candidates to rerank per recall (RRF pre-filters the rest) \| `300`". |
| `HINDSIGHT_API_WORKER_ID` must be set or in-flight tasks orphan on restart | **VERIFIED (name and default)** | `configuration.md:1678` — "Unique worker identifier \| hostname". The orphaning consequence is a reasonable inference from the default, not a quoted upstream sentence — mark it **PLAUSIBLE** until Phase 2 quotes the operations page. |
| Claude Code first-party plugin exists | **VERIFIED** | `hindsight-docs references/sdks/integrations/claude-code.md:14-16`: `claude plugin marketplace add vectorize-io/hindsight` then `claude plugin install hindsight-memory`. Hooks table at `:54-57`: `session_start.py`→`SessionStart`, `recall.py`→`UserPromptSubmit`, `retain.py`→`Stop`, `session_end.py`→`SessionEnd`. |
| Codex CLI hooks integration exists | **VERIFIED** | `sdks/integrations/codex.md:14` `curl -fsSL https://hindsight.vectorize.io/get-codex \| bash`; three hooks on `SessionStart`, `UserPromptSubmit`, `Stop` (`:35-55`); requires `codex_hooks = true` under `[features]` in `~/.codex/config.toml` (`:168`). |
| Codex CLI **≥ v0.116.0** required | **UNVERIFIABLE** | Neither `sdks/integrations/codex.md` nor `changelog/integrations/codex.md` states any minimum Codex version; the documented gate is the `codex_hooks` feature flag. Do not write the number into Phase 2 without re-deriving it. |
| `llmProvider: openai-codex` is supported | **VERIFIED** | `sdks/integrations/claude-code.md:129`: supported values `openai`, `anthropic`, `gemini`, `groq`, `ollama`, `ollama-cloud`, **`openai-codex`**, `claude-code`. |
| Plugin `requestTimeoutSeconds` defaults to 10 s, needs 45 on CPU-only | **MOSTLY VERIFIED, imprecise** | `claude-code.md:119`: the setting's own default is **`null`**; the per-call defaults it overrides are recall **10 s**, retain **15 s**, knowledge tools 10–15 s; the health check stays at 5 s regardless. The doc's own remedy language matches the record: "Bump this when self-hosted Hindsight legitimately takes longer than 10s under contention". Separately `:286` notes the recall hook has a **12-second** timeout. Phase 2 must write "recall 10 s / retain 15 s", not "10 s". |
| Banks are strictly isolated, no cross-bank query | **VERIFIED indirectly** | Every API path is bank-scoped (`/v1/default/banks/{bank_id}/…`), MCP tools "resolve the active bank from the same config" and "None of the tools accept a `bank_id` parameter" (`claude-code.md:209`). The one-bank `alaa-memory` decision follows correctly. |
| Codex refresh tokens are single-use, so the server needs its own `CODEX_HOME` | **UNVERIFIABLE from Hindsight docs** | Not addressed in the Hindsight documentation set. It is an OpenAI Codex auth property; treat as owner-supplied operational knowledge and route the model/runtime question to `alaa-prompting-guide`. |

### Claude Code hook surface (both hook scripts)

| Claim | Verdict | Evidence |
|---|---|---|
| `PreCompact` is still a current hook event | **VERIFIED** | `https://code.claude.com/docs/en/hooks` — `PreCompact` ("Before context compaction") is in the current event list, alongside a newer `PostCompact`. |
| `SessionStart` is still a current hook event | **VERIFIED** | Same page: "when Claude Code starts a new session or resumes an existing session", with the caveat "SessionStart runs on every session, so keep these hooks fast." |
| `session_start_context.ps1:8` — "Output on stdout is added to the session context by Claude Code" | **VERIFIED, verbatim** | "For most events, stdout is written to the debug log but not shown in the transcript. The exceptions are `UserPromptSubmit`, `UserPromptExpansion`, and `SessionStart`, where stdout is added as context that Claude can see and act on." |
| `precompact_checkpoint.ps1` reads `$hookEvent.trigger` and `.transcript_path` | **PLAUSIBLE, not confirmed** | The docs confirm the common input fields `session_id`, `transcript_path`, `cwd`, `hook_event_name`, and that PreCompact matchers filter on `"manual"` / `"auto"`; they do not show the `trigger` field name in the current schema. Phase 2 must confirm against a live hook payload. |
| Exit codes for hooks | **Important collision — VERIFIED** | For hooks, "Exit 2 means a blocking error… stderr text is fed back to Claude as an error message", and for `SessionStart` specifically the table reads "Can block? No — Shows stderr to user only". **This means hook scripts are legitimately exempt from the programme's 0/1/2 checker contract**: 2 is reserved by the runtime and means something else. Phase 2 must state that exemption explicitly, or a well-meaning agent will "fix" the hooks into misbehaviour. |

### `raw/processed` and the Prompt 1/2/3 pipeline

**UNVERIFIABLE — path not reachable.** The device session mounts exactly four folders:
`alaa-go-chi`, `service-ci-kit`, `service-runtime-kit`, `skills`. `D:\Sohrab\Project\raw` is not
among them (`ls` returns "No such file or directory" for both `D:/Sohrab/Project/raw` and
`/mnt/d/Sohrab/Project/raw`). No folder-access dialog was raised, per the read-only phase.

Therefore every claim in `references/prompt-3-publishing.md:7-9` (the three `_global` input paths) and
`references/operating-model.md:16` (`D:/Sohrab/Project/raw/processed`) is **unchecked**, as is
whether the `_manifest.md` figure (187 claude-code sessions, last run 2026-07-04) still matches disk.
Re-derive with:
`mcp__remote-devices__device_request_folder_access(["D:\\Sohrab\\Project\\raw\\processed"])` then
`ls .../\_global/ && head -40 .../_manifest.md`.

One thing is checkable without the folder and is worth flagging now: `operating-model.md:16` and
`prompt-3-publishing.md:7-9` write these as **forward-slash `D:/…` paths** while every script writes
**backslash `D:\…`**. Two conventions for the same path in one skill is the kind of inconsistency that
survives because nothing checks it.

---

## 7. Executable-check inventory

Environment: PowerShell **7.4.6** on Linux (`/opt/pwsh/pwsh`). Windows PowerShell 5.1 was not
available; every 5.1 claim below is marked as such and is derived from documented behavioural
differences, not observed.

**All six scripts parse cleanly** under
`[System.Management.Automation.Language.Parser]::ParseFile` — zero parse errors. The defects are all
runtime or semantic.

| Script | Runs? | Asserts | 0/1/2 contract | Windows / PS5.1 |
|---|---|---|---|---|
| `alaa_memory_health.ps1` | Needs `bm`; **logic bug reproduced in isolation** | store reachable, doctor clean, 12 schema types valid, optional orphans, drift list | **FAIL — and inverted.** `throw` on a missing `bm` (`:25`) exits **1**, identical to "findings". With `-Strict`, `exit $code` where `$code` is an array exits **0** (§6-B). | Runs on both. `Invoke-Bm`'s bug is runtime-independent. |
| `alaa_memory_post_task.ps1` | Needs `bm` + the vault | reindex, status, per-type schema validate, doctor, then `git status --short` / `git diff --stat` | **FAIL.** Every failure path is `throw` → 1. Schema failures only `Write-Warning` (`:27`) and do **not** affect the exit code, so a validation failure exits 0. | `:4` hardcodes `D:\Sohrab\Project\agent-memory`. `Push-Location`/`Pop-Location` in `try`/`finally` is correct on both. |
| `alaa_memory_reindex.ps1` | Needs `bm` | reindex + status + doctor all zero | **FAIL.** All three `throw` → 1; no distinction between missing tool and reported problem. | Runs on both. |
| `alaa_obsidian_linkcheck.ps1` | **RUN — twice, observed** | broken wikilinks, orphan notes, notes missing `## Relations` | **FAIL in both directions — §6-C** | Windows-only by construction; see below. |
| `precompact_checkpoint.ps1` | Hook; not exercised end-to-end (would write into a vault) | writes an `inbox_capture` note; redacts six secret patterns from an optional tail | **Exempt** (hook protocol reserves 2). Always `exit 0`, including in `catch` (`:122`, `:126`) — deliberate and correct for a hook, but it means a silently failed checkpoint is indistinguishable from a successful one. | `:4` hardcodes the vault path. **`Set-Content -Encoding UTF8` at `:115` writes UTF-8 *with* BOM on Windows PowerShell 5.1 and *without* on PowerShell 7** — a BOM immediately before `---` can break YAML frontmatter parsing. Use `-Encoding utf8NoBOM` (PS7) or `[IO.File]::WriteAllText` with a BOM-less `UTF8Encoding` for cross-runtime safety. `git branch --show-current` needs git ≥ 2.22. |
| `session_start_context.ps1` | **RUN-equivalent**: pure stdout, no side effects | emits 7 governance lines; conditionally one drift line | **Exempt** (hook). Always `exit 0` (`:31`). | Runs on both. `$ErrorActionPreference = "SilentlyContinue"` at `:10` means a broken `bm` is silently swallowed — appropriate here. **Content defect:** `:14` runs `bm tool search-notes --type drift` and then, at `:15-16`, sets the warning if the command merely **succeeded** — `$LASTEXITCODE -eq 0 -and $driftJson`. A successful search returning *zero* drift notes still prints "Open drift notes may exist". The condition tests for command success, not for results. |

### §6-A — `alaa_memory_health.ps1:48` reports failures on clean validations (reproduced)

`Invoke-Bm` (`:28-40`) writes its progress with `Write-Host` (host stream, correct) but then runs
`& bm @BmArgs` — whose **stdout goes to the output stream** — before `return $code`. In PowerShell a
function returns everything on the output stream, so the caller at `:48`,
`$code = Invoke-Bm -BmArgs $validateArgs -AllowFailure`, receives an array of `bm`'s output lines
*plus* the exit code. `$code -ne 0` on an array is a filter, not a comparison: it yields the
non-zero-matching elements, which is a non-empty array, which is truthy.

Reproduced with a stub that prints two lines and exits 0:

```
bm schema validate drift
--- captured type: System.Object[]  count: 3
--- value: stub bm output line 1|stub bm output line 2|0
*** WARNING BRANCH TAKEN (bug) ***
```

**Every one of the twelve schema types will report "Schema validation reported issues" on every run**
in which `bm` prints anything at all. The health check's central assertion is a constant.

### §6-B — `-Strict` mode exits 0 on failure (reproduced)

`:51` is `if ($Strict) { exit $code }` with the same array. Observed:

```
$ pwsh -c '$code = @("a","b",0); exit $code'
observed exit code: 0
```

So the mode explicitly named "Strict", intended to make schema failures fatal, **exits 0**. A CI gate
built on this script treats a schema-validation failure as a pass — the precise failure this
programme's exit-code contract exists to eliminate, present in the one script that has a strict mode.

### §6-C — `alaa_obsidian_linkcheck.ps1` exit code is wrong in both directions (reproduced)

Two synthetic vaults were built and the shipped script run against each, read-only.

**Vault with one broken link** (`/tmp/fakevault`, 3 notes, `A.md` links to a non-existent
`[[Missing Note]]`). Report body was correct:

```
# Obsidian Link Check Report

- Vault: /tmp/fakevault
- Date: 2026-07-29 18:51
- Notes scanned: 3

## Broken wikilinks (1)

- `/A.md` -> [[Missing Note]] not found
...
```

then, verbatim:

```
lc.ps1: The term ' ' is not recognized as a name of a cmdlet, function, script file, or executable program.
EXIT=1
```

**Clean vault** (`/tmp/cleanvault`, 2 notes, all links resolve, both have `## Relations`): report
correctly shows zero broken links — and the process **still exits 1**, from the same NUL bytes.

**Same clean-vault script with the two NUL bytes stripped** (`tr -d '\000'`): `EXIT_CLEANSCRIPT=0`.
**Same de-NUL'd script against the broken vault:** `EXIT with 1 broken link, NULs stripped = 0`.

So: as shipped it is **always 1** (a CI gate on it fails permanently, and gets disabled); with the
obvious one-character fix it becomes **always 0** (a CI gate on it passes permanently, and finds
nothing). There is no state in which this checker reports the truth. It needs an explicit
`exit` mapping: 0 when `$broken.Count -eq 0`, 1 when there are findings, 2 when the vault path does
not resolve — replacing the `throw` at `:20`, which currently exits 1 for an unreachable vault.

Two further observations from the runs, both Windows-only-by-construction and therefore not defects
on the target platform, but worth recording because they show the script has never been run outside
Windows: the template exclusions at `:78-80` use backslash globs (`'00-control\templates\*'`), so on
PS7/Linux the template note was **not** excluded and appeared in both the orphan and no-Relations
lists; and `:66,77` `.TrimStart('\')` leaves a leading `/` on the reported paths. `:123`
`Join-Path $env:TEMP …` is also Windows-only. All three are fine for the stated platform; Phase 2
should simply say so rather than leaving it ambiguous.

### §6-D — the checker the skill does not ship

Nothing verifies `last_verified` freshness or that `canonical_source_paths` still resolve, despite
`note-governance.md:12-13` requiring both fields on every source-derived note. This is the one new
script Phase 2 must add, and it is entirely store-agnostic: it reads note frontmatter and stats the
filesystem.

---

## 8. Phase 2 work order

Target: **rewrite as `alaa-memory-os`**, store-agnostic. Budget **≤ 29,757 bytes** (no growth),
with growth permitted only for the two new checkers named below — which are a genuinely new
capability (the skill currently ships no rule that any tool can report a violation of, except a link
checker whose exit code is always wrong).

### New files

| Path | Contents |
|---|---|
| `SKILL.md` | ≤ 110 body lines. Owns: the four-surface model; the observable trigger replacing `:14`; task-start with a **recall budget and a fail-open rule**; note creation; Extraction/Design modes; the drift rule (pointer only); the derive-don't-remember discrimination; end-of-work; the routing table with a trigger condition per reference; completion checks. Every cross-skill mention in both `/name` and `$name` forms. Names at minimum `alaa-workflow`, `alaa-low-noise`, `alaa-reliability-sla`, `alaa-security-review`, `alaa-observability-soc`, `alaa-services-contract`, `alaa-project-constitution` at real call sites. |
| `references/drift-management.md` | Kept, promoted, made store-independent. Adds: the drift registry lives in **repository files under version control**, not in the memory store, because "do not delete" must be a fact and not a request; the Reflect-supersession collision stated explicitly; the derive-don't-remember discrimination for service topology with SigNoz `POST /api/v1/dependency_graph`, oasdiff and Serena/ast-grep named as the derivers. |
| `references/knowledge-shape.md` | Merges `note-governance.md` + the vocabulary half of `obsidian-usage.md`. Keeps the 18 observation labels, status/confidence enumerations, `canonical_source_paths`/`last_verified`. **Deletes** the frontmatter/observations/relations mechanics and routes them to `vendor/basic-memory/memory-notes/SKILL.md` by full path. |
| `references/store-basic-memory.md` | The current `cli-and-mcp.md` plus the pinned version (0.22.1) and its re-derivation command, plus the `--wait` no-op warning from §5, plus the reason `127.0.0.1` is load-bearing. |
| `references/store-hindsight.md` | Bank layout (`alaa-memory`, one bank); the ingest contract with the verified path and body; tags as the only filterable axis and `all_strict` as the only real filter; `document_id` as upsert and concurrency key; the historical-import script requirement (the official plugins never send `timestamp`); the bulk-import sequence (`ENABLE_AUTO_CONSOLIDATION=false` → retain → `POST …/consolidate` → re-enable); the security defaults (API and MCP open; the two tenant variables); the four operational knobs with their verified defaults; the pinned image version with `curl … pypi.org/pypi/hindsight-api/json` beside it. Points at the vendored `hindsight-docs` pack for mechanics rather than restating them. |
| `references/skill-boundaries.md` | Rewritten against the current fleet. Corrects the `alaa-low-noise` two-lever description. Names all **14** vendored skills **by path**, not by bare name. Adds the doctrine owners the skill delegates to. |
| `references/prompt-3-publishing.md` | Kept, after the `raw/processed` paths are re-verified against disk (§5). Path separators normalised to one convention. |
| `scripts/_common.ps1` | Shared: store invocation, the 0/1/2 exit mapping, report emission, vault-root resolution from an environment variable with boundary validation. |
| `scripts/alaa_memory_staleness.ps1` | **New.** For every note carrying `canonical_source_paths`: assert each path exists, and assert `last_verified` is not older than a configurable threshold. Exit 0 clean, 1 findings, 2 could not run (vault unresolvable). Store-agnostic. |
| `tests/run-tests.ps1` + `tests/fixtures/` | Per-script self-tests against a fixture vault holding one known-good and one known-bad note. A self-test whose target exits 2 records **BLOCKED, not FAIL**, and the harness then exits 2 rather than 1. |
| `agents/openai.yaml` | Add the `interface:` block: `display_name`, a `short_description` of 25–64 characters, a `default_prompt` containing `$alaa-memory-os`, and `policy: allow_implicit_invocation: true`. Model the shape on `alaa-golang/agents/openai.yaml`. |

### Rewritten in place

- `scripts/alaa_obsidian_linkcheck.ps1` — strip the two NUL bytes; add the explicit 0/1/2 exit
  mapping; replace `throw` at `:20` with exit 2; replace the O(notes × links) crediting loop at
  `:61-63` with a base-name index; make `:119` honour the resolved project instead of the hardcoded
  `alaa-memory`; state the Windows-only path handling rather than leaving it implicit.
- `scripts/alaa_memory_health.ps1` — fix `Invoke-Bm` to return only the exit code (assign
  `& bm @BmArgs 2>&1 | Out-Host` or capture explicitly); make `-Strict` exit 1 on findings and 2 when
  the store is unreachable; drive the 12 schema types from a parameter default rather than a literal.
- `scripts/alaa_memory_post_task.ps1`, `scripts/alaa_memory_reindex.ps1` — collapse onto
  `_common.ps1`; map "tool missing" and "store unreachable" to 2, "reported problem" to 1; make the
  schema-validation warning affect the exit code.
- `scripts/precompact_checkpoint.ps1` — BOM-less UTF-8 write; collision-proof filename (append a
  short random suffix); state in a comment that hook scripts are exempt from the 0/1/2 contract and
  why (exit 2 is reserved by the hook protocol).
- `scripts/session_start_context.ps1` — fix `:15-16` so the drift line reflects results, not command
  success; same hook-exemption comment.

### Retired to `_to_delete/2026-07-29-batch8/`

- `references/compact-and-handoff.md` — trespasses on `alaa-workflow`
  `references/context-continuity.md`, which says of exactly this material "Do not restate them here."
  One replacement sentence goes in the new body.
- `references/operating-model.md` — the four-surface block moves into the body; the store/do-not-store
  lists merge into `knowledge-shape.md` as the single authoritative list, preserving **every** member
  of all four current lists, including `secrets/credentials/tokens/cookies/private keys`, which today
  appears in only one of them.
- `references/obsidian-usage.md` — vocabulary half merges into `knowledge-shape.md`; the graph-hygiene
  half becomes the doc comment of the link checker.
- `alaa-basic-memory-os/` itself, after the rename stub has served its purpose.

### Also in scope for this lane's downstream edits

`skills/sohrab/README.md:117` and `README.fa.md` list this skill under the old name — and the
carry-over already records at `:216` that the README "does not match the directory" and must be
fixed in Batch 8. The rename should be folded into that single README pass rather than done twice.

---

## 9. Open questions for the owner

**Q1 — Are the existing `alaa-memory` notes migrated into Hindsight, or frozen as an archive?**
*Recommendation: migrate, with a custom import script, and keep the vault as a read-only archive
rather than deleting it.* Reason: the official plugins never send `timestamp`, so a plugin-driven
import stamps every historical note with import time; since Reflect supersedes on latest
`mentioned_at`, that flattens the entire history into one instant and destroys the ordering that
makes recall useful. A custom script sending each note's `last_verified` (or the session frontmatter
`session_datetime`) as `timestamp`, with the note permalink as `document_id`, preserves it — and
`document_id` makes the import safely re-runnable. Trade-off: freezing is zero work and zero risk but
means two places to look for a year; migrating costs one script and one careful dry run.

**Q2 — Does the drift registry move into Hindsight, or stay in the repository?**
*Recommendation: repository, permanently, under version control.* Reason in §2: Hindsight's
consolidation refines rather than preserves, and "do not delete drift notes; archive them (audit
trail)" (`drift-management.md:42`) cannot be enforced by a store whose entire value proposition is
synthesising a smoothed belief from conflicting evidence. Trade-off: the registry stops being
semantically searchable, so open drift will not surface through recall unless a tagged pointer is
also retained. Cost: one extra write per drift record.

**Q3 — Does this skill get renamed, or does the name `alaa-basic-memory-os` outlive the product?**
*Recommendation: rename to `alaa-memory-os`.* Reason: a skill named after a product it no longer
wraps mis-triggers — an agent working with Hindsight will not match a description built around
"Basic Memory project alaa-memory". Trade-off: the rename cost is real but bounded and fully
enumerated in §0 (4 skill/README call sites plus 3 carry-over mentions), and one of the two
`alaa-golang` call sites must be touched in Batch 8 anyway.

**Q4 — Is the vendored pack re-pointed from `basic-memory` to `hindsight-docs`, or are both carried?**
*Recommendation: carry both during the transition, then drop `basic-memory` at cutover.* Reason: the
whole of §5's Hindsight verification came from `skills/hindsight-docs/references/` — vendoring it
makes that verification local, greppable, and pinnable, instead of a live network fetch each batch.
Trade-off: `vendor/subtrees.json` grows one entry and one more subtree must be re-pulled; against
that, Hindsight ships weekly and a vendored pinned copy is the only way to make D10 tractable for a
0.x dependency.

**Q5 — What is the recall latency budget, and what does an agent do when it is exceeded?**
*Recommendation: 5 seconds, fail open, and a mandatory line in the final report saying memory was
unavailable.* Reason: recall is a contributor, not a gate — proceeding without it does not let
anything through that must not get through — so by `alaa-reliability-sla`'s discrimination question
it fails open. Drift *recording* is the opposite: it is a gate and must fail closed. Trade-off: a
5-second budget will be exceeded routinely against Basic Memory today (upstream #980 measures search
at ~12 s), which is itself part of the argument for the migration; setting it to 15 s to accommodate
the current store would bake the defect into policy.

**Q6 — Should the two hook scripts ship registered, or stay manual?**
*Recommendation: ship the registration snippets in `references/store-*.md` and leave installation
manual.* Reason: they currently ship as dead files — nothing in the repository references them but
one line of prose, so nobody can install them from the skill alone. Trade-off: auto-registration
would touch the user's `settings.json`, which is a shared-system change and belongs to
`alaa-controlled-ops`, not to this skill.

**Q7 — `D:\Sohrab\Project\raw\processed` could not be reached this session.**
Not a recommendation, a request: if `references/prompt-3-publishing.md` is to survive Phase 2 with
its three input paths asserted, that folder needs to be granted read access for one verification
pass, or those paths must be demoted to "as of the last check" with a re-derivation command beside
them.


---

# Appendix F — Repository hygiene and cross-reference survey

# L6 — Repository-wide hygiene and cross-reference survey

**Date of measurement:** 2026-07-29
**Tree measured:** `D:\Sohrab\Project\skills\skills\sohrab\`, reached read-only through
`mcp__remote-devices__device_bash`, mounted at
`/sessions/rcw-01nfpk8ndxrrswndyp6txjwc/mnt/skills/skills/sohrab` (referred to below as `$R`;
the repository root `D:\Sohrab\Project\skills` is `$S`).
**Method:** every number below was produced by a command printed beside it. No number is an estimate.
Scratch work ran in the device VM's `/tmp` (outside every mount) and in this container. Nothing under
`D:\` was created or modified.

## 0. Tree shape — the denominators every table below uses

| Quantity | Value | Command |
| --- | --- | --- |
| Directories directly under `skills/sohrab/` | 70 | `find $R -maxdepth 1 -mindepth 1 -type d \| wc -l` |
| Of those, directories holding a `SKILL.md` | **67** | `find $R -maxdepth 2 -name SKILL.md \| wc -l` |
| Non-skill directories | 3 — `.claude`, `.obsidian`, `_to_delete` | same walk, set difference |
| Total files under `skills/sohrab/` | 1317 | `find $R -type f \| wc -l` |
| Total bytes | 13,092,618 | `du -sb $R` |
| Markdown files inside skill directories | 805 | Python walk over the 67 skill roots |
| Repo-root `.md` files (not skills) | 9 (`AGENTS.md`, `CLAUDE.md`, `CONTRACT-DECISIONS.md`, `README.md`, `README.fa.md`, `UPGRADE-BATCH-5/6/7-ANALYSIS.md`, `UPGRADE-CARRYOVER.md`) | `ls -1 $R` |

**Correction to the carry-over.** The brief and `UPGRADE-CARRYOVER.md` speak of "~68 skill
directories". The measured count of directories carrying a `SKILL.md` is **67**. Every per-skill
table below has 67 rows. A concurrent lane's "814 files" and "813 md files" figures include the 9
repo-root Markdown files and the `_to_delete/` tree; scoped to skill directories the figure is 805.

---

## 1. The cross-reference resolution census — the headline deliverable

### 1.1 The measurement artifact that had to be removed first

`UPGRADE-CARRYOVER.md:198` assigns Batch 8 "a link check that every cross-skill path in
`skills/sohrab/` resolves". A concurrent lane's throwaway resolver reported **582 unresolved bare
paths across 223 files**, and read that as a mass missing-owner-prefix defect.

**That figure is a measurement artifact, and the defect it describes is roughly a hundred times
smaller than reported.** I reproduced it — my first-pass resolver, using the same "owner name must sit
immediately before the path" rule, produced **619 AMBIGUOUS-BARE across 235 files**, within 6% of the
concurrent lane's number. Then I looked at what the resolver was actually rejecting:

```
$R/alaa-frontend-developer/SKILL.md:33
| test design, layers, doubles, proof levels | `/alaa-testing-strategy` (`$alaa-testing-strategy`) `references/40-proof-strength.md` |
```

The owner **is** named alongside the path. The resolver missed it because the intervening
`` ` `` and `)` characters break token adjacency. The fleet's dominant citation form is
`` `/owner` (`$owner`) `references/…` ``, and any resolver that requires the owner to be the
immediately preceding path segment or word rejects all of it.

The same failure hits the second-largest form, where the owner is named *after* the path in a
two-column table:

```
$R/alaa-vue-typescript-clean-code/SKILL.md:49
| Identifier encode/decode, and `scripts/codec-conformance.sh` | `/alaa-crockford-base32-codecs` (`$alaa-crockford-base32-codecs`) |
```

The `references/40-proof-strength.md` example the carry-over cites as evidence of the defect is in
fact a **correctly attributed** citation in every file I checked. It is cited 20 times; 20 of those
citations name `alaa-testing-strategy` on the same line.

### 1.2 The definitive resolver

Built in this container's logic, executed against the device tree with `python3` on the device VM.
Classification order (each citation gets exactly one class; earlier rules win):

1. Path carries an explicit owning-skill prefix (`alaa-x/references/y.md`) → check that skill.
2. A known skill name other than the citing skill appears **earlier on the same line** and that
   skill owns the path → `RESOLVES-CROSS-SKILL`.
3. The path exists inside the citing skill → `RESOLVES-LOCALLY`.
4. A known skill name appears **later on the same line** and owns the path → `RESOLVES-CROSS-SKILL`.
5. A known skill name appears on a **preceding line within the same paragraph** (max 6 lines, stops
   at a blank line) and owns the path → `RESOLVES-CROSS-SKILL-CONTEXTUAL`.
6. Otherwise: exists in exactly one other skill → `AMBIGUOUS-BARE`; in more than one →
   `AMBIGUOUS-MULTI`; nowhere → `DANGLING`.

Path regex, final form. Three corrections were needed to get here, each caught by inspecting the
output rather than trusting it:

```
(?<![A-Za-z0-9_./-])((?:\.\.?/|[A-Za-z0-9_.-]+/)*?
 (?:references|scripts|assets|templates|agents|examples|prompts|evals|fixtures)
 /[A-Za-z0-9_./-]+\.(?:mjs|json|jsonc|md|js|py|sh|ps1|yaml|yml|toml|txt|sql|ts|cjs|vrl))(?![A-Za-z0-9])
```

1. **Extension alternation ordered longest-first.** `js|json` matches `.js` inside `.json`, which
   turned `references/arvan-caas-openAPI-1.25.json` (exists) into
   `references/arvan-caas-openAPI-1.25.js` (does not) and produced two phantom danglings.
2. **Leading directory segments must be kept, not consumed.** An earlier form treated any single
   leading segment as a possible owning-skill prefix and discarded it when it was not a skill name.
   That turned `assets/templates/vector-basic.yaml` into `templates/vector-basic.yaml` and invented
   36 phantom `templates/` danglings — including three against
   `vector-rust-observability-pipelines/SKILL.md:225-227`, whose paths in fact resolve.
3. **`./` and `../` resolve against the citing file's directory, not the skill root.**
   `alaa-makefile/references/00-topic-map.md:43` cites `` `../scripts/validate_makefile.sh` ``,
   which resolves correctly. 14 citations needed this.

### 1.3 The census — all bundled-resource prefixes

Command: single `python3` heredoc over all 805 skill Markdown files, results in `/tmp/rF.json`.

| Class | Citations | Share |
| --- | ---: | ---: |
| RESOLVES-LOCALLY | 2059 | 69.7% |
| RESOLVES-CROSS-SKILL (owner named on the same line, or as a path prefix) | 644 | 21.8% |
| RESOLVES-CROSS-SKILL-CONTEXTUAL (owner named on a nearby line, not alongside the path) | 154 | 5.2% |
| AMBIGUOUS-BARE (not local; exists in exactly one other skill; owner named nowhere near) | **4** | 0.14% |
| AMBIGUOUS-MULTI (exists in more than one other skill) | **5** | 0.17% |
| DANGLING (exists nowhere in the fleet) | 89 | 3.0% |
| DANGLING-NAMED (owner explicitly named, owner lacks the file) | **0** | 0% |
| **TOTAL** | **2955** | |

Owner-detection method histogram (same run): `LOCAL` 2059, `SAME-LINE-BEFORE` 637, `NEARBY-LINE`
154, `BARE` 98, `SAME-LINE-AFTER` 4, `PATH-PREFIX` 3.

**Robustness note.** Four successive generations of this resolver were run, differing in the three
corrections above. The `references/`-scoped census in §1.4 came out **bit-identical in all four** —
2252 citations, 1 DANGLING, 3 AMBIGUOUS-BARE, 4 AMBIGUOUS-MULTI, 150 CONTEXTUAL, 625 CROSS-SKILL,
1469 LOCAL. Only the non-`references/` prefixes moved. The headline number is not an artifact of the
regex.

### 1.4 The census scoped to `references/` — the number the carry-over actually asked for

`scripts/`, `templates/`, `assets/` and `agents/` paths in this fleet frequently name **paths in the
target repository the skill operates on**, not paths bundled inside the skill. `references/` is the
only prefix that is unambiguously skill-bundled. Scoped to it:

| Class | Citations |
| --- | ---: |
| RESOLVES-LOCALLY | 1469 |
| RESOLVES-CROSS-SKILL | 625 |
| RESOLVES-CROSS-SKILL-CONTEXTUAL | 150 |
| AMBIGUOUS-BARE | 3 |
| AMBIGUOUS-MULTI | 4 |
| DANGLING | **1** |
| **TOTAL** | **2252** |

**Every cross-skill `references/…` path in `skills/sohrab/` resolves, with eight exceptions.** The
link check `UPGRADE-CARRYOVER.md:198` demanded is, as of today, effectively already passing.

### 1.5 The full DANGLING list under `references/` — 1 citation

| Citing file:line | Cited path | Verdict |
| --- | --- | --- |
| `$R/ansible-validator/references/failure-classes.md:4` | `references/common_errors.md` | **Not a live citation.** The sentence is `` `references/common_errors.md`, which was a flat list of symptoms with prose `` — a retrospective note about a file this skill already retired. A checker must not fail on it, which is an argument for the past-tense/prose-context exclusion in §1.9. |

Two further `references/` danglings appeared in an earlier pass and are **regex artifacts, not
defects**: `caas-arvan-kuber/SKILL.md:39` and
`caas-arvan-kuber/references/arvan-capability-matrix.md:9` both cite
`references/arvan-caas-openAPI-1.25.json`, which exists; an extension alternation with `js` before
`json` truncated it to `.js`. Recorded here so the Phase 2 checker author does not repeat it.

### 1.6 The full AMBIGUOUS-MULTI list — 5 citations

| Citing file:line | Cited path | Skills that own a file of that name | Verdict |
| --- | --- | --- | --- |
| `$R/alaa-cicd-laravel-postgres/references/90-source-map.md:10` | `references/SOURCES.md` | 9 skills | **False positive.** The line reads `` …belongs to `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`) `references/SOURCES.md` ``. `alaa-gitlab-ci-cd` has no `references/SOURCES.md` — this is a genuine **broken cross-skill citation**, but of the DANGLING-NAMED kind, and the multi-owner ambiguity masks it. Real defect. |
| `$R/alaa-docker-production/references/00-source-map.md:4` | `references/SOURCES.md` | 9 skills | Self-referential prose: "It replaces the former `references/SOURCES.md`". Historical, not a live citation. |
| `$R/alaa-indexeddb-browser-storage/references/99-sources-and-maintenance.md:74` | `references/full-guide.md` | `alaa-docs-farsi`, `alaa-octane-performance` | Historical prose about this skill's own retired `full-guide.md`. Not a live citation. |
| `$R/alaa-input-normalization/references/60-provider-seam-and-open-items.md:16` | `scripts/phone-conformance-corpus.json` | `alaa-bale-provider`, `alaa-sms-provider-mediana` | **Deliberate.** The line documents that the corpus ships as "two byte-identical copies". The ambiguity is the design. |
| `$R/alaa-prompting-guide/references/60-skill-authoring.md:69` | `references/failure-taxonomy.md` | `alaa-cc-orchestrator`, `alaa-codex-orchestrator` | **Illustrative example inside a code span**, not a citation: `` `Read references/failure-taxonomy.md when a check fails` ``. A checker must exclude example text; see §1.9. |

Net: **one real defect** (`alaa-cicd-laravel-postgres:90-source-map.md:10` points at a
`references/SOURCES.md` that `alaa-gitlab-ci-cd` does not have), one deliberate duplicate, three
non-citations.

### 1.7 AMBIGUOUS-BARE — 4 citations, and there is no "twenty worst offenders" list to give

With the corrected resolver the class has 4 members, so the requested top-twenty table does not
exist. All four, in full:

| Citing file:line | Cited path | Sole owner | Note |
| --- | --- | --- | --- |
| `$R/alaa-shaka-player/references/50-offline-and-in-app-download.md:21` | `references/72-offline-media-store.md` | `alaa-indexeddb-browser-storage` | Owner named 7 lines above, across a blank line, inside a blockquote (`:16`). Paragraph-scope detection stops at the blank line. |
| `…:22` | `references/32-eviction-and-recovery.md` | `alaa-indexeddb-browser-storage` | same |
| `…:23` | `references/41-multitab-versionchange-and-locks.md` | `alaa-indexeddb-browser-storage` | same |
| `$R/alaa-vue-typescript-clean-code/references/72-frontend-security-binding.md:98` | `scripts/codec-conformance.sh` | `alaa-crockford-base32-codecs` | Owner named 3 lines above (`:96`), across a blank line. |

All four are the **same defect shape**: the owner is named in the paragraph that introduces the
subject, then the following paragraph lists bare paths. The prose is unambiguous to a human and
ambiguous to a tool. Under the convention as literally written
("cross-skill references always name the owning skill alongside the path") all four violate.

### 1.8 The class that *is* large — CONTEXTUAL, 154 citations across 79 files

This is what the concurrent lane's 582 was reaching for. These citations resolve unambiguously to
another skill, the owner **is** named nearby, but not alongside the path. Under a strict reading of
the convention they are violations; under a reading that admits paragraph scope they are fine.

Worst twenty citing files:

| Citations | File |
| ---: | --- |
| 10 | `alaa-mongodb-patterns/references/40-failure-configuration-and-observability.md` |
| 8 | `alaa-frontend-developer/references/25-frontend-security.md` |
| 8 | `alaa-frontend-developer/references/47-frontend-observability.md` |
| 7 | `alaa-frontend-developer/references/30-pwa-sw-and-offline.md` |
| 6 | `alaa-frontend-developer/references/46-resilience-and-degradation.md` |
| 5 | `alaa-frontend-developer/references/22-input-validation-and-normalization.md` |
| 4 | `alaa-data-layer/references/50-redis-laravel-octane.md` |
| 4 | `alaa-frontend-developer/references/21-ssr-auth-and-session-patterns.md` |
| 3 | `alaa-data-layer/references/30-concurrency-projections-and-pooling.md` |
| 3 | `alaa-data-layer/references/51-redis-golang.md` |
| 3 | `alaa-frontend-developer/references/10-contract-and-boundaries.md` |
| 3 | `alaa-frontend-developer/references/95-sources-and-maintenance.md` |
| 3 | `alaa-mongodb-patterns/references/30-writes-consistency-and-change-streams.md` |
| 3 | `alaa-octane-performance/references/full-guide.md` |
| 3 | `alaa-postman-collections/references/41-response-contract-and-error-coverage.md` |
| 3 | `alaa-trust-gateway-auth/references/20-claims-headers-and-sentinels.md` |
| 3 | `ansible-generator/references/module-patterns.md` |
| 3 | `clickhouse-performance-schema-ops/references/70-failure-and-degradation.md` |
| 3 | `clickhouse-performance-schema-ops/references/85-access-and-configuration.md` |
| 2 | `alaa-bale-provider/references/30-failure-classes.md` |

By skill: `alaa-frontend-developer` 58, `alaa-data-layer` 15, `alaa-mongodb-patterns` 15,
`alaa-octane-performance` 9, `clickhouse-performance-schema-ops` 8, `alaa-trust-gateway-auth` 6,
`alaa-shaka-player` 5, `ansible-generator` 5, `alaa-golang` 4,
`alaa-laravel-public-api-contract-pack` 4, `alaa-postman-collections` 4, then 12 skills with 1–2.

Representative site — `$R/alaa-mongodb-patterns/references/40-failure-configuration-and-observability.md:10-13`:

```
`references/10-deadlines-and-timeouts.md`, `references/20-retries.md`,
`references/40-admission-and-shedding.md`, and `references/50-degradation.md`. The Ala numbers behind them are
`references/22-failure-load-and-deprecation-contract.md`. This file owns only the MongoDB knobs and behaviours
```

Four paths belong to `alaa-reliability-sla`, one to `alaa-services-contract`, and the line naming
those owners is above the quoted block. **`alaa-frontend-developer` carries 38% of the whole class in
one skill**, which makes it a single-file-family fix rather than a fleet-wide one.

### 1.9 The 89 DANGLING outside `references/` — they are target-repository paths, not broken links

Once the resolver stops mangling leading directories, the shape of this class is unmistakable. First
segment of each dangling path:

| First segment | Citations | Reading |
| --- | ---: | --- |
| `scripts/` | 35 | mixed — see below |
| `assets/` | 9 | mixed |
| `charts/` | 9 | **Helm chart in the target repo** — `charts/gateway/templates/configmap.yaml`, `charts/wa/templates/deployment.yaml` |
| `service-runtime-kit/` | 8 | **another repository on this device**, `D:\Sohrab\Project\service-runtime-kit` |
| `SKILL_DIR/` | 7 | **a placeholder**, not a path — `alaa-postman-collections` writes `$SKILL_DIR/scripts/…` |
| `./` | 5 | a command example assuming the target repo's cwd |
| `docs/` | 4 | target-repo docs |
| `.service-ci-kit/` | 4 | **another repository**, `D:\Sohrab\Project\service-ci-kit` |
| `ci/` | 3 | target-repo CI directory |
| `../` | 2 | a command example assuming cwd is `skills/sohrab/` |
| `templates/` | 2 | target-repo chart templates |
| `references/` | 1 | §1.5 |

**31 of 89 name a top-level directory the citing skill has; 58 name one it does not have at all.**
Both groups are dominated by target-repository paths. The decisive experiment: adding `docs` to the
regex's directory alternation raises the DANGLING count from 89 to **520**, of which **422 are
`docs/…`** — a skill telling an agent to write `docs/BIG_PICTURE.md` in the repository it is working
on. No amount of resolver refinement makes those into broken links, because they were never links.

Full list of the 89, grouped (skill, path as written, citing lines):

```
alaa-bale-provider   ../alaa-sms-provider-mediana/scripts/validate_mediana_payload.py   [215]
alaa-bash-shell      ../scripts/validate-shell.sh                                       [20]
alaa-codex-orchestrator  ./alaa-codex-orchestrator/scripts/install-skill.sh             [30]
alaa-docker-production   scripts/docker/up-local.sh                                     [379]
alaa-docker-production   service-runtime-kit/scripts/render-runtime.sh                  [166]
alaa-docker-production   service-runtime-kit/scripts/up-local.sh                        [55, 376]
alaa-docker-production   service-runtime-kit/scripts/validate-runtime.sh                [78, 87, 226]
alaa-docker-production   service-runtime-kit/templates/generated/docker/octane/entrypoint.sh   [54]
alaa-docker-production   service-runtime-kit/templates/generated/docker/octane/healthcheck.sh  [52]
alaa-docker-production   templates/generated/scripts/docker/ensure-local-secrets.sh     [115]
alaa-gitlab-ci-cd    ./scripts/deploy.sh                                                [106, 111]
alaa-gitlab-ci-cd    ./scripts/teardown.sh                                              [122]
alaa-gitlab-ci-cd    ci/scripts/deploy.sh                                               [64]
alaa-k8s-helm        templates/NOTES.txt                                                [66]
alaa-laravel-job-rabbitmq   assets/helm/values.worker.rabbitmq.yaml                     [43, 67, 77]
alaa-laravel-upgrade-all-packages  docs/agents/dependency-freeze.md                     [15]
alaa-laravel-upgrade-all-packages  docs/agents/upgrade-all-packages-execution-state.md  [14]
alaa-makefile        .service-ci-kit/ci/scripts/build_image.sh                          [12, 91, 104]
alaa-makefile        .service-ci-kit/ci/scripts/release.sh                              [13]
alaa-makefile        ci/scripts/build_image.sh                                          [59, 77]
alaa-makefile        scripts/docker/up-local.sh                                         [24, 158]
alaa-minio-object-storage   docs/agents/tusd-api-contract-state.md                      [86, 195]
alaa-minio-object-storage   scripts/docker/smoke-compose-tar-tgz-extraction.sh          [85, 235]
alaa-minio-object-storage   scripts/docker/smoke-compose-upload.sh                      [85, 234]
alaa-minio-object-storage   scripts/docker/smoke-compose-zip-extraction.sh              [85, 234]
alaa-minio-object-storage   scripts/docker/validate-compose-runtime.sh                  [86, 196]
alaa-octane-performance     ./scripts/octane-rss-check.sh                               [92]
alaa-postman-collections    SKILL_DIR/scripts/audit_collection_contract.py              [45, 134]
alaa-postman-collections    SKILL_DIR/scripts/validate_postman_artifacts.py             [72, 78, 85, 104, 147]
alaa-postman-collections    scripts/postman/audit_collection_contract.py                [45]
alaa-postman-collections    scripts/postman/generate_gateway_collection.sh              [77]
alaa-services-contract      charts/gateway/templates/configmap.yaml                     [204, 230, 246, 313, 322]
alaa-services-contract      charts/wa/templates/deployment.yaml                         [355]
alaa-services-contract      scripts/docker/up-local.sh                                  [40]
alaa-services-contract      scripts/validate_sohrab_skill_pack.py                       [277, 280]
alaa-sms-provider-mediana   ../alaa-bale-provider/scripts/validate_bale_payload.py      [108]
alaa-trust-gateway-auth     charts/gateway/templates/configmap.yaml                     [48, 183]
ansible-generator           scripts/setup.sh                                            [379]
ansible-validator           assets/molecule.yml                                         [60]
ansible-validator           fixtures/{extract,fqcn,lint,modules,secrets,tasks,yaml}/…   [47–56, 11 paths]
ansible-validator           references/common_errors.md                                 [4]   (§1.5)
caas-arvan-kuber            assets/README.operator.md                                   [15]
caas-arvan-kuber            assets/RUNBOOK.operator.md                                  [15]
caas-arvan-kuber            assets/values.secret.yaml                                   [54, 71, 137]
service-runtime-kit-governance  scripts/docker/ensure-local-secrets.sh                  [20]
service-runtime-kit-governance  scripts/docker/ensure-swarm-runtime-secrets.sh          [20]
service-runtime-kit-governance  scripts/docker/provision-postgres.sh                    [20]
service-runtime-kit-governance  scripts/docker/provision-rabbitmq.sh                    [20]
service-runtime-kit-governance  scripts/docker/up-local.sh                              [20, 26, 30, 36]
service-runtime-kit-governance  scripts/runtime/ensure-runtime-kit.sh                   [12]
service-runtime-kit-governance  scripts/runtime/render-runtime.sh                       [9, 17, 24, 63]
service-runtime-kit-governance  scripts/runtime/validate-runtime.sh                     [17, 64, 73]
service-runtime-kit-governance  scripts/setup-git-hooks-bom.ps1                         [66]
service-runtime-kit-governance  scripts/setup-git-hooks-bom.sh                          [65]
```

Verified spot-checks:

- `$R/ansible-validator/test/README.md:47-56` — the eleven `fixtures/…` paths are cited from
  `test/README.md` and there is no `ansible-validator/test/fixtures/` or
  `ansible-validator/scripts/fixtures/` directory. **This is a real defect**: a test README
  documenting eleven fixture files the skill does not ship.
- `$R/alaa-bale-provider/references/40-phone-and-conformance.md:215` — the line is a shell command,
  `python3 ../alaa-sms-provider-mediana/scripts/validate_mediana_payload.py --self-test`. It resolves
  only if cwd is `skills/sohrab/<some-skill>/`, and the reciprocal command in
  `alaa-sms-provider-mediana/references/…:108` has the same shape. **A real usability defect**: both
  commands are correct from exactly one undocumented working directory.
- `$R/alaa-postman-collections` writes `$SKILL_DIR/scripts/…` at 7 sites — a documented placeholder,
  not a defect. But it also writes `scripts/postman/audit_collection_contract.py`
  (`references/70-aggregate-collections-and-consumer-repos.md:45`) while shipping
  `scripts/audit_collection_contract.py` with no `postman/` subdirectory. **Batch 8 member; needs a
  decision** — target-repo path or stale self-citation.
- `$R/alaa-services-contract/references/24-metric-registry.md:277,280` cites
  `scripts/validate_sohrab_skill_pack.py`, which lives at the **repository root**
  (`skills/scripts/…`), not inside the skill. Correct as prose, unresolvable as a path.

**This is the reason a naive fleet link checker produces 88 false positives on day one**, and the
reason §1.11 scopes failures to `references/` and reports everything else as INFO.

### 1.10 Markdown links versus inline code — confirming the concurrent lane

| Quantity | Value | Command |
| --- | ---: | --- |
| Markdown links whose target contains a bundled-resource prefix | **8** | `grep -roE '\]\([^)]*(references\|scripts\|assets\|templates)/[^)]*\)' $R --include=*.md \| wc -l` |
| Inline path citations (all prefixes) | **2955** | resolver run, §1.3 |

The concurrent lane's finding stands and is stronger than it reported: a link checker built on
Markdown link syntax would inspect **0.27%** of this fleet's cross-references.

### 1.11 The checker Phase 2 must write

**Name:** `check_fleet_references.py`
**Location:** `skills/scripts/check_fleet_references.py` — beside
`validate_sohrab_skill_pack.py`, not inside any skill. It is a fleet-scope tool; putting it in a
skill would make one skill the owner of every other skill's correctness.
**Interpreter:** Python 3, standard library only. It must run on Windows PowerShell with no
`npm install` and no `pip install`. It must not use `Path(__file__).resolve().parents[N]` — see §7.4;
it takes `--root` and defaults to the current working directory's nearest ancestor containing
`skills/sohrab/`, failing with exit 2 if it cannot find one.

**Flags:**

| Flag | Behaviour |
| --- | --- |
| `--root PATH` | repository root. Default: search upward from cwd for `skills/sohrab/`. |
| `--skill NAME` (repeatable) | restrict scanning to these skills. Default: all 67. |
| `--strict-owner` | promote `RESOLVES-CROSS-SKILL-CONTEXTUAL` from pass to finding. Default off. |
| `--baseline PATH` | read a baseline file; suppress every finding whose key is present. |
| `--write-baseline PATH` | write the current findings as a baseline and exit 0. |
| `--format {text,json}` | `json` emits one object per finding for CI ingestion. Default `text`. |
| `--self-test` | run against bundled fixtures; exit 0 pass, 1 fail, 2 could not run. |
| `--help` | usage, the rule list, and the exit-code table. |

**What it asserts, rule by rule:**

| Rule id | Assertion | Default severity |
| --- | --- | --- |
| `R1-DANGLING-NAMED` | A citation that explicitly names an owning skill resolves inside that skill. | finding |
| `R2-DANGLING-LOCAL` | A `references/…` citation with no named owner resolves inside the citing skill. | finding |
| `R3-AMBIGUOUS-MULTI` | No `references/…` citation resolves in more than one other skill with no owner named. | finding |
| `R4-AMBIGUOUS-BARE` | No `references/…` citation resolves only in another skill with no owner named anywhere in its paragraph. | finding |
| `R5-CONTEXTUAL` | The owning skill is named on the **same line** as the path. | off unless `--strict-owner` |
| `R6-TOPIC-MAP` | Every path in `references/00-topic-map.md` resolves. | finding |

**Exclusions, each with the evidence that forces it** (a checker without these produces 88+4
false positives on day one and will be switched off within a week):

1. **Non-`references/` prefixes are advisory only.** `scripts/`, `templates/`, `assets/`, `agents/`
   paths are reported under a separate `INFO` heading and never fail the build, because 58 of 89
   name a directory the citing skill does not have, and the rest name paths in another repository
   on the same disk (§1.9). Promote to findings only behind a future
   `--check-bundled-assets` flag once the fleet distinguishes the two path kinds in prose.
2. **Skip a line whose path sits inside an illustrative code span in a sentence about authoring
   skills** — evidence: `$R/alaa-prompting-guide/references/60-skill-authoring.md:69`. Concretely:
   skip when the code span contains whitespace (the span is a command or a sentence, not a path).
   `validate_sohrab_skill_pack.py:33` already implements exactly this as `is_command_example`.
3. **Skip past-tense retirement prose.** Evidence: `ansible-validator/references/failure-classes.md:4`,
   `alaa-docker-production/references/00-source-map.md:4`,
   `alaa-indexeddb-browser-storage/references/99-sources-and-maintenance.md:74`. Rule: skip when the
   same line matches `\b(was|were|formerly|replaces the former|used to be|retired)\b` within 80
   characters before the path.
4. **Skip globs and placeholders** — `*`, `?`, `[`, `]`, `<`, `>`. Already implemented as
   `validate_sohrab_skill_pack.py:29` `is_placeholder_or_glob`.

**Exit codes — the contract:**

| Code | Meaning | Trigger |
| ---: | --- | --- |
| 0 | clean | zero findings after baseline suppression |
| 1 | findings | one or more findings after baseline suppression |
| 2 | could not run | `--root` not found; `skills/sohrab/` absent; a Markdown file unreadable or undecodable; zero skills discovered; baseline file named but unreadable or malformed |

The zero-skills case matters: a CI gate that runs the checker from the wrong directory must not see
a pass. `validate_sohrab_skill_pack.py` today returns only 0 or 1
(`skills/scripts/validate_sohrab_skill_pack.py:221` — `return 1 if errors else 0`) and therefore has
exactly this hole.

**Baseline handling — how an existing backlog does not make it useless on day one:**

- Baseline file: `skills/scripts/fleet-references-baseline.txt`, one finding per line, sorted, with
  `#` comments allowed.
- **Finding key is `<rule-id>|<citing-skill>|<citing-file-relpath>|<cited-path>` — deliberately not
  the line number.** A line number changes on every unrelated edit above it and would make the
  baseline churn on every commit and silently un-suppress real findings.
- `--write-baseline` regenerates it. Run once at adoption.
- **The baseline shrinks and never grows.** The checker exits 1 when a baseline entry no longer
  matches any finding (`stale baseline entry`) as well as when a new finding appears. Without that,
  a baseline becomes a permanent amnesty.
- Baseline entries carry a `# owner: <skill>` comment so a reviewer can see who owes the fix.
- Seed value today, at the checker's default scope (`references/` fails, other prefixes are INFO):
  with `--strict-owner` **off** the baseline is **8 entries** — 3 AMBIGUOUS-BARE + 4 AMBIGUOUS-MULTI
  + 1 DANGLING (§1.4). That is small enough that the honest option is to fix all eight and adopt with
  no baseline at all. With `--strict-owner` **on** the baseline is **158 entries** (those 8 plus the
  150 CONTEXTUAL citations under `references/`) and the baseline mechanism earns its keep.

**Recommendation:** ship it with `--strict-owner` off and no baseline; fix the 9. Add
`--strict-owner` to CI only after `alaa-frontend-developer`'s 58 CONTEXTUAL citations are converted,
because that one skill is 38% of the class.

---

## 2. The executable-check census

Scope: files under each skill's `scripts/` directory with extension
`.py .sh .mjs .js .ps1 .cjs .ts`.
Command: `python3` walk over `$R/*/scripts/`, purpose line extracted from each file's header
comment or module docstring.

**Fleet total: 101 scripts across 43 skills. 24 of 67 skills ship zero.**

### 2.1 Exit-code contract — method and its limits

Determined by reading exit paths, never by running. Two detectors were run and unioned:

1. numeric literals in `sys.exit(N)`, `SystemExit(N)`, `process.exit(N)`, `return N`, `exit N`;
2. named-constant resolution — collect `NAME = <int>` and tuple assignments
   (`EXIT_CLEAN, EXIT_FINDINGS, EXIT_CANNOT_RUN = 0, 1, 2`), then resolve `return EXIT_CANNOT_RUN`.

The second detector was necessary: the first reported `alaa-trust-gateway-auth/scripts/trust_boundary_check.py`
as having **no** exit codes, when the file in fact declares `EXIT_USAGE = 2` at `:38` and
`EXIT_NOT_RUN = 3` at `:39`.

| Measure | Value |
| --- | ---: |
| Scripts with a demonstrable exit-2 ("could not run") path | **63 / 101** |
| Scripts with all three of 0, 1, 2 demonstrable | **49 / 101** |
| Scripts accepting `--self-test` | 70 / 101 |
| Scripts accepting `--help` | 49 / 101 |
| Scripts documenting an exit contract in their first 60 lines | 51 / 101 |

**Known residual false negatives, stated so the number is not over-trusted.** Static analysis cannot
follow an exit routed through a sourced shell library or a helper function. Nine
`ansible-validator/scripts/*.sh` files show no literal `exit 2` but `source` `scripts/lib/common.sh`,
which does carry the full 0/1/2 contract (`ansible-validator/scripts/lib/common.sh`, header states
it). `ansible-validator/scripts/self_test.sh` exists precisely to assert this — its header reads
"run every checker's own `--self-test` and assert that the four exit codes are distinct across the
whole toolchain". Treat the 63 as a floor.

### 2.2 The 24 skills that ship zero executable checks

Under this programme's rule — *a skill whose rules have no tool that reports a violation is shipping
preferences, not rules* — these 24 ship preferences:

`alaa-algorithms-data-structures`, `alaa-codex-runtime-ops`, `alaa-controlled-ops`,
`alaa-data-layer`, `alaa-frontend-developer`, `alaa-golang`, `alaa-golang-clean-code-principles`,
`alaa-golang-fiber`, `alaa-keyset-pagination`, `alaa-laravel-job-rabbitmq`,
`alaa-laravel-upgrade-all-packages`, `alaa-low-noise`, `alaa-mongodb-patterns`,
`alaa-observability-soc`, `alaa-octane-performance`, `alaa-php-clean-code`, `alaa-prompting-guide`,
`alaa-reliability-sla`, `alaa-security-review`, `alaa-services-contract`,
**`alaa-signoz-clickhouse-docs`**, `alaa-system-design`, `alaa-testing-strategy`,
`service-runtime-kit-governance`.

Two observations that matter more than the count:

- **Eight of the twenty-four are doctrine owners** the lane brief names as "already at standard":
  `alaa-services-contract`, `alaa-observability-soc`, `alaa-reliability-sla`,
  `alaa-security-review`, `alaa-testing-strategy`, `alaa-system-design`, `alaa-controlled-ops`,
  `alaa-data-layer`, plus `alaa-low-noise`, `alaa-prompting-guide`,
  `alaa-algorithms-data-structures`, `alaa-keyset-pagination` and
  `service-runtime-kit-governance`. The fleet's authorities are the least verifiable parts of it.
  `alaa-services-contract` is the extreme case: it owns every metric name, log field and error code
  in the fleet, and the only tool that checks any of it lives in *another* repository directory —
  `validate_sohrab_skill_pack.py:96` `check_registries()`, which is hard-coded to fire only when
  `skill_dir.name == "alaa-services-contract"`.
- **`alaa-signoz-clickhouse-docs` is a Batch 8 member with zero checkers.**
- `alaa-frontend-developer` now ships zero because its only script was correctly retired (§8); it
  routes to the owner instead, which is the right outcome, not a gap.

### 2.3 Per-skill table — all 67 skills

`2✓` = scripts with a demonstrable exit-2 path.

| Skill | Scripts | 2✓ | Script names and what each asserts |
| --- | ---: | ---: | --- |
| alaa-algorithms-data-structures | 0 | 0 | — |
| alaa-arvan-object-storage | 1 | 1 | `check_arvan_storage_config.py` — lexical configuration checker for ArvanCloud Object Storage consumers. codes 0/1/2/3 |
| alaa-async-messaging | 1 | 1 | `check-consumer-bounds.sh` — fails a change on three message-plane defects no single-file review catches (C1: consumer construction with no explicit prefetch, …). 0/1/2 |
| alaa-bale-provider | 1 | 1 | `validate_bale_payload.py` — validates Bale Safir payloads and normalises Iranian mobile numbers for the Safir wire |
| alaa-bash-shell | 2 | 1 | `new-script.sh` scaffolds a shell file from a bundled template (0/1, **no 2**); `validate-shell.sh` validates Bash/POSIX with locally available tools (0/1/2) |
| alaa-basic-memory-os | 6 | **0** | `alaa_memory_health.ps1`, `alaa_memory_post_task.ps1`, `alaa_memory_reindex.ps1`, `alaa_obsidian_linkcheck.ps1`, `precompact_checkpoint.ps1`, `session_start_context.ps1` — **none carries a header comment, none documents an exit contract, none has a demonstrable exit-2 path.** Batch 8 member. |
| alaa-cc-orchestrator | 3 | 1 | `Invoke-AlaaLowPriority.ps1` (no header); `run-low-priority.sh` (exit 2 only); `validate_pack.py` — structural validator for the pack, exits 1 only |
| alaa-cicd-laravel-postgres | 1 | 1 | `check-ci-determinism.sh` — lexical determinism checks over a CI configuration; POSIX sh, no dependencies beyond grep/sed/mktemp. 0/1/2/3/4 |
| alaa-codex-orchestrator | 8 | 2 | `Get-AlaaCodexAgentStatus.ps1`, `Install-AlaaCodexAgents.ps1`, `Install-AlaaCodexOrchestrator.ps1`, `Invoke-AlaaLowPriority.ps1` (all four: no header, no contract); `install-agents.sh` (1/2); `install-skill.sh` (0/1); `run-low-priority.sh` (2); `validate_pack.py` (1 only) |
| alaa-codex-runtime-ops | 0 | 0 | — |
| alaa-controlled-ops | 0 | 0 | — |
| alaa-crockford-base32-codecs | 2 | 1 | `codec-conformance.sh` — cross-runtime conformance harness driving all four shipped codec implementations over one shared corpus; `crockford-base32-cli.sh` — reference CLI, header names the owning reference file |
| alaa-data-layer | 0 | 0 | — |
| alaa-docker-production | 7 | 5 | `check-compose-interpolation.mjs` (fail-closed interpolation, enforces `references/25-…`); `check-dockerfile-contract.mjs` (Dockerfile authorship, `references/10-…`); `check-image-pinning.mjs` (image-reference determinism + freshness, `references/45-…`); `check-stack-rollout.mjs` (Swarm rollout control, `references/30-…`); `lib/common.mjs` (shared helpers; states the five contracts every checker obeys); `lib/mini-yaml.mjs`, `lib/safety-controls.mjs` (libraries, no exit path — correct) |
| alaa-docs-farsi | 1 | 1 | `check_markdown_links.py` — validates inline and reference-style Markdown links for local docs. 0/1/2 verified at `:177,:184,:198,:202`. Batch 8 member. |
| alaa-frontend-developer | 0 | 0 | — (correctly retired; routes to `alaa-quasar-app-vite-v3`, §8) |
| alaa-frontend-devops | 1 | 1 | `verify-artifact-contract.mjs` — asserts a frontend build output tree against the declared artifact contract |
| alaa-frontend-doc-annotations | 1 | 1 | `check-annotations.mjs` — checks comments against the code they claim to describe; never edits. Header states "0 clean, 1 findings, 2 could not run" |
| alaa-gitlab-ci-cd | 2 | 2 | `validate_gitlab_ci.py` (static GitLab CI/CD validator, 55.8 KB); `validate_runner_config.py` (static validator for Runner `config.toml` and Runner Helm `values.yaml`) |
| alaa-go-chi-development | 1 | 1 | `phase-check.sh` — reads the alaa-go-chi execution scope phase from repository truth; 0/1/2/3/4/5 |
| alaa-golang | 0 | 0 | — |
| alaa-golang-clean-code-principles | 0 | 0 | — |
| alaa-golang-fiber | 0 | 0 | — |
| alaa-haproxy | 2 | 2 | `check_defaults_scope.py` (enforces the HAProxy `defaults` association rule); `check_examples.py` (checks every HAProxy example shipped in the skill) |
| alaa-haproxy-lua | 1 | 1 | `check_haproxy_lua.py` — static checker for HAProxy Lua modules |
| alaa-indexeddb-browser-storage | 3 | 3 | `capability_contract_conformance.py` (asserts the three declarations of one contract agree and every index resolves); `check_references.py` (every reference reachable, every path resolves — declares `EXIT_CLEAN, EXIT_FINDINGS, EXIT_CANNOT_RUN = 0, 1, 2` at `:23`); `validate_skill_pack.py` (structure, trigger syntax, boundaries, budget templates) |
| alaa-input-normalization | 1 | 0 | `normalization-conformance.sh` — cross-language conformance harness over `assets/input-normalization/`; codes 0/1/3/4/5/6 detected, **no exit-2 path found** |
| alaa-k8s-helm | 9 | 5 | `check_manifests.py`; `check_tools.sh` (tool inventory, 0/1 only); `check_versions.py` (re-derives the pins in `references/version-awareness.md`); `cluster_health.sh` (read-only snapshot); `detect_crd.py` + `detect_crd_wrapper.sh` (classify YAML docs as k8s/OpenShift/custom; wrapper supplies PyYAML, 0/1 only); `network_debug.sh` (read-only, **no code detected**); `pod_diagnostics.py`; `validate_chart_structure.sh` (0 only) |
| alaa-keyset-pagination | 0 | 0 | — |
| alaa-laravel-architecture | 1 | 1 | `architecture-gate.sh` — fails a build on five Laravel layer-boundary defect classes. 0/1/2 |
| alaa-laravel-job-rabbitmq | 0 | 0 | — |
| alaa-laravel-public-api-contract-pack | 1 | 0 | `contract_pack_audit.py` — deterministic audit for a Laravel public API contract pack; codes 0/1/3, **no exit-2 path found** |
| alaa-laravel-upgrade-all-packages | 0 | 0 | — |
| alaa-low-noise | 0 | 0 | — |
| alaa-makefile | 3 | 3 | `add_standard_targets.sh`, `generate_makefile_template.sh` (both 0/1 literal; both state bash ≥4.2 and the `.gitattributes` LF requirement); `validate_makefile.sh` (0/1/2, 44 KB) |
| alaa-minio-object-storage | 1 | 1 | `check_object_storage_posture.py` — static posture checker for an object-storage consumer repository. 0/1/2/3 |
| alaa-mongodb-patterns | 0 | 0 | — |
| alaa-mono-package | 1 | 1 | `verify-package-entrypoints.mjs` — asserts export surface, peer contract and asset side-effect declaration of every workspace package |
| alaa-observability-soc | 0 | 0 | — |
| alaa-octane-performance | 0 | 0 | — |
| alaa-partitioned-table-fk-audit | 1 | 1 | `partitioned_fk_audit.py` — audits source trees for foreign keys referencing a partitioned parent through an incomplete key |
| alaa-permission-generator | 1 | 0 | `bitmap-conformance.sh` — cross-language conformance harness over `assets/permission-bitmap/`; codes 0/3/4/5/6, **no exit-2 path found** |
| alaa-php-clean-code | 0 | 0 | — |
| alaa-postman-collections | 2 | 1 | `audit_collection_contract.py` — audits Postman v2.1 request documentation, examples and executable scripts; **exit 1 only, no 0/2 path, no `--help`, no `--self-test`**. `validate_postman_artifacts.py` — validates Collection v2.1 and environment artifacts as an implementation contract; declares `EXIT_OK/RULES/INPUT/SCHEMA/SECRET = 0/1/2/3/4` at `:30-34`, **no `--help`, no `--self-test`**. Batch 8 member. |
| alaa-project-constitution | 1 | 1 | `validate_constitution.py` — validates constitution templates and generated constitutions. 0/1/2 |
| alaa-prompting-guide | 0 | 0 | — |
| alaa-quasar-app-vite-v3 | 2 | 2 | `check-upstream-versions.mjs` — package-manager-neutral npm snapshot; its own header states "exit codes are meaningful and 'could not run' is never reported as 'clean'". `query-installed-quasar-api.mjs` — delegates exact API output to the target project's installed Quasar CLI |
| alaa-reliability-sla | 0 | 0 | — |
| alaa-security-review | 0 | 0 | — |
| alaa-services-contract | 0 | 0 | — (its registries are checked from `skills/scripts/validate_sohrab_skill_pack.py:96`) |
| alaa-shaka-player | 1 | 1 | `check-shaka-api.mjs` — reports Shaka call sites using an API removed or deprecated between the installed version and the current release |
| alaa-signoz-clickhouse-docs | **0** | 0 | — Batch 8 member |
| alaa-sms-provider-mediana | 1 | 1 | `validate_mediana_payload.py` — validates a Mediana/IPPanel Edge payload, or normalises an Iranian mobile number |
| alaa-system-design | 0 | 0 | — |
| alaa-testing-strategy | 0 | 0 | — |
| alaa-trust-gateway-auth | 1 | 1 | `trust_boundary_check.py` — deterministic checks on the Ala gateway trust boundary; `EXIT_USAGE = 2` at `:38`, `EXIT_NOT_RUN = 3` at `:39`, exit-code epilogue at `:763` |
| alaa-ui-ux-design-system | 1 | 1 | `check-design-system.mjs` — header states "A design rule with no tool that reports its violation is a preference"; `EXIT_COULD_NOT_RUN` used at `:584,:585,:590,:638` |
| alaa-vue-typescript-clean-code | 1 | 1 | `check-frontend-versions.mjs` — installed-versus-latest for the packages that gate this skill's rules |
| alaa-workflow | 2 | **0** | `init_workflow_files.py` (creates workflow artifacts, exit 0 only); `validate_workflow_files.py` (semantic validation of adaptive and legacy artifacts, **exit 1 only — no 0/2 discrimination**) |
| ansible-generator | 1 | 1 | `check_templates.py` — asserts generated Ansible parses and nothing was left unsubstituted |
| ansible-validator | 18 | 10 | `check_assets.sh` (proves shipped lint configs still enable the rules they claim); `check_fqcn.py`/`check_fqcn.sh` (short-name vs FQCN); `check_module_currency.py` (an FQCN that no longer resolves); `check_task_safety.py`; `extract_ansible_info.py` + wrapper; `scan_secrets.sh` (credential shapes Checkov's ansible framework does not model); `self_test.sh` (**asserts the four exit codes are distinct across the whole toolchain**); `setup_tools.sh` (enforces tool floors, not merely prints them); `test_role.sh` (Molecule; never runs on its own initiative); `validate_playbook{,_security}.sh`; `validate_role{,_security}.sh`; `lib/ansible_walk.py`, `lib/checkov_scan.sh`, `lib/common.sh` (the shared exit-code contract) |
| caas-arvan-kuber | 3 | 2 | `render-helm.sh` (deterministic Helm render; header states the security defect the previous version had — rendered output contains every Secret); `summarize-openapi.sh` (only permitted reader of the 1.5 MB vendored OpenAPI document); `verify-cluster.sh` (read-only capability and RBAC probe, creates/updates/deletes nothing) |
| clickhouse-performance-schema-ops | 1 | 1 | `review_clickhouse_ddl.py` — reviews CREATE TABLE statements against the skill's stated rules |
| jitsi-platform-architect | 1 | 1 | `check_jitsi_jwt.py` — asserts the Jitsi join-token claim contract and the room-name rules. 0/1/2/3 |
| service-runtime-kit-governance | 0 | 0 | — |
| tusd-upload-platform | 1 | 1 | `validate_pack.py` — validates the skill pack. 0/1/2 |
| vector-rust-observability-pipelines | 1 | **0** | `validate-and-test.sh` — **240 bytes, no header comment, exit 1 only**. The smallest checker in the fleet by an order of magnitude; the next smallest is `alaa-cc-orchestrator/scripts/run-low-priority.sh` at 822 bytes. Batch 8 member. |

### 2.4 The Batch 8 members' checker posture, isolated

| Skill | Scripts | Verdict |
| --- | ---: | --- |
| `alaa-signoz-clickhouse-docs` | 0 | ships preferences |
| `vector-rust-observability-pipelines` | 1 (240 bytes, exit 1 only, no header, no `--help`, no `--self-test`) | effectively ships preferences |
| `alaa-basic-memory-os` | 6 PowerShell, none with a header, none with a demonstrable exit-2 path | no contract |
| `alaa-postman-collections` | 2 (17 KB + 38 KB, substantive), neither with `--help` or `--self-test` | real checkers, missing the fleet's ergonomics |
| `alaa-docs-farsi` | 1, full 0/1/2, but no `--help` and no `--self-test` | closest to standard |

---

## 3. The router-convention census — and whether the convention survives

Convention under test: **≤8 references → list them in `SKILL.md` with a trigger condition each;
≥9 references → use a separate `references/00-topic-map.md`.**

Command: `python3` — for each skill, `len([f for f in os.listdir(skill/references) if
f.endswith('.md')])` and `'00-topic-map.md' in that list`.

| Quantity | Value |
| --- | ---: |
| Skills with a `references/00-topic-map.md` | **29 / 67** |
| Skills without | 38 / 67 |
| CONFORMS (counting the topic map itself as a reference) | 64 / 67 |
| CONFORMS (excluding the topic map from the count) | 61 / 67 |

The carry-over records "28 of 68 carry `references/00-topic-map.md` and 40 do not". Measured today:
**29 of 67 and 38 do not.**

### 3.1 The threshold is ambiguous, and three skills fall exactly on the ambiguity

Does the topic map count toward its own threshold? The convention as written does not say, and three
skills sit precisely on the seam:

| Skill | `.md` files in `references/` | Of which the topic map | Verdict if map counts | Verdict if map does not count |
| --- | ---: | --- | --- | --- |
| `alaa-bash-shell` | 9 | yes | CONFORMS (9 ≥ 9) | VIOLATES — 8 body refs, should not have a map |
| `alaa-reliability-sla` | 9 | yes | CONFORMS | VIOLATES — 8 body refs |
| `alaa-async-messaging` | 9 | no | VIOLATES — 9 refs, no map | VIOLATES — 9 refs, no map |

`UPGRADE-CARRYOVER.md` does not resolve this. **Phase 2 must pick one reading and write it down**;
otherwise three skills oscillate between conforming and violating depending on who reads the rule.
Recommended reading: **the topic map does not count toward its own threshold** — the threshold is
about how many *destinations* a router must offer, and a router is not a destination. Under that
reading `alaa-bash-shell` and `alaa-reliability-sla` become violations.

### 3.2 Violations — ≥9 references and no topic map

| Skill | References | Note |
| --- | ---: | --- |
| `alaa-prompting-guide` | 14 | The worst case. It is a doctrine owner named in the lane brief as "the authority for every model and effort question", cited bare or contextually 37 times fleet-wide for `references/50-effort-and-thinking.md` alone (§1.7 data), and offers no router. |
| **`vector-rust-observability-pipelines`** | 11 | **Batch 8 member.** Also carries a 227-line `SKILL.md` body — the largest in the fleet (§6). |
| `alaa-async-messaging` | 9 | Exactly on the threshold. |

### 3.3 Violations — ≤8 references and a topic map

| Skill | References | Body references (excl. map) | Note |
| --- | ---: | ---: | --- |
| `alaa-codex-runtime-ops` | 6 | 5 | Unambiguous violation under either reading. |
| `alaa-bash-shell` | 9 | 8 | Seam case, §3.1. |
| `alaa-reliability-sla` | 9 | 8 | Seam case, §3.1. |

### 3.4 Does the convention survive contact with the data?

**Yes, and the threshold is right.** Evidence:

- 61 of 67 skills conform under the stricter reading; 64 under the looser one. A convention with a
  91–96% observed compliance rate is a description of practice, not an aspiration.
- The distribution has no mass at the boundary that would suggest a wrong threshold. Skills without
  a map: median 7 references, max 14 (`alaa-prompting-guide`). Skills with a map: min 6
  (`alaa-codex-runtime-ops`, the violation), then 9, and the bulk sit at 10–32.
- The three seam cases are an artifact of the rule's silence about whether the map counts itself,
  not of the number 8 being wrong.

**What the data does argue against is making the convention mandatory as a build gate today.**
Three of the four unambiguous violations are large, heavily cited doctrine skills
(`alaa-prompting-guide` 14 refs, `vector-rust-observability-pipelines` 11 refs) where the fix is a
real authoring task, not a formatting change. Recommend: state the tie-break in `AGENTS.md`, add the
rule to `validate_sohrab_skill_pack.py` as a **warning**, and promote it to an error only after the
four are fixed.

---

## 4. Trigger-syntax census, in both directions

Command: per skill, over every `.md` file in the skill directory, count matches of
`(?<![A-Za-z0-9_/.$-])/(<any of the 67 skill names>)(?![A-Za-z0-9_-])` for Claude Code and
`(?<![A-Za-z0-9_${-])\$(<any of the 67 skill names>)(?![A-Za-z0-9_-])` for Codex. The negative
look-behind on `{` and the requirement that the token be a **known skill name** exclude `$PATH`,
`${VAR}`, `$1` and every other shell variable by construction. `agents/openai.yaml` is excluded
because only `.md` files are scanned.

`cc` = `/name` occurrences, `cx` = `$name` occurrences.

### 4.1 Skills with one direction and zero of the other

| Skill | cc (all `.md`) | cx (all `.md`) | cc (SKILL.md) | cx (SKILL.md) | Verdict |
| --- | ---: | ---: | ---: | ---: | --- |
| `alaa-cc-orchestrator` | **97** | **0** | 3 | 0 | Claude-only. Arguably legitimate — it is the Claude Code orchestrator — but 97 to 0 means it can never route a reader to a Codex counterpart. |
| `alaa-codex-orchestrator` | **0** | **33** | 0 | 2 | Codex-only, mirror image. |
| **`alaa-docs-farsi`** | **0** | **14** | 0 | 9 | **Batch 8 member. Nine `$name` triggers in the always-loaded body and not one `/name`.** A Claude Code agent reading this skill is told to invoke skills by a syntax Claude Code does not accept. |
| **`vector-rust-observability-pipelines`** | **0** | **4** | 0 | 3 | **Batch 8 member.** Same defect, smaller. |
| **`alaa-signoz-clickhouse-docs`** | **0** | **3** | 0 | 1 | **Batch 8 member.** Same defect. |
| `alaa-codex-runtime-ops` | **0** | 2 | 0 | 1 | Codex-only. |
| **`alaa-basic-memory-os`** | **0** | **0** | 0 | 0 | **Batch 8 member. Zero triggers of either syntax anywhere in the skill.** It routes to nothing and names no companion at any call site. This is the strongest boundary finding in the survey. |

**Four of the five Batch 8 members fail the trigger-syntax check, all in the same direction
(Codex-only or none).** The batch's cluster — observability, documentation, knowledge — appears to
have been authored in a Codex-first session.

### 4.2 Severe asymmetries worth naming

Not zero-in-one-direction, but far enough from parity to matter:

| Skill | cc | cx | Ratio |
| --- | ---: | ---: | --- |
| `alaa-services-contract` | 23 | 124 | 1 : 5.4 — a doctrine owner, Codex-leaning |
| `alaa-security-review` | 25 | **2** | 12.5 : 1 — a doctrine owner, Claude-leaning |
| `alaa-system-design` | 52 | 34 | 1.5 : 1 |
| `alaa-php-clean-code` | 122 | 94 | 1.3 : 1 |
| `alaa-postman-collections` | 3 | 3 | balanced but **very sparse for a 14-reference skill** — Batch 8 member |
| `alaa-bash-shell` | 1 | 1 | balanced and near-zero |

### 4.3 Fleet totals

Measured directly rather than summed from the table: **2934 `/name` occurrences and 2788 `$name`
occurrences** across the 67 skills' Markdown (single `python3` pass, same regexes). Near parity at
the fleet level — 1.05 : 1 — so the failures in §4.1 are all local, not a fleet-wide drift.

Corroborating totals from the same pass: **29** skills carry `references/00-topic-map.md`; **43**
skills ship at least one executable check; **24** ship none.

---

## 5. `agents/openai.yaml` coverage and validity

Command: `python3` with `yaml.safe_load` over `$R/*/agents/openai.yaml`, asserting
`interface.short_description` length in [25, 64], `'$' + skill_name` present in
`interface.default_prompt`, and an `interface:` mapping present.

A regex-based first pass gave wrong answers for two files and is recorded here because
**the repository's own validator uses that regex** — see §5.3.

| Quantity | Value |
| --- | ---: |
| Skills | 67 |
| `agents/openai.yaml` present | 65 |
| Missing | **2** |
| Fully valid (all four checks) | **50** |
| Failing at least one check | 15 |

### 5.1 Missing the file entirely

- `alaa-cc-orchestrator`
- `alaa-go-chi-development`

### 5.2 Present and failing, with the actual value and its length

| Skill | `short_description` length | Actual value | Other failures |
| --- | ---: | --- | --- |
| `alaa-keyset-pagination` | **159** | `Keyset pagination design: unique ordering, matching index, signed context-bound cursor, nullable and mutable columns, backward traversal, limits, errors, tests` | — |
| `alaa-system-design` | **142** | `Pre-implementation design method: boundaries, contracts, data ownership, dependency classification, compared candidates, one reviewable record` | — |
| `alaa-algorithms-data-structures` | **141** | `Complexity budgets, bounds on N, structure choice from the access pattern, the N+1 family, memory, tuning points, and when none of it applies` | — |
| `alaa-testing-strategy` | **120** | `Test design doctrine: what makes a test a test, layers, doubles, six proof levels, flake, coverage obligations, evidence` | — |
| `alaa-octane-performance` | **113** | `Octane worker-state safety, cross-request leak prevention, worker lifecycle, and hot-path performance for Laravel` | — |
| `alaa-reliability-sla` | **112** | `Reliability doctrine: deadlines, retries, breakers, bulkheads, shedding, degradation, idempotency, error budgets` | — |
| `alaa-haproxy-lua` | **97** | `Lua inside HAProxy: execution model, failure visibility, testing, patterns, performance, security` | — |
| `alaa-security-review` | **95** | `Security review gate: trust boundaries, authz, tenant isolation, injection, SSRF, files, crypto` | — |
| `clickhouse-performance-schema-ops` | **84** | `ClickHouse table design, ingest shape, query tuning, and read-lane failure behaviour` | — |
| `alaa-laravel-job-rabbitmq` | **82** | `Laravel jobs on RabbitMQ: worker modes, ack/nack, delivery limits, failure classes` | — |
| `alaa-cicd-laravel-postgres` | **68** | `Release gates for Laravel on Postgres: what gates, at what threshold` | 4 over |
| `alaa-codex-orchestrator` | **68** | `Production multi-agent coding with verification and specialist gates` | 4 over |
| `alaa-mongodb-patterns` | **67** | `MongoDB document shape, indexes, TTL, writes, and failure behaviour` | 3 over |
| `alaa-golang-fiber` | **66** | `Build, debug, or migrate a Fiber v3 Go service on the Ala platform` | 2 over |
| **`alaa-basic-memory-os`** | **absent** | — the file uses an entirely different schema: `version: 1` / `name:` / `description:` with **no `interface:` block, no `short_description`, no `default_prompt`** | all three. **Batch 8 member.** |

Ten of the fifteen are **more than 30 characters over** the limit — they are one-line summaries
written to a different budget, not near-misses. Four (`alaa-cicd-laravel-postgres`,
`alaa-codex-orchestrator`, `alaa-mongodb-patterns`, `alaa-golang-fiber`) are within 4 characters and
are trivially fixable.

### 5.3 A validator false-positive class, found by comparing the two methods

`skills/scripts/validate_sohrab_skill_pack.py:196-197` extracts the two fields with
`re.search(r'short_description:\s*"([^"]+)"', raw_yaml)` — **it requires double quotes.** Two skills
write valid YAML with unquoted scalars, and the validator reports four errors against them that are
not real:

| Skill | Actual `short_description` | Real length | Validator says |
| --- | --- | ---: | --- |
| `alaa-signoz-clickhouse-docs` | `SigNoz docs routing and ClickHouse SQL` | **38 — valid** | "short_description must be 25-64 chars" **and** "default_prompt must mention $alaa-signoz-clickhouse-docs" (the prompt does mention it, at line 4 of the file) |
| `alaa-observability-soc` | `Signal requirement levels, budgets, alerting, SOC evidence` | **58 — valid** | same two false errors |

`alaa-quasar-app-vite-v3` writes its `interface:` as a **single-line flow mapping**
(`interface: {display_name: "…",short_description: "…",…}`). The validator's regex happens to match
it; a line-oriented regex would not. The file is valid — `short_description` is
`Version-aware Quasar workflows and local API lookup`, 51 characters.

**Fix for Phase 2: replace the two regexes in `validate_sohrab_skill_pack.py` with `yaml.safe_load`,
falling back to exit 2 if PyYAML is unavailable.** That removes 4 of the 51 reported errors and one
of them belongs to a Batch 8 member.

---

## 6. The repository's own validator, run

Location: `$S/scripts/validate_sohrab_skill_pack.py` (9383 bytes). It takes **no arguments** — it
ignores `argv` entirely and always walks `Path(__file__).resolve().parents[1] / "skills" / "sohrab"`.
It ran directly against the live device tree; no staging or per-skill fallback was needed.

```
cd $S && python3 scripts/validate_sohrab_skill_pack.py
exit=1
```

| Quantity | Value | Command |
| --- | ---: | --- |
| Errors | **51** | `awk '/^Errors:/{m=1;next}/^Warnings:/{m=2;next} m==1&&/^- /{e++} m==2&&/^- /{w++} END{print e,w}'` |
| Warnings | **26** | same |
| Errors + warnings | **77** | same |
| Exit code | 1 | `echo $?` |

**Correction to the carry-over.** `UPGRADE-CARRYOVER.md` records "77 repo-wide errors after Batch 7".
The true split is **51 errors and 26 warnings**, totalling 77. The carry-over conflated the two
sections of the validator's output. Of the 51 errors, **4 are false positives** (§5.3), so the real
error count is **47**.

### 6.1 The full error list — 51 lines, verbatim

```
- alaa-algorithms-data-structures: missing a 'When not to use' or 'Do not use' section
- alaa-algorithms-data-structures: short_description must be 25-64 chars
- alaa-bash-shell: missing a 'When not to use' or 'Do not use' section
- alaa-basic-memory-os: short_description must be 25-64 chars
- alaa-basic-memory-os: default_prompt must mention $alaa-basic-memory-os
- alaa-cc-orchestrator: missing a 'When not to use' or 'Do not use' section
- alaa-cc-orchestrator: missing agents/openai.yaml
- alaa-cicd-laravel-postgres: missing a 'When not to use' or 'Do not use' section
- alaa-cicd-laravel-postgres: short_description must be 25-64 chars
- alaa-codex-orchestrator: missing a 'When not to use' or 'Do not use' section
- alaa-codex-orchestrator: short_description must be 25-64 chars
- alaa-codex-runtime-ops: missing a 'When not to use' or 'Do not use' section
- alaa-crockford-base32-codecs: missing a 'When not to use' or 'Do not use' section
- alaa-go-chi-development: missing a 'When not to use' or 'Do not use' section
- alaa-go-chi-development: missing agents/openai.yaml
- alaa-golang: missing a 'When not to use' or 'Do not use' section
- alaa-golang: referenced path does not exist -> references/05-phase-and-source-truth.md
- alaa-golang-clean-code-principles: referenced path does not exist -> references/10-
- alaa-golang-fiber: missing a 'When not to use' or 'Do not use' section
- alaa-golang-fiber: short_description must be 25-64 chars
- alaa-haproxy-lua: missing a 'When not to use' or 'Do not use' section
- alaa-haproxy-lua: short_description must be 25-64 chars
- alaa-keyset-pagination: missing a 'When not to use' or 'Do not use' section
- alaa-keyset-pagination: short_description must be 25-64 chars
- alaa-laravel-architecture: missing a 'When not to use' or 'Do not use' section
- alaa-laravel-job-rabbitmq: missing a 'When not to use' or 'Do not use' section
- alaa-laravel-job-rabbitmq: short_description must be 25-64 chars
- alaa-laravel-public-api-contract-pack: missing a 'When not to use' or 'Do not use' section
- alaa-laravel-upgrade-all-packages: missing a 'When not to use' or 'Do not use' section
- alaa-low-noise: missing a 'When not to use' or 'Do not use' section
- alaa-mongodb-patterns: referenced path does not exist -> references/24-metric-registry.md
- alaa-mongodb-patterns: short_description must be 25-64 chars
- alaa-observability-soc: missing a 'When not to use' or 'Do not use' section
- alaa-observability-soc: short_description must be 25-64 chars          <-- FALSE (§5.3)
- alaa-observability-soc: default_prompt must mention $alaa-observability-soc   <-- FALSE (§5.3)
- alaa-octane-performance: missing a 'When not to use' or 'Do not use' section
- alaa-octane-performance: short_description must be 25-64 chars
- alaa-php-clean-code: missing a 'When not to use' or 'Do not use' section
- alaa-reliability-sla: missing a 'When not to use' or 'Do not use' section
- alaa-reliability-sla: short_description must be 25-64 chars
- alaa-security-review: missing a 'When not to use' or 'Do not use' section
- alaa-security-review: short_description must be 25-64 chars
- alaa-signoz-clickhouse-docs: short_description must be 25-64 chars     <-- FALSE (§5.3)
- alaa-signoz-clickhouse-docs: default_prompt must mention $alaa-signoz-clickhouse-docs  <-- FALSE (§5.3)
- alaa-system-design: missing a 'When not to use' or 'Do not use' section
- alaa-system-design: short_description must be 25-64 chars
- alaa-testing-strategy: missing a 'When not to use' or 'Do not use' section
- alaa-testing-strategy: short_description must be 25-64 chars
- clickhouse-performance-schema-ops: missing a 'When not to use' or 'Do not use' section
- clickhouse-performance-schema-ops: short_description must be 25-64 chars
- service-runtime-kit-governance: missing a 'When not to use' or 'Do not use' section
```

Breakdown by rule:

| Rule | Errors | False | Real |
| --- | ---: | ---: | ---: |
| missing a 'When not to use' / 'Do not use' heading | 27 | 0 | 27 |
| `short_description` not 25–64 chars | 17 | 2 | 15 |
| `default_prompt` missing `$name` | 3 | 2 | 1 |
| missing `agents/openai.yaml` | 2 | 0 | 2 |
| referenced path does not exist | 2 | 0 | 2 |
| **Total** | **51** | **4** | **47** |

The two path errors are genuine and are the only cross-reference defects this validator can see,
because `local_reference_paths` is called from `main()` on only two inputs
(`validate_sohrab_skill_pack.py:190` for the body and `:213` for the topic map): it inspects
**`SKILL.md` and `references/00-topic-map.md` and nothing else** — never the other 738 Markdown files
in the fleet (805 total minus 67 `SKILL.md`). That is the gap the §1.11 checker fills, and it is why
the validator sees 2 path errors where the full census sees 2252 `references/` citations.

- `alaa-golang: references/05-phase-and-source-truth.md` — the file exists at exactly one place in
  the fleet, `$R/alaa-go-chi-development/references/05-phase-and-source-truth.md`
  (`ls $R/*/references/05-phase-and-source-truth.md`). `alaa-golang/SKILL.md` cites it **twice**:
  at `:29` it names the owner — `` `alaa-go-chi-development` `references/05-phase-and-source-truth.md` ``
  — and at `:59` it cites the same file bare. The validator sees only the second. This is the
  §1.8 CONTEXTUAL class caught in the act, and it proves the class is a real defect and not a
  stylistic quibble: the same document is right on one line and wrong forty lines later.
- `alaa-golang-clean-code-principles: references/10-` — a **truncated path** in the source, not a
  missing file.
- `alaa-mongodb-patterns: references/24-metric-registry.md` — belongs to `alaa-services-contract`.
  Missing owner prefix.

### 6.2 Body-line warnings above 120 — 22 skills, each with its N

The carry-over records "22 skills over the body-line warning". **Confirmed: 22.**

| Skill | Body lines | Over by |
| --- | ---: | ---: |
| `vector-rust-observability-pipelines` | **227** | +107 |
| `alaa-project-constitution` | 207 | +87 |
| `alaa-laravel-job-rabbitmq` | 204 | +84 |
| `alaa-php-clean-code` | 198 | +78 |
| `alaa-permission-generator` | 171 | +51 |
| `alaa-laravel-public-api-contract-pack` | 170 | +50 |
| `alaa-gitlab-ci-cd` | 167 | +47 |
| `alaa-cc-orchestrator` | 159 | +39 |
| `alaa-codex-orchestrator` | 159 | +39 |
| `alaa-system-design` | 157 | +37 |
| `alaa-services-contract` | 156 | +36 |
| `alaa-postman-collections` | **154** | +34 |
| `alaa-golang-clean-code-principles` | 147 | +27 |
| `alaa-algorithms-data-structures` | 144 | +24 |
| `alaa-octane-performance` | 142 | +22 |
| `alaa-basic-memory-os` | **140** | +20 |
| `alaa-security-review` | 136 | +16 |
| `alaa-testing-strategy` | 136 | +16 |
| `alaa-bale-provider` | 135 | +15 |
| `alaa-minio-object-storage` | 135 | +15 |
| `alaa-reliability-sla` | 131 | +11 |
| `alaa-docs-farsi` | **127** | +7 |

**Four of Batch 8's five members are in this table**, and one of them holds the fleet record. Only
`alaa-signoz-clickhouse-docs` is under 120.

### 6.3 The four description-length warnings

| Skill | Description chars | Headroom to 1024 |
| --- | ---: | ---: |
| `alaa-laravel-architecture` | 1001 | 23 |
| `alaa-laravel-public-api-contract-pack` | 994 | 30 |
| `alaa-php-clean-code` | 984 | 40 |
| `clickhouse-performance-schema-ops` | 956 | 68 |

The lane brief's advice to keep every description **at or below 900 characters** is stricter than
the validator's own 950 target (`validate_sohrab_skill_pack.py:66` `DESCRIPTION_TARGET_MAX = 950`).
No Batch 8 member appears here.

### 6.4 Two defects in the validator itself

1. **No exit code 2.** `validate_sohrab_skill_pack.py:221` — `return 1 if errors else 0`. If
   `PACK_DIR` does not exist, `iterdir()` raises and the process dies with a traceback and exit 1 —
   indistinguishable from "found errors", and a CI gate cannot tell "the tree moved" from "the tree
   is broken". The programme's own defining deliverable is violated by its own flagship tool.
2. **Fragile root resolution.** `:7` — `ROOT = Path(__file__).resolve().parents[1]`. It is defect
   class 7 from the lane brief, in the file that enforces the other classes.

---

## 7. Residual hygiene

### 7.1 Shipped `__pycache__` — 7 directories, 9 `.pyc` files

Command: `find $R $S/scripts -name __pycache__ -type d`

```
$R/alaa-bale-provider/scripts/__pycache__
$R/alaa-gitlab-ci-cd/scripts/__pycache__
$R/alaa-k8s-helm/scripts/__pycache__
$R/alaa-sms-provider-mediana/scripts/__pycache__
$R/ansible-validator/scripts/__pycache__
$R/ansible-validator/scripts/lib/__pycache__
$S/scripts/__pycache__                        <-- the repository's own scripts directory
```

The 9 `.pyc` files (`find $R -name '*.pyc' | wc -l` → 9):

```
alaa-bale-provider/scripts/__pycache__/validate_bale_payload.cpython-310.pyc
alaa-gitlab-ci-cd/scripts/__pycache__/validate_gitlab_ci.cpython-314.pyc
alaa-gitlab-ci-cd/scripts/__pycache__/validate_runner_config.cpython-314.pyc
alaa-k8s-helm/scripts/__pycache__/detect_crd.cpython-314.pyc
alaa-k8s-helm/scripts/__pycache__/pod_diagnostics.cpython-314.pyc
alaa-sms-provider-mediana/scripts/__pycache__/validate_mediana_payload.cpython-310.pyc
ansible-validator/scripts/lib/__pycache__/ansible_walk.cpython-310.pyc
ansible-validator/scripts/lib/__pycache__/ansible_walk.cpython-314.pyc
ansible-validator/scripts/__pycache__/extract_ansible_info.cpython-314.pyc
```

**None is tracked by git** — `git ls-files | grep __pycache__` returns nothing against a 4328-file
index. They are local build residue from prior batches running the checkers, not shipped artifacts.
The right fix is a repository `.gitignore` entry plus `PYTHONDONTWRITEBYTECODE=1` in whatever
harness runs them, not a retirement move.

### 7.2 `.fuse_hidden*` — zero, in both the worktree and the index

| Check | Command | Result |
| --- | --- | --- |
| Worktree | `find $R -name '.fuse_hidden*' \| wc -l` | **0** |
| Git index | `git ls-files -z \| tr '\0' '\n' \| grep -i fuse_hidden` | **no matches** (index has 4328 files) |

**The carry-over item is resolved.** Batch 7 recorded twenty `.fuse_hidden*` files staged as added
but absent from the worktree, showing as `AD` and needing `git rm --cached`. Neither the files nor
the index entries exist today. No `git rm --cached` is needed.

### 7.3 `git status --porcelain` — UNMEASURED

```
cd $S && timeout 42 git status --porcelain
exit=124   (timeout)
```

Exactly the failure the carry-over warns about. **Not retried.** The working-tree status of this
repository is unmeasured in this survey.

`ls -la .git/index.lock` → `No such file or directory`. **No stale lock was left behind.**

Two cheaper index-only reads did complete and are reported instead:

| Command | Result |
| --- | --- |
| `git ls-files \| wc -l` | 4328 tracked files |
| `git ls-files 'skills/sohrab/alaa-quasar-app-vite-v3/*' \| wc -l` | 36 |

### 7.4 `Path(__file__).parents[N]` — 8 sites in 5 skill scripts, 3 more in repo scripts

```
$R/alaa-indexeddb-browser-storage/scripts/capability_contract_conformance.py:281
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
$R/alaa-indexeddb-browser-storage/scripts/check_references.py:11    (docstring, explains the choice)
$R/alaa-indexeddb-browser-storage/scripts/check_references.py:149
$R/alaa-indexeddb-browser-storage/scripts/validate_skill_pack.py:251
$R/alaa-workflow/scripts/init_workflow_files.py:14      ROOT = Path(__file__).resolve().parents[1]
$R/alaa-workflow/tests/test_workflow_files.py:13        SKILL_DIR = Path(__file__).resolve().parents[1]
$R/tusd-upload-platform/scripts/validate_pack.py:616
$R/tusd-upload-platform/scripts/validate_pack.py:692

$S/scripts/validate_sohrab_skill_pack.py:7
$S/scripts/vendor_skill_links.py:11
$S/scripts/vendor_subtrees.py:12
```

Severity differs by site. The three `alaa-indexeddb-browser-storage` sites and
`tusd-upload-platform:692` use it only as an **argparse default** with `--root` available to
override; that is the mitigated form. `alaa-workflow/scripts/init_workflow_files.py:14` and the
three repository scripts bind it at module scope with no override, which is the unmitigated form.
`UPGRADE-BATCH-6-ANALYSIS.md:203` records a prior lane judging the indexeddb pattern "acceptable *as
invoked*"; that judgement holds for the argparse-default form and does not extend to the four
module-scope bindings.

### 7.5 `new URL(import.meta.url).pathname` — zero live occurrences

Command: `grep -rn 'import\.meta\.url' $R --include=*.mjs --include=*.js`

Nine matches, and **every one is either the correct `fileURLToPath(import.meta.url)` or a comment
warning against the broken form**:

```
$R/alaa-frontend-devops/scripts/verify-artifact-contract.mjs:13-15
  // On Windows, new URL(import.meta.url).pathname is "/D:/...", which Node cannot
  const SELF_PATH = fileURLToPath(import.meta.url);
$R/alaa-mono-package/scripts/verify-package-entrypoints.mjs:15-17     (identical pattern)
$R/alaa-docker-production/scripts/lib/common.mjs:9-10
  //   4. It runs on Windows. It resolves its own directory with `fileURLToPath(import.meta.url)`
  //      and never `new URL(import.meta.url).pathname`, which yields `/D:/...` on Windows.
```

**Clean.** The Windows defect class the lane brief names is eradicated from live code and documented
in three places.

### 7.6 `_to_delete/` — 32 files at the repository level, **0 in the skill-pack level**

`$S/_to_delete/` — 7 dated directories, 32 files total
(`find $S/_to_delete -type f | wc -l` → 32):

```
20260725-batch1/        (23 files: retired reference bodies, .pyc residue, batch1-pending.tar.gz,
                         .writetest, _linktest_target)
2026-07-26-batch2/      (1 file: contract_pack_audit.cpython-310.pyc)
2026-07-26-batch3/      (0 files)
2026-07-26-batch4/      (0 files)
20260727-batch5/        (5 files, all .pyc)
20260727-stale-git-lock/(0 files)
20260728-batch6/        (0 files)
```

`$R/_to_delete/` — 4 dated directories, **0 files**
(`du -sb` → 0; `find … -type f | wc -l` → 0):

```
2026-07-26-batch4/alaa-data-layer/     empty
20260728-batch6/alaa-shaka-player/     empty
20260729-batch7/                       empty
20260729-fuse-artifacts/               empty
```

**Finding.** The convention is "retired files move to `_to_delete/<date>-<batch>/`; nothing is ever
deleted". The skill-pack-level retirement directories for batches 4, 6 and 7, and the
fuse-artifacts directory, are **all empty**. Either the moves did not land, or the content was
removed afterwards. Whichever it was, the retirement audit trail for three batches does not exist.
The repository-level `_to_delete/` holds only 32 files, 29 of which are `.pyc` residue — the actual
retired Markdown bodies (5 files) are all from batch 1.

### 7.7 An empty directory left by a landed retirement

`$R/alaa-frontend-developer/scripts/` exists and contains nothing
(`for d in $R/*/scripts; do [ "$(ls -A $d | wc -l)" = 0 ] && echo $d; done` → exactly one hit).
It is the only empty `scripts/` directory in the fleet. Git does not track empty directories, so it
is cosmetic, but a `scripts/` directory with no scripts invites a future agent to put one there.

---

## 8. The duplicate-script retirement — **it landed**

`UPGRADE-CARRYOVER.md:210` records that `alaa-frontend-developer/scripts/check-upstream-versions.mjs`
was to be retired in favour of the `alaa-quasar-app-vite-v3` copy, and that as of 2026-07-28 the
duplicate was still present with both call sites still invoking it locally.

**Verified on disk today, 2026-07-29: the retirement is complete. No diff is possible because the
duplicate no longer exists.**

| Claim in the carry-over | State today | Evidence |
| --- | --- | --- |
| `alaa-frontend-developer/scripts/check-upstream-versions.mjs` still present | **Gone.** `alaa-frontend-developer/scripts/` is an empty directory. | `ls -la $R/alaa-frontend-developer/scripts` → `total 0` |
| `alaa-frontend-developer/SKILL.md` still invokes it locally | **No.** The only `scripts/` citation in that `SKILL.md` is line 42, routing to `alaa-crockford-base32-codecs`. | `grep -n 'scripts/' $R/alaa-frontend-developer/SKILL.md` → one line, `:42` |
| `references/90-upstream-deltas-and-maintenance.md` still invokes it locally | **File no longer exists.** Its successor `references/95-sources-and-maintenance.md:5-12` now routes to the owner. | `grep -rn 'check-upstream-versions' $R --include=*.md` |
| `alaa-quasar-app-vite-v3/references/91-agent-authoring-and-dual-runtime.md` asserts its copy is the fleet's only one | **Still asserts it, and the assertion is now true.** | `:25` |

The current routing text, `$R/alaa-frontend-developer/references/95-sources-and-maintenance.md:5-12`:

```
This skill states no package versions. A version written into prose is stale the week after it is
written, and this skill previously carried five copies of one snapshot. The source of truth is the live
check, which belongs to `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`)
`scripts/check-upstream-versions.mjs` — the fleet's only copy. Run it from that skill's root before any
version-sensitive change; it takes `--help` and `--self-test`, honours `HTTPS_PROXY`, applies a request
timeout, and isolates a failing package so one unreachable registry entry does not lose the rest.
```

The counterpart assertion, `$R/alaa-quasar-app-vite-v3/references/91-agent-authoring-and-dual-runtime.md:25`:

```
- `scripts/check-upstream-versions.mjs` exists because every version number in this pack expires, and a
  live registry read is deterministic while model memory is not. It is the fleet's only copy;
  `/alaa-frontend-developer` (`$alaa-frontend-developer`) routes here rather than keeping a duplicate.
```

Both sides now name each other, both use the dual-runtime trigger form, and the surviving copy has
the `--help`, `--self-test`, per-request timeout and `HTTPS_PROXY` handling the carry-over required.
The surviving script's own header states its exit-code discipline: *"exit codes are meaningful and
'could not run' is never reported as 'clean'."*

**What would still have to change — the only residue:**

1. `$R/alaa-frontend-developer/scripts/` is an empty directory (§7.7). Removing it is optional and
   cosmetic; the device mount forbids `unlink`, so it would go to `_to_delete/` if removed at all.
2. `UPGRADE-CARRYOVER.md:210` is now stale and should be marked done.
3. The surviving script does **not** carry a `--self-test` code path that exercises the exit-2
   branch under a simulated network failure; §2.1 detected 0/1 literals and the header's own claim of
   a meaningful exit 2. Worth a read by whoever owns that skill.

**This is a report, not a fix.** Both files are outside Batch 8's membership. The retirement appears
already done by a prior batch or lane, so **the owner's decision required here is only whether to
close the carry-over item** — no code change is proposed.

---

## 9. Summary of every correction this survey makes to the carry-over

| Carry-over claim | Measured today | Delta |
| --- | --- | --- |
| ~68 skill directories | 67 with a `SKILL.md` | −1 |
| 582 unresolved bare cross-skill paths across 223 files | 4 AMBIGUOUS-BARE + 5 AMBIGUOUS-MULTI + 1 real DANGLING-NAMED; 154 owner-named-nearby | the 582 was a resolver artifact |
| 28 of 68 carry `references/00-topic-map.md` | 29 of 67 | +1 |
| 77 repo-wide validator errors | 51 errors + 26 warnings = 77; 4 errors false → **47 real errors** | conflation corrected |
| 22 skills over the body-line warning | **22 — confirmed**, N values in §6.2 | confirmed |
| Twenty `.fuse_hidden*` staged `AD`, need `git rm --cached` | 0 in worktree, 0 in index | resolved |
| `alaa-frontend-developer/scripts/check-upstream-versions.mjs` still present | gone; both sides now route correctly | resolved |

## 10. Open questions for the owner

1. **Does the topic map count toward its own ≤8/≥9 threshold?** Recommendation: no. Reason: the
   threshold measures how many destinations a router must offer, and a router is not a destination.
   Trade-off: saying "no" makes `alaa-bash-shell` and `alaa-reliability-sla` violations requiring a
   real restructure; saying "yes" leaves them alone but makes the rule read oddly (a skill with 8
   bodies plus a map "has 9 references").
2. **Should `--strict-owner` be the default for the new link checker?** Recommendation: no, not on
   day one. Reason: it converts 154 passing citations into findings, 58 of them in one skill.
   Trade-off: leaving it off tolerates a citation form that a future automated consumer of these
   files cannot resolve; turning it on stalls adoption behind an `alaa-frontend-developer` rewrite.
3. **Do the 88 non-`references/` citations that name target-repository paths need a distinct
   notation?** Recommendation: yes — a `repo:` prefix or a fenced-block convention. Reason: today no
   tool can distinguish "run the checker I ship" from "edit the file in your repository", and that
   ambiguity is the sole reason the fleet link checker needs an 88-item exclusion list — 520 items,
   422 of them `docs/…`, if `docs/` is included in the scan (§1.9).
   Trade-off: a notation change touches ~66 distinct paths across 20 skills.
4. **Should the three empty `_to_delete/` batch directories be investigated?** The retirement audit
   trail for batches 4, 6 and 7 is empty (§7.6). Recommendation: confirm whether files were moved and
   later removed, or never moved. Reason: the "nothing is ever deleted" convention currently has no
   evidence behind it for three of seven batches.
5. **Close `UPGRADE-CARRYOVER.md:210`?** Recommendation: yes (§8). The work is done.


---

# Appendix G — Repository index and inventory audit

# L7 — Repository index and inventory audit

**Lane:** Batch 8, repository-level cleanup (carry-over section 6).
**Date of every observation below:** 2026-07-29.
**Access mode:** read-only. Every device command was issued through
`mcp__remote-devices__device_bash`; nothing was written to `D:\`. Scratch work is in `/tmp/w` in the
analysis container. Files were staged read-only into `/mnt/user-data/uploads/` for close reading.

Throughout, `$R` = `/sessions/rcw-01nfpk8ndxrrswndyp6txjwc/mnt/skills`, which is the device mount of
`D:\Sohrab\Project\skills`. `$S` = `$R/skills/sohrab` = `D:\Sohrab\Project\skills\skills\sohrab`.

**Headline: the carry-over's section 6 is materially out of date.** The single largest defect it
records — a `README.md` skill map listing ~20 phantom skills and omitting 13 real ones — was fixed on
2026-07-28, one day before this lane ran. The real remaining index defects are smaller, but there are
more of them, and two are new. Every claim below carries the command that produced it.

---

## 0. Summary of verdicts

| Claim under audit | Carry-over says | Disk says today | Verdict |
|---|---|---|---|
| `README.md` lists ~20 skills not on disk | true | **0 phantom entries** | **STALE — already fixed** |
| `README.md` omits ≥13 real skills | true | **omits exactly 2** | **STALE — partially fixed** |
| `alaa-input-normalization` in neither README | true (2026-07-28) | **still true** | **CONFIRMED** |
| `README.fa.md` and `README.md` describe different fleets | not recorded | **identical 65-name sets** | **NOT A DEFECT today** |
| Root `AGENTS.md` / `CLAUDE.md` byte-identical | true | **identical in git, drifted in the working tree** | **CONFIRMED with a twist** |
| `skills/sohrab/CLAUDE.md` is a symlink | (not recorded) | **yes, mode `120000` in git** | **CONFIRMED — Windows hazard** |
| `install-skills.md` authoritative for install paths | true | **true, but incomplete and one src root is wrong** | **PARTIALLY CONFIRMED** |
| 63 skill directories | 63 | **67** | **WRONG (as is 68 and 69)** |
| 51 assigned to eight batches | 51 | **51** | **CONFIRMED** |
| 7 rebuilt pre-programme | 7 | **7** | **CONFIRMED** |
| 5 created by the programme | 5 | **8** (3 more since) | **STALE** |
| `cc-skills-golang` 46 skills | 46 | **46** | **CONFIRMED** |
| `basic-memory` 19 skills | 19 | **19 `SKILL.md` files, 14 unique skills** | **MISLEADING** |
| `openfga-agent-skills` 1, `skill-temporal-developer` 1 | 1 / 1 | **1 / 1** | **CONFIRMED** |
| Repository validator passes | required by DoD | **exits 1 with 51 errors across 30 skills** | **FAILS TODAY** |

---

## 1. `README.md` versus the actual directory

### 1.1 The two-way diff — English README

Command that produced the README side:

```bash
awk '/^## Current skill map/{f=1} /^## Consolidated or removed/{f=0} f' \
  skills/sohrab/README.md | grep -oP '^- `\K[a-z0-9-]+' | sort -u
```
→ **65 unique names, 65 raw `- \`` bullets** (no duplicates; `uniq -d` returned nothing). This
satisfies `README.md:93`'s own "appears exactly once" clause in the *no-duplicate* direction.

Command that produced the disk side:

```bash
find $S -maxdepth 1 -mindepth 1 -type d | wc -l          # 70
find $S -maxdepth 2 -mindepth 2 -name SKILL.md | wc -l   # 67
for d in $S/*/; do [ -f "$d/SKILL.md" ] || echo "NO_SKILL_MD: $d"; done
#   → _to_delete/ only; plus hidden .claude/ and .obsidian/
```
→ **67 skill directories** (70 minus `_to_delete/`, `.claude/`, `.obsidian/`).

`comm -23 readme_map.txt disk.txt` → **empty**.
`comm -13 readme_map.txt disk.txt` →

```
alaa-haproxy-lua
alaa-input-normalization
```

**Finding R1 (CONFIRMED, current).** `skills/sohrab/README.md` lists **zero** skills that do not
exist on disk. Every one of the names the carry-over listed as phantom — `azure-pipelines-*`,
`fluentbit-*`, `github-actions-*`, `jenkinsfile-*`, `terraform-*`, `terragrunt-*`, `promql-*`,
`logql-generator`, `loki-config-generator` — is now in the **"Consolidated or removed from this
pack"** section at `README.md:189–196`, correctly marked as having no folder, "checked 2026-07-25".
I re-verified all thirteen of those names plus `dockerfile-*`/`makefile-*` against disk with a
`[ -d ]` loop: **every one is absent**, so that section is accurate. The carry-over section 6 first
paragraph is stale and Phase 2 must not act on it as written.

**Finding R2 (CONFIRMED, current, and it is the real defect).** `README.md:93` asserts:

> "Every folder in this directory appears exactly once below."

That sentence is **false**. Two directories are missing from the map:

| Missing from `README.md` | On disk since | `SKILL.md` bytes | Evidence |
|---|---|---|---|
| `alaa-haproxy-lua` | commit `b920bfdb` "upgrade batch 4", 2026-07-27 | 6775 | `git log --diff-filter=A -- skills/sohrab/alaa-haproxy-lua/SKILL.md` |
| `alaa-input-normalization` | 2026-07-28 21:10 | 5810 | `ls -la $S/alaa-input-normalization` |

`alaa-input-normalization` was already flagged by the carry-over (`UPGRADE-CARRYOVER.md:206`).
**`alaa-haproxy-lua` was not, and this is a new finding for the index lane** — it is absent from
`UPGRADE-CARRYOVER.md` entirely (`grep -c "haproxy-lua" UPGRADE-CARRYOVER.md` → `0`).

### 1.2 The two-way diff — Persian README

```bash
grep -oP '`\K[a-z0-9][a-z0-9-]*(?=`)' skills/sohrab/README.fa.md \
  | grep -E '^(alaa|ansible|caas|clickhouse|jitsi|service|tusd|vector)' | sort -u
```
→ **65 names.**

- `comm -23 fa_map disk` → **empty** (no phantoms).
- `comm -13 fa_map disk` → `alaa-haproxy-lua`, `alaa-input-normalization` — **exactly the same two**.

### 1.3 English versus Persian

- `comm -23 readme_map fa_map` → **empty**
- `comm -13 readme_map fa_map` → **empty**

**Finding R3 (NOT A DEFECT).** The two indexes describe **the same 65-skill fleet**. The lane
hypothesis — "a Persian index and an English index that describe different fleets are two lies rather
than one" — does not hold today. They are the *same* lie, told twice: both omit the same two
directories. That is materially cheaper to fix and should be recorded as such.

Structural note: the two files are **not** parallel documents. `README.md` is a routing/policy
document whose map is bare names in eight groups (`README.md:95–187`); `README.fa.md` is a table
with a one-line purpose per skill in nine groups (`README.fa.md:13–120`). `README.md:93` says
"Groups match `README.fa.md`" — they do not exactly: English has 8 groups, Persian has 9, because
Persian splits "Core Ala architecture and policy" into §1 (doctrine) and §2 (multi-agent), which
English merges differently. `README.fa.md` groups `alaa-basic-memory-os` under §2 (multi-agent);
`README.md` also puts it under "Multi-agent orchestration and cross-session memory". Those agree.
The mismatch is only in group **count and boundaries**, not membership. Low severity; worth one
sentence of correction rather than a restructure.

### 1.4 Description drift — README one-liners versus frontmatter `description`

`README.md` carries a one-line description for exactly **one** skill (`alaa-keyset-pagination`,
`README.md:107`); the rest of its map is bare names. So the description audit is necessarily against
`README.fa.md`, which carries one for all 65. Frontmatter was extracted with:

```bash
awk 'BEGIN{p=0} /^description:/{p=1;print;next} p&&/^[a-zA-Z_-]+:/{exit} p{print}' "$d/SKILL.md"
```

Eighteen skills checked. **Nine are accurate, six are materially incomplete, three are wrong.**

| Skill | `README.fa.md` line and text (translated) | Frontmatter `description` says | Verdict |
|---|---|---|---|
| `alaa-async-messaging` | `:106` "async architecture on RabbitMQ: the fleet's only broker; prefetch, ack, confirm, outbox, DLQ and replay" | "RabbitMQ message-plane architecture… the seam between a database commit and a published message, the transactional outbox…, publisher confirms, the acknowledgement point, prefetch and consumer concurrency, dead-letter topology, and the DLQ replay procedure" | **ACCURATE** |
| `alaa-keyset-pagination` | `:28` "cursor pagination design: deterministic order with tie-breaker, matching index, cursor signature and validation, and the offset exception for admin tables" | "…deriving an ordering tuple whose final component is unique, building the index that serves it, and defining a signed cursor that carries its filter and sort context" | **ACCURATE** (and `README.md:107` matches too) |
| `alaa-minio-object-storage` | `:72` "object storage on MinIO and S3: bucket and object-key design, lifecycle, credentials and signed URLs" | adds "tenant scoping inside the key", "the incomplete-multipart abort rule", versioning, encryption, **replication**, bucket-policy shape, TLS and addressing style, "failure classes of an unreachable or half-written store" | **INCOMPLETE** — the fa line omits the failure-behaviour half, which is the part an SLA reader needs |
| `alaa-docs-farsi` | `:120` "writing Persian documentation" | "…repository documentation such as `README.md`, `docs/BIG_PICTURE.md`, `docs/api-summary.md`, storage or data-architecture docs, error or event or observability docs… **It produces rich, simple-English docs**…" | **WRONG.** The skill's own frontmatter says it produces **English** docs. The Persian index says it writes **Persian** documentation. These contradict. This is the single worst description mismatch in the tree and it sits on a Batch 8 skill. |
| `alaa-postman-collections` | `:119` "building and validating Postman collections and environments, and the doctrine of a multi-service aggregate collection" | adds "saved examples for its success case and **for every error it can actually return**", a post-response script capturing tokens/ids, "tests that would fail against a broken implementation", docs for a frontend developer **and a security te…** | **INCOMPLETE** — omits the error-example and failing-test obligations, which are the skill's actual quality claim |
| `alaa-signoz-clickhouse-docs` | `:117` "searching SigNoz docs and ClickHouse queries" | "…Query Builder v5 routing, search syntax, dashboard variables, field ambiguity, missing spans, trace-quality troubleshooting, and writing/repairing SigNoz ClickHouse SQL. **Pair with alaa-observability-soc**…" | **INCOMPLETE** — omits the pairing rule, which is the routing fact an index exists to convey |
| `alaa-basic-memory-os` | `:37` "cross-session memory on Basic Memory and Obsidian" | enumerates note classes (architecture, service-ownership, contract, operations, drift, lesson, work-pattern, project-index, project-state, handoff, research, inbox-capture), drift recording/resolution, publishing Prompt 1/2 self-improvement outputs, resuming work | **INCOMPLETE** — the fa line describes a storage location; the skill describes a governance contract |
| `vector-rust-observability-pipelines` | `:118` "Vector pipeline" | "Vector topology design, VRL transforms, sink tuning, buffering, acknowledgement strategy, or production troubleshooting" | **INCOMPLETE** but not misleading |
| `alaa-golang` | `:56` "Go entry point and routing to the 46 upstream `golang-*` skills" | "Front door and router… **Owns the HTTP framework decisio…**" plus "holds the Go rules no other skill owns" | **INCOMPLETE** — omits that it owns the framework decision, a routing-relevant fact |
| `alaa-frontend-developer` | `:79` "frontend entry point: SSR, PWA, performance and browser debugging" | adds "hydration determinism, cleanup safety, SSR auth and session posture", "the Lighthouse and Core Web Vitals playbook", "the client-side half of resilience, security, observability and input contracts" | **INCOMPLETE** — omits the security/observability half |
| `alaa-docker-production` | `:93` "production-ready Dockerfile and Compose" | "…**It owns how the image and runtime file are expressed and decides no gate.** Not for gate policy (alaa-frontend-devops)…" | **WRONG BY OMISSION** — decision D8's whole point ("decides no gate") is absent from the index, and that is precisely the boundary Batch 7 was told to publish |
| `alaa-haproxy` | `:96` "HAProxy configuration" | "…Do not use to decide caching policy, owned by /alaa-frontend-devops…; for HAProxy Lua, owned by **/alaa-haproxy-lua**…" | **WRONG BY OMISSION** — the skill routes to `alaa-haproxy-lua`, a skill the index does not list at all (see R2) |
| `alaa-crockford-base32-codecs` | `:70` "identifier encoding with Crockford Base32" | "…**four byte-identical implementations for PHP, JavaScript, bash, and HAProxy Lua, plus a harness proving they still agree**" | **INCOMPLETE** — the conformance harness is the skill's distinguishing capability |
| `alaa-partitioned-table-fk-audit` | `:69` "partitioned table and foreign-key review" | "**Ships a tested detector**… SQLSTATE 42830" | **INCOMPLETE** — an executable detector is not conveyed |
| `alaa-controlled-ops` | `:20` "ownership boundary between the `alaa/controlled-ops` package and the consuming service, and its publication on Satis" | matches, plus semver tagging, Composer-lock/Satis dist verification, dry-run canonical hashes | **ACCURATE** |
| `alaa-project-constitution` | `:15` "…**owner of the ten-point quality bar** and the archetype layer" | "…Matches the repository's project archetypes from ob…" | **ACCURATE** |
| `alaa-trust-gateway-auth` | `:107` "issuing and validating tokens and trusted headers at the gateway" | names the exact claims `pid, sub, prm, rol, loc` and headers `X-Project-Id, X-User-Id, X-Access, X-User-Roles, X-Location-*`, TOTP step-up headers | **ACCURATE** at index granularity |
| `alaa-reliability-sla` | `:17` "…**Alaa's numbers are in `alaa-services-contract`**" | "…Use when adding or reviewing an outbound call, a retry, a timeout, a po…" | **ACCURATE**, and it correctly carries the boundary |

**Finding R4 (CONFIRMED).** `README.fa.md:120` describes `alaa-docs-farsi` as producing Persian
documentation while `alaa-docs-farsi/SKILL.md:3` states it "produces rich, **simple-English** docs".
A reader routing from the index will pick this skill expecting Persian output. This is an
index-versus-owner contradiction of the kind the programme exists to eliminate, and it lands on a
Batch 8 skill, so lane L3 should be told.

**Finding R5 (CONFIRMED).** The `README.fa.md` one-liners systematically drop the **failure,
security and executable-check** halves of the descriptions rewritten by batches 1–7. Six of the
eighteen sampled show this pattern (`alaa-minio-object-storage`, `alaa-postman-collections`,
`alaa-frontend-developer`, `alaa-crockford-base32-codecs`, `alaa-partitioned-table-fk-audit`,
`alaa-basic-memory-os`). The index was written against the pre-upgrade fleet and has been amended
name-by-name rather than re-derived. That is the structural cause and it will recur.

---

## 2. `AGENTS.md` and `CLAUDE.md`

### 2.1 Current state of the root pair

```bash
sha256sum $R/AGENTS.md $R/CLAUDE.md
# 106d581d…  AGENTS.md
# 8a7a8857…  CLAUDE.md          → DIFFERENT

file $R/AGENTS.md $R/CLAUDE.md
# AGENTS.md: UTF-8 text, with very long lines (1157), with CRLF line terminators
# CLAUDE.md: UTF-8 text, with very long lines (1157)          ← LF

diff --strip-trailing-cr $R/AGENTS.md $R/CLAUDE.md   → identical
tr -d '\r' < AGENTS.md | sha256sum  = tr -d '\r' < CLAUDE.md | sha256sum = 8a7a8857…

wc -lc  → 10 3604 AGENTS.md ; 10 3594 CLAUDE.md      (10 lines, 10 bytes of CR)
```

```bash
git ls-files -s AGENTS.md CLAUDE.md
# 100644 52209cfa3079e6fa732a11b488c69607abaaf060 0  AGENTS.md
# 100644 52209cfa3079e6fa732a11b488c69607abaaf060 0  CLAUDE.md   ← SAME BLOB
git status --porcelain -- AGENTS.md CLAUDE.md   →  " M AGENTS.md"
git cat-file -p 52209cfa… | wc -c               →  3594   (the LF form)
git config --get core.autocrlf                  →  (unset)
ls .gitattributes                               →  No such file
```

**Finding A1 (CONFIRMED, and it is the predicted drift arriving).** In **git** the two files are the
same blob — the carry-over's "byte-identical duplicates" is true of the committed state. In the
**working tree** they have already diverged: `AGENTS.md` carries CRLF and shows as an uncommitted
modification, `CLAUDE.md` carries LF and is clean. With `core.autocrlf` unset and no
`.gitattributes`, nothing normalises this, so the next `git add -A` commits a whitespace-only
divergence and the "identical" invariant is silently gone. The failure mode the carry-over predicted
has already begun; it just happens to be invisible in a `diff` that ignores CR. Any Phase-2 checker
that compares the two files must compare **normalised** content, or it will report a false failure
today and mask a real one later.

### 2.2 The `skills/sohrab/CLAUDE.md` symlink

```bash
ls -la $S/CLAUDE.md      → lrwxrwxrwx … CLAUDE.md -> AGENTS.md
readlink -f $S/CLAUDE.md → …/skills/sohrab/AGENTS.md
file $S/AGENTS.md        → UTF-8 text (regular file, 10205 bytes)
git ls-files -s skills/sohrab/CLAUDE.md
#   120000 47dc3e3d863cfb5727b87d785d09abf9743c0a72 0  skills/sohrab/CLAUDE.md
git cat-file -p 47dc3e3d…  →  AGENTS.md      (9 bytes: the link target)
git config --get core.symlinks  →  true
```

**Finding A2 (CONFIRMED — Windows hazard, currently latent).**

- The root pair are **regular files** (mode `100644`), duplicated by hand.
- `skills/sohrab/CLAUDE.md` is a **real symlink**, committed as git mode `120000` with a 9-byte blob
  containing the literal text `AGENTS.md`.
- This clone has `core.symlinks=true`, so it is materialised correctly **here**.
- On any Windows checkout where `core.symlinks` is false — which is git-for-Windows' default unless
  the user has Developer Mode or runs elevated — git writes a **plain 9-byte text file containing
  `AGENTS.md`**. Claude Code would then load a one-line file whose entire content is the word
  `AGENTS.md`, and every rule in the 10,205-byte `skills/sohrab/AGENTS.md` would be silently absent
  from the Claude Code session. Nothing errors. Nothing warns.

This is not speculation about the mechanism: the committed blob **is** the 9-byte path string, which
is exactly what a non-symlink checkout materialises.

The repository's own doctrine already says this. `alaa-prompting-guide/references/70-agent-instruction-files.md:80`:

> **Symlink.** `ln -s AGENTS.md CLAUDE.md`. Simplest, and truly one file. Two costs: there is nowhere
> to add runtime-specific content, and **on Windows creating a symlink requires Administrator
> privileges or Developer Mode, so mixed-OS teams should use the import bridge instead.**

The repository is developed on Windows (`get_device_info` → `"platform": "win32"`). The tree
therefore uses, in `skills/sohrab/`, the exact mechanism its own authority tells it not to use on
this platform — and at the root, the exact mechanism (`Two maintained files`) the same reference
calls the worst option (`:82`).

### 2.3 The three options, as `70-agent-instruction-files.md` actually states them

Read on the device at
`$S/alaa-prompting-guide/references/70-agent-instruction-files.md`, lines 74–84 and the defect table
at 88–98. Represented faithfully, not paraphrased into a preference:

| Option | The reference's own words | Cost it names | Fit for this repo |
|---|---|---|---|
| **Import bridge** — `CLAUDE.md` = `@AGENTS.md` | ":78 … the approach Claude Code's documentation recommends by name. Both runtimes read the same content, divergence is structurally impossible for the shared part, and there is still a place to put genuinely Claude-only guidance." | ":78 two files exist, and a reader must know which one is authoritative" | **Best fit.** Works on Windows with no privilege. Leaves room for the Claude-only adapter text that `skills/sohrab` may later need. |
| **Symlink** | ":80 Simplest, and truly one file." | ":80 nowhere to add runtime-specific content, and on Windows creating a symlink requires Administrator privileges or Developer Mode" | **Currently in use in `skills/sohrab/` and contraindicated by this very sentence.** |
| **Two maintained files** | ":82 Only justified when the two runtimes genuinely need different content" | ":82 every convention change must be made twice, and the files drift silently because nothing fails when they disagree" | **Currently in use at the root, and the drift in A1 is exactly the predicted symptom.** |

The reference also lists, at `:98`, the defect "Two divergent runtime files → Collapse to the import
bridge or a symlink" — i.e. it treats the root pair as a defect with a named fix.

**A fourth option the reference does not discuss, which the carry-over asks about: a generated copy
plus a divergence checker.** The reference's framing argues against it implicitly — its objection to
two files is that "nothing fails when they disagree", and a checker is precisely a thing that fails.
But a checker has a cost the reference's ranking already implies: it is a *second* mechanism to
maintain, it only fires where it is wired in (this repository has `.githooks/post-merge` and
`post-rewrite` but no pre-commit hook — `ls $R/.githooks` → `post-merge`, `post-rewrite`), and under
this programme's own exit-code contract it must distinguish "could not run" from "clean", which the
existing repository validator does not do (see §6.2). Recommend the import bridge and no checker.

One caveat that binds any option chosen: `70-agent-instruction-files.md:84` —

> "do not put runtime-specific paths or trigger syntax in the shared body. A shared file that says
> `/alaa-security-review` is wrong under Codex and one that says `$alaa-security-review` is wrong
> under Claude Code."

`skills/sohrab/AGENTS.md:35` currently says "`/alaa-prompting-guide` (`$alaa-prompting-guide` in
Codex)" — it gives both forms and labels them, which satisfies the spirit. The root `AGENTS.md:3`
says "`use [$alaa-prompting-guide](…)`" — Codex syntax only, in a file Claude Code also reads. That
is a violation of `:84` in the file that is loaded by both runtimes on every task.

### 2.4 Root `AGENTS.md` content audit

Full text read (`/mnt/user-data/uploads/skills/AGENTS.md`, 11 lines, 3604/3594 bytes).

| Line | Text | Defect |
|---|---|---|
| `:1` | "You write outcome-first prompts for **GPT-5.6**/Codex, clear and explicit agent instructions for Claude/Claude Code" | **Hardcoded model name in an always-loaded file.** `skills/sohrab/AGENTS.md:35` states "Never state a model name. Not in a skill, not in a script, not in an agent definition, not in a generated artifact. Route every model, effort, and runtime-capability question to `/alaa-prompting-guide`." The root file breaks the rule its own subtree enforces. Verified by `grep -inE '\b(gpt-5\|opus 5\|sonnet 5\|fable 5)\b'` over the eight root-level docs: **the only hits in the whole set are `AGENTS.md:1` and `CLAUDE.md:1`.** |
| `:3` | `[$alaa-prompting-guide](D:\\Sohrab\\Project\\skills\\skills\\sohrab\\alaa-prompting-guide\\SKILL.md)` | **Hardcoded machine path**, forbidden by `skills/sohrab/AGENTS.md:39` ("`D:\…` breaks on every other machine"). Also Codex-only trigger syntax in a dual-runtime file — see `:84` above. |
| `:1–2` | ~1157-character single-line paragraphs of role prose | `70-agent-instruction-files.md:58` — "General programming advice… 'Write clean code,' 'handle errors,' 'add tests.' The model already knows, and this content displaces the repository-specific facts it does not know." Lines 1–2 are almost entirely of this kind. |
| `:10` | "Ruls:" | Typo in a binding rule heading. |
| whole file | Names **no skill**, states **no build/test/lint command**, names **no off-limits directory** | `70-agent-instruction-files.md:44–50` lists exactly these as what an instruction file is for. The root file contains none of them. It does not mention `vendor/` being off limits, does not mention `_to_delete/`, does not name `scripts/validate_sohrab_skill_pack.py`, and does not mention that `skills/sohrab/` has its own binding `AGENTS.md`. |

**Does it name skills that no longer exist?** No — it names exactly one skill,
`alaa-prompting-guide`, which exists.

**Does it state conventions later batches overturned?** Yes, by omission rather than assertion: it
predates every convention batches 1–7 established (ownership table, routing convention, exit-code
contract, retirement to `_to_delete/`, description budget). None of them are reachable from the root
file. An agent that starts at the repository root and never descends into `skills/sohrab/` — which is
what Codex does when the working directory is the repository root — gets none of the programme's
rules.

**Does it hardcode a model name?** Yes: `GPT-5.6` at `:1`, in both copies.

---

## 3. `install-skills.md`

**Location:** `D:\Sohrab\Project\skills\install-skills.md`, 11,386 bytes, mtime 2026-07-25 10:23.
Read in full at `/mnt/user-data/uploads/skills/install-skills.md`.

### 3.1 What it actually says

It is a PowerShell symlink-farm installer. Its destination list is `install-skills.md:23–26`:

```powershell
$destinations = @(
    [pscustomobject]@{ Name = "codex";  Path = (Join-Path $HOME ".codex\skills") }
    [pscustomobject]@{ Name = "claude"; Path = (Join-Path $HOME ".claude\skills") }
)
```

**Correction to the lane prompt.** The prompt states the file "targets `~/.codex/skills`". It targets
**both** `~/.codex/skills` **and** `~/.claude/skills`. That matters: it means the file is authoritative
for *two* runtimes, and any skill doc naming only one of them is incomplete rather than merely wrong.
The value `~/.codex/skills` is corroborated as field-verified at
`alaa-prompting-guide/references/11-codex-runtime-features.md:83–88` and `60-skill-authoring.md:33`,
both of which also state that `.agents/skills` is reserved for repository-scoped skills.

Its source-root list is `:10–21`, machine-generated between
`# vendor-subtrees:codex-src-roots:start/end` markers by `python scripts\vendor_subtrees.py refresh-docs`.

### 3.2 Every installation instruction in the tree, checked against it

```bash
grep -rn --include='*.md' --include='*.yaml' -E \
  '\.agents[/\\]skills|~[/\\]\.codex|~[/\\]\.claude|\$HOME[/\\.]*\.(codex|claude|agents)|USERPROFILE.*\.(codex|claude|agents)' \
  $S $R/*.md $R/scripts $R/docs
find $S -iname '*install*' -type f
grep -rn --include='*.md' -iE '^#+ .*install' $S
```

Exactly **one** skill ships a top-level `INSTALL.md`:

**Finding I1 (CONFIRMED — the one the concurrent lane found, re-verified independently).**
`vector-rust-observability-pipelines/INSTALL.md`, full text (12 lines):

```
:4  Recommended locations:
:5  - Repo-local: `<repo>/.agents/skills/vector-rust-observability-pipelines/`
:6  - User-level: `~/.agents/skills/vector-rust-observability-pipelines/`
:10 2. invoke via `/skills` or `$vector-rust-observability-pipelines`
:12 This skill is explicit-first (`allow_implicit_invocation: false`) …
```

against `vector-rust-observability-pipelines/agents/openai.yaml:7`:

```yaml
policy:
  allow_implicit_invocation: true
```

Three separate defects in twelve lines: (a) `:6` names `~/.agents/skills` as the user-level path,
contradicting `install-skills.md:24`; (b) `:5` offers repo-local as an equal option when
`install-skills.md` installs user-level only; (c) `:12` asserts a policy value that its own
`openai.yaml` contradicts. Batch 8 lane L2 owns this skill.

**Finding I2 (CONFIRMED — a second, milder disagreement, not previously reported).**
`alaa-codex-orchestrator/references/installation.md` is the only *other* dedicated installation
document. It is substantially **correct** — `:10` recommends `~/.codex/skills/alaa-codex-orchestrator/`,
`:16` gives the Windows form `Join-Path $HOME ".codex\skills"`, and `:19` states the reservation rule
verbatim ("Use `.agents/skills` when the skill should travel with a specific repository rather than
follow the user"). Its only disagreement with `install-skills.md` is that it says
`$HOME/.agents/skills` and the three repo-local paths "work too", presenting them as co-equal
alternatives rather than as the reserved case; and it does not mention `~/.claude/skills` at all,
which is correct for a Codex-only pack. **Verdict: consistent enough; Phase 2 should leave it and
only align the phrase "those work too" with the reservation rule in the following sentence.**

**Finding I3 (CONFIRMED).** `alaa-codex-orchestrator/README-fa.md:32,44,78,86` gives install paths in
`%USERPROFILE%\.codex\skills\…` and `%USERPROFILE%\.codex\agents` form. These **agree** with
`install-skills.md` on location. They are Persian, in a repository whose `AGENTS.md` requires
artifacts in English — a separate defect class, and outside this lane, but recorded because a lane
grepping install paths is the only lane that will see it.

**No other installation instruction anywhere disagrees.** The remaining `~/.codex`, `~/.claude` and
`.agents/skills` hits in the grep above are of four legitimate kinds, each verified by reading the
line: (i) agent-file install targets `~/.claude/agents` / `~/.codex/agents`, which
`install-skills.md:109–118` itself uses; (ii) runtime-behaviour documentation in
`alaa-prompting-guide/references/11-…`, `41-…`, `60-…`, `70-…`, `80-…`, which is the authority the
carry-over cites and which states the same rule; (iii) references to `.agents/skills/` as the place a
**consumer repository** ships *its own* upstream skills (`alaa-php-clean-code`,
`alaa-laravel-architecture:82`, `alaa-octane-performance:92,97`, `alaa-laravel-upgrade-all-packages`,
`alaa-frontend-doc-annotations:9`) — this is a different subject entirely and is correct;
(iv) diagnostic paths in `alaa-codex-runtime-ops` (`~/.codex/sessions`, `config.toml`).

**Finding I4 (CONFIRMED — a live bug in the authoritative file itself).**
`install-skills.md:16` lists

```powershell
(Join-Path $repoRoot "vendor\basic-memory\basic-memory")
```

as a source root. On disk, `vendor/basic-memory/basic-memory/` contains **only 5** skill directories
(`memory-capture`, `memory-continue`, `memory-metadata-search`, `memory-notes`, `memory-schema`),
while the **14** actual vendored skills live one level up at `vendor/basic-memory/*` — see §5. All
five nested copies are byte-identical duplicates of the top-level ones (`sha256sum` on each pair →
IDENTICAL). Consequence: running the documented installer links **5 of 14** basic-memory skills, and
the nine that `alaa-basic-memory-os` would most plausibly route to (`memory-ingest`, `memory-curate`,
`memory-defrag`, `memory-lifecycle`, `memory-reflect`, `memory-research`, `memory-tasks`,
`memory-ci-capture`, `memory-literary-analysis`) are never installed. `vendor` itself is also a
source root at `:19`, but the loop at `:67–71` requires `SKILL.md` **directly** inside each child
directory, and `vendor/basic-memory/` has none, so that root does not rescue it.

The carry-over's claim that this file "is correct and worth treating as authoritative" is therefore
true about **paths** and false about **coverage**. Lane L5 (`alaa-basic-memory-os`) needs this.

---

## 4. The inventory

### 4.1 Count reconciliation

| Source | Count | Reality |
|---|---|---|
| `UPGRADE-CARRYOVER.md:111` | 63 skill directories | wrong |
| `UPGRADE-CARRYOVER.md:204` | "sixty-eight skill directories" — the same document, 93 lines later | wrong, and **internally inconsistent with its own line 111** |
| A concurrent Batch 8 lane | 69 | wrong |
| Other memory | 68 | wrong |
| **Disk, 2026-07-29** | **67** | `find $S -maxdepth 2 -mindepth 2 -name SKILL.md \| wc -l` → 67 |

The 70/67 gap is `_to_delete/`, `.claude/`, `.obsidian/`. A count of 69 or 70 is what you get by
counting directories without checking for `SKILL.md`; 68 is what you get by excluding two of the three.

**Arithmetic reconciliation of the carry-over's own decomposition:**

- 51 assigned to eight batches — **CONFIRMED.** Summing the eight membership lists at
  `UPGRADE-CARRYOVER.md:162–200`: 6 + 8 + 4 + 5 + 6 + 9 + 8 + 5 = **51**, with no name appearing twice.
- 7 rebuilt pre-programme (`:9–20`) — **CONFIRMED**, and they match the lane brief's list exactly.
- 5 created by the programme (`:111`) — **STALE.** Three more have been created since that sentence
  was written: `alaa-input-normalization` (`UPGRADE-CARRYOVER.md:206` acknowledges it),
  `alaa-minio-object-storage` and `alaa-arvan-object-storage` (both named at `:192` as owners, both
  absent from every batch membership list). The lane brief's list of **8** is correct.
- 51 + 7 + 8 = **66**. Disk = **67**. The residual is exactly one directory: **`alaa-haproxy-lua`**.

So the carry-over's "63" is the sum 51 + 7 + 5 computed against a fleet that has since gained three
created skills and one unclassified one. The number was never a count; it was an accounting identity
that stopped balancing.

### 4.2 The full inventory

Generated by one loop over `$S/*/` with `du -sb`, `find … -type f | wc -l`,
`find "$d/references" -type f | wc -l`, `find "$d/scripts" -type f | wc -l`, `stat -c%s SKILL.md`,
and `find "$d" -type f -printf '%T@ %TY-%Tm-%Td\n' | sort -rn | head -1`.

Batch column: **B1–B8** from `UPGRADE-CARRYOVER.md:162–200` (certain — these are written
memberships). **pre** from `:9–20` (certain). **new** = created by the programme (certain for the
five at `:111`; inferred for `alaa-input-normalization`, `alaa-minio-object-storage`,
`alaa-arvan-object-storage` from the lane brief plus their absence from every membership list).
**none** = assigned nowhere (inferred, then confirmed by `grep -c` returning 0 over the carry-over).

"Rewritten?" is derived from newest-file mtime against the batch's known execution window
(B1 2026-07-25, B2 07-26, B3 07-26, B4 07-26/27, B5 07-28/29, B6 07-28/29, B7 07-29, B8 not yet run).
Where mtime and membership agree I mark **yes**; where the skill is in B8 and its mtime predates the
programme I mark **no (pending)**; this is the one column that is inference rather than observation
and is flagged as such.

| # | Skill | Bytes | Files | Refs | Scripts | `SKILL.md` | Newest mtime | Batch | Rewritten? |
|---|---|---|---|---|---|---|---|---|---|
| 1 | alaa-algorithms-data-structures | 80,233 | 10 | 8 | 0 | 18,540 | 2026-07-26 | new | yes |
| 2 | alaa-arvan-object-storage | 99,894 | 9 | 6 | 1 | 10,178 | 2026-07-28 | new (inferred) | yes |
| 3 | alaa-async-messaging | 127,072 | 19 | 9 | 8 | 7,168 | 2026-07-28 | B5 | yes |
| 4 | alaa-bale-provider | 149,580 | 9 | 4 | 3 | 8,857 | 2026-07-29 | B5 | yes |
| 5 | alaa-bash-shell | 78,572 | 17 | 9 | 2 | 4,754 | 2026-07-25 | pre | pre-programme |
| 6 | alaa-basic-memory-os | 46,141 | 16 | 8 | 6 | 6,326 | **2026-07-03** | B8 | **no (pending)** |
| 7 | alaa-cc-orchestrator | 157,844 | 34 | 7 | 3 | 19,401 | 2026-07-25 | pre | pre-programme |
| 8 | alaa-cicd-laravel-postgres | 60,549 | 10 | 7 | 1 | 4,257 | 2026-07-26 | B2 | yes |
| 9 | alaa-codex-orchestrator | 180,518 | 43 | 8 | 8 | 19,781 | 2026-07-25 | pre | pre-programme |
| 10 | alaa-codex-runtime-ops | 35,766 | 8 | 6 | 0 | 7,452 | 2026-07-25 | pre | pre-programme |
| 11 | alaa-controlled-ops | 35,264 | 7 | 5 | 0 | 3,742 | 2026-07-28 | B1 | yes |
| 12 | alaa-crockford-base32-codecs | 128,721 | 9 | 2 | 2 | 3,365 | 2026-07-26 | B4 | yes |
| 13 | alaa-data-layer | 93,878 | 10 | 8 | 0 | 4,928 | 2026-07-28 | B4 | yes |
| 14 | alaa-docker-production | 340,188 | 37 | 14 | 21 | 3,996 | 2026-07-29 | B7 | yes |
| 15 | alaa-docs-farsi | 150,140 | 14 | 11 | 1 | 10,703 | **2026-05-10** | B8 | **no (pending)** |
| 16 | alaa-frontend-developer | 115,638 | 21 | 19 | 0 | 10,930 | 2026-07-29 | B6 | yes |
| 17 | alaa-frontend-devops | 91,754 | 14 | 11 | 1 | 3,779 | 2026-07-29 | B6 | yes |
| 18 | alaa-frontend-doc-annotations | 90,928 | 11 | 8 | 1 | 4,005 | 2026-07-29 | B6 | yes |
| 19 | alaa-gitlab-ci-cd | 346,595 | 37 | 12 | 15 | 9,117 | 2026-07-29 | B7 | yes |
| 20 | alaa-go-chi-development | 132,367 | 16 | 8 | 1 | 7,130 | 2026-07-28 | B3 | yes |
| 21 | alaa-golang | 147,733 | 18 | 16 | 0 | 6,383 | 2026-07-28 | B3 | yes |
| 22 | alaa-golang-clean-code-principles | 94,683 | 10 | 7 | 0 | 12,249 | 2026-07-26 | B3 | yes |
| 23 | alaa-golang-fiber | 97,200 | 11 | 8 | 0 | 8,209 | 2026-07-26 | B3 | yes |
| 24 | alaa-haproxy | 275,812 | 54 | 12 | 10 | 4,583 | 2026-07-29 | B7 | yes |
| 25 | **alaa-haproxy-lua** | 138,994 | 17 | 11 | 1 | 6,775 | **2026-07-26** | **none** | **NEVER TOUCHED** |
| 26 | alaa-indexeddb-browser-storage | 292,970 | 46 | 22 | 3 | 7,504 | 2026-07-29 | B6 | yes |
| 27 | alaa-input-normalization | 272,789 | 15 | 6 | 3 | 5,810 | 2026-07-29 | new (inferred) | yes |
| 28 | alaa-k8s-helm | 271,208 | 55 | 10 | 39 | 8,673 | 2026-07-29 | B7 | yes |
| 29 | alaa-keyset-pagination | 75,682 | 10 | 8 | 0 | 14,564 | 2026-07-26 | new | yes |
| 30 | alaa-laravel-architecture | 92,474 | 13 | 10 | 1 | 8,507 | 2026-07-26 | B2 | yes |
| 31 | alaa-laravel-job-rabbitmq | 203,762 | 21 | 17 | 0 | 15,962 | 2026-07-26 | B2 | yes |
| 32 | alaa-laravel-public-api-contract-pack | 82,573 | 7 | 4 | 1 | 12,581 | 2026-07-26 | B2 | yes |
| 33 | alaa-laravel-upgrade-all-packages | 58,633 | 8 | 6 | 0 | 7,798 | 2026-07-26 | B2 | yes |
| 34 | alaa-low-noise | 42,324 | 6 | 4 | 0 | 5,226 | 2026-07-25 | pre | pre-programme |
| 35 | alaa-makefile | 213,013 | 23 | 13 | 7 | 7,387 | 2026-07-29 | B7 | yes |
| 36 | alaa-minio-object-storage | 214,894 | 17 | 14 | 1 | 12,298 | 2026-07-28 | new (inferred) | yes |
| 37 | alaa-mongodb-patterns | 55,180 | 8 | 6 | 0 | 3,988 | 2026-07-26 | B4 | yes |
| 38 | alaa-mono-package | 100,254 | 16 | 13 | 1 | 4,406 | 2026-07-29 | B6 | yes |
| 39 | alaa-observability-soc | 80,815 | 12 | 10 | 0 | 6,717 | 2026-07-28 | B1 | yes |
| 40 | alaa-octane-performance | 63,180 | 10 | 8 | 0 | 10,826 | 2026-07-26 | B2 | yes |
| 41 | alaa-partitioned-table-fk-audit | 68,301 | 5 | 2 | 1 | 6,073 | 2026-07-26 | B4 | yes |
| 42 | alaa-permission-generator | 170,712 | 18 | 10 | 2 | 15,267 | 2026-07-28 | B2 | yes |
| 43 | alaa-php-clean-code | 169,332 | 15 | 12 | 0 | 25,259 | 2026-07-28 | B2 | yes |
| 44 | alaa-postman-collections | 183,552 | 21 | 14 | 2 | 9,271 | **2026-07-25** | B8 | **no (pending)** |
| 45 | alaa-project-constitution | 193,906 | 13 | 8 | 1 | 14,835 | 2026-07-25 | B1 | yes |
| 46 | alaa-prompting-guide | 200,682 | 16 | 14 | 0 | 6,731 | 2026-07-26 | pre | pre-programme |
| 47 | alaa-quasar-app-vite-v3 | 264,279 | 36 | 32 | 2 | 7,524 | 2026-07-29 | B6 | yes |
| 48 | alaa-reliability-sla | 112,479 | 11 | 9 | 0 | 16,359 | 2026-07-26 | new | yes |
| 49 | alaa-security-review | 113,981 | 10 | 8 | 0 | 15,090 | 2026-07-28 | B1 | yes |
| 50 | alaa-services-contract | 397,778 | 24 | 22 | 0 | 12,995 | 2026-07-29 | B1 | yes |
| 51 | alaa-shaka-player | 375,945 | 35 | 27 | 1 | 8,823 | 2026-07-29 | B6 | yes |
| 52 | alaa-signoz-clickhouse-docs | 75,423 | 13 | 11 | 0 | 5,608 | **2026-07-06** | B8 | **no (pending)** |
| 53 | alaa-sms-provider-mediana | 185,377 | 13 | 8 | 3 | 10,609 | 2026-07-29 | B5 | yes |
| 54 | alaa-system-design | 82,953 | 10 | 7 | 0 | 18,764 | 2026-07-26 | new | yes |
| 55 | alaa-testing-strategy | 82,284 | 10 | 8 | 0 | 18,786 | 2026-07-26 | new | yes |
| 56 | alaa-trust-gateway-auth | 132,569 | 11 | 8 | 1 | 9,173 | 2026-07-28 | B5 | yes |
| 57 | alaa-ui-ux-design-system | 202,269 | 25 | 22 | 1 | 7,144 | 2026-07-29 | B6 | yes |
| 58 | alaa-vue-typescript-clean-code | 185,912 | 23 | 19 | 1 | 10,725 | 2026-07-29 | B6 | yes |
| 59 | alaa-workflow | 122,084 | 14 | 5 | 2 | 7,391 | 2026-07-25 | pre | pre-programme |
| 60 | ansible-generator | 245,370 | 41 | 5 | 1 | 4,947 | 2026-07-29 | B7 | yes |
| 61 | ansible-validator | 512,391 | 102 | 7 | 22 | 5,190 | 2026-07-29 | B7 | yes |
| 62 | caas-arvan-kuber | 1,685,700 | 24 | 7 | 12 | 8,643 | 2026-07-29 | B7 | yes |
| 63 | clickhouse-performance-schema-ops | 140,925 | 18 | 11 | 1 | 4,252 | 2026-07-26 | B4 | yes |
| 64 | jitsi-platform-architect | 127,709 | 10 | 7 | 1 | 6,688 | 2026-07-28 | B5 | yes |
| 65 | service-runtime-kit-governance | 54,268 | 8 | 6 | 0 | 8,112 | 2026-07-26 | B1 | yes |
| 66 | tusd-upload-platform | 236,916 | 33 | 15 | 1 | 8,668 | 2026-07-28 | B5 | yes |
| 67 | vector-rust-observability-pipelines | 54,441 | 21 | 11 | 1 | 9,487 | **2026-05-31** | B8 | **no (pending)** |

Totals: **9,451,565 bytes**, 1,168 files across 67 skills. Largest: `caas-arvan-kuber` (1.69 MB,
dominated by non-Markdown assets). Smallest: `alaa-controlled-ops` (35 KB). Ships scripts: **43 of
67**; ships **no** scripts: 24.

### 4.3 The "never touched" column — the remaining backlog

**This is the point of the table, and the answer is a single name.**

> **`alaa-haproxy-lua` is the only skill directory in `skills/sohrab/` that this eight-batch
> programme never rewrote and never planned to.**

Evidence chain:

1. `grep -c "haproxy-lua" UPGRADE-CARRYOVER.md` → **0**. It appears in no batch membership, no
   candidate-skill table, no defect list, nowhere in the working contract.
2. `grep -c "haproxy-lua"` over `UPGRADE-BATCH-5-ANALYSIS.md` → 0; `UPGRADE-BATCH-6-ANALYSIS.md` → 0;
   `UPGRADE-BATCH-7-ANALYSIS.md` → **12**, and `UPGRADE-BATCH-7-ANALYSIS.md:408` states independently:
   "**`alaa-haproxy-lua` is assigned to no batch in the carry-over plan**". Batch 7 reached the same
   conclusion from the other direction; two lanes agreeing raises confidence.
3. `git log --diff-filter=A -- skills/sohrab/alaa-haproxy-lua/SKILL.md` → `b920bfdb 2026-07-27
   upgrade batch 4`. It was **added** in the Batch 4 commit, while Batch 4's membership
   (`UPGRADE-CARRYOVER.md:174–176`) is `alaa-data-layer`, `alaa-mongodb-patterns`,
   `alaa-partitioned-table-fk-audit`, `alaa-crockford-base32-codecs`,
   `clickhouse-performance-schema-ops`. It rode in on a commit whose message does not describe it.
4. Newest file mtime 2026-07-26 22:10, i.e. it has not been touched since Batch 4's window and was
   not re-opened by Batch 7 when Batch 7 rewrote `alaa-haproxy`.
5. Batch 7 **did** wire the routing in: `alaa-haproxy/SKILL.md:3` and
   `alaa-haproxy/references/90-companion-boundary.md:22,44,51` and `references/10-version-and-branch.md:82`
   now name `/alaa-haproxy-lua` (`$alaa-haproxy-lua`). So it is reachable — but the target of that
   routing has never been measured against the ten criteria.

**Everything else is accounted for.** The 51 batch-assigned skills have all been rewritten except the
five Batch 8 owns, which are in flight in this very batch (rows 6, 15, 44, 52, 67 above — all with
pre-programme mtimes, which independently corroborates that Batch 8 has not yet executed Phase 2).
The 7 pre-programme skills and the 8 programme-created skills are at standard by construction.

**Secondary backlog, distinct from "never touched": skills rewritten by a batch that still fail the
repository's own validator.** See §6.2 — 30 of 67 do. Those are not backlog in the same sense
(someone looked at them), but they are the list a "definition of done" reader would expect to be
empty. Nobody has written that list down either; §6.2 is it.

### 4.4 Router-convention conformance, re-measured

`skills/sohrab/AGENTS.md:49` makes this binding: ≤8 references → router in `SKILL.md`, **no**
`references/00-topic-map.md`; ≥9 references → router **in** `references/00-topic-map.md`.

```bash
ls -d $S/*/references/00-topic-map.md $S/*/docs/00-topic-map.md 2>/dev/null | wc -l   # 29
```

**29 of 67 carry a topic map; 38 do not.** The carry-over's `:204` figure ("Twenty-eight of the
sixty-eight") is off by one on both numbers.

Four skills violate the rule as written:

| Skill | `references/*.md` count | Topic map? | Violation |
|---|---|---|---|
| `alaa-codex-runtime-ops` | 6 (incl. the topic map itself → 5 real) | **yes** | below threshold, should not have one |
| `alaa-async-messaging` | 9 | **no** | at/above threshold, should have one |
| `alaa-prompting-guide` | 14 | **no** | above threshold, should have one |
| `vector-rust-observability-pipelines` | 11 | **no** | above threshold, should have one — **and it is a Batch 8 skill, so lane L2 can fix it in-batch** |

Note that two of the four are pre-programme skills (`alaa-codex-runtime-ops`, `alaa-prompting-guide`)
rebuilt *before* the convention existed. That is the honest reason for the inconsistency, and it is
the fact the "mandatory or optional" decision should turn on.

### 4.5 `agents/openai.yaml` coverage

`README.md:14` asserts: "`agents/openai.yaml` ships with every skill a Codex agent can load; a
Claude-Code-only skill with a Codex twin is the only exception."

```bash
for d in $S/*/; do [ -f "$d/SKILL.md" ] || continue; [ -f "$d/agents/openai.yaml" ] || basename $d; done
# alaa-cc-orchestrator
# alaa-go-chi-development
```

- `alaa-cc-orchestrator` — **legitimate exception**: it is Claude-Code-only and its Codex twin
  `alaa-codex-orchestrator` does ship one. The README sentence covers it exactly.
- `alaa-go-chi-development` — **violation**. It has no Codex twin and no `openai.yaml`. It is a
  Batch 3 skill, rewritten 2026-07-28. The validator flags it (`§6.2`).

So `README.md:14` is **one exception short of true**, and the carry-over's "verify per batch rather
than assuming" instruction was warranted.

---

## 5. `vendor/`

**Nothing under `vendor/` was modified. Read-only inspection only.**

```bash
ls -la $R/vendor/
cat $R/vendor/subtrees.json
for d in $R/vendor/*/; do echo "$(basename $d) $(find "$d" -name SKILL.md | wc -l) $(du -sb "$d"|cut -f1)"; done
```

### 5.1 `subtrees.json` versus disk versus the carry-over

| Subtree | `subtrees.json` upstream | Pin | Carry-over says | On disk (`find -name SKILL.md`) | Verdict |
|---|---|---|---|---|---|
| `openfga-agent-skills` | `https://github.com/openfga/agent-skills.git`, branch `main`, `post_sync` runs `node vendor/openfga-agent-skills/scripts/build-agents-md.js` | none (tracks `main`) | 1 | **1** (`skills/openfga/SKILL.md`) | **CONFIRMED** |
| `cc-skills-golang` | `https://github.com/samber/cc-skills-golang.git`, `main` | none | 46 | **46** | **CONFIRMED** |
| `claude-plugins-official` | `https://github.com/anthropics/claude-plugins-official.git`, `main` | **`f42c6edab38a90e56b7120a45525c541dee86ecc`** | "Anthropic, pinned commit, —" | **29** | pin CONFIRMED; count now known |
| `knowledge-work-plugins` | `https://github.com/anthropics/knowledge-work-plugins.git`, `main` | **`73b2b2dc0cf8467da112d0ef6b555ab022ee219d`** | "Anthropic, pinned commit, —" | **212** | pin CONFIRMED; count now known |
| `basic-memory` | `https://github.com/basicmachines-co/basic-memory.git`, `main`, `source_path: "skills"` | **`a1e0987eaf5ac9853c32fed5d907b1451e7a90df`** | 19 | **19 files / 14 unique skills** | **MISLEADING — see 5.2** |
| `skill-temporal-developer` | `https://github.com/temporalio/skill-temporal-developer.git`, `main` | none | 1 | **1** (root `SKILL.md`) | **CONFIRMED** |

Byte sizes: `cc-skills-golang` 4,229,573; `claude-plugins-official` 5,799,199;
`knowledge-work-plugins` 8,981,573; `basic-memory` 259,984; `openfga-agent-skills` 256,283;
`skill-temporal-developer` 759,301.

The carry-over's table (`:87–99`) is correct on every count it gives and understates the two
Anthropic packs, which between them hold **241** skills — more than three times the size of the
first-party fleet. That is worth knowing before anyone proposes a new skill.

### 5.2 The 19 vendored `basic-memory` skill names, in full

Lane L5 needs these and nothing records them. **Fourteen unique skills** at
`vendor/basic-memory/<name>/SKILL.md`:

1. `memory-capture`
2. `memory-ci-capture`
3. `memory-continue`
4. `memory-curate`
5. `memory-defrag`
6. `memory-ingest`
7. `memory-lifecycle`
8. `memory-literary-analysis`
9. `memory-metadata-search`
10. `memory-notes`
11. `memory-reflect`
12. `memory-research`
13. `memory-schema`
14. `memory-tasks`

Plus a nested duplicate directory `vendor/basic-memory/basic-memory/` holding **five** of them again:

15. `basic-memory/memory-capture`
16. `basic-memory/memory-continue`
17. `basic-memory/memory-metadata-search`
18. `basic-memory/memory-notes`
19. `basic-memory/memory-schema`

`sha256sum` of each nested `SKILL.md` against its top-level counterpart: **IDENTICAL for all five.**
So "19" counts files, not skills; **14** is the number of distinct vendored memory skills, and 5 are
duplicated. The duplicate directory was introduced by commit `a82b2ea5 "basis memory"`
(`git log -- vendor/basic-memory/basic-memory`), and it is the directory `install-skills.md:16`
points at — see Finding I4.

Cross-check against `vendor/basic-memory/skills-lock.json`: it records **nine** skills with upstream
hashes (`memory-defrag`, `memory-ingest`, `memory-lifecycle`, `memory-metadata-search`,
`memory-notes`, `memory-reflect`, `memory-research`, `memory-schema`, `memory-tasks`). The lock file,
the directory listing and the installer source root give **three different answers** (9, 14, 5) about
what this vendored pack contains. Lane L5 should treat the directory listing as truth and the other
two as artifacts.

The five duplicated names are also exactly the five that appear in this session's own skill listing as
`memory-capture`, `memory-continue`, `memory-metadata-search`, `memory-notes`, `memory-schema` — which
is consistent with the installer having linked only the nested directory.

---

## 6. Repository-level defects found while auditing the indexes

These are in scope because each is an index or a checker that is not telling the truth.

### 6.1 The root `README.md` declares the repository deprecated

`D:\Sohrab\Project\skills\README.md:1–2`, 4,594 bytes:

> `> [!IMPORTANT]`
> `> **This repository is deprecated.** For current Codex skill and plugin examples, use the
> [OpenAI Plugins repository](https://github.com/openai/plugins)…`

This is inherited verbatim from the upstream `openai/skills` repository this tree was forked from —
lines 4–39 are the upstream README unchanged, including "`Skills in .system are automatically
installed in the latest version of Codex`" and `$skill-installer` usage. Only the vendored-upstreams
block (`:41–90`) is local. The file also points at `skills/.experimental/` (`:19`, `:27–31`), which
**does not exist** (`ls $R/skills/` → `.curated`, `.system`, `sohrab` only).

The topmost, most-read index file in the repository opens by telling the reader the repository is
dead. That is the most consequential index defect in the tree after the validator failure, and it is
not in the carry-over at all.

`skills/.curated/` holds 39 skills and `skills/.system/` holds 5 — including `openai-docs`,
`playwright` and `playwright-interactive`, the three that `skills/sohrab/README.md:54–56` calls
"system-level helpers: referenceable, not pack-local". That description is right about their status
and silent about their location, which is two directories away in this same repository.

### 6.2 The repository's own validator fails, and does not honour the exit-code contract

Run read-only, from `/tmp`, with bytecode writing disabled so nothing was created on the device:

```bash
cd /tmp && PYTHONDONTWRITEBYTECODE=1 python3 $R/scripts/validate_sohrab_skill_pack.py; echo "EXIT=$?"
```

Observed: **`EXIT=1`, 51 errors across 30 of 67 skills, 26 warnings.** Verbatim error classes:

- **`missing a 'When not to use' or 'Do not use' section` — 26 skills**:
  `alaa-algorithms-data-structures`, `alaa-bash-shell`, `alaa-cc-orchestrator`,
  `alaa-cicd-laravel-postgres`, `alaa-codex-orchestrator`, `alaa-codex-runtime-ops`,
  `alaa-crockford-base32-codecs`, `alaa-go-chi-development`, `alaa-golang`, `alaa-golang-fiber`,
  `alaa-haproxy-lua`, `alaa-keyset-pagination`, `alaa-laravel-architecture`,
  `alaa-laravel-job-rabbitmq`, `alaa-laravel-public-api-contract-pack`,
  `alaa-laravel-upgrade-all-packages`, `alaa-low-noise`, `alaa-observability-soc`,
  `alaa-octane-performance`, `alaa-php-clean-code`, `alaa-reliability-sla`, `alaa-security-review`,
  `alaa-system-design`, `alaa-testing-strategy`, `clickhouse-performance-schema-ops`,
  `service-runtime-kit-governance`.
- **`short_description must be 25-64 chars` — 18 skills**, including six doctrine owners
  (`alaa-observability-soc`, `alaa-reliability-sla`, `alaa-security-review`, `alaa-system-design`,
  `alaa-testing-strategy`, `alaa-keyset-pagination`).
- **`missing agents/openai.yaml` — 2**: `alaa-cc-orchestrator` (legitimate), `alaa-go-chi-development`
  (defect).
- **`default_prompt must mention $<name>` — 3**: `alaa-basic-memory-os`, `alaa-observability-soc`,
  `alaa-signoz-clickhouse-docs`. Two of the three are Batch 8 skills.
- **`referenced path does not exist` — 3 broken links**:
  - `alaa-golang: references/05-phase-and-source-truth.md`
  - `alaa-golang-clean-code-principles: references/10-` (a truncated path in the source text)
  - `alaa-mongodb-patterns: references/24-metric-registry.md` (a cross-skill path written without
    naming `alaa-services-contract`, which is the exact convention violation
    `skills/sohrab/AGENTS.md:57` prohibits — and which is why the validator resolves it locally and
    fails)

Warnings: 22 bodies over 120 lines (worst: `vector-rust-observability-pipelines` at **227**,
`alaa-project-constitution` 207, `alaa-laravel-job-rabbitmq` 204, `alaa-php-clean-code` 198), and 4
descriptions over the 950 author target (`alaa-laravel-architecture` 1001, `alaa-laravel-public-api-contract-pack`
994, `alaa-php-clean-code` 984, `clickhouse-performance-schema-ops` 956).

**Three structural defects in the validator itself**, all relevant to this lane because a lying
checker is a lying index:

1. **It has no exit code 2.** `validate_sohrab_skill_pack.py:main()` ends `return 1 if errors else 0`.
   A missing Python, an unreadable `PACK_DIR`, or an exception produces a non-zero exit that a CI gate
   cannot distinguish from "found defects", and a *successful* run on an *empty* pack directory
   returns 0. This is exactly the failure the programme's exit-code contract exists to prevent, in the
   programme's own gate.
2. **`ROOT = Path(__file__).resolve().parents[1]`** (line 7) — defect class 7 from the lane brief,
   verbatim. The script cannot be run from anywhere but its committed location.
3. **The 950 target contradicts the batch-8 rule.** The script warns above 950
   (`DESCRIPTION_TARGET_MAX = 950`) and `skills/sohrab/AGENTS.md:78` states "Author target: 950",
   while the lane brief and `UPGRADE-CARRYOVER.md:238` both say **"Keep every description at or below
   900 characters"** because the plugin validator's own count exceeds a YAML-parsed count by ≥30.
   Three files, two numbers. Whichever is right, the tree currently says both.

### 6.3 Six shipped `__pycache__` directories

```bash
find $S -name '__pycache__' -type d
```
→ `alaa-bale-provider/scripts/`, `alaa-gitlab-ci-cd/scripts/`, `alaa-k8s-helm/scripts/`,
`alaa-sms-provider-mediana/scripts/`, `ansible-validator/scripts/`,
`ansible-validator/scripts/lib/`, plus `$R/scripts/__pycache__/validate_sohrab_skill_pack.cpython-310.pyc`
at the repository root.

`.gitignore` ignores `__pycache__/` and `*.pyc`, so none are committed. But
`skills/sohrab/AGENTS.md:84` requires "Move any `__pycache__` your test runs created into
`_to_delete/`", and they are on disk in the working tree that gets zipped and installed. Defect class
8, seven instances.

### 6.4 Untracked working directories at the repository root

`ls $R` shows `.tmp-review-20260729/` (three subdirectories named
`haproxy-defaults-crlf-cj_fq04t`, `haproxy-defaults-selftest-lssnzz5a`, `haproxy-examples-crlf-_1yjdjnj`),
`artifacts/`, `outputs/`, `test-results/`, and `other/`. `other/` is gitignored; the rest are not
named in `.gitignore` and none is described in any README. `.tmp-review-20260729` is a temp directory
inside the repository — defect class 7's second half ("temp dirs inside the repository") — created
today, presumably by a Batch 7 or Batch 8 script run.

---

## 7. The standing edit prohibition — the conflict, stated, not resolved

**I am not resolving this. It is the first owner decision.**

### 7.1 The two rules, quoted

**Rule A — `UPGRADE-CARRYOVER.md`, which assigns these files to Batch 8.** Three separate places:

- `:158` (Rules that hold whether batches run one at a time or not) — "**Nobody but the coordinator
  edits shared files.** `README.md`, `AGENTS.md` and this document belong to the human between
  batches, **and to Batch 8 at the end.**"
- `:149` — "**Documentation last.** Batch 8 owns `README.md` and the repository-level cleanup, so it
  must see the final inventory."
- `:201` (Batch 8 membership) — "Plus the repository-level cleanup in section 6, and a link check that
  every cross-skill path in `skills/sohrab/` resolves."
- `:216` — "An index that lies is worse than no index, because agents route from it. **Fix it in Batch
  8**, once the real inventory is settled."
- `:222` — the `AGENTS.md`/`CLAUDE.md` duplication "falls to Batch 8 with the rest of the
  repository-level cleanup."

**Rule B — the session prompt at `UPGRADE-CARRYOVER.md:252–…`, HARD RULES block:**

> "- Never edit a skill outside this batch, and **never edit README.md or UPGRADE-CARRYOVER.md**.
>   Other batches may be running against the same repository. If you find a defect outside your batch,
>   report it to me instead of fixing it."

### 7.2 Exactly which files each rule covers

| File | Rule A (Batch 8 owns) | Rule B (never edit) | Net |
|---|---|---|---|
| `skills/sohrab/README.md` | **yes**, explicitly, `:216` | **yes**, by name | **CONFLICT** |
| `skills/sohrab/README.fa.md` | implied by "repository-level cleanup" and by `:206` naming both READMEs | **not named** — Rule B says "README.md" | **AMBIGUOUS**. A literal reading permits editing the Persian file and forbids the English one, which would make the two indexes disagree for the first time. |
| `skills/sohrab/UPGRADE-CARRYOVER.md` | belongs to "the human between batches, and to Batch 8 at the end" (`:158`) | **yes**, by name | **CONFLICT** |
| Root `AGENTS.md` | **yes**, `:158` and `:222` | not named | permitted by both, if "README.md" is read literally |
| Root `CLAUDE.md` | implied by `:222` ("a single source with a generation or link step") | not named | permitted |
| `skills/sohrab/AGENTS.md` | `:158` says "`AGENTS.md`" without a path; both files exist | not named | ambiguous which `AGENTS.md` `:158` means |
| Root `README.md` | not named anywhere | not named ("README.md" in Rule B most naturally reads as the one beside the carry-over) | **unowned by anyone**, which is why §6.1 has survived |
| `install-skills.md` | "repository-level cleanup" | not named | permitted |
| `scripts/validate_sohrab_skill_pack.py` | "repository-level cleanup" | not named | permitted |

Note what falls out of that table: the root `README.md` that declares the repository deprecated is
covered by **neither** rule. It is nobody's file. That is the likeliest reason it has survived seven
batches unchanged.

### 7.3 Why the conflict exists (offered as context, not as a resolution)

Rule B's own stated reason is concurrency — "Other batches may be running against the same
repository". Rule A's carve-out at `:158` ("and to Batch 8 at the end") is the exception written for
precisely the batch that runs alone (`:153`: "8 runs alone"). So the two rules are reconcilable *in
intent*. But the session prompt is a copy-paste template whose only documented edit point is the
`BATCH` line (`:254`: "Paste this into a fresh session, changing only the `BATCH` line"), and its
HARD RULES were never amended for the batch that was always going to need the exception. The literal
text of the prompt driving this batch forbids what the plan driving this batch requires.

**This is the owner's call because either reading has a real cost, and because the prohibition is a
standing instruction from him.**

### 7.4 The options, with costs

**Option 1 — the owner lifts the prohibition for Batch 8 and Phase 2 edits the files in place.**

- *Cost:* none to correctness. The concurrency reason for Rule B does not apply — Batch 8 runs alone
  by `:153`, and no other batch remains. Requires one sentence from the owner.
- *Benefit:* the index that agents route from becomes true. `README.md:93`'s "every folder appears
  exactly once" becomes a fact instead of a claim.
- *Risk:* if the owner is in fact running something else against this repository right now, an edit
  to `README.md` can collide. The `.tmp-review-20260729/` directory created today shows something
  else has been running.

**Option 2 — ship the corrected inventory as a NEW file and leave `README.md` untouched.**

- *Cost, and it is higher than it looks:* the repository would then hold **three** skill indexes
  (`README.md`, `README.fa.md`, and the new file) where it holds two today. `skills/sohrab/AGENTS.md:15`
  is explicit: "A rule has exactly one owning file. When two skills state the same rule, one of them is
  wrong." A third index is a third thing to drift. Worse, an agent loading the repository has no way to
  learn that the new file supersedes `README.md` — nothing routes to it, because the thing that would
  route to it is `README.md`, which we are not allowed to edit. **The new file would be correct and
  unreachable.** That is the specific cost the lane prompt asked me to price, and it is the reason I
  do not recommend this option.
- *Mitigation that does not work:* naming it `README.new.md` or `INVENTORY.md` and telling the owner
  to rename it later converts a documentation fix into a pending manual step, which is how the
  `alaa-frontend-developer` script retirement failed to land (`UPGRADE-CARRYOVER.md:210`).

**Option 3 — Phase 2 produces a machine-generated inventory plus a checker, and the owner applies it.**

- Generate `skills/sohrab/README.md`'s map section from disk, and ship
  `scripts/check_skill_index.py` (exit 0/1/2) that fails when the map and the directory disagree in
  either direction. Phase 2 writes the script and the diff; the owner applies the diff.
- *Cost:* one more script to maintain, and the map section of `README.md` becomes generated, so a
  human editing it by hand loses the edit. Mitigated by generating only between explicit
  `<!-- skill-map:start/end -->` markers, the pattern `install-skills.md:13,20` and `:187,195`
  already uses successfully for the vendor block.
- *Benefit:* this is the only option that makes the defect **non-recurring**. R1 and R2 both exist
  because a human maintained a list by hand; R5 exists for the same reason.

**My recommendation: Option 3 for the map, gated on Option 1 for the one-time apply.** Ask the owner
for a narrow, explicit lift of the prohibition covering exactly five files —
`skills/sohrab/README.md`, `skills/sohrab/README.fa.md`, root `AGENTS.md`, root `CLAUDE.md`, root
`README.md` — and leave `UPGRADE-CARRYOVER.md` under the prohibition, because the carry-over is the
programme's own history and Phase 2 has no reason to rewrite it. Reason: the marker-delimited
generated block plus a 0/1/2 checker is the only shape that satisfies both "the index must stop lying"
and "nobody maintains two lists by hand", and it costs one owner sentence rather than an ongoing
manual step.

---

## 8. The Phase 2 work order

File by file, executable without re-deriving this analysis. Everything below is **blocked on the
owner's decision in §7** except items 8.6 and 8.7.

### 8.1 `skills/sohrab/README.md` — edit (2 insertions, 1 sentence corrected)

- Insert `alaa-haproxy-lua` into the group **"Containers, CI/CD, Kubernetes, and platform delivery"**
  (beside `alaa-haproxy`, `README.md:166`).
- Insert `alaa-input-normalization` into **"Core Ala architecture and policy"** — the lane brief's
  doctrine-owner list places it beside `alaa-keyset-pagination` and `alaa-algorithms-data-structures`,
  which are both in that group (`README.md:106–107`).
- Wrap the map section in `<!-- skill-map:start -->` / `<!-- skill-map:end -->` so 8.6 can regenerate it.
- Correct `README.md:93` "Groups match `README.fa.md`" → the two files use different group
  boundaries; either state that they carry the same membership in different groupings, or renumber
  the Persian groups to match. Prefer the former; renumbering the Persian file is churn.
- Result: map goes 65 → 67 names. Byte growth ≈ +60. No capability claimed; this is a correction.

### 8.2 `skills/sohrab/README.fa.md` — edit (2 rows added, 1 row corrected)

- Add `alaa-haproxy-lua` to §7 (زیرساخت و تحویل) and `alaa-input-normalization` to §1.
- **Correct `README.fa.md:120`**: `alaa-docs-farsi` produces English documentation per its own
  frontmatter. Rewrite the purpose cell to say it writes repository documentation in simple English
  for maintainers, frontend integrators, operators and agents. Coordinate with lane L3 — if L3
  changes what that skill owns, this row must be written from L3's final frontmatter, not from
  today's.
- Re-derive the six one-liners flagged in R5 from the current frontmatter, keeping the failure and
  security halves: `alaa-minio-object-storage:72`, `alaa-postman-collections:119`,
  `alaa-frontend-developer:79`, `alaa-crockford-base32-codecs:70`,
  `alaa-partitioned-table-fk-audit:69`, `alaa-basic-memory-os:37`.
- Add the `alaa-docker-production` "decides no gate" clause at `:93` and the `alaa-haproxy` →
  `alaa-haproxy-lua` routing at `:96`, since D8's boundary is the fact an index most needs to carry.

### 8.3 Root `AGENTS.md` + `CLAUDE.md` — rewrite one, replace the other with an import bridge

- **Normalise line endings first.** `AGENTS.md` currently differs from `CLAUDE.md` only by CRLF and
  shows as an uncommitted modification. Restore it to the committed LF form before any content edit,
  or the content diff will be unreadable.
- Rewrite root `AGENTS.md` to the shape `70-agent-instruction-files.md:44–50` prescribes, removing:
  - the hardcoded model name `GPT-5.6` (`:1`) — replace with a pointer to `alaa-prompting-guide`
    without a model name;
  - the hardcoded path `D:\\Sohrab\\Project\\skills\\…` (`:3`) — replace with the repo-relative
    `skills/sohrab/alaa-prompting-guide/SKILL.md`;
  - the Codex-only `$` prefix in the shared body (`:3`), per `:84` — give both forms or neither;
  - the two 1157-character general-advice paragraphs (`:1–2`).
  And **adding** what it currently lacks: `vendor/` is never edited; nothing is deleted, retired files
  go to `_to_delete/<YYYYMMDD>-<reason>/`; the validator command
  `python scripts\validate_sohrab_skill_pack.py` and what its exit codes mean; the fact that
  `skills/sohrab/AGENTS.md` is the binding contract for work inside the pack. Target ≤ 60 lines.
- **Replace root `CLAUDE.md` with a one-line import bridge**: `@AGENTS.md`, optionally followed by a
  Claude-only section. This is `70-agent-instruction-files.md:78`'s named recommendation and it is
  the only option that survives a Windows checkout without Developer Mode.
- Retire the current root `CLAUDE.md` body to `_to_delete/20260729-batch8/CLAUDE.md` — it is
  byte-identical to `AGENTS.md`'s committed blob, so nothing is lost, but the rule is that nothing is
  deleted.

### 8.4 `skills/sohrab/CLAUDE.md` — convert the symlink to an import bridge

- Replace the `120000` symlink with a regular file containing `@AGENTS.md`.
- Reason, in one sentence for the commit message: a git symlink checked out on Windows without
  `core.symlinks` becomes a 9-byte text file containing the word `AGENTS.md`, and Claude Code then
  loads that instead of the 10,205-byte contract, silently.
- **This changes a file mode in git.** Flag it to the owner explicitly; it is not a content-only edit.

### 8.5 `vector-rust-observability-pipelines/INSTALL.md` — retire, and fold into `SKILL.md`

Owned by lane L2, listed here so the two lanes do not both write it. Retire the file to
`_to_delete/20260729-batch8/`, because a top-level `INSTALL.md` is not part of the Agent Skills
layout and no other skill in the fleet ships one. If installation guidance is kept at all, it belongs
in one line pointing at `install-skills.md`. Separately, `agents/openai.yaml:7` and the retired
`INSTALL.md:12` disagree on `allow_implicit_invocation`; L2 decides which is intended and states it
once.

### 8.6 New: `scripts/check_skill_index.py` — the checker that makes R1/R2/R5 non-recurring

Asserts, exiting **0 clean / 1 findings / 2 could not run**:

1. The set of directories under `skills/sohrab/` containing a `SKILL.md` equals the set of names
   inside `<!-- skill-map:start/end -->` in `README.md` — **both directions**, reported separately.
2. The same set equals the names in backticks inside the group tables of `README.fa.md`.
3. `README.md`'s "Consolidated or removed" list contains **no** name that exists as a directory.
4. Root `AGENTS.md` and root `CLAUDE.md` agree after `\r` normalisation, **or** `CLAUDE.md` is exactly
   an import of `AGENTS.md`. (Normalised comparison, per §2.1 — a byte comparison fails today for the
   wrong reason.)
5. Exit **2**, not 1, when `skills/sohrab/` is unreadable, when either README is missing, or when the
   marker block is absent — the three ways this check can be wrong rather than failing.

Takes the pack root as an argument with a default, so it does not repeat
`Path(__file__).parents[N]`. Must run under Windows PowerShell: no shebang reliance, no
`os.symlink`, and every path built with `pathlib`.

### 8.7 `scripts/validate_sohrab_skill_pack.py` — three fixes

- Add exit code **2** for could-not-run (unreadable `PACK_DIR`, zero skills found, any unhandled
  exception), and make a zero-skill run a **2**, not a **0**.
- Replace `ROOT = Path(__file__).resolve().parents[1]` with an argument defaulting to the current
  behaviour.
- Reconcile `DESCRIPTION_TARGET_MAX` with the 900-character rule at `UPGRADE-CARRYOVER.md:238` and
  `skills/sohrab/AGENTS.md:78`. One number, in one place, cited by the other two.
- Do **not** attempt to fix the 51 errors it reports — 26 of them are missing "when not to use"
  headings in skills outside Batch 8, which Rule B forbids touching. Report them (§6.2 is the report).

### 8.8 Root `README.md` — owner decision required before any edit

It is owned by no rule (§7.2). It declares the repository deprecated and points at a
`skills/.experimental/` directory that does not exist. Minimum fix: delete the inherited deprecation
banner (`:1–2`) and the `.experimental` references (`:19`, `:27–31`). This is the highest
value-per-byte edit available anywhere in the tree, and it needs one sentence of permission.

### 8.9 Housekeeping

- Move the seven `__pycache__` directories (§6.3) to `_to_delete/20260729-batch8/pycache/`.
- Ask the owner whether `.tmp-review-20260729/` at the repository root is still needed; if not, move
  it to `_to_delete/`. Do not delete.
- Add `.tmp-review-*/`, `artifacts/`, `outputs/`, `test-results/` to `.gitignore` **only if** the
  owner confirms they are scratch. Three of the four are untracked and undescribed.

### 8.10 Byte budget

| File | Now | Target | Capability earning any growth |
|---|---|---|---|
| `skills/sohrab/README.md` | 11,034 | ≤ 11,300 | +2 index entries, +markers. No new capability; correction only. |
| `skills/sohrab/README.fa.md` | 12,281 | ≤ 12,900 | +2 rows, 8 rewritten one-liners. Correction only. |
| Root `AGENTS.md` | 3,594 | ≤ 3,600 | Content is replaced, not added: role prose out, repository facts in. Must not grow. |
| Root `CLAUDE.md` | 3,594 | **~12** | `@AGENTS.md`. |
| `skills/sohrab/CLAUDE.md` | 9 (symlink) | ~12 | `@AGENTS.md`. |
| `scripts/check_skill_index.py` | — | ≤ 8,000 new | **New capability:** the fleet gains a checker for the two-way index identity, which no tool currently reports. |
| `scripts/validate_sohrab_skill_pack.py` | 9,383 | ≤ 9,900 | **New capability:** exit code 2, so a CI gate can tell "could not run" from "clean". |

---

## 9. Open questions for the owner

**Q1 — the edit prohibition (blocks almost everything above).**
`UPGRADE-CARRYOVER.md:158/:216/:222` assign `README.md` and `AGENTS.md` to Batch 8; the session
prompt's HARD RULES say "never edit README.md or UPGRADE-CARRYOVER.md". *Recommendation:* lift the
prohibition for exactly five files — `skills/sohrab/README.md`, `skills/sohrab/README.fa.md`, root
`AGENTS.md`, root `CLAUDE.md`, root `README.md` — and keep it for `UPGRADE-CARRYOVER.md`. *Reason:*
Rule B's own stated cause is concurrent batches, and `:153` says Batch 8 runs alone, so the cause does
not apply; the carry-over is programme history and Phase 2 has no reason to rewrite it. *Trade-off:*
the alternative — a new inventory file — produces a correct index that nothing routes to, because the
thing that would route to it is the file we may not edit.

**Q2 — `alaa-haproxy-lua`, the whole remaining backlog.**
It is the one skill directory assigned to no batch, never rewritten, 138,994 bytes, 11 references, 1
script, and it fails the validator on "missing a 'When not to use' section" and
"short_description must be 25-64 chars". `alaa-haproxy` now routes to it from four places.
*Recommendation:* add it to Batch 8 as a sixth member, or schedule a Batch 9 of one. *Reason:* after
Batch 8 closes it becomes the only unaudited skill in a fleet whose whole claim is uniformity, and it
is reachable from a Batch 7 skill that was rewritten to standard. *Trade-off:* adding it to Batch 8
grows a batch that already owns five skills plus the repository cleanup; deferring it leaves the
programme unable to say "the fleet is at standard".

**Q3 — the router convention: mandatory or optional.**
29 of 67 carry `references/00-topic-map.md`; four skills violate the threshold rule at
`skills/sohrab/AGENTS.md:49` (`alaa-codex-runtime-ops` has one below threshold;
`alaa-async-messaging`, `alaa-prompting-guide` and `vector-rust-observability-pipelines` lack one
above it). Two of the four are pre-programme skills that predate the rule. *Recommendation:* keep the
rule mandatory and fix the four, but fix only `vector-rust-observability-pipelines` in this batch (it
is Batch 8's) and file the other three. *Reason:* a threshold rule with four public exceptions is not
a rule; and the fix is mechanical. *Trade-off:* touching `alaa-prompting-guide` means editing the
authority skill outside its batch, which Rule B forbids.

**Q4 — the description character budget: 900 or 950.**
`scripts/validate_sohrab_skill_pack.py` and `skills/sohrab/AGENTS.md:78` say 950;
`UPGRADE-CARRYOVER.md:238` and the Batch 8 lane brief say 900. Four skills currently sit between
(956, 984, 994, 1001). *Recommendation:* measure the plugin validator's real count against one of
those four and set a single number everywhere. *Reason:* the 900 figure is explicitly provisional in
its own source ("until someone measures the real rule from a second data point"). *Trade-off:*
adopting 900 without measuring forces rewrites of four descriptions that may not need them.

**Q5 — `vendor/basic-memory` has three different answers about what it contains.**
`skills-lock.json` names 9 skills, the directory holds 14, `install-skills.md:16` points the installer
at a nested duplicate holding 5. *Recommendation:* change `install-skills.md:16` from
`vendor\basic-memory\basic-memory` to `vendor\basic-memory`, and ask upstream-sync whether the nested
directory should be removed on the next `git subtree pull`. *Reason:* today the documented installer
links 5 of 14 basic-memory skills and `alaa-basic-memory-os` (Batch 8) routes into a pack that is
mostly not installed. *Trade-off:* `install-skills.md` is generated between markers by
`vendor_subtrees.py refresh-docs`, so the fix probably belongs in that script rather than in the
Markdown — confirm before editing the generated block by hand. **Do not touch `vendor/` itself.**

**Q6 — root `README.md` says the repository is deprecated.**
Inherited from the `openai/skills` fork; it also points at a `skills/.experimental/` directory that
does not exist. It is assigned to no rule and no batch. *Recommendation:* let Batch 8 delete the
banner and the `.experimental` references, keeping the vendored-upstreams block. *Reason:* it is the
first thing any reader or agent sees, and it is false. *Trade-off:* none that I can identify, which is
itself a reason to ask — a false deprecation banner surviving seven batches suggests someone may have
kept it deliberately.
