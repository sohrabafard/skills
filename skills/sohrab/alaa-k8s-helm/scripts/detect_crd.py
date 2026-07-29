#!/usr/bin/env python3
"""Classify every document in a YAML file as Kubernetes, OpenShift, or custom.

The script is resilient to a syntax error in one document of a multi-document
file: it parses each document independently so one bad document does not hide
the rest. It does **not** treat a parse error as success. A file whose documents
could not be parsed exits 1 with the errors listed, because a caller that
branches on exit status must not read total parse failure as a clean verdict.

Exit codes, shared by every script in this skill:
    0  every document parsed and every apiVersion is a standard Kubernetes one
    1  findings: a document failed to parse, or a non-standard apiVersion was found
    2  could not run: missing PyYAML, bad usage, or an unreadable path

Windows: pure Python 3 plus PyYAML; input is read with universal newlines so a
CRLF checkout cannot change a classification.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_CANNOT_RUN = 2

SCRIPT_PATH = os.path.abspath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
FIXTURE_DIR = os.path.join(SCRIPT_DIR, "fixtures")

try:
    import yaml
except ImportError:  # pragma: no cover
    print("detect_crd: PyYAML is required. Run scripts/detect_crd_wrapper.sh instead.",
          file=sys.stderr)
    sys.exit(EXIT_CANNOT_RUN)

# Standard, currently served Kubernetes API versions. Anything outside this set
# is reported so a human decides. Keep it aligned with
# references/version-awareness.md, which is the only place a version claim lives.
STANDARD_API_VERSIONS = {
    "v1",
    "apps/v1",
    "batch/v1",
    "networking.k8s.io/v1",
    "policy/v1",
    "rbac.authorization.k8s.io/v1",
    "storage.k8s.io/v1",
    "autoscaling/v1",
    "autoscaling/v2",
    "apiextensions.k8s.io/v1",
    "certificates.k8s.io/v1",
    "admissionregistration.k8s.io/v1",
    "coordination.k8s.io/v1",
    "discovery.k8s.io/v1",
    "events.k8s.io/v1",
    "flowcontrol.apiserver.k8s.io/v1",
    "node.k8s.io/v1",
    "scheduling.k8s.io/v1",
    "snapshot.storage.k8s.io/v1",
    "authentication.k8s.io/v1",
    "authorization.k8s.io/v1",
    "apiregistration.k8s.io/v1",
    "gateway.networking.k8s.io/v1",
    "gateway.networking.k8s.io/v1beta1",
    # Dynamic Resource Allocation went GA in 1.34; v1beta1 is retained because
    # clusters on 1.34 and older still serve it.
    "resource.k8s.io/v1",
    "resource.k8s.io/v1beta1",
}

# apiVersions that were removed upstream. Emitting one is a hard error, not a
# classification, because the API server rejects it outright.
REMOVED_API_VERSIONS = {
    "policy/v1beta1": "removed in Kubernetes 1.25",
    "autoscaling/v2beta1": "removed in Kubernetes 1.26",
    "autoscaling/v2beta2": "removed in Kubernetes 1.26",
    "batch/v1beta1": "CronJob moved to batch/v1 in 1.21 and v1beta1 was removed in 1.25",
    "flowcontrol.apiserver.k8s.io/v1beta3": "removed in Kubernetes 1.32",
}


class CouldNotRun(Exception):
    pass


def read_text(path: str) -> str:
    if not os.path.isfile(path):
        raise CouldNotRun(f"file not found: {path}")
    try:
        with open(path, "r", encoding="utf-8", newline=None) as handle:
            return handle.read()
    except (OSError, UnicodeDecodeError) as exc:
        raise CouldNotRun(f"cannot read {path}: {exc}") from exc


def split_yaml_documents(content: str) -> list[dict[str, Any]]:
    documents: list[dict[str, Any]] = []
    current: list[str] = []
    start = 1
    for line_num, line in enumerate(content.splitlines(), start=1):
        if line.strip() == "---":
            text = "\n".join(current)
            if text.strip():
                documents.append({"content": text, "start_line": start})
            current = []
            start = line_num + 1
        else:
            current.append(line)
    text = "\n".join(current)
    if text.strip():
        documents.append({"content": text, "start_line": start})
    return documents


def parse_yaml_file(path: str) -> tuple[list[Any], list[dict[str, Any]]]:
    content = read_text(path)
    try:
        return list(yaml.safe_load_all(content)), []
    except yaml.YAMLError:
        pass

    documents: list[Any] = []
    errors: list[dict[str, Any]] = []
    for index, info in enumerate(split_yaml_documents(content), start=1):
        try:
            parsed = yaml.safe_load(info["content"])
            if parsed is not None:
                documents.append(parsed)
        except yaml.YAMLError as exc:
            message = str(exc)
            match = re.search(r"line (\d+)", message)
            error_line = info["start_line"]
            if match:
                error_line = info["start_line"] + int(match.group(1)) - 1
            errors.append({
                "document": index,
                "start_line": info["start_line"],
                "error_line": error_line,
                "error": message,
            })
    return documents, errors


def classify(api_version: str) -> str:
    group = api_version.split("/")[0] if "/" in api_version else "core"
    if api_version in REMOVED_API_VERSIONS:
        return "removed"
    if api_version in STANDARD_API_VERSIONS:
        return "kubernetes"
    if group.endswith(".openshift.io"):
        return "openshift"
    return "custom"


def resource_info(doc: Any) -> dict[str, Any] | None:
    if not isinstance(doc, dict):
        return None
    kind = doc.get("kind")
    api_version = doc.get("apiVersion")
    if not kind or not api_version:
        return None
    platform = classify(api_version)
    metadata = doc.get("metadata") or {}
    if not isinstance(metadata, dict):
        metadata = {}
    info = {
        "kind": kind,
        "apiVersion": api_version,
        "group": api_version.split("/")[0] if "/" in api_version else "core",
        "version": api_version.split("/")[-1],
        "platform": platform,
        "isCustomResource": platform == "custom",
        "isOpenShiftResource": platform == "openshift",
        "name": metadata.get("name", "unnamed"),
        "namespace": metadata.get("namespace"),
    }
    if platform == "removed":
        info["removalNote"] = REMOVED_API_VERSIONS[api_version]
    return info


def analyse(path: str) -> tuple[dict, int]:
    documents, parse_errors = parse_yaml_file(path)
    resources = [info for doc in documents if (info := resource_info(doc))]
    if not documents and not parse_errors:
        raise CouldNotRun(
            f"{path} contains no YAML document; a classifier cannot return a verdict on it"
        )
    output = {
        "resources": resources,
        "parseErrors": parse_errors,
        "summary": {
            "totalDocuments": len(documents) + len(parse_errors),
            "parsedSuccessfully": len(documents),
            "parseErrors": len(parse_errors),
            "customResources": sum(1 for r in resources if r["platform"] == "custom"),
            "openShiftResources": sum(1 for r in resources if r["platform"] == "openshift"),
            "removedApiVersions": sum(1 for r in resources if r["platform"] == "removed"),
        },
    }
    findings = (len(parse_errors)
                + output["summary"]["customResources"]
                + output["summary"]["openShiftResources"]
                + output["summary"]["removedApiVersions"])
    return output, findings


def self_test() -> int:
    failures: list[str] = []
    cases = [
        ("clean.yaml", EXIT_CLEAN),
        ("removed-apis.yaml", EXIT_FINDINGS),
        ("unparsable.yaml", EXIT_FINDINGS),
    ]
    for fixture, expected in cases:
        path = os.path.join(FIXTURE_DIR, fixture)
        try:
            _, findings = analyse(path)
        except CouldNotRun as exc:
            failures.append(f"{fixture}: could not run: {exc}")
            continue
        actual = EXIT_FINDINGS if findings else EXIT_CLEAN
        if actual != expected:
            failures.append(f"{fixture}: expected exit {expected}, computed {actual}")

    try:
        analyse(os.path.join(FIXTURE_DIR, "no-such-file.yaml"))
    except CouldNotRun:
        pass
    else:
        failures.append("a missing file returned a verdict instead of could-not-run")

    crlf = os.path.join(FIXTURE_DIR, "bad-deployment-crlf.yaml")
    lf = os.path.join(FIXTURE_DIR, "bad-deployment.yaml")
    if os.path.isfile(crlf):
        if analyse(crlf)[0]["summary"] != analyse(lf)[0]["summary"]:
            failures.append("CRLF input changed the classification summary")
    else:
        failures.append("fixtures/bad-deployment-crlf.yaml is missing")

    if failures:
        for line in failures:
            print(f"SELF-TEST FAIL: {line}", file=sys.stderr)
        return EXIT_FINDINGS
    print("detect_crd --self-test: 5 cases passed")
    return EXIT_CLEAN


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="detect_crd.py",
        description="Classify each YAML document as a standard Kubernetes, OpenShift, "
                    "custom, or removed API version, and report parse errors as findings.",
        epilog="Exit codes: 0 all standard and parsed, 1 findings, 2 could not run.",
    )
    parser.add_argument("yaml_file", nargs="?", help="path to a YAML file")
    parser.add_argument("--self-test", action="store_true",
                        help="run the shipped fixtures and exit")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.yaml_file:
        print("detect_crd: a YAML file is required (or --self-test)", file=sys.stderr)
        return EXIT_CANNOT_RUN
    try:
        output, findings = analyse(args.yaml_file)
    except CouldNotRun as exc:
        print(f"detect_crd: could not run: {exc}", file=sys.stderr)
        return EXIT_CANNOT_RUN
    print(json.dumps(output, indent=2))
    if findings:
        print(f"detect_crd: {findings} document(s) need a human decision "
              f"(parse errors, OpenShift, custom, or removed API versions)", file=sys.stderr)
        return EXIT_FINDINGS
    return EXIT_CLEAN


if __name__ == "__main__":
    sys.exit(main())
