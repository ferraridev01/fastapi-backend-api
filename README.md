# Products and Orders API

![CI](https://github.com/ferraridev01/fastapi-backend-api/actions/workflows/ci.yml/badge.svg)

Professional REST API built with FastAPI, SQLAlchemy, and PostgreSQL,
featuring JWT authentication, refresh tokens, role-based authorization,
and a robust ordering system.

## Overview

This project is a production-ready backend application focused on:

-   Layered FastAPI architecture (Routers, Services, Models, Schemas)
-   Advanced SQLAlchemy ORM relationships and data integrity
-   JWT Authentication with Access and Refresh Tokens
-   Role-Based Authorization (Admin/User)
-   Dynamic filtering, pagination, and sorting
-   Request Logging Middleware
-   Containerized infrastructure with Docker and Docker Compose

## Tech Stack

-   **Language:** Python
-   **Framework:** FastAPI
-   **ORM:** SQLAlchemy
-   **Database:** PostgreSQL
-   **Security:** Passlib (Bcrypt), Python-jose (JWT)
-   **Validation:** Pydantic v2
-   **Server:** Uvicorn
-   **Containers:** Docker, Docker Compose
- **CI/CD:** GitHub Actions

## Project Structure

``` text
app/
├── core/
│   ├── config.py
│   └── security.py
├── database/
│   └── database.py
├── models/
│   ├── order_model.py
│   ├── product_model.py
│   └── user_model.py
├── routers/
│   ├── auth_router.py
│   ├── order_router.py
│   └── product_router.py
├── schemas/
│   ├── order_schema.py
│   ├── product_schema.py
│   └── user_schema.py
├── services/
│   ├── auth_service.py
│   ├── order_service.py
│   └── product_service.py
└── main.py
```

## 🚀 How to Run the Project

### Environment Configuration

Create a `.env` file in the root directory:

``` env
SECRET_KEY=your_super_secret_jwt_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/products_db
```

### Setup Virtual Environment

``` bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run with Docker Compose

``` bash
docker compose up --build
```

API:

``` text
http://localhost:8000
```

### Run PostgreSQL Container + Local Uvicorn

``` bash
docker run --name products-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=products_db \
  -p 5432:5432 \
  -d postgres:16
```

``` bash
uvicorn app.main:app --reload
```

## API Documentation

-   Swagger UI: `http://localhost:8000/docs`
-   ReDoc: `http://localhost:8000/redoc`

## Features

-   JWT Authentication
-   Refresh Token Flow
-   Role-Based Authorization (Admin/User)
-   Protected Routes
-   Request Logging Middleware
-   Product Filtering
-   Pagination
-   Sorting
-   Partial Updates with PATCH
-   SQLAlchemy Relationships
-   Dockerized Environment

## Authentication Endpoints

### `/auth`

-   `POST /auth/` - Register a new user
-   `POST /auth/login` - Authenticate and receive access and refresh
    tokens
-   `POST /auth/refresh` - Generate a new access token using a valid
    refresh token

## Product Endpoints

### `/products`

Authenticated Users:

-   `GET /products/`
-   `GET /products/{product_id}`

Admin Only:

-   `POST /products/`
-   `PATCH /products/{product_id}`
-   `DELETE /products/{product_id}`

Available query parameters:

-   `?category=Hardware`
-   `?limit=10&skip=0`
-   `?order_by=price`

## Order Endpoints

### `/orders`

-   `POST /orders/` - Create an order
-   `GET /orders/` - List authenticated user orders
-   `PATCH /orders/{order_id}/status` - Update order status

## Security & Authorization

### Authentication

The API uses JWT authentication with:

-   Access Token
-   Refresh Token

Access tokens are used to access protected endpoints.

Refresh tokens are used to obtain a new access token without requiring a
new login.

### Authorization

The API implements role-based authorization.

Roles:

-   User
-   Admin

Permissions:

  Endpoint                User   Admin
  ----------------------- ------ -------
  GET /products           ✓      ✓
  GET /products/{id}      ✓      ✓
  POST /products          ✗      ✓
  PATCH /products/{id}    ✗      ✓
  DELETE /products/{id}   ✗      ✓

## Middleware

A custom HTTP middleware logs:

-   Request Method
-   Request Path
-   Response Status Code
-   Request Execution Time

Example:

``` text
GET /products 200 9.78ms
POST /auth/login 200 206.59ms
```

## Tests and Code Quality
This project includes automated API tests using PyTest and FastAPI TestClient.

Every push and pull request is automatically validated by GitHub Actions through the following pipeline:

- PyTest
- Ruff
- Black
- Docker image build validation

### Test Structure

```text
tests/
├── conftest.py
├── test_auth.py
├── test_products.py
└── test_orders.py
```

### Covered Scenarios

- User Registration
- User Authentication (JWT)
- Product Creation
- Product Retrieval
- Product Update
- Authentication and Authorization Validation
- Order Creation
- Order Listing
- Order Status Update
- Error Handling (401, 403, 404, 422)

### Run Tests

```bash
PYTHONPATH=. pytest
```

### Coverage Report

```bash
PYTHONPATH=. pytest --cov=app --cov-report=term-missing
```

Current coverage:

```text
Coverage: 88%
Tests: 20 passing
```

### Ruff

```bash
ruff check .
ruff format .
```

## Future Improvements

-   Alembic Database Migrations
-   Redis Caching
-   Background Tasks with Celery
-   AWS Deployment

## Author

**Yan Ferrari** - Python Backend Developer