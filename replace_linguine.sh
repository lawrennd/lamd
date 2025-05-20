#!/bin/bash
# This script replaces all occurrences of 'linguine' with 'lynguine' in *.py files on macOS

for file in *.py; do
  sed -i '' 's/linguine/lynguine/g' "$file"
done
for file in */*.py; do
  sed -i '' 's/linguine/lynguine/g' "$file"
done
