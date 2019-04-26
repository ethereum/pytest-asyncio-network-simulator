import asyncio
import os
from typing import (  # noqa: F401
    Any,
    Dict,
    Tuple,
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


class _AsyncioMonkeypatcher:
    def __init__(self,
                 network: 'Network',
                 paths_to_patch: Tuple[str, ...]) -> None:
        self.original_values: Dict[str, Any] = {}
        self.paths_to_patch = paths_to_patch
        self.network = network

    def patch(self) -> None:
        for path in self.paths_to_patch:
            self.original_values[path] = getattr(asyncio, path)
            monkey_value = getattr(self.network, path)
            setattr(asyncio, path, monkey_value)

    def unpatch(self) -> None:
        for path in self.paths_to_patch:
            setattr(asyncio, path, self.original_values[path])

    def __enter__(self) -> None:
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):  # type: ignore
        self.unpatch()


DEFAULT_PATHS = ('start_server', 'open_connection')


class Network:
    router: Router
    name: str
    _default_host: str

    def __init__(self, name: str, router: Router, default_host: str=None) -> None:
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
        _host = self.router.get_host(host)
        return await _host.start_server(client_connected_cb, port)

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

    #
    # Monkeypatch API
    #
    _patcher = None

    def patch_asyncio(
            self,
            paths_to_patch: Tuple[str, ...] = None) -> _AsyncioMonkeypatcher:
        if self._patcher is None:
            if paths_to_patch is None:
                paths_to_patch = DEFAULT_PATHS

            self._patcher = _AsyncioMonkeypatcher(self, paths_to_patch)
            self._patcher.patch()
        return self._patcher

    def unpatch_asynio(
            self,
            paths_to_unpatch: Tuple[str, ...] = None) -> None:
        if self._patcher is None:
            raise RuntimeError(
                'The `asyncio` library does not appear to be patched.'
            )
        self._patcher.unpatch()
        self._patcher = None
