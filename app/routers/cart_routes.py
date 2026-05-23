from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.carts import CartItemAdd, CartItemUpdate, CartResponse
from app.services import carts as cart_service

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post(
    "/items",
    status_code=status.HTTP_200_OK,
    summary="Add item to cart",
)
def add_item(
    payload: CartItemAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CartResponse:
    return cart_service.add_item(db, current_user.id, payload)


@router.get(
    "",
    summary="View cart with total",
)
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CartResponse:
    return cart_service.get_cart(db, current_user.id)


@router.patch(
    "/items/{item_id}",
    summary="Update quantity of a cart item",
)
def update_item(
    item_id: int,
    payload: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CartResponse:
    return cart_service.update_item(db, current_user.id, item_id, payload)


@router.delete(
    "/items/{item_id}",
    summary="Remove a single item from cart",
)
def remove_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CartResponse:
    return cart_service.remove_item(db, current_user.id, item_id)


@router.delete(
    "",
    status_code=status.HTTP_200_OK,
    summary="Clear all items from cart",
)
def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    return cart_service.clear_cart(db, current_user.id)