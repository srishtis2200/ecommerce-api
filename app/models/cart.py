from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Numeric,
    UniqueConstraint
)

from sqlalchemy.orm import relationship
from app.database import Base

from datetime import datetime, timezone



# Cart Model (One Cart Per User)

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
        index=True
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    user = relationship(
        "User",
        back_populates="cart"
    )

    items = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Cart(id={self.id}, user_id={self.user_id})>"



# Cart Item Model

class CartItem(Base):
    __tablename__ = "cart_items"

    # Prevent duplicate products in same cart
    __table_args__ = (
        UniqueConstraint(
            "cart_id",
            "product_id",
            name="unique_cart_product"
        ),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    cart_id = Column(
        Integer,
        ForeignKey("carts.id"),
        nullable=False,
        index=True
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False,
        index=True
    )

    quantity = Column(
        Integer,
        default=1,
        nullable=False
    )

    # Snapshot of product price when added
    price_at_addition = Column(
        Numeric(10, 2),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    cart = relationship(
        "Cart",
        back_populates="items"
    )

    product = relationship(
        "Product",
        back_populates="cart_items"
    )

    def __repr__(self):
        return (
            f"<CartItem(id={self.id}, "
            f"product_id={self.product_id}, "
            f"quantity={self.quantity})>"
        )