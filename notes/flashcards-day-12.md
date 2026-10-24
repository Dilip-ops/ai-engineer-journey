## Day 12: multi-turn chats, streaming, errors, rate limits

**Q:** How do you build a multi-turn chat on a stateless API?
**A:** Keep the message list in your code and resend all of it every call, appending each assistant reply and user message. Cost and latency grow with length, because input tokens grow.

**Q:** Where does the system prompt go in a multi-turn chat?
**A:** In the separate top-level `system` field, not in the message list; roles in `messages` alternate user and assistant.

**Q:** What does streaming improve, and when is it not worth it?
**A:** Time to first token, which makes chat UIs feel fast. Not worth it for batch jobs like evals, because nobody waits on partial text.

**Q:** Which HTTP errors should you retry?
**A:** 429, 5xx and network failures, with limited attempts. Not 400, 401, 403, 404, because the same bad request fails again.

**Q:** What is exponential backoff?
**A:** Waiting longer after each failure (1x, 2x, 4x the base delay) with a maximum number of tries, so you stop hammering a struggling service.

**Q:** Why add jitter?
**A:** Random extra delay spreads out clients that failed together, so they do not all retry at the same instant.

**Q:** How do you test retry logic without the real API?
**A:** A fake client that fails N times then succeeds, asserting call count and delays, and one call only for non-retryable errors.

**Q:** What are two ways to handle a conversation that has grown too long?
**A:** Trim old turns or summarize earlier history; which one depends on whether exact detail must be kept, because summaries lose detail.

**Q:** ROW_NUMBER with PARTITION BY ... ORDER BY ... DESC: what does `rn = 1` give you?
**A:** The most recent row per group, because rows are numbered newest first within each partition.
