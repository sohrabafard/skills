"""Check the approved upgrade against its base; no writes. Exit 0/1/2."""
from __future__ import annotations

import json
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "3aa602487ff9f347b12a9b332db37cca527ab558"
GUIDE = "skills/sohrab/alaa-prompting-guide"
PACK = "skills/sohrab/alaa-codex-orchestrator"


def original(path: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"{BASE}:{path}"], cwd=ROOT
    ).decode("utf-8")


def main() -> int:
    try:
        before = json.loads(original(f"{GUIDE}/assets/codex-model-policy.json"))
        after = json.loads((ROOT / GUIDE / "assets/codex-model-policy.json").read_text())
        expected = json.loads(json.dumps(before["profiles"]))
        migrated = []
        for name, profile in expected.items():
            if profile["model"] == "gpt-6-sol":
                migrated.append(name)
                profile["model"] = "gpt-6.1-sol"
        assert len(migrated) == 16, "baseline profile count changed"
        assert after["profiles"] == expected, "profile model-only preservation failed"
        assert after["policy_version"] == "1.1.0"
        assert after["legacy_exceptions"] == before["legacy_exceptions"]
        for name, spec in before["models"].items():
            assert after["models"][name] == spec, f"old capability changed: {name}"

        corpus_path = f"{GUIDE}/assets/evals/agent-comparisons.json"
        expected_corpus = json.loads(original(corpus_path))
        expected_corpus["policy_version"] = "1.1.0"
        cases = 0
        for case in expected_corpus["scenarios"]:
            if case["candidate"]["model"] == "gpt-6-sol":
                cases += 1
                case["comparator"] = dict(case["candidate"])
                case["candidate"]["model"] = "gpt-6.1-sol"
        assert cases == 4
        assert json.loads((ROOT / corpus_path).read_text()) == expected_corpus, "corpus fixture or non-Sol comparison drift"

        changed_agents = 0
        paths = list((ROOT / PACK / "agents").glob("*.toml"))
        paths.append(ROOT / GUIDE / "assets/rule-writer/codex/alaa-rule-writer.toml")
        for path in paths:
            old = tomllib.loads(original(path.relative_to(ROOT).as_posix()))
            new = tomllib.loads(path.read_text(encoding="utf-8"))
            if old["model"] == "gpt-6-sol":
                changed_agents += 1
                old["model"] = "gpt-6.1-sol"
            assert old == new, f"agent changed beyond model pin: {path.name}"
        assert changed_agents == 15

        reference = f"{GUIDE}/references/12-gpt-6.md"
        old_prompt = original(reference).split("## Prompt design", 1)[1].split("## API is not the Codex harness", 1)[0]
        new_prompt = (ROOT / reference).read_text(encoding="utf-8").split("## Prompt design", 1)[1].split("## API is not the Codex harness", 1)[0]
        assert old_prompt == new_prompt, "prompting behavior section changed"
        assert (ROOT / PACK / "VERSION").read_text().strip() == "4.1.0"
        print("PASS: 16 model-only profiles, 15 model-only agent definitions, four model-only comparisons, preserved prompt behavior and non-Sol capabilities")
        return 0
    except AssertionError as exc:
        print(f"FINDINGS: {exc}")
        return 1
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"could not run: {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
