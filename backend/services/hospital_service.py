from pathlib import Path
import math

import pandas as pd


BASE_DIR = Path(__file__).parent.parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "ma_hospitals_geocoded.csv"
)

def load_hospitals():
    df = pd.read_csv(
        DATA_PATH,
        dtype={"ZIP Code": str},
    )

    df["ZIP Code"] = (
        df["ZIP Code"]
        .str.zfill(5)
    )

    # Remove hospitals without valid coordinates
    df = df.dropna(
        subset=[
            "Latitude",
            "Longitude",
        ]
    )

    # Keep only hospitals that provide emergency services
    df = df[
        df["Emergency Services"] == "Yes"
    ].copy()

    # Exclude psychiatric facilities
    df = df[
        ~df["Hospital Type"]
        .str.contains(
            "Psychiatric",
            case=False,
            na=False,
        )
    ].copy()

    return df

def haversine_distance(
    lat1,
    lon1,
    lat2,
    lon2,
):
    earth_radius_miles = 3958.8

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a),
    )

    distance = earth_radius_miles * c

    return distance

def find_nearby_hospitals(
    user_latitude,
    user_longitude,
    limit=5,
):
    hospitals = load_hospitals()

    hospitals["DistanceMiles"] = hospitals.apply(
        lambda hospital: haversine_distance(
            user_latitude,
            user_longitude,
            hospital["Latitude"],
            hospital["Longitude"],
        ),
        axis=1,
    )

    hospitals = hospitals.sort_values(
        "DistanceMiles"
    )

    nearby = hospitals.head(limit)

    return nearby

if __name__ == "__main__":

    test_latitude = 42.3732
    test_longitude = -72.5199

    nearby = find_nearby_hospitals(
        test_latitude,
        test_longitude,
        limit=5,
    )

    print("\nNearest hospitals:\n")

    for _, hospital in nearby.iterrows():

        print(
            hospital["Facility Name"]
        )

        print(
            f"  {hospital['City/Town']}, "
            f"{hospital['State']}"
        )

        print(
            f"  Distance: "
            f"{hospital['DistanceMiles']:.2f} miles"
        )

        print()