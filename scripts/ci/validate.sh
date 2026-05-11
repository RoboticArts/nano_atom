#!/bin/bash

set -euo pipefail

# Run scripts form this script path
SCRIPT_DIR="$(realpath "$(dirname "$0")/../../modules")"
echo $SCRIPT_DIR
pushd "$SCRIPT_DIR" > /dev/null

if ! command -v licensecheck &> /dev/null; then
  echo "❌ FAILED: licensecheck is not installed"
  exit 1
fi

EXCLUDED_PACKAGES=(
  "camera_ros"
)

FIND_ARGS=(
  -name '*launch.py'
)

for pkg in "${EXCLUDED_PACKAGES[@]}"; do
  FIND_ARGS+=(-not -path "*/${pkg}/*")
done

# if ament_copyright --verbose; then
if ! licensecheck --machine --copyright $(find . "${FIND_ARGS[@]}") | grep -E "UNKNOWN|No copyright"; then
  echo "✅ PASSED: Launch copyright"
  exit_code=0
else
  echo "❌ FAILED: Launch copyright"
  exit_code=1
fi

popd > /dev/null

exit $exit_code