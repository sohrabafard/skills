#!/usr/bin/env python3
"""Focused 3.4.6 dynamic-backend lifecycle in a cached Alpine Docker image.

Requires Docker and image-provided sh/nc/wget; no pulls or published ports.
Exit 0 observed scenarios passed, 1 assertion failed, 2 prerequisite/operation unavailable.
Temporary fixture/container only; no production/config changes or deployment proof.
"""
from __future__ import annotations

import argparse
import csv
import io
from pathlib import Path
import re
import subprocess
import tempfile
import time
import uuid

from check_examples import classify_parse_warnings, remove_owned_container, run_haproxy

CONFIG = """global
  tune.lua.bool-sample-conversion normal
  lua-load /fixtures/slow.lua
  stats socket ipv4@127.0.0.1:9999 level admin
  stats timeout 2s
  hard-stop-after 3s
  nbthread 1
defaults runtime_http
  mode http
  timeout client 8s
  timeout server 8s
  timeout connect 1s
  option httpchk GET /readyz
frontend probe from runtime_http
  bind 127.0.0.1:8080
  use_backend %[path,map(virt@routes.map,be_fallback)]
  default_backend be_fallback
backend be_fallback from runtime_http
  http-request return status 200 content-type text/plain string fallback
frontend origin from runtime_http
  bind 127.0.0.1:8081
  http-request use-service lua.slow if { path /slow }
  http-request return status 200 content-type text/plain string origin
"""

# Controlled streaming origin: a response starts before the server enters
# maintenance, then completes without aborting the existing request.
SLOW_ORIGIN = """core.register_service("slow", "http", function(applet)
  applet:set_status(200)
  applet:add_header("content-length", "8")
  applet:start_response()
  applet:send("begin")
  core.msleep(4000)
  applet:send("end")
end)
"""


def target_version(version: str) -> bool:
    return re.fullmatch(r"3\.4\.6(?:-[A-Za-z0-9][A-Za-z0-9._-]*)?", version) is not None


def wait_done(reply: str) -> None:
    assert reply.strip() == "Done.", "removal wait did not succeed: " + reply.strip()


def validate_parser_result(result: subprocess.CompletedProcess[str]) -> None:
    output = result.stdout + result.stderr
    assert result.returncode == 0, "fixture parser rejected config: " + output.strip()[:400]
    warnings = classify_parse_warnings("runtime fixture", output)
    assert not warnings, "unresolved fixture parser warning: " + str(warnings[0]) if warnings else ""


def active_server(output: str) -> bool:
    rows = csv.DictReader(io.StringIO(output.lstrip("# ")))
    return any(row.get("pxname") == "be_live" and row.get("svname") == "app"
               and int(row.get("scur") or "0") > 0 for row in rows)


def run(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, timeout=30)
    if result.returncode:
        raise RuntimeError("{} exited {}: {}".format(command[0], result.returncode,
                                                    (result.stderr or result.stdout).strip()[:400]))
    return result.stdout


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docker-image", required=True, help="cached HAProxy 3.4.6 Alpine image")
    args = parser.parse_args()
    name = "haproxy-skill-runtime-" + uuid.uuid4().hex[:12]
    creation_attempted = False
    stage = "prerequisites"
    active = None
    code = 0
    with tempfile.TemporaryDirectory(prefix="haproxy-runtime-") as scratch:
        cfg = Path(scratch) / "haproxy.cfg"
        cfg.write_text(CONFIG, encoding="utf-8")
        (Path(scratch) / "slow.lua").write_text(SLOW_ORIGIN, encoding="utf-8")
        mount = "type=bind,source={},target=/fixtures,readonly".format(Path(scratch).resolve())
        try:
            binary = "docker://" + args.docker_image
            result = run_haproxy(binary, ["-vq"])
            version = result.stdout.strip()
            if result.returncode or not target_version(version):
                raise RuntimeError("expected 3.4.6 binary, observed " + version)
            build = run_haproxy(binary, ["-vv"])
            if build.returncode or "+LUA" not in build.stdout:
                raise RuntimeError("controlled streaming origin requires +LUA")
            stage = "create isolated container"
            creation_attempted = True
            run(["docker", "run", "--pull", "never", "--rm", "-d", "--name", name,
                 "--network", "none", "--read-only", "--cpus", "1", "--memory", "256m",
                 "--mount", mount, "--entrypoint", "haproxy", args.docker_image,
                 "-W", "-db", "-f", "/fixtures/haproxy.cfg"])

            def cli(command: str) -> str:
                # Commands are fixed fixture strings; shell variables/escaping are not accepted.
                return run(["docker", "exec", name, "sh", "-c",
                            "printf '%s\\n' '" + command + "' | nc -w 6 127.0.0.1 9999"])

            def request() -> str:
                result = subprocess.run(["docker", "exec", name, "wget", "-q", "-O", "-",
                                         "http://127.0.0.1:8080/live"],
                                        capture_output=True, text=True, timeout=10)
                if result.returncode == 1 and "503 Service Unavailable" in result.stderr:
                    return "pending-health-503"
                if result.returncode:
                    raise RuntimeError("HTTP probe failed: " + result.stderr.strip()[:400])
                return result.stdout

            def await_body(wanted: str) -> None:
                deadline = time.monotonic() + 8
                while time.monotonic() < deadline:
                    if request() == wanted:
                        return
                    time.sleep(0.2)
                raise AssertionError("routed response did not become " + wanted)

            # Fail an unavailable process immediately, rather than disguising operation errors.
            stage = "fixture parser and warning gate"
            validate_parser_result(subprocess.run(
                ["docker", "exec", name, "haproxy", "-c", "-f", "/fixtures/haproxy.cfg"],
                capture_output=True, text=True, timeout=30))
            stage = "initial fallback"
            await_body("fallback")

            def create(label: str) -> None:
                nonlocal stage
                stage = label + " registration/unpublished fallback"
                assert "registered" in cli("add backend be_live from runtime_http mode http")
                assert "registered" in cli("add server be_live/app 127.0.0.1:8081 check")
                cli("enable server be_live/app")
                cli("enable health be_live/app")
                cli("add map virt@routes.map /live be_live")
                cli("add map virt@routes.map /slow be_live")
                await_body("fallback")  # unpublished backend cannot receive traffic
                stage = label + " published positive origin"
                cli("publish backend be_live")
                await_body("origin")

            create("first")
            stage = "active stream established"
            active = subprocess.Popen(["docker", "exec", name, "wget", "-q", "-O", "-",
                                       "http://127.0.0.1:8080/slow"],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            deadline = time.monotonic() + 3
            while not active_server(cli("show stat")):
                assert active.poll() is None, "stream ended before active state was observed"
                assert time.monotonic() < deadline, "server active stream not observed"
                time.sleep(0.1)
            stage = "unpublished admission fallback with existing stream"
            cli("unpublish backend be_live")
            await_body("fallback")
            cli("set server be_live/app state maint")
            stage = "active stream prevents deletion"
            wait_reply = cli("wait 100ms srv-removable be_live/app")
            assert "Wait delay expired." in wait_reply, "unexpected removal wait reply: " + repr(wait_reply)
            stage = "active stream completes under maintenance"
            stdout, stderr = active.communicate(timeout=10)
            assert active.returncode == 0 and stdout == "beginend", "stream truncated: " + stderr.strip()
            active = None
            stage = "drained server removal"
            wait_done(cli("wait 3s srv-removable be_live/app"))
            cli("del server be_live/app")
            wait_done(cli("wait 3s be-removable be_live"))
            cli("del backend be_live")
            assert "be_live" not in cli("show backend")
            cli("del map virt@routes.map /live")
            cli("del map virt@routes.map /slow")
            stage = "static backend deletion refusal"
            # A static config reference is retained, proving refusal isn't silently treated as success.
            cli("unpublish backend be_fallback")
            assert cli("del backend be_fallback").strip()
            assert "be_fallback" in cli("show backend")
            cli("publish backend be_fallback")
            create("before reload")
            stage = "reload loses dynamic membership"
            run(["docker", "kill", "--signal", "USR2", name])
            await_body("fallback")
            assert "be_live" not in cli("show backend")
            create("reconstruction")
            print("PASS: unpublished fallback, publish/route, active-stream drain/delete, deletion refusal, reload loss/reconstruction")
        except AssertionError as exc:
            print("FAIL [{}]: {}".format(stage, str(exc) or "lifecycle assertion"))
            code = 1
        except (OSError, subprocess.SubprocessError, RuntimeError) as exc:
            print("could not run [{}]: {}".format(stage, exc))
            code = 2
        finally:
            if active is not None:
                try:
                    active.kill()
                    active.communicate(timeout=10)
                except (OSError, subprocess.SubprocessError) as exc:
                    print("could not terminate isolated probe client: " + str(exc))
                    code = 2
            if creation_attempted:
                try:
                    remove_owned_container(name)
                except (OSError, subprocess.SubprocessError, RuntimeError) as exc:
                    print("could not remove isolated container {}: {}".format(name, exc))
                    code = 2
    return code


if __name__ == "__main__":
    raise SystemExit(main())
