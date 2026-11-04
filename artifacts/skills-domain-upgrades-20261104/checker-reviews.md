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
