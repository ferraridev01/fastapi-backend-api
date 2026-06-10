import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import get_db
from app.main import app as fastapi_app
from app.models.order_model import Order
from app.models.product_model import Product
from app.models.user_model import User
from app.services.auth_service import get_password_hash


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


fastapi_app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    User.metadata.create_all(bind=engine)
    Product.metadata.create_all(bind=engine)
    Order.metadata.create_all(bind=engine)

    yield

    User.metadata.drop_all(bind=engine)
    Product.metadata.drop_all(bind=engine)
    Order.metadata.drop_all(bind=engine)

    engine.dispose()

    if os.path.exists("test_db.db"):
        os.remove("test_db.db")


@pytest.fixture
def client():
    return TestClient(fastapi_app)


@pytest.fixture
def user_data():
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "securepassword123",
    }


@pytest.fixture
def invalid_user_data():
    return {
        "email": "invalid@example.com",
        "username": "baduser",
    }


@pytest.fixture
def login_data(user_data):
    return {
        "username": user_data["username"],
        "password": user_data["password"],
    }


@pytest.fixture
def registered_user(client, user_data):
    response = client.post("/auth/", json=user_data)

    assert response.status_code == 201

    return response.json()


@pytest.fixture
def auth_token(client, registered_user, login_data):
    response = client.post("/auth/login", data=login_data)

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    return {
        "Authorization": f"Bearer {auth_token}",
    }


@pytest.fixture
def admin_password():
    return "securepassword123"


@pytest.fixture
def admin_user(admin_password):
    db = TestingSessionLocal()

    user = User(
        username="adminuser",
        email="admin@example.com",
        hashed_password=get_password_hash(admin_password),
        is_active=True,
        is_admin=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    return user


@pytest.fixture
def admin_login_data(admin_password):
    return {
        "username": "adminuser",
        "password": admin_password,
    }


@pytest.fixture
def admin_auth_token(client, admin_user, admin_login_data):
    response = client.post("/auth/login", data=admin_login_data)

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture
def admin_auth_headers(admin_auth_token):
    return {
        "Authorization": f"Bearer {admin_auth_token}",
    }


@pytest.fixture
def product_data():
    return {
        "category": "Hardware",
        "name": "Keyboard",
        "price": 250,
    }


@pytest.fixture
def updated_product_data():
    return {
        "category": "Hardware",
        "name": "Mechanical Keyboard",
        "price": 400,
    }


@pytest.fixture
def created_product(client, product_data, admin_auth_headers):
    response = client.post(
        "/products/",
        json=product_data,
        headers=admin_auth_headers,
    )

    assert response.status_code == 201

    return response.json()


@pytest.fixture
def order_data(created_product):
    return {
        "items": [
            {
                "product_id": created_product["id"],
                "quantity": 2,
            }
        ]
    }


@pytest.fixture
def invalid_order_data():
    return {
        "items": [
            {
                "product_id": 9999,
                "quantity": 1,
            }
        ]
    }


@pytest.fixture
def order_status_data():
    return {
        "status": "processing",
    }


@pytest.fixture
def created_order(client, order_data, auth_headers):
    response = client.post(
        "/orders/",
        json=order_data,
        headers=auth_headers,
    )

    assert response.status_code == 201

    return response.json()
