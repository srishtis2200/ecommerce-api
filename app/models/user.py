from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Enum,
    ForeignKey
)

from sqlalchemy.orm import relationship
from app.database import Base

from datetime import datetime, timezone
import enum

# Enum for user roles

class UserRole(str, enum.Enum):
    admin = "admin"
    customer = "customer"


# User Model

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    name = Column(String(100), nullable=False)

    email = Column(String(100), unique=True, index=True, nullable=False)

    password = Column(String(255), nullable=False)

    phone = Column(String(15), nullable=True)

    role = Column(
        Enum(UserRole, name="user_roles"),
        default=UserRole.customer,
        nullable=False
    )

    is_active = Column(Boolean, default=True)

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
    addresses = relationship(
        "Address",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    cart = relationship(
        "Cart",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    orders = relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"


# Address Model

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    house_no = Column(String(50), nullable=False)

    street = Column(String(150), nullable=False)

    city = Column(String(100), nullable=False)

    state = Column(String(100), nullable=False)

    pincode = Column(String(10), nullable=False)

    is_default = Column(Boolean, default=False)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    # Relationship
    user = relationship(
        "User",
        back_populates="addresses"
    )

    def __repr__(self):
        return f"<Address(id={self.id}, city={self.city})>"