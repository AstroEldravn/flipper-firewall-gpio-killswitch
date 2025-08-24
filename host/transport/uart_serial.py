from __future__ import annotations
import platform, glob, logging, asyncio
from typing import Optional
import serial
from host.transport.base import BaseTransport
from host.config_loader import TransportConfig

log = logging.getLogger(__name__)

def _auto_ports():
    sysname = platform.system().lower()
    if sysname == "windows":
        return [f"COM{i}" for i in range(1, 257)]
    elif sysname == "darwin":
        return glob.glob("/dev/tty.*") + glob.glob("/dev/cu.*")
    else:
        return glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*") + glob.glob("/dev/tty.*")

class UARTTransport(BaseTransport):
    name = "uart_serial"

    def __init__(self, cfg: TransportConfig):
        self.cfg = cfg
        self.ser: Optional[serial.Serial] = None
        self._open()

    def _try_open(self, dev: str) -> Optional[serial.Serial]:
        try:
            s = serial.Serial(dev, 115200, timeout=0.1)
            return s
        except Exception:
            return None

    def _open(self):
        device = self.cfg.device or "auto"
        if device == "auto":
            for cand in _auto_ports():
                ser = self._try_open(cand)
                if ser:
                    log.info("uart: using %s", cand)
                    self.ser = ser
                    break
        else:
            self.ser = self._try_open(device)
        if not self.ser:
            raise RuntimeError("No serial device available (set transport.device)")

    async def set_state(self, high: bool):
        if not self.ser:
            raise RuntimeError("serial not open")
        line = (self.cfg.line or "rts").lower()
        if line == "dtr":
            self.ser.dtr = bool(high)
        else:
            self.ser.rts = bool(high)
        # Give the line a moment to settle
        await asyncio.sleep(0.01)

    async def close(self):
        if self.ser:
            try:
                self.ser.close()
            except Exception:
                pass
            self.ser = None
