import asyncio
from host.transport.dryrun import DryRunTransport
from host.config_loader import TransportConfig

def test_dryrun():
    t = DryRunTransport(TransportConfig())
    async def go():
        await t.set_state(True)
        assert t.state is True
        await t.set_state(False)
        assert t.state is False
    asyncio.run(go())
