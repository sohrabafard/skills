#!/usr/bin/env python3
"""Compatibility entry point for installing the personal Claude rule-writer."""

from pathlib import Path
import runpy
import sys


if __name__ == "__main__":
    installer = runpy.run_path(str(Path(__file__).with_name("install_claude_agents.py")))
    sys.exit(installer["main"](only_writer=True))
