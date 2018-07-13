import asyncio
from typing import Tuple


ReaderWriterPair = Tuple[asyncio.StreamReader, asyncio.StreamWriter]
