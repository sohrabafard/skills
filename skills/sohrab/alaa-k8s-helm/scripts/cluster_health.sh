#!/usr/bin/env bash
set -euo pipefail

if command -v oc >/dev/null 2>&1; then
  cli="oc"
elif command -v kubectl >/dev/null 2>&1; then
  cli="kubectl"
else
  echo "kubectl or oc is required" >&2
  exit 1
fi

run_section() {
  local title="$1"
  shift
  echo
  echo "## $title ##"
  "$@" 2>/dev/null || echo "(unavailable)"
}

echo "========================================"
echo "Cluster health snapshot via $cli"
echo "Timestamp: $(date -u +'%Y-%m-%d %H:%M:%S UTC')"
echo "========================================"

run_section "VERSION" $cli version
run_section "NODES" $cli get nodes -o wide
run_section "NAMESPACES" $cli get namespaces
run_section "PODS (ALL NAMESPACES)" $cli get pods -A -o wide
run_section "DEPLOYMENTS" $cli get deployments -A
run_section "STATEFULSETS" $cli get statefulsets -A
run_section "DAEMONSETS" $cli get daemonsets -A
run_section "SERVICES" $cli get services -A
run_section "INGRESS OR ROUTE" bash -lc "$cli get ingress -A 2>/dev/null || $cli get route -A 2>/dev/null"
run_section "PVC" $cli get pvc -A
run_section "PV" $cli get pv
run_section "RESOURCE QUOTAS" $cli get resourcequotas -A
run_section "NETWORK POLICIES" $cli get networkpolicies -A
run_section "RECENT EVENTS" bash -lc "$cli get events -A --sort-by='.lastTimestamp' | tail -50"
run_section "TOP NODES" $cli top nodes
run_section "TOP PODS" $cli top pods -A

echo
if [[ "$cli" == "oc" ]]; then
  echo "Hint: use 'oc adm top pods -A' or 'oc get co' for deeper OpenShift operator views."
else
  echo "Hint: use 'kubectl cluster-info dump' only when namespace-level evidence is insufficient."
fi
