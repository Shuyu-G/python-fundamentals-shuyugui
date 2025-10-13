from __future__ import annotations

from functools import partial
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


# ---------- Helpers ----------

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
DATA_PATH = DATA_DIR / "users_pandas.csv"  # Could also be .json


def ensure_data_file() -> None:
    """Create an example CSV with mixed/dirty types if missing."""
    if not DATA_PATH.exists():
        # Intentionally include some “dirty” data for cleaning examples:
        rows = [
            # id, name, email, age,    height_cm, signup_date,    active, city
            [
                1,
                "Alice",
                "alice@example.com",
                "28",
                165.0,
                "2024-03-01",
                "yes",
                "Berlin",
            ],
            [2, "Bob", "bob@example.com", 31, None, "01/04/2024", "no", "Bremen"],
            [3, "Carol", "carol@example.com", "24", 170.5, "2024/05/10", "yes", ""],
            [4, "Dave", "dave@example.com", "?", 180.2, "10-06-2024", "yes", "Munich"],
            [5, "Eve", "eve@example.com", 29, np.nan, "2024-07-15", "no", "Cologne"],
            [
                6,
                "Eve2",
                "alice@example.com",
                29,
                171.0,
                "invalid",
                "no",
                None,
            ],  # duplicate email
        ]
        df0 = pd.DataFrame(
            rows,
            columns=[
                "id",
                "name",
                "email",
                "age",
                "height_cm",
                "signup_date",
                "active",
                "city",
            ],
        )
        df0.to_csv(DATA_PATH, index=False)


# ---------- Functions used in .pipe() ----------


def cast_types(df: pd.DataFrame) -> pd.DataFrame:
    """Safe type conversion using pd.to_numeric / pd.to_datetime."""
    return df.assign(
        age=pd.to_numeric(df["age"], errors="coerce"),
        signup_date=pd.to_datetime(df["signup_date"], errors="coerce"),
        active=df["active"].astype(str).str.lower().map({"yes": True, "no": False}),
    )


def fill_missing_city(val: Any) -> str:
    """Default city value for .apply()."""
    if pd.isna(val) or str(val).strip() == "":
        return "Unknown"
    return str(val)


def remove_col_if_null_fraction_above(
    df: pd.DataFrame, *, col: str, threshold: float
) -> pd.DataFrame:
    """Drop a column if its NaN fraction > threshold (demonstrates .pipe + partial)."""
    frac = df[col].isna().mean()
    print(f"[pipe] NaN fraction of '{col}' = {frac:.2%} (threshold={threshold:.0%})")
    if frac > threshold:
        print(f"[pipe] Dropping column '{col}'")
        return df.drop(columns=[col])
    return df


def filter_age_range(
    df: pd.DataFrame, *, min_age: float, max_age: float
) -> pd.DataFrame:
    """Filter ages in [min_age, max_age]."""
    return df[(df["age"] >= min_age) & (df["age"] <= max_age)]


# ---------- Main: satisfies each assignment bullet ----------


def main() -> None:
    # 1) Create an example data file (CSV)
    ensure_data_file()
    print(f"Created/verified data file at: {DATA_PATH}")

    # 2) Pandas Series with a custom index
    s = pd.Series([23, 18, 30], index=["alice", "bob", "carol"], name="ages")
    print("\n# Series with custom index")
    print(s)

    # 3) DataFrame with specified columns (small demo)
    df_small = pd.DataFrame(
        [{"id": 1, "name": "X", "age": 20}, {"id": 2, "name": "Y", "age": 22}],
        columns=["id", "name", "age"],
    )
    print("\n# Small DataFrame with specified columns")
    print(df_small)

    # Load the main demo data
    df = pd.read_csv(DATA_PATH)
    print("\n# Loaded DataFrame (raw)")
    print(df)

    # 4) Inspect dtypes / head / tail / describe
    print("\n# dtypes")
    print(df.dtypes)
    print("\n# head(3)")
    print(df.head(3))
    print("\n# tail(2)")
    print(df.tail(2))
    print("\n# describe(numeric_only=True)")
    print(df.select_dtypes(include="number").describe())

    # 5) Slicing by row position and by column name
    print("\n# iloc slice rows [1:4]")
    print(df.iloc[1:4])
    print("\n# column slice ['id','name']")
    print(df[["id", "name"]])

    # 6) Boolean flags & data range filtering
    flags = df["city"].astype(str).str.contains("e", case=False, na=False)
    print("\n# boolean mask (city contains 'e')")
    print(df[flags])

    # Range filter on age: convert first, then filter
    df_age = df.assign(age=pd.to_numeric(df["age"], errors="coerce"))
    print("\n# age in [20, 35]")
    print(df_age[(df_age["age"] >= 20) & (df_age["age"] <= 35)][["id", "name", "age"]])

    # 7) duplicated / nunique / drop_duplicates
    print("\n# duplicated on 'email'")
    print(df["email"].duplicated(keep=False))
    print("# nunique on 'email':", df["email"].nunique())
    print("\n# drop_duplicates on 'email' (keep first)")
    print(df.drop_duplicates(subset=["email"], keep="first"))

    # 8) pd.to_numeric / pd.to_datetime (safe conversion)
    df_conv = df.copy()
    df_conv["age"] = pd.to_numeric(df_conv["age"], errors="coerce")
    df_conv["signup_date"] = pd.to_datetime(df_conv["signup_date"], errors="coerce")
    print("\n# after to_numeric/to_datetime -> dtypes")
    print(df_conv.dtypes)

    # 9) Set default values with .apply()
    df_city_fixed = df.copy()
    df_city_fixed["city"] = df_city_fixed["city"].apply(fill_missing_city)
    print("\n# city after .apply(default):")
    print(df_city_fixed[["id", "name", "city"]])

    # 10) Cleaning pipeline using .pipe() (type conversion) and print result
    df_clean = df.pipe(cast_types)
    print("\n# pipe(cast_types) -> dtypes and null counts")
    print(df_clean.dtypes)
    print(df_clean.isna().sum())

    # 11) .pipe() with partial args (threshold parameter in pipeline)
    remove_height_if_too_null = partial(
        remove_col_if_null_fraction_above, col="height_cm", threshold=0.30
    )
    df_piped = (
        df.pipe(cast_types)
        .pipe(remove_height_if_too_null)  # apply thresholded column drop
        .pipe(
            filter_age_range, min_age=20, max_age=40
        )  # additional filter using kwargs
    )
    print("\n# final piped result (head)")
    print(df_piped.head())
    print("\n# final dtypes")
    print(df_piped.dtypes)


if __name__ == "__main__":
    main()
