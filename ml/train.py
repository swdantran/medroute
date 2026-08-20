from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import (
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

BASE_DIR = Path(__file__).parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "hospital_wait_times.csv"
)

MODEL_PATH = (
    BASE_DIR
    / "artifacts"
    / "wait_model.pkl"
)

df = pd.read_csv(DATA_PATH)

print(f"Loaded {len(df)} rows.")

df["ActualArrivalTime"] = pd.to_datetime(
    df["ActualArrivalTime"],
    format="%d-%m-%Y %H:%M",
)

df["ProviderStartTime"] = pd.to_datetime(
    df["ProviderStartTime"],
    format="%d-%m-%Y %H:%M",
)

df["WaitToProviderMinutes"] = (
    df["ProviderStartTime"]
    - df["ActualArrivalTime"]
).dt.total_seconds() / 60

categorical_features = [
    "Department",
    "ArrivalMethod",
    "AgeGroup",
    "DayOfWeek",
    "Month",
    "TriageCategory",
]

numeric_features = [
    "FacilityOccupancyRate",
    "ProvidersOnShift",
    "NursesOnShift",
    "StaffToPatientRatio",
    "ArrivalHour",
]

features = categorical_features + numeric_features

X = df[features]
y = df["WaitToProviderMinutes"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
)

print(f"Training rows: {len(X_train)}")
print(f"Testing rows:  {len(X_test)}")

def make_preprocessor():
    return ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
                categorical_features,
            ),
            (
                "numeric",
                "passthrough",
                numeric_features,
            ),
        ]
    )

def evaluate_model(name, model, X_test, y_test):
    predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions,
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions,
        )
    )

    r2 = r2_score(
        y_test,
        predictions,
    )

    print("\n" + "=" * 40)
    print(name)
    print("=" * 40)

    print(f"MAE:  {mae:.2f} minutes")
    print(f"RMSE: {rmse:.2f} minutes")
    print(f"R²:   {r2:.3f}")

    return {
        "model": model,
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
    }

baseline_prediction = np.full(
    shape=len(y_test),
    fill_value=y_train.mean(),
)

baseline_mae = mean_absolute_error(
    y_test,
    baseline_prediction,
)

baseline_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        baseline_prediction,
    )
)

baseline_r2 = r2_score(
    y_test,
    baseline_prediction,
)

print("\n" + "=" * 40)
print("MEAN BASELINE")
print("=" * 40)

print(
    f"Always predicts: "
    f"{y_train.mean():.2f} minutes"
)

print(
    f"MAE:  "
    f"{baseline_mae:.2f} minutes"
)

print(
    f"RMSE: "
    f"{baseline_rmse:.2f} minutes"
)

print(
    f"R²:   "
    f"{baseline_r2:.3f}"
)

linear_model = Pipeline(
    steps=[
        (
            "preprocessor",
            make_preprocessor(),
        ),
        (
            "model",
            LinearRegression(),
        ),
    ]
)

linear_model.fit(
    X_train,
    y_train,
)

linear_results = evaluate_model(
    "LINEAR REGRESSION",
    linear_model,
    X_test,
    y_test,
)

random_forest_model = Pipeline(
    steps=[
        (
            "preprocessor",
            make_preprocessor(),
        ),
        (
            "model",
            RandomForestRegressor(
                n_estimators=200,
                random_state=42,
                n_jobs=-1,
            ),
        ),
    ]
)

random_forest_model.fit(
    X_train,
    y_train,
)

random_forest_results = evaluate_model(
    "RANDOM FOREST",
    random_forest_model,
    X_test,
    y_test,
)

gradient_boosting_model = Pipeline(
    steps=[
        (
            "preprocessor",
            make_preprocessor(),
        ),
        (
            "model",
            GradientBoostingRegressor(
                random_state=42,
            ),
        ),
    ]
)

gradient_boosting_model.fit(
    X_train,
    y_train,
)

gradient_boosting_results = evaluate_model(
    "GRADIENT BOOSTING",
    gradient_boosting_model,
    X_test,
    y_test,
)

results = {
    "Linear Regression": linear_results,
    "Random Forest": random_forest_results,
    "Gradient Boosting": gradient_boosting_results,
}

best_model_name = "Linear Regression"

best_result = results[best_model_name]
best_model = best_result["model"]

print("\n" + "=" * 40)
print("BEST MODEL")
print("=" * 40)

print(best_model_name)

print(
    f"MAE: "
    f"{best_result['mae']:.2f} minutes"
)

joblib.dump(
    best_model,
    MODEL_PATH,
)

print(
    f"\nSaved model to:\n"
    f"{MODEL_PATH}"
)