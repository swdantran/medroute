from datetime import datetime

from services.simulated_conditions_service import (
    get_simulated_conditions,
)

from services.hospital_service import (
    find_nearby_hospitals,
)

from services.routing_service import (
    get_travel_times,
)

from services.wait_time_service import (
    predict_wait_time,
)


def recommend_hospitals(
    user_latitude,
    user_longitude,
    triage_category,
    age_group,
    arrival_method="Walk-in",
    limit=5,
):
    hospitals = find_nearby_hospitals(
        user_latitude,
        user_longitude,
        limit=limit,
    )

    travel_times = get_travel_times(
        user_latitude,
        user_longitude,
        hospitals,
    )

    recommendations = []

    # Use the current date/time for prediction features
    now = datetime.now()

    for index, (_, hospital) in enumerate(
        hospitals.iterrows()
    ):
        route = travel_times.get(index)

        if route is None:
            continue

        # These are simulated prototype conditions.
        # They are NOT real-time hospital data.
        conditions = get_simulated_conditions(
            hospital["Facility Name"]
        )

        predicted_wait = predict_wait_time(
            department="Emergency",
            arrival_method=arrival_method,
            age_group=age_group,
            day_of_week=now.strftime("%a"),
            month=now.strftime("%b"),
            triage_category=triage_category,
            occupancy_rate=conditions[
                "occupancy_rate"
            ],
            providers_on_shift=conditions[
                "providers_on_shift"
            ],
            nurses_on_shift=conditions[
                "nurses_on_shift"
            ],
            staff_patient_ratio=conditions[
                "staff_patient_ratio"
            ],
            arrival_hour=now.hour,
        )

        travel_minutes = route[
            "travel_minutes"
        ]

        time_to_care = (
            travel_minutes
            + predicted_wait
        )

        recommendations.append(
            {
                "hospital_name": hospital[
                    "Facility Name"
                ],
                "city": hospital[
                    "City/Town"
                ],
                "travel_minutes": travel_minutes,
                "driving_miles": route[
                    "driving_miles"
                ],
                "predicted_wait_minutes": (
                    predicted_wait
                ),
                "time_to_care_minutes": (
                    time_to_care
                ),
                "occupancy_rate": conditions[
                    "occupancy_rate"
                ],
                "providers_on_shift": conditions[
                    "providers_on_shift"
                ],
                "nurses_on_shift": conditions[
                    "nurses_on_shift"
                ],
                "staff_patient_ratio": conditions[
                    "staff_patient_ratio"
                ],
            }
        )

    recommendations.sort(
        key=lambda hospital: hospital[
            "time_to_care_minutes"
        ]
    )

    return recommendations