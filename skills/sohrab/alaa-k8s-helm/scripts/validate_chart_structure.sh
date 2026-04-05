#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <chart-directory>" >&2
  exit 1
fi

chart_dir="$1"
if [[ ! -d "$chart_dir" ]]; then
  echo "Directory not found: $chart_dir" >&2
  exit 1
fi

errors=()
warnings=()

say_ok() { echo "✅ $1"; }
say_warn() { echo "⚠️  $1"; }
say_err() { echo "❌ $1"; }

check_file() {
  local path="$1"
  local label="$2"
  if [[ -f "$path" ]]; then
    say_ok "$label"
  else
    say_err "$label missing"
    errors+=("$label missing")
  fi
}

echo "Validating Helm chart structure: $chart_dir"
echo

check_file "$chart_dir/Chart.yaml" "Chart.yaml"
check_file "$chart_dir/values.yaml" "values.yaml"

if [[ -d "$chart_dir/templates" ]]; then
  say_ok "templates/ directory"
else
  say_err "templates/ directory missing"
  errors+=("templates/ directory missing")
fi

if command -v yq >/dev/null 2>&1 && [[ -f "$chart_dir/Chart.yaml" ]]; then
  api_version="$(yq eval '.apiVersion' "$chart_dir/Chart.yaml" 2>/dev/null || true)"
  chart_type="$(yq eval '.type' "$chart_dir/Chart.yaml" 2>/dev/null || true)"
  name="$(yq eval '.name' "$chart_dir/Chart.yaml" 2>/dev/null || true)"
  version="$(yq eval '.version' "$chart_dir/Chart.yaml" 2>/dev/null || true)"
  [[ "$api_version" == "v2" ]] || warnings+=("Chart.yaml apiVersion should normally be v2")
  [[ -n "$name" && "$name" != "null" ]] || errors+=("Chart.yaml name missing")
  [[ -n "$version" && "$version" != "null" ]] || errors+=("Chart.yaml version missing")
  if [[ -n "$chart_type" && "$chart_type" != "null" && "$chart_type" != "application" && "$chart_type" != "library" ]]; then
    warnings+=("Chart.yaml type is unusual: $chart_type")
  fi
fi

for recommended in "$chart_dir/.helmignore" "$chart_dir/templates/_helpers.tpl" "$chart_dir/values.schema.json"; do
  if [[ -e "$recommended" ]]; then
    say_ok "$(basename "$recommended")"
  else
    say_warn "$(basename "$recommended") not found"
  fi
done

if [[ -d "$chart_dir/templates" ]]; then
  template_count="$(find "$chart_dir/templates" -type f \( -name '*.yaml' -o -name '*.tpl' -o -name '*.txt' \) | wc -l | tr -d ' ')"
  if [[ "$template_count" == "0" ]]; then
    warnings+=("templates/ has no YAML, TPL, or NOTES files")
  fi
fi

if [[ -f "$chart_dir/values.schema.json" ]] && command -v jq >/dev/null 2>&1; then
  if ! jq empty "$chart_dir/values.schema.json" >/dev/null 2>&1; then
    errors+=("values.schema.json is invalid JSON")
  fi
fi

if [[ -d "$chart_dir/crds" ]]; then
  say_ok "crds/ directory"
fi
if [[ -d "$chart_dir/charts" ]]; then
  say_ok "charts/ directory"
fi

echo
if ((${#errors[@]})); then
  echo "Blocking issues:"
  printf ' - %s
' "${errors[@]}"
fi
if ((${#warnings[@]})); then
  echo "Warnings:"
  printf ' - %s
' "${warnings[@]}"
fi

if ((${#errors[@]})); then
  exit 1
fi

echo "Chart structure validation complete."
