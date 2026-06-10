def test_register_user_success(client, user_data):
    response = client.post(
        "/auth/",
        json=user_data,
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]


def test_register_user_invalid_data_should_return_422(client, invalid_user_data):
    response = client.post(
        "/auth/",
        json=invalid_user_data,
    )

    assert response.status_code == 422


def test_login_success(client, registered_user, login_data):
    response = client.post(
        "/auth/login",
        data=login_data,
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["access_token"] is not None
    assert "token_type" in data
    assert data["token_type"] == "bearer"
