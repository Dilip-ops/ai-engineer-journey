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
