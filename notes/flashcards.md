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
