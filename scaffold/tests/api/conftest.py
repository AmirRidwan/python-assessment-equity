import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def unique_email():
    from uuid import uuid4

    return f"test_{uuid4().hex}@example.com"


@pytest.fixture
def create_manager(client):
    def _create_manager(
        name="API Test Manager",
        email=None,
        seniority="associate",
    ):
        if email is None:
            from uuid import uuid4

            email = f"manager_{uuid4().hex}@example.com"

        response = client.post(
            "/managers",
            json={
                "name": name,
                "email": email,
                "seniority": seniority,
            },
        )

        assert response.status_code == 201

        return response.json()

    return _create_manager


@pytest.fixture
def get_tickers(client):
    def _get_tickers():
        response = client.get("/tickers/")

        assert response.status_code == 200

        return response.json()

    return _get_tickers


@pytest.fixture
def aapl_ticker(client):
    response = client.get("/tickers/")

    assert response.status_code == 200

    tickers = response.json()

    ticker = next(
        (item for item in tickers if item["symbol"] == "AAPL"),
        None,
    )

    assert ticker is not None, "AAPL ticker was not found"

    return ticker
