from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
import uuid
from contextlib import contextmanager
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[4]
INIT = SKILL_DIR / "scripts" / "init_workflow_files.py"
VALIDATE = SKILL_DIR / "scripts" / "validate_workflow_files.py"
STAMP = "20260710-010101"


@contextmanager
def workspace_tempdir():
    path = REPO_ROOT / f".tmp-alaa-workflow-{uuid.uuid4().hex}"
    path.mkdir()
    try:
        yield str(path)
    finally:
        resolved = path.resolve()
        if resolved.parent != REPO_ROOT.resolve() or not resolved.name.startswith(".tmp-alaa-workflow-"):
            raise RuntimeError(f"Refusing to remove unexpected test path: {resolved}")
        if resolved.exists():
            shutil.rmtree(resolved)


class WorkflowFilesTest(unittest.TestCase):
    def run_script(self, script: Path, args: list[str], cwd: Path, expected: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(script), *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
        return result

    def init(self, root: Path, *args: str) -> tuple[dict[str, object], subprocess.CompletedProcess[str]]:
        result = self.run_script(INIT, ["--task", "Adaptive workflow", "--timestamp", STAMP, *args], root)
        return json.loads(result.stdout), result

    def test_direct_is_default_and_creates_one_small_plan(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            self.assertEqual("direct", payload["profile"])
            self.assertEqual(1, len(payload["outputs"]))
            plan = root / str(payload["outputs"][0])
            self.assertTrue(plan.exists())
            self.assertLessEqual(plan.stat().st_size, 5 * 1024)
            self.assertFalse((root / "docs/agents").exists())
            self.assertFalse((root / ".codex/state").exists())

    def test_profiles_create_only_declared_companions(self) -> None:
        expectations = {
            "direct": 1,
            "resumable": 2,
            "orchestrated": 3,
            "legacy": 4,
        }
        for profile, count in expectations.items():
            with self.subTest(profile=profile), workspace_tempdir() as tmp:
                payload, _ = self.init(Path(tmp), "--profile", profile)
                self.assertEqual(profile, payload["profile"])
                self.assertEqual(count, len(payload["outputs"]))
                if profile != "legacy":
                    self.run_script(VALIDATE, ["--plan", str(payload["outputs"][0])], Path(tmp))

    def test_explicit_prompt_pack_records_roles_and_freshness(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(
                root,
                "--with-prompts",
                "--implementer-runtime",
                "runtime-a",
                "--implementer-model",
                "current-a",
                "--reviewer-runtime",
                "runtime-b",
                "--reviewer-model",
                "current-b",
                "--verified-on",
                "2026-07-10",
                "--verification-source",
                "https://example.invalid/official-a",
            )
            self.assertEqual(2, len(payload["outputs"]))
            plan = root / str(payload["outputs"][0])
            prompts = root / str(payload["outputs"][1])
            self.assertEqual(f"{plan.stem}__phase-prompts.md", prompts.name)
            content = prompts.read_text(encoding="utf-8")
            self.assertIn("## Implementer", content)
            self.assertIn("## Independent reviewer", content)
            self.assertIn("runtime-a / current-a", content)
            self.assertNotIn("NEEDS_LIVE_VERIFICATION", content)
            implementer = content.split("## Implementer", 1)[1].split("## Independent reviewer", 1)[0]
            reviewer = content.split("## Independent reviewer", 1)[1]
            self.assertLessEqual(len(implementer.split()), 250)
            self.assertLessEqual(len(reviewer.split()), 250)

            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root)
            self.assertIn("profile: direct", result.stdout)

    def test_with_state_alias_reproduces_legacy_four_file_set(self) -> None:
        with workspace_tempdir() as tmp:
            payload, result = self.init(Path(tmp), "--with-state")
            self.assertEqual("legacy", payload["profile"])
            self.assertEqual(4, len(payload["outputs"]))
            self.assertIn("DEPRECATED", result.stderr)

    def test_remaining_compatibility_flags_still_execute(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            state_payload, state_result = self.init(root, "--state-only")
            self.assertEqual("orchestrated", state_payload["profile"])
            self.assertEqual([f".codex/state/{STAMP}_adaptive-workflow.json"], state_payload["outputs"])
            self.assertIn("DEPRECATED", state_result.stderr)

        with workspace_tempdir() as tmp:
            payload, result = self.init(Path(tmp), "--no-continuation")
            self.assertEqual(1, len(payload["outputs"]))
            self.assertIn("DEPRECATED", result.stderr)

        with workspace_tempdir() as tmp:
            root = Path(tmp)
            parent, _ = self.init(root)
            parent_path = str(parent["outputs"][0])
            lane = self.run_script(
                INIT,
                [
                    "--task",
                    "Frontend lane",
                    "--timestamp",
                    STAMP,
                    "--mode",
                    "resume",
                    "--lane",
                    "frontend",
                    "--parent-plan",
                    parent_path,
                ],
                root,
            )
            lane_payload = json.loads(lane.stdout)
            self.assertEqual("delegated", lane_payload["mode"])
            self.assertEqual(1, len(lane_payload["outputs"]))
            self.assertIn("DEPRECATED", lane.stderr)

    def test_unverified_prompt_pack_is_rejected_until_resolved(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, result = self.init(root, "--with-prompts")
            self.assertIn("NEEDS_LIVE_VERIFICATION", result.stderr)
            plan = str(payload["outputs"][0])
            validation = self.run_script(VALIDATE, ["--plan", plan], root, expected=1)
            self.assertIn("[prompts.freshness]", validation.stdout)

    def test_orchestrated_round_trip_and_same_stem_correlation(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root, "--profile", "orchestrated")
            plan = Path(str(payload["outputs"][0]))
            (root / "docs/agents/unrelated-state.md").write_text("# unrelated\n", encoding="utf-8")
            result = self.run_script(VALIDATE, ["--plan", str(plan)], root)
            self.assertIn(str(plan).replace("\\", "/"), result.stdout)
            self.assertNotIn("unrelated-state.md", result.stdout)

    def test_missing_correlated_checkpoint_never_uses_unrelated_newest(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root, "--profile", "orchestrated")
            plan = root / str(payload["outputs"][0])
            checkpoint = root / str(payload["outputs"][1])
            checkpoint.unlink()
            unrelated = root / "docs/agents/newest-state.md"
            unrelated.write_text("# Workflow Checkpoint\n- Status: planning\n", encoding="utf-8")
            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root, expected=1)
            self.assertIn("[artifact.checkpoint]", result.stdout)
            self.assertNotIn("newest-state.md", result.stdout)

    def test_representative_completed_legacy_artifacts_are_accepted(self) -> None:
        relatives = (
            "docs/_agent_plans/20260708-013000_alaa-quasar-app-vite-v3-pack.md",
            "docs/_agent_plans/20260708-013000_alaa-quasar-app-vite-v3-pack__phase-prompts.md",
            ".codex/state/20260708-013000_alaa-quasar-app-vite-v3-pack.json",
            "docs/agents/alaa-quasar-app-vite-v3-pack-state.md",
        )
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            for relative in relatives:
                destination = root / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(REPO_ROOT / relative, destination)
            result = self.run_script(VALIDATE, ["--plan", relatives[0]], root)
            self.assertIn("profile: legacy", result.stdout)
            self.assertIn("WARN", result.stdout)

    def test_malformed_state_is_blocking(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            state = root / "broken.json"
            state.write_text('{"schema_version": 2,', encoding="utf-8")
            result = self.run_script(VALIDATE, ["--state", str(state)], root, expected=1)
            self.assertIn("[state.json]", result.stdout)

    def test_completed_plan_with_unresolved_placeholders_is_blocking(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            plan = root / str(payload["outputs"][0])
            content = plan.read_text(encoding="utf-8").replace("- Status: planning", "- Status: complete")
            plan.write_text(content, encoding="utf-8")
            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root, expected=1)
            self.assertIn("[plan.placeholders]", result.stdout)

    def test_task_text_is_json_escaped(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            result = self.run_script(
                INIT,
                ["--task", 'Quoted "task"', "--timestamp", STAMP, "--profile", "orchestrated"],
                root,
            )
            payload = json.loads(result.stdout)
            state = root / str(payload["outputs"][-1])
            self.assertEqual('Quoted "task"', json.loads(state.read_text(encoding="utf-8"))["task"])


if __name__ == "__main__":
    unittest.main()
