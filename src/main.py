from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from src.db_setup import SessionLocal
from src.orm_models import User


def get_all_users(db: Session) -> List[User]:
    """Retrieve all users."""
    # Use list() to satisfy mypy: returns list[User]
    return list(db.execute(select(User)).scalars().all())


def get_user_by_name(db: Session, username: str) -> Optional[User]:
    """Find user by username."""
    return db.execute(
        select(User).where(User.username == username)
    ).scalar_one_or_none()


def insert_user(db: Session, username: str, email: str, age: int) -> None:
    """Insert a new user with error handling."""
    try:
        new_user = User(username=username, email=email, age=age)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"✅ User '{username}' added successfully.")
    except Exception as e:
        db.rollback()
        print(f"❌ Failed to insert user '{username}':", e)


def update_user_age(db: Session, username: str, new_age: int) -> None:
    """Update a user's age."""
    stmt = update(User).where(User.username == username).values(age=new_age)
    result = db.execute(stmt)
    db.commit()

    # Safe check for number of affected rows (for SQLAlchemy 2.x compatibility)
    count = getattr(result, "rowcount", 0)
    if count:
        print(f"✅ Updated '{username}' age to {new_age}.")
    else:
        print(f"⚠️ No user found with username '{username}'.")


def main() -> None:
    """Main workflow for database operations."""
    db = SessionLocal()

    print("\n📋 All users in database:")
    for u in get_all_users(db):
        print(f" - {u}")

    print("\n🔎 Find user 'alice':")
    print(get_user_by_name(db, "alice"))

    print("\n➕ Insert new user:")
    insert_user(db, "david", "david@example.com", 27)

    print("\n✏️ Update user age:")
    update_user_age(db, "bob", 35)

    print("\n📋 Users after changes:")
    for u in get_all_users(db):
        print(f" - {u}")

    db.close()


if __name__ == "__main__":
    main()
