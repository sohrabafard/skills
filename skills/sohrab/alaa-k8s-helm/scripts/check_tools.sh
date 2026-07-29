#!/usr/bin/env bash
# Inventory the tools a lane needs.
#
# Requires bash 4.0 or newer (associative-array-free, but it uses `mapfile`-free
# array idioms that still need bash arrays). macOS ships bash 3.2 as
# /bin/bash: run this with a Homebrew bash, or with `bash scripts/check_tools.sh`
# after installing one. On Windows use Git Bash or WSL.
#
# Exit codes, shared by every script in this skill:
#   0  every required tool for the lane is present
#   1  findings: a required tool is missing
#   2  could not run: bad lane name, bad usage, or an unusable interpreter
set -uo pipefail

EXIT_CLEAN=0
EXIT_FINDINGS=1
EXIT_CANNOT_RUN=2

usage() {
  cat <<'EOF'
Usage: check_tools.sh [all|yaml|helm|debug]
       check_tools.sh --help
       check_tools.sh --self-test

Reports the required and optional tools for a lane, and prefers `oc` over
`kubectl` when OpenShift tooling is present.

Lanes:
  yaml    yamllint, kubeconform
  helm    helm, yamllint, kubeconform (optional: helm-diff)
  debug   no required tool; kubectl or oc is reported when present
  all     yamllint, kubeconform (optional: helm, helm-diff)

Exit codes: 0 every required tool present, 1 a required tool missing,
2 could not run (unknown lane or bad usage).
EOF
}

self_test() {
  local failures=0

  # The lane table must resolve for every documented lane.
  local lane
  for lane in all yaml helm debug; do
    if ! lane_required "$lane" >/dev/null; then
      echo "SELF-TEST FAIL: lane '$lane' has no required-tool list" >&2
      failures=$((failures + 1))
    fi
  done

  # An unknown lane must be "could not run", never "clean".
  ( main not-a-lane >/dev/null 2>&1 )
  if [[ $? -ne ${EXIT_CANNOT_RUN} ]]; then
    echo "SELF-TEST FAIL: an unknown lane did not exit ${EXIT_CANNOT_RUN}" >&2
    failures=$((failures + 1))
  fi

  # --help must exit 0, because a wrapper that checks status must not see a failure.
  ( main --help >/dev/null 2>&1 )
  if [[ $? -ne ${EXIT_CLEAN} ]]; then
    echo "SELF-TEST FAIL: --help did not exit ${EXIT_CLEAN}" >&2
    failures=$((failures + 1))
  fi

  # A missing tool must produce exit 1 and name the tool.
  local out
  out="$(REQUIRED_OVERRIDE="definitely-not-a-real-tool" main yaml 2>&1)"
  if [[ $? -ne ${EXIT_FINDINGS} ]] || [[ "$out" != *definitely-not-a-real-tool* ]]; then
    echo "SELF-TEST FAIL: a missing required tool did not exit ${EXIT_FINDINGS} with its name" >&2
    failures=$((failures + 1))
  fi

  if [[ ${failures} -gt 0 ]]; then
    return ${EXIT_FINDINGS}
  fi
  echo "check_tools --self-test: 7 cases passed"
  return ${EXIT_CLEAN}
}

have() { command -v "$1" >/dev/null 2>&1; }

lane_required() {
  case "$1" in
    yaml)  echo "yamllint kubeconform" ;;
    helm)  echo "helm yamllint kubeconform" ;;
    debug) echo "" ;;
    all)   echo "yamllint kubeconform" ;;
    *)     return 1 ;;
  esac
  return 0
}

lane_optional() {
  case "$1" in
    yaml)  echo "jq yq stern k9s kubectl-neat" ;;
    helm)  echo "jq yq stern k9s kubectl-neat helm-diff" ;;
    debug) echo "jq yq stern k9s kubectl-neat" ;;
    all)   echo "jq yq stern k9s kubectl-neat helm helm-diff" ;;
  esac
}

main() {
  local lane="${1:-all}"

  case "$lane" in
    -h|--help) usage; return ${EXIT_CLEAN} ;;
    --self-test) self_test; return $? ;;
  esac

  local required_list
  if ! required_list="$(lane_required "$lane")"; then
    echo "check_tools: unknown lane '${lane}'" >&2
    usage >&2
    return ${EXIT_CANNOT_RUN}
  fi
  # Test hook used by --self-test only.
  required_list="${REQUIRED_OVERRIDE:-$required_list}"

  local kube_cli=""
  if have oc; then kube_cli="oc"; elif have kubectl; then kube_cli="kubectl"; fi

  if [[ -n "$kube_cli" ]]; then
    echo "[ok]   Kubernetes CLI: $kube_cli"
    "$kube_cli" version --client 2>/dev/null | sed 's/^/       /' || true
  else
    echo "[warn] no Kubernetes CLI found (kubectl or oc)"
  fi

  echo
  local missing=""
  local tool
  for tool in ${required_list}; do
    if have "$tool"; then
      echo "[ok]   $tool"
      case "$tool" in
        helm)        helm version 2>/dev/null | head -n 1 | sed 's/^/       /' || true ;;
        yamllint)    yamllint --version 2>/dev/null | sed 's/^/       /' || true ;;
        kubeconform) kubeconform -v 2>/dev/null | sed 's/^/       /' || true ;;
      esac
    else
      echo "[FAIL] $tool (required for lane: $lane)"
      missing="${missing} ${tool}"
    fi
  done

  echo
  for tool in $(lane_optional "$lane"); do
    if [[ "$tool" == "helm-diff" ]]; then
      if have helm && helm plugin list 2>/dev/null | awk '{print $1}' | grep -qx diff; then
        echo "[ok]   helm-diff"
      else
        echo "[warn] helm-diff not installed"
      fi
      continue
    fi
    if have "$tool"; then echo "[ok]   $tool"; else echo "[warn] $tool not installed"; fi
  done

  echo
  if [[ -n "${missing// /}" ]]; then
    echo "check_tools: missing required tool(s) for lane ${lane}:${missing}" >&2
    return ${EXIT_FINDINGS}
  fi

  echo "check_tools: lane ${lane} has every required tool."
  return ${EXIT_CLEAN}
}

main "$@"
exit $?
