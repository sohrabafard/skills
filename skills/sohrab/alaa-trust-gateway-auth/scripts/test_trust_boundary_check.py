"""CLI regressions for the sanitize check's frontend-to-backend delete coverage."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CHECKER = Path(__file__).with_name("trust_boundary_check.py")

DELETING_FRONTEND = """frontend fe_http
  http-request del-header X-Forwarded-For
  use_backend be_app if { path_beg /app }
"""
PLAIN_FRONTEND = """frontend fe_other
  default_backend be_app
"""
BACKEND_SET = """backend be_app
  http-request set-header X-Forwarded-For %[var(txn.client_ip)]
  server app 10.0.0.1:80
"""


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), *args], capture_output=True, text=True, check=False
    )


def sanitize(config: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "haproxy.cfg"
        path.write_text(config, encoding="utf-8")
        return run("--gateway-config", str(path))


class FrontendDeleteCoverage(unittest.TestCase):
    def test_frontend_delete_covers_backend_set(self):
        # Defends against: the per-section model reporting a backend set as
        # unsanitized although every frontend reaching it deletes the header.
        result = sanitize(DELETING_FRONTEND + BACKEND_SET)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_backend_set_without_any_delete_fails(self):
        # Defends against: X-Forwarded-For exempted from the sanitize check, so
        # a forgeable client copy passes unreported.
        result = sanitize(PLAIN_FRONTEND + BACKEND_SET)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("x-forwarded-for is injected", result.stdout)
        self.assertIn("never deleted", result.stdout)

    def test_backend_reached_by_a_frontend_without_the_delete_fails(self):
        # Defends against: one deleting frontend standing in for every frontend
        # that reaches the backend.
        result = sanitize(DELETING_FRONTEND + PLAIN_FRONTEND + BACKEND_SET)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("x-forwarded-for is injected in section 'backend be_app'", result.stdout)
        self.assertIn("without the delete: 'frontend fe_other'", result.stdout)


class ForwardedForReads(unittest.TestCase):
    def test_source_read_of_forwarded_for_is_not_a_trusted_header_finding(self):
        # Defends against: removing X-Forwarded-For from the sanitize exemption
        # also turning a service's XFF read into a trusted-header finding.
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "Proxy.php"
            source.write_text("<?php $ip = $request->header('X-Forwarded-For');\n", encoding="utf-8")
            allowlist = Path(tmp) / "allowlist.txt"
            allowlist.write_text("X-User-Id\n", encoding="utf-8")
            result = run("--source-root", str(source), "--allowlist", str(allowlist))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
