import unittest

from fake_generator import GOOD_REPLY, FakeGeneratorClient, reply
from generator import build_prompt, extract_json, generate_test_cases, validate

STORY = "As a shopper, I can apply one discount code at checkout so that I pay less."


class TestBuildPrompt(unittest.TestCase):
    def test_story_is_wrapped_in_tags_and_system_is_separate(self):
        system, messages = build_prompt(STORY)
        self.assertTrue(system.strip())
        self.assertEqual(messages[0]["role"], "user")
        self.assertIn("<user_story>", messages[0]["content"])
        self.assertIn(STORY, messages[0]["content"])
        self.assertNotIn(STORY, system)


class TestExtractJson(unittest.TestCase):
    def test_extracts_from_tags_and_falls_back_to_plain(self):
        self.assertEqual(extract_json('hi <json>{"a": 1}</json> bye'), '{"a": 1}')
        self.assertEqual(extract_json('  {"a": 1}  '), '{"a": 1}')


class TestValidate(unittest.TestCase):
    def good_case(self, **over):
        case = {"title": "t", "steps": ["s"], "expected": "e", "priority": "P1", "type": "negative"}
        case.update(over)
        return case

    def test_valid_data_passes(self):
        self.assertEqual(len(validate({"test_cases": [self.good_case()]})), 1)

    def test_rejects_bad_priority(self):
        with self.assertRaises(ValueError):
            validate({"test_cases": [self.good_case(priority="high")]})

    def test_rejects_empty_steps(self):
        with self.assertRaises(ValueError):
            validate({"test_cases": [self.good_case(steps=[])]})

    def test_requires_a_negative_case(self):
        with self.assertRaises(ValueError):
            validate({"test_cases": [self.good_case(type="positive")]})

    def test_rejects_empty_list_and_wrong_shape(self):
        with self.assertRaises(ValueError):
            validate({"test_cases": []})
        with self.assertRaises(ValueError):
            validate([])


class TestGenerate(unittest.TestCase):
    def test_happy_path(self):
        client = FakeGeneratorClient([reply(GOOD_REPLY)])
        result = generate_test_cases(client, STORY)
        self.assertEqual(len(result["test_cases"]), 2)
        self.assertEqual(len(client.messages.calls), 1)
        self.assertEqual(result["usage"]["input_tokens"], 120)

    def test_system_prompt_is_sent_separately(self):
        client = FakeGeneratorClient([reply(GOOD_REPLY)])
        generate_test_cases(client, STORY)
        call = client.messages.calls[0]
        self.assertIn("system", call)
        self.assertGreater(call["max_tokens"], 0)

    def test_repairs_after_invalid_json(self):
        client = FakeGeneratorClient([reply("<json>{not json}</json>"), reply(GOOD_REPLY)])
        result = generate_test_cases(client, STORY)
        self.assertEqual(len(client.messages.calls), 2)
        second_messages = client.messages.calls[1]["messages"]
        self.assertEqual([m["role"] for m in second_messages], ["user", "assistant", "user"])
        self.assertIn("invalid", second_messages[-1]["content"].lower())
        self.assertEqual(result["usage"]["input_tokens"], 240)   # both calls counted

    def test_gives_up_after_max_retries(self):
        bad = reply("<json>{not json}</json>")
        client = FakeGeneratorClient([bad, bad, bad])
        with self.assertRaises(ValueError):
            generate_test_cases(client, STORY, max_retries=2)
        self.assertEqual(len(client.messages.calls), 3)

    def test_truncated_reply_is_not_retried(self):
        client = FakeGeneratorClient([reply('<json>{"test_cases": [', stop_reason="max_tokens")])
        with self.assertRaises(ValueError):
            generate_test_cases(client, STORY)
        self.assertEqual(len(client.messages.calls), 1)


if __name__ == "__main__":
    unittest.main()
