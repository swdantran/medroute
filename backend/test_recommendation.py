from services.recommendation_service import (
    recommend_hospitals,
)


USER_LATITUDE = 42.3732
USER_LONGITUDE = -72.5199


recommendations = recommend_hospitals(
    user_latitude=USER_LATITUDE,
    user_longitude=USER_LONGITUDE,
    triage_category="Urgent",
    age_group="Adult (36-60)",
)


print("\nMEDROUTE RECOMMENDATIONS\n")


for rank, hospital in enumerate(
    recommendations,
    start=1,
):
    print(
        f"{rank}. "
        f"{hospital['hospital_name']}"
    )

    print(
        f"   {hospital['city']}, MA"
    )

    print(
    f"   Simulated occupancy: "
    f"{hospital['occupancy_rate'] * 100:.0f}%"
)

    print(
        f"   Drive: "
        f"{hospital['travel_minutes']:.1f} min"
    )

    print(
        f"   Predicted wait: "
        f"{hospital['predicted_wait_minutes']:.1f} min"
    )

    print(
        f"   Estimated time-to-care: "
        f"{hospital['time_to_care_minutes']:.1f} min"
    )

    print()