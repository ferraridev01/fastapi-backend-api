import os

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import get_db
from app.main import app as fastapi_app
from app.models.order_model import Order
from app.models.product_model import Product
from app.models.user_model import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


fastapi_app.dependency_overrides[get_db] = override_get_db

client = TestClient(fastapi_app)


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


def test_register_user_success():
    response = client.post(
        "/auth/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "securepassword123",
        },
    )
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
    assert "id" in response.json()


def test_get_product_not_found():
    response = client.get("/products/9999")
    assert response.status_code == 401


def test_get_order_not_found_should_return_404():
    response = client.get("/orders/9999")
    assert response.status_code == 404


def test_register_user_invalid_data_should_return_422():
    response = client.post(
        "/auth/",
        json={
            "email": "invalid@example.com",
            "username": "baduser",
        },
    )
    assert response.status_code == 422