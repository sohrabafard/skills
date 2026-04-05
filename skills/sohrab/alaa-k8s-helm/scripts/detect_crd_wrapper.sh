#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <yaml-file>" >&2
  exit 1
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python_script="$script_dir/detect_crd.py"
yaml_file="$1"

if python3 -c 'import yaml' >/dev/null 2>&1; then
  python3 "$python_script" "$yaml_file"
  exit 0
fi

tmp_venv="$(mktemp -d -t alaa-k8s-helm.XXXXXX)"
trap 'rm -rf "$tmp_venv"' EXIT

echo "PyYAML not found. Creating a temporary virtual environment..." >&2
python3 -m venv "$tmp_venv" >&2
# shellcheck source=/dev/null
source "$tmp_venv/bin/activate"
pip install --quiet pyyaml >&2
python3 "$python_script" "$yaml_file"
