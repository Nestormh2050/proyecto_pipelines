from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

FREQUENCIES = ["Weekly", "Fortnightly", "bi-weekly"]


def step1(df):
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df = df[df["payment_method"] == "PayPal"]
    df = df[df["frequency_of_purchases"].isin(FREQUENCIES)]
    return df


def step2(df):
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
    return df


def step3(df):
    return list(df[["customer_id", "category"]].itertuples(index=False, name=None))


def step4(result):
    with (BASE_DIR / "result.txt").open("w", encoding="utf-8") as f:
        for customer_id, category in result:
            f.write(f"{customer_id}, {category}\n")


def main():
    df = pd.read_csv(BASE_DIR / "data" / "csv" / "shopping_behavior_2023.csv")
    step4(step3(step2(step1(df))))


if __name__ == "__main__":
    main()
