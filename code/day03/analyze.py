import pandas as pd

df = pd.read_csv("test_runs.csv")

print("Shape:", df.shape)
print(df.dtypes)
print(df.isna().sum())

# Clean
df["status"] = df["status"].str.strip().str.lower()
df = df.drop_duplicates()
df["duration"] = df["duration"].fillna(df["duration"].median())

# Select
failed = df[df["status"] == "failed"]
slowest = df.sort_values("duration", ascending=False).head(3)

print("\nFailed tests:")
print(failed[["test_name", "browser"]])
print("\nSlowest tests:")
print(slowest[["test_name", "duration"]])