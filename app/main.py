from fastapi import FastAPI, Request
from app.database.database import Base, engine
from app.routers.auth_router import router as auth_router
from app.routers.order_router import router as order_router
from app.routers.product_router import router as product_router
from time import perf_counter


app = FastAPI(title="E-Commerce API", version="1.0.0")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = perf_counter()

    response = await call_next(request)

    duration = perf_counter() - start_time
    duration_ms = round(duration * 1000, 2)

    print(
        f"{request.method} {request.url.path} "
        f"{response.status_code} {duration_ms}ms"
    )

    return response


app.include_router(auth_router)
app.include_router(product_router)
app.include_router(order_router)
