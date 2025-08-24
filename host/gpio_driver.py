from __future__ import annotations
import logging
from host.transport.base import BaseTransport
from host.transport.dryrun import DryRunTransport
from host.transport.uart_serial import UARTTransport
from host.transport.gpio_local import GPIOLocalTransport
from host.config_loader import TransportConfig

log = logging.getLogger(__name__)

class GPIODriver:
    def __init__(self, cfg: TransportConfig):
        self.cfg = cfg
        self.transport: BaseTransport
        if cfg.type == "uart_serial":
            self.transport = UARTTransport(cfg)
        elif cfg.type == "gpio_local":
            self.transport = GPIOLocalTransport(cfg)
        else:
            self.transport = DryRunTransport(cfg)

    async def set_kill(self, state: bool):
        state = not state if self.cfg.invert_logic else state
        await self.transport.set_state(state)
        log.info("transport=%s state=%s", self.transport.name, state)

    async def close(self):
        await self.transport.close()
