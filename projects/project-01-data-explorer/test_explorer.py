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