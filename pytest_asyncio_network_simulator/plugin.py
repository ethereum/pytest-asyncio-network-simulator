import asyncio
from typing import (
    Any,
    AsyncGenerator,
)

import pytest

from .network import (
    Network,
)
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


@pytest.fixture
def network(router: Router, monkeypatch: Any) -> Network:
    network = router.get_network('localhost')
    # TODO: this should be configurable.
    network.default_host = '127.0.0.1'

    monkeypatch.setattr(asyncio, 'start_server', network.start_server)
    monkeypatch.setattr(asyncio, 'open_connection', network.open_connection)
    return network
