from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from sqlalchemy import text

DATABASE_URL = "mysql+pymysql://root:example@localhost:3306/demo_db"

# Create engine
engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

# Create session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    """Provide a SQLAlchemy session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT DATABASE()"))
            print("✅ Connected to:", result.scalar())
    except Exception as e:
        print("❌ Connection failed:", e)
