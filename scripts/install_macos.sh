#!/usr/bin/env bash
set -euo pipefail

echo "[*] Installing Python dependencies..."
if ! command -v python3 >/dev/null 2>&1; then
  echo "[-] python3 not found; install via Homebrew: brew install python"
  exit 1
fi

python3 -m pip install --upgrade pip
python3 -m pip install -r host/requirements.txt

echo "[*] Note: macOS has no native GPIO; use uart_serial or dryrun."
python3 scripts/helpers/verify_env.py || true

echo "[+] macOS setup complete."
