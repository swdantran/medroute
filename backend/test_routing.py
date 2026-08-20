from services.hospital_service import (
    find_nearby_hospitals,
)

from services.routing_service import (
    get_travel_times,
)


USER_LATITUDE = 42.3732
USER_LONGITUDE = -72.5199


hospitals = find_nearby_hospitals(
    USER_LATITUDE,
    USER_LONGITUDE,
    limit=5,
)

travel_times = get_travel_times(
    USER_LATITUDE,
    USER_LONGITUDE,
    hospitals,
)


print("\nHospital travel times:\n")


for index, (_, hospital) in enumerate(
    hospitals.iterrows()
):

    route = travel_times.get(index)

    print(
        hospital["Facility Name"]
    )

    print(
        f"  Straight-line distance: "
        f"{hospital['DistanceMiles']:.2f} mi"
    )

    if route:

        print(
            f"  Driving distance: "
            f"{route['driving_miles']:.2f} mi"
        )

        print(
            f"  Travel time: "
            f"{route['travel_minutes']:.1f} min"
        )

    else:

        print(
            "  No driving route found."
        )

    print()