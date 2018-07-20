import asyncio

from .address import (
    Address,
)
from .transports import (
    AddressedTransport,
    MemoryTransport,
)
from .utils import (
    ReaderWriterPair,
)


def addressed_pipe(address: Address) -> ReaderWriterPair:
    reader = asyncio.StreamReader()

    transport = AddressedTransport(address, reader)
    protocol = asyncio.StreamReaderProtocol(reader)

    writer = asyncio.StreamWriter(
        transport=transport,
        protocol=protocol,
        reader=reader,
        loop=asyncio.get_event_loop(),
    )
    return reader, writer


def direct_pipe() -> ReaderWriterPair:
    reader = asyncio.StreamReader()

    transport = MemoryTransport(reader)
    protocol = asyncio.StreamReaderProtocol(reader)

    writer = asyncio.StreamWriter(
        transport=transport,
        protocol=protocol,
        reader=reader,
        loop=asyncio.get_event_loop(),
    )
    return reader, writer
