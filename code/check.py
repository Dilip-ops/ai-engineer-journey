import os
from types import SimpleNamespace  # FIX 1: Imported SimpleNamespace
from fake_claude import FakeClient, FakeAuthenticationError

# FIX 2: Added the safe_text implementation from Experiment 6
def safe_text(message):
    """
    Joins text blocks from the message and raises a ValueError 
    if the generation was cut off due to hitting max tokens.
    """
    if getattr(message, "stop_reason", None) == "max_tokens":
        raise ValueError("Generation stopped: Maximum token limit reached.")
        
    return "".join(
        block.text for block in message.content if getattr(block, "type", None) == "text"
    )


client = FakeClient(api_key=os.environ.get("FAKE_KEY", "fake-key"))

try:
    message = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=8,
        system="You are a QA assistant. Be concise.",
        messages=[{"role": "user", "content": "Give me 3 negative test cases for a login form."}],
    )
except FakeAuthenticationError as exc:
    raise SystemExit(f"Auth problem: {exc}")

for block in message.content:
    if block.type == "text":
        print(block.text)

print("stop_reason:", message.stop_reason)
print("tokens in/out:", message.usage.input_tokens, message.usage.output_tokens)
print(message.content)
if message.stop_reason == "max_tokens":
    print("WARNING: answer was cut off")


def test_safe_text():
    client = FakeClient()
    ok = client.messages.create(model="x", max_tokens=300,
                                messages=[{"role": "user", "content": "hi"}])
    assert "negative" not in safe_text(ok)  # it returns text without raising
    assert safe_text(ok).startswith("1.")

    cut = client.messages.create(model="x", max_tokens=8,
                                 messages=[{"role": "user", "content": "hi"}])
    try:
        safe_text(cut)
        assert False, "should have raised"
    except ValueError:
        pass

    empty = SimpleNamespace(stop_reason="end_turn", content=[])
    assert safe_text(empty) == ""   # change this if you add the no-text check

test_safe_text()
print("All checks passed")
