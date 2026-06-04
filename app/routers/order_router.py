from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.database.database import get_db
from app.models.user_model import User
from app.schemas.order_schema import OrderCreate, OrderResponse, OrderStatusUpdate
from app.services.order_service import (
    create_order,
    get_user_orders,
    update_order_status,
)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderResponse)
async def create_new_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_order(db, order_data=order_data, user_id=current_user.id)


@router.get("/", response_model=list[OrderResponse])
async def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_user_orders(db, user_id=current_user.id)


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def change_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await update_order_status(
        db,
        order_id=order_id,
        new_status=status_data.status,
        user_id=current_user.id,
    )