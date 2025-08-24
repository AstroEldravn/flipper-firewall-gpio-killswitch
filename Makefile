.PHONY: help setup setup-linux setup-macos setup-windows lint test run format check zip

help:
	@echo "Common targets:"
	@echo "  make setup           - Install deps on your OS"
	@echo "  make lint            - Run ruff"
	@echo "  make test            - Run pytest"
	@echo "  make run             - Run demo with example config"
	@echo "  make zip             - Zip the repo for sharing"

setup:
	@./scripts/install_linux.sh || true
	@./scripts/install_macos.sh || true
	@powershell -ExecutionPolicy Bypass -File scripts/install_windows.ps1 || true

setup-linux:
	bash scripts/install_linux.sh

setup-macos:
	bash scripts/install_macos.sh

setup-windows:
	powershell -ExecutionPolicy Bypass -File scripts/install_windows.ps1

lint:
	python -m pip install -r host/requirements.txt
	python -m pip install ruff
	ruff check host

format:
	python -m pip install ruff
	ruff format host

test:
	python -m pip install -r host/requirements.txt
	python -m pip install pytest
	pytest -q

run:
	python -m host.main --config host/config/example.yaml

zip:
	@cd .. && zip -r flipper-firewall-gpio-killswitch.zip flipper-firewall-gpio-killswitch >/dev/null && echo "Created ../flipper-firewall-gpio-killswitch.zip"
