def test_get_product_not_found_without_token(client):
    response = client.get("/products/9999")

    assert response.status_code == 401


def test_create_product_authenticated(client, product_data, admin_auth_headers):
    response = client.post(
        "/products/",
        json=product_data,
        headers=admin_auth_headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["category"] == product_data["category"]
    assert data["name"] == product_data["name"]
    assert data["price"] == product_data["price"]


def test_create_product_without_token(client, product_data):
    response = client.post(
        "/products/",
        json=product_data,
    )

    assert response.status_code == 401


def test_create_product_without_admin(client, product_data, auth_headers):
    response = client.post(
        "/products/",
        json=product_data,
        headers=auth_headers,
    )

    assert response.status_code == 403


def test_get_product_by_id(client, created_product, auth_headers):
    product_id = created_product["id"]

    response = client.get(
        f"/products/{product_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["category"] == created_product["category"]
    assert data["name"] == created_product["name"]
    assert data["price"] == created_product["price"]


def test_update_product_authenticated(
    client,
    created_product,
    updated_product_data,
    admin_auth_headers,
):
    product_id = created_product["id"]

    response = client.patch(
        f"/products/{product_id}",
        json=updated_product_data,
        headers=admin_auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["category"] == updated_product_data["category"]
    assert data["name"] == updated_product_data["name"]
    assert data["price"] == updated_product_data["price"]


def test_update_product_not_found(client, updated_product_data, admin_auth_headers):
    response = client.patch(
        "/products/9999",
        json=updated_product_data,
        headers=admin_auth_headers,
    )

    assert response.status_code == 404