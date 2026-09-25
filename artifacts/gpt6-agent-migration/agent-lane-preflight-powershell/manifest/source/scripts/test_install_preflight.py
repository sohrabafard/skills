#!/usr/bin/env python3
"""Prove installer rejection leaves scratch destinations absent; never installs globally.

Requires a new --scratch-dir and --shell powershell|bash. Keeps all fixture evidence.
Exit 0 pass, 1 regression, 2 unavailable proof.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch-dir", type=Path, required=True)
    parser.add_argument("--shell", choices=("powershell", "bash"), required=True)
    parser.add_argument("--executable", help="explicit shell executable")
    parser.add_argument("--policy-root", type=Path,
                        default=ROOT.parent / "alaa-prompting-guide")
    args = parser.parse_args()
    executable = args.executable or (shutil.which("pwsh") or shutil.which("powershell")
                                    if args.shell == "powershell" else shutil.which("bash"))
    if not executable:
        print(f"{args.shell} unavailable", file=sys.stderr)
        return 2
    try:
        scratch = args.scratch_dir.resolve()
        if scratch == ROOT or ROOT in scratch.parents:
            raise ValueError("scratch directory must be outside the source skill to avoid recursive copying")
        scratch.mkdir(parents=True, exist_ok=False)
        policy_root = args.policy_root.resolve()
        count = 0
        for kind in ("pin", "wrapper", "manifest", "missing-owner"):
            source = scratch / kind / "source"
            shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            if kind == "pin":
                path = source / "agents" / "alaa-implementer.toml"
                text = path.read_text(encoding="utf-8")
                import re
                path.write_text(re.sub(r'^model = .*$', 'model = "unapproved-model"', text, flags=re.M),
                                encoding="utf-8", newline="\n")
            elif kind == "wrapper":
                path = source / "agents" / "alaa-reviewer-deep.toml"
                path.write_bytes(path.read_bytes() + b"# changed generated wrapper\n")
            elif kind == "manifest":
                path = source / "assets" / "manifest.json"
                data = json.loads(path.read_text(encoding="utf-8"))
                data["version"] = "stale"
                path.write_text(json.dumps(data) + "\n", encoding="utf-8", newline="\n")
            owner = scratch / "absent-policy-owner" if kind == "missing-owner" else policy_root
            result = subprocess.run(
                [sys.executable, "-B", str(source / "scripts" / "validate_pack.py"),
                 "--policy-root", str(owner)], capture_output=True, text=True, timeout=30)
            (source.parent / "validator.log").write_text(result.stdout + result.stderr, encoding="utf-8")
            expected = 2 if kind == "missing-owner" else 1
            if result.returncode != expected:
                print(f"{kind}: source validator expected {expected}, got {result.returncode}", file=sys.stderr)
                return 1
            for installer in ("agents", "skill"):
                target = source.parent / f"{args.shell}-{installer}-target"
                agent_target = source.parent / f"{args.shell}-{installer}-agent-target"
                if args.shell == "powershell":
                    script = ("Install-AlaaCodexAgents.ps1" if installer == "agents"
                              else "Install-AlaaCodexOrchestrator.ps1")
                    command = [executable, "-NoProfile", "-File", str(source / "scripts" / script)]
                    if installer == "agents":
                        command += ["-SourceDirectory", str(source / "agents"), "-TargetDirectory", str(target)]
                    else:
                        command += ["-TargetSkillDirectory", str(target), "-TargetAgentDirectory", str(agent_target)]
                    command += ["-PolicyRoot", str(owner)]
                else:
                    script = "install-agents.sh" if installer == "agents" else "install-skill.sh"
                    command = [executable, (source / "scripts" / script).as_posix()]
                    command += ([(source / "agents").as_posix(), target.as_posix(), owner.as_posix()]
                                if installer == "agents" else
                                [target.as_posix(), owner.as_posix(), agent_target.as_posix()])
                result = subprocess.run(command, capture_output=True, text=True, timeout=30)
                (source.parent / f"{args.shell}-{installer}.log").write_text(
                    result.stdout + result.stderr, encoding="utf-8")
                if result.returncode == 0 or target.exists() or agent_target.exists():
                    print(f"{kind}/{installer}: rejection or zero-destination-effect invariant failed", file=sys.stderr)
                    return 1
                # A shell launch error must not masquerade as source rejection.
                proof = "canonical policy unavailable" if kind == "missing-owner" else "PACK VALIDATION FAILED"
                if proof not in result.stdout + result.stderr:
                    print(f"{kind}/{installer}: source rejection was not observed", file=sys.stderr)
                    return 2
                count += 1
        print(f"INSTALL PREFLIGHT PASS: {count} {args.shell} negative paths; destinations untouched; {scratch}")
        return 0
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"preflight proof unavailable: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
