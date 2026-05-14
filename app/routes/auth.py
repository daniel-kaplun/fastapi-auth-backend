import os

import jwt
from dotenv import load_dotenv
from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session

from app.core.security import (
    ALGORITHM,
    create_access_token,
    create_refresh_token
)

from app.database.db import get_db

from app.models.user import Registration

from app.schemas.auth import (
    UserLogin,
    UserRegistration
)

from app.services.auth_service import (
    authenticate_user,
    register_user,
    save_refresh_token
)

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    user: UserRegistration,
    db: Session = Depends(get_db)
):
    return register_user(db, user)


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and issue JWT tokens.
    """

    verified_user = authenticate_user(
        db,
        user.username,
        user.password
    )

    if not verified_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        user_id=verified_user.user_id,
        username=verified_user.username
    )

    refresh_token = create_refresh_token(
        user_id=verified_user.user_id,
        username=verified_user.username
    )

    save_refresh_token(
        db,
        verified_user.user_id,
        refresh_token
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@router.post("/refresh")
def refresh_access_token(
    jwt_token: str,
    db: Session = Depends(get_db)
):
    """
    Validate refresh token and issue a new access token.
    """

    try:
        payload = jwt.decode(
            jwt_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")
        username = payload.get("username")

        # Ensure refresh token exists in database
        token_exists = (
            db.query(Registration)
            .filter_by(
                user_id=user_id,
                refresh_token=jwt_token
            )
            .first()
        )

        if not token_exists:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

        new_access_token = create_access_token(
            user_id=user_id,
            username=username
        )

        return {
            "access_token": new_access_token
        }

    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=401,
            detail="Refresh token expired"
        )

    except jwt.InvalidTokenError:

        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )