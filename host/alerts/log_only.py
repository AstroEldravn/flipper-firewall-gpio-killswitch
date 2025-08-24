from __future__ import annotations
import logging, asyncio

log = logging.getLogger(__name__)

class LogOnlyAlert:
    async def send(self, title: str, message: str):
        log.info("[ALERT] %s - %s", title, message)
        await asyncio.sleep(0)
