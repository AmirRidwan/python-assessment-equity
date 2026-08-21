from datetime import datetime, timedelta


def test_list_tickers(client, get_tickers):
    response = client.get("/tickers/")

    assert response.status_code == 200

    tickers = response.json()

    assert isinstance(tickers, list)
    assert len(tickers) > 0

    for ticker in tickers:
        assert "id" in ticker
        assert "symbol" in ticker
        assert "company_name" in ticker
        assert "sector" in ticker
        assert "is_active" in ticker


def test_aapl_exists(client, aapl_ticker):
    assert aapl_ticker["symbol"] == "AAPL"
    assert aapl_ticker["id"] > 0


def test_list_price_history(
    client,
    aapl_ticker,
):
    ticker_id = aapl_ticker["id"]

    response = client.get(
        f"/tickers/{ticker_id}/prices",
        params={
            "page": 1,
            "page_size": 20,
        },
    )

    assert response.status_code == 200

    prices = response.json()

    assert isinstance(prices, list)

    if prices:
        assert "id" in prices[0]
        assert "ticker_id" in prices[0]
        assert "price" in prices[0]
        assert "volume" in prices[0]
        assert "captured_at" in prices[0]
        assert "source" in prices[0]


def test_price_history_is_most_recent_first(
    client,
    aapl_ticker,
):
    response = client.get(
        f"/tickers/{aapl_ticker['id']}/prices",
        params={
            "page": 1,
            "page_size": 20,
        },
    )

    assert response.status_code == 200

    prices = response.json()

    if len(prices) < 2:
        return

    timestamps = [datetime.fromisoformat(item["captured_at"]) for item in prices]

    assert timestamps == sorted(
        timestamps,
        reverse=True,
    )


def test_price_history_pagination(
    client,
    aapl_ticker,
):
    response = client.get(
        f"/tickers/{aapl_ticker['id']}/prices",
        params={
            "page": 1,
            "page_size": 5,
        },
    )

    assert response.status_code == 200

    prices = response.json()

    assert len(prices) <= 5


def test_create_valid_price(
    client,
    aapl_ticker,
):
    ticker_id = aapl_ticker["id"]

    history_response = client.get(
        f"/tickers/{ticker_id}/prices",
        params={
            "page": 1,
            "page_size": 20,
        },
    )

    assert history_response.status_code == 200

    history = history_response.json()

    if history:
        latest = max(
            history,
            key=lambda item: item["captured_at"],
        )

        latest_dt = datetime.fromisoformat(latest["captured_at"])

        captured_at = latest_dt + timedelta(days=1)
    else:
        captured_at = datetime.utcnow()

    response = client.post(
        f"/tickers/{ticker_id}/prices",
        json={
            "price": 230.50,
            "volume": 1250000,
            "captured_at": captured_at.isoformat(),
            "source": "pytest",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["ticker_id"] == ticker_id
    assert float(data["price"]) > 0
    assert data["volume"] >= 0
    assert data["source"] == "pytest"


def test_negative_price_rejected(
    client,
    aapl_ticker,
):
    response = client.post(
        f"/tickers/{aapl_ticker['id']}/prices",
        json={
            "price": -1,
            "volume": 1000,
            "captured_at": "2099-01-01T10:00:00",
            "source": "pytest",
        },
    )

    assert response.status_code == 422


def test_zero_price_rejected(
    client,
    aapl_ticker,
):
    response = client.post(
        f"/tickers/{aapl_ticker['id']}/prices",
        json={
            "price": 0,
            "volume": 1000,
            "captured_at": "2099-01-02T10:00:00",
            "source": "pytest",
        },
    )

    assert response.status_code == 422


def test_negative_volume_rejected(
    client,
    aapl_ticker,
):
    response = client.post(
        f"/tickers/{aapl_ticker['id']}/prices",
        json={
            "price": 200,
            "volume": -1,
            "captured_at": "2099-01-03T10:00:00",
            "source": "pytest",
        },
    )

    assert response.status_code == 422


def test_missing_ticker_returns_404(client):
    response = client.post(
        "/tickers/999999/prices",
        json={
            "price": 200,
            "volume": 1000,
            "captured_at": "2099-01-04T10:00:00",
            "source": "pytest",
        },
    )

    assert response.status_code == 404


def test_out_of_order_price_rejected(
    client,
    aapl_ticker,
):
    ticker_id = aapl_ticker["id"]

    history_response = client.get(
        f"/tickers/{ticker_id}/prices",
        params={
            "page": 1,
            "page_size": 20,
        },
    )

    assert history_response.status_code == 200

    history = history_response.json()

    if not history:
        return

    latest = max(
        history,
        key=lambda item: item["captured_at"],
    )

    latest_dt = datetime.fromisoformat(latest["captured_at"])

    earlier = latest_dt - timedelta(days=1)

    response = client.post(
        f"/tickers/{ticker_id}/prices",
        json={
            "price": 220,
            "volume": 100000,
            "captured_at": earlier.isoformat(),
            "source": "pytest",
        },
    )

    assert response.status_code == 400

    detail = response.json()["detail"]

    assert "captured_at" in detail


def test_equal_timestamp_rejected(
    client,
    aapl_ticker,
):
    ticker_id = aapl_ticker["id"]

    history_response = client.get(
        f"/tickers/{ticker_id}/prices",
        params={
            "page": 1,
            "page_size": 20,
        },
    )

    assert history_response.status_code == 200

    history = history_response.json()

    if not history:
        return

    latest = max(
        history,
        key=lambda item: item["captured_at"],
    )

    response = client.post(
        f"/tickers/{ticker_id}/prices",
        json={
            "price": 220,
            "volume": 100000,
            "captured_at": latest["captured_at"],
            "source": "pytest",
        },
    )

    assert response.status_code == 400
