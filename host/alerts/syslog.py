from __future__ import annotations
import asyncio, logging
from logging.handlers import SysLogHandler

class SyslogAlert:
    def __init__(self, address: str | None = None):
        self.logger = logging.getLogger("killswitch-syslog")
        handler = SysLogHandler(address=address or "/dev/log")
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    async def send(self, title: str, message: str):
        self.logger.info("%s - %s", title, message)
        await asyncio.sleep(0)
