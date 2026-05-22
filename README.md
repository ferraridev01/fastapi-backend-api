# Products and Orders API

Professional REST API built with FastAPI, SQLAlchemy, and PostgreSQL, featuring secure JWT authentication and a robust ordering system.

## Overview

This project is a production-ready backend application focused on:
- Layered FastAPI architecture (Routers, Services, Models, Schemas)
- Advanced SQLAlchemy ORM relationships and data integrity
- Secure user authentication and authorization using JWT
- Dynamic filtering, pagination, and sorting
- Containerized database infrastructure with Docker

## Tech Stack

- **Language:** Python
- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL
- **Security:** Passlib (Bcrypt), Python-jose (JWT)
- **Validation:** Pydantic v2
- **Server:** Uvicorn

## Project Structure

```text
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

### 💻 Local Development

### 1. Environment Configuration

Create a `.env` file in the root directory:

```env
SECRET_KEY=your_super_secret_jwt_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/products_db
```

### 2. Setup Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
```

#### Option 1: Full Environment with Docker Compose (Recommended)

This command starts both the FastAPI application and a local PostgreSQL database inside containers:

```bash
docker compose up --build
```

The API will be available at:

```txt
http://localhost:8000
```

#### Option 2: Running Application with Docker Run

If you already have a PostgreSQL instance running locally on your machine:

```bash
docker build -t fastapi-app .

docker run -p 8000:8000 \
  --env DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/products_db \
  fastapi-app
```

The API will be available at:

```txt
http://localhost:8000
```

#### Option 3: Manual PostgreSQL Container + Local Uvicorn

If you want to run only PostgreSQL in Docker and run the API directly with Uvicorn:

```bash
docker run --name products-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=products_db \
  -p 5432:5432 \
  -d postgres:16
```

Then start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

### ☁️ Production Deploy (Render)

This project is configured for seamless deployment on Render.

**Database**
- Provision a managed PostgreSQL instance on Render.

**Web Service**
- Connect this GitHub repository.
- Render will automatically detect the Dockerfile to build and deploy the container.

**Environment Variables**
- Inject the `DATABASE_URL` provided by Render into the Web Service settings.
- Inject `SECRET_KEY`, `ALGORITHM`, and `ACCESS_TOKEN_EXPIRE_MINUTES` into the Web Service settings.

## API Documentation

Once the application is running, access the interactive documentation at:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## Features & Endpoints

### Authentication (`/auth`)
- `POST /auth/` - Register a new user
- `POST /auth/login` - Authenticate user and receive JWT bearer token

### Products (`/products`) - *Requires Authentication*
- `POST /products/` - Create a new product
- `GET /products/` - List products with optional queries:
  - **Filter:** `?category=Hardware`
  - **Pagination:** `?limit=10&skip=0`
  - **Sorting:** `?order_by=price`
- `GET /products/{product_id}` - Fetch a specific product by ID
- `PUT /products/{product_id}` - Update product details
- `DELETE /products/{product_id}` - Remove a product

### Orders (`/orders`) - *Requires Authentication*
- `POST /orders/` - Place a new order containing multiple items
- `GET /orders/` - Retrieve orders belonging to the authenticated user
- `PATCH /orders/{order_id}/status` - Update order progression status

## 🧪 Tests and Code Quality

### 1. Install Dependencies

Ensure you have installed all development dependencies inside your virtual environment:

```bash
pip install pytest httpx ruff
```

### 2. Running Tests

To run the automated test suite, use the following command from the project root:

```bash
PYTHONPATH=. pytest
```

### 3. Code Linting and Formatting

To check code style guidelines (PEP 8) and format files automatically using Ruff:

#### Check code rules

```bash
ruff check .
```

#### Format code automatically

```bash
ruff format .
```

## Future Improvements

- Implementation of database migrations using Alembic
- Containerizing the entire application context using Docker Compose
- Continuous Integration and Continuous Deployment (CI/CD) pipelines

## Author

**Yan Ferrari** - Backend & Automation Software Engineer Specialist.
