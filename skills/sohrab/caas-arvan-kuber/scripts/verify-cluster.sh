#!/usr/bin/env bash
set -euo pipefail

# Read-only cluster capability probe for Arvan CaaS / Kubernetes / OpenShift.
# This script MUST NOT create or modify resources.
#
# Usage:
#   bash verify-cluster.sh <namespace> [runner-serviceaccount-name]
#
# Examples:
#   bash verify-cluster.sh vk
#   bash verify-cluster.sh vk gitlab-runner

NS="${1:-}"
RUNNER_SA="${2:-}"

have() { command -v "$1" >/dev/null 2>&1; }

section() {
  echo
  echo "== $1"
}

note() {
  echo "$1"
}

kubectl_safe() {
  # Non-fatal read command helper.
  kubectl "$@" || true
}

if [[ "${NS}" == "-h" || "${NS}" == "--help" ]]; then
  cat <<'EOF'
Usage:
  bash verify-cluster.sh <namespace> [runner-serviceaccount-name]

This script runs read-only discovery checks:
- API groups/versions
- namespaced resource availability
- quota/limitrange visibility
- RBAC can-i checks (optionally impersonating runner SA)

No resources are created, updated, or deleted.
EOF
  exit 0
fi

if [[ -z "${NS}" ]]; then
  echo "ERROR: namespace is required. Use --help for usage." >&2
  exit 1
fi

K_TOOL=""
if have kubectl; then
  K_TOOL="kubectl"
elif have arvan; then
  K_TOOL="arvan"
else
  echo "ERROR: neither kubectl nor arvan CLI found in PATH." >&2
  exit 1
fi

echo "== Tool: ${K_TOOL}"
echo "== Namespace: ${NS}"
if [[ -n "${RUNNER_SA}" ]]; then
  echo "== Runner ServiceAccount hint: ${RUNNER_SA}"
else
  echo "== Runner ServiceAccount hint: (not provided)"
fi

if [[ "${K_TOOL}" != "kubectl" ]]; then
  section "Arvan CLI fallback"
  note "kubectl was not found; running minimal non-mutating Arvan CLI checks."
  arvan paas --help >/dev/null 2>&1 || true
  note "Run full probe with kubectl for API/RBAC/resource checks."
  echo
  echo "Done."
  exit 0
fi

section "Context and namespace"
note "Current context: $(kubectl config current-context 2>/dev/null || echo unknown)"
kubectl_safe get ns "${NS}" -o name

section "OpenAPI-aligned API versions"
kubectl_safe api-versions | grep -E "^(apps/v1|autoscaling/v2|autoscaling/v2beta2|autoscaling/v1|batch/v1|networking.k8s.io/v1|rbac.authorization.k8s.io/v1|coordination.k8s.io/v1|discovery.k8s.io/v1|events.k8s.io/v1)$" || true

section "OpenAPI-aligned namespaced resources"
RESOURCE_LIST="$(kubectl api-resources --namespaced=true -o name 2>/dev/null || true)"
if [[ -z "${RESOURCE_LIST}" ]]; then
  note "(unable to list namespaced resources)"
else
  # Expected in Arvan OpenAPI 1.25.
  REQUIRED_RESOURCES=(
    "configmaps"
    "secrets"
    "services"
    "pods"
    "persistentvolumeclaims"
    "serviceaccounts"
    "limitranges"
    "resourcequotas"
    "deployments.apps"
    "statefulsets.apps"
    "replicasets.apps"
    "jobs.batch"
    "cronjobs.batch"
    "horizontalpodautoscalers.autoscaling"
    "ingresses.networking.k8s.io"
    "roles.rbac.authorization.k8s.io"
    "rolebindings.rbac.authorization.k8s.io"
  )

  MISSING_REQUIRED=()
  for r in "${REQUIRED_RESOURCES[@]}"; do
    if ! grep -qx "${r}" <<<"${RESOURCE_LIST}"; then
      MISSING_REQUIRED+=("${r}")
    fi
  done

  if [[ "${#MISSING_REQUIRED[@]}" -eq 0 ]]; then
    note "Required Arvan OpenAPI resources: OK"
  else
    note "Required Arvan OpenAPI resources: missing -> ${MISSING_REQUIRED[*]}"
  fi

  # Usually absent in Arvan OpenAPI 1.25, but may appear in other clusters.
  OPTIONAL_NON_OPENAPI=(
    "daemonsets.apps"
    "networkpolicies.networking.k8s.io"
    "poddisruptionbudgets.policy"
    "storageclasses.storage.k8s.io"
    "clusterroles.rbac.authorization.k8s.io"
    "clusterrolebindings.rbac.authorization.k8s.io"
  )

  PRESENT_NON_OPENAPI=()
  for r in "${OPTIONAL_NON_OPENAPI[@]}"; do
    if grep -qx "${r}" <<<"${RESOURCE_LIST}"; then
      PRESENT_NON_OPENAPI+=("${r}")
    fi
  done

  if [[ "${#PRESENT_NON_OPENAPI[@]}" -gt 0 ]]; then
    note "Present but not in Arvan OpenAPI 1.25: ${PRESENT_NON_OPENAPI[*]}"
  else
    note "No non-OpenAPI optional resources detected in namespaced list."
  fi
fi

section "Quota and LimitRange visibility"
kubectl_safe -n "${NS}" get resourcequota,limitrange

section "Workload API smoke checks (read-only)"
kubectl_safe -n "${NS}" get deploy
kubectl_safe -n "${NS}" get sts
kubectl_safe -n "${NS}" get job
kubectl_safe -n "${NS}" get cronjob
kubectl_safe -n "${NS}" get ingress

section "Namespace RBAC can-i (current identity)"
kubectl_safe -n "${NS}" auth can-i create deployments.apps
kubectl_safe -n "${NS}" auth can-i create statefulsets.apps
kubectl_safe -n "${NS}" auth can-i create secrets
kubectl_safe -n "${NS}" auth can-i create configmaps
kubectl_safe -n "${NS}" auth can-i create services
kubectl_safe -n "${NS}" auth can-i create rolebindings.rbac.authorization.k8s.io
kubectl_safe -n "${NS}" auth can-i get pods
kubectl_safe -n "${NS}" auth can-i list pods
kubectl_safe -n "${NS}" auth can-i watch pods

section "Namespace RBAC can-i (runner SA impersonation; optional)"
if [[ -n "${RUNNER_SA}" ]]; then
  AS_SA="system:serviceaccount:${NS}:${RUNNER_SA}"
  kubectl_safe -n "${NS}" auth can-i create pods --as="${AS_SA}"
  kubectl_safe -n "${NS}" auth can-i create secrets --as="${AS_SA}"
  kubectl_safe -n "${NS}" auth can-i create configmaps --as="${AS_SA}"
  kubectl_safe -n "${NS}" auth can-i create rolebindings.rbac.authorization.k8s.io --as="${AS_SA}"
  kubectl_safe -n "${NS}" auth can-i get pods --as="${AS_SA}"
  kubectl_safe -n "${NS}" auth can-i list pods --as="${AS_SA}"
else
  note "(skipped: no runner SA provided)"
fi

section "RBAC identity evidence (alias/canonical troubleshooting)"
if [[ -n "${RUNNER_SA}" ]]; then
  kubectl_safe -n "${NS}" get serviceaccount "${RUNNER_SA}" -o name
fi
kubectl_safe -n "${NS}" get rolebinding -o custom-columns=NAME:.metadata.name,SUBJECT_KINDS:.subjects[*].kind,SUBJECT_NAMESPACES:.subjects[*].namespace,SUBJECT_NAMES:.subjects[*].name
note "Reminder: '--as' checks require impersonation permission for the current caller."
note "If Helm release is healthy but runtime calls are forbidden, inspect alias vs canonical namespace identity."

section "Cluster-scoped checks (non-fatal; often restricted on Arvan)"
kubectl_safe get nodes -o name
kubectl_safe get storageclass
kubectl_safe api-resources | grep -Ei "route|buildconfig|networkpolicy|poddisruptionbudget|daemonset" || true

echo
echo "Done."
