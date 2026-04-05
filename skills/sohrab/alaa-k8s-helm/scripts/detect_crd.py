#!/usr/bin/env python3
"""Detect standard Kubernetes, OpenShift, and custom resources in YAML files.

The script is resilient to syntax errors in multi-document YAML. It parses each
valid document independently so one bad document does not hide the rest.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print(
        "PyYAML is required. Run with scripts/detect_crd_wrapper.sh if needed.",
        file=sys.stderr,
    )
    sys.exit(1)

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
    "resource.k8s.io/v1beta1",
}


def split_yaml_documents(content: str) -> list[dict[str, Any]]:
    documents: list[dict[str, Any]] = []
    current_doc: list[str] = []
    current_start_line = 1

    for line_num, line in enumerate(content.splitlines(), start=1):
        if line.strip() == "---":
            if current_doc:
                doc_content = "\n".join(current_doc)
                if doc_content.strip():
                    documents.append({"content": doc_content, "start_line": current_start_line})
            current_doc = []
            current_start_line = line_num + 1
        else:
            current_doc.append(line)

    if current_doc:
        doc_content = "\n".join(current_doc)
        if doc_content.strip():
            documents.append({"content": doc_content, "start_line": current_start_line})

    return documents


def parse_yaml_file(file_path: Path) -> tuple[list[Any], list[dict[str, Any]]]:
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover - minimal utility
        return [], [{"document": 0, "error": str(exc)}]

    try:
        return list(yaml.safe_load_all(content)), []
    except yaml.YAMLError:
        pass

    documents: list[Any] = []
    errors: list[dict[str, Any]] = []
    for index, doc_info in enumerate(split_yaml_documents(content), start=1):
        try:
            parsed = yaml.safe_load(doc_info["content"])
            if parsed is not None:
                documents.append(parsed)
        except yaml.YAMLError as exc:
            message = str(exc)
            line_match = re.search(r"line (\d+)", message)
            error_line = doc_info["start_line"]
            if line_match:
                error_line = doc_info["start_line"] + int(line_match.group(1)) - 1
            errors.append(
                {
                    "document": index,
                    "start_line": doc_info["start_line"],
                    "error_line": error_line,
                    "error": message,
                }
            )
    return documents, errors


def classify_resource(api_version: str) -> str:
    group = api_version.split("/")[0] if "/" in api_version else "core"
    if api_version in STANDARD_API_VERSIONS:
        return "kubernetes"
    if group.endswith(".openshift.io") or group in {"route.openshift.io", "security.openshift.io"}:
        return "openshift"
    return "custom"


def extract_resource_info(doc: Any) -> dict[str, Any] | None:
    if not isinstance(doc, dict):
        return None
    kind = doc.get("kind")
    api_version = doc.get("apiVersion")
    if not kind or not api_version:
        return None

    group = api_version.split("/")[0] if "/" in api_version else "core"
    version = api_version.split("/")[-1]
    platform = classify_resource(api_version)
    metadata = doc.get("metadata") or {}
    return {
        "kind": kind,
        "apiVersion": api_version,
        "group": group,
        "version": version,
        "platform": platform,
        "isCustomResource": platform == "custom",
        "isOpenShiftResource": platform == "openshift",
        "name": metadata.get("name", "unnamed"),
        "namespace": metadata.get("namespace"),
    }


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: detect_crd.py <yaml-file>", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)

    documents, parse_errors = parse_yaml_file(path)
    resources = [info for doc in documents if (info := extract_resource_info(doc))]

    output = {
        "resources": resources,
        "parseErrors": parse_errors,
        "summary": {
            "totalDocuments": len(documents) + len(parse_errors),
            "parsedSuccessfully": len(documents),
            "parseErrors": len(parse_errors),
            "customResources": sum(1 for item in resources if item["platform"] == "custom"),
            "openShiftResources": sum(1 for item in resources if item["platform"] == "openshift"),
        },
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
