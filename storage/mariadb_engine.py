from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DB_USER = "demo_user"
DB_PASS = "demo_pass"
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "demo_db"


class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models."""


engine = create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    connect_args={
        "charset": "utf8mb4",
        "collation": "utf8mb4_general_ci",  # MariaDB supports this
    },
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_session() -> Generator:
    """Yield a DB session (useful later for FastAPI style)."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
