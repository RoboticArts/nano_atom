#!/bin/bash

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

print_error()   { echo -e "${RED}$1${NC}"; }
print_success() { echo -e "${GREEN}$1${NC}"; }
print_info()    { echo -e "${BLUE}$1${NC}"; }

find_ws_root() {
  local dir="$(pwd)"
  while [ "$dir" != "/" ]; do
    if [ -d "$dir/install" ]; then
      echo "$dir"
      return
    fi
    dir="$(dirname "$dir")"
  done
  echo "Workspace not found" >&2
  exit 1
}

WS_ROOT="$(find_ws_root)"
echo ${WS_ROOT}
pushd "$WS_ROOT"

# Add packages to test
packages_list=(
  nano_atom_integration_tests
)

packages_result=()

# Build workspace
colcon build --symlink-install --cmake-args -DBUILD_TESTING=ON

# Test packages from the list
for package in "${packages_list[@]}"; do
  cd "build/${package}"
  set +e
  ctest --output-on-failure -T Test --no-compress-output -V
  rc=$?
  set -e
  packages_result+=($rc)
  cd -
done

# Print results
printf "TEST SUMMARY"
printf "\n%-30s | %-15s\n" "Package" "Result"
printf -- "--------------------------------+-----------------\n"

exit_code=0
for i in "${!packages_list[@]}"; do
  if [ "${packages_result[$i]}" -eq 0 ]; then
    printf "%-30s | " "${packages_list[$i]}"
    print_success "PASSED"
  else
    printf "%-30s | " "${packages_list[$i]}"
    print_error "FAILED (code ${packages_result[$i]})"
    exit_code="${packages_result[$i]}"
    exit $exit_code
  fi
done

popd > /dev/null

exit $exit_code