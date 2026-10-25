# Day 14: Project 2 (user story to test-case generator) and Week 2 review

Date: Sun Oct 25, 2026 (calendar Day 15; Day 14 is the Week 2 project and review)
Your lag is 2. Project 2 is the core of this week, so do it before the extras.

Because you have no API key yet, you build this against a **fake client**. When credit arrives, you change one line and it runs against real Claude. The tests you write now are the same ones that protect it then.

---

## 1. What you are building

A function `generate_test_cases(client, story)` that:
1. Builds a prompt with a system prompt and an XML-tagged user story (Day 10).
2. Calls the Messages API (Days 11 and 12).
3. Refuses truncated replies (`stop_reason == "max_tokens"`, Day 11).
4. Extracts and parses JSON, then **validates** it like contract testing (Day 10).
5. If the reply is invalid, sends the error back to Claude and retries a limited number of times (Day 12).
6. Returns the test cases plus total token usage (Day 13).

This is a small version of what an AI QA engineer builds: a model call wrapped in checks you can test.

---

## 2. Files (attached to this message; put them in `projects/project-02-testcase-generator/`)

| File | Who writes it |
|---|---|
| `fake_generator.py` | Given. A fake client that returns canned replies in order and records every call. |
| `test_generator.py` | Given. 12 tests. Read them first: they are the specification. |
| `generator.py` | **You.** Skeleton with five TODOs and a docstring for each. |

Run the tests from that folder (no installs needed):

```bash
python -m unittest -v
```

Right now all 12 fail, which is correct. A failing test suite before the code exists is how test-first work starts, and you already know that rhythm.

---

## 3. Work in this order

1. Read `fake_generator.py` and `test_generator.py` (15 min). Write down what each test expects before you code.
2. TODO 1 and 2: `SYSTEM_PROMPT` and `build_prompt`.
3. TODO 3: `extract_json`.
4. TODO 4: `validate` (reuse your Day 10 validator thinking).
5. TODO 5: `generate_test_cases`. Do this last; it uses all the others.
6. After each TODO, run the tests and watch the count of passing tests rise.

Hints, only if stuck (try 15 minutes first):
- `build_prompt`: two tests check it. The story must be inside `<user_story>` tags in the user message and must not appear in the system prompt.
- `validate`: collect problems in a list and raise one `ValueError` at the end with `"; ".join(problems)`. Remember the "at least one negative case" rule.
- `generate_test_cases` loop: `for attempt in range(max_retries + 1)`. Check `stop_reason` first. On a `json.JSONDecodeError` or `ValueError`, extend `messages` with the assistant reply and a new user message that includes the error. Add up `usage` after every call, including failed ones.
- Mutable default arguments: do not use `[]` or `{}` as a default anywhere. You know why.

---

## 4. Extend it (after all 12 pass)

Do at least two:
1. Add a test of your own that the tests above do not cover, such as a reply with the right JSON but an empty `title`.
2. Handle a reply that has a `thinking` block before the text (use `answer_text` thinking from Day 13).
3. Add `generate_many(client, stories)` that returns results for several stories and records which one failed instead of crashing.
4. Add a `cost_estimate(usage, price_in, price_out)` using placeholder prices.
5. Write a README: what it does, how to run the tests, and what happens when Claude returns bad JSON.

---

## 5. When you get a real key (about 15 minutes)

1. `pip install anthropic`, set `ANTHROPIC_API_KEY` in the terminal (never commit it).
2. In a small `run_real.py`: `client = anthropic.Anthropic()`, call `generate_test_cases(client, STORY)` and print the result.
3. Compare real output with the fake. Which validations fire? Add a test for each real failure you see. That is how an eval set starts.

---

## 6. Definition of done

- All 12 tests pass; your own extra tests pass.
- No API key anywhere in the repo; `.venv/` and `.env` are in `.gitignore`.
- Committed to your GitHub repo on the `develop` branch, in `projects/project-02-testcase-generator/`.
- You can explain every function aloud in under three minutes, ending each part with "because".

---

## 7. Week 2 self-quiz (10 questions, 20 minutes, no notes)

1. What is the difference between the Claude app and the API?
2. List the main fields of a Messages API request. Which one is required besides `model` and `messages`?
3. What does "stateless" mean, and what does it do to cost in a long chat?
4. What does `stop_reason == "max_tokens"` tell you, and what must you do about it?
5. Why is `response.content` a list? Name three block types you may see.
6. Which HTTP errors do you retry and which not? Why?
7. What is exponential backoff and why add jitter?
8. How are thinking tokens billed, and when is thinking not worth using?
9. How do you choose between Haiku, Sonnet and Opus?
10. Name three things you do to make model output safe to use in code.

Score yourself with the answers at the bottom, then fill in the scorecard.

---

## 8. Weekly scorecard and cheat sheet

Scorecard (copy into your notes):
- Days completed this week: 
- Project 2 shipped (tests passing): yes / no
- Flashcards reviewed: 
- Self-quiz score: /10 (Week 1 was 8/10)
- Biggest struggle: 
- Biggest win: 

One-page cheat sheet: write one page in your own words covering the request/response shape, `stop_reason`, errors and retries, thinking and cost, and prompt structure. If it does not fit on one page, one of those is not understood yet.

Error log: add one row each for `temperature 0` and the pandas two-condition filter.

---

## 9. "Day 14 done" reply

Send: your quiz score with the questions you missed, the output of `python -m unittest -v`, your `generator.py` (or the part you are stuck on), your scorecard, and one thing you would change about your own code.

---

## Answers: Week 2 self-quiz

1. The app is a finished product with its own interface and plan. The API gives code direct control over the model, system prompt, parameters and output, so it can be automated and tested. API usage is billed separately.
2. `model`, `messages`, and `max_tokens` (required); optional `system`, thinking settings and others.
3. The server remembers nothing between calls, so the client resends the full history each time. Input tokens, and therefore cost and latency, grow every turn.
4. The reply was cut off, so it may be incomplete (for example, JSON that ends mid-object). Do not parse it as complete; raise the limit, shorten the task, or fail loudly.
5. A reply can hold several blocks of different types, so code checks each block's `type`. Types in responses: `text`, `thinking` (when thinking is on) and `tool_use` (Day 15).
6. Retry 429, 5xx and network errors with backoff and a limit. Do not retry 400, 401, 403, 404, because the same bad request fails the same way.
7. Waiting 1x, 2x, 4x the base delay after each failure, with a maximum number of tries. Jitter spreads out clients that failed together so they do not all retry at the same moment.
8. As output tokens, and they count toward `max_tokens`. Not worth it for simple tasks like classification or formatting, because it adds cost and latency without better answers.
9. Build an eval set from real inputs, run each candidate, compare quality, cost and latency, and take the cheapest model that passes.
10. Ask for a schema and wrap it in tags, check `stop_reason`, parse and validate in code, retry with the error text a limited number of times, and test all of it with a fake client.
