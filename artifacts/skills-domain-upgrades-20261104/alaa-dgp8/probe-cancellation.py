"""Send SIGTERM to an admitted fixture once its actual server is ready."""

from pathlib import Path
import re
import subprocess
import sys

runner, image = sys.argv[1:]
with subprocess.Popen(
    [sys.executable, "-B", str(Path(runner)), "--image", image],
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
) as process:
    name = None
    sent = False
    cleanup = False
    for line in process.stdout:
        print(line, end="", flush=True)
        if line.startswith("fixture container: "):
            name = line.removeprefix("fixture container: ").strip()
            if not re.fullmatch(r"alaa-dgp8-merge-[0-9a-f]{32}", name):
                raise RuntimeError(f"unexpected fixture identity {name!r}")
        if line == "server version: '24.8.14.39'\n":
            if name is None:
                raise RuntimeError("fixture identity missing before readiness")
            process.terminate()
            sent = True
            print(f"probe sent SIGTERM to fixture runner for {name}", flush=True)
        if name and line == f"fixture cleanup {name}: ''\n":
            cleanup = True

    status = process.wait(timeout=25)
    print(f"cancelled runner exit={status}", flush=True)
    if not sent or not cleanup or status != 143:
        raise RuntimeError("SIGTERM did not produce the required cancellation and cleanup")
    observed = subprocess.run(
        ["docker", "ps", "-aq", "--filter", f"name=^/{name}$",
         "--filter", f"label=alaa.fixture.aggregate-merge={name}"],
        check=True, capture_output=True, text=True, timeout=5,
    )
    if observed.stdout.strip():
        raise RuntimeError("cancelled fixture still exists")
    print(f"probe independently observed no remaining {name} container")
