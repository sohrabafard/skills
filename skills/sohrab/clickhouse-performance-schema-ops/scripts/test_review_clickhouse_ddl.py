"""CLI regressions for merge identity, sparse-index evidence and retained DDL checks."""

from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

CHECKER = Path(__file__).with_name("review_clickhouse_ddl.py")
SOURCE = """CREATE TABLE raw.events (
  tenant_id UInt32, timestamp DateTime, object_id UInt64, object_type String,
  region UInt32, zone UInt32, campus UInt32, value UInt64
) ENGINE MergeTree ORDER BY tenant_id;
"""
ORDER = "tenant_id, day, object_id, object_type, region, zone, campus"
READ = """SELECT sum(amount) AS total FROM agg.rollup
WHERE tenant_id = {tenant:UInt32} AND day >= '2024-08-01';"""


def ddl(order=ORDER, primary="tenant_id, day", engine="AggregatingMergeTree"):
    index = f"PRIMARY KEY ({primary})" if primary is not None else ""
    return f"""CREATE TABLE agg.rollup (
  tenant_id UInt32, day Date, object_id UInt64, object_type String,
  region UInt32, zone UInt32, campus UInt32, amount SimpleAggregateFunction(sum, UInt64)
) ENGINE = {engine}
ORDER BY ({order})
{index};
"""


def writer(group=ORDER, target="agg.rollup", name="mv"):
    projection = ORDER.replace("day", "toDate(timestamp) AS day") + ", sum(value) AS amount"
    return f"""CREATE MATERIALIZED VIEW agg.{name} TO {target}
AS SELECT {projection}
FROM raw.events
GROUP BY {group};
"""


class ReviewClickHouseDDL(unittest.TestCase):
    def audit(self, bundle, reads=(), extra_ddl=None):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "bundle.sql").write_text(bundle, encoding="utf-8")
            command = [sys.executable, "-B", str(CHECKER), "bundle.sql"]
            if extra_ddl is not None:
                (root / "extra.sql").write_text(extra_ddl, encoding="utf-8")
                command.append("extra.sql")
            for index, contents in enumerate(reads):
                path = f"read{index}.sql"
                (root / path).write_text(contents, encoding="utf-8")
                command.extend(("--read-query", path))
            return subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=10)

    def assert_audit(self, result, code, findings=(), problems=()):
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, code, output)
        actual = re.findall(r"^.+:\d+: (CH\d+) \[([^\]]+)\]", result.stdout, re.M)
        self.assertCountEqual(actual, findings, output)
        actual = re.findall(r"^(.+:\d+): CH011 (.+)$", result.stderr, re.M)
        self.assertCountEqual(actual, problems, output)

    def test_aggregate_valid_prefix_plain_and_replicated(self):
        for engine in ("AggregatingMergeTree", "ReplicatedAggregatingMergeTree('/tmp/path','replica')"):
            with self.subTest(engine=engine):
                quoted = ddl(engine=engine).replace("agg.rollup", '"agg".`rollup`')
                quoted = quoted.replace("ORDER BY (tenant_id", "oRdEr\n  bY (`tenant_id`")
                result = self.audit("-- ignored; INSERT INTO agg.rollup VALUES (1)\n" + writer(),
                                    ("SELECT * FROM raw.events WHERE tenant_id = 1;", READ),
                                    extra_ddl=SOURCE + quoted)
                self.assert_audit(result, 0)
                self.assertIn("sparse PRIMARY KEY predicate evidence for [agg.rollup] at read1.sql:1", result.stdout)

    def test_aggregate_missing_dimension_with_qualifying_prefix(self):
        broken = ddl(order=ORDER.replace("object_type, ", ""))
        result = self.audit(SOURCE + broken + writer(), (READ,))
        self.assert_audit(result, 1, (("CH010", "agg.rollup"),))
        self.assertIn("ORDER BY omits writer GROUP BY dimension(s): object_type", result.stdout)

    def test_aggregate_effective_index_implicit_and_long_explicit(self):
        for primary in (None, ORDER.rsplit(", ", 1)[0]):
            with self.subTest(primary=primary):
                reads = ()
                if primary is not None:
                    reads = (READ.replace(
                        "day >= '2024-08-01';",
                        "day = '2024-08-01' AND object_id = 1 AND object_type = 'A' AND region = 2 AND zone = 3;"),)
                result = self.audit(SOURCE + ddl(primary=primary) + writer(), reads)
                self.assert_audit(result, 1, (("CH006", "agg.rollup"), ("CH007", "agg.rollup")))
                self.assertIn("effective PRIMARY KEY", result.stdout)

    def test_aggregate_effective_index_nonprefix_and_unjustified_short(self):
        self.assert_audit(self.audit(SOURCE + ddl(primary="day, tenant_id") + writer(), (READ,)),
                          1, (("CH009", "agg.rollup"),))
        self.assert_audit(self.audit(SOURCE + ddl() + writer()), 2, problems=(
            ("bundle.sql:5", "agg.rollup: short PRIMARY KEY has no qualifying --read-query"),))

    def test_aggregate_proof_refusal_wrong_or_ambiguous_read(self):
        gap = ("bundle.sql:5", "agg.rollup: short PRIMARY KEY has no qualifying --read-query")
        cases = (
            ("SELECT * FROM raw.events WHERE tenant_id = 1;", None),
            (READ.replace("tenant_id =", "tenant_id >"), None),
            (READ.replace(" AND day", " OR day"),
             "expected AND-connected target column comparisons to literals or parameters"),
            (READ.replace("sum(amount) AS total", "'foo' AS tenant_id"),
             "read alias can shadow target column 'tenant_id'"),
            (READ.replace(";", " UNION ALL SELECT * FROM agg.rollup;"),
             "expected a single SELECT without nested queries"),
        )
        for query, problem in cases:
            with self.subTest(query=query):
                problems = (("read0.sql:1", problem), gap) if problem else (gap,)
                result = self.audit(SOURCE + ddl() + writer(), (query,))
                self.assert_audit(result, 2, problems=problems)
                self.assertNotIn("sparse PRIMARY KEY predicate evidence", result.stdout)

    def test_aggregate_proof_refusal_all_writers_and_structural_diagnostics(self):
        second = writer(group=ORDER.replace("object_type", "lower(object_type)"), name="mv2")
        bundle = SOURCE + ddl(order=ORDER.replace("object_type, ", "")) + writer() + second
        result = self.audit(bundle, (READ,))
        self.assert_audit(result, 2, (("CH010", "agg.rollup"),), (
            ("bundle.sql:15", "agg.rollup: GROUP BY must list distinct bare column names or SELECT AS aliases"),))
        self.assertIn("dimension(s): object_type", result.stdout)

    def test_aggregate_proof_refusal_preserves_unambiguous_dimensions_of_same_writer(self):
        source = SOURCE.replace("timestamp DateTime", "timestamp DateTime, day Date")
        bundle = source + ddl(order=ORDER.replace("object_type, ", "")) + writer()
        result = self.audit(bundle, (READ,))
        self.assert_audit(result, 2, (("CH010", "agg.rollup"),), (
            ("bundle.sql:11", "agg.rollup: GROUP BY alias 'day' has unresolved source binding"),))
        self.assertIn("dimension(s): object_type", result.stdout)

    def test_aggregate_proof_refusal_missing_writer_direct_write_or_unknown_target(self):
        for suffix, problem in (
            ("/* " + writer() + " */", ("bundle.sql:5", "agg.rollup: no analyzable materialized view writer")),
            (writer() + "INSERT INTO agg.rollup VALUES (1);",
             ("bundle.sql:15", "unsupported direct write or alteration of 'agg.rollup'")),
            (writer() + writer(target="agg.unknown", name="unknown"),
             ("bundle.sql:15", "materialized view target 'agg.unknown' is unresolved")),
        ):
            with self.subTest(problem=problem):
                self.assert_audit(self.audit(SOURCE + ddl() + suffix, (READ,)), 2, problems=(problem,))

    def test_aggregate_proof_refusal_wrapped_key_or_unresolved_group(self):
        bundle = SOURCE + ddl(order=ORDER.replace("object_type", "tuple(object_type)")) + writer()
        self.assert_audit(self.audit(bundle, (READ,)), 2, (("CH010", "agg.rollup"),), (
            ("bundle.sql:5", "agg.rollup: expected bare ORDER BY and PRIMARY KEY column lists"),))
        bundle = SOURCE + ddl() + writer(group=ORDER.replace("object_type", "kind"))
        self.assert_audit(self.audit(bundle, (READ,)), 2, problems=(
            ("bundle.sql:11", "agg.rollup: GROUP BY output 'kind' is unresolved in the target"),))

    def test_repair_nested_comments_cannot_supply_phantom_writer(self):
        bundle = SOURCE + ddl() + "/* outer /* inner */; " + writer() + " */;"
        self.assert_audit(self.audit(bundle, (READ,)), 2, problems=(
            ("bundle.sql:5", "agg.rollup: no analyzable materialized view writer"),))
        genuine = writer().replace("CREATE", "CREATE /* outer /* inner */ still outer */", 1)
        self.assert_audit(self.audit(SOURCE + ddl() + genuine, (READ,)), 0)

    def test_repair_slash_comment_cannot_hide_direct_write(self):
        bundle = SOURCE + ddl() + writer() + "// backfill\nINSERT INTO agg.rollup VALUES (1);"
        self.assert_audit(self.audit(bundle, (READ,)), 2, problems=(
            ("bundle.sql:16", "unsupported direct write or alteration of 'agg.rollup'"),))

    def test_repair_global_read_aliases_cannot_prove_predicates(self):
        bundle = SOURCE + ddl() + writer()
        aliases = (
            READ.replace("sum(amount) AS total", "toString(1 AS tenant_id) AS marker"),
            READ.replace(";", " ORDER BY (1 AS tenant_id);"),
        )
        for query in aliases:
            with self.subTest(query=query):
                self.assert_audit(self.audit(bundle, (query,)), 2, problems=(
                    ("read0.sql:1", "read alias can shadow target column 'tenant_id'"),
                    ("bundle.sql:5", "agg.rollup: short PRIMARY KEY has no qualifying --read-query"),
                ))

    def test_repair_mutation_of_writer_or_source_invalidates_bundle_proof(self):
        bundle = SOURCE + ddl() + writer()
        cases = (
            (bundle + "ALTER TABLE agg.mv MODIFY QUERY SELECT 1;", 15),
            (bundle + "DROP TABLE agg.mv;", 15),
            (SOURCE + ddl() + "ALTER TABLE raw.events ADD COLUMN day Date;\n" + writer(), 11),
        )
        for changed, line in cases:
            with self.subTest(changed=changed):
                self.assert_audit(self.audit(changed, (READ,)), 2, problems=(
                    (f"bundle.sql:{line}", "unsupported statement in aggregate bundle"),))

    def test_repair_unadmitted_statements_cannot_hide_writers(self):
        bundle = SOURCE + ddl() + writer()
        alternative_mv = writer(name="mv2").replace(
            "CREATE MATERIALIZED VIEW", "CREATE DEFINER = CURRENT_USER SQL SECURITY DEFINER MATERIALIZED VIEW")
        cases = (
            ("INSERT INTO TABLE FUNCTION remote('localhost','agg','rollup') VALUES (1);",
             "unsupported table-function INSERT in aggregate bundle"),
            ("WITH q AS (SELECT 1) INSERT INTO agg.rollup SELECT * FROM q;",
             "unsupported statement in aggregate bundle"),
            ("DETACH TABLE agg.rollup;", "unsupported statement in aggregate bundle"),
            (alternative_mv, "unsupported statement in aggregate bundle"),
        )
        for suffix, issue in cases:
            with self.subTest(suffix=suffix):
                self.assert_audit(self.audit(bundle + suffix, (READ,)), 2,
                                  problems=(("bundle.sql:15", issue),))
        self.assert_audit(self.audit(bundle + "INSERT INTO raw.events VALUES (1);", (READ,)), 0)

    def test_repair_bom_and_empty_ddl_cannot_drop_aggregate_target(self):
        broken = ddl(order=ORDER.replace("object_type, ", ""))
        self.assert_audit(self.audit("\ufeff" + broken + SOURCE + writer(), (READ,)),
                          1, (("CH010", "agg.rollup"),))
        self.assert_audit(self.audit("/* no table */"), 2, problems=(
            ("bundle.sql:1", "no table declaration was checked"),))

    def test_repair_unsupported_quoted_column_cannot_hide_nullable_proof_gap(self):
        ddl_sql = """CREATE TABLE raw.bad (
  tenant_id UInt32,
  `opt-in` Nullable(UInt8),
  another Nullable(UInt8)
) ENGINE MergeTree ORDER BY tenant_id;
"""
        self.assert_audit(self.audit(ddl_sql), 2, (("CH005", "raw.bad"),), (
            ("bundle.sql:3", "raw.bad: unsupported column declaration"),))

    def test_ddl_retained_guards(self):
        raw = """CREATE TABLE raw.bad (
  tenant_id UInt32, day Date, account_id UInt32, region UInt8, zone UInt8,
  object_id UInt64, flag Nullable(UInt8)
) ENGINE MergeTree
PARTITION BY object_id
ORDER BY (day, tenant_id, object_id, account_id, region, zone, unknown)
PRIMARY KEY (tenant_id);
"""
        findings = tuple((f"CH{i:03}", "raw.bad") for i in (1, 3, 5, 6, 7, 8, 9))
        self.assert_audit(self.audit(raw), 1, findings)
        self.assert_audit(self.audit(raw, ("/* unterminated",), extra_ddl="/* no DDL */"),
                          2, findings, (("read0.sql:1", "unsupported or unterminated SQL token"),))


if __name__ == "__main__":
    unittest.main()
