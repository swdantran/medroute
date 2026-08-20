SIMULATED_CONDITIONS = {
    "COOLEY DICKINSON HOSPITAL INC,THE": {
        "occupancy_rate": 0.92,
        "providers_on_shift": 4,
        "nurses_on_shift": 8,
        "staff_patient_ratio": 0.22,
    },

    "HOLYOKE MEDICAL CENTER": {
        "occupancy_rate": 0.68,
        "providers_on_shift": 7,
        "nurses_on_shift": 13,
        "staff_patient_ratio": 0.38,
    },

    "BAYSTATE FRANKLIN MEDICAL CENTER": {
        "occupancy_rate": 0.75,
        "providers_on_shift": 6,
        "nurses_on_shift": 10,
        "staff_patient_ratio": 0.32,
    },

    "BAYSTATE WING HOSPITAL": {
        "occupancy_rate": 0.87,
        "providers_on_shift": 5,
        "nurses_on_shift": 9,
        "staff_patient_ratio": 0.27,
    },

    "BAYSTATE MEDICAL CENTER": {
        "occupancy_rate": 0.80,
        "providers_on_shift": 9,
        "nurses_on_shift": 16,
        "staff_patient_ratio": 0.40,
    },
}


DEFAULT_CONDITIONS = {
    "occupancy_rate": 0.80,
    "providers_on_shift": 5,
    "nurses_on_shift": 10,
    "staff_patient_ratio": 0.30,
}


def get_simulated_conditions(
    hospital_name,
):
    return SIMULATED_CONDITIONS.get(
        hospital_name,
        DEFAULT_CONDITIONS,
    )