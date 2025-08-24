from __future__ import annotations
import abc

class BaseTransport(abc.ABC):
    name = "base"

    @abc.abstractmethod
    async def set_state(self, high: bool):
        ...

    async def close(self):
        return None
