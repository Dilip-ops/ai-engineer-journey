"""Day 15 (zero-cost): the tool-use loop with a scripted fake model. No key, no network."""
import json
from types import SimpleNamespace

TOOLS = [
    {
        "name": "get_test_status",
        "description": (
            "Return the latest status (PASSED or FAILED) of one automated test. "
            "Use when the user asks whether a specific test passed or failed. "
            "Do not use it to list tests."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "test_name": {"type": "string", "description": "Exact test name, e.g. login_valid"}
            },
            "required": ["test_name"],
        },
    }
]

TEST_DB = {"login_valid": "PASSED", "checkout_discount": "FAILED"}


def get_test_status(test_name):
    if test_name not in TEST_DB:
        raise KeyError(f"unknown test: {test_name}")
    return {"test_name": test_name, "status": TEST_DB[test_name]}


REGISTRY = {"get_test_status": get_test_status}   # only functions listed here can ever run


# ---------- scripted fake model: same SHAPES as real replies ----------
def tool_use_reply(tool_name, tool_input, tool_id="toolu_fake_1"):
    return SimpleNamespace(
        stop_reason="tool_use",
        content=[SimpleNamespace(type="tool_use", id=tool_id, name=tool_name, input=tool_input)],
    )


def text_reply(text):
    return SimpleNamespace(stop_reason="end_turn", content=[SimpleNamespace(type="text", text=text)])


class _Messages:
    def __init__(self, replies):
        self.replies, self.calls = list(replies), []

    def create(self, **kwargs):
        self.calls.append({**kwargs, "messages": list(kwargs["messages"])})  # snapshot
        return self.replies.pop(0)


class FakeToolClient:
    def __init__(self, replies):
        self.messages = _Messages(replies)


# ---------- the loop YOU own ----------
def run_conversation(client, user_text, max_turns=5):
    messages = [{"role": "user", "content": user_text}]
    for _ in range(max_turns):
        response = client.messages.create(
            model="claude-sonnet-5-5", max_tokens=500, tools=TOOLS, messages=messages
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            return "".join(b.text for b in response.content if b.type == "text")

        results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            try:
                func = REGISTRY[block.name]          # unknown tool name -> KeyError
                output = func(**block.input)
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": json.dumps(output)})
            except Exception as exc:                 # report the error to the model, do not crash
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": f"Error: {exc}", "is_error": True})
        messages.append({"role": "user", "content": results})
    raise RuntimeError(f"No final answer after {max_turns} turns")


if __name__ == "__main__":
    # 1. happy path: model asks for a tool, we run it, model answers
    client = FakeToolClient([
        tool_use_reply("get_test_status", {"test_name": "checkout_discount"}),
        text_reply("checkout_discount is FAILED."),
    ])
    print(run_conversation(client, "Did checkout_discount pass?"))
    second_call_roles = [m["role"] for m in client.messages.calls[1]["messages"]]
    print("roles on 2nd call:", second_call_roles)
    print("tool_result sent back:", client.messages.calls[1]["messages"][-1]["content"])

    # 2. tool error is returned to the model, not raised
    client = FakeToolClient([
        tool_use_reply("get_test_status", {"test_name": "nope"}),
        text_reply("I could not find a test called nope."),
    ])
    print(run_conversation(client, "Did nope pass?"))
    print("error result:", client.messages.calls[1]["messages"][-1]["content"])

    # 3. runaway loop guard
    client = FakeToolClient([tool_use_reply("get_test_status", {"test_name": "login_valid"})] * 3)
    try:
        run_conversation(client, "loop forever", max_turns=3)
    except RuntimeError as exc:
        print("guard fired:", exc)
