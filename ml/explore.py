from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = (
    Path(__file__).parent
    /"data"
    /"hospital_wait_times.csv"
)

# Load the CSV into a pandas DataFrame
df = pd.read_csv(DATA_PATH)

# Basic information
print("Dataset shape:")
print(df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nColumns:")
print(df.columns.tolist())

# Convert timestamp columns from text into real datetime objects
df["ActualArrivalTime"] = pd.to_datetime(
    df["ActualArrivalTime"],
    format="%d-%m-%Y %H:%M"
)

df["ProviderStartTime"] = pd.to_datetime(
    df["ProviderStartTime"],
    format="%d-%m-%Y %H:%M"
)

# Calculate how long the patient waited before seeing a provider
df["WaitToProviderMinutes"] = (
    df["ProviderStartTime"]
    - df["ActualArrivalTime"]
).dt.total_seconds() / 60

print("\nWait time statistics:")
print(df["WaitToProviderMinutes"].describe())
y = df["WaitToProviderMinutes"]

# ==========================================
# EXPLORATORY DATA ANALYSIS
# ==========================================

print("\n" + "=" * 50)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 50)


# -------------------------
# MISSING VALUES
# -------------------------

print("\nMissing values:")
missing_values = df.isnull().sum()

print(
    missing_values[missing_values > 0]
    .sort_values(ascending=False)
)


# -------------------------
# DEPARTMENTS
# -------------------------

print("\nDepartment counts:")
print(df["Department"].value_counts())


# -------------------------
# TRIAGE CATEGORIES
# -------------------------

print("\nTriage category counts:")
print(df["TriageCategory"].value_counts())


# -------------------------
# ARRIVAL METHODS
# -------------------------

print("\nArrival methods:")
print(df["ArrivalMethod"].value_counts())


# -------------------------
# DAY OF WEEK
# -------------------------

print("\nDay of week:")
print(df["DayOfWeek"].value_counts())


# -------------------------
# NUMERIC FEATURES
# -------------------------

numeric_features = [
    "FacilityOccupancyRate",
    "ProvidersOnShift",
    "NursesOnShift",
    "StaffToPatientRatio",
    "ArrivalHour",
    "WaitToProviderMinutes"
]

print("\nNumeric feature statistics:")
print(df[numeric_features].describe())

print("\nWait time by triage category:")

triage_waits = (
    df.groupby("TriageCategory")["WaitToProviderMinutes"]
    .agg(["count", "mean", "median"])
    .sort_values("median")
)

print(triage_waits)

print("\nWait time by occupancy level:")

occupancy_waits = (
    df.groupby("OccupancyRateBin")["WaitToProviderMinutes"]
    .agg(["count", "mean", "median"])
)

print(occupancy_waits)

plt.hist(
    df["WaitToProviderMinutes"],
    bins=30
)

plt.xlabel("Wait Time (minutes)")
plt.ylabel("Number of Patients")
plt.title("Distribution of Wait Times")

plt.show()

categorical_features = [
    "Department",
    "ArrivalMethod",
    "AgeGroup",
    "DayOfWeek",
    "Month"
]

numeric_features = [
    "FacilityOccupancyRate",
    "ProvidersOnShift",
    "NursesOnShift",
    "StaffToPatientRatio",
    "ArrivalHour"
]