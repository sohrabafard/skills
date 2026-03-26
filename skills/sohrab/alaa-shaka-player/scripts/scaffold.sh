#!/usr/bin/env bash
set -euo pipefail

# Copies the starter templates into a target directory.
# Example:
#   ./scripts/scaffold.sh ./src/components/player

TARGET_DIR="${1:-}"

if [[ -z "$TARGET_DIR" ]]; then
  echo "Usage: $0 <target-directory>"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$(cd "${SCRIPT_DIR}/../assets/templates" && pwd)"

mkdir -p "$TARGET_DIR"

cp "${TEMPLATES_DIR}/ShakaPlayer.vue" "${TARGET_DIR}/ShakaPlayer.vue"
cp "${TEMPLATES_DIR}/useShakaCore.ts" "${TARGET_DIR}/useShakaCore.ts"

echo "Copied core templates into: ${TARGET_DIR}"
echo "Copy the services folder and PlayerLab template manually if needed."
