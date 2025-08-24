from __future__ import annotations
import logging
from typing import List
from host.config_loader import Alert, AlertDesktop, AlertLog, AlertSyslog, AlertWebhook
from host.alerts.log_only import LogOnlyAlert
from host.alerts.desktop_notify import DesktopNotifyAlert
from host.alerts.webhook import WebhookAlert
from host.alerts.syslog import SyslogAlert

log = logging.getLogger(__name__)

class AlertManager:
    def __init__(self, alerts_cfg: List[Alert]):
        self.alerts = []
        for a in alerts_cfg:
            if isinstance(a, AlertLog):
                self.alerts.append(LogOnlyAlert())
            elif isinstance(a, AlertDesktop):
                self.alerts.append(DesktopNotifyAlert(a.title, a.app_name))
            elif isinstance(a, AlertWebhook):
                self.alerts.append(WebhookAlert(a.url))
            elif isinstance(a, AlertSyslog):
                self.alerts.append(SyslogAlert(a.address))

    async def notify(self, title: str, message: str):
        for alert in self.alerts:
            try:
                await alert.send(title, message)
            except Exception as e:
                log.warning("Alert failed (%s): %s", type(alert).__name__, e)
