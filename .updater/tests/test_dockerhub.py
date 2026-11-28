import unittest
from unittest.mock import Mock

import requests

from version_checker import DockerHubChecker


def tag(name, digest):
    return {
        "name": name,
        "digest": digest,
        "images": [{}],
        "last_updated": "2026-09-24T23:12:50.559482Z",
    }


class DockerHubCheckerTests(unittest.TestCase):
    def checker(self, pages):
        checker = DockerHubChecker()
        checker.session = Mock()
        checker.session.get.side_effect = [Mock(json=Mock(return_value=p)) for p in pages]
        return checker

    def test_anchor_and_digest_aliases_across_pages(self):
        checker = self.checker([
            {"results": [tag("0.64.2", "stable")], "next": "page2"},
            {"results": [tag("develop", "dev")], "next": "page3"},
            {"results": [tag("latest", "stable"), tag("stable", "stable")], "next": "page4"},
        ])

        version = checker.get_latest_version("deluan/navidrome", label="latest")

        self.assertEqual(version.digest, "stable")
        self.assertEqual(version.tags, ["0.64.2", "latest", "stable"])
        self.assertEqual(checker.session.get.call_count, 3)

    def test_alias_on_second_page_when_anchor_is_on_first(self):
        checker = self.checker([
            {"results": [tag("latest", "stable")], "next": "page2"},
            {"results": [tag("0.64.2", "stable")], "next": "page3"},
        ])
        self.assertEqual(
            checker.get_latest_version("deluan/navidrome", label="latest").tags,
            ["0.64.2", "latest"],
        )

    def test_without_label_uses_newest_tag(self):
        checker = self.checker([
            {"results": [tag("newest", "new"), tag("old", "old")], "next": None},
        ])
        self.assertEqual(checker.get_latest_version("ubuntu").tags, ["newest"])

    def test_missing_anchor_still_fails(self):
        checker = self.checker([
            {"results": [tag("develop", "dev")], "next": "page2"},
            {"results": [tag("old", "old")], "next": None},
        ])
        with self.assertRaisesRegex(ValueError, "No tags matching label 'latest'"):
            checker.get_latest_version("deluan/navidrome", label="latest")

    def test_pagination_http_error_is_not_ignored(self):
        checker = self.checker([
            {"results": [tag("latest", "stable")], "next": "page2"},
        ])
        failed_response = Mock()
        failed_response.raise_for_status.side_effect = requests.HTTPError("unavailable")
        first_response = checker.session.get.side_effect
        checker.session.get.side_effect = [next(first_response), failed_response]
        with self.assertRaises(requests.HTTPError):
            checker.get_latest_version("deluan/navidrome", label="latest")


if __name__ == "__main__":
    unittest.main()
