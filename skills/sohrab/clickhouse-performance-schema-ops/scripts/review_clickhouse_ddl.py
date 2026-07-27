#!/usr/bin/env python3
"""Review ClickHouse CREATE TABLE statements against this skill's stated rules.

The checker is lexical. It strips SQL comments while preserving offsets, splits
the file into statements, and parses the column list, ENGINE, PARTITION BY,
ORDER BY, and PRIMARY KEY of every CREATE TABLE it finds. It never connects to a
server and never executes anything.

It checks the mechanical half of references/20-table-design.md: tenant-first
ordering, partition-key cardinality, Nullable columns that a typed default would
replace, sort keys that are longer than they can use, high-cardinality tails that
cannot prune, references to undeclared columns, and a PRIMARY KEY that is not a
prefix of ORDER BY. What it cannot check is printed at the end of every run, so a
clean result is a floor and not a pass.
"""

import argparse
import os
import re
import sys
import tempfile

VERSION = "1.0.0"

DEFAULT_TENANT_COLUMNS = (
    "project_id",
    "tenant_id",
    "org_id",
    "organization_id",
    "account_id",
    "workspace_id",
    "customer_id",
)

# Partition expressions that keep the distinct-partition count inside the range
# the official partitioning guidance calls usually optimal (fewer than 100-1,000).
COARSE_PARTITION_FUNCTIONS = (
    "toyyyymm",
    "tostartofmonth",
    "tostartofquarter",
    "tostartofyear",
    "toyear",
    "toquarter",
    "tomonday",
    "tostartofweek",
)

# Partition expressions finer than monthly. Legal, but the distinct count has to
# be computed against the retention window before it is accepted.
FINE_PARTITION_FUNCTIONS = (
    "toyyyymmdd",
    "todate",
    "tostartofday",
    "tostartofhour",
    "tostartofminute",
    "todatetime",
)

IDENTIFIER_TAIL = re.compile(r"(^|_)(id|uuid|ulid|guid|key|hash|token)$", re.I)

CLAUSE_KEYWORDS = (
    "ENGINE",
    "PARTITION BY",
    "PRIMARY KEY",
    "ORDER BY",
    "SAMPLE BY",
    "TTL",
    "SETTINGS",
    "AS SELECT",
    "COMMENT",
)


class Finding(object):
    def __init__(self, code, path, line, table, summary, obligation):
        self.code = code
        self.path = path
        self.line = line
        self.table = table
        self.summary = summary
        self.obligation = obligation

    def render(self):
        return "{0}:{1}: {2} [{3}] {4}\n    -> {5}".format(
            self.path, self.line, self.code, self.table, self.summary, self.obligation
        )


# --------------------------------------------------------------------------
# Lexical scrubbing and offset helpers
# --------------------------------------------------------------------------


def scrub(sql):
    """Replace comments and string-literal bodies with spaces, keeping offsets.

    Offsets and line numbers in the returned text are valid positions in the
    input text, so a match position can be reported against the original file.
    """
    out = list(sql)
    i = 0
    n = len(sql)

    def blank(start, end):
        for k in range(start, min(end, n)):
            if out[k] != "\n":
                out[k] = " "

    while i < n:
        ch = sql[i]
        if ch == "-" and sql.startswith("--", i):
            j = sql.find("\n", i)
            j = n if j == -1 else j
            blank(i, j)
            i = j
            continue
        if ch == "/" and sql.startswith("/*", i):
            j = sql.find("*/", i + 2)
            j = n if j == -1 else j + 2
            blank(i, j)
            i = j
            continue
        if ch == "'":
            j = i + 1
            while j < n:
                if sql[j] == "\\":
                    j += 2
                    continue
                if sql[j] == "'":
                    j += 1
                    break
                j += 1
            blank(i + 1, j - 1)
            i = j
            continue
        i += 1
    return "".join(out)


def line_of(text, offset):
    return text.count("\n", 0, offset) + 1


def match_paren(text, open_index):
    """Return the index just past the parenthesis that closes text[open_index]."""
    depth = 0
    for i in range(open_index, len(text)):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return i + 1
    return -1


def split_top_level(text):
    """Split on commas that are not inside parentheses."""
    parts = []
    depth = 0
    current = []
    for ch in text:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(current))
            current = []
            continue
        current.append(ch)
    if "".join(current).strip():
        parts.append("".join(current))
    return [p.strip() for p in parts if p.strip()]


def identifiers_in(expression):
    """Bare identifiers in an expression, excluding function names."""
    names = []
    for match in re.finditer(r"[A-Za-z_][A-Za-z_0-9]*", expression):
        end = match.end()
        rest = expression[end:]
        if rest.lstrip().startswith("("):
            continue
        names.append(match.group(0))
    return names


# --------------------------------------------------------------------------
# Statement parsing
# --------------------------------------------------------------------------


class Table(object):
    def __init__(self, name, offset):
        self.name = name
        self.offset = offset
        self.columns = []          # list of (name, type_text, offset)
        self.engine = ""
        self.engine_offset = offset
        self.partition_by = ""
        self.partition_offset = offset
        self.order_by = []         # list of expression strings
        self.order_offset = offset
        self.primary_key = []
        self.primary_offset = offset

    def column_names(self):
        return [c[0] for c in self.columns]


CREATE_TABLE = re.compile(
    r"\bCREATE\s+(?:OR\s+REPLACE\s+)?(?:TEMPORARY\s+)?TABLE\s+"
    r"(?:IF\s+NOT\s+EXISTS\s+)?([`\"]?[A-Za-z_][A-Za-z_0-9]*[`\"]?"
    r"(?:\s*\.\s*[`\"]?[A-Za-z_][A-Za-z_0-9]*[`\"]?)?)",
    re.I,
)


def parse_tables(scrubbed):
    tables = []
    for match in CREATE_TABLE.finditer(scrubbed):
        name = re.sub(r"[`\"\s]", "", match.group(1))
        table = Table(name, match.start())
        open_index = scrubbed.find("(", match.end())
        if open_index == -1:
            continue
        close_index = match_paren(scrubbed, open_index)
        if close_index == -1:
            continue
        body = scrubbed[open_index + 1:close_index - 1]
        base = open_index + 1
        cursor = 0
        for item in split_top_level(body):
            item_at = body.find(item, cursor)
            cursor = item_at + len(item) if item_at >= 0 else cursor
            head = item.strip()
            if re.match(r"^(INDEX|PROJECTION|CONSTRAINT|PRIMARY\s+KEY)\b", head, re.I):
                continue
            column = re.match(r"^[`\"]?([A-Za-z_][A-Za-z_0-9]*)[`\"]?\s+(.*)$", head, re.S)
            if not column:
                continue
            table.columns.append(
                (column.group(1), column.group(2).strip(), base + max(item_at, 0))
            )
        tail_end = scrubbed.find(";", close_index)
        tail_end = len(scrubbed) if tail_end == -1 else tail_end
        tail = scrubbed[close_index:tail_end]
        parse_clauses(table, tail, close_index)
        tables.append(table)
    return tables


def clause_text(tail, keyword):
    """Text of one trailing clause, and its offset within tail."""
    match = re.search(r"\b" + keyword.replace(" ", r"\s+") + r"\b", tail, re.I)
    if not match:
        return None, -1
    start = match.end()
    end = len(tail)
    for other in CLAUSE_KEYWORDS:
        if other == keyword:
            continue
        following = re.search(r"\b" + other.replace(" ", r"\s+") + r"\b", tail[start:], re.I)
        if following:
            end = min(end, start + following.start())
    return tail[start:end].strip(), match.start()


def tuple_elements(text):
    text = text.strip()
    if text.startswith("("):
        close = match_paren(text, 0)
        if close != -1:
            return split_top_level(text[1:close - 1])
    return [text] if text else []


def parse_clauses(table, tail, tail_base):
    engine, at = clause_text(tail, "ENGINE")
    if engine is not None:
        table.engine = engine.lstrip("=").strip()
        table.engine_offset = tail_base + at
    partition, at = clause_text(tail, "PARTITION BY")
    if partition is not None:
        table.partition_by = partition
        table.partition_offset = tail_base + at
    order, at = clause_text(tail, "ORDER BY")
    if order is not None:
        table.order_by = tuple_elements(order)
        table.order_offset = tail_base + at
    primary, at = clause_text(tail, "PRIMARY KEY")
    if primary is not None:
        table.primary_key = tuple_elements(primary)
        table.primary_offset = tail_base + at


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------


def justification_comment(original, offset):
    """True when the column's own line, or the line above it, records a reason.

    The rule in references/20-table-design.md is that a Nullable column names the
    query that needs the null. The checker clears the finding only when the text
    'nullable:' appears in a comment on that line or the line before it, because
    a reason that is not written down cannot be reviewed.
    """
    line_index = original.count("\n", 0, offset)
    lines = original.split("\n")
    window = lines[max(0, line_index - 1):line_index + 1]
    return any("nullable:" in line.lower() for line in window)


def is_nullable(type_text):
    return re.match(r"^\s*Nullable\s*\(", type_text, re.I) is not None


def nullable_inner(type_text):
    match = re.match(r"^\s*Nullable\s*\(\s*([A-Za-z_][A-Za-z_0-9]*)", type_text, re.I)
    return match.group(1) if match else "T"


def replacement_for(inner):
    lowered = inner.lower()
    if lowered == "string":
        return "LowCardinality(String) DEFAULT '' for a repeated dimension, or String DEFAULT ''"
    if lowered.startswith("float") or lowered.startswith("decimal"):
        return "{0} DEFAULT 0".format(inner)
    if lowered.startswith("uint") or lowered.startswith("int"):
        return "{0} DEFAULT 0".format(inner)
    if lowered.startswith("date") or lowered.startswith("datetime"):
        return "{0} with an explicit sentinel the readers agree on".format(inner)
    return "{0} DEFAULT <the empty value>".format(inner)


def check_table(path, original, scrubbed, table, tenant_columns, single_tenant):
    findings = []
    declared = set(name.lower() for name in table.column_names())
    order_names = [identifiers_in(e) for e in table.order_by]
    order_first = [names[0].lower() if names else "" for names in order_names]

    # CH001 / CH002 -- tenancy
    present = [c for c in table.column_names() if c.lower() in tenant_columns]
    if present:
        if not table.order_by:
            findings.append(Finding(
                "CH001", path, line_of(original, table.offset), table.name,
                "table has tenant column '{0}' but no ORDER BY".format(present[0]),
                "Give the table an ORDER BY whose first element is the tenant column, "
                "or every tenant query reads every tenant's rows."))
        elif order_first[0] not in tenant_columns:
            findings.append(Finding(
                "CH001", path, line_of(original, table.order_offset), table.name,
                "ORDER BY starts with '{0}', not the tenant column '{1}'".format(
                    table.order_by[0], present[0]),
                "Move '{0}' to the first position in ORDER BY, because the sparse index "
                "prunes on a prefix and a query filtered only by tenant prunes nothing "
                "today.".format(present[0])))
    elif not single_tenant:
        findings.append(Finding(
            "CH002", path, line_of(original, table.offset), table.name,
            "no tenant column found (looked for: {0})".format(", ".join(sorted(tenant_columns))),
            "Add the tenant column and put it first in ORDER BY. If this table really "
            "holds one tenant's rows only, re-run with --single-tenant so the assertion "
            "is recorded in the command line rather than assumed."))

    # CH003 / CH004 -- partition key cardinality
    if table.partition_by:
        expression = table.partition_by.strip()
        functions = [f.lower() for f in re.findall(r"([A-Za-z_][A-Za-z_0-9]*)\s*\(", expression)]
        bare = not functions and expression.lower() not in ("tuple()", "")
        if bare or any(
            f not in COARSE_PARTITION_FUNCTIONS and f not in FINE_PARTITION_FUNCTIONS
            for f in functions
        ):
            findings.append(Finding(
                "CH003", path, line_of(original, table.partition_offset), table.name,
                "PARTITION BY {0} has no bounded distinct count".format(expression),
                "Partition on a coarse time bucket such as toYYYYMM(<date column>) and let "
                "ORDER BY do the pruning. Parts are never merged across partitions, so an "
                "unbounded key accumulates unmergeable parts until inserts fail."))
        elif any(f in FINE_PARTITION_FUNCTIONS for f in functions):
            findings.append(Finding(
                "CH004", path, line_of(original, table.partition_offset), table.name,
                "PARTITION BY {0} is finer than monthly".format(expression),
                "State the retention window and show that window divided by this "
                "granularity stays under 1,000 partitions, or move to toYYYYMM."))

    # CH005 -- Nullable columns with no recorded reason
    for name, type_text, offset in table.columns:
        if is_nullable(type_text) and not justification_comment(original, offset):
            inner = nullable_inner(type_text)
            findings.append(Finding(
                "CH005", path, line_of(original, offset), table.name,
                "column '{0}' is Nullable({1}) with no recorded reason".format(name, inner),
                "Replace with {0}, or write a comment on that line starting 'nullable:' "
                "naming the query that must tell an absent value from an empty one. A "
                "Nullable column carries a separate UInt8 column processed on every "
                "access.".format(replacement_for(inner))))

    # CH006 -- sort key longer than it can use
    if len(table.order_by) > 5:
        findings.append(Finding(
            "CH006", path, line_of(original, table.order_offset), table.name,
            "ORDER BY has {0} elements".format(len(table.order_by)),
            "Cut to five or fewer, or name for each element past the fifth a real query "
            "that filters on it and on every element before it. Official guidance is that "
            "4-5 keys are typically sufficient."))

    # CH007 -- high-cardinality tail
    tail = []
    for position, names in enumerate(order_names[2:], start=3):
        head = names[0] if names else ""
        if head and IDENTIFIER_TAIL.search(head):
            tail.append((position, head))
    if tail:
        listed = ", ".join("{0} (position {1})".format(n, p) for p, n in tail)
        findings.append(Finding(
            "CH007", path, line_of(original, table.order_offset), table.name,
            "identifier-like columns in the ORDER BY tail: {0}".format(listed),
            "Each one prunes only for a query that already constrains every element to "
            "its left; otherwise it is write cost and index memory. Drop it, or serve "
            "the identifier-first access path with a projection or a rollup."))

    # CH008 -- keys referencing undeclared columns
    for label, expressions, offset in (
        ("ORDER BY", table.order_by, table.order_offset),
        ("PARTITION BY", [table.partition_by] if table.partition_by else [], table.partition_offset),
        ("PRIMARY KEY", table.primary_key, table.primary_offset),
    ):
        for expression in expressions:
            for name in identifiers_in(expression):
                if name.lower() in declared:
                    continue
                if re.match(r"^\d", name) or name.lower() in ("tuple",):
                    continue
                findings.append(Finding(
                    "CH008", path, line_of(original, offset), table.name,
                    "{0} references '{1}', which the table does not declare".format(label, name),
                    "Declare the column or correct the name. ClickHouse rejects this at "
                    "CREATE time, so the DDL cannot be applied as written."))

    # CH009 -- PRIMARY KEY must be a prefix of ORDER BY
    if table.primary_key and table.order_by:
        normal_pk = [re.sub(r"\s+", "", e).lower() for e in table.primary_key]
        normal_ob = [re.sub(r"\s+", "", e).lower() for e in table.order_by]
        if normal_ob[:len(normal_pk)] != normal_pk:
            findings.append(Finding(
                "CH009", path, line_of(original, table.primary_offset), table.name,
                "PRIMARY KEY is not a prefix of ORDER BY",
                "Make PRIMARY KEY a leading prefix of ORDER BY, or drop it and let it "
                "default to ORDER BY. ClickHouse rejects a non-prefix primary key."))

    return findings


def check_source(path, sql, tenant_columns, single_tenant):
    scrubbed = scrub(sql)
    findings = []
    tables = parse_tables(scrubbed)
    for table in tables:
        findings.extend(
            check_table(path, sql, scrubbed, table, tenant_columns, single_tenant)
        )
    return tables, findings


# --------------------------------------------------------------------------
# Self-test fixtures
# --------------------------------------------------------------------------

BAD_FIXTURE = """
CREATE TABLE analytics.events
(
    ts DateTime64(3),
    event_date Date DEFAULT toDate(ts),
    user_id UInt64,
    session_locale Nullable(String),
    retries Nullable(UInt32),
    service LowCardinality(String),
    event_type LowCardinality(String),
    content_id String,
    set_id String,
    play_id String,
    event_id String
)
ENGINE = MergeTree
PARTITION BY user_id
PRIMARY KEY (event_type, ts)
ORDER BY (ts, event_type, content_id, set_id, play_id, event_id, missing_column)
SETTINGS index_granularity = 8192;
"""

GOOD_FIXTURE = """
CREATE TABLE IF NOT EXISTS analytics.events_rollup
(
    project_id String DEFAULT '',
    event_date Date,
    event_type LowCardinality(String) DEFAULT '',
    -- nullable: completion_rate_report must tell 'never reported' from 'reported 0'
    completion_ratio Nullable(Float32),
    hits UInt64 DEFAULT 0
)
ENGINE = SummingMergeTree
PARTITION BY toYYYYMM(event_date)
ORDER BY (project_id, event_date, event_type)
SETTINGS index_granularity = 8192;
"""


def self_test():
    tenant = set(DEFAULT_TENANT_COLUMNS)
    cases = []

    _, bad = check_source("<bad-fixture>", BAD_FIXTURE, tenant, False)
    codes = [f.code for f in bad]
    for expected in ("CH002", "CH003", "CH005", "CH006", "CH007", "CH008", "CH009"):
        cases.append(("bad fixture reports " + expected, expected in codes))
    cases.append(("bad fixture reports both unjustified Nullable columns",
                  codes.count("CH005") == 2))

    _, good = check_source("<good-fixture>", GOOD_FIXTURE, tenant, False)
    cases.append(("good fixture reports nothing", good == []))

    _, single = check_source("<bad-fixture>", BAD_FIXTURE, tenant, True)
    cases.append(("--single-tenant clears CH002 only",
                  "CH002" not in [f.code for f in single] and len(single) == len(bad) - 1))

    tenant_last = """
CREATE TABLE t (project_id String, event_date Date, hits UInt64)
ENGINE = MergeTree PARTITION BY toYYYYMM(event_date)
ORDER BY (event_date, project_id);
"""
    _, misordered = check_source("<order-fixture>", tenant_last, tenant, False)
    cases.append(("tenant column not first reports CH001",
                  "CH001" in [f.code for f in misordered]))

    fine = """
CREATE TABLE t (project_id String, event_date Date)
ENGINE = MergeTree PARTITION BY toYYYYMMDD(event_date)
ORDER BY (project_id, event_date);
"""
    _, daily = check_source("<fine-fixture>", fine, tenant, False)
    cases.append(("daily partitioning reports CH004", "CH004" in [f.code for f in daily]))

    scrubbed = scrub("SELECT 'Nullable(String)' -- Nullable(String)\nNullable(String)\n")
    cases.append(("comments and string bodies are ignored",
                  scrubbed.count("Nullable(String)") == 1))
    cases.append(("scrubbing preserves length", len(scrubbed) == len(
        "SELECT 'Nullable(String)' -- Nullable(String)\nNullable(String)\n")))

    cases.append(("top-level split respects nested parens",
                  split_top_level("a DateTime64(3, 'UTC'), b String") == [
                      "a DateTime64(3, 'UTC')", "b String"]))
    cases.append(("function names are not read as columns",
                  identifiers_in("toYYYYMM(event_date)") == ["event_date"]))

    failed = [name for name, ok in cases if not ok]
    for name, ok in cases:
        print("{0} {1}".format("ok  " if ok else "FAIL", name))
    print("")
    print("{0} of {1} self-test cases passed".format(len(cases) - len(failed), len(cases)))
    return 0 if not failed else 3


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

CANNOT_CHECK = """\
not checked by this tool, and still your responsibility:
  - whether the ORDER BY prefix matches the queries that will actually run
  - whether a LowCardinality column really holds under ~10,000 distinct values
  - whether the retention window times the partition granularity stays bounded
  - whether the engine's deduplication model matches what readers assume
  - whether the tenant predicate is present in every query against this table
  - whether the deployed table still matches this file (compare system.columns)
"""

EPILOG = """\
exit codes:
  0  no finding. The DDL clears the mechanical rules; the unchecked list below
     is still open and must be answered in the change request.
  1  at least one finding. Fix every finding or record the justification the
     finding names, then run this checker again; do not apply the DDL while any
     finding stands.
  2  a path could not be read, or the arguments were wrong. Correct the
     invocation and rerun; no file was checked and no result should be quoted.
  3  --self-test failed, so the checker itself is untrustworthy. Report the
     failing case, and review the DDL by hand against
     references/20-table-design.md until the checker passes.

checks:
  CH001  a tenant column exists but does not lead ORDER BY
  CH002  no tenant column found, and --single-tenant was not given
  CH003  PARTITION BY has no bounded distinct count
  CH004  PARTITION BY is finer than monthly
  CH005  a Nullable column with no 'nullable:' comment naming the query that
         needs the null
  CH006  ORDER BY has more than five elements
  CH007  identifier-like columns in the ORDER BY tail, which cannot prune
  CH008  ORDER BY, PARTITION BY, or PRIMARY KEY names an undeclared column
  CH009  PRIMARY KEY is not a prefix of ORDER BY

CH002 and CH005 are cleared by recording an assertion, not by deleting the
check: CH002 by passing --single-tenant, CH005 by writing the reason on the
column's line. Both leave the claim where a reviewer can read it.
"""


def main(argv):
    parser = argparse.ArgumentParser(
        prog="review_clickhouse_ddl.py",
        description="Review ClickHouse CREATE TABLE statements against this skill's rules.",
        epilog=EPILOG + "\n" + CANNOT_CHECK,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("paths", nargs="*", help="SQL files containing CREATE TABLE statements")
    parser.add_argument(
        "--tenant-column",
        action="append",
        default=[],
        metavar="NAME",
        help="treat NAME as a tenant column (repeatable; adds to the built-in list)",
    )
    parser.add_argument(
        "--single-tenant",
        action="store_true",
        help="assert these tables hold one tenant's rows only, which clears CH002",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run the checker against its own fixtures and exit",
    )
    parser.add_argument("--version", action="version", version=VERSION)
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    if not args.paths:
        parser.print_usage(sys.stderr)
        sys.stderr.write("error: give at least one SQL file, or --self-test\n")
        return 2

    tenant_columns = set(DEFAULT_TENANT_COLUMNS)
    tenant_columns.update(name.lower() for name in args.tenant_column)

    all_findings = []
    table_count = 0
    for path in args.paths:
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as handle:
                sql = handle.read()
        except OSError as exc:
            sys.stderr.write("error: {0}\n".format(exc))
            return 2
        tables, findings = check_source(path, sql, tenant_columns, args.single_tenant)
        table_count += len(tables)
        all_findings.extend(findings)

    for finding in all_findings:
        print(finding.render())

    print("")
    print("{0} file(s), {1} table(s) checked, {2} finding(s)".format(
        len(args.paths), table_count, len(all_findings)))
    print("")
    sys.stdout.write(CANNOT_CHECK)
    return 1 if all_findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
