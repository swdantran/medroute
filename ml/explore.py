from pathlib import Path
import pandas as pd

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