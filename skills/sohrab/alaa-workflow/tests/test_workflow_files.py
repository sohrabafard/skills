from __future__ import annotations

import json
import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
from unittest.mock import patch
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
SKILL_ROW = "| example-owner | skills/example-owner/SKILL.md | source edits | always | block this task |"

# A plan in the shape the previous skill version produced: no handoff package, and phases that
# still carry the combined "Validation commands/evidence" field. It must keep validating.
PREVIOUS_VERSION_PLAN = """# Workflow Plan - Previous version

- Task ID: `20260101-000000_previous-version`
- Mode: `plan`
- Profile: `resumable`
- Status: complete
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
- Status: complete
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
            [sys.executable, "-B", str(script), *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
        return result

    def init(self, root: Path, *args: str) -> tuple[dict[str, object], subprocess.CompletedProcess[str]]:
        # New phased fixtures explicitly adopt a portable binding; this helper never
        # claims live Beads verification. Direct/local and deprecated state-only stay distinct.
        direct = "--profile" in args and args[args.index("--profile") + 1] == "direct"
        binding = [] if "--task-store" in args or direct or "--no-continuation" in args or "--state-only" in args else ["--task-store", "beads", "--beads-binding", "AGENTS.md#beads"]
        result = self.run_script(INIT, ["--task", "Adaptive workflow", "--timestamp", STAMP, *binding, *args], root)
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

    def drop_line(self, path: Path, prefix: str) -> None:
        """Remove the first line starting with prefix, asserting one was there to remove."""
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        index = next((i for i, line in enumerate(lines) if line.startswith(prefix)), None)
        self.assertIsNotNone(index, f"no line starting with {prefix!r} in {path.name}")
        del lines[index]
        path.write_text("".join(lines), encoding="utf-8")

    def fill_skills(self, root: Path, plan: Path) -> None:
        self.write_files(root, {"skills/example-owner/SKILL.md": "---\nname: example-owner\n---\n"})
        content = plan.read_text(encoding="utf-8")
        content = content.replace("| NEEDS_FILL | NEEDS_FILL | NEEDS_FILL | NEEDS_FILL | NEEDS_FILL |", SKILL_ROW)
        content = content.replace("- Required skills: NEEDS_FILL", "- Required skills: example-owner")
        for number in (1, 2):
            for level in ("PHASE", "TASK", "SUBTASK"):
                content = content.replace(f"NEEDS_FILL_{level}_{number}", f"opaque-{level.lower()}-{number}")
        plan.write_text(content, encoding="utf-8")

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
            self.assertNotIn("four moments", help_text)

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
                "--implementer-effort", "medium",
                "--reviewer-effort", "high",
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
            "--implementer-effort", "medium",
            "--reviewer-effort", "high",
            "--verified-on",
            "2026-07-10",
            "--verification-source",
            "https://example.invalid/official-a",
        ]
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root, *resolved, "--documenter-runtime", "runtime-c", "--documenter-model", "current-c", "--documenter-effort", "low")
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
            # Exit 2, not 1: a half-supplied flag pair is a misuse of the invocation, and the
            # initializer reserves 1 for the one outcome the caller must decide about, which
            # is an artifact family already on disk.
            failure = self.run_script(
                INIT,
                ["--task", "Adaptive workflow", "--timestamp", STAMP, *resolved, "--documenter-runtime", "runtime-c"],
                root,
                expected=2,
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
                    "--task-store", "beads", "--beads-binding", "AGENTS.md#beads",
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

    def test_generated_plan_exposes_reasoning_and_dependency_schedule_without_extra_artifacts(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            self.assertEqual(2, len(payload["outputs"]))
            plan = root / str(payload["outputs"][0])
            content = plan.read_text(encoding="utf-8")
            for phase in content.split("### Phase ")[1:]:
                block = phase.split("\n## ", 1)[0]
                for field in ("Reasoning and selection reason", "Settled/open decisions and invariants", "Risk and required observers"):
                    self.assertIn(f"- {field}: NEEDS_FILL", block)
            for field in (
                "Disjoint writes and shared-resource conflicts",
                "Integration barriers and parallel/serialized rationale",
                "Consolidated tasks/checks and preserved outcome/evidence mappings",
                "Reusable evidence and invalidation conditions",
            ):
                self.assertIn(f"- {field}: NEEDS_FILL", content)
            self.assertIn("- Dependency edges and ready sets: Beads owns issue dependencies and readiness; the plan owns phase barriers and shared-resource conflicts.", content)
            self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root)

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

    def test_unfilled_work_branch_blocks_once_the_plan_leaves_planning(self) -> None:
        """A run past planning that has not recorded its work branch cannot be told apart
        from one committing onto the user's base branch."""
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            plan = root / str(payload["outputs"][0])
            self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root)
            self.edit(plan, "- Status: planning", "- Status: executing")
            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root, expected=1)
            self.assertIn("ERROR [plan.workspace]", result.stdout)

    def test_recorded_work_branch_and_base_satisfy_the_workspace_gate(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            plan = root / str(payload["outputs"][0])
            self.fill_skills(root, plan)
            self.edit(plan, "- Status: planning", "- Status: executing")
            checkpoint = root / str(payload["outputs"][1])
            self.edit(checkpoint, "- Status: planning", "- Status: executing")
            self.edit(plan, "- Base branch and commit: NEEDS_FILL", "- Base branch and commit: `main` at `abc1234`")
            self.edit(plan, "- Work branch: NEEDS_FILL", "- Work branch: `agent/adaptive-workflow`")
            self.edit(plan, "- Read first on resume (ordered exact paths): NEEDS_FILL", "- Read first on resume (ordered exact paths): `README.md`")
            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root)
            self.assertNotIn("[plan.workspace]", result.stdout)

    def test_missing_base_commit_blocks_once_execution_has_begun(self) -> None:
        """The integration handshake names its merge target and compares against this
        commit to decide whether its verification evidence still describes the tree."""
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            plan = root / str(payload["outputs"][0])
            self.edit(plan, "- Status: planning", "- Status: executing")
            self.drop_line(plan, "- Base branch and commit")
            self.edit(plan, "- Work branch: NEEDS_FILL", "- Work branch: `agent/adaptive-workflow`")
            self.edit(plan, "- Read first on resume (ordered exact paths): NEEDS_FILL", "- Read first on resume (ordered exact paths): `README.md`")
            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root, expected=1)
            self.assertIn("ERROR [plan.workspace]", result.stdout)

    def test_unfilled_base_commit_blocks_like_a_missing_one(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            plan = root / str(payload["outputs"][0])
            self.edit(plan, "- Status: planning", "- Status: executing")
            self.edit(plan, "- Work branch: NEEDS_FILL", "- Work branch: `agent/adaptive-workflow`")
            self.edit(plan, "- Read first on resume (ordered exact paths): NEEDS_FILL", "- Read first on resume (ordered exact paths): `README.md`")
            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root, expected=1)
            self.assertIn("ERROR [plan.workspace]", result.stdout)

    def test_previous_version_plan_is_exempt_from_the_workspace_gate(self) -> None:
        """A plan written before the protocol existed carries no work branch and is history,
        not a run in flight. It must not start failing."""
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            self.write_files(root, {
                "docs/_agent_plans/20260101-000000_previous-version.md": PREVIOUS_VERSION_PLAN,
                "docs/agents/20260101-000000_previous-version-state.md": PREVIOUS_VERSION_CHECKPOINT,
            })
            result = self.run_script(
                VALIDATE, ["--plan", "docs/_agent_plans/20260101-000000_previous-version.md"], root
            )
            self.assertNotIn("[plan.workspace]", result.stdout)

    def test_phase_without_commit_or_snapshot_only_warns_while_planning(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            plan = root / str(payload["outputs"][0])
            self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root)
            self.drop_line(plan, "- Snapshot:")
            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root)
            self.assertIn("WARN [plan.phase-snapshot]", result.stdout)

    def test_phase_without_commit_or_snapshot_blocks_once_execution_has_begun(self) -> None:
        """An absent evidence identity differs from a phase that changed nothing."""
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            plan = root / str(payload["outputs"][0])
            self.edit(plan, "- Status: planning", "- Status: executing")
            self.edit(plan, "- Base branch and commit: NEEDS_FILL", "- Base branch and commit: `main` at `abc1234`")
            self.edit(plan, "- Work branch: NEEDS_FILL", "- Work branch: `agent/adaptive-workflow`")
            self.edit(plan, "- Read first on resume (ordered exact paths): NEEDS_FILL", "- Read first on resume (ordered exact paths): `README.md`")
            self.drop_line(plan, "- Snapshot:")
            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root, expected=1)
            self.assertIn("ERROR [plan.phase-snapshot]", result.stdout)

    def test_a_phase_that_changed_nothing_records_none_and_passes(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            plan = root / str(payload["outputs"][0])
            self.fill_skills(root, plan)
            self.edit(plan, "- Status: planning", "- Status: executing")
            checkpoint = root / str(payload["outputs"][1])
            self.edit(checkpoint, "- Status: planning", "- Status: executing")
            self.edit(plan, "- Base branch and commit: NEEDS_FILL", "- Base branch and commit: `main` at `abc1234`")
            self.edit(plan, "- Work branch: NEEDS_FILL", "- Work branch: `agent/adaptive-workflow`")
            self.edit(plan, "- Read first on resume (ordered exact paths): NEEDS_FILL", "- Read first on resume (ordered exact paths): `README.md`")
            self.edit(plan, "### Phase 1 - Ground and implement\n\n- Status: pending", "### Phase 1 - Ground and implement\n\n- Status: complete")
            content = plan.read_text(encoding="utf-8").replace("- Snapshot: not captured yet", "- Snapshot: no files changed")
            plan.write_text(content, encoding="utf-8")
            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root)
            self.assertNotIn("[plan.phase-snapshot]", result.stdout)
            self.assertNotIn("[plan.workspace]", result.stdout)

    def test_completed_uncommitted_phase_requires_observed_snapshot(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            plan = root / str(payload["outputs"][0])
            self.fill_skills(root, plan)
            self.edit(plan, "- Status: planning", "- Status: executing")
            checkpoint = root / str(payload["outputs"][1])
            self.edit(checkpoint, "- Status: planning", "- Status: executing")
            self.edit(plan, "- Base branch and commit: NEEDS_FILL", "- Base branch and commit: `main` at `abc1234`")
            self.edit(plan, "- Work branch: NEEDS_FILL", "- Work branch: `agent/adaptive-workflow`")
            self.edit(plan, "- Read first on resume (ordered exact paths): NEEDS_FILL", "- Read first on resume (ordered exact paths): `README.md`")
            self.edit(plan, "### Phase 1 - Ground and implement\n\n- Status: pending", "### Phase 1 - Ground and implement\n\n- Status: complete")
            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root, expected=1)
            self.assertIn("ERROR [plan.phase-snapshot]", result.stdout)

            digest = "a" * 64
            self.edit(plan, "- Snapshot: not captured yet", f"- Snapshot: HEAD abc1234; SHA-256 {digest}; paths README.md; observed 2026-09-25T00:00:00Z")
            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root)
            self.assertNotIn("[plan.phase-snapshot]", result.stdout)

    def test_existing_commit_field_remains_compatible(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            plan, _ = TaskStoreFixture().fixture(root)
            self.edit(plan, "### Phase 1 - Ground and implement\n\n- Status: pending", "### Phase 1 - Ground and implement\n\n- Status: complete")
            self.edit(plan, "- Snapshot: not captured yet", "- Commit: abc1234")
            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root)
            self.assertNotIn("[plan.phase-snapshot]", result.stdout)

    def test_completed_phase_rejects_non_commit_prose_without_snapshot(self) -> None:
        for value in ("not authorized", "pending", "`abc1234` pending"):
            with self.subTest(value=value), workspace_tempdir() as tmp:
                root = Path(tmp)
                payload, _ = self.init(root)
                plan = root / str(payload["outputs"][0])
                self.edit(plan, "### Phase 1 - Ground and implement\n\n- Status: pending", "### Phase 1 - Ground and implement\n\n- Status: complete")
                self.edit(plan, "- Snapshot: not captured yet", f"- Commit: {value}")
                result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root, expected=1)
                self.assertIn("ERROR [plan.phase-snapshot]", result.stdout)

    def test_completed_phase_accepts_legacy_no_change_sentinel(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            plan = root / str(payload["outputs"][0])
            self.fill_skills(root, plan)
            self.edit(plan, "### Phase 1 - Ground and implement\n\n- Status: pending", "### Phase 1 - Ground and implement\n\n- Status: complete")
            self.edit(plan, "- Snapshot: not captured yet", "- Commit: none; this phase changed no files")
            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root)
            self.assertNotIn("[plan.phase-snapshot]", result.stdout)

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

    def test_initializer_misuse_reports_could_not_run(self) -> None:
        for arguments, expected_text in (
            (["--timestamp", "not-a-stamp"], "yyyymmdd-hhmmss"),
            (["--lane", "frontend"], "--parent-plan"),
            (["--parent-plan", "docs/_agent_plans/absent.md"], "parent plan not found"),
        ):
            with self.subTest(arguments=arguments), workspace_tempdir() as tmp:
                failure = self.run_script(
                    INIT, ["--task", "Adaptive workflow", *arguments], Path(tmp), expected=2
                )
                self.assertIn(expected_text, (failure.stdout + failure.stderr).lower())

    def test_existing_outputs_are_refused_whole_and_nothing_is_written(self) -> None:
        """The refusal is exit 1 and it is all-or-nothing.

        Writing until the first collision leaves half an artifact family behind, and the
        next run then cannot start without --force over a conflict it did not create.
        """
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root, "--profile", "orchestrated")
            plan = root / str(payload["outputs"][0])
            checkpoint = root / str(payload["outputs"][1])
            state = root / str(payload["outputs"][2])
            checkpoint.unlink()
            state.unlink()

            failure = self.run_script(
                INIT, ["--task", "Adaptive workflow", "--timestamp", STAMP, "--profile", "orchestrated", "--task-store", "beads", "--beads-binding", "AGENTS.md#beads"], root, expected=1
            )
            self.assertIn("nothing was written", (failure.stdout + failure.stderr).lower())
            self.assertIn(plan.name, failure.stdout + failure.stderr)
            self.assertFalse(checkpoint.exists(), "a refused run must not have written the companions")
            self.assertFalse(state.exists(), "a refused run must not have written the companions")

            forced, _ = self.init(root, "--profile", "orchestrated", "--force")
            self.assertEqual(3, len(forced["outputs"]))
            self.assertTrue(checkpoint.exists())
            self.assertTrue(state.exists())

    def test_initializer_help_states_every_exit_code(self) -> None:
        with workspace_tempdir() as tmp:
            result = self.run_script(INIT, ["--help"], Path(tmp))
            help_text = " ".join(result.stdout.split())
            self.assertIn("exit 0", help_text)
            self.assertIn("exit 1", help_text)
            self.assertIn("exit 2", help_text)
            self.assertIn("not evidence that the artifacts exist", help_text)

    def test_nothing_selected_reports_could_not_run(self) -> None:
        with workspace_tempdir() as tmp:
            result = self.run_script(VALIDATE, [], Path(tmp), expected=2)
            self.assertIn("Nothing to validate", result.stdout)

    def test_absent_plan_reports_could_not_run_rather_than_findings(self) -> None:
        with workspace_tempdir() as tmp:
            result = self.run_script(VALIDATE, ["--plan", "docs/_agent_plans/absent.md"], Path(tmp), expected=2)
            self.assertIn("[plan.path]", result.stdout)

    def test_uncorrelatable_companion_reports_could_not_run(self) -> None:
        with workspace_tempdir() as tmp:
            result = self.run_script(VALIDATE, ["--state", "auto"], Path(tmp), expected=2)
            self.assertIn("[correlation]", result.stdout)

    def test_named_companion_that_does_not_exist_reports_could_not_run(self) -> None:
        """A path the caller typed and a path this run correlated are different claims.

        The first not existing is a broken invocation; the second not existing stays a
        finding about the artifact family, which the two correlation tests pin.
        """
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            plan = root / str(payload["outputs"][0])
            result = self.run_script(
                VALIDATE,
                ["--plan", str(plan.relative_to(root)), "--state", ".codex/state/absent.json"],
                root,
                expected=2,
            )
            self.assertIn("Explicitly selected state path does not exist", result.stdout)

    def test_unreadable_plan_reports_could_not_run_rather_than_findings(self) -> None:
        """An artifact that cannot be read is a validation that did not happen.

        Exiting 1 here would be indistinguishable from findings, and a caller would read
        "the artifacts are wrong" where the truth is that nobody checked them.
        """
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            unreadable = root / "docs/_agent_plans/a-directory.md"
            unreadable.mkdir(parents=True)
            result = self.run_script(VALIDATE, ["--plan", "docs/_agent_plans/a-directory.md"], root, expected=2)
            self.assertIn("could not run", (result.stdout + result.stderr).lower())

    def test_real_findings_still_exit_one_and_not_two(self) -> None:
        """The could-not-run class must not swallow the findings class."""
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            plan = root / str(payload["outputs"][0])
            self.edit(plan, "- Status: planning", "- Status: executing")
            self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root, expected=1)

    def test_help_states_every_exit_code_and_that_two_is_never_a_pass(self) -> None:
        with workspace_tempdir() as tmp:
            result = self.run_script(VALIDATE, ["--help"], Path(tmp))
            help_text = " ".join(result.stdout.split())
            self.assertIn("exit 0", help_text)
            self.assertIn("exit 1", help_text)
            self.assertIn("exit 2", help_text)
            self.assertIn("never evidence that the artifacts are clean", help_text)

    def test_task_text_is_json_escaped(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            result = self.run_script(
                INIT,
                ["--task", 'Quoted "task"', "--timestamp", STAMP, "--profile", "orchestrated", "--task-store", "beads", "--beads-binding", "AGENTS.md#beads"],
                root,
            )
            payload = json.loads(result.stdout)
            state = root / str(payload["outputs"][-1])
            self.assertEqual('Quoted "task"', json.loads(state.read_text(encoding="utf-8"))["task"])


class SkillBindingsTest(unittest.TestCase):
    """Exercise missing-owner and inheritance failures against real skill source files."""

    @classmethod
    def setUpClass(cls) -> None:
        spec = importlib.util.spec_from_file_location("workflow_validator", VALIDATE)
        assert spec is not None and spec.loader is not None
        cls.validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.validator)

    def check(self, replacement: tuple[str, str] | None = None, status: str = "executing", profile: str = "resumable", source_content: str = "---\nname: example-owner\n---\n", content_override: str | None = None) -> list[str]:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            source = root / "skills/example-owner/SKILL.md"
            source.parent.mkdir(parents=True)
            source.write_text(source_content, encoding="utf-8")
            other = root / "skills/other-owner/SKILL.md"
            other.parent.mkdir(parents=True)
            other.write_text("---\nname: other-owner\n---\n", encoding="utf-8")
            content = """## Handoff Package
- Confirmed facts: none
## Skill Bindings
| Skill | Source | Load before | When | If unavailable |
|---|---|---|---|---|
""" + SKILL_ROW + """
| other-owner | skills/other-owner/SKILL.md | review | always | block review |
## Ordered Work
### Phase 1 - Repair
- Status: pending
- Required skills: example-owner
- Work:
  - [ ] Repair behavior. [skills: inherit]
  - [ ] Review the repair. [skills: other-owner]
"""
            if replacement:
                self.assertIn(replacement[0], content)
                content = content.replace(*replacement)
            if content_override is not None:
                content = content_override
            return self.validator.validate_skill_bindings(content, root / "plan.md", profile, status)

    def assert_blocked(self, messages: list[str], invariant: str) -> None:
        self.assertTrue(any(line.startswith(f"ERROR [{invariant}]") for line in messages), messages)

    def test_missing_bindings_block_an_active_plan(self) -> None:
        messages = self.check(("## Skill Bindings", "## Missing bindings"))
        self.assert_blocked(messages, "plan.skills")

    def test_statusless_plan_cannot_inherit_first_completed_phase_status(self) -> None:
        content = "# Plan\n### Phase 1\n- Status: done\n### Phase 2\n- Status: pending\n"
        self.assertEqual("", self.validator.detect_status(content))
        with workspace_tempdir() as tmp:
            status = self.validator.effective_plan_status(content, Path(tmp) / "plan.md", "legacy")
            self.assertEqual("", status)
            self.assert_blocked(self.check(profile="legacy", status=status, content_override=content), "plan.skills")

    def test_incomplete_status_never_admits_historical_mapping_exemption(self) -> None:
        self.assertFalse(self.validator.is_complete_status("incomplete"))
        self.assertFalse(self.validator.is_complete_status("not complete"))
        self.assert_blocked(self.check(("## Skill Bindings", "## Missing bindings"), status="incomplete", profile="legacy"), "plan.skills")

    def test_task_only_plan_with_empty_bindings_cannot_bypass_phase_mapping(self) -> None:
        header = "## Skill Bindings\n| Skill | Source | Load before | When | If unavailable |\n|---|---|---|---|---|\n## Ordered Work\n"
        for task in ("- [ ] Repair behavior.", "1. Repair behavior."):
            with self.subTest(task=task):
                self.assert_blocked(self.check(content_override=header + task), "plan.skills-structure")

    def test_numbered_task_within_phase_requires_mapping(self) -> None:
        self.assert_blocked(self.check(("  - [ ] Repair behavior. [skills: inherit]", "  1. Repair behavior.")), "plan.skills-mapping")

    def test_numbered_task_with_explicit_inheritance_is_valid(self) -> None:
        self.assertEqual([], self.check(("  - [ ] Repair behavior.", "  1. Repair behavior.")))

    def test_numbered_resume_references_are_not_executable_tasks(self) -> None:
        replacement = (
            "- Confirmed facts: none",
            "- Confirmed facts: none\n- Read first on resume:\n  1. README.md\n  2. docs/context.md",
        )
        self.assertEqual([], self.check(replacement))

    def test_numbered_references_after_ordered_work_are_not_tasks(self) -> None:
        old = "  - [ ] Review the repair. [skills: other-owner]"
        self.assertEqual([], self.check((old, old + "\n## Resume references\n1. README.md\n2. docs/context.md")))

    def test_numbered_work_outside_phase_still_blocks_with_valid_phase_present(self) -> None:
        replacement = ("## Ordered Work\n### Phase", "## Ordered Work\n1. Unmapped repair.\n### Phase")
        self.assert_blocked(self.check(replacement), "plan.skills-structure")

    def test_unmapped_task_outside_existing_phase_blocks(self) -> None:
        old = "  - [ ] Review the repair. [skills: other-owner]"
        self.assert_blocked(self.check((old, old + "\n## Other work\n- [ ] Unmapped repair.")), "plan.skills-structure")

    def test_body_only_or_malformed_name_is_not_skill_frontmatter(self) -> None:
        for source in (
            "# Owner\nname: example-owner\n",
            "---\nname: example-owner\n",
            "---\nname: 'example-owner\n---\n",
            "---\nname: example-owner\nname: example-owner\n---\n",
            "---\ndescription: Owner\n---\nname: example-owner\n",
        ):
            with self.subTest(source=source):
                self.assert_blocked(self.check(source_content=source), "plan.skills-source")

    def test_delimited_quoted_name_uses_frontmatter_not_body(self) -> None:
        self.assertEqual([], self.check(source_content="---\nname: 'example-owner'\ndescription: Owner\n---\nname: wrong-body-name\n"))

    def test_correlated_completion_rejects_same_basename_in_other_directory(self) -> None:
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            plan = root / "plan.md"
            state = root / "state.json"
            state.write_text(json.dumps({"plan_path": "other/plan.md", "status": "complete"}), encoding="utf-8")
            content = f"- Machine state: `{state.as_posix()}`\n"
            self.assertEqual("", self.validator.effective_plan_status(content, plan, "legacy"))

    def test_executing_old_plan_without_handoff_or_bindings_must_migrate(self) -> None:
        replacement = (
            "## Handoff Package\n- Confirmed facts: none\n## Skill Bindings",
            "## Historical notes\n- Confirmed facts: none\n## Missing bindings",
        )
        self.assert_blocked(self.check(replacement), "plan.skills")

    def test_completed_adaptive_archive_without_bindings_remains_readable(self) -> None:
        messages = self.check(("## Skill Bindings", "## Archived notes"), status="complete")
        self.assertTrue(messages)
        self.assertTrue(all(line.startswith("WARN") for line in messages), messages)

    def test_legacy_completion_requires_terminal_correlated_evidence(self) -> None:
        cases = (
            ({}, "None - complete", "", ""),
            ({"phase-1": "done"}, "continue phase 2", "", ""),
            ({"phase-1": "done"}, "None - complete", "", "complete"),
            ({"phase-1": "done"}, "None - complete", "executing", "executing"),
        )
        for phases, next_step, declared, expected in cases:
            with self.subTest(phases=phases, next_step=next_step, status=declared), workspace_tempdir() as tmp:
                root = Path(tmp)
                plan = root / "plan.md"
                state = root / "plan-state.json"
                state.write_text(json.dumps({"plan_path": "plan.md", "phases": phases, "next_step": next_step}), encoding="utf-8")
                content = f"- Machine state: `{state.as_posix()}`\n"
                if declared:
                    content += f"- Status: {declared}\n"
                self.assertEqual(expected, self.validator.effective_plan_status(content, plan, "legacy"))

    def test_missing_phase_mapping_blocks(self) -> None:
        self.assert_blocked(self.check(("- Required skills: example-owner", "")), "plan.skills-mapping")

    def test_missing_task_mapping_blocks(self) -> None:
        self.assert_blocked(self.check((" [skills: inherit]", "")), "plan.skills-mapping")

    def test_vague_phase_skills_block(self) -> None:
        self.assert_blocked(self.check(("- Required skills: example-owner", "- Required skills: relevant skills")), "plan.skills-mapping")

    def test_unbound_task_override_blocks(self) -> None:
        self.assert_blocked(self.check(("[skills: other-owner]", "[skills: invented-owner]")), "plan.skills-mapping")

    def test_dangling_source_blocks(self) -> None:
        self.assert_blocked(self.check(("skills/example-owner/SKILL.md", "skills/absent-owner/SKILL.md")), "plan.skills-source")

    def test_source_name_mismatch_blocks(self) -> None:
        self.assert_blocked(self.check(("skills/example-owner/SKILL.md", "skills/other-owner/SKILL.md")), "plan.skills-source")

    def test_missing_load_point_condition_or_absence_blocks(self) -> None:
        for old in ("| source edits |", "| always |", "| block this task |"):
            with self.subTest(field=old):
                self.assert_blocked(self.check((old, "| |")), "plan.skills")

    def test_unavailable_unconditional_owner_blocks(self) -> None:
        self.assert_blocked(self.check(("skills/example-owner/SKILL.md", "unavailable")), "plan.skills-source")

    def test_conditional_absence_is_recorded_without_installation(self) -> None:
        deferred = "| example-owner | unavailable | source edits | deployment is requested | block this task |"
        self.assertEqual([], self.check((SKILL_ROW, deferred)))

    def test_unresolved_mapping_warns_in_draft_and_blocks_on_resume(self) -> None:
        replacement = ("- Required skills: example-owner", "- Required skills: NEEDS_FILL")
        draft = self.check(replacement, status="planning")
        self.assertTrue(all(line.startswith("WARN") for line in draft), draft)
        self.assert_blocked(self.check(replacement), "plan.skills-mapping")

    def test_completed_legacy_missing_mappings_remain_warnings(self) -> None:
        messages = self.check(("- Required skills: example-owner", ""), status="complete", profile="legacy")
        self.assertTrue(messages)
        self.assertTrue(all(line.startswith("WARN") for line in messages), messages)

    def test_valid_inheritance_and_task_override_need_no_duplicate_manuals(self) -> None:
        self.assertEqual([], self.check())

    def test_explicit_no_owner_reason_can_be_inherited(self) -> None:
        self.assertEqual([], self.check(("- Required skills: example-owner", "- Required skills: none (plain fixture inspection)")))


class TaskControlMetadataTest(unittest.TestCase):
    """Pure focused checks for complete intent versus effective runtime evidence."""
    @classmethod
    def setUpClass(cls) -> None:
        spec = importlib.util.spec_from_file_location("workflow_init_task_controls", INIT)
        cls.init_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.init_module)
        spec = importlib.util.spec_from_file_location("workflow_validate_task_controls", VALIDATE)
        cls.validate_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.validate_module)

    def metadata(self, **overrides):
        from argparse import Namespace
        values = dict(implementer_runtime="codex", implementer_model="selected-a",
                      reviewer_runtime="codex", reviewer_model="selected-b",
                      documenter_runtime=None, documenter_model=None,
                      implementer_effort="medium", reviewer_effort="high", documenter_effort=None,
                      verified_on="2026-10-09", verification_source=["https://example.invalid/official"])
        values.update(overrides)
        return self.init_module.resolve_prompt_metadata(Namespace(**values), True)

    def prompt(self, metadata):
        return self.init_module.render("phase-prompts-template.md",
            {**metadata, "task": "Control selection", "plan_path": "plan.md"})

    def test_complete_pair_records_intent_without_claiming_runtime_observation(self):
        content = self.prompt(self.metadata())
        self.assertIn("configured intent; source metadata supplied", content)
        self.assertIn("Implementer effort: medium", content)
        self.assertIn("Independent reviewer effort: high", content)
        self.assertIn("not observed by initializer", content)
        self.assertNotIn("NEEDS_LIVE_VERIFICATION", content)
        self.assertEqual([], self.validate_module.prompt_task_controls_failures(content))

    def test_legacy_model_only_input_remains_unresolved_draft(self):
        metadata = self.metadata(implementer_effort=None, reviewer_effort=None)
        self.assertEqual("NEEDS_LIVE_VERIFICATION", metadata["verification_status"])
        self.assertTrue(self.validate_module.prompt_task_controls_failures(self.prompt(metadata)))

    def test_partial_or_empty_effort_is_rejected(self):
        for changes in ({"reviewer_effort": None}, {"implementer_effort": " "},
                        {"documenter_effort": "low"}):
            with self.subTest(changes=changes), self.assertRaises(self.init_module.Misuse):
                self.metadata(**changes)

    def test_included_documenter_needs_its_own_effort(self):
        draft = self.metadata(documenter_runtime="codex", documenter_model="selected-c")
        self.assertEqual("NEEDS_LIVE_VERIFICATION", draft["documenter_effort"])
        self.assertTrue(self.validate_module.prompt_task_controls_failures(self.prompt(draft)))
        complete = self.metadata(documenter_runtime="codex", documenter_model="selected-c", documenter_effort="low")
        self.assertEqual([], self.validate_module.prompt_task_controls_failures(self.prompt(complete)))

    def test_missing_selection_or_runtime_verification_clause_is_rejected(self):
        content = self.prompt(self.metadata())
        for removed in ("- Implementer effort: medium\n", "- Independent reviewer runtime/model: codex / selected-b\n",
                        "verify BOTH effective model and effort"):
            with self.subTest(removed=removed):
                self.assertTrue(self.validate_module.prompt_task_controls_failures(content.replace(removed, "")))
        for malformed in ("codex /", "/ selected-b", "codex / not included",
                          "codex / NEEDS_LIVE_VERIFICATION"):
            with self.subTest(malformed=malformed):
                broken = content.replace("codex / selected-b", malformed)
                self.assertTrue(self.validate_module.prompt_task_controls_failures(broken))

    def test_same_role_can_record_routine_and_demanding_task_controls(self):
        routine = self.prompt(self.metadata(implementer_model="selected-small", implementer_effort="low"))
        demanding = self.prompt(self.metadata(implementer_model="selected-workhorse", implementer_effort="high"))
        self.assertEqual([], self.validate_module.prompt_task_controls_failures(routine))
        self.assertEqual([], self.validate_module.prompt_task_controls_failures(demanding))
        self.assertEqual(routine.split("## Implementer", 1)[1], demanding.split("## Implementer", 1)[1])


class TaskStoreFixture(unittest.TestCase):
    run_script = WorkflowFilesTest.run_script
    init = WorkflowFilesTest.init
    write_files = WorkflowFilesTest.write_files
    edit = WorkflowFilesTest.edit
    fill_skills = WorkflowFilesTest.fill_skills

    def fixture(self, root: Path, store: str = "local", profile: str = "direct") -> tuple[Path, dict[str, object]]:
        # Reconstruct the pre-hierarchy family explicitly. These tests protect old
        # local/flat Beads contracts; they do not admit new local phased generation.
        args = ["--profile", profile, "--task-store", "beads", "--beads-binding", "AGENTS.md#task-binding"]
        payload, _ = self.init(root, *args)
        payload["task_store"] = store
        plan = root / str(payload["outputs"][0])
        self.fill_skills(root, plan)
        content = plan.read_text(encoding="utf-8")
        content = content.replace("- Task hierarchy: phase-task-subtask\n", "")
        if "### Phase 2" not in content:
            phase = content.split("### Phase 1 - Ground and implement", 1)[1].split("\n## Task Allocation", 1)[0]
            second = phase.replace("- Depends on: none", "- Depends on: Phase 1").replace("NEEDS_FILL_ISSUE_1", "NEEDS_FILL_ISSUE_3").replace("NEEDS_FILL_ISSUE_2", "NEEDS_FILL_ISSUE_4")
            content = content.replace("\n## Task Allocation", "\n### Phase 2 - Validate and reconcile" + second + "\n## Task Allocation", 1)
        for number in (1, 2):
            content = content.replace(f"- Phase issue: opaque-phase-{number}\n", "")
            content = content.replace(f"  - Task issue: opaque-task-{number} [skills: inherit]\n    - Subtask issue: opaque-subtask-{number} [skills: inherit]", f"  - Issue: NEEDS_FILL_ISSUE_{2 * number - 1} [skills: inherit]\n  - Issue: NEEDS_FILL_ISSUE_{2 * number} [skills: inherit]")
        if store == "local":
            content = content.replace("- Task store: `beads`", "- Task store: `local`").replace("- Task binding: AGENTS.md#task-binding", "- Task binding: not applicable")
            tasks = (
                "Read the named sources and verify current behavior.", "Make the smallest in-scope change.",
                "Run the affected validation surface and repair failures.", "Reconcile documentation, status, blockers, and remaining work.",
            )
            for number, outcome in enumerate(tasks, 1):
                dependency = "none" if number == 1 else f"T{number - 1}"
                content = content.replace(f"- Issue: NEEDS_FILL_ISSUE_{number} [skills: inherit]", f"- [ ] T{number}: {outcome} [depends: {dependency}] [skills: inherit]")
        for number in range(1, 5):
            content = content.replace(f"NEEDS_FILL_ISSUE_{number}", f"opaque/{number}")
        content = content.replace("NEEDS_FILL", "repository-grounded")
        plan.write_text(content, encoding="utf-8")
        for output in payload["outputs"]:
            path = root / str(output)
            if path.suffix == ".json":
                data = json.loads(path.read_text())
                data["schema_version"] = 2
                data.pop("current_task", None)
                data.pop("current_subtask", None)
                path.write_text(json.dumps(data), encoding="utf-8")
        if profile == "legacy":
            prompt = next(root / str(path) for path in payload["outputs"] if str(path).endswith("__phase-prompts.md"))
            prompt.write_text(prompt.read_text(encoding="utf-8").replace("NEEDS_LIVE_VERIFICATION", "resolved"), encoding="utf-8")
        return plan, payload

    def validate(self, root: Path, plan: Path, expected: int = 0, *args: str) -> str:
        return self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root)), *args], root, expected).stdout

    def inventory(self, root: Path) -> dict[str, bytes]:
        return {str(path.relative_to(root)): path.read_bytes() for path in root.rglob("*") if path.is_file()}


class TaskStoreCliTest(TaskStoreFixture):
    def test_historical_profiles_both_stores(self):
        for store in ("local", "beads"):
            for profile in ("direct", "resumable", "orchestrated", "legacy"):
                with self.subTest(store=store, profile=profile), workspace_tempdir() as tmp:
                    root = Path(tmp)
                    plan, payload = self.fixture(root, store, profile)
                    result = self.validate(root, plan)
                    self.assertEqual(store, payload["task_store"])
                    self.assertIn(f"- Task store: `{store}`", plan.read_text(encoding="utf-8"))
                    if store == "beads":
                        self.assertIn("WARN [plan.beads-offline]", result)
                    state = next((root / str(path) for path in payload["outputs"] if str(path).endswith(".json")), None)
                    if state:
                        self.assertEqual(2, json.loads(state.read_text())["schema_version"])
                        self.assertNotIn("tasks", json.loads(state.read_text()))

    def test_direct_default_and_explicit_local(self):
        for args in (("--profile", "direct"), ("--profile", "direct", "--task-store", "local")):
            with self.subTest(args=args), workspace_tempdir() as tmp:
                root = Path(tmp)
                payload, _ = self.init(root, *args)
                plan = root / str(payload["outputs"][0])
                self.assertEqual("local", payload["task_store"])
                self.assertIn("[depends: T1]", plan.read_text())
                self.assertNotIn("### Phase 2", plan.read_text())

    def test_invalid_options_write_nothing(self):
        invalid = (
            ("--task-store", "unknown"), ("--task-store", "beads"),
            ("--beads-binding", "AGENTS.md"),
            ("--task-store", "beads", "--beads-binding", " "),
            ("--task-store", "beads", "--beads-binding", "C:/private/AGENTS.md"),
            ("--task-store", "beads", "--beads-binding", "/private/AGENTS.md"),
            ("--task-store", "beads", "--beads-binding", "AGENTS.md\n- Task store: local"),
            ("--task-store", "beads", "--beads-binding", "`AGENTS.md`"),
            ("--task-store", "beads", "--beads-binding", "NEEDS_FILL"),
            ("--task-store", "beads", "--beads-binding", "[todo]"),
            ("--task-store", "beads", "--beads-binding", "AGENTS.md\n"),
            ("--task-store", "beads", "--beads-binding", "#hub"),
            ("--task-store", "beads", "--beads-binding", "AGENTS.md", "--state-only"),
        )
        for args in invalid:
            with self.subTest(args=args), workspace_tempdir() as tmp:
                root = Path(tmp)
                self.write_files(root, {"keep.txt": "unchanged"})
                before = self.inventory(root)
                directories = set(root.rglob("*"))
                self.run_script(INIT, ["--task", "invalid", *args], root, 2)
                self.assertEqual(before, self.inventory(root))
                self.assertEqual(directories, set(root.rglob("*")))

    def test_collisions_are_atomic(self):
        for store in ("local", "beads"):
            with self.subTest(store=store), workspace_tempdir() as tmp:
                root = Path(tmp)
                profile = "direct" if store == "local" else "orchestrated"
                collision = (f"docs/_agent_plans/{STAMP}_adaptive-workflow.md" if store == "local"
                             else f"docs/agents/{STAMP}_adaptive-workflow-state.md")
                self.write_files(root, {collision: "existing bytes"})
                before = self.inventory(root)
                args = ["--task", "Adaptive workflow", "--timestamp", STAMP, "--profile", profile, "--task-store", store]
                if store == "beads":
                    args += ["--beads-binding", "AGENTS.md#external-hub"]
                self.run_script(INIT, args, root, 1)
                self.assertEqual(before, self.inventory(root))

    def test_no_tracker_or_network_operations(self):
        spec = importlib.util.spec_from_file_location("offline_workflow_init", INIT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with workspace_tempdir() as tmp, patch("subprocess.run", side_effect=AssertionError("live process")), patch("socket.create_connection", side_effect=AssertionError("network")):
            args = ["initializer", "--task", "Offline", "--task-store", "beads", "--beads-binding", "AGENTS.md#hub", "--plan-dir", str(Path(tmp) / "plans"), "--profile", "direct", "--dry-run"]
            with patch.object(sys, "argv", args):
                self.assertEqual(0, module.main())


class LocalGraphTest(TaskStoreFixture):
    def test_invalid_local_graph_properties(self):
        mutations = (
            ("T1:", "1bad:", "plan.local-task"),
            ("T2:", "T1:", "plan.local-id"),
            ("[depends: T1]", "[depends: missing]", "plan.local-dependency"),
            ("[depends: T1]", "[depends: T1, T1]", "plan.local-dependency"),
            ("[depends: T1]", "[depends: ]", "plan.local-dependency"),
            ("[depends: none]", "[depends: T4]", "plan.local-cycle"),
            ("[ ] T2:", "[x] T2:", "plan.local-progress"),
            ("[depends: T1]", "", "plan.local-task"),
        )
        for old, new, diagnostic in mutations:
            with self.subTest(diagnostic=diagnostic, new=new), workspace_tempdir() as tmp:
                root = Path(tmp)
                plan, _ = self.fixture(root)
                self.validate(root, plan)
                original = plan.read_bytes()
                self.edit(plan, old, new)
                self.assertIn(f"ERROR [{diagnostic}]", self.validate(root, plan, 1))
                plan.write_bytes(original)
                self.validate(root, plan)

    def test_unresolved_work_warns_in_draft_and_blocks_active_phase(self):
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            plan, _ = self.fixture(root)
            self.edit(plan, "Read the named sources", "NEEDS_FILL")
            self.assertIn("WARN [plan.local-task]", self.validate(root, plan))
            self.edit(plan, "- Status: pending", "- Status: in_progress")
            self.assertIn("ERROR [plan.local-task]", self.validate(root, plan, 1))

    def test_draft_placeholder_preserves_ids_and_defers_only_unknown_edges(self):
        spec = importlib.util.spec_from_file_location("draft_workflow_validator", VALIDATE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        content = "- Task store: local\n- Task binding: not applicable\n- Status: planning\n### Phase 1\n- Status: pending\n"
        content += "- [ ] T1: NEEDS_FILL [depends: none] [skills: inherit]\n- [ ] T2: outcome [depends: T1, NEEDS_FILL] [skills: inherit]"
        messages = module.validate_task_store(content, "planning")
        self.assertEqual(2, len(messages))
        self.assertTrue(all(message.startswith("WARN [plan.local-task]") for message in messages))
        active = content.replace("- Status: pending", "- Status: in_progress")
        self.assertTrue(all(message.startswith("ERROR [plan.local-task]") for message in module.validate_task_store(active, "planning")))
        broken = content.replace("T1, NEEDS_FILL", "missing, NEEDS_FILL")
        self.assertTrue(any(message.startswith("ERROR [plan.local-dependency]") for message in module.validate_task_store(broken, "planning")))

    def test_task_skill_override_is_validated(self):
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            plan, _ = self.fixture(root)
            self.edit(plan, "[skills: inherit]", "[skills: missing-owner]")
            self.assertIn("ERROR [plan.skills-mapping]", self.validate(root, plan, 1))
            self.edit(plan, "[skills: missing-owner]", "[skills: example-owner]")
            self.validate(root, plan)

    def test_completed_chain_and_large_chain_without_recursion(self):
        spec = importlib.util.spec_from_file_location("graph_workflow_validator", VALIDATE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for size in (10, 2000):
            content = "- Task store: local\n- Task binding: not applicable\n- Status: planning\n### Phase 1\n- Status: pending\n"
            content += "\n".join(f"- [x] T{i}: outcome [depends: {'none' if i == 1 else 'T' + str(i - 1)}] [skills: inherit]" for i in range(1, size + 1))
            self.assertEqual([], module.validate_task_store(content, "planning"))


class BeadsMappingTest(TaskStoreFixture):
    def test_opaque_ids_and_explicit_skill_override(self):
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            plan, _ = self.fixture(root, "beads")
            self.edit(plan, "opaque/1", "other-prefix:987")
            self.edit(plan, "[skills: inherit]", "[skills: example-owner]")
            self.assertIn("WARN [plan.beads-offline]", self.validate(root, plan))

    def test_duplicate_and_missing_issue_mappings(self):
        mutations = (
            ("opaque/3", "opaque/1"),
            ("  - Issue: opaque/1 [skills: inherit]\n  - Issue: opaque/2 [skills: inherit]", ""),
            ("opaque/1", ""),
        )
        for old, new in mutations:
            with self.subTest(new=new), workspace_tempdir() as tmp:
                root = Path(tmp)
                plan, _ = self.fixture(root, "beads")
                self.validate(root, plan)
                original = plan.read_bytes()
                self.edit(plan, old, new)
                self.assertIn("ERROR [plan.beads-mapping]", self.validate(root, plan, 1))
                plan.write_bytes(original)
                self.validate(root, plan)

    def test_mixed_stores_and_missing_skills(self):
        for replacement, diagnostic in (
            ("- [ ] Local work. [skills: inherit]", "plan.beads-local-tasks"),
            ("1. Local work. [skills: inherit]", "plan.beads-local-tasks"),
            ("- Issue: opaque/1", "plan.skills-mapping"),
            ("- Issue: opaque/1 [skills: missing-owner]", "plan.skills-mapping"),
        ):
            with self.subTest(replacement=replacement), workspace_tempdir() as tmp:
                root = Path(tmp)
                plan, _ = self.fixture(root, "beads")
                self.edit(plan, "- Issue: opaque/1 [skills: inherit]", replacement)
                self.assertIn(f"ERROR [{diagnostic}]", self.validate(root, plan, 1))

    def test_issue_mapping_cannot_escape_phase(self):
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            plan, _ = self.fixture(root, "beads")
            with plan.open("a", encoding="utf-8") as stream:
                stream.write("\n## Other work\n- Issue: escaped [skills: inherit]\n")
            self.assertIn("ERROR [plan.skills-structure]", self.validate(root, plan, 1))

    def test_unresolved_active_phase_despite_planning_header(self):
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            plan, _ = self.fixture(root, "beads")
            self.edit(plan, "opaque/1", "NEEDS_FILL_ISSUE_1")
            self.assertIn("WARN [plan.beads-mapping]", self.validate(root, plan))
            self.edit(plan, "- Status: pending", "- Status: in_progress")
            self.assertIn("ERROR [plan.beads-mapping]", self.validate(root, plan, 1))


class FamilyConsistencyTest(TaskStoreFixture):
    def test_headers_mark_even_legacy_families(self):
        changes = (
            ("- Task store: `local`\n", ""), ("- Task binding: not applicable\n", ""),
            ("- Task store: `local`", "- Task store: `local`\n- Task store: `beads`"),
            ("- Task binding: not applicable", "- Task binding: not applicable\n- Task binding: other"),
            ("- Task store: `local`", "- Task store: `unknown`"),
        )
        for old, new in changes:
            with self.subTest(new=new), workspace_tempdir() as tmp:
                root = Path(tmp)
                plan, _ = self.fixture(root, profile="legacy")
                self.validate(root, plan)
                self.edit(plan, old, new)
                self.assertIn("ERROR [plan.task-store]", self.validate(root, plan, 1))

    def test_binding_pair_and_local_issue_rejection(self):
        for store, old, new, diagnostic in (
            ("local", "not applicable", "AGENTS.md", "plan.task-binding"),
            ("beads", "AGENTS.md#task-binding", "C:/machine/AGENTS.md", "plan.task-binding"),
            ("local", "- Work:", "- Work:\n  - Issue: mixed [skills: inherit]", "plan.local-issue-mapping"),
        ):
            with self.subTest(store=store, new=new), workspace_tempdir() as tmp:
                root = Path(tmp)
                plan, _ = self.fixture(root, store)
                self.edit(plan, old, new)
                self.assertIn(f"ERROR [{diagnostic}]", self.validate(root, plan, 1))

    def test_independently_stale_status_snapshots(self):
        for target in ("plan", "checkpoint", "state"):
            with self.subTest(target=target), workspace_tempdir() as tmp:
                root = Path(tmp)
                plan, payload = self.fixture(root, profile="orchestrated")
                self.validate(root, plan)
                path = plan if target == "plan" else next(root / str(p) for p in payload["outputs"] if str(p).endswith(".json" if target == "state" else "-state.md"))
                self.edit(path, '"status": "planning"' if target == "state" else "- Status: planning", '"status": "draft"' if target == "state" else "- Status: draft")
                output = self.validate(root, plan, 1)
                self.assertIn("snapshot-status]", output)

    def test_stale_cursor_fields_and_whole_scalar_projection(self):
        for field in ("current_phase", "next_actions", "blockers"):
            with self.subTest(field=field), workspace_tempdir() as tmp:
                root = Path(tmp)
                plan, payload = self.fixture(root, profile="orchestrated")
                state = next(root / str(p) for p in payload["outputs"] if str(p).endswith(".json"))
                data = json.loads(state.read_text())
                original = state.read_bytes()
                data[field] = "Wrong phase" if field == "current_phase" else ["wrong snapshot"]
                state.write_text(json.dumps(data), encoding="utf-8")
                self.assertIn(f"ERROR [state.snapshot-{field}]", self.validate(root, plan, 1))
                state.write_bytes(original)
                self.validate(root, plan)
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            plan, payload = self.fixture(root, profile="orchestrated")
            checkpoint = next(root / str(p) for p in payload["outputs"] if str(p).endswith("-state.md"))
            state = next(root / str(p) for p in payload["outputs"] if str(p).endswith(".json"))
            action = "Inspect a, b; retain c."
            self.edit(checkpoint, "Complete the plan's repository-grounding fields.", action)
            data = json.loads(state.read_text())
            data["next_actions"] = [action]
            state.write_text(json.dumps(data), encoding="utf-8")
            self.validate(root, plan)
            data["next_actions"] = ["Inspect a", "b", "retain c."]
            state.write_text(json.dumps(data), encoding="utf-8")
            self.assertIn("ERROR [state.snapshot-next_actions]", self.validate(root, plan, 1))

    def test_wrong_directory_same_basename_every_companion(self):
        for kind in ("checkpoint", "state", "prompts"):
            with self.subTest(kind=kind), workspace_tempdir() as tmp:
                root = Path(tmp)
                plan, payload = self.fixture(root, profile="legacy")
                selected = next(root / str(p) for p in payload["outputs"] if str(p).endswith({"checkpoint": "-state.md", "state": ".json", "prompts": "__phase-prompts.md"}[kind]))
                self.edit(selected, str(plan.relative_to(root)).replace("\\", "/"), "other/" + plan.name)
                self.assertIn(f"ERROR [{kind}.plan]", self.validate(root, plan, 1))

    def test_duplicate_cursor_owner_and_direct_fallback(self):
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            plan, _ = self.fixture(root, profile="resumable")
            with plan.open("a", encoding="utf-8") as stream:
                stream.write("\n- Next action: duplicated.\n")
            self.assertIn("ERROR [family.cursor-owner]", self.validate(root, plan, 1))
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            plan, _ = self.fixture(root)
            self.edit(plan, "- Current phase: Phase 1\n", "")
            self.assertIn("ERROR [family.cursor]", self.validate(root, plan, 1))

    def test_completed_unmarked_history_is_unchanged(self):
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            self.write_files(root, LEGACY_PACK)
            plan = root / next(path for path in LEGACY_PACK if path.endswith("legacy-pack.md"))
            before = self.inventory(root)
            self.validate(root, plan)
            self.assertEqual(before, self.inventory(root))


class ReviewRepairTest(TaskStoreFixture):
    def test_local_rejects_escaped_issue_with_known_or_unknown_skills(self):
        for skill in ("example-owner", "missing-owner"):
            with self.subTest(skill=skill), workspace_tempdir() as tmp:
                root = Path(tmp)
                plan, _ = self.fixture(root)
                self.validate(root, plan)
                original = plan.read_bytes()
                with plan.open("a", encoding="utf-8") as stream:
                    stream.write(f"\n## Other work\n- Issue: external:99 [skills: {skill}]\n")
                self.assertIn("ERROR [plan.local-issue-mapping]", self.validate(root, plan, 1))
                plan.write_bytes(original)
                self.validate(root, plan)

    def test_empty_cursor_fields_keep_empty_array_and_nonempty_value(self):
        for label, key, original, value in (
            ("Blockers", "blockers", "none known", "Waiting for source."),
            ("Next action", "next_actions", "Complete the plan's repository-grounding fields.", "Inspect source."),
        ):
            with self.subTest(label=label), workspace_tempdir() as tmp:
                root = Path(tmp)
                plan, payload = self.fixture(root, profile="orchestrated")
                checkpoint = next(root / str(path) for path in payload["outputs"] if str(path).endswith("-state.md"))
                state = next(root / str(path) for path in payload["outputs"] if str(path).endswith(".json"))
                self.validate(root, plan)
                data = json.loads(state.read_text())
                self.edit(checkpoint, f"- {label}: {original}", f"- {label}: {value}")
                data[key] = [value]
                state.write_text(json.dumps(data), encoding="utf-8")
                self.validate(root, plan)
                self.edit(checkpoint, f"- {label}: {value}", f"- {label}: ")
                data[key] = []
                state.write_text(json.dumps(data), encoding="utf-8")
                self.validate(root, plan)
                spec = importlib.util.spec_from_file_location("empty_field_validator", VALIDATE)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.assertEqual("", module.field_value(checkpoint.read_text(), label))
                self.assertEqual(value, module.field_value(f"- {label}: {value}\n- Other: following field\n", label))

    def test_beads_reserved_local_binding_rejects_before_any_write(self):
        for binding in ("not applicable", "  not applicable  "):
            with self.subTest(binding=binding), workspace_tempdir() as tmp:
                root = Path(tmp)
                self.write_files(root, {"keep.txt": "preserved bytes"})
                before = self.inventory(root)
                paths = set(root.rglob("*"))
                result = self.run_script(INIT, ["--task", "Reserved binding", "--task-store", "beads", "--beads-binding", binding], root, 2)
                self.assertIn("MISUSE:", result.stderr)
                self.assertIn("not applicable", result.stderr)
                self.assertEqual(before, self.inventory(root))
                self.assertEqual(paths, set(root.rglob("*")))


class HierarchyUnitTest(unittest.TestCase):
    """Topic: hierarchy/cadence/cursor; layer: pure parser unit checks."""

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("hierarchy_validator", VALIDATE)
        cls.validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.validator)

    def content(self):
        return """# Plan
- Task store: beads
- Task binding: AGENTS.md#beads
- Task hierarchy: phase-task-subtask
- Review boundary: final
- Final phase: Phase 1
- Commit authority: not granted
- Status: executing
### Phase 1 - Implement
- Phase issue: phase/one
- Status: in_progress
- Required skills: exact-owner
- Work:
  - Task issue: task/one [skills: inherit]
    - Subtask issue: leaf/one [skills: inherit]
  - Task issue: task/two [skills: inherit]
    - Subtask issue: leaf/two [skills: inherit]
- Review status: REVIEW_PENDING
- Review evidence: not run
- Validation commands: python -B targeted_check.py
- Evidence observed: selected tests passed; snapshot evidence.md
## Execution Position
- Current phase: Phase 1
- Current task: task/one
- Current subtask: leaf/one
- Next action: Run leaf selector.
- Blockers: none
"""

    def errors(self, content):
        return [line for line in self.validator.validate_task_store(content, "executing") if line.startswith("ERROR")]

    def test_valid_three_level_containment_does_not_invent_prerequisites(self):
        nodes, messages = self.validator.hierarchy_nodes(self.content(), "executing")
        self.assertEqual([], messages)
        self.assertEqual(("subtask", "task/one", "Phase 1"), nodes["leaf/one"])
        self.assertEqual(("task", "phase/one", "Phase 1"), nodes["task/two"])
        self.assertEqual([], self.errors(self.content()))

    def test_optional_engagement_root_header_is_not_an_escaped_phase_node(self):
        content = self.content().replace("- Task store: beads", "- Root issue: `engagement`; discovered-from `origin`\n- Task store: beads")
        self.assertEqual([], self.errors(content))
        escaped = self.content() + "\n- Root issue: escaped\n"
        self.assertTrue(self.errors(escaped))

    def test_missing_duplicate_orphan_and_unknown_levels_are_refused(self):
        changes = (
            ("- Phase issue: phase/one\n", ""),
            ("leaf/two", "leaf/one"),
            ("  - Task issue: task/one [skills: inherit]\n", ""),
            ("    - Subtask issue: leaf/two [skills: inherit]\n", ""),
            ("    - Subtask issue:", "    - Leaf issue:"),
            ("    - Subtask issue:", "  - Subtask issue:"),
            ("task/one [skills", " [skills"),
            ("## Execution Position", "## Outside\n  - Task issue: escaped [skills: inherit]\n## Execution Position"),
        )
        for old, new in changes:
            with self.subTest(change=(old, new)):
                self.assertTrue(self.errors(self.content().replace(old, new, 1)))

    def test_binding_marker_and_mixed_store_cannot_bypass_hierarchy(self):
        for old, new in (
            ("Task store: beads", "Task store: local"),
            ("Task binding: AGENTS.md#beads", "Task binding: not applicable"),
            ("Task binding: AGENTS.md#beads", "Task binding: C:/private/AGENTS.md"),
            ("Task hierarchy: phase-task-subtask", "Task hierarchy: flat"),
            ("Task hierarchy: phase-task-subtask", "Task hierarchy: phase-task-subtask\n- Task hierarchy: phase-task-subtask"),
            ("- Work:", "- Work:\n  - Issue: flat [skills: inherit]"),
            ("- Work:", "- Work:\n  - [ ] T1: local [depends: none] [skills: inherit]"),
        ):
            with self.subTest(change=(old, new)):
                self.assertTrue(self.errors(self.content().replace(old, new, 1)))

    def test_unresolved_nodes_warn_only_before_execution(self):
        draft = self.content().replace("leaf/one", "NEEDS_FILL_LEAF").replace("- Status: in_progress", "- Status: pending").replace("- Status: executing", "- Status: planning")
        messages = self.validator.validate_task_store(draft, "planning")
        self.assertFalse(any(line.startswith("ERROR") for line in messages), messages)
        self.assertTrue(any(line.startswith("WARN [plan.hierarchy]") for line in messages))
        self.assertTrue(self.errors(draft))

    def test_cursor_requires_mapped_phase_task_and_its_actual_subtask(self):
        def check(content):
            return self.validator.validate_family_snapshots(Path("plan.md"), content, {"checkpoint": None, "state": None, "prompts": None})
        self.assertEqual([], check(self.content()))
        for old, new in (
            ("Current phase: Phase 1", "Current phase: Phase 9"),
            ("Current task: task/one", "Current task: leaf/one"),
            ("Current task: task/one", "Current task: none"),
            ("Current subtask: leaf/one", "Current subtask: leaf/two"),
            ("Current subtask: leaf/one", "Current subtask: unknown"),
            ("- Current subtask: leaf/one\n", ""),
            ("- Current task: task/one", "- Current task: task/one\n- Current task: task/two"),
        ):
            with self.subTest(change=(old, new)):
                self.assertTrue(check(self.content().replace(old, new, 1)))

    def test_removed_hierarchy_guard_is_detected_by_the_negative_oracle(self):
        malformed = self.content().replace("  - Task issue: task/one [skills: inherit]\n", "")
        self.assertTrue(self.errors(malformed))
        # Scratch mutation: remove the owned containment control in memory. The
        # negative oracle must fail, without editing the source or hiding a survivor.
        with patch.object(self.validator, "hierarchy_nodes", return_value=({}, [])):
            with self.assertRaisesRegex(AssertionError, "Missing hierarchy rejection"):
                self.assertTrue(self.errors(malformed), "Missing hierarchy rejection")

    def test_final_only_intermediate_milestone_keeps_review_pending(self):
        first, cursor = self.content().split("## Execution Position", 1)
        second = first.split("### Phase 1 - Implement", 1)[1]
        for old, new in (("phase/one", "phase/final"), ("task/one", "task/final"), ("task/two", "task/final-two"), ("leaf/one", "leaf/final"), ("leaf/two", "leaf/final-two")):
            second = second.replace(old, new)
        family = first.replace("Final phase: Phase 1", "Final phase: Phase 2").replace("Status: in_progress", "Status: complete") + "### Phase 2 - Accept" + second + "## Execution Position" + cursor
        self.assertEqual([], self.errors(family))
        reviewed_early = family.replace("Review status: REVIEW_PENDING", "Review status: APPROVED", 1).replace("Review evidence: not run", "Review evidence: review.md", 1)
        self.assertTrue(self.errors(reviewed_early))

    def test_commits_require_authority_and_accepted_boundary_not_leaf_review(self):
        commit = self.content().replace("- Review status:", "- Commit: abc1234\n- Review status:")
        self.assertTrue(self.errors(commit))
        accepted = commit.replace("Commit authority: not granted", "Commit authority: explicit user grant: current user instruction; accepted scoped changes").replace("Review status: REVIEW_PENDING", "Review status: APPROVED").replace("Review evidence: not run", "Review evidence: review.md; snapshot abc1234; fixes/retests passed").replace("Status: in_progress", "Status: complete")
        self.assertEqual([], self.errors(accepted))
        self.assertTrue(self.errors(accepted.replace("- Commit: abc1234", "    - Commit: abc1234")))
        self.assertTrue(self.errors(accepted.replace("Review evidence: review.md; snapshot abc1234; fixes/retests passed", "Review evidence: not run")))
        self.assertTrue(self.errors(accepted.replace("Status: complete", "Status: failed")))
        self.assertTrue(self.errors(accepted.replace("Evidence observed: selected tests passed; snapshot evidence.md", "Evidence observed: not run")))
        self.assertTrue(self.errors(self.content().replace("Final phase: Phase 1", "Final phase: Phase 9")))

    def test_completed_required_boundary_rejects_missing_or_unrun_validation(self):
        accepted = self.content().replace("- Status: executing", "- Status: complete").replace("Status: in_progress", "Status: complete").replace("Review status: REVIEW_PENDING", "Review status: APPROVED").replace("Review evidence: not run", "Review evidence: final-review.md; exact candidate")
        self.assertEqual([], self.errors(accepted))
        for old, new in (
            ("- Evidence observed: selected tests passed; snapshot evidence.md", ""),
            ("Evidence observed: selected tests passed; snapshot evidence.md", "Evidence observed: "),
            ("Evidence observed: selected tests passed; snapshot evidence.md", "Evidence observed: NOT RUN"),
            ("Evidence observed: selected tests passed; snapshot evidence.md", "Evidence observed: not_run; required check pending"),
            ("Evidence observed: selected tests passed; snapshot evidence.md", "Evidence observed: NEEDS_FILL"),
            ("- Validation commands: python -B targeted_check.py", ""),
            ("Validation commands: python -B targeted_check.py", "Validation commands: none"),
            ("Evidence observed: selected tests passed; snapshot evidence.md", "Evidence observed: not applicable (no behavior changed)"),
        ):
            with self.subTest(change=(old, new)):
                errors = self.errors(accepted.replace(old, new))
                self.assertTrue(any("[plan.boundary-validation]" in line for line in errors), errors)

    def test_accepted_completed_phase_boundary_requires_validation_before_engagement_completion(self):
        content = self.content().replace("Review boundary: final", "Review boundary: phase").replace("Status: in_progress", "Status: complete").replace("Review status: REVIEW_PENDING", "Review status: APPROVED").replace("Review evidence: not run", "Review evidence: phase-review.md")
        self.assertEqual([], self.errors(content))
        broken = content.replace("Evidence observed: selected tests passed; snapshot evidence.md", "Evidence observed: not run")
        self.assertTrue(any("[plan.boundary-validation]" in line for line in self.errors(broken)))

    def test_completed_boundary_accepts_only_explicit_justified_no_validation(self):
        content = self.content().replace("- Status: executing", "- Status: complete").replace("Status: in_progress", "Status: complete").replace("Review status: REVIEW_PENDING", "Review status: APPROVED").replace("Review evidence: not run", "Review evidence: final-review.md")
        content = content.replace("Validation commands: python -B targeted_check.py", "Validation commands: none (read-only decision; no executable surface changed)").replace("Evidence observed: selected tests passed; snapshot evidence.md", "Evidence observed: not applicable (read-only decision; no executable surface changed)")
        self.assertEqual([], self.errors(content))
        for old, new in (
            ("none (read-only decision; no executable surface changed)", "none ()"),
            ("not applicable (read-only decision; no executable surface changed)", "not applicable"),
            ("not applicable (read-only decision; no executable surface changed)", "not run"),
        ):
            with self.subTest(change=(old, new)):
                self.assertTrue(any("[plan.boundary-validation]" in line for line in self.errors(content.replace(old, new))))

    def test_final_boundary_reuses_aggregate_without_intermediate_review(self):
        first, cursor = self.content().split("## Execution Position", 1)
        second = first.split("### Phase 1 - Implement", 1)[1]
        for old, new in (("phase/one", "phase/final"), ("task/one", "task/final"), ("task/two", "task/final-two"), ("leaf/one", "leaf/final"), ("leaf/two", "leaf/final-two")):
            second = second.replace(old, new)
        second = second.replace("Review status: REVIEW_PENDING", "Review status: APPROVED").replace("Review evidence: not run", "Review evidence: final-review.md; all phase candidates").replace("Evidence observed: selected tests passed; snapshot evidence.md", "Evidence observed: aggregate passed covering Phase 1 and Phase 2; candidate evidence.md")
        family = first.replace("Final phase: Phase 1", "Final phase: Phase 2").replace("Evidence observed: selected tests passed; snapshot evidence.md", "Evidence observed: not run; covered by final aggregate") + "### Phase 2 - Accept" + second + "## Execution Position" + cursor
        family = family.replace("Status: executing", "Status: complete").replace("Status: in_progress", "Status: complete")
        self.assertEqual([], self.errors(family))

    def test_nested_final_only_local_name_match_cannot_claim_engagement_acceptance(self):
        nested = self.content().replace("- Final phase: Phase 1", "- Final phase: Phase 1\n- Local final phase: Phase 1\n- Parent plan: root.md")
        self.assertEqual([], self.errors(nested))
        accepted = nested.replace("Review status: REVIEW_PENDING", "Review status: APPROVED").replace("Review evidence: not run", "Review evidence: local-review.md")
        self.assertTrue(any("[plan.review-boundary]" in line for line in self.errors(accepted)))

    def test_parent_resolution_has_a_finite_ancestry_bound(self):
        root = self.content()
        def ancestor(path):
            number = int(path.stem)
            return root if number == 64 else root.replace("- Final phase: Phase 1", f"- Final phase: Phase 1\n- Local final phase: Phase 1\n- Parent plan: {number + 1}.md")
        with patch.object(self.validator, "read_text", side_effect=ancestor):
            with self.assertRaisesRegex(ValueError, "64-plan bound"):
                self.validator.resolve_review_contract(Path("bounded-ancestry-fixture/0.md"))


class HierarchyCliTest(unittest.TestCase):
    """Topic: new-family generation; layer: offline CLI contract checks."""

    run_script = WorkflowFilesTest.run_script
    init = WorkflowFilesTest.init
    fill_skills = WorkflowFilesTest.fill_skills
    write_files = WorkflowFilesTest.write_files
    edit = WorkflowFilesTest.edit

    def test_new_phased_generation_requires_explicit_binding_without_writes(self):
        for args in ([], ["--profile", "orchestrated"], ["--task-store", "local"], ["--profile", "direct", "--mode", "delegated"], ["--state-only", "--mode", "delegated"]):
            with self.subTest(args=args), workspace_tempdir() as tmp:
                root = Path(tmp)
                self.run_script(INIT, ["--task", "Unbound", *args], root, 2)
                self.assertEqual([], list(root.rglob("*")))

    def test_new_hierarchy_round_trip_and_schema3_cursor(self):
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root, "--profile", "orchestrated", "--review-boundary", "final")
            plan = root / str(payload["outputs"][0])
            self.fill_skills(root, plan)
            self.assertIn("- Task hierarchy: phase-task-subtask", plan.read_text())
            self.assertIn("- Review boundary: final", plan.read_text())
            self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root)
            state = next(root / str(path) for path in payload["outputs"] if str(path).endswith(".json"))
            data = json.loads(state.read_text())
            self.assertEqual(3, data["schema_version"])
            self.assertEqual("none", data["current_task"])
            data["current_subtask"] = "wrong"
            state.write_text(json.dumps(data), encoding="utf-8")
            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root, 1)
            self.assertIn("state.snapshot-current_subtask", result.stdout)

    def test_hierarchy_skill_override_inherits_the_task_not_the_phase(self):
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root)
            plan = root / str(payload["outputs"][0])
            self.fill_skills(root, plan)
            self.write_files(root, {"skills/other-owner/SKILL.md": "---\nname: other-owner\n---\n"})
            self.edit(plan, SKILL_ROW, SKILL_ROW + "\n| other-owner | skills/other-owner/SKILL.md | changes | always | stop |")
            self.edit(plan, "Task issue: opaque-task-1 [skills: inherit]", "Task issue: opaque-task-1 [skills: other-owner]")
            self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root)
            self.edit(plan, "Task issue: opaque-task-1 [skills: other-owner]", "Task issue: opaque-task-1 [skills: missing-owner]")
            result = self.run_script(VALIDATE, ["--plan", str(plan.relative_to(root))], root, 1)
            self.assertIn("ERROR [plan.skills-mapping] Phase 1 - Ground and implement subtask 'opaque-subtask-1 [skills: inherit]' refers to unbound skills: missing-owner.", result.stdout)

    def test_nested_initialization_inherits_canonical_cadence_and_keeps_local_identity(self):
        for boundary in ("phase", "final"):
            with self.subTest(boundary=boundary), workspace_tempdir() as tmp:
                root = Path(tmp)
                parent, _ = self.init(root, "--review-boundary", boundary)
                parent_path = root / str(parent["outputs"][0])
                self.edit(parent_path, "Final phase: Phase 2", "Final phase: Phase 4")
                self.edit(parent_path, "### Phase 2 -", "### Phase 4 -")
                original = parent_path.read_bytes()
                current = str(parent_path.relative_to(root))
                for lane, override in (("child", []), ("grandchild", ["--review-boundary", boundary])):
                    result = self.run_script(INIT, ["--task", lane, "--parent-plan", current, "--profile", "direct", "--task-store", "beads", "--beads-binding", "AGENTS.md#beads", *override], root)
                    current = json.loads(result.stdout)["outputs"][0]
                    child = root / current
                    content = child.read_text(encoding="utf-8")
                    self.assertIn(f"- Review boundary: {boundary}\n", content)
                    self.assertIn("- Final phase: Phase 4\n- Local final phase: Phase 1\n", content)
                    self.assertIn("- Current phase: Phase 1\n", content)
                    self.assertNotIn("### Phase 4", content)
                    self.run_script(VALIDATE, ["--plan", current], root)
                self.assertEqual(original, parent_path.read_bytes())

    def test_nested_conflicting_override_is_rejected_without_writes(self):
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            parent, _ = self.init(root, "--review-boundary", "final")
            before = {str(p): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            paths = set(root.rglob("*"))
            result = self.run_script(INIT, ["--task", "Rejected", "--parent-plan", str(parent["outputs"][0]), "--review-boundary", "phase", "--task-store", "beads", "--beads-binding", "AGENTS.md#beads"], root, 2)
            self.assertIn("conflicts with the canonical parent", result.stderr)
            self.assertEqual(before, {str(p): p.read_bytes() for p in root.rglob("*") if p.is_file()})
            self.assertEqual(paths, set(root.rglob("*")))

    def test_nested_malformed_or_unresolvable_parent_refuses_before_writes(self):
        changes = (
            ("- Review boundary: final", "- Review boundary: final\n- Review boundary: phase"),
            ("- Final phase: Phase 2\n", ""),
            ("Final phase: Phase 2", "Final phase: Phase 99"),
            ("Review boundary: final", "Review boundary: NEEDS_FILL"),
            ("- Parent plan: not created", "- Parent plan: absent.md\n- Local final phase: Phase 2"),
            ("- Parent plan: not created", "- Parent plan: absent.md\n- Parent plan: another.md"),
            ("### Phase 2 -", "### Phase 1 -"),
        )
        for old, new in changes:
            with self.subTest(change=(old, new)), workspace_tempdir() as tmp:
                root = Path(tmp)
                parent, _ = self.init(root, "--review-boundary", "final")
                self.edit(root / str(parent["outputs"][0]), old, new)
                before = {str(p): p.read_bytes() for p in root.rglob("*") if p.is_file()}
                paths = set(root.rglob("*"))
                result = self.run_script(INIT, ["--task", "Rejected", "--parent-plan", str(parent["outputs"][0]), "--task-store", "beads", "--beads-binding", "AGENTS.md#beads"], root, 2)
                self.assertIn("Cannot inherit parent review contract", result.stderr)
                self.assertEqual(before, {str(p): p.read_bytes() for p in root.rglob("*") if p.is_file()})
                self.assertEqual(paths, set(root.rglob("*")))

    def test_nested_cycle_and_legacy_cadence_refuse_without_migration(self):
        for kind in ("cycle", "legacy"):
            with self.subTest(kind=kind), workspace_tempdir() as tmp:
                root = Path(tmp)
                if kind == "legacy":
                    self.write_files(root, LEGACY_PACK)
                    parent_path = next(iter(LEGACY_PACK))
                    self.run_script(VALIDATE, ["--plan", parent_path], root)
                else:
                    parent, _ = self.init(root)
                    parent_path = str(parent["outputs"][0])
                    self.edit(root / parent_path, "- Parent plan: not created", f"- Parent plan: `{parent_path}`\n- Local final phase: Phase 2")
                before = {str(p): p.read_bytes() for p in root.rglob("*") if p.is_file()}
                result = self.run_script(INIT, ["--task", "Rejected", "--parent-plan", parent_path, "--task-store", "beads", "--beads-binding", "AGENTS.md#beads"], root, 2)
                self.assertIn("cycle" if kind == "cycle" else "explicitly reconcile legacy", result.stderr)
                self.assertEqual(before, {str(p): p.read_bytes() for p in root.rglob("*") if p.is_file()})

    def test_nested_validation_rejects_drifted_canonical_ancestry(self):
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            parent, _ = self.init(root, "--review-boundary", "final")
            child, _ = self.init(root, "--parent-plan", str(parent["outputs"][0]), "--lane", "child")
            child_path = root / str(child["outputs"][0])
            self.run_script(VALIDATE, ["--plan", str(child_path.relative_to(root))], root)
            self.edit(root / str(parent["outputs"][0]), "Review boundary: final", "Review boundary: phase")
            result = self.run_script(VALIDATE, ["--plan", str(child_path.relative_to(root))], root, 1)
            self.assertIn("ERROR [plan.review-inheritance]", result.stdout)

    def test_reviewer_prompt_covers_the_entire_declared_boundary(self):
        with workspace_tempdir() as tmp:
            root = Path(tmp)
            payload, _ = self.init(root, "--with-prompts", "--review-boundary", "final")
            prompt = (root / str(payload["outputs"][1])).read_text(encoding="utf-8")
            reviewer = prompt.split("## Independent reviewer", 1)[1].split("## Documenter", 1)[0]
            outcome = reviewer.split("**Outcome:**", 1)[1].split("**Read first:**", 1)[0]
            read_first = reviewer.split("**Read first:**", 1)[1].split("**Scope:**", 1)[0]
            done = reviewer.split("**Done:**", 1)[1].split("**Blocked:**", 1)[0]
            for required in ("complete phase candidate", "complete engagement candidate", "all earlier phases with pending review"):
                self.assertIn(required, outcome)
            for required in ("canonical engagement plan", "entire selected phase", "every engagement phase including earlier pending phases"):
                self.assertIn(required, read_first)
            self.assertIn("entire declared boundary", done)
            self.assertIn("incomplete phase or engagement coverage blocks acceptance", done)


if __name__ == "__main__":
    unittest.main()
