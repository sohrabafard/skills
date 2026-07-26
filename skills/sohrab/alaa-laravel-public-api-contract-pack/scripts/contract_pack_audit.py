#!/usr/bin/env python3
"""
contract_pack_audit.py - deterministic audit for a Laravel public API contract pack.

Three checks, each selectable, all reported in one run:

  parity   route inventory vs OpenAPI operations vs Postman requests
  version  contract.meta.json contract_version / api_version vs OpenAPI info.version
  gate     every OpenAPI operation resolves an api version, an explicit deprecation
           status, and - when deprecated - a real sunset date that is not a marker

Stdlib only. Python 3.8+. Read the exit-code table with --help.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys

HTTP_METHODS = ("get", "put", "post", "delete", "patch", "head", "options", "trace")
COMPARED = ("get", "put", "post", "delete", "patch")
PLACEHOLDER = re.compile(r"^(\{\{.*\}\}|\{.*\}|:.+)$")
VERSION_SEG = re.compile(r"^v\d+$")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MARKERS = ("NEEDS_BACKEND_CONFIRMATION", "not_implemented", "TBD", "TODO",
           "unknown", "unconfirmed", "reserved")

EXIT_OK, EXIT_USAGE, EXIT_PARITY, EXIT_UNPARSABLE, EXIT_VERSION, EXIT_GATE = 0, 1, 2, 3, 4, 5

PATH_KEY = re.compile(r'^(\s+)("?)(/[^"\s:]*)\2\s*:\s*(.*)$')
KEY_LINE = re.compile(r'^(\s+)([A-Za-z][A-Za-z0-9_.\-]*)\s*:\s*(.*)$')
REF_LINE = re.compile(r'^(\s+)\$ref\s*:')
INFO_VER = re.compile(r'^\s{1,4}version\s*:\s*(.+?)\s*$')


class Unparsable(Exception):
    def __init__(self, line_no, why):
        super().__init__("line %d: %s" % (line_no, why))
        self.line_no = line_no
        self.why = why


def indent_of(line):
    return len(line) - len(line.lstrip(" "))


def norm_path(raw, drop_leading_placeholders=False):
    """Normalise one path for comparison; every parameter segment becomes `{}`.

    Parameter names are erased on purpose: Postman spells a parameter `{{courseId}}`
    where routes and OpenAPI spell it `{course_id}`. Parity answers coverage; a name
    mismatch is a review finding, not a missing operation.
    """
    raw = str(raw).strip()
    raw = re.sub(r"^[a-zA-Z][a-zA-Z0-9+.\-]*://[^/]+", "", raw)
    raw = raw.split("?", 1)[0].split("#", 1)[0]
    segs = [s for s in raw.split("/") if s != ""]
    out = []
    for s in segs:
        out.append("{}" if PLACEHOLDER.match(s) else s)
    if drop_leading_placeholders:
        while out and out[0] == "{}":
            out.pop(0)
    return "/" + "/".join(out)


def read_text(path):
    try:
        if path == "-":
            return sys.stdin.read()
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError as exc:
        raise SystemExit("%s: cannot read: %s" % (path, exc))


def read_json(path):
    text = read_text(path)
    try:
        return json.loads(text)
    except ValueError as exc:
        raise SystemExit("%s: not valid JSON: %s" % (path, exc))


def load_routes(path):
    """`php artisan route:list --json` output -> {(method, path)}."""
    data = read_json(path)
    if not isinstance(data, list):
        raise SystemExit("%s: expected a JSON array from `route:list --json`" % path)
    ops = set()
    for row in data:
        if not isinstance(row, dict) or "uri" not in row:
            continue
        for meth in str(row.get("method", "")).split("|"):
            meth = meth.strip().lower()
            if meth in COMPARED:
                ops.add((meth, norm_path(row["uri"])))
    return ops


def load_postman(path):
    """Postman Collection v2.1 -> {(method, path)}."""
    doc = read_json(path)
    ops = set()

    def walk(items):
        for item in items or []:
            if isinstance(item, dict) and isinstance(item.get("item"), list):
                walk(item["item"])
                continue
            req = item.get("request") if isinstance(item, dict) else None
            if not isinstance(req, dict):
                continue
            meth = str(req.get("method", "")).strip().lower()
            if meth not in COMPARED:
                continue
            url = req.get("url")
            if isinstance(url, dict) and isinstance(url.get("path"), list):
                raw = "/".join(str(s) for s in url["path"])
            elif isinstance(url, dict):
                raw = str(url.get("raw", ""))
            else:
                raw = str(url or "")
            ops.add((meth, norm_path(raw, drop_leading_placeholders=True)))

    walk(doc.get("item"))
    return ops


def scan_openapi_yaml(text):
    """Operations and their direct scalar keys from a `paths:` block.

    Reads block-style YAML with space indentation and nothing else. Any construct it
    cannot prove it understands raises Unparsable: a parity result computed from a
    half-read artifact is worse than no result.
    """
    lines = text.splitlines()
    start = None
    for idx, line in enumerate(lines):
        if re.match(r"^paths:\s*$", line):
            start = idx + 1
            break
        if re.match(r"^paths:\s*\S", line):
            raise Unparsable(idx + 1, "`paths:` is inline or flow-style; only a block mapping is read")
    if start is None:
        raise Unparsable(0, "no top-level `paths:` block found")

    block = []
    for idx in range(start, len(lines)):
        line = lines[idx]
        if "\t" in line:
            raise Unparsable(idx + 1, "tab indentation inside `paths:`")
        if line.strip() and indent_of(line) == 0:
            break
        block.append((idx + 1, line))

    ops = {}
    path_indent = op_indent = child_indent = None
    cur_path = cur_op = None
    pos = 0
    while pos < len(block):
        line_no, line = block[pos]
        pos += 1
        if "\t" in line:
            raise Unparsable(line_no, "tab indentation inside `paths:`")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        ind = indent_of(line)

        match = PATH_KEY.match(line)
        if match and (path_indent is None or ind == path_indent):
            trailing = match.group(4).strip()
            if trailing and not trailing.startswith("#"):
                raise Unparsable(line_no, "path item is inline or aliased; expected a nested mapping")
            path_indent = ind
            cur_path, cur_op, op_indent, child_indent = match.group(3), None, None, None
            continue
        if cur_path is None or path_indent is None or ind <= path_indent:
            continue
        if REF_LINE.match(line):
            # A deep `$ref` in a response schema is ordinary. One standing where a path
            # item or an operation body belongs hides the fields the gate reads.
            if cur_op is None or (op_indent is not None and ind == op_indent):
                raise Unparsable(line_no, "`$ref` in place of a path item; resolve it or pass OpenAPI as JSON")
            if child_indent is None or ind == child_indent:
                raise Unparsable(line_no, "`$ref` in place of an operation body; resolve it or pass OpenAPI as JSON")
            continue

        match = KEY_LINE.match(line)
        if not match:
            continue
        key, value = match.group(2).lower(), match.group(3).strip()
        if value.startswith("&") or value.startswith("*"):
            raise Unparsable(line_no, "YAML anchor or alias inside `paths:`")
        if value.startswith("|") or value.startswith(">"):
            while pos < len(block):
                nxt_no, nxt = block[pos]
                if nxt.strip() and indent_of(nxt) <= ind:
                    break
                pos += 1

        if key in HTTP_METHODS and (op_indent is None or ind == op_indent):
            op_indent, child_indent = ind, None
            cur_op = (key, cur_path)
            ops.setdefault(cur_op, {})
            continue
        if cur_op is None or op_indent is None or ind <= op_indent:
            continue
        if child_indent is None:
            child_indent = ind
        if ind == child_indent and value and not value.startswith("#"):
            ops[cur_op][match.group(2)] = value.strip('"\'')
    return ops


def scan_info_version(text):
    inside = False
    for line in text.splitlines():
        if re.match(r"^info:\s*$", line):
            inside = True
            continue
        if inside:
            if line.strip() and indent_of(line) == 0:
                return None
            match = INFO_VER.match(line)
            if match:
                return match.group(1).strip().strip('"\'')
    return None


def load_openapi(path):
    """-> ({(method, path): {scalar key: value}}, info_version)."""
    if path.lower().endswith(".json"):
        doc = read_json(path)
        paths = doc.get("paths") or {}
        ops = {}
        for raw_path, item in paths.items():
            if not isinstance(item, dict):
                continue
            for meth, body in item.items():
                if meth.lower() in HTTP_METHODS and isinstance(body, dict):
                    scalars = {k: v for k, v in body.items()
                               if isinstance(v, (str, bool, int, float)) or v is None}
                    ops[(meth.lower(), raw_path)] = scalars
        return ops, str(((doc.get("info") or {}).get("version") or "")) or None
    text = read_text(path)
    return scan_openapi_yaml(text), scan_info_version(text)


def infer_openapi_base(oa_ops, route_ops, override):
    """Prefix that makes server-relative OpenAPI paths comparable to route URIs.

    Among the empty prefix and every 1-to-3 leading non-parameter segment prefix in
    the route inventory, take the one matching the most operations; ties go to the
    shortest. The chosen prefix is printed, so the reader never has to guess.
    """
    if override is not None:
        return norm_path(override) if override.strip("/") else ""
    candidates = {""}
    for _, path in route_ops:
        segs = [s for s in path.split("/") if s]
        for n in (1, 2, 3):
            if len(segs) >= n and all(s != "{}" for s in segs[:n]):
                candidates.add("/" + "/".join(segs[:n]))
    best, best_score = "", -1
    for cand in sorted(candidates, key=lambda c: (len(c), c)):
        score = sum(1 for meth, path in oa_ops if (meth, norm_path(cand + path)) in route_ops)
        if score > best_score:
            best, best_score = cand, score
    return best


def label(op):
    return "%s %s" % (op[0].upper(), op[1])


def keep(op, include, exclude):
    text = label(op)
    if include and not any(op[1] == pre or op[1].startswith(pre.rstrip("/") + "/") for pre in include):
        return False
    return not any(fnmatch.fnmatch(text, pat) for pat in exclude)


def is_exempt(path):
    return path in ("/metrics",) or path.endswith("/health") or path.endswith("/ready")


def check_parity(routes, oa_norm, postman, include, exclude, findings):
    routes = {op for op in routes if keep(op, include, exclude)}
    oa_norm = {op for op in oa_norm if keep(op, include, exclude)}
    postman = {op for op in postman if keep(op, include, exclude)}
    counts = {"routes": len(routes), "openapi": len(oa_norm), "postman": len(postman)}
    # An unsupplied artifact is unknown, never an empty truth: comparing against it
    # would report every operation as drift. Each pair needs both sides present.
    for name, other in (("openapi", oa_norm), ("postman", postman)):
        if not other or not routes:
            continue
        for op in sorted(routes - other):
            findings.append((EXIT_PARITY, "missing_in_" + name, label(op)))
        for op in sorted(other - routes):
            findings.append((EXIT_PARITY, "stale_in_" + name, label(op)))
    if oa_norm and postman:
        for op in sorted(oa_norm ^ postman):
            side = "postman" if op in oa_norm else "openapi"
            findings.append((EXIT_PARITY, "openapi_postman_divergence",
                             "%s (absent from %s)" % (label(op), side)))
    return counts


def check_version(meta, info_version, routes, findings):
    contract_version = str(meta.get("contract_version", "")).strip()
    api_version = str(meta.get("api_version", "")).strip()
    if not re.match(r"^\d+\.\d+\.\d+$", contract_version):
        findings.append((EXIT_VERSION, "contract_version_not_semver",
                         "contract.meta.json contract_version=%r" % contract_version))
    if info_version is not None and contract_version and info_version != contract_version:
        findings.append((EXIT_VERSION, "openapi_info_version_drift",
                         "openapi info.version=%s but contract_version=%s" % (info_version, contract_version)))
    route_versions = set()
    for _, path in routes:
        for seg in path.split("/"):
            if VERSION_SEG.match(seg):
                route_versions.add(seg)
    if api_version and route_versions and api_version not in route_versions:
        findings.append((EXIT_VERSION, "api_version_not_in_routes",
                         "api_version=%s but route inventory carries %s"
                         % (api_version, ",".join(sorted(route_versions)))))
    if len(route_versions) > 1:
        findings.append((EXIT_VERSION, "multiple_api_versions_served",
                         "routes carry %s; the pack must document each" % ",".join(sorted(route_versions))))


def check_gate(oa_ops, base, include, exclude, findings):
    """The emission gate. Every non-operational operation resolves all three fields."""
    checked = 0
    for op, scalars in sorted(oa_ops.items()):
        norm = (op[0], norm_path(base + op[1]))
        if not keep(norm, include, exclude) or is_exempt(norm[1]):
            continue
        checked += 1
        name = label(norm)
        for field, value in scalars.items():
            if field in ("deprecated", "x-sunset-date", "x-api-version") \
                    and any(mark.lower() in str(value).lower() for mark in MARKERS):
                findings.append((EXIT_GATE, "marker_in_contract_field",
                                 "%s: %s=%r is a marker, not a resolved value" % (name, field, value)))
        has_version = any(VERSION_SEG.match(seg) for seg in norm[1].split("/")) \
            or str(scalars.get("x-api-version", "")).strip() != ""
        if not has_version:
            findings.append((EXIT_GATE, "version_unresolved",
                             "%s: no /vN path segment and no x-api-version" % name))
        raw = scalars.get("deprecated", None)
        flag = str(raw).strip().lower()
        if raw is None or flag not in ("true", "false"):
            findings.append((EXIT_GATE, "deprecation_unresolved",
                             "%s: `deprecated` absent or not true/false (got %r)" % (name, raw)))
        elif flag == "true":
            sunset = str(scalars.get("x-sunset-date", "")).strip()
            if not ISO_DATE.match(sunset):
                findings.append((EXIT_GATE, "sunset_unresolved",
                                 "%s: deprecated with x-sunset-date=%r; need YYYY-MM-DD" % (name, sunset)))
    return checked


HELP_EPILOG = """
exit codes (all findings print regardless; the code is the highest one present)
  0  every requested check passed
  1  usage error, or an input file could not be read or parsed as JSON
  2  parity drift: an operation exists in one artifact and not another
  3  the OpenAPI YAML uses a construct this reader will not guess at
  4  version incoherence between contract.meta.json, OpenAPI, and the routes
  5  emission gate failed: a version, deprecation status, or sunset date is
     unresolved, or one of those fields holds an uncertainty marker

what a non-zero exit obliges you to do
  1  fix the invocation or the unreadable file, then re-run. Never hand-count
     instead.
  2  reconcile against the route inventory, which is the only executable truth
     here, then regenerate the other two artifacts and re-run.
  3  resolve the construct named on the reported line, or convert the document to
     JSON and pass it with --openapi <file>.json. Do not edit this reader to
     tolerate the construct.
  4  set one version in one place and regenerate. Do not raise a version to make
     the check pass.
  5  do not emit the pack. Report the listed operations as unresolved, name what
     would resolve each, and stop. A marker in one of these three fields is a
     gate failure by design, so it is not an escape from this exit code.
"""


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="contract_pack_audit.py",
        description="Audit a Laravel public API contract pack: route/OpenAPI/Postman "
                    "parity, version coherence, and the version/deprecation/sunset gate.",
        epilog=HELP_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--routes", metavar="FILE",
                       help="`php artisan route:list --json` output, or - for stdin")
    parser.add_argument("--openapi", metavar="FILE", help="OpenAPI .yaml, .yml or .json")
    parser.add_argument("--postman", metavar="FILE", help="Postman Collection v2.1 JSON")
    parser.add_argument("--meta", metavar="FILE", help="contract.meta.json")
    parser.add_argument("--openapi-base", metavar="PREFIX", default=None,
                       help="prefix added to OpenAPI paths before comparison "
                            "(default: inferred from the route inventory and printed)")
    parser.add_argument("--include-prefix", metavar="PREFIX", action="append", default=[],
                       help="only audit operations under this path prefix; repeatable")
    parser.add_argument("--exclude", metavar="GLOB", action="append", default=[],
                       help="skip operations matching this glob on `METHOD /path`; repeatable")
    parser.add_argument("--no-gate", action="store_true",
                       help="run parity and version checks only")
    parser.add_argument("--json", action="store_true", dest="as_json",
                       help="emit findings as JSON")
    parser.add_argument("--self-test", action="store_true",
                       help="run the built-in fixtures and exit")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()
    if not any((args.routes, args.openapi, args.postman, args.meta)):
        parser.print_usage(sys.stderr)
        sys.stderr.write("error: give at least one of --routes/--openapi/--postman/--meta\n")
        return EXIT_USAGE

    findings, notes = [], []
    routes = load_routes(args.routes) if args.routes else set()
    postman = load_postman(args.postman) if args.postman else set()
    oa_ops, info_version = {}, None
    if args.openapi:
        try:
            oa_ops, info_version = load_openapi(args.openapi)
        except Unparsable as exc:
            sys.stderr.write("%s: %s\n" % (args.openapi, exc))
            return EXIT_UNPARSABLE

    base = infer_openapi_base(oa_ops, routes, args.openapi_base) if oa_ops else ""
    if oa_ops:
        notes.append("openapi_base=%r" % base)
    oa_norm = {(meth, norm_path(base + path)) for meth, path in oa_ops}

    counts = check_parity(routes, oa_norm, postman, args.include_prefix, args.exclude, findings)
    if args.meta:
        check_version(read_json(args.meta), info_version, routes, findings)
    if oa_ops and not args.no_gate:
        gated = check_gate(oa_ops, base, args.include_prefix, args.exclude, findings)
        notes.append("gated_operations=%d" % gated)

    code = max([f[0] for f in findings], default=EXIT_OK)
    if args.as_json:
        print(json.dumps({"exit_code": code, "counts": counts, "notes": notes,
                          "findings": [{"exit": f[0], "rule": f[1], "subject": f[2]}
                                       for f in findings]}, indent=2, sort_keys=True))
    else:
        print("counts: " + ", ".join("%s=%d" % kv for kv in sorted(counts.items())))
        for note in notes:
            print("note: " + note)
        for exit_code, rule, subject in findings:
            print("[%d] %s: %s" % (exit_code, rule, subject))
        print("findings: %d, exit: %d" % (len(findings), code))
    return code


SELF_OPENAPI = '''openapi: 3.1.0
info:
  title: Fixture
  version: 1.2.3
paths:
  /health:
    get:
      operationId: getHealth
      responses:
        "200":
          description: |
            A block scalar that contains
            get: not-an-operation
            deprecated: not-a-field
  /v3/things:
    get:
      deprecated: false
      responses:
        "200":
          description: ok
    post:
      deprecated: true
      x-sunset-date: NEEDS_BACKEND_CONFIRMATION
      responses:
        "201":
          description: made
  /v3/things/{thing_id}:
    delete:
      responses:
        "204":
          description: gone
  /things/{thing_id}:
    patch:
      x-api-version: v3
      deprecated: false
      responses:
        "200":
          description: ok
'''

SELF_ROUTES = json.dumps([
    {"method": "GET|HEAD", "uri": "api/health", "name": "api.health"},
    {"method": "GET|HEAD", "uri": "api/v3/things", "name": "things.index"},
    {"method": "POST", "uri": "api/v3/things", "name": "things.store"},
    {"method": "PATCH", "uri": "api/things/{thing_id}", "name": "things.update"},
    {"method": "DELETE", "uri": "api/v3/things/{thing_id}", "name": "things.destroy"},
])

SELF_POSTMAN = json.dumps({
    "info": {"name": "Fixture", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
    "item": [
        {"name": "ops", "item": [
            {"name": "health", "request": {"method": "GET", "url": {"raw": "{{baseUrl}}/api/health",
                                                                    "path": ["api", "health"]}}}]},
        {"name": "list", "request": {"method": "GET", "url": {"raw": "{{baseUrl}}/api/v3/things"}}},
        {"name": "make", "request": {"method": "POST", "url": {"raw": "{{baseUrl}}/api/v3/things"}}},
        {"name": "patch", "request": {"method": "PATCH", "url": {"raw": "{{baseUrl}}/api/things/{{thingId}}"}}},
    ],
})


DEEP_REF = '''paths:
  /a:
    get:
      deprecated: false
      x-api-version: v1
      responses:
        "200":
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Thing"
'''


def self_test():
    import os
    import tempfile

    results = []

    def check(name, got, want):
        results.append((name, got == want, got, want))

    check("norm_path erases parameter spelling",
          (norm_path("api/v3/x/{course_id}"), norm_path("/api/v3/x/{{courseId}}"), norm_path("/api/v3/x/:course")),
          ("/api/v3/x/{}",) * 3)
    check("norm_path strips scheme, host, query and trailing slash",
          norm_path("https://h.test/api/v3/x/?a=1"), "/api/v3/x")

    tmp = tempfile.mkdtemp(prefix="contract-pack-audit-")
    paths = {}
    for name, body in (("openapi.yaml", SELF_OPENAPI), ("routes.json", SELF_ROUTES),
                       ("postman.json", SELF_POSTMAN),
                       ("meta.json", json.dumps({"contract_version": "1.0.0", "api_version": "v9"})),
                       ("deepref.yaml", DEEP_REF)):
        paths[name] = os.path.join(tmp, name)
        with open(paths[name], "w", encoding="utf-8") as fh:
            fh.write(body)

    ops, info_version = load_openapi(paths["openapi.yaml"])
    check("yaml scan finds every operation and no block-scalar ghost",
          sorted(label(o) for o in ops),
          ["DELETE /v3/things/{thing_id}", "GET /health", "GET /v3/things",
           "PATCH /things/{thing_id}", "POST /v3/things"])
    check("a deep schema $ref is ordinary and does not stop the scan",
          sorted(label(o) for o in load_openapi(paths["deepref.yaml"])[0]), ["GET /a"])
    check("yaml scan reads operation scalars, not description children",
          (ops[("post", "/v3/things")].get("deprecated"),
           ops[("post", "/v3/things")].get("x-sunset-date"),
           ops[("get", "/health")]),
          ("true", "NEEDS_BACKEND_CONFIRMATION", {"operationId": "getHealth"}))
    check("info.version is read", info_version, "1.2.3")

    for bad, why in (("paths: {}\n", "flow style"),
                     ("paths:\n  /a:\n    $ref: './a.yaml'\n", "$ref path item"),
                     ("paths:\n  /a:\n    get:\n      $ref: './g.yaml'\n", "$ref operation body"),
                     ("paths:\n  /a:\n\t    get: {}\n", "tab indent"),
                     ("info:\n  version: 1\n", "no paths block")):
        try:
            scan_openapi_yaml(bad)
            check("refuses to guess at " + why, "parsed", "Unparsable")
        except Unparsable:
            check("refuses to guess at " + why, "Unparsable", "Unparsable")

    routes = load_routes(paths["routes.json"])
    check("route:list HEAD is not a compared method",
          sorted(label(o) for o in routes),
          ["DELETE /api/v3/things/{}", "GET /api/health", "GET /api/v3/things",
           "PATCH /api/things/{}", "POST /api/v3/things"])
    postman = load_postman(paths["postman.json"])
    check("postman reads nested folders and strips {{baseUrl}}",
          sorted(label(o) for o in postman),
          ["GET /api/health", "GET /api/v3/things", "PATCH /api/things/{}", "POST /api/v3/things"])

    base = infer_openapi_base(ops, routes, None)
    check("openapi base is inferred as the shortest best-matching prefix", base, "/api")
    check("explicit --openapi-base overrides inference",
          infer_openapi_base(ops, routes, "/api/v3"), "/api/v3")

    oa_norm = {(m, norm_path(base + p)) for m, p in ops}
    findings = []
    counts = check_parity(routes, oa_norm, postman, [], [], findings)
    absent = []
    check_parity(set(), oa_norm, postman, [], [], absent)
    check("an unsupplied route inventory is not an empty truth",
          [f for f in absent if f[1].endswith("_openapi") or f[1].endswith("_postman")], [])
    check("parity counts the three artifacts",
          (counts["routes"], counts["openapi"], counts["postman"]), (5, 5, 4))
    check("parity names the route the collection never got",
          sorted(f[2] for f in findings if f[1] == "missing_in_postman"),
          ["DELETE /api/v3/things/{}"])
    excluded = []
    check_parity(routes, oa_norm, postman, [], ["DELETE *"], excluded)
    check("parity exclusion glob is honoured", excluded, [])

    findings = []
    gated = check_gate(ops, base, [], [], findings)
    rules = sorted(f[1] for f in findings)
    check("gate skips operational probes", gated, 4)
    check("gate catches the marker, the missing status, and the unresolved sunset",
          rules, ["deprecation_unresolved", "marker_in_contract_field", "sunset_unresolved"])
    check("gate accepts x-api-version in place of a /vN segment",
          [f for f in findings if f[1] == "version_unresolved"], [])
    check("every gate finding exits 5", {f[0] for f in findings}, {EXIT_GATE})

    findings = []
    check_version(read_json(paths["meta.json"]), info_version, routes, findings)
    check("version check catches info.version drift and a wrong api_version",
          sorted(f[1] for f in findings),
          ["api_version_not_in_routes", "openapi_info_version_drift"])

    for name in paths.values():
        os.remove(name)
    os.rmdir(tmp)

    failed = 0
    for name, ok, got, want in results:
        print("%-4s %s" % ("PASS" if ok else "FAIL", name))
        if not ok:
            failed += 1
            print("       got:  %r" % (got,))
            print("       want: %r" % (want,))
    print("%d checks, %d failed" % (len(results), failed))
    return EXIT_OK if failed == 0 else EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main())
