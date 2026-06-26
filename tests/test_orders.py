def test_create_order_authenticated(client, order_data, auth_headers):
    response = client.post(
        "/orders/",
        json=order_data,
        headers=auth_headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert "user_id" in data
    assert "status" in data
    assert "created_at" in data
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == order_data["items"][0]["product_id"]
    assert data["items"][0]["quantity"] == order_data["items"][0]["quantity"]


def test_create_order_without_token(client, order_data):
    response = client.post(
        "/orders/",
        json=order_data,
    )

    assert response.status_code == 401


def test_create_order_with_invalid_product_should_return_404(
    client,
    invalid_order_data,
    auth_headers,
):
    response = client.post(
        "/orders/",
        json=invalid_order_data,
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_get_user_orders(client, created_order, auth_headers):
    response = client.get(
        "/orders/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == created_order["id"]
    assert data[0]["user_id"] == created_order["user_id"]


def test_get_user_orders_without_token(client):
    response = client.get("/orders/")

    assert response.status_code == 401


def test_update_order_status_authenticated(
    client,
    created_order,
    order_status_data,
    auth_headers,
):
    order_id = created_order["id"]

    response = client.patch(
        f"/orders/{order_id}/status",
        json=order_status_data,
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == order_id
    assert data["status"] == order_status_data["status"]


def test_update_order_status_not_found(
    client,
    order_status_data,
    auth_headers,
):
    response = client.patch(
        "/orders/9999/status",
        json=order_status_data,
        headers=auth_headers,
    )

    assert response.status_code == 404
