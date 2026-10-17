# Day 7 (Sat Oct 17): Project 1 and Week 1 Review

**Time:** about 4 hrs · **Goal:** build a small Python and SQL data explorer on your own, then consolidate Week 1 with a cheat sheet, an error log and a self-quiz.

## Schedule

| Block | Time | Task |
| --- | --- | --- |
| A | 15 min | Catch up: send me your Day 5 drill 6 answer and your Day 6 revision answers |
| B | 20 min | Read the project brief below and plan it |
| C | 110 min | Build the project |
| D | 25 min | Add the checks, write the README, commit |
| E | 40 min | Weekly review: cheat sheet, error log, self-quiz |
| F | 20 min | Flashcards and a 2-minute explanation of the whole week |

## Part 1: Project 1, Test Results Explorer

### What you are building

A command-line script that reads the `tests.db` database from Days 4 and 5, loads it into pandas, cleans it, and prints a short report. It uses everything from Week 1: Python functions, SQL joins, pandas, and `if __name__ == "__main__"`.

### Folder

```text
projects/project-01-data-explorer/
  explorer.py
  test_explorer.py
  tests.db          (copy from code/day05)
  README.md
  report.csv        (created by the script)
```

### Requirements

The script must:
1. Load every test run joined with its module and owner (SQL join, read into a DataFrame with `pd.read_sql_query`).
2. Clean the data (trim and lowercase `status`, remove duplicate rows).
3. Print a summary: total runs, passed, failed and pass rate as a percentage.
4. Print the number of failures per module.
5. Print the 3 slowest runs.
6. Print the tests that have never been run (LEFT JOIN, then `IS NULL`).
7. Save the cleaned data to `report.csv`.

### Starter skeleton

You write the bodies. The `TODO` lines tell you what each function needs.

```python
import sqlite3

import pandas as pd

DB_PATH = "tests.db"


def load_data(db_path: str) -> pd.DataFrame:
    """Join test_runs with test_cases and return one DataFrame."""
    # TODO: connect with sqlite3, write a JOIN query,
    #       and read it with pd.read_sql_query(sql, conn)
    ...


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Trim and lowercase status, drop duplicate rows."""
    # TODO
    ...


def summarise(df: pd.DataFrame) -> dict:
    """Return total, passed, failed and pass_rate (percent, one decimal)."""
    # TODO
    ...


def failures_by_module(df: pd.DataFrame) -> pd.Series:
    """Number of failed runs per module."""
    # TODO
    ...


def slowest_runs(df: pd.DataFrame, n: int = 3) -> pd.DataFrame:
    """The n slowest runs, with test_name, duration and browser."""
    # TODO
    ...


def never_run_tests(db_path: str) -> list[str]:
    """Names of tests in test_cases that have no runs."""
    # TODO: LEFT JOIN test_cases to test_runs and keep rows where run id IS NULL
    ...


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
```

### Expected results (use these to check your work)

With the Day 4 and Day 5 data, you should see:

| Check | Expected |
| --- | --- |
| Total runs | 10 |
| Passed / failed | 7 / 3 |
| Pass rate | 70.0 |
| Failures by module | payments 2, auth 1 |
| Slowest 3 durations | 3.9, 3.4, 3.1 (all checkout_test) |
| Never run | logout_test |

### Automated check

Create `test_explorer.py`. Real test frameworks (pytest) arrive in Week 3, so this uses plain `assert`:

```python
from explorer import clean, load_data, never_run_tests, summarise


def test_summary():
    df = clean(load_data("tests.db"))
    s = summarise(df)
    assert s["total"] == 10
    assert s["passed"] == 7
    assert s["failed"] == 3
    assert s["pass_rate"] == 70.0


def test_never_run():
    assert never_run_tests("tests.db") == ["logout_test"]


if __name__ == "__main__":
    test_summary()
    test_never_run()
    print("All checks passed")
```

Run it with `python3 test_explorer.py`.

### Rules for the build

- **Try it yourself first.** Spend at least 15 minutes on any function before you ask me for help.
- **When you are stuck,** tell me what you tried and what you saw, and I'll give a hint before the answer.
- **Commit as you go**, with messages like `Project 1: load_data works`.

### README template

Create `README.md` in the project folder:

```markdown
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
- (two or three lines in your own words)
```

## Part 2: Week 1 review

### 1. One-page cheat sheet

Create `notes/week-01-cheatsheet.md`. If it does not fit on one page, you have not yet compressed it. Use these headings:

- The AI map in two lines
- Python vs Java: five differences
- Pandas: the five calls I use most
- SQL: SELECT order, WHERE vs HAVING, JOIN types
- LLM basics: token, context window, temperature

### 2. Error log

Create `notes/error-log.md` with this table. I pre-filled the real slips from your first week:

```markdown
| Date | Topic | Mistake | Root cause | Fix |
| --- | --- | --- | --- | --- |
| Oct 12 | Python setup | `python: command not found` | macOS uses `python3` until a venv is active | Use `python3` to create the venv, then `python` inside it |
| Oct 13 | Running scripts | `analyze.py` not found | Terminal was in the wrong folder | Run `pwd` and `ls`, then `cd` to the script's folder |
| Oct 13 | VS Code | pandas import warning | Wrong interpreter selected | Select the `.venv` interpreter |
| Oct 14 | SQL | Used HAVING on a raw column | Mixed up WHERE vs HAVING | WHERE filters rows, HAVING filters groups |
| Oct 15 | Python | Swapped list and tuple mutability | Memorised, not understood | List = mutable, tuple = immutable |
```

Add anything else that tripped you up this week.

### 3. Week 1 self-quiz (answer without notes, then check below)

1. What is the nesting from AI to LLM?
2. Workflow vs agent?
3. What are the three things an MCP server can expose?
4. What does `with open(...)` guarantee?
5. `loc` vs `iloc`?
6. Why must you assign the result of `df.drop_duplicates()` back to a variable?
7. `WHERE` vs `HAVING`?
8. LEFT JOIN plus `IS NULL`: what does it find?
9. What is a context window?
10. Is temperature 0 fully deterministic?

**Answers:**
1. AI > ML > Deep Learning > LLM.
2. Workflow: code fixes the steps. Agent: the model decides the steps.
3. Tools, resources and prompts.
4. The file is closed even if an error occurs.
5. `loc` selects by label, `iloc` by integer position.
6. Pandas methods return a new object; the original does not change.
7. `WHERE` filters rows before grouping, `HAVING` filters groups after aggregation.
8. Rows in the left table that have no match in the right table.
9. The maximum number of tokens the model can consider at once, including prompt, history and response.
10. No. It is more repeatable, but identical output is not guaranteed.

Score yourself and send me the number.

### 4. Weekly scorecard

| Item | Your number |
| --- | --- |
| Lessons completed (of 7) | |
| Project 1 finished (yes / no) | |
| Flashcard pairs in `flashcards.md` | |
| Self-quiz score (of 10) | |
| Biggest struggle | |
| Biggest win | |

## Review dates

Revisit the cheat sheet on Day 14, Day 28 and Day 35.
