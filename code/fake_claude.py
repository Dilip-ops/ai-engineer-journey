"""A fake Claude client with the same response SHAPE as the real Messages API.
No network, no key, no cost. Swap it for anthropic.Anthropic() on the day you have credit."""
from types import SimpleNamespace


class FakeAuthenticationError(Exception):
    """Stands in for anthropic.AuthenticationError (HTTP 401)."""


def _response(text, stop_reason="end_turn", in_tok=24, out_tok=None):
    out_tok = out_tok if out_tok is not None else len(text.split())
    return SimpleNamespace(
        id="msg_fake_001",
        type="message",
        role="assistant",
        model="claude-fake",
        content=[SimpleNamespace(type="text", text=text)],
        stop_reason=stop_reason,
        usage=SimpleNamespace(input_tokens=in_tok, output_tokens=out_tok),
    )


class _Messages:
    def __init__(self, api_key):
        self.api_key = api_key

    def create(self, *, model, max_tokens, messages, system=None, **kwargs):
        if not self.api_key:
            raise FakeAuthenticationError("401: missing or invalid API key")
        if max_tokens < 1 or not messages:
            raise ValueError("400: max_tokens must be >= 1 and messages non-empty")
        full = (
            "1. Empty username and password.\n"
            "2. Valid username with a wrong password.\n"
            "3. SQL injection string in the username field."
        )
        words = full.split()
        if max_tokens < len(words):  # crude: treat one word as one token
            return _response(" ".join(words[:max_tokens]), "max_tokens", out_tok=max_tokens)
        return _response(full)


class FakeClient:
    def __init__(self, api_key="fake-key"):
        self.messages = _Messages(api_key)


    def safe_text(message):
        # Check if the output was truncated because it reached the token limit.
        if getattr(message, "stop_reason", None) == "max_tokens":
            raise ValueError("Generation stopped: Maximum token limit reached.")

        # Join the text content from all text blocks in the message.
        text_content = "".join(
            block.text
            for block in message.content
            if getattr(block, "type", None) == "text"
        )
        return text_content


    