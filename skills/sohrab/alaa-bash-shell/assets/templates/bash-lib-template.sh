#!/usr/bin/env bash
# shellcheck shell=bash
#
# __SCRIPT_NAME__
#
# Description:
#   Shared Bash helpers for __NAMESPACE__ consumers.
#
# Notes:
#   This is a sourced library, not a standalone CLI.

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  printf '%s\n' 'This file is a Bash library and should be sourced, not executed.' >&2
  exit 1
fi

if [[ -n "${__NAMESPACE___LIB_GUARD:-}" ]]; then
  return 0
fi
readonly __NAMESPACE___LIB_GUARD=1

__NAMESPACE__::log() {
  local level=$1
  shift
  printf '[%s] %s\n' "${level}" "$*" >&2
}

__NAMESPACE__::die() {
  __NAMESPACE__::log ERROR "$@"
  return 1
}

__NAMESPACE__::require_cmd() {
  local tool=$1
  command -v "${tool}" >/dev/null 2>&1 || {
    __NAMESPACE__::die "missing required command: ${tool}"
    return 1
  }
}
