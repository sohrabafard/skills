"""Scoped text hygiene, invariant assertions and before/after evidence; no runtime proof."""
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess

ROOT = Path.cwd()
OUT = ROOT / "artifacts/skill-pack-optimization-20261018/lanes"
before = json.loads((OUT / "SHARED-input-snapshot.json").read_text(encoding="utf8"))
scope = before["scope"]
roots = [f"skills/sohrab/{name}" for name in scope]
changed = subprocess.check_output(["git", "diff", "--name-only", "--", *roots], text=True).splitlines()
assert changed and all(p.endswith(".md") for p in changed), "Unexpected executable/config input change"

# Convert only legacy dual calls in substantively edited Markdown, preserving the first call.
dual = re.compile(r"(`?/([a-z][a-z0-9-]+)`?)\s*\(\s*`?\$\2`?\s*\)")
previous = OUT / "SHARED-final-checks.json"
conversions = json.loads(previous.read_text(encoding="utf8")).get("dual_form_conversions", {}) if previous.exists() else {}
for name in changed:
    path = ROOT / name
    text = path.read_text(encoding="utf8")
    text, count = dual.subn(lambda m: m.group(1), text)
    if count:
        conversions[name] = conversions.get(name, 0) + count
    path.write_text(text, encoding="utf8", newline="\n")

checks = []
def require(label, result):
    assert result, label
    checks.append(label)

def read(skill, rel):
    return (ROOT / f"skills/sohrab/{skill}/{rel}").read_text(encoding="utf8")

service = "alaa-services-contract"
wire = read(service, "references/25-end-to-end-flow-and-boundaries.md")
offset = wire.split("### Admin-table offset exception", 1)[1].split("\nScope:", 1)[0]
require("Five offset guards remain in the authorizing owner", re.findall(r"(?m)^([1-5])\. ", offset) == list("12345"))
for phrase in ["admin-only", "request time", "public gateway", "SDK", "maximum reachable offset", "page size", "400", "INPUT_VALIDATION_FAILED", "pagination: offset", "operational", "same", "filters", "production-shaped"]:
    require(f"Offset guard: {phrase}", phrase in offset)
key_route = read("alaa-keyset-pagination", "references/10-route-mode-and-sort-allowlist.md")
require("No stale offset prohibition or second numbered guard list", "currently forbids" not in key_route and "all five conditions" in key_route and not re.search(r"(?m)^1\. The route", key_route))
for code in ["INVALID_CURSOR", "CURSOR_VERSION_UNSUPPORTED", "CURSOR_EXPIRED", "INVALID_CURSOR_CONTEXT"]:
    require(f"Existing cursor code registered with 400: {code}", bool(re.search(r"\| 400 \| `" + code + r"` \|", wire)))
for phrase in ["absent cursor", "sibling `pagination`", "`after`", "`before`", "Do not echo `limit`", "`sort` outside", "compatibility/deprecation stop"]:
    require(f"Wire invariant: {phrase}", phrase in wire)
values = read(service, "references/22-failure-load-and-deprecation-contract.md").split("## List page-size values", 1)[1].split("\n## ", 1)[0]
require("Existing keyset values and applicability preserved", all(p in values for p in ["`20`", "`100`", "cursor", "measured", "recorded exception", "distinct admin-offset"]))
key_body = read("alaa-keyset-pagination", "SKILL.md")
key_wire = read("alaa-keyset-pagination", "references/40-wire-contract-limits-and-errors.md")
require("Keyset defaults and duplicate response schema removed", "defaults to 20" not in key_body and "Default 20" not in key_wire and "```json" not in key_wire)

for skill in [service, "alaa-reliability-sla"]:
    body = read(skill, "SKILL.md")
    topic = read(skill, "references/00-topic-map.md")
    old = subprocess.check_output(["git", "show", f"{before['head']}:skills/sohrab/{skill}/SKILL.md"], text=True)
    removed = set(re.findall(r"(?:references/)?(\d\d-[a-z0-9-]+\.md)", old)) - set(re.findall(r"(?:references/)?(\d\d-[a-z0-9-]+\.md)", body))
    require(f"Removed body destinations remain in {skill} external router", all(p in topic for p in removed))
    require(f"External topic map remains routed: {skill}", "references/00-topic-map.md" in body)
require("Services duplicate router removed", "## Trigger to file" not in read(service, "SKILL.md"))

trust = read("alaa-trust-gateway-auth", "references/30-fail-closed-cases.md")
require("No flat timeout 403 and unmapped response remains denied with explicit stop", all(p in trust for p in ["public-code row", "report the gap and stop", "unparseable or unmappable", "protected backend is not called"]) and "deny produce the same outward result" not in trust)
require("Context case tests selected service status", "assert the documented denial status" in trust)
deny = read("alaa-trust-gateway-auth", "references/50-deny-codes.md")
require("AUTHZ and TOTP definitions point to their owners", "| `AUTHZ_DENIED` |" not in deny and "| `TOTP_STEP_UP_REQUIRED` |" not in deny and "401 or 403" in deny)

obs = "alaa-observability-soc"
gates = read(obs, "references/20-instrumentation-gates.md")
for phrase in ["Errors and rejections", "Web Vitals field data", "Request outcomes", "Connection transitions", "Service-worker lifecycle", "Failed updates", "conditional requirements", "Error capture stays unsampled", "Product analytics", "source-of-truth fallbacks", "latency histogram", "without a cache", "invents neither a family nor a label"]:
    require(f"Conditional telemetry requirement: {phrase}", phrase in gates)
phone = read(obs, "references/80-review-gates.md").split("### Permitted phone derivative", 1)[1].split("\n## ", 1)[0]
require("Phone gate defaults safe and retains no subscriber digits", all(p in phone for p in ["by default", "explicitly approved", "entire national subscriber", "fixed marker", "98[redacted]", "+98[redacted]", "Preserve no subscriber prefix or suffix", "never enters a metric label", "enumerable phone hash"]))
sentry = read(obs, "references/60-sentry-and-profiling.md")
require("Sentry keeps privacy, source injection and per-signal caveat", all(p in sentry for p in ["Real DSNs are never committed", "public event-submission", "tokens stay secret", "installed SDK version", "other enabled signal types", "exception", "approved frontend configuration"]))
require("Sentry stack authority stays explicit without invented browser env defaults", all(p in read(service, "references/21-alaa-platform-observability-directive.md") for p in ["no fleet browser Sentry environment keys", "approved build/runtime configuration", "PHP/Composer", "pinned versions"]))
require("SOC forwards fail-open without bypassing required audit write", "forwarding/export" in read(obs, "SKILL.md") and "non-repudiation" in read(obs, "SKILL.md"))
require("Telemetry buffering has bounded capacity and visible drops", all(p in read(obs, "references/50-telemetry-pipeline.md") for p in ["bounded capacity", "drops are counted and visible", "never converted"]))
require("Read-only container default retains documented exception", all(p in read("alaa-security-review", "references/60-deep-review-and-hardening.md") for p in ["read-only root filesystem by default", "exact writable paths", "compensating control", "no added capabilities", "no container-runtime socket", "pinned by digest"]))
reliability = read("alaa-reliability-sla", "SKILL.md")
require("Contributor behavior retains accepted obligation and unknown classification stop", all(p in reliability for p in ["fail-open releases no accepted obligation", "treat the dependency as a gate and report it", "never substitute for a gate's answer"]))
vector = "vector-rust-observability-pipelines"
for rel in ["SKILL.md", "references/30-buffers-acks-and-backpressure.md", "references/75-ala-ingest-pipeline.md"]:
    text = read(vector, rel)
    require(f"Vector gate owner and path consequences: {rel}", "/alaa-security-review" in text and "/alaa-reliability-sla" in text and "when_full" in text)
historical = read(vector, "references/75-ala-ingest-pipeline.md")
require("Historical commercial exactness/recoverability/privacy boundaries preserved", all(p in historical for p in ["5bbe3c2", "2026-07-30", "must be exact", "recoverable record of every rejection", "security policy forbids", "No consumer checkout or deployment was revalidated"]))

files = sorted((p for name in scope for p in (ROOT / "skills/sohrab" / name).rglob("*") if p.is_file()), key=lambda p: p.relative_to(ROOT).as_posix())
old_files = {f["path"]: f for f in before["files"]}
require("No owned file added, removed or retired", {p.relative_to(ROOT).as_posix() for p in files} == set(old_files))
manifest = []
digest = sha256()
growth = defaultdict(lambda: {"before_bytes": 0, "after_bytes": 0})
for path in files:
    rel = path.relative_to(ROOT).as_posix()
    data = path.read_bytes()
    digest.update(rel.encode() + b"\0" + data)
    item = {"path": rel, "bytes": len(data), "sha256": sha256(data).hexdigest()}
    manifest.append(item)
    skill = rel.split("/")[2]
    growth[skill]["before_bytes"] += old_files[rel]["bytes"]
    growth[skill]["after_bytes"] += len(data)
    if rel in changed:
        require(f"UTF8/noBOM/LF and nonempty: {rel}", bool(data) and not data.startswith(b"\xef\xbb\xbf") and b"\r" not in data)
        data.decode("utf8")
        require(f"No legacy dual call remains in changed file: {rel}", not dual.search(data.decode("utf8")))
    else:
        require(f"Untouched owned input hash preserved: {rel}", item["sha256"] == old_files[rel]["sha256"])
for row in growth.values():
    row["delta_bytes"] = row["after_bytes"] - row["before_bytes"]
result = {"head": before["head"], "scope": scope, "checks_passed": len(checks), "checks": checks, "changed_markdown": changed, "dual_form_conversions": conversions, "manifest_algorithm": before["algorithm"], "manifest_sha256": digest.hexdigest(), "growth": dict(growth), "files": manifest, "proof_limit": "Static source/instruction assertions only; no consumer or live runtime behavior proof."}
(OUT / "SHARED-final-checks.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf8", newline="\n")
print(f"PASS: {len(checks)} scoped assertions; {len(changed)} changed Markdown files; {len(manifest)} owned files; SHA256 {digest.hexdigest()}")
