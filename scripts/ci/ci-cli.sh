#!/bin/bash

# Start a new process group so that all children share it
set -euo pipefail

# Trap Ctrl+C and kill all subprocesses
trap 'echo -e "\n\033[1;31mInterrupted by user. Exiting.\033[0m"; pkill -P $$; exit 130' SIGINT

# Run scripts form this script path
SCRIPT_DIR="$(realpath "$(dirname "$0")")"
pushd "$SCRIPT_DIR" > /dev/null

show_help() {
    echo "Usage: $0 --version <version> [--command <command>]"
    echo
    echo "Required arguments:"
    echo "  --version   Version to use"
    echo
    echo "Optional arguments:"
    echo "  --command  Valid values: all (default), preflight, validate, build, test, package"
    echo
    echo "Example:"
    echo "  $0 --version 1.2.3 --command build"
}

# Initialize variables
VERSION=""
COMMAND="all"

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --version)
            if [[ -n "$2" && "$2" != --* ]]; then
                VERSION="$2"
                shift 2
            else
                echo "Error: --version requires a value."
                exit 1
            fi
            ;;
        --command)
            if [[ -n "$2" && "$2" != --* ]]; then
                case "$2" in
                    preflight|validate|build|test|package|upload|all)
                        COMMAND="$2"
                        ;;
                    *)
                        echo "Error: Invalid command '$2'. Valid commands are: validate, build, package, all."
                        exit 1
                        ;;
                esac
                shift 2
            else
                echo "Error: --command requires a value."
                exit 1
            fi
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo "Error: Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

echo "Version: $VERSION"
echo "Command: $COMMAND"

preflight() {

  ./preflight.sh

}

validate() {

  ./validate.sh

}

build() {

  ./build.sh roboticarts/nano-atom:${VERSION}

}

test() {

  IMAGE="roboticarts/nano-atom:${VERSION}"

  if docker image inspect "$IMAGE" >/dev/null 2>&1; then
    echo "Docker image found. Running tests on "$IMAGE" image"
    docker run --rm "$IMAGE" ./src/nano_atom/scripts/ci/test.sh 
  else
    echo "Running tests locally"
    ./test.sh
  fi

}

upload() {

  ./upload.sh roboticarts/nano-atom:${VERSION}

}

main() {
  case "$COMMAND" in
    preflight)
      preflight
      ;;
    validate)
      validate
      ;;
    build)
      build
      ;;
    test)
      test
      ;;
    upload)
      upload
      ;;
    all)
      preflight
      validate
      build
      test
      upload
      echo "Success!"
      ;;
    *)
      echo "Usage: $0 {preflight|validate|build|test|upload|all}"
      exit 1
      ;;
  esac
}

main "$@"

popd > /dev/null