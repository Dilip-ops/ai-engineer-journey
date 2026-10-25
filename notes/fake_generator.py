"""Fake Claude client for Project 2. Returns canned replies in order and records every call."""
from types import SimpleNamespace

GOOD_REPLY = """<json>
{"test_cases": [
  {"title": "Apply a valid discount code", "steps": ["Add an item", "Enter SAVE10", "Click Apply"],
   "expected": "Total is reduced by 10 percent", "priority": "P1", "type": "positive"},
  {"title": "Apply an expired discount code", "steps": ["Add an item", "Enter OLD20", "Click Apply"],
   "expected": "An error says the code is expired", "priority": "P2", "type": "negative"}
]}
</json>"""


def reply(text, stop_reason="end_turn", in_tok=120, out_tok=80):
    return SimpleNamespace(
        content=[SimpleNamespace(type="text", text=text)],
        stop_reason=stop_reason,
        usage=SimpleNamespace(input_tokens=in_tok, output_tokens=out_tok),
    )


class _Messages:
    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = []                      # every kwargs dict passed to create()

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if not self.replies:
            raise RuntimeError("FakeGeneratorClient ran out of canned replies")
        return self.replies.pop(0)


class FakeGeneratorClient:
    def __init__(self, replies):
        self.messages = _Messages(replies)
