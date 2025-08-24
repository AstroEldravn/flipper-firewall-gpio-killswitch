from __future__ import annotations
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional, Literal, Union
import yaml, pathlib, sys

TransportType = Literal["uart_serial", "gpio_local", "dryrun"]

class TransportConfig(BaseModel):
    type: TransportType = "dryrun"
    device: str | None = "auto"
    line: Optional[Literal["rts", "dtr"]] = "rts"  # uart_serial only
    invert_logic: bool = False
    # gpio_local specifics
    chip: Optional[str] = None       # e.g., "/dev/gpiochip0"
    line_offset: Optional[int] = None  # gpiod line offset or BCM pin

class TriggerFile(BaseModel):
    name: str
    type: Literal["file_exists"]
    path: str
    action: Literal["kill_on", "kill_off"]

class TriggerTimer(BaseModel):
    name: str
    type: Literal["timer"]
    seconds: float = 5.0
    action: Literal["kill_on", "kill_off"]

class TriggerLogRegex(BaseModel):
    name: str
    type: Literal["log_regex"]
    path: str
    regex: str
    action: Literal["kill_on", "kill_off"]

class TriggerHttpProbe(BaseModel):
    name: str
    type: Literal["http_probe"]
    url: str
    expect_status: Optional[int] = 200
    contains: Optional[str] = None
    interval: float = 5.0
    action: Literal["kill_on", "kill_off"]

Trigger = Union[TriggerFile, TriggerTimer, TriggerLogRegex, TriggerHttpProbe]

class Policy(BaseModel):
    default_kill_state: bool = False
    debounce_ms: int = 100
    triggers: List[Trigger] = Field(default_factory=list)

class AlertLog(BaseModel):
    type: Literal["log_only"]

class AlertDesktop(BaseModel):
    type: Literal["desktop_notify"]
    title: str | None = "GPIO Killswitch"
    app_name: str | None = "Killswitch"

class AlertWebhook(BaseModel):
    type: Literal["webhook"]
    url: str

class AlertSyslog(BaseModel):
    type: Literal["syslog"]
    address: str | None = None  # default local

Alert = Union[AlertLog, AlertDesktop, AlertWebhook, AlertSyslog]

class Config(BaseModel):
    transport: TransportConfig = TransportConfig()
    policy: Policy = Policy()
    alerts: List[Alert] = Field(default_factory=lambda: [AlertLog(type="log_only")])

def load_config(path: str | pathlib.Path) -> Config:
    p = pathlib.Path(path)
    if not p.exists():
        print(f"[-] Config not found: {p}", file=sys.stderr)
        sys.exit(1)
    with p.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    try:
        return Config(**data)
    except ValidationError as e:
        print(f"[-] Config validation error:\n{e}", file=sys.stderr)
        sys.exit(2)
