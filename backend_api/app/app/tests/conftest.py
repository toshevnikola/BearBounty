import pytest

from typing import Generator

from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.tests.settings import TestingSessionLocal, tests_get_db, engine
from fastapi.testclient import TestClient
from app.main import app
from app.crud import exchange
from app.schemas import ExchangeCreate
from app.db.base_class import Base


@pytest.fixture(scope="session")
def db() -> Generator:
    yield TestingSessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    app.dependency_overrides[get_db] = tests_get_db
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=False)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
