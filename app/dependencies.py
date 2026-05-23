from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User, UserRole
from app.services.auth import decode_access_token
from app.schemas.users import TokenData

#OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/form")


#Get Current Logged-in User
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:

    # Decode JWT token
    token_data: TokenData = decode_access_token(token)

    # Find user in database
    user = db.query(User).filter(User.id == token_data.user_id).first()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    return user


#Admin-only Dependency
def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:

    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user