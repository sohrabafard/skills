from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
from contextlib import contextmanager
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
# Only used to locate optional legacy fixtures when this skill sits inside the wider
# skills repository. A fixed parents[N] hop breaks anywhere else, so resolve by marker
# and fall back to the skill directory rather than indexing off the end of the path.
def _find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in here.parents:
        if (candidate / ".git").exists() or (candidate / "skills").is_dir():
            return candidate
    return SKILL_DIR


REPO_ROOT = _find_repo_root()
INIT = SKILL_DIR / "scripts" / "init_workflow_files.py"
VALIDATE = SKILL_DIR / "scripts" / "validate_workflow_files.py"
STAMP = "20260710-010101"
HANDOFF_FIELDS = (
    "Confirmed facts",
    "Open assumptions",
    "Ruled out",
    "Read first on resume",
    "Environment notes",
    "Traps",
)
PHASE_FIELDS = ("Depends on", "Owned scope", "Excluded from this phase", "Validation commands", "Evidence observed")

# A plan in the shape the previous skill version produced: no handoff package, and phases that
# still carry the combined "Validation commands/evidence" field. It must keep validating.
PREVIOUS_VERSION_PLAN = """# Workflow Plan - Previous version

- Task ID: `20260101-000000_previous-version`
- Mode: `plan`
- Profile: `resumable`
- Status: executing
- Created: `2026-01-01T00:00:00Z`
- Checkpoint: `docs/agents/20260101-000000_previous-version-state.md`

## Summary and Outcome

- Current repository truth: written before the handoff package existed.
- Outcome: keep old plans readable.

## Scope

- In scope: this plan.
- Out of scope: nothing.
- Constraints and assumptions: none.

## Ordered Work

### Phase 1 - Do the work

- Status: pending
- Work:
  - [ ] Do it.
- Acceptance criteria: it is done.
- Validation commands/evidence: `python3 -m unittest discover -s tests` not run

## Blockers and Next Action

- Blockers: none known.
- Next action: continue from Phase 1.
"""

PREVIOUS_VERSION_CHECKPOINT = """# Workflow Checkpoint - Previous version

- Plan: `docs/_agent_plans/20260101-000000_previous-version.md`
- Status: executing
- Current phase: Phase 1
- Last verified result: not run
- Blockers: none known
- Next action: continue from Phase 1
- Touched surfaces: none
"""

LEGACY_PACK = {
    "docs/_agent_plans/20260708-013000_legacy-pack.md": """# Workflow Plan - Legacy pack

- Task ID: `20260708-013000_legacy-pack`
- Mode: `execute`
- Status: complete
- Created: `2026-07-08T01:30:00Z`
- Phase prompts: `docs/_agent_plans/20260708-013000_legacy-pack__phase-prompts.md`
- Continuation state: `docs/agents/20260708-013000_legacy-pack-state.md`
- Machine state: `.codex/state/20260708-013000_legacy-pack.json`

## Summary and Outcome

- Outcome: the legacy four-file pack shipped.

## Scope

- In scope: the legacy pack.
- Out of scope: everything else.
- Constraints and assumptions: none recorded.

## Ordered Work

### Phase 1 - Ship the pack

- Status: complete
- Work:
  - [x] Ship the pack.
- Acceptance criteria: the pack is published.
- Validation commands/evidence: `python3 -m unittest discover -s tests` returned OK.

## Blockers and Next Action

- Blockers: none.
- Next action: none; retained as history.
""",
    "docs/_agent_plans/20260708-013000_legacy-pack__phase-prompts.md": """# Phase Prompts - Legacy pack

- Plan: `docs/_agent_plans/20260708-013000_legacy-pack.md`

## Implementer

Historic prompt retained as read-only history.

## Independent reviewer

Historic prompt retained as read-only history.
""",
    ".codex/state/20260708-013000_legacy-pack.json": """{
  "task_id": "20260708-013000_legacy-pack",
  "status": "complete",
  "plan_path": "docs/_agent_plans/20260708-013000_legacy-pack.md",
  "next_step": "none; retained as history"
}
""",
    "docs/agents/20260708-013000_legacy-pack-state.md": """# Continuation State - Legacy pack

- Plan: `docs/_agent_plans/20260708-013000_legacy-pack.md`
- Status: complete
- Next action: none; retained as history.
""",
}


@contextmanager
def workspace_tempdir():
    """Yield a throwaway workspace outside the repository.

    Using the system temp directory keeps the suite runnable from a read-only or
    unlink-restricted checkout, and keeps test artifacts out of the working tree.
    """
    base = Path(tempfile.mkdtemp(prefix="alaa-workflow-"))
    path = base / f".tmp-alaa-workflow-{uuid.uuid4().hex}"
    path.mkdir()
    try:
        yield str(path)
    finally:
        resolved = base.resolve()
        if not resolved.name.startswith("alaa-workflow-"):
            raise RuntimeError(f"Refusing to remove unexpected test path: {resolved}")
        shutil.rmtree(resolved, ignore_errors=True)


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

    def write_files(self, root: Path, files: dict[str, str]) -> None:
        for relative, content in files.items():
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8")

    def edit(self, path: Path, old: str, new: str) -> None:
        content = path.read_text(encoding="utf-8")
        self.assertIn(old, content)
        path.write_text(content.replace(old, new, 1), encoding="utf-8")

    def test_resumable_is_the_default_and_creates_a_plan_plus_checkpoint(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            self.assertEqual("resumable", payload["profile"])
            self.assertEqual(2, len(payload["outputs"]))
            plan = root / str(payload["outputs"][0])
            checkpoint = root / str(payload["outputs"][1])
            self.assertTrue(plan.exists())
            self.assertTrue(checkpoint.exists())
            self.assertIn(plan.name, checkpoint.read_text(encoding="utf-8"))
            self.assertFalse((root / ".codex/state").exists())
            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root)
            self.assertIn("profile: resumable", result.stdout)

    def test_direct_remains_available_as_one_small_plan(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root, "--profile", "direct")
            self.assertEqual("direct", payload["profile"])
            self.assertEqual(1, len(payload["outputs"]))
            plan = root / str(payload["outputs"][0])
            self.assertTrue(plan.exists())
            self.assertLessEqual(plan.stat().st_size, 5 * 1024)
            self.assertFalse((root / "docs/agents").exists())
            self.assertFalse((root / ".codex/state").exists())

    def test_help_states_the_default_profile_and_its_reason(self) -> None:
        with workspace_tempdir() as tmp:
            result = self.run_script(INIT, ["--help"], Path(tmp))
            help_text = " ".join(result.stdout.split())
            self.assertIn("Default: resumable", help_text)
            self.assertIn("more than one phase", help_text)
            self.assertIn("Choose direct deliberately for genuinely single-phase bounded work", help_text)

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
            self.assertEqual(3, len(payload["outputs"]))
            plan = root / str(payload["outputs"][0])
            prompts = root / str(payload["outputs"][1])
            self.assertEqual(f"{plan.stem}__phase-prompts.md", prompts.name)
            content = prompts.read_text(encoding="utf-8")
            self.assertIn("## Implementer", content)
            self.assertIn("## Independent reviewer", content)
            self.assertIn("runtime-a / current-a", content)
            self.assertNotIn("NEEDS_LIVE_VERIFICATION", content)
            implementer = content.split("## Implementer", 1)[1].split("## Independent reviewer", 1)[0]
            reviewer = content.split("## Independent reviewer", 1)[1].split("## Documenter", 1)[0]
            self.assertLessEqual(len(implementer.split()), 250)
            self.assertLessEqual(len(reviewer.split()), 250)

            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root)
            self.assertIn("profile: resumable", result.stdout)

    def test_documenter_metadata_is_optional_and_paired(self) -> None:
        resolved = [
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
        ]
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root, *resolved, "--documenter-runtime", "runtime-c", "--documenter-model", "current-c")
            content = (root / str(payload["outputs"][1])).read_text(encoding="utf-8")
            self.assertIn("## Documenter", content)
            self.assertIn("runtime-c / current-c", content)
            documenter = content.split("## Documenter", 1)[1]
            self.assertLessEqual(len(documenter.split()), 250)
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root, *resolved)
            content = (root / str(payload["outputs"][1])).read_text(encoding="utf-8")
            self.assertIn("not included / not included", content)
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            failure = self.run_script(
                INIT,
                ["--task", "Adaptive workflow", "--timestamp", STAMP, *resolved, "--documenter-runtime", "runtime-c"],
                root,
                expected=1,
            )
            self.assertIn("documenter runtime and model", (failure.stdout + failure.stderr).lower())

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
            self.assertEqual("resumable", lane_payload["profile"])
            self.assertEqual(2, len(lane_payload["outputs"]))
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
        repository_pack = (
            "docs/_agent_plans/20260708-013000_alaa-quasar-app-vite-v3-pack.md",
            "docs/_agent_plans/20260708-013000_alaa-quasar-app-vite-v3-pack__phase-prompts.md",
            ".codex/state/20260708-013000_alaa-quasar-app-vite-v3-pack.json",
            "docs/agents/alaa-quasar-app-vite-v3-pack-state.md",
        )
        use_repository_pack = all((REPO_ROOT / relative).exists() for relative in repository_pack)
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            if use_repository_pack:
                plan_relative = repository_pack[0]
                for relative in repository_pack:
                    destination = root / relative
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(REPO_ROOT / relative, destination)
            else:
                plan_relative = next(iter(LEGACY_PACK))
                self.write_files(root, LEGACY_PACK)
            result = self.run_script(VALIDATE, ["--plan", plan_relative], root)
            self.assertIn("profile: legacy", result.stdout)
            self.assertIn("WARN", result.stdout)
            self.assertNotIn("ERROR", result.stdout)

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

    def test_generated_plan_carries_the_handoff_package_between_scope_and_ordered_work(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            content = (root / str(payload["outputs"][0])).read_text(encoding="utf-8")
            self.assertIn("## Handoff Package", content)
            self.assertLess(content.index("## Scope"), content.index("## Handoff Package"))
            self.assertLess(content.index("## Handoff Package"), content.index("## Ordered Work"))
            for field in HANDOFF_FIELDS:
                self.assertIn(f"- {field}", content)

    def test_generated_phases_carry_dependencies_ownership_exclusions_and_evidence(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            content = (root / str(payload["outputs"][0])).read_text(encoding="utf-8")
            self.assertNotIn("Validation commands/evidence", content)
            phases = content.split("### Phase ")[1:]
            self.assertGreaterEqual(len(phases), 2)
            for phase in phases:
                block = phase.split("\n## ", 1)[0]
                for field in PHASE_FIELDS:
                    self.assertIn(f"- {field}:", block, msg=f"{field} missing from phase: {block.splitlines()[0]}")

    def test_previous_version_plan_without_a_handoff_package_only_warns(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            self.write_files(
                root,
                {
                    "docs/_agent_plans/20260101-000000_previous-version.md": PREVIOUS_VERSION_PLAN,
                    "docs/agents/20260101-000000_previous-version-state.md": PREVIOUS_VERSION_CHECKPOINT,
                },
            )
            result = self.run_script(VALIDATE, ["--plan", "docs/_agent_plans/20260101-000000_previous-version.md"], root)
            self.assertNotIn("ERROR", result.stdout)
            self.assertIn("WARN [plan.handoff]", result.stdout)
            self.assertIn("WARN [plan.phase-fields]", result.stdout)
            self.assertIn("Validation commands/evidence", result.stdout)

    def test_missing_handoff_field_blocks_a_current_format_plan(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            plan = root / str(payload["outputs"][0])
            content = plan.read_text(encoding="utf-8")
            traps = next(line for line in content.splitlines() if line.startswith("- Traps"))
            plan.write_text(content.replace(f"{traps}\n", ""), encoding="utf-8")
            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root, expected=1)
            self.assertIn("ERROR [plan.handoff]", result.stdout)
            self.assertIn("Traps", result.stdout)

    def test_unfilled_read_first_blocks_once_the_plan_leaves_planning(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            plan = root / str(payload["outputs"][0])
            self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root)
            self.edit(plan, "- Status: planning", "- Status: executing")
            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root, expected=1)
            self.assertIn("ERROR [plan.handoff.read-first]", result.stdout)

    def test_missing_phase_field_blocks_a_current_format_plan(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            plan = root / str(payload["outputs"][0])
            self.edit(plan, "- Owned scope: NEEDS_FILL\n", "")
            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root, expected=1)
            self.assertIn("ERROR [plan.phase-fields]", result.stdout)
            self.assertIn("Owned scope", result.stdout)

    def test_resumable_plan_requires_its_correlated_checkpoint(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            plan = root / str(payload["outputs"][0])
            (root / str(payload["outputs"][1])).unlink()
            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root, expected=1)
            self.assertIn("[artifact.checkpoint]", result.stdout)

    def test_checkpoint_plan_field_must_point_back_at_the_plan(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            plan = root / str(payload["outputs"][0])
            checkpoint = root / str(payload["outputs"][1])
            declared = next(line for line in checkpoint.read_text(encoding="utf-8").splitlines() if line.startswith("- Plan:"))
            self.edit(checkpoint, declared, "- Plan: `docs/_agent_plans/some-other-plan.md`")
            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root, expected=1)
            self.assertIn("ERROR [checkpoint.plan]", result.stdout)

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
