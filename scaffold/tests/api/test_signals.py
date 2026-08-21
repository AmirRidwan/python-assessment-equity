def test_list_signals(client):
    response = client.get(
        "/signals/",
        params={
            "page": 1,
            "page_size": 20,
        },
    )

    assert response.status_code == 200

    signals = response.json()

    assert isinstance(signals, list)


def test_filter_signals_by_ticker(
    client,
    aapl_ticker,
):
    ticker_id = aapl_ticker["id"]

    response = client.get(
        "/signals/",
        params={
            "ticker_id": ticker_id,
            "page": 1,
            "page_size": 20,
        },
    )

    assert response.status_code == 200

    signals = response.json()

    assert isinstance(signals, list)

    for signal in signals:
        assert signal["ticker_id"] == ticker_id


def test_signal_pagination(client):
    response = client.get(
        "/signals/",
        params={
            "page": 1,
            "page_size": 5,
        },
    )

    assert response.status_code == 200

    signals = response.json()

    assert len(signals) <= 5


def test_filter_unknown_ticker_returns_404(
    client,
):
    response = client.get(
        "/signals/",
        params={
            "ticker_id": 999999,
        },
    )

    assert response.status_code == 404
