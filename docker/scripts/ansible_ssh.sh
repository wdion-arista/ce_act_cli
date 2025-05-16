#!/bin/bash

# Usage: ansible_ssh.sh BLUE RED PURPLE

if ! command -v yq >/dev/null 2>&1; then
    echo "Error: 'yq' is not installed or not in your PATH."
    echo "Please install yq (https://github.com/mikefarah/yq) before running this script."
    echo "Please install yq MacOS sudo brew install yq"
    exit 1
fi

INVENTORY=inventory.yml

# Combine all input patterns into a single regex (case-insensitive)
PATTERN=$(printf "|%s" "$@" | cut -c2-)
PATTERN="(${PATTERN})"

# Extract all hostnames and their IPs from the inventory using yq v4
yq '
  .. | select(has("hosts")) | .hosts |
  to_entries[] | [.key, .value.ansible_host] | @tsv
' "$INVENTORY" |
# Filter hostnames that match any of the input patterns (case-insensitive)
awk -v pat="$PATTERN" 'BEGIN{IGNORECASE=1} $1 ~ pat {print $2}' |
# Remove empty lines and deduplicate
grep -v '^$' | sort -u > /tmp/ssh_hosts.txt

# If no hosts found, exit
if [ ! -s /tmp/ssh_hosts.txt ]; then
  echo "No matching hosts found for pattern: $PATTERN"
  exit 1
fi

# Use xpanes to SSH to each host in parallel
xpanes --ssh  $(cat /tmp/ssh_hosts.txt)
