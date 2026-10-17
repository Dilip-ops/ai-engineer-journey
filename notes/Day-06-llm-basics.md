# Day 6 (Fri Oct 16): How LLMs Work I: Tokens, Context Window, Temperature

**Time:** about 2.5-3 hrs · **Goal:** explain how an LLM reads, remembers and generates text, and see temperature working in a small script.

## Revisit first (10 min)

Answer these without notes, then check `flashcards.md`:

1. INNER JOIN vs LEFT JOIN?
2. In a LEFT JOIN, what happens if you filter the right table in `WHERE` instead of `ON`?
3. How do you filter a DataFrame on two conditions?
4. `loc` vs `iloc`?
5. **From Day 5:** send me your drill 6 query (runs per test, including tests with zero runs) and its result.

## Schedule

| Block | Time | Task |
| --- | --- | --- |
| A | 50 min | Study the concepts below |
| B | 45 min | Hands-on: run the temperature demo, then the optional tokenizer demo |
| C | 30 min | Drill: 6 exercises (below) |
| D | 30 min | Write your note, add 5-8 pairs to `flashcards.md`, explain aloud for 2 min |

## Concepts

### An LLM predicts the next token

A large language model is trained on huge amounts of text to do one thing: given the text so far, predict what comes next. It produces a **probability for every possible next token**, one token is chosen, added to the text, and the process repeats. A whole answer is built one token at a time.

### Tokens

A **token** is a chunk of text: a whole short word, part of a longer word, a punctuation mark or a piece of code. Models read and write tokens, not characters or words.

| Rule of thumb (English, approximate) | Value |
| --- | --- |
| 1 token | about 4 characters, or about three-quarters of a word |
| 1,500 words | about 2,000 tokens |

Code, other languages and unusual words usually use more tokens. **Each model family has its own tokenizer, so counts differ between providers.** For exact Claude numbers, use the token counting that the Claude API provides (check the current docs).

### Context window

The **context window** is the maximum amount of text (in tokens) the model can consider at once. It includes everything: the system prompt, the whole conversation so far, any documents you paste, and the answer it is writing.

- **The model has no memory between calls.** A chat app resends the earlier messages every time. "Memory" features work by putting saved text back into the context.
- **Longer context costs more and is slower.** You pay for the tokens you send and receive.
- **A bigger window is not always better.** Very long, cluttered context can make it harder for the model to focus on what matters.
- When you exceed the window, you must shorten, summarise or split the content. We'll return to this as "context engineering" in Week 8.

### Temperature

Temperature controls **how random the choice of the next token is**.

| Temperature | Behaviour |
| --- | --- |
| Low (near 0) | Picks the most likely tokens: focused and more repeatable |
| Higher | Gives less likely tokens a better chance: more varied and creative, but less reliable |

Even at the lowest setting, outputs are **not guaranteed to be identical** on every run. For the available range and default on Claude, check the current API documentation.

### Key ideas

1. **LLMs generate one token at a time from a probability distribution.**
2. **The context window is a budget** shared by input and output.
3. **No memory between calls.** Anything the model should know must be in the context.
4. **Temperature changes the odds, not the model.**
5. **Non-determinism is normal**, which is why AI testing needs graded evals and repeated runs. That is your QA strength.

## Hands-on

### Part 1: Temperature demo (no installs)

Create `temp_demo.py` in `code/day06`:

```python
import math
import random

tokens = ["pass", "fail", "error", "skip"]
logits = [3.0, 2.0, 1.0, 0.0]


def softmax_with_temperature(logits, temperature):
    scaled = [x / temperature for x in logits]
    biggest = max(scaled)
    exps = [math.exp(x - biggest) for x in scaled]
    total = sum(exps)
    return [e / total for e in exps]


for t in [0.2, 1.0, 2.0]:
    probs = softmax_with_temperature(logits, t)
    print(f"temperature = {t}")
    for token, p in zip(tokens, probs):
        print(f"  {token:6} {p:.2%}")
    picks = random.choices(tokens, weights=probs, k=15)
    print("  15 samples:", picks)
    print()
```

Run it with `python3 temp_demo.py`. **Before you run it, predict:** at temperature 0.2, which token will dominate, and how will the picture change at 2.0?

Check yourself afterwards (approximate): at 0.2 the top token is about 99%; at 1.0 about 64%, 24%, 9%, 3%; at 2.0 about 46%, 28%, 17%, 10%. Run it a few times and notice that the 15 samples change.

### Part 2: Tokenizer demo (optional, needs internet)

This uses OpenAI's open-source tokenizer **only to show how text gets split**. Claude uses its own tokenizer, so counts will differ.

```bash
pip install tiktoken
```

```python
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")
for text in ["Hello world", "login_test failed", "antidisestablishmentarianism"]:
    ids = enc.encode(text)
    print(len(ids), [enc.decode([i]) for i in ids])
```

Notice how a rare long word splits into several pieces, while common short words are one token.

## Drill (30 min)

1. Estimate the tokens in a 1,500-word document using the rule of thumb.
2. Explain why the 50th message in a chat costs more than the first (hint: the history is resent).
3. Change `temp_demo.py` to use temperatures 0.5 and 5.0. Describe what happens at the extremes.
4. Write 3 sentences on how you would test a feature whose model runs at a temperature above 0.
5. On paper, draw the context window as a box and fill it: system prompt, history, new message, space for the reply.
6. Stretch: explain why a bigger context window does not automatically give better answers.

## Interview questions

1. **What is a token?**
   A chunk of text the model reads and writes: a word, part of a word, punctuation or code. As a rough guide for English, one token is about four characters or three-quarters of a word.

2. **What is a context window?**
   The maximum number of tokens the model can handle at once, covering the system prompt, the conversation, any provided documents and the response being generated.

3. **Does an LLM remember previous conversations?**
   Not by itself. Each call starts fresh. Chat apps resend the earlier messages, and memory features store text and put it back into the context.

4. **What does temperature do?**
   It controls randomness when the next token is chosen. Low values favour the most likely tokens, giving more focused and repeatable output. Higher values give more variety but less reliability.

5. **Is output at temperature 0 fully deterministic?**
   Not guaranteed. It is much more repeatable, but small differences can still appear between runs, so tests should not rely on exact matches.

6. **How does an LLM generate a response?**
   It predicts a probability distribution over the next token, selects one, appends it to the text and repeats until it finishes.

7. **Why do cost and latency grow with context length?**
   Providers charge by tokens processed, and the model has more text to process on every call, so longer inputs cost more and take longer.

8. **What can you do when content exceeds the context window?**
   Shorten or summarise earlier content, split the task, retrieve only the relevant parts (RAG), or keep a running summary.

9. **The same prompt gives different answers. What does that mean for testing?**
   Output is probabilistic, so exact-match assertions are fragile. Use graded evaluations, repeated runs, pass-rate thresholds and checks on properties of the answer.

10. **Why should engineers care about tokens?**
    Tokens determine cost, speed and limits. They also drive design choices such as how to chunk documents for RAG and how much history to keep.

## My own words (fill in)

- One thing that surprised me:
- My 2-minute explanation:
- Flashcards added today:

## Review dates

Revisit on Day 7, Day 9, Day 13 and Day 27.
