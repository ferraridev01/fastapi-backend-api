from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.product_model import Product
from app.schemas.product_schema import ProductCreate


async def create_product(product: ProductCreate, db: Session) -> Product:
    db_product = Product(
        category=product.category, name=product.name, price=product.price
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


async def get_all_products(
    db: Session,
    category: str | None = None,
    limit: int = 10,
    skip: int = 0,
    order_by: str | None = None,
) -> list[Product]:
    query = db.query(Product)

    if category:
        query = query.filter(Product.category == category)

    if order_by and hasattr(Product, order_by):
        query = query.order_by(getattr(Product, order_by))

    return query.offset(skip).limit(limit).all()


async def get_product_by_id(product_id: int, db: Session) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )
    return product


async def update_product(
    product_id: int, product: ProductCreate, db: Session
) -> Product:
    db_product = await get_product_by_id(product_id, db)

    db_product.category = product.category
    db_product.name = product.name
    db_product.price = product.price

    db.commit()
    db.refresh(db_product)
    return db_product


async def delete_product(product_id: int, db: Session) -> Product:
    db_product = await get_product_by_id(product_id, db)

    db.delete(db_product)
    db.commit()
    return db_product
