
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

if [[ -n "${DOCKERHUB_TOKEN:-}" && -n "${DOCKERHUB_USER:-}" ]]; then
    echo "Using DOCKERHUB_TOKEN and DOCKERHUB_USER from environment."
    echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USER" --password-stdin
else
  # Prompt the user without echoing
    echo "DOCKERHUB_TOKEN and DOCKERHUB_USER environment variables not defined."
    read -p "DockerHub Username: " DOCKERHUB_USER
    read -s -p "DockerHub Token/Password: " DOCKERHUB_TOKEN
    echo
    echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USER" --password-stdin
fi

docker push ${image_reference}