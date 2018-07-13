import asyncio

from cancel_token import CancelToken


async def _connect_streams(
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        queue: asyncio.Queue,
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
            data = await token.wait_for(reader.readexactly(size))
            writer.write(data)
            queue.task_done()
            await token.wait_for(writer.drain())
    except OperationCancelled:
        pass
    finally:
        writer.write_eof()

    if reader.at_eof():
        reader.feed_eof()


class Router(BaseService):
    hosts: Dict[str, 'Host']
    networks = Dict[str, 'Network']
    connections = Dict[CancelToken, asyncio.Task]

    def __init__(self):
        super().__init__()
        self.hosts = {}
        self.networks = {}
        self.connections = {}

    #
    # Service API
    #
    async def _run(self) -> None:
        while not self.cancel_token.triggered:
            await asyncio.sleep(0.02)

    async def _cleanup(self) -> None:
        # all of the cancel tokens *should* be triggered already so we just
        # wait for the networking processes to complete.
        if self.connections:
            await asyncio.wait(
                self.connections.values(),
                timeout=2,
                return_when=asyncio.ALL_COMPLETED
            )

    #
    # Connections API
    #
    def get_host(self, host: str) -> 'Host':
        if host not in self.hosts:
            self.hosts[host] = Host(host, self)
        return self.hosts[host]

    def get_network(self, name: str) -> 'Network':
        if name not in self.networks:
            self.networks[name] = Network(name, self)
        return self.networks[name]

    def get_connected_readers(self, address: Address) -> ReaderWriterPair:
        external_reader, internal_writer = direct_pipe()
        internal_reader, external_writer = addressed_pipe(address)

        token = CancelToken(str(address)).chain(self.cancel_token)
        connection = asyncio.ensure_future(_connect_streams(
            internal_reader, internal_writer, external_writer.transport.queue, token,
        ))
        self.connections[token] = connection

        return (external_reader, external_writer)
