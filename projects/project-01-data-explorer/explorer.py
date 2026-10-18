import sqlite3
import pandas as pd

DB_PATH = "tests.db"


def load_data(db_path: str) -> pd.DataFrame:
    """Join test_runs with test_cases and return one DataFrame."""
    conn = sqlite3.connect(db_path)
    # Using an INNER JOIN here since we want to analyze actual runs
    query = """
    SELECT 
        tr.id,
        tr.test_name,
        tr.status,
        tr.duration,
        tr.browser,
        tc.module,
        tc.owner
    FROM test_runs tr
    JOIN test_cases tc ON tr.test_name = tc.test_name
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Trim and lowercase status, drop duplicate rows."""
    df = df.copy()
    if "status" in df.columns:
        df["status"] = df["status"].astype(str).str.strip().str.lower()
    df = df.drop_duplicates()
    return df


def summarise(df: pd.DataFrame) -> dict:
    """Return total, passed, failed and pass_rate (percent, one decimal)."""
    total = len(df)
    
    # Handle the case where the dataframe might be empty to prevent division by zero
    if total == 0:
        return {"total": 0, "passed": 0, "failed": 0, "pass_rate": 0.0}
        
    passed = int((df["status"] == "passed").sum())
    failed = int((df["status"] == "failed").sum())
    pass_rate = round((passed / total) * 100, 1)
    
    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": pass_rate
    }


def failures_by_module(df: pd.DataFrame) -> pd.Series:
    """Number of failed runs per module."""
    failed_df = df[df["status"] == "failed"]
    # Group by module and count the occurrences
    return failed_df.groupby("module").size()


def slowest_runs(df: pd.DataFrame, n: int = 3) -> pd.DataFrame:
    """The n slowest runs, with test_name, duration and browser."""
    # Sort descending by duration and grab top n records
    sorted_df = df.sort_values(by="duration", ascending=False)
    return sorted_df[["test_name", "duration", "browser"]].head(n)


def never_run_tests(db_path: str) -> list[str]:
    """Names of tests in test_cases that have no runs."""
    conn = sqlite3.connect(db_path)
    # LEFT JOIN identifies tests that exist in test_cases but missing from test_runs
    query = """
    SELECT tc.test_name
    FROM test_cases tc
    LEFT JOIN test_runs tr ON tc.test_name = tr.test_name
    WHERE tr.id IS NULL
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df["test_name"].tolist()


def main() -> None:
    df = clean(load_data(DB_PATH))
    summary = summarise(df)
    print("Summary:", summary)
    print("\nFailures by module:")
    print(failures_by_module(df))
    print("\nSlowest runs:")
    print(slowest_runs(df))
    print("\nNever run:", never_run_tests(DB_PATH))
    df.to_csv("report.csv", index=False)
    print("\nSaved report.csv")


if __name__ == "__main__":
    main()
