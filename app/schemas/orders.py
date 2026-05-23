from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models.order import OrderStatus, PaymentStatus
from app.schemas.products import ProductResponse


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_at_purchase: Decimal
    product: ProductResponse
    created_at: datetime

    model_config = {"from_attributes": True}


class OrderCreate(BaseModel):
    address_id: int
    notes: Optional[str] = Field(None, max_length=500)


class OrderStatusUpdate(BaseModel):
    order_status: OrderStatus


class OrderResponse(BaseModel):
    id: int
    user_id: int
    delivery_address: str
    total_amount: Decimal
    order_status: OrderStatus
    payment_status: PaymentStatus
    notes: Optional[str]
    items: list[OrderItemResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}