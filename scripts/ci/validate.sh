#!/bin/bash

set -euo pipefail

# Run scripts form this script path
SCRIPT_DIR="$(realpath "$(dirname "$0")/../../src")"
echo $SCRIPT_DIR
pushd "$SCRIPT_DIR" > /dev/null

if ament_copyright --verbose; then
  echo "✅ PASSED: Copyright"
  exit_code=0
else
  echo "❌ FAILED: Copyright"
  exit_code=1
fi

popd > /dev/null

exit $exit_code