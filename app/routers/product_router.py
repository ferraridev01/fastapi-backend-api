from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.security import get_current_admin_user, get_current_user
from app.database.database import get_db
from app.models.user_model import User
from app.schemas.product_schema import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import (
    create_product,
    delete_product,
    get_all_products,
    get_product_by_id,
    update_product,
)

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
async def create_new_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_admin_user),
):
    return await create_product(product, db)


@router.get("/", response_model=list[ProductResponse])
async def get_products(
    db: Session = Depends(get_db),
    category: str | None = None,
    limit: int = Query(default=10, ge=1, le=100),
    skip: int = Query(default=0, ge=0),
    order_by: str | None = None,
    _current_user: User = Depends(get_current_user),
):
    return await get_all_products(db, category, limit, skip, order_by)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return await get_product_by_id(product_id, db)


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_existing_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_admin_user),
):
    return await update_product(product_id, product, db)


@router.delete("/{product_id}", response_model=ProductResponse)
async def delete_existing_product(
    product_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_admin_user),
):
    return await delete_product(product_id, db)
