## Day 11: API key and first Messages API call

**Q:** How is the Claude API different from the Claude app?
**A:** The app is a finished product; the API lets your code control the model, system prompt, parameters and output, so it can be automated, tested and embedded. Billing is separate from the app plan.

**Q:** What does "stateless" mean for the Messages API?
**A:** The server remembers nothing between calls, so your code resends the conversation history every time, and token cost grows with its length.

**Q:** What are the main fields of a Messages API request?
**A:** `model`, `max_tokens` (required), `messages` (list of role and content), and optionally `system`.

**Q:** Why is `max_tokens` required, and what must you check afterwards?
**A:** It caps reply length, cost and latency. Check `stop_reason`: `max_tokens` means the answer was truncated, so parsing may break.

**Q:** Where does the system prompt go in the API?
**A:** In the top-level `system` field, not inside `messages`.

**Q:** Why is `response.content` a list?
**A:** It holds blocks of different types (text now, tool-use later), so check each block's `type` instead of assuming `content[0]` is text.

**Q:** How do you keep an API key safe?
**A:** Environment variable or secrets manager, never in code or git, `.env` in `.gitignore`, rotate at once if exposed, because anyone with the key can spend your credit.

**Q:** Which API errors do you retry and which not?
**A:** Retry rate limits, connection errors and server errors with backoff and a limit. Do not retry authentication or invalid-request errors; fix the cause instead.

**Q:** WHERE versus HAVING?
**A:** WHERE filters rows before grouping; HAVING filters groups after aggregation and can use aggregates.

**Q:** Filter a DataFrame on two conditions?
**A:** `df[(df["a"] > 1) & (df["b"] == "x")]`: `&` is element-wise and needs parentheses because it binds tighter than comparisons; `and` fails on a Series.

**Q:** Find and handle missing values in pandas?
**A:** `df.isna().sum()` to count per column; handle with `dropna()`, `fillna(value)` or flagging, depending on why they are missing.
