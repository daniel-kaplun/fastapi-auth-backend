from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    TIMESTAMP,
    func
)

from app.database.db import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)

    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    # Store hashed password instead of plaintext credentials
    hashed_password = Column(
        String(255),
        nullable=False
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )


class Registration(Base):
    __tablename__ = "registration"

    token_id = Column(Integer, primary_key=True)

    # Delete refresh tokens if associated user is removed
    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    refresh_token = Column(
        String(255),
        nullable=False
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )