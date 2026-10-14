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