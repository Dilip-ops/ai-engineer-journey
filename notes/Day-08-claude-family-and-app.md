# Day 8 (Mon Oct 19): The Claude Model Family and the Claude App

**Time:** about 3 hrs · **Goal:** know the Claude model lineup well enough to choose between models, and understand what the Claude app offers beyond a chat box.

## Revisit first (10 min)

Answer these without notes, then check `flashcards.md`:

1. What is the nesting from AI to LLM, and where do agents and MCP fit?
2. What are the three things an MCP server can expose?
3. INNER JOIN vs LEFT JOIN?
4. What is a Cartesian product, and how does it happen by accident?

## Schedule

| Block | Time | Task |
| --- | --- | --- |
| A | 45 min | Study the concepts below |
| B | 50 min | Hands-on in the Claude app (no code) |
| C | 30 min | Drill: SQL joins refresher (your Week 1 weak spot) |
| D | 30 min | Write your note, write your own flashcards, explain aloud for 2 min |
| E | 15 min | Check the official docs links at the bottom |

## Concepts

### Claude is a family of models

Anthropic offers several models that trade off speed, cost and capability. The current publicly available lineup (verified against the official Models overview on Oct 18, 2026):

| Model | API ID | Described as | Latency | Price per million tokens (input / output) |
| --- | --- | --- | --- | --- |
| Claude Fable 5.1 | `claude-fable-5-1` | Demanding reasoning and long-horizon agentic work | Slower | $10 / $50 |
| Claude Opus 5.5 | `claude-opus-5-5` | Long-running agentic coding and knowledge work | Moderate | $4 / $20 |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | Best combination of speed and intelligence | Fast | $2 / $10 |
| Claude Haiku 5.5 | `claude-haiku-5-5` | High-volume, latency-sensitive tasks: classification, extraction, routing | Fastest | From $0.10 / $0.50 |

All four list a 1M-token context window, up to 128K tokens of output, and support for tools, images and multiple languages. Thinking is adaptive on all of them.

**Model names, prices and limits change often.** Treat the table as a snapshot and always check the official Models overview before you build.

### How to choose a model

1. **Start with the task, not the hype.** What must the model do, how fast, at what volume?
2. **The docs suggest starting with Opus 5.5 for most workloads.** Move up to Fable 5.1 for demanding reasoning and long-horizon agent work, or when your evals on Opus at higher effort still fall short.
3. **Use Haiku for high-volume, simple, latency-sensitive jobs**, such as labelling thousands of test failures.
4. **Use Sonnet when you want a strong balance of speed and quality.**
5. **Let evals decide.** Run your own test set on two models and compare quality, cost and speed. This is where your QA skills matter, and it comes back in Week 9.

### Where you use Claude

| Place | What it is | Who it is for |
| --- | --- | --- |
| Claude app (web, desktop, mobile) | Chat and longer tasks that produce finished work | Everyone |
| Claude Code | Agentic coding from the terminal, web, desktop and mobile | Engineers |
| Claude API and Console | Build Claude into your own software | Developers |
| Cloud platforms | Claude is also offered through cloud providers (for example AWS and Google Cloud) | Teams that already run on those clouds |

### Features inside the Claude app

| Feature | What it does |
| --- | --- |
| **Projects** | A self-contained workspace with its own chats and uploaded knowledge, plus instructions. Available on all plans; free users can create up to 5 |
| **Artifacts** | Claude creates documents, pages, tools and other outputs you can open, keep and edit |
| **Connectors** | Link Claude to your own apps so it can use their data |
| **Skills** | Packaged instructions that teach Claude how to do a particular task well |
| **Web search, memory, past-chat search** | Features you can switch on or off in settings |

Which features you get depends on your plan, so check the support centre for your account. Do not assume.

### Key ideas

1. **Pick the model for the job.** A bigger model is not automatically better, and it costs more and is slower.
2. **Claude app, Claude Code and the API are different products** for different people.
3. **Projects give Claude persistent context** (instructions and files) for one purpose.
4. **Artifacts turn a chat answer into something you keep.**
5. **Verify product facts at the source.** Models and features change quickly.

## Hands-on (in the Claude app, no code)

1. **Compare models on one task.** Ask Claude to "write five test cases for a login page". If your plan lets you switch models, run it on two, and note differences in quality and speed.
2. **Create a Project** called "AI Engineer Prep". Add your Week 1 cheat sheet, add one instruction such as "Quiz me one question at a time on these notes, then correct me", and run a short quiz.
3. **Create an artifact.** Ask Claude to turn five of your flashcards into a small self-test page.
4. **Explore settings.** Look at which features are available on your plan (web search, memory, past-chat search). Switch on only what you are comfortable with, and write down what you found.

Write 3-4 lines in your note about what surprised you.

## Drill (30 min): SQL joins refresher

Use `tests.db` and `run_query.py` from Day 5. Predict each result first.

1. List every failed run with its module and owner.
2. Which owner has the most failed runs?
3. List modules that have no failed run (hint: think LEFT JOIN, or `NOT IN` with a subquery).
4. Show the average duration per module, including modules that have no runs.
5. In your own words: why does a `WHERE` filter on the right table turn a LEFT JOIN into an INNER JOIN?

Expected for drill 1: three rows (ids 2, 5 and 6), with owners Ravi, Asha and Ravi. Expected for drill 2: Ravi with 2.

## Interview questions

1. **What are the Claude model tiers, and how do they differ?**
   Claude is a family with models that trade off speed, cost and capability. Haiku is the fastest and cheapest, Sonnet balances speed and intelligence, Opus targets long-running agentic work, and Fable targets the most demanding reasoning. Names and versions change, so check the current docs.

2. **How do you choose between Haiku, Sonnet and Opus?**
   Start from the task. Use Haiku for high-volume, latency-sensitive work such as classification and routing, Sonnet for a balance, and Opus (or higher) for complex, long-running work. Then confirm with your own evals on cost, speed and quality.

3. **Why not always use the biggest model?**
   Larger models cost more and respond more slowly. For many tasks, a smaller model meets the quality bar at a fraction of the cost and latency.

4. **How would you compare two models fairly?**
   Build an evaluation set from realistic inputs, run both models on the same set with the same prompt, score the results with graders, and compare quality, cost and latency.

5. **What is the difference between the Claude app, Claude Code and the Claude API?**
   The app is for chat and longer tasks. Claude Code is an agentic coding tool for engineers. The API lets developers build Claude into their own products.

6. **What is a Claude Project?**
   A workspace that groups chats, uploaded knowledge and instructions around one purpose, so Claude has persistent context for that work.

7. **What are artifacts?**
   Outputs that Claude creates, such as documents, pages or small tools, that you can open, keep and edit, instead of leaving them as text inside a chat.

8. **What is the context window of the current Claude models?**
   The current models list a 1M-token context window, but you should check the model's page, because limits change between versions.

9. **Where can you access Claude besides Anthropic's own products?**
   Through major cloud platforms, for example AWS and Google Cloud, which matters for teams that keep their data and security on those clouds.

10. **Why must engineers verify model information at the source?**
    Model names, prices, limits and features change frequently, so memory and blog posts go stale. The official Models overview and API docs are the source of truth.

## Official links

- Models overview: https://platform.claude.com/docs/en/models/overview
- Choosing a model: https://platform.claude.com/docs/en/about-claude/models/choosing-a-model
- What are projects: https://support.claude.com/en/articles/9517075-what-are-projects

## My own words (fill in)

- One thing that surprised me:
- My 2-minute explanation:
- Flashcards I wrote myself today:

## Review dates

Revisit on Day 9, Day 11, Day 15 and Day 29.
