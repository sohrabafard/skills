# Independent aggregate checker reviews

Round 1 candidate: `0ee59aa0`. Date: 2026-11-04.
The independent verifier passed the declared focused suite, both broken controls,
the actual 24.8 merge fixture, and the unchanged-WA comparison. Those checks did
not cover every parser trust-boundary case discovered below.

## Collected findings

- Correctness/domain review: CHANGES-REQUESTED. Reproduced exit-0 bypasses:
  nested comments and `//`-prefixed writes; global aliases inside expressions or
  trailing ORDER BY; ALTER/DROP of an admitted MV; source schema alteration before
  alias resolution; table-function INSERT, WITH-prefixed INSERT and DETACH; a leading
  BOM skipping the first declaration. A quoted `opt-in` Nullable column was silently
  omitted. Reject unsupported statements and declarations rather than losing their
  effects. No checked declaration is unavailable proof. Add focused regressions for
  every reproduction group and preserve the existing valid and broken controls.
- Instruction review: CHANGES-REQUESTED. Ref20 section 3 still applies the five-column
  cap and prefix workload condition to physical aggregate ORDER BY. This conflicts
  with preserving all merge dimensions. Ref80 also overstates typed-parameter grammar.
- Security review: BLOCK. Valid alternate CREATE DEFINER materialized-view syntax
  can hide a second writer. ALTER by view name can replace an admitted writer without
  scrutiny. Nested comments can supply a phantom writer. Each reproduced exit 0.
  Low-severity fixture hardening: record the owned container before launch and handle
  SIGTERM so a wrapper timeout does not bypass cleanup; retain a recovery procedure
  for uncatchable termination.
- Migration review: SAFE-WITH-CONDITIONS. Correct the conflicting key-width rule and
  stale ref50 exception router. A lossy rollup must be recomputed from trustworthy
  pre-aggregation history with proved coverage. Copying the damaged rollup and comparing
  it to itself is not parity. Missing historical coverage or per-type discrepancies
  block cutover. Effective compatibility can change the 26.7+ guard default. Upgrading
  or switching back cannot reconstruct lost dimensions.

The parent accepts these findings. Completeness review cannot justify skipping SQL
that is present in the supplied bundle. Ref50's directly related router is admitted
to the repair scope. No WA schema change or migration is authorized here.
The collected batch was returned to the original checker implementer. This is the
first checker repair cycle, separate from the completed domain-upgrade repair cycle.

## Primary evidence cited by reviewers

- [ClickHouse 24.8 lexer](https://github.com/ClickHouse/ClickHouse/blob/v24.8.14.39-lts/src/Parsers/Lexer.cpp#L310)
- [ClickHouse 24.8 CREATE parser](https://github.com/ClickHouse/ClickHouse/blob/v24.8.14.39-lts/src/Parsers/ParserCreateQuery.cpp#L1400)
- [ALTER VIEW](https://clickhouse.com/docs/reference/statements/alter/view)
- [ALTER ORDER BY](https://clickhouse.com/docs/reference/statements/alter/order-by)
- [SQL syntax and aliases](https://clickhouse.com/docs/reference/syntax)
- [26.7 aggregate-dimension guard](https://github.com/ClickHouse/ClickHouse/pull/108087)

Observers: `checker_review` requested gpt-6.1-sol/high; `upgrade_instruction`,
`upgrade_security`, and `checker_migration` requested gpt-6.1-sol/medium.
All configured roles are model-neutral; observed serving identities are unknown.
Review mandates are read-only within a workspace-write sandbox.

## First repair review

Candidate: `8359b7b9`. Independent verification passed 17 CLI tests, both negative
controls, the unchanged 24.8 merge oracle and a SIGTERM cancellation probe. The probe
observed child exit 143 and absence of the exact named container. WA retained 32 findings
and now reports four proof gaps: two source ALTER statements and two alias bindings.

Instruction review: APPROVED-WITH-NITS. Clarify that wider-index design justification
does not clear CH006. Migration review: SAFE for source delivery, with a wording nit
about the narrow metadata-only ORDER BY alteration supported for newly added columns.
The existing WA discriminator still requires the documented recovery path.

Correctness review: CHANGES-REQUESTED. Security review: BLOCK. Remaining reproduced
false-clean cases are a quoted aggregate engine, compound PARALLEL WITH statements,
forwarding through a Buffer table, unrecognized Unicode alias quotes, and duplicate
materialized-view names or table/view collisions suppressed by IF NOT EXISTS.
These present-bundle cases invalidate mechanical proof; external completeness review
does not excuse them. Cancellation during Docker creation remains untested, distinct
from the passed cancellation after readiness and the recorded manual recovery address.

The parent dispatched one collected second repair batch to the original implementer.
This is the final permitted checker repair cycle. Failed mandatory review after this
cycle blocks closure; neither thresholds nor proof requirements may be weakened.

## Second repair review

Candidate: `0f8348f2`. Independent verification passed 23 CLI cases, six focused
selectors and both broken controls. The untouched-WA output remained byte-identical:
exit 2, 32 findings and four proof gaps. The physical-merge runner is unchanged from
the independent 24.8 run. A fresh cancellation probe recorded its own SHA256, child
exit 143 and absence of the exact named container.

Instruction review: APPROVED. Security review initially passed its inspected cases.
Correctness review: CHANGES-REQUESTED, major. CREATE_TABLE.finditer scans inside an
unsupported quoted table name, invents a raw table and skips the real aggregate.
The parent reproduced exit 0 instead of CH011/exit 2. Exact fixture, invocation,
source identity and output are in `alaa-dgp8/blocked-quoted-name-result.json` and
its adjacent SQL/output files. This observed counterexample blocks acceptance;
the earlier passing checks do not cover it.

Both permitted checker repair cycles are consumed. Source writes stopped and the
parent requested explicit authority for one additional bounded repair/review cycle.
No WA2 blocker is claimed removed while this finding remains.

The user subsequently authorized exactly one additional bounded cycle for this
finding, its regression, independent retesting and review. The original actor resumes
the same issue. This grants no broader SQL feature work or external action.

## Authorized additional cycle: final source verdict

Candidate: `c8681fe3`. The two-file change anchors CREATE TABLE recognition to the
real statement head and adds a discriminating CLI regression. The exact historical
counterexample now produces CH011 and exit 2. A mixed bundle still checks the genuine
table and preserves its structural findings. Valid quoted declarations pass.

- Correctness/domain: APPROVED, `checker_review`, requested gpt-6.1-sol/high.
- Security: PASS, `upgrade_security`, requested gpt-6.1-sol/medium; original
  counterexample and positive/mixed controls replayed independently.
- Instruction: APPROVED at `0f8348f2`; instruction files are unchanged in `c8681fe3`.
- Migration: SAFE at `0f8348f2`; migration guidance is unchanged in `c8681fe3`.
- Independent verification: PASS, `upgrade_verify`, requested gpt-6.1-sol/medium.
  All 24 CLI cases passed. Both original mutants failed the intended assertions.
  The untouched WA audit retained exit 2, 32 findings and four CH011 proof gaps.
  Exact commands and manifests: `checker-verification/cycle3/`.

The merge runner and cancellation probe match their independently tested identities.
Reuse the cycle1 real 24.8 merge evidence and cycle2 fresh cancellation evidence;
neither was rerun merely because unrelated checker code changed.
Current 26.x runtime, cancellation during container creation, abrupt uncatchable
termination, deployed writer coverage and WA acceptance remain unproved.
No mandatory review finding remains for the bounded source delivery. Documentation
and final repository gates are separate completion requirements.
