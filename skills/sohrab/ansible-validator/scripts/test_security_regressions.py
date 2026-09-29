#!/usr/bin/env python3
"""Synthetic regressions: explicit Bash, no installed Ansible/Molecule or network."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest

BASH = ""
SKILL = Path(__file__).resolve().parent.parent


class SecurityRegressions(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="ansible-validator-test-")
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.env = os.environ.copy()
        for key in ("AV_ALLOW_BOOTSTRAP", "AV_NO_BOOTSTRAP", "AV_UNAVAILABLE_TOOLS",
                    "AV_SKILL_DIR", "BASH_ENV", "ENV"):
            self.env.pop(key, None)
        self.env.update(NO_COLOR="1", AV_CACHE_DIR=str(self.root / "cache"))
        # Pin nested Bash launches and standard POSIX tools to the chosen Bash.
        bash_dir = Path(BASH).parent
        candidates = [bash_dir, bash_dir.parent / "usr" / "bin"]
        self.env["PATH"] = os.pathsep.join(map(str, candidates)) + os.pathsep + self.env.get("PATH", "")

    def shell(self, command, env=None):
        return subprocess.run([BASH, "--noprofile", "--norc", "-c", command],
                              env=env or self.env, text=True, capture_output=True,
                              timeout=20, check=False)

    def script(self, name, *args, env=None):
        command = " ".join(shlex.quote(str(arg).replace("\\", "/")) for arg in
                           [BASH, SKILL / "scripts" / name, *args])
        return self.shell(command, env)

    def test_bootstrap_requires_explicit_opt_in(self):
        common = shlex.quote((SKILL / "scripts/lib/common.sh").as_posix())
        marker = shlex.quote((self.root / "installer-called").as_posix())
        # Shell function intercepts every Python invocation before an install.
        command = (f"source {common}; python3() {{ printf called > {marker}; return 1; }}; "
                   "av_bootstrap; exit $?")
        for allow, deny, expected_call in [(None, None, False), ("1", "1", False),
                                           ("yes", None, False), ("1", None, True)]:
            with self.subTest(allow=allow, deny=deny):
                env = self.env.copy()
                if allow is not None:
                    env["AV_ALLOW_BOOTSTRAP"] = allow
                if deny is not None:
                    env["AV_NO_BOOTSTRAP"] = deny
                result = self.shell(command, env)
                self.assertEqual(result.returncode, 1, "bootstrap must remain unsuccessful")
                self.assertEqual((self.root / "installer-called").exists(), expected_call)
                if not expected_call:
                    self.assertFalse((self.root / "cache").exists())

    def test_existing_cache_needs_no_install_authority(self):
        common = shlex.quote((SKILL / "scripts/lib/common.sh").as_posix())
        marker = shlex.quote((self.root / "installer-called").as_posix())
        command = (
            f"source {common}; "
            'key="$(av_hash_file "$(av_requirements_file)")"; '
            'bindir="$(av_cache_root)/venv-$key/bin"; mkdir -p "$bindir"; '
            'printf "#!/usr/bin/env bash\\nexit 0\\n" > "$bindir/python"; '
            'cp "$bindir/python" "$bindir/fixture-cached-tool"; chmod +x "$bindir/"*; '
            f"python3() {{ printf called > {marker}; return 99; }}; "
            f"mkdir() {{ printf called > {marker}; return 99; }}; "
            f"pip() {{ printf called > {marker}; return 99; }}; "
            'av_resolve_tool fixture-cached-tool'
        )
        for deny in (None, "1"):
            with self.subTest(no_bootstrap=deny):
                env = self.env.copy()
                if deny:
                    env["AV_NO_BOOTSTRAP"] = deny
                result = self.shell(command, env)
                self.assertEqual(result.returncode, 0)
                self.assertTrue(result.stdout.strip().endswith("/bin/fixture-cached-tool"))
                self.assertFalse((self.root / "installer-called").exists())

    def test_missing_tool_is_blocked_without_install(self):
        env = self.env | {"AV_UNAVAILABLE_TOOLS": "yamllint,ansible-lint,ansible-playbook"}
        result = self.script("validate_playbook.sh", SKILL / "test/playbooks/good-playbook.yml", env=env)
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.root / "cache").exists())

    def test_secret_values_are_redacted_in_file_directory_and_json(self):
        fixture = SKILL / "test/fixtures/secrets/planted-secrets.yml"
        planted = ["hunter2-plaintext", "AKIAIOSFODNN7EXAMPLE", "wJalrXUtnFEMI",
                   "ghp_012345", "s3cr3tpass", "BEGIN RSA PRIVATE KEY"]
        for target, fmt in [(fixture, "text"), (fixture.parent, "text"), (fixture, "json")]:
            with self.subTest(target=target.name, format=fmt):
                result = self.script("scan_secrets.sh", target, "--format", fmt)
                self.assertEqual(result.returncode, 1)
                output = result.stdout + result.stderr
                self.assertTrue(all(value not in output for value in planted), "credential content leaked")
                for shape in ["hardcoded password", "AWS access key ID", "AWS secret access key",
                              "API token", "database connection string", "private key block"]:
                    self.assertIn(shape, output)
                if fmt == "text":
                    self.assertIn("planted-secrets.yml:", output)
                    self.assertIn("[redacted]", output)
        self.assertEqual(self.script("scan_secrets.sh", SKILL / "test/fixtures/secrets/vaulted-clean.yml").returncode, 0)

    def test_molecule_stage_failures_fail_and_attempt_teardown(self):
        role = self.root / "role"
        (role / "molecule/default").mkdir(parents=True)
        bindir = self.root / "bin"
        bindir.mkdir()
        mock = bindir / "molecule"
        mock.write_text('#!/usr/bin/env bash\nprintf "%s\\n" "$1" >> "$MOCK_LOG"\n'
                        'if [ "$1" = "${MOCK_FAIL:-}" ]; then exit 7; fi\nexit 0\n', encoding="utf-8", newline="\n")
        mock.chmod(0o700)
        for failed in ["", "dependency", "prepare", "destroy"]:
            with self.subTest(failed=failed or "none"):
                log = self.root / ("stages-" + (failed or "pass"))
                env = self.env | {"PATH": str(bindir) + os.pathsep + self.env["PATH"],
                                  "MOCK_LOG": log.as_posix(), "MOCK_FAIL": failed}
                result = self.script("test_role.sh", role, "default", "--i-confirm-disposable-host", env=env)
                self.assertEqual(result.returncode, 1 if failed else 0)
                self.assertEqual(log.read_text().splitlines()[-1], "destroy")
        env = self.env | {"AV_UNAVAILABLE_TOOLS": "molecule"}
        self.assertEqual(self.script("test_role.sh", role, "default", "--i-confirm-disposable-host", env=env).returncode, 2)


def main():
    global BASH
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bash", required=True, help="Explicit path to a supported Bash executable")
    args = parser.parse_args()
    path = Path(args.bash)
    if not path.is_absolute() or not path.is_file():
        print("BLOCKED: --bash must name an existing absolute executable path")
        return 2
    BASH = str(path.resolve())
    try:
        probe = subprocess.run([BASH, "--noprofile", "--norc", "-c", "exit 0"],
                               capture_output=True, timeout=20, check=False)
    except (OSError, subprocess.TimeoutExpired):
        print("BLOCKED: Bash could not start")
        return 2
    if probe.returncode:
        print("BLOCKED: Bash startup failed")
        return 2
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(SecurityRegressions))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
