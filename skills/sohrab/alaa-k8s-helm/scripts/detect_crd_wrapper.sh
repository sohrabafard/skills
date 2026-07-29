#!/usr/bin/env bash
# Entrypoint for scripts/detect_crd.py that supplies PyYAML when it is absent.
#
# Requires bash 4.0 or newer. On Windows use Git Bash or WSL; the virtual
# environment's activation script lives in Scripts/ there and bin/ elsewhere,
# and this script selects the right one instead of assuming POSIX layout.
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
       detect_crd_wrapper.sh --self-test

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

  # CPython creates Scripts/ on Windows and bin/ everywhere else.
  local venv_python=""
  if [[ -x "${tmp_venv}/bin/python" ]]; then
    venv_python="${tmp_venv}/bin/python"
  elif [[ -x "${tmp_venv}/Scripts/python.exe" ]]; then
    venv_python="${tmp_venv}/Scripts/python.exe"
  elif [[ -x "${tmp_venv}/Scripts/python" ]]; then
    venv_python="${tmp_venv}/Scripts/python"
  else
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

self_test() {
  local failures=0 py
  if ! py="$(find_python)"; then
    echo "SELF-TEST FAIL: no python3 on PATH" >&2
    return ${EXIT_CANNOT_RUN}
  fi
  if [[ ! -f "${python_script}" ]]; then
    echo "SELF-TEST FAIL: detect_crd.py is missing beside this wrapper" >&2
    return ${EXIT_CANNOT_RUN}
  fi

  ( main --help >/dev/null 2>&1 )
  [[ $? -eq ${EXIT_CLEAN} ]] || { echo "SELF-TEST FAIL: --help did not exit ${EXIT_CLEAN}" >&2; failures=$((failures+1)); }

  ( main >/dev/null 2>&1 )
  [[ $? -eq ${EXIT_CANNOT_RUN} ]] || { echo "SELF-TEST FAIL: no argument did not exit ${EXIT_CANNOT_RUN}" >&2; failures=$((failures+1)); }

  ( main "${script_dir}/fixtures/clean.yaml" >/dev/null 2>&1 )
  [[ $? -eq ${EXIT_CLEAN} ]] || { echo "SELF-TEST FAIL: clean.yaml did not exit ${EXIT_CLEAN}" >&2; failures=$((failures+1)); }

  ( main "${script_dir}/fixtures/removed-apis.yaml" >/dev/null 2>&1 )
  [[ $? -eq ${EXIT_FINDINGS} ]] || { echo "SELF-TEST FAIL: removed-apis.yaml did not exit ${EXIT_FINDINGS}" >&2; failures=$((failures+1)); }

  # The delegated self-test must pass too.
  "$py" "${python_script}" --self-test >/dev/null 2>&1
  [[ $? -eq ${EXIT_CLEAN} ]] || { echo "SELF-TEST FAIL: detect_crd.py --self-test failed" >&2; failures=$((failures+1)); }

  if [[ ${failures} -gt 0 ]]; then return ${EXIT_FINDINGS}; fi
  echo "detect_crd_wrapper --self-test: 5 cases passed"
  return ${EXIT_CLEAN}
}

main() {
  case "${1:-}" in
    -h|--help) usage; return ${EXIT_CLEAN} ;;
    --self-test) self_test; return $? ;;
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
