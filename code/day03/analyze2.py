import pandas as pd

# Load the CSV file
df = pd.read_csv("test_runs.csv")

# 1. Count how many tests ran on each browser
print("Test count by browser:")
print(df["browser"].value_counts())

# 2. Filter Firefox tests with duration greater than 1 second
print("\nFirefox tests with duration > 1 second:")
firefox_tests = df[
    (df["browser"] == "firefox") &
    (df["duration"] > 1)
]
print(firefox_tests)

# 3. Add a new column 'slow'
# True if duration > 2 seconds, otherwise False
df["slow"] = df["duration"] > 2

print("\nUpdated DataFrame:")
print(df)

# 4. Save the cleaned DataFrame to a new CSV file
df.to_csv("clean_runs.csv", index=False)

print("\nData saved successfully to clean_runs.csv")