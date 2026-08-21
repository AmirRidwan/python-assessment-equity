def create_test_holding(
    client,
    manager_id,
    ticker_id,
    weight,
):
    response = client.post(
        "/holdings/",
        headers={
            "X-Manager-Id": str(manager_id),
        },
        json={
            "ticker_id": ticker_id,
            "target_weight_pct": weight,
        },
    )

    return response


def test_holdings_require_manager_header(client):
    response = client.get("/holdings/")

    assert response.status_code == 422


def test_manager_can_list_only_own_holdings(
    client,
    create_manager,
    get_tickers,
):
    manager = create_manager(
        name="Isolation Manager",
        seniority="associate",
    )

    tickers = get_tickers()

    assert len(tickers) >= 1

    ticker_id = tickers[0]["id"]

    response = create_test_holding(
        client,
        manager["id"],
        ticker_id,
        20,
    )

    assert response.status_code == 201

    holdings_response = client.get(
        "/holdings/",
        headers={
            "X-Manager-Id": str(manager["id"]),
        },
    )

    assert holdings_response.status_code == 200

    holdings = holdings_response.json()

    assert len(holdings) >= 1

    for holding in holdings:
        assert holding["manager_id"] == manager["id"]


def test_manager_isolation_between_two_managers(
    client,
    create_manager,
    get_tickers,
):
    manager_a = create_manager(
        name="Manager A Isolation",
        seniority="associate",
    )

    manager_b = create_manager(
        name="Manager B Isolation",
        seniority="associate",
    )

    tickers = get_tickers()

    assert len(tickers) >= 2

    ticker_a = tickers[0]["id"]
    ticker_b = tickers[1]["id"]

    response_a = create_test_holding(
        client,
        manager_a["id"],
        ticker_a,
        20,
    )

    response_b = create_test_holding(
        client,
        manager_b["id"],
        ticker_b,
        30,
    )

    assert response_a.status_code == 201
    assert response_b.status_code == 201

    holdings_a_response = client.get(
        "/holdings/",
        headers={
            "X-Manager-Id": str(manager_a["id"]),
        },
    )

    holdings_b_response = client.get(
        "/holdings/",
        headers={
            "X-Manager-Id": str(manager_b["id"]),
        },
    )

    assert holdings_a_response.status_code == 200
    assert holdings_b_response.status_code == 200

    holdings_a = holdings_a_response.json()
    holdings_b = holdings_b_response.json()

    assert all(holding["manager_id"] == manager_a["id"] for holding in holdings_a)

    assert all(holding["manager_id"] == manager_b["id"] for holding in holdings_b)

    assert not any(holding["ticker_id"] == ticker_b for holding in holdings_a)

    assert not any(holding["ticker_id"] == ticker_a for holding in holdings_b)


def test_duplicate_holding_rejected(
    client,
    create_manager,
    get_tickers,
):
    manager = create_manager(
        name="Duplicate Holding Manager",
        seniority="associate",
    )

    ticker_id = get_tickers()[0]["id"]

    first = create_test_holding(
        client,
        manager["id"],
        ticker_id,
        20,
    )

    assert first.status_code == 201

    second = create_test_holding(
        client,
        manager["id"],
        ticker_id,
        10,
    )

    assert second.status_code == 400

    detail = second.json()["detail"]

    assert "already" in detail.lower()


def test_total_weight_cannot_exceed_100(
    client,
    create_manager,
    get_tickers,
):
    manager = create_manager(
        name="Weight Constraint Manager",
        seniority="associate",
    )

    tickers = get_tickers()

    assert len(tickers) >= 3

    assert (
        create_test_holding(
            client,
            manager["id"],
            tickers[0]["id"],
            40,
        ).status_code
        == 201
    )

    assert (
        create_test_holding(
            client,
            manager["id"],
            tickers[1]["id"],
            40,
        ).status_code
        == 201
    )

    response = create_test_holding(
        client,
        manager["id"],
        tickers[2]["id"],
        21,
    )

    assert response.status_code == 400

    detail = response.json()["detail"]

    assert "100%" in detail


def test_total_weight_exactly_100_is_allowed(
    client,
    create_manager,
    get_tickers,
):
    manager = create_manager(
        name="Exact Weight Manager",
        seniority="associate",
    )

    tickers = get_tickers()

    assert len(tickers) >= 3

    weights = [40, 30, 30]

    for ticker, weight in zip(
        tickers[:3],
        weights,
    ):
        response = create_test_holding(
            client,
            manager["id"],
            ticker["id"],
            weight,
        )

        assert response.status_code == 201


def test_update_holding(
    client,
    create_manager,
    get_tickers,
):
    manager = create_manager(
        name="Update Holding Manager",
        seniority="associate",
    )

    tickers = get_tickers()

    ticker_id = tickers[0]["id"]

    create_response = create_test_holding(
        client,
        manager["id"],
        ticker_id,
        20,
    )

    assert create_response.status_code == 201

    update_response = client.put(
        f"/holdings/{ticker_id}",
        headers={
            "X-Manager-Id": str(manager["id"]),
        },
        json={
            "target_weight_pct": 25,
        },
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["ticker_id"] == ticker_id
    assert float(data["target_weight_pct"]) == 25


def test_update_holding_respects_100_percent_limit(
    client,
    create_manager,
    get_tickers,
):
    manager = create_manager(
        name="Update Constraint Manager",
        seniority="associate",
    )

    tickers = get_tickers()

    assert len(tickers) >= 2

    first = create_test_holding(
        client,
        manager["id"],
        tickers[0]["id"],
        60,
    )

    second = create_test_holding(
        client,
        manager["id"],
        tickers[1]["id"],
        30,
    )

    assert first.status_code == 201
    assert second.status_code == 201

    update_response = client.put(
        f"/holdings/{tickers[0]['id']}",
        headers={
            "X-Manager-Id": str(manager["id"]),
        },
        json={
            "target_weight_pct": 71,
        },
    )

    assert update_response.status_code == 400

    assert "100%" in update_response.json()["detail"]


def test_update_nonexistent_holding_returns_404(
    client,
    create_manager,
):
    manager = create_manager(
        name="Missing Holding Manager",
        seniority="associate",
    )

    response = client.put(
        "/holdings/999999",
        headers={
            "X-Manager-Id": str(manager["id"]),
        },
        json={
            "target_weight_pct": 20,
        },
    )

    assert response.status_code == 404


def test_delete_holding(
    client,
    create_manager,
    get_tickers,
):
    manager = create_manager(
        name="Delete Holding Manager",
        seniority="associate",
    )

    ticker_id = get_tickers()[0]["id"]

    create_response = create_test_holding(
        client,
        manager["id"],
        ticker_id,
        20,
    )

    assert create_response.status_code == 201

    delete_response = client.delete(
        f"/holdings/{ticker_id}",
        headers={
            "X-Manager-Id": str(manager["id"]),
        },
    )

    assert delete_response.status_code == 204

    second_delete = client.delete(
        f"/holdings/{ticker_id}",
        headers={
            "X-Manager-Id": str(manager["id"]),
        },
    )

    assert second_delete.status_code == 404


def test_inactive_manager_rejected_from_holdings(
    client,
    create_manager,
):
    manager = create_manager(
        name="Inactive Holdings Manager",
        seniority="associate",
    )

    deactivate_response = client.put(
        f"/managers/{manager['id']}",
        json={
            "active": False,
        },
    )

    assert deactivate_response.status_code == 200

    response = client.get(
        "/holdings/",
        headers={
            "X-Manager-Id": str(manager["id"]),
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Portfolio manager is inactive"
