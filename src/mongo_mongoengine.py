from __future__ import annotations

from typing import List, Optional

from mongoengine import (
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ListField,
    StringField,
    IntField,
    BooleanField,
    connect,
    NotUniqueError,
)

MONGO_URI = "mongodb://appuser:apppass@localhost:27017/appdb?authSource=appdb"


class Profile(EmbeddedDocument):
    full_name = StringField(required=True)
    age = IntField(required=True, min_value=0)
    city = StringField(required=True)


class User(Document):
    meta = {"collection": "users"}  # 与 PyMongo 使用同集合
    username = StringField(required=True, unique=True)
    email = StringField(required=True)
    profile = EmbeddedDocumentField(Profile, required=True)
    tags = ListField(StringField(), default=list)
    active = BooleanField(default=True)


def connect_db() -> None:
    connect(host=MONGO_URI, alias="default")


def create_user_idempotent(
    username: str, email: str, full_name: str, age: int, city: str
) -> str:
    created = User.objects(username=username).modify(
        upsert=True,
        new=True,
        set_on_insert__email=email,
        set_on_insert__profile=Profile(full_name=full_name, age=age, city=city),
        set_on_insert__tags=[],
        set_on_insert__active=True,
    )

    return str(created.id)


def get_user(username: str) -> Optional[User]:
    return User.objects(username=username).first()


def find_users_in_city(city: str) -> List[User]:
    return list(User.objects(profile__city=city))


def add_tag(username: str, tag: str) -> int:
    res = User.objects(username=username).update_one(add_to_set__tags=tag)
    return res


def update_city(username: str, new_city: str) -> int:
    res = User.objects(username=username).update_one(set__profile__city=new_city)
    return res


def deactivate_user(username: str) -> int:
    res = User.objects(username=username).update_one(set__active=False)
    return res


def main() -> None:
    connect_db()

    print("count:", User.objects.count())

    uid = create_user_idempotent(
        "david", "david@example.com", "David Sun", 27, "Hamburg"
    )
    print("idempotent create id:", uid)
    uid2 = create_user_idempotent(
        "david", "ignored@example.com", "Ignored Name", 99, "IgnoredCity"
    )
    print("idempotent create (again) id:", uid2)

    u = get_user("david")
    if u:
        print(
            "david:",
            {
                "username": u.username,
                "email": u.email,
                "city": u.profile.city,
                "tags": u.tags,
                "active": u.active,
            },
        )

    print("add tag:", add_tag("david", "pro"))
    print("update city:", update_city("david", "Berlin"))
    print("deactivate:", deactivate_user("david"))

    after = get_user("david")
    if after:
        print(
            "after:",
            {
                "username": after.username,
                "city": after.profile.city,
                "tags": after.tags,
                "active": after.active,
            },
        )

    berlin_users = [u.username for u in find_users_in_city("Berlin")]
    print("city Berlin:", berlin_users)


if __name__ == "__main__":
    try:
        main()
    except NotUniqueError as e:
        print("NotUniqueError:", e)
