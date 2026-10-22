# Day 11: API key and your first Messages API call in Python

Date: Thu Oct 22, 2026 (calendar Day 12, lag 2)
Phase 1, Week 2. Drill today: SQL (LEFT JOIN plus HAVING) and pandas (missing values, two-condition filters), because both are weak spots.

| Block | Minutes |
|---|---|
| Revision questions (section 0) | 10 |
| Main topic (sections 1-5) | 100 |
| SQL and pandas drill (section 6) | 30 |
| Notes, flashcards, own cards | 20 |
| Explain aloud (section 8) | 10 |

---

## 0. Revision first (answer from memory, then check the bottom of this file)

1. (Day 4) What is the difference between `WHERE` and `HAVING`? Give the reason.
2. (Day 8) Name the job each model family is best at: Haiku, Sonnet, Opus, Fable. How do you confirm a choice for YOUR task?
3. (Pandas) Write the filter for rows where `status == "FAILED"` AND `duration > 2`. Why the parentheses, and why `&` instead of `and`?
4. (Pandas) How do you count missing values per column, and name two ways to handle them?
5. (Weak spot) LEFT JOIN, no match found: what do the right-side columns hold, and what do `COUNT(r.id)` and `COUNT(*)` return?
6. (Weak spot) Why is `def f(x, items=[])` a bug?

---

## 1. The big picture

You have used Claude in the app. Today you call it from your own code. The app is a finished product; the **API** is the engine you build products on. Every agent, MCP client and eval harness in this plan sits on top of the call you write today.

QA analogy: using the app is manual testing through the UI. Using the API is testing through the service layer, where you control every input, can log every output and can automate it.

---

## 2. Key concepts

| Concept | What to remember |
|---|---|
| API key | A secret string that identifies and bills your account. Treat it like a password. |
| Console | Where you create the key and add prepaid credit. API usage is billed **separately** from the Claude chat app plan. |
| Messages API | The main endpoint. You send a list of messages, you get back one reply. |
| Stateless | The API remembers nothing between calls. For a conversation you resend the history each time (Day 12). |
| `model` | Which Claude model to use. Model names change over time, so copy the current ID from the docs. |
| `max_tokens` | Upper limit on the reply length, required. It caps cost and runaway output. |
| `system` | Optional top-level field for the system prompt (Day 10). It is NOT a message. |
| `messages` | List of `{"role": "user" or "assistant", "content": ...}`. |
| Response | `content` is a **list of blocks** (text blocks now, tool-use blocks later), plus `stop_reason` and `usage` (input and output token counts). |

Why `stop_reason` matters: `end_turn` means Claude finished naturally; `max_tokens` means the reply was **cut off**. A pipeline that ignores this will parse truncated JSON.

---

## 3. Setup (Mac, VS Code)

1. Create an account and key in the Claude Console. Add a small prepaid credit (a few dollars is plenty for Phase 1). Check current pricing there.
2. In your repo, create the project folder and virtual environment:

```bash
cd ai-engineer-journey/code
python3 -m venv .venv
source .venv/bin/activate
pip install anthropic
```

3. Set the key as an environment variable in the same terminal (the SDK reads `ANTHROPIC_API_KEY` automatically):

```bash
export ANTHROPIC_API_KEY="paste-your-key-here"
```

4. **Never commit the key.** Add these lines to `.gitignore` before your next `git add`:

```text
.venv/
.env
```

   Never paste the key into code, notes, flashcards or chat. If it ever lands in GitHub, delete that key in the Console and create a new one immediately.

---

## 4. Your first call

Save as `code/first_call.py`:

```python
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment

message = client.messages.create(
    model="claude-sonnet-5-5",  # confirm the current model ID in the docs
    max_tokens=300,
    system="You are a QA assistant. Be concise.",
    messages=[
        {"role": "user", "content": "Give me 3 negative test cases for a login form."}
    ],
)

block = message.content[0]
if block.type == "text":
    print(block.text)

print("stop_reason:", message.stop_reason)
print("tokens in/out:", message.usage.input_tokens, message.usage.output_tokens)
```

Run it with `python first_call.py` (inside the activated venv, `python` works).

### Handle errors like a tester

```python
import anthropic

client = anthropic.Anthropic()

try:
    message = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=300,
        messages=[{"role": "user", "content": "Say hello in five words."}],
    )
    print(message.content[0].text)
except anthropic.AuthenticationError:
    print("Bad or missing API key. Check ANTHROPIC_API_KEY.")
except anthropic.RateLimitError:
    print("Rate limited. Wait and retry (Day 12 covers backoff).")
except anthropic.APIConnectionError:
    print("Network problem reaching the API.")
except anthropic.APIStatusError as exc:
    print("API returned an error:", exc.status_code)
```

---

## 5. Experiments (this is the real learning, 20-25 min)

Do each one and write one line in your error log or note.

1. Set `max_tokens=20`. What is `stop_reason`, and what happened to the answer?
2. Unset the key (`unset ANTHROPIC_API_KEY`) and run again. Which exception? Then export it again.
3. Run the same prompt three times. Are the replies identical?
4. Add `temperature=0` and run three more times. More repeatable? Identical every time? Why not guaranteed? (If the API rejects a parameter for your model, read the docs and note it.)
5. Move the instruction between `system` and the user message. Does the answer change?
6. Print `usage` for a short and a long prompt. How do input tokens grow? This is the root of cost.

---

## 6. Drills (30 min)

### SQL
Tables: `tests(id, name, suite)` and `test_runs(id, test_id, status, run_date)`.

1. List every test with its number of runs, **including tests with zero runs**.
2. List tests that have **no failed runs at all**, including tests that have never run.

Answers are at the bottom.

### Pandas
Given `df` with columns `test`, `status`, `duration` where some `duration` values are missing:

1. Count missing values per column.
2. Show rows where status is FAILED and duration is over 2 seconds.
3. Replace missing durations with the median duration.

Run this to check your answers:

```python
import pandas as pd

df = pd.DataFrame({
    "test": ["a", "b", "c", "d"],
    "status": ["FAILED", "PASSED", "FAILED", "PASSED"],
    "duration": [3.1, None, 1.2, 2.5],
})

print(df.isna().sum())
print(df[(df["status"] == "FAILED") & (df["duration"] > 2)])
df["duration"] = df["duration"].fillna(df["duration"].median())
print(df)
```

---

## 7. Interview questions and answers

**Q1. What is the difference between using Claude in the app and via the API?**
The app is a finished product with its own interface and plan. The API gives your code direct control over the model, system prompt, parameters and output, so it can be automated, tested and embedded in other systems. That control is why every agent and eval harness is built on the API, because they need to run without a person typing.

**Q2. The Messages API is stateless. What does that mean for a chatbot?**
The server stores nothing between calls, so the application must send the full conversation history with every request. This means you control what the model sees and can trim or summarize history, and it also means token cost grows with conversation length.

**Q3. Why does `max_tokens` matter, and what do you check after a call?**
It caps the reply length and therefore cost and latency. After the call, check `stop_reason`: if it is `max_tokens`, the output was truncated, so downstream parsing (such as JSON) may break, because the model stopped mid-answer.

**Q4. How do you handle an API key safely?**
Keep it in an environment variable or a secrets manager, never in source code or git, add `.env` to `.gitignore`, use separate keys per project, and rotate immediately if exposed. This matters because anyone with the key can spend your credit, so treat it like a password.

**Q5. What errors should a production client handle?**
Authentication errors (fix config, do not retry), rate limits (retry with exponential backoff), connection errors and server errors (retry a limited number of times), and invalid requests (fix the input). Distinguishing retryable from non-retryable errors prevents both lost work and infinite retry loops.

**Q6. Why is the response `content` a list rather than a string?**
A reply can contain several blocks of different types, such as text and, once you use tools, tool-use requests. A list lets one response carry both, so code should check each block's `type` instead of assuming `content[0]` is text.

---

## 8. Explain aloud (2 minutes)

"Explain to a Java developer what happens when my Python script calls the Messages API, from key to response, and what I must check in the response." End each part with "because".

---

## 9. Your own flashcards and the "Day 11 done" reply

Add the provided cards from `flashcards-day-11.md`, then write 3-4 of your own in your own words.

When you reply "Day 11 done", include:
- Your answers to the 6 revision questions
- Your SQL and pandas answers
- The output of `first_call.py` (**never include the key**), including `stop_reason` and token counts
- What you saw in experiments 1 and 4
- Your own flashcards

If you hit an error or get stuck, paste the full error text (without the key) and I'll debug it with you.

---

## Answers (check after you try)

### Revision answers
1. `WHERE` filters individual rows **before** grouping; `HAVING` filters groups **after** aggregation, so only `HAVING` can use aggregate functions like `COUNT(*) > 3`.
2. Haiku: fast and low-cost, for simple high-volume tasks. Sonnet: smart and efficient, the everyday default. Opus: long-running agentic coding and knowledge work. Fable: the most demanding reasoning. Confirm with your own evals on your own data, because benchmark reputation does not guarantee fit for your task.
3. `df[(df["status"] == "FAILED") & (df["duration"] > 2)]`. `&` works element by element across the Series, whereas `and` tries to turn a whole Series into one True/False and raises an ambiguity error. Parentheses are needed because `&` binds tighter than `==` and `>`, so without them Python evaluates the wrong part first.
4. `df.isna().sum()` (or `isnull()`, same thing). Handle by `dropna()` (remove rows), `fillna(value)` (replace with a constant, median or mean), or by keeping them and flagging them. The right choice depends on why the values are missing, because filling can hide a real data problem.
5. NULL in every right-side column. `COUNT(r.id)` returns 0 and `COUNT(*)` returns 1, because `COUNT(column)` skips NULLs while `COUNT(*)` counts the row itself.
6. The default list is created once at definition time and shared across all calls using the default, so data leaks between calls. Use `items=None` and create a new list inside the function.

### SQL answers

```sql
-- 1. Every test with its run count, including zero
SELECT t.name, COUNT(r.id) AS run_count
FROM tests t
LEFT JOIN test_runs r ON r.test_id = t.id
GROUP BY t.id, t.name;
-- COUNT(r.id), not COUNT(*): unmatched tests have NULL r.id, so they count 0, not 1.

-- 2. Tests with no failed runs (including never-run tests)
SELECT t.name
FROM tests t
LEFT JOIN test_runs r
       ON r.test_id = t.id AND r.status = 'FAILED'
GROUP BY t.id, t.name
HAVING COUNT(r.id) = 0;
-- The FAILED filter is in ON, not WHERE. In WHERE it would remove the NULL rows
-- and turn the LEFT JOIN into an INNER JOIN, dropping the tests we want.
```

### Experiment hints
1. `stop_reason` is `max_tokens` and the answer is cut off mid-sentence.
2. `anthropic.AuthenticationError`.
3. and 4. Replies usually differ without temperature 0 and are much more similar with it, but identical output is still not guaranteed, because floating-point differences can flip near-tied tokens.
