from pathlib import Path
import importlib.util
import shutil
import subprocess
import sys
import types

repo = Path.cwd()
source = repo / "skills/sohrab/alaa-codex-orchestrator"
owner = repo / "skills/sohrab/alaa-prompting-guide"
evidence = Path(__file__).resolve().parent
scripts = evidence / "copied-pack/scripts"
scripts.mkdir(parents=True)
for name in ("render_agents.py", "validate_pack.py", "check_agent_contracts.py"):
    shutil.copyfile(source / "scripts" / name, scripts / name)
assert not (scripts.parent.parent / "alaa-prompting-guide").exists()
spec = importlib.util.spec_from_file_location("copied_renderer", scripts / "render_agents.py")
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)
stale = types.ModuleType("task_model_controls")
sys.modules["task_model_controls"] = stale
policy_module, policy = renderer.policy_api(owner)
assert sys.modules["task_model_controls"] is stale
assert Path(policy_module.__file__).resolve() == (owner / "scripts/codex_model_policy.py").resolve()
assert Path(policy_module.validate_task_selection.__code__.co_filename).resolve() == (owner / "scripts/task_model_controls.py").resolve()
outputs = renderer.expected_outputs(source, policy, owner)
assert len(outputs) == 34 and not renderer.drift(outputs)
print("PASS: copied renderer imports without sibling owner; selected policy, controls and projection produce 34 unchanged outputs")
missing = subprocess.run([sys.executable, "-B", str(scripts / "validate_pack.py"), "--policy-root", str(evidence / "missing-owner")], capture_output=True, text=True)
(evidence / "missing-owner.log").write_text(missing.stdout + missing.stderr, encoding="utf-8")
assert missing.returncode == 2 and "canonical policy unavailable:" in missing.stderr
assert "ModuleNotFoundError" not in missing.stderr
print("PASS: copied validator missing owner exits 2 with canonical-policy-unavailable diagnostic")
