from __future__ import annotations
import asyncio

try:
    from plyer import notification
except Exception:
    notification = None

class DesktopNotifyAlert:
    def __init__(self, title: str | None, app_name: str | None):
        self.title = title or "GPIO Killswitch"
        self.app_name = app_name or "Killswitch"

    async def send(self, title: str, message: str):
        if notification:
            notification.notify(title=title or self.title, message=message, app_name=self.app_name, timeout=3)
        await asyncio.sleep(0)
