#!/bin/sh
# shellcheck shell=sh
#
# __SCRIPT_NAME__
#
# Description:
#   __DESCRIPTION__
#
# Dependencies:
#   POSIX sh
#
# Environment:
#   TMPDIR      Optional temp directory
#   NO_COLOR    Disable ANSI color output
#
# Exit codes:
#   0 success
#   1 runtime failure
#   2 usage error

set -eu

SCRIPT_NAME=${0##*/}
VERSION="__VERSION__"

VERBOSE=0
DEBUG=0
DRY_RUN=0

usage() {
  cat <<EOF
Usage: ${SCRIPT_NAME} [OPTIONS]

Description:
  __DESCRIPTION__

Options:
  -h, --help        Show this help and exit
      --version     Print the version and exit
  -v, --verbose     Increase log verbosity
      --debug       Enable shell tracing
      --dry-run     Print actions without changing files

Environment:
  TMPDIR            Override temp directory
  NO_COLOR          Disable ANSI color output

Dependencies:
  POSIX sh

Exit codes:
  0 success
  1 runtime failure
  2 usage error

Examples:
  ${SCRIPT_NAME}
  ${SCRIPT_NAME} --dry-run
EOF
}

log() {
  level=$1
  shift
  printf '[%s] %s\n' "${level}" "$*" >&2
}

die() {
  log ERROR "$@"
  exit 1
}

require_cmd() {
  tool=$1
  command -v "${tool}" >/dev/null 2>&1 || die "missing required command: ${tool}"
}

parse_args() {
  while [ "$#" -gt 0 ]; do
    case "$1" in
      -h|--help)
        usage
        exit 0
        ;;
      --version)
        printf '%s %s\n' "${SCRIPT_NAME}" "${VERSION}"
        exit 0
        ;;
      -v|--verbose)
        VERBOSE=1
        shift
        ;;
      --debug)
        DEBUG=1
        shift
        ;;
      --dry-run)
        DRY_RUN=1
        shift
        ;;
      --)
        shift
        break
        ;;
      -*)
        usage >&2
        die "unknown option: $1"
        ;;
      *)
        break
        ;;
    esac
  done
}

main() {
  parse_args "$@"

  if [ "${DEBUG}" -eq 1 ]; then
    set -x
  fi

  if [ "${VERBOSE}" -eq 1 ]; then
    log INFO "verbose mode enabled"
  fi

  if [ "${DRY_RUN}" -eq 1 ]; then
    log INFO "dry-run: nothing will be changed"
  fi

  log INFO "__DESCRIPTION__"
}

main "$@"
