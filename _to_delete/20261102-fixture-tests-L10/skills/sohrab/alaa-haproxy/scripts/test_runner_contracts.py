#!/usr/bin/env python3
"""Synthetic runner regressions; no Docker, network, binary or scratch writes."""
from contextlib import redirect_stdout
import io
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

import check_examples as examples
import check_runtime_3_4 as runtime
import check_http_error_bytes as http_bytes


def result(code=0, stdout="", stderr=""):
    return subprocess.CompletedProcess([], code, stdout, stderr)


class RunnerContracts(unittest.TestCase):
    def test_only_constructed_fixture_environment_is_forwarded(self):
        with patch.object(examples.subprocess, "run", side_effect=[result(), result()]) as run:
            examples.run_haproxy("docker://synthetic-image", ["-v"],
                                 env={"HAPROXY_UNRELATED_SENTINEL": "synthetic-sensitive-value",
                                      "HAPROXY_CERT_DIR": "inherited-sensitive-value"},
                                 fixture_env={"HAPROXY_CERT_DIR": "/synthetic-fixture"})
        command = run.call_args_list[0].args[0]
        self.assertIn("HAPROXY_CERT_DIR=/synthetic-fixture", command)
        self.assertNotIn("synthetic-sensitive-value", " ".join(command))
        self.assertNotIn("inherited-sensitive-value", " ".join(command))
        self.assertIn("--pull", command)
        self.assertIn("never", command)

    def test_parser_timeout_removes_the_allocated_name(self):
        with patch.object(examples.subprocess, "run", side_effect=[
                subprocess.TimeoutExpired("synthetic", 120), result()]) as run:
            with self.assertRaises(subprocess.TimeoutExpired):
                examples.run_haproxy("docker://synthetic-image", ["-v"])
        launch = run.call_args_list[0].args[0]
        name = launch[launch.index("--name") + 1]
        self.assertEqual(run.call_args_list[1].args[0], ["docker", "rm", "-f", name])

    def test_parser_failed_creation_still_removes_owned_name(self):
        with patch.object(examples.subprocess, "run", side_effect=[result(1), result()]) as run:
            self.assertEqual(examples.run_haproxy("docker://synthetic-image", ["-v"]).returncode, 1)
        self.assertEqual(run.call_count, 2)

    def test_cleanup_failure_is_not_silently_accepted(self):
        with patch.object(examples.subprocess, "run", return_value=result(1, stderr="synthetic denied")):
            with self.assertRaises(OSError):
                examples.remove_owned_container("synthetic-owned")

    def test_already_removed_container_is_accepted(self):
        with patch.object(examples.subprocess, "run", return_value=result(1, stderr="No such container: synthetic-owned")):
            examples.remove_owned_container("synthetic-owned")

    def test_cleanup_timeout_propagates(self):
        with patch.object(examples.subprocess, "run", side_effect=subprocess.TimeoutExpired("rm", 30)):
            with self.assertRaises(subprocess.TimeoutExpired):
                examples.remove_owned_container("synthetic-owned")

    def test_runtime_failed_creation_runs_cleanup_and_reports_stage(self):
        with patch.object(runtime.tempfile, "TemporaryDirectory") as directory, \
             patch.object(Path, "write_text"), \
             patch.object(runtime, "run_haproxy", side_effect=[result(stdout="3.4.6"), result(stdout="+LUA")]), \
             patch.object(runtime, "run", side_effect=subprocess.TimeoutExpired("synthetic-create", 30)), \
             patch.object(runtime, "remove_owned_container") as remove, \
             patch("sys.argv", ["runner", "--docker-image", "synthetic-image"]), redirect_stdout(io.StringIO()) as output:
            directory.return_value.__enter__.return_value = "synthetic-scratch"
            self.assertEqual(runtime.main(), 2)
        self.assertEqual(remove.call_count, 1)
        self.assertIn("create isolated container", output.getvalue())

    def test_exact_patch_boundary(self):
        for value, wanted in [("3.4.6", True), ("3.4.6-56332c5", True),
                              ("3.4.60", False), ("3.4.6junk", False),
                              ("3.4.7", False), ("3.4.6-", False)]:
            with self.subTest(value=value):
                self.assertEqual(runtime.target_version(value), wanted)

    def test_wait_reply_requires_done(self):
        runtime.wait_done("Done.\n")
        for reply in ["", "Wait delay expired. active streams", "Failed. not in maintenance", "Interrupted."]:
            with self.subTest(reply=reply), self.assertRaises(AssertionError):
                runtime.wait_done(reply)

    def test_runtime_parser_warnings_block_even_on_success(self):
        self.assertLess(runtime.CONFIG.index("tune.lua.bool-sample-conversion normal"),
                        runtime.CONFIG.index("lua-load"))
        runtime.validate_parser_result(result(stdout="Configuration file is valid\n"))
        for parsed in [result(stderr="[WARNING] synthetic warning\n"),
                       result(stdout="[WARNING] synthetic warning\n"),
                       result(1, stderr="[ALERT] synthetic rejection\n")]:
            with self.subTest(parsed=parsed), self.assertRaises(AssertionError):
                runtime.validate_parser_result(parsed)

    def test_active_stream_counter_selects_the_real_server(self):
        header = "# pxname,svname,scur\n"
        self.assertTrue(runtime.active_server(header + "be_live,app,1\n"))
        self.assertFalse(runtime.active_server(header + "be_live,app,0\nbe_live,BACKEND,1\nother,app,2\n"))

    def test_absurd_decimal_length_is_a_finding(self):
        self.assertTrue(http_bytes.findings(b"HTTP/1.1 503 Synthetic\nContent-Length: " + b"9" * 5000 + b"\n\nx"))
        self.assertFalse(http_bytes.findings(b"HTTP/1.1 503 Synthetic\nContent-Length: " + b"0" * 5000 + b"1\n\nx"))


if __name__ == "__main__":
    unittest.main()
