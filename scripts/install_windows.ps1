#requires -version 5
$ErrorActionPreference = "Stop"

Write-Host "[*] Checking Python..."
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  Write-Host "[-] Python not found. Install Python 3.9+ from https://www.python.org/downloads/ and re-run."
  exit 1
}

Write-Host "[*] Installing deps..."
python -m pip install --upgrade pip
python -m pip install -r host/requirements.txt

Write-Host "[*] Verifying environment..."
python scripts\helpers\verify_env.py

Write-Host "[+] Windows setup complete."
