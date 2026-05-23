from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.schemas.carts import CartItemAdd, CartItemUpdate, CartResponse


# ── Private helpers ───────────────────────────────────────────────────────────

def _get_or_create_cart(db: Session, user_id: int) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


def _get_active_product(db: Session, product_id: int) -> Product:
    product = (
        db.query(Product)
        .filter(
            Product.id == product_id,
            Product.is_active == True,
        )
        .first()
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or unavailable.",
        )
    return product


def _get_cart_item(db: Session, cart_id: int, item_id: int) -> CartItem:
    item = (
        db.query(CartItem)
        .filter(
            CartItem.id == item_id,
            CartItem.cart_id == cart_id,
        )
        .first()
    )
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found.",
        )
    return item


# ── Service functions ─────────────────────────────────────────────────────────

def add_item(db: Session, user_id: int, payload: CartItemAdd) -> CartResponse:
    product = _get_active_product(db, payload.product_id)

    if product.stock < payload.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only {product.stock} unit(s) in stock.",
        )

    cart = _get_or_create_cart(db, user_id)

    # If product already in cart, increment quantity
    existing = (
        db.query(CartItem)
        .filter(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product.id,
        )
        .first()
    )

    if existing:
        new_qty = existing.quantity + payload.quantity
        if new_qty > product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Cannot add {payload.quantity} more — only "
                    f"{product.stock - existing.quantity} unit(s) left."
                ),
            )
        existing.quantity = new_qty
        existing.price_at_addition = product.price  # refresh price snapshot
    else:
        item = CartItem(
            cart_id=cart.id,
            product_id=product.id,
            quantity=payload.quantity,
            price_at_addition=product.price,
        )
        db.add(item)

    db.commit()
    db.refresh(cart)
    return CartResponse.model_validate(cart)


def get_cart(db: Session, user_id: int) -> CartResponse:
    cart = _get_or_create_cart(db, user_id)
    return CartResponse.model_validate(cart)


def update_item(
    db: Session,
    user_id: int,
    item_id: int,
    payload: CartItemUpdate,
) -> CartResponse:
    cart = _get_or_create_cart(db, user_id)
    item = _get_cart_item(db, cart.id, item_id)
    product = _get_active_product(db, item.product_id)

    if payload.quantity > product.stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only {product.stock} unit(s) in stock.",
        )

    item.quantity = payload.quantity
    item.price_at_addition = product.price  # refresh price snapshot

    db.commit()
    db.refresh(cart)
    return CartResponse.model_validate(cart)


def remove_item(db: Session, user_id: int, item_id: int) -> CartResponse:
    cart = _get_or_create_cart(db, user_id)
    item = _get_cart_item(db, cart.id, item_id)

    db.delete(item)
    db.commit()
    db.refresh(cart)
    return CartResponse.model_validate(cart)


def clear_cart(db: Session, user_id: int) -> dict:
    cart = _get_or_create_cart(db, user_id)

    # Delete via ORM so cascade/events fire correctly
    for item in cart.items:
        db.delete(item)

    db.commit()
    return {"detail": "Cart cleared successfully."}