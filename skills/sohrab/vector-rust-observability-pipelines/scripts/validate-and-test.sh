
#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <vector-config-file> [more config/test files...]"
  exit 1
fi

echo "==> vector validate $*"
vector validate "$@"

echo "==> vector test $*"
vector test "$@"
