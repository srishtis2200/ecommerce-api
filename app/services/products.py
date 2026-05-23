from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.product import Product, Category
from app.schemas.products import (
    CategoryCreate, CategoryUpdate,
    ProductCreate, ProductUpdate
)


# ── Category Services ──────────────────────────────────────────────────────────

def create_category(db: Session, data: CategoryCreate) -> Category:
    existing = db.query(Category).filter(Category.name == data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists"
        )
    category = Category(
        name=data.name,
        description=data.description
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_all_categories(db: Session) -> list[Category]:
    return db.query(Category).filter(Category.is_active == True).all()


def get_category_by_id(db: Session, category_id: int) -> Category:
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.is_active == True
    ).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category


def update_category(db: Session, category_id: int, data: CategoryUpdate) -> Category:
    category = get_category_by_id(db, category_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int) -> dict:
    category = get_category_by_id(db, category_id)
    category.is_active = False
    db.commit()
    return {"message": "Category deleted successfully"}


# ── Product Services ───────────────────────────────────────────────────────────

def create_product(db: Session, data: ProductCreate) -> Product:
    # Verify category exists
    get_category_by_id(db, data.category_id)
    product = Product(
        name=data.name,
        description=data.description,
        price=data.price,
        stock=data.stock,
        image_url=data.image_url,
        category_id=data.category_id
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_all_products(
    db: Session,
    category_id: int = None,
    min_price: float = None,
    max_price: float = None,
    in_stock: bool = None
) -> list[Product]:
    query = db.query(Product).filter(Product.is_active == True)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if in_stock:
        query = query.filter(Product.stock > 0)
    return query.all()


def get_product_by_id(db: Session, product_id: int) -> Product:
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_active == True
    ).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


def update_product(db: Session, product_id: int, data: ProductUpdate) -> Product:
    product = get_product_by_id(db, product_id)
    if data.category_id:
        get_category_by_id(db, data.category_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> dict:
    product = get_product_by_id(db, product_id)
    product.is_active = False
    db.commit()
    return {"message": "Product deleted successfully"}