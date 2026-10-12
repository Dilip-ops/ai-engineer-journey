import json


def load_results(path: str) -> list[dict]:
    """Opens a JSON file safely and returns its data as a list of dictionaries.
    
    Catches FileNotFoundError if the file doesn't exist.
    """
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ Error: The file '{path}' could not be found. Please check the file path.")
        return []


def summarise(results: list[dict]) -> dict:
    """Processes the test results list and generates a metrics summary dictionary."""
    # Safety check: If the list is empty (missing file or empty JSON), return default empty metrics
    if not results:
        return {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "failed_names": [],
            "avg_duration": 0.0,
            "slow_tests": []
        }

    # 1. Filter statuses using list comprehensions
    passed = [r for r in results if r["status"] == "passed"]
    failed = [r for r in results if r["status"] == "failed"]
    
    # 2. Calculate average duration of all tests
    total_duration = sum(r["duration"] for r in results)
    avg_duration = total_duration / len(results)

    # 3. Filter tests slower than 1.0 second and sort them by duration ascendingly
    slow_tests_raw = [r for r in results if r["duration"] > 1.0]
    slow_tests_sorted = sorted(slow_tests_raw, key=lambda r: r["duration"])
    slow_test_names = [r["name"] for r in slow_tests_sorted]

    # Return everything inside a single unified summary dictionary
    return {
        "total": len(results),
        "passed": len(passed),
        "failed": len(failed),
        "failed_names": [r["name"] for r in failed],
        "avg_duration": avg_duration,
        "slow_tests": slow_test_names,
    }


if __name__ == "__main__":
    # Attempt to load data
    results_data = load_results("results.json")
    
    # Only run the summary printout if data was successfully loaded
    if results_data:
        summary = summarise(results_data)
        
        # Print counts
        print(f"Total: {summary['total']}, Passed: {summary['passed']}, Failed: {summary['failed']}")
        
        # Print average duration formatted to 2 decimal places
        print(f"Average Duration: {summary['avg_duration']:.2f}s")
        
        # Print list of slow tests (sorted)
        slow_list_str = ", ".join(summary["slow_tests"]) or "none"
        print(f"Tests slower than 1s (sorted): {slow_list_str}")
        
        # Print list of failed tests
        failed_list_str = ", ".join(summary["failed_names"]) or "none"
        print(f"Failed tests: {failed_list_str}")