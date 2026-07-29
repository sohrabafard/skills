#!/usr/bin/env bash
#
# check_fqcn.sh - report task actions written as short names instead of FQCN.
#
# The detection is a single YAML parse per file, implemented in
# scripts/check_fqcn.py so that it runs identically on Windows. This wrapper
# exists because the rule identifier `check_fqcn.sh` is cited elsewhere; it
# resolves the interpreter and passes every argument through unchanged.
#
# Exit codes: 0 clean, 1 findings, 2 could not run, 64 usage error. FQCN is an
# error here, not advice, because assets/.ansible-lint enables fqcn[action-core]
# as an error and the two must not disagree.

set -uo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib/common.sh"

PY="$AV_SCRIPT_DIR/check_fqcn.py"

if ! PYTHON_BIN="$(command -v python3)"; then
    if ! PYTHON_BIN="$(command -v python)"; then
        av_cannot_run "python3 is not on PATH; check_fqcn.py cannot run"
    fi
fi

if [ ! -f "$PY" ]; then
    av_cannot_run "check_fqcn.py not found beside this script at $PY"
fi

if ! "$PYTHON_BIN" -c "import yaml" >/dev/null 2>&1; then
    if av_bootstrap; then
        PYTHON_BIN="$(av_venv_bin "$AV_VENV")/python"
    else
        av_cannot_run "PyYAML is not importable and no tool environment could be created. Install it with: python3 -m pip install -r scripts/requirements.txt"
    fi
fi

exec "$PYTHON_BIN" "$PY" "$@"
