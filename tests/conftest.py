import sys
from pathlib import Path

import pymongo
import pytest
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


class _DummyCollection:
    def __init__(self, name: str):
        self.name = name


class _DummyDatabase:
    def __getitem__(self, name: str):
        return _DummyCollection(name)


class _DummyClient:
    def __getitem__(self, name: str):
        return _DummyDatabase()


def _dummy_mongo_client(*_args, **_kwargs):
    return _DummyClient()


pymongo.MongoClient = _dummy_mongo_client


@pytest.fixture
def app():
    from apps.fastapi.src import app as fastapi_app

    return fastapi_app


@pytest.fixture
def client(app):
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides = {}
