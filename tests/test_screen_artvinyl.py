from __future__ import annotations

import unittest
from pathlib import Path

from research.screen_artvinyl import ArchiveParser, ROOT, require_external_output


class ArtVinylScreeningTest(unittest.TestCase):
    def test_archive_parser_extracts_credit_without_network(self) -> None:
        parser = ArchiveParser()
        parser.feed(
            """
            <div class="bestitem">
              <img src="https://example.test/cover.jpg">
              <h5>Artist</h5><p>Example Artist</p>
              <h5>Title</h5><p>Example Title</p>
              <h5>Label</h5><p>Example Label</p>
              <h5>Design</h5><p>Example Studio</p>
            </div>
            """
        )
        self.assertEqual(
            parser.items,
            [{
                "image_url": "https://example.test/cover.jpg",
                "artist": "Example Artist",
                "title": "Example Title",
                "label": "Example Label",
                "design": "Example Studio",
            }],
        )

    def test_output_inside_repository_is_rejected(self) -> None:
        with self.assertRaises(SystemExit):
            require_external_output(ROOT / "research" / "downloaded-covers")

    def test_external_output_is_resolved(self) -> None:
        external = Path("/tmp/album-cover-director-test-output")
        self.assertEqual(require_external_output(external), external.resolve())


if __name__ == "__main__":
    unittest.main()
