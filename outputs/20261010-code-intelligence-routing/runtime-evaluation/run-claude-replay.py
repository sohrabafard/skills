"""Task-local, tool-disabled Claude source-prompt replay; not an installed-skill test."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
from datetime import datetime, timezone

base = Path(__file__).resolve().parent
prompt_file = base / "prompt.txt"
record_file = base / "claude-result.json"
receipt_file = base / "claude-receipt.json"
requested = {"model": "claude-sonnet-5-5", "effort": "medium"}
receipt = {
    "kind": "synthetic source-prompt routing conformance",
    "requested": requested,
    "observed": {"model": "unknown", "effort": "unknown"},
    "configuration_verified": False,
    "live_provider_actions": False,
    "installed_skill_activation": False,
    "status": "unrun",
    "started_at": datetime.now(timezone.utc).isoformat(),
}
exe = shutil.which("claude")
override = os.environ.get("CLAUDE_CODE_EFFORT_LEVEL")
receipt["effort_environment_override"] = override if override in ("low","medium","high","xhigh","max") else ("unset" if override is None else "unrecognized")
args = ["--safe-mode", "--strict-mcp-config", "--tools", "", "--permission-mode", "plan",
        "--no-session-persistence", "--model", requested["model"], "--effort", requested["effort"],
        "--output-format", "json", "--print"]
receipt["arguments"] = args
if not exe or not prompt_file.is_file():
    receipt.update(status="blocked", reason="Claude executable or generated prompt missing")
elif override is not None and override != requested["effort"]:
    receipt.update(status="blocked", reason="Existing effort override does not realize the requested control; it was not changed")
else:
    start = time.monotonic()
    try:
        result = subprocess.run([exe, *args], input=prompt_file.read_text(encoding="utf-8"),
            text=True, encoding="utf-8", errors="replace", capture_output=True, cwd=base, timeout=180)
        (base / "claude-stdout.txt").write_text(result.stdout, encoding="utf-8")
        (base / "claude-stderr.txt").write_text(result.stderr, encoding="utf-8")
        receipt["exit_code"] = result.returncode
        receipt["duration_seconds"] = round(time.monotonic()-start, 3)
        try:
            payload = json.loads(result.stdout)
            record_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
            models = list(payload.get("modelUsage", {}))
            receipt["observed"]["model"] = models[0] if len(models)==1 else (models or "unknown")
            receipt["usage"] = payload.get("usage", "unknown")
            receipt["is_error"] = payload.get("is_error", "unknown")
            receipt["status"] = "captured" if result.returncode==0 and not payload.get("is_error") else "blocked"
            if models == [requested["model"]]:
                receipt["configuration_verified"] = True
                receipt["configuration_control_evidence"] = "Explicit full model and effort CLI arguments; no conflicting effort environment override; safe mode; matching modelUsage. Effective effort is not directly reported."
            elif models:
                receipt["status"] = "control-mismatch"
            if receipt["status"] == "blocked":
                receipt["reason"] = str(payload.get("result", payload.get("errors", "runtime returned error")))[:1000]
        except json.JSONDecodeError:
            receipt.update(status="blocked", reason="CLI did not return a JSON result; see bounded stdout/stderr artifacts")
    except subprocess.TimeoutExpired as error:
        receipt.update(status="timeout", duration_seconds=round(time.monotonic()-start,3), reason="180-second harness timeout; no automatic replay")
        stdout = error.stdout or ""
        stderr = error.stderr or ""
        if isinstance(stdout,bytes): stdout=stdout.decode("utf-8","replace")
        if isinstance(stderr,bytes): stderr=stderr.decode("utf-8","replace")
        (base / "claude-stdout.txt").write_text(stdout,encoding="utf-8")
        (base / "claude-stderr.txt").write_text(stderr,encoding="utf-8")
receipt["ended_at"] = datetime.now(timezone.utc).isoformat()
receipt_file.write_text(json.dumps(receipt, indent=2, ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps({key:receipt.get(key) for key in ("status","exit_code","duration_seconds","requested","observed","reason")}))
