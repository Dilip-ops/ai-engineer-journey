# Day 9 (Mon Oct 19): Prompt Engineering I: Clarity, Examples, Roles

**Time:** about 2.5-3 hrs · **Goal:** write prompts that reliably get the output you want, and start your own prompt library.

## Revisit first (10 min)

Answer these without notes, then check `flashcards.md`:

1. Why use a virtual environment?
2. Why are mutable default arguments dangerous in Python?
3. Is temperature 0 fully deterministic? Why or why not?
4. What is a context window?
5. How do you choose between Haiku, Sonnet and Opus?

## Schedule

| Block | Time | Task |
| --- | --- | --- |
| A | 45 min | Study the concepts below |
| B | 50 min | Hands-on: prompt lab in the Claude app (no code) |
| C | 30 min | Drill: SQL CTEs (new this week) |
| D | 30 min | Write your note, write your own flashcards, explain aloud for 2 min |

## Concepts

A prompt is the instructions and context you give a model. **Claude cannot read your mind.** A good mental model: you are briefing a smart new colleague who knows nothing about your situation.

### The five habits

| Habit | What to do | Weak vs strong |
| --- | --- | --- |
| **Be clear and direct** | State the task, audience, format, length and constraints | "Write tests" vs "Write 5 test cases for a login page, as a table with steps and expected results" |
| **Give context and the reason** | Say what it is for, so Claude can make good choices | "This is for a regression suite run by a junior tester" |
| **Show examples** | Give 2-3 varied examples of the output you want (called few-shot or multishot) | One example of a test case in your exact format |
| **Assign a role** | Tell Claude who to act as, usually in the system prompt | "You are a senior QA engineer who writes precise, atomic test cases" |
| **Ask for the format you want** | Table, bullet list, JSON, word limit | "Return a Markdown table with the columns ID, Steps, Expected" |

### A reusable prompt template

```text
Role: You are a senior QA engineer.

Context: We are testing the login page of a banking web app. Users are
retail customers. The tests will be run manually by junior testers.

Task: Write test cases for the login page.

Format: A Markdown table with columns ID, Title, Steps, Expected result.

Constraints: Cover happy path, invalid input and security cases.
Maximum 8 test cases. Do not invent features that are not described.

Example:
| TC-01 | Valid login | 1. Open page 2. Enter valid user and password 3. Click Login | User lands on the dashboard |
```

### Tips that matter

1. **Say what to do, not only what to avoid.** "Write in plain sentences" works better than "don't use bullet points" alone.
2. **Examples are powerful and sticky.** Claude will copy their style. Vary them so it doesn't copy one example too closely.
3. **Put long documents first and the question last.** Mark them off clearly (XML tags arrive tomorrow).
4. **Allow "I don't know".** Telling Claude it may say it lacks information reduces made-up answers.
5. **Prompts are code.** Test them, version them, and change one thing at a time. This is where your QA habits fit perfectly.

### Key ideas

1. **A vague prompt gives a vague answer.** Detail is cheap, and rework is expensive.
2. **Context and examples do the most work.**
3. **A role focuses tone and behaviour.**
4. **Iterate and compare.** Keep what works in a library.
5. **Always check the output.** A good prompt reduces errors but does not remove them.

## Hands-on: prompt lab (in the Claude app)

Task: **generate test cases for a login page.** Create `notes/prompt-lab.md` and run five versions, one change at a time:

| Version | What you add |
| --- | --- |
| 1 | A one-line vague prompt: "Write test cases for login" |
| 2 | Add clear task, format and a limit |
| 3 | Add context (who it is for, what the app is) |
| 4 | Add a role |
| 5 | Add one example in your exact format |

Record this table in your note:

| Version | Change | Quality (1-5) | Why |
| --- | --- | --- | --- |
| 1 | | | |

Then answer in 3 lines: which change helped most, and did anything get worse?

**Start your prompt library.** Create `prompts/test-case-generator.md` with your best version, so you can reuse it on Day 14.

## Drill (30 min): SQL CTEs

A **CTE** (common table expression) is a named, temporary result you define with `WITH ... AS` at the top of a query, then use like a table. It makes long queries readable. Using `tests.db`:

```sql
WITH failed AS (
    SELECT test_name, COUNT(*) AS failures
    FROM test_runs
    WHERE status = 'failed'
    GROUP BY test_name
)
SELECT c.test_name, c.module, f.failures
FROM test_cases c
JOIN failed f ON c.test_name = f.test_name
```

Predict the result first. Expected: `checkout_test` (payments, 2) and `login_test` (auth, 1).

Exercises:
1. Rewrite your Day 5 drill 6 (runs per test, including zero) using a CTE called `run_counts`, then LEFT JOIN from `test_cases`.
2. Write a CTE that gives the average duration per test, then select the tests whose average is above 2 seconds.
3. Stretch: show tests whose average duration is above the **overall** average of all runs. (Expected: only `checkout_test`.)
4. In your own words: what is a CTE, and why use one?

## Interview questions

1. **What is prompt engineering?**
   Designing and refining the instructions and context given to a model so it produces reliable, useful output. It involves clarity, context, examples, format and iteration.

2. **Why does being specific help?**
   The model cannot see your intent or situation. Details about task, audience, format and constraints remove guesswork and reduce rework.

3. **What is few-shot (multishot) prompting?**
   Including a few examples of the desired input and output in the prompt, so the model copies the pattern. Use varied examples so it does not over-copy one.

4. **What does role prompting do?**
   Assigning a role, usually in the system prompt, focuses the model's tone, expertise and behaviour, for example "senior QA engineer".

5. **System prompt vs user prompt?**
   The system prompt sets standing instructions, role and rules for the whole conversation. The user prompt is the specific request in each turn.

6. **How can prompts reduce hallucination?**
   Give the source material, tell the model it may say it does not know, ask it to base answers on the provided text, and verify important claims.

7. **Prompting vs fine-tuning: when do you prefer prompting?**
   Prompting is faster, cheaper and easy to change, so try it first. Consider other approaches only when prompting and retrieval cannot reach the quality you need.

8. **How do you test a prompt?**
   Build a small set of realistic inputs with expected properties, run the prompt on all of them, score the results, change one thing at a time, and track changes like code.

9. **Why should you change one thing at a time when improving a prompt?**
   Otherwise you cannot tell which change helped or hurt. It is the same reasoning as isolating variables in debugging.

10. **How does a QA mindset help in prompt engineering?**
    You think in test cases, edge cases and regressions: build an input set, define pass criteria, catch prompt changes that break previously good behaviour, and keep a versioned library.

## Official links

- Prompt engineering overview: https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview
- Prompting best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices

Check these for current, model-specific guidance. Advice changes between model versions.

## My own words (fill in)

- One thing that surprised me:
- My 2-minute explanation:
- Flashcards I wrote myself today:

## Review dates

Revisit on Day 10, Day 12, Day 16 and Day 30.
