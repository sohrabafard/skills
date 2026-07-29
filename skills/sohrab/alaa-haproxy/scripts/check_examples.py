#!/usr/bin/env python3
"""Check every HAProxy example shipped in this skill.

Two phases.

STRUCTURE  Pure Python. Every example must state its own contract in its header
           (charter, minimum branch, preconditions, variables, failure mode), must
           not carry a keyword in a section that keyword does not belong to, must
           not leave a retry without a redispatch, must parameterise its addresses,
           and must not ship a Kubernetes bundle whose metrics endpoint cannot be
           reached by the Service that targets it.

PARSE      `haproxy -c -f` on a real binary, for every example whose declared
           minimum branch that binary satisfies. This phase builds a throwaway
           certificate and map tree in the system temporary directory and sets the
           example variables to point at it, because `-c` stats every certificate
           and map path the config names.

Pure Python 3 standard library plus, for the parse phase, `haproxy` and `openssl`
on PATH. Runs on Windows, Linux and macOS.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_CANNOT_RUN = 2

# The label must open a header block. A qualifier may follow it, so
# "# Preconditions, all three of which fail silently:" satisfies the same rule as
# "# Preconditions:".
REQUIRED_HEADERS = [
    ("HP-EX-001", "Charter", re.compile(r"^#\s*Charter\b", re.M)),
    ("HP-EX-002", "Minimum branch", re.compile(r"^#\s*Minimum branch\b", re.M)),
    ("HP-EX-003", "Preconditions", re.compile(r"^#\s*Preconditions\b", re.M)),
    ("HP-EX-004", "Variables", re.compile(r"^#\s*Variables\b", re.M)),
    ("HP-EX-005", "Failure mode", re.compile(r"^#\s*Failure mode\b", re.M)),
]

RULES = {
    "HP-EX-001": "the file states its charter in its header",
    "HP-EX-002": "the file states the minimum HAProxy branch it needs",
    "HP-EX-003": "the file states its preconditions",
    "HP-EX-004": "the file lists the variables it reads",
    "HP-EX-005": "the file states its failure mode",
    "HP-EX-006": "`idle-ping` appears only as a bind or server argument, never as a proxy-level line",
    "HP-EX-007": "`balance hash` carries its mandatory sample expression",
    "HP-EX-008": "a config with a `peers` section sets `localpeer` and puts `ssl` on the peers bind",
    "HP-EX-009": "a section that sets `retries` also sets `option redispatch`",
    "HP-EX-010": "the `master-worker` global directive is not used (deprecated from 3.3; use -W or -Ws)",
    "HP-EX-011": "a `server` address is supplied by a variable, not hardcoded",
    "HP-EX-012": "no metrics listener binds loopback while a Service or ServiceMonitor in the same bundle targets it",
    "HP-EX-013": "every haproxy image tag matches the branch recorded in references/10-version-and-branch.md",
    "HP-EX-014": "no end-of-life kubectl or Kubernetes version is pinned in an example",
}

# Optional header. `# Requires-build: QUIC !QUIC_OPENSSL_COMPAT` names the feature-list
# tokens the running build must have, and must not have, for this example to be parseable.

# Kubernetes minor versions past end of life as of the read date recorded in
# references/SOURCES.md. Re-derive from https://kubernetes.io/releases/patch-releases/.
EOL_KUBERNETES = {
    "1.32": "2026-02-28", "1.31": "2025-10-28", "1.30": "2025-06-28",
    "1.29": "2025-02-28", "1.28": "2024-10-28", "1.27": "2024-06-28",
}

SECTION_KEYWORDS = {
    "global", "defaults", "frontend", "backend", "listen", "peers", "resolvers",
    "cache", "ring", "log-forward", "mailers", "userlist", "http-errors",
    "crt-store", "traces", "fcgi-app", "acme", "healthcheck", "program",
}

BRANCH_REFERENCE = Path("references") / "10-version-and-branch.md"


class Finding:
    def __init__(self, path: str, line: int, rule: str, detail: str) -> None:
        self.path = path
        self.line = line
        self.rule = rule
        self.detail = detail

    def __str__(self) -> str:
        return "{}:{}: {}: {}".format(self.path, self.line, self.rule, self.detail)


def skill_root(start: Path) -> Path | None:
    """Ascend from `start` until a directory containing SKILL.md is found."""
    current = start.resolve()
    for _ in range(8):
        if (current / "SKILL.md").is_file():
            return current
        if current.parent == current:
            break
        current = current.parent
    return None


def strip_comment(line: str) -> str:
    out = []
    prev = ""
    for index, char in enumerate(line):
        if char == "#" and prev != "\\" and (index == 0 or prev.isspace()):
            break
        out.append(char)
        prev = char
    return "".join(out)


def read_lines(path: Path) -> list[str]:
    """Universal newlines, then strip any stray carriage return.

    A CRLF checkout otherwise leaves \\r on the last field of every parsed line,
    so every comparison fails while the rendered bytes look identical.
    """
    with path.open("r", encoding="utf-8", errors="replace", newline=None) as handle:
        return [line.rstrip("\r\n") for line in handle]


def parse_branch(text: str) -> tuple[int, int] | None:
    match = re.search(r"(\d+)\.(\d+)", text)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def declared_build_features(lines: list[str]) -> list[str]:
    """Tokens from a `# Requires-build:` header. A leading `!` means must be absent.

    These are the names HAProxy prints in the `Feature list` of `haproxy -vv`, so this
    header is gate G2 of references/80-gate-register.md written into the file.
    """
    for line in lines[:60]:
        if re.match(r"^#\s*Requires-build\b", line):
            body = line.split(":", 1)[1] if ":" in line else ""
            return body.split()
    return []


def binary_features(haproxy: str) -> set[str] | None:
    """The `+NAME` tokens from the binary's feature list."""
    try:
        result = subprocess.run([haproxy, "-vv"], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    output = result.stdout + result.stderr
    match = re.search(r"^Feature list\s*:\s*(.+)$", output, re.M)
    if not match:
        return None
    return {token[1:] for token in match.group(1).split() if token.startswith("+")}


def declared_branch(lines: list[str]) -> tuple[int, int] | None:
    for line in lines[:60]:
        if re.match(r"^#\s*Minimum branch\b", line):
            return parse_branch(line.split(":", 1)[1] if ":" in line else line)
    return None


def check_structure(path: Path, display: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = read_lines(path)
    joined = "\n".join(lines)

    for rule, label, pattern in REQUIRED_HEADERS:
        if not pattern.search(joined):
            findings.append(Finding(display, 1, rule,
                                    "header does not state `{}`".format(label)))

    if declared_branch(lines) is None and re.search(r"^#\s*Minimum branch\b", joined, re.M):
        findings.append(Finding(display, 1, "HP-EX-002",
                                "`# Minimum branch:` does not name a branch number"))

    section = None
    section_line = 0
    section_has_retries = 0
    section_has_redispatch = False
    peers_sections: list[int] = []
    peers_bind_ssl = False
    has_localpeer = False

    def close_section() -> None:
        nonlocal section_has_retries, section_has_redispatch
        if section_has_retries and not section_has_redispatch:
            findings.append(Finding(
                display, section_has_retries, "HP-EX-009",
                "`retries` with no `option redispatch` in section `{}` starting at line {}: "
                "every retry goes to the same failed server".format(section, section_line)))
        section_has_retries = 0
        section_has_redispatch = False

    for number, raw in enumerate(lines, start=1):
        text = strip_comment(raw)
        stripped = text.strip()
        if not stripped or stripped.startswith("."):
            continue
        tokens = stripped.split()
        unindented = not raw[:1].isspace()

        if unindented and tokens[0] in SECTION_KEYWORDS:
            close_section()
            section = tokens[0]
            section_line = number
            if section == "peers":
                peers_sections.append(number)
            continue

        if section is None:
            continue

        first = tokens[0]

        if first == "idle-ping":
            findings.append(Finding(
                display, number, "HP-EX-006",
                "`idle-ping` is a bind and a server argument, never a proxy-level directive. "
                "HAProxy reports `unknown keyword 'idle-ping'` and refuses to start."))

        if first == "balance" and len(tokens) >= 2 and tokens[1] == "hash" and len(tokens) == 2:
            findings.append(Finding(
                display, number, "HP-EX-007",
                "`balance hash` requires a sample expression naming what is hashed"))

        if first == "master-worker":
            findings.append(Finding(
                display, number, "HP-EX-010",
                "the `master-worker` global directive is deprecated from 3.3; start with "
                "`-W` or `-Ws` on the command line instead"))

        if first == "retries":
            section_has_retries = number
        if first == "option" and len(tokens) >= 2 and tokens[1] == "redispatch":
            section_has_redispatch = True
        if first == "localpeer":
            has_localpeer = True

        if section == "peers" and first == "bind" and "ssl" in tokens:
            peers_bind_ssl = True

        if first == "server" and section in {"backend", "listen"}:
            # tokens: server <name> <address> [args...]
            if len(tokens) >= 3 and "${" not in tokens[2]:
                findings.append(Finding(
                    display, number, "HP-EX-011",
                    "`server {}` hardcodes the address `{}`. Use a variable: "
                    "\"${{NAME-default}}\".".format(tokens[1], tokens[2])))

    close_section()

    if peers_sections:
        if not has_localpeer:
            findings.append(Finding(
                display, peers_sections[0], "HP-EX-008",
                "a `peers` section with no `localpeer` in `global`: with a hostname that "
                "matches no peer entry the section never activates, the config still passes "
                "`haproxy -c -f`, and the limit silently works per node in isolation"))
        if not peers_bind_ssl:
            findings.append(Finding(
                display, peers_sections[0], "HP-EX-008",
                "the peers `bind` carries no `ssl`: anything that reaches the port can write "
                "stick-table entries"))

    return findings


def check_bundle_metrics(directory: Path, display_root: Path) -> list[Finding]:
    """A metrics listener on loopback that a Service or ServiceMonitor targets."""
    findings: list[Finding] = []
    if not directory.is_dir():
        return findings

    loopback_ports: list[tuple[str, int, str]] = []
    service_ports: set[str] = set()
    monitor_present = False

    for path in sorted(directory.rglob("*.yaml")):
        display = str(path.relative_to(display_root))
        lines = read_lines(path)
        for number, raw in enumerate(lines, start=1):
            text = strip_comment(raw).strip()
            if not text:
                continue
            match = re.match(r"bind\s+(?:127\.0\.0\.1|localhost|\[::1\]):(\d+)", text)
            if match:
                loopback_ports.append((display, number, match.group(1)))
            match = re.match(r"-?\s*targetPort:\s*(\S+)", text)
            if match:
                service_ports.add(match.group(1).strip('"'))
            match = re.match(r"-?\s*port:\s*(\d+)", text)
            if match:
                service_ports.add(match.group(1))
            if "kind: ServiceMonitor" in text:
                monitor_present = True

    for display, number, port in loopback_ports:
        if port in service_ports or monitor_present:
            findings.append(Finding(
                display, number, "HP-EX-012",
                "binds loopback on port {} while a Service or ServiceMonitor in the same "
                "bundle targets it. A loopback bind is unreachable through the pod IP, so "
                "the target is down from the first rollout with nothing in HAProxy's "
                "logs.".format(port)))
    return findings


def current_lts(root: Path) -> str | None:
    """Read the branch marked LTS and current from the version reference."""
    reference = root / BRANCH_REFERENCE
    if not reference.is_file():
        return None
    for line in read_lines(reference):
        if line.startswith("| **") and "**LTS**" in line:
            match = re.search(r"\*\*(\d+\.\d+)\*\*", line)
            if match:
                return match.group(1)
    return None


def check_version_pins(root: Path) -> tuple[list[Finding], str | None]:
    findings: list[Finding] = []
    lts = current_lts(root)
    if lts is None:
        return findings, "cannot read the current LTS branch from {}".format(BRANCH_REFERENCE)

    examples = root / "examples"
    for path in sorted(examples.rglob("*")):
        if not path.is_file() or path.suffix not in {".yaml", ".yml", ".cfg"}:
            continue
        display = str(path.relative_to(root))
        for number, raw in enumerate(read_lines(path), start=1):
            text = raw.strip()
            for match in re.finditer(r"haproxy:(\d+\.\d+)(?:\.\d+)?", text):
                if match.group(1) != lts:
                    findings.append(Finding(
                        display, number, "HP-EX-013",
                        "image pin `{}` is not on the current LTS branch {} recorded in "
                        "{}".format(match.group(0), lts, BRANCH_REFERENCE)))
            for match in re.finditer(r"kubectl[:@]?v?(\d+\.\d+)", text):
                if match.group(1) in EOL_KUBERNETES:
                    findings.append(Finding(
                        display, number, "HP-EX-014",
                        "Kubernetes {} reached end of life {}".format(
                            match.group(1), EOL_KUBERNETES[match.group(1)])))
            for match in re.finditer(r"version:\s*v?(\d+\.\d+)\.\d+", text):
                if match.group(1) in EOL_KUBERNETES:
                    findings.append(Finding(
                        display, number, "HP-EX-014",
                        "Kubernetes {} reached end of life {}".format(
                            match.group(1), EOL_KUBERNETES[match.group(1)])))
    return findings, None


def binary_branch(haproxy: str) -> tuple[int, int] | None:
    try:
        result = subprocess.run([haproxy, "-v"], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    return parse_branch(result.stdout + result.stderr)


def build_fixture_tree(root: Path) -> tuple[dict[str, str], str] | tuple[None, str]:
    """Create certificates and maps outside the repository, and the environment for them."""
    openssl = shutil.which("openssl")
    if openssl is None:
        return None, "openssl is not on PATH; the parse phase needs it to build test certificates"

    scratch = tempfile.mkdtemp(prefix="haproxy-examples-")
    certs = Path(scratch) / "certs"
    ca = Path(scratch) / "ca"
    client = Path(scratch) / "client"
    maps = Path(scratch) / "maps"
    for directory in (certs, ca, client, maps):
        directory.mkdir(parents=True, exist_ok=True)

    key = Path(scratch) / "k.pem"
    crt = Path(scratch) / "c.pem"
    result = subprocess.run(
        [openssl, "req", "-x509", "-newkey", "rsa:2048", "-keyout", str(key), "-out", str(crt),
         "-days", "2", "-nodes", "-subj", "/CN=haproxy-example-fixture"],
        capture_output=True, text=True, timeout=180)
    if result.returncode != 0 or not crt.is_file():
        shutil.rmtree(scratch, ignore_errors=True)
        return None, "openssl could not generate a test certificate: {}".format(result.stderr.strip())

    combined = key.read_text() + crt.read_text()
    for name in ("edge.pem", "peers.pem", "example.pem", "public.pem"):
        (certs / name).write_text(combined)
    for name in ("clients-ca.pem", "origin-ca.pem", "internal-ca.pem", "backend-ca.pem",
                 "peers-ca.pem"):
        (ca / name).write_text(crt.read_text())
    (client / "backend-client.pem").write_text(combined)
    (maps / "canary-paths.map").write_text("/beta 1\n")
    (maps / "allowed-hosts.map").write_text("app.example 1\n")

    environment = {
        "HAPROXY_CERT_DIR": str(certs),
        "HAPROXY_CA_DIR": str(ca),
        "HAPROXY_CLIENT_DIR": str(client),
        "HAPROXY_MAP_DIR": str(maps),
        # Policy values that examples/haproxy/20 refuses to start without, by design.
        "HAPROXY_ASSET_PREFIX": "/assets",
        "HAPROXY_HASHED_ASSET_CACHE_CONTROL": "public, max-age=31536000, immutable",
        "HAPROXY_HTML_CACHE_CONTROL": "no-cache",
        "HAPROXY_COMPRESS_TYPES": "text/html text/css application/javascript",
    }
    return environment, scratch


def run_parse_phase(root: Path, haproxy: str, allow_skips: bool) -> tuple[list[Finding], list[str], list[str], str | None]:
    findings: list[Finding] = []
    skipped: list[str] = []
    notes: list[str] = []

    branch = binary_branch(haproxy)
    if branch is None:
        return findings, skipped, notes, "cannot determine the branch of `{}`".format(haproxy)

    features = binary_features(haproxy)
    if features is None:
        return findings, skipped, notes, "cannot read the feature list of `{}`".format(haproxy)

    environment, scratch = build_fixture_tree(root)
    if environment is None:
        return findings, skipped, notes, scratch  # scratch carries the error message

    try:
        env = dict(os.environ)
        env.update(environment)
        directory = root / "examples" / "haproxy"
        for path in sorted(directory.glob("*.cfg")):
            display = str(path.relative_to(root))
            required = declared_branch(read_lines(path))
            if required is None:
                findings.append(Finding(display, 1, "HP-EX-002",
                                        "cannot parse: no declared minimum branch"))
                continue
            if required > branch:
                skipped.append("{}: needs branch {}.{}, binary is {}.{}".format(
                    display, required[0], required[1], branch[0], branch[1]))
                continue
            missing = []
            for token in declared_build_features(read_lines(path)):
                if token.startswith("!"):
                    if token[1:] in features:
                        missing.append("build has {} and this file needs it absent".format(token[1:]))
                elif token not in features:
                    missing.append("build lacks {}".format(token))
            if missing:
                skipped.append("{}: {}".format(display, "; ".join(missing)))
                continue
            # -dr: a placeholder backend hostname must not read as a config defect.
            result = subprocess.run([haproxy, "-dr", "-c", "-f", str(path)],
                                    capture_output=True, text=True, timeout=120, env=env)
            output = (result.stdout + result.stderr)
            if result.returncode != 0:
                detail = " | ".join(
                    line.strip() for line in output.splitlines() if "[ALERT]" in line)[:400]
                findings.append(Finding(
                    display, 1, "HP-EX-PARSE",
                    detail or "haproxy -c -f exited {} with no alert".format(result.returncode)))
            else:
                for line in output.splitlines():
                    if "[WARNING]" in line:
                        notes.append("{}: {}".format(display, line.split("config : ", 1)[-1].strip()))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    if skipped and not allow_skips:
        return findings, skipped, notes, (
            "{} example(s) could not be parsed: the binary's branch or build features do not "
            "meet what they declare. Pass --allow-skips to accept this, or use a binary that "
            "does.".format(len(skipped)))
    return findings, skipped, notes, None


BAD_FIXTURE = """\
# no-contract.cfg
# This fixture deliberately states nothing about itself.
global
  master-worker

defaults api
  mode http
  retries 3

peers cluster
  bind :1024
  server a
  server b 10.0.0.2:1024

frontend fe from api
  bind :8080
  idle-ping 30s
  default_backend be

backend be from api
  balance hash
  server s1 10.0.0.1:80
"""

GOOD_FIXTURE = """\
# contract.cfg
# Charter: a minimal example that states its own contract.
# Minimum branch: 3.2.
# Preconditions: none beyond a 3.2 or later binary.
# Variables: FIXTURE_PORT=8080, FIXTURE_APP=10.0.0.1:80
# Failure mode: none; this file exists to be checked, not to be deployed.
global
  log /dev/log local0 info

defaults api
  mode http
  timeout connect 5s
  timeout client 30s
  timeout server 30s
  retries 3
  option redispatch

frontend fe from api
  bind ":${FIXTURE_PORT-8080}"
  default_backend be

backend be from api
  balance roundrobin
  server s1 "${FIXTURE_APP-10.0.0.1:80}" check
"""


def self_test(script_dir: Path) -> int:
    fixtures = script_dir / "fixtures" / "examples"
    failures: list[str] = []

    if not fixtures.is_dir():
        print("self-test: fixture directory missing: {}".format(fixtures), file=sys.stderr)
        return EXIT_CANNOT_RUN

    expectations = {
        "contract.cfg": set(),
        "no-contract.cfg": {"HP-EX-001", "HP-EX-002", "HP-EX-003", "HP-EX-004", "HP-EX-005",
                            "HP-EX-006", "HP-EX-007", "HP-EX-008", "HP-EX-009", "HP-EX-010",
                            "HP-EX-011"},
    }
    for name, want in expectations.items():
        path = fixtures / name
        if not path.is_file():
            print("self-test: fixture missing: {}".format(path), file=sys.stderr)
            return EXIT_CANNOT_RUN
        got = {finding.rule for finding in check_structure(path, name)}
        if got != want:
            failures.append("{}: expected {} got {}".format(name, sorted(want), sorted(got)))
        else:
            print("self-test: {} -> {}".format(name, sorted(got) or "clean"))

    # Bundle rule, on fixtures rather than on the shipped bundle.
    bundle = fixtures / "bundle"
    if not bundle.is_dir():
        print("self-test: fixture bundle missing: {}".format(bundle), file=sys.stderr)
        return EXIT_CANNOT_RUN
    got = {finding.rule for finding in check_bundle_metrics(bundle, fixtures)}
    if got != {"HP-EX-012"}:
        failures.append("bundle: expected ['HP-EX-012'] got {}".format(sorted(got)))
    else:
        print("self-test: bundle -> ['HP-EX-012']")

    # Could-not-run path: a binary that does not exist.
    if binary_branch(str(script_dir / "not-a-binary")) is not None:
        failures.append("binary_branch accepted a nonexistent binary")
    else:
        print("self-test: nonexistent binary -> could not run")

    # CRLF resilience on the clean fixture.
    scratch = tempfile.mkdtemp(prefix="haproxy-examples-crlf-")
    try:
        crlf = Path(scratch) / "contract.cfg"
        crlf.write_bytes(GOOD_FIXTURE.replace("\n", "\r\n").encode("utf-8"))
        got = {finding.rule for finding in check_structure(crlf, "crlf")}
        if got:
            failures.append("CRLF copy of the clean fixture produced {}".format(sorted(got)))
        else:
            print("self-test: CRLF copy of contract.cfg -> clean")
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    if failures:
        for line in failures:
            print("self-test FAILED: {}".format(line), file=sys.stderr)
        return EXIT_FINDINGS
    print("self-test: all checks passed")
    return EXIT_CLEAN


def build_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(
        prog="check_examples.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__,
        epilog=(
            "Rules\n"
            + "".join("  {}  {}\n".format(rule, text) for rule, text in sorted(RULES.items()))
            + "  HP-EX-PARSE  `haproxy -c -f` accepts the file\n"
            "\n"
            "Exit codes\n"
            "  0  clean\n"
            "  1  findings reported\n"
            "  2  could not run: no haproxy binary, no openssl for the certificate fixtures,\n"
            "     a missing examples directory, an unreadable version reference, or an example\n"
            "     whose declared branch the available binary cannot parse (use --allow-skips)\n"
        ),
    )


def main(argv: list[str]) -> int:
    parser = build_parser()
    parser.add_argument("--self-test", action="store_true",
                        help="run against the fixtures in scripts/fixtures/examples and exit")
    parser.add_argument("--structure-only", action="store_true",
                        help="run the pure-Python phase only; makes no claim that anything parses")
    parser.add_argument("--haproxy", default=None,
                        help="path to the haproxy binary to parse with. Defaults to `haproxy` on PATH.")
    parser.add_argument("--allow-skips", action="store_true",
                        help="report, rather than fail, examples whose branch the binary is older than")
    parser.add_argument("--root", default=None,
                        help="skill root. Defaults to the nearest ancestor containing SKILL.md.")
    args = parser.parse_args(argv)

    script_dir = Path(__file__).resolve().parent

    if args.self_test:
        return self_test(script_dir)

    if args.root:
        root = Path(args.root).resolve()
        if not (root / "SKILL.md").is_file():
            print("could not run: no SKILL.md under {}".format(root), file=sys.stderr)
            return EXIT_CANNOT_RUN
    else:
        located = skill_root(script_dir)
        if located is None:
            print("could not run: no SKILL.md above {}; pass --root".format(script_dir),
                  file=sys.stderr)
            return EXIT_CANNOT_RUN
        root = located

    examples = root / "examples" / "haproxy"
    if not examples.is_dir():
        print("could not run: missing {}".format(examples), file=sys.stderr)
        return EXIT_CANNOT_RUN
    configs = sorted(examples.glob("*.cfg"))
    if not configs:
        print("could not run: no *.cfg under {}".format(examples), file=sys.stderr)
        return EXIT_CANNOT_RUN

    findings: list[Finding] = []
    for path in configs:
        findings.extend(check_structure(path, str(path.relative_to(root))))

    findings.extend(check_bundle_metrics(root / "examples" / "kubernetes", root))

    version_findings, version_error = check_version_pins(root)
    if version_error is not None:
        print("could not run: {}".format(version_error), file=sys.stderr)
        return EXIT_CANNOT_RUN
    findings.extend(version_findings)

    parsed = 0
    skipped: list[str] = []
    if args.structure_only:
        print("structure phase only: no claim is made that any example parses")
    else:
        haproxy = args.haproxy or shutil.which("haproxy")
        if haproxy is None or not Path(haproxy).exists():
            for finding in findings:
                print(str(finding))
            print("could not run: no haproxy binary. Pass --haproxy <path>, or --structure-only "
                  "to run the pure-Python phase and claim nothing about parsing.", file=sys.stderr)
            return EXIT_CANNOT_RUN
        parse_findings, skipped, notes, parse_error = run_parse_phase(
            root, haproxy, args.allow_skips)
        findings.extend(parse_findings)
        parsed = len(configs) - len(skipped)
        for line in notes:
            print("NOTE    {}".format(line))
        for line in skipped:
            print("SKIPPED {}".format(line))
        if parse_error is not None:
            for finding in findings:
                print(str(finding))
            print("could not run: {}".format(parse_error), file=sys.stderr)
            return EXIT_CANNOT_RUN

    for finding in findings:
        print(str(finding))

    print("checked {} example config(s); parsed {}; skipped {}; {} finding(s)".format(
        len(configs), parsed, len(skipped), len(findings)))
    return EXIT_FINDINGS if findings else EXIT_CLEAN


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
