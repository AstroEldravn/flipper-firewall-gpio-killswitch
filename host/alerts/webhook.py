from __future__ import annotations
import asyncio, json, time
import requests

class WebhookAlert:
    def __init__(self, url: str):
        self.url = url

    async def send(self, title: str, message: str):
        payload = {"title": title, "message": message, "ts": time.time()}
        try:
            requests.post(self.url, json=payload, timeout=2)
        except Exception:
            pass
        await asyncio.sleep(0)
