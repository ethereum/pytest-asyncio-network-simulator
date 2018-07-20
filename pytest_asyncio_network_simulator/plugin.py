import asyncio
from typing import (
    AsyncGenerator,
)

import pytest

from .router import (
    Router,
)


@pytest.fixture
async def router() -> AsyncGenerator[Router, None]:
    router = Router()
    try:
        asyncio.ensure_future(router.run())
        yield router
    finally:
        await asyncio.wait_for(router.cancel(), timeout=2)
