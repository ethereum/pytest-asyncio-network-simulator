import asyncio
import pytest

from pytest_asyncio_network_simulator.network import Network


class sentinal_a:
    pass


class sentinal_b:
    pass


@pytest.fixture(autouse=True)
def _pre_patch(monkeypatch):
    monkeypatch.setattr(asyncio, 'start_server', sentinal_a)
    monkeypatch.setattr(asyncio, 'open_connection', sentinal_b)


def test_network_patch_asyncio_context_manager_api():
    network = Network('test', None, 'localhost')

    assert asyncio.start_server == sentinal_a
    assert asyncio.open_connection == sentinal_b

    with network.patch_asyncio():
        assert asyncio.start_server == network.start_server
        assert asyncio.open_connection == network.open_connection

    assert asyncio.start_server == sentinal_a
    assert asyncio.open_connection == sentinal_b


def test_network_patch_asyncio_context_manager_api_with_error():
    network = Network('test', None, 'localhost')

    assert asyncio.start_server == sentinal_a
    assert asyncio.open_connection == sentinal_b

    with pytest.raises(AssertionError):
        with network.patch_asyncio():
            assert asyncio.start_server == network.start_server
            assert asyncio.open_connection == network.open_connection
            raise AssertionError('failed')

    assert asyncio.start_server == sentinal_a
    assert asyncio.open_connection == sentinal_b
