import asyncio
import logging
from typing import (
    TYPE_CHECKING,
    cast,
)

from cancel_token import (
    CancelToken,
    OperationCancelled,
)

from .address import (
    Address,
)
from .streams import (
    addressed_pipe,
    direct_pipe,
)
from .transports import (
    AddressedTransport,
)
from .utils import (
    ReaderWriterPair,
)

if TYPE_CHECKING:
    from typing import Dict  # noqa: F401
    from .network import Network  # noqa: F401
    from .host import Host  # noqa: F401


async def _connect_streams(
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        queue: "asyncio.Queue[int]",
        token: CancelToken) -> None:
    try:
        while not token.triggered:
            if reader.at_eof():
                break

            try:
                size = queue.get_nowait()
            except asyncio.QueueEmpty:
                await asyncio.sleep(0)
                continue
            data = await token.cancellable_wait(reader.readexactly(size))
            writer.write(data)
            queue.task_done()
            await token.cancellable_wait(writer.drain())
    except OperationCancelled:
        pass
    finally:
        writer.write_eof()

    if reader.at_eof():
        reader.feed_eof()


class Router:
    logger: logging.Logger = logging.getLogger('pytest_asyncio_network_simulator.router.Router')

    def __init__(self) -> None:
        self.hosts: Dict[str, 'Host'] = {}
        self.networks: Dict[str, 'Network'] = {}
        self.connections: Dict[CancelToken, asyncio.Future[None]] = {}

        self.cancel_token = CancelToken('Router')

        self._run_lock = asyncio.Lock()
        self.cleaned_up = asyncio.Event()

    #
    # Connections API
    #
    def get_host(self, host: str) -> 'Host':
        from .host import Host  # noqa: F811
        if host not in self.hosts:
            self.hosts[host] = Host(host, self)
        return self.hosts[host]

    def get_network(self, name: str) -> 'Network':
        from .network import Network  # noqa: F811
        if name not in self.networks:
            self.networks[name] = Network(name, self)
        return self.networks[name]

    def get_connected_readers(self, address: Address) -> ReaderWriterPair:
        external_reader, internal_writer = direct_pipe()
        internal_reader, external_writer = addressed_pipe(address)

        token = CancelToken(str(address)).chain(self.cancel_token)
        connection = asyncio.ensure_future(_connect_streams(
            internal_reader,
            internal_writer,
            cast(AddressedTransport, external_writer.transport).queue,
            token,
        ))
        self.connections[token] = connection

        return (external_reader, external_writer)

    #
    # Run, Cancel and Cleanup API
    #
    async def run(self) -> None:
        """Await for the service's _run() coroutine.

        Once _run() returns, triggers the cancel token, call cleanup() and
        finished_callback (if one was passed).
        """
        if self.is_running:
            raise RuntimeError("Cannot start the service while it's already running")
        elif self.cancel_token.triggered:
            raise RuntimeError("Cannot restart a service that has already been cancelled")

        try:
            async with self._run_lock:
                await self.cancel_token.wait()
        finally:
            await self.cleanup()

    async def cleanup(self) -> None:
        """
        Run the ``_cleanup()`` coroutine and set the ``cleaned_up`` event after
        the service finishes cleanup.
        """
        if self.connections:
            await asyncio.wait(
                self.connections.values(),
                timeout=2,
                return_when=asyncio.ALL_COMPLETED
            )
        self.cleaned_up.set()

    async def cancel(self) -> None:
        """Trigger the CancelToken and wait for the cleaned_up event to be set."""
        if self.cancel_token.triggered:
            self.logger.warning("Tried to cancel %s, but it was already cancelled", self)
            return
        elif not self.is_running:
            raise RuntimeError("Cannot cancel a service that has not been started")

        self.logger.debug("Cancelling %s", self)
        self.cancel_token.trigger()
        try:
            await asyncio.wait_for(
                self.cleaned_up.wait(),
                timeout=5,
            )
        except asyncio.futures.TimeoutError:
            self.logger.info("Timed out waiting for %s to finish its cleanup, exiting anyway", self)
        else:
            self.logger.debug("%s finished cleanly", self)

    @property
    def is_running(self) -> bool:
        return self._run_lock.locked()
