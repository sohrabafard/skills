#!/usr/bin/env bash
# Read the vendored Arvan CaaS OpenAPI document and keep the capability matrix
# honest about it.
#
# Three copies of the same machine-derivable facts used to exist -- the spec, the
# hand-written matrix, and a transcription in SKILL.md -- and nothing compared
# them. `--check` compares them and fails when they have drifted apart.
#
# Requires bash 4.0 or newer plus python3 (or python 3.x). On Windows use Git
# Bash or WSL; the embedded Python is what does the work, so it is portable.
# Every file is read with universal newlines, so a CRLF checkout cannot make a
# matching block look different.
#
# Exit codes, shared by every script in this skill:
#   0  clean: the printed summary succeeded, or --check found no drift
#   1  findings: --check found drift, a missing capture stamp, or a re-introduced
#      transcription in SKILL.md
#   2  could not run: no spec, no python, an unparsable spec, or a matrix file
#      with no generated block
set -uo pipefail

EXIT_CLEAN=0
EXIT_FINDINGS=1
EXIT_CANNOT_RUN=2

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "${SCRIPT_DIR}")"
DEFAULT_SPEC="${SKILL_DIR}/references/arvan-caas-openAPI-1.25.json"
DEFAULT_MATRIX="${SKILL_DIR}/references/arvan-capability-matrix.md"
DEFAULT_BODY="${SKILL_DIR}/SKILL.md"

usage() {
  cat <<'EOF'
Usage:
  summarize-openapi.sh [--spec FILE]                 print the summary to stdout
  summarize-openapi.sh --check  [--spec FILE] [--matrix FILE] [--body FILE]
  summarize-openapi.sh --update [--spec FILE] [--matrix FILE]
  summarize-openapi.sh --help
  summarize-openapi.sh --self-test

Modes:
  (default)   print the machine-derived summary; changes nothing
  --check     regenerate the block and compare it with the one committed in the
              matrix; also require a capture stamp in the matrix and refuse a
              re-introduced metadata transcription in SKILL.md
  --update    rewrite the generated block in the matrix in place, then exit 0

Defaults resolve from this script's own location:
  spec    ../references/arvan-caas-openAPI-1.25.json
  matrix  ../references/arvan-capability-matrix.md
  body    ../SKILL.md

Example:
  bash scripts/summarize-openapi.sh --check

Exit codes: 0 clean, 1 findings, 2 could not run.
EOF
}

find_python() {
  local candidate
  for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1 &&
       "$candidate" -c 'import sys; sys.exit(0 if sys.version_info[0] == 3 else 1)' >/dev/null 2>&1; then
      printf '%s' "$candidate"
      return 0
    fi
  done
  return 1
}

run_python() {
  local py
  if ! py="$(find_python)"; then
    echo "summarize-openapi: python3 is required and was not found on PATH" >&2
    return ${EXIT_CANNOT_RUN}
  fi
  "$py" - "$@" <<'PYCODE'
import json
import os
import re
import sys

EXIT_CLEAN, EXIT_FINDINGS, EXIT_CANNOT_RUN = 0, 1, 2

BEGIN = "<!-- BEGIN GENERATED: summarize-openapi.sh -->"
END = "<!-- END GENERATED -->"
METHODS = ("get", "post", "put", "patch", "delete")


def die(message):
    print(f"summarize-openapi: could not run: {message}", file=sys.stderr)
    raise SystemExit(EXIT_CANNOT_RUN)


def read_text(path, what):
    if not os.path.isfile(path):
        die(f"{what} not found: {path}")
    try:
        with open(path, "r", encoding="utf-8", newline=None) as handle:
            return handle.read()
    except (OSError, UnicodeDecodeError) as exc:
        die(f"cannot read {what} {path}: {exc}")


def load_spec(path):
    text = read_text(path, "spec file")
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        die(f"{path} is not parsable JSON: {exc}")


def summarise(doc):
    paths = doc.get("paths")
    if not isinstance(paths, dict) or not paths:
        die("the spec has no `paths` object; nothing can be derived from it")

    total = len(paths)
    namespaced = sum(1 for p in paths if "/namespaces/{namespace}" in p)
    operations = sum(1 for p in paths.values() for m in METHODS if m in p)

    resources = {}
    for path, node in paths.items():
        core = re.match(r"^/api/v1/namespaces/\{namespace\}/([^/]+)(?:/\{name\})?(?:/([^/]+))?$", path)
        if core:
            group, resource, sub = "core/v1", core.group(1), core.group(2) or ""
        else:
            other = re.match(
                r"^/apis/([^/]+)/([^/]+)/namespaces/\{namespace\}/([^/]+)(?:/\{name\})?(?:/([^/]+))?$",
                path,
            )
            if not other:
                continue
            group = f"{other.group(1)}/{other.group(2)}"
            resource, sub = other.group(3), other.group(4) or ""

        key = f"{group}/{resource}"
        entry = resources.setdefault(key, {"collection": set(), "item": set(), "subs": {}})
        has_name = "/{name}" in path
        for method in METHODS:
            if method not in node:
                continue
            if not has_name:
                entry["collection"].add(method)
            elif not sub:
                entry["item"].add(method)
            else:
                entry["subs"].setdefault(sub, set()).add(method)

    return {
        "openapi": doc.get("openapi"),
        "title": (doc.get("info") or {}).get("title"),
        "version": (doc.get("info") or {}).get("version"),
        "paths": total,
        "operations": operations,
        "namespaced": namespaced,
        "servers": [s.get("url") for s in (doc.get("servers") or []) if isinstance(s, dict)],
        "resources": resources,
    }


def render_block(summary):
    lines = [
        BEGIN,
        f"- `openapi`: `{summary['openapi']}`",
        f"- `info.title`: `{summary['title']}`",
        f"- `info.version`: `{summary['version']}`",
        f"- Paths: `{summary['paths']}`",
        f"- Operations: `{summary['operations']}`",
        f"- Namespaced paths: `{summary['namespaced']}/{summary['paths']}`",
    ]
    if summary["servers"]:
        lines.append("- Servers:")
        for url in summary["servers"]:
            lines.append(f"  - `{url}`")
    lines.append("")
    lines.append("| API resource | Collection | Item | Subresources |")
    lines.append("|---|---|---|---|")
    for key in sorted(summary["resources"]):
        data = summary["resources"][key]
        collection = "[" + ",".join(sorted(data["collection"])) + "]" if data["collection"] else "-"
        item = "[" + ",".join(sorted(data["item"])) + "]" if data["item"] else "-"
        if data["subs"]:
            subs = "; ".join(
                f"{name}=[{','.join(sorted(methods))}]"
                for name, methods in sorted(data["subs"].items())
            )
        else:
            subs = "-"
        lines.append(f"| `{key}` | `{collection}` | `{item}` | `{subs}` |")
    lines.append(END)
    return "\n".join(lines)


def extract_block(matrix_text, path):
    start = matrix_text.find(BEGIN)
    end = matrix_text.find(END)
    if start == -1 or end == -1 or end < start:
        die(f"{path} has no generated block delimited by the BEGIN and END markers; "
            "add them, or run --update against a matrix that has them")
    return matrix_text[start:end + len(END)]


def print_summary(summary):
    print(f"OpenAPI: {summary['openapi']}")
    print(f"Title: {summary['title']}")
    print(f"Version: {summary['version']}")
    print(f"Paths: {summary['paths']}")
    print(f"Operations: {summary['operations']}")
    print(f"Namespaced paths: {summary['namespaced']}/{summary['paths']}")
    for url in summary["servers"]:
        print(f"Server: {url}")
    print()
    for key in sorted(summary["resources"]):
        data = summary["resources"][key]
        collection = ",".join(sorted(data["collection"])) or "-"
        item = ",".join(sorted(data["item"])) or "-"
        subs = "; ".join(
            f"{name}=[{','.join(sorted(methods))}]"
            for name, methods in sorted(data["subs"].items())
        ) or "-"
        print(f"- {key} | collection=[{collection}] | item=[{item}] | sub={subs}")


CAPTURE_STAMP = re.compile(r"^\s*-\s+\*\*(Spec capture date|Matrix last reconciled|Vendor cross-check)",
                           re.MULTILINE)
# A metadata transcription in the always-loaded body is the third copy this
# script exists to prevent. Any of these lines outside the matrix is drift.
BODY_TRANSCRIPTION = re.compile(
    r"(^|\n)\s*[-*|]\s*`?(info\.version|info\.title|openapi)`?\s*[:|]"
    r"|(^|\n)\s*[-*|]\s*(Paths|Operations|Namespaced paths)\s*:\s*`?\d+",
    re.IGNORECASE,
)


def main():
    mode = sys.argv[1]
    spec_path = sys.argv[2]
    matrix_path = sys.argv[3]
    body_path = sys.argv[4]

    summary = summarise(load_spec(spec_path))

    if mode == "print":
        print_summary(summary)
        return EXIT_CLEAN

    generated = render_block(summary)

    if mode == "update":
        matrix_text = read_text(matrix_path, "matrix file")
        committed = extract_block(matrix_text, matrix_path)
        if committed == generated:
            print(f"summarize-openapi: {matrix_path} generated block already matches the spec")
            return EXIT_CLEAN
        with open(matrix_path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(matrix_text.replace(committed, generated))
        print(f"summarize-openapi: rewrote the generated block in {matrix_path}; "
              "review the diff and commit it")
        return EXIT_CLEAN

    if mode == "check":
        findings = []
        matrix_text = read_text(matrix_path, "matrix file")
        committed = extract_block(matrix_text, matrix_path)
        if committed != generated:
            expected = committed.splitlines()
            actual = generated.splitlines()
            findings.append(
                f"{matrix_path}: the generated block does not match {spec_path}. "
                f"Committed block has {len(expected)} lines, the spec produces {len(actual)}."
            )
            for index in range(max(len(expected), len(actual))):
                old = expected[index] if index < len(expected) else "<missing>"
                new = actual[index] if index < len(actual) else "<missing>"
                if old != new:
                    findings.append(f"  line {index + 1}: committed {old!r}")
                    findings.append(f"  line {index + 1}: spec says {new!r}")
        if not CAPTURE_STAMP.search(matrix_text):
            findings.append(
                f"{matrix_path}: no capture stamp. The matrix must state when the spec was "
                "captured, when the block was last reconciled, and when the vendor docs were "
                "last cross-checked."
            )
        if os.path.isfile(body_path):
            body_text = read_text(body_path, "body file")
            if BODY_TRANSCRIPTION.search(body_text):
                findings.append(
                    f"{body_path}: the always-loaded body transcribes spec metadata again. "
                    "The body carries the conclusion; the numbers live only in the matrix's "
                    "generated block."
                )
        if findings:
            for line in findings:
                print(line)
            print("summarize-openapi: the spec, the matrix, and the body have drifted apart; "
                  "run --update and re-read the body", file=sys.stderr)
            return EXIT_FINDINGS
        print("summarize-openapi: spec, matrix, and body agree")
        return EXIT_CLEAN

    die(f"unknown mode {mode!r}")


raise SystemExit(main())
PYCODE
  return $?
}

self_test() {
  local fixtures="${SCRIPT_DIR}/fixtures" failures=0 rc

  ( main --help >/dev/null 2>&1 )
  [[ $? -eq ${EXIT_CLEAN} ]] || { echo "SELF-TEST FAIL: --help did not exit ${EXIT_CLEAN}" >&2; failures=$((failures+1)); }

  main --check --spec "${fixtures}/mini-openapi.json" --matrix "${fixtures}/mini-matrix.md" --body "${fixtures}/mini-body.md" >/dev/null 2>&1
  rc=$?
  [[ ${rc} -eq ${EXIT_CLEAN} ]] || { echo "SELF-TEST FAIL: matching fixtures exited ${rc}, expected ${EXIT_CLEAN}" >&2; failures=$((failures+1)); }

  main --check --spec "${fixtures}/mini-openapi.json" --matrix "${fixtures}/mini-matrix-drifted.md" --body "${fixtures}/mini-body.md" >/dev/null 2>&1
  rc=$?
  [[ ${rc} -eq ${EXIT_FINDINGS} ]] || { echo "SELF-TEST FAIL: drifted matrix exited ${rc}, expected ${EXIT_FINDINGS}" >&2; failures=$((failures+1)); }

  main --check --spec "${fixtures}/mini-openapi.json" --matrix "${fixtures}/mini-matrix.md" --body "${fixtures}/mini-body-transcribing.md" >/dev/null 2>&1
  rc=$?
  [[ ${rc} -eq ${EXIT_FINDINGS} ]] || { echo "SELF-TEST FAIL: a body that re-transcribes metadata exited ${rc}, expected ${EXIT_FINDINGS}" >&2; failures=$((failures+1)); }

  main --check --spec "${fixtures}/mini-openapi.json" --matrix "${fixtures}/mini-matrix-no-stamp.md" --body "${fixtures}/mini-body.md" >/dev/null 2>&1
  rc=$?
  [[ ${rc} -eq ${EXIT_FINDINGS} ]] || { echo "SELF-TEST FAIL: a matrix with no capture stamp exited ${rc}, expected ${EXIT_FINDINGS}" >&2; failures=$((failures+1)); }

  main --check --spec "${fixtures}/no-such-spec.json" --matrix "${fixtures}/mini-matrix.md" >/dev/null 2>&1
  rc=$?
  [[ ${rc} -eq ${EXIT_CANNOT_RUN} ]] || { echo "SELF-TEST FAIL: a missing spec exited ${rc}, expected ${EXIT_CANNOT_RUN}" >&2; failures=$((failures+1)); }

  main --check --spec "${fixtures}/unparsable-openapi.json" --matrix "${fixtures}/mini-matrix.md" >/dev/null 2>&1
  rc=$?
  [[ ${rc} -eq ${EXIT_CANNOT_RUN} ]] || { echo "SELF-TEST FAIL: an unparsable spec exited ${rc}, expected ${EXIT_CANNOT_RUN}" >&2; failures=$((failures+1)); }

  main --check --spec "${fixtures}/mini-openapi.json" --matrix "${fixtures}/mini-matrix-no-markers.md" >/dev/null 2>&1
  rc=$?
  [[ ${rc} -eq ${EXIT_CANNOT_RUN} ]] || { echo "SELF-TEST FAIL: a matrix with no markers exited ${rc}, expected ${EXIT_CANNOT_RUN}" >&2; failures=$((failures+1)); }

  # A CRLF matrix must produce the same verdict as its LF twin.
  if [[ -f "${fixtures}/mini-matrix-crlf.md" ]]; then
    main --check --spec "${fixtures}/mini-openapi.json" --matrix "${fixtures}/mini-matrix-crlf.md" --body "${fixtures}/mini-body.md" >/dev/null 2>&1
    rc=$?
    [[ ${rc} -eq ${EXIT_CLEAN} ]] || { echo "SELF-TEST FAIL: a CRLF matrix exited ${rc}, expected ${EXIT_CLEAN}" >&2; failures=$((failures+1)); }
  else
    echo "SELF-TEST FAIL: fixtures/mini-matrix-crlf.md is missing" >&2; failures=$((failures+1))
  fi

  if [[ ${failures} -gt 0 ]]; then return ${EXIT_FINDINGS}; fi
  echo "summarize-openapi --self-test: 9 cases passed"
  return ${EXIT_CLEAN}
}

main() {
  local mode="print"
  local spec="${DEFAULT_SPEC}" matrix="${DEFAULT_MATRIX}" body="${DEFAULT_BODY}"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -h|--help)   usage; return ${EXIT_CLEAN} ;;
      --self-test) self_test; return $? ;;
      --check)     mode="check"; shift ;;
      --update)    mode="update"; shift ;;
      --spec)      spec="${2:-}"; shift 2 || return ${EXIT_CANNOT_RUN} ;;
      --matrix)    matrix="${2:-}"; shift 2 || return ${EXIT_CANNOT_RUN} ;;
      --body)      body="${2:-}"; shift 2 || return ${EXIT_CANNOT_RUN} ;;
      -*)          echo "summarize-openapi: unknown option: $1" >&2; usage >&2; return ${EXIT_CANNOT_RUN} ;;
      *)           spec="$1"; shift ;;
    esac
  done

  run_python "${mode}" "${spec}" "${matrix}" "${body}"
  return $?
}

main "$@"
exit $?
