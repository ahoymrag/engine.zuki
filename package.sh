#!/bin/bash
set -e

# Create a portable zip excluding virtual envs, caches, and VCS metadata

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ZIP_NAME="engine.zuki.zip"

cd "${PROJECT_ROOT}"

echo "Creating ${ZIP_NAME}..."
zip -r "${ZIP_NAME}" . \
  -x "*/__pycache__/*" \
  -x ".git/*" \
  -x ".zuki/*" \
  -x "*.zip"

echo "Done. Zip located at: ${PROJECT_ROOT}/${ZIP_NAME}"


