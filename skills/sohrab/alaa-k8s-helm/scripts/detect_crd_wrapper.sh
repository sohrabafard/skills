#!/usr/bin/env bash
# Entrypoint for scripts/detect_crd.py that supplies PyYAML when it is absent.
#
# Requires bash 4.0 or newer.
#
# Exit codes are the ones detect_crd.py returns, plus:
#   2  could not run: bad usage, no python3, or PyYAML could not be installed
set -uo pipefail

EXIT_CLEAN=0
EXIT_FINDINGS=1
EXIT_CANNOT_RUN=2

usage() {
  cat <<'EOF'
Usage: detect_crd_wrapper.sh <yaml-file>
       detect_crd_wrapper.sh --help

Classifies each YAML document as a standard Kubernetes, OpenShift, custom, or
removed API version. Uses the system python3 when PyYAML is importable; builds a
throwaway virtual environment in the system temp directory otherwise, and never
inside the repository.

Exit codes: 0 all standard and parsed, 1 findings, 2 could not run.
EOF
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python_script="${script_dir}/detect_crd.py"

find_python() {
  local candidate
  for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys; sys.exit(0 if sys.version_info[0] == 3 else 1)' >/dev/null 2>&1; then
      printf '%s' "$candidate"
      return 0
    fi
  done
  return 1
}

run_with_venv() {
  local py="$1"
  shift
  local tmp_venv
  tmp_venv="$(mktemp -d 2>/dev/null || mktemp -d -t k8s-helm-crd)" || {
    echo "detect_crd_wrapper: cannot create a temporary directory" >&2
    return ${EXIT_CANNOT_RUN}
  }
  trap 'rm -rf "${tmp_venv}"' EXIT

  echo "detect_crd_wrapper: PyYAML not found; creating a temporary virtual environment in ${tmp_venv}" >&2
  "$py" -m venv "${tmp_venv}" >&2 || {
    echo "detect_crd_wrapper: python venv creation failed" >&2
    return ${EXIT_CANNOT_RUN}
  }

  local venv_python="${tmp_venv}/bin/python"
  if [[ ! -x "${venv_python}" ]]; then
    echo "detect_crd_wrapper: no interpreter in the new virtual environment" >&2
    return ${EXIT_CANNOT_RUN}
  fi

  # A restricted or offline network must fail, not hang. Without these flags pip
  # retries a blocked index for minutes and the caller sees no verdict at all.
  if ! "${venv_python}" -m pip install --quiet --disable-pip-version-check \
       --timeout 20 --retries 1 pyyaml >&2; then
    echo "detect_crd_wrapper: could not install PyYAML (offline, or the index is blocked). Install PyYAML into the system interpreter and re-run." >&2
    return ${EXIT_CANNOT_RUN}
  fi

  "${venv_python}" "${python_script}" "$@"
  return $?
}

main() {
  case "${1:-}" in
    -h|--help) usage; return ${EXIT_CLEAN} ;;
    "") echo "detect_crd_wrapper: a YAML file is required" >&2; usage >&2; return ${EXIT_CANNOT_RUN} ;;
  esac
  if [[ $# -ne 1 ]]; then
    echo "detect_crd_wrapper: exactly one YAML file is required" >&2
    return ${EXIT_CANNOT_RUN}
  fi

  local py
  if ! py="$(find_python)"; then
    echo "detect_crd_wrapper: python3 is required and was not found on PATH" >&2
    return ${EXIT_CANNOT_RUN}
  fi

  if "$py" -c 'import yaml' >/dev/null 2>&1; then
    "$py" "${python_script}" "$1"
    return $?
  fi

  run_with_venv "$py" "$1"
  return $?
}

main "$@"
exit $?
