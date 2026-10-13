import io
import json
import unittest
import urllib.error
from unittest.mock import patch
import refresh_threads_token as refresh


class RefreshTests(unittest.TestCase):
    def test_refresh_response(self):
        response = io.BytesIO(json.dumps({"access_token": "fixture", "expires_in": 5184000}).encode())
        with patch.object(refresh.urllib.request, "urlopen", return_value=response):
            self.assertEqual(refresh.refresh("original"), ("fixture", 5184000))

    def test_invalid_response(self):
        with patch.object(refresh.urllib.request, "urlopen", return_value=io.BytesIO(b'{}')):
            with self.assertRaisesRegex(RuntimeError, "invalid"):
                refresh.refresh("original")

    def test_http_errors_do_not_leak_tokens(self):
        error = urllib.error.HTTPError("https://example.org/?token=private", 400, "private", {}, None)
        with patch.object(refresh.urllib.request, "urlopen", side_effect=error):
            with self.assertRaises(RuntimeError) as caught:
                refresh.refresh("private")
        self.assertNotIn("private", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
