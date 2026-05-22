from fastapi import FastAPI
from app.database.database import Base, engine
from app.routers.auth_router import router as auth_router
from app.routers.order_router import router as order_router
from app.routers.product_router import router as product_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce API", version="1.0.0")

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(order_router)
