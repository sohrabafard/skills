#!/usr/bin/env python3
"""Read or replace the developer_instructions body of a Codex agent TOML.

Usage:
  codex_body.py get <agent.toml>              print the decoded body
  codex_body.py set <agent.toml> <body-file>  replace the body with the file's text

Exit 0 done, 2 the TOML has no single-line JSON-string body.
"""
import json
import re
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in {"get", "set"} or (sys.argv[1] == "set" and len(sys.argv) != 4):
        print(__doc__, file=sys.stderr)
        return 2
    path = Path(sys.argv[2])
    text = path.read_text(encoding="utf-8")
    match = re.search(r'^developer_instructions = (".*")$', text, re.M)
    if not match:
        print(f"{path}: no single-line developer_instructions string", file=sys.stderr)
        return 2
    if sys.argv[1] == "get":
        sys.stdout.write(json.loads(match[1]))
        return 0
    body = Path(sys.argv[3]).read_text(encoding="utf-8").rstrip("\n")
    path.write_text(text[:match.start(1)] + json.dumps(body, ensure_ascii=False) + text[match.end(1):], encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
