from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.order_model import Order, OrderItem
from app.models.product_model import Product
from app.schemas.order_schema import OrderCreate


async def create_order(db: Session, order_data: OrderCreate, user_id: int) -> Order:
    for item in order_data.items:
        product_exists = db.query(Product).filter(Product.id == item.product_id).first()
        if not product_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {item.product_id} not found",
            )

    db_order = Order(user_id=user_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order_data.items:
        db_item = OrderItem(
            order_id=db_order.id, product_id=item.product_id, quantity=item.quantity
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_order)
    return db_order


async def get_user_orders(db: Session, user_id: int) -> list[Order]:
    return db.query(Order).filter(Order.user_id == user_id).all()


async def update_order_status(
    db: Session, order_id: int, new_status: str, user_id: int
) -> Order | None:
    db_order = (
        db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    )
    if not db_order:
        return None

    db_order.status = new_status
    db.commit()
    db.refresh(db_order)
    return db_order
