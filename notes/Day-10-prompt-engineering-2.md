# Day 10 (Tue Oct 20): Prompt Engineering II: XML Tags, System Prompts, Structured Output

**Time:** about 2.5-3 hrs · **Goal:** structure prompts so they are unambiguous, get machine-readable output, and validate that output with code.

## Revisit first (10 min)

Answer these without notes, then check `flashcards.md`:

1. How do you find and handle missing values in pandas?
2. How do you filter a DataFrame on two conditions?
3. What are the five habits of a good prompt?
4. What is few-shot prompting, and what is the risk of using only one example?

## Schedule

| Block | Time | Task |
| --- | --- | --- |
| A | 45 min | Study the concepts below |
| B | 55 min | Hands-on: restructure your prompt, get JSON, validate it with a script |
| C | 30 min | Drill: SQL window functions |
| D | 30 min | Write your note, write your own flashcards, explain aloud for 2 min |

## Concepts

### XML tags: separate instructions from data

When a prompt mixes instructions, documents and examples in one block of text, the model can confuse them. **XML-style tags** give each part a clear label.

```text
<context>
We are testing the login page of a banking web app.
</context>

<user_story>
As a customer, I want to log in with my username and password so that
I can see my account balance.
</user_story>

<task>
Write test cases for the user story above.
</task>

<format>
Return a JSON array. Each item has the fields: id, title, steps, expected.
</format>
```

Why it helps:
1. **Clarity.** The model can tell your instructions from the content you are asking about.
2. **Reference.** You can say "using the story in `<user_story>` tags...".
3. **Easy to reuse.** You swap the content inside one tag and keep the rest.

There are no magic tag names. Pick clear ones and **use them consistently**. Tags help, but they do not make untrusted text safe. Week 6 covers prompt injection properly.

### System prompts

A **system prompt** is the standing set of instructions and role for a whole conversation. It is where you put the role, tone, rules and format that should apply to every turn. In the API it is a separate `system` field, which you meet on Day 11.

```text
You are a senior QA engineer. You write precise, atomic test cases.
You never invent features that are not described. If information is
missing, say what is missing instead of guessing.
```

### Structured output

When code will read the model's answer, ask for a predictable format, usually JSON:

1. Name the exact fields you want.
2. Show one example of the format.
3. Say "return only the JSON, with no extra text".
4. **Always validate the result in code.** A model may still add text or skip a field.

Later in the plan (Day 17), you will see the more reliable approaches in the API. Check the current docs for the options available for your model.

### Key ideas

1. **Tags separate instructions from content.**
2. **The system prompt holds the rules that apply to every turn.**
3. **For code to consume output, specify the format and validate it.**
4. **Never trust model output blindly.** Validation turns "usually right" into a checked system.
5. **Your QA skill is the edge:** schema checks, edge cases and failure handling.

## Hands-on

### Part 1: Restructure your prompt (in the Claude app)

1. Take your best prompt from Day 9.
2. Rewrite it with tags: `<context>`, `<user_story>`, `<task>`, `<format>`.
3. Ask for a **JSON array** with the fields `id`, `title`, `steps` (a list) and `expected`.
4. Add the line "Return only the JSON, with no extra text".
5. Run it. Does Claude follow the format exactly? Run it twice and compare.

Save the improved prompt to `prompts/test-case-generator.md` as version 2.

### Part 2: Validate the output with code

Copy Claude's JSON output into a file called `cases.json`. Create `validate_cases.py` in `code/day10`:

```python
import json
import sys

REQUIRED = ["id", "title", "steps", "expected"]


def validate(cases):
    errors = []
    for i, case in enumerate(cases):
        for field in REQUIRED:
            if field not in case:
                errors.append(f"case {i}: missing '{field}'")
        if "steps" in case and not isinstance(case["steps"], list):
            errors.append(f"case {i}: 'steps' must be a list")
    return errors


if __name__ == "__main__":
    path = sys.argv[1]
    with open(path) as f:
        try:
            cases = json.load(f)
        except json.JSONDecodeError as e:
            print("Not valid JSON:", e)
            sys.exit(1)
    problems = validate(cases)
    print("OK" if not problems else "\n".join(problems))
```

Run it with `python3 validate_cases.py cases.json`. Then break the file on purpose (delete a field, add some text before the JSON) and watch the script catch it.

## Drill (30 min): SQL window functions

A **window function** calculates across a set of related rows **without collapsing them** the way `GROUP BY` does. Using `tests.db`:

```sql
SELECT test_name, duration,
       RANK() OVER (ORDER BY duration DESC) AS slowest_rank
FROM test_runs
```

Exercises:
1. Run the query above. Expected: rank 1 is 3.9, rank 2 is 3.4, rank 3 is 3.1.
2. Find the **slowest run per browser**, using `ROW_NUMBER() OVER (PARTITION BY browser ORDER BY duration DESC)` inside a CTE, then keep rows where the number is 1. Expected: chrome 3.4 (`checkout_test`), firefox 3.9 (`checkout_test`).
3. In your own words: how is a window function different from `GROUP BY`?

## Interview questions

1. **Why use XML tags in prompts?**
   They separate instructions, documents and examples, so the model does not confuse them. They also let you refer to a section by name and reuse the structure.

2. **What is a system prompt, and what goes in it?**
   Standing instructions for a conversation: the role, tone, rules and format. The user prompt then carries the specific request each turn.

3. **How do you get reliable JSON from a model?**
   Name the fields, show an example, say to return only JSON, and validate the result in code. For stronger guarantees, use API features designed for structured output, and check the current docs.

4. **Why validate model output in code?**
   Output is probabilistic. It can add text, omit a field or use the wrong type. Validation catches these failures before they reach other systems.

5. **What does your validation check?**
   That the text parses as JSON, that required fields exist, and that types are right (for example `steps` is a list). Real systems add value checks and retries.

6. **Why put documents and data inside tags?**
   It marks them as content to work on, not instructions to follow, and it makes the prompt easier to maintain. Tags alone do not fully prevent prompt injection.

7. **Where should long documents go in a prompt?**
   Place long documents near the top and the question or instruction at the end, clearly separated. This tends to improve results.

8. **How do you handle a model that adds explanation around the JSON?**
   Tighten the instruction ("return only the JSON"), give an example, and strip or reject extra text in code. Better still, use an API mechanism that enforces structure.

9. **What would you do when validation fails?**
   Retry with the error message included, log the failure, and after a few attempts fail safely or send the item for human review.

10. **How does a QA engineer add value to LLM features?**
    By treating outputs as untrusted data: defining schemas, building edge-case sets, testing for regressions and measuring failure rates instead of assuming the model is right.

## Official links

- Prompting best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Prompt engineering overview: https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview

## My own words (fill in)

- One thing that surprised me:
- My 2-minute explanation:
- Flashcards I wrote myself today:

## Review dates

Revisit on Day 11, Day 13, Day 17 and Day 31.
