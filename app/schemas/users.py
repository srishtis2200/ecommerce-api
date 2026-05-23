from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

from app.models.user import UserRole


#Address Schemas

class AddressCreate(BaseModel):
    house_no: str = Field(..., max_length=50)
    street: str = Field(..., max_length=150)
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)
    pincode: str = Field(..., max_length=10)
    is_default: bool = False


class AddressResponse(BaseModel):
    id: int
    house_no: str
    street: str
    city: str
    state: str
    pincode: str
    is_default: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


#User Schemas

class UserCreate(BaseModel):
    name: str = Field(..., max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    phone: Optional[str] = Field(None, max_length=15)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=15)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    role: UserRole
    is_active: bool
    created_at: datetime
    addresses: list[AddressResponse] = Field(default_factory=list)

    model_config = {
        "from_attributes": True
    }


#Token Schemas

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[UserRole] = None