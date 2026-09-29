"""Bounded parent-run verification; preserve stdout, stderr, argv and exit status."""
import hashlib
import json
import runpy
import subprocess
import sys
from pathlib import Path

out = Path(__file__).resolve().parent
root = out.parents[4]
records = []


def execute(name, argv):
    result = subprocess.run(argv, cwd=root, capture_output=True, timeout=60)
    (out / f"candidate7-{name}.stdout.log").write_bytes(result.stdout)
    (out / f"candidate7-{name}.stderr.log").write_bytes(result.stderr)
    records.append({"name": name, "argv": argv, "exit": result.returncode,
                    "stdout_bytes": len(result.stdout), "stderr_bytes": len(result.stderr)})
    print(name, result.returncode, flush=True)


def record(name, findings, **details):
    records.append({"name": name, "exit": 1 if findings else 0,
                    "findings": findings, **details})
    print(name, records[-1]["exit"], flush=True)


def manifest(name):
    return {p: h for h, p in (line.split("  ", 1) for line in
            (out / f"{name}.sha256").read_text(encoding="utf-8").splitlines())}


current = manifest("candidate-7")
previous = manifest("candidate-6")
record("source-identity", [p for p, h in current.items()
       if hashlib.sha256((root / p).read_bytes()).hexdigest() != h], paths=len(current))
review = json.loads((out / "review-instructions-docs-candidate6.json").read_text(encoding="utf-8-sig"))
foundation = json.loads((out / "documentation-foundation-repair2.json").read_text(encoding="utf-8-sig"))
operations = json.loads((out / "documentation-operations-repair2.json").read_text(encoding="utf-8-sig"))
semantic = set(foundation["semantic_text_deltas"]) | set(operations["scope"]["semantic_files"])
delta_findings = []
eof_proven = []
for p, h in current.items():
    if p not in previous:
        delta_findings.append(p + ": added")
    elif h != previous[p] and p not in semantic:
        data = (root / p).read_bytes()
        if any(hashlib.sha256(data + ending * n).hexdigest() == previous[p]
               for ending in (b"\n", b"\r\n") for n in range(1, 5)):
            eof_proven.append(p)
        else:
            delta_findings.append(p + ": not proven EOF-only")
delta_findings += [p + ": removed" for p in previous.keys() - current.keys()]
record("repair2-scope", delta_findings, semantic_paths=sorted(semantic), eof_proven=eof_proven)

grades = json.loads((out / "documentation-grades.json").read_text(encoding="utf-8-sig"))["documents"]
record("grade-hashes", [d["path"] for d in grades if
       hashlib.sha256((root / d["path"]).read_bytes()).hexdigest() != d["sha256"]], rows=len(grades))
py = [sys.executable, "-B"]
execute("structure", py + ["scripts/validate_sohrab_skill_pack.py"])
execute("fleet", py + ["scripts/check_fleet_references.py"])
checker = "skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py"
markdown = [d["path"] for d in grades if Path(d["path"]).suffix == ".md"]
eligible = [d["path"] for d in grades if d["applicable_grade"] != "EXEMPT-ATOMIC"]
for prefix, paths, flags in (("links", markdown, []), ("size", eligible, ["--line-budget"])):
    for start in range(0, len(paths), 70):
        execute(f"{prefix}-{start // 70 + 1:02d}", py + [checker, ".", "--files"] + paths[start:start + 70] + flags)

api = runpy.run_path(str(root / checker), run_name="candidate7_template_check")
template_findings = []
templates = [d["path"] for d in grades if Path(d["path"]).suffix != ".md"]
for name in templates:
    path = root / name
    for line, target in api["extract_targets"](path):
        template_findings.extend(str(x) for x in api["validate_target"](root, path, line, target, {}))
record("template-links-direct-api", template_findings, paths=templates)
artifact_docs = sorted(p.relative_to(root).as_posix() for p in out.rglob("*.md"))
execute("artifact-links", py + [checker, ".", "--files"] + artifact_docs)
plan = (out / "docs/_agent_plans/20260929-120000_sohrab-modernization.md").relative_to(root).as_posix()
execute("workflow", py + ["skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py", "--plan", plan])
execute("whitespace", ["git", "diff", "HEAD", "--check", "--", "skills/sohrab"])
assessment = json.loads((out / "assessment.json").read_text(encoding="utf-8-sig"))
skills = {p.parent.name for p in (root / "skills/sohrab").glob("*/SKILL.md")}
assessed = [a["skill"] for a in assessment]
record("assessment-coverage", sorted(skills ^ set(assessed)) +
       (["duplicate assessment"] if len(assessed) != len(set(assessed)) else []), skills=len(skills), rows=len(assessed))
eof_findings = [d["path"] for d in grades if (root / d["path"]).read_bytes().splitlines()[-1:].count(b"")]
record("all-document-eof", eof_findings, paths=len(grades))
record("source-postcheck", [p for p, h in current.items()
       if hashlib.sha256((root / p).read_bytes()).hexdigest() != h], paths=len(current))
report = {"operator": "parent; independent role unavailable due agent-thread capacity",
          "snapshot": "candidate-7", "checks": records,
          "result": "PASS" if all(x["exit"] == 0 for x in records) else "FAIL",
          "limits": "Does not replace required independent instruction acceptance or verifier provenance reconciliation."}
(out / "verification-candidate7-parent.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
sys.exit(0 if report["result"] == "PASS" else 1)
