#!/usr/bin/env bash
# Read-only pod-to-service and DNS debugging helper. Creates and modifies nothing.
#
# Requires bash 4.0 or newer. On Windows use Git Bash or WSL.
#
# Exit codes, shared by every script in this skill:
#   0  every probe returned data
#   1  findings: at least one probe returned nothing, so the picture is partial
#   2  could not run: no kubectl or oc, bad usage, or the pod does not exist
set -uo pipefail

EXIT_CLEAN=0
EXIT_FINDINGS=1
EXIT_CANNOT_RUN=2

usage() {
  cat <<'EOF'
Usage: network_debug.sh <namespace> <pod-name>
       network_debug.sh --help
       network_debug.sh --self-test

Collects the evidence the service-path trace in
references/networking-observability-and-tuning.md asks for, in that order: the
Pod, Services, EndpointSlices, NetworkPolicies, the Pod's resolv.conf, a DNS
test, listening sockets, and exposure objects.

Exit codes: 0 every probe returned data, 1 at least one probe returned nothing,
2 could not run.
EOF
}

missing=0

probe() {
  local title="$1"; shift
  printf '\n## %s ##\n' "$title"
  if ! "$@" 2>/dev/null; then
    printf '(no data)\n'
    missing=$((missing + 1))
  fi
}

self_test() {
  local failures=0

  ( main --help >/dev/null 2>&1 )
  [[ $? -eq ${EXIT_CLEAN} ]] || { echo "SELF-TEST FAIL: --help did not exit ${EXIT_CLEAN}" >&2; failures=$((failures+1)); }

  ( main only-one-argument >/dev/null 2>&1 )
  [[ $? -eq ${EXIT_CANNOT_RUN} ]] || { echo "SELF-TEST FAIL: wrong arity did not exit ${EXIT_CANNOT_RUN}" >&2; failures=$((failures+1)); }

  ( PATH="/nonexistent" main ns pod >/dev/null 2>&1 )
  [[ $? -eq ${EXIT_CANNOT_RUN} ]] || { echo "SELF-TEST FAIL: missing CLI did not exit ${EXIT_CANNOT_RUN}" >&2; failures=$((failures+1)); }

  missing=0
  probe "DELIBERATE FAILURE" false >/dev/null 2>&1
  [[ ${missing} -eq 1 ]] || { echo "SELF-TEST FAIL: an empty probe was not counted" >&2; failures=$((failures+1)); }

  if [[ ${failures} -gt 0 ]]; then return ${EXIT_FINDINGS}; fi
  echo "network_debug --self-test: 4 cases passed (no cluster required)"
  return ${EXIT_CLEAN}
}

main() {
  case "${1:-}" in
    -h|--help) usage; return ${EXIT_CLEAN} ;;
    --self-test) self_test; return $? ;;
  esac
  if [[ $# -ne 2 ]]; then
    echo "network_debug: a namespace and a pod name are required" >&2
    usage >&2
    return ${EXIT_CANNOT_RUN}
  fi

  local namespace="$1" pod="$2" cli=""
  if command -v oc >/dev/null 2>&1; then cli="oc"
  elif command -v kubectl >/dev/null 2>&1; then cli="kubectl"
  else
    echo "network_debug: kubectl or oc is required and neither is on PATH" >&2
    return ${EXIT_CANNOT_RUN}
  fi

  if ! "$cli" get pod "$pod" -n "$namespace" >/dev/null 2>&1; then
    echo "network_debug: pod ${namespace}/${pod} is not visible to this identity" >&2
    return ${EXIT_CANNOT_RUN}
  fi

  exec_try() { "$cli" exec -n "$namespace" "$pod" -- "$@" 2>/dev/null; }

  printf '========================================\n'
  printf 'Network debug for %s/%s via %s\n' "$namespace" "$pod" "$cli"
  printf 'Timestamp: %s\n' "$(date -u +'%Y-%m-%d %H:%M:%S UTC')"
  printf '========================================\n'

  probe "POD"              "$cli" get pod "$pod" -n "$namespace" -o wide
  probe "SERVICES"         "$cli" get svc -n "$namespace"
  probe "ENDPOINTSLICES"   "$cli" get endpointslices -n "$namespace"
  probe "NETWORK POLICIES" "$cli" get networkpolicies -n "$namespace"
  probe "RESOLV.CONF"      exec_try cat /etc/resolv.conf
  probe "DNS TEST"         sh -c "$cli exec -n '$namespace' '$pod' -- getent hosts kubernetes.default.svc.cluster.local 2>/dev/null || $cli exec -n '$namespace' '$pod' -- nslookup kubernetes.default.svc.cluster.local 2>/dev/null"
  probe "LISTENING SOCKETS" sh -c "$cli exec -n '$namespace' '$pod' -- ss -lntp 2>/dev/null || $cli exec -n '$namespace' '$pod' -- netstat -lntp 2>/dev/null"
  probe "INGRESS"          "$cli" get ingress -n "$namespace"
  probe "ROUTE"            "$cli" get route -n "$namespace"

  printf '\n'
  if [[ ${missing} -gt 0 ]]; then
    printf 'network_debug: %d probe(s) returned nothing; the picture is partial.\n' "${missing}" >&2
    return ${EXIT_FINDINGS}
  fi
  printf 'network_debug: every probe returned data.\n'
  return ${EXIT_CLEAN}
}

main "$@"
exit $?
