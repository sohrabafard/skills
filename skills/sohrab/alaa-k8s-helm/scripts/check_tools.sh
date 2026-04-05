#!/usr/bin/env bash
set -euo pipefail

lane="${1:-all}"
case "$lane" in
  all|yaml|helm|debug) ;;
  *)
    echo "Usage: $0 [all|yaml|helm|debug]" >&2
    exit 1
    ;;
esac

have() { command -v "$1" >/dev/null 2>&1; }

kube_cli=""
if have oc; then
  kube_cli="oc"
elif have kubectl; then
  kube_cli="kubectl"
fi

required=()
optional=(jq yq stern k9s kubectl-neat)

case "$lane" in
  yaml)
    required=(yamllint kubeconform)
    ;;
  helm)
    required=(helm yamllint kubeconform)
    optional+=(helm-diff)
    ;;
  debug)
    required=()
    ;;
  all)
    required=(yamllint kubeconform)
    optional+=(helm helm-diff)
    ;;
esac

if [[ -n "$kube_cli" ]]; then
  echo "✅ Kubernetes CLI: $kube_cli"
  if [[ "$kube_cli" == "oc" ]]; then
    oc version --client 2>/dev/null | sed 's/^/   /' || true
  else
    kubectl version --client 2>/dev/null | sed 's/^/   /' || true
  fi
else
  echo "⚠️  No Kubernetes CLI found (kubectl or oc)"
fi

echo
missing=()
for tool in "${required[@]}"; do
  if have "$tool"; then
    echo "✅ $tool"
    case "$tool" in
      helm) helm version 2>/dev/null | head -n 1 | sed 's/^/   /' || true ;;
      yamllint) yamllint --version 2>/dev/null | sed 's/^/   /' || true ;;
      kubeconform) kubeconform -v 2>/dev/null | sed 's/^/   /' || true ;;
    esac
  else
    echo "❌ $tool (required for lane: $lane)"
    missing+=("$tool")
  fi
done

echo
for tool in "${optional[@]}"; do
  if [[ "$tool" == "helm-diff" ]]; then
    if have helm && helm plugin list 2>/dev/null | awk '{print $1}' | grep -qx diff; then
      echo "✅ helm-diff"
    else
      echo "⚠️  helm-diff not found"
    fi
    continue
  fi

  if have "$tool"; then
    echo "✅ $tool"
  else
    echo "⚠️  $tool not found"
  fi
done

echo
if ((${#missing[@]})); then
  echo "Missing required tools: ${missing[*]}" >&2
  exit 1
fi

echo "Tool check complete."
