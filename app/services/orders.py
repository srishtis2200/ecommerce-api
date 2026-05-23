from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from decimal import Decimal

from app.models.order import Order, OrderItem, OrderStatus
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.models.user import Address
from app.schemas.orders import OrderCreate, OrderStatusUpdate, OrderResponse


# ── Private helpers ───────────────────────────────────────────────────────────

def _get_user_address(db: Session, address_id: int, user_id: int) -> Address:
    address = (
        db.query(Address)
        .filter(
            Address.id == address_id,
            Address.user_id == user_id,
        )
        .first()
    )
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found.",
        )
    return address


def _get_user_cart(db: Session, user_id: int) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart or not cart.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty. Add items before placing an order.",
        )
    return cart


def _get_order(db: Session, order_id: int) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found.",
        )
    return order


def _build_address_snapshot(address: Address) -> str:
    """Flatten address fields into a single string snapshot."""
    parts = [
        address.house_no,
        address.street,
        address.city,
        address.state,
        address.pincode,
    ]
    return ", ".join(str(p) for p in parts if p)


# ── Service functions ─────────────────────────────────────────────────────────

def place_order(db: Session, user_id: int, payload: OrderCreate) -> OrderResponse:
    # 1. Validate address belongs to user
    address = _get_user_address(db, payload.address_id, user_id)

    # 2. Validate cart is not empty
    cart = _get_user_cart(db, user_id)

    # 3. Validate stock for all items before touching anything
    for cart_item in cart.items:
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()
        if not product or not product.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product ID {cart_item.product_id} is no longer available.",
            )
        if product.stock < cart_item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"'{product.name}' only has {product.stock} unit(s) in stock, "
                    f"but {cart_item.quantity} requested."
                ),
            )

    # 4. Calculate total
    total = sum(
        cart_item.price_at_addition * cart_item.quantity
        for cart_item in cart.items
    )

    # 5. Create order
    order = Order(
        user_id=user_id,
        delivery_address=_build_address_snapshot(address),
        total_amount=total,
        order_status=OrderStatus.pending,
        notes=payload.notes,
    )
    db.add(order)
    db.flush()  # get order.id without committing

    # 6. Create order items + decrement stock
    for cart_item in cart.items:
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()

        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price_at_purchase=cart_item.price_at_addition,
        )
        db.add(order_item)

        product.stock -= cart_item.quantity

    # 7. Clear cart
    for cart_item in cart.items:
        db.delete(cart_item)

    db.commit()
    db.refresh(order)
    return OrderResponse.model_validate(order, from_attributes=True)


def get_my_orders(db: Session, user_id: int) -> list[OrderResponse]:
    orders = (
        db.query(Order)
        .filter(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return [OrderResponse.model_validate(o, from_attributes=True) for o in orders]


def get_my_order(db: Session, user_id: int, order_id: int) -> OrderResponse:
    order = _get_order(db, order_id)
    if order.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied.",
        )
    return OrderResponse.model_validate(order, from_attributes=True)


def get_all_orders(db: Session) -> list[OrderResponse]:
    orders = (
        db.query(Order)
        .order_by(Order.created_at.desc())
        .all()
    )
    return [OrderResponse.model_validate(o, from_attributes=True) for o in orders]


def update_order_status(
    db: Session,
    order_id: int,
    payload: OrderStatusUpdate,
) -> OrderResponse:
    order = _get_order(db, order_id)
    order.order_status = payload.order_status
    db.commit()
    db.refresh(order)
    return OrderResponse.model_validate(order, from_attributes=True)