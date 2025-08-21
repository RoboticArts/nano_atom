
# docker push roboticarts/nano-atom:tagname

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

if [[ -n "${CI_DOCKERHUB_TOKEN:-}" && -n "${CI_DOCKERHUB_USER:-}" ]]; then
    echo "Using CI_DOCKERHUB_TOKEN and CI_DOCKERHUB_USER from environment."
    echo "$CI_DOCKERHUB_TOKEN" | docker login -u "$CI_DOCKERHUB_USER" --password-stdin
else
  # Prompt the user without echoing
    read -p "DockerHub Username: " DOCKERHUB_USER
    read -s -p "DockerHub Token/Password: " DOCKERHUB_TOKEN
    echo
    echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USER" --password-stdin
fi

docker push ${image_reference}