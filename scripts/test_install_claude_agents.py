"""Focused filesystem tests for the personal Claude agent installer."""

import contextlib
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts import install_claude_agents as installer


class InstallClaudeAgentsTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.home = self.root / "profile"
        self.make_profile(self.home)
        self.legacy = self.home / "skills" / installer.WRITER
        self.target = self.home / "agents" / installer.WRITER_SOURCE.name
        self.writer = installer.WRITER_SOURCE.read_bytes()

    @staticmethod
    def make_profile(home):
        skill = home / "skills/alaa-prompting-guide/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("# Prompting guide\n")

    def seed_legacy(self):
        manifest = self.legacy / installer.MANIFEST
        manifest.parent.mkdir(parents=True)
        manifest.write_text('{"name":"alaa-rule-writer","version":"1.0.0"}\n')
        old_agent = self.legacy / "agents" / self.target.name
        old_agent.parent.mkdir()
        old_agent.write_bytes(b"plugin writer")
        (self.legacy / "extra.txt").write_bytes(b"retained")
        return manifest

    @staticmethod
    def snapshot(root):
        result = {}
        for path in sorted(root.rglob("*")):
            if path.is_symlink():
                value = ("symlink", os.readlink(path))
            elif path.is_dir():
                value = ("directory",)
            else:
                value = ("file", path.read_bytes())
            result[path.relative_to(root)] = value
        return result

    def invoke(self, *args, explicit_home=True):
        argv = ["--claude-home", str(self.home)] if explicit_home else []
        out, error = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(error):
            code = installer.main([*argv, *args])
        return code, out.getvalue(), error.getvalue()

    def apply_writer(self):
        return self.invoke("--apply", "--only", installer.WRITER)

    def archives(self):
        return sorted((self.home / installer.ARCHIVE_DIR).glob("install-*"))

    def assert_refused(self, fragment, *args):
        before = self.snapshot(self.root)
        code, _, error = self.invoke("--apply", *args)
        self.assertNotEqual(code, 0)
        self.assertIn(fragment, error)
        self.assertEqual(before, self.snapshot(self.root))

    def test_destination_symlink_blocks_every_selected_write(self):
        self.seed_legacy()
        self.target.parent.mkdir()
        other = self.root / "elsewhere.md"
        other.write_bytes(b"keep")
        self.target.symlink_to(other)
        self.assert_refused("Unexpected file type or symlink")

    def test_conflicting_archive_and_agents_paths_refuse_preflight(self):
        for name in ("agents", installer.ARCHIVE_DIR):
            with self.subTest(name=name):
                conflict = self.home / name
                conflict.write_bytes(b"keep")
                self.assert_refused("Unexpected file type or symlink")
                conflict.unlink()

    def test_symlinked_home_is_refused(self):
        alias = self.root / "alias"
        alias.symlink_to(self.home)
        before = self.snapshot(self.root)
        code, _, error = self.invoke(
            "--apply", "--claude-home", str(alias), explicit_home=False
        )
        self.assertEqual(code, 1)
        self.assertIn("symlink", error)
        self.assertEqual(before, self.snapshot(self.root))

    def test_legacy_manifest_conflicts_leave_profile_untouched(self):
        manifest = self.seed_legacy()
        for raw, expected in (
            ('{"name":', "Invalid plugin manifest"),
            ('{"name":"other"}', "Manifest name must be"),
            ('{"name":"other","name":"alaa-rule-writer"}', "Invalid plugin manifest"),
            ('{"name":"alaa-rule-writer","other":NaN}', "Invalid plugin manifest"),
        ):
            with self.subTest(raw=raw):
                manifest.write_text(raw)
                self.assert_refused(expected, "--only", installer.WRITER)

    def test_symlinked_plugin_member_is_refused(self):
        self.seed_legacy()
        (self.legacy / "unexpected").symlink_to(self.home / "skills")
        self.assert_refused("Unexpected file type or symlink", "--only", installer.WRITER)

    def test_missing_dependency_blocks_every_selected_write(self):
        dependency = self.home / "skills/alaa-prompting-guide/SKILL.md"
        dependency.unlink()
        self.assert_refused("Missing required personal skill")

    def test_unreadable_source_and_duplicate_destination_block_preflight(self):
        wrappers = self.root / "wrappers"
        wrappers.mkdir()
        wrapper = wrappers / self.target.name
        wrapper.symlink_to(installer.WRITER_SOURCE)
        with patch.object(installer, "ORCHESTRATOR_AGENTS", wrappers):
            self.assert_refused("Unexpected file type or symlink")
            wrapper.unlink()
            wrapper.write_bytes(self.writer)
            self.assert_refused("Duplicate agent destination")

    def test_publish_failure_preserves_previous_writer_and_plugin(self):
        self.seed_legacy()
        self.target.parent.mkdir()
        self.target.write_bytes(b"previous")
        legacy_before = self.snapshot(self.legacy)
        replace = os.replace

        def fail_install(staged, target):
            if target == self.target:
                raise OSError("publish failed")
            return replace(staged, target)

        with patch.object(installer.os, "replace", side_effect=fail_install):
            code, _, error = self.apply_writer()
        self.assertEqual(code, 2)
        self.assertIn("publish failed", error)
        self.assertEqual(self.target.read_bytes(), b"previous")
        self.assertEqual(self.snapshot(self.legacy), legacy_before)
        self.assertEqual(list(self.target.parent.iterdir()), [self.target])
        self.assertEqual((self.archives()[0] / self.target.name).read_bytes(), b"previous")
        self.assertEqual(self.apply_writer()[0], 0)
        self.assertEqual(self.target.read_bytes(), self.writer)
        self.assertFalse(self.legacy.exists())

    def test_archive_rename_failure_leaves_live_plugin_for_retry(self):
        self.seed_legacy()
        legacy_before = self.snapshot(self.legacy)
        with patch.object(Path, "rename", side_effect=OSError("archive failed")):
            code, _, error = self.apply_writer()
        self.assertEqual(code, 2)
        self.assertIn("archive failed", error)
        self.assertEqual(self.target.read_bytes(), self.writer)
        self.assertEqual(self.snapshot(self.legacy), legacy_before)
        self.assertEqual(self.apply_writer()[0], 0)
        archived = [archive / installer.WRITER for archive in self.archives()]
        archived = [plugin for plugin in archived if plugin.exists()]
        self.assertEqual(len(archived), 1)
        self.assertEqual(self.snapshot(archived[0]), legacy_before)
        self.assertFalse(self.legacy.exists())

    def test_preflight_under_cooperating_lock(self):
        self.seed_legacy()
        before = self.snapshot(self.root)
        with installer.installer_lock(self.home):
            code, _, error = self.apply_writer()
        self.assertEqual(code, 1)
        self.assertIn("holds the lock", error)
        self.assertEqual(before, self.snapshot(self.root))

    def test_default_preview_does_not_change_profile(self):
        self.seed_legacy()
        before = self.snapshot(self.root)
        code, out, error = self.invoke()
        self.assertEqual((code, error), (0, ""))
        self.assertIn(f"dry-run create: {self.target}", out)
        self.assertIn(f"dry-run archive: {self.legacy}", out)
        self.assertEqual(before, self.snapshot(self.root))

    def test_apply_all_installs_inventory_and_preserves_unrelated_state(self):
        self.target.parent.mkdir()
        extra = self.target.parent / "personal.md"
        extra.write_bytes(b"keep")
        settings = self.home / "settings.json"
        settings.write_bytes(b'{"custom":true}')
        registry = self.home / "plugins/installed_plugins.json"
        registry.parent.mkdir()
        registry.write_bytes(b'{"plugins":{}}')
        before = self.snapshot(self.home)
        code, _, error = self.invoke("--apply")
        self.assertEqual((code, error), (0, ""))
        wrappers = sorted(installer.ORCHESTRATOR_AGENTS.glob("*.md"))
        self.assertTrue(wrappers)
        expected = dict(before)
        for source in [*wrappers, installer.WRITER_SOURCE]:
            expected[Path("agents") / source.name] = ("file", source.read_bytes())
        self.assertEqual(self.snapshot(self.home), expected)

    def test_only_writer_preserves_other_agents_and_archives_both_old_versions(self):
        self.seed_legacy()
        legacy_before = self.snapshot(self.legacy)
        self.target.parent.mkdir()
        extra = self.target.parent / "alaa-verifier.md"
        extra.write_bytes(b"keep")
        self.target.write_bytes(b"previous standalone")
        code, _, error = self.apply_writer()
        self.assertEqual((code, error), (0, ""))
        self.assertEqual(set(self.target.parent.iterdir()), {self.target, extra})
        self.assertEqual(extra.read_bytes(), b"keep")
        self.assertEqual(self.target.read_bytes(), self.writer)
        archive, = self.archives()
        self.assertEqual((archive / self.target.name).read_bytes(), b"previous standalone")
        self.assertEqual(self.snapshot(archive / installer.WRITER), legacy_before)
        self.assertFalse(self.legacy.exists())

    def test_matching_writer_still_archives_legacy_once(self):
        self.seed_legacy()
        self.target.parent.mkdir()
        self.target.write_bytes(self.writer)
        self.assertEqual(self.apply_writer()[0], 0)
        archive, = self.archives()
        self.assertEqual(set(archive.iterdir()), {archive / installer.WRITER})
        before = self.snapshot(self.root)
        self.assertEqual(self.apply_writer()[0], 0)
        self.assertEqual(self.snapshot(self.root), before)

    def test_symlinked_prompting_skill_is_supported(self):
        installed_skill = self.home / "skills/alaa-prompting-guide"
        alternate = installed_skill.rename(self.root / "external-prompting-guide")
        installed_skill.symlink_to(alternate)
        self.assertEqual(self.apply_writer()[0], 0)
        self.assertEqual(self.target.read_bytes(), self.writer)
        self.assertTrue(installed_skill.is_symlink())

    def test_home_precedence_and_empty_env_fallback(self):
        fallback = self.root / "user" / ".claude"
        self.make_profile(fallback)
        alternate = self.root / "configured"
        self.make_profile(alternate)
        with patch.dict(os.environ, {"HOME": str(fallback.parent), "CLAUDE_CONFIG_DIR": str(alternate)}):
            self.assertEqual(self.apply_writer()[0], 0)
            self.assertTrue(self.target.exists())
            alt_target = alternate / "agents" / self.target.name
            self.assertFalse(alt_target.exists())
            self.assertEqual(self.invoke("--apply", "--only", installer.WRITER, explicit_home=False)[0], 0)
            self.assertTrue(alt_target.exists())
        with patch.dict(os.environ, {"HOME": str(fallback.parent), "CLAUDE_CONFIG_DIR": ""}):
            self.assertEqual(self.invoke("--apply", "--only", installer.WRITER, explicit_home=False)[0], 0)
        self.assertEqual((fallback / "agents" / self.target.name).read_bytes(), self.writer)

    def test_compatibility_entry_installs_only_writer(self):
        self.seed_legacy()
        entry = Path(installer.__file__).with_name("install_claude_rule_writer.py")
        command = [sys.executable, "-B", str(entry), "--claude-home", str(self.home)]
        before = self.snapshot(self.root)
        preview = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(preview.returncode, 0, preview.stderr)
        self.assertEqual(before, self.snapshot(self.root))
        result = subprocess.run([*command, "--apply"], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(list(self.target.parent.iterdir()), [self.target])
        self.assertEqual(self.target.read_bytes(), self.writer)
        self.assertFalse(self.legacy.exists())
