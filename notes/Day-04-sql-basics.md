# Day 4 (Wed Oct 14): SQL I: SELECT, WHERE, GROUP BY

**Time:** about 2.5-3 hrs · **Goal:** query a table with SELECT, WHERE, ORDER BY, LIMIT, GROUP BY and HAVING, using SQLite from Python with nothing to install.

## Revisit first (10 min)

Answer these without notes, then check `flashcards.md`:

1. DataFrame vs Series?
2. `loc` vs `iloc`?
3. What is the difference between a workflow and an agent?
4. What does MCP do, and what does it not do?

## Schedule

| Block | Time | Task |
| --- | --- | --- |
| A | 45 min | Study the concepts below |
| B | 50 min | Hands-on: build a small SQLite database and run queries |
| C | 30 min | Drill: 6 exercises (below) |
| D | 30 min | Write your note, add 5-8 pairs to `flashcards.md`, explain aloud for 2 min |

## Setup

SQLite is built into Python, so there is nothing to install. Make a folder `code/day04` and put the two scripts below in it. You do not need a virtual environment for this one, but using your existing one is fine.

## Concepts

**SQL** is the language for asking questions of a relational database. You already know the idea from JDBC and JPA. The SQL itself is the same.

| Clause | What it does |
| --- | --- |
| `SELECT` | Chooses the columns to return |
| `FROM` | Names the table |
| `WHERE` | Filters individual rows |
| `GROUP BY` | Collapses rows into groups |
| `HAVING` | Filters the groups after aggregation |
| `ORDER BY` | Sorts the result |
| `LIMIT` | Returns only the first N rows |

**Aggregate functions** summarise a group: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`.

### The order the database really runs a query

You write SELECT first, but the database processes it like this:

1. `FROM`
2. `WHERE`
3. `GROUP BY`
4. `HAVING`
5. `SELECT`
6. `ORDER BY`
7. `LIMIT`

This explains common errors, for example why you cannot use a column alias in `WHERE`.

### Key ideas

1. **`WHERE` filters rows before grouping. `HAVING` filters groups after.**
2. **`NULL` is not equal to anything.** Use `IS NULL`, never `= NULL`.
3. **Always pair `LIMIT` with `ORDER BY`.** Without an order, which rows you get is not guaranteed.
4. **`COUNT(*)` counts rows. `COUNT(column)` skips NULLs.**

## Hands-on

Create `setup_db.py`:

```python
import sqlite3

conn = sqlite3.connect("tests.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS test_runs")
cur.execute("""
CREATE TABLE test_runs (
    id INTEGER PRIMARY KEY,
    test_name TEXT,
    status TEXT,
    duration REAL,
    browser TEXT,
    run_date TEXT
)
""")

rows = [
    (1, "login_test", "passed", 1.2, "chrome", "2026-10-01"),
    (2, "checkout_test", "failed", 3.4, "chrome", "2026-10-01"),
    (3, "search_test", "passed", 0.8, "firefox", "2026-10-01"),
    (4, "profile_test", "passed", 0.9, "firefox", "2026-10-02"),
    (5, "login_test", "failed", 1.5, "firefox", "2026-10-02"),
    (6, "checkout_test", "failed", 3.9, "firefox", "2026-10-02"),
    (7, "search_test", "passed", 0.7, "chrome", "2026-10-03"),
    (8, "profile_test", "passed", 1.0, "chrome", "2026-10-03"),
    (9, "login_test", "passed", 1.1, "chrome", "2026-10-03"),
    (10, "checkout_test", "passed", 3.1, "chrome", "2026-10-03"),
]
cur.executemany("INSERT INTO test_runs VALUES (?, ?, ?, ?, ?, ?)", rows)

conn.commit()
conn.close()
print("tests.db created with", len(rows), "rows")
```

Create `run_query.py`:

```python
import sqlite3
import sys

sql = sys.argv[1]
conn = sqlite3.connect("tests.db")
cur = conn.execute(sql)

columns = [d[0] for d in cur.description]
print(" | ".join(columns))
for row in cur.fetchall():
    print(" | ".join(str(v) for v in row))

conn.close()
```

Run `python3 setup_db.py` once, then try these queries one at a time:

```bash
python3 run_query.py "SELECT test_name, status FROM test_runs"

python3 run_query.py "SELECT * FROM test_runs WHERE status = 'failed' AND browser = 'chrome'"

python3 run_query.py "SELECT test_name, duration FROM test_runs ORDER BY duration DESC LIMIT 3"

python3 run_query.py "SELECT status, COUNT(*) AS runs FROM test_runs GROUP BY status"

python3 run_query.py "SELECT test_name, COUNT(*) AS runs, ROUND(AVG(duration), 2) AS avg_duration FROM test_runs GROUP BY test_name"

python3 run_query.py "SELECT test_name, COUNT(*) AS failures FROM test_runs WHERE status = 'failed' GROUP BY test_name HAVING COUNT(*) >= 2"
```

For each one, predict the output before you run it. That is the learning.

## Drill (30 min)

Write each query and run it:

1. All tests that took longer than 3 seconds.
2. The number of runs per browser.
3. The average duration per browser, rounded to 2 decimals.
4. Tests whose average duration is above 2 seconds (use `HAVING`).
5. The 3 fastest passing tests.
6. Stretch: the pass rate per test. Hint: `SUM(CASE WHEN status = 'passed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)`.

## Interview questions

1. **What is the difference between `WHERE` and `HAVING`?**
   `WHERE` filters individual rows before grouping. `HAVING` filters groups after aggregation, so it can use aggregate functions like `COUNT(*)`.

2. **In what order does a database process a SELECT query?**
   FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY, LIMIT.

3. **`COUNT(*)` vs `COUNT(column)` vs `COUNT(DISTINCT column)`?**
   `COUNT(*)` counts all rows. `COUNT(column)` counts rows where that column is not NULL. `COUNT(DISTINCT column)` counts unique non-NULL values.

4. **How does SQL treat NULL?**
   NULL means unknown, so `= NULL` is never true. Use `IS NULL` or `IS NOT NULL`. Most aggregate functions ignore NULLs, except `COUNT(*)`.

5. **`DISTINCT` vs `GROUP BY`?**
   Both can remove duplicates. `DISTINCT` just de-duplicates the result. `GROUP BY` forms groups so you can apply aggregates to each one.

6. **Can you use a SELECT alias in `WHERE`?**
   Not in standard SQL, because `WHERE` runs before `SELECT`. You can use the alias in `ORDER BY`.

7. **What is a primary key?**
   A column (or set of columns) that uniquely identifies each row. It cannot be NULL or duplicated.

8. **Why use `ORDER BY` with `LIMIT`?**
   Without `ORDER BY`, the database may return any rows. Ordering makes the "top N" result meaningful and repeatable.

9. **Why does a QA engineer need SQL?**
   To verify data after tests, set up and clean test data, investigate failures by querying the database directly, and check that a feature wrote the right records.

10. **Pandas vs SQL for the same job?**
    Both can filter, group and aggregate. SQL runs inside the database next to the data and scales to large tables. Pandas runs in memory in your script and suits exploration and preparation. The concepts transfer directly between them.

## My own words (fill in)

- One thing that surprised me:
- My 2-minute explanation:
- Flashcards added today:

## Review dates

Revisit on Day 5, Day 7, Day 11 and Day 25.
