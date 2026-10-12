# Day 3 (Tue Oct 13): Pandas Basics

**Time:** about 2.5-3 hrs · **Goal:** load a messy CSV, clean it, and select the rows and columns you need.

## Revisit first (10 min)

Answer these without notes, then check `flashcards.md`:

1. Why use a virtual environment?
2. List vs tuple vs set vs dict?
3. What does `with open(...) as f` guarantee?

## Schedule

| Block | Time | Task |
| --- | --- | --- |
| A | 45 min | Study the concepts below and run the examples |
| B | 50 min | Hands-on: clean the messy `test_runs.csv` |
| C | 30 min | Drill: 4 exercises (below) |
| D | 30 min | Write your note, add 5-8 pairs to `flashcards.md`, explain aloud for 2 min |

## Setup

Activate your virtual environment first (use `python3` only for creating it, then `python`):

```bash
cd day03
python3 -m venv .venv
source .venv/bin/activate
pip install pandas
```

## Concepts

**Pandas** is a Python library for working with tables of data.

| Idea | What it is | Java analogy |
| --- | --- | --- |
| DataFrame | A table with rows and named columns | A database table or `ResultSet` you can query in memory |
| Series | One column of a DataFrame | A `List` of values with an index |
| Index | The row labels (0, 1, 2 by default) | A row id |
| `read_csv` | Loads a CSV into a DataFrame | Reading a file into a list of objects, in one line |

### Inspect a DataFrame

```python
df.shape          # (rows, columns)
df.head()         # first 5 rows
df.info()         # column types and missing counts
df.describe()     # basic statistics
df.dtypes         # data type of each column
```

### Select data

```python
df["status"]                         # one column (Series)
df[["test_name", "status"]]          # several columns (DataFrame)
df[df["status"] == "failed"]         # rows matching a condition
df.loc[0, "test_name"]               # by label
df.iloc[0, 0]                        # by position
```

### Clean data

```python
df.isna().sum()                      # missing values per column
df["duration"].fillna(0)             # fill missing values
df.dropna()                          # drop rows with missing values
df.drop_duplicates()                 # remove repeated rows
df["status"].str.strip().str.lower() # trim spaces and lowercase text
df["duration"].astype(float)         # change the type
```

### Key ideas

1. **Check the data before you trust it.** Always look at `shape`, `info()` and `head()` first.
2. **Cleaning is most of the work.** Spaces, mixed case, missing values and duplicates are the usual problems.
3. **Selecting with a condition keeps the whole row.** `df[df["status"] == "failed"]` returns rows, not just a column.
4. **Most pandas operations return a new DataFrame.** Assign the result back (`df = df.drop_duplicates()`) or the change is lost.

## Hands-on: clean a messy test-runs file

Create `test_runs.csv` (it is deliberately messy):

```text
test_name,status,duration,browser
login_test,passed,1.2,chrome
checkout_test, failed ,3.4,chrome
search_test,passed,,firefox
login_test,passed,1.2,chrome
profile_test,PASSED,0.9,firefox
```

Create `analyze.py`:

```python
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
```

Run it with `python analyze.py`. Then change the CSV (add a row, blank a value) and watch the output change.

## Drill (30 min)

1. Print how many tests ran on each browser (hint: `df["browser"].value_counts()`).
2. Print only the tests on `firefox` with a duration over 1 second.
3. Add a new column `slow` that is `True` when duration is above 2 seconds.
4. Save the cleaned DataFrame to `clean_runs.csv` with `df.to_csv("clean_runs.csv", index=False)`.

## Interview questions

1. **What is pandas, and when would you use it?**
   A Python library for working with tabular data. Use it for loading, cleaning, exploring and transforming datasets, often before analysis or machine learning.

2. **DataFrame vs Series?**
   A DataFrame is a 2D table with named columns. A Series is a single column, a 1D labeled array.

3. **`loc` vs `iloc`?**
   `loc` selects by label (row labels and column names). `iloc` selects by integer position.

4. **How do you handle missing values?**
   First find them with `isna().sum()`, then decide: drop rows (`dropna`), fill with a value such as zero, mean or median (`fillna`), or leave them if the model or analysis can handle them. The choice depends on the data and why it is missing.

5. **How do you remove duplicate rows?**
   `df.drop_duplicates()`, optionally with `subset=[...]` to compare only some columns.

6. **Why did my change to the DataFrame disappear?**
   Most pandas methods return a new object instead of changing the original. Assign the result back, or use the `inplace` option where it exists.

7. **How do you filter rows with two conditions?**
   Wrap each condition in parentheses and use `&` or `|`, for example `df[(df["status"] == "failed") & (df["browser"] == "chrome")]`. Python's `and`/`or` do not work here.

8. **What does `df.info()` tell you?**
   Column names, data types, non-null counts and memory use. It is the fastest way to spot missing values and wrong types.

9. **Why does data cleaning matter for AI and ML?**
   Models learn from whatever data they get. Duplicates, missing values and inconsistent labels lead to biased or unreliable results. "Garbage in, garbage out."

10. **How could a QA engineer use pandas around AI work?**
    To analyze test results and flaky-test patterns, clean and prepare test data, build evaluation datasets, and compare model outputs against expected results.

## My own words (fill in)

- One thing that surprised me:
- My 2-minute explanation:
- Flashcards added today:

## Review dates

Revisit on Day 4, Day 6, Day 10 and Day 24.
