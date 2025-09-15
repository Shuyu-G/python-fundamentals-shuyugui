from typing import List, Optional, Dict, Tuple
from utils import hallo
import sys
def to_ints(items: List[str]) -> List[Optional[int]]:
    # Try to convert strings to integers; return None if not possible
    out: List[Optional[int]] = []
    for s in items:
        try:
            out.append(int(s))
        except ValueError:
            out.append(None)
    return out

def main() -> None:
    # Variables
    title: str = "Data Analyzer"
    version: int = 1
    person: Dict[str, str] = {"name": "Shuyu", "role": "student"}
    coords: Tuple[int, int] = (3, 5)
    numbers_raw: List[str] = sys.argv[1:] if len(sys.argv) > 1 else ["10", "20", "abc", "30"]

    # Import from utils.py
    print(f"{title} v{version}")
    print(hallo(person["name"]))

    # String to int casting
    maybe_ints: List[Optional[int]] = to_ints(numbers_raw)
    print("Casted:", maybe_ints)

    # For loop + enumerate
    for i, v in enumerate(maybe_ints):
        print(f"item[{i}] = {v}")

    # Conditionals
    if None in maybe_ints:
        print("There were invalid numbers.")
    elif len(maybe_ints) > 5:
        print("Many numbers.")
    else:
        print("All valid and short list.")

    # While loop
    doubled: List[int] = []
    idx = 0
    while idx < len(maybe_ints):
        val = maybe_ints[idx]
        if val is not None:
            doubled.append(val * 2)
        idx += 1
    print("Doubled:", doubled)

    # Built-in functions: range, id
    print("range example:", list(range(3)))
    print("id(doubled):", id(doubled))

if __name__ == "__main__":
    main()
