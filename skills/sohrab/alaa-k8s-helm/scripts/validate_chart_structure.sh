#!/usr/bin/env bash
# Fast Helm chart structure audit.
#
# Requires bash 4.0 or newer. On Windows use Git Bash or WSL. Every `printf`
# format string in this file is a single line with an escaped \n, so a CRLF
# checkout cannot leave a carriage return inside a rendered bullet.
#
# Exit codes, shared by every script in this skill:
#   0  the chart's structure is sound
#   1  findings: a required file or field is missing or malformed
#   2  could not run: bad usage, or the path is not a directory
set -uo pipefail

EXIT_CLEAN=0
EXIT_FINDINGS=1
EXIT_CANNOT_RUN=2

usage() {
  cat <<'EOF'
Usage: validate_chart_structure.sh <chart-directory>
       validate_chart_structure.sh --help
       validate_chart_structure.sh --self-test

Asserts that Chart.yaml, values.yaml and templates/ exist; that Chart.yaml
declares apiVersion v2, a name and a version; that values.schema.json parses;
and that templates/ contains at least one template.

`yq` and `jq` are optional, and their absence is reported as a skipped check
rather than passed over silently, because a check that did not run is not a
check that passed.

Exit codes: 0 sound, 1 findings, 2 could not run.
EOF
}

errors=()
warnings=()
skipped=()

say_ok()   { printf '[ok]   %s\n' "$1"; }
say_warn() { printf '[warn] %s\n' "$1"; }
say_err()  { printf '[FAIL] %s\n' "$1"; }

check_file() {
  if [[ -f "$1" ]]; then say_ok "$2"; else say_err "$2 missing"; errors+=("$2 missing"); fi
}

# Two incompatible programs are called `yq`: the Go implementation (`yq eval`)
# and the Python jq wrapper (`yq -r`). Guessing wrong returns an empty string,
# which would silently pass every Chart.yaml field check. Detect instead.
READER_KIND=""
reader_kind() {
  if [[ -n "${READER_KIND}" ]]; then
    [[ "${READER_KIND}" == "none" ]] && return 0
    printf '%s' "${READER_KIND}"
    return 0
  fi
  if command -v python3 >/dev/null 2>&1 && python3 -c 'import yaml' >/dev/null 2>&1; then
    READER_KIND="python"
  elif command -v yq >/dev/null 2>&1 && yq eval '.' /dev/null >/dev/null 2>&1; then
    READER_KIND="go-yq"
  elif command -v yq >/dev/null 2>&1 && printf 'a: 1\n' | yq -r '.a' >/dev/null 2>&1; then
    READER_KIND="python-yq"
  else
    READER_KIND="none"
    return 0
  fi
  printf '%s' "${READER_KIND}"
}

chart_field() {
  local file="$1" field="$2" value=""
  case "$(reader_kind)" in
    python)
      value="$(python3 -c 'import sys,yaml
doc = yaml.safe_load(open(sys.argv[1], encoding="utf-8", newline=None)) or {}
print(doc.get(sys.argv[2], "") if isinstance(doc, dict) else "")' "$file" "$field" 2>/dev/null || true)"
      ;;
    go-yq)     value="$(yq eval ".${field}" "$file" 2>/dev/null || true)" ;;
    python-yq) value="$(yq -r ".${field} // \"\"" "$file" 2>/dev/null || true)" ;;
  esac
  [[ "$value" == "null" ]] && value=""
  printf '%s' "${value//$'\r'/}"
}

audit() {
  local chart_dir="$1"
  errors=(); warnings=(); skipped=()

  printf 'Validating Helm chart structure: %s\n\n' "$chart_dir"

  check_file "$chart_dir/Chart.yaml" "Chart.yaml"
  check_file "$chart_dir/values.yaml" "values.yaml"

  if [[ -d "$chart_dir/templates" ]]; then
    say_ok "templates/ directory"
  else
    say_err "templates/ directory missing"
    errors+=("templates/ directory missing")
  fi

  if [[ -f "$chart_dir/Chart.yaml" ]]; then
    if [[ -n "$(reader_kind)" ]]; then
      local api_version chart_type name version
      api_version="$(chart_field "$chart_dir/Chart.yaml" apiVersion)"
      chart_type="$(chart_field "$chart_dir/Chart.yaml" type)"
      name="$(chart_field "$chart_dir/Chart.yaml" name)"
      version="$(chart_field "$chart_dir/Chart.yaml" version)"
      [[ "$api_version" == "v2" ]] || errors+=("Chart.yaml apiVersion is '${api_version}', expected v2")
      [[ -n "$name" && "$name" != "null" ]] || errors+=("Chart.yaml name missing")
      [[ -n "$version" && "$version" != "null" ]] || errors+=("Chart.yaml version missing")
      if [[ -n "$chart_type" && "$chart_type" != "null" && "$chart_type" != "application" && "$chart_type" != "library" ]]; then
        errors+=("Chart.yaml type is '${chart_type}', expected application or library")
      fi
    else
      skipped+=("Chart.yaml field checks: no YAML reader found (install python3 with PyYAML, or yq)")
    fi
  fi

  local recommended
  for recommended in "$chart_dir/.helmignore" "$chart_dir/templates/_helpers.tpl" "$chart_dir/values.schema.json"; do
    if [[ -e "$recommended" ]]; then
      say_ok "$(basename "$recommended")"
    else
      say_warn "$(basename "$recommended") not found"
      warnings+=("$(basename "$recommended") not found")
    fi
  done

  if [[ -d "$chart_dir/templates" ]]; then
    local template_count
    template_count="$(find "$chart_dir/templates" -type f \( -name '*.yaml' -o -name '*.tpl' -o -name '*.txt' \) 2>/dev/null | wc -l | tr -d ' \r')"
    if [[ "$template_count" == "0" ]]; then
      errors+=("templates/ contains no YAML, TPL, or NOTES file")
    fi
  fi

  if [[ -f "$chart_dir/values.schema.json" ]]; then
    if command -v jq >/dev/null 2>&1; then
      jq empty "$chart_dir/values.schema.json" >/dev/null 2>&1 || errors+=("values.schema.json is invalid JSON")
    else
      skipped+=("values.schema.json parse check: jq is not installed")
    fi
  fi

  [[ -d "$chart_dir/crds" ]] && say_ok "crds/ directory"
  [[ -d "$chart_dir/charts" ]] && say_ok "charts/ directory"

  printf '\n'
  local item
  if ((${#errors[@]})); then
    printf 'Blocking issues:\n'
    for item in "${errors[@]}"; do printf ' - %s\n' "$item"; done
  fi
  if ((${#warnings[@]})); then
    printf 'Warnings:\n'
    for item in "${warnings[@]}"; do printf ' - %s\n' "$item"; done
  fi
  if ((${#skipped[@]})); then
    printf 'Checks skipped (these did not pass, they did not run):\n'
    for item in "${skipped[@]}"; do printf ' - %s\n' "$item"; done
  fi

  if ((${#errors[@]})); then return ${EXIT_FINDINGS}; fi
  printf 'validate_chart_structure: %s is structurally sound.\n' "$chart_dir"
  return ${EXIT_CLEAN}
}

self_test() {
  local fixtures failures=0
  fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/fixtures"

  ( audit "${fixtures}/chart-good" >/dev/null 2>&1 )
  [[ $? -eq ${EXIT_CLEAN} ]] || { echo "SELF-TEST FAIL: chart-good was not clean" >&2; failures=$((failures+1)); }

  ( audit "${fixtures}/chart-broken" >/dev/null 2>&1 )
  [[ $? -eq ${EXIT_FINDINGS} ]] || { echo "SELF-TEST FAIL: chart-broken did not report findings" >&2; failures=$((failures+1)); }

  ( main "${fixtures}/no-such-chart" >/dev/null 2>&1 )
  [[ $? -eq ${EXIT_CANNOT_RUN} ]] || { echo "SELF-TEST FAIL: a missing directory did not exit ${EXIT_CANNOT_RUN}" >&2; failures=$((failures+1)); }

  ( main --help >/dev/null 2>&1 )
  [[ $? -eq ${EXIT_CLEAN} ]] || { echo "SELF-TEST FAIL: --help did not exit ${EXIT_CLEAN}" >&2; failures=$((failures+1)); }

  # A CRLF Chart.yaml must produce the same verdict as its LF twin.
  if [[ -d "${fixtures}/chart-crlf" ]]; then
    local a b
    audit "${fixtures}/chart-good" >/dev/null 2>&1; a=$?
    audit "${fixtures}/chart-crlf" >/dev/null 2>&1; b=$?
    [[ "$a" -eq "$b" ]] || { echo "SELF-TEST FAIL: CRLF chart gave verdict $b, LF twin gave $a" >&2; failures=$((failures+1)); }
  else
    echo "SELF-TEST FAIL: fixtures/chart-crlf is missing" >&2; failures=$((failures+1))
  fi

  if [[ ${failures} -gt 0 ]]; then return ${EXIT_FINDINGS}; fi
  echo "validate_chart_structure --self-test: 5 cases passed"
  return ${EXIT_CLEAN}
}

main() {
  case "${1:-}" in
    -h|--help) usage; return ${EXIT_CLEAN} ;;
    --self-test) self_test; return $? ;;
    "") echo "validate_chart_structure: a chart directory is required" >&2; usage >&2; return ${EXIT_CANNOT_RUN} ;;
  esac
  if [[ $# -ne 1 ]]; then
    echo "validate_chart_structure: exactly one chart directory is required" >&2
    return ${EXIT_CANNOT_RUN}
  fi
  if [[ ! -d "$1" ]]; then
    echo "validate_chart_structure: not a directory: $1" >&2
    return ${EXIT_CANNOT_RUN}
  fi
  audit "$1"
  return $?
}

main "$@"
exit $?
