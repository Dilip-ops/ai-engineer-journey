import os
from fake_claude import FakeClient, FakeAuthenticationError

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


