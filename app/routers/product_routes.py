from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_admin
from app.schemas.products import (
    CategoryCreate, CategoryUpdate, CategoryResponse,
    ProductCreate, ProductUpdate, ProductResponse
)
from app.services.products import (
    create_category, get_all_categories, get_category_by_id,
    update_category, delete_category,
    create_product, get_all_products, get_product_by_id,
    update_product, delete_product
)

router = APIRouter(tags=["Products"])


#Category Routes

@router.post(
    "/categories",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED
)
def add_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return create_category(db, data)


@router.get(
    "/categories",
    response_model=list[CategoryResponse]
)
def list_categories(db: Session = Depends(get_db)):
    return get_all_categories(db)


@router.get(
    "/categories/{category_id}",
    response_model=CategoryResponse
)
def get_category(category_id: int, db: Session = Depends(get_db)):
    return get_category_by_id(db, category_id)


@router.put(
    "/categories/{category_id}",
    response_model=CategoryResponse
)
def edit_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return update_category(db, category_id, data)


@router.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_200_OK
)
def remove_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return delete_category(db, category_id)


#Product Routes

@router.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def add_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return create_product(db, data)


@router.get(
    "/products",
    response_model=list[ProductResponse]
)
def list_products(
    db: Session = Depends(get_db),
    category_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    in_stock: Optional[bool] = Query(None)
):
    return get_all_products(db, category_id, min_price, max_price, in_stock)


@router.get(
    "/products/{product_id}",
    response_model=ProductResponse
)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return get_product_by_id(db, product_id)


@router.put(
    "/products/{product_id}",
    response_model=ProductResponse
)
def edit_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return update_product(db, product_id, data)


@router.delete(
    "/products/{product_id}",
    status_code=status.HTTP_200_OK
)
def remove_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return delete_product(db, product_id)