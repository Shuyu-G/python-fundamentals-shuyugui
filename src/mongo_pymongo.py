from __future__ import annotations

from typing import Any, Dict, List, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError

MONGO_URI = "mongodb://appuser:apppass@localhost:27017/appdb?authSource=appdb"

_client: Optional[MongoClient] = None


def client() -> MongoClient:
    """Get (and cache) a MongoClient."""
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    return _client


def db() -> Database:
    """Return target database."""
    return client().get_database("appdb")


def users() -> Collection:
    """Return users collection."""
    return db().get_collection("users")


def create_user(
    username: str,
    email: str,
    full_name: str,
    age: int,
    city: str,
) -> str:
    """Insert a user; if duplicate username, reuse existing _id."""
    doc: Dict[str, Any] = {
        "username": username,
        "email": email,
        "profile": {"full_name": full_name, "age": age, "city": city},
        "tags": ["a", "x"],
        "active": True,
    }
    try:
        res = users().insert_one(doc)
        return str(res.inserted_id)
    except DuplicateKeyError:
        found = users().find_one({"username": username}, {"_id": 1})
        if found and "_id" in found:
            print(
                f"[duplicate] username '{username}' exists, "
                f"reuse _id={found['_id']}"
            )
            return str(found["_id"])
        raise


def get_user(username: str) -> Optional[Dict[str, Any]]:
    return users().find_one({"username": username}, {"_id": 0})


def find_users_in_city(city: str) -> List[Dict[str, Any]]:
    cur = users().find(
        {"profile.city": city},
        {"_id": 0, "username": 1, "email": 1},
    )
    return list(cur)


def add_tag(username: str, tag: str) -> int:
    """Add tag only if not exists; returns matched/modified count (0 or 1)."""
    res = users().update_one({"username": username}, {"$addToSet": {"tags": tag}})

    return int(res.modified_count)


def update_city(username: str, new_city: str) -> int:
    res = users().update_one(
        {"username": username},
        {"$set": {"profile.city": new_city}},
    )
    return int(res.modified_count)


def deactivate_user(username: str) -> int:
    res = users().update_one(
        {"username": username},
        {"$set": {"active": False}},
    )
    return int(res.modified_count)


def main() -> None:
    pong = db().command("ping")
    print("ping ok:", bool(pong.get("ok", 0)))

    new_id = create_user(
        "carol",
        "carol@example.com",
        "Carol Kim",
        22,
        "Munich",
    )
    print("insert id:", new_id)

    alice = get_user("alice")
    if alice:
        print("alice:", alice)

    berlin = find_users_in_city("Berlin")
    print("city Berlin:", berlin)

    print("add tag:", add_tag("alice", "pro"))
    print("update city:", update_city("alice", "Cologne"))
    print("deactivate:", deactivate_user("alice"))


if __name__ == "__main__":
    main()
