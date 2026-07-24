#!/usr/bin/env bash
# shellcheck shell=bash
#
# Validate Bash and POSIX shell scripts with the local tools that are available.

set -uo pipefail

readonly SCRIPT_NAME=${0##*/}

override_shell=""
format_check=1
smoke_help=0
matrix_check=0
declare -a files=()

usage() {
  cat <<EOF
Usage: ${SCRIPT_NAME} [OPTIONS] FILE...

Description:
  Run syntax checks and any available shell validators against the given files.

Options:
  -s, --shell DIALECT  Override shell detection (bash, sh, dash, ksh)
      --no-format      Skip shfmt diff checks
      --smoke-help     Run -h and --help smoke tests with the detected shell
      --matrix         For sh-family targets, also try dash, busybox ash, and
                       ShellCheck's busybox dialect when available
  -h, --help           Show this help and exit

Checks:
  - syntax with the detected shell
  - ShellCheck when installed
  - shfmt when installed, unless --no-format is used
  - checkbashisms for sh/dash targets when installed
  - optional help smoke checks

Examples:
  ${SCRIPT_NAME} scripts/sync-cache.sh
  ${SCRIPT_NAME} --shell sh --matrix scripts/portable-tool.sh
  ${SCRIPT_NAME} --smoke-help scripts/sync-cache.sh
EOF
}

note() {
  printf 'INFO: %s\n' "$*" >&2
}

warn() {
  printf 'WARN: %s\n' "$*" >&2
}

error() {
  printf 'ERROR: %s\n' "$*" >&2
}

detect_shell() {
  local file=$1
  local first_line=''

  if [[ -n "${override_shell}" ]]; then
    printf '%s\n' "${override_shell}"
    return 0
  fi

  IFS= read -r first_line < "${file}" || true
  case "${first_line}" in
    '#!'*'bash'*) printf 'bash\n' ;;
    '#!'*'dash'*) printf 'dash\n' ;;
    '#!'*'ksh'*) printf 'ksh\n' ;;
    '#!'*'sh'*) printf 'sh\n' ;;
    *) printf 'unknown\n' ;;
  esac
}

syntax_shell_for() {
  case "$1" in
    bash) printf 'bash\n' ;;
    dash) if command -v dash >/dev/null 2>&1; then printf 'dash\n'; else printf 'sh\n'; fi ;;
    sh) printf 'sh\n' ;;
    ksh) printf 'ksh\n' ;;
    *) return 1 ;;
  esac
}

run_syntax_check() {
  local file=$1 dialect=$2 runner
  runner=$(syntax_shell_for "${dialect}") || {
    warn "cannot syntax-check ${file}: unknown shell target"
    return 0
  }

  if ! command -v "${runner}" >/dev/null 2>&1; then
    warn "cannot syntax-check ${file}: ${runner} is not installed"
    return 0
  fi

  if "${runner}" -n "${file}"; then
    note "syntax ok (${runner} -n): ${file}"
    return 0
  fi

  error "syntax check failed (${runner} -n): ${file}"
  return 1
}

run_shellcheck() {
  local file=$1 dialect=$2

  if ! command -v shellcheck >/dev/null 2>&1; then
    warn "shellcheck not installed; skipping ${file}"
    return 0
  fi

  case "${dialect}" in
    bash|sh|dash|ksh) ;;
    *)
      warn "shellcheck skipped for ${file}: unknown shell target"
      return 0
      ;;
  esac

  if shellcheck -s "${dialect}" "${file}"; then
    note "shellcheck ok: ${file}"
    return 0
  fi

  error "shellcheck failed: ${file}"
  return 1
}

run_shfmt() {
  local file=$1

  if [[ "${format_check}" -ne 1 ]]; then
    return 0
  fi

  if ! command -v shfmt >/dev/null 2>&1; then
    warn "shfmt not installed; skipping ${file}"
    return 0
  fi

  if shfmt -d "${file}"; then
    note "shfmt ok: ${file}"
    return 0
  fi

  error "shfmt reported formatting changes: ${file}"
  return 1
}

run_checkbashisms() {
  local file=$1 dialect=$2

  case "${dialect}" in
    sh|dash) ;;
    *) return 0 ;;
  esac

  if ! command -v checkbashisms >/dev/null 2>&1; then
    warn "checkbashisms not installed; skipping ${file}"
    return 0
  fi

  if checkbashisms "${file}"; then
    note "checkbashisms ok: ${file}"
    return 0
  fi

  error "checkbashisms found issues: ${file}"
  return 1
}

run_help_smoke() {
  local file=$1 dialect=$2 runner

  [[ "${smoke_help}" -eq 1 ]] || return 0

  runner=$(syntax_shell_for "${dialect}") || {
    warn "help smoke skipped for ${file}: unknown shell target"
    return 0
  }

  if ! command -v "${runner}" >/dev/null 2>&1; then
    warn "help smoke skipped for ${file}: ${runner} is not installed"
    return 0
  fi

  if ! "${runner}" "${file}" -h >/dev/null; then
    error "help smoke failed for -h: ${file}"
    return 1
  fi

  if ! "${runner}" "${file}" --help >/dev/null; then
    error "help smoke failed for --help: ${file}"
    return 1
  fi

  note "help smoke ok: ${file}"
  return 0
}

run_matrix_checks() {
  local file=$1 dialect=$2 rc=0

  [[ "${matrix_check}" -eq 1 ]] || return 0

  case "${dialect}" in
    sh|dash)
      if command -v dash >/dev/null 2>&1; then
        if dash -n "${file}"; then
          note "matrix syntax ok (dash -n): ${file}"
        else
          error "matrix syntax failed (dash -n): ${file}"
          rc=1
        fi
      fi

      if command -v busybox >/dev/null 2>&1; then
        if busybox ash -n "${file}"; then
          note "matrix syntax ok (busybox ash -n): ${file}"
        else
          error "matrix syntax failed (busybox ash -n): ${file}"
          rc=1
        fi
      fi

      if command -v shellcheck >/dev/null 2>&1; then
        local busybox_out busybox_rc=0
        busybox_out=$(shellcheck -s busybox "${file}" 2>&1) || busybox_rc=$?

        if ((busybox_rc == 0)); then
          note "matrix shellcheck ok (-s busybox): ${file}"
        elif [[ "${busybox_out}" == *'Unknown shell'* ]]; then
          # The busybox dialect is absent from older ShellCheck releases.
          warn "shellcheck has no busybox dialect in this version; skipping ${file}"
        else
          printf '%s\n' "${busybox_out}"
          error "matrix shellcheck failed (-s busybox): ${file}"
          rc=1
        fi
      fi
      ;;
  esac

  return "${rc}"
}

validate_one() {
  local file=$1 dialect rc=0

  [[ -f "${file}" ]] || {
    error "file not found: ${file}"
    return 1
  }

  dialect=$(detect_shell "${file}")
  printf '==> %s [%s]\n' "${file}" "${dialect}"

  run_syntax_check "${file}" "${dialect}" || rc=1
  run_shellcheck "${file}" "${dialect}" || rc=1
  run_shfmt "${file}" || rc=1
  run_checkbashisms "${file}" "${dialect}" || rc=1
  run_matrix_checks "${file}" "${dialect}" || rc=1
  run_help_smoke "${file}" "${dialect}" || rc=1

  return "${rc}"
}

main() {
  while (($#)); do
    case "$1" in
      -s|--shell)
        (($# >= 2)) || {
          error "missing value for $1"
          exit 2
        }
        override_shell=$2
        shift 2
        ;;
      --no-format)
        format_check=0
        shift
        ;;
      --smoke-help)
        smoke_help=1
        shift
        ;;
      --matrix)
        matrix_check=1
        shift
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      -*)
        usage >&2
        error "unknown option: $1"
        exit 2
        ;;
      *)
        files+=("$1")
        shift
        ;;
    esac
  done

  ((${#files[@]})) || {
    usage >&2
    exit 2
  }

  local file rc=0
  for file in "${files[@]}"; do
    validate_one "${file}" || rc=1
  done

  exit "${rc}"
}

main "$@"
