import asyncio
from typing import (
    List,
)

from .address import (
    Address,
)
from .utils import (
    ConnectionCallback,
)


class Server(asyncio.AbstractServer):
    """
    Mock version of `asyncio.Server` object.
    """
    connections: List[asyncio.StreamWriter]

    def __init__(
            self,
            client_connected_cb: ConnectionCallback,
            address: Address) -> None:
        self.client_connected_cb = client_connected_cb
        self.address = address
        self.connections = []

    def __repr__(self) -> str:
        return '<%s %s>' % (self.__class__.__name__, self.address)

    def close(self) -> None:
        for writer in self.connections:
            writer.write_eof()

    async def wait_closed(self) -> None:  # type: ignore
        await asyncio.wait(
            tuple(writer.drain() for writer in self.connections),
            timeout=0.01,
            return_when=asyncio.ALL_COMPLETED
        )

    def add_connection(self, writer: asyncio.StreamWriter) -> None:
        self.connections.append(writer)
