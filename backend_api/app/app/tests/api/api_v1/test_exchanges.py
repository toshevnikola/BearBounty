import logging
from pprint import pprint

from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.crud import exchange
from app.core.config import settings


def test_read_exchanges(setup_db: Session, client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/exchanges/")
    pprint(response.json())
    assert len(response.json()) == 0
    assert response.status_code == 200


def test_read_single_exchange(setup_db: Session, client: TestClient) -> None:
    # setup
    name = "Coinbase1234"
    pairs = ["BTCUSDT", "ETHUSDT"]
    data = {"name": name, "supported_pairs": pairs}
    response = client.post(f"{settings.API_V1_STR}/exchanges/", json=data)
    json_obj = response.json()

    # endpoint to test
    response = client.get(f"{settings.API_V1_STR}/exchanges/{json_obj['id']}")

    # assertions
    assert response.json()["name"] == name
    assert response.json()['supported_pairs'] == pairs
    assert response.status_code == 200
