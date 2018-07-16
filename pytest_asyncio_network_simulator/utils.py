import asyncio
from typing import (
    Any,
    Callable,
    Tuple,
)

ConnectionCallback = Callable[[asyncio.StreamReader, asyncio.StreamWriter], Any]
ReaderWriterPair = Tuple[asyncio.StreamReader, asyncio.StreamWriter]
