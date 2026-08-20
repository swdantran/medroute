import os

import requests
from dotenv import load_dotenv


load_dotenv()


GOOGLE_MAPS_API_KEY = os.getenv(
    "GOOGLE_MAPS_API_KEY"
)

ROUTES_URL = (
    "https://routes.googleapis.com/"
    "distanceMatrix/v2:computeRouteMatrix"
)


def make_waypoint(
    latitude,
    longitude,
):
    return {
        "waypoint": {
            "location": {
                "latLng": {
                    "latitude": float(latitude),
                    "longitude": float(longitude),
                }
            }
        }
    }


def get_travel_times(
    user_latitude,
    user_longitude,
    hospitals,
):
    if not GOOGLE_MAPS_API_KEY:
        raise RuntimeError(
            "GOOGLE_MAPS_API_KEY is not set."
        )

    origin = make_waypoint(
        user_latitude,
        user_longitude,
    )

    destinations = []

    for _, hospital in hospitals.iterrows():
        destinations.append(
            make_waypoint(
                hospital["Latitude"],
                hospital["Longitude"],
            )
        )

    body = {
        "origins": [origin],
        "destinations": destinations,
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_MAPS_API_KEY,
        "X-Goog-FieldMask": (
            "originIndex,"
            "destinationIndex,"
            "status,"
            "condition,"
            "duration,"
            "distanceMeters"
        ),
    }


    response = requests.post(
        ROUTES_URL,
        headers=headers,
        json=body,
        timeout=15,
    )

    response.raise_for_status()

    results = response.json()

    travel_results = {}

    for result in results:

        if result.get("condition") != "ROUTE_EXISTS":
            continue

        destination_index = result[
            "destinationIndex"
        ]

        duration_string = result[
            "duration"
        ]

        duration_seconds = float(
            duration_string.rstrip("s")
        )

        duration_minutes = (
            duration_seconds / 60
        )

        distance_meters = result[
            "distanceMeters"
        ]

        distance_miles = (
            distance_meters / 1609.344
        )

        travel_results[
            destination_index
        ] = {
            "travel_minutes": duration_minutes,
            "driving_miles": distance_miles,
        }

    return travel_results