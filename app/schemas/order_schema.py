from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.product_schema import ProductResponse


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(1, ge=1)


class OrderCreate(BaseModel):
    items: list[OrderItemCreate]


class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    product: ProductResponse

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str
    created_at: datetime
    items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)


class OrderStatusUpdate(BaseModel):
    status: Literal[
        "pending",
        "processing",
        "shipped",
        "delivered",
        "cancelled",
    ]