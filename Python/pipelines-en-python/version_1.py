from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

FREQUENCIES = ["Weekly", "Fortnightly", "bi-weekly"]


def main():
    df = pd.read_csv(BASE_DIR / "data" / "csv" / "shopping_behavior_2023.csv")

    df.columns = df.columns.str.lower().str.replace(" ", "_")

    df = df[df["payment_method"] == "PayPal"]
    df = df[df["frequency_of_purchases"].isin(FREQUENCIES)]

    df = (
        df[["customer_id", "category", "purchase_amount_(usd)"]]
        .groupby(["customer_id", "category"])
        .sum()
        .reset_index()
    )

    df["rank"] = df.groupby("category")["purchase_amount_(usd)"].rank(
        method="dense", ascending=False
    )

    df = df[df["rank"] == 1]

    result = list(df[["customer_id", "category"]].itertuples(index=False, name=None))

    with (BASE_DIR / "result.txt").open("w", encoding="utf-8") as f:
        for customer_id, category in result:
            f.write(f"{customer_id}, {category}\n")


if __name__ == "__main__":
    main()
