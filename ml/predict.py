from pathlib import Path

import joblib
import pandas as pd


# ==========================================
# LOAD TRAINED MODEL
# ==========================================

BASE_DIR = Path(__file__).parent

MODEL_PATH = (
    BASE_DIR
    / "artifacts"
    / "wait_model.pkl"
)

model = joblib.load(MODEL_PATH)


# ==========================================
# TEST DIFFERENT TRIAGE CATEGORIES
# ==========================================

triage_categories = [
    "Immediate",
    "Emergency",
    "Urgent",
    "Semi-urgent",
    "Non-urgent",
]

for triage in triage_categories:
    hospital_conditions = pd.DataFrame(
        [
            {
                "Department": "Emergency",
                "ArrivalMethod": "Walk-in",
                "AgeGroup": "Adult (36-60)",
                "DayOfWeek": "Mon",
                "Month": "Mar",
                "TriageCategory": triage,
                "FacilityOccupancyRate": 0.85,
                "ProvidersOnShift": 5,
                "NursesOnShift": 10,
                "StaffToPatientRatio": 0.30,
                "ArrivalHour": 18,
            }
        ]
    )

    prediction = model.predict(
        hospital_conditions
    )[0]

    print(
        f"{triage:12} -> "
        f"{prediction:.1f} minutes"
    )