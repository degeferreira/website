import json
import unittest
from urllib.parse import urlsplit

from site_content import BASE_URL, ROOT


class DomainMigrationTests(unittest.TestCase):
    def test_canonical_domain(self):
        self.assertEqual(BASE_URL, "https://degeferreira.me/")
        self.assertEqual((ROOT / "static/CNAME").read_text().strip(), "degeferreira.me")

    def test_existing_social_records_keep_file_keys_and_targets(self):
        state = json.loads((ROOT / "data/social/syndication.json").read_text())
        self.assertTrue(state)
        for key, record in state.items():
            self.assertTrue(key.startswith("content/"))
            self.assertEqual(urlsplit(record["permalink"]).netloc, "degeferreira.me")
            self.assertTrue(record["targets"])
            for target in record["targets"].values():
                if target.get("url"):
                    self.assertNotEqual(urlsplit(target["url"]).netloc, "degeferreira.me")


if __name__ == "__main__":
    unittest.main()
