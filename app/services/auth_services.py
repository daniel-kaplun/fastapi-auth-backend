from fastapi import HTTPException
from sqlalchemy.exc import (
    IntegrityError,
    SQLAlchemyError
)
from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password
)

from app.models.user import (
    User,
    Registration
)

from app.schemas.auth import UserRegistration


def register_user(
    db: Session,
    user: UserRegistration
):
    """
    Create and store a new user account.
    """

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "User registered successfully"
        }

    except IntegrityError as error:

        # Revert transaction if unique constraints fail
        db.rollback()

        error_message = str(error.orig).lower()

        if "username" in error_message:
            raise HTTPException(
                status_code=400,
                detail="Username already taken"
            )

        if "email" in error_message:
            raise HTTPException(
                status_code=400,
                detail="Email already taken"
            )

        raise HTTPException(
            status_code=500,
            detail="Database integrity error"
        )


def authenticate_user(
    db: Session,
    username: str,
    password: str
):
    """
    Verify user credentials during login.
    """

    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.hashed_password
    ):
        return None

    return user


def save_refresh_token(
    db: Session,
    user_id: int,
    refresh_token: str
):
    """
    Store refresh token for validation and revocation.
    """

    new_token = Registration(
        user_id=user_id,
        refresh_token=refresh_token
    )

    try:
        db.add(new_token)
        db.commit()

    except SQLAlchemyError:

        # Prevent partial database updates
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Could not save refresh token"
        )