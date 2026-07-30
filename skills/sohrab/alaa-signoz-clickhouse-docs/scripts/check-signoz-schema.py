#!/usr/bin/env python3
"""Assert every table and column this skill claims against a real SigNoz install.

A finding here means the skill is stale, not that a query is wrong. That is the whole point:
SigNoz owns these tables, upgrades them without asking, and a reference file that quietly
describes last year's schema produces SQL that fails in a dashboard panel.

Two input modes, exactly one required:
  --describe-dir DIR   captured output, one <db>.<table>.tsv per table, so this runs with no
                       ClickHouse access at all. Optional sorting-keys.tsv gives
                       "<db>.<table><TAB><sorting key>" so the key assertion also runs offline.
  --dsn URL            live, over the ClickHouse HTTP interface, e.g.
                       http://user:pass@clickhouse:8123/

Exit codes:
  0  every asserted table and column is present, and the sorting-key prefix still holds
  1  something asserted is absent, or the sorting key changed
  2  no input, unreadable input, DSN unreachable, credentials refused, or DESCRIBE denied

Runs on Windows and POSIX: pure Python 3, no shell pipelines.
"""

from __future__ import annotations

import argparse
import base64
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CLEAN = 0
FINDINGS = 1
BLOCKED = 2

# What the reference files claim. Editing a reference without editing this list is the
# drift this script exists to catch, so keep them in step.
REQUIRED = {
    "logs": {
        "signoz_logs.distributed_logs_v2": [
            "timestamp", "ts_bucket_start", "resource_fingerprint", "trace_id", "span_id",
            "severity_text", "severity_number", "body", "attributes_string", "attributes_number",
            "attributes_bool", "resource", "scope_name", "scope_version",
        ],
        "signoz_logs.distributed_logs_v2_resource": [
            "fingerprint", "labels", "seen_at_ts_bucket_start",
        ],
    },
    "traces": {
        "signoz_traces.distributed_signoz_index_v3": [
            "ts_bucket_start", "resource_fingerprint", "timestamp", "trace_id", "span_id",
            "parent_span_id", "name", "kind", "kind_string", "duration_nano", "status_code",
            "status_code_string", "has_error", "attributes_string", "attributes_number",
            "attributes_bool", "resource", "http_method", "http_url", "http_host",
            "db_name", "db_operation",
        ],
        "signoz_traces.distributed_traces_v3_resource": [
            "fingerprint", "labels", "seen_at_ts_bucket_start",
        ],
    },
    "metrics": {
        "signoz_metrics.distributed_samples_v4": [
            "env", "temporality", "metric_name", "fingerprint", "unix_milli", "value", "flags",
        ],
        "signoz_metrics.distributed_time_series_v4": [
            "env", "temporality", "metric_name", "description", "unit", "type",
            "is_monotonic", "fingerprint", "unix_milli", "labels",
        ],
        "signoz_metrics.distributed_time_series_v4_6hrs": [
            "env", "temporality", "metric_name", "fingerprint", "unix_milli", "labels",
        ],
        "signoz_metrics.distributed_time_series_v4_1day": [
            "env", "temporality", "metric_name", "fingerprint", "unix_milli", "labels",
        ],
    },
}

# Absent is information, not a defect: these arrive with a SigNoz upgrade, and a query must
# confirm one exists before reading it. Reported as notes.
PROBES = {
    "logs": [
        ("signoz_logs.distributed_logs_v2", "body_v2"),
        ("signoz_logs.distributed_logs_v2", "body_promoted"),
        ("signoz_metadata.distributed_field_keys", None),
        ("signoz_metadata.distributed_attributes_metadata", None),
    ],
    "traces": [
        ("signoz_traces.distributed_dependency_graph_minutes_v2", None),
        ("signoz_traces.distributed_signoz_error_index_v2", None),
    ],
    "metrics": [
        ("signoz_metrics.samples_v4_agg_5m", None),
        ("signoz_metrics.samples_v4_agg_30m", None),
        ("signoz_metrics.distributed_samples_v4_agg_5m", None),
        ("signoz_metrics.distributed_samples_v4_agg_30m", None),
        ("signoz_metrics.distributed_exp_hist", None),
        ("signoz_metrics.distributed_metadata", None),
        ("signoz_metrics.distributed_updated_metadata", None),
        ("signoz_metrics.distributed_metric_reduction_rules", None),
        ("signoz_metrics.distributed_time_series_v4_1week", None),
    ],
}

# The fact every rule in the traces reference rests on. If this prefix changes, the bucket
# predicate stops being a primary-key range and every performance claim needs rewriting.
SORTING_KEY_PREFIX = {
    "signoz_traces.signoz_index_v3": ["ts_bucket_start", "resource_fingerprint"],
}


class Blocked(Exception):
    pass


def default_skill_dir() -> Path:
    return Path(sys.argv[0]).resolve().parent.parent


def parse_sorting_key(expression: str):
    text = expression.strip()
    if text.startswith("(") and text.endswith(")"):
        text = text[1:-1]
    return [part.strip() for part in text.split(",") if part.strip()]


class DirSource:
    """Reads captured DESCRIBE output. Column name is the first tab-separated field."""

    def __init__(self, directory: Path):
        if not directory.is_dir():
            raise Blocked("--describe-dir does not exist: {}".format(directory))
        self.directory = directory
        self.keys = {}
        key_file = directory / "sorting-keys.tsv"
        if key_file.is_file():
            for line in key_file.read_text(encoding="utf-8").splitlines():
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                parts = line.split("\t", 1)
                if len(parts) == 2:
                    self.keys[parts[0].strip()] = parts[1]

    def columns(self, qualified):
        path = self.directory / "{}.tsv".format(qualified)
        if not path.is_file():
            return None
        names = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            names.append(line.split("\t", 1)[0].strip())
        return names

    def sorting_key(self, qualified):
        expression = self.keys.get(qualified)
        return parse_sorting_key(expression) if expression else None


class DsnSource:
    """Live query over the ClickHouse HTTP interface."""

    def __init__(self, dsn: str, timeout: int):
        parsed = urllib.parse.urlparse(dsn)
        if parsed.scheme not in ("http", "https"):
            raise Blocked("--dsn must be an http:// or https:// ClickHouse HTTP endpoint")
        self.base = "{}://{}:{}{}".format(parsed.scheme, parsed.hostname,
                                          parsed.port or (8443 if parsed.scheme == "https" else 8123),
                                          parsed.path or "/")
        self.auth = None
        if parsed.username:
            raw = "{}:{}".format(parsed.username, parsed.password or "")
            self.auth = base64.b64encode(raw.encode("utf-8")).decode("ascii")
        self.timeout = timeout

    def query(self, sql: str):
        request = urllib.request.Request(self.base, data=sql.encode("utf-8"), method="POST")
        if self.auth:
            request.add_header("Authorization", "Basic {}".format(self.auth))
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:300]
            raise Blocked("ClickHouse refused a query ({}): {}".format(exc.code, detail))
        except Exception as exc:
            raise Blocked("ClickHouse unreachable: {}: {}".format(type(exc).__name__, exc))

    def columns(self, qualified):
        database, table = qualified.split(".", 1)
        sql = ("SELECT name FROM system.columns WHERE database = '{}' AND table = '{}' "
               "FORMAT TabSeparated".format(database, table))
        rows = [line.strip() for line in self.query(sql).splitlines() if line.strip()]
        return rows or None

    def sorting_key(self, qualified):
        database, table = qualified.split(".", 1)
        sql = ("SELECT sorting_key FROM system.tables WHERE database = '{}' AND name = '{}' "
               "FORMAT TabSeparated".format(database, table))
        rows = [line for line in self.query(sql).splitlines() if line.strip()]
        return parse_sorting_key(rows[0]) if rows else None


def check(source, signals):
    findings, notes = [], []

    for signal in signals:
        for qualified, required in sorted(REQUIRED[signal].items()):
            present = source.columns(qualified)
            if present is None:
                findings.append("{}: table absent from the target".format(qualified))
                continue
            missing = [name for name in required if name not in present]
            for name in missing:
                findings.append("{}: column `{}` claimed by this skill is absent".format(qualified, name))

    for signal in signals:
        for qualified, column in PROBES[signal]:
            present = source.columns(qualified)
            if present is None:
                notes.append("{}: not present on this target".format(qualified))
            elif column is not None and column not in present:
                notes.append("{}: optional column `{}` not present".format(qualified, column))
            else:
                notes.append("{}: present{}".format(qualified, "" if column is None else " with `{}`".format(column)))

    if "traces" in signals:
        for qualified, expected in sorted(SORTING_KEY_PREFIX.items()):
            actual = source.sorting_key(qualified)
            if actual is None:
                notes.append("{}: sorting key unavailable, prefix assertion not run".format(qualified))
            elif actual[:len(expected)] != expected:
                findings.append("{}: sorting key begins {} -- this skill's rules require {}. "
                                "Rewrite the traces reference before any query.".format(
                                    qualified, ", ".join(actual[:len(expected)]), ", ".join(expected)))
            else:
                notes.append("{}: sorting key still begins {}".format(qualified, ", ".join(expected)))

    return findings, notes


def report(findings, notes, as_json):
    if as_json:
        print(json.dumps({"findings": findings, "notes": notes}, indent=2))
    else:
        for note in notes:
            print("NOTE    {}".format(note))
        for finding in findings:
            print("FINDING {}".format(finding))
        print("{} finding(s), {} note(s)".format(len(findings), len(notes)))
    return FINDINGS if findings else CLEAN


def self_test(skill_dir: Path) -> int:
    """Green fixture must exit 0; red fixture must exit 1 and name the removed column;
    a missing directory must exit 2. Committed under test/fixtures/schema/."""
    base = skill_dir / "test" / "fixtures" / "schema"
    failures = []

    try:
        findings, _ = check(DirSource(base / "green"), ["logs", "traces", "metrics"])
        if findings:
            failures.append("green fixture produced {} finding(s): {}".format(len(findings), findings))
    except Blocked as exc:
        failures.append("green fixture blocked: {}".format(exc))

    try:
        findings, _ = check(DirSource(base / "red-missing-column"), ["traces"])
        joined = " | ".join(findings)
        if not findings:
            failures.append("red fixture produced no finding")
        elif "ts_bucket_start" not in joined:
            failures.append("red fixture did not name ts_bucket_start: {}".format(joined))
    except Blocked as exc:
        failures.append("red fixture blocked: {}".format(exc))

    try:
        findings, _ = check(DirSource(base / "red-sorting-key"), ["traces"])
        if not any("sorting key begins" in f for f in findings):
            failures.append("red sorting-key fixture did not report a changed key: {}".format(findings))
    except Blocked as exc:
        failures.append("red sorting-key fixture blocked: {}".format(exc))

    try:
        DirSource(base / "does-not-exist")
        failures.append("a missing --describe-dir did not raise Blocked")
    except Blocked:
        pass

    print("self-test: 4 fixture case(s), {} failure(s)".format(len(failures)))
    for failure in failures:
        print("  FAIL {}".format(failure))
    return FINDINGS if failures else CLEAN


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Assert this skill's SigNoz table and column claims against a target install.",
        epilog="Exit 0 clean, 1 findings, 2 could not run. A 2 is never a pass.")
    parser.add_argument("--describe-dir", type=Path, default=None,
                        help="directory of captured <db>.<table>.tsv DESCRIBE output")
    parser.add_argument("--dsn", default=None, help="ClickHouse HTTP endpoint to query live")
    parser.add_argument("--signal", choices=["logs", "traces", "metrics", "all"], default="all")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--json", dest="as_json", action="store_true")
    parser.add_argument("--skill-dir", type=Path, default=None, help="used only by --self-test")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test(args.skill_dir if args.skill_dir is not None else default_skill_dir())

    if (args.describe_dir is None) == (args.dsn is None):
        print("BLOCKED: supply exactly one of --describe-dir or --dsn. Without a target this "
              "script cannot tell a correct claim from an unchecked one.", file=sys.stderr)
        return BLOCKED

    signals = ["logs", "traces", "metrics"] if args.signal == "all" else [args.signal]
    try:
        source = DirSource(args.describe_dir) if args.describe_dir else DsnSource(args.dsn, args.timeout)
        findings, notes = check(source, signals)
    except Blocked as exc:
        print("BLOCKED: {}".format(exc), file=sys.stderr)
        return BLOCKED
    return report(findings, notes, args.as_json)


if __name__ == "__main__":
    raise SystemExit(main())
