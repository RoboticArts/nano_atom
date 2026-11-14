#!/bin/bash

# Load YAML and flatten its hierarchical structure.
# Example: robot.devices.laser.id=front_laser
load_yaml() {
    local file="$1"

    yq -r '
        paths(type != "object" and type != "array") as $path |
        ($path | join(".")) + "=" + (getpath($path) | tostring)
    ' "$file"
}


# Extract raw name and value from a flattened YAML entry.
get_name_value_raw() {
    local line="$1"
    local -n name_out="$2"
    local -n value_out="$3"

    # Everything before the first "=" is the parameter name.
    name_out="${line%%=*}"

    # Everything after the first "=" is the parameter value.
    value_out="${line#*=}"
}


# Convert a YAML parameter name into an environment variable name.
resolve_name() {
    local name="$1"

    # Replace hierarchy separators "." with underscores "_".
    # Example: robot.devices.laser.id -> robot_devices_laser_id
    name="${name//./_}"

    # Convert all characters to uppercase.
    # Example: robot_devices_laser_id -> ROBOT_DEVICES_LASER_ID
    name="${name^^}"

    # Return the resolved parameter name.
    printf '%s' "$name"
}


# Resolve a YAML parameter value.
resolve_value() {
    local value="$1"
    local yaml="$2"
    local placeholder reference entry replacement

    # Preserve the original value unless a reference is detected.
    # References must use absolute paths from the YAML root.
    # References follow the format ${path.to.parameter}.
    # Example: ${robot.devices.laser.id}/scan
    while [[ "$value" =~ \$\{([a-zA-Z0-9_.]+)\} ]]; do

        # Extract the complete reference placeholder.
        # Example: ${robot.devices.laser.id}
        placeholder="${BASH_REMATCH[0]}"

        # Extract the referenced YAML parameter path.
        # Example: robot.devices.laser.id
        reference="${BASH_REMATCH[1]}"

        # Find the referenced parameter in the flattened YAML.
        # Example: robot.devices.laser.id=front_laser
        entry=$(awk -F= -v key="$reference" \
            '$1 == key {print; exit}' <<< "$yaml")

        # Return an error if the referenced parameter does not exist.
        if [[ -z "$entry" ]]; then
            echo "Unknown YAML reference: $reference" >&2
            return 1
        fi

        # Extract the value of the referenced parameter.
        # Example: front_laser
        replacement="${entry#*=}"

        # Reject references pointing to values containing other references.
        # Nested and circular references are not supported.
        if [[ "$replacement" == *'${'* ]]; then
            echo "Nested YAML reference not supported: $reference" >&2
            return 1
        fi

        # Replace the placeholder with the referenced value.
        # Example: ${robot.devices.laser.id}/scan -> front_laser/scan
        value="${value//"$placeholder"/"$replacement"}"

        # Repeat until all references in the value have been resolved.
    done

    # Return the resolved value, or the original value if no references exist.
    printf '%s' "$value"
}


# Main
main() {
    local yaml line
    local raw_name raw_value
    local name value

    # This script must be sourced to modify the current shell environment.
    if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
        echo "Error: This script must be executed using source." >&2
        echo "Usage: source yaml_to_env.sh <yaml_file>" >&2
        exit 1
    fi

    # Check that a YAML file has been provided.
    if [[ -z "$1" ]]; then
        echo "Error: No YAML file provided." >&2
        echo "Usage: source yaml_to_env.sh <yaml_file>" >&2
        return 1
    fi

    # Load YAML configuration.
    yaml=$(load_yaml "$1") || return 1

    # Create a temporary environment configuration file.
    env_file=$(mktemp /tmp/robot_params_XXXXXX.env) || return 1

    # Iterate over each YAML parameter.
    while IFS= read -r line; do

        [[ -z "$line" ]] && continue

        get_name_value_raw "$line" raw_name raw_value

        name=$(resolve_name "$raw_name")
        value=$(resolve_value "$raw_value" "$yaml") || return 1

        # Write the resolved parameter as a Bash export statement.
        printf 'export %s=%q\n' "$name" "$value" >> "$env_file" || return 1

    done <<< "$yaml"

    # Load the resolved configuration into the current environment.
    source "$env_file" || return 1

    # Report the location of the resolved configuration.
    echo "Environment configuration loaded from: $env_file"
}


main "$1"