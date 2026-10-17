# Day 2 (Mon Oct 12): Python for Java Developers

**Time:** about 2.5-3 hrs · **Goal:** write small, clean Python scripts that read files and JSON, and set up an isolated project environment.

## Schedule

| Block | Time | Task |
| --- | --- | --- |
| A | 60 min | Study the Java-to-Python mapping and run the examples |
| B | 40 min | Hands-on: virtual environment, script that reads a JSON test-results file |
| C | 30 min | Drill: 3 small Python exercises (below) |
| D | 30 min | Write your note, add 5-8 pairs to `notes/flashcards.md`, explain aloud for 2 min |

## Java to Python: what changes

| Idea | Java | Python |
| --- | --- | --- |
| Typing | Static, declared | Dynamic; type hints are optional (`def f(x: int) -> str:`) |
| Blocks | Braces `{}` | Indentation (4 spaces) |
| Entry point | `public static void main` | `if __name__ == "__main__":` |
| Lists / maps | `ArrayList`, `HashMap` | `list` `[]`, `dict` `{}` |
| Loops | `for (int i...)`, enhanced for | `for x in items:`, `range(n)` |
| String format | `String.format`, `+` | f-strings: `f"Passed: {count}"` |
| Null | `null` | `None` |
| Exceptions | `try / catch / finally` | `try / except / finally` |
| Resources | try-with-resources | `with open(...) as f:` |
| Packages | Maven / Gradle | `pip` plus virtual environments |
| Classes | Required for most code | Optional; plain functions are normal |

## Key ideas

1. **Indentation is syntax.** A wrong indent is a bug or an error.
2. **Everything is an object, and functions are values.** You can pass functions around, which is why decorators and callbacks look simple.
3. **Use a virtual environment for every project.** It keeps each project's packages separate, like a per-project Maven repository.
4. **Read and write files with `with`.** It closes the file for you.
5. **JSON maps directly to dict and list.** `json.load(f)` gives you ordinary Python data.

## Commands (run these in your terminal)

```bash
mkdir day02 && cd day02
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install requests
python --version
```

## Hands-on: summarise a test-results file

Create `results.json`:

```json
[
  {"name": "login_test", "status": "passed", "duration": 1.2},
  {"name": "checkout_test", "status": "failed", "duration": 3.4},
  {"name": "search_test", "status": "passed", "duration": 0.8}
]
```

Create `summary.py`:

```python
import json


def load_results(path: str) -> list[dict]:
    with open(path) as f:
        return json.load(f)


def summarise(results: list[dict]) -> dict:
    passed = [r for r in results if r["status"] == "passed"]
    failed = [r for r in results if r["status"] == "failed"]
    return {
        "total": len(results),
        "passed": len(passed),
        "failed": len(failed),
        "failed_names": [r["name"] for r in failed],
    }


if __name__ == "__main__":
    summary = summarise(load_results("results.json"))
    print(f"Total: {summary['total']}, Passed: {summary['passed']}, Failed: {summary['failed']}")
    print("Failed tests:", ", ".join(summary["failed_names"]) or "none")
```

Run it with `python summary.py`. Then change the file and see the output change.

## Drill (30 min)

1. Print the average `duration` of all tests.
2. Print the names of tests slower than 1 second, sorted by duration.
3. Handle a missing file: catch `FileNotFoundError` and print a friendly message.

## Interview questions

1. **Is Python compiled or interpreted?**
   Python source is compiled to bytecode, which the Python interpreter then runs. In practice people call it interpreted.

2. **What is a virtual environment, and why use one?**
   An isolated directory with its own Python packages, so each project has its own dependency versions and does not interfere with others.

3. **List vs tuple vs set vs dict?**
   List: ordered and mutable. Tuple: ordered and immutable. Set: unordered unique items. Dict: key-value pairs.

4. **What are list comprehensions?**
   A compact way to build a list from an iterable, such as `[r["name"] for r in results if r["status"] == "failed"]`.

5. **What does `with open(...) as f` do?**
   It is a context manager that opens the file and guarantees it is closed, even if an error occurs.

6. **What is `None`, and how do you check for it?**
   The single null value in Python. Check with `x is None`, not `x == None`.

7. **What does `if __name__ == "__main__":` do?**
   It runs the code only when the file is executed directly, not when it is imported as a module.

8. **Mutable default arguments: why are they dangerous?**
   A default like `def f(x=[])` is created once and shared across calls, so changes persist. Use `None` and create a new list inside the function.

9. **How would a QA engineer use Python scripts around AI work?**
   For parsing test results, calling APIs, preparing test data and running evaluation checks. That is why Python is worth learning even as a Java developer.

10. **Java vs Python: when would you choose each?**
    Java suits large, long-lived, strongly typed backend systems. Python suits quick scripting, data work and the AI tooling ecosystem. Many teams use both.

## My own words (fill in)

- One thing that surprised me:
- My 2-minute explanation:
- Flashcards added today:

## Review dates

Revisit on Day 3, Day 5, Day 9 and Day 23.
