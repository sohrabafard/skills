#!/usr/bin/env bash
#
# extract_ansible_info_wrapper.sh - resolve an interpreter with PyYAML and run
# extract_ansible_info.py. Every argument passes through unchanged.
#
# Requires bash 4.0 or newer. Exit codes are the Python script's: 0 clean,
# 2 could not run, 64 usage error.

set -uo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib/common.sh"

PY="$AV_SCRIPT_DIR/extract_ansible_info.py"

if ! PYTHON_BIN="$(command -v python3)"; then
    if ! PYTHON_BIN="$(command -v python)"; then
        av_cannot_run "python3 is not on PATH; extract_ansible_info.py cannot run"
    fi
fi

if [ ! -f "$PY" ]; then
    av_cannot_run "extract_ansible_info.py not found beside this script at $PY"
fi

if ! "$PYTHON_BIN" -c "import yaml" >/dev/null 2>&1; then
    if av_bootstrap; then
        PYTHON_BIN="$(av_venv_bin "$AV_VENV")/python"
    else
        av_cannot_run "PyYAML is not importable and no tool environment could be created. Install it with: python3 -m pip install -r scripts/requirements.txt"
    fi
fi

exec "$PYTHON_BIN" "$PY" "$@"
