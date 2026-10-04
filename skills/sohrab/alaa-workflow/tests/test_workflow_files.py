from __future__ import annotations

import json
import importlib.util
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
            payload, _ = self.init(root)
            plan = root / str(payload["outputs"][0])
            self.fill_skills(root, plan)
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
                INIT, ["--task", "Adaptive workflow", "--timestamp", STAMP, "--profile", "orchestrated"], root, expected=1
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
                ["--task", 'Quoted "task"', "--timestamp", STAMP, "--profile", "orchestrated"],
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


if __name__ == "__main__":
    unittest.main()
