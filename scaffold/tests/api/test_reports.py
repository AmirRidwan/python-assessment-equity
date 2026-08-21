def add_holding(
    client,
    manager_id,
    ticker_id,
    weight=20,
):
    return client.post(
        "/holdings/",
        headers={
            "X-Manager-Id": str(manager_id),
        },
        json={
            "ticker_id": ticker_id,
            "target_weight_pct": weight,
        },
    )


def test_reports_require_manager_header(client):
    response = client.get("/reports/")

    assert response.status_code == 422


def test_report_requires_holding(
    client,
    create_manager,
):
    manager = create_manager(
        name="No Portfolio Report Manager",
        seniority="principal",
    )

    response = client.post(
        "/reports/",
        headers={
            "X-Manager-Id": str(manager["id"]),
        },
        json={
            "date_from": "2024-01-01",
            "date_to": "2099-12-31",
        },
    )

    assert response.status_code == 400

    assert "add a holding" in response.json()["detail"].lower()


def test_report_date_range_validation(
    client,
    create_manager,
    get_tickers,
):
    manager = create_manager(
        name="Invalid Report Range Manager",
        seniority="principal",
    )

    ticker_id = get_tickers()[0]["id"]

    holding_response = add_holding(
        client,
        manager["id"],
        ticker_id,
        20,
    )

    assert holding_response.status_code == 201

    response = client.post(
        "/reports/",
        headers={
            "X-Manager-Id": str(manager["id"]),
        },
        json={
            "date_from": "2026-08-18",
            "date_to": "2026-08-01",
        },
    )

    assert response.status_code == 400

    assert "date_from" in response.json()["detail"]


def test_generate_report(
    client,
    create_manager,
    aapl_ticker,
):
    manager = create_manager(
        name="Report Generation Manager",
        seniority="principal",
    )

    holding_response = add_holding(
        client,
        manager["id"],
        aapl_ticker["id"],
        20,
    )

    assert holding_response.status_code == 201

    response = client.post(
        "/reports/",
        headers={
            "X-Manager-Id": str(manager["id"]),
        },
        json={
            "date_from": "2000-01-01",
            "date_to": "2099-12-31",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["manager_id"] == manager["id"]
    assert data["filename"]
    assert data["row_count"] >= 0
    assert data["date_from"] == "2000-01-01"
    assert data["date_to"] == "2099-12-31"

    return data


def test_list_reports(
    client,
    create_manager,
    aapl_ticker,
):
    manager = create_manager(
        name="List Reports Manager",
        seniority="principal",
    )

    holding_response = add_holding(
        client,
        manager["id"],
        aapl_ticker["id"],
        20,
    )

    assert holding_response.status_code == 201

    generate_response = client.post(
        "/reports/",
        headers={
            "X-Manager-Id": str(manager["id"]),
        },
        json={
            "date_from": "2000-01-01",
            "date_to": "2099-12-31",
        },
    )

    assert generate_response.status_code == 201

    response = client.get(
        "/reports/",
        headers={
            "X-Manager-Id": str(manager["id"]),
        },
        params={
            "page": 1,
            "page_size": 20,
        },
    )

    assert response.status_code == 200

    reports = response.json()

    assert isinstance(reports, list)
    assert len(reports) >= 1

    for report in reports:
        assert report["manager_id"] == manager["id"]


def test_report_isolation_between_managers(
    client,
    create_manager,
    aapl_ticker,
):
    manager_a = create_manager(
        name="Report Isolation A",
        seniority="principal",
    )

    manager_b = create_manager(
        name="Report Isolation B",
        seniority="principal",
    )

    holding_response = add_holding(
        client,
        manager_a["id"],
        aapl_ticker["id"],
        20,
    )

    assert holding_response.status_code == 201

    generate_response = client.post(
        "/reports/",
        headers={
            "X-Manager-Id": str(manager_a["id"]),
        },
        json={
            "date_from": "2000-01-01",
            "date_to": "2099-12-31",
        },
    )

    assert generate_response.status_code == 201

    reports_a = client.get(
        "/reports/",
        headers={
            "X-Manager-Id": str(manager_a["id"]),
        },
    )

    reports_b = client.get(
        "/reports/",
        headers={
            "X-Manager-Id": str(manager_b["id"]),
        },
    )

    assert reports_a.status_code == 200
    assert reports_b.status_code == 200

    manager_a_reports = reports_a.json()
    manager_b_reports = reports_b.json()

    assert all(report["manager_id"] == manager_a["id"] for report in manager_a_reports)

    assert all(report["manager_id"] == manager_b["id"] for report in manager_b_reports)

    assert not any(
        report["manager_id"] == manager_a["id"] for report in manager_b_reports
    )


def test_download_report(
    client,
    create_manager,
    aapl_ticker,
):
    manager = create_manager(
        name="Download Report Manager",
        seniority="principal",
    )

    holding_response = add_holding(
        client,
        manager["id"],
        aapl_ticker["id"],
        20,
    )

    assert holding_response.status_code == 201

    generate_response = client.post(
        "/reports/",
        headers={
            "X-Manager-Id": str(manager["id"]),
        },
        json={
            "date_from": "2000-01-01",
            "date_to": "2099-12-31",
        },
    )

    assert generate_response.status_code == 201

    report = generate_response.json()

    download_response = client.get(
        f"/reports/{report['id']}/download",
        headers={
            "X-Manager-Id": str(manager["id"]),
        },
    )

    assert download_response.status_code == 200

    assert (
        download_response.headers["content-type"]
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


def test_download_missing_report(
    client,
    create_manager,
    aapl_ticker,
):
    manager = create_manager(
        name="Missing Report File Manager",
        seniority="principal",
    )

    holding_response = add_holding(
        client,
        manager["id"],
        aapl_ticker["id"],
        20,
    )

    assert holding_response.status_code == 201

    generate_response = client.post(
        "/reports/",
        headers={
            "X-Manager-Id": str(manager["id"]),
        },
        json={
            "date_from": "2000-01-01",
            "date_to": "2099-12-31",
        },
    )

    assert generate_response.status_code == 201

    report = generate_response.json()

    from pathlib import Path

    report_path = Path("reports") / report["filename"]

    assert report_path.exists()

    backup_path = report_path.parent / f"{report_path.name}.bak"

    report_path.rename(backup_path)

    try:
        response = client.get(
            f"/reports/{report['id']}/download",
            headers={
                "X-Manager-Id": str(manager["id"]),
            },
        )

        assert response.status_code == 404

        assert "missing" in response.json()["detail"].lower()

    finally:
        if backup_path.exists():
            backup_path.rename(report_path)


def test_inactive_manager_rejected_from_reports(
    client,
    create_manager,
):
    manager = create_manager(
        name="Inactive Reports Manager",
        seniority="principal",
    )

    deactivate_response = client.put(
        f"/managers/{manager['id']}",
        json={
            "active": False,
        },
    )

    assert deactivate_response.status_code == 200

    response = client.get(
        "/reports/",
        headers={
            "X-Manager-Id": str(manager["id"]),
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Portfolio manager is inactive"
