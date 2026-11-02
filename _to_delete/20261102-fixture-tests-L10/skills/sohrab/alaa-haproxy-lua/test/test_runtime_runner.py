"""Synthetic timeout/cleanup tests; no Docker invocation or network access."""
import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
from types import SimpleNamespace
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'check_runtime.py'
SPEC = importlib.util.spec_from_file_location('runtime_runner', SCRIPT)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class TimeoutCleanupTests(unittest.TestCase):
    def exercise(self, cleanup_result, unconfirmed):
        stderr = io.StringIO()
        with patch.object(RUNNER.sys, 'argv', ['check_runtime.py', '--image', 'cached-test']), \
             patch.object(RUNNER.uuid, 'uuid4', return_value=SimpleNamespace(hex='fixture')), \
             patch.object(RUNNER.subprocess, 'run', side_effect=[
                 subprocess.TimeoutExpired('docker run', 90), cleanup_result,
             ]) as run, contextlib.redirect_stderr(stderr):
            self.assertEqual(RUNNER.main(), 2)
        self.assertEqual(run.call_count, 2)
        self.assertEqual(run.call_args.args[0], ['docker', 'rm', '-f', 'alaa-lua-probe-fixture'])
        self.assertEqual(run.call_args.kwargs['timeout'], 10)
        self.assertEqual('cleanup unconfirmed' in stderr.getvalue(), unconfirmed)
        self.assertIn('could not run:', stderr.getvalue())

    def test_nonzero_cleanup_is_unconfirmed(self):
        self.exercise(SimpleNamespace(returncode=1), True)

    def test_successful_cleanup_is_not_unconfirmed(self):
        self.exercise(SimpleNamespace(returncode=0), False)

    def test_cleanup_os_error_is_unconfirmed(self):
        self.exercise(OSError('unavailable'), True)

    def test_cleanup_timeout_is_unconfirmed(self):
        self.exercise(subprocess.TimeoutExpired('docker rm', 10), True)


if __name__ == '__main__':
    unittest.main()
