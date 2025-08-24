from __future__ import annotations
import asyncio, logging, os, re, time
import socket
from typing import Optional
import requests

from host.config_loader import Policy
from host.gpio_driver import GPIODriver
from host.alert_manager import AlertManager

log = logging.getLogger(__name__)

class FirewallListener:
    def __init__(self, policy: Policy, driver: GPIODriver, alerts: AlertManager):
        self.policy = policy
        self.driver = driver
        self.alerts = alerts
        self.state: Optional[bool] = None  # last applied

    async def run(self):
        log.info("Starting rules engine with %d trigger(s)...", len(self.policy.triggers))
        try:
            while True:
                matched = None
                for trig in self.policy.triggers:
                    if trig.type == "file_exists":
                        if os.path.exists(trig.path):
                            matched = (trig.name, trig.action)
                            break
                    elif trig.type == "timer":
                        # naive timer: fires once after N seconds since program start
                        # (for demo/auto-clear; real systems should store state externally)
                        if time.monotonic() > getattr(trig, "_deadline", time.monotonic()+trig.seconds):
                            setattr(trig, "_deadline", time.monotonic()+10**9)  # never again
                            matched = (trig.name, trig.action)
                            break
                    elif trig.type == "log_regex":
                        # tail-like: read from last position
                        path = trig.path
                        regex = re.compile(trig.regex)
                        pos = getattr(trig, "_pos", 0)
                        try:
                            with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                                fh.seek(pos)
                                for line in fh:
                                    if regex.search(line):
                                        matched = (trig.name, trig.action)
                                        break
                                setattr(trig, "_pos", fh.tell())
                        except FileNotFoundError:
                            pass
                        if matched:
                            break
                    elif trig.type == "http_probe":
                        if time.monotonic() >= getattr(trig, "_next", 0):
                            setattr(trig, "_next", time.monotonic() + trig.interval)
                            try:
                                r = requests.get(trig.url, timeout=2)
                                ok = (trig.expect_status is None or r.status_code == trig.expect_status)
                                if ok and trig.contains:
                                    ok = trig.contains in r.text
                                if ok:
                                    matched = (trig.name, trig.action)
                                    break
                            except Exception:
                                # treat failure as not matched
                                pass

                target_state = self.policy.default_kill_state
                if matched:
                    name, action = matched
                    target_state = (action == "kill_on")
                    log.info("trigger=%s matched → %s", name, "KILL ON" if target_state else "KILL OFF")
                    await self.alerts.notify("Trigger matched", f"{name} → {action}")

                if self.state is None or target_state != self.state:
                    await self.driver.set_kill(target_state)
                    self.state = target_state

                await asyncio.sleep(max(0.05, self.policy.debounce_ms / 1000))
        finally:
            await self.driver.close()
