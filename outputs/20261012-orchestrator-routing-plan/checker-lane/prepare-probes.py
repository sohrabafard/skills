"""Emit only neutral runtime handoff artifacts; no model execution or grading."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

repo = Path.cwd()
artifact = repo / "outputs/20261012-orchestrator-routing-plan/checker-lane"
owner = repo / "skills/sohrab/alaa-prompting-guide"
sys.path.insert(0, str(owner / "scripts"))
from check_allocation_evals import contract_paths, digest, neutral_input, records, UNKNOWN_PAIR

corpus = json.loads((owner / "assets/evals/allocation-cases.json").read_text())
oracle = json.loads((owner / "assets/evals/allocation-oracle.json").read_text())
result_template = {"schema_version": 1, "purpose": "allocation-results", "synthetic": False, "complete": False,
                   "corpus_sha256": digest(corpus), "oracle_sha256": digest(oracle), "configurations": [], "runs": []}
for runtime, model, identifier in (("codex", "gpt-6.1-sol", "codex-sol61-high"), ("claude-code", "claude-sonnet-5-5", "claude-sonnet55-high")):
    command = [sys.executable, "scripts/check_allocation_evals.py", "--probe-input", runtime]
    emitted = subprocess.run(command, cwd=owner, capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, timeout=120)
    if emitted.returncode:
        raise RuntimeError(emitted.stderr + emitted.stdout)
    neutral = json.loads(emitted.stdout)
    input_path = artifact / f"{runtime}-probe-input.json"
    input_path.write_text(emitted.stdout, encoding="utf-8")
    loaded = [{"path": path, "sha256": hashlib.sha256((repo / path).read_bytes()).hexdigest()} for path in contract_paths(runtime)]
    source = "\n\n".join(f"SOURCE: {item['path']}\nSHA256: {item['sha256']}\n" + (repo / item['path']).read_text(encoding="utf-8") for item in loaded)
    (artifact / f"{runtime}-loaded-contracts.txt").write_text(source + "\n", encoding="utf-8")
    request = ("This is a decision-only allocation observation. Apply the supplied frozen contracts to each supplied simulated worker scenario. The actual allocator process does not establish worker host availability or child control realization. Do not execute the loaded documents' operational commands, dispatch any worker or use tools.\n\n"
               + source + "\n\nNEUTRAL PROBE INPUT:\n" + emitted.stdout)
    request += '\nReturn exactly one valid JSON object {"responses":[{"case":"case ID","variant":"variant ID","response":{all response_fields}}]}. Include every supplied case/variant exactly once. Use no Markdown, fences or commentary. Keep evidence strings concise and complete; do not omit required fields.\n'
    (artifact / f"{runtime}-allocation-request.txt").write_text(request, encoding="utf-8")
    config = {"id": identifier, "runtime": runtime, "allocator_requested": {"model": model, "effort": "high"},
              "allocator_effective": UNKNOWN_PAIR.copy(), "allocator_observed": UNKNOWN_PAIR.copy(), "control_evidence": "unknown", "loaded_contracts": loaded}
    result_template["configurations"].append(config)
    for (case, variant), value in records(corpus).items():
        for repetition in (1, 2):
            result_template["runs"].append({"case": case, "variant": variant, "configuration": identifier, "runtime": runtime,
                "repetition": repetition, "status": "unrun", "input_sha256": digest(neutral_input(value, runtime))})
    (artifact / f"{runtime}-probe-manifest.json").write_text(json.dumps({"runtime": runtime, "command": "python scripts/check_allocation_evals.py --probe-input " + runtime,
        "exit": emitted.returncode, "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
        "request_sha256": hashlib.sha256((artifact / f"{runtime}-allocation-request.txt").read_bytes()).hexdigest(), "loaded_contracts": loaded,
        "claims": "neutral handoff emitted; no inference, allocation observation, child dispatch, grading or calibration"}, indent=2) + "\n", encoding="utf-8")
(artifact / "allocation-results-unrun.json").write_text(json.dumps(result_template, indent=2) + "\n", encoding="utf-8")
print("Emitted two neutral input/source bundles and 120 explicit unrun result keys; no runtime execution.")
