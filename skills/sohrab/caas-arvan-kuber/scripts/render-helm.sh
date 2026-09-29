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
# Requires bash 4.0 or newer, helm on PATH, and demonstrable POSIX mode 0600.
# Git Bash/WSL support depends on the output filesystem enforcing that mode;
# otherwise rendering blocks before Helm. GNU-compatible stat and /dev/fd are required.
# Output parent must be caller-owned mode 0700; ancestors must be root/caller-owned
# and not group/other-writable, except root-owned sticky ancestors such as /tmp.
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
  --out FILE            new output path; existing files and symlinks are refused
                        parent must be caller-owned mode 0700 with trusted ancestors
                        (default: private system-temp directory, deleted on exit)
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
OUTPUT_ID=""
OUTPUT_OPEN=0
PRIVATE_TEMP_DIR=""

die() {
  echo "render-helm: could not run: $*" >&2
  return ${EXIT_CANNOT_RUN}
}

# The retained descriptor is the write authority; the pathname is only a label.
output_matches() {
  [[ -n "${OUTPUT_ID}" && ! -L "${OUT}" && -f "${OUT}" ]] || return 1
  [[ "$(stat -Lc '%d:%i' -- "${OUT}" 2>/dev/null)" == "${OUTPUT_ID}" ]]
}

cleanup() {
  if [[ ${KEEP} -eq 0 && -n "${CLEANUP_TARGET}" ]] && output_matches; then
    rm -f -- "${CLEANUP_TARGET}"
  fi
  if [[ ${OUTPUT_OPEN} -eq 1 ]]; then exec 9>&-; OUTPUT_OPEN=0; fi
  # Remove only an empty private directory created by this invocation.
  if [[ ${KEEP} -eq 0 && -n "${PRIVATE_TEMP_DIR}" ]]; then
    rmdir -- "${PRIVATE_TEMP_DIR}" 2>/dev/null || true
  fi
}

trusted_parent() {
  local parent="$1" current="$1" owner mode bits caller
  caller="$(id -u)" || return 1
  while :; do
    read -r owner mode < <(stat -Lc '%u %a' -- "${current}" 2>/dev/null)
    [[ "${owner}" =~ ^[0-9]+$ && "${mode}" =~ ^[0-7]+$ ]] || return 1
    [[ "${owner}" == "${caller}" || "${owner}" == 0 ]] || return 1
    bits=$((8#${mode}))
    if [[ "${current}" == "${parent}" ]]; then
      # Other identities cannot enter or replace entries in the output directory.
      [[ "${owner}" == "${caller}" && ${bits} -eq $((8#700)) ]] || return 1
    elif (( bits & 8#22 )); then
      # A root-owned sticky ancestor (e.g. /tmp) protects our owned child entry.
      [[ "${owner}" == 0 ]] && (( bits & 8#1000 )) || return 1
    fi
    [[ "${current}" == / ]] && break
    current="$(dirname -- "${current}")"
  done
}

validate_descriptor() {
  local owner mode
  [[ ${OUTPUT_OPEN} -eq 1 && -f /dev/fd/9 ]] || return 1
  read -r owner mode < <(stat -Lc '%u %a' /dev/fd/9 2>/dev/null)
  [[ "${owner}" == "$(id -u)" && "${mode}" == 600 ]]
}

prepare_output() {
  local parent previous_noclobber=0 previous_umask
  if [[ -z "${OUT}" ]]; then
    PRIVATE_TEMP_DIR="$(umask 077; mktemp -d)" || { die "cannot create a private temporary directory"; return $?; }
    OUT="${PRIVATE_TEMP_DIR}/rendered.yaml"
  else
    [[ ! -e "${OUT}" && ! -L "${OUT}" ]] || { die "output already exists; choose a new --out path"; return $?; }
    (umask 077; mkdir -p -- "$(dirname -- "${OUT}")") 2>/dev/null || { die "cannot create the output directory"; return $?; }
  fi
  parent="$(cd -- "$(dirname -- "${OUT}")" && pwd -P)" || { die "cannot resolve output directory"; return $?; }
  trusted_parent "${parent}" || { die "output needs a caller-owned mode-0700 directory and trusted ancestors"; return $?; }
  OUT="${parent}/$(basename -- "${OUT}")"
  case $- in *C*) previous_noclobber=1 ;; esac
  previous_umask="$(umask)"
  umask 077
  set -o noclobber
  if { exec 9> "${OUT}"; } 2>/dev/null; then
    OUTPUT_OPEN=1
  else
    umask "${previous_umask}"
    [[ ${previous_noclobber} -eq 1 ]] || set +o noclobber
    die "cannot exclusively create output"; return $?
  fi
  umask "${previous_umask}"
  [[ ${previous_noclobber} -eq 1 ]] || set +o noclobber
  CLEANUP_TARGET="${OUT}"
  OUTPUT_ID="$(stat -Lc '%d:%i' /dev/fd/9 2>/dev/null)" || { die "cannot inspect retained output descriptor"; return $?; }
  chmod 600 /dev/fd/9 2>/dev/null || { die "cannot restrict output permissions; render blocked"; return $?; }
  validate_descriptor || { die "cannot prove regular caller-owned mode-0600 output descriptor"; return $?; }
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

  prepare_output || return $?

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

  if ! validate_descriptor || ! output_matches; then
    die "output identity or permissions changed before rendering"; return $?
  fi
  echo "== helm template -> ${OUT}"
  if ! helm template "${RELEASE_NAME}" "${CHART_DIR}" -n "${NAMESPACE}" \
        ${values_args[@]+"${values_args[@]}"} >&9; then
    echo "render-helm: helm template failed" >&2
    return ${EXIT_FINDINGS}
  fi

  output_matches || { die "output pathname changed during rendering; replacement preserved"; return $?; }
  local secret_count
  secret_count="$(grep -c '^kind: Secret' /dev/fd/9 2>/dev/null || true)"
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
    prepare_output || exit $?
    mode="$(stat -c '%a' "${OUT}" 2>/dev/null || stat -f '%Lp' "${OUT}" 2>/dev/null)"
    [[ "${mode}" == "600" ]] || { echo "SELF-TEST FAIL: mode was ${mode}, expected 600" >&2; exit 1; }
    KEEP=0
    CLEANUP_TARGET="${OUT}"
    cleanup
    [[ ! -f "${OUT}" ]] || { echo "SELF-TEST FAIL: cleanup did not remove the output file" >&2; exit 1; }
    KEEP=1
    prepare_output || exit $?
    cleanup
    [[ -f "${OUT}" ]] || { echo "SELF-TEST FAIL: --keep did not retain the output file" >&2; exit 1; }
  )
  rc=$?
  [[ ${rc} -eq 0 ]] || failures=$((failures+1))

  # Exercise the real render entrypoint with a synthetic Helm function only.
  # Any Helm call on these failure paths is a regression, not a network action.
  mkdir -p "${tmp}/chart"
  printf 'apiVersion: v2\nname: fixture\nversion: 0.1.0\n' > "${tmp}/chart/Chart.yaml"
  local scenario
  for scenario in existing chmod_failure wrong_mode; do
    (
      CHART_DIR="${tmp}/chart"
      OUT="${tmp}/${scenario}.yaml"
      CLEANUP_TARGET=""
      helm() { echo unexpected_helm_call >> "${tmp}/helm-calls"; return 99; }
      case "${scenario}" in
        existing) printf 'preserve this synthetic content' > "${OUT}" ;;
        chmod_failure) chmod() { return 1; } ;;
        wrong_mode) stat() { echo 644; } ;;
      esac
      render >/dev/null 2>&1
      rc=$?
      [[ ${rc} -eq ${EXIT_CANNOT_RUN} && ! -e "${tmp}/helm-calls" ]] || exit 1
      if [[ "${scenario}" == existing ]]; then
        [[ "$(cat "${OUT}")" == 'preserve this synthetic content' && -z "${CLEANUP_TARGET}" ]] || exit 1
      else
        [[ ! -s "${OUT}" ]] || exit 1
      fi
    )
    rc=$?
    [[ ${rc} -eq 0 ]] || { echo "SELF-TEST FAIL: ${scenario} did not protect output" >&2; failures=$((failures+1)); }
  done
  for scenario in dependency_swap template_swap unsafe_parent; do
    (
      CHART_DIR="${tmp}/chart"
      OUT="${tmp}/${scenario}.yaml"
      CLEANUP_TARGET=""
      OUTPUT_ID=""
      OUTPUT_OPEN=0
      local replacement="${tmp}/${scenario}-replacement"
      printf 'unchanged' > "${replacement}"
      helm() {
        case "$1" in
          dependency)
            if [[ "${scenario}" == dependency_swap ]]; then
              rm -f -- "${OUT}"
              ln -s "${replacement}" "${OUT}"
            fi ;;
          template)
            if [[ "${scenario}" == template_swap ]]; then
              rm -f -- "${OUT}"
              ln -s "${replacement}" "${OUT}"
            fi
            printf 'kind: Secret\nsynthetic-secret-sentinel\n' ;;
        esac
        return 0
      }
      if [[ "${scenario}" == unsafe_parent ]]; then
        mkdir "${tmp}/unsafe-parent"
        chmod 0777 "${tmp}/unsafe-parent"
        OUT="${tmp}/unsafe-parent/output.yaml"
      fi
      render >/dev/null 2>&1
      rc=$?
      [[ ${rc} -eq ${EXIT_CANNOT_RUN} ]] || exit 1
      cleanup
      [[ "$(cat "${replacement}")" == unchanged ]] || exit 1
      if [[ "${scenario}" != unsafe_parent ]]; then
        [[ -L "${OUT}" ]] || exit 1
      fi
    )
    rc=$?
    [[ ${rc} -eq 0 ]] || { echo "SELF-TEST FAIL: ${scenario} did not protect retained output" >&2; failures=$((failures+1)); }
  done
  rm -rf -- "${tmp}"

  if [[ ${failures} -gt 0 ]]; then return ${EXIT_FINDINGS}; fi
  echo "render-helm --self-test: 12 cases passed (mocked; no helm and no cluster required)"
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
