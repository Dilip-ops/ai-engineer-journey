## Day 15: tool use (function calling), concepts

**Q:** What is tool use?
**A:** Claude asks your code to run a function (query a database, call an API) and uses the result in its answer. Your code runs it, never Claude.

**Q:** What does `stop_reason == "tool_use"` mean?
**A:** Claude is not finished; it needs you to run one or more tools and send back results.

**Q:** What are the parts of a tool definition?
**A:** `name`, `description` and `input_schema` (JSON Schema). The description matters most, because it is how Claude decides when to call the tool.

**Q:** What does a `tool_use` block contain?
**A:** An `id`, the tool `name` and an `input` object with the arguments.

**Q:** How do you return a tool result?
**A:** A `tool_result` block inside a user message, with `tool_use_id` equal to the request's id, so Claude can match result to request.

**Q:** What must you keep in the history for a tool round trip?
**A:** The assistant's tool-request reply, then the user message with the tool results, because the API is stateless.

**Q:** How do you report a tool failure to Claude?
**A:** Send a `tool_result` with `is_error: true` and the error text, so it can recover or explain, instead of crashing the conversation.

**Q:** Why dispatch through a registry and validate inputs?
**A:** Tool names and arguments from the model are untrusted input; only allowed functions should run, with checked arguments.

**Q:** Why cap the number of agent-loop turns?
**A:** A confused model could request tools forever, which costs money; the cap makes the loop fail loudly.

**Q:** Workflow versus agent?
**A:** In a workflow, code fixes the steps; in an agent, the model decides which tools to call and when to stop.

**Q:** Two Sum with a hash map: time and space?
**A:** O(n) time and O(n) space, because one pass with a dict lookup replaces the O(n^2) double loop.
