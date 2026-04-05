#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <namespace> <pod-name>" >&2
  exit 1
fi

namespace="$1"
pod="$2"

if command -v oc >/dev/null 2>&1; then
  cli="oc"
elif command -v kubectl >/dev/null 2>&1; then
  cli="kubectl"
else
  echo "kubectl or oc is required" >&2
  exit 1
fi

exec_try() {
  "$cli" exec -n "$namespace" "$pod" -- "$@" 2>/dev/null
}

echo "========================================"
echo "Network debug for $namespace/$pod via $cli"
echo "Timestamp: $(date -u +'%Y-%m-%d %H:%M:%S UTC')"
echo "========================================"

echo
echo "## POD ##"
$cli get pod "$pod" -n "$namespace" -o wide || true

echo
echo "## SERVICES ##"
$cli get svc -n "$namespace" || true

echo
echo "## ENDPOINTS ##"
$cli get endpoints,endpointslices -n "$namespace" || true

echo
echo "## NETWORK POLICIES ##"
$cli get networkpolicies -n "$namespace" || true

echo
echo "## RESOLV.CONF ##"
exec_try cat /etc/resolv.conf || echo "Unable to read /etc/resolv.conf"

echo
echo "## DNS TEST ##"
exec_try getent hosts kubernetes.default.svc.cluster.local || exec_try nslookup kubernetes.default.svc.cluster.local || echo "No DNS tool available in the container"

echo
echo "## LISTENING SOCKETS ##"
exec_try ss -lntp || exec_try netstat -lntp || echo "No socket tool available"

echo
echo "## ROUTES / INGRESS ##"
$cli get ingress -n "$namespace" 2>/dev/null || true
$cli get route -n "$namespace" 2>/dev/null || true
