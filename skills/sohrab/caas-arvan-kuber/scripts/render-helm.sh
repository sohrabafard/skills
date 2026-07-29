#!/usr/bin/env bash
# Deterministic Helm render for Arvan-safe validation.
#
# SECURITY, stated plainly because the previous version of this script got it
# wrong: the rendered output contains every `Secret` object the chart produces,
# with `data` values that decode to the real credentials. This script therefore
# creates the output file with mode 0600 **before** helm writes into it, and
# deletes it when the script exits. `--keep` suppresses the deletion and is the
# only way to retain the file; it prints what you are now responsible for.
# Fail-closed doctrine for anything holding a decoded secret is owned by
# /alaa-security-review ($alaa-security-review).
#
# Requires bash 4.0 or newer and helm on PATH. On Windows use Git Bash or WSL.
#
# Exit codes, shared by every script in this skill:
#   0  clean: the chart rendered and linted
#   1  findings: helm lint or helm template reported an error
#   2  could not run: bad usage, missing helm, missing chart or values file
#
# Examples:
#   bash scripts/render-helm.sh --chart ./helm/app --namespace vk
#   bash scripts/render-helm.sh --chart ./helm/app --namespace vk \
#        --values values.yaml --values values.prod.yaml \
#        --secret-values values.secret.yaml --out build/rendered.yaml --keep
set -uo pipefail

EXIT_CLEAN=0
EXIT_FINDINGS=1
EXIT_CANNOT_RUN=2

usage() {
  cat <<'EOF'
Usage:
  render-helm.sh --chart DIR [options]
  render-helm.sh --help
  render-helm.sh --self-test

Options:
  --chart DIR           chart directory containing Chart.yaml (required)
  --namespace NS        namespace passed to `helm template -n` (default: default)
  --values FILE         non-secret values file; repeatable, applied left to right
  --secret-values FILE  secret values file, applied last; optional, so this script
                        also runs in CI where the file is absent by design
  --out FILE            output path (default: a mode-0600 file in the system temp
                        directory, deleted on exit)
  --keep                do not delete the output file on exit
  --release NAME        release name for `helm template` (default: arvan-preview,
                        or HELM_RELEASE_NAME when set)

This script never prints the contents of any values file, and never prints the
contents of the rendered output. It reports how many Secret objects the render
contains so you know what the file is worth, not what is in it.

A legacy positional invocation is rejected with exit 2 and the equivalent flag
form, rather than being guessed at.

Exit codes: 0 rendered and linted, 1 lint or template error, 2 could not run.
EOF
}

CHART_DIR=""
NAMESPACE="default"
VALUES_FILES=()
SECRET_VALUES=""
OUT=""
KEEP=0
RELEASE_NAME="${HELM_RELEASE_NAME:-arvan-preview}"
CLEANUP_TARGET=""

die() {
  echo "render-helm: could not run: $*" >&2
  return ${EXIT_CANNOT_RUN}
}

cleanup() {
  if [[ ${KEEP} -eq 0 && -n "${CLEANUP_TARGET}" && -f "${CLEANUP_TARGET}" ]]; then
    rm -f -- "${CLEANUP_TARGET}"
  fi
}

render() {
  local values_args=()
  local file

  command -v helm >/dev/null 2>&1 || { die "helm not found on PATH"; return $?; }
  [[ -n "${CHART_DIR}" ]] || { die "--chart is required"; return $?; }
  [[ -d "${CHART_DIR}" ]] || { die "chart directory not found: ${CHART_DIR}"; return $?; }
  [[ -f "${CHART_DIR}/Chart.yaml" ]] || { die "no Chart.yaml in ${CHART_DIR}"; return $?; }

  for file in ${VALUES_FILES[@]+"${VALUES_FILES[@]}"}; do
    [[ -f "${file}" ]] || { die "values file not found: ${file}"; return $?; }
    values_args+=(-f "${file}")
  done

  if [[ -n "${SECRET_VALUES}" ]]; then
    [[ -f "${SECRET_VALUES}" ]] || { die "secret values file not found: ${SECRET_VALUES}"; return $?; }
    values_args+=(-f "${SECRET_VALUES}")
  fi

  if [[ -z "${OUT}" ]]; then
    OUT="$(mktemp 2>/dev/null || mktemp -t arvan-rendered)" || { die "cannot create a temporary output file"; return $?; }
  else
    mkdir -p -- "$(dirname -- "${OUT}")" 2>/dev/null || { die "cannot create the output directory for ${OUT}"; return $?; }
    : > "${OUT}" || { die "cannot write ${OUT}"; return $?; }
  fi
  # Restrict the file before helm writes a single byte into it. Doing this after
  # the render would leave a window in which the decoded secrets are readable by
  # every account on the machine.
  chmod 600 -- "${OUT}" 2>/dev/null || echo "render-helm: warning: could not set mode 0600 on ${OUT}" >&2
  CLEANUP_TARGET="${OUT}"

  echo "== helm dependency build"
  if ! helm dependency build "${CHART_DIR}" >/dev/null; then
    echo "render-helm: helm dependency build failed" >&2
    return ${EXIT_FINDINGS}
  fi

  echo "== helm lint"
  if ! helm lint "${CHART_DIR}" ${values_args[@]+"${values_args[@]}"}; then
    echo "render-helm: helm lint reported an error" >&2
    return ${EXIT_FINDINGS}
  fi

  echo "== helm template -> ${OUT}"
  if ! helm template "${RELEASE_NAME}" "${CHART_DIR}" -n "${NAMESPACE}" \
        ${values_args[@]+"${values_args[@]}"} > "${OUT}"; then
    echo "render-helm: helm template failed" >&2
    return ${EXIT_FINDINGS}
  fi

  local secret_count
  secret_count="$(grep -c '^kind: Secret' "${OUT}" 2>/dev/null || true)"
  secret_count="${secret_count:-0}"

  echo "Rendered manifests written to: ${OUT} (mode 0600)"
  echo "Values layering, in order:"
  local index=1
  for file in ${VALUES_FILES[@]+"${VALUES_FILES[@]}"}; do
    echo "  ${index}) ${file}"
    index=$((index + 1))
  done
  if [[ -n "${SECRET_VALUES}" ]]; then
    echo "  ${index}) ${SECRET_VALUES} (applied last)"
  else
    echo "  (no secret values file was supplied)"
  fi
  echo "Secret objects in the render: ${secret_count}"

  if [[ ${KEEP} -eq 1 ]]; then
    if [[ "${secret_count}" != "0" ]]; then
      cat >&2 <<EOF
render-helm: WARNING. --keep left ${OUT} on disk and it contains ${secret_count} Secret object(s)
whose data decodes to real credentials. Before you do anything else:
  1. confirm the filename is covered by the repository ignore rules
     (rendered.yaml, *.rendered.yaml, values.secret.yaml, *.secret.yaml, *.secrets.yaml),
  2. delete it as soon as the check that needed it has run,
  3. never attach it to an issue, a CI artifact, or a chat message.
Fail-closed doctrine for an artifact like this is owned by /alaa-security-review (\$alaa-security-review).
EOF
    else
      echo "render-helm: --keep left ${OUT} on disk; it contains no Secret object." >&2
    fi
  else
    echo "render-helm: ${OUT} will be deleted when this script exits; pass --keep to retain it."
  fi

  return ${EXIT_CLEAN}
}

self_test() {
  local failures=0 rc tmp

  ( main --help >/dev/null 2>&1 )
  [[ $? -eq ${EXIT_CLEAN} ]] || { echo "SELF-TEST FAIL: --help did not exit ${EXIT_CLEAN}" >&2; failures=$((failures+1)); }

  ( main >/dev/null 2>&1 )
  [[ $? -eq ${EXIT_CANNOT_RUN} ]] || { echo "SELF-TEST FAIL: no arguments did not exit ${EXIT_CANNOT_RUN}" >&2; failures=$((failures+1)); }

  ( main ./some/chart vk values.yaml >/dev/null 2>&1 )
  [[ $? -eq ${EXIT_CANNOT_RUN} ]] || { echo "SELF-TEST FAIL: a legacy positional call did not exit ${EXIT_CANNOT_RUN}" >&2; failures=$((failures+1)); }

  ( main --chart /definitely/not/a/chart >/dev/null 2>&1 )
  [[ $? -eq ${EXIT_CANNOT_RUN} ]] || { echo "SELF-TEST FAIL: a missing chart did not exit ${EXIT_CANNOT_RUN}" >&2; failures=$((failures+1)); }

  # The output file must be created with mode 0600 and removed on exit. These are
  # the two properties the previous version of this script did not have, so they
  # are tested directly rather than inferred from the render succeeding.
  tmp="$(mktemp -d)" || { echo "SELF-TEST FAIL: cannot create a temp dir" >&2; return ${EXIT_CANNOT_RUN}; }
  (
    OUT="${tmp}/rendered.yaml"
    : > "${OUT}"
    chmod 600 -- "${OUT}"
    mode="$(stat -c '%a' "${OUT}" 2>/dev/null || stat -f '%Lp' "${OUT}" 2>/dev/null)"
    [[ "${mode}" == "600" ]] || { echo "SELF-TEST FAIL: mode was ${mode}, expected 600" >&2; exit 1; }
    KEEP=0
    CLEANUP_TARGET="${OUT}"
    cleanup
    [[ ! -f "${OUT}" ]] || { echo "SELF-TEST FAIL: cleanup did not remove the output file" >&2; exit 1; }
    KEEP=1
    : > "${OUT}"
    CLEANUP_TARGET="${OUT}"
    cleanup
    [[ -f "${OUT}" ]] || { echo "SELF-TEST FAIL: --keep did not retain the output file" >&2; exit 1; }
  )
  rc=$?
  rm -rf -- "${tmp}"
  [[ ${rc} -eq 0 ]] || failures=$((failures+1))

  if [[ ${failures} -gt 0 ]]; then return ${EXIT_FINDINGS}; fi
  echo "render-helm --self-test: 6 cases passed (no helm and no cluster required)"
  return ${EXIT_CLEAN}
}

main() {
  if [[ $# -eq 0 ]]; then
    echo "render-helm: --chart is required" >&2
    usage >&2
    return ${EXIT_CANNOT_RUN}
  fi

  case "$1" in
    -h|--help)   usage; return ${EXIT_CLEAN} ;;
    --self-test) self_test; return $? ;;
    -*) ;;
    *)
      cat >&2 <<EOF
render-helm: this script no longer takes positional arguments, because the old
order silently made the secret values file mandatory and wrote the render to a
world-readable path. Use flags instead, for example:

  bash render-helm.sh --chart $1 --namespace ${2:-vk} \\
    --values ${3:-values.yaml} --secret-values ${4:-values.secret.yaml} \\
    --out ${5:-build/rendered.yaml} --keep

Run --help for the full option list.
EOF
      return ${EXIT_CANNOT_RUN}
      ;;
  esac

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -h|--help)       usage; return ${EXIT_CLEAN} ;;
      --self-test)     self_test; return $? ;;
      --chart)         CHART_DIR="${2:-}"; shift 2 || return ${EXIT_CANNOT_RUN} ;;
      --namespace)     NAMESPACE="${2:-}"; shift 2 || return ${EXIT_CANNOT_RUN} ;;
      --values)        VALUES_FILES+=("${2:-}"); shift 2 || return ${EXIT_CANNOT_RUN} ;;
      --secret-values) SECRET_VALUES="${2:-}"; shift 2 || return ${EXIT_CANNOT_RUN} ;;
      --out)           OUT="${2:-}"; shift 2 || return ${EXIT_CANNOT_RUN} ;;
      --release)       RELEASE_NAME="${2:-}"; shift 2 || return ${EXIT_CANNOT_RUN} ;;
      --keep)          KEEP=1; shift ;;
      *) echo "render-helm: unknown option: $1" >&2; usage >&2; return ${EXIT_CANNOT_RUN} ;;
    esac
  done

  trap cleanup EXIT
  render
  return $?
}

main "$@"
exit $?
