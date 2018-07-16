import os

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


class Network:
    router: Router
    name: str
    _default_host: str = None

    def __init__(self, name: str, router: Router, default_host: str=None):
        self.name = name
        self.router = router
        self.default_host = default_host

    @property
    def default_host(self) -> str:
        if self._default_host is not None:
            return self._default_host
        else:
            return os.environ.get('P2P_DEFAULT_HOST', '127.0.0.1')

    @default_host.setter
    def default_host(self, value: str) -> None:
        self._default_host = value

    #
    # Asyncio API
    #
    async def start_server(
            self,
            client_connected_cb: ConnectionCallback,
            host: str,
            port: int) -> Server:
        host = self.router.get_host(host)
        return await host.start_server(client_connected_cb, port)

    async def open_connection(
            self,
            host: str,
            port: int) -> ReaderWriterPair:
        client_host = self.router.get_host(self.default_host)
        try:
            return await client_host.open_connection(host, port)
        except ConnectionRefusedError as err:
            # if we fail to connect to the specified host, check if there is a
            # server running on `0.0.0.0` and connect to that.
            catch_all_host = self.router.get_host('0.0.0.0')
            try:
                return await catch_all_host.open_connection('0.0.0.0', port)
            except ConnectionRefusedError:
                pass
            raise err
