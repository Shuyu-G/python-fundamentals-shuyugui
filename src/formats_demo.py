from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, NamedTuple, TypedDict, Callable, TypeVar
import json
import yaml
import numpy as np
import pandas as pd
import time
from pathlib import Path
from pydantic import BaseModel


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

users = [
    {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com",
        "is_active": True,
        "tags": ["admin", "beta"],
        "profile": {"age": 28, "city": "Berlin"},
    },
    {
        "id": 2,
        "name": "Bob",
        "email": "bob@example.com",
        "is_active": False,
        "tags": [],
        "profile": {"age": 31, "city": "Bremen"},
    },
    {
        "id": 3,
        "name": "Carol",
        "email": "carol@example.com",
        "is_active": True,
        "tags": ["new"],
        "profile": {"age": 24, "city": "Hamburg"},
    },
    {
        "id": 4,
        "name": "Dave",
        "email": "dave@example.com",
        "is_active": True,
        "tags": ["staff"],
        "profile": {"age": 35, "city": "Munich"},
    },
]

with open(DATA_DIR / "users.json", "w", encoding="utf-8") as f:
    json.dump(users, f, indent=2)

with open(DATA_DIR / "users.yaml", "w", encoding="utf-8") as f:
    yaml.dump(users, f)

pd.DataFrame(users).to_csv(DATA_DIR / "users.csv", index=False)

xml_content = "<users>\n"
for u in users:
    xml_content += (
        f'  <user id="{u["id"]}" name="{u["name"]}" email="{u["email"]}" />\n'
    )
xml_content += "</users>"
with open(DATA_DIR / "users.xml", "w", encoding="utf-8") as f:
    f.write(xml_content)


class ProfileTD(TypedDict):
    age: int
    city: str


class UserTD(TypedDict):
    id: int
    name: str
    email: str
    is_active: bool
    tags: List[str]
    profile: ProfileTD


class UserNT(NamedTuple):
    id: int
    name: str
    email: str
    is_active: bool
    tags: List[str]
    profile: Dict[str, Any]


@dataclass
class UserDC:
    id: int
    name: str
    email: str
    is_active: bool
    tags: List[str]
    profile: Dict[str, Any]


class UserModel(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    tags: List[str]
    profile: Dict[str, Any]


R = TypeVar("R")


def timeit(fn: Callable[..., R]) -> Callable[..., R]:
    """Decorator to measure and print execution time of a function."""

    def wrapper(*args: Any, **kwargs: Any) -> R:
        start = time.perf_counter()
        result: R = fn(*args, **kwargs)
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        print(f"{fn.__name__} took {elapsed_ms:.2f} ms")
        return result

    return wrapper


@timeit
def scalar_vec_mul_list(vec: List[float], scalar: float) -> List[float]:
    return [scalar * x for x in vec]


@timeit
def scalar_vec_mul_numpy(vec: np.ndarray, scalar: float) -> np.ndarray:
    return scalar * vec


def demo_pandas_load_csv() -> None:
    print("\n=== Pandas load CSV ===")
    df = pd.read_csv(DATA_DIR / "users.csv")
    print("CSV content:\n", df)


def main() -> None:
    print("\n=== User structures ===")
    print(
        UserTD(
            id=1,
            name="Alice",
            email="alice@example.com",
            is_active=True,
            tags=["admin"],
            profile={"age": 28, "city": "Berlin"},
        )
    )
    print(UserNT(2, "Bob", "bob@example.com", False, [], {"age": 31, "city": "Bremen"}))
    print(
        UserDC(
            3,
            "Carol",
            "carol@example.com",
            True,
            ["new"],
            {"age": 24, "city": "Hamburg"},
        )
    )
    print(
        UserModel(
            id=4,
            name="Dave",
            email="dave@example.com",
            is_active=True,
            tags=["staff"],
            profile={"age": 35, "city": "Munich"},
        )
    )

    print("\n=== Scalar-Vector multiply: Python List vs NumPy ===")
    data_list = list(range(1_000_000))
    data_np = np.arange(1_000_000)
    scalar_vec_mul_list(data_list, 2.5)
    scalar_vec_mul_numpy(data_np, 2.5)

    demo_pandas_load_csv()


if __name__ == "__main__":
    main()
