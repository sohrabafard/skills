#!/usr/bin/env python3
"""Check SigNoz ClickHouse SQL against the rules this skill states.

Every rule below is a rule the reference files assert in prose. Before this script existed they
were preferences: nothing reported a violation, so nothing enforced them, and the skill shipped
examples that broke its own rules. Run it over the skill (`--skill-dir`) to regression-test the
examples, or over a query you are about to hand over (`--sql`).

  S1  a bounded time predicate, using the signal's own variables
  S2  a ts_bucket_start predicate on a logs or traces record table
  S3  two signoz_* databases in one statement without an explicit JOIN ... ON
  S4  a resource subquery reached with GLOBAL IN, never a plain IN
  S5  a resource CTE present exactly when a resource attribute is filtered -- both directions
  S6  a raw metrics sample scan with neither a rollup nor a stated window bound
  S7  GROUP BY on a denylisted high-cardinality expression
  S8  a destructive or DDL statement against a vendor-owned table
  S9  the panel output shape, including a LIMIT on a table-shaped result
  S10 a credential-shaped literal
  S11 alert-destined SQL while the alert surface is not confirmed for this install

Exit codes:
  0  every statement passed
  1  at least one rule fired
  2  no input, an unreadable input, or a missing denylist file

Runs on Windows and POSIX: pure Python 3, no shell pipelines.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CLEAN = 0
FINDINGS = 1
BLOCKED = 2

SQL_BLOCK_RE = re.compile(r"^```sql\s*$")
FENCE_END_RE = re.compile(r"^```\s*$")

LOG_TABLES = ("distributed_logs_v2", "logs_v2")
TRACE_TABLES = ("distributed_signoz_index_v3", "signoz_index_v3")
METRIC_SAMPLE_TABLES = ("distributed_samples_v4", "samples_v4")
METRIC_SERIES_RE = re.compile(r"\btime_series_v4(_6hrs|_1day|_1week|_reduced\w*)?\b")
ROLLUP_RE = re.compile(r"samples_v4_agg_(5m|30m)\b")
RAW_SCAN_OK_RE = re.compile(r"--\s*raw-scan-ok:", re.I)

TIME_VARS = {
    "logs": ("$start_timestamp_nano", "$end_timestamp_nano"),
    "traces": ("$start_datetime", "$end_datetime"),
    "metrics": ("{{.start_timestamp_ms}}", "{{.end_timestamp_ms}}"),
}

DESTRUCTIVE = ("insert", "alter", "drop", "truncate", "optimize", "create", "system", "kill",
               "rename", "detach", "attach")

# Names, not a ceiling. The ceiling on distinct label values belongs to alaa-observability-soc
# references/30-quantitative-budgets.md and is deliberately not restated here.
# `fingerprint` is absent on purpose: grouping by it is required by the counter-rate pattern.
DEFAULT_DENYLIST = ["trace_id", "span_id", "user_id", "request_id", "http_url", "body",
                    "session_id", "email", "phone"]

CREDENTIAL_RE = re.compile(
    r"(password\s*=\s*['\"][^'\"]+['\"]|Bearer\s+[A-Za-z0-9._-]{10,}|AKIA[0-9A-Z]{12,}"
    r"|eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,})")


class Blocked(Exception):
    pass


def default_skill_dir() -> Path:
    return Path(sys.argv[0]).resolve().parent.parent


def extract_blocks(skill_dir: Path):
    """Yield (relative_path, first_line_number, sql_text) for every fenced sql block."""
    blocks = []
    for md in sorted(skill_dir.rglob("*.md")):
        rel = md.relative_to(skill_dir).as_posix()
        lines = md.read_text(encoding="utf-8").splitlines()
        index = 0
        while index < len(lines):
            if SQL_BLOCK_RE.match(lines[index]):
                start = index + 1
                body = []
                index += 1
                while index < len(lines) and not FENCE_END_RE.match(lines[index]):
                    body.append(lines[index])
                    index += 1
                blocks.append((rel, start + 1, "\n".join(body)))
            index += 1
    return blocks


def split_statements(text: str):
    """Split on ';' at paren depth zero, outside string literals, and outside comments.

    Comment awareness is not a nicety. A ';' inside a `--` comment used to split one query
    into two fragments that classify() then skipped, so the query was never checked and the
    run reported clean. A checker that silently drops its input is worse than a red one.
    """
    statements, current, depth, quote = [], [], 0, None
    line_comment, block_comment = False, False
    index, length = 0, len(text)
    while index < length:
        char = text[index]
        if line_comment:
            current.append(char)
            if char == "\n":
                line_comment = False
            index += 1
            continue
        if block_comment:
            current.append(char)
            if char == "*" and index + 1 < length and text[index + 1] == "/":
                current.append("/")
                index += 2
                block_comment = False
                continue
            index += 1
            continue
        if quote:
            current.append(char)
            if char == quote:
                quote = None
            index += 1
            continue
        if char == "-" and index + 1 < length and text[index + 1] == "-":
            line_comment = True
            current.append(char)
            index += 1
            continue
        if char == "/" and index + 1 < length and text[index + 1] == "*":
            block_comment = True
            current.append(char)
            index += 1
            continue
        if char in "'\"`":
            quote = char
            current.append(char)
            index += 1
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth = max(0, depth - 1)
        if char == ";" and depth == 0:
            statements.append("".join(current))
            current = []
            index += 1
            continue
        current.append(char)
        index += 1
    if "".join(current).strip():
        statements.append("".join(current))
    return [s for s in (st.strip() for st in statements) if s]


def strip_comments(sql: str) -> str:
    without_block = re.sub(r"/\*.*?\*/", " ", sql, flags=re.S)
    return re.sub(r"--[^\n]*", " ", without_block)


def classify(sql: str):
    """Return (kind, signal). kind is 'statement', 'fragment', or 'template'."""
    stripped = strip_comments(sql).strip()
    head = stripped.lstrip("(").lstrip().lower()
    if not head.startswith("with") and not head.startswith("select"):
        return "fragment", None
    if re.search(r"^\s*SELECT\s*\.\.\.\s*$", stripped, re.M) or re.search(r"FROM\s*\{\{", stripped):
        return "template", None
    if any(t in stripped for t in TRACE_TABLES) or "signoz_traces." in stripped:
        return "statement", "traces"
    if any(t in stripped for t in LOG_TABLES) or "signoz_logs." in stripped:
        return "statement", "logs"
    if "signoz_metrics." in stripped or "signoz_metadata." in stripped:
        return "statement", "metrics"
    return "template", None


def reads_data_table(sql: str, signal: str) -> bool:
    """True when the statement reads a record, span or sample table, as opposed to a
    catalog table such as distributed_metadata. Time bounds and panel shape apply only
    to the former: a metric-metadata lookup has no window and is not a panel."""
    if signal == "logs":
        return any(t in sql for t in LOG_TABLES)
    if signal == "traces":
        return any(t in sql for t in TRACE_TABLES)
    return bool(any(t in sql for t in METRIC_SAMPLE_TABLES) or METRIC_SERIES_RE.search(sql)
                or ROLLUP_RE.search(sql))


def aliases(sql: str):
    mapping = {}
    for expression, alias in re.findall(r"([`\w\.\[\]'\$\{\}\(\)]+)\s+AS\s+`?([\w\.]+)`?", sql, re.I):
        mapping.setdefault(alias, expression)
    return mapping


def group_by_terms(sql: str):
    terms = []
    for match in re.finditer(r"\bGROUP\s+BY\s+(.+?)(?=\bORDER\b|\bLIMIT\b|\bHAVING\b|\bWINDOW\b|\)|$)",
                             sql, re.I | re.S):
        for part in match.group(1).split(","):
            cleaned = part.strip().strip("`").strip()
            if cleaned:
                terms.append(cleaned)
    return terms


def output_columns(sql: str):
    """Top-level SELECT list aliases, best effort. Used only to classify the panel shape."""
    match = re.search(r"\bSELECT\b(?!.*\bSELECT\b)", sql, re.I | re.S)
    if not match:
        return []
    tail = sql[match.end():]
    from_match = re.search(r"\bFROM\b", tail, re.I)
    select_list = tail[: from_match.start()] if from_match else tail
    columns, depth, current = [], 0, []
    for char in select_list:
        if char == "(":
            depth += 1
        elif char == ")":
            depth = max(0, depth - 1)
        if char == "," and depth == 0:
            columns.append("".join(current))
            current = []
            continue
        current.append(char)
    columns.append("".join(current))
    names = []
    for column in columns:
        text = column.strip()
        if not text:
            continue
        alias = re.search(r"\bAS\s+`?([\w\.]+)`?\s*$", text, re.I)
        names.append(alias.group(1) if alias else text.strip("`"))
    return names


def panel_shape(sql: str):
    names = [n.lower() for n in output_columns(sql)]
    has_ts = bool(re.search(r"\bAS\s+ts\b", sql, re.I))
    has_value = bool(re.search(r"\bAS\s+value\b", sql, re.I))
    if has_ts and has_value:
        return "timeseries"
    if has_value and len(names) == 1:
        return "value"
    return "table"


def load_denylist(path):
    if path is None:
        return list(DEFAULT_DENYLIST)
    target = Path(path)
    if not target.is_file():
        raise Blocked("--cardinality-denylist not found: {}".format(target))
    entries = []
    for line in target.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if text and not text.startswith("#"):
            entries.append(text)
    return entries


def read_alert_surface(skill_dir: Path):
    path = skill_dir / "assets" / "alert-surface.json"
    if not path.is_file():
        return "unconfirmed", "assets/alert-surface.json is absent"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise Blocked("assets/alert-surface.json is not valid JSON: {}".format(exc))
    status = data.get("status") or "unconfirmed"
    return status, "assets/alert-surface.json says status={}".format(status)


def check_statement(sql, signal, denylist, surface_status, surface_reason):
    """Return a list of (rule_id, message). Pure: this is what the self-test drives."""
    findings = []
    clean = strip_comments(sql)
    lowered = clean.lower()
    data_table = reads_data_table(clean, signal)

    head = clean.strip().lstrip("(").lstrip().split(None, 1)
    if head and head[0].lower() in DESTRUCTIVE:
        findings.append(("S8", "statement begins with `{}`: this skill proposes no DDL or mutation "
                               "against a vendor-owned table".format(head[0].upper())))

    if data_table:
        start_var, end_var = TIME_VARS[signal]
        if start_var not in sql or end_var not in sql:
            findings.append(("S1", "no bounded time predicate using {} and {}, which is what the {} "
                                   "surface supplies".format(start_var, end_var, signal)))

    if signal in ("logs", "traces") and data_table and "ts_bucket_start" not in lowered:
        findings.append(("S2", "no ts_bucket_start predicate: ts_bucket_start is the first sorting-key "
                               "column, so the query reads every part in the partition"))

    databases = set(re.findall(r"\b(signoz_(?:logs|traces|metrics|metadata|meter))\.", clean))
    if len(databases) > 1 and not re.search(r"\bJOIN\b[^;]*?\bON\b", clean, re.I | re.S):
        findings.append(("S3", "reads {} without an explicit JOIN ... ON".format(
            ", ".join(sorted(databases)))))

    resource_table = re.search(r"\b(\w*_resource)\b", clean)
    if resource_table:
        for match in re.finditer(r"(\bGLOBAL\s+IN\b|\bIN\b)", clean, re.I):
            if match.group(1).strip().lower() == "in":
                preceding = clean[max(0, match.start() - 8):match.start()].lower()
                if "global" not in preceding:
                    findings.append(("S4", "a resource subquery is reached with a plain IN: on a "
                                           "clustered install each shard evaluates it locally and rows "
                                           "go missing without an error. Use GLOBAL IN."))
                    break

    if resource_table:
        cte = re.search(r"FROM\s+\S*?_resource\s+WHERE\s+(.*?)\)", clean, re.I | re.S)
        cte_body = cte.group(1) if cte else ""
        filters_attribute = "simplejsonextractstring" in cte_body.lower() or "jsonextractstring" in cte_body.lower()
        if not filters_attribute:
            findings.append(("S5", "a resource CTE is present but filters no resource attribute, so it "
                                   "widens the fingerprint set instead of narrowing it. Remove the CTE."))
    elif signal in ("logs", "traces") and re.search(r"WHERE[\s\S]*?resource\.\w", clean, re.I):
        findings.append(("S5", "filters a resource attribute in the main WHERE with no resource CTE, so "
                               "the filter cannot become a primary-key range on resource_fingerprint"))

    if signal == "metrics" and any(t in clean for t in METRIC_SAMPLE_TABLES):
        if not ROLLUP_RE.search(clean) and not RAW_SCAN_OK_RE.search(sql):
            findings.append(("S6", "reads raw samples with neither a rollup nor a `-- raw-scan-ok:` bound. "
                                   "A panel's window is chosen at view time, so the raw table needs a "
                                   "stated window under which it is the right table."))

    alias_map = aliases(clean)
    for term in group_by_terms(clean):
        resolved = alias_map.get(term.strip("`"), term)
        for banned in denylist:
            if re.search(r"\b{}\b".format(re.escape(banned)), resolved, re.I):
                findings.append(("S7", "GROUP BY `{}` resolves to `{}`, which carries the denylisted "
                                       "high-cardinality field `{}`".format(term, resolved, banned)))
                break

    if data_table:
        shape = panel_shape(clean)
        if shape == "table" and not re.search(r"\bLIMIT\b", clean, re.I):
            findings.append(("S9", "table-shaped result with no LIMIT: an unbounded table panel returns "
                                   "every group and the widget renders whatever arrives first"))
        if shape == "timeseries" and not re.search(r"\bORDER\s+BY\s+ts\b", clean, re.I):
            findings.append(("S9", "timeseries result is not ordered by ts, so the line is drawn in "
                                   "storage order"))

    if CREDENTIAL_RE.search(sql):
        findings.append(("S10", "a credential-shaped literal appears in the statement"))

    if surface_status is not None and surface_status != "dashboards-and-alerts":
        findings.append(("S11", "requested as alert SQL, but the ClickHouse alert surface is not "
                                "confirmed on this install ({}). Deliver the dashboard-panel form and "
                                "the Query Builder alert path instead.".format(surface_reason)))

    return findings


def gather(args):
    items = []
    if args.sql:
        for name in args.sql:
            path = Path(name)
            if not path.is_file():
                raise Blocked("--sql file not found: {}".format(path))
            items.append((path.as_posix(), 1, path.read_text(encoding="utf-8")))
    if args.scan_skill:
        directory = args.skill_dir
        if not directory.is_dir():
            raise Blocked("--skill-dir does not exist: {}".format(directory))
        items.extend(extract_blocks(directory))
    if not items:
        raise Blocked("no input: supply --sql FILE or --skill-dir PATH")
    return items


def run(args) -> int:
    denylist = load_denylist(args.cardinality_denylist)
    surface_status, surface_reason = (None, None)
    if args.surface == "alert":
        surface_status, surface_reason = read_alert_surface(args.skill_dir)

    items = gather(args)
    findings, checked, skipped = [], 0, 0
    for rel, lineno, text in items:
        for statement in split_statements(text):
            kind, signal = classify(statement)
            if kind != "statement":
                skipped += 1
                continue
            checked += 1
            for rule, message in check_statement(statement, signal, denylist,
                                                 surface_status, surface_reason):
                snippet = " ".join(statement.split())[:70]
                findings.append({"file": rel, "line": lineno, "rule": rule,
                                 "signal": signal, "message": message, "statement": snippet})

    if args.as_json:
        print(json.dumps({"checked": checked, "skipped": skipped, "findings": findings}, indent=2))
    else:
        for item in findings:
            print("{file}:{line}  {rule}  [{signal}]  {message}".format(**item))
            print("        statement: {statement}".format(**item))
        print("checked {} statement(s), skipped {} fragment/template block(s), {} finding(s)".format(
            checked, skipped, len(findings)))
    return FINDINGS if findings else CLEAN


def self_test() -> int:
    """One statement per rule, each violating exactly the rule named, plus one clean statement.
    Committed inline so the assertions are shown to fail before the checker is trusted."""
    cases = [
        ("S1", "logs", "SELECT toFloat64(count()) AS value FROM signoz_logs.distributed_logs_v2 "
                       "WHERE ts_bucket_start BETWEEN 1 AND 2"),
        ("S2", "logs", "SELECT toFloat64(count()) AS value FROM signoz_logs.distributed_logs_v2 "
                       "WHERE timestamp >= $start_timestamp_nano AND timestamp <= $end_timestamp_nano"),
        ("S3", "traces", "SELECT toFloat64(count()) AS value FROM signoz_traces.distributed_signoz_index_v3, "
                         "signoz_logs.distributed_logs_v2 WHERE timestamp BETWEEN $start_datetime AND "
                         "$end_datetime AND ts_bucket_start BETWEEN 1 AND 2"),
        ("S4", "traces", "WITH __r AS (SELECT fingerprint FROM signoz_traces.distributed_traces_v3_resource "
                         "WHERE simpleJSONExtractString(labels, 'service.name') = 'a') "
                         "SELECT toFloat64(count()) AS value FROM signoz_traces.distributed_signoz_index_v3 "
                         "WHERE resource_fingerprint IN __r AND timestamp BETWEEN $start_datetime AND "
                         "$end_datetime AND ts_bucket_start BETWEEN 1 AND 2"),
        ("S5", "traces", "WITH __r AS (SELECT fingerprint FROM signoz_traces.distributed_traces_v3_resource "
                         "WHERE seen_at_ts_bucket_start BETWEEN 1 AND 2) "
                         "SELECT toFloat64(count()) AS value FROM signoz_traces.distributed_signoz_index_v3 "
                         "WHERE resource_fingerprint GLOBAL IN __r AND timestamp BETWEEN $start_datetime "
                         "AND $end_datetime AND ts_bucket_start BETWEEN 1 AND 2"),
        ("S6", "metrics", "SELECT toStartOfInterval(toDateTime(intDiv(unix_milli, 1000)), "
                          "toIntervalSecond(60)) AS ts, avg(value) AS value FROM "
                          "signoz_metrics.distributed_samples_v4 WHERE unix_milli >= "
                          "{{.start_timestamp_ms}} AND unix_milli < {{.end_timestamp_ms}} "
                          "GROUP BY ts ORDER BY ts ASC"),
        ("S7", "traces", "SELECT trace_id AS grp, toFloat64(count()) AS value FROM "
                         "signoz_traces.distributed_signoz_index_v3 WHERE timestamp BETWEEN "
                         "$start_datetime AND $end_datetime AND ts_bucket_start BETWEEN 1 AND 2 "
                         "GROUP BY grp LIMIT 10"),
        ("S8", "traces", "OPTIMIZE TABLE signoz_traces.distributed_signoz_index_v3 FINAL"),
        ("S9", "traces", "SELECT http_method, toFloat64(avg(duration_nano)) AS avg_ns FROM "
                         "signoz_traces.distributed_signoz_index_v3 WHERE timestamp BETWEEN "
                         "$start_datetime AND $end_datetime AND ts_bucket_start BETWEEN 1 AND 2 "
                         "GROUP BY http_method"),
        ("S10", "logs", "SELECT toFloat64(count()) AS value FROM signoz_logs.distributed_logs_v2 "
                        "WHERE timestamp >= $start_timestamp_nano AND timestamp <= "
                        "$end_timestamp_nano AND ts_bucket_start BETWEEN 1 AND 2 AND "
                        "attributes_string['auth'] = 'Bearer abcdef1234567890'"),
    ]
    clean = ("SELECT toStartOfInterval(timestamp, INTERVAL 1 MINUTE) AS ts, toFloat64(count()) AS value "
             "FROM signoz_traces.distributed_signoz_index_v3 WHERE timestamp BETWEEN $start_datetime AND "
             "$end_datetime AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp "
             "GROUP BY ts ORDER BY ts ASC")

    failures = []
    for expected, signal, sql in cases:
        fired = {rule for rule, _ in check_statement(sql, signal, DEFAULT_DENYLIST, None, None)}
        if expected not in fired:
            failures.append("{} did not fire on its red case (fired: {})".format(
                expected, sorted(fired) or "nothing"))

    fired = {rule for rule, _ in check_statement(clean, "traces", DEFAULT_DENYLIST, None, None)}
    if fired:
        failures.append("the clean statement fired {}".format(sorted(fired)))

    surface_fired = {rule for rule, _ in check_statement(
        clean, "traces", DEFAULT_DENYLIST, "unconfirmed", "self-test")}
    if "S11" not in surface_fired:
        failures.append("S11 did not fire on a clean statement requested as alert SQL")
    confirmed = {rule for rule, _ in check_statement(
        clean, "traces", DEFAULT_DENYLIST, "dashboards-and-alerts", "self-test")}
    if "S11" in confirmed:
        failures.append("S11 fired even though the alert surface is confirmed")

    # A ';' inside a comment is not a statement boundary. Regression: it used to be, and a
    # query whose comment contained one was split into fragments and never checked.
    commented = "-- note: read `last`; then difference it\n" + clean
    parts = split_statements(commented)
    if len(parts) != 1:
        failures.append("split_statements broke one commented statement into {}".format(len(parts)))
    elif classify(parts[0])[0] != "statement":
        failures.append("a commented statement classified as {}".format(classify(parts[0])[0]))
    if len(split_statements("SELECT 1 /* a; b */ FROM t")) != 1:
        failures.append("split_statements split on a ';' inside a block comment")
    if len(split_statements("SELECT 1; SELECT 2")) != 2:
        failures.append("split_statements failed to split two real statements")

    print("self-test: {} red case(s) + 1 clean + 2 surface case(s) + 4 splitter case(s), "
          "{} failure(s)".format(len(cases), len(failures)))
    for failure in failures:
        print("  FAIL {}".format(failure))
    return FINDINGS if failures else CLEAN


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check SigNoz ClickHouse SQL against the rules this skill states.",
        epilog="Exit 0 clean, 1 findings, 2 could not run. A 2 is never a pass.")
    parser.add_argument("--sql", action="append", help="a file of SQL to check; repeatable")
    parser.add_argument("--skill-dir", type=Path, default=None,
                        help="with no --sql, check every ```sql block under this directory; with "
                             "--sql, used only to locate assets/alert-surface.json")
    parser.add_argument("--surface", choices=["dashboard", "alert"], default="dashboard",
                        help="what the SQL is destined for; 'alert' enables rule S11")
    parser.add_argument("--cardinality-denylist", default=None,
                        help="file of field names, one per line, replacing the built-in list")
    parser.add_argument("--json", dest="as_json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    # --sql names the corpus. --skill-dir then only locates assets/alert-surface.json, because
    # --surface is a property of the query being handed over, not of this skill's own examples.
    args.scan_skill = not args.sql
    if args.skill_dir is None:
        args.skill_dir = default_skill_dir()

    try:
        return run(args)
    except Blocked as exc:
        print("BLOCKED: {}".format(exc), file=sys.stderr)
        return BLOCKED


if __name__ == "__main__":
    raise SystemExit(main())
