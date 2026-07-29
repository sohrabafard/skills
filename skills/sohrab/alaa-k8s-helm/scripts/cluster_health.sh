#!/usr/bin/env bash
# Read-only cluster snapshot for triage. This script creates and modifies nothing.
#
# Requires bash 4.0 or newer. On Windows use Git Bash or WSL.
#
# Exit codes, shared by every script in this skill:
#   0  every section returned data
#   1  findings: at least one section was unavailable, so the snapshot is partial
#   2  could not run: no kubectl or oc, or the cluster is unreachable
#
# A partial snapshot is a finding rather than a success, because a section that
# printed "(unavailable)" proved nothing and a caller that branches on exit
# status must not read it as a healthy cluster.
set -uo pipefail

EXIT_CLEAN=0
EXIT_FINDINGS=1
EXIT_CANNOT_RUN=2

usage() {
  cat <<'EOF'
Usage: cluster_health.sh [namespace]
       cluster_health.sh --help
       cluster_health.sh --self-test

Collects a broad, read-only snapshot: version, nodes, namespaces, workloads,
services, exposure objects, storage, quotas, network policies, recent events and
resource usage. With a namespace argument, the namespaced sections are scoped to
it, which is what a namespace-scoped identity on a managed platform needs.

Exit codes: 0 every section returned data, 1 at least one section was
unavailable, 2 no Kubernetes CLI or the cluster is unreachable.
EOF
}

unavailable=0

run_section() {
  local title="$1"; shift
  printf '\n## %s ##\n' "$title"
  if ! "$@" 2>/dev/null; then
    printf '(unavailable)\n'
    unavailable=$((unavailable + 1))
  fi
}

snapshot() {
  local cli="$1" ns="${2:-}"
  local scope=(-A)
  [[ -n "$ns" ]] && scope=(-n "$ns")

  printf '========================================\n'
  printf 'Cluster health snapshot via %s\n' "$cli"
  printf 'Scope: %s\n' "${ns:-all namespaces}"
  printf 'Timestamp: %s\n' "$(date -u +'%Y-%m-%d %H:%M:%S UTC')"
  printf '========================================\n'

  run_section "VERSION"          "$cli" version
  run_section "NODES"            "$cli" get nodes -o wide
  run_section "NAMESPACES"       "$cli" get namespaces
  run_section "PODS"             "$cli" get pods "${scope[@]}" -o wide
  run_section "DEPLOYMENTS"      "$cli" get deployments "${scope[@]}"
  run_section "STATEFULSETS"     "$cli" get statefulsets "${scope[@]}"
  run_section "DAEMONSETS"       "$cli" get daemonsets "${scope[@]}"
  run_section "SERVICES"         "$cli" get services "${scope[@]}"
  run_section "INGRESS"          "$cli" get ingress "${scope[@]}"
  run_section "ROUTE"            "$cli" get route "${scope[@]}"
  run_section "PVC"              "$cli" get pvc "${scope[@]}"
  run_section "PV"               "$cli" get pv
  run_section "RESOURCE QUOTAS"  "$cli" get resourcequotas "${scope[@]}"
  run_section "LIMIT RANGES"     "$cli" get limitranges "${scope[@]}"
  run_section "NETWORK POLICIES" "$cli" get networkpolicies "${scope[@]}"
  run_section "PDB"              "$cli" get poddisruptionbudgets "${scope[@]}"
  run_section "RECENT EVENTS"    "$cli" get events "${scope[@]}" --sort-by=.lastTimestamp
  run_section "TOP NODES"        "$cli" top nodes
  run_section "TOP PODS"         "$cli" top pods "${scope[@]}"

  printf '\n'
  if [[ "$cli" == "oc" ]]; then
    printf "Hint: 'oc get co' shows cluster operator health when the access surface allows it.\n"
  else
    printf "Hint: use 'kubectl cluster-info dump' only when namespace evidence is insufficient.\n"
  fi

  if [[ ${unavailable} -gt 0 ]]; then
    printf '\ncluster_health: %d section(s) were unavailable; this snapshot is partial.\n' "${unavailable}" >&2
    return ${EXIT_FINDINGS}
  fi
  printf '\ncluster_health: every section returned data.\n'
  return ${EXIT_CLEAN}
}

self_test() {
  local failures=0

  ( main --help >/dev/null 2>&1 )
  [[ $? -eq ${EXIT_CLEAN} ]] || { echo "SELF-TEST FAIL: --help did not exit ${EXIT_CLEAN}" >&2; failures=$((failures+1)); }

  # With no Kubernetes CLI on PATH, the script must exit 2 rather than pretending.
  ( PATH="/nonexistent" main >/dev/null 2>&1 )
  [[ $? -eq ${EXIT_CANNOT_RUN} ]] || { echo "SELF-TEST FAIL: missing CLI did not exit ${EXIT_CANNOT_RUN}" >&2; failures=$((failures+1)); }

  # A failing section must be counted, so a partial snapshot exits 1.
  unavailable=0
  run_section "DELIBERATE FAILURE" false >/dev/null 2>&1
  [[ ${unavailable} -eq 1 ]] || { echo "SELF-TEST FAIL: a failing section was not counted" >&2; failures=$((failures+1)); }

  unavailable=0
  run_section "DELIBERATE SUCCESS" true >/dev/null 2>&1
  [[ ${unavailable} -eq 0 ]] || { echo "SELF-TEST FAIL: a succeeding section was counted as unavailable" >&2; failures=$((failures+1)); }

  if [[ ${failures} -gt 0 ]]; then return ${EXIT_FINDINGS}; fi
  echo "cluster_health --self-test: 4 cases passed (no cluster required)"
  return ${EXIT_CLEAN}
}

main() {
  case "${1:-}" in
    -h|--help) usage; return ${EXIT_CLEAN} ;;
    --self-test) self_test; return $? ;;
  esac

  local cli=""
  if command -v oc >/dev/null 2>&1; then cli="oc"
  elif command -v kubectl >/dev/null 2>&1; then cli="kubectl"
  else
    echo "cluster_health: kubectl or oc is required and neither is on PATH" >&2
    return ${EXIT_CANNOT_RUN}
  fi

  if ! "$cli" version --request-timeout=10s >/dev/null 2>&1; then
    if ! "$cli" version --client >/dev/null 2>&1; then
      echo "cluster_health: ${cli} is present but unusable" >&2
      return ${EXIT_CANNOT_RUN}
    fi
    echo "cluster_health: ${cli} cannot reach the cluster API" >&2
    return ${EXIT_CANNOT_RUN}
  fi

  snapshot "$cli" "${1:-}"
  return $?
}

main "$@"
exit $?
