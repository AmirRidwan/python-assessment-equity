def test_list_managers(client):
    response = client.get(
        "/managers",
        params={
            "page": 1,
            "page_size": 20,
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_managers_pagination(client):
    response = client.get(
        "/managers",
        params={
            "page": 1,
            "page_size": 2,
        },
    )

    assert response.status_code == 200

    managers = response.json()

    assert isinstance(managers, list)
    assert len(managers) <= 2


def test_create_manager(client, unique_email):
    response = client.post(
        "/managers",
        json={
            "name": "Created API Manager",
            "email": unique_email,
            "seniority": "associate",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Created API Manager"
    assert data["email"] == unique_email
    assert data["seniority"] == "associate"
    assert data["active"] is True
    assert "id" in data
    assert "created_at" in data


def test_create_manager_invalid_seniority(client, unique_email):
    response = client.post(
        "/managers",
        json={
            "name": "Invalid Seniority Manager",
            "email": unique_email,
            "seniority": "manager",
        },
    )

    assert response.status_code == 422


def test_create_manager_invalid_email(client):
    response = client.post(
        "/managers",
        json={
            "name": "Invalid Email Manager",
            "email": "not-an-email",
            "seniority": "analyst",
        },
    )

    assert response.status_code == 422


def test_duplicate_manager_email(client, unique_email):
    first_response = client.post(
        "/managers",
        json={
            "name": "First Manager",
            "email": unique_email,
            "seniority": "analyst",
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/managers",
        json={
            "name": "Second Manager",
            "email": unique_email,
            "seniority": "principal",
        },
    )

    assert second_response.status_code == 400

    body = second_response.json()

    assert "email" in body["detail"].lower()


def test_get_manager(client, create_manager):
    manager = create_manager()

    response = client.get(f"/managers/{manager['id']}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == manager["id"]
    assert data["email"] == manager["email"]


def test_get_missing_manager(client):
    response = client.get("/managers/999999")

    assert response.status_code == 404


def test_update_manager(client, create_manager):
    manager = create_manager(name="Before Update")

    response = client.put(
        f"/managers/{manager['id']}",
        json={
            "name": "After Update",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == manager["id"]
    assert data["name"] == "After Update"


def test_update_manager_email_duplicate(
    client,
    create_manager,
):
    manager_a = create_manager(name="Manager A")

    manager_b = create_manager(name="Manager B")

    response = client.put(
        f"/managers/{manager_a['id']}",
        json={
            "email": manager_b["email"],
        },
    )

    assert response.status_code == 400


def test_deactivate_manager(
    client,
    create_manager,
):
    manager = create_manager(name="Manager To Deactivate")

    response = client.put(
        f"/managers/{manager['id']}",
        json={
            "active": False,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == manager["id"]
    assert data["active"] is False


def test_delete_manager_not_supported(
    client,
    create_manager,
):
    manager = create_manager()

    response = client.delete(f"/managers/{manager['id']}")

    assert response.status_code == 405
