python3 run_query.py "SELECT test_name, status FROM test_runs"

python3 run_query.py "SELECT * FROM test_runs WHERE status = 'failed' AND browser = 'chrome'"

python3 run_query.py "SELECT test_name, duration FROM test_runs ORDER BY duration DESC LIMIT 3"

python3 run_query.py "SELECT status, COUNT(*) AS runs FROM test_runs GROUP BY status"

python3 run_query.py "SELECT test_name, COUNT(*) AS runs, ROUND(AVG(duration), 2) AS avg_duration FROM test_runs GROUP BY test_name"

python3 run_query.py "SELECT test_name, COUNT(*) AS failures FROM test_runs WHERE status = 'failed' GROUP BY test_name HAVING COUNT(*) >= 2"