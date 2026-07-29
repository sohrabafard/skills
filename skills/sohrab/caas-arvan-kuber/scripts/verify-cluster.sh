#!/usr/bin/env bash
# Read-only Arvan CaaS capability and RBAC probe. Creates, updates and deletes
# nothing.
#
# It answers two questions in one pass:
#   1. which Kubernetes line the target is on -- the pinned 1.25-era surface or a
#      current one -- using `autoscaling/v2beta2` as the discriminator, because
#      that group was removed upstream in 1.26;
#   2. whether the capabilities and permissions a deployment needs are actually
#      present, and it FAILS when they are not.
#
# The previous version of this script always exited 0, so a cluster serving none
# of the required APIs produced the same status as a perfect one.
#
# Requires bash 4.0 or newer and kubectl. On Windows use Git Bash or WSL. Every
# comparison pipeline strips carriage returns, because a CR on the end of a line
# makes `grep -x` and an anchored `$` never match while the bytes look identical.
#
# Exit codes, shared by every script in this skill:
#   0  clean: every required API and every required permission is present
#   1  findings: a required API or permission is absent
#   2  could not run: no kubectl, or the cluster API is unreachable
set -uo pipefail

EXIT_CLEAN=0
EXIT_FINDINGS=1
EXIT_CANNOT_RUN=2

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<'EOF'
Usage:
  verify-cluster.sh <namespace> [runner-serviceaccount-name]
  verify-cluster.sh --help
  verify-cluster.sh --self-test

Read-only checks:
  - which Kubernetes line the API server is on
  - whether the API surface is namespace-only
  - which of the required namespaced resources are served
  - which line-dependent resources are served (PodDisruptionBudget, NetworkPolicy)
  - quota and LimitRange visibility
  - can-i for the caller, and, when a ServiceAccount is named, the conclusive
    token-based check for that ServiceAccount's own identity
  - the RoleBinding subject table, which is what shows an alias-versus-canonical
    namespace mismatch

Nothing is created, updated, or deleted.

Exit codes: 0 every required API and permission present, 1 something required is
absent, 2 no kubectl or the cluster is unreachable.
EOF
}

# Resources the deployment path needs. These are namespaced and present on both
# the pinned line and the current upstream stable, so their absence is a finding
# regardless of which line the target is on.
REQUIRED_RESOURCES=(
  "configmaps"
  "secrets"
  "services"
  "pods"
  "persistentvolumeclaims"
  "serviceaccounts"
  "deployments.apps"
  "statefulsets.apps"
  "jobs.batch"
  "cronjobs.batch"
  "horizontalpodautoscalers.autoscaling"
  "ingresses.networking.k8s.io"
  "roles.rbac.authorization.k8s.io"
  "rolebindings.rbac.authorization.k8s.io"
)

# Resources whose presence depends on the line, or on the platform's tenancy
# choices. Their absence is reported, not failed: the capability matrix explains
# what to do in each case.
LINE_DEPENDENT_RESOURCES=(
  "limitranges"
  "resourcequotas"
  "replicasets.apps"
  "poddisruptionbudgets.policy"
  "networkpolicies.networking.k8s.io"
  "daemonsets.apps"
)

# Verbs the deployment path needs from the identity that runs it.
REQUIRED_VERBS=(
  "create deployments.apps"
  "create services"
  "create configmaps"
  "create secrets"
  "get pods"
  "list pods"
)

section() { printf '\n== %s\n' "$1"; }

strip_cr() { tr -d '\r'; }

# --- pure helpers, exercised by --self-test without a cluster ----------------

# missing_from_list <newline-separated-list> <name>...
# Prints the names that are absent from the list. Carriage returns are stripped
# from both sides so a CRLF-polluted stream cannot report everything as missing.
missing_from_list() {
  local list="$1"; shift
  local cleaned name
  cleaned="$(printf '%s\n' "${list}" | strip_cr)"
  for name in "$@"; do
    if ! printf '%s\n' "${cleaned}" | grep -qx -- "$(printf '%s' "${name}" | strip_cr)"; then
      printf '%s\n' "${name}"
    fi
  done
}

# detect_line <newline-separated api-versions>
detect_line() {
  local versions
  versions="$(printf '%s\n' "$1" | strip_cr)"
  if printf '%s\n' "${versions}" | grep -qx 'autoscaling/v2beta2'; then
    printf 'pinned'
  elif printf '%s\n' "${versions}" | grep -qx 'resource.k8s.io/v1'; then
    printf 'current'
  else
    printf 'between'
  fi
}

# --- self test ---------------------------------------------------------------

self_test() {
  local failures=0 out

  ( main --help >/dev/null 2>&1 )
  [[ $? -eq ${EXIT_CLEAN} ]] || { echo "SELF-TEST FAIL: --help did not exit ${EXIT_CLEAN}" >&2; failures=$((failures+1)); }

  ( main >/dev/null 2>&1 )
  [[ $? -eq ${EXIT_CANNOT_RUN} ]] || { echo "SELF-TEST FAIL: no namespace did not exit ${EXIT_CANNOT_RUN}" >&2; failures=$((failures+1)); }

  ( PATH="/nonexistent" main vk >/dev/null 2>&1 )
  [[ $? -eq ${EXIT_CANNOT_RUN} ]] || { echo "SELF-TEST FAIL: missing kubectl did not exit ${EXIT_CANNOT_RUN}" >&2; failures=$((failures+1)); }

  out="$(missing_from_list "$(printf 'pods\nservices\n')" pods services secrets)"
  [[ "${out}" == "secrets" ]] || { echo "SELF-TEST FAIL: missing_from_list returned '${out}', expected 'secrets'" >&2; failures=$((failures+1)); }

  # The CRLF case: the same list with carriage returns must give the same answer.
  out="$(missing_from_list "$(printf 'pods\r\nservices\r\n')" pods services secrets)"
  [[ "${out}" == "secrets" ]] || { echo "SELF-TEST FAIL: CRLF input returned '${out}', expected 'secrets'" >&2; failures=$((failures+1)); }

  out="$(detect_line "$(printf 'apps/v1\nautoscaling/v2beta2\n')")"
  [[ "${out}" == "pinned" ]] || { echo "SELF-TEST FAIL: detect_line returned '${out}', expected 'pinned'" >&2; failures=$((failures+1)); }

  out="$(detect_line "$(printf 'apps/v1\r\nresource.k8s.io/v1\r\n')")"
  [[ "${out}" == "current" ]] || { echo "SELF-TEST FAIL: detect_line on CRLF returned '${out}', expected 'current'" >&2; failures=$((failures+1)); }

  out="$(detect_line "$(printf 'apps/v1\nautoscaling/v2\n')")"
  [[ "${out}" == "between" ]] || { echo "SELF-TEST FAIL: detect_line returned '${out}', expected 'between'" >&2; failures=$((failures+1)); }

  if [[ ${failures} -gt 0 ]]; then return ${EXIT_FINDINGS}; fi
  echo "verify-cluster --self-test: 8 cases passed (no cluster required)"
  return ${EXIT_CLEAN}
}

# --- main --------------------------------------------------------------------

probe() {
  local ns="$1" runner_sa="$2"
  local findings=()

  echo "== Namespace: ${ns}"
  echo "== Current context: $(kubectl config current-context 2>/dev/null || echo unknown)"
  [[ -n "${runner_sa}" ]] && echo "== Runner ServiceAccount: ${runner_sa}"

  section "Which Kubernetes line is this"
  local api_versions line
  api_versions="$(kubectl api-versions 2>/dev/null | strip_cr | sort)"
  if [[ -z "${api_versions}" ]]; then
    echo "verify-cluster: the API server returned no api-versions" >&2
    return ${EXIT_CANNOT_RUN}
  fi
  line="$(detect_line "${api_versions}")"
  case "${line}" in
    pinned)  echo "PINNED LINE: autoscaling/v2beta2 is served, so the API server is at most Kubernetes 1.25. Read column A of references/arvan-capability-matrix.md." ;;
    current) echo "CURRENT LINE: resource.k8s.io/v1 is served, so the API server is Kubernetes 1.34 or newer. Read column B of references/arvan-capability-matrix.md." ;;
    between) echo "BETWEEN THE TWO: autoscaling/v2beta2 is absent, so the server is 1.26 or newer, and resource.k8s.io/v1 is absent, so it is older than 1.34. Read column B and confirm every kind with api-resources." ;;
  esac
  kubectl version -o json 2>/dev/null | grep -i 'gitVersion' | strip_cr || echo "(server version not readable by this identity)"

  section "Is the API surface namespace-only"
  local cluster_scoped
  cluster_scoped="$(kubectl api-resources --namespaced=false -o name 2>/dev/null | strip_cr)"
  if [[ -z "${cluster_scoped}" ]]; then
    echo "No cluster-scoped resource is listable by this identity: treat the surface as namespace-only."
  else
    echo "Cluster-scoped resources are listable ($(printf '%s\n' "${cluster_scoped}" | wc -l | tr -d ' \r') kinds). This identity is broader than a normal Arvan tenant; say so in the deliverable."
  fi

  section "Required namespaced resources"
  local resource_list missing_required
  resource_list="$(kubectl api-resources --namespaced=true -o name 2>/dev/null | strip_cr)"
  if [[ -z "${resource_list}" ]]; then
    echo "verify-cluster: cannot list namespaced resources" >&2
    return ${EXIT_CANNOT_RUN}
  fi
  missing_required="$(missing_from_list "${resource_list}" "${REQUIRED_RESOURCES[@]}")"
  if [[ -z "${missing_required}" ]]; then
    echo "All ${#REQUIRED_RESOURCES[@]} required resources are served."
  else
    echo "MISSING: $(printf '%s ' ${missing_required})"
    findings+=("missing required resources: $(printf '%s ' ${missing_required})")
  fi

  section "Line-dependent resources"
  local name
  for name in "${LINE_DEPENDENT_RESOURCES[@]}"; do
    if printf '%s\n' "${resource_list}" | grep -qx -- "${name}"; then
      echo "served:     ${name}"
    else
      echo "not served: ${name}"
    fi
  done
  echo "The capability matrix says what to do for each one that is not served."

  section "Quota and LimitRange"
  kubectl -n "${ns}" get resourcequota,limitrange 2>/dev/null || echo "(not readable)"

  section "Workload smoke reads"
  local kind
  for kind in deploy sts job cronjob ingress; do
    printf -- '-- %s\n' "${kind}"
    kubectl -n "${ns}" get "${kind}" 2>/dev/null || echo "(not readable)"
  done

  section "Required permissions for the calling identity"
  local verb answer
  for verb in "${REQUIRED_VERBS[@]}"; do
    # shellcheck disable=SC2086
    answer="$(kubectl -n "${ns}" auth can-i ${verb} 2>/dev/null | strip_cr)"
    printf '%-40s %s\n' "${verb}" "${answer:-unknown}"
    if [[ "${answer}" != "yes" ]]; then
      findings+=("caller cannot '${verb}' in ${ns}")
    fi
  done

  if [[ -n "${runner_sa}" ]]; then
    section "Conclusive check for the ServiceAccount's own identity"
    echo "'--as' proves nothing when the caller lacks impersonation rights. A token"
    echo "issued for the ServiceAccount evaluates the real principal instead."
    local token
    token="$(kubectl -n "${ns}" create token "${runner_sa}" 2>/dev/null | strip_cr)"
    if [[ -z "${token}" ]]; then
      echo "(could not mint a token for ${runner_sa}: the caller may lack serviceaccounts/token create, or the SA does not exist in ${ns})"
      echo "Falling back to impersonation, which is indicative and not conclusive:"
      for verb in "${REQUIRED_VERBS[@]}"; do
        # shellcheck disable=SC2086
        printf '%-40s %s\n' "${verb}" "$(kubectl -n "${ns}" auth can-i ${verb} --as="system:serviceaccount:${ns}:${runner_sa}" 2>/dev/null | strip_cr || echo unknown)"
      done
    else
      for verb in "${REQUIRED_VERBS[@]}"; do
        # shellcheck disable=SC2086
        answer="$(kubectl --token="${token}" -n "${ns}" auth can-i ${verb} 2>/dev/null | strip_cr)"
        printf '%-40s %s\n' "${verb}" "${answer:-unknown}"
        if [[ "${answer}" != "yes" ]]; then
          findings+=("serviceaccount ${runner_sa} cannot '${verb}' in ${ns}")
        fi
      done
    fi
    unset token
  fi

  section "RoleBinding subjects (alias versus canonical namespace evidence)"
  kubectl -n "${ns}" get rolebinding -o custom-columns=NAME:.metadata.name,SUBJECT_KINDS:.subjects[*].kind,SUBJECT_NAMESPACES:.subjects[*].namespace,SUBJECT_NAMES:.subjects[*].name 2>/dev/null || echo "(not readable)"
  echo "If a subject namespace differs from '${ns}', read references/arvan-rbac-namespace-facts.md before changing any RoleBinding."

  echo
  if [[ ${#findings[@]} -gt 0 ]]; then
    echo "verify-cluster: ${#findings[@]} finding(s):" >&2
    for name in "${findings[@]}"; do echo "  - ${name}" >&2; done
    return ${EXIT_FINDINGS}
  fi
  echo "verify-cluster: every required API and permission is present in ${ns}."
  return ${EXIT_CLEAN}
}

main() {
  case "${1:-}" in
    -h|--help)   usage; return ${EXIT_CLEAN} ;;
    --self-test) self_test; return $? ;;
    "")          echo "verify-cluster: a namespace is required. Use --help for usage." >&2; return ${EXIT_CANNOT_RUN} ;;
  esac

  command -v kubectl >/dev/null 2>&1 || {
    echo "verify-cluster: kubectl is required and was not found on PATH" >&2
    return ${EXIT_CANNOT_RUN}
  }
  if ! kubectl version --request-timeout=10s >/dev/null 2>&1; then
    echo "verify-cluster: kubectl cannot reach the cluster API" >&2
    return ${EXIT_CANNOT_RUN}
  fi

  probe "$1" "${2:-}"
  return $?
}

main "$@"
exit $?
