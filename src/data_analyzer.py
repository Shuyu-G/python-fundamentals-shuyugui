import sys
from typing import Dict, List, Optional, Tuple

from src.utils import hallo


def to_ints(items: List[str]) -> List[Optional[int]]:
    """Try to convert strings to integers; return None if not possible."""
    out: List[Optional[int]] = []
    for s in items:
        try:
            out.append(int(s))
        except ValueError:
            out.append(None)
    return out


def main() -> None:
    title: str = "Data Analyzer"
    version: int = 1
    person: Dict[str, str] = {"name": "Shuyu", "role": "student"}
    coords: Tuple[int, int] = (3, 5)
    print("Coords tuple:", coords)

    numbers_raw: List[str] = (
        sys.argv[1:] if len(sys.argv) > 1 else ["10", "20", "abc", "30"]
    )
    print(f"{title} v{version}")
    print(hallo(person["name"]))

    maybe_ints: List[Optional[int]] = to_ints(numbers_raw)
    print("Casted:", maybe_ints)

    for i, v in enumerate(maybe_ints):
        print(f"item[{i}] = {v}")

    if None in maybe_ints:
        print("There were invalid numbers.")
    elif len(maybe_ints) > 5:
        print("Many numbers.")
    else:
        print("All valid and short list.")

    doubled: List[int] = []
    idx = 0
    while idx < len(maybe_ints):
        val = maybe_ints[idx]
        if val is not None:
            doubled.append(val * 2)
        idx += 1
    print("Doubled:", doubled)

    print("range example:", list(range(3)))
    print("id(doubled):", id(doubled))


if __name__ == "__main__":
    main()
