#!/usr/bin/env bash
# Pure PHP+shell, no jq/Python/Node dependency. Called by Claude PostToolUse.
set -euo pipefail
[[ "${ALAA_PHPANTOM_LINT:-1}" != "0" ]] || exit 0
command -v php >/dev/null 2>&1 || exit 0
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
exec php "$SCRIPT_DIR/post-edit-lint.php"
