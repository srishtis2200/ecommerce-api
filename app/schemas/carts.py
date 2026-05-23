from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from decimal import Decimal
from app.schemas.products import ProductResponse


#Cart Item Schemas

class CartItemAdd(BaseModel):
    product_id: int
    quantity: int = Field(1, gt=0)


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0)


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_at_addition: Decimal
    product: ProductResponse
    created_at: datetime

    model_config = {"from_attributes": True}


#Cart Schemas

class CartResponse(BaseModel):
    id: int
    user_id: int
    items: list[CartItemResponse] = Field(default_factory=list)
    total: Decimal = Decimal("0.00")
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

    @model_validator(mode="after")
    def compute_total(self) -> "CartResponse":
        self.total = sum(
            (item.price_at_addition * item.quantity for item in self.items),
            Decimal("0.00"),
        )
        return self