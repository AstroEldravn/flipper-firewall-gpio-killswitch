import asyncio
from host.config_loader import TransportConfig
from host.gpio_driver import GPIODriver

async def _run():
    cfg = TransportConfig(type="dryrun", invert_logic=False)
    drv = GPIODriver(cfg)
    await drv.set_kill(True)
    await drv.set_kill(False)
    await drv.close()

def test_driver_runs():
    asyncio.run(_run())
