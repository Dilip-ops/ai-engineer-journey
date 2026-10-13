import json


def load_results(path: str) -> list[dict]:
    with open(path) as f:
        return json.load(f)


def summarise(results: list[dict]) -> dict:
    passed = [r for r in results if r["status"] == "passed"]
    failed = [r for r in results if r["status"] == "failed"]
    total_duration = sum(r["duration"] for r in results)
    avg_duration = total_duration / len(results) if results else 0.0


    return {
        "total": len(results),
        "passed": len(passed),
        "failed": len(failed),
        "failed_names": [r["name"] for r in failed],
        "avg_duration": avg_duration,
    }


if __name__ == "__main__":
    summary = summarise(load_results("results.json"))
    print(f"Total: {summary['total']}, Passed: {summary['passed']}, Failed: {summary['failed']}")
    print(f"Average Duration: {summary['avg_duration']:.2f}s")
    print("Failed tests:", ", ".join(summary["failed_names"]) or "none")