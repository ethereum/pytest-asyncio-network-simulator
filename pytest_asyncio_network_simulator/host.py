import asyncio
import random
from typing import (
    Dict,
)

from .address import (
    Address,
)
from .router import (
    Router,
)
from .server import (
    Server,
)
from .utils import (
    ConnectionCallback,
    ReaderWriterPair,
)


class Host:
    servers: Dict[int, Server]
    connections: Dict[int, Address]

    def __init__(self, host: str, router: Router) -> None:
        self.router = router
        self.host = host
        self.servers = {}
        self.connections = {}

    def get_server(self, port: int) -> Server:
        try:
            return self.servers[port]
        except KeyError:
            raise ConnectionRefusedError("No server running at {0}:{1}".format(self.host, port))

    def _get_open_port(self) -> int:
        while True:
            port = random.randint(2**15, 2**16 - 1)
            if port in self.connections:
                continue
            elif port in self.servers:
                continue
            else:
                break
        return port

    async def start_server(self, client_connected_cb: ConnectionCallback, port: int) -> Server:
        if port in self.servers:
            raise OSError('Address already in use')

        address = Address(self.host, port)

        server = Server(client_connected_cb, address)
        self.servers[port] = server
        return server

    def receive_connection(self, port: int) -> ReaderWriterPair:
        address = Address(self.host, port)
        if port not in self.servers:
            raise ConnectionRefusedError("No server running at {0}:{1}".format(self.host, port))
        elif address.port in self.connections:
            raise OSError('Address already in use')

        reader, writer = self.router.get_connected_readers(address)

        server = self.servers[port]
        server.add_connection(writer)

        return reader, writer

    async def open_connection(self, host: str, port: int) -> ReaderWriterPair:
        if port in self.connections:
            raise OSError('already connected')

        to_address = Address(host, port)

        to_host = self.router.get_host(host)
        client_reader, server_writer = to_host.receive_connection(port)

        from_port = self._get_open_port()
        from_address = Address(self.host, from_port)

        server_reader, client_writer = self.router.get_connected_readers(from_address)
        self.connections[from_port] = to_address

        server = to_host.get_server(port)
        asyncio.ensure_future(server.client_connected_cb(server_reader, server_writer))

        return client_reader, client_writer
