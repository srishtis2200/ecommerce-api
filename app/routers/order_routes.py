from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, get_current_admin
from app.models.user import User
from app.schemas.orders import OrderCreate, OrderStatusUpdate, OrderResponse
from app.services import orders as order_service

router = APIRouter(prefix="/orders", tags=["Orders"])


#User endpoints

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Place order from cart",
)
def place_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrderResponse:
    return order_service.place_order(db, current_user.id, payload)


@router.get(
    "/my",
    summary="Get all orders for current user",
)
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[OrderResponse]:
    return order_service.get_my_orders(db, current_user.id)


@router.get(
    "/my/{order_id}",
    summary="Get a single order for current user",
)
def get_my_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrderResponse:
    return order_service.get_my_order(db, current_user.id, order_id)


#Admin endpoints

@router.get(
    "",
    summary="[Admin] Get all orders",
)
def get_all_orders(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> list[OrderResponse]:
    return order_service.get_all_orders(db)


@router.patch(
    "/{order_id}/status",
    summary="[Admin] Update order status",
)
def update_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> OrderResponse:
    return order_service.update_order_status(db, order_id, payload)