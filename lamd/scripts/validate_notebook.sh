#!/bin/bash

# Dependencies: python3, jq (optional but recommended)

# This script validates that Jupyter notebooks have sufficient cell structure.
# Usage: validate_notebook.sh <notebook_file> [expected_min_cells]

# Enable error handling
set -e
trap 'echo "Error on line $LINENO: $BASH_COMMAND"' ERR

# Parse command line arguments
if [ "$#" -lt 1 ]; then
    echo "Error: Incorrect number of arguments"
    echo "Usage: $0 <notebook_file> [expected_min_cells]"
    exit 1
fi

notebook_file=$1
expected_min=${2:-1}  # Default to 1 if not specified

# Check if notebook file exists
if [ ! -f "$notebook_file" ]; then
    echo "ERROR: Notebook file $notebook_file does not exist" >&2
    exit 1
fi

# Function to count cells using Python
count_cells_python() {
    python3 -c "
import json
import sys
try:
    with open('$notebook_file', 'r') as f:
        notebook = json.load(f)
    cell_count = len(notebook.get('cells', []))
    print(cell_count)
except Exception as e:
    print(f'ERROR: Failed to read notebook: {e}', file=sys.stderr)
    sys.exit(1)
"
}

# Function to count cells using jq (if available)
count_cells_jq() {
    if command -v jq &> /dev/null; then
        jq '.cells | length' "$notebook_file" 2>/dev/null || echo "0"
    else
        echo "0"
    fi
}

# Try to count cells
if command -v jq &> /dev/null; then
    cell_count=$(count_cells_jq)
    if [ "$cell_count" = "0" ] || [ "$cell_count" = "null" ]; then
        cell_count=$(count_cells_python)
    fi
else
    cell_count=$(count_cells_python)
fi

# Validate cell count
if [ "$cell_count" -ge "$expected_min" ]; then
    echo "✅ $notebook_file: $cell_count cells (>= $expected_min)"
    exit 0
else
    echo "❌ $notebook_file: $cell_count cells (expected >= $expected_min)" >&2
    exit 1
fi
