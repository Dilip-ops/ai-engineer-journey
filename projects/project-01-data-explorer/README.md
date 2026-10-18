# Project 1: Test Results Explorer

A command-line tool that reads test run data from SQLite, cleans it with pandas
and prints a report.

## What it shows
- Summary of runs and pass rate
- Failures per module
- Slowest runs
- Tests that were never run

## How to run
    python3 setup_db.py   (once, to create the database)
    python3 explorer.py
    python3 test_explorer.py

## What I learned
- **Data Engineering Basics**: How to extract raw data using SQL `JOIN` statements and map relational tables directly into memory using `pandas.read_sql_query`.
- **Defensive Data Cleaning**: Techniques for data normalization, such as standardizing string values (`.str.strip().str.lower()`) and removing duplicates before building analysis profiles.
- **Relational Integrity Exploration**: Utilizing `LEFT JOIN` and `IS NULL` filters in both raw SQL queries and pandas indexing to successfully identify orphan records (unexecuted tests).