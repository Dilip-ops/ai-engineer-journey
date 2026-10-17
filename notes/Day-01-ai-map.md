# Day 1 (Sun Oct 11): The AI Map and Your Setup

**Time:** about 3 hrs · **Goal:** explain AI → ML → LLM → Agent → MCP in 2 minutes and have your tools ready.

## Schedule

| Block | Time | Task |
| --- | --- | --- |
| A | 45 min | Study the notes below |
| B | 60 min | Setup: Python, VS Code, Git, Jupyter, a GitHub repo, Obsidian, Anki |
| C | 30 min | Explore the Claude app with a few test questions about today's topic |
| D | 30 min | Write your note, make 5-8 Anki cards, explain aloud for 2 min, take the quiz |

## Notes

### The nesting

| Term | Meaning | Analogy |
| --- | --- | --- |
| AI | Machines doing tasks that seem intelligent | The whole hospital |
| Machine Learning | Learns patterns from data instead of hand-written rules | A doctor who learns from patients |
| Deep Learning | ML using many-layered neural networks | A specialist with deep training |
| LLM | A huge neural network trained on text to predict the next token | A doctor who has read every textbook |
| Claude | A family of LLMs from Anthropic | One well-known doctor |
| Agent | An LLM in a loop: plan, call tools, observe, repeat | The doctor who also orders tests and acts on results |
| MCP | Open standard for connecting AI apps to tools and data | The standard plug socket for medical equipment |

### Three ideas to remember

1. **Claude is the brain, the agent is the behavior, MCP is the plug socket, ML is the discipline underneath.**
2. **Workflow vs agent:** in a workflow, your code fixes the steps. In an agent, the model decides them. Agents are flexible but harder to test, which is your advantage.
3. **A model is not a product.** Real systems combine a model, tools, data, evals and guardrails.

## Setup checklist

- [ ] Python 3.11 or newer installed (`python --version`)
- [ ] VS Code, Git and Jupyter working
- [ ] GitHub account and a repo named `ai-engineer-journey` with a `notes/` folder
- [ ] Obsidian vault inside that repo
- [ ] Anki installed
- [ ] Today's note saved as `Day-01-ai-map.md`

## Interview questions

1. **What is the difference between AI, ML and deep learning?**
   AI is the broad goal of machines performing intelligent tasks. ML is a subset where systems learn patterns from data instead of following hand-written rules. Deep learning is ML using multi-layer neural networks.

2. **What is an LLM?**
   A large neural network, usually a transformer, trained on huge amounts of text to predict the next token. That simple objective gives it broad language ability.

3. **Is Claude the same as ChatGPT?**
   No. They are different model families from different companies (Anthropic and OpenAI). Both are LLM-based assistants, but they differ in training, behavior and tooling.

4. **What is generative AI?**
   Models that produce new content such as text, code or images. LLMs are the text and code branch of it.

5. **What is an AI agent?**
   An LLM in a loop that plans, calls tools, observes the results and continues toward a goal, with some autonomy over the steps.

6. **Workflow vs agent?**
   A workflow follows steps defined in code, so it is predictable. An agent decides its own steps, so it is flexible but harder to control and test. Use the simplest option that works.

7. **What is MCP?**
   The Model Context Protocol is an open standard that lets AI applications connect to tools, data and prompts through servers. It is plumbing and adds no intelligence itself.

8. **Are AI, ML, agents and MCP interchangeable?**
   No. They sit at different layers: the field, the technique, the behavior pattern and the connection standard.

9. **Why might a QA engineer be valuable in AI teams?**
   AI systems are non-deterministic and fail in subtle ways. Evals, regression testing, edge cases, release gates and flakiness are core QA skills, and production AI needs exactly them.

10. **Why is non-determinism a testing challenge?**
    The same input can produce different outputs, so exact-match assertions fail. You test with graded evals, repeated runs, thresholds and LLM-as-judge instead.

## My own words (fill in)

- One thing that surprised me:
- My 2-minute explanation, in my own words:
- Anki cards made today:

## Review dates

Revisit on Day 2, Day 4, Day 8 and Day 22.
