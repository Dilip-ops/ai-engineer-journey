# Day 11, zero-cost edition: the Messages API without a key or credit

Use this instead of the key-based steps in `Day-11-first-api-call.md`. The concepts, revision questions, interview Q&A, drills and flashcards in that file still apply, so do those parts as written. Only section 3 (setup) and section 4 (first call) change, because you have no payment method yet.

## 1. The idea

A real API call is just: send a request with `model`, `max_tokens`, `messages` (and optionally `system`), then read the response. The thing you must learn is the **shape** of that response and how to handle its edge cases. A fake client with the same shape teaches that at no cost, the same way you would use a stub in test automation.

What the fake covers: `content` as a list of blocks, `stop_reason` (`end_turn` vs `max_tokens`), `usage` token counts, and an authentication failure.
What it cannot show: the real wording of Claude's replies, real token counts, real latency, real rate limits. Those need a real key later.

## 2. Setup (no key, no cost)

```bash
cd ai-engineer-journey/code
python3 -m venv .venv
source .venv/bin/activate
```

You do not need `pip install anthropic` today because the fake client has no dependencies. (Installing it is free if you want it ready: `pip install anthropic`.)

Create two files in `code/`.

### `fake_claude.py`

```python
"""A fake Claude client with the same response SHAPE as the real Messages API.
No network, no key, no cost. Swap it for anthropic.Anthropic() on the day you have credit."""
from types import SimpleNamespace


class FakeAuthenticationError(Exception):
    """Stands in for anthropic.AuthenticationError (HTTP 401)."""


def _response(text, stop_reason="end_turn", in_tok=24, out_tok=None):
    out_tok = out_tok if out_tok is not None else len(text.split())
    return SimpleNamespace(
        id="msg_fake_001",
        type="message",
        role="assistant",
        model="claude-fake",
        content=[SimpleNamespace(type="text", text=text)],
        stop_reason=stop_reason,
        usage=SimpleNamespace(input_tokens=in_tok, output_tokens=out_tok),
    )


class _Messages:
    def __init__(self, api_key):
        self.api_key = api_key

    def create(self, *, model, max_tokens, messages, system=None, **kwargs):
        if not self.api_key:
            raise FakeAuthenticationError("401: missing or invalid API key")
        if max_tokens < 1 or not messages:
            raise ValueError("400: max_tokens must be >= 1 and messages non-empty")
        full = (
            "1. Empty username and password.\n"
            "2. Valid username with a wrong password.\n"
            "3. SQL injection string in the username field."
        )
        words = full.split()
        if max_tokens < len(words):  # crude: treat one word as one token
            return _response(" ".join(words[:max_tokens]), "max_tokens", out_tok=max_tokens)
        return _response(full)


class FakeClient:
    def __init__(self, api_key="fake-key"):
        self.messages = _Messages(api_key)
```

### `first_call.py`

```python
import os
from fake_claude import FakeClient, FakeAuthenticationError

client = FakeClient(api_key=os.environ.get("FAKE_KEY", "fake-key"))

try:
    message = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=300,
        system="You are a QA assistant. Be concise.",
        messages=[{"role": "user", "content": "Give me 3 negative test cases for a login form."}],
    )
except FakeAuthenticationError as exc:
    raise SystemExit(f"Auth problem: {exc}")

for block in message.content:
    if block.type == "text":
        print(block.text)

print("stop_reason:", message.stop_reason)
print("tokens in/out:", message.usage.input_tokens, message.usage.output_tokens)
if message.stop_reason == "max_tokens":
    print("WARNING: answer was cut off")
```

Run it:

```bash
python first_call.py
```

## 3. Experiments (this is the learning)

1. Run it as is. Which fields did you read, and in what order? Write them down from memory.
2. Change `max_tokens=300` to `max_tokens=8`. What is `stop_reason`? What happened to the answer? Why is this dangerous if the answer were JSON?
3. Run `FAKE_KEY= python first_call.py` (empty key). What error text appears? In the real SDK this becomes `anthropic.AuthenticationError`; the right reaction is to fix config, not retry.
4. Change `max_tokens=0`. Which error type is it, and should you retry it? (No: it is an invalid request, so fix the input.)
5. Add `print(message.content)` and look at it. Why is `content` a list and not a string?
6. Write a function `safe_text(message)` that returns the joined text of all text blocks and raises `ValueError` if `stop_reason == "max_tokens"`. Test it against both the normal and the truncated response.

Write one line per experiment in your note.

## 4. Swap to the real client later (about 5 minutes)

When you have credit and a key:

1. `pip install anthropic`
2. `export ANTHROPIC_API_KEY="..."` (never commit it; `.venv/` and `.env` go in `.gitignore`)
3. In `first_call.py`, replace the fake client and the exception:

```diff
-from fake_claude import FakeClient, FakeAuthenticationError
+import anthropic
-client = FakeClient(api_key=os.environ.get("FAKE_KEY", "fake-key"))
+client = anthropic.Anthropic()
-except FakeAuthenticationError as exc:
+except anthropic.AuthenticationError as exc:
```

Everything else (`message.content`, `stop_reason`, `usage`) stays the same, because the fake was built to match the real response shape. Confirm the current model ID in the docs. Then compare the real output with your fake and note what differs.

## 5. "Day 11 done" reply (zero-cost version)

Send:
- Your answers to the 6 revision questions from `Day-11-first-api-call.md` and your SQL and pandas drill answers
- The output of `first_call.py` and of the `max_tokens=8` run
- Your `safe_text` function
- One sentence for each experiment
- Your own flashcards (3 to 4)

Write the interview answers aloud once, ending each part with "because".
