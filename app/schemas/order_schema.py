from datetime import datetime
from pydantic import BaseModel
from app.schemas.product_schema import ProductResponse


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class OrderCreate(BaseModel):
    items: list[OrderItemCreate]


class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    product: ProductResponse

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str
    created_at: datetime
    items: list[OrderItemResponse]

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: str
