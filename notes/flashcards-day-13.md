## Day 13: thinking, choosing a model, cost basics

**Q:** What is adaptive thinking?
**A:** `thinking={"type": "adaptive"}` (plus optional `output_config={"effort": ...}`): Claude decides whether and how much to reason before answering. Used by current models; manual `budget_tokens` mode returns a 400 on the newest ones, so check the docs for your model.

**Q:** How are thinking tokens billed?
**A:** As output tokens, and they count toward `max_tokens`. `usage.output_tokens_details.thinking_tokens` shows how many.

**Q:** What new block type appears in `content` when thinking is on?
**A:** `thinking` blocks next to `text` blocks, so filter on `type` and never assume `content[0]` is the answer.

**Q:** When is thinking not worth it?
**A:** Simple tasks like classification, extraction and formatting, because it adds cost and latency without improving easy answers.

**Q:** How do you choose a Claude model?
**A:** Eval set from real inputs, run candidates, compare quality, cost and latency, take the cheapest that passes, because reputation does not guarantee fit.

**Q:** What is model routing?
**A:** Easy requests to a small model, hard ones to a larger one; saves cost but needs monitoring because bad routing silently lowers quality.

**Q:** Cost per call formula?
**A:** input tokens x input price + output tokens x output price; output is usually pricier, so long answers and thinking dominate.

**Q:** Name three ways to cut API cost.
**A:** Shorter prompts and answers, a smaller model, less thinking; later also prompt caching and batch processing.

**Q:** Why can adding thinking break a pipeline?
**A:** The response gains `thinking` blocks and thinking uses `max_tokens`, so `content[0].text` can fail and a small limit can truncate the answer.

**Q:** Share of output tokens that were thinking, in SQL?
**A:** `SUM(thinking_tokens) * 1.0 / SUM(output_tokens)` grouped by model; the `* 1.0` avoids integer division.
