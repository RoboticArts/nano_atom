#!/bin/bash

set -e

# Check if image reference name is provided
if [ -z "$1" ]; then
  echo "Image reference name is required"
  echo "Usage: $0 <image_reference>"
  echo "Example: roboticarts/nano-atom:dev"
  exit 1
fi

image_reference="$1"

# From repository root
pushd "$(dirname "$0")/../.." > /dev/null

docker build -t ${image_reference} -f docker/Dockerfile .

# Continue in the original path
popd > /dev/null
