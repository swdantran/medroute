from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "hospitals.csv"
)


df = pd.read_csv(
    DATA_PATH,
    dtype={"ZIP Code": str},
)

df["ZIP Code"] = (
    df["ZIP Code"]
    .str.zfill(5)
)


print("Dataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 hospitals:")
print(df.head())

print("\nStates:")
print(df["State"].value_counts().head(10))

ma_hospitals = df[
    df["State"] == "MA"
]

print("\nMassachusetts hospitals:")
print(len(ma_hospitals))

print(
    ma_hospitals[
        [
            "Facility Name",
            "Address",
            "City/Town",
            "State",
            "ZIP Code",
        ]
    ].head(20)
)