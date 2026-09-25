"""Bounded writer regression evidence; run from the repository root with -B."""
import runpy

versions = runpy.run_path("skills/sohrab/alaa-k8s-helm/scripts/check_versions.py")
checks = {item["id"]: item for item in versions["CHECKS"]}
assert versions["observed_value"](checks["helm-latest"], "v4.3.0 v4.4.0-rc.1") == "4.3.0"
assert versions["observed_value"](checks["kubernetes-latest"], "1.37.1 1.38.0-alpha.1") == "1.37"
assert versions["compare"](checks["helm3-eol"], "2027-02-10", "February 10th, 2028") is not None
print("Three before-change defects now return their expected results.")

manifests = runpy.run_path("skills/sohrab/alaa-k8s-helm/scripts/check_manifests.py")
service = {"kind": "Service", "metadata": {"name": "synthetic"},
           "spec": {"externalIPs": ["192.0.2.1"]}}
findings = manifests["check_service"]("synthetic.yaml", service, set(), set())
assert len(findings) == 1 and findings[0].rule == "EXTERNAL-IPS"
assert "CVE-2020-8554" in findings[0].message
assert "removed from Kubernetes" not in findings[0].message
assert "references/version-awareness.md" in findings[0].message
print("externalIPs remains rejected with the same rule and security rationale.")
