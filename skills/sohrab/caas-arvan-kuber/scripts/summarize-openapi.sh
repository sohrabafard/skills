#!/usr/bin/env bash
set -euo pipefail

# Summarize Arvan CaaS OpenAPI capabilities for agent workflows.
# Usage:
#   bash summarize-openapi.sh [openapi-file]
#
# Example:
#   bash summarize-openapi.sh ../arvann-caas-openAPI-1.25.json

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_SPEC="${SCRIPT_DIR}/../references/arvan-caas-openAPI-1.25.json"
SPEC_FILE="${1:-${DEFAULT_SPEC}}"

if [[ ! -f "${SPEC_FILE}" ]]; then
  echo "ERROR: spec file not found: ${SPEC_FILE}" >&2
  exit 1
fi

PY=""
if command -v python3 >/dev/null 2>&1; then
  PY="python3"
elif command -v python >/dev/null 2>&1; then
  PY="python"
else
  echo "ERROR: python3/python not found in PATH." >&2
  exit 1
fi

"${PY}" - "${SPEC_FILE}" <<'PYCODE'
import json
import re
import sys
from collections import defaultdict

spec_path = sys.argv[1]
with open(spec_path, "r", encoding="utf-8") as f:
    doc = json.load(f)

paths = doc.get("paths", {})
total_paths = len(paths)
with_ns = sum(1 for p in paths if "/namespaces/{namespace}" in p)

ops_count = 0
for p in paths.values():
    for m in ("get", "post", "put", "patch", "delete"):
        if m in p:
            ops_count += 1

resource_ops = defaultdict(lambda: {"collection": set(), "item": set(), "subs": defaultdict(set)})

for path, pobj in paths.items():
    m_core = re.match(r"^/api/v1/namespaces/\{namespace\}/([^/]+)(?:/\{name\})?(?:/([^/]+))?$", path)
    if m_core:
        group = "core/v1"
        resource = m_core.group(1)
        sub = m_core.group(2) or ""
    else:
        m_api = re.match(
            r"^/apis/([^/]+)/([^/]+)/namespaces/\{namespace\}/([^/]+)(?:/\{name\})?(?:/([^/]+))?$",
            path,
        )
        if not m_api:
            continue
        group = f"{m_api.group(1)}/{m_api.group(2)}"
        resource = m_api.group(3)
        sub = m_api.group(4) or ""

    key = f"{group}/{resource}"
    has_name = "/{name}" in path

    for method in ("get", "post", "put", "patch", "delete"):
        if method not in pobj:
            continue
        if not has_name:
            resource_ops[key]["collection"].add(method)
        elif not sub:
            resource_ops[key]["item"].add(method)
        else:
            resource_ops[key]["subs"][sub].add(method)

print(f"Spec: {spec_path}")
print(f"OpenAPI: {doc.get('openapi')}")
print(f"Title: {doc.get('info', {}).get('title')}")
print(f"Version: {doc.get('info', {}).get('version')}")
print(f"Paths: {total_paths}")
print(f"Operations: {ops_count}")
print(f"Namespaced paths: {with_ns}/{total_paths}")

servers = doc.get("servers") or []
if servers:
    print("Servers:")
    for s in servers:
        print(f"  - {s.get('url')}")

print("\nResources:")
for key in sorted(resource_ops):
    data = resource_ops[key]
    c = ",".join(sorted(data["collection"])) or "-"
    i = ",".join(sorted(data["item"])) or "-"
    if data["subs"]:
        subs = "; ".join(
            f"{name}=[{','.join(sorted(methods))}]"
            for name, methods in sorted(data["subs"].items())
        )
    else:
        subs = "-"
    print(f"- {key} | collection=[{c}] | item=[{i}] | sub={subs}")
PYCODE
