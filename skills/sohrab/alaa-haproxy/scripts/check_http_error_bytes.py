#!/usr/bin/env python3
"""Check Content-Length against raw body bytes in standalone HTTP error responses.

This checks byte portability, not HTTP validity; also run HAProxy's real parser.
Exit 0 clean, 1 findings, 2 could not run. Never repairs/normalizes input.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys


def findings(data: bytes) -> list[str]:
    split = re.search(rb"\r?\n\r?\n", data)
    if split is None:
        return ["missing header/body separator"]
    header, body = data[:split.start()], data[split.end():]
    lengths = re.findall(rb"(?im)^content-length:[ \t]*([^\r\n]*)", header)
    if len(lengths) != 1 or not re.fullmatch(rb"[0-9]+[ \t]*", lengths[0]):
        return ["requires exactly one decimal Content-Length"]
    # Compare decimal text: arbitrarily long input must remain a finding, not hit
    # Python's integer-conversion digit limit. Leading zeroes retain decimal meaning.
    declared = lengths[0].strip().lstrip(b"0") or b"0"
    actual = str(len(body)).encode("ascii")
    detail = declared.decode("ascii") if len(declared) <= 40 else "{}-digit value".format(len(declared))
    return [] if declared == actual else ["Content-Length {} != {} raw body bytes".format(detail, len(body))]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="HTTP response files, read as bytes")
    args = parser.parse_args()
    if not args.paths:
        parser.error("supply response paths")
    count = 0
    for raw in args.paths:
        try:
            problems = findings(Path(raw).read_bytes())
        except OSError as exc:
            print("could not run: {}: {}".format(raw, exc), file=sys.stderr)
            return 2
        for problem in problems:
            print("{}: HP-HTTP-BYTES: {}".format(raw, problem))
        count += len(problems)
    print("checked {} response(s); {} finding(s)".format(len(args.paths), count))
    return int(bool(count))


if __name__ == "__main__":
    sys.exit(main())
