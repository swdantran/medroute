from pathlib import Path
import time

import pandas as pd
import requests


BASE_DIR = Path(__file__).parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "hospitals.csv"
)

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "ma_hospitals_geocoded.csv"
)


# Load hospital data
df = pd.read_csv(
    DATA_PATH,
    dtype={"ZIP Code": str},
)

df["ZIP Code"] = (
    df["ZIP Code"]
    .str.zfill(5)
)

def geocode_address(
    street,
    city,
    state,
    zip_code,
):
    url = (
        "https://geocoding.geo.census.gov/"
        "geocoder/locations/address"
    )

    params = {
        "street": street,
        "city": city,
        "state": state,
        "zip": zip_code,
        "benchmark": "Public_AR_Current",
        "format": "json",
    }

    response = requests.get(
        url,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    matches = (
        data["result"]
        ["addressMatches"]
    )

    if not matches:
        return None, None

    coordinates = (
        matches[0]["coordinates"]
    )

    longitude = coordinates["x"]
    latitude = coordinates["y"]

    return latitude, longitude

# Keep only Massachusetts hospitals
ma_hospitals = (
    df[df["State"] == "MA"]
    .copy()
)

print(
    f"Found {len(ma_hospitals)} "
    f"Massachusetts hospitals."
)

latitudes = []
longitudes = []


for index, hospital in ma_hospitals.iterrows():

    print(
        f"Geocoding "
        f"{hospital['Facility Name']}..."
    )

    try:
        latitude, longitude = geocode_address(
            hospital["Address"],
            hospital["City/Town"],
            hospital["State"],
            hospital["ZIP Code"],
        )

    except requests.RequestException as error:

        print(
            f"Request failed: {error}"
        )

        latitude = None
        longitude = None


    latitudes.append(latitude)
    longitudes.append(longitude)

    time.sleep(0.1)


ma_hospitals["Latitude"] = latitudes
ma_hospitals["Longitude"] = longitudes

print(
    "\nSuccessfully geocoded:"
)

print(
    ma_hospitals[
        "Latitude"
    ].notna().sum()
)

print(
    f"out of {len(ma_hospitals)} hospitals"
)

ma_hospitals.to_csv(
    OUTPUT_PATH,
    index=False,
)

print(
    f"\nSaved to:\n{OUTPUT_PATH}"
)