#!/bin/bash

set -euo pipefail

# Run scripts form this script path
SCRIPT_DIR="$(realpath "$(dirname "$0")/../../modules")"
echo $SCRIPT_DIR
pushd "$SCRIPT_DIR" > /dev/null

# if ament_copyright --verbose; then
if ! licensecheck --machine --copyright $(find . -name '*launch.py') | grep -E "UNKNOWN|No copyright"; then
  echo "✅ PASSED: Launch copyright"
  exit_code=0
else
  echo "❌ FAILED: Launch copyright"
  exit_code=1
fi

popd > /dev/null

exit $exit_code