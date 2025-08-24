from __future__ import annotations
import logging, asyncio, os
from host.transport.base import BaseTransport
from host.config_loader import TransportConfig

log = logging.getLogger(__name__)

class _GPIOD:
    def __init__(self, chip: str, line_offset: int):
        import gpiod  # type: ignore
        self.chip = gpiod.Chip(chip)
        self.line = self.chip.get_line(line_offset)
        self.line.request(consumer="gpio-killswitch", type=gpiod.LINE_REQ_DIR_OUT)

    def set(self, high: bool):
        self.line.set_value(1 if high else 0)

    def close(self):
        try:
            self.line.release()
        except Exception:
            pass
        try:
            self.chip.close()
        except Exception:
            pass

class _RPiGPIO:
    def __init__(self, bcm_pin: int):
        import RPi.GPIO as GPIO  # type: ignore
        self.GPIO = GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(bcm_pin, GPIO.OUT, initial=GPIO.LOW)
        self.pin = bcm_pin

    def set(self, high: bool):
        self.GPIO.output(self.pin, self.GPIO.HIGH if high else self.GPIO.LOW)

    def close(self):
        try:
            self.GPIO.cleanup(self.pin)
        except Exception:
            pass

class GPIOLocalTransport(BaseTransport):
    name = "gpio_local"

    def __init__(self, cfg: TransportConfig):
        self.cfg = cfg
        self.backend = None
        # Prefer gpiod if available and chip/line set
        if cfg.chip and cfg.line_offset is not None:
            try:
                self.backend = _GPIOD(cfg.chip, int(cfg.line_offset))
                log.info("gpio_local: using gpiod %s line %s", cfg.chip, cfg.line_offset)
            except Exception as e:
                log.warning("gpiod init failed: %s, trying RPi.GPIO", e)

        if self.backend is None:
            # Try RPi.GPIO with BCM pin number
            if cfg.line_offset is None:
                raise RuntimeError("gpio_local requires line_offset (BCM pin) or gpiod chip+line_offset")
            try:
                self.backend = _RPiGPIO(int(cfg.line_offset))
                log.info("gpio_local: using RPi.GPIO on BCM %s", cfg.line_offset)
            except Exception as e:
                raise RuntimeError(f"RPi.GPIO init failed: {e}")

    async def set_state(self, high: bool):
        self.backend.set(bool(high))
        await asyncio.sleep(0)

    async def close(self):
        try:
            self.backend.close()
        except Exception:
            pass
