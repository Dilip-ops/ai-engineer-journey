# Flashcards

Add 5-8 question and answer pairs per day. Cover the answer, say it aloud, then check.

## Day 1: The AI map

**Q:** What is the nesting from broadest to narrowest?

**A:** AI > Machine Learning > Deep Learning > LLM. Claude is an LLM family, an agent is an LLM in a loop, and MCP is the connection standard.

---

**Q:** What is the difference between a workflow and an agent?

**A:** In a workflow, code fixes the steps, so it is predictable and easy to test. In an agent, the model decides the steps, so it is flexible but harder to test.

---

**Q:** What is MCP, and what does it not do?

**A:** MCP is an open standard that connects AI apps to tools, data and prompt templates through servers. It adds no intelligence. The model still does the reasoning.

---

**Q:** What are the three things an MCP server can expose?

**A:** Tools (actions), resources (data) and prompts (reusable prompt templates).

---

**Q:** What is an AI agent?

**A:** An LLM in a loop that plans, calls tools, observes the results and continues toward a goal.

---

**Q:** One-line memory hook for the whole map?

**A:** Claude is the brain, the agent is the behavior, MCP is the plug socket, and ML is the discipline underneath.

---

**Q:** Why is non-determinism a testing challenge for AI?

**A:** The same input can give different outputs, so exact-match assertions fail. Use graded evals, repeated runs, thresholds and LLM-as-judge.

## Day 2: Python for Java developers

**Q:** What is a virtual environment, and why use one?

**A:** An isolated directory with its own Python packages, so each project has its own dependency versions and does not interfere with others.

---

**Q:** List vs tuple vs set vs dict?

**A:** List: ordered and mutable. Tuple: ordered and immutable. Set: unordered unique items. Dict: key-value pairs.

---

**Q:** What does `with open(...) as f` do?

**A:** It is a context manager that opens the file and guarantees it is closed, even if an error occurs.

---

**Q:** What does `if __name__ == "__main__":` do?

**A:** It runs the code only when the file is executed directly, not when it is imported as a module.

---

**Q:** Why are mutable default arguments dangerous?

**A:** A default like `def f(x=[])` is created once and shared across calls, so changes persist. Use `None` and create a new list inside the function.

---

**Q:** How do you check for null in Python?

**A:** Use `x is None`, not `x == None`.

## Day 3: Pandas basics

**Q:** DataFrame vs Series?

**A:** A DataFrame is a 2D table with named columns. A Series is a single column, a 1D labeled array.

---

**Q:** `loc` vs `iloc`?

**A:** `loc` selects by label (row labels and column names). `iloc` selects by integer position.

---

**Q:** How do you find missing values?

**A:** `df.isna().sum()` gives the count of missing values per column.

---

**Q:** How do you filter rows with two conditions?

**A:** Wrap each condition in parentheses and use `&` or `|`, for example `df[(df["a"] == 1) & (df["b"] == 2)]`. Do not use `and` or `or`.

---

**Q:** Why did my change to the DataFrame disappear?

**A:** Most pandas methods return a new object instead of changing the original. Assign the result back, for example `df = df.drop_duplicates()`.

---

**Q:** What do you check first when you load a dataset?

**A:** `shape`, `info()` and `head()`: the size, column types, missing counts and a sample of rows.

---

**Q:** Why does data cleaning matter for AI and ML?

**A:** Models learn from whatever data they get. Duplicates, missing values and inconsistent labels lead to unreliable results. Garbage in, garbage out.

## Day 4: SQL basics

**Q:** What is the difference between `WHERE` and `HAVING`?

**A:** `WHERE` filters individual rows before grouping. `HAVING` filters groups after aggregation, so it can use aggregate functions.

---

**Q:** In what order does a database process a SELECT query?

**A:** FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY, LIMIT.

---

**Q:** `COUNT(*)` vs `COUNT(column)`?

**A:** `COUNT(*)` counts all rows. `COUNT(column)` counts only rows where that column is not NULL.

---

**Q:** How do you check for NULL in SQL?

**A:** Use `IS NULL` or `IS NOT NULL`. `= NULL` is never true.

---

**Q:** Why pair `LIMIT` with `ORDER BY`?

**A:** Without an order, which rows come back is not guaranteed. Ordering makes "top N" meaningful.

---

**Q:** Can you use a SELECT alias in `WHERE`?

**A:** No, because `WHERE` runs before `SELECT`. You can use the alias in `ORDER BY`.

---

**Q:** Why does a QA engineer need SQL?

**A:** To verify data after tests, set up and clean test data, and investigate failures by querying the database directly.

## Day 5: SQL joins

**Q:** What is the difference between INNER JOIN and LEFT JOIN?

**A:** INNER JOIN keeps only rows with a match in both tables. LEFT JOIN keeps every row from the left table, with NULLs where the right table has no match.

---

**Q:** What are a primary key and a foreign key?

**A:** A primary key uniquely identifies each row in a table. A foreign key references another table's primary key.

---

**Q:** How do you find rows with no match in another table?

**A:** LEFT JOIN, then filter `right_table.key IS NULL`.

---

**Q:** What is a Cartesian product?

**A:** Every row of one table paired with every row of the other. It happens when a join has no `ON` condition or a wrong one.

---

**Q:** Why can a join return more rows than either table?

**A:** When one row matches several rows on the other side, you get one result row per match.

---

**Q:** `ON` vs `WHERE` in a LEFT JOIN?

**A:** A `WHERE` filter on the right table removes the NULL rows and turns the LEFT JOIN into an INNER JOIN. Put right-table filters in `ON`.

---

**Q:** Why count with `COUNT(r.id)` after a LEFT JOIN?

**A:** `COUNT(*)` counts the NULL-filled row as 1. `COUNT(r.id)` skips NULLs, so unmatched rows count as 0.

## Day 6: LLM basics

**Q:** How does an LLM generate text?

**A:** It predicts a probability for every possible next token, picks one, appends it and repeats, building the answer one token at a time.

---

**Q:** What is a token?

**A:** A chunk of text the model reads and writes: a word, part of a word, punctuation or code. In English, roughly four characters or three-quarters of a word.

---

**Q:** What is a context window?

**A:** The maximum number of tokens the model can handle at once: system prompt, conversation, documents and the response itself.

---

**Q:** Does an LLM remember earlier conversations on its own?

**A:** No. Each call starts fresh. Apps resend the history, and memory features put saved text back into the context.

---

**Q:** What does temperature do?

**A:** It controls randomness when the next token is chosen. Low is focused and repeatable, higher is more varied and less reliable.

---

**Q:** Is temperature 0 fully deterministic?

**A:** Not guaranteed. It is much more repeatable, but tests should not rely on exact matches.

---

**Q:** Why do longer contexts cost more?

**A:** Providers charge by tokens processed, and the model reprocesses the whole context on every call.

## Day 7: Project 1 and Week 1 review

**Q:** What does `pd.read_sql_query(sql, conn)` do?

**A:** It runs a SQL query on the database connection and returns the result as a DataFrame.

---

**Q:** How do you compute a pass rate in pandas?

**A:** The mean of a boolean column gives the fraction, for example `(df["status"] == "passed").mean() * 100`.

---

**Q:** Why write expected results before you run your code?

**A:** It turns "looks right" into a testable check and catches mistakes early.

---

**Q:** What is an error log for?

**A:** Recording each mistake with its root cause and fix, so you review patterns weekly instead of repeating them.

---

**Q:** Why keep functions separate from `main()` in a script?

**A:** Other files, such as tests, can import and call the functions without running the whole script. `if __name__ == "__main__":` stops `main()` from running on import.

## Day 8: Claude models and the Claude app

**Q:** How do the Claude model tiers differ?

**A:** They trade off speed, cost and capability. Haiku is fastest and cheapest, Sonnet balances speed and intelligence, Opus suits long-running agentic work, and Fable suits the most demanding reasoning.

---

**Q:** When would you pick Haiku?

**A:** For high-volume, latency-sensitive tasks such as classification, extraction and routing.

---

**Q:** How do you decide between models?

**A:** Start from the task, then run your own eval set on the candidates and compare quality, cost and latency.

---

**Q:** Why not always use the biggest model?

**A:** It costs more and responds more slowly. A smaller model often meets the quality bar for much less.

---

**Q:** Claude app vs Claude Code vs Claude API?

**A:** The app is for chat and longer tasks, Claude Code is an agentic coding tool for engineers, and the API lets developers build Claude into their own products.

---

**Q:** What is a Claude Project?

**A:** A workspace that groups chats, uploaded knowledge and instructions around one purpose, giving Claude persistent context for that work.

---

**Q:** Why check model details at the source?

**A:** Names, prices, limits and features change often, so memory and blog posts go stale. Use the official Models overview.

## Day 9: Prompt engineering I

**Q:** What are the five habits of a good prompt?

**A:** Be clear and direct, give context and the reason, show examples, assign a role, and ask for the format you want.

---

**Q:** What is few-shot (multishot) prompting?

**A:** Including a few examples of the desired output in the prompt so the model copies the pattern. Vary the examples so it does not over-copy one.

---

**Q:** System prompt vs user prompt?

**A:** The system prompt sets standing instructions, role and rules for the whole conversation. The user prompt is the request in each turn.

---

**Q:** How can a prompt reduce made-up answers?

**A:** Provide the source material, allow the model to say it does not know, and ask it to base the answer on the text. Still verify important claims.

---

**Q:** Why change one thing at a time when improving a prompt?

**A:** Otherwise you cannot tell which change helped or hurt, as when isolating variables in debugging.

---

**Q:** What is a CTE in SQL?

**A:** A named temporary result defined with `WITH ... AS` at the top of a query, then used like a table. It makes long queries readable.

---

**Q:** Is temperature 0 fully deterministic?

**A:** No. Output is much more repeatable, but small numerical differences can still change results, so test with graded checks and repeated runs.
