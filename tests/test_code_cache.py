import pytest

from server.events import ReplaceData
from server.main import ConnectionManager


class DummyClient:
    def __init__(self) -> None:
        self._websocket = ""
        self.id = ""


@pytest.fixture(scope="class")
def connection():
    manager = ConnectionManager()
    dummy_client = DummyClient()
    manager.create_room(dummy_client, "CODE")
    return manager


@pytest.fixture
def update_cache(connection):
    new_data = ReplaceData(code=[{"from": 0, "to": 1, "value": "a"}])
    connection.update_code_cache("CODE", new_data)


class TestCodeCache:
    def test_code_cache_empty_on_connect(self, connection: ConnectionManager):
        assert connection._rooms["CODE"]["code"] == ""

    def test_code_cache_added(self, connection: ConnectionManager, update_cache):
        assert connection._rooms["CODE"]["code"] == "a"

    def test_code_cache_replacement(self, connection: ConnectionManager, update_cache):
        assert connection._rooms["CODE"]["code"] == "a"

        new_data = ReplaceData(code=[{"from": 0, "to": 1, "value": "b"}])
        connection.update_code_cache("CODE", new_data)

        assert connection._rooms["CODE"]["code"] == "b"
