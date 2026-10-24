# Day 12 (zero-cost edition): multi-turn chats, streaming, errors and rate limits

Date: Sat Oct 24, 2026 (calendar Day 14; after this lesson your lag is 2)
Phase 1, Week 2. Uses the `fake_claude.py` you built on Day 11. No key, card or network needed.

| Block | Minutes |
|---|---|
| Revision questions (section 0) | 10 |
| Main topic (sections 1-4) | 100 |
| Drill (section 6) | 30 |
| Notes and flashcards | 20 |
| Explain aloud (section 7) | 10 |

---

## 0. Revision first (answer from memory)

1. Why does `stop_reason == "max_tokens"` matter before you parse a reply?
2. Why is `response.content` a list?
3. In a LEFT JOIN, where must a filter on the right table go to keep unmatched left rows, and why?
4. Why is `def f(x, items=[])` a bug, and what is the fix?
5. Filter a DataFrame on two conditions. Why `&` and parentheses?
6. (Day 11, still open) The six revision answers and SQL/pandas drills from the Day 11 note, if you have not sent them.

---

## 1. Multi-turn chats: the API remembers nothing

The Messages API is **stateless**. For a conversation, your code keeps a list of messages and resends the **whole list** on every call:

```text
call 1: [user]
call 2: [user, assistant, user]
call 3: [user, assistant, user, assistant, user]
```

Consequences you must be able to explain:
- Cost and latency grow every turn, because input tokens grow (Day 6 context window).
- You decide what Claude sees, so you can trim or summarize old turns.
- Roles alternate `user` / `assistant`. The `system` prompt stays a separate top-level field.
- Past the context window the call fails or loses history, so long chats need trimming or summarizing (Week 8 covers context engineering).

QA analogy: each call is a fresh test run with no shared state. You pass state in explicitly, like a fixture.

---

## 2. Streaming

Without streaming you wait for the **whole** reply. With streaming the server sends the reply in small pieces as they are generated, so users see text appear immediately. Total time is similar, but **time to first token** is much shorter, which matters for chat UIs. For batch pipelines (eval runs, JSON extraction) streaming adds complexity for no benefit.

In the real Python SDK it looks like this (read it now, run it when you have a key; confirm the syntax in the current docs):

```text
with client.messages.stream(model=..., max_tokens=..., messages=...) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

Trade-offs to remember: a stream can break halfway (network), so handle errors mid-stream, and you only know the final `stop_reason` and token usage at the end.

---

## 3. Errors and rate limits

| HTTP | Meaning | Retry? |
|---|---|---|
| 400 | Invalid request (bad field, `max_tokens` 0) | No. Fix the input. |
| 401 | Bad or missing API key | No. Fix config. |
| 403 | Not allowed for this key | No. |
| 404 | Unknown model or resource | No. |
| 429 | Rate limited (too many requests or tokens) | **Yes**, after waiting |
| 5xx | Server-side problem (including overloaded) | **Yes**, limited times |
| network | Connection dropped or timed out | **Yes**, limited times |

**Rule:** retry only errors that can succeed later (429, 5xx, network). Never retry 4xx input errors, because the same bad request fails the same way and wastes quota.

**Exponential backoff:** wait 1x, 2x, 4x, 8x the base delay between retries, usually with a little random jitter and a hard maximum number of tries. Jitter prevents many clients retrying at the same instant. If the server sends a `retry-after` hint, respect it. The real SDK already retries some errors automatically (check the current default in the docs), so you tune it instead of writing it from scratch.

---

## 4. Code: all three, offline

Save as `code/chat_demo.py` (same folder as `fake_claude.py`):

```python
"""Day 12 (zero-cost): multi-turn history, streaming, retries with backoff.
Uses fake_claude.py from Day 11 plus the small fakes below. No key, no network."""
import time
from types import SimpleNamespace
from fake_claude import FakeClient


class FakeRateLimitError(Exception):
    """Stands in for anthropic.RateLimitError (HTTP 429). Retryable."""


class FakeBadRequestError(Exception):
    """Stands in for anthropic.BadRequestError (HTTP 400). NOT retryable."""


# ---------- 1. Multi-turn: the API is stateless, so YOU keep the history ----------
def ask(client, history, user_text, max_tokens=300):
    history.append({"role": "user", "content": user_text})
    reply = client.messages.create(
        model="claude-sonnet-5-5", max_tokens=max_tokens, messages=history
    )
    text = "".join(b.text for b in reply.content if b.type == "text")
    history.append({"role": "assistant", "content": text})
    return reply, text


# ---------- 2. Streaming: tokens arrive in small pieces ----------
def fake_stream(text, chunk_words=2):
    words = text.split()
    for i in range(0, len(words), chunk_words):
        yield " ".join(words[i:i + chunk_words]) + " "


# ---------- 3. Retries with exponential backoff ----------
class FlakyClient:
    """Fails with a rate limit twice, then succeeds."""
    def __init__(self):
        self.calls = 0
        self.inner = FakeClient()

    def create(self, **kwargs):
        self.calls += 1
        if self.calls <= 2:
            raise FakeRateLimitError("429: slow down")
        return self.inner.messages.create(**kwargs)


def call_with_retry(create, max_retries=4, base_delay=0.1, **kwargs):
    for attempt in range(max_retries + 1):
        try:
            return create(**kwargs)
        except FakeRateLimitError as exc:
            if attempt == max_retries:
                raise
            delay = base_delay * (2 ** attempt)   # 0.1, 0.2, 0.4 ...
            print(f"  retry {attempt + 1} after {delay:.1f}s ({exc})")
            time.sleep(delay)
        # FakeBadRequestError is deliberately NOT caught: fix the input, do not retry


if __name__ == "__main__":
    client = FakeClient()
    history = []

    print("--- multi-turn ---")
    _, t1 = ask(client, history, "Give me 3 negative test cases for a login form.")
    _, t2 = ask(client, history, "Now make the second one more specific.")
    print("messages sent on 2nd call:", len(history) - 1, "(history grows every turn)")
    print([m["role"] for m in history])

    print("--- streaming ---")
    for piece in fake_stream(t1):
        print(piece, end="", flush=True)
        time.sleep(0.05)
    print()

    print("--- retry ---")
    flaky = FlakyClient()
    resp = call_with_retry(flaky.create, model="x", max_tokens=300,
                           messages=[{"role": "user", "content": "hi"}])
    print("succeeded after", flaky.calls, "calls; stop_reason =", resp.stop_reason)
```

Run `python chat_demo.py`. Expected: the role list `['user', 'assistant', 'user', 'assistant']`, text printing in pieces, then two retries before success.

**Honest limit of the fake:** it ignores history and always returns the same text, so it shows the mechanics (growing list, streaming, retries) but not Claude actually using earlier turns. That needs a real key.

---

## 5. Experiments (write one line each)

1. Add a third `ask(...)` call. How many messages are sent on it? What does that do to cost?
2. In `ask`, print `reply.usage.input_tokens`. Does it grow? (In the fake it will not, because it is fixed. In the real API it grows. Say why.)
3. Change `FlakyClient` to fail 6 times. What happens with `max_retries=4`? Why re-raise at the end?
4. Make `call_with_retry` also raise immediately on `FakeBadRequestError` and write a test proving it was called once (a counter in a fake that raises it).
5. Add jitter: `delay = base_delay * (2 ** attempt) + random.uniform(0, base_delay)`. Why does it help?
6. Write `trim_history(history, keep_last=6)` that keeps only the last N messages but never starts with an `assistant` message. Test it.

---

## 6. Drill (30 min)

SQL: `test_runs(id, test_id, status, run_date)`.
1. For each test, the longest streak is hard, so start simpler: for each test, its most recent run (use `ROW_NUMBER() OVER (PARTITION BY test_id ORDER BY run_date DESC)`).
2. Tests whose last two runs both failed (hint: `LAG(status)`).

Answers are at the bottom.

---

## 7. Interview questions and answers

**Q1. The Messages API is stateless. How do you build a chatbot on it?**
Keep the message list in your application and resend all of it on each call, appending the assistant reply and the next user message. This gives you control over what the model sees, and it means cost and latency grow with conversation length, because every turn re-sends all earlier tokens.

**Q2. When would you use streaming, and when not?**
Use it for interactive UIs, where seeing the first words quickly makes the product feel fast. Skip it for batch jobs such as evals or JSON extraction, because there nobody waits on partial text and streaming only adds handling for mid-stream failures.

**Q3. Which API errors do you retry?**
Retry 429, 5xx and network failures, with exponential backoff, jitter and a maximum number of attempts. Do not retry 400, 401, 403 or 404, because those mean the request or config is wrong and the same call fails again, so retrying only burns quota.

**Q4. Why add jitter to backoff?**
Without it, many clients that failed together retry together at the same moments and hit the limit again. Random jitter spreads them out, which means fewer repeat failures.

**Q5. How would you test your retry logic without calling the real API?**
Use a fake client that fails a set number of times and then succeeds, as in `FlakyClient`, then assert on the call count, the delays and what happens when retries run out. The same idea works for 400-type errors, where the assertion is that there was exactly one call, because test doubles make failure paths deterministic.

**Q6. Your chat gets very long. What are your options?**
Trim old turns, summarize earlier history into a short message, or store key facts outside the conversation and retrieve them when needed. Which one is right depends on what must be remembered exactly, because summaries lose detail.

---

## 8. Explain aloud (2 minutes)

"Explain to a Java developer why a chatbot on this API must resend its history, what that costs, and how I handle a 429 versus a 400." End each part with "because".

---

## 9. "Day 12 done" reply

Send: your revision answers, the output of `chat_demo.py`, your answers to experiments 1, 3 and 4 (with the test for 4), your `trim_history`, SQL answers, and 3-4 flashcards of your own.

---

## Answers

### Revision
1. `max_tokens` means the reply was cut off, so parsing or using it as complete would be wrong, for example JSON that ends mid-object.
2. A reply can hold several blocks of different types (text, and later tool-use requests), so code checks each block's `type`.
3. In `ON`, not `WHERE`, because `WHERE` runs after the join and removes the NULL rows, turning the LEFT JOIN into an INNER JOIN.
4. The default list is created once and shared across calls. Use `items=None` and create a new list inside.
5. `df[(df["a"] > 1) & (df["b"] == "x")]`. `&` works element by element, and parentheses are needed because `&` binds tighter than the comparisons.

### SQL

```sql
-- 1. Most recent run per test
WITH ranked AS (
  SELECT test_id, status, run_date,
         ROW_NUMBER() OVER (PARTITION BY test_id ORDER BY run_date DESC) AS rn
  FROM test_runs
)
SELECT test_id, status, run_date FROM ranked WHERE rn = 1;

-- 2. Tests whose last two runs both failed
WITH ranked AS (
  SELECT test_id, status,
         ROW_NUMBER() OVER (PARTITION BY test_id ORDER BY run_date DESC) AS rn
  FROM test_runs
)
SELECT test_id
FROM ranked
WHERE rn <= 2
GROUP BY test_id
HAVING COUNT(*) = 2 AND SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) = 2;
-- A test with only one run is excluded by COUNT(*) = 2.
```
