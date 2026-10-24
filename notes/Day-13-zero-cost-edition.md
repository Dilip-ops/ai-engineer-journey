# Day 13 (zero-cost edition): thinking, choosing a model, and cost basics

Date: Sun Oct 25, 2026 (calendar Day 15; after this lesson your lag is 2)
Phase 1, Week 2. Offline again: the code uses fake responses and placeholder prices.

| Block | Minutes |
|---|---|
| Revision questions (section 0) | 10 |
| Main topic (sections 1-4) | 100 |
| Drill (section 6) | 30 |
| Notes and flashcards | 20 |
| Explain aloud (section 8) | 10 |

---

## 0. Revision first (answer from memory)

1. Why must a chatbot resend its whole history, and what does that do to cost?
2. Which HTTP errors do you retry, which not, and why?
3. What is exponential backoff, and why add jitter?
4. LEFT JOIN: right-table filter in `ON` or `WHERE`, and why?
5. Why is `items=[]` as a default argument a bug?
6. Why can temperature 0 still give slightly different outputs?
7. Still open from Day 11 and Day 12: the revision answers, SQL answers and experiment outputs, if you have not sent them.

---

## 1. Extended and adaptive thinking

Some tasks (maths, multi-step logic, tricky debugging, planning) improve if the model **reasons before answering**. The API can let Claude produce internal reasoning first, then the final answer.

Two modes exist, and **which one works depends on the model**. This is based on Anthropic's docs when I checked; confirm on the current docs page before you rely on it:

| Mode | How you enable it | Used by |
|---|---|---|
| Manual extended thinking | `thinking={"type": "enabled", "budget_tokens": N}` | Older models. On the newest models (the 4.7+ generation, which includes Sonnet 5.5, Opus 5.5 and Haiku 5.5) it is rejected with a **400** error. |
| Adaptive thinking | `thinking={"type": "adaptive"}`, plus optional `output_config={"effort": "low"|"medium"|"high"|...}` | Current models. Claude decides whether and how much to think; `effort` is soft guidance. |

Real-SDK shape (read it now, run it when you have a key):

```text
response = client.messages.create(
    model="...", max_tokens=16000,
    thinking={"type": "adaptive"},
    output_config={"effort": "medium"},
    messages=[...],
)
for block in response.content:
    if block.type == "thinking":   # a summary of the reasoning
        ...
    elif block.type == "text":     # the final answer
        ...
```

Facts to remember:
- Thinking tokens are **billed as output tokens** and count toward `max_tokens`. The response reports them in `usage.output_tokens_details.thinking_tokens`.
- `max_tokens` is the hard ceiling on thinking plus answer. Too low and the answer is cut off (`stop_reason == "max_tokens"`, Day 11).
- `content` now contains `thinking` blocks as well as `text` blocks, which is another reason to filter on `type`.
- Changing the thinking settings between requests can invalidate prompt caching (Day 18).
- Thinking is not free and not always better: simple tasks (classification, formatting, extraction) usually do not need it. Measure with evals.

---

## 2. Choosing a model

The families (from your Day 8 note): **Haiku** fast and cheap; **Sonnet** the everyday balance; **Opus** long-running agentic coding and knowledge work; **Fable** the most demanding reasoning. Model names and versions change, so always copy the current ID from the docs.

How to choose:
1. Start with the cheapest model that might work.
2. Build a small eval set (Day 20) from real inputs.
3. Run all candidate models on it and compare quality, cost and latency.
4. Move up a tier only where the cheaper one fails.

Many production systems **route**: a small model handles easy requests, a larger one handles hard ones. QA analogy: you do not run the full regression suite on every commit, you pick the right suite for the risk.

---

## 3. Cost basics

Cost per call = input tokens x input price + output tokens x output price. Output tokens are usually priced higher than input tokens, so verbose answers and thinking are the expensive part.

Ways to cut cost, in order of effort:
1. Shorter prompts and shorter answers (`max_tokens`, "reply in under 100 words").
2. A smaller model for easy work.
3. Less or no thinking where it does not help.
4. Prompt caching (Day 18) for repeated long prefixes.
5. Batch processing (Day 18) for work that is not urgent.

I do not have verified current prices, so the code below uses **placeholder numbers**. Replace them with the real ones from the pricing page before you trust any figure.

---

## 4. Code: thinking blocks and cost, offline

Save as `code/cost_demo.py`:

```python
"""Day 13 (zero-cost): thinking blocks, token cost, model choice. No key, no network."""
from types import SimpleNamespace

# PLACEHOLDER prices in USD per million tokens. They are NOT real.
# Copy the current numbers from the pricing page before trusting any cost figure.
PRICES = {
    "small":  {"in": 1.0,  "out": 5.0},    # stands in for the cheap, fast model
    "medium": {"in": 3.0,  "out": 15.0},   # stands in for the everyday model
    "large":  {"in": 15.0, "out": 75.0},   # stands in for the top model
}


def fake_response(answer, thinking_tokens=0, in_tok=200, answer_tok=60):
    """Same SHAPE as a real reply when thinking is on: a thinking block, then text."""
    content = []
    if thinking_tokens:
        content.append(SimpleNamespace(type="thinking", thinking="(summary of reasoning)"))
    content.append(SimpleNamespace(type="text", text=answer))
    out_total = thinking_tokens + answer_tok          # thinking is billed as OUTPUT
    return SimpleNamespace(
        content=content,
        stop_reason="end_turn",
        usage=SimpleNamespace(
            input_tokens=in_tok,
            output_tokens=out_total,
            output_tokens_details=SimpleNamespace(thinking_tokens=thinking_tokens),
        ),
    )


def cost_usd(usage, tier):
    p = PRICES[tier]
    return usage.input_tokens / 1e6 * p["in"] + usage.output_tokens / 1e6 * p["out"]


def answer_text(response):
    """Return only the text blocks; skip thinking blocks."""
    return "".join(b.text for b in response.content if b.type == "text")


if __name__ == "__main__":
    plain = fake_response("Use a boundary value test.", thinking_tokens=0)
    deep = fake_response("Use a boundary value test.", thinking_tokens=4000)

    for name, r in [("no thinking", plain), ("with thinking", deep)]:
        u = r.usage
        print(f"{name:14} in={u.input_tokens} out={u.output_tokens} "
              f"thinking={u.output_tokens_details.thinking_tokens} "
              f"cost(medium)=${cost_usd(u, 'medium'):.5f}")
        print("  blocks:", [b.type for b in r.content], "| text:", answer_text(r))

    ratio = cost_usd(deep.usage, "medium") / cost_usd(plain.usage, "medium")
    print(f"thinking made this call {ratio:.1f}x more expensive")

    # 10,000 calls a month, same prompt, three tiers
    for tier in PRICES:
        print(f"10k calls on {tier}: ${cost_usd(plain.usage, tier) * 10_000:.2f}")
```

Run `python cost_demo.py`. You should see the call with thinking cost about 41 times more than the same call without it, and the 10,000-calls-a-month numbers differ 15x between the cheapest and the largest tier. The numbers are fake; the **ratios** are the lesson.

---

## 5. Experiments (one line each)

1. Change `thinking_tokens` to 500. At what point is the answer "worth" the extra cost? (Answer in terms of how you would measure it.)
2. Write `route(task)` that returns `"small"` for tasks in `{"classify", "extract", "format"}` and `"large"` otherwise. Test both branches.
3. Write `monthly_cost(calls, usage, tier)` and a test that checks the cheapest tier is cheaper than the most expensive one.
4. What happens in `answer_text` if a response has only a thinking block and no text (for example, truncated by `max_tokens`)? Add a check that raises `ValueError` and test it.
5. Make `cost_usd` raise a clear error for an unknown tier instead of a bare `KeyError`.

---

## 6. Drill (30 min)

Table `api_calls(id, model, input_tokens, output_tokens, thinking_tokens, called_at)`.

1. Total input and output tokens per model.
2. Models whose **average output tokens** exceed 1,000 (use `HAVING`).
3. The share of each model's output tokens that were thinking (use `SUM(thinking_tokens) * 1.0 / SUM(output_tokens)`).

Pandas version of question 2: `df.groupby("model")["output_tokens"].mean()` then filter with a condition on the result.

Answers are at the bottom.

---

## 7. Interview questions and answers

**Q1. What is extended or adaptive thinking, and when would you use it?**
It lets Claude reason before answering, which helps on multi-step problems such as maths, planning and hard debugging. I would use it for those and skip it for simple classification or formatting, because the thinking tokens are billed as output and add latency without improving easy tasks.

**Q2. How are thinking tokens billed?**
As output tokens, and they count toward `max_tokens`. The usage object reports them separately, so you can see how much of the bill came from reasoning rather than the visible answer, which is how you spot an unexpectedly expensive prompt.

**Q3. How do you choose between Haiku, Sonnet and Opus?**
Build a small eval set from real inputs, run each candidate, and compare quality, cost and latency, starting with the cheapest. I choose the cheapest model that passes my quality bar, because reputation or benchmarks may not match my task.

**Q4. What is model routing?**
Sending easy requests to a small model and hard ones to a larger model, based on a classifier or simple rules. It cuts cost because most traffic is usually easy, and it needs monitoring, because a wrong routing decision silently lowers quality.

**Q5. A call that worked yesterday now returns a 400 error mentioning thinking. What do you suspect?**
The model or the thinking mode changed. Newer models reject the manual `budget_tokens` mode and expect adaptive thinking, so I would read the error text and the current docs for that model before changing code.

**Q6. Why can adding thinking make a pipeline fail even when answers are better?**
The response now contains `thinking` blocks as well as `text`, and thinking counts toward `max_tokens`. Code that reads `content[0].text` can break, and a small `max_tokens` can truncate the final answer, so I filter by block type and set `max_tokens` with room for both.

---

## 8. Explain aloud (2 minutes)

"Explain to a Java developer how I decide which Claude model and how much thinking to use for a new feature, and how I would prove the decision with data." End each part with "because".

---

## 9. "Day 13 done" reply

Send: your revision answers, the output of `cost_demo.py`, your `route`, `monthly_cost` and tests, your answer to experiment 4, SQL answers, and 3-4 flashcards of your own.

Project 2 (user story to test-case generator) comes next in the plan. With no key yet, the plan is to build it against a fake client and swap in the real one later; we will decide that tomorrow.

---

## Answers

### Revision
1. The API remembers nothing, so each call must carry the full history, which means input tokens and cost grow every turn.
2. Retry 429, 5xx and network errors. Do not retry 400, 401, 403, 404, because the same bad request fails again.
3. Waiting longer after each failure (1x, 2x, 4x) up to a limit. Jitter spreads out clients that failed together, so they do not retry at the same instant.
4. `ON`, because `WHERE` runs after the join and removes NULL rows, turning it into an INNER JOIN.
5. The default list is created once and shared between calls. Use `None` and build a new list inside.
6. Floating-point differences can flip near-tied tokens, so output is repeatable but not guaranteed identical.

### SQL

```sql
-- 1. Tokens per model
SELECT model, SUM(input_tokens) AS total_in, SUM(output_tokens) AS total_out
FROM api_calls
GROUP BY model;

-- 2. Models averaging more than 1000 output tokens
SELECT model, AVG(output_tokens) AS avg_out
FROM api_calls
GROUP BY model
HAVING AVG(output_tokens) > 1000;

-- 3. Thinking share of output tokens
SELECT model,
       SUM(thinking_tokens) * 1.0 / SUM(output_tokens) AS thinking_share
FROM api_calls
GROUP BY model;
-- The * 1.0 avoids integer division returning 0 in some databases.
```
