from __future__ import annotations
from host.transport.base import BaseTransport
from host.config_loader import TransportConfig

class DryRunTransport(BaseTransport):
    name = "dryrun"

    def __init__(self, cfg: TransportConfig):
        self.state = False

    async def set_state(self, high: bool):
        self.state = high

    async def close(self):
        return None
