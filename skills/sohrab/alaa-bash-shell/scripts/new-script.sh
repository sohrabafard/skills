#!/usr/bin/env bash
# shellcheck shell=bash
#
# Scaffold a shell file from a bundled template.

set -euo pipefail

readonly SCRIPT_NAME=${0##*/}
readonly SCRIPT_DIR=$(cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd)
readonly TEMPLATE_DIR="${SCRIPT_DIR}/../assets/templates"

kind=""
output_file=""
description="TODO: describe this script"
version="0.1.0"
force=0

usage() {
  cat <<EOF
Usage: ${SCRIPT_NAME} --kind KIND --output PATH [OPTIONS]

Description:
  Create a new shell file from a bundled template.

Required:
      --kind KIND       One of: bash-cli, posix-cli, bash-lib, bats
      --output PATH     Output path to create

Options:
      --description TX  Short description to place in the template
      --version V       Version string for CLI templates (default: 0.1.0)
      --force           Overwrite an existing output file
  -h, --help            Show this help and exit

Examples:
  ${SCRIPT_NAME} --kind bash-cli --output scripts/sync-cache.sh --description "Synchronize cache metadata"
  ${SCRIPT_NAME} --kind posix-cli --output scripts/prune-cache.sh --description "Prune stale cache entries"
  ${SCRIPT_NAME} --kind bash-lib --output lib/project-common.sh
  ${SCRIPT_NAME} --kind bats --output tests/sync-cache.bats
EOF
}

die() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

escape_sed_replacement() {
  printf '%s' "$1" | sed -e 's/[&|\\]/\\&/g'
}

template_for_kind() {
  case "$1" in
    bash-cli) printf '%s\n' "${TEMPLATE_DIR}/bash-cli-template.sh" ;;
    posix-cli) printf '%s\n' "${TEMPLATE_DIR}/posix-cli-template.sh" ;;
    bash-lib) printf '%s\n' "${TEMPLATE_DIR}/bash-lib-template.sh" ;;
    bats) printf '%s\n' "${TEMPLATE_DIR}/bats-test-template.bats" ;;
    *) return 1 ;;
  esac
}

main() {
  while (($#)); do
    case "$1" in
      --kind)
        kind=${2:-}
        shift 2
        ;;
      --output)
        output_file=${2:-}
        shift 2
        ;;
      --description)
        description=${2:-}
        shift 2
        ;;
      --version)
        version=${2:-}
        shift 2
        ;;
      --force)
        force=1
        shift
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        usage >&2
        die "unknown option: $1"
        ;;
    esac
  done

  [[ -n "${kind}" ]] || die "--kind is required"
  [[ -n "${output_file}" ]] || die "--output is required"

  local template
  template=$(template_for_kind "${kind}") || die "unsupported kind: ${kind}"

  if [[ -e "${output_file}" && "${force}" -ne 1 ]]; then
    die "output already exists: ${output_file} (use --force to overwrite)"
  fi

  mkdir -p "$(dirname "${output_file}")"
  cp "${template}" "${output_file}"

  local script_base namespace
  script_base=$(basename "${output_file}")
  namespace=${script_base%.*}
  namespace=${namespace//-/_}

  local escaped_script escaped_description escaped_version escaped_namespace
  escaped_script=$(escape_sed_replacement "${script_base}")
  escaped_description=$(escape_sed_replacement "${description}")
  escaped_version=$(escape_sed_replacement "${version}")
  escaped_namespace=$(escape_sed_replacement "${namespace}")

  sed -i.bak     -e "s|__SCRIPT_NAME__|${escaped_script}|g"     -e "s|__DESCRIPTION__|${escaped_description}|g"     -e "s|__VERSION__|${escaped_version}|g"     -e "s|__NAMESPACE__|${escaped_namespace}|g"     "${output_file}"

  rm -f -- "${output_file}.bak"

  chmod +x "${output_file}"
  printf 'Created %s from %s\n' "${output_file}" "${kind}"
}

main "$@"
