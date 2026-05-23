from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.users import (
    UserCreate,
    UserResponse,
    UserLogin,
    Token
)
from app.services.auth import (
    register_user,
    login_user
)
from app.dependencies import get_current_user
from app.models.user import User


#Router
router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


#Register User
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    return register_user(db, user_data)


#Login User (JSON) — for API clients 
@router.post(
    "/login",
    response_model=Token
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    token = login_user(
        db,
        user_data.email,
        user_data.password
    )
    return {
        "access_token": token,
        "token_type": "bearer"
    }


#Login User (Form) — for Swagger UI Authorize button
@router.post(
    "/login/form",
    response_model=Token,
    include_in_schema=False
)
def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    token = login_user(
        db,
        form_data.username,
        form_data.password
    )
    return {
        "access_token": token,
        "token_type": "bearer"
    }


#Current Logged-in User
@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user