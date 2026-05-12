#!/bin/bash

set -euo pipefail

# Run scripts form this script path
SCRIPT_DIR="$(realpath "$(dirname "$0")/../..")"
echo $SCRIPT_DIR
pushd "$SCRIPT_DIR" > /dev/null

required=(
  "scripts/ci"
  "modules/tests"
  "docker/Dockerfile"
  "docker/docker-compose.yaml"
)

missing=0
for path in "${required[@]}"; do
  if [[ -e "$path" ]]; then
      echo -e "✅ FOUND: $path"
  else
      echo -e "❌ MISSING: $path"
      missing=1
  fi
done

if (( missing == 1 )); then
  echo "Error: Required structure is missing. Check repository structure"
  exit_code=1
  else
  echo "All required files and directories exist."
  exit_code=0
fi

popd > /dev/null

exit $exit_code