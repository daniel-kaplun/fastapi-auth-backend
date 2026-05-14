from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine for MySQL connection
engine = create_engine(DATABASE_URL)

# Database session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for ORM models
Base = declarative_base()


def get_db():
    """
    Provides a database session for each request.
    Session automatically closes after request completes.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()