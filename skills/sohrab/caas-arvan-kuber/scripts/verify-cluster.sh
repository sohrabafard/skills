#!/usr/bin/env bash
# Read-only Arvan CaaS capability and RBAC probe. Creates, updates and deletes
# nothing.
#
# It answers two questions in one pass:
#   1. which API capabilities are visible, with server version reported separately;
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
#   2  blocked: discovery, identity, or required permission proof unavailable
set -uo pipefail

EXIT_CLEAN=0
EXIT_FINDINGS=1
EXIT_CANNOT_RUN=2

usage() {
  cat <<'EOF'
Usage:
  verify-cluster.sh <namespace> [runner-serviceaccount-name]
  verify-cluster.sh --help
  verify-cluster.sh --self-test

Read-only checks:
  - server-reported version and visible API capabilities, without inferring a
    version or authorization from an absent API or an empty catalog
  - which of the required namespaced resources are served
  - which line-dependent resources are served (PodDisruptionBudget, NetworkPolicy)
  - quota and LimitRange visibility
  - can-i for the caller; when a ServiceAccount is named, the current context
    must already authenticate as that exact namespace/ServiceAccount principal
  - the RoleBinding subject table, which is what shows an alias-versus-canonical
    namespace mismatch

Nothing is created, updated, or deleted. No token is minted and no impersonation
is attempted. An unavailable or mismatched ServiceAccount identity blocks proof.

Exit codes: 0 every required API and permission present, 1 something required is
absent or denied, 2 required discovery, identity, or permission proof unavailable.
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
    printf 'unknown'
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
  [[ "${out}" == "unknown" ]] || { echo "SELF-TEST FAIL: detect_line returned '${out}', expected 'unknown'" >&2; failures=$((failures+1)); }

  # Every probe command is mocked here, including a trap for credential issuance.
  local scenario rc expected
  for scenario in clean missing_api api_error partial_api resources_error denied unknown_permission runner_match runner_mismatch runner_unknown catalog_empty catalog_denied; do
    case "${scenario}" in
      missing_api|denied) expected=${EXIT_FINDINGS} ;;
      api_error|partial_api|resources_error|unknown_permission|runner_mismatch|runner_unknown) expected=${EXIT_CANNOT_RUN} ;;
      *) expected=${EXIT_CLEAN} ;;
    esac
    out="$(
      kubectl() {
        case "$*" in
          'config current-context') echo synthetic ;;
          'api-versions')
            [[ "${scenario}" != api_error ]] || return 1
            printf 'apps/v1\nautoscaling/v2\n'
            [[ "${scenario}" != partial_api ]] ;;
          'get --raw=/version') printf '{"gitVersion":"v1.37.0"}\n' ;;
          'api-resources --namespaced=false -o name')
            [[ "${scenario}" != catalog_denied ]] || return 1
            [[ "${scenario}" == catalog_empty ]] || echo namespaces ;;
          'api-resources --namespaced=true -o name')
            [[ "${scenario}" != resources_error ]] || return 1
            if [[ "${scenario}" == missing_api ]]; then echo pods
            else printf '%s\n' "${REQUIRED_RESOURCES[@]}"; fi ;;
          'auth whoami -o jsonpath={.status.userInfo.username}')
            [[ "${scenario}" != runner_unknown ]] || return 1
            if [[ "${scenario}" == runner_mismatch ]]; then echo operator
            else echo system:serviceaccount:test:runner; fi ;;
          '-n test auth can-i '*)
            case "${scenario}" in
              denied) echo no; return 1 ;;
              unknown_permission) return 1 ;;
              *) echo yes ;;
            esac ;;
          *'create token'*|*'--as='*) echo 'UNEXPECTED credential operation'; return 99 ;;
          '-n test get '*) return 0 ;;
          *) echo "UNEXPECTED command: $*"; return 99 ;;
        esac
      }
      case "${scenario}" in
        runner_*) probe test runner ;;
        *) probe test '' ;;
      esac
    )"
    rc=$?
    [[ ${rc} -eq ${expected} && "${out}" != *UNEXPECTED* ]] || {
      echo "SELF-TEST FAIL: ${scenario} exited ${rc}, expected ${expected}" >&2
      failures=$((failures+1))
    }
    [[ "${out}" != *'server is 1.26'* && "${out}" != *'identity is broader'* ]] || failures=$((failures+1))
  done

  if [[ ${failures} -gt 0 ]]; then return ${EXIT_FINDINGS}; fi
  echo "verify-cluster --self-test: 20 cases passed (mocked; no cluster required)"
  return ${EXIT_CLEAN}
}

# --- main --------------------------------------------------------------------

probe() {
  local ns="$1" runner_sa="$2"
  local findings=() blocked=()

  echo "== Namespace: ${ns}"
  echo "== Current context: $(kubectl config current-context 2>/dev/null || echo unknown)"
  [[ -n "${runner_sa}" ]] && echo "== Runner ServiceAccount: ${runner_sa}"

  section "Visible API capabilities and server-reported version"
  local api_versions line
  if ! api_versions="$(kubectl api-versions 2>/dev/null | strip_cr | sort)" || [[ -z "${api_versions}" ]]; then
    echo "verify-cluster: API version discovery is unavailable or incomplete" >&2
    return ${EXIT_CANNOT_RUN}
  fi
  line="$(detect_line "${api_versions}")"
  case "${line}" in
    pinned) echo "LEGACY API OBSERVED: autoscaling/v2beta2 was removed upstream in 1.26; this is a capability observation, not proof of the vendor server version." ;;
    current) echo "CURRENT API OBSERVED: resource.k8s.io/v1 became stable upstream in 1.34; confirm the vendor server version separately." ;;
    unknown) echo "VERSION UNKNOWN FROM APIs: missing discriminators establish no version range. Confirm required kinds individually." ;;
  esac
  kubectl get --raw=/version 2>/dev/null | grep -i 'gitVersion' | strip_cr || echo "(server version not readable by this identity)"

  section "Cluster-scoped API catalog (not an authorization check)"
  local cluster_scoped
  if ! cluster_scoped="$(kubectl api-resources --namespaced=false -o name 2>/dev/null | strip_cr)"; then
    echo "Cluster-scoped discovery unavailable or denied; platform scope remains unknown."
  elif [[ -z "${cluster_scoped}" ]]; then
    echo "No cluster-scoped kind visible in this catalog; platform scope remains unknown."
  else
    echo "Cluster-scoped kinds visible: $(printf '%s\n' "${cluster_scoped}" | wc -l | tr -d ' \r'). Visibility grants no verb; check auth can-i for each required operation."
  fi

  section "Required namespaced resources"
  local resource_list missing_required
  if ! resource_list="$(kubectl api-resources --namespaced=true -o name 2>/dev/null | strip_cr)" || [[ -z "${resource_list}" ]]; then
    echo "verify-cluster: cannot list namespaced resources" >&2
    return ${EXIT_CANNOT_RUN}
  fi
  missing_required="$(missing_from_list "${resource_list}" "${REQUIRED_RESOURCES[@]}")"
  if [[ -z "${missing_required}" ]]; then
    echo "All ${#REQUIRED_RESOURCES[@]} required resources are served."
  else
    echo "MISSING: ${missing_required//$'\n'/, }"
    findings+=("missing required resources: ${missing_required//$'\n'/, }")
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
  local verb answer permission_rc
  for verb in "${REQUIRED_VERBS[@]}"; do
    # shellcheck disable=SC2086
    answer="$(kubectl -n "${ns}" auth can-i ${verb} 2>/dev/null | strip_cr)"
    permission_rc=$?
    printf '%-40s %s\n' "${verb}" "${answer:-unknown}"
    if [[ "${answer}" == "no" ]]; then
      findings+=("caller cannot '${verb}' in ${ns}")
    elif [[ ${permission_rc} -ne 0 || "${answer}" != "yes" ]]; then
      blocked+=("caller permission proof unavailable for '${verb}' in ${ns}")
    fi
  done

  if [[ -n "${runner_sa}" ]]; then
    section "ServiceAccount identity for the permission checks above"
    local principal
    if ! principal="$(kubectl auth whoami -o 'jsonpath={.status.userInfo.username}' 2>/dev/null | strip_cr)"; then
      blocked+=("ServiceAccount identity unavailable; use an authorized context with identity discovery support")
    elif [[ "${principal}" != "system:serviceaccount:${ns}:${runner_sa}" ]]; then
      blocked+=("current identity does not match the requested namespace/ServiceAccount; confirm canonical namespace and context")
    else
      echo "Current context matches the requested ServiceAccount; caller permission checks apply to it."
    fi
  fi

  section "RoleBinding subjects (alias versus canonical namespace evidence)"
  kubectl -n "${ns}" get rolebinding -o custom-columns=NAME:.metadata.name,SUBJECT_KINDS:.subjects[*].kind,SUBJECT_NAMESPACES:.subjects[*].namespace,SUBJECT_NAMES:.subjects[*].name 2>/dev/null || echo "(not readable)"
  echo "If a subject namespace differs from '${ns}', read references/arvan-rbac-namespace-facts.md before changing any RoleBinding."

  echo
  if [[ ${#blocked[@]} -gt 0 ]]; then
    echo "verify-cluster: required proof blocked:" >&2
    for name in "${blocked[@]}" "${findings[@]}"; do echo "  - ${name}" >&2; done
    return ${EXIT_CANNOT_RUN}
  fi
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
