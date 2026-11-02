#!/usr/bin/env python3
"""Lexical configuration checker for ArvanCloud Object Storage consumers.

It reads repository files as text and contacts no endpoint, so a clean run proves
what the repository declares and not how the live bucket behaves. It cannot prove
that a bucket exists, that a credential works, that a region is correct, or that
any S3 operation is supported by the provider.

Checks
  ARV001  multipart part size above ArvanCloud's 400 MB part ceiling
  ARV002  path-style addressing forced on an ArvanCloud endpoint
  ARV003  AWS Signature Version 2 selected
  ARV004  ArvanCloud endpoint reached over plaintext http://
  ARV005  ArvanCloud endpoint present with no region identifier pinned anywhere
  ARV006  bucket name that is not a valid DNS label
  ARV007  ArvanCloud endpoint present with no signature version pinned anywhere
  ARV008  ArvanCloud endpoint present with no provider profile pinned, or with a
          profile pinned to something other than arvancloud

ARV008 treats a profile supplied by variable reference as pinned and compares only
a bare literal against the provider the endpoint names, because the value behind a
reference is chosen outside the repository. It recognises STORAGE_PROVIDER as well
as STORAGE_PROVIDER_PROFILE, so a repository using the shorter spelling is read as
having pinned a profile; the spelling the contract defines is
STORAGE_PROVIDER_PROFILE.

Exit codes
  0  no finding
  1  findings printed with file and line
  2  bad arguments or an unreadable root, so nothing was checked
"""

from __future__ import annotations

import argparse
import os
import re
import sys

# ArvanCloud publishes a 400 MB part ceiling in prose and writes 400 * 2**20 = 419,430,400
# bytes in its own multipart example, so the two readings of "400 MB" disagree. Where the
# provider's published numbers conflict the ceiling here is the minimum of them, because the
# smaller value fails locally before any byte is sent and the larger fails only after a whole
# part crossed the network.
ARVAN_PART_CEILING_BYTES = 400 * 1000 * 1000
ARVAN_HOST_SUFFIX = "arvanstorage"
KNOWN_REGION_IDS = ("ir-thr-at1", "ir-tbz-sh1")
ARVAN_PROFILE_NAME = "arvancloud"

SCANNED_SUFFIXES = (
    ".py", ".php", ".js", ".mjs", ".cjs", ".ts", ".go", ".rb", ".java", ".cs",
    ".yml", ".yaml", ".json", ".toml", ".ini", ".cfg", ".conf", ".tf", ".sh",
    ".env", ".properties", ".xml",
)
SKIPPED_DIRS = {
    ".git", "vendor", "node_modules", "__pycache__", ".gocache", ".gomodcache",
    ".venv", "venv", "dist", "build", ".idea", ".gradle", "target",
}

SIZE_KEY_RE = re.compile(
    r"(?i)\b([A-Za-z0-9_.\-]*(?:part[_\-]?size|chunk[_\-]?size|multipart[_\-]?(?:threshold|chunksize))"
    r"(?:[_\-]?bytes)?)\b"
    r"\s*[:=]{1,2}\s*([^;,\n\r)]+)"
)
SIG_PINNED_RE = re.compile(
    r"(?i)\b[A-Za-z0-9_.\-]*signature[_\-]?(?:version|v2|v4)\b\s*[:=]{1,2}\s*\S"
)
PATH_STYLE_RE = re.compile(
    r"(?i)\b(force[_\-]?path[_\-]?style|use[_\-]?path[_\-]?style[_\-]?endpoint|s3ForcePathStyle)\b"
    r"\s*[:=]{1,2}\s*(true|1|yes|on)\b"
)
ADDRESSING_STYLE_RE = re.compile(r"""(?i)\baddressing[_\-]?style\b\s*[:=]{1,2}\s*['"]?path['"]?""")
SIG_V2_RE = re.compile(
    r"""(?i)(\bsignature[_\-]?v2\b\s*[:=]{1,2}\s*(?:true|1|yes|on)\b"""
    r"""|\bsignature[_\-]?version\b\s*[:=]{1,2}\s*['"]?(?:s3|2|v2)['"]?(?![0-9a-z]))"""
)
HTTP_ARVAN_RE = re.compile(r"(?i)http://[A-Za-z0-9.\-]*arvanstorage[A-Za-z0-9.\-]*")
PROFILE_PINNED_RE = re.compile(
    r"(?i)\b(?:STORAGE_PROVIDER_PROFILE|STORAGE_PROVIDER)\b\s*[:=]{1,2}\s*\S"
)
PROFILE_VALUE_RE = re.compile(
    r"""(?i)\b(STORAGE_PROVIDER_PROFILE|STORAGE_PROVIDER)\b\s*[:=]{1,2}\s*['"]?([A-Za-z][A-Za-z0-9_.\-]*)['"]?\s*$"""
)
BUCKET_NAME_RE = re.compile(
    r"""(?i)\b([A-Za-z0-9_.\-]*bucket(?:[_\-]?name)?)\b\s*[:=]{1,2}\s*['"]([^'"]{1,120})['"]"""
)
POW_RE = re.compile(r"(?i)(?:math\.)?pow\s*\(\s*2\s*,\s*(\d{1,2})\s*\)")
STAR_POW_RE = re.compile(r"\b2\s*\*\*\s*(\d{1,2})\b")
UNIT_RE = re.compile(r"(?i)^(\d+(?:\.\d+)?)\s*(kib|mib|gib|kb|mb|gb|k|m|g|b)?$")
UNIT_FACTORS = {
    None: 1, "b": 1,
    "k": 1024, "kb": 1024, "kib": 1024,
    "m": 1024 ** 2, "mb": 1024 ** 2, "mib": 1024 ** 2,
    "g": 1024 ** 3, "gb": 1024 ** 3, "gib": 1024 ** 3,
}
DNS_LABEL_RE = re.compile(r"^(?!\d+(\.\d+)*$)[a-z0-9]([a-z0-9.\-]{1,61})?[a-z0-9]$")


class Finding:
    def __init__(self, code: str, path: str, line: int, message: str) -> None:
        self.code, self.path, self.line, self.message = code, path, line, message

    def render(self) -> str:
        return f"{self.code} {self.path}:{self.line}: {self.message}"


def parse_size(expr: str) -> int | None:
    """Return a byte count for a simple size expression, or None when unparsable.

    Handles products of integers, KB/MB/GB suffixes, pow(2, N) and 2**N. Returns
    None rather than guessing, because a false finding costs more than a miss.
    """
    text = expr.strip().strip("'\"").replace("_", "")
    text = text.split("//")[0].split("#")[0].strip()
    if not text:
        return None
    text = POW_RE.sub(lambda m: str(2 ** int(m.group(1))), text)
    text = STAR_POW_RE.sub(lambda m: str(2 ** int(m.group(1))), text)
    text = re.sub(r"(?i)\((?:long|int|double|float)\)", "", text)
    text = text.replace("(", " ").replace(")", " ")
    total = 1.0
    seen = False
    for factor in text.split("*"):
        token = factor.strip()
        if not token:
            return None
        match = UNIT_RE.match(token)
        if not match:
            return None
        total *= float(match.group(1)) * UNIT_FACTORS[(match.group(2) or "").lower() or None]
        seen = True
    return int(total) if seen else None


def iter_files(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIPPED_DIRS]
        for name in sorted(filenames):
            if name.endswith(SCANNED_SUFFIXES) or name.startswith(".env"):
                yield os.path.join(dirpath, name)


def scan(root: str) -> list[Finding]:
    findings: list[Finding] = []
    arvan_hits: list[tuple[str, int]] = []
    region_pinned = False
    signature_pinned = False
    profile_pinned = False

    for path in iter_files(root):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as handle:
                lines = handle.read().splitlines()
        except OSError:
            continue
        rel = os.path.relpath(path, root)
        for number, line in enumerate(lines, start=1):
            if ARVAN_HOST_SUFFIX in line.lower():
                arvan_hits.append((rel, number))
            if any(region in line for region in KNOWN_REGION_IDS):
                region_pinned = True
            if SIG_PINNED_RE.search(line):
                signature_pinned = True

            if PROFILE_PINNED_RE.search(line):
                profile_pinned = True
            profile = PROFILE_VALUE_RE.search(line)
            if profile:
                if profile.group(2).lower() != ARVAN_PROFILE_NAME:
                    findings.append(Finding(
                        "ARV008", rel, number,
                        f"{profile.group(1)} is pinned to {profile.group(2)!r}; an endpoint on "
                        "arvanstorage.ir takes the arvancloud profile, because another profile "
                        "supplies a 5 GiB part ceiling and a path-style default that Arvan's "
                        "400 MB ceiling and CDN caching both contradict",
                    ))

            for match in SIZE_KEY_RE.finditer(line):
                size = parse_size(match.group(2))
                if size is not None and size > ARVAN_PART_CEILING_BYTES:
                    findings.append(Finding(
                        "ARV001", rel, number,
                        f"{match.group(1)} is {size} bytes, above ArvanCloud's 400 MB part ceiling; "
                        f"cap it at {ARVAN_PART_CEILING_BYTES}. ArvanCloud publishes 400 MB in prose "
                        "and 400 * 2**20 in its own example, and the ceiling here is the smaller of "
                        "the two because that is the one that cannot be exceeded by accident",
                    ))

            if PATH_STYLE_RE.search(line) or ADDRESSING_STYLE_RE.search(line):
                findings.append(Finding(
                    "ARV002", rel, number,
                    "path-style addressing is forced; ArvanCloud needs virtual-hosted style for CDN caching",
                ))

            if SIG_V2_RE.search(line):
                findings.append(Finding(
                    "ARV003", rel, number,
                    "AWS Signature Version 2 is selected; leave the SDK on its Signature Version 4 default",
                ))

            for match in HTTP_ARVAN_RE.finditer(line):
                findings.append(Finding(
                    "ARV004", rel, number,
                    f"{match.group(0)} uses plaintext http://; use https:// for a non-loopback endpoint",
                ))

            for match in BUCKET_NAME_RE.finditer(line):
                name = match.group(2)
                if "/" in name or "{" in name or "$" in name or " " in name:
                    continue
                if not DNS_LABEL_RE.match(name) or ".." in name:
                    findings.append(Finding(
                        "ARV006", rel, number,
                        f"bucket name {name!r} is not a valid DNS label, so it cannot be addressed "
                        "virtual-hosted on ArvanCloud",
                    ))

    if arvan_hits and not region_pinned:
        rel, number = arvan_hits[0]
        findings.append(Finding(
            "ARV005", rel, number,
            "an ArvanCloud endpoint appears with no region identifier "
            f"({' or '.join(KNOWN_REGION_IDS)}) pinned anywhere in the repository",
        ))

    if arvan_hits and not profile_pinned:
        rel, number = arvan_hits[0]
        findings.append(Finding(
            "ARV008", rel, number,
            "an ArvanCloud endpoint appears with no provider profile pinned anywhere in the "
            "repository; set STORAGE_PROVIDER_PROFILE to arvancloud, because a profile chosen "
            "by omission hands another provider's part ceiling and addressing style to an Arvan "
            "endpoint and the first symptom is a part rejected after it crossed the network",
        ))

    if arvan_hits and not signature_pinned:
        rel, number = arvan_hits[0]
        findings.append(Finding(
            "ARV007", rel, number,
            "an ArvanCloud endpoint appears with no signature version pinned anywhere in the "
            "repository; set STORAGE_SIGNATURE_VERSION to s3v4, because a version left to an SDK "
            "default changes on a dependency upgrade and the failure reads as a wrong secret key",
        ))

    findings.sort(key=lambda f: (f.path, f.line, f.code))
    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="check_arvan_storage_config.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--root", help="repository root to scan")
    args = parser.parse_args(argv)

    if not args.root:
        print("error: --root is required", file=sys.stderr)
        return 2
    if not os.path.isdir(args.root):
        print(f"error: not a readable directory: {args.root}", file=sys.stderr)
        return 2

    findings = scan(args.root)
    for finding in findings:
        print(finding.render())
    if findings:
        print(f"\n{len(findings)} finding(s). This checker reads files lexically and contacts no endpoint.",
              file=sys.stderr)
        return 1
    print("no finding. This checker reads files lexically and contacts no endpoint, "
          "so it does not prove how the live bucket is configured.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
