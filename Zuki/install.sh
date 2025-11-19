#!/bin/bash
set -e

# Local, offline-friendly setup for Raspberry Pi
# This script assumes you've copied/unzipped the project already.

echo "=== Zuki local setup (offline-friendly) ==="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "Project root: ${PROJECT_ROOT}"

echo
echo "1) Checking for Python 3..."
if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 not found. Please install Python 3."
  exit 1
fi

echo
echo "2) Checking for Tkinter (python3-tk)..."
if python3 -c "import tkinter" >/dev/null 2>&1; then
  echo "Tkinter OK."
else
  echo "Warning: Tkinter not found."
  echo "If on Raspberry Pi OS: sudo apt-get install -y python3-tk"
fi

echo
echo "3) Checking for espeak (optional TTS)..."
if command -v espeak >/dev/null 2>&1; then
  echo "espeak OK."
else
  echo "Note: 'espeak' not found. To enable TTS: sudo apt-get install -y espeak-ng"
fi

echo
echo "Setup complete."
echo "To start the tiny offline chat UI:"
echo "  cd \"${PROJECT_ROOT}\""
echo "  python3 pi_start.py"
echo
echo "Tip: For auto-start on boot later, you can create a systemd service pointing to pi_start.py."