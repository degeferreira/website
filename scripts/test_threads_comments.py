import unittest
from unittest.mock import patch
import social_collect_comments as comments


class ThreadsCommentsTests(unittest.TestCase):
    def test_conversation_mapping(self):
        reply = {"username": "reader", "text": "Hello", "permalink": "https://www.threads.com/post/example", "timestamp": "2026-10-13T10:00:00Z"}
        with patch.dict(comments.os.environ, {"THREADS_ACCESS_TOKEN": "fixture"}), patch.object(comments, "get_json", return_value={"data": [reply]}) as get:
            result = comments.threads_replies({"id": "123"})
        self.assertEqual(result[0]["source"], "threads")
        self.assertEqual(result[0]["author"], "reader")
        self.assertIn("/123/conversation?", get.call_args.args[0])
        self.assertNotIn("fixture", get.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
