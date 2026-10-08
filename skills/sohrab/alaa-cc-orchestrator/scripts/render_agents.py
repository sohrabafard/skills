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
from profile_projection import expected_profiles, profile_text


def expected_outputs(root, policy):
    wrappers = expected_profiles(root, policy, "yaml")
    agents = {p: p.read_bytes() for p in sorted((root / "agents").glob("*.md"))}
    agents.update(wrappers)
    manifest = {"pack": "alaa-cc-orchestrator",
                "version": (root / "VERSION").read_text().strip(),
                "managed_agents": [{"name": p.stem, "file": p.relative_to(root).as_posix(),
                                    "sha256": hashlib.sha256(data).hexdigest()}
                                   for p, data in sorted(agents.items())]}
    return {**wrappers, root / "assets/manifest.json": (json.dumps(manifest, indent=2) + "\n").encode()}


def drift(outputs):
    return [p for p, data in outputs.items() if not p.is_file() or p.read_bytes() != data]


def self_test(policy, evidence_dir=None):
    from check_agent_grants import frontmatter
    from tempfile import TemporaryDirectory
    from contextlib import nullcontext
    if evidence_dir is not None:
        # Retain requested evidence; never overwrite or clean a caller's directory.
        evidence_dir.mkdir(parents=True, exist_ok=False)
    context = (nullcontext(str(evidence_dir)) if evidence_dir is not None
               else TemporaryDirectory(prefix="alaa-profile-test-"))
    with context as directory:
        root = Path(directory)
        policy = {**policy, "profiles": {"alaa-implementer": policy["profiles"]["alaa-implementer"]}}
        (root / "assets").mkdir(); (root / "agents").mkdir()
        (root / "VERSION").write_text("fixture\n")
        metadata = {"description": "fixture", "disallowedTools": "mcp__hindsight"}
        body = 'Contract with "quotes" and \\paths.\n'
        (root / "assets/implementation-contract.md").write_text(body)
        (root / "assets/profile-wrappers.json").write_text(json.dumps({"profiles": {
            "alaa-implementer": {"contract": "assets/implementation-contract.md", "metadata": metadata}}}))
        outputs = expected_outputs(root, policy)
        assert len(drift(outputs)) == 2
        for path, data in outputs.items(): path.write_bytes(data)
        assert not drift(expected_outputs(root, policy))
        wrapper = root / "agents/alaa-implementer.md"
        assert frontmatter(str(wrapper))["model"] == policy["profiles"]["alaa-implementer"]["model"]
        assert wrapper.read_text().split("\n---\n", 1)[1].endswith(body)
        wrapper.write_text(wrapper.read_text() + "drift\n")
        assert wrapper in drift(expected_outputs(root, policy))
        try: profile_text("yaml", "alaa-implementer", {**metadata, "model": "override"}, body,
                          policy["profiles"]["alaa-implementer"], "contract")
        except ValueError: pass
        else: raise AssertionError("metadata pin override accepted")
        (root / "assets/profile-wrappers.json").write_text('{"profiles": {}}\n')
        try: expected_outputs(root, policy)
        except ValueError: pass
        else: raise AssertionError("omitted managed profile accepted")
    print("RENDER SELF-TEST OK: standalone projection, drift and canonical pin ownership")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true"); mode.add_argument("--check", action="store_true")
    mode.add_argument("--self-test", action="store_true")
    parser.add_argument("--self-test-dir", type=Path,
                        help="new evidence directory to retain instead of a temporary directory")
    args = parser.parse_args()
    if args.self_test_dir is not None and not args.self_test:
        parser.error("--self-test-dir requires --self-test")
    try:
        policy = load_policy()
        if args.self_test: return self_test(policy, args.self_test_dir)
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
