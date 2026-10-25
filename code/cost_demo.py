"""Day 13 (zero-cost): thinking blocks, token cost, model choice. No key, no network."""
from types import SimpleNamespace

# PLACEHOLDER prices in USD per million tokens. They are NOT real.
# Copy the current numbers from the pricing page before trusting any cost figure.
PRICES = {
    "small":  {"in": 1.0,  "out": 5.0},    # stands in for the cheap, fast model
    "medium": {"in": 3.0,  "out": 15.0},   # stands in for the everyday model
    "large":  {"in": 15.0, "out": 75.0},   # stands in for the top model
}


def fake_response(answer, thinking_tokens=0, in_tok=100, answer_tok=60):
    """Same SHAPE as a real reply when thinking is on: a thinking block, then text."""
    content = []
    if thinking_tokens:
        content.append(SimpleNamespace(type="thinking", thinking="(summary of reasoning)"))
    content.append(SimpleNamespace(type="text", text=answer))
    out_total = thinking_tokens + answer_tok          # thinking is billed as OUTPUT
    return SimpleNamespace(
        content=content,
        stop_reason="end_turn",
        usage=SimpleNamespace(
            input_tokens=in_tok,
            output_tokens=out_total,
            output_tokens_details=SimpleNamespace(thinking_tokens=thinking_tokens),
        ),
    )


def cost_usd(usage, tier):
    p = PRICES[tier]
    return usage.input_tokens / 1e6 * p["in"] + usage.output_tokens / 1e6 * p["out"]


def answer_text(response):
    """Return only the text blocks; skip thinking blocks."""
    return "".join(b.text for b in response.content if b.type == "text")


if __name__ == "__main__":
    plain = fake_response("Use a boundary value test.", thinking_tokens=0)
    deep  = fake_response("Use a boundary value test.", thinking_tokens=500)

    for name, r in [("no thinking", plain), ("with thinking", deep)]:
        u = r.usage
        print(f"{name:14} in={u.input_tokens} out={u.output_tokens} "
              f"thinking={u.output_tokens_details.thinking_tokens} "
              f"cost(medium)=${cost_usd(u, 'medium'):.5f}")
        print("  blocks:", [b.type for b in r.content], "| text:", answer_text(r))

    ratio = cost_usd(deep.usage, "medium") / cost_usd(plain.usage, "medium")
    print(f"thinking made this call {ratio:.1f}x more expensive")

    # 10,000 calls a month, same prompt, three tiers
    for tier in PRICES:
        print(f"10k calls on {tier}: ${cost_usd(plain.usage, tier) * 10_000:.2f}")