from pathlib import Path
import uuid

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "csv"

FREQUENCIES = ["Weekly", "Fortnightly", "bi-weekly"]


def pipeline(*steps):
    def wrapper(inputs):
        for step in steps:
            inputs = apply(step, inputs)
        return inputs

    return wrapper


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
    output_file = BASE_DIR / f"result_{uuid.uuid4()}.txt"
    with output_file.open("w", encoding="utf-8") as f:
        for customer_id, category in result:
            f.write(f"{customer_id}, {category}\n")
    return output_file


def apply(step, values):
    return [step(value) for value in values]


def main():
    dfs = [pd.read_csv(DATA_DIR / f"shopping_behavior_{year}.csv") for year in (2023, 2024, 2025)]

    p = pipeline(step1, step2, step3, step4)
    p(dfs)


if __name__ == "__main__":
    main()
