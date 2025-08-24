import argparse
import asyncio
import logging
from host.config_loader import load_config
from host.gpio_driver import GPIODriver
from host.alert_manager import AlertManager
from host.firewall_listener import FirewallListener
from host.utils import setup_logging

def parse_args():
    ap = argparse.ArgumentParser(description="GPIO Killswitch Host")
    ap.add_argument("--config", default="host/config/example.yaml", help="Path to YAML config")
    ap.add_argument("--verbose", action="store_true", help="Enable debug logging")
    return ap.parse_args()

async def amain():
    args = parse_args()
    setup_logging(logging.DEBUG if args.verbose else logging.INFO)

    cfg = load_config(args.config)
    driver = GPIODriver(cfg.transport)
    alerts = AlertManager(cfg.alerts)

    listener = FirewallListener(cfg.policy, driver, alerts)
    await listener.run()

def main():
    try:
        asyncio.run(amain())
    except KeyboardInterrupt:
        print("\n[!] Exiting on Ctrl+C.")

if __name__ == "__main__":
    main()
