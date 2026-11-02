#!/usr/bin/env python3
"""Render standalone managed wrappers and manifest. Exit 0 clean, 1 drift, 2 error."""
from pathlib import Path
import argparse
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
OWNER = ROOT.parent / "alaa-prompting-guide"
sys.path.insert(0, str(OWNER / "scripts"))
from claude_model_policy import load_policy
from profile_projection import expected_profiles, neutral_agent_text


def expected_outputs(root, policy):
    wrappers = expected_profiles(root, policy, "yaml")
    agents = {p: p.read_bytes() for p in sorted((root / "agents").glob("*.md"))}
    agents.update(wrappers)
    agents = {p: neutral_agent_text("yaml", data.decode("utf-8"),
              policy["profiles"][p.stem]).encode("utf-8") for p, data in agents.items()}
    manifest = {"pack": "alaa-cc-orchestrator",
                "version": (root / "VERSION").read_text().strip(),
                "managed_agents": [{"name": p.stem, "file": p.relative_to(root).as_posix(),
                                    "sha256": hashlib.sha256(data).hexdigest()}
                                   for p, data in sorted(agents.items())]}
    return {**agents, root / "assets/manifest.json": (json.dumps(manifest, indent=2) + "\n").encode()}


def drift(outputs):
    return [p for p, data in outputs.items() if not p.is_file() or p.read_bytes() != data]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true"); mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        policy = load_policy()
        outputs = expected_outputs(ROOT, policy); changed = drift(outputs)
        if args.check and changed:
            for path in changed: print(f"generated drift: {path.relative_to(ROOT)}", file=sys.stderr)
            return 1
        if args.write:
            for path in changed: path.write_bytes(outputs[path])
        print(f"RENDER {'WRITE' if args.write else 'CHECK'} OK: {len(outputs)} generated files")
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print(f"render unavailable: {exc}", file=sys.stderr); return 2
    except AssertionError as exc:
        print(f"render findings: {exc}", file=sys.stderr); return 1


if __name__ == "__main__":
    raise SystemExit(main())
