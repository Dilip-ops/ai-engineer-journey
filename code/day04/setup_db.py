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