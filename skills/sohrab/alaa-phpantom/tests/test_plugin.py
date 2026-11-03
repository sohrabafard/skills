"""Offline integration tests for the self-contained skill/plugin pack.

No package installs. PHP CLI is optional for hook tests (skip when missing).
"""
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(command, *, payload=None, env=None, cwd=None):
    return subprocess.run(command, input=payload, text=True, capture_output=True,
                          env=env, cwd=cwd, timeout=15, check=False)


class PluginContract(unittest.TestCase):
    def test_manifest_and_lsp(self):
        manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        lsp = json.loads((ROOT / ".lsp.json").read_text())
        self.assertEqual(manifest["name"], "alaa-phpantom")
        self.assertEqual(lsp["phpantom"]["transport"], "stdio")
        self.assertEqual(lsp["phpantom"]["extensionToLanguage"][".blade.php"], "blade")
        command = Path(lsp["phpantom"]["command"])
        self.assertTrue(command.is_absolute(), "LSP must start the installed binary directly")
        self.assertEqual(command.name, "phpantom_lsp")
        self.assertFalse((ROOT / "bin").exists(), "The plugin must not bundle a launcher")
        self.assertNotIn("mcpServers", manifest)
        self.assertTrue((ROOT / "SKILL.md").read_text().startswith("---\n"))
        self.assertFalse((ROOT / "skills").exists(), "Root SKILL.md should be the only plugin skill")

    def test_hooks_registered_at_plugin_level(self):
        hooks = json.loads((ROOT / "hooks/hooks.json").read_text())["hooks"]
        post = hooks["PostToolUse"]
        self.assertEqual(len(post), 1)
        self.assertEqual(post[0]["matcher"], "Write|Edit")
        h = post[0]["hooks"][0]
        self.assertEqual(h["command"], "bash")
        self.assertEqual(h["args"], ["${CLAUDE_PLUGIN_ROOT}/scripts/php-lint.sh"])
        self.assertTrue((ROOT / "scripts/php-lint.sh").is_file())


@unittest.skipUnless(shutil.which("php"), "requires existing PHP CLI")
class HookContract(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)
        self.env = {**os.environ, "CLAUDE_PROJECT_DIR": str(self.path)}

    def event(self, file, tool="Edit"):
        return json.dumps({"tool_name": tool, "tool_input": {"file_path": str(file)}})

    def hook(self, payload, env=None):
        return run(["bash", str(ROOT / "scripts/php-lint.sh")], payload=payload,
                   env=(env or self.env), cwd=str(self.path))

    def test_good_php(self):
        f = self.path / "valid file.php"
        f.write_text("<?php\nfunction add(int $x): int { return $x + 1; }\n")
        out = self.hook(self.event(f))
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(out.stdout, "")

    def test_bad_php_feedback_exit_2(self):
        f = self.path / "bad.php"
        f.write_text("<?php function broken( {\n")
        out = self.hook(self.event(f))
        self.assertEqual(out.returncode, 2)
        self.assertIn("syntax error", out.stderr.lower())
        self.assertEqual(out.stdout, "")

    def test_blade_is_excluded(self):
        f = self.path / "index.blade.php"
        f.write_text("@if ($x) {{ $x }} @endif")
        out = self.hook(self.event(f))
        self.assertEqual(out.returncode, 0, out.stderr)

    def test_malformed_and_unrelated_payloads_are_ignored(self):
        self.assertEqual(self.hook("invalid-json").returncode, 0)
        f = self.path / "bad.php"
        f.write_text("<?php function broken( {\n")
        self.assertEqual(self.hook(self.event(f, tool="Bash")).returncode, 0)
        self.assertEqual(self.hook(self.event(f).replace('"Edit"', '"Read"')).returncode, 0)

    def test_outside_project_is_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "bad.php"
            f.write_text("<?php function broken( {\n")
            self.assertEqual(self.hook(self.event(f)).returncode, 0)

    def test_disabled_hook(self):
        f = self.path / "bad.php"
        f.write_text("<?php function broken( {\n")
        env = {**self.env, "ALAA_PHPANTOM_LINT": "0"}
        self.assertEqual(self.hook(self.event(f), env=env).returncode, 0)

    def test_symlink_outside_project_is_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            outside = Path(d) / "bad.php"
            outside.write_text("<?php function broken( {\n")
            inside = self.path / "link.php"
            inside.symlink_to(outside)
            self.assertEqual(self.hook(self.event(inside)).returncode, 0)


if __name__ == "__main__":
    unittest.main()
