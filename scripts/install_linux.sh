#!/usr/bin/env bash
set -euo pipefail

echo "[*] Installing Python dependencies..."
if ! command -v python3 >/dev/null 2>&1; then
  echo "[-] python3 not found; please install Python 3.9+ and re-run."
  exit 1
fi

python3 -m pip install --upgrade pip
python3 -m pip install -r host/requirements.txt

echo "[*] (Optional) Setting up udev for USB-UART (if present)..."
if [ -d "/etc/udev/rules.d" ]; then
  sudo cp -f scripts/udev/99-gpio-killswitch.rules /etc/udev/rules.d/ || true
  sudo udevadm control --reload-rules || true
  sudo udevadm trigger || true
fi

echo "[*] Verifying environment..."
python3 scripts/helpers/verify_env.py || true

echo "[+] Linux setup complete."
