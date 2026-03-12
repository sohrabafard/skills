#!/usr/bin/env bash
set -euo pipefail

# Deterministic Helm render wrapper for Arvan-safe validation.
#
# Usage:
#   bash render-helm.sh <chart_dir> [namespace] [values.yaml] [values.secret.yaml] [out.yaml] [extra-values...]
#
# Examples:
#   bash render-helm.sh ./helm/app vk
#   bash render-helm.sh ./helm/app vk values.yaml values.secret.yaml rendered.yaml values.prod.yaml
#
# Notes:
# - The layering order is:
#     base values -> extra values (left to right) -> secret values
# - This script never prints secret file contents.

CHART_DIR="${1:-}"
NS="${2:-default}"
VALUES_FILE="${3:-values.yaml}"
SECRETS_FILE="${4:-values.secret.yaml}"
OUT="${5:-/tmp/rendered.yaml}"
shift $(( $# > 5 ? 5 : $# ))
EXTRA_VALUES=("$@")

RELEASE_NAME="${HELM_RELEASE_NAME:-arvan-preview}"

die() {
  echo "ERROR: $*" >&2
  exit 1
}

if [[ -z "${CHART_DIR}" || "${CHART_DIR}" == "-h" || "${CHART_DIR}" == "--help" ]]; then
  cat <<'EOF'
Usage:
  bash render-helm.sh <chart_dir> [namespace] [values.yaml] [values.secret.yaml] [out.yaml] [extra-values...]

Environment:
  HELM_RELEASE_NAME   Optional release name used for 'helm template' (default: arvan-preview)
EOF
  exit 1
fi

command -v helm >/dev/null 2>&1 || die "helm not found in PATH"
[[ -d "${CHART_DIR}" ]] || die "chart dir not found: ${CHART_DIR}"
[[ -f "${CHART_DIR}/Chart.yaml" ]] || die "missing Chart.yaml in chart dir: ${CHART_DIR}"
[[ -f "${VALUES_FILE}" ]] || die "values file not found: ${VALUES_FILE}"
[[ -f "${SECRETS_FILE}" ]] || die "secret values file not found: ${SECRETS_FILE}"

for f in "${EXTRA_VALUES[@]}"; do
  [[ -f "${f}" ]] || die "extra values file not found: ${f}"
done

mkdir -p "$(dirname "${OUT}")"

VALUES_ARGS=(-f "${VALUES_FILE}")
for f in "${EXTRA_VALUES[@]}"; do
  VALUES_ARGS+=(-f "${f}")
done
VALUES_ARGS+=(-f "${SECRETS_FILE}")

echo "== helm dependency build"
helm dependency build "${CHART_DIR}" >/dev/null

echo "== helm lint"
helm lint "${CHART_DIR}" "${VALUES_ARGS[@]}"

echo "== helm template -> ${OUT}"
helm template "${RELEASE_NAME}" "${CHART_DIR}" -n "${NS}" "${VALUES_ARGS[@]}" > "${OUT}"

echo "Rendered manifests written to: ${OUT}"
echo "Values layering:"
echo "  1) ${VALUES_FILE}"
if [[ "${#EXTRA_VALUES[@]}" -gt 0 ]]; then
  idx=2
  for f in "${EXTRA_VALUES[@]}"; do
    echo "  ${idx}) ${f}"
    idx=$((idx + 1))
  done
  echo "  ${idx}) ${SECRETS_FILE} (applied last)"
else
  echo "  2) ${SECRETS_FILE} (applied last)"
fi
