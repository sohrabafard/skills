#!/usr/bin/env python3
"""Gate a rendered Kubernetes manifest set against this skill's own rules.

Nothing else in /alaa-k8s-helm ($alaa-k8s-helm) or /caas-arvan-kuber
($caas-arvan-kuber) can fail a Deployment that
ships with no resources, no probes, `privileged: true`, or a mutated selector.
This script does.

Exit codes, shared by every script in this skill:
    0  clean
    1  findings
    2  could not run (missing dependency, unreadable path, unparsable input)

Findings are printed as `file:line kind/name RULE message` so a human and a
pipeline read the same output.

Design constraints this file honours:
  * runs on Windows: pure Python 3, no shell, no POSIX-only path assumptions,
    and every input is decoded with newline normalisation so a CRLF checkout
    cannot leave a carriage return on a compared value.
  * resolves its own location from `__file__` directly, never through
    `Path(__file__).parents[N]`.
  * creates no temporary directory anywhere, so a read-only mount is fine.
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Any, Iterable

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_CANNOT_RUN = 2

SCRIPT_PATH = os.path.abspath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
FIXTURE_DIR = os.path.join(SCRIPT_DIR, "fixtures")

try:
    import yaml
except ImportError:  # pragma: no cover - environment problem, not a finding
    print(
        "check_manifests: PyYAML is required. Install it, or run "
        "scripts/detect_crd_wrapper.sh once to create the fallback environment.",
        file=sys.stderr,
    )
    sys.exit(EXIT_CANNOT_RUN)


WORKLOAD_KINDS = {"Deployment", "StatefulSet", "DaemonSet", "ReplicaSet", "Job", "CronJob"}
SELECTOR_KINDS = {"Deployment", "StatefulSet", "DaemonSet", "ReplicaSet", "Job"}
TRAFFIC_KINDS = {"Deployment", "StatefulSet", "ReplicaSet"}

# Kinds a namespace-scoped tenant on Arvan CaaS cannot create. The list is
# owned and kept current by /caas-arvan-kuber ($caas-arvan-kuber)
# references/arvan-capability-matrix.md;
# this script only enforces whatever that file says, and `--profile arvan`
# turns the enforcement on.
ARVAN_ABSENT_KINDS = {
    "DaemonSet",
    "NetworkPolicy",
    "PodDisruptionBudget",
    "StorageClass",
    "ClusterRole",
    "ClusterRoleBinding",
    "CustomResourceDefinition",
    "Route",
    "BuildConfig",
}


class LineLoader(yaml.SafeLoader):
    """SafeLoader that records the 1-based source line of every mapping."""


def _construct_mapping(loader: LineLoader, node: yaml.Node, deep: bool = False) -> dict:
    mapping = yaml.SafeLoader.construct_mapping(loader, node, deep=deep)
    mapping["__line__"] = node.start_mark.line + 1
    return mapping


LineLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


class CouldNotRun(Exception):
    """Raised for anything that makes a verdict impossible."""


class Finding:
    def __init__(self, path: str, line: int, subject: str, rule: str, message: str) -> None:
        self.path = path
        self.line = line
        self.subject = subject
        self.rule = rule
        self.message = message

    def __str__(self) -> str:
        return f"{self.path}:{self.line} {self.subject} {self.rule} {self.message}"


def read_text(path: str) -> str:
    """Read a file with universal newlines so CRLF never reaches a comparison."""
    if not os.path.isfile(path):
        raise CouldNotRun(f"path is not a readable file: {path}")
    try:
        with open(path, "r", encoding="utf-8", newline=None) as handle:
            return handle.read()
    except OSError as exc:
        raise CouldNotRun(f"cannot read {path}: {exc}") from exc
    except UnicodeDecodeError as exc:
        raise CouldNotRun(f"{path} is not UTF-8 text: {exc}") from exc


def load_documents(path: str) -> list[dict]:
    text = read_text(path)
    try:
        raw = list(yaml.load_all(text, Loader=LineLoader))
    except yaml.YAMLError as exc:
        raise CouldNotRun(f"{path} is not parsable YAML: {exc}") from exc
    docs = [doc for doc in raw if isinstance(doc, dict) and doc.get("kind")]
    if not docs:
        raise CouldNotRun(
            f"{path} contains no Kubernetes document with a `kind` field; "
            "a manifest checker cannot return a clean verdict on input it did not understand"
        )
    return docs


def line_of(node: Any, default: int = 1) -> int:
    if isinstance(node, dict):
        value = node.get("__line__")
        if isinstance(value, int):
            return value
    return default


def subject_of(doc: dict) -> str:
    meta = doc.get("metadata") or {}
    name = meta.get("name", "unnamed") if isinstance(meta, dict) else "unnamed"
    return f"{doc.get('kind')}/{name}"


def pod_spec_of(doc: dict) -> tuple[dict | None, int]:
    """Return the PodSpec for any workload kind, plus its line."""
    kind = doc.get("kind")
    spec = doc.get("spec")
    if not isinstance(spec, dict):
        return None, line_of(doc)
    if kind == "Pod":
        return spec, line_of(spec)
    if kind == "CronJob":
        job = ((spec.get("jobTemplate") or {}).get("spec") or {})
        template = job.get("template") if isinstance(job, dict) else None
    else:
        template = spec.get("template")
    if isinstance(template, dict):
        inner = template.get("spec")
        if isinstance(inner, dict):
            return inner, line_of(inner)
    return None, line_of(spec)


def containers_of(pod_spec: dict) -> list[tuple[str, dict, bool]]:
    """Return (list-name, container, is_init) for every container in a PodSpec."""
    out: list[tuple[str, dict, bool]] = []
    for key, is_init in (("initContainers", True), ("containers", False)):
        entries = pod_spec.get(key)
        if isinstance(entries, list):
            for entry in entries:
                if isinstance(entry, dict):
                    out.append((key, entry, is_init))
    return out


def quantities_present(resources: Any, section: str) -> bool:
    block = resources.get(section) if isinstance(resources, dict) else None
    if not isinstance(block, dict):
        return False
    return bool(block.get("cpu")) and bool(block.get("memory"))


def normalise_quantity(value: Any) -> str:
    """Normalise a Kubernetes quantity so `0.2` and `200m` compare equal.

    The API server parses both to the same resource.Quantity, so a string
    comparison would report a difference the cluster does not see.
    """
    text = str(value).strip()
    if text.endswith("m"):
        try:
            return f"{float(text[:-1]) / 1000:.9f}".rstrip("0").rstrip(".")
        except ValueError:
            return text
    try:
        return f"{float(text):.9f}".rstrip("0").rstrip(".")
    except ValueError:
        return text


def check_container(path: str, subject: str, list_name: str, container: dict,
                    kind: str, is_init: bool, profile: str) -> list[Finding]:
    findings: list[Finding] = []
    line = line_of(container)
    name = container.get("name", "unnamed")
    where = f"{subject} {list_name}[{name}]"

    resources = container.get("resources")
    if not quantities_present(resources, "requests") or not quantities_present(resources, "limits"):
        findings.append(Finding(
            path, line, where, "RESOURCES",
            "container must declare resources.requests and resources.limits, "
            "each with cpu and memory",
        ))
    elif profile == "arvan":
        req, lim = resources["requests"], resources["limits"]
        for quantity in ("cpu", "memory"):
            if normalise_quantity(req.get(quantity)) != normalise_quantity(lim.get(quantity)):
                findings.append(Finding(
                    path, line, where, "ARVAN-PARITY",
                    f"Arvan CaaS requires requests.{quantity} to equal limits.{quantity} "
                    f"(got {req.get(quantity)!r} and {lim.get(quantity)!r})",
                ))

    if kind in TRAFFIC_KINDS and not is_init and not container.get("readinessProbe"):
        findings.append(Finding(
            path, line, where, "READINESS",
            "container in a traffic-serving workload must declare a readinessProbe",
        ))

    sec = container.get("securityContext")
    sec = sec if isinstance(sec, dict) else {}
    sec_line = line_of(sec, line)

    if sec.get("privileged") is True:
        findings.append(Finding(path, sec_line, where, "PRIVILEGED",
                                "securityContext.privileged must not be true"))
    if sec.get("allowPrivilegeEscalation") is not False:
        findings.append(Finding(path, sec_line, where, "PRIVILEGE-ESCALATION",
                                "securityContext.allowPrivilegeEscalation must be false"))
    caps = sec.get("capabilities")
    drop = caps.get("drop") if isinstance(caps, dict) else None
    if not isinstance(drop, list) or "ALL" not in drop:
        findings.append(Finding(path, sec_line, where, "CAPABILITIES",
                                "securityContext.capabilities.drop must contain ALL"))
    if "runAsUser" in sec:
        findings.append(Finding(path, sec_line, where, "FIXED-UID",
                                "securityContext.runAsUser pins a UID and breaks on any "
                                "platform that assigns an arbitrary one"))

    for port in container.get("ports") or []:
        if not isinstance(port, dict):
            continue
        number = port.get("containerPort")
        if isinstance(number, int) and number < 1024:
            findings.append(Finding(
                path, line_of(port, line), where, "LOW-PORT",
                f"containerPort {number} is below 1024; listen on 8080 or 8443 and map "
                "the low port at the Service, Ingress, or Route",
            ))
    return findings


def check_pod_spec(path: str, subject: str, kind: str, pod_spec: dict,
                   profile: str) -> list[Finding]:
    findings: list[Finding] = []
    line = line_of(pod_spec)

    for field in ("hostNetwork", "hostPID", "hostIPC"):
        if pod_spec.get(field) is True:
            findings.append(Finding(path, line, subject, "HOST-NAMESPACE",
                                    f"{field} must not be true"))

    for volume in pod_spec.get("volumes") or []:
        if isinstance(volume, dict) and "hostPath" in volume:
            findings.append(Finding(
                path, line_of(volume, line), subject, "HOSTPATH",
                f"volume {volume.get('name', 'unnamed')!r} uses hostPath, which writes to "
                "the node filesystem and pins the Pod to a node",
            ))

    pod_sec = pod_spec.get("securityContext")
    pod_sec = pod_sec if isinstance(pod_sec, dict) else {}
    if pod_sec.get("runAsNonRoot") is not True:
        findings.append(Finding(path, line_of(pod_sec, line), subject, "RUN-AS-NON-ROOT",
                                "spec.securityContext.runAsNonRoot must be true"))
    seccomp = pod_sec.get("seccompProfile")
    if not isinstance(seccomp, dict) or seccomp.get("type") != "RuntimeDefault":
        findings.append(Finding(path, line_of(pod_sec, line), subject, "SECCOMP",
                                "spec.securityContext.seccompProfile.type must be RuntimeDefault"))

    containers = containers_of(pod_spec)
    if not containers:
        findings.append(Finding(path, line, subject, "NO-CONTAINERS",
                                "workload declares no containers"))
    for list_name, container, is_init in containers:
        findings.extend(check_container(path, subject, list_name, container, kind, is_init, profile))
    return findings


def container_port_index(docs: Iterable[dict]) -> tuple[set[str], set[int]]:
    """Collect every declared container port name and number in the document set."""
    names: set[str] = set()
    numbers: set[int] = set()
    for doc in docs:
        pod_spec, _ = pod_spec_of(doc)
        if not pod_spec:
            continue
        for _, container, _ in containers_of(pod_spec):
            for port in container.get("ports") or []:
                if not isinstance(port, dict):
                    continue
                if isinstance(port.get("name"), str):
                    names.add(port["name"])
                if isinstance(port.get("containerPort"), int):
                    numbers.add(port["containerPort"])
    return names, numbers


def check_service(path: str, doc: dict, port_names: set[str], port_numbers: set[int]) -> list[Finding]:
    findings: list[Finding] = []
    subject = subject_of(doc)
    spec = doc.get("spec")
    if not isinstance(spec, dict):
        return findings
    if spec.get("externalIPs"):
        findings.append(Finding(
            path, line_of(spec), subject, "EXTERNAL-IPS",
            "spec.externalIPs trusts every cluster user (CVE-2020-8554) and is being "
            "removed from Kubernetes 1.36; use a LoadBalancer Service, Ingress, or Gateway API",
        ))
    for port in spec.get("ports") or []:
        if not isinstance(port, dict):
            continue
        target = port.get("targetPort", port.get("port"))
        if isinstance(target, str) and target not in port_names:
            findings.append(Finding(
                path, line_of(port, line_of(spec)), subject, "TARGET-PORT",
                f"targetPort {target!r} matches no named containerPort in this manifest set",
            ))
        elif isinstance(target, int) and port_numbers and target not in port_numbers:
            findings.append(Finding(
                path, line_of(port, line_of(spec)), subject, "TARGET-PORT",
                f"targetPort {target} matches no declared containerPort in this manifest set",
            ))
    return findings


def check_hpa(path: str, doc: dict, workloads: dict[tuple[str, str], dict],
              profile: str) -> list[Finding]:
    findings: list[Finding] = []
    subject = subject_of(doc)
    spec = doc.get("spec")
    if not isinstance(spec, dict):
        return findings
    ref = spec.get("scaleTargetRef")
    ref = ref if isinstance(ref, dict) else {}
    target_kind, target_name = ref.get("kind"), ref.get("name")
    minr, maxr = spec.get("minReplicas"), spec.get("maxReplicas")
    if isinstance(minr, int) and isinstance(maxr, int) and maxr < minr:
        findings.append(Finding(path, line_of(spec), subject, "HPA-BOUNDS",
                                f"maxReplicas {maxr} is below minReplicas {minr}"))

    target = workloads.get((str(target_kind), str(target_name)))
    if target is not None:
        pod_spec, _ = pod_spec_of(target)
        if pod_spec:
            for list_name, container, is_init in containers_of(pod_spec):
                if is_init:
                    continue
                resources = container.get("resources")
                if not quantities_present(resources, "requests"):
                    findings.append(Finding(
                        path, line_of(spec), subject, "HPA-NEEDS-REQUESTS",
                        f"scale target {target_kind}/{target_name} container "
                        f"{container.get('name', 'unnamed')!r} has no resources.requests.cpu, "
                        "so a CPU-utilisation HPA is inert",
                    ))
        if isinstance(target.get("spec"), dict) and "replicas" in target["spec"]:
            findings.append(Finding(
                path, line_of(spec), subject, "HPA-VS-REPLICAS",
                f"scale target {target_kind}/{target_name} also sets spec.replicas; "
                "the HPA and the static replica count fight on every reconcile",
            ))
    if profile == "arvan" and target_kind and target_kind != "Deployment":
        findings.append(Finding(
            path, line_of(spec), subject, "ARVAN-HPA-TARGET",
            f"Arvan CaaS disables manual and automatic scaling for workloads with persistent "
            f"storage, so an HPA targets a Deployment only (got {target_kind})",
        ))
    return findings


def check_pdb(path: str, doc: dict, workloads: dict[tuple[str, str], dict]) -> list[Finding]:
    findings: list[Finding] = []
    subject = subject_of(doc)
    spec = doc.get("spec")
    if not isinstance(spec, dict):
        return findings
    if "minAvailable" in spec and "maxUnavailable" in spec:
        findings.append(Finding(path, line_of(spec), subject, "PDB-BOTH-FIELDS",
                                "a PodDisruptionBudget sets minAvailable or maxUnavailable, "
                                "never both; the API rejects it"))
    for workload in workloads.values():
        wspec = workload.get("spec")
        if isinstance(wspec, dict) and wspec.get("replicas") == 1 and "minAvailable" in spec:
            findings.append(Finding(
                path, line_of(spec), subject, "PDB-SINGLE-REPLICA",
                f"{subject_of(workload)} has one replica, so this budget blocks every "
                "voluntary disruption, including a node drain the platform started",
            ))
            break
    return findings


def check_arvan_kinds(path: str, doc: dict) -> list[Finding]:
    kind = doc.get("kind")
    if kind in ARVAN_ABSENT_KINDS:
        return [Finding(
            path, line_of(doc), subject_of(doc), "ARVAN-ABSENT-KIND",
            f"{kind} is absent from the Arvan CaaS API surface on the pinned line; confirm with "
            "`kubectl api-resources` on the target before emitting it",
        )]
    return []


def selector_index(docs: Iterable[dict]) -> dict[str, Any]:
    """Map subject to the identity fields that must never change on an upgrade."""
    index: dict[str, Any] = {}
    for doc in docs:
        kind = doc.get("kind")
        if kind not in SELECTOR_KINDS:
            continue
        spec = doc.get("spec")
        if not isinstance(spec, dict):
            continue
        selector = spec.get("selector")
        if isinstance(selector, dict):
            selector = {k: v for k, v in selector.items() if k != "__line__"}
            if isinstance(selector.get("matchLabels"), dict):
                selector["matchLabels"] = {
                    k: v for k, v in selector["matchLabels"].items() if k != "__line__"
                }
        claims = []
        for claim in spec.get("volumeClaimTemplates") or []:
            if isinstance(claim, dict):
                meta = claim.get("metadata") or {}
                claims.append(meta.get("name") if isinstance(meta, dict) else None)
        index[subject_of(doc)] = {"selector": selector, "volumeClaimTemplates": claims,
                                  "line": line_of(spec)}
    return index


def check_baseline(path: str, docs: list[dict], baseline_path: str) -> list[Finding]:
    findings: list[Finding] = []
    new = selector_index(docs)
    old = selector_index(load_documents(baseline_path))
    for subject, current in new.items():
        previous = old.get(subject)
        if previous is None:
            continue
        if previous["selector"] != current["selector"]:
            findings.append(Finding(
                path, current["line"], subject, "SELECTOR-DRIFT",
                "spec.selector changed against the baseline; a selector is immutable, so the "
                "upgrade will be rejected. Emit a new resource under a new name and delete the "
                "old one before the new one takes its traffic",
            ))
        if previous["volumeClaimTemplates"] != current["volumeClaimTemplates"]:
            findings.append(Finding(
                path, current["line"], subject, "STORAGE-IDENTITY-DRIFT",
                "volumeClaimTemplates[].metadata.name changed against the baseline; the "
                "existing PVCs will be orphaned and the new replicas will start empty",
            ))
    return findings


def analyse(path: str, baseline: str | None, profile: str) -> list[Finding]:
    docs = load_documents(path)
    findings: list[Finding] = []

    workloads: dict[tuple[str, str], dict] = {}
    for doc in docs:
        if doc.get("kind") in WORKLOAD_KINDS:
            meta = doc.get("metadata") or {}
            name = meta.get("name") if isinstance(meta, dict) else None
            workloads[(str(doc.get("kind")), str(name))] = doc

    port_names, port_numbers = container_port_index(docs)

    for doc in docs:
        kind = doc.get("kind")
        subject = subject_of(doc)
        if kind in WORKLOAD_KINDS or kind == "Pod":
            pod_spec, spec_line = pod_spec_of(doc)
            if pod_spec is None:
                findings.append(Finding(path, spec_line, subject, "NO-POD-SPEC",
                                        "workload has no pod template spec"))
            else:
                findings.extend(check_pod_spec(path, subject, str(kind), pod_spec, profile))
        if kind == "Service":
            findings.extend(check_service(path, doc, port_names, port_numbers))
        if kind == "HorizontalPodAutoscaler":
            findings.extend(check_hpa(path, doc, workloads, profile))
        if kind == "PodDisruptionBudget":
            findings.extend(check_pdb(path, doc, workloads))
        if profile == "arvan":
            findings.extend(check_arvan_kinds(path, doc))

    if baseline:
        findings.extend(check_baseline(path, docs, baseline))

    findings.sort(key=lambda f: (f.line, f.subject, f.rule))
    return findings


SELF_TEST_CASES = [
    ("clean.yaml", None, "default", 0),
    ("bad-deployment.yaml", None, "default",
     ["RESOURCES", "READINESS", "PRIVILEGED", "PRIVILEGE-ESCALATION", "CAPABILITIES",
      "HOST-NAMESPACE", "HOSTPATH", "RUN-AS-NON-ROOT", "SECCOMP", "LOW-PORT", "TARGET-PORT"]),
    ("clean.yaml", "baseline-drift.yaml", "default",
     ["SELECTOR-DRIFT", "STORAGE-IDENTITY-DRIFT"]),
    ("arvan-violations.yaml", None, "arvan",
     ["ARVAN-PARITY", "ARVAN-HPA-TARGET", "ARVAN-ABSENT-KIND"]),
]


def self_test() -> int:
    failures: list[str] = []
    if not os.path.isdir(FIXTURE_DIR):
        print(f"check_manifests --self-test: fixture directory missing: {FIXTURE_DIR}",
              file=sys.stderr)
        return EXIT_CANNOT_RUN

    for fixture, baseline, profile, expectation in SELF_TEST_CASES:
        target = os.path.join(FIXTURE_DIR, fixture)
        base = os.path.join(FIXTURE_DIR, baseline) if baseline else None
        try:
            found = analyse(target, base, profile)
        except CouldNotRun as exc:
            failures.append(f"{fixture} ({profile}): could not run: {exc}")
            continue
        rules = {f.rule for f in found}
        if expectation == 0:
            if found:
                failures.append(f"{fixture} ({profile}): expected clean, got {sorted(rules)}")
        else:
            missing = [rule for rule in expectation if rule not in rules]
            if missing:
                failures.append(f"{fixture} ({profile}): did not report {missing}")

    # A file the checker cannot understand must not return a clean verdict.
    for broken in ("unparsable.yaml", "not-kubernetes.yaml"):
        target = os.path.join(FIXTURE_DIR, broken)
        try:
            analyse(target, None, "default")
        except CouldNotRun:
            pass
        else:
            failures.append(f"{broken}: returned a verdict on input it could not understand")

    # A CRLF fixture must produce exactly the findings its LF twin produces.
    crlf = os.path.join(FIXTURE_DIR, "bad-deployment-crlf.yaml")
    lf = os.path.join(FIXTURE_DIR, "bad-deployment.yaml")
    if os.path.isfile(crlf):
        try:
            if {f.rule for f in analyse(crlf, None, "default")} != \
               {f.rule for f in analyse(lf, None, "default")}:
                failures.append("bad-deployment-crlf.yaml: CRLF input changed the findings")
        except CouldNotRun as exc:
            failures.append(f"bad-deployment-crlf.yaml: could not run: {exc}")
    else:
        failures.append("bad-deployment-crlf.yaml: fixture missing")

    if failures:
        for line in failures:
            print(f"SELF-TEST FAIL: {line}", file=sys.stderr)
        return EXIT_FINDINGS
    print(f"check_manifests --self-test: {len(SELF_TEST_CASES) + 3} cases passed")
    return EXIT_CLEAN


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="check_manifests.py",
        description=(
            "Fail a rendered Kubernetes manifest set that omits resources or probes, "
            "sets a host-level or privileged field, mismatches a Service targetPort, or "
            "mutates an immutable selector against a baseline."
        ),
        epilog=(
            "Exit codes: 0 clean, 1 findings, 2 could not run. "
            "Rule identifiers are stable and are cited from "
            "/alaa-k8s-helm ($alaa-k8s-helm) references/validation-workflows.md."
        ),
    )
    parser.add_argument("manifest", nargs="?",
                        help="path to a rendered manifest file (helm template output, or raw YAML)")
    parser.add_argument("--baseline", metavar="FILE",
                        help="the currently deployed rendered manifest set; enables the "
                             "selector and storage-identity drift checks")
    parser.add_argument("--profile", choices=("default", "arvan"), default="default",
                        help="`arvan` additionally asserts the predicates that "
                             "/caas-arvan-kuber ($caas-arvan-kuber) contributes: requests equal to "
                             "limits, an HPA "
                             "target that is a Deployment, and no kind absent from the Arvan "
                             "capability matrix")
    parser.add_argument("--self-test", action="store_true",
                        help="run the shipped fixtures and exit; needs no cluster and no network")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    if not args.manifest:
        parser.print_usage(sys.stderr)
        print("check_manifests: a manifest path is required (or --self-test)", file=sys.stderr)
        return EXIT_CANNOT_RUN

    try:
        findings = analyse(args.manifest, args.baseline, args.profile)
    except CouldNotRun as exc:
        print(f"check_manifests: could not run: {exc}", file=sys.stderr)
        return EXIT_CANNOT_RUN

    if not findings:
        print(f"check_manifests: {args.manifest}: clean ({args.profile} profile)")
        return EXIT_CLEAN

    for finding in findings:
        print(str(finding))
    print(f"check_manifests: {len(findings)} finding(s) in {args.manifest} "
          f"({args.profile} profile)", file=sys.stderr)
    return EXIT_FINDINGS


if __name__ == "__main__":
    sys.exit(main())
