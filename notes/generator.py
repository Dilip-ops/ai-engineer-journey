"""Project 2: user story -> validated test cases.

Your job: replace every `raise NotImplementedError` so that `python -m unittest -v` passes.
Work in the order below and run the tests after each function.
"""
import json
import re

ALLOWED_PRIORITIES = {"P1", "P2", "P3"}
ALLOWED_TYPES = {"positive", "negative"}
MODEL = "claude-sonnet-5-5"   # confirm the current model ID in the docs

SYSTEM_PROMPT = ""   # TODO 1: write a short system prompt (role, rules WITH reasons, always include a negative case)


def build_prompt(story):
    """TODO 2: return (system_prompt, messages).

    - system_prompt is SYSTEM_PROMPT (it must NOT contain the story)
    - messages is [{"role": "user", "content": ...}] where content wraps the story in
      <user_story> tags and has <instructions> that ask for ONLY JSON inside <json> tags,
      with the exact shape:
      {"test_cases": [{"title": str, "steps": [str], "expected": str,
                       "priority": "P1"|"P2"|"P3", "type": "positive"|"negative"}]}
    """
    raise NotImplementedError


def extract_json(text):
    """TODO 3: return the text inside <json>...</json>; if there are no tags, return text.strip()."""
    raise NotImplementedError


def validate(data):
    """TODO 4: return data["test_cases"] if valid, else raise ValueError listing ALL problems.

    Rules: test_cases is a non-empty list; each case has a non-empty string title and expected,
    a non-empty list of steps, priority in ALLOWED_PRIORITIES, type in ALLOWED_TYPES;
    and at least one case has type "negative". Also reject data that is not a dict.
    """
    raise NotImplementedError


def generate_test_cases(client, story, max_retries=2, max_tokens=1500):
    """TODO 5: call client.messages.create(model=MODEL, max_tokens=..., system=..., messages=...).

    - If stop_reason == "max_tokens": raise ValueError immediately (do NOT retry).
    - Join only the text blocks of the reply, extract the JSON, json.loads it, validate it.
    - If parsing or validation fails: append the assistant reply and a user message that
      contains the error text and asks for corrected JSON, then try again.
    - Make at most max_retries + 1 calls in total; then raise ValueError.
    - On success return {"test_cases": [...], "usage": {"input_tokens": n, "output_tokens": n}}
      where usage is summed over ALL calls made.
    """
    raise NotImplementedError
