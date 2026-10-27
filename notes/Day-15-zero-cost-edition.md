# Day 15 (zero-cost edition): tool use (function calling), concepts

Date: Tue Oct 27, 2026 (calendar Day 17; after this lesson your lag is 2)
Phase 1, Week 3: Tool use. Drill this week: DSA arrays, strings, hash maps.
Offline again: a scripted fake model replays the real message shapes.

| Block | Minutes |
|---|---|
| Revision questions (section 0) | 10 |
| Main topic (sections 1-4) | 100 |
| DSA drill (section 6) | 30 |
| Notes and flashcards | 20 |
| Explain aloud (section 8) | 10 |

This is the most important concept so far. **Tool use is what turns a chatbot into an agent**, and MCP (Weeks 5 and 6) is a standard way to supply tools. Take your time here.

---

## 0. Revision first (answer from memory)

1. In Project 2, why do you check `stop_reason` before parsing, and why is a truncated reply NOT retried?
2. Why is the invalid-JSON retry limited, and what do you send back to Claude on a retry?
3. At temperature 0, why can outputs still differ slightly?
4. Filter a DataFrame where `status == "FAILED"` and `duration > 2`. Why `&` and parentheses, and why not `and`?
5. LEFT JOIN: where does the right-table filter go to keep unmatched left rows, and why?
6. Why does a thinking-only reply (no text block) need handling in code?
7. Still open if you have not sent them: Day 12 outputs and Day 13 experiments 2 to 5.

---

## 1. The key idea

A language model can only produce text. It cannot check your test database, run code, or call your API. **Tool use** lets it *ask your code* to do those things:

1. You describe your tools to Claude (name, description, input schema).
2. Claude decides whether it needs one, and replies with a **tool request** instead of a final answer.
3. **Your code** runs the function. Claude never executes anything itself.
4. You send the result back.
5. Claude uses the result to write the final answer (or asks for another tool).

QA analogy: Claude is a manager who cannot touch the system, so it sends you a ticket ("check the status of test X"). You do the work and reply with the result. Claude then writes the report.

This is why "model plus tools plus a loop" is the working definition of an **agent** from Day 1.

---

## 2. The message flow (memorize this)

```text
you   -> API: messages=[user: "Did checkout_discount pass?"], tools=[...]
API   -> you: stop_reason="tool_use",
              content=[tool_use block: id, name="get_test_status", input={"test_name": "checkout_discount"}]
you:  run get_test_status("checkout_discount")
you   -> API: messages=[user, assistant(the tool_use reply), user: [tool_result block with the SAME id]]
API   -> you: stop_reason="end_turn", content=[text: "checkout_discount is FAILED."]
```

Facts to remember:
- **Tool definition** = `name`, `description`, `input_schema` (JSON Schema). The **description is the most important part**, because it is how Claude decides when to use the tool (Week 5 returns to tool design).
- `stop_reason == "tool_use"` means "I need you to run something", not "I am done".
- A `tool_use` block has an `id`, a `name` and an `input` object. Your `tool_result` must carry the same id as `tool_use_id`, so Claude can match results to requests.
- Claude can request **several tools in one reply**; return one `tool_result` per request, in one user message.
- Tool results go back inside a **user** message. The assistant's tool-request reply must also be appended to the history first (Day 12: you own the history).
- Errors: send a `tool_result` with `is_error: true` and the error text, so Claude can recover or explain. Do not crash the conversation.
- Safety: **you** decide which functions exist. Look up the tool name in a registry of allowed functions; never run a name or arguments from the model without checking them, because the model's output is untrusted input (this is the root of the MCP security topics in Week 6).
- Always cap the loop (`max_turns`), because a confused model could keep requesting tools forever, which costs money.

Details such as `tool_choice` (forcing or forbidding tools), parallel calls and strict schemas exist and change over time; check the current docs when you build with a real key.

---

## 3. Code: the whole loop, offline

Save as `code/tool_demo.py`:

```python
"""Day 15 (zero-cost): the tool-use loop with a scripted fake model. No key, no network."""
import json
from types import SimpleNamespace

TOOLS = [
    {
        "name": "get_test_status",
        "description": (
            "Return the latest status (PASSED or FAILED) of one automated test. "
            "Use when the user asks whether a specific test passed or failed. "
            "Do not use it to list tests."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "test_name": {"type": "string", "description": "Exact test name, e.g. login_valid"}
            },
            "required": ["test_name"],
        },
    }
]

TEST_DB = {"login_valid": "PASSED", "checkout_discount": "FAILED"}


def get_test_status(test_name):
    if test_name not in TEST_DB:
        raise KeyError(f"unknown test: {test_name}")
    return {"test_name": test_name, "status": TEST_DB[test_name]}


REGISTRY = {"get_test_status": get_test_status}   # only functions listed here can ever run


# ---------- scripted fake model: same SHAPES as real replies ----------
def tool_use_reply(tool_name, tool_input, tool_id="toolu_fake_1"):
    return SimpleNamespace(
        stop_reason="tool_use",
        content=[SimpleNamespace(type="tool_use", id=tool_id, name=tool_name, input=tool_input)],
    )


def text_reply(text):
    return SimpleNamespace(stop_reason="end_turn", content=[SimpleNamespace(type="text", text=text)])


class _Messages:
    def __init__(self, replies):
        self.replies, self.calls = list(replies), []

    def create(self, **kwargs):
        self.calls.append({**kwargs, "messages": list(kwargs["messages"])})  # snapshot
        return self.replies.pop(0)


class FakeToolClient:
    def __init__(self, replies):
        self.messages = _Messages(replies)


# ---------- the loop YOU own ----------
def run_conversation(client, user_text, max_turns=5):
    messages = [{"role": "user", "content": user_text}]
    for _ in range(max_turns):
        response = client.messages.create(
            model="claude-sonnet-5-5", max_tokens=500, tools=TOOLS, messages=messages
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            return "".join(b.text for b in response.content if b.type == "text")

        results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            try:
                func = REGISTRY[block.name]          # unknown tool name -> KeyError
                output = func(**block.input)
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": json.dumps(output)})
            except Exception as exc:                 # report the error to the model, do not crash
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": f"Error: {exc}", "is_error": True})
        messages.append({"role": "user", "content": results})
    raise RuntimeError(f"No final answer after {max_turns} turns")


if __name__ == "__main__":
    # 1. happy path: model asks for a tool, we run it, model answers
    client = FakeToolClient([
        tool_use_reply("get_test_status", {"test_name": "checkout_discount"}),
        text_reply("checkout_discount is FAILED."),
    ])
    print(run_conversation(client, "Did checkout_discount pass?"))
    second_call_roles = [m["role"] for m in client.messages.calls[1]["messages"]]
    print("roles on 2nd call:", second_call_roles)
    print("tool_result sent back:", client.messages.calls[1]["messages"][-1]["content"])

    # 2. tool error is returned to the model, not raised
    client = FakeToolClient([
        tool_use_reply("get_test_status", {"test_name": "nope"}),
        text_reply("I could not find a test called nope."),
    ])
    print(run_conversation(client, "Did nope pass?"))
    print("error result:", client.messages.calls[1]["messages"][-1]["content"])

    # 3. runaway loop guard
    client = FakeToolClient([tool_use_reply("get_test_status", {"test_name": "login_valid"})] * 3)
    try:
        run_conversation(client, "loop forever", max_turns=3)
    except RuntimeError as exc:
        print("guard fired:", exc)
```

Run `python tool_demo.py`. You should see three things: the final answer after a tool call; an error result with `is_error`; and the runaway-loop guard firing.

**Honest limit:** the fake replays scripted replies, so it does not decide anything. It teaches the exact message shapes and the loop you must write, not Claude's judgment about when to call a tool.

---

## 4. Experiments (one line each)

1. Print `client.messages.calls[1]["messages"]` after the happy path. Identify every message and block type. Why is the `tool_result` in a **user** message?
2. Add a second tool `list_failed_tests()` to `TOOLS` and `REGISTRY` that returns the FAILED test names. Write the description so it is clearly different from `get_test_status`.
3. Make the fake request **both** tools in one reply (two `tool_use` blocks with different ids). Run it. Does your loop return two `tool_result` blocks in one message?
4. Make Claude (the fake) request a tool name that is not in `REGISTRY`. What does your loop send back? Is that safe?
5. Add input validation: if `test_name` is not a string, return an `is_error` result before calling the function. Why validate even though there is a schema?
6. Change `max_turns` to 1 and run the happy path. What happens, and why is that the correct behaviour?

---

## 5. Why this matters for Project 3 and beyond

Project 3 (Day 21) is the test-case generator v2 with **tools and eval checks**. For example, a tool that looks up existing test cases so Claude does not duplicate them. Today's loop is the engine of that project, so keep `tool_demo.py` clean and tested.

---

## 6. DSA drill (30 min): arrays, strings, hash maps

Solve in Python before reading the answers. For each, state time and space complexity.

1. **Two Sum.** Given a list `nums` and a `target`, return the indexes of the two numbers that add up to the target, or `[]` if none. (Use a dict, not two nested loops.)
2. **Valid anagram.** Given two strings, return True if one is a rearrangement of the other.
3. **First unique character.** Return the index of the first character in a string that appears exactly once, or -1.

---

## 7. Interview questions and answers

**Q1. What is tool use, and who actually runs the tool?**
Tool use lets Claude request that your code run a function, such as querying a database or an API, and then use the result in its answer. Your application runs the function, not Claude, which matters for security because you control which tools exist and what arguments are allowed.

**Q2. Walk me through the message flow of a tool call.**
I send the user message and tool definitions. Claude replies with `stop_reason: tool_use` and a `tool_use` block containing an id, a name and an input. I run the function, then send a user message with a `tool_result` block carrying the same id. Claude then replies with the final answer, because it can now see the result. The assistant's tool request must be kept in the history, since the API is stateless.

**Q3. How do tool descriptions affect behaviour?**
The description is how Claude decides whether and when to use a tool, so a vague or overlapping description causes wrong or missed calls. I write what it does, when to use it, and when not to, and I test it with examples, because tool descriptions are effectively part of the prompt.

**Q4. What can go wrong in an agent loop, and how do you guard it?**
The model can loop forever, request an unknown tool, send invalid arguments, or hit a tool error. I cap the number of turns, only dispatch through a registry of allowed functions, validate inputs in code, and return errors as `is_error` results so the model can recover, because a crash in the middle of a conversation loses work and a runaway loop costs money.

**Q5. Is tool use the same as an agent?**
Tool use is a building block. An agent is the model running in a loop where it decides which tools to call and when to stop, until the task is done. A fixed pipeline that always calls the same tools in the same order is a workflow, not an agent, because code rather than the model decides the steps.

**Q6. How would you test code that uses tool calls without a real model?**
Script the model's replies with a fake client, as in `FakeToolClient`, and assert on what my code sends back: the tool result's id, the `is_error` flag, the number of calls, and that the loop stops. Scripted replies make the tests deterministic, because the real model's choices vary run to run.

---

## 8. Explain aloud (2 minutes)

"Explain to a Java developer who runs the tool in a Claude tool call, what messages go back and forth, and what could go wrong." End each part with "because".

---

## 9. "Day 15 done" reply

Send: your revision answers, the output of `tool_demo.py`, your answers to experiments 1, 3 and 4, your DSA solutions with complexity, and 3-4 flashcards of your own.

Also still pending from Day 14: your Week 2 quiz score, the output of `python -m unittest -v` for Project 2, and your scorecard. Those are worth sending first, because I have not seen your Project 2 code.

---

## Answers

### Revision
1. A truncated reply may be cut off in the middle of the JSON, so parsing cannot succeed. Retrying with the same limit would likely be truncated again, so it fails loudly instead of burning calls. The fix is a higher `max_tokens` or a shorter task.
2. Retries cost money and a model that keeps failing will not suddenly succeed, so there is a maximum. On a retry I send the assistant's invalid reply and a user message containing the validation error, so the model can see what to fix.
3. Floating-point differences can flip near-tied tokens, so output is repeatable but not guaranteed identical.
4. `df[(df["status"] == "FAILED") & (df["duration"] > 2)]`. `&` works element by element on the columns; `and` needs one True/False and fails on a Series. Parentheses are needed because `&` binds tighter than the comparisons.
5. In `ON`, because `WHERE` runs after the join and removes the NULL rows, so the LEFT JOIN behaves like an INNER JOIN.
6. With thinking on, a reply can contain only a thinking block (for example when `max_tokens` cuts it off), so `content[0].text` fails or returns nothing. Filter by block type and raise a clear error if there is no text.

### DSA

```python
def two_sum(nums, target):
    seen = {}                      # value -> index
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
    return []
# Time O(n), space O(n). The dict replaces the inner loop (O(n^2)) with a O(1) lookup.

from collections import Counter

def is_anagram(a, b):
    return Counter(a) == Counter(b)
# Time O(n + m), space O(k) for k distinct characters.

def first_unique_char(s):
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1
# Two passes, time O(n), space O(k). Counting first, then scanning in order, keeps "first" correct.
```

Test cases to try: `two_sum([2, 7, 11, 15], 9)` gives `[0, 1]`; `two_sum([3, 3], 6)` gives `[0, 1]`; `is_anagram("listen", "silent")` is True; `first_unique_char("aabb")` is -1.
