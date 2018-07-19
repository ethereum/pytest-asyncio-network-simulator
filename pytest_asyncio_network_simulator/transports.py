import asyncio
from typing import (
    Any,
    Iterable,
)

from .address import (
    Address,
)


class MemoryTransport(asyncio.Transport):
    """
    Direct connection between a StreamWriter and StreamReader.
    """
    _reader: asyncio.StreamReader

    def __init__(self, reader: asyncio.StreamReader) -> None:
        super().__init__()
        self._reader = reader

    def write(self, data: bytes) -> None:
        self._reader.feed_data(data)

    def writelines(self, data: Iterable[bytes]) -> None:
        for line in data:
            self.write(line)
            self.write(b'\n')

    def write_eof(self) -> None:
        self._reader.feed_eof()

    def can_write_eof(self) -> bool:
        return True

    def is_closing(self) -> bool:
        return False

    def close(self) -> None:
        self.write_eof()


class AddressedTransport(MemoryTransport):
    """
    Direct connection between a StreamWriter and StreamReader.
    """
    _queue: "asyncio.Queue[int]"

    def __init__(self, address: Address, reader: asyncio.StreamReader) -> None:
        super().__init__(reader)
        self._address = address
        self._queue = asyncio.Queue()

    @property
    def queue(self) -> "asyncio.Queue[int]":
        return self._queue

    def get_extra_info(self, name: str, default: Any=None) -> Any:
        if name == 'peername':
            return (self._address.host, self._address.port)
        else:
            return super().get_extra_info(name, default)

    def write(self, data: bytes) -> None:
        super().write(data)
        self._queue.put_nowait(len(data))
