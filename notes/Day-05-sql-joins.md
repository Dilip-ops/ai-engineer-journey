# Day 5 (Thu Oct 15): SQL II: JOINs

**Time:** about 2.5-3 hrs · **Goal:** combine two tables with INNER JOIN and LEFT JOIN, and use joins with GROUP BY.

## Revisit first (10 min)

Answer these without notes, then check `flashcards.md`:

1. `WHERE` vs `HAVING`?
2. `COUNT(*)` vs `COUNT(column)`?
3. List vs tuple vs set vs dict?
4. What does `with open(...) as f` guarantee?

## Schedule

| Block | Time | Task |
| --- | --- | --- |
| A | 45 min | Study the concepts below |
| B | 50 min | Hands-on: add a second table and run join queries |
| C | 30 min | Drill: 6 exercises (below) |
| D | 30 min | Write your note, add 5-8 pairs to `flashcards.md`, explain aloud for 2 min |

## Concepts

Real databases split data across tables to avoid repetition. A **JOIN** combines rows from two tables using a column they share.

| Term | Meaning |
| --- | --- |
| Primary key | A column that uniquely identifies each row in its table |
| Foreign key | A column that points to another table's primary key |
| `INNER JOIN` | Keeps only rows that have a match in **both** tables |
| `LEFT JOIN` | Keeps **all** rows from the left table, with NULLs where the right table has no match |
| `ON` | The condition that says how rows match |

**Java analogy:** a foreign key is like an object reference. A join is how SQL follows that reference.

### Key ideas

1. **INNER JOIN drops unmatched rows. LEFT JOIN keeps them.**
2. **LEFT JOIN plus `WHERE right.id IS NULL` finds rows with no match.** For example, tests that were never run.
3. **Use table aliases** (`FROM test_runs r JOIN test_cases c`) so queries stay short and clear.
4. **Joining can multiply rows.** If one row on the left matches several on the right, you get several rows back.
5. **With a LEFT JOIN, put filters on the right table in `ON`, not `WHERE`.** A `WHERE` filter on the right table turns it back into an INNER JOIN.

## Hands-on

Create `setup_joins.py` in `code/day05` (copy your `tests.db` and `run_query.py` from Day 4 into the same folder, or re-run Day 4's `setup_db.py` there):

```python
import sqlite3

conn = sqlite3.connect("tests.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS test_cases")
cur.execute("""
CREATE TABLE test_cases (
    test_name TEXT PRIMARY KEY,
    module TEXT,
    owner TEXT
)
""")

cases = [
    ("login_test", "auth", "Asha"),
    ("checkout_test", "payments", "Ravi"),
    ("search_test", "catalog", "Meena"),
    ("profile_test", "account", "Asha"),
    ("logout_test", "auth", "Ravi"),
]
cur.executemany("INSERT INTO test_cases VALUES (?, ?, ?)", cases)

conn.commit()
conn.close()
print("test_cases created with", len(cases), "rows")
```

Run `python3 setup_joins.py`, then try these queries with `run_query.py`:

```bash
python3 run_query.py "SELECT r.id, r.test_name, r.status, c.module, c.owner FROM test_runs r INNER JOIN test_cases c ON r.test_name = c.test_name"

python3 run_query.py "SELECT c.test_name, c.module FROM test_cases c LEFT JOIN test_runs r ON c.test_name = r.test_name WHERE r.id IS NULL"

python3 run_query.py "SELECT c.module, COUNT(*) AS failures FROM test_runs r INNER JOIN test_cases c ON r.test_name = c.test_name WHERE r.status = 'failed' GROUP BY c.module"

python3 run_query.py "SELECT c.owner, ROUND(AVG(r.duration), 2) AS avg_duration FROM test_runs r INNER JOIN test_cases c ON r.test_name = c.test_name GROUP BY c.owner"
```

**Predict each output before running it.** For the second query, which test do you expect to see, and why?

## Drill (30 min)

1. List every run with its module and owner (INNER JOIN).
2. Count the runs per owner.
3. List the modules that have at least one failed run.
4. Find the tests with no runs (LEFT JOIN, then `IS NULL`).
5. Show the average duration per module, highest first.
6. Stretch: show the number of runs per test **including tests with zero runs**. Hint: use a LEFT JOIN with `COUNT(r.id)`, and think about why `COUNT(*)` would give the wrong answer. This links to Day 4.

## Interview questions

1. **What is the difference between INNER JOIN and LEFT JOIN?**
   INNER JOIN returns only rows with a match in both tables. LEFT JOIN returns every row from the left table, filling the right table's columns with NULL where there is no match.

2. **What are a primary key and a foreign key?**
   A primary key uniquely identifies each row in a table. A foreign key is a column that references another table's primary key, linking the two tables.

3. **How do you find rows in one table that have no match in another?**
   Use a LEFT JOIN and filter for `right_table.key IS NULL`. For example, tests that were never run.

4. **What is a Cartesian product, and how does it happen accidentally?**
   Every row of one table paired with every row of the other. It happens when you join without an `ON` condition (or with a wrong one), and it produces a huge, meaningless result.

5. **What is a self join?**
   A table joined to itself using two aliases, for example to match employees with their managers stored in the same table.

6. **Why can a join return more rows than either table?**
   When one row matches several rows on the other side, the result has one row per match. This is why counts can look inflated after a join.

7. **`ON` vs `WHERE` in a LEFT JOIN?**
   `ON` decides how rows match. A `WHERE` condition on the right table removes the NULL rows that a LEFT JOIN kept, which effectively turns it into an INNER JOIN. Put right-table filters in `ON` to keep the LEFT JOIN behaviour.

8. **JOIN vs subquery?**
   Both can combine data. Joins are usually clearer and often faster for combining columns from two tables. Subqueries suit "is this value in that set" questions. Modern databases optimise both.

9. **Why do indexes matter for joins?**
   Joins look up matching rows by the join column. An index on that column lets the database find matches quickly instead of scanning the whole table.

10. **How does a QA engineer use joins?**
    To verify that related records line up after an action (for example an order and its payment), to find orphaned or missing records, and to build test reports that combine run results with test metadata.

## My own words (fill in)

- One thing that surprised me:
- My 2-minute explanation:
- Flashcards added today:

## Review dates

Revisit on Day 6, Day 8, Day 12 and Day 26.
